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

from ..core import osis_run
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
)
from ..dynamic.modal import osis_mod_opt



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
        '''设置整体坐标系下三个方向的重力加速度分量

        Args:
            g (float): 重力加速度值，默认 9.8066 m/s²

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_acel(g)
        if not ok:
            raise RuntimeError(f"设置重力加速度失败: {err}")

    def export_apdl(self, path: str | None = None) -> None:
        '''导出当前前处理状态到 APDL .out 文件

        Args:
            path (str | None): 输出文件完整路径，可缺省；不传则使用程序当前路径

        Returns:
            None

        Raises:
            RuntimeError: 导出失败时抛出异常
        '''
        ok, err = osis_apdl(path)
        if not ok:
            raise RuntimeError(f"导出 APDL 文件失败: {err}")
        
    def import_apdl(self, path: str | None = None) -> None:
        '''读取 APDL .out / .sml 文件

        Args:
            path (str): 完整文件名，可缺省。path 中如果不输入绝对路径的话，
                默认使用程序执行文件所在的路径，例如 "D:\\\\Rbin\\\\X.sml"。

        Returns:
            None

        Raises:
            RuntimeError: 导入失败时抛出异常
        '''
        ok, err = osis_run(f"/input,{path}")
        if not ok:
            raise RuntimeError(f"导入 APDL 文件失败: {err}")


    # ── 材料效应开关 ────────────────────────────

    def set_calc_tendon(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否计算预应力效应

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_calc_tendon(enabled)
        if not ok:
            raise RuntimeError(f"设置预应力计算失败: {err}")

    def set_calc_concurrent_force(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否计算并发反力

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_calc_con_force(enabled)
        if not ok:
            raise RuntimeError(f"设置并发反力计算失败: {err}")

    def set_calc_shrink(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否计算收缩

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_calc_shrink(enabled)
        if not ok:
            raise RuntimeError(f"设置收缩计算失败: {err}")

    def set_calc_creep(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否计算徐变

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_calc_creep(enabled)
        if not ok:
            raise RuntimeError(f"设置徐变计算失败: {err}")

    def set_calc_shear(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否计算剪切变形

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_calc_shear(enabled)
        if not ok:
            raise RuntimeError(f"设置剪切计算失败: {err}")

    def set_calc_relaxation(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否计算钢束松弛

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_calc_rlx(enabled)
        if not ok:
            raise RuntimeError(f"设置钢束松弛计算失败: {err}")

    def set_mod_loc_coor(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否修改变截面单元局部坐标轴以计算内力/应力

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_mod_loc_coor(enabled)
        if not ok:
            raise RuntimeError(f"设置局部坐标轴修正失败: {err}")

    def set_inc_tendon(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否考虑钢束自重及钢束对截面几何特性的影响

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_inc_tendon(enabled)
        if not ok:
            raise RuntimeError(f"设置钢束自重影响失败: {err}")

    # ── 非线性分析 ──────────────────────────────

    def set_nonlinear(
        self,
        geom: Literal[0,1] = 0,
        link: Literal[0,1] = 0,
    ) -> None:
        '''设置非线性分析控制开关

        Args:
            geom (int): 是否打开几何非线性（大位移大转角），1=开，0=关
            link (int): 是否考虑非线性连接单元，1=考虑，0=不考虑

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_nl(1 if geom else 0, 1 if link else 0)
        if not ok:
            raise RuntimeError(f"设置非线性控制失败: {err}")

    def set_line_search(self, enabled: Literal[0,1] = 1) -> None:
        '''设置求解阶段的线性搜索开关

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_ln_srch(enabled)
        if not ok:
            raise RuntimeError(f"设置线性搜索失败: {err}")

    def set_auto_time_step(self, enabled: Literal[0,1] = 1) -> None:
        '''设置是否启用自动计算时间荷载步

        Args:
            enabled (int): 1=开，0=关

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_auto_ts(enabled)
        if not ok:
            raise RuntimeError(f"设置自动时间步长失败: {err}")

    def set_substitution_steps(self, ls: int, sbmx: int) -> None:
        '''指定荷载步数与最大荷载子步数

        Args:
            ls (int): 荷载步数
            sbmx (int): 最大荷载子步数

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常
        '''
        ok, err = osis_NSUBST(ls, sbmx)
        if not ok:
            raise RuntimeError(f"设置荷载步数失败: {err}")

    # ── 模态分析 ────────────────────────────────

    def set_modal_opt(self, num: int = 1) -> None:
        '''定义模态分析所需计算的特征值最大数目

        Args:
            num (int): 需要计算的特征值最大数目，缺省值：1

        Returns:
            None

        Raises:
            RuntimeError: 设置失败时抛出异常

        Examples:
            >>> control_manager.set_modal_opt(5)  # 设置计算前 5 阶模态
        '''
        ok, err = osis_mod_opt(num)
        if not ok:
            raise RuntimeError(f"设置模态分析参数失败: {err}")

    def __repr__(self) -> str:
        return "ControlManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

control_manager = ControlManager()
