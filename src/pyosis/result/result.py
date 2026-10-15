from itertools import islice
from pathlib import Path

from pyosis.project import interface
from pyosis.core import command

_LOAD_CASE_FILE_PATH = "Temperary"
_LOAD_CASE_TXT_PATH = "Temperary"


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


def txt_file_path(file_name, e_type, cmd, min_lines: int = 1) -> tuple[bool, str, str]:
    """
    用于获取工况和包络结果的txt路径

    Args:
        file_name: 文件名称
        e_type: 指令名称
        cmd: 命令流
        min_lines: 结果 txt 至少要有的行数（抬头 + 表头）。不足即按失败报出。

    Returns:
        tuple (bool, str, str): 是否成功，失败原因，txt文件路径
    """
    # 1 获取项目目录
    project_path = interface.get_project_directory()
    if not project_path:
        return False, "获取文件夹失败", ""

    project_path = Path(project_path)

    # 2 工况文件路径
    load_case_file_path = project_path / _LOAD_CASE_FILE_PATH / file_name

    # 3 生成命令
    str_cmd = cmd.format(out_file_path=load_case_file_path, e_type=e_type, check_file_name=file_name)

    # 4 执行命令
    is_ok, osis_msg = command.osis_run(str_cmd, mode="exec")
    if not is_ok:
        return False, osis_msg, ""

    # 5 读取结果
    file_path = project_path / _LOAD_CASE_TXT_PATH / file_name
    file_path = file_path.with_suffix(".txt")

    # 6 命令成功不等于写出了表，这里替下游把空文件挡下来
    problem = _output_problem(file_path, min_lines)
    if problem:
        osis_note = osis_msg.strip() or "（OSIS 未返回错误或警告）"
        return False, f"{problem}；OSIS 返回：{osis_note}；命令流：{str_cmd}", ""

    return True, "", file_path
