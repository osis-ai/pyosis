"""
pyosis.dynamic.seismic 的 Docstring

地震反应谱分析底层命令接口
"""

from typing import Literal
from ..core import REGISTRY


# ──────────────────────────────────────────────
# 地震反应谱定义
# ──────────────────────────────────────────────


@REGISTRY.register("SeisRspSpec")
def osis_seis_rsp_spec_import(
    strName: str,
    strType: Literal["N", "A", "V", "D"],
    dG: float,
    nNum: int,
    spectrum_data: list[tuple[float, float]],
):
    """定义或修改导入类型地震反应谱。

    Args:
        strName (str): 名称
        strType (str): 谱类型，N=无量纲加速度谱，A=加速度谱，V=速度谱，D=位移谱
        dG (float): 输入g值
        nNum (int): 点数
        spectrum_data (list): 反应谱数据列表，每个元素为 (周期, 谱值) 元组

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> data = [(0.1, 0.5), (0.2, 0.8), (0.5, 1.2), (1.0, 0.9)]
        >>> result = osis_seis_rsp_spec_import("RS1", "A", 9.806, 4, data)
        >>> print(result)
        (True, "")
    """
    pass


@REGISTRY.register("SeisRspSpec")
def osis_seis_rsp_spec_code(
    strName: str,
    strType: Literal["N", "A", "V", "D"],
    dG: float,
    strCode: str = "JTGT_2231_01_2020",
    strBridgeType: Literal["A", "B", "C", "D"] = "A",
    nIsLongSpan: Literal[0, 1] = 0,
    nLevel: Literal[0, 1] = 0,
    dIntensity: float = 0.2,
    nSite: Literal[0, 1, 2, 3, 4] = 2,
    nDirection: Literal[0, 1] = 0,
    dPeriod: float = 0.35,
    dKsi: float = 0.05,
    dT: float = 6.0,
    dDeltaT: float = 0.01,
):
    """定义或修改按规范生成类型地震反应谱。

    Args:
        strName (str): 名称
        strType (str): 谱类型，N=无量纲加速度谱，A=加速度谱，V=速度谱，D=位移谱
        dG (float): 输入g值
        strCode (str): 规范名称，如 "JTGT_2231_01_2020"
        strBridgeType (str): 桥梁类别，A/B/C/D
        nIsLongSpan (int): 0=非高速公路和一级公路上的B类大桥特大桥，1=高速公路和一级公路上的B类大桥特大桥
        nLevel (int): 设防水准，0=E1，1=E2
        dIntensity (float): 设防烈度，0.05=Ⅵ(0.05g), 0.1=Ⅶ(0.1g), 0.15=Ⅶ(0.15g), 0.2=Ⅶ(0.2g), 0.3=Ⅷ(0.3g), 0.4=Ⅸ(0.4g)
        nSite (int): 场地类型，0=I0, 1=I1, 2=Ⅱ, 3=Ⅲ, 4=Ⅳ
        nDirection (int): 方向，0=水平，1=竖直
        dPeriod (float): 分区特征周期，0.35/0.4/0.45
        dKsi (float): 阻尼比
        dT (float): 最长周期
        dDeltaT (float): 周期间隔

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> result = osis_seis_rsp_spec_code("RS2", "N", 9.806,
        ...     strCode="JTGT_2231_01_2020", strBridgeType="A", nIsLongSpan=0,
        ...     nLevel=0, dIntensity=0.2, nSite=2, nDirection=0,
        ...     dPeriod=0.35, dKsi=0.05, dT=6.0, dDeltaT=0.01)
        >>> print(result)
        (True, "")
    """
    pass


@REGISTRY.register("SeisRspSpecDel")
def osis_seis_rsp_spec_del(strName: str):
    """删除地震反应谱。

    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SeisRspSpecMod")
def osis_seis_rsp_spec_mod(nOld: int, nNew: int):
    """修改地震反应谱编号。

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ──────────────────────────────────────────────
# 反应谱工况
# ──────────────────────────────────────────────


@REGISTRY.register("RSpecAnal")
def osis_rspec_anal(
    strName: str,
    nDirection: Literal[1, 0] = 1,
    dAngle: float = 0.0,
    dScalar: float = 1.0,
    strSpectrum: str = "",
    nInterpolated: Literal[1, 0] = 1,
    strCmb: Literal["SRSS", "CQC"] = "CQC",
    strDampingName: str = "",
    nNum: int = 1,
):
    """定义或修改反应谱工况。

    Args:
        strName (str): 工况名称
        nDirection (int): 方向，1=水平，0=竖向
        dAngle (float): 水平地震动的入射角度，单位为度（°）
        dScalar (float): 工况缩放系数
        strSpectrum (str): 反应谱荷载名称
        nInterpolated (int): 谱荷载插值方法，1=线性，0=对数
        strCmb (str): 结构振型响应的组合方法，SRSS=完全平方和开平方，CQC=完全二次型组合
        strDampingName (str): 阻尼模型名称
        nNum (int): 组合的模态数量

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("RSpecAnalDel")
def osis_rspec_anal_del(strName: str):
    """删除反应谱工况。

    Args:
        strName (str): 工况名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("RSpecAnalMod")
def osis_rspec_anal_mod(nOld: int, nNew: int):
    """修改反应谱工况编号。

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
