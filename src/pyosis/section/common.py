'''
pyosis.section.interface 的 Docstring
'''

from typing import Any, Dict, Literal
from ..core import REGISTRY

@REGISTRY.register('Section')
def osis_section_Lshape(nSec: int, strName: str, eSectionType: Literal["LSHAPE"]="LSHAPE", nDir: Literal[0, 1]=1, H: float=0.1, B: float=0.1, Tf1: float=0.016, Tf2: float=0.016):
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
def osis_section_circle(nSec: int, strName: str, eSectionType: Literal["CIRCLE"]="CIRCLE", eCircleType: Literal["Hollow", "Solid"]="Solid", D: float=0.5, Tw: float=0.02):
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
def osis_section_Tshape(nSec: int, strName: str, eSectionType: Literal["TSHAPE"]="TSHAPE", nDir: Literal[0, 1]=1, H: float=0.3, B: float=0.2, Tf: float=0.016, Tw: float=0.016):
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
def osis_section_Ishape(nSec: int, strName: str, eSectionType: Literal["ISHAPE"]="ISHAPE", H: float=0.3, Bt: float=0.13, Bb: float=0.13, Tt: float=0.016, Tb: float=0.016, Tw: float=0.016):
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
def osis_section_smallbox(nSec: int, strName: str, eSectionType: Literal["SMALLBOX"]="SMALLBOX", eGirderPos: Literal["LEFT", "MIDDLE", "RIGHT"]="MIDDLE", 
                          H: float=1.6, Bs: float=1.65, Bm: float=1.2, Bc: float=0.0, Bb: float=1, Tt: float=0.18, Tb: float=0.2, Tw: float=0.2, i: float=4, 
                          Tc: float=0.18, Tc1: float=0.25, x: float=0.2, xi1: float=0.15, Tt1: float=0.25, xi2: float=0.05, yi2: float=0.05, bSlope: bool=False, i1: float=0.0, i2: float=0.0, R: float=0.05):
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
def osis_section_rect(nSec: int, strName: str, eSectionType: Literal["RECT"]="RECT", TransitionType: Literal["Chamfer", "Fillet"]="Fillet", SecType: Literal["Solid", "Hollow"]="Solid",
        B: float=6.5, H: float=3.2, xo1: float=1.0, yo1: float=0.5, R: float=0.5, t1: float=1.0, t2: float=1.0, xi1: float=0.5, yi1: float=0.25, HasDiaphragm: bool=False, tw: float=1.0, xi2: float=0.5, yi2: float=0.25,
        HasGroove: bool=False, b1: float=1.2, b2: float=0.8, h: float=0.2):
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
        Tc (float): 边板悬臂端部厚，eGirderPos=Middle时不变
        Tc1 (float): 边板悬臂根部厚，eGirderPos=Middle时不变
        Bc (float): 边板悬臂厚，eGirderPos=Middle时不变
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

@REGISTRY.register('Section')
def osis_section_rounded_end(nSec: int, strName: str, eSectionType: Literal["ROUNDEDEND"]="ROUNDEDEND", 
                             eFillingType: Literal["Solid", "Hollow"]="Solid",
                             B: float=7.0, H: float=3.0, R: float=2.0, bHasDiaphragm: bool=False, 
                             b: float=4.0, t: float=1.0, xi1: float=0.5, yi1: float=0.25, 
                             tw: float=1.0, xi2: float=0.5, yi2: float=0.25):
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
def osis_section_conventionalbox(nSec: int, strName: str, eSectionType: Literal["CONVENTIONALBOX"]="CONVENTIONALBOX",
                                  H: float=2.7, BtL: float=6.375, BtR: float=6.375, BbL: float=3.5, BbR: float=3.5, Bs: float=0.5,
                                  Tt: float=0.28, Tb: float=0.32, Tw1: float=0.5, Tw2: float=0.5, nCellNum: int=1,
                                  Bi1: float=5.05, Bi2: float=4.5, Bi3: float=5.05, Bi4: float=5.05,
                                  xi1: float=1.5, Tt1: float=0.7, xi2: float=0.0, Tt2: float=0.0, 
                                  xi3: float=1.0, yi3: float=0.5, xi4: float=0.5, Tt4: float=0.35,
                                  xi5: float=0.6, yi5: float=0.3, xi6: float=1.0, Tt6: float=0.5,
                                  xi7: float=0.6, yi7: float=0.3,
                                  BcL: float=2.875, TcL: float=0.2, Bc1L: float=1.325, Tc1L: float=0.7, Tc2L: float=0.4,
                                  bSymmetry: bool=True, BcR: float=2.875, TcR: float=0.2, Bc1R: float=1.325, Tc1R: float=0.7, Tc2R: float=0.4,
                                  eSlopeType: Literal["Integral", "CastInPlace"]="Integral",
                                  i: float=0, i1: float=0, i2: float=0, i3: float=0, i4: float=0,
                                  R1: float=0, R2: float=0):
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
        eSlopeType (str): 横坡类型，Integral=整体旋转找坡，CastInPlace=现浇模板找坡。
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
def osis_section_flat_box(nSec: int, strName: str, eSectionType: Literal["StreamedBox"]="StreamedBox",
                          H: float=4.0, BtL: float=20.0, BtR: float=20.0, BbL: float=10.5, BbR: float=10.5, Bs: float=0.8,
                          Tt: float=0.28, Tb1: float=0.27, Tb2: float=0.27, Tw: float=0.25, Ttj: float=0.5, Tbj: float=0.27, Twj: float=0.4,
                          nCellNum: int=5, Bi1: float=4.7, Bi2: float=6.85, Bi3: float=6, Bi4: float=6.85,
                          xi1: float=0.6, Tt1: float=0.6, xi2: float=1.0, Tt2: float=0.7,
                          xi3: float=0.2, yi3: float=0.2, xi4: float=1.0, Tt4: float=0.7,
                          xi5: float=0.6, yi5: float=0.3, xi6: float=0.5, Tt6: float=0.7,
                          xi7: float=0.5, yi7: float=0.3,
                          BcL: float=4.0, TcL: float=0.2, Bc1L: float=0.5, Tc1L: float=0.7, Tc2L: float=0.4,
                          bSymmetry: bool=True, BcR: float=4.0, TcR: float=0.2, Bc1R: float=0.5, Tc1R: float=0.7, Tc2R: float=0.4,
                          eSlopeType: Literal["Integral", "CastInPlace"]="Integral",
                          i: float=0.0, i1: float=0.0, i2: float=0.0, i3: float=0.0, i4: float=0.0,
                          R1: float=0.5, R2: float=0.2):
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
        eSlopeType (str): 横坡类型，Integral=整体旋转找坡，CastInPlace=现浇模板找坡。
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
def osis_section_double_side_box(nSec: int, strName: str, eSectionType: Literal["DOUBLESIDEBOX"]="DOUBLESIDEBOX",
                                 H: float=3.8, Bt: float=36.0, bt: float=14.8, Bs: float=2.1, Bb: float=4.4,
                                 tt: float=0.3, Tb1: float=0.3, Tb2: float=0.3, Tw: float=0.5,
                                 b: float=1.0, n: float=1.0, 
                                 Bi: float=8.0, xi1: float=1.0, Tt1: float=0.6, xi2: float=1.0, Tt2: float=0.7,
                                 xi3: float=0.6, yi3: float=0.3, xo4: float=1.0, Tt4: float=0.7, b1: float=0.3,
                                 eSlopeType: Literal["Integral", "CastInPlace"]="Integral",
                                 i: float=0.0, i1: float=0.0, i2: float=0.0):
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
        eSlopeType (str): 箱梁橫坡类型，Integral=整体旋转找坡，CastInPlace=现浇模板找坡。
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
def osis_section_ribbed_slab(nSec: int, strName: str, eSectionType: Literal["RIBBEDSLAB"]="RIBBEDSLAB",
                             H: float=2.8, Bt: float=21.5, bt: float=17.7, Tt: float=0.3,
                             b: float=0.2, h: float=1.25, b1: float=1.8, b2: float=0.2,
                             x: float=1.5, y: float=0.3,
                             eSlopeType: Literal["Integral", "CastInPlace"]="Integral",
                             i: float=0.0, i1: float=0.0, i2: float=0.0):
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
        eSlopeType (str): 横坡类型，Integral=整体旋转找坡，CastInPlace=现浇模板找坡。
        i (float): 整体转梁横坡，SlopeType=CastInPlace时缺省。
        i1 (float): 顶左坡，SlopeType=Integral时缺省。
        i2 (float): 顶右坡，SlopeType=Integral时缺省。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Section')
def osis_section_TGirder(nSec: int, strName: str, eSectionType: Literal["TGIRDER"]="TGIRDER",
                          eGirderPos: Literal["Left", "Middle", "Right"]="Middle",
                          H: float=2.5, Bs: float=1.125, Bm: float=0.85, Bc: float=0.0,
                          Tt1: float=0.16, Tt2: float=0.25, x: float=0.6, Tw: float=0.2,
                          Bh: float=0.6, Hh: float=0.35, yh: float=0.25,
                          bSlope: bool=False, i1: float=0.0, i2: float=0.0, R: float=0.05):
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


@REGISTRY.register("Section")
def osis_section_custom(nSec: int, strName: str, eSectionType: Literal["CUSTOM"], contourMatrix: str):
    """定义或修改自定义截面(CUSTOM)。

    Args:
        nSec (int): 截面编号，从1开始编号，所有类型的截面均使用同一编号序列。
        strName (str): 截面名称。
        eSectionType (str): 截面类型，固定为 CUSTOM
        contourMatrix (str): 轮廓点矩阵，大小为n*3，n为点的个数，第一列为点所在的轮廓线编号，第二列为点的x坐标，第三列为点的y坐标。需要使用osis_matrix先定义list

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    Example:
        >>> matrix = [[1, 2, 20], [2, 3, 25], [3, 4, 30], [4, 1, 25]]
        >>> osis_matrix("LineMatrix", matrix)
        >>> osis_section_custom(1,"三角形截面","CUSTOM","LineMatrix")
    """
    pass
