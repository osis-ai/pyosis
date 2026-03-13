from typing import Literal, Any

from pyosis.post.result import txt_file_path

# 将包络结果转换为txt的命令
_CMD = "/output,{out_file_path}.txt,{e_type},{check_file_name}"

def osis_env_result(fileName:str, eType: Literal['EnvBF','EnvEF','EnvES','EnvS','EnvND']) -> tuple[bool, str, Any]:
    """
    提取包络结果
    Args:
        fileName (str): 文件名字
        eType (str): 包络结果名
            * EnvBF = 包络/并发结果的边界反力;
            * EnvEF = 包络/并发结果的单元内力;
            * EnvES = 包络/并发结果的单元应变;
            * EnvS = 包络/并发结果的单元应力;
            * EnvND = 包络/并发结果的节点位移;
    Returns:
        tuple (bool, str): 是否成功，失败原因

    """
    is_ok, err, file_path = txt_file_path(fileName, eType, _CMD)
    data = read_env_txt_file_to_json(str(file_path))
    return True, "", data

def read_env_txt_file_to_json(file_path)-> list[dict]:
    with open(file_path, 'r', encoding='gbk') as f:
        lines = f.readlines()

    # 查找实际数据开始的位置
    start_index = 0
    for i, line in enumerate(lines):
        if "工况" in line and "边界" in line:  # 查找包含表头的行
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
            header = header.replace(' ', '')
            value = values[i].replace(' ', '')

            row_dict[header] = value

        result.append(row_dict)

    return result