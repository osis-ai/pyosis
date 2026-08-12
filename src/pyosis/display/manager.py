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

from .interface import osis_control, osis_disp_ctrl, osis_plsm, osis_jpeg


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

    def control(self, action: str, arg: str | None = None, *values) -> None:
        """视图 / 界面控制（对应 ``/control,...``）。

        Args:
            action: 子命令，如 ``view``、``quickCreateModel``
            arg: 子命令参数；``view`` 时为 ``standard`` / ``top`` / ``right`` /
                ``front`` / ``zoom`` / ``move``
            *values: 附加参数。``view`` 子命令下：
                * ``zoom``: 缩放系数（值越小模型越小）
                * ``move``: (x, y) 像素偏移

        Raises:
            RuntimeError: 操作失败时抛出异常

        Examples:
            >>> display_manager.control("view", "top")
            >>> display_manager.control("view", "zoom", 0.8)
            >>> display_manager.control("view", "move", 30, 10)
        """
        ok, err = osis_control(action, arg, *values)
        if not ok:
            raise RuntimeError(f"界面控制失败: {err}")

    def set_view(
        self,
        view: Literal["standard", "top", "right", "front", "zoom", "move"] = "standard",
        *values,
    ) -> None:
        """切换视图方向。

        Args:
            view: 视图
                * ``standard``: 标准视图
                * ``top``: 俯视
                * ``right``: 右视
                * ``front``: 前视
                * ``zoom``: 缩放（附加系数：值越小模型越小）
                * ``move``: 平移（附加参数：x, y）
            *values: ``zoom`` 时为缩放系数，``move`` 时为 x, y 像素偏移

        Raises:
            RuntimeError: 操作失败时抛出异常

        Examples:
            >>> display_manager.set_view("top")
            >>> display_manager.set_view("front")
            >>> display_manager.set_view("zoom", 0.8)
            >>> display_manager.set_view("move", 30, 10)
        """
        self.control("view", view, *values)

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

    def capture(self, path: str) -> None:
        """截图工具（对应 ``jpeg,...``）。

        把当前画面截图保存到 ``path``。文件扩展名固定为 ``.jpg``。
        若仅传入文件名（不含目录分隔符），图片默认保存到
        ``<project_dir>/image/{path}.jpg``；传入完整路径则保存到对应位置。

        Args:
            path: 图片保存路径或文件名

        Raises:
            RuntimeError: 截图失败时抛出异常

        Examples:
            >>> display_manager.capture("D:\\reports\\fig1.jpg")
            >>> display_manager.capture("crack.jpg")    # 保存到 <project_dir>/image/crack.jpg
            >>> display_manager.capture("crack")        # 保存到 <project_dir>/image/crack.jpg
        """
        ok, err = osis_jpeg(path)
        if not ok:
            raise RuntimeError(f"截图失败: {err}")

    def __repr__(self) -> str:
        return "DisplayManager()"


# ═════════════════════════════════════════════
# 全局单例
# ═════════════════════════════════════════════

display_manager = DisplayManager()
