"""命令流解析器.

支持:
    - 行注释（//、#）
    - 多行续行（行末逗号 / 下一行首字符为空白+逗号）
    - 分号分隔的多条命令
    - 空行
    - *dim / 矩阵赋值（kind=matrix_dim / matrix_assign）
    - OSIS 粘连命令拆分（如 BothSectionOffset → Both + SectionOffset）
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from .split import split_cmd, split_commands

# OSIS 导出时将下一条命令名粘在上一个字段末尾的情况（如 BothSectionOffset）
_GLUED_TAIL_COMMANDS = ("SectionOffset",)

MATRIX_ASSIGN_RE = re.compile(r"^(\w+)\[([\d,\s]+)\]\s*=\s*(.+)$")

_COMMENT_LINE_RE = re.compile(r"^\s*(//|#)")
_BLANK_RE = re.compile(r"^\s*$")


@dataclass
class ParsedCommand:
    """一条已解析的 OSIS 命令。"""

    raw: str
    fields: List[str]
    name: str
    source: str = ""
    kind: str = "normal"  # normal | matrix_dim | matrix_assign
    matrix_name: str = ""
    matrix_indices: tuple[int, ...] = ()
    matrix_value: str = ""


def _join_continuation_lines(lines: List[str]) -> List[str]:
    """合并续行, 返回已合并的物理行列表。"""
    result: List[str] = []
    buf = ""
    for raw_line in lines:
        if buf:
            buf += " " + raw_line.strip()
            if not buf.rstrip().endswith(","):
                result.append(buf.strip().rstrip(";"))
                buf = ""
        else:
            if raw_line.rstrip().endswith(","):
                buf = raw_line.rstrip()
            else:
                result.append(raw_line.strip().rstrip(";"))
    if buf:
        result.append(buf.strip().rstrip(";"))
    return result


def _split_glued_command_fields(fields: List[str]) -> List[List[str]]:
    """将粘连字段拆成多条命令的 fields 列表。

    例: SteelPlate,...,BothSectionOffset,50,... →
        [SteelPlate,...,Both] + [SectionOffset,50,...]
    """
    if not fields:
        return [fields]

    groups: List[List[str]] = []
    current = list(fields)

    while current:
        split_at: int | None = None
        tail_cmd: str | None = None
        prefix: str | None = None

        for i, field in enumerate(current):
            for tail in _GLUED_TAIL_COMMANDS:
                if len(field) > len(tail) and field.endswith(tail):
                    split_at = i
                    tail_cmd = tail
                    prefix = field[: -len(tail)]
                    break
            if split_at is not None:
                break

        if split_at is None:
            groups.append(current)
            break

        head = current[:split_at]
        if prefix:
            head.append(prefix)
        groups.append(head)
        current = [tail_cmd] + current[split_at + 1 :]  # type: ignore[list-item]

    return groups


def _make_parsed_command(fields: List[str], source: str) -> ParsedCommand:
    first = fields[0] if fields else ""
    return ParsedCommand(
        raw=source,
        fields=fields,
        name=first,
        source=source,
        kind="normal",
    )

# 解析一条命令
def _parse_one_command(source: str) -> List[ParsedCommand]:
    fields = split_cmd(source)
    first = fields[0] if fields else ""
    lower_first = first.lower()
    # 处理 *dim 命令
    if lower_first.startswith("*dim") or lower_first == "charn":
        return [
            ParsedCommand(
                raw=source,
                fields=fields,
                name=first,
                source=source,
                kind="matrix_dim",
            )
        ]

    # 处理矩阵赋值命令
    assign_match = MATRIX_ASSIGN_RE.match(source)
    if assign_match:
        indices = tuple(int(x.strip()) for x in assign_match.group(2).split(",") if x.strip() != "")
        return [
            ParsedCommand(
                raw=source,
                fields=fields,
                name=assign_match.group(1),
                source=source,
                kind="matrix_assign",
                matrix_name=assign_match.group(1),
                matrix_indices=indices,
                matrix_value=assign_match.group(3).strip(),
            )
        ]

    result: List[ParsedCommand] = []
    # 处理粘连命令
    for group in _split_glued_command_fields(fields):
        if not group:
            continue
        sub_source = ",".join(group)
        result.append(_make_parsed_command(group, sub_source))
    return result


def parse_text(text: str) -> List[ParsedCommand]:
    """解析 OSIS 命令流文本。

    Returns:
        ParsedCommand 列表（不含注释、空行）。
    """
    lines = text.splitlines()
    physical_lines = _join_continuation_lines(lines)

    commands: List[ParsedCommand] = []

    for physical in physical_lines:
        if not physical:
            continue
        if _COMMENT_LINE_RE.match(physical):
            continue
        if _BLANK_RE.match(physical):
            continue
        if "//" in physical:
            hash_pos = physical.find("//")
            if hash_pos == 0:
                continue
            if hash_pos > 0 and physical[hash_pos - 1] in (" ", "\t"):
                physical = physical[:hash_pos].rstrip()
        if not physical:
            continue

        for sub in split_commands(physical):
            commands.extend(_parse_one_command(sub))

    return commands