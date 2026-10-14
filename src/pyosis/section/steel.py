from typing import Any, Dict, Literal, List
from ..core import REGISTRY

@REGISTRY.register("Section")
def osis_section_steel_i(Index: int, Name: str, Type: Literal["STEELBEAMI"],
                         H: float, Bt: float, Bb: float, Tt: float, Tb: float, Tw: float,
                         WebRibPos: Literal["Left", "Right", "Both"]):
    """定义或修改工字钢梁截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELBEAMI。
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
def osis_section_steel_box(Index: int, Name: str, Type: Literal["STEELBEAMBOX"],
                           H: float, Bt: float, Bct: float, Bb: float, Bcb: float,
                           Tt: float, Tb: float, Tw: float, SameLayout: Literal[0, 1]):
    """定义或修改箱型钢梁截面。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELBEAMBOX。
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
def osis_section_steel_box_three_cell(Index: int, Name: str, Type: Literal["STEELBOXTHREECELL"], 
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
def osis_section_steel_box_itf(Index: int, Name: str, Type: Literal["STEELBOXITF"], 
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
def osis_section_steel_canti_box(Index: int, Name: str, Type: Literal["STEELCANTIBOX"], 
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
def osis_section_steel_canti_box_ibf(Index: int, Name: str, Type: Literal["STEELCANTIBOXIBF"], 
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
def osis_section_steel_custom(Index: int, Name: str, Type: Literal["STEELCUSTOM"], 
                              PointMatrix: str, LineMatrix: str):
    """定义或修改自定义钢梁截面（通过点线关系输入）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELCUSTOM。
        PointMatrix (str): n行3列，几何点矩阵，每行第一个元素为点的编号，第二个元素为点的x坐标，第三个元素为点的y坐标,需使用osis_matrix先定义矩阵。
        LineMatrix (str): n行3列，几何线矩阵，每行第一个元素为起始点编号，第二个元素为终点编号，第三个元素为线宽,需使用osis_matrix先定义矩阵。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    Example:
        >>> matrix = [[1, 2, 20], [2, 3, 25], [3, 4, 30], [4, 1, 25]]
        >>> osis_matrix("PointMatrix", matrix)
        >>> osis_matrix("LineMatrix", matrix)
        >>> osis_section_steel_custom(1,"三角形钢截面","STEELCUSTOM","PointMatrix","LineMatrix")
    """
    pass

@REGISTRY.register("Section")
def osis_section_steel_custom_plate(Index: int, Name: str, Type: Literal["STEELCUSTOMPLATE"],
                                    IsSymmetric: Literal[0, 1] = 0):
    """定义或修改自定义钢梁截面（通过参数板输入）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 STEELCUSTOMPLATE。
        IsSymmetric (int): 截面是否关于 y 轴对称，1=对称，0=不对称。
            板件用 SteelPlate 命令（Section.add_steel_plate）逐一添加。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("SteelPlate")
def osis_steel_plate(Index: int, PlateID: int, PlateType: Literal["Top", "Bottom", "Web"],
                     StartX: float, StartY: float, EndX: float, EndY: float, Thickness: float):
    """定义或修改自定义钢梁截面的板件。

    Args:
        Index (int): 截面编号。
        PlateID (int): 板件编号，大于 0，同一截面内唯一；已存在的编号表示修改。
        PlateType (str): 板件类型。
            * Top = 顶板
            * Bottom = 底板
            * Web = 腹板
        StartX (float): 板件起始点x坐标。
        StartY (float): 板件起始点y坐标。
        EndX (float): 板件终点x坐标。
        EndY (float): 板件终点y坐标。
        Thickness (float): 板件厚度，大于 0。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass