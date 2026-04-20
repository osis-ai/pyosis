# --- project相关的函数

from typing import Tuple
from ..core.client import osis_client
from ..core import REGISTRY

def get_project_directory() -> 'str | None':
    response = osis_client("GetProjectDirectory", {})
    if response["success"]:
        return response["path"]
    raise Exception(response["error"])

@REGISTRY.register("/Open")
def open_project(filepath) -> Tuple[bool, str]:
    """
    打开项目
    
    Args:
        filepath: 项目文件路径

    Returns: 
        Tuple[bool, str]
    """
    pass

@REGISTRY.register("/Create")
def create_project(type, filePath) -> Tuple[bool, str]:
    """
    创建项目
    
    Args:
        type: 项目类型， 默认 1
        filepath: 项目文件路径

    Returns: 
        Tuple[bool, str]
    """
    pass

@REGISTRY.register("/Save")
def save_project(filePath) -> Tuple[bool, str]:
    """
    保存项目
    
    Args:
        filepath: 为空或者当前工程文件路径

    Returns: 
        Tuple[bool, str]
    """
    pass

@REGISTRY.register("/SaveAs")
def save_project_as(filePath) -> Tuple[bool, str]:
    """
    在 filePath 新建一个项目
    
    Args:
        filepath: 项目文件路径，不能使用当前工程文件路径

    Returns: 
        Tuple[bool, str]
    """
    pass
