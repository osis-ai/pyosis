from pathlib import Path
from typing import Literal, Any
from ..core import OSISEngine, project, command
import json

_CMD = "/output,{out_file_path},echk,{check_file_name}"
_CHECK_FILE_PATH = "check"
_CHECK_TXT_PATH = "temp"

def osis_check_result(
        eSheetType: Literal["一般", "混凝土"], 
        eCheckItem: Literal["EN_MOMENTCAPACITY_PSC_JTG33622018",
                            "EN_SHEARCAPACITY_PSC_JTG33622018",
                            "EN_NORMALCOMPRESSANDTENSIONCAPACITY_PSC_JTG33622018",
                            "EN_TORSIONCAPACITY_PSC_JTG33622018",
                            "EN_NORMALCRACKSHORT_PSC_JTG33622018",
                            "EN_NORMALCRACKLONG_PSC_JTG33622018",
                            "EN_OBLIQUECRACKTOPBOT_PSC_JTG33622018",
                            "EN_OBLIQUECRACKPLATE_PSC_JTG33622018",
                            "EN_CRACKWIDTH_PSC_JTG33622018",
                            "EN_DEFLECTION_PSC_JTG33622018",
                            "EN_NORMALCOMPSTRESS_PSC_JTG33622018",
                            "EN_OBLIQUECOMPSTRESS_PSC_JTG33622018",
                            "EN_STRANDSTRESS_PSC_JTG33622018",
                            "EN_STAGENORMALCOMPRESS_PSC_JTG33622018",
                            "EN_STAGENORMALTENSILE_PSC_JTG33622018"
                            ], 
        strCheckName: str) -> tuple[bool, str, Any]:
    '''
    验算
    
    Args:
        eSheetType (Literal["一般", "混凝土"]): 
        eCheckItem (Literal["正截面抗弯验算",
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
                            "PC施工阶段正截面拉应力验算"
                            ])
        strCheckName (str): 文件名称

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
    is_ok, project_path = project.get_project_directory()
    if not is_ok:
        return False, "获取文件夹失败", ""

    project_path = Path(project_path)

    # 2 工况文件路径
    check_file_path = project_path / _CHECK_FILE_PATH

    # 3 生成命令
    str_cmd = _CMD.format(out_file_path=check_file_path, check_file_name=strCheckName)

    # 4 执行命令
    is_ok, error, _ = command.osis_run(str_cmd, mode="exec")
    if not is_ok:
        return False, error, ""

    # 5 读取结果
    txt_file_path = project_path / _CHECK_TXT_PATH / strCheckName
    txt_file_path = txt_file_path.with_suffix(".txt")
    data = read_check_txt_file_to_json(str(txt_file_path))

    return True, "", json.dumps(data, indent=2, ensure_ascii=False)

    
def read_check_txt_file_to_json(file_path):

    with open(file_path, 'r', encoding='gbk') as f:
        lines = f.readlines()
    
    # 查找实际数据开始的位置
    start_index = 0
    for i, line in enumerate(lines):
        if "单元" in line and "验算位置" in line:  # 查找包含表头的行
            start_index = i
            break
    
    if start_index == 0 and len(lines) < 2:
        return []
    
    # 解析表头
    headers = lines[start_index].strip().split('\t')
    
    # 处理数据行
    result = []
    for line in lines[start_index + 1:]:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        values = line.split('\t')
        if len(values) != len(headers):
            continue  # 跳过不完整行
            
        # 创建字典对象
        row_dict = {}
        for i, header in enumerate(headers):
            header = header.replace(' ','')
            value = values[i].replace(' ','')

            row_dict[header] = value
        
        result.append(row_dict)
    
    return result