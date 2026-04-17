from pathlib import Path
from typing import Literal, Any

from ..common import project
from ..core import command
import json
import pandas as pd

# /output,D:\\temp\\Temp1\\Check\\频遇组合包络.txt,echk,混凝土_PC腹板斜截面抗裂验算_频遇组合包络
_CMD = "/output,{out_file_path}.txt,echk,{check_file_name}"
_CHECK_TXT_PATH = "Temperary"

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
    strCheckName: str) -> tuple[bool, str, pd.DataFrame]:
    '''
    验算结果导出
    
    Args:
        eSheetType (str): 表格名称
            * "一般"
            * "混凝土"
            * "施工阶段荷载包络"
        eCheckItem (str): 验算类型
            * "正截面抗弯验算"
            * "斜截面抗剪验算"
            * "正截面抗压验算"
            * "PC抗扭验算"
            * "PS正截面短期抗裂验算"
            * "PC正截面长期抗裂验算"
            * "PC顶底板斜截面抗裂验算"
            * "PC腹板斜截面抗裂验算"
            * "裂缝宽度验算"
            * "挠度验算"
            * "PC正截面压应力验算"
            * "PC斜截面主压应力验算"
            * "PC钢束拉应力验算"
            * "PC施工阶段正截面压应力验算"
            * "PC施工阶段正截面拉应力验算"
            * "PC施工阶段正截面拉应力验算",
            * "正截面杭拉/压承载力验算",
            * "PC斜载面抗裂验算",
            * "PC使用阶段正截面压应力验算",
            * "PC使用阶段斜载面主压应力验算",
            * "RC施工阶段正截面压应力验算",
            * "RC施工阶段中性轴处主拉应力验算",
            * "RC施工阶段受拉钢筋拉应力验算"
        strCheckName (str): 验算名称

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    # e = OSISEngine.GetInstance()
    # # return e.OSIS_CheckResult(base_path, middle_path, end_path)
    # isok, error, result_txt_path = e.OSIS_CheckResult(eSheetType, eCheckItem, strCheckName)
    # if isok:
    #     data = read_ansi_file_to_json(result_txt_path)
    #     return isok, error, json.dumps(data, indent=2, ensure_ascii=False)
    # else:
    #     return isok, error, None
    # 1 获取项目目录
    project_path = project.get_project_directory()
    if not project_path:
        return False, "获取文件夹失败", None

    project_path = Path(project_path)
    check_name = eSheetType + "_" + eCheckItem + "_" + strCheckName

    # 2 工况文件路径
    check_file_path = project_path / _CHECK_TXT_PATH / check_name

    # 3 生成命令
    str_cmd = _CMD.format(out_file_path=check_file_path, check_file_name=check_name)

    # 4 执行命令
    is_ok, error = command.osis_run(str_cmd, mode="exec")
    if not is_ok:
        return False, error, None

    # 5 读取结果
    txt_file_path = project_path / _CHECK_TXT_PATH / check_name
    txt_file_path = txt_file_path.with_suffix(".txt")
    df = pd.read_csv(
        txt_file_path,
        sep=r"\s+",          # 用正则匹配任意空白（空格/制表符）
        header=2,            # 表头在第3行（索引从0开始，这里跳过前两行标题）
        skiprows=[],         # 若还有多余空行可在这里加行号
        encoding="gbk",    # 若乱码可换成 "gbk" / "gb2312"
        on_bad_lines="skip"  # 跳过格式异常行
    )

    return True, "", df
