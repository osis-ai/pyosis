"""命令流 → pyosis 代码生成器.

只有三类映射(详见 routes.py 的模块说明):
  - direct: engine.method(f0, f1, ...)
  - chain:  engine.get(fk).method(其余字段原序)
  - list:   前 n_head 个字段按位置传,其余聚合成一个 list

生成的调用一律使用位置实参: 第 N 个实参对应命令流第 N 个字段。
矩阵 *dim / 赋值由 MatrixAccumulator 合并为 engine.matrix(...)。
未注册命令 → engine.run("原始命令流")。
"""

from __future__ import annotations

from typing import List

from .matrix import MatrixAccumulator
from .parser import ParsedCommand
from .routes import CMD_ALIASES, ROUTES

_ROUTE_ALIASES = {
    "clear": "Clear",
    "clc": "Clc",
    # 5.0 文档/命令流里这些命令以全小写或不同大小写出现
    "combine": "Combine",
    "post": "Post",
    "combinesolve": "CombineSolve",
    "check": "Check",
    "checksolve": "CheckSolve",
    "cdpc": "CdPC",
}
_SKIP_COMMANDS = frozenset({"CalcSecProp"})


def _format_value(raw: str) -> str:
    s = raw.strip()
    if s == "":
        return '""'
    try:
        f = float(s)
        if f == int(f) and "e" not in s.lower() and "." not in s and "E" not in s:
            return str(int(f))
        return repr(f)
    except ValueError:
        pass
    if s.startswith('"') and s.endswith('"'):
        return s
    if s.startswith("'") and s.endswith("'"):
        return f'"{s[1:-1]}"'
    escaped = s.replace('"', '\\"')
    return f'"{escaped}"'


def _route_key(name: str) -> str:
    canonical = _ROUTE_ALIASES.get(name.lower(), name)
    return CMD_ALIASES.get(canonical, canonical)


def _fallback_run(cmd: ParsedCommand) -> str:
    """未注册命令(或字段不足)的兜底：用 engine.run("...") 包裹原始命令流。"""
    raw = cmd.source.replace("\\", "\\\\").replace('"', '\\"')
    return f'engine.run("{raw}")'


def _join_args(fields: list[str]) -> str:
    return ", ".join(_format_value(v) for v in fields)


def _render_route(cmd: ParsedCommand) -> str:
    """按 ROUTES 生成单行 Python 调用，无任何 per-command 特殊分支。"""
    route = ROUTES.get(_route_key(cmd.name))
    if route is None:
        return _fallback_run(cmd)

    fields = cmd.fields[1:]

    if isinstance(route, str):
        return f"{route}({_join_args(fields)})"

    if route[0] == "chain":
        _, get_path, method_name, key_index = route
        if key_index >= len(fields):
            return _fallback_run(cmd)
        key_field = _format_value(fields[key_index])
        rest = fields[:key_index] + fields[key_index + 1:]
        return f"{get_path}({key_field}).{method_name}({_join_args(rest)})"

    if route[0] == "list":
        _, target, n_head = route
        head, tail = fields[:n_head], fields[n_head:]
        tail_lit = "[" + _join_args(tail) + "]"
        head_args = _join_args(head)
        return f"{target}({head_args}, {tail_lit})" if head_args else f"{target}({tail_lit})"

    return _fallback_run(cmd)


def generate_lines(commands: List[ParsedCommand]) -> List[str]:
    """生成 Python 调用行；矩阵命令合并为 engine.matrix(...)。"""
    lines: List[str] = []
    accumulator = MatrixAccumulator()

    for cmd in commands:
        if cmd.name in _SKIP_COMMANDS:
            continue
        if cmd.kind == "matrix_dim":
            flushed = accumulator.flush()
            if flushed:
                lines.append(flushed)
            accumulator.on_dim(cmd.fields)
            continue

        if cmd.kind == "matrix_assign":
            accumulator.on_assign(cmd.matrix_name, cmd.matrix_indices, cmd.matrix_value)
            continue

        flushed = accumulator.flush()
        if flushed:
            lines.append(flushed)

        lines.append(_render_route(cmd))

    flushed = accumulator.flush()
    if flushed:
        lines.append(flushed)

    return lines


def generate(commands: List[ParsedCommand]) -> str:
    return "\n".join(generate_lines(commands)) + "\n"
