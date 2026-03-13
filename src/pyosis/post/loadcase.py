from typing import Literal, Any
from .result import txt_file_path

# 将工况结果转换为txt的命令
_CMD = "/output,{out_file_path}.txt,{e_type},{check_file_name}"

def osis_loadcase_result(fileName:str, eType: Literal['LCEF','LCED','LCND','LCBF','LCTL','LCS']) -> tuple[bool, str, Any]:
    """
    提取荷载工况结果
    Args:
        fileName (str): 文件名字
        eType (str): 荷载工况结果名
            * LCEF = 荷载工况结果的单元内力;
            * LCED = 荷载工况结果的单元位移;
            * LCND = 荷载工况结果的节点位移;
            * LCBF = 荷载工况结果的边界反力;
            * LCTL = 荷载工况结果的钢束损失;
            * LCS = 荷载工况结果的单元应力;
    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    is_ok, err, file_path, = txt_file_path(fileName, eType, _CMD)
    data = read_loadcase_txt_file_to_json(str(file_path))
    return True, "", data

def read_loadcase_txt_file_to_json(file_path)-> list[dict]:
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
    return result