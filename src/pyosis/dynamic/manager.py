"""动力分析管理器 - 统一管理荷载转换质量、模态分析和地震反应谱

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 支持荷载转换质量、自振模态分析、地震反应谱分析
"""

from __future__ import annotations

from typing import Literal

from .load_to_mass import (
    osis_ltm_anal,
    osis_ltm_anal_del,
    osis_ltm_anal_mod,
    osis_ltm_anal_inc,
)
from .modal import osis_mod_opt
from .seismic import (
    osis_seis_rsp_spec_import,
    osis_seis_rsp_spec_code,
    osis_seis_rsp_spec_del,
    osis_seis_rsp_spec_mod,
    osis_rspec_anal,
    osis_rspec_anal_del,
    osis_rspec_anal_mod,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


class LoadToMassItem:
    """荷载转换质量项信息"""
    
    def __init__(
        self,
        lc_name: str,
        mass_factor: float,
        g: float,
        bx: Literal[0, 1] = 1,
        by: Literal[0, 1] = 1,
        bz: Literal[0, 1] = 1,
        bnf: Literal[0, 1] = 1,
        bbf: Literal[0, 1] = 1,
        bsf: Literal[0, 1] = 1,
    ):
        self.lc_name = lc_name
        self.mass_factor = mass_factor
        self.g = g
        self.bx = bx
        self.by = by
        self.bz = bz
        self.bnf = bnf
        self.bbf = bbf
        self.bsf = bsf
    
    def __repr__(self) -> str:
        return (f"LoadToMassItem(lc={self.lc_name!r}, factor={self.mass_factor}, "
                f"g={self.g}, dir=({self.bx},{self.by},{self.bz}))")


class SpectrumData:
    """反应谱数据点"""
    
    def __init__(self, period: float, value: float):
        self.period = period
        self.value = value
    
    def __repr__(self) -> str:
        return f"SpectrumData(T={self.period}, S={self.value})"


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class DynamicManager:
    """动力分析管理器

    统一管理荷载转换质量、自振模态分析和地震反应谱分析。

    用法:
        >>> from pyosis.dynamic import dynamic_manager
        >>> # 荷载转换质量
        >>> dynamic_manager.create_ltm("LTM1")
        >>> dynamic_manager.add_ltm("LTM1", "D", 1.0, 9.806)
        >>> # 模态分析
        >>> dynamic_manager.set_modal_opt(10)
        >>> # 地震反应谱
        >>> data = [(0.1, 0.5), (0.2, 0.8)]
        >>> dynamic_manager.create_rsp_spec("RS1", "A", 9.806, data)
        >>> # 反应谱工况
        >>> dynamic_manager.create_rspec_anal("RA1", "RS1", num=10)
    """

    def __init__(self) -> None:
        ...

    # ── 荷载转换质量管理 ─────────────────────────

    def create_ltm(self, name: str) -> None:
        """创建或修改荷载转换质量总体信息。

        Args:
            name: 荷载转换质量标识名称

        Note:
            - 无论荷载工况是否被激活，均可转化为质量
        """
        ok, err = osis_ltm_anal(name)
        if not ok:
            raise RuntimeError(f"创建荷载转换质量 {name} 失败: {err}")

    def delete_ltm(self, name: str) -> None:
        """删除荷载转换质量。

        Args:
            name: 荷载转换质量标识名称
        """
        ok, err = osis_ltm_anal_del(name)
        if not ok:
            raise RuntimeError(f"删除荷载转换质量 {name} 失败: {err}")

    def renumber_ltm(self, old_no: int, new_no: int) -> None:
        """修改荷载转换质量编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_ltm_anal_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改荷载转换质量编号 {old_no} -> {new_no} 失败: {err}")

    def add_ltm(
        self,
        name: str,
        lc_name: str,
        mass_factor: float,
        g: float,
        bx: Literal[0, 1] = 1,
        by: Literal[0, 1] = 1,
        bz: Literal[0, 1] = 1,
        bnf: Literal[0, 1] = 1,
        bbf: Literal[0, 1] = 1,
        bsf: Literal[0, 1] = 1,
    ) -> None:
        """添加荷载转换质量项。

        Args:
            name: 荷载转换质量标识
            lc_name: 荷载工况名称
            mass_factor: 质量系数
            g: 重力加速度值
            bx: 质量方向，0=不考虑X向，1=考虑X向
            by: 质量方向，0=不考虑Y向，1=考虑Y向
            bz: 质量方向，0=不考虑Z向，1=考虑Z向
            bnf: 0=不转换节点荷载，1=转换节点荷载
            bbf: 0=不转换梁荷载，1=转换梁荷载
            bsf: 0=不转换面荷载，1=转换面荷载

        Note:
            - 无论荷载工况是否被激活，均可转化为质量
        """
        ok, err = osis_ltm_anal_inc(
            name, "a", lc_name, mass_factor, g, bx, by, bz, bnf, bbf, bsf
        )
        if not ok:
            raise RuntimeError(f"添加荷载转换质量项 {lc_name} 到 {name} 失败: {err}")

    def remove_ltm(self, name: str, lc_name: str) -> None:
        """移除荷载转换质量项。

        Args:
            name: 荷载转换质量标识
            lc_name: 荷载工况名称
        """
        ok, err = osis_ltm_anal_inc(name, "r", lc_name, 0.0, 0.0)
        if not ok:
            raise RuntimeError(f"移除荷载转换质量项 {lc_name} 从 {name} 失败: {err}")

    # ── 自振模态分析 ────────────────────────────

    def set_modal_opt(self, num: int = 1) -> None:
        """定义模态分析所需的特征值最大数目。

        Args:
            num: 需要计算的特征值最大数目，缺省值：1
        """
        ok, err = osis_mod_opt(num)
        if not ok:
            raise RuntimeError(f"设置模态分析选项失败: {err}")

    # ── 地震反应谱管理 ───────────────────────────

    def create_rsp_spec(
        self,
        name: str,
        spec_type: Literal["N", "A", "V", "D"],
        g: float,
        spectrum_data: list[tuple[float, float]],
    ) -> None:
        """创建导入类型地震反应谱。

        Args:
            name: 反应谱名称
            spec_type: 谱类型，N=无量纲加速度谱，A=加速度谱，V=速度谱，D=位移谱
            g: 输入g值
            spectrum_data: 反应谱数据列表，每个元素为 (周期, 谱值) 元组
        """
        n_num = len(spectrum_data)
        ok, err = osis_seis_rsp_spec_import(name, spec_type, g, n_num, spectrum_data)
        if not ok:
            raise RuntimeError(f"创建地震反应谱 {name} 失败: {err}")

    def create_rsp_spec_code(
        self,
        name: str,
        spec_type: Literal["N", "A", "V", "D"],
        g: float,
        code: str = "JTGT_2231_01_2020",
        bridge_type: Literal["A", "B", "C", "D"] = "A",
        is_long_span: Literal[0, 1] = 0,
        level: Literal[0, 1] = 0,
        intensity: float = 0.2,
        site: Literal[0, 1, 2, 3, 4] = 2,
        direction: Literal[0, 1] = 0,
        period: float = 0.35,
        ksi: float = 0.05,
        t: float = 6.0,
        delta_t: float = 0.01,
    ) -> None:
        """创建按规范生成类型地震反应谱。

        Args:
            name: 反应谱名称
            spec_type: 谱类型，N=无量纲加速度谱，A=加速度谱，V=速度谱，D=位移谱
            g: 输入g值
            code: 规范名称，如 "JTGT_2231_01_2020"
            bridge_type: 桥梁类别，A/B/C/D
            is_long_span: 0=非高速公路和一级公路上的B类大桥特大桥，1=高速公路和一级公路上的B类大桥特大桥
            level: 设防水准，0=E1，1=E2
            intensity: 设防烈度
            site: 场地类型，0=I0, 1=I1, 2=Ⅱ, 3=Ⅲ, 4=Ⅳ
            direction: 方向，0=水平，1=竖直
            period: 分区特征周期
            ksi: 阻尼比
            t: 最长周期
            delta_t: 周期间隔
        """
        ok, err = osis_seis_rsp_spec_code(
            name, spec_type, g,
            code, bridge_type, is_long_span, level, intensity,
            site, direction, period, ksi, t, delta_t
        )
        if not ok:
            raise RuntimeError(f"创建规范地震反应谱 {name} 失败: {err}")

    def delete_rsp_spec(self, name: str) -> None:
        """删除地震反应谱。

        Args:
            name: 反应谱名称
        """
        ok, err = osis_seis_rsp_spec_del(name)
        if not ok:
            raise RuntimeError(f"删除地震反应谱 {name} 失败: {err}")

    def renumber_rsp_spec(self, old_no: int, new_no: int) -> None:
        """修改地震反应谱编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_seis_rsp_spec_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改地震反应谱编号 {old_no} -> {new_no} 失败: {err}")

    # ── 反应谱工况管理 ───────────────────────────

    def create_rspec_anal(
        self,
        name: str,
        spectrum: str,
        direction: Literal[1, 0] = 1,
        angle: float = 0.0,
        scalar: float = 1.0,
        interpolated: Literal[1, 0] = 1,
        cmb: Literal["SRSS", "CQC"] = "CQC",
        damping_name: str = "",
        num: int = 1,
    ) -> None:
        """定义或修改反应谱工况。

        Args:
            name: 工况名称
            spectrum: 反应谱荷载名称
            direction: 方向，1=水平，0=竖向
            angle: 水平地震动的入射角度，单位为度（°）
            scalar: 工况缩放系数
            interpolated: 谱荷载插值方法，1=线性，0=对数
            cmb: 结构振型响应的组合方法，SRSS/CQC
            damping_name: 阻尼模型名称
            num: 组合的模态数量
        """
        ok, err = osis_rspec_anal(
            name, direction, angle, scalar, spectrum,
            interpolated, cmb, damping_name, num
        )
        if not ok:
            raise RuntimeError(f"创建反应谱工况 {name} 失败: {err}")

    def delete_rspec_anal(self, name: str) -> None:
        """删除反应谱工况。

        Args:
            name: 工况名称
        """
        ok, err = osis_rspec_anal_del(name)
        if not ok:
            raise RuntimeError(f"删除反应谱工况 {name} 失败: {err}")

    def renumber_rspec_anal(self, old_no: int, new_no: int) -> None:
        """修改反应谱工况编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_rspec_anal_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改反应谱工况编号 {old_no} -> {new_no} 失败: {err}")

    def __repr__(self) -> str:
        return f"DynamicManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

dynamic_manager = DynamicManager()
