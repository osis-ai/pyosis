"""厚度管理器 - 统一管理板或壳的厚度特性

用法:
    >>> from pyosis.thickness import thickness_manager
    >>> thickness_manager.create(1, 0.3, 0.3)
    >>> thickness_manager.delete(1)
"""

from __future__ import annotations

from .interface import (
    osis_shell_thickness,
    osis_shell_thickness_del,
    osis_shell_thickness_mod,
)


class ThicknessManager:
    """厚度管理器"""

    def create(
        self,
        no: int,
        in_plane: float,
        out_plane: float,
    ) -> None:
        """创建或修改板或壳的厚度特性

        Args:
            no: 厚度特性编号
            in_plane: 面内厚度
            out_plane: 面外厚度

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_shell_thickness(no, in_plane, out_plane)
        if not ok:
            raise RuntimeError(f"创建厚度特性 {no} 失败: {err}")

    def delete(self, no: int) -> None:
        """删除板或壳的厚度特性

        Args:
            no: 厚度特性编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_shell_thickness_del(no)
        if not ok:
            raise RuntimeError(f"删除厚度特性 {no} 失败: {err}")

    def renumber(self, old: str, new: str) -> None:
        """修改厚度特性编号

        Args:
            old: 旧编号
            new: 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_shell_thickness_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改厚度特性编号 {old} -> {new} 失败: {err}")

    def __repr__(self) -> str:
        return "ThicknessManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

thickness_manager = ThicknessManager()
