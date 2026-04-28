"""几何管理器 - 统一管理三维样条曲线

用法:
    >>> from pyosis.geometry import geometry_manager
    >>> geometry_manager.create_general("Lane1", "LIVE", [
    ...     0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    ...     10.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    ... ])
    >>> geometry_manager.delete("Lane1")
    >>> # 查询
    >>> splines = geometry_manager.all()
    >>> spline = geometry_manager.get("Lane1")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from ..core.client import osis_client
from .interface import (
    osis_spline3d_general,
    osis_spline3d_natural,
    osis_spline3d_arc2d,
    osis_spline3d_arc3d,
    osis_spline3d_del,
)


# 与服务端 splineType 字段对应
class SplineType(Enum):
    """样条曲线类型"""
    Unassigned = 0  # 未分配
    General = 1     # 一般边界
    Natural = 2     # 自然边界
    Arc3D = 3       # 3D圆弧
    Arc2D = 4       # 2D圆弧


SPLINE_TYPE_NAMES: dict[int, str] = {
    0: "UNASSIGNED",
    1: "General",
    2: "Natural",
    3: "Arc3D",
    4: "Arc2D",
}


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Spline:
    """样条曲线数据类

    由 GeometryManager 内部创建，用户不应直接实例化。
    字段与 HTTP 接口 GetAllSplineInfo 返回的 JSON 一一对应。
    """

    no: int | None = None            # 编号
    name: str | None = None          # 名称
    owner: int | None = None         # 用途（0=其他, 1=活载, 2=钢束）
    spline_type: SplineType | None = None  # 曲线类型
    related_lanes: list[str] | None = None       # 关联车道
    related_tendon_shapes: list[str] | None = None  # 关联钢束形状
    points: list[list[float]] | None = None      # 统一格式的点列表（坐标值列表）

    @classmethod
    def _from_dict(cls, d: dict) -> Spline:
        """从接口 dict 构造 Spline 对象（内部使用）"""

        def _extract_points(pts: list[dict], s_type: SplineType | None) -> list[list[float]]:
            """根据曲线类型提取坐标值列表"""
            result = []
            for pt in pts:
                if s_type == SplineType.General:
                    # General: x, y, z, tx, ty, tz
                    result.append([
                        pt.get("x"),
                        pt.get("y"),
                        pt.get("z"),
                        pt.get("tx"),
                        pt.get("ty"),
                        pt.get("tz"),
                    ])
                elif s_type == SplineType.Natural:
                    # Natural: x, y, z
                    result.append([
                        pt.get("x"),
                        pt.get("y"),
                        pt.get("z"),
                    ])
                elif s_type == SplineType.Arc3D:
                    # Arc3D: x, y, z, r
                    result.append([
                        pt.get("x"),
                        pt.get("y"),
                        pt.get("z"),
                        pt.get("r"),
                    ])
                elif s_type == SplineType.Arc2D:
                    # Arc2D: x, y, r
                    result.append([
                        pt.get("x"),
                        pt.get("y"),
                        pt.get("r"),
                    ])
                else:
                    # 未知类型，提取所有可能字段
                    result.append([
                        pt.get("x"),
                        pt.get("y"),
                        pt.get("z"),
                        pt.get("r"),
                        pt.get("tx"),
                        pt.get("ty"),
                        pt.get("tz"),
                    ])
            return result

        spline_type = SplineType(d.get("splineType"))
        points_raw = d.get("points")
        points = _extract_points(points_raw, spline_type) if points_raw else None

        return cls(
            no=d.get("no"),
            name=d.get("name"),
            owner=d.get("owner"),
            spline_type=spline_type,
            related_lanes=d.get("relatedLanes"),
            related_tendon_shapes=d.get("relatedTendonShapes"),
            points=points,
        )

    def __repr__(self) -> str:
        return (
            f"Spline(no={self.no}, name={self.name!r}, "
            f"type={self.spline_type.name if self.spline_type else None}, "
            f"points={len(self.points) if self.points else 0})"
        )


# ──────────────────────────────────────────────
# GeometryManager
# ──────────────────────────────────────────────


class GeometryManager:
    """几何管理器

    统一管理三维样条曲线的增删改查。
    """

    def _load(self) -> list[Spline]:
        """从服务端加载所有样条曲线信息"""
        resp = osis_client("GetAllSplineInfo", {})
        if not resp["success"]:
            raise RuntimeError(resp["error"])
        
        splines = [
            Spline._from_dict(d)
            for d in resp.get("data", [])
            if isinstance(d, dict) and "no" in d
        ]
        return splines

    # ── 增删改 ────────────────────────────────

    def create_general(
        self,
        name: str,
        owner: Literal["LIVE", "TENDON"],
        coordinates: list[float],
    ) -> Spline:
        """创建或修改三维样条曲线（一般边界/GENERAL）

        Args:
            name: 曲线名称
            owner: 用途，LIVE=活载车道线，TENDON=钢束定义
            coordinates: 坐标序列，按 x, y, z, vx, vy, vz 顺序交替排列

        Returns:
            创建后的 Spline 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_general(name, "GENERAL", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建一般样条曲线 {name} 失败: {err}")
        return self.get(name)

    def create_natural(
        self,
        name: str,
        owner: Literal["LIVE", "TENDON"],
        coordinates: list[float],
    ) -> Spline:
        """创建或修改三维样条曲线（自然边界/NATURAL）

        Args:
            name: 曲线名称
            owner: 用途
            coordinates: 坐标序列，按 x, y, z 顺序交替排列

        Returns:
            创建后的 Spline 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_natural(name, "NATURAL", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建自然样条曲线 {name} 失败: {err}")
        return self.get(name)

    def create_arc2d(
        self,
        name: str,
        owner: str,
        coordinates: list[float],
    ) -> Spline:
        """创建或修改三维样条曲线（2D圆弧/ARC2D）

        Args:
            name: 曲线名称
            owner: 用途，TENDON=钢束定义
            coordinates: 坐标序列，按 x, y, R 顺序交替排列

        Returns:
            创建后的 Spline 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_arc2d(name, "ARC2D", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建2D圆弧 {name} 失败: {err}")
        return self.get(name)

    def create_arc3d(
        self,
        name: str,
        owner: str,
        coordinates: list[float],
    ) -> Spline:
        """创建或修改三维样条曲线（3D圆弧/ARC3D）

        Args:
            name: 曲线名称
            owner: 用途，TENDON=钢束定义
            coordinates: 坐标序列，按 x, y, z, R 顺序交替排列

        Returns:
            创建后的 Spline 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_spline3d_arc3d(name, "ARC3D", owner, *coordinates)
        if not ok:
            raise RuntimeError(f"创建3D圆弧 {name} 失败: {err}")
        return self.get(name)

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

    # ── 查询 ──────────────────────────────────

    def get(self, name: str | list[str]) -> Spline | list[Spline | None] | None:
        """根据名称获取单个或多个样条曲线

        Args:
            name: 曲线名称或名称列表

        Returns:
            单个 Spline 对象，或 Spline 对象列表
        """
        if isinstance(name, str):
            names = [name]
        elif isinstance(name, list):
            names = name
        else:
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetSplineInfoByNames", {"names": names})
        if not resp["success"]:
            raise RuntimeError(f"{resp['error']}")
        
        splines = [
            Spline._from_dict(d) if d else None
            for d in resp.get("data", [])
        ]
        
        if len(splines) == 0:
            return None
        elif len(splines) == 1:
            return splines[0]
        return splines

    def all(self) -> list[Spline]:
        """获取所有样条曲线"""
        return self._load()

    def count(self) -> int:
        """获取样条曲线总数"""
        return len(self._load())

    def __repr__(self) -> str:
        return "GeometryManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

geometry_manager = GeometryManager()
