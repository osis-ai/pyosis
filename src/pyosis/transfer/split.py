"""OSIS 命令流拆分工具（transfer 专用，不依赖 core/build）。"""

from __future__ import annotations


def split_commands(text: str) -> list[str]:
    """按 ; 分割命令，去除空白。"""
    commands: list[str] = []
    for cmd in text.split(";"):
        cleaned = cmd.strip()
        if not cleaned:
            continue
        cleaned = " ".join(cleaned.split())
        cleaned = cleaned.replace(" ,", ",").replace(", ", ",")
        commands.append(cleaned)
    return commands


def split_cmd(cmd: str) -> list[str]:
    """按逗号分割参数；方括号 [] 内的逗号不分割。"""
    if not cmd:
        return []

    parts: list[str] = []
    current = ""
    in_quotes = False
    bracket_depth = 0
    for char in cmd:
        if char == '"':
            in_quotes = not in_quotes
            current += char
        elif char == "[" and not in_quotes:
            bracket_depth += 1
            current += char
        elif char == "]" and not in_quotes:
            bracket_depth -= 1
            current += char
        elif char == "," and not in_quotes and bracket_depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    parts.append(current.strip())
    return parts
