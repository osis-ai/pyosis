from typing import Any, Dict, Literal
from ..core import REGISTRY


@REGISTRY.register("RebarL")
def osis_rebar_l_point(SecNo: int, RebarLNo: int, RebarLType: Literal["Point"], 
                       MaterialNo: int, CoorY: float, CoorZ: float, Diameter: str):
    """定义或修改纵向钢筋，通过点输入。

    Args:
        SecNo (int): 截面编号。
        RebarLNo (int): 钢筋编号。
        RebarLType (str): 钢筋类型，固定为 Point。
        MaterialNo (int): 钢筋材料编号。
        CoorY (float): 中心点Y坐标。
        CoorZ (float): 中心点Z坐标。
        Diameter (str): 钢筋直径，范围为从D4-D50。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarL")
def osis_rebar_l_line_a(SecNo: int, RebarLNo: int, RebarLType: Literal["LineA"], 
                        MaterialNo: int, YRef: Literal["Left", "Center"], YRefValue: float, 
                        ZRef: Literal["Top", "Bottom"], ZRefValue: float, Num: int, Interval: float, Diameter: str):
    """定义或修改纵向钢筋，通过直线-输入方法A输入。

    Args:
        SecNo (int): 截面编号。
        RebarLNo (int): 钢筋编号。
        RebarLType (str): 钢筋类型，固定为 LineA。
        MaterialNo (int): 钢筋材料编号。
        YRef (str): Y方向参考位置，Left=左，Center=质心。
        YRefValue (float): 与Y方向参考位置的距离，Y轴正方向为正。
        ZRef (str): Z方向参考位置，Top=顶，Bottom=底。
        ZRefValue (float): 与Z方向参考位置的距离，Z轴正方向为正。
        Num (int): 数量。
        Interval (float): 间距。
        Diameter (str): 钢筋直径，范围为从D4-D50。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarL")
def osis_rebar_l_line_b(SecNo: int, RebarLNo: int, RebarLType: Literal["LineB"], 
                        MaterialNo: int, StartY: float, StartZ: float, EndY: float, EndZ: float, 
                        Method: Literal[0, 1], Num: int, Interval: float, 
                        LayoutRef: Literal["StartPoint", "MidPoint", "EndPoint"], HasEndRebar: Literal[0, 1], Diameter: str):
    """定义或修改纵向钢筋，通过直线-输入方法B输入。

    Args:
        SecNo (int): 截面编号。
        RebarLNo (int): 钢筋编号。
        RebarLType (str): 钢筋类型，固定为 LineB。
        MaterialNo (int): 钢筋材料编号。
        StartY (float): 开始点Y坐标。
        StartZ (float): 开始点Z坐标。
        EndY (float): 结束点Y坐标。
        EndZ (float): 结束点Z坐标。
        Method (int): 1=输入数量，0=输入间距。
        Num (int): 数量。
        Interval (float): 间距。
        LayoutRef (str): 分布参考，StartPoint=起点，MidPoint=中点，EndPoint=终点。
        HasEndRebar (int): 1=有端筋，0=无端筋。
        Diameter (str): 钢筋直径，范围为从D4-D50。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarLDel")
def osis_rebar_l_del(SecNo: int, RebarLNo: int):
    """删除纵向钢筋。

    Args:
        SecNo (int): 截面编号。
        RebarLNo (int): 钢筋编号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarS")
def osis_rebar_s_bent_up(SecNo: int, RebarSType: Literal["BentUpRebar"], 
                         MaterialNo: int, Interval: float, Area: float, Angle: float):
    """定义或修改弯起钢筋。

    Args:
        SecNo (int): 截面编号。
        RebarSType (str): 钢筋类型，固定为 BentUpRebar。
        MaterialNo (int): 材料编号。
        Interval (float): 间距。
        Area (float): 面积。
        Angle (float): 角度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarS")
def osis_rebar_s_shear_stirrup(SecNo: int, RebarSType: Literal["ShearStirrup"], 
                               MaterialNo: int, Interval: float, Area: float):
    """定义或修改抗剪箍筋。

    Args:
        SecNo (int): 截面编号。
        RebarSType (str): 钢筋类型，固定为 ShearStirrup。
        MaterialNo (int): 材料编号。
        Interval (float): 间距。
        Area (float): 面积。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarS")
def osis_rebar_s_web_vertical(SecNo: int, RebarSType: Literal["WebVerticalRebar"], 
                              MaterialNo: int, Interval: float, Area: float, Angle: float, 
                              EffectiveStress: float, ReductionFactor: float):
    """定义或修改腹板竖筋。

    Args:
        SecNo (int): 截面编号。
        RebarSType (str): 钢筋类型，固定为 WebVerticalRebar。
        MaterialNo (int): 材料编号。
        Interval (float): 间距。
        Area (float): 面积。
        Angle (float): 角度。
        EffectiveStress (float): 有效应力。
        ReductionFactor (float): 折减系数。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarS")
def osis_rebar_s_torsional_stirrup(SecNo: int, RebarSType: Literal["TorsionalStirrup"], 
                                   MaterialNo: int, Interval: float, LongiArea: float, StirrupArea: float):
    """定义或修改扭转箍筋。

    Args:
        SecNo (int): 截面编号。
        RebarSType (str): 钢筋类型，固定为 TorsionalStirrup。
        MaterialNo (int): 材料编号。
        Interval (float): 间距。
        LongiArea (float): 纵筋面积。
        StirrupArea (float): 箍筋面积。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RebarSDel")
def osis_rebar_s_del(SecNo: int, RebarSType: Literal["BentUpRebar", "ShearStirrup", "WebVerticalRebar", "TorsionalStirrup"]):
    """删除抗剪钢筋。

    Args:
        SecNo (int): 截面编号。
        RebarSType (str): 钢筋类型，BentUpRebar=弯起钢筋，ShearStirrup=抗剪箍筋，WebVerticalRebar=腹板竖筋，TorsionalStirrup=扭转箍筋。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass