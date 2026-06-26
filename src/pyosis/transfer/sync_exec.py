"""transfer 同步链路的共享工具：路径解析、写 prep、执行 prep。

供 apdl_sync（export → 写 prep）与 sync_test（执行 prep）使用。

路径约定（与 build / apdl_sync 一致）:
    {项目目录}/_pyosis_sync.out
    {项目目录}/py/prep/_0_engine.py … _10_stage.py
"""

from __future__ import annotations

import importlib.util
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from pyosis.transfer.generator import generate_lines
from pyosis.transfer.parser import ParsedCommand

if TYPE_CHECKING:
    from pyosis.core.engine import OSISEngine

DEFAULT_EXPORT_NAME = "_pyosis_sync.out"

# 模块文件名
MODULE_FILES = {
    "CONTROL": "_1_control.py",
    "PROPERTY": "_2_property.py",
    "MATERIAL": "_3_material.py",
    "SECTION": "_4_section.py",
    "NODE": "_5_node.py",
    "ELEMENT": "_6_element.py",
    "BOUNDARY": "_7_boundary.py",
    "LOADCASE": "_8_loadcase.py",
    "ANALYSIS": "_9_analysis.py",
    "STAGE": "_10_stage.py",
}

# 模块生成函数名
MODULE_BUILDERS = {
    "CONTROL": "setup_control",
    "PROPERTY": "build_property",
    "MATERIAL": "build_materials",
    "SECTION": "build_sections",
    "NODE": "build_nodes",
    "ELEMENT": "build_elements",
    "BOUNDARY": "build_boundaries",
    "LOADCASE": "build_loadcases",
    "ANALYSIS": "build_analysis",
    "STAGE": "build_stages",
}

MODULE_ORDER = tuple(MODULE_FILES.keys())


@dataclass
class ExecResult:
    index: int
    line: str
    ok: bool
    error: str

# 获取项目目录
def get_project_dir_optional(engine: OSISEngine) -> Path | None:
    try:
        proj_dir = engine.project.get_directory()
    except RuntimeError:
        return None
    if not proj_dir:
        return None
    return Path(proj_dir)


# 解析项目路径
def resolve_project_paths(engine: OSISEngine) -> tuple[Path, Path]:
    """返回 (out_path, prep_dir)。"""
    proj_dir = get_project_dir_optional(engine)
    if proj_dir is None:
        raise RuntimeError("无法获取 OSIS 项目目录")
    prep_dir = proj_dir / "py" / "prep"
    prep_dir.mkdir(parents=True, exist_ok=True)
    return proj_dir / DEFAULT_EXPORT_NAME, prep_dir


# 解析 .out 文件
def resolve_out_file(
    engine: OSISEngine,
    out_path: Path,
    *,
    force_export: bool = False,
) -> Path:
    """确保 .out 存在；不存在或 force_export 时 export_apdl。"""
    if out_path.is_file() and not force_export:
        return out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"执行 export_apdl → {out_path}")
    engine.export_apdl(str(out_path))

    if not out_path.is_file() or out_path.stat().st_size == 0:
        raise FileNotFoundError(f"导出失败或未生成有效 .out 文件: {out_path}")

    return out_path


# 按模块分桶
def _bucket_by_module(parsed: list[ParsedCommand]) -> dict[str, list[ParsedCommand]]:
    buckets: dict[str, list[ParsedCommand]] = defaultdict(list)
    for cmd in parsed:
        buckets[cmd.module or "PREAMBLE"].append(cmd)
    return buckets


# 合并 preamble 到 control
def _merge_preamble_into_control(
    buckets: dict[str, list[ParsedCommand]],
) -> dict[str, list[ParsedCommand]]:
    if "PREAMBLE" not in buckets:
        return buckets
    merged = dict(buckets)
    preamble = merged.pop("PREAMBLE")
    merged.setdefault("CONTROL", [])
    merged["CONTROL"] = preamble + merged["CONTROL"]
    return merged


# 写入 prep 模块
def _write_prep_module(prep_dir: Path, module: str, lines: list[str]) -> Path:
    """写入 prep 模块；lines 为空时写 pass stub。"""
    fname = MODULE_FILES[module]
    builder = MODULE_BUILDERS[module]
    empty = not lines
    doc = f"由 pyosis.transfer.sync_exec 从 .out 自动生成: {module}"
    if empty:
        doc += "（无命令）"

    fn_body = ["    pass"] if empty else [f"    {line}" for line in lines]
    body_lines = [
        f'"""{doc}"""',
        "",
        "from pyosis.core.engine import OSISEngine",
        "",
        f"def {builder}(engine: OSISEngine) -> None:",
        *fn_body,
        "",
        'if __name__ == "__main__":',
        "    from _0_engine import engine",
        f"    {builder}(engine)",
        "",
    ]
    path = prep_dir / fname
    path.write_text("\n".join(body_lines), encoding="utf-8")
    return path

def _write_main_py(prep_dir: Path) -> Path:
    """写入 main.py：依次执行 _1_control … _10_stage。"""
    import_lines = [
        f"from {Path(fname).stem} import {MODULE_BUILDERS[mod]}"
        for mod in MODULE_ORDER
        for fname in [MODULE_FILES[mod]]
    ]
    call_lines = [f"    {MODULE_BUILDERS[mod]}(eng)" for mod in MODULE_ORDER]

    body_lines = [
        '"""由 pyosis.transfer.sync_exec 自动生成：依次执行 prep 模块。"""',
        "",
        "from __future__ import annotations",
        "",
        "from _0_engine import engine as default_engine",
        *import_lines,
        "",
        "def main(engine=None) -> None:",
        "    eng = default_engine if engine is None else engine",
        *call_lines,
        "",
        'if __name__ == "__main__":',
        "    main()",
        "",
    ]
    path = prep_dir / "main.py"
    path.write_text("\n".join(body_lines), encoding="utf-8")
    return path

def write_prep_outputs(parsed: list[ParsedCommand], prep_dir: Path) -> tuple[int, list[Path]]:
    """写入 _0_engine.py 与 _1~_10 prep 模块，返回 (代码行数, 文件列表)。

    每个标准模块都会写入文件；.out 中无对应命令时生成 pass stub，避免遗留旧 prep。
    """
    code_line_count = 0
    prep_paths: list[Path] = []
    buckets = _merge_preamble_into_control(_bucket_by_module(parsed))

    for module in MODULE_ORDER:
        cmds = buckets.get(module, [])
        lines = generate_lines(cmds) if cmds else []
        code_line_count += len(lines)
        prep_paths.append(_write_prep_module(prep_dir, module, lines))

    (prep_dir / "_0_engine.py").write_text(
        "from pyosis.core.engine import OSISEngine\n\n"
        "engine = OSISEngine()\n",
        encoding="utf-8",
    )
    prep_paths.append(_write_main_py(prep_dir))
    return code_line_count, prep_paths


# 加载 prep 模块
def _load_prep_module(prep_dir: Path, filename: str):
    path = prep_dir / filename
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


# 执行 prep 模块
def execute_prep_modules(prep_dir: Path, engine: OSISEngine) -> list[ExecResult]:
    """按 _1_control … _10_stage 顺序执行 prep 模块。"""
    prep_dir = prep_dir.resolve()
    if str(prep_dir) not in sys.path:
        sys.path.insert(0, str(prep_dir))

    results: list[ExecResult] = []
    step = 0

    for module in MODULE_ORDER:
        fname = MODULE_FILES[module]
        builder_name = MODULE_BUILDERS[module]
        mod = _load_prep_module(prep_dir, fname)
        if mod is None:
            print(f"[SKIP] {fname} 不存在")
            continue
        builder = getattr(mod, builder_name, None)
        if builder is None:
            print(f"[SKIP] {fname} 无函数 {builder_name}")
            continue

        step += 1
        desc = f"{fname} → {builder_name}(engine)"
        try:
            builder(engine)
            results.append(ExecResult(step, desc, True, ""))
            print(f"[OK] {step}: {desc}")
        except Exception as exc:
            msg = str(exc)
            results.append(ExecResult(step, desc, False, msg))
            print(f"[FAIL] {step}: {desc}")
            print(f"       {msg}")

    return results
