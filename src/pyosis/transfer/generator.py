"""命令流 → pyosis 代码生成器.

按字段顺序生成调用, 支持:
  - direct: engine.method(args...)  (args=fields[skip:])
  - chain:  engine.get(fields[skip]).method(fields[rest_prefix] + fields[skip+1:]...)
"""

from __future__ import annotations
from typing import List

from .parser import ParsedCommand
from .routes import ROUTES


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


def _render_command(cmd: ParsedCommand) -> str:
    route = ROUTES.get(cmd.name)

    if route is None:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    fields = cmd.fields[1:]

    # chain:  engine.get(key).method(rest...)
    # route = ("chain", get_path, method_name, skip, rest_prefix)
    if isinstance(route, tuple) and route[0] == "chain":
        _, get_path, method_name, skip = route[:4]
        rest_prefix = route[4] if len(route) > 4 else 0
        if len(fields) <= skip:
            return f"{get_path}().{method_name}()"
        key = fields[skip]
        rest_fields = list(fields[:rest_prefix]) + list(fields[skip + 1:])
        formatted_key = _format_value(key)
        formatted_rest = [_format_value(v) for v in rest_fields]
        return f"{get_path}({formatted_key}).{method_name}({', '.join(formatted_rest)})"

    # direct:  engine.method(args...)
    method = route
    formatted = [_format_value(v) for v in fields]
    return f"{method}({', '.join(formatted)})"


def generate(commands: List[ParsedCommand]) -> str:
    return "\n".join(_render_command(cmd) for cmd in commands) + "\n"