from typing import Any, Dict, Literal
from ..core import REGISTRY

@REGISTRY.register("Rib")
def osis_rib_flat(SecIndex: int, Type: Literal["Flat"], Name: str, H: float, T: float):
    """定义或修改扁平加劲肋。

    Args:
        SecIndex (int): 所属截面编号。
        Type (str): 加劲肋类型，固定为 Flat。
        Name (str): 加劲肋名称。
        H (float): 加劲肋高度。
        T (float): 加劲肋厚度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Rib")
def osis_rib_t(SecIndex: int, Type: Literal["T"], Name: str, H: float, B: float, T1: float, T2: float):
    """定义或修改T形加劲肋。

    Args:
        SecIndex (int): 所属截面编号。
        Type (str): 加劲肋类型，固定为 T。
        Name (str): 加劲肋名称。
        H (float): 加劲肋高度。
        B (float): 加劲肋宽度。
        T1 (float): 竖肋厚度。
        T2 (float): 横肋厚度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Rib")
def osis_rib_u(SecIndex: int, Type: Literal["U"], Name: str, H: float, B1: float, B2: float, T: float, R: float):
    """定义或修改U形加劲肋。

    Args:
        SecIndex (int): 所属截面编号。
        Type (str): 加劲肋类型，固定为 U。
        Name (str): 加劲肋名称。
        H (float): 加劲肋高度。
        B1 (float): 加劲肋上端宽度。
        B2 (float): 加劲肋下端宽度。
        T (float): 加劲肋厚度。
        R (float): 加劲肋转角处圆弧半径。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Rib")
def osis_rib_l(SecIndex: int, Type: Literal["LL", "LR"], Name: str, H: float, B: float, T: float, R: float):
    """定义或修改L形加劲肋。

    Args:
        SecIndex (int): 所属截面编号。
        Type (str): 加劲肋类型，LL = 左向L形加劲肋，LR = 右向L形加劲肋。
        Name (str): 加劲肋名称。
        H (float): 加劲肋高度。
        B (float): 加劲肋宽度。
        T (float): 加劲肋厚度。
        R (float): 加劲肋转角处圆弧半径。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RibDel")
def osis_rib_del(SecIndex: int, Name: str):
    """删除加劲肋。

    Args:
        SecIndex (int): 所属截面编号。
        Name (str): 加劲肋名称。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RibLayout")
def osis_rib_layout(
    SecIndex: int, 
    GirderType: Literal["STEELISIDE", "STEELIMIDDLE", "STEELBOX", "STEELTROUGH", "STEEL"], 
    PlateType: Literal[
        "TopFlange", "TopFlange1", "TopFlange2", "TopFlange3", "TopFlange4", "TopFlange5",
        "TopFlangeInclined", "TopFlangeInclined1", "TopFlangeInclined2", "TopFlangeInclined3", "TopFlangeInclined4", "TopFlangeInclined5",
        "BottomFlange", "BottomFlange1", "BottomFlange2", "BottomFlange3", "BottomFlange4", "BottomFlange5",
        "BottomFlangeInclined", "BottomFlangeInclined1", "BottomFlangeInclined2", "BottomFlangeInclined3", "BottomFlangeInclined4", "BottomFlangeInclined5",
        "SideWeb", "SideWebL", "SideWebR",
        "MiddleWeb", "MiddleWeb1", "MiddleWeb2", "MiddleWeb3", "MiddleWeb4", "MiddleWeb5",
        "PlateWithoutRib"
    ], 
    RibLayoutNo: int, 
    RibName: str, 
    PositionDistance: float, 
    Interval: float, 
    IntervalNum: int
):
    """定义或修改加劲肋布置信息，每次定义为一组。

    Args:
        SecIndex (int): 所属截面的编号。
        GirderType (str): 钢梁类型。
            * STEELISIDE = 组合梁的边工字钢梁
            * STEELIMIDDLE = 组合梁的中工字钢梁
            * STEELBOX = 组合梁的钢箱梁
            * STEELTROUGH = 组合梁的槽型钢梁
            * STEEL = 一般钢梁截面
        PlateType (str): 板件所在位置。
            * 顶板：TopFlange、TopFlange1~TopFlange5
            * 斜顶板：TopFlangeInclined、TopFlangeInclined1~TopFlangeInclined5
            * 底板：BottomFlange、BottomFlange1~BottomFlange5
            * 斜底板：BottomFlangeInclined、BottomFlangeInclined1~BottomFlangeInclined5
            * 边腹板：SideWeb、SideWebL、SideWebR
            * 中腹板：MiddleWeb、MiddleWeb1~MiddleWeb5
            * 无加劲肋的板件：PlateWithoutRib
        RibLayoutNo (int): 加劲肋布置信息的编号。
        RibName (str): 加劲肋的名称。
        PositionDistance (float): 加劲肋与参考点的定位距离。
        Interval (float): 加劲肋布置间距。
        IntervalNum (int): 间距数量。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("RibLayoutDel")
def osis_rib_layout_del(
    SecIndex: int, 
    GirderType: Literal["STEELISIDE", "STEELIMIDDLE", "STEELBOX", "STEELTROUGH", "STEEL"], 
    PlateType: Literal[
        "TopFlange", "TopFlange1", "TopFlange2", "TopFlange3", "TopFlange4", "TopFlange5",
        "TopFlangeInclined", "TopFlangeInclined1", "TopFlangeInclined2", "TopFlangeInclined3", "TopFlangeInclined4", "TopFlangeInclined5",
        "BottomFlange", "BottomFlange1", "BottomFlange2", "BottomFlange3", "BottomFlange4", "BottomFlange5",
        "BottomFlangeInclined", "BottomFlangeInclined1", "BottomFlangeInclined2", "BottomFlangeInclined3", "BottomFlangeInclined4", "BottomFlangeInclined5",
        "SideWeb", "SideWebL", "SideWebR",
        "MiddleWeb", "MiddleWeb1", "MiddleWeb2", "MiddleWeb3", "MiddleWeb4", "MiddleWeb5",
        "PlateWithoutRib"
    ], 
    RibLayoutNo: int
):
    """删除加劲肋布置信息。

    Args:
        SecIndex (int): 所属截面的编号。
        GirderType (str): 钢梁类型。
            * STEELISIDE = 组合梁的边工字钢梁
            * STEELIMIDDLE = 组合梁的中工字钢梁
            * STEELBOX = 组合梁的钢箱梁
            * STEELTROUGH = 组合梁的槽型钢梁
            * STEEL = 一般钢梁截面
        PlateType (str): 板件所在位置。
            * 顶板：TopFlange、TopFlange1~TopFlange5
            * 斜顶板：TopFlangeInclined、TopFlangeInclined1~TopFlangeInclined5
            * 底板：BottomFlange、BottomFlange1~BottomFlange5
            * 斜底板：BottomFlangeInclined、BottomFlangeInclined1~BottomFlangeInclined5
            * 边腹板：SideWeb、SideWebL、SideWebR
            * 中腹板：MiddleWeb、MiddleWeb1~MiddleWeb5
            * 无加劲肋的板件：PlateWithoutRib
        RibLayoutNo (int): 加劲肋布置信息的编号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass