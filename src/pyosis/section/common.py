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
                          H: float, Bs: float, Bm: float, Bc: float, Bb: float, Tt: float, Tb: float, Tw: float, i: float, Tc: float, Tc1: float, x: float, xi1: float, Tt1: float, xi2: float, yi2: float, bSlope: bool, i1: float, i2: float, R: float):
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

@REGISTRY.register('Section')
def osis_section_rounded_end(nSec: int, strName: str, eSectionType: Literal["ROUNDEDEND"], 
                             eFillingType: Literal["Solid", "Hollow"],
                             B: float, H: float, R: float, bHasDiaphragm: bool, 
                             b: float, t: float, xi1: float, yi1: float, 
                             tw: float, xi2: float, yi2: float):
    """定义或修改圆端形截面(RoundedEnd)。

    Args:
        nSec (int): 截面编号，从1开始编号。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 ROUNDEDEND。
        eFillingType (str): 填充类型，Solid=实腹，Hollow=空腹。
        B (float): 截面宽。
        H (float): 截面高。
        R (float): 圆弧半径。
        bHasDiaphragm (bool): 是否有隔板，1=有隔板，0=无隔板。
        b (float): 内宽。
        t (float): 壁厚。
        xi1 (float): 内倒角宽。
        yi1 (float): 内倒角高。
        tw (float): 隔板厚。
        xi2 (float): 隔板倒角宽。
        yi2 (float): 隔板倒角高。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Section')
def osis_section_conventionalbox(nSec: int, strName: str, eSectionType: Literal["CONVENTIONALBOX"],
                                  H: float, BtL: float, BtR: float, BbL: float, BbR: float, Bs: float,
                                  Tt: float, Tb: float, Tw1: float, Tw2: float, nCellNum: int,
                                  Bi1: float, Bi2: float, Bi3: float, Bi4: float,
                                  xi1: float, Tt1: float, xi2: float, Tt2: float, 
                                  xi3: float, yi3: float, xi4: float, Tt4: float,
                                  xi5: float, yi5: float, xi6: float, Tt6: float,
                                  xi7: float, yi7: float,
                                  BcL: float, TcL: float, Bc1L: float, Tc1L: float, Tc2L: float,
                                  bSymmetry: bool, BcR: float, TcR: float, Bc1R: float, Tc1R: float, Tc2R: float,
                                  eSlopeType: Literal["Intergal", "CastInPlace"],
                                  i: float, i1: float, i2: float, i3: float, i4: float,
                                  R1: float, R2: float):
    """定义或修改常规箱梁截面(ConventionalBox)。

    Args:
        nSec (int): 截面编号，从1开始编号。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 CONVENTIONALBOX。
        H (float): 截面高度。
        BtL (float): 设计线左顶板宽。
        BtR (float): 设计线右顶板宽。
        BbL (float): 设计线左底板宽。
        BbR (float): 设计线右底板宽。
        Bs (float): 悬臂根部至边腹板顶内侧宽度。
        Tt (float): 顶板厚。
        Tb (float): 底板厚。
        Tw1 (float): 边腹板厚。
        Tw2 (float): 中腹板厚。
        nCellNum (int): 箱室个数。
        Bi1 (float): 箱室1宽度。
        Bi2 (float): 箱室2宽度。
        Bi3 (float): 箱室3宽度。
        Bi4 (float): 箱室4宽度。
        xi1 (float): 倒角1宽(边室顶板)。
        Tt1 (float): 倒角1根部厚。
        xi2 (float): 倒角2宽(边室顶板)。
        Tt2 (float): 倒角2根部厚。
        xi3 (float): 倒角3宽(边室顶板)。
        yi3 (float): 倒角3根部厚。
        xi4 (float): 倒角4宽(边室底板)。
        Tt4 (float): 倒角4高。
        xi5 (float): 倒角5宽(边室底板)。
        yi5 (float): 倒角5高。
        xi6 (float): 倒角6宽(中室顶板)。
        Tt6 (float): 倒角6根部厚。
        xi7 (float): 倒角7宽(中室底板)。
        yi7 (float): 倒角7高。
        BcL (float): 左悬臂长。
        TcL (float): 左悬臂端部厚。
        Bc1L (float): 左悬臂倒角1根部厚。
        Tc1L (float): 左悬臂倒角1根部厚（参数名重复，保留原定义）。
        Tc2L (float): 左悬臂倒角2根部厚。
        bSymmetry (bool): 右侧是否对称，0=非对称，1=对称。
        BcR (float): 右悬臂长。
        TcR (float): 右悬臂端部厚。
        Bc1R (float): 右悬臂倒角1宽。
        Tc1R (float): 右悬臂倒角1根部厚。
        Tc2R (float): 右悬臂倒角2根部厚。
        eSlopeType (str): 横坡类型，Intergal=整体旋转找坡，CastInPlace=现浇模板找坡。
        i (float): 整体旋转的横坡。
        i1 (float): 顶左坡。
        i2 (float): 顶右坡。
        i3 (float): 底左坡。
        i4 (float): 底右坡。
        R1 (float): 顶板倒角圆弧半径。
        R2 (float): 底板倒角圆弧半径。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Section')
def osis_section_flat_box(nSec: int, strName: str, eSectionType: Literal["FLATBOX"],
                          H: float, BtL: float, BtR: float, BbL: float, BbR: float, Bs: float,
                          Tt: float, Tb1: float, Tb2: float, Tw: float, Ttj: float, Tbj: float, Twj: float,
                          nCellNum: int, Bi1: float, Bi2: float, Bi3: float, Bi4: float,
                          xi1: float, Tt1: float, xi2: float, Tt2: float,
                          xi3: float, yi3: float, xi4: float, Tt4: float,
                          xi5: float, yi5: float, xi6: float, Tt6: float,
                          xi7: float, yi7: float,
                          BcL: float, TcL: float, Bc1L: float, Tc1L: float, Tc2L: float,
                          bSymmetry: bool, BcR: float, TcR: float, Bc1R: float, Tc1R: float, Tc2R: float,
                          eSlopeType: Literal["Intergal", "CastInPlace"],
                          i: float, i1: float, i2: float, i3: float, i4: float,
                          R1: float, R2: float):
    """定义或修改扁平箱梁截面(FlatBox)。

    Args:
        nSec (int): 截面编号，从1开始编号。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 FLATBOX。
        H (float): 截面高度。
        BtL (float): 设计线左顶板宽。
        BtR (float): 设计线右顶板宽。
        BbL (float): 设计线左底板宽。
        BbR (float): 设计线右底板宽。
        Bs (float): 悬臂根部至边腹板顶内侧宽度。
        Tt (float): 顶板厚。
        Tb1 (float): 底板厚。
        Tb2 (float): 斜底板厚。
        Tw (float): 腹板厚。
        Ttj (float): 加强室顶板厚。
        Tbj (float): 加强室底板厚。
        Twj (float): 加强室腹板厚。
        nCellNum (int): 箱室个数。
        Bi1 (float): 箱室1宽度。
        Bi2 (float): 箱室2宽度。
        Bi3 (float): 箱室3宽度。
        Bi4 (float): 箱室4宽度。
        xi1 (float): 倒角1宽(边室顶板)。
        Tt1 (float): 倒角1根部厚。
        xi2 (float): 倒角2宽(边室顶板)。
        Tt2 (float): 倒角2根部厚。
        xi3 (float): 倒角3宽(边室底板)。
        yi3 (float): 倒角3高。
        xi4 (float): 倒角4宽(一般中室底板)。
        Tt4 (float): 倒角4根部厚。
        xi5 (float): 倒角5宽(一般中室底板)。
        yi5 (float): 倒角5高。
        xi6 (float): 倒角6宽(加强中室顶板)。
        Tt6 (float): 倒角6根部厚。
        xi7 (float): 倒角7宽(加强中室底板)。
        yi7 (float): 倒角7高。
        BcL (float): 左悬臂长。
        TcL (float): 左悬臂端部厚。
        Bc1L (float): 左悬臂倒角1根部厚。
        Tc1L (float): 左悬臂倒角1根部厚。
        Tc2L (float): 左悬臂倒角2根部厚。
        bSymmetry (bool): 右侧是否对称，0=非对称，1=对称。
        BcR (float): 右悬臂长。
        TcR (float): 右悬臂端部厚。
        Bc1R (float): 右悬臂倒角1宽。
        Tc1R (float): 右悬臂倒角1根部厚。
        Tc2R (float): 右悬臂倒角2根部厚。
        eSlopeType (str): 横坡类型，Intergal=整体旋转找坡，CastInPlace=现浇模板找坡。
        i (float): 整体旋转的横坡。
        i1 (float): 顶左坡。
        i2 (float): 顶右坡。
        i3 (float): 底左坡。
        i4 (float): 底右坡。
        R1 (float): 顶板倒角圆弧半径。
        R2 (float): 底板倒角圆弧半径。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Section')
def osis_section_double_side_box(nSec: int, strName: str, eSectionType: Literal["DOUBLESIDEBOX"],
                                 H: float, Bt: float, bt: float, Bs: float, Bb: float,
                                 tt: float, Tb1: float, Tb2: float, Tw: float,
                                 b: float, n: float, Bi: float,
                                 xi1: float, Tt1: float, xi2: float, Tt2: float,
                                 xi3: float, yi3: float, xo4: float, Tt4: float, b1: float,
                                 eSlopeType: Literal["Intergal", "CastInPlace"],
                                 i: float, i1: float, i2: float):
    """定义或修改双边箱截面(DoubleSideBox)。

    Args:
        nSec (int): 截面编号，从1开始编号。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 DOUBLESIDEBOX。
        H (float): 梁高。
        Bt (float): 顶板顶宽。
        bt (float): 顶板底宽。
        Bs (float): 边箱实心段顶板宽。
        Bb (float): 底板宽。
        tt (float): 顶板厚。
        Tb1 (float): 底板厚。
        Tb2 (float): 斜底板厚。
        Tw (float): 腹板厚。
        b (float): 风嘴上部水平宽度。
        n (float): 风嘴上部竖向高度。
        Bi (float): 室内宽。
        xi1 (float): 倒角1宽(顶板边)。
        Tt1 (float): 倒角1根部厚。
        xi2 (float): 倒角2宽(顶板中)。
        Tt2 (float): 倒角2根部厚。
        xi3 (float): 倒角3宽(底板中)。
        yi3 (float): 倒角3高。
        xo4 (float): 倒角4宽(顶板)。
        Tt4 (float): 倒角4根部厚。
        b1 (float): 腹板内侧倒角宽。
        eSlopeType (str): 箱梁橫坡类型，Intergal=整体旋转找坡，CastInPlace=现浇模板找坡。
        i (float): 整体转梁横坡。
        i1 (float): 顶左坡。
        i2 (float): 顶右坡。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Section')
def osis_section_ribbed_slab(nSec: int, strName: str, eSectionType: Literal["RIBBEDSLAB"],
                             H: float, Bt: float, bt: float, Tt: float,
                             b: float, h: float, b1: float, b2: float,
                             x: float, y: float,
                             eSlopeType: Literal["Intergal", "CastInPlace"],
                             i: float, i1: float, i2: float):
    """定义或修改肋板式截面(RibbedSlab)。

    Args:
        nSec (int): 截面编号，从1开始编号。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 RIBBEDSLAB。
        H (float): 截面高度。
        Bt (float): 顶板顶宽。
        bt (float): 顶板底宽。
        Tt (float): 顶板厚。
        b (float): 风嘴上部水平宽度。
        h (float): 风嘴上部竖向宽度。
        b1 (float): 边肋底宽。
        b2 (float): 边肋内侧倒角宽。
        x (float): 顶板倒角宽。
        y (float): 顶板倒角高。
        eSlopeType (str): 横坡类型，Intergal=整体旋转找坡，CastInPlace=现浇模板找坡。
        i (float): 整体转梁横坡，SlopeType=CastInPlace时缺省。
        i1 (float): 顶左坡，SlopeType=Intergal时缺省。
        i2 (float): 顶右坡，SlopeType=Intergal时缺省。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Section')
def osis_section_TGirder(nSec: int, strName: str, eSectionType: Literal["TGIRDER"],
                          eGirderPos: Literal["Left", "Middle", "Right"],
                          H: float, Bs: float, Bm: float, Bc: float,
                          Tt1: float, Tt2: float, x: float, Tw: float,
                          Bh: float, Hh: float, yh: float,
                          bSlope: bool, i1: float, i2: float, R: float):
    """定义或修改T梁截面(TGirder)。

    Args:
        nSec (int): 截面编号，从1开始编号。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 TGIRDER。
        eGirderPos (str): 截面位置，Left=左边梁，Middle=中梁，Right=右边梁。
        H (float): 梁高。
        Bs (float): 边翼板宽，GirderPos=Middle时缺省。
        Bm (float): 中梁半宽。
        Bc (float): 现浇湿接缝半宽。
        Tt1 (float): 翼板厚。
        Tt2 (float): 翼板根部厚。
        x (float): 翼板倒角宽。
        Tw (float): 腹板厚度。
        Bh (float): 马蹄宽度。
        Hh (float): 马蹄高度。
        yh (float): 马蹄倒角高。
        bSlope (bool): 指定是否输入横坡，1=是，0=否。
        i1 (float): 顶左坡。
        i2 (float): 顶右坡。
        R (float): 顶板处倒角半径。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass