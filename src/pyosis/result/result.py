from pathlib import Path

from pyosis.common import project
from pyosis.core import command

_LOAD_CASE_FILE_PATH = "Temperary"
_LOAD_CASE_TXT_PATH = "Temperary"

def txt_file_path(file_name, e_type, cmd) -> tuple[bool, str, str]:
    """
    用于获取工况和包络结果的txt路径
    Args:
        file_name: 文件名称
        e_type: 指令名称
        cmd: 命令流

    Returns:
        tuple (bool, str): 是否成功，失败原因，txt文件路径
    """
    # 1 获取项目目录
    project_path = project.get_project_directory()
    if not project_path:
        return False, "获取文件夹失败", ""

    project_path = Path(project_path)

    # 2 工况文件路径
    load_case_file_path = project_path / _LOAD_CASE_FILE_PATH / file_name

    # 3 生成命令
    str_cmd = cmd.format(out_file_path=load_case_file_path, e_type=e_type, check_file_name=file_name)

    # 4 执行命令
    is_ok, error = command.osis_run(str_cmd, mode="exec")
    if not is_ok:
        return False, error, ""

    # 5 读取结果
    file_path = project_path / _LOAD_CASE_TXT_PATH / file_name
    file_path = file_path.with_suffix(".txt")

    return True, "", file_path
