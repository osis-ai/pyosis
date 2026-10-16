import io
from typing import Literal

from .result import txt_file_path
import pandas as pd

# 将工况结果转换为txt的命令
_CMD = "/output,{out_file_path}.txt,{e_type},{check_file_name}"


def _is_number(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False


def _find_header_row(lines: list[str]) -> int | None:
    """结果 txt 的表头所在行（0 起），找不到返回 None。

    抬头行数按结果类型不同：LCND/LCEF 没有抬头（表头就在第 0 行）、
    LCBF 抬头 2 行、LCS 抬头 3 行。抬头行都是单字段的标题或空行，
    表头则是第一个不止一个字段的行，据此识别。
    """
    for i, line in enumerate(lines):
        if len(line.split()) > 1:
            return i
    return None


def osis_loadcase_result(strLCName:str, eType: Literal['LCEF','LCED','LCND','LCBF','LCTL','LCS']) -> tuple[bool, str, pd.DataFrame]:       # todo: 该函数日后需要修改成从OSIS的HDF5里导出
    """
    提取荷载工况结果
    Args:
        strLCName (str): 工况名称
        eType (str): 荷载工况结果类型
            * LCEF = 荷载工况结果的单元内力;
            * LCED = 荷载工况结果的单元位移;
            * LCND = 荷载工况结果的节点位移;
            * LCBF = 荷载工况结果的边界反力;
            * LCTL = 荷载工况结果的钢束损失;
            * LCS  = 荷载工况结果的单元应力;
    Returns:
        tuple (bool, str): 是否成功，失败原因

    """
    is_ok, err, file_path = txt_file_path(strLCName, eType, _CMD, min_lines=1)
    if not is_ok:
        return False, err, None

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()

    header_row = _find_header_row(lines)
    if header_row is None:
        return False, f"结果文件 {file_path} 里找不到表头行（每行都不足 2 个字段）", None

    # 从表头那行起喂给 pandas：抬头行数按类型变，交给它自己按行号跳过容易数错
    df = pd.read_csv(
        io.StringIO("\n".join(lines[header_row:])),
        sep=r"\s+",          # 用正则匹配任意空白（空格/制表符）
        header=0,            # 上面已切到表头，这里就是第 0 行
        skiprows=[],         # 若还有多余空行可在这里加行号
        encoding="utf-8",    # OSIS /output 生成的 .txt 是 UTF-8 编码
        on_bad_lines="skip"  # 跳过格式异常行
    )

    # 表头认成数据行时，列名会全是数字（真表头里没有纯数字列名）
    if len(df.columns) and all(_is_number(str(c)) for c in df.columns):
        return False, (f"结果文件 {file_path} 的表头识别有误：第 {header_row} 行不像表头"
                       f"（列名全是数字），请检查 /output 的输出格式"), None

    return True, "", df
