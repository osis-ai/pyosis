from typing import Literal

from ..core import REGISTRY


@REGISTRY.register("Section")
def osis_section_composite_steel_i(
    Index: int,
    Name: str,
    Type: Literal["COMPOSITESTEELI"],
    Bt: float,
    Bc: float,
    Tt1: float,
    Tt2: float,
    Tt3: float,
    Tc1: float,
    Tc2: float,
    B1: float,
    B2: float,
    x1: float,
    x2: float,
    x3: float,
    GirderNum: Literal["SINGLE", "DOUBLE", "TRIPLE"],
    H1: float,
    Bf1: float,
    Bb1: float,
    Tf1: float,
    Tb1: float,
    Tw1: float,
    WebRibPos1: Literal["LEFT", "RIGHT", "BOTH"],
    MiddleSameWithSide: Literal[0, 1],
    H2: float,
    Bf2: float,
    Bb2: float,
    Tf2: float,
    Tb2: float,
    Tw2: float,
    WebRibPos2: Literal["LEFT", "RIGHT", "BOTH"],
):
    """定义或修改工字型钢组合截面（COMPOSITESTEELI）。

    Args:
        Index: 截面编号
        Name: 截面名
        Type: 固定为 COMPOSITESTEELI
        Bt: 板宽
        Bc: 悬臂长
        Tt1: 标准段板厚
        Tt2: 两侧加厚段板厚
        Tt3: 中间加厚段板厚
        Tc1: 悬臂端板厚
        Tc2: 悬臂倒角处板厚
        B1: 两侧加厚段板宽
        B2: 中间加厚段板宽
        x1, x2, x3: 倒角
        GirderNum: SINGLE=单梁, DOUBLE=双梁, TRIPLE=三梁
        H1, Bf1, Bb1, Tf1, Tb1, Tw1, WebRibPos1: 边梁
        MiddleSameWithSide: 中梁构造同边梁，1=相同，0=不同
        H2, Bf2, Bb2, Tf2, Tb2, Tw2, WebRibPos2: 中梁（MiddleSameWithSide=1 时 H2 等可填 0）
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_composite_steel_trough(
    Index: int,
    Name: str,
    Type: Literal["COMPOSITESTEELTROUGH"],
    Bt: float,
    Bc: float,
    Tt1: float,
    Tt2: float,
    Tt3: float,
    Tc1: float,
    Tc2: float,
    B1: float,
    B2: float,
    x1: float,
    x2: float,
    x3: float,
    H1: float,
    Bb: float,
    Bf1: float,
    Tf1: float,
    Tb: float,
    Tw1: float,
    RightSameWithLeft: Literal[0, 1],
    HasSteelI: Literal[0, 1],
    H2: float,
    Bf2: float,
    Bf3: float,
    Tf2: float,
    Tf3: float,
    Tw2: float,
):
    """定义或修改槽型钢组合截面（COMPOSITESTEELTROUGH）。

    Args:
        Index: 截面编号
        Name: 截面名
        Type: 固定为 COMPOSITESTEELTROUGH
        Bt: 板宽
        Bc: 悬臂长
        Tt1: 标准段板厚
        Tt2: 两侧加厚段板厚
        Tt3: 中间加厚段板厚
        Tc1: 悬臂端板厚
        Tc2: 悬臂倒角处板厚
        B1: 两侧加厚段板宽
        B2: 中间加厚段板宽
        x1, x2, x3: 倒角
        H1: 主梁梁高
        Bb: 主梁底板宽
        Bf1: 主梁上翼缘宽
        Tf1: 主梁上翼缘厚
        Tb: 主梁底板厚
        Tw1: 主梁腹板厚
        RightSameWithLeft: 右腹板加劲肋布置是否与左侧相同，1=相同，0=不同
        HasSteelI: 是否有小纵梁，1=有，0=无
        H2:小纵梁梁高,
        Bf2:小纵梁上翼缘宽,
        Bf3:小纵梁下翼缘宽,
        Tf2:小纵梁上翼缘厚,
        Tf3:小纵梁下翼缘厚,
        Tw2:小纵梁腹板厚
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
@REGISTRY.register("Section")
def osis_section_composite_steel_box(
    Index: int,
    Name: str,
    Type: Literal["COMPOSITESTEELBOX"],
    Bt: float,
    Bc: float,
    Tt1: float,
    Tt2: float,
    Tt3: float,
    Tc1: float,
    Tc2: float,
    B1: float,
    B2: float,
    x1: float,
    x2: float,
    x3: float,
    GirderNum: Literal["SINGLE", "DOUBLE", "TRIPLE"],
    H1: float,
    Bf1: float,
    Bct: float,
    Bb: float,
    Bcb: float,
    Tf1: float,
    Tb: float,
    Tw1: float,
    SameLayout: Literal[0, 1],
    H2: float,
    Bf2: float,
    Bf3: float,
    Tf2: float,
    Tf3: float,
    Tw2: float,
):
    """定义或修改箱型钢组合截面（COMPOSITESTEELBOX）。

    Args:
        Index: 截面编号
        Name: 截面名
        Type: 固定为 COMPOSITESTEELBOX
        Bt: 板宽
        Bc: 悬臂长
        Tt1: 标准段板厚
        Tt2: 两侧加厚段板厚
        Tt3: 中间加厚段板厚
        Tc1: 悬臂端板厚
        Tc2: 悬臂倒角处板厚
        B1: 两侧加厚段板宽
        B2: 中间加厚段板宽
        x1, x2, x3: 倒角
        GirderNum: SINGLE=单梁, DOUBLE=双梁, TRIPLE=三梁
        H1: 主梁梁高
        Bf1: 主梁上翼缘宽
        Bct: 主梁上翼缘悬出宽
        Bb: 主梁下翼缘宽
        Bcb: 主梁下翼缘悬出宽
        Tf1: 主梁上翼缘厚
        Tb: 主梁下翼缘厚
        Tw1: 主梁腹板厚
        SameLayout: 下翼缘加劲肋布置与上翼缘是否相同，1=相同，0=不同
        H2:小纵梁梁高
        Bf2:小纵梁上翼缘宽
        Bf3:小纵梁下翼缘宽
        Tf2:小纵梁上翼缘厚
        Tf3:小纵梁下翼缘厚
        Tw2:小纵梁腹板厚
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("Section")
def osis_section_composite_custom(
    Index: int,
    Name: str,
    Type: Literal["COMPOSITECUSTOM"],
    PartNum: int,
    BaseE: float,
    BaseMu: float,
):
    """定义或修改自定义组合截面（COMPOSITECUSTOM）。
    Args:
        Index:编号
        Name:截面名
        Type:CustomComp=自定义组合截面
        PartNum:截面分部数量
        BaseE:基准材料的弹性模量
        BaseMu:基准材料的泊松比
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SectionPart")
def osis_section_part_polygon(
    SecIndex: int,
    PartIndex: int,
    PartMatType: Literal["Concrete", "Steel"],
    PartE: float,
    PartMu: float,
    PartDensity: float,
    PartGeoType: Literal["Polygon"],
    ContourMatrix: str,
):
    """定义或修改自定义组合截面的面域Part信息。
    Args:
        SecIndex：截面编号
        PartIndex：Part编号
        PartMatType：=Concrete为混凝土，可布置钢筋，=Steel为钢，不可布置钢筋
        PartE：分部弹性模量
        PartMu：分部泊松比
        PartDensity：分部重度
        PartGeoType：分部几何类型，=Polygon为面域
        ContourMatrix：轮廓点矩阵，大小为n*3，n为点的个数，第一列为点所在的轮廓线编号，第二列为点的x坐标，第三列为点的y坐标
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SectionPart")
def osis_section_part_line(
    SecIndex: int,
    PartIndex: int,
    PartMatType: Literal["Concrete", "Steel"],
    PartE: float,
    PartMu: float,
    PartDensity: float,
    PartGeoType: Literal["Line"],
    PointMatrix: str,
    LineMatrix: str,
    WidthMatrix: str,
):
    """定义或修改自定义组合截面的线域Part信息。
    Args:
        SecIndex：截面编号
        PartIndex：Part编号
        PartMatType：=Concrete为混凝土，可布置钢筋，=Steel为钢，不可布置钢筋
        PartE：分部弹性模量
        PartMu：分部泊松比
        PartDensity：分部重度
        PartGeoType：分部几何类型，=Line为线域
        PointMatrix：n行3列，几何点矩阵，每行第一个元素为点的编号，第二个元素为点的x坐标，第三个元素为点的y坐标
        LineMatrix：n行2列，几何线矩阵，第一列为点所在的轮廓线编号，第二列为点的编号
        WidthMatrix：n行1列，轮廓线宽度矩阵，n为轮廓线数量，与ContourMatrix中最大编号须保持一致



        ContourMatrix：轮廓点矩阵，大小为n*3，n为点的个数，第一列为点所在的轮廓线编号（从1开始一次递增），第二列为点的x坐标，第三列为点的y坐标
        ContourWidth：轮廓线宽度矩阵，大小为n*1，n为轮廓线数量，与ContourMatrix中最大编号须保持一致

        PointMatrix：n行3列，几何点矩阵，每行第一个元素为点的编号，第二个元素为点的x坐标，第三个元素为点的y坐标
        LineMatrix：n行2列，几何线矩阵，第一列为点所在的轮廓线编号，第二列为点的编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass