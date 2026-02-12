# --- project相关的函数

from .engine import OSISEngine

def get_project_directory():
    return OSISEngine.GetProjectDirectory()