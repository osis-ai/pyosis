"""transfer 同步链路的纯文本处理工具：把 .out 文本转换为 pyosis prep 模块。

只负责文本解析与 Python 代码生成：
    - 解析 OSIS 导出的命令流（parse_text）
    - 按模块分桶并生成 prep 模块（_1_control.py … _10_stage.py + main.py）

不负责：
    - .out 文件的获取（export_apdl） —— 由调用方管理
    - prep 模块的执行（import + builder 调用） —— 由调用方管理
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from pyosis.transfer.generator import generate_lines
from pyosis.transfer.parser import ParsedCommand

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
    doc = f"由 pyosis.transfer.out_to_python 从 .out 自动生成: {module}"
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
        '"""由 pyosis.transfer.out_to_python 自动生成：依次执行 prep 模块。"""',
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
    """写入 _0_engine.py 与 _1~_10 prep 模块 + main.py，返回 (代码行数, 文件路径列表)。

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