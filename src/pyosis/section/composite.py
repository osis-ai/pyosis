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
        H2, Bf2, Bf3, Tf2, Tf3, Tw2: 小纵梁（HasSteelI=0 时可填 0）
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
        H2, Bf2, Bf3, Tf2, Tf3, Tw2: 小纵梁/次梁（单梁时可填 0）
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
    """定义或修改自定义组合截面（COMPOSITECUSTOM）。"""
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
    ContourWidth: str,
):
    """自定义组合截面 - 面域 Part（Polygon）。"""
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
    """自定义组合截面 - 线域 Part（Line）。"""
    pass