

from typing import Any, Dict, Literal
from ..core import REGISTRY

@REGISTRY.register("Section")
def osis_section_steel_i(Index: int, Name: str, Type: Literal["STEELI"]="STEELI", 
                         H: float, Bt: float, Bb: float, Tt: float, Tb: float, Tw: float, 
                         WebRibPos: Literal["Left", "Right", "Both"]):
    """定义或修改工字形截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELI。
        H (float): 梁高。
        Bt (float): 上翼缘宽度。
        Bb (float): 下翼缘宽度。
        Tt (float): 上翼缘厚度。
        Tb (float): 下翼缘厚度。
        Tw (float): 腹板厚度。
        WebRibPos (str): 加劲肋位置，Left=左侧，Right=右侧，Both=两侧。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_box(Index: int, Name: str, Type: Literal["STEELBOX"]="STEELBOX", 
                           H: float, Bt: float, Bct: float, Bb: float, Bcb: float, 
                           Tt: float, Tb: float, Tw: float, SameLayout: Literal[0, 1]):
    """定义或修改箱型截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELBOX。
        H (float): 梁高。
        Bt (float): 上翼缘宽度。
        Bct (float): 上翼缘悬出宽。
        Bb (float): 下翼缘宽度。
        Bcb (float): 下翼缘悬出宽。
        Tt (float): 上翼缘厚度。
        Tb (float): 下翼缘厚度。
        Tw (float): 腹板厚度。
        SameLayout (int): 下翼缘加劲肋是否与上翼缘相同，1=相同，0=不同。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_box_three_cell(Index: int, Name: str, Type: Literal["STEELBOXTHREECELL"]="STEELBOXTHREECELL", 
                                      H: float, Bt: float, Bb: float, i: float, a1: float, a2: float, 
                                      Dt: float, Tt1: float, Tt2: float, Tb1: float, Db: float, 
                                      Tb2: float, Tb3: float, Tw1: float, Dw: float, 
                                      HasWeb: Literal[0, 1], Tw2: float, 
                                      WebRibPos: Literal["Left", "Right", "Both"]):
    """定义或修改单箱单/三室截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELBOXTHREECELL。
        H (float): 梁高。
        Bt (float): 上翼缘宽度。
        Bb (float): 下翼缘宽度。
        i (float): 顶面横坡。
        a1 (float): 边腹板倾角。
        a2 (float): 斜底板倾角。
        Dt (float): 顶点变厚点至起点距离。
        Tt1 (float): 顶板厚度1。
        Tt2 (float): 顶板厚度2。
        Tb1 (float): 底板厚度。
        Db (float): 斜底板变厚点至起点距离。
        Tb2 (float): 斜底板厚度1。
        Tb3 (float): 斜底板厚度2。
        Tw1 (float): 边腹板厚度。
        Dw (float): 中腹板至主梁中心线距离。
        HasWeb (int): 是否有中腹板，1=有中腹板，0=无中腹板。
        Tw2 (float): 中腹板厚度。
        WebRibPos (str): 加劲肋位置，Left=左侧，Right=右侧，Both=两侧。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_box_itf(Index: int, Name: str, Type: Literal["STEELBOXITF"]="STEELBOXITF", 
                               H: float, B: float, Bt: float, Bb: float, i: float, a1: float, a2: float, 
                               Dt: float, Tt1: float, Tt2: float, Tt3: float, Tb1: float, 
                               Db: float, Tb2: float, Tb3: float, Tw1: float):
    """定义或修改单箱单室斜顶板截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELBOXITF。
        H (float): 梁高。
        B (float): 梁宽。
        Bt (float): 顶板宽度。
        Bb (float): 平底板宽度。
        i (float): 顶面横坡。
        a1 (float): 斜顶板倾角。
        a2 (float): 斜底板倾角。
        Dt (float): 顶板变厚点至起点距离。
        Tt1 (float): 顶板厚度1。
        Tt2 (float): 顶板厚度2。
        Tt3 (float): 斜顶板厚度。
        Tb1 (float): 底板厚度。
        Db (float): 斜底板变厚点至起点距离。
        Tb2 (float): 斜底板厚度1。
        Tb3 (float): 斜底板厚度2。
        Tw1 (float): 边腹板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_canti_box(Index: int, Name: str, Type: Literal["STEELCANTIBOX"]="STEELCANTIBOX", 
                                 H: float, Bt: float, Bb: float, i: float, a: float, Dt: float, 
                                 Tt1: float, Tt2: float, Tb1: float, Tw1: float, 
                                 HasWeb: Literal[0, 1], Tw2: float, 
                                 WebRibPos: Literal["Left", "Right", "Both"], h: float, t: float):
    """定义或修改悬臂单箱单/双室截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELCANTIBOX。
        H (float): 梁高。
        Bt (float): 顶板宽度。
        Bb (float): 平底板宽度。
        i (float): 顶面横坡。
        a (float): 边腹板倾角。
        Dt (float): 顶板变厚点至起点距离。
        Tt1 (float): 顶板厚度1。
        Tt2 (float): 顶板厚度2。
        Tb1 (float): 底板厚度。
        Tw1 (float): 边腹板厚度。
        HasWeb (int): 是否有中腹板，1=有中腹板，0=无中腹板。
        Tw2 (float): 中腹板厚度。
        WebRibPos (str): 加劲肋位置，Left=左侧，Right=右侧，Both=两侧。
        h (float): 悬臂端封板高。
        t (float): 悬臂端封板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_canti_box_ibf(Index: int, Name: str, Type: Literal["STEELCANTIBOXIBF"]="STEELCANTIBOXIBF", 
                                     H: float, Bt: float, Bb: float, Bc: float, i: float, a: float, 
                                     Dt: float, Tt1: float, Tt2: float, Tb1: float, Tb2: float, 
                                     Tw1: float, HasWeb: Literal[0, 1], Tw2: float, 
                                     WebRibPos: Literal["Left", "Right", "Both"], h: float, t: float):
    """定义或修改悬臂单箱单/双室斜底板截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELCANTIBOXIBF。
        H (float): 梁高。
        Bt (float): 顶板宽度。
        Bb (float): 平底板宽度。
        Bc (float): 悬臂长。
        i (float): 顶面横坡。
        a (float): 边腹板倾角。
        Dt (float): 顶板变厚点至起点距离。
        Tt1 (float): 顶板厚度1。
        Tt2 (float): 顶板厚度2。
        Tb1 (float): 底板厚度。
        Tb2 (float): 斜底板厚度。
        Tw1 (float): 边腹板厚度。
        HasWeb (int): 是否有中腹板，1=有中腹板，0=无中腹板。
        Tw2 (float): 中腹板厚度。
        WebRibPos (str): 加劲肋位置，Left=左侧，Right=右侧，Both=两侧。
        h (float): 悬臂端封板高。
        t (float): 悬臂端封板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_custom(Index: int, Name: str, Type: Literal["STEELCUSTOM"]="STEELCUSTOM", 
                              PointMatrix: List[List[float]], LineMatrix: List[List[float]]):
    """定义或修改自定义钢梁截面（通过点线关系输入）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELCUSTOM。
        PointMatrix (List[List[float]]): n行3列，几何点矩阵，每行第一个元素为点的编号，第二个元素为点的x坐标，第三个元素为点的y坐标。
        LineMatrix (List[List[float]]): n行3列，几何线矩阵，每行第一个元素为起始点编号，第二个元素为终点编号，第三个元素为线宽。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_custom_plate(Index: int, Name: str, Type: Literal["STEELCUSTOMPLATE"]="STEELCUSTOMPLATE", 
                                    PlatePositions: List[Literal[
                                        "TopFlange", "TopFlange1", "TopFlange2", "TopFlange3", "TopFlange4", "TopFlange5",
                                        "TopFlangeInclined", "TopFlangeInclined1", "TopFlangeInclined2", "TopFlangeInclined3", "TopFlangeInclined4", "TopFlangeInclined5",
                                        "BottomFlange", "BottomFlange1", "BottomFlange2", "BottomFlange3", "BottomFlange4", "BottomFlange5",
                                        "BottomFlangeInclined", "BottomFlangeInclined1", "BottomFlangeInclined2", "BottomFlangeInclined3", "BottomFlangeInclined4", "BottomFlangeInclined5",
                                        "SideWeb", "SideWebL", "SideWebR",
                                        "MiddleWeb", "MiddleWeb1", "MiddleWeb2", "MiddleWeb3", "MiddleWeb4", "MiddleWeb5",
                                        "PlateWithoutRib"
                                    ]]):
    """定义或修改自定义钢梁截面（通过参数板输入）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELCUSTOMPLATE。
        PlatePositions (List[str]): 指定该截面拥有的板件列表，可选择：
            * 顶板：TopFlange、TopFlange1~TopFlange5
            * 斜顶板：TopFlangeInclined、TopFlangeInclined1~TopFlangeInclined5
            * 底板：BottomFlange、BottomFlange1~BottomFlange5
            * 斜底板：BottomFlangeInclined、BottomFlangeInclined1~BottomFlangeInclined5
            * 边腹板：SideWeb、SideWebL、SideWebR
            * 中腹板：MiddleWeb、MiddleWeb1~MiddleWeb5
            * 无加劲肋的板件：PlateWithoutRib
            注意：带有加劲肋的板件位置不可重复。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("SteelPlate")
def osis_steel_plate(Index: int, GirderType: Literal["STEELISIDE", "STEELIMIDDLE", "STEELBOX", "STEELTROUGH", "STEEL"], 
                     PlatePostion: Literal[
                         "TopFlange", "TopFlange1", "TopFlange2", "TopFlange3", "TopFlange4", "TopFlange5",
                         "TopFlangeInclined", "TopFlangeInclined1", "TopFlangeInclined2", "TopFlangeInclined3", "TopFlangeInclined4", "TopFlangeInclined5",
                         "BottomFlange", "BottomFlange1", "BottomFlange2", "BottomFlange3", "BottomFlange4", "BottomFlange5",
                         "BottomFlangeInclined", "BottomFlangeInclined1", "BottomFlangeInclined2", "BottomFlangeInclined3", "BottomFlangeInclined4", "BottomFlangeInclined5",
                         "SideWeb", "SideWebL", "SideWebR",
                         "MiddleWeb", "MiddleWeb1", "MiddleWeb2", "MiddleWeb3", "MiddleWeb4", "MiddleWeb5",
                         "PlateWithoutRib"
                     ], 
                     StartX: float, StartY: float, EndX: float, EndY: float, Thickness: float, 
                     IsSymmetric: Literal[0, 1], RibStartPosition: Literal[0, 1], RibStartDistance: float, 
                     RibLocation: Literal["Left", "Right", "Both"]):
    """定义或修改自定义钢梁截面的板件。

    Args:
        Index (int): 截面编号。
        GirderType (str): 钢梁类型。
            * STEELISIDE = 组合梁的边工字钢梁
            * STEELIMIDDLE = 组合梁的中工字钢梁
            * STEELBOX = 组合梁的钢箱梁
            * STEELTROUGH = 组合梁的槽型钢梁
            * STEEL = 一般钢梁截面
        PlatePostion (str): 板件所在位置。
            * 顶板：TopFlange、TopFlange1~TopFlange5
            * 斜顶板：TopFlangeInclined、TopFlangeInclined1~TopFlangeInclined5
            * 底板：BottomFlange、BottomFlange1~BottomFlange5
            * 斜底板：BottomFlangeInclined、BottomFlangeInclined1~BottomFlangeInclined5
            * 边腹板：SideWeb、SideWebL、SideWebR
            * 中腹板：MiddleWeb、MiddleWeb1~MiddleWeb5
            * 无加劲肋的板件：PlateWithoutRib
        StartX (float): 板件起始点x坐标。
        StartY (float): 板件起始点y坐标。
        EndX (float): 板件终点x坐标。
        EndY (float): 板件终点y坐标。
        Thickness (float): 板件厚度。
        IsSymmetric (int): 板件是否关于y轴对称，1=对称，0=不对称。
        RibStartPosition (int): 加劲肋起始位置，1=从起点开始布置，0=从终点开始布置。
        RibStartDistance (float): 加劲肋起始位置与板件端点的距离。
        RibLocation (str): 加劲肋布置位置。
            * 对于非中腹板的一般板件，以起点到终点的线段为基准，在线段左侧则为Left，反之为Right，不可选择Both
            * 对于中腹板，指加劲肋在腹板两侧布置的绝对位置，与起止点无关。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass