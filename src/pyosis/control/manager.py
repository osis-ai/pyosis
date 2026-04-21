"""控制管理器 - 统一管理全局参数、分析设置和项目控制

设计理念：
- 隐藏底层命令接口细节，提供原生 Python 风格 API
- 集中管理所有全局开关和参数设置
- 提供项目级操作（运行、保存、导出等）

用法:
    >>> from pyosis.control import control_manager
    >>> control_manager.set_unit("m", "kN", "C")
    >>> control_manager.set_calc_creep(True)
    >>> control_manager.set_nonlinear(geom=True)
    >>> control_manager.run()
"""

from __future__ import annotations

from typing import Literal

from .control import (
    osis_acel,
    osis_calc_tendon,
    osis_calc_con_force,
    osis_calc_shrink,
    osis_calc_creep,
    osis_calc_shear,
    osis_calc_rlx,
    osis_mod_loc_coor,
    osis_inc_tendon,
)
from .io import osis_apdl
from .nonlinear import (
    osis_nl,
    osis_ln_srch,
    osis_auto_ts,
    osis_NSUBST,
    osis_mod_opt,
)
# from ..general.project import (
#     osis_new_project,
#     osis_open_project,
#     osis_save_project,
#     osis_close_project,
# )
# from ..general.project import osis_get_project_info


class ControlManager:
    """控制管理器

    统一管理全局参数、分析设置和项目级操作。
    """

    # ── 单位与项目 ──────────────────────────────

    # def set_unit(
    #     self,
    #     length: str = "m",
    #     force: str = "kN",
    #     temperature: str = "C",
    # ) -> None:
    #     """设置单位制

    #     Args:
    #         length: 长度单位
    #         force: 力单位
    #         temperature: 温度单位
    #     """
    #     ok, err = osis_set_unit(length, force, temperature)
    #     if not ok:
    #         raise RuntimeError(f"设置单位制失败: {err}")


    def set_gravity_acceleration(self, g: float = 9.8066) -> None:
        """设置重力加速度值，默认 9.8066 m/s²"""
        ok, err = osis_acel(g)
        if not ok:
            raise RuntimeError(f"设置重力加速度失败: {err}")

    def export_apdl(self, path: str | None = None) -> None:
        """导出前处理状态为 .out 文件"""
        ok, err = osis_apdl(path)
        if not ok:
            raise RuntimeError(f"导出 APDL 文件失败: {err}")

    # ── 材料效应开关 ────────────────────────────

    def set_calc_tendon(self, enabled: bool = True) -> None:
        """是否计算预应力"""
        ok, err = osis_calc_tendon(enabled)
        if not ok:
            raise RuntimeError(f"设置预应力计算失败: {err}")

    def set_calc_concurrent_force(self, enabled: bool = True) -> None:
        """是否计算并发反力"""
        ok, err = osis_calc_con_force(enabled)
        if not ok:
            raise RuntimeError(f"设置并发反力计算失败: {err}")

    def set_calc_shrink(self, enabled: bool = True) -> None:
        """是否计算收缩"""
        ok, err = osis_calc_shrink(enabled)
        if not ok:
            raise RuntimeError(f"设置收缩计算失败: {err}")

    def set_calc_creep(self, enabled: bool = True) -> None:
        """是否计算徐变"""
        ok, err = osis_calc_creep(enabled)
        if not ok:
            raise RuntimeError(f"设置徐变计算失败: {err}")

    def set_calc_shear(self, enabled: bool = True) -> None:
        """是否计算剪切"""
        ok, err = osis_calc_shear(enabled)
        if not ok:
            raise RuntimeError(f"设置剪切计算失败: {err}")

    def set_calc_relaxation(self, enabled: bool = True) -> None:
        """是否计算钢束松弛"""
        ok, err = osis_calc_rlx(enabled)
        if not ok:
            raise RuntimeError(f"设置钢束松弛计算失败: {err}")

    def set_mod_loc_coor(self, enabled: bool = True) -> None:
        """是否修改变截面单元局部坐标轴来计算内力/应力"""
        ok, err = osis_mod_loc_coor(enabled)
        if not ok:
            raise RuntimeError(f"设置局部坐标轴修正失败: {err}")

    def set_inc_tendon(self, enabled: bool = True) -> None:
        """是否考虑钢束自重及钢束对截面几何特性的影响"""
        ok, err = osis_inc_tendon(enabled)
        if not ok:
            raise RuntimeError(f"设置钢束自重影响失败: {err}")

    # ── 非线性分析 ──────────────────────────────

    def set_nonlinear(
        self,
        geom: bool = False,
        link: bool = False,
    ) -> None:
        """设置非线性控制开关

        Args:
            geom: 打开几何非线性（大位移大转角）
            link: 考虑非线性连接单元
        """
        ok, err = osis_nl(1 if geom else 0, 1 if link else 0)
        if not ok:
            raise RuntimeError(f"设置非线性控制失败: {err}")

    def set_line_search(self, enabled: bool = True) -> None:
        """设置线性搜索开关"""
        ok, err = osis_ln_srch(enabled)
        if not ok:
            raise RuntimeError(f"设置线性搜索失败: {err}")

    def set_auto_time_step(self, enabled: bool = True) -> None:
        """设置是否自动计算时间荷载步"""
        ok, err = osis_auto_ts(enabled)
        if not ok:
            raise RuntimeError(f"设置自动时间步长失败: {err}")

    def set_substitution_steps(self, nls: int, nsbmx: int) -> None:
        """指定荷载步数和最大荷载子步数"""
        ok, err = osis_NSUBST(nls, nsbmx)
        if not ok:
            raise RuntimeError(f"设置荷载步数失败: {err}")

    # ── 模态分析 ────────────────────────────────

    def set_modal_opt(self, n_mod: int = 1) -> None:
        """定义模态分析所需的特征值最大数目"""
        ok, err = osis_mod_opt(n_mod)
        if not ok:
            raise RuntimeError(f"设置模态分析参数失败: {err}")

    def __repr__(self) -> str:
        return "ControlManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

control_manager = ControlManager()
