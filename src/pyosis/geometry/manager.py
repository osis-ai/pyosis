"""几何管理器 - 统一管理三维样条曲线

用法:
    >>> from pyosis.geometry import geometry_manager
    >>> geometry_manager.create_general("Lane1", "LIVE", [
    ...     0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    ...     10.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    ... ])
    >>> geometry_manager.delete("Lane1")
"""

from __future__ import annotations

from typing import Literal

from .interface import (
    osis_spline3d_general,
    osis_spline3d_natural,
    osis_spline3d_arc2d,
    osis_spline3d_arc3d,
    osis_spline3d_del,
)


class GeometryManager:
    """几何管理器"""

    def create_general(
        self,
        name: str,
        owner: Literal["LIVE", "TENDON"],
        coordinates: list[float],
    ) -> None:
        """创建或修改三维样条曲线（一般边界/GENERAL）

        Args:
            name: 曲线名称
            owner: 用途，LIVE=活载车道线，TENDON=钢束定义
            coordinates: 坐标序列，按 x, y, z, vx, vy, vz 顺序交替排列

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_general(name, "GENERAL", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建一般样条曲线 {name} 失败: {err}")

    def create_natural(
        self,
        name: str,
        owner: Literal["LIVE", "TENDON"],
        coordinates: list[float],
    ) -> None:
        """创建或修改三维样条曲线（自然边界/NATURAL）

        Args:
            name: 曲线名称
            owner: 用途
            coordinates: 坐标序列，按 x, y, z, R 顺序交替排列

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_natural(name, "NATURAL", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建自然样条曲线 {name} 失败: {err}")

    def create_arc2d(
        self,
        name: str,
        owner: str,
        coordinates: list[float],
    ) -> None:
        """创建或修改三维样条曲线（2D圆弧/ARC2D）

        Args:
            name: 曲线名称
            owner: 用途，TENDON=钢束定义
            coordinates: 坐标序列，按 x, y, R 顺序交替排列

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_arc2d(name, "ARC2D", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建2D圆弧 {name} 失败: {err}")

    def create_arc3d(
        self,
        name: str,
        owner: str,
        coordinates: list[float],
    ) -> None:
        """创建或修改三维样条曲线（3D圆弧/ARC3D）

        Args:
            name: 曲线名称
            owner: 用途，TENDON=钢束定义
            coordinates: 坐标序列，按 x, y, z, R 顺序交替排列

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_arc3d(name, "ARC3D", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建3D圆弧 {name} 失败: {err}")

    def delete(self, name: str) -> None:
        """删除三维样条曲线

        Args:
            name: 曲线名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_spline3d_del(name)
        if not ok:
            raise RuntimeError(f"删除样条曲线 {name} 失败: {err}")

    def __repr__(self) -> str:
        return "GeometryManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

geometry_manager = GeometryManager()
