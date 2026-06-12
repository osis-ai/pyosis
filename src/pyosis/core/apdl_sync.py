"""通过 APDL 导出实现 OSIS → pyosis 主动同步。

针对真实 .out 格式：
  - 模块标记: //----------------------------- SECTION ---------------------------->>
  - 多行命令: Spline3D,... 续行缩进参数
  - 模块名与 pyosis 域不一致: PROPERTY 里含 ShellThk、Spline3D

用法:
    report = engine.sync_apdl(domains=["section", "geometry"])
    print(report.summary())
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from ..transfer.parser import parse_text as _parse_text, ParsedCommand

if TYPE_CHECKING:
    from .engine import OSISEngine


# ── 命令名 → pyosis 同步域（跨 .out 模块扫描）────────────────

CMD_TO_DOMAIN: dict[str, str] = {
    # control（一般不做 sync 统计，可按需开启）
    "Acel": "control",
    "CalcTendon": "control",
    "NL": "control",
    "ModOpt": "control",
    # geometry（在 .out 的 PROPERTY 段里）
    "Spline3D": "geometry",
    # thickness（在 .out 的 PROPERTY 段里）
    "ShellThk": "thickness",
    # property
    "CrpShrk": "creep_shrink",
    "Damp": "damping",
    "CoorSys": "coordinate",
    # material
    "Material": "material",
    # section
    "Section": "section",
    # node / element
    "Node": "node",
    "Element": "element",
    "Beam3D": "element",
    "Truss": "element",
    "Spring": "element",
    "Cable": "element",
    "Shell": "element",
    # boundary
    "Boundary": "boundary",
    "BdGrp": "boundary",
    # load / tendon
    "LoadCase": "loadcase",
    "Load": "loadcase",
    "TendonProp": "tendon_prop",
    "TendonShape": "tendon_shape",
    # stage
    "Stage": "stage",
}

# 删除/修改类命令，不计入「实体数量」
_SKIP_CMDS = {
    "SectionDel", "SectionMod", "NodeDel", "NodeMod", "ElementDel", "ElementMod",
    "MaterialDel", "MaterialMod", "ShellThkDel", "ShellThkMod",
    "Spline3DDel", "CrpShrkDel", "LoadCaseDel", "TendonPropDel", "TendonShapeDel",
}

DEFAULT_APDL_DOMAINS = sorted(set(CMD_TO_DOMAIN.values()))

# build 生成代码输出到「项目目录/py/」
BUILD_OUTPUT_SUBDIR = "py"

@dataclass
class ApdlDomainResult:
    """APDL 同步域结果"""
    domain: str
    synced: bool = False
    count_before: int = 0
    count_after: int = 0
    commands: list[ParsedCommand] = field(default_factory=list)

    @property
    def delta(self) -> int:
        return self.count_after - self.count_before

    @property
    def changed(self) -> bool:
        return self.delta != 0


@dataclass
class ApdlSyncResult:
    """APDL 同步结果"""
    export_path: str
    file_hash: str = ""
    exported_at: float = 0.0
    changed: bool = False
    domains: dict[str, ApdlDomainResult] = field(default_factory=dict)
    modules: dict[str, list[ParsedCommand]] = field(default_factory=dict)
    module_stats: dict[str, int] = field(default_factory=dict)

    def summary(self) -> str:
        """同步结果摘要"""
        parts: list[str] = []
        for name in sorted(self.domains.keys()):
            r = self.domains[name]
            if not r.synced:
                continue
            if r.delta != 0:
                parts.append(f"{name}: {r.count_before}→{r.count_after} ({r.delta:+d})")
            else:
                parts.append(f"{name}: {r.count_after}")
        return "; ".join(parts) if parts else "已同步，数量无变化"

    def get_commands(self, domain: str) -> list[ParsedCommand]:
        """获取指定域的命令"""
        if domain not in self.domains:
            return []
        return self.domains[domain].commands


class ApdlSessionStore:
    """APDL 会话存储"""
    def __init__(self) -> None:
        """初始化 APDL 会话存储"""
        self.counts: dict[str, int] = {}
        self.last_path: str = ""
        self.last_hash: str = ""
    
    def get_count(self, domain: str) -> int | None:
        """获取指定域的命令数量"""
        return self.counts.get(domain)

    def set_count(self, domain: str, count: int) -> None:
        """设置指定域的命令数量"""
        self.counts[domain] = count

    def update_file(self, path: str, file_hash: str) -> None:
        """更新文件路径和文件哈希"""
        self.last_path = path
        self.last_hash = file_hash


# ── 多行命令预处理 ────────────────────────────


def merge_multiline_commands(text: str) -> str:
    """把 OSIS.out 里的多行命令合并成单行，便于 CommandParser 解析。

    例如:
        Spline3D,name,ARC3D,TENDON,
            1.5,0.0,-0.75,0.0,
            ...;
    合并为:
        Spline3D,name,ARC3D,TENDON,1.5,0.0,-0.75,0.0,...;
    """
    merged: list[str] = []
    buffer = ""
    """把 OSIS.out 里的多行命令合并成单行，便于 CommandParser 解析。"""
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            if buffer:
                merged.append(buffer)
                buffer = ""
            continue

        # 模块标记、注释行原样保留
        if stripped.startswith("//"):
            if buffer:
                merged.append(buffer)
                buffer = ""
            merged.append(stripped)
            continue

        if buffer:
            # 续行：去掉首尾空白直接拼接
            buffer += stripped
        else:
            buffer = stripped

        if stripped.endswith(";"):
            merged.append(buffer)
            buffer = ""

    if buffer:
        merged.append(buffer)

    return "\n".join(merged)


# ── 解析与统计 ────────────────────────────────


def _default_export_path(engine: "OSISEngine") -> str:
    proj_dir = engine.project.get_directory()
    if not proj_dir:
        raise RuntimeError("无法获取 OSIS 项目目录。")
    base = Path(proj_dir)
    if not base.is_dir():
        raise RuntimeError(f"项目目录不存在或无效: {proj_dir}")
    return str(base / "_pyosis_sync.out")

def _resolve_build_output_dir(engine: "OSISEngine") -> str:
    """解析 build 输出目录：项目目录下的 py/ 文件夹。"""
    proj_dir = engine.project.get_directory()
    if not proj_dir:
        raise RuntimeError(
            "无法获取 OSIS 项目目录。"
        )
    base = Path(proj_dir)
    if not base.is_dir():
        raise RuntimeError(f"项目目录不存在或无效: {proj_dir}")
    out = base / BUILD_OUTPUT_SUBDIR
    out.mkdir(parents=True, exist_ok=True)
    return str(out)


def _run_build_from_apdl(export_path: str, output_dir: str) -> None:
    """MD5 变化后，根据导出文件生成 Python 代码到 output_dir。"""
    from .build import build_project
    build_project(export_path, output_dir)

def _run_generated_main(output_dir: str) -> None:
    """在 py/ 目录下执行 build 生成的 main.py。"""
    main_py = Path(output_dir) / "main.py"
    if not main_py.is_file():
        raise FileNotFoundError(f"未找到生成的 main.py: {main_py}")

    # 让生成的代码能 import pyosis（开发态：src 在 PYTHONPATH）
    src_root = Path(__file__).resolve().parent.parent.parent  # .../src
    env = os.environ.copy()
    prefix = str(src_root)
    env["PYTHONPATH"] = prefix + os.pathsep + env.get("PYTHONPATH", "")

    subprocess.run(
        [sys.executable, str(main_py)],
        cwd=output_dir,
        env=env,
        check=True,
    )

def _file_hash(path: Path) -> str:
    """获取文件的哈希值"""
    return hashlib.md5(path.read_bytes()).hexdigest()


def _classify_command(cmd: ParsedCommand) -> str | None:
    """根据命令名分类到 pyosis 域"""
    if cmd.name in _SKIP_CMDS:
        return None
    return CMD_TO_DOMAIN.get(cmd.name)


def _collect_by_domain(
    modules: dict[str, list[ParsedCommand]],
) -> dict[str, list[ParsedCommand]]:
    """跨所有 .out 模块，按命令名归类到 pyosis 域"""
    buckets: dict[str, list[ParsedCommand]] = {}
    for cmds in modules.values():
        for cmd in cmds:
            domain = _classify_command(cmd)
            if domain is None:
                continue
            buckets.setdefault(domain, []).append(cmd)
    return buckets


def parse_apdl_file(path: str | Path) -> list[ParsedCommand]:
    """读取 .out → 合并多行 → 解析"""
    path = Path(path)
    content = None
    for encoding in ("utf-8", "gbk", "gb2312", "gb18030", "latin-1"):
        try:
            content = path.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    if content is None:
        raise ValueError(f"无法读取文件: {path}")

    merged = merge_multiline_commands(content)
    return _parse_text(merged)


def perform_apdl_sync(
    engine: "OSISEngine", 
    path: str | None = None, # APDL 文件路径
    *,
    parse_only: bool = False, # 只解析不导出
    force: bool = False, # 强制同步
):
    """执行 APDL 同步"""
    export_path = path or _default_export_path(engine)
    path_obj = Path(export_path)
    session: ApdlSessionStore = engine._apdl_session

    if not parse_only:
        engine.export_apdl(export_path)

    if not path_obj.is_file():
        raise FileNotFoundError(f"APDL 文件不存在: {export_path}")

    file_hash = _file_hash(path_obj)

    if not force and file_hash == session.last_hash:
        return
        # return ApdlSyncResult(
        #     export_path=export_path,
        #     file_hash=file_hash,
        #     exported_at=time.time(),
        #     changed=False,
        # )

    # modules = parse_apdl_file(path_obj)
    # by_domain = _collect_by_domain(modules)
    #
    # target_domains = domains or DEFAULT_APDL_DOMAINS
    # result = ApdlSyncResult(
    #     export_path=export_path,
    #     file_hash=file_hash,
    #     exported_at=time.time(),
    #     modules=modules,
    #     module_stats={k: len(v) for k, v in modules.items()},
    # )
    #
    # any_changed = False
    # for domain in target_domains:
    #     commands = by_domain.get(domain, [])
    #     count_after = len(commands)
    #     count_before = session.get_count(domain)
    #     if count_before is None:
    #         count_before = 0
    #
    #     dr = ApdlDomainResult(
    #         domain=domain,
    #         synced=True,
    #         count_before=count_before,
    #         count_after=count_after,
    #         commands=commands,
    #     )
    #     result.domains[domain] = dr
    #     session.set_count(domain, count_after)
    #
    #     if count_before != count_after:
    #         any_changed = True
    #
    # result.changed = any_changed or (session.last_hash != "" and file_hash != session.last_hash)
    # session.update_file(export_path, file_hash)

    # MD5 相对上次已变化
    output_dir = _resolve_build_output_dir(engine)
    _run_build_from_apdl(export_path, output_dir)
    session.update_file(export_path, file_hash)
    _run_generated_main(output_dir)

    # return result