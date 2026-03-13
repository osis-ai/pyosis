from pathlib import Path
from typing import Literal, Any
from ..core import OSISEngine, project, command
import json

# 将工况结果转换为txt的命令
_CMD = "/output,{out_file_path},{e_type},{check_file_name}"
_LOAD_CASE_FILE_PATH = "result"
_LOAD_CASE_TXT_PATH = "temp"

def osis_elem_force(strLCName: str, eDataItem: Literal['EF'], eElementType: Literal["BEAM3D", "TRUSS", "SPRING", "CABLE", "SHELL"]):
    '''
    提取内力结果
    
    Args:
        strLCName (str): 工况名称
        eDataItem (str): 数据类型，不区分大小写。EF = 内力
        eElementType (str): 单元类型，不区分大小写。BEAM3D = 梁柱单元，TRUSS = 桁架单元，SPRING = 弹簧单元，CABLE = 拉索单元，SHELL = 壳单元

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    e = OSISEngine.GetInstance()
    eDataItem = eDataItem.upper()
    eElementType = eElementType.upper()
    return e.OSIS_ElemForce(strLCName, eDataItem, eElementType)

def osis_load_case_result(fileName:str, eType:Literal['LCEF','LCED','LCND','LCBF','LCTL','LCS']) -> tuple[bool, str, Any]:
    """
    提取荷载工况结果
    Args:
        fileName(str):文件名字
        eType(Literal): 荷载工况结果名
            * LCEF = 荷载工况结果的单元内力;
            * LCED = 荷载工况结果的单元位移;
            * LCND = 荷载工况结果的节点位移;
            * LCBF = 荷载工况结果的边界反力;
            * LCTL = 荷载工况结果的钢束损失;
            * LCS = 荷载工况结果的单元应力;
    Returns:
        tuple (bool, str): 是否成功，失败原因

    """
    # 1 获取项目目录
    is_ok, project_path = project.get_project_directory()
    if not is_ok:
        return False, "获取文件夹失败", ""

    project_path = Path(project_path)

    # 2 工况文件路径
    load_case_file_path = project_path / _LOAD_CASE_FILE_PATH

    # 3 生成命令
    str_cmd = _CMD.format(out_file_path=load_case_file_path,e_type=eType,check_file_name=fileName)

    # 4 执行命令
    is_ok, error, _ = command.osis_run(str_cmd, mode="exec")
    if not is_ok:
        return False, error, ""

    # 5 读取结果
    txt_file_path = project_path / _LOAD_CASE_TXT_PATH / fileName
    txt_file_path = txt_file_path.with_suffix(".txt")
    data = read_load_case_txt_file_to_json(str(txt_file_path))

    return True, "", json.dumps(data, indent=2, ensure_ascii=False)

def read_load_case_txt_file_to_json(file_path)-> list[dict]:
    with open(file_path, 'r', encoding='gbk') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    # 提取表头（第一行）
    headers = lines[0].split()
    num_cols = len(headers)

    # 初始化结果列表
    result = []

    # 处理数据行
    for line in lines[1:]:
        # 按空白分割，但最多分割 num_cols - 1 次，防止 Rw 列缺失导致错位
        parts = line.split(maxsplit=num_cols - 1)

        # 如果列数不足，用空字符串补齐到 num_cols
        while len(parts) < num_cols:
            parts.append("")

        # 构建字典，所有值保持为字符串
        row_dict = {headers[i]: parts[i].strip() for i in range(num_cols)}
        result.append(row_dict)
    # json_result = json.dumps(result, ensure_ascii=False)
    # 打印结果
    return result