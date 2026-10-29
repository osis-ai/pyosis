"""命令流 → pyosis 代码生成器.

所有普通命令经 routes.ROUTES 透传:
  - direct: engine.method(args...)
  - chain:  engine.get(key).method(reordered args...)

长参数列表(≥ KWARGS_MIN 个形参、签名可内省、无 *args)的调用生成为
关键字实参——命令流字段重排不再静默错位到别的形参上。
矩阵 *dim / 赋值仍由 MatrixAccumulator 合并为 engine.matrix(...)。
未注册命令 → engine.run("原始命令流")。

generate_lines(commands, ctx=None) 的 ctx 为跨命令下文:
    ctx["creep_grades"]: 编号 → CONC 材料等级集合(由 out_to_python 预扫描)
    ctx["warnings"]: fixer 追加的告警,作为注释行插在对应调用前
"""

from __future__ import annotations

from typing import List

from .introspect import positional_param_names, resolve_chain_method, resolve_callable
from .matrix import MatrixAccumulator
from .parser import ParsedCommand
from .routes import CMD_ALIASES, REST_FIXERS, ROUTES

# 形参个数达到该值的调用才生成关键字实参;短调用保持位置实参(生成的代码更紧凑)
KWARGS_MIN = 5

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
    """未注册命令的兜底：用 engine.run("...") 包裹原始命令流，确保所有命令都可执行。"""
    raw = cmd.source.replace("\\", "\\\\").replace('"', '\\"')
    return f'engine.run("{raw}")'


def _join_args(fields: list[str], func) -> str:
    """按目标方法签名渲染实参:长签名用关键字实参,其余位置实参。"""
    formatted = [_format_value(v) for v in fields]
    if not formatted:
        return ""
    if len(formatted) >= KWARGS_MIN and func is not None:
        names = positional_param_names(func)
        # 实参个数须不超过形参个数(逐位对应),否则映射不可靠,退回位置实参
        if names and len(formatted) <= len(names):
            return ", ".join(f"{n}={v}" for n, v in zip(names, formatted))
    return ", ".join(formatted)


def _render_route(cmd: ParsedCommand, ctx: dict | None) -> str:
    """按 ROUTES 生成单行 Python 调用，无 per-command 特殊分支。"""
    key = _route_key(cmd.name)
    route = ROUTES.get(key)
    if route is None:
        return _fallback_run(cmd)

    engine = ctx.get("engine") if ctx else None

    fields = cmd.fields[1:]

    if isinstance(route, str):
        fixer = REST_FIXERS.get(key)
        if fixer is not None:
            fields = fixer(fields, ctx)
        args = _join_args(fields, resolve_callable(engine, route) if engine else None)
        return f"{route}({args})"

    if isinstance(route, tuple) and route[0] == "list":
        # 前 n_head 个字段按位置传,其余合并成一个 list 字面量
        # (如 Spline3D 的坐标序列,接口收的是 list 而不是展平的多个实参)
        _, target, n_head = route[:3]
        head, tail = list(fields[:n_head]), list(fields[n_head:])
        head_args = _join_args(head, resolve_callable(engine, target) if engine else None)
        tail_lit = "[" + ", ".join(_format_value(v) for v in tail) + "]"
        return f"{target}({head_args}, {tail_lit})" if head_args else f"{target}({tail_lit})"

    if isinstance(route, tuple) and route[0] == "chain":
        _, get_path, method_name, skip = route[:4]
        rest_prefix = route[4] if len(route) > 4 else 0
        if len(fields) <= skip:
            return f"{get_path}().{method_name}()"
        key_field = fields[skip]
        rest_fields = list(fields[:rest_prefix]) + list(fields[skip + 1:])
        fixer = REST_FIXERS.get(key)
        if fixer is not None:
            rest_fields = fixer(rest_fields, ctx)
        method = resolve_chain_method(engine, get_path, method_name) if engine else None
        args = _join_args(rest_fields, method)
        formatted_key = _format_value(key_field)
        return f"{get_path}({formatted_key}).{method_name}({args})"

    return _fallback_run(cmd)


def generate_lines(commands: List[ParsedCommand], ctx: dict | None = None) -> List[str]:
    """生成 Python 调用行；矩阵命令合并为 engine.matrix(...)。

    ctx 同时传 engine 实例时可启用关键字实参;fixer 告警以注释行形式
    插在对应调用前。
    """
    lines: List[str] = []
    accumulator = MatrixAccumulator()
    warnings = ctx.setdefault("warnings", []) if ctx is not None else None

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

        rendered = _render_route(cmd, ctx)
        if warnings:
            lines.extend(f"# 注意: {w}" for w in warnings)
            warnings.clear()
        lines.append(rendered)

    flushed = accumulator.flush()
    if flushed:
        lines.append(flushed)

    return lines


def generate(commands: List[ParsedCommand], ctx: dict | None = None) -> str:
    return "\n".join(generate_lines(commands, ctx)) + "\n"
