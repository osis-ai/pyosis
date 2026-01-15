'''
pyosis.section.interface 的 Docstring
'''

from typing import Any, Dict, Literal
from ..core import REGISTRY


# @REGISTRY.register('Section')
# def osis_section(nSec: int, strName: str, eSectionType: Literal["RECT", "ISHAPE", "TSHAPE", "CIRCLE", "LSHAPE"], params: Dict[str, Any]):
#     """创建或修改截面
    
#     根据指定的截面类型和参数创建或修改截面定义。重复使用截面编号会修改现有截面。
    
#     Args:
#         nSec: 截面编号，从1开始编号，所有类型的截面均使用同一编号序列
#         strName: 截面名称，默认为"截面1"
#         eSectionType: 截面类型，可选值：
#             - RECT: 矩形截面
#             - ISHAPE: 工字形截面  
#             - TSHAPE: T形截面
#             - CIRCLE: 圆形截面
#             - LSHAPE: L形截面
#         kwargs: 截面参数字典，具体参数根据eSectionType不同而变化，详细参数说明请查看函数完整文档
    
#     Returns:
#         tuple (bool, str): 返回一个元组，包含：
#             - bool: 操作是否成功
#             - str: 失败原因（如果操作失败）
    
#     Examples:
#         >>> # 创建矩形截面
#         >>> result = osis_section(1, "截面1 (矩形)", "RECT", {
#         ...     "TransitionType": "Fillet", "SecType": "Solid",
#         ...     "B": 0.6, "H": 0.3
#         ... })
#         >>> print(result)
#         (True, "")
        
#         >>> # 创建工字形截面  
#         >>> result = osis_section(2, "截面2 (工字形)", "ISHAPE", {
#         ...     "H": 0.4, "Bt": 0.2, "Bb": 0.2,
#         ...     "Tt": 0.016, "Tb": 0.016, "Tw": 0.01
#         ... })
#         >>> print(result)
#         (True, "")
    
#     """
#     e = OSISEngine.GetInstance()
#     return e.OSIS_Section(nSec, strName, eSectionType, params)


@REGISTRY.register('Section')
def osis_section_Lshape(nSec: int, strName: str, eSectionType: Literal["LSHAPE"], nDir: Literal[0, 1], H: float, B: float, Tf1: float, Tf2: float):
    """创建或修改L形截面(LShape)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 LSHAPE
        nDir (int): L形截面方向
            * 0 = 左下向
            * 1 = 左上向
        H (float): 截面总高度
        B (float): 截面总宽度
        Tf1 (float): 竖肢厚度
        Tf2 (float): 横肢厚度

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 创建左下向L形截面
        >>> result = section_Lshape(1, "截面1 (左下向L形)", "LSHAPE", 0, 6, 4, 1.2, 1.2)
        >>> print(result)
        (True, "")

    """ 
    pass

@REGISTRY.register('Section')
def osis_section_circle(nSec: int, strName: str, eSectionType: Literal["CIRCLE"], eCircleType: Literal["Hollow", "Solid"], D: float,Tw: float):
    """创建或修改圆形截面(Circle)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 CIRCLE
        eCircleType (str): 截面类型：
            * Hollow = 空腹截面e
            * Solid = 实腹截面
        D (float): 圆形截面直径
        Tw (float): 空腹截面的壁厚
            仅当 eCircleType 为 "Hollow" 时需要指定。
e
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 创建实心圆形截面
        >>> result = section_circle(1, "截面1 (实心圆形)", "CIRCLE", "Solid", 6.0, 0.0)
        >>> print(result)
        (True, "")
        
    """
    pass

@REGISTRY.register('Section')
def osis_section_Tshape(nSec: int, strName: str, eSectionType: Literal["TSHAPE"], nDir: Literal[0, 1], H: float, B: float, Tf: float, Tw: float):
    """创建或修改T形截面(TShape)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称
        eSectionType (str): 截面类型，固定为 TSHAPE
        nDir (int): 截面方向：
            * 0: T形
            * 1: 倒T形
        H (float): 截面总高度
        B (float): 翼缘宽度
        Tf (float): 翼缘厚度
        Tw (float): 腹板厚度

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 创建基本T形截面
        >>> result = section_Tshape(1, "截面1 (T形)", "TSHAPE", 0, 2, 12, 0.2, 0.5)
        >>> print(result)
        (True, "")

    """
    pass

@REGISTRY.register('Section')
def osis_section_Ishape(nSec: int, strName: str, eSectionType: Literal["ISHAPE"], H: float, Bt: float, Bb: float, Tt: float, Tb: float, Tw: float):
    """创建或修改I形截面（工字形截面）(IShape)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称
        eSectionType (str): 截面类型，固定为 ISHAPE
        H (float): 截面总高度
        Bt (float): 上翼缘宽度
        Bb (float): 下翼缘宽度
        Tt (float): 上翼缘厚度
        Tb (float): 下翼缘厚度
        Tw (float): 腹板厚度

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 创建基本工字形截面
        >>> result = section_Ishape(1, "截面1 (工字形)", "ISHAPE", 2.0, 12.0, 12.0, 0.5, 0.5, 1.0)
        >>> print(result)
        (True, "")
    """
    pass

@REGISTRY.register('Section')
def osis_section_smallbox(nSec: int, strName: str, eSectionType: Literal["SMALLBOX"], eGirderPos: Literal["LEFT", "MIDDLE", "RIGHT"], 
                          H: float, Bs: float, Bc: float, Bb: float, Tt: float, Tb: float, Tw: float, i: float, Tc: float, Tc1: float, x: float, xi1: float, Tt1: float, xi2: float, yi2: float, bSlope: bool, i1: float, i2: float, R: float):
    """定义或修改小箱梁截面(SMALLBOX)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 SMALLBOX
        eGirderPos (str): 截面位置
            * Left = 左边梁
            * Middle = 中梁
            * Right = 右边梁
        H (float): 箱梁高度
        Bs (float): 边翼板宽
        Bm (float): 中梁半宽
        Bc (float): 现浇湿接缝半宽
        Bb (float): 底板宽
        Tt (float): 顶板厚
        Tb (float): 底板厚
        Tw (float): 腹板厚
        i (float): 腹板倾斜比
        Tc (float): 边梁悬臂端部厚
        Tc1 (float): 边梁悬臂根部厚
        x (float): 中梁翼板倒角宽
        xi1 (float): 倒角1宽（顶板）
        Tt1 (float): 倒角1根部厚
        xi2 (float): 倒角2宽（底板）
        yi2 (float): 倒角2高
        bSlope (bool): 是否输入横坡
            * 0 = 否
            * 1 = 是
        i1 (float): 顶左坡
        i2 (float): 顶右坡
        R (float): 底板倒角圆弧半径

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Section')
def osis_section_rect(nSec: int, strName: str, eSectionType: Literal["RECT"], TransitionType: Literal["Chamfer", "Fillet"], SecType: Literal["Solid", "Hollow"],
        B: float, H: float, xo1: float, yo1: float, R: float, t1: float, t2: float, xi1: float, yi1: float, HasDiaphragm: bool, tw: float, xi2: float, yi2: float,
        HasGroove: bool, b1: float, b2: float, h: float):
    """创建或修改矩形截面(RECT)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 RECT
        TransitionType (str): 倒角类型，可选值：
            * Chamfer: 斜倒角
            * Fillet: 圆倒角
        SecType (str): 截面类型，可选值：
            * Solid: 实腹截面
            * Hollow: 空腹截面
        B (float): 截面宽度
        H (float): 截面高度
        xo1 (float): 斜倒角宽度
        yo1 (float): 斜倒角高度
        R (float): 圆倒角半径
        t1 (float): 壁厚1
        t2 (float): 壁厚2
        xi1 (float): 内倒角宽度
        yi1 (float): 内倒角高度
        HasDiaphragm (bool): 隔板标志：
            * 0: 无隔板
            * 1: 有隔板
        tw (float): 隔板厚度
        xi2 (float): 隔板倒角宽度
        yi2 (float): 隔板倒角高度
        HasGroove (bool): 凹槽标志：
            * 0: 无凹槽
            * 1: 有凹槽
        b1 (float): 凹槽上口宽度
        b2 (float): 凹槽下口宽度
        h (float): 凹槽深度

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 创建基本实心矩形截面
        >>> result = section_rect(1, "截面1 (矩形)", "RECT", "Fillet", "Solid", 12.0, 2.0, 1.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.25, 0, 1.0, 0.5, 0.25, 0, 1.2, 0.8, 0.2)
        >>> print(result)
        (True, "")

    Note:
        - 单位：所有尺寸参数单位均为米(m)
        - 重复使用截面编号会修改现有截面
    """
    pass

# 0.9500,1.0000,0.5700,0.0500,0.1200,0.1200,0.1600,0.1200,0.1600,0.3800, 0.1500,0.0800,0.1200,0.0800,0.0500,0.0500,0.0800,0.0800,0.1200; SectionOffset,1,Middle,0.0000,Center,0.0000; SectionMesh,1,0,0.1000; 
@REGISTRY.register("Section")
def osis_section_hollowslab(nSec: int=1, strName: str="截面1-空心板", eSectionType: Literal["HOLLOWSLAB"]="HOLLOWSLAB", eGirderPos: Literal["LEFT", "MIDDLE", "RIGHT"]="MIDDLE", 
                          H: float=0.95, Bs: float=1.0, Bm: float=0.57, Bj: float=0.05, Tt: float=0.12, Tb: float=0.12, Tw: float=0.16, 
                          Tc: float=0.12, Tc1: float=0.16, Bc: float=0.38, xi1: float=0.15, yi1: float=0.08, xi2: float=0.12, yi2: float=0.08, xo3: float=0.05, yo3: float=0.05, xo4: float=0.08, yo4: float=0.08, h1: float=0.12):
    """定义或修改空心板截面(HOLLOWSLAB)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 HOLLOWSLAB
        eGirderPos (str): 截面位置
            * Left = 左边梁
            * Middle = 中梁
            * Right = 右边梁
        H (float): 板高
        Bs (float): 边板宽，eGirderPos=Middle时设置为 ""
        Bm (float): 中梁半宽
        Bj (float): 铰缝上端缩进宽
        Tt (float): 顶板厚
        Tb (float): 底板厚
        Tw (float): 腹板下端厚
        Tc (float): 边板悬臂端部厚，eGirderPos=Middle时设置为 ""
        Tc1 (float): 边板悬臂根部厚，eGirderPos=Middle时设置为 ""
        Bc (float): 边板悬臂厚，eGirderPos=Middle时设置为 ""
        xi1 (float): 倒角1宽（顶板）
        yi1 (float): 倒角1高
        xi2 (float): 倒角2宽（底板）
        yi2 (float): 倒角2高
        xo3 (float): 倒角3宽（上端）
        yo3 (float): 倒角3高
        xo4 (float): 倒角4宽（下端）
        yo4 (float): 倒角4高
        h1 (float): 下端竖直段高

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_custom(nSec: int, strName: str, eSectionType: Literal["CUSTOM"], contourMatrix: list):
    """定义或修改自定义截面(CUSTOM)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 CUSTOM
        contourMatrix (list): 轮廓点矩阵，大小为n*3，n为点的个数，第一列为点所在的轮廓线编号，第二列为点的x坐标，第三列为点的y坐标。需要按照行顺序组织成list

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
