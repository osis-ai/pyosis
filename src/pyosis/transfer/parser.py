"""命令流解析器.

职责:把输入的一整段 OSIS 命令流文本解析成多条 ParsedCommand.
不做任何 .out 格式相关的事(比如识别 //--- CONTROL --- 这类模块标记),
那是 out_to_python 的职责.

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
from typing import Iterator, List

from .split import split_cmd, split_commands

# OSIS 导出时将下一条命令名粘在上一个字段末尾的情况（如 BothSectionOffset）
_GLUED_TAIL_COMMANDS = ("SectionOffset",)

# 矩阵赋值命令正则表达式
MATRIX_ASSIGN_RE = re.compile(r"^(\w+)\[([\d,\s]+)\]\s*=\s*(.+)$")
# 注释行正则表达式
COMMENT_LINE_RE = re.compile(r"^\s*(//|#)")
# 空白行正则表达式
BLANK_RE = re.compile(r"^\s*$")


# 已解析的 OSIS 命令
@dataclass
class ParsedCommand:
    """一条已解析的 OSIS 命令"""
    raw: str
    fields: List[str]
    name: str
    source: str = ""
    kind: str = "normal"  # normal | matrix_dim | matrix_assign
    matrix_name: str = ""
    matrix_indices: tuple[int, ...] = ()
    matrix_value: str = ""


def _join_continuation_lines(lines: List[str]) -> List[str]:
    """处理一条命令拆成多行命令的情况"""
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


# 去除一行内的 // 注释（保留 // 之前的有效命令部分）
def strip_inline_comment(line: str) -> str:
    if "//" not in line:
        return line
    pos = line.find("//")
    if pos == 0:
        return ""
    if line[pos - 1] in (" ", "\t"):
        return line[:pos].rstrip()
    return line


# 迭代"物理命令行":合并续行;不过滤注释/空行,留给调用方决定
def iter_physical_lines(text: str) -> Iterator[str]:
    """逐行 yield 物理命令行(已合并续行)。

    不做任何注释/空行过滤——调用方按需处理:
        - parse_text 会跳过 //、#、空行(以及 //--- MODULE_NAME --- 这种模块标记);
          因为 parser 不识别模块,所以这条规则保持宽泛。
        - out_to_python._split_by_module 同样跳过注释/空行,但用 MODULE_PATTERN
          提前捕获模块标记以切换 current_module。
    """
    yield from _join_continuation_lines(text.splitlines())


# 创建已解析的命令
def _make_parsed_command(fields: List[str], source: str) -> ParsedCommand:
    first = fields[0] if fields else ""
    return ParsedCommand(
        raw=source,
        fields=fields,
        name=first,
        source=source,
        kind="normal",
    )


# 解析一条命令,返回已解析的命令列表
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


# 解析一行物理命令为多条 ParsedCommand(处理 ; 分隔)
def _parse_physical_line(line: str) -> List[ParsedCommand]:
    out: List[ParsedCommand] = []
    for sub in split_commands(line):
        out.extend(_parse_one_command(sub))
    return out


# 解析 OSIS 命令流文本,返回已解析的命令列表
def parse_text(text: str) -> List[ParsedCommand]:
    """解析 OSIS 命令流文本。

    Returns:
        ParsedCommand 列表（不含注释、空行）。
        不识别 //--- MODULE_NAME --- 这类 .out 模块标记,那是 out_to_python 的职责。
    """
    commands: List[ParsedCommand] = []
    for line in iter_physical_lines(text):
        if COMMENT_LINE_RE.match(line):
            continue
        if BLANK_RE.match(line):
            continue
        line = strip_inline_comment(line)
        if BLANK_RE.match(line):
            continue
        commands.extend(_parse_physical_line(line))
    return commands
