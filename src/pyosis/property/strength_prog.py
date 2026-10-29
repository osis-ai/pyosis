'''
pyosis.property.strength_prog 的 Docstring

强度进展特性
'''

from __future__ import annotations

from typing import Any, Literal

from ..core import REGISTRY
from ..core.basic_manager import BasicManager


@REGISTRY.register("StrengthPrg")
def osis_strength_prog_aci(
    index: str,
    e_type: Literal["ACI"],
    f28: float,
    a: float,
    b: float,
):
    """创建或修改 ACI 规范强度进展特性

    命令流：StrengthPrg, Index, Type, f28, a, b
    形参顺序与命令流字段顺序一致，Type 固定为 ACI。

    Args:
        index (str): 强度进展名称（Index）
        e_type (str): 强度进展类型，固定为 "ACI"
        f28 (float): 混凝土 28 天抗压强度，按工程当前压力单位填写
        a (float): 强度系数 a
        b (float): 强度系数 b

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("StrengthPrg")
def osis_strength_prog_cebfip2010(
    index: str,
    e_type: Literal["CEBFIP2010"],
    fcm: float,
    cement_coeff: float,
    aggregate_coeff: float,
):
    """创建或修改 CEBFIP2010 强度进展特性

    命令流：StrengthPrg, Index, Type, fcm, CementCoeff, AggregateCoeff
    形参顺序与命令流字段顺序一致，Type 固定为 CEBFIP2010。

    Args:
        index (str): 强度进展名称（Index）
        e_type (str): 强度进展类型，固定为 "CEBFIP2010"
        fcm (float): 混凝土平均抗压强度，按工程当前压力单位填写
        cement_coeff (float): 水泥类型系数（CementCoeff），文档给出的取值为
            0.20、0.25、0.38
        aggregate_coeff (float): 骨料类型系数（AggregateCoeff），文档给出的取值为
            1.2、1.0、0.9、0.7

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("StrengthPrg")
def osis_strength_prog_custom(
    index: str,
    e_type: Literal["CUSTOM"],
    factor: float,
    curve: list[float],
):
    """创建或修改用户定义强度进展特性

    命令流：StrengthPrg, Index, Type, Factor, day_i, comp_i, tension_i, e_i, ...
    curve 按点展平，每点 4 个值：天数、抗压强度、抗拉强度、弹性模量，
    点数 n 时共 4*n 个数。至少两个点，day 严格单调递增；
    comp/tension/e 需做应力单位换算。

    Args:
        index (str): 强度进展名称（Index）
        e_type (str): 强度进展类型，固定为 "CUSTOM"（用户定义）
        factor (float): 调幅系数（Factor）
        curve (list): 曲线点展平后的数值，每点依次为 day、comp、tension、e

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("StrengthPrgDel")
def osis_strength_prog_del(index: str):
    """删除强度进展特性

    Args:
        index (str): 强度进展名称（Index）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("StrengthPrgMod")
def osis_strength_prog_mod(old_index: str, new_index: str):
    """修改强度进展特性名称。名称存在时，交换

    Args:
        old_index (str): 原名称（oldIndex）
        new_index (str): 新名称（newIndex）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


class StrengthProgManager(BasicManager):
    '''强度进展特性管理器'''

    _entity_key_attr = "name"

    def create(
        self,
        index: str,
        type: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        '''创建或修改强度进展特性（便捷入口，内部转发到对应 create_* 方法）

        type 路由映射：
            * "ACI" -> create_aci
            * "CEBFIP2010" -> create_cebfip2010
            * "CUSTOM" -> create_custom

        Args:
            index (str): 强度进展名称
            type (str): 强度进展类型
            *args: 按位置传给对应 create_* 的参数
            **kwargs: 按关键字传给对应 create_* 的参数

        Raises:
            ValueError: 未知 type
            RuntimeError: 创建失败时抛出

        Examples:
            >>> property_manager.strength_prog.create("SP1", "ACI", 5.0e7, 0.5, 0.9)
            >>> property_manager.strength_prog.create("SP2", "CEBFIP2010", 3.8e7, 0.25, 1.0)
            >>> property_manager.strength_prog.create("SP3", "CUSTOM", 1.0,
            ...     [1.0, 2.0e7, 1.0e6, 2.0e10, 28.0, 5.0e7, 2.5e6, 3.0e10])
        '''
        _creator = {
            "ACI": self.create_aci,
            "CEBFIP2010": self.create_cebfip2010,
            "CUSTOM": self.create_custom,
        }
        type_key = str(type).strip().upper()
        if type_key not in _creator:
            raise ValueError(
                f"未知强度进展类型: {type!r}，支持: {', '.join(_creator)}"
            )
        return _creator[type_key](index, *args, **kwargs)

    def create_aci(self, index: str, f28: float, a: float, b: float) -> None:
        '''创建或修改 ACI 规范强度进展特性

        Args:
            index (str): 强度进展名称
            f28 (float): 混凝土 28 天抗压强度，按工程当前压力单位填写
            a (float): 强度系数 a
            b (float): 强度系数 b

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_strength_prog_aci(index, "ACI", f28, a, b)
        if not ok:
            raise RuntimeError(f"创建 ACI 强度进展特性 {index} 失败: {err}")

    def create_cebfip2010(
        self,
        index: str,
        fcm: float,
        cement_coeff: float,
        aggregate_coeff: float,
    ) -> None:
        '''创建或修改 CEBFIP2010 强度进展特性

        Args:
            index (str): 强度进展名称
            fcm (float): 混凝土平均抗压强度，按工程当前压力单位填写
            cement_coeff (float): 水泥类型系数（CementCoeff），文档给出的取值为
                0.20、0.25、0.38
            aggregate_coeff (float): 骨料类型系数（AggregateCoeff），文档给出的取值为
                1.2、1.0、0.9、0.7

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_strength_prog_cebfip2010(
            index, "CEBFIP2010", fcm, cement_coeff, aggregate_coeff
        )
        if not ok:
            raise RuntimeError(f"创建 CEBFIP2010 强度进展特性 {index} 失败: {err}")

    def create_custom(self, index: str, factor: float, curve: list[float]) -> None:
        '''创建或修改用户定义强度进展特性

        Args:
            index (str): 强度进展名称
            factor (float): 调幅系数
            curve (list): 曲线点展平后的数值，每点依次为 day、comp、tension、e，
                点数 n 时共 4*n 个数

        Raises:
            ValueError: 曲线点数不足、每点不是 4 个值、或 day 不是严格单调递增
            RuntimeError: 创建失败时抛出
        '''
        values = [float(x) for x in curve]
        if len(values) % 4 != 0:
            raise ValueError(
                f"用户定义强度进展特性 {index} 的曲线点数需为 4 的整数倍"
                f"（每点 day、comp、tension、e），实际给了 {len(values)} 个值"
            )
        if len(values) < 8:
            raise ValueError(
                f"用户定义强度进展特性 {index} 至少需要两个点，实际给了 {len(values) // 4} 个点"
            )
        days = values[0::4]
        if any(b <= a for a, b in zip(days, days[1:])):
            raise ValueError(
                f"用户定义强度进展特性 {index} 的 day 必须严格单调递增"
            )
        ok, err = osis_strength_prog_custom(index, "CUSTOM", factor, values)
        if not ok:
            raise RuntimeError(f"创建用户定义强度进展特性 {index} 失败: {err}")

    def delete(self, index: str) -> None:
        '''删除强度进展特性

        Args:
            index (str): 强度进展名称

        Raises:
            RuntimeError: 删除失败时抛出
        '''
        ok, err = osis_strength_prog_del(index)
        if not ok:
            raise RuntimeError(f"删除强度进展特性 {index} 失败: {err}")

    def rename(self, old_index: str, new_index: str) -> None:
        '''修改强度进展特性名称。名称存在时，交换

        Args:
            old_index (str): 原名称
            new_index (str): 新名称

        Raises:
            RuntimeError: 修改失败时抛出
        '''
        ok, err = osis_strength_prog_mod(old_index, new_index)
        if not ok:
            raise RuntimeError(f"修改强度进展特性名称 {old_index} -> {new_index} 失败: {err}")

    def __repr__(self) -> str:
        return "StrengthProgManager()"
