"""项目管理器 - 统一管理项目操作

用法:
    >>> from pyosis.project import project_manager
    >>> project_manager.create(type=1, filepath="D:/Models/bridge.sis")
    >>> project_manager.open("D:/Models/bridge.sis")
    >>> project_manager.save()
    >>> project_manager.save("D:/Models/bridge.sis")
    >>> project_manager.save_as("D:/Models/bridge_v2.sis")
    >>> project_manager.close()
    >>> project_manager.get_directory()
"""

from __future__ import annotations

import os

from .interface import (
    create_project,
    open_project,
    save_project,
    save_project_as,
    close_osis,
    get_project_directory,
)


class ProjectManager:
    """项目管理器

    统一管理项目的创建、打开、保存和查询。
    """

    def create(self, type: int = 101, filepath: str = "") -> None:
        '''创建新项目

        Args:
            type (int): 项目类型，默认 101
            filepath (str): 项目文件路径，将自动转换为绝对路径

        Returns:
            None

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = create_project(type, os.path.abspath(filepath))
        if not ok:
            raise RuntimeError(f"创建项目失败: {err}")

    def open(self, filepath: str) -> None:
        '''打开已存在的项目文件

        Args:
            filepath (str): 项目文件路径，将自动转换为绝对路径

        Returns:
            None

        Raises:
            RuntimeError: 打开失败时抛出异常
        '''
        ok, err = open_project(os.path.abspath(filepath))
        if not ok:
            raise RuntimeError(f"打开项目失败: {err}")

    def save(self, filepath: str = "") -> None:
        '''保存当前项目

        Args:
            filepath (str): 工程文件路径。为空时使用当前项目路径；
                非空时使用传入路径，并将转换为绝对路径。

        Returns:
            None

        Raises:
            RuntimeError: 保存失败时抛出异常
        '''
        if not filepath:
            filepath = self._current_project_file()
        ok, err = save_project(os.path.abspath(filepath))
        if not ok:
            raise RuntimeError(f"保存项目失败: {err}")

    def save_as(self, filepath: str) -> None:
        '''将当前项目另存到新路径

        Args:
            filepath (str): 新的项目文件路径，将自动转换为绝对路径；
                不能与当前工程文件路径相同

        Returns:
            None

        Raises:
            RuntimeError: 另存为失败时抛出异常
        '''
        ok, err = save_project_as(os.path.abspath(filepath))
        if not ok:
            raise RuntimeError(f"另存为失败: {err}")

    def close(self) -> None:
        '''关闭当前 OSIS 项目

        Returns:
            None

        Raises:
            RuntimeError: 关闭失败时抛出异常
        '''
        ok, err = close_osis()
        if not ok:
            raise RuntimeError(f"关闭软件失败: {err}")

    def get_directory(self) -> str:
        '''获取当前项目所在目录路径

        Returns:
            str: 项目目录路径

        Raises:
            RuntimeError: 获取失败时抛出异常
        '''
        try:
            return get_project_directory()
        except Exception as e:
            raise RuntimeError(f"获取项目目录失败: {e}")

    def _current_project_file(self) -> str:
        """由当前项目目录推导工程文件路径（目录同名 .sis）。"""
        directory = self.get_directory().rstrip("\\/")
        return f"{directory}.sis"

    def __repr__(self) -> str:
        return "ProjectManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

project_manager = ProjectManager()
