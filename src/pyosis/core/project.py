# --- project相关的函数

from typing import Tuple
# from .engine import OSISEngine
from .client import osis_client

def get_project_directory() -> Tuple[bool, str]:
    return osis_client("GetProjectDirectory", {})