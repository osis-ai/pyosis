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


# 模块职责一句话(给 AI 看的提示)
MODULE_PURPOSE = {
    "CONTROL": "全局控制参数(重力、非线性、收缩徐变开关等)",
    "PROPERTY": "几何属性(坐标系、收缩徐变特性、钢束线型等)",
    "MATERIAL": "材料定义(混凝土、钢筋、钢绞线)",
    "SECTION": "截面定义(标准截面 + 加厚/变化截面)",
    "NODE": "节点坐标",
    "ELEMENT": "单元(梁/弹簧)创建 + 分组",
    "BOUNDARY": "边界条件(支座、约束自由度)",
    "LOADCASE": "荷载工况(自重、二期、预应力、温度、沉降)",
    "ANALYSIS": "分析设置(活载等级、车道)",
    "STAGE": "施工阶段(激活/钝化、体系转换)",
}


# 写 prep 模块时,按调用特征(method + 第一个 string 参数)分段,加注释
def _group_key(line: str) -> str | None:
    """提取一行的"分组键":method 链 + 第一个 string 参数。

    例:
        engine.load.get("防撞护栏右").create("LINE", ...) -> load.get+防撞护栏右
        engine.element.group.create("0号块单元", ...)      -> element.group.create+0号块单元
        engine.element.create(1, "BEAM3D", ...)            -> element.create+BEAM3D
        engine.control.set_gravity_acceleration(9.8)      -> control.set_gravity_acceleration+-

    无特征(如赋值)返 None。
    """
    s = line.strip()
    # 找第一个 '('
    i = s.find("(")
    if i < 0:
        return None
    # method 链 = 整行直到 "("
    method = s[:i]
    # 第一个 string 参数
    rest = s[i + 1:].lstrip()
    if not rest.startswith('"'):
        return None
    j = rest.find('"', 1)
    if j < 0:
        return None
    return f"{method}|{rest[1:j]}"


def _insert_group_comments(lines: list[str]) -> list[str]:
    """在 group key 变化处插入 `# ---- <method>: <name> ----` 注释。

    输入 lines 假设跟 generator 输出对齐(**每行无缩进**,已有 `engine.xxx` 前缀)。
    注释也保持无缩进,跟代码一致;最终由 `_write_prep_module` 统一加 def body 缩进。
    """
    out: list[str] = []
    prev_key: str | None = None
    for line in lines:
        key = _group_key(line)
        if key is not None and key != prev_key:
            method, name = key.split("|", 1)
            short = method.rsplit(".", 1)[-1]  # 最后一个方法名
            out.append(f"# ---- {short}: {name} ----")
        out.append(line)
        prev_key = key if key is not None else prev_key
    return out


# 写入 prep 模块
def _write_prep_module(prep_dir: Path, module: str, lines: list[str]) -> Path:
    """写入 prep 模块；lines 为空时写 pass stub。

    生成顺序:
        1. docstring(说明模块职责)
        2. imports
        3. builder 函数(按 group 加注释)
        4. if __name__ == "__main__": 单跑入口
    """
    fname = MODULE_FILES[module]
    builder = MODULE_BUILDERS[module]
    empty = not lines
    purpose = MODULE_PURPOSE.get(module, module)

    if empty:
        doc = f"OSIS 命令流 {module} 模块 — 当前 .out 中无该段,无需调用。"
        fn_body = ["    pass"]
    else:
        doc = (
            f"OSIS 命令流 {module} 模块 — {purpose}\n\n"
            f"由 pyosis.transfer.out_to_python 从 .out 自动生成。"
            f"按调用特征分组(注释头 # ---- method: name ----),同组相邻命令共享同一上下文。"
        )
        annotated = _insert_group_comments(lines)
        fn_body = [f"    {line}" for line in annotated]

    body_lines = [
        f'"""{doc}"""',
        "",
        "from __future__ import annotations",
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
        '"""main.py — 入口脚本,按 _1.._10 顺序依次执行 prep 模块。',
        "",
        "可单独跑(`python main.py`),也可被 import 后调 main(engine)。",
        "默认使用 _0_engine 模块级单例 OSISEngine,也可注入外部 engine。",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "import sys",
        "from pathlib import Path",
        "",
        "# 让 main.py 不管从哪个目录跑都能 import 同目录的 prep modules",
        "sys.path.insert(0, str(Path(__file__).resolve().parent))",
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
        '"""模块级单例 OSISEngine,供同包内其他 prep 模块 import 使用。\n\n'
        "不要在主代码里直接 new OSISEngine();通过 main.py 调度。\n"
        '"""\n'
        "from pyosis.core.engine import OSISEngine\n\n"
        "engine = OSISEngine()\n",
        encoding="utf-8",
    )
    prep_paths.append(_write_main_py(prep_dir))
    return code_line_count, prep_paths