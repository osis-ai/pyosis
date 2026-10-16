"""规范验算结果——/output 命令流 + txt 解析

验算结果尚无 HTTP 路由，本模块是当前唯一可用的取数方式，也是 pyosis 里最后一处
走 /output 的地方。路由就绪后删除——除了验算本身，还需要一个「列出有哪些验算项」
的路由，用来替掉 ResultManager.check_all 扫描项目目录 Check/*.lcc 的做法。
"""
from itertools import islice
from pathlib import Path
from typing import Literal

import pandas as pd

from pyosis.core import command
from pyosis.project import interface

# /output,D:\\temp\\Temp1\\Check\\频遇组合包络.txt,echk,混凝土_PC腹板斜截面抗裂验算_频遇组合包络
_CMD = "/output,{out_file_path}.txt,echk,{check_file_name}"

_TXT_DIR = "Temperary"


def _output_problem(txt_path: Path, min_lines: int) -> str:
    """结果 txt 读不出表格时给出原因；正常返回空串。

    /output 是「先建文件再干活」，命令失败也会留下一个 0 字节的 txt；
    命令成功也只保证它返回 true，不保证写出了表。min_lines 是「抬头 + 表头」
    所需的最小行数，少于它下游 pandas 只会抛 "No columns to parse from file"，
    把 OSIS 侧的真实原因盖掉。
    """
    if not txt_path.exists():
        return f"/output 未生成结果文件：{txt_path}"
    if txt_path.stat().st_size == 0:
        return f"/output 生成的结果文件是 0 字节空文件：{txt_path}"
    with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
        lines = sum(1 for _ in islice(f, min_lines))
    if lines < min_lines:
        return (f"/output 生成的结果文件只有 {lines} 行，"
                f"不足表头所需的 {min_lines} 行：{txt_path}")
    return ""


def _output_txt_path(file_name: str, e_type: str, cmd: str,
                     min_lines: int = 1) -> tuple[bool, str, str]:
    """跑一次 /output，返回结果 txt 的路径

    Args:
        file_name: 文件名称
        e_type: 指令名称
        cmd: 命令流
        min_lines: 结果 txt 至少要有的行数（抬头 + 表头）。不足即按失败报出。

    Returns:
        tuple (bool, str, str): 是否成功，失败原因，txt文件路径
    """
    project_path = interface.get_project_directory()
    if not project_path:
        return False, "获取文件夹失败", ""

    project_path = Path(project_path)
    out_path = project_path / _TXT_DIR / file_name
    str_cmd = cmd.format(out_file_path=out_path, e_type=e_type,
                         check_file_name=file_name)

    is_ok, osis_msg = command.osis_run(str_cmd, mode="exec")
    if not is_ok:
        return False, osis_msg, ""

    file_path = (project_path / _TXT_DIR / file_name).with_suffix(".txt")

    # 命令成功不等于写出了表，这里替下游把空文件挡下来
    problem = _output_problem(file_path, min_lines)
    if problem:
        osis_note = osis_msg.strip() or "（OSIS 未返回错误或警告）"
        return False, f"{problem}；OSIS 返回：{osis_note}；命令流：{str_cmd}", ""

    return True, "", file_path


def osis_check_result(
    eSheetType: Literal["一般", "混凝土", "施工阶段荷载包络"],
    eCheckItem: Literal["正截面抗弯验算",
                        "斜截面抗剪验算",
                        "正截面抗压验算",
                        "PC抗扭验算",
                        "PS正截面短期抗裂验算",
                        "PC正截面长期抗裂验算",
                        "PC顶底板斜截面抗裂验算",
                        "PC腹板斜截面抗裂验算",
                        "裂缝宽度验算",
                        "挠度验算",
                        "PC正截面压应力验算",
                        "PC斜截面主压应力验算",
                        "PC钢束拉应力验算",
                        "PC施工阶段正截面压应力验算",
                        "PC施工阶段正截面拉应力验算",
                        "正截面杭拉/压承载力验算",
                        "PC斜载面抗裂验算",
                        "PC使用阶段正截面压应力验算",
                        "PC使用阶段斜载面主压应力验算",
                        "RC施工阶段正截面压应力验算",
                        "RC施工阶段中性轴处主拉应力验算",
                        "RC施工阶段受拉钢筋拉应力验算"],
    strCheckName: str) -> tuple[bool, str, pd.DataFrame]:       # todo: 该函数日后需要修改成从OSIS的HDF5里导出
    '''
    验算结果导出

    Args:
        eSheetType (str): 表格名称
            * "一般"
            * "混凝土"
            * "施工阶段荷载包络"
        eCheckItem (str): 验算类型，取值见 ResultManager.check 的文档
        strCheckName (str): 验算名称

    Returns:
        tuple (bool, str, DataFrame):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
            - DataFrame: 结果表
    '''
    check_name = eSheetType + "_" + eCheckItem + "_" + strCheckName

    # 验算 txt 表头在第 3 行（header=2），少于 3 行就解析不出表
    is_ok, error, file_path = _output_txt_path(check_name, "echk", _CMD, min_lines=3)
    if not is_ok:
        return False, error, None

    df = pd.read_csv(
        file_path,
        sep=r"\s+",          # 用正则匹配任意空白（空格/制表符）
        header=2,            # 表头在第3行（索引从0开始，这里跳过前两行标题）
        skiprows=[],         # 若还有多余空行可在这里加行号
        encoding="utf-8",    # OSIS /output 生成的 .txt 是 UTF-8 编码
        on_bad_lines="skip"  # 跳过格式异常行
    )

    return True, "", df
