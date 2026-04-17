# --- project相关的函数

import os
from pathlib import Path
from typing import Tuple
# from .engine import OSISEngine
from ..core.client import osis_client

def get_project_directory() -> 'str | None':
    isok, path = osis_client("GetProjectDirectory", {})
    return path if isok else None

def open_project() -> Tuple[bool, str]:
    ...

def create_project() -> Tuple[bool, str]:
    ...

# class OSISProject():
#     def __init__(self, path):
#         self.root_path = self._parse_project_path(path)
#         # 路径对象（方便后续操作）
#         self.root_path_obj = Path(self.root_path)

#     def _parse_project_path(self, path: str) -> str:
#         """
#         私有方法：解析项目路径（核心逻辑）
#         1. 如果是绝对路径 → 直接返回
#         2. 如果是项目名 → 拼接当前工作目录返回
#         """
#         # 判断是否为完整绝对路径
#         if os.path.isabs(path):
#             return path
        
#         # 不是绝对路径 → 在当前目录创建项目
#         current_dir = os.getcwd()
#         return os.path.join(current_dir, path)

#     def open(self):
#         return osis_client("GetProjectDirectory", {})

#     def create(self):
#         return osis_client("GetProjectDirectory", {})

#     def close(self):
#         return osis_client("GetProjectDirectory", {})
    
#     def clear(self):
#         ...

#     def __str__(self):
#         return f"OSISProject: {self.root_path}"

#     def __repr__(self):
#         return self.__str__()