from pathlib import Path
from typing import Literal, Any

from .result import txt_file_path
from ..core import project, command
import json
import pandas as pd

# 将工况结果转换为txt的命令
_CMD = "/output,{out_file_path}.txt,{e_type},{check_file_name}"
_LOAD_CASE_FILE_PATH = "Temperary"
_LOAD_CASE_TXT_PATH = "Temperary"

# def osis_elem_force(strLCName: str, eDataItem: Literal['EF'], eElementType: Literal["BEAM3D", "TRUSS", "SPRING", "CABLE", "SHELL"]):
#     '''
#     提取内力结果
#
#     Args:
#         strLCName (str): 工况名称
#         eDataItem (str): 数据类型，不区分大小写。EF = 内力
#         eElementType (str): 单元类型，不区分大小写。BEAM3D = 梁柱单元，TRUSS = 桁架单元，SPRING = 弹簧单元，CABLE = 拉索单元，SHELL = 壳单元
#
#     Returns:
#         tuple (bool, str):
#             - bool: 操作是否成功
#             - str: 失败原因（如果操作失败）
#     '''
#     e = OSISEngine.GetInstance()
#     eDataItem = eDataItem.upper()
#     eElementType = eElementType.upper()
#     return e.OSIS_ElemForce(strLCName, eDataItem, eElementType)

def osis_loadcase_result(strLCName:str, eType: Literal['LCEF','LCED','LCND','LCBF','LCTL','LCS']) -> tuple[bool, str, pd.DataFrame]:
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

    is_ok, err, file_path = txt_file_path(strLCName, eType, _CMD)

    df = pd.read_csv(
        file_path,
        sep=r"\s+",          # 用正则匹配任意空白（空格/制表符）
        header=0,            # 表头在第3行（索引从0开始，这里跳过前两行标题）
        skiprows=[],         # 若还有多余空行可在这里加行号
        encoding="gbk",    # 若乱码可换成 "gbk" / "gb2312"
        on_bad_lines="skip"  # 跳过格式异常行
    )

    return True, "", df
