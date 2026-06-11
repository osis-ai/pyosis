"""命令流解析器.

支持:
    - 行注释（//、#）
    - 多行续行（行末逗号 / 下一行首字符为空白+逗号）
    - 分号分隔的多条命令
    - 空行
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class ParsedCommand:
    """一条已解析的 OSIS 命令。"""

    raw: str
    fields: List[str]
    name: str
    source: str = ""


_COMMENT_LINE_RE = re.compile(r"^\s*(//|#)")
_BLANK_RE = re.compile(r"^\s*$")


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
        if not physical or physical.endswith(";"):
            physical = physical.rstrip(";").rstrip()
        if not physical:
            continue

        fields = [f.strip() for f in physical.split(",")]
        cmd_name = fields[0] if fields else ""

        commands.append(
            ParsedCommand(
                raw=physical,
                fields=fields,
                name=cmd_name,
                source=physical,
            )
        )

    return commands