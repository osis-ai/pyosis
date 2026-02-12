# --- project相关的函数

from typing import Tuple
from .engine import OSISEngine

def get_project_directory() -> Tuple[bool, str]:
    return OSISEngine.GetProjectDirectory()