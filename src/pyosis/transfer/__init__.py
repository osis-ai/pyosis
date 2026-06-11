"""pyosis.transfer — OSIS 命令流 → pyosis 代码

用法:
    from pyosis.transfer import transfer

    code = transfer('Material,1,C50,CONC,JTG3362_2018,C50,1,0.05;')
"""

from .parser import parse_text, ParsedCommand
from .generator import generate

__all__ = ["transfer", "parse_text", "ParsedCommand", "generate"]


def transfer(text: str) -> str:
    """把 OSIS 命令流文本转换为 pyosis Python 代码字符串。

    Returns:
        每行一条 ``engine.xxx.create_yyy(...)`` 或 ``engine.run("原始命令流")``。
    """
    return generate(parse_text(text))