"""属性管理器 - 统一管理坐标系、收缩徐变、阻尼、荷载-位移曲线等属性

用法:
    >>> from pyosis.property import property_manager
    >>> property_manager.coord.create_three_point(1, 0, 0, 0, 10, 0, 0, 0, 10, 0)
    >>> property_manager.creep_shrink.create(1, "CS1", 70.0, 7, 5.0, 3)
    >>> property_manager.damping.create_modal("Damp1", 0.05)
    >>> property_manager.pu_curve.create(1, "PU1", 0, 3, [0, 0.01, 0.02], [0, 100, 150])
"""

from __future__ import annotations

from typing import Literal

from .coordinate import (
    osis_coord_sys_three_point,
    osis_coord_sys_two_point_rotation,
    osis_coord_sys_del,
    osis_coord_sys_mod,
)
from .creep_shrink import (
    osis_creep_shrink,
    osis_creep_shrink_del,
    osis_creep_shrink_mod,
)
from .damping import (
    osis_damping_modal,
    osis_damping_rayleigh_custom,
    osis_damping_rayleigh_formula,
    osis_damping_del,
    osis_damping_mod,
)
from .pu_curve import (
    osis_pu_curve,
    osis_pu_curve_del,
    osis_pu_curve_mod,
)
from .component_thickness import osis_assign_component_thickness


# ──────────────────────────────────────────────
# 子管理器
# ──────────────────────────────────────────────


class CoordinateManager:
    """坐标系管理器"""

    def create_three_point(
        self,
        no: int,
        p1x: float, p1y: float, p1z: float,
        p2x: float, p2y: float, p2z: float,
        p3x: float, p3y: float, p3z: float,
    ) -> None:
        """创建或修改三点空间坐标系"""
        ok, err = osis_coord_sys_three_point(
            no, "TRIPT",
            p1x, p1y, p1z, p2x, p2y, p2z, p3x, p3y, p3z,
        )
        if not ok:
            raise RuntimeError(f"创建坐标系 {no} 失败: {err}")

    def create_two_point_rotation(
        self,
        no: int,
        p1x: float, p1y: float, p1z: float,
        p2x: float, p2y: float, p2z: float,
        angle: float,
    ) -> None:
        """创建或修改两点+旋转角空间坐标系"""
        ok, err = osis_coord_sys_two_point_rotation(
            no, "DBPT",
            p1x, p1y, p1z, p2x, p2y, p2z, angle,
        )
        if not ok:
            raise RuntimeError(f"创建坐标系 {no} 失败: {err}")

    def delete(self, no: int) -> None:
        """删除坐标系"""
        ok, err = osis_coord_sys_del(no)
        if not ok:
            raise RuntimeError(f"删除坐标系 {no} 失败: {err}")

    def renumber(self, old: str, new: str) -> None:
        """修改坐标系编号"""
        ok, err = osis_coord_sys_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改坐标系编号 {old} -> {new} 失败: {err}")

    def __repr__(self) -> str:
        return "CoordinateManager()"


class CreepShrinkManager:
    """收缩徐变管理器"""

    def create(
        self,
        no: int = 1,
        name: str = "收缩徐变1",
        avg_humidity: float = 70.0,
        birth_time: int = 7,
        type_coeff: float = 5.0,
        shrink_birth: int = 3,
    ) -> None:
        """创建或修改收缩徐变特性"""
        ok, err = osis_creep_shrink(
            no, name, avg_humidity, birth_time, type_coeff, shrink_birth,
        )
        if not ok:
            raise RuntimeError(f"创建收缩徐变特性 {no} 失败: {err}")

    def delete(self, no: int) -> None:
        """删除收缩徐变特性"""
        ok, err = osis_creep_shrink_del(no)
        if not ok:
            raise RuntimeError(f"删除收缩徐变特性 {no} 失败: {err}")

    def renumber(self, old: int, new: int) -> None:
        """修改收缩徐变特性编号"""
        ok, err = osis_creep_shrink_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改收缩徐变编号 {old} -> {new} 失败: {err}")

    def __repr__(self) -> str:
        return "CreepShrinkManager()"


class DampingManager:
    """阻尼管理器"""

    def create_modal(self, name: str, ksi: float) -> None:
        """创建或修改振型阻尼"""
        ok, err = osis_damping_modal(name, "modal", ksi)
        if not ok:
            raise RuntimeError(f"创建振型阻尼 {name} 失败: {err}")

    def create_rayleigh_custom(
        self, name: str, alpha: float, beta: float,
    ) -> None:
        """创建或修改Rayleigh阻尼（自定义因子）"""
        ok, err = osis_damping_rayleigh_custom(name, "ryl", 1, alpha, beta)
        if not ok:
            raise RuntimeError(f"创建Rayleigh阻尼 {name} 失败: {err}")

    def create_rayleigh_formula(
        self,
        name: str,
        ksii: float, ksij: float,
        wi: float, wj: float,
    ) -> None:
        """创建或修改Rayleigh阻尼（公式计算因子）"""
        ok, err = osis_damping_rayleigh_formula(name, "ryl", 0, ksii, ksij, wi, wj)
        if not ok:
            raise RuntimeError(f"创建Rayleigh阻尼 {name} 失败: {err}")

    def delete(self, name: str) -> None:
        """删除阻尼模型"""
        ok, err = osis_damping_del(name)
        if not ok:
            raise RuntimeError(f"删除阻尼模型 {name} 失败: {err}")

    def rename(self, old: str, new: str) -> None:
        """修改阻尼模型名称"""
        ok, err = osis_damping_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改阻尼名称 {old} -> {new} 失败: {err}")

    def __repr__(self) -> str:
        return "DampingManager()"


class PuCurveManager:
    """荷载-位移曲线管理器"""

    def create(
        self,
        no: int,
        name: str,
        curve_type: Literal[0, 1],
        num: int,
        displacement: list[float],
        force: list[float],
    ) -> None:
        """创建或修改荷载-位移曲线

        Args:
            no: 曲线编号
            name: 曲线名称
            curve_type: 0=力, 1=力矩
            num: 曲线点数
            displacement: 位移值列表
            force: 力（矩）值列表
        """
        ok, err = osis_pu_curve(no, name, curve_type, num, displacement, force)
        if not ok:
            raise RuntimeError(f"创建荷载-位移曲线 {no} 失败: {err}")

    def delete(self, no: int) -> None:
        """删除荷载-位移曲线"""
        ok, err = osis_pu_curve_del(no)
        if not ok:
            raise RuntimeError(f"删除荷载-位移曲线 {no} 失败: {err}")

    def renumber(self, old: int, new: int) -> None:
        """修改荷载-位移曲线编号"""
        ok, err = osis_pu_curve_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改荷载-位移曲线编号 {old} -> {new} 失败: {err}")

    def __repr__(self) -> str:
        return "PuCurveManager()"


# ──────────────────────────────────────────────
# 主管理器
# ──────────────────────────────────────────────


class PropertyManager:
    """属性管理器

    统一管理坐标系、收缩徐变、阻尼、荷载-位移曲线等属性。

    各子管理器通过属性访问：
        - coord:        坐标系管理器
        - creep_shrink: 收缩徐变管理器
        - damping:      阻尼管理器
        - pu_curve:     荷载-位移曲线管理器
    """

    def __init__(self) -> None:
        self._coord = CoordinateManager()
        self._creep_shrink = CreepShrinkManager()
        self._damping = DampingManager()
        self._pu_curve = PuCurveManager()

    @property
    def coord(self) -> CoordinateManager:
        """坐标系管理器"""
        return self._coord

    @property
    def creep_shrink(self) -> CreepShrinkManager:
        """收缩徐变管理器"""
        return self._creep_shrink

    @property
    def damping(self) -> DampingManager:
        """阻尼管理器"""
        return self._damping

    @property
    def pu_curve(self) -> PuCurveManager:
        """荷载-位移曲线管理器"""
        return self._pu_curve

    def assign_component_thickness(
        self,
        thickness: float,
        op: Literal["a", "s", "r"],
        elems: str,
    ) -> None:
        """分配或重置单个单元的理论厚度

        Args:
            thickness: 构件理论厚度
            op: a=添加, s=替换, r=移除
            elems: 待分配单元的编号，支持 *to* 格式
        """
        ok, err = osis_assign_component_thickness(thickness, op, elems)
        if not ok:
            raise RuntimeError(f"分配构件厚度失败: {err}")

    def __repr__(self) -> str:
        return "PropertyManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

property_manager = PropertyManager()
