"""显示管理器 - 控制显隐、视图方向与显示开关

设计理念：
- 隐藏底层命令接口细节，提供原生 Python 风格 API
- 无状态设计，操作直接提交到 OSIS

用法:
    >>> from pyosis.display import display_manager
    >>> display_manager.disp_ctrl("bc", "all", "all", 1)
    >>> display_manager.set_view("top")
    >>> display_manager.set_plsm(1)
"""

from __future__ import annotations

from typing import Literal, Sequence, Union

from .interface import osis_control, osis_disp_ctrl, osis_plsm


class DisplayManager:
    """显示管理器

    控制边界 / 荷载 / 钢束显隐、视图方向与显示开关。
    """

    def disp_ctrl(
        self,
        obj: Literal["bc", "boundary", "lg", "load", "td", "tendon"],
        type: str,
        ids: Union[str, int, Sequence[Union[str, int]]],
        show: Literal[0, 1] = 1,
    ) -> None:
        """控制边界 / 荷载 / 钢束的显示与隐藏。

        Args:
            obj: 对象类型
                * ``bc`` / ``boundary`` = 边界
                * ``lg`` / ``load`` = 荷载
                * ``td`` / ``tendon`` = 钢束
            type: 子类型（``all`` 或具体类型，见 ``osis_disp_ctrl`` 文档）
            ids: 编号或名称（``all`` / 单个 / 序列）
            show: ``0`` = 隐藏，``1`` = 显示

        Raises:
            RuntimeError: 操作失败时抛出异常

        Examples:
            >>> display_manager.disp_ctrl("bc", "all", "all", 1)
            >>> display_manager.disp_ctrl("bc", "general", [1, 2, "3to10"], 1)
            >>> display_manager.disp_ctrl("lg", "nforce", "all", 1)
            >>> display_manager.disp_ctrl("td", "all", ["T1", "T2"], 1)
        """
        ok, err = osis_disp_ctrl(obj, type, ids, show)
        if not ok:
            raise RuntimeError(f"显示控制失败: {err}")

    def control(self, action: str, arg: str | None = None) -> None:
        """视图 / 界面控制（对应 ``/control,...``）。

        Args:
            action: 子命令，如 ``view``、``quickCreateModel``
            arg: 子命令参数；``view`` 时为 ``standard`` / ``top`` / ``right`` / ``front``

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_control(action, arg)
        if not ok:
            raise RuntimeError(f"界面控制失败: {err}")

    def set_view(
        self,
        view: Literal["standard", "top", "right", "front"] = "standard",
    ) -> None:
        """切换视图方向。

        Args:
            view: ``standard`` / ``top`` / ``right`` / ``front``

        Raises:
            RuntimeError: 操作失败时抛出异常

        Examples:
            >>> display_manager.set_view("top")
            >>> display_manager.set_view("front")
        """
        self.control("view", view)

    def set_plsm(self, enabled: Literal[0, 1] = 1) -> None:
        """显示开关（Plsm）。

        Args:
            enabled: ``0`` = 关，``1`` = 开

        Raises:
            RuntimeError: 操作失败时抛出异常

        Examples:
            >>> display_manager.set_plsm(1)
            >>> display_manager.set_plsm(0)
        """
        ok, err = osis_plsm(enabled)
        if not ok:
            raise RuntimeError(f"设置 Plsm 失败: {err}")

    def __repr__(self) -> str:
        return "DisplayManager()"


# ═════════════════════════════════════════════
# 全局单例
# ═════════════════════════════════════════════

display_manager = DisplayManager()
