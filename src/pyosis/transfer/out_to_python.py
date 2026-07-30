"""transfer 同步链路的纯文本处理工具：把 .out 文本转换为 pyosis prep 模块。

只负责文本解析与 Python 代码生成:
    - 读 .out 源文件
    - 用 parser 解析出命令流,并按 //--- MODULE_NAME --- 标记分桶
    - 第一个模块标记之前的"前言"命令(典型为 clear/clc)写到 main.py
    - 每个模块的命令写到 _1_control.py … _10_stage.py

不负责:
    - .out 文件的获取（export_apdl） —— 由调用方管理
    - prep 模块的执行（import + builder 调用） —— 由 main.py 调度
"""

from __future__ import annotations

import inspect
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from pyosis.transfer.generator import generate_lines
from pyosis.transfer.parser import (
    BLANK_RE,
    COMMENT_LINE_RE,
    ParsedCommand,
    _parse_physical_line,
    iter_physical_lines,
    strip_inline_comment,
)

# 匹配链式调用中的 .get(...) 部分(如 engine.section.get("k").set_offset(...))
_CHAIN_GET_RE = re.compile(r"""\.get\((?:"[^"]*"|'[^']*'|[^()]*)\)""")

# .out 中模块标记行的正则: //----- CONTROL ----- 之类
MODULE_PATTERN = re.compile(r"^\s*//-+\s*(\w+)\s*-*")
# 已知的模块名(用于过滤 .out 中的非模块横线注释,例如 //--- VERSION: x.xx ---//)
KNOWN_MODULES = frozenset({
    "CONTROL",
    "PROPERTY",
    "MATERIAL",
    "SECTION",
    "NODE",
    "ELEMENT",
    "BOUNDARY",
    "LOADCASE",
    "ANALYSIS",
    "STAGE",
})

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


# 按模块分桶
def _split_by_module(text: str) -> tuple[list[ParsedCommand], dict[str, list[ParsedCommand]]]:
    """走一遍 .out 文本,把命令按 //--- MODULE_NAME --- 标记分桶。

    Returns:
        (preamble, {MODULE: [cmd, ...]})
        - preamble: 第一个模块标记之前的命令(典型为 clear/clc)
        - by_module: 每个模块的命令列表,按 .out 出现顺序
    """
    preamble: list[ParsedCommand] = []
    by_module: dict[str, list[ParsedCommand]] = defaultdict(list)
    current: str | None = None

    for line in iter_physical_lines(text):
        m = MODULE_PATTERN.match(line)
        if m:
            name = m.group(1).upper()
            current = name if name in KNOWN_MODULES else None
            continue
        if COMMENT_LINE_RE.match(line) or BLANK_RE.match(line):
            continue
        line = strip_inline_comment(line)
        if BLANK_RE.match(line):
            continue
        cmds = _parse_physical_line(line)
        if current is None:
            preamble.extend(cmds)
        else:
            by_module[current].extend(cmds)

    return preamble, dict(by_module)


# 读取 .out 文件内容(容错编码)
def _read_out_text(path: Path) -> str:
    for encoding in ("gbk", "utf-8", "gb2312", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"无法解码 .out 文件: {path}")


# ──────────────────────────────────────────────────────────────────────
# 方法 docstring 注释:在每个被调用方法的第一次出现处,插入其 docstring 第一行
# ──────────────────────────────────────────────────────────────────────

_ENGINE_INSTANCE: object | None = None


def _get_engine() -> object:
    """懒加载一个 OSISEngine 实例,只读属性,不会真正连 OSIS。"""
    global _ENGINE_INSTANCE
    if _ENGINE_INSTANCE is None:
        from pyosis.core.engine import OSISEngine
        _ENGINE_INSTANCE = OSISEngine()
    return _ENGINE_INSTANCE


def _strip_outer_args(line: str) -> str:
    """剥离最外层调用的实参列表,返回接收者表达式。

    取的是最后一个顶层 `(`,这样链式调用也能保留中间的 .get(...)。
    engine.control.set_gravity_acceleration(9.8)   → engine.control.set_gravity_acceleration
    engine.section.get(1).set_offset("Middle", 0) → engine.section.get(1).set_offset
    engine.matrix("M", [[1]])                      → engine.matrix
    """
    depth = 0
    last_paren = -1
    in_str = False
    sc: str | None = None
    for i, ch in enumerate(line):
        if in_str:
            if ch == sc and (i == 0 or line[i - 1] != "\\"):
                in_str = False
            continue
        if ch in ('"', "'"):
            in_str = True
            sc = ch
            continue
        if ch == "(":
            if depth == 0:
                last_paren = i
            depth += 1
        elif ch == ")":
            depth -= 1
    return line[:last_paren] if last_paren >= 0 else line


def _doc_first_line(doc: str | None) -> str:
    if not doc:
        return ""
    return doc.strip().split("\n", 1)[0].strip()


def _resolve_chain_target(head: str, engine: object) -> object | None:
    """从 'engine.X.method'(已折叠 .get)解析出真正的可调用对象。

    1) 直接 getattr 链:engine.section.create → SectionManager.create;engine.matrix → OSISEngine.matrix
    2) 链式调用:head 折叠后是 engine.section.set_offset(或嵌套的 engine.live.case.include),
       中间某一层管理器没有这个属性。从该层往前找带 .get 的管理器,用其返回类型注解
       (Section / LiveCase / TendonShape 等)找到方法本体。
    """
    parts = head.split(".")
    if len(parts) < 2 or parts[0] != "engine":
        return None

    # 1) 直接 getattr 链
    try:
        obj = engine
        for p in parts[1:]:
            obj = getattr(obj, p)
        if callable(obj):
            return obj
    except AttributeError:
        pass

    if len(parts) < 3:
        return None
    method_name = parts[-1]

    # 2) 从尾往头试每一层,看它是不是一个带 .get 的管理器
    for cut in range(len(parts) - 1, 1, -1):
        try:
            mgr_obj = engine
            for p in parts[1:cut]:
                mgr_obj = getattr(mgr_obj, p)
        except AttributeError:
            continue
        get_method = type(mgr_obj).__dict__.get("get")
        if get_method is None:
            continue
        try:
            sig = inspect.signature(get_method)
        except (ValueError, TypeError):
            continue
        ann = sig.return_annotation
        if ann is inspect.Parameter.empty:
            continue
        if isinstance(ann, str):
            mod = sys.modules.get(get_method.__module__)
            if mod is None:
                continue
            try:
                ann = eval(ann, vars(mod))
            except Exception:
                continue
        candidates: list[type] = []
        if isinstance(ann, type):
            candidates.append(ann)
        else:
            for arg in getattr(ann, "__args__", ()):
                if isinstance(arg, type):
                    candidates.append(arg)
                else:
                    for inner in getattr(arg, "__args__", ()):
                        if isinstance(inner, type):
                            candidates.append(inner)
        for cand in candidates:
            target = vars(cand).get(method_name)
            if target is not None and callable(target):
                return target
    return None


def _method_doc_for(line: str) -> str:
    """取这一行生成代码所调用方法的 docstring 第一行。非 engine 调用返空串。"""
    s = line.strip()
    if not s.startswith("engine."):
        return ""
    head = _CHAIN_GET_RE.sub("", _strip_outer_args(s))
    # head 形如 'engine.section.set_offset' 或 'engine.control.set_gravity_acceleration'
    target = _resolve_chain_target(head, _get_engine())
    if target is None:
        return ""
    return _doc_first_line(getattr(target, "__doc__", None))


def _insert_method_doc_comments(lines: list[str]) -> list[str]:
    """在每个被调用的独特方法的第一次出现处,插入一行 # <docstring 第一行>。"""
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        s = line.strip()
        if s.startswith("engine."):
            # 用与解析时相同的 head 作为去重键,保证多次调用同一方法只注一次
            head = _CHAIN_GET_RE.sub("", _strip_outer_args(s))
            if head not in seen:
                doc = _method_doc_for(line)
                if doc:
                    out.append(f"# {doc}")
                seen.add(head)
        out.append(line)
    return out


# 写入 prep 模块
def _write_prep_module(prep_dir: Path, module: str, lines: list[str]) -> Path:
    """写入 prep 模块；lines 为空时写 pass stub。

    生成顺序:
        1. docstring(说明模块职责)
        2. imports
        3. builder 函数
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
        doc = f"OSIS 命令流 {module} 模块 — {purpose}"
        annotated = _insert_method_doc_comments(lines)
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


def _iter_module_call_lines() -> Iterable[str]:
    """main.py 中依次调用各模块 builder 的语句(4 空格缩进)。"""
    for mod in MODULE_ORDER:
        yield f"    {MODULE_BUILDERS[mod]}(engine)"


def _write_main_py(prep_dir: Path, preamble_lines: list[str]) -> Path:
    """写入 main.py：先执行 preamble(典型为 clear/clc),再依次执行 _1.._10 builder。"""
    import_lines = [f"from {Path(MODULE_FILES[mod]).stem} import {MODULE_BUILDERS[mod]}" for mod in MODULE_ORDER]

    body_lines = [
        '"""main.py — 入口脚本,按 _1.._10 顺序依次执行 prep 模块。',
        "",
        "可直接 `python main.py`,或被 import 后调 main()。",
        "engine 用 _0_engine 模块级单例,跟同包内的 prep 模块保持一致。",
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
        "from _0_engine import engine",
        *import_lines,
        "",
        "def main() -> None:",
    ]
    for line in preamble_lines:
        body_lines.append(f"    {line}")
    body_lines.append("")
    body_lines.extend(_iter_module_call_lines())
    body_lines.extend([
        "",
        'if __name__ == "__main__":',
        "    main()",
        "",
    ])

    path = prep_dir / "main.py"
    path.write_text("\n".join(body_lines), encoding="utf-8")
    return path


def write_prep_outputs(out_path: Path, prep_dir: Path) -> tuple[int, list[Path]]:
    """读 .out 源文件,生成 _0_engine.py + _1~_10 prep 模块 + main.py,返回 (代码行数, 文件路径列表)。

    每个标准模块都会写入文件;.out 中无对应命令时生成 pass stub,避免遗留旧 prep。

    Args:
        out_path: 源 .out 文件路径(由 apdl_sync 管理获取,这里只读取)
        prep_dir: prep 输出目录(必须已存在)
    """
    text = _read_out_text(out_path)
    preamble, by_module = _split_by_module(text)

    code_line_count = 0
    prep_paths: list[Path] = []

    for module in MODULE_ORDER:
        cmds = by_module.get(module, [])
        lines = generate_lines(cmds) if cmds else []
        code_line_count += len(lines)
        prep_paths.append(_write_prep_module(prep_dir, module, lines))

    # 前言(典型 clear/clc)放到 main.py 顶部;无前言时为空列表
    preamble_lines = generate_lines(preamble) if preamble else []

    (prep_dir / "_0_engine.py").write_text(
        '"""模块级单例 OSISEngine,供同包内其他 prep 模块 import 使用。\n\n'
        "不要在主代码里直接 new OSISEngine();通过 main.py 调度。\n"
        '"""\n'
        "from pyosis.core.engine import OSISEngine\n\n"
        "engine = OSISEngine()\n",
        encoding="utf-8",
    )
    prep_paths.append(_write_main_py(prep_dir, preamble_lines))
    return code_line_count, prep_paths
