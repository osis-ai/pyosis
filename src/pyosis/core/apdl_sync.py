"""通过 APDL 导出实现 OSIS → pyosis 主动同步。

流程:
    1. export .out
    2. 对比 MD5 与 {项目}/py/.apdl_sync.json
    3. 未变化 → 跳过 parse / 写 prep
    4. 有变化 → parse → 写 prep → 存本次 hash

用法:
    changed = engine.sync_apdl()
    if changed:
        print("命令流已变化,已写 prep")
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from ..transfer.out_to_python import write_prep_outputs

if TYPE_CHECKING:
    from .engine import OSISEngine

SYNC_STATE_FILE = ".apdl_sync.json"

# 默认 .out 文件名（位于项目根目录）
DEFAULT_EXPORT_NAME = "_pyosis_sync.out"

# 忽略 TIME: 行，避免时间戳导致 MD5 每次不同
_TIME_LINE_PATTERN = re.compile(
    r"^//-+ TIME:.*//\s*$",
    re.MULTILINE | re.IGNORECASE,
)


@dataclass
class ApdlSessionStore:
    """记录最近一次同步的 .out 路径与 hash（供调试/展示）。"""

    last_path: str = ""
    last_hash: str = ""

    def update_file(self, path: str, file_hash: str) -> None:
        self.last_path = path
        self.last_hash = file_hash


# 读取 .out 文件内容
def _read_out_text(path: Path) -> str:
    for encoding in ("gbk", "utf-8", "gb2312", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"无法解码 .out 文件: {path}")


# 忽略 TIME: 行，避免时间戳导致 MD5 每次不同
def _normalize_out_for_hash(text: str) -> str:
    return _TIME_LINE_PATTERN.sub("", text)


# 计算 .out 文件内容的 MD5
def _text_hash(text: str) -> str:
    return hashlib.md5(_normalize_out_for_hash(text).encode("utf-8")).hexdigest()


# 获取同步状态文件路径
def _sync_state_path(prep_dir: Path) -> Path:
    return prep_dir.parent / SYNC_STATE_FILE


# 加载持久化存储的 hash
def _load_persisted_hash(state_path: Path, out_path: Path) -> str:
    if not state_path.is_file():
        return ""
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        saved_out = Path(data.get("out_path", ""))
        if saved_out.resolve() == out_path.resolve():
            return str(data.get("file_hash", ""))
    except (OSError, json.JSONDecodeError, TypeError):
        pass
    return ""


# 保存持久化存储的 hash
def _save_persisted_hash(state_path: Path, out_path: Path, file_hash: str) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {"out_path": str(out_path), "file_hash": file_hash},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


# 解析项目目录
def _get_project_dir(engine: "OSISEngine") -> Path | None:
    try:
        proj_dir = engine.project.get_directory()
    except RuntimeError:
        return None
    if not proj_dir:
        return None
    return Path(proj_dir)


# 解析 (out_path, prep_dir)
def _resolve_project_paths(engine: "OSISEngine") -> tuple[Path, Path]:
    """返回 (默认 out_path, prep_dir)。prep_dir 不存在会自动创建。"""
    proj_dir = _get_project_dir(engine)
    if proj_dir is None:
        raise RuntimeError("无法获取 OSIS 项目目录")
    prep_dir = proj_dir / "py" / "prep"
    prep_dir.mkdir(parents=True, exist_ok=True)
    return proj_dir / DEFAULT_EXPORT_NAME, prep_dir


# 确保 .out 文件存在
def _ensure_out_file(
    engine: "OSISEngine",
    out_path: Path,
    *,
    force_export: bool,
) -> Path:
    """确保 .out 存在；不存在或 force_export 时调用 engine.export_apdl。"""
    if out_path.is_file() and not force_export:
        return out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"执行 export_apdl → {out_path}")
    engine.export_apdl(str(out_path))

    if not out_path.is_file() or out_path.stat().st_size == 0:
        raise FileNotFoundError(f"导出失败或未生成有效 .out 文件: {out_path}")

    return out_path


# 执行 APDL 同步
def perform_apdl_sync(
    engine: "OSISEngine",
    path: str | None = None,
    *,
    force_export: bool = False,
) -> bool | None:
    """执行 APDL 同步：export → 比 hash → 有变化则写 prep（不执行 prep）。

    Returns:
        True  - 命令流已变化,已写 prep
        False - 命令流未变化
        None  - 未获取到项目路径(无法同步)
    """
    if _get_project_dir(engine) is None:
        return None

    session: ApdlSessionStore = engine._apdl_session

    default_out, prep_dir = _resolve_project_paths(engine)
    out_path = Path(path) if path is not None else default_out
    out_path = _ensure_out_file(engine, out_path, force_export=force_export)

    text = _read_out_text(out_path)
    file_hash = _text_hash(text)

    state_path = _sync_state_path(prep_dir)
    last_hash = _load_persisted_hash(state_path, out_path)

    session.update_file(str(out_path), file_hash)

    if file_hash == last_hash:
        return False

    write_prep_outputs(out_path, prep_dir)

    # 未执行 prep，OSIS 未变
    _save_persisted_hash(state_path, out_path, file_hash)

    return True