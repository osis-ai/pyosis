from typing import Literal, Any

import pandas as pd

from pyosis.result.result import txt_file_path

# 将包络结果转换为txt的命令
_CMD = "/output,{out_file_path}.txt,{e_type},{check_file_name}"

def osis_env_result(strEnvName:str, eType: Literal['EnvBF','EnvEF','EnvES','EnvS','EnvND']) -> tuple[bool, str, pd.DataFrame]:       # todo: 该函数日后需要修改成从OSIS的HDF5里导出
    """
    提取包络结果
    Args:
        strEnvName (str): 包络名称
        eType (str): 包络类型
            * EnvBF = 包络/并发结果的边界反力;
            * EnvEF = 包络/并发结果的单元内力;
            * EnvES = 包络/并发结果的单元应变;
            * EnvS = 包络/并发结果的单元应力;
            * EnvND = 包络/并发结果的节点位移;
    Returns:
        tuple (bool, str): 是否成功，失败原因

    """
    is_ok, err, file_path = txt_file_path(strEnvName, eType, _CMD)
    if not is_ok:
        return False, err, None
    df = pd.read_csv(
        file_path,
        sep=r"\s+",  # 用正则匹配任意空白（空格/制表符）
        header=0,  # 表头在第3行（索引从0开始，这里跳过前两行标题）
        skiprows=4,  # 若还有多余空行可在这里加行号
        encoding="utf-8",  # OSIS /output 生成的 .txt 是 UTF-8 编码
        on_bad_lines="skip"  # 跳过格式异常行
    )

    return True, "", df