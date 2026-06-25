"""命令流 → pyosis 代码生成器.

所有普通命令经 routes.ROUTES 透传:
  - direct: engine.method(args...)
  - chain:  engine.get(key).method(reordered args...)

矩阵 *dim / 赋值仍由 MatrixAccumulator 合并为 engine.matrix(...)。
未注册命令 → engine.run("原始命令流")。
"""

from __future__ import annotations

from typing import List

from .matrix import MatrixAccumulator
from .parser import ParsedCommand
from .routes import ROUTES

_ROUTE_ALIASES = {
    "clear": "Clear",
    "clc": "Clc",
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
    return _ROUTE_ALIASES.get(name.lower(), name)


def _fallback_run(cmd: ParsedCommand) -> str:
    raw = cmd.source.replace('"', '\\"')
    return raw


def _render_route(cmd: ParsedCommand) -> str:
    """按 ROUTES 生成单行 Python 调用，无 per-command 特殊分支。"""
    route = ROUTES.get(_route_key(cmd.name))
    if route is None:
        return _fallback_run(cmd)

    fields = cmd.fields[1:]

    if isinstance(route, str):
        formatted = [_format_value(v) for v in fields]
        if not formatted:
            return f"{route}()"
        return f"{route}({', '.join(formatted)})"

    if isinstance(route, tuple) and route[0] == "chain":
        _, get_path, method_name, skip = route[:4]
        rest_prefix = route[4] if len(route) > 4 else 0
        if len(fields) <= skip:
            return f"{get_path}().{method_name}()"
        key = fields[skip]
        rest_fields = list(fields[:rest_prefix]) + list(fields[skip + 1:])
        formatted_key = _format_value(key)
        formatted_rest = [_format_value(v) for v in rest_fields]
        if formatted_rest:
            return f"{get_path}({formatted_key}).{method_name}({', '.join(formatted_rest)})"
        return f"{get_path}({formatted_key}).{method_name}()"

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