"""预制枚举：pyosis 全部枚举的唯一出处 + 整数编码 → 名称。

设计（不重复维护映射表）：
    枚举成员名 **就是** OSIS 命令流里的写法，因此 str(枚举) / .name
    直接给出名字；整数编码是枚举的值。JSON 里只有编码，转名字走
    ``XxxType.name_of(code)``。

        >>> from pyosis.core.enums import SectionType
        >>> SectionType.name_of(5)      # "Rectangle"
        >>> str(SectionType.Rectangle)  # "Rectangle"
        >>> SectionType.Rectangle.value # 5
"""

from __future__ import annotations

from enum import IntEnum


# ══════════════════════════════════════════════
# 基类
# ══════════════════════════════════════════════


class OsisEnum(IntEnum):
    """OSIS 预制枚举基类。

    - ``str(e)`` / ``e.name`` → OSIS 命令流写法（成员名）
    - ``name_of(code)``       → 编码转名字；未知编码或 Unassigned 返回 ""
    - ``of(code)``            → 编码转成员；未知编码退回 Unassigned
    """

    def __str__(self) -> str:
        return self.name

    @classmethod
    def name_of(cls, code, default: str = "") -> str:
        """编码 → OSIS 命令流写法；未知编码 / Unassigned 返回 default。"""
        member = cls.of(code)
        return default if member.name == "Unassigned" else member.name

    @classmethod
    def of(cls, code):
        """编码 → 成员；未知编码 / None → Unassigned（所有子类都定义了它）。"""
        try:
            return cls(int(code))
        except (ValueError, TypeError):
            return cls.Unassigned


# ══════════════════════════════════════════════
# 枚举定义
# ══════════════════════════════════════════════


class ElementType(OsisEnum):
    """单元类型（PrepEnum::Element）"""
    Unassigned = 0
    BEAM3D = 1
    TRUSS = 2
    SPRING = 3
    CABLE = 4
    SHELL = 5
    SOLID = 6

    UNASSIGNED = 0  # 兼容旧拼写


class BoundaryType(OsisEnum):
    """边界类型（PrepEnum::Boundary）"""
    Unassigned = 0
    GENERAL = 1				    # 一般支撑
    MSTSLV = 2				    # 主从约束
    RELEASE = 3				    # 释放梁端约束
    ELSTCSPT = 4				# 节点弹性支承
    GES = 5				        # 一般弹性支承（GeneralElstcSpt）
    RIGID = 6				    # 刚性连接
    SECF = 7                    # 截面特性修改
    GLINK = 8                   # 一般连接
    UNISPT = 9                  # 单向弹性支承
    UNILNK = 10                 # 单向弹性连接
    LELNK = 11                  # 线弹性连接
    SOILSPRING = 12             # 土弹簧
    SURFSPT = 13                # 面弹性支承

    UNASSIGNED = 0              # 兼容旧拼写
    GENERALELSTCSPT = 5         # 兼容旧命名（= GES）


class MaterialType(OsisEnum):
    """材料类型（PrepEnum::Material）"""
    Unassigned = 0      # 未定义
    CONC = 1            # 混凝土
    STEEL = 2           # 钢材
    PRESTRESSED = 3     # 预应力
    REBAR = 4           # 钢筋
    CUSTOM = 5          # 自定义

    UNASSIGNED = 0      # 兼容旧拼写
    Prestressed = 3     # 兼容旧命名
    Rebar = 4           # 兼容旧命名
    Custom = 5          # 兼容旧命名


class MaterialCode(OsisEnum):
    """材料规范（PrepEnum::Code，值非连续）"""
    Unassigned = 0
    JTG3362_2018 = 1
    JTGD62_2004 = 2
    JTGD60_2015 = 3
    JTGT2231_01_2020 = 4
    JTGD64_2015 = 5
    GBT5224_2014 = 6
    GBT20065_2016 = 7
    GB50017_2017 = 8
    GB50018_2002 = 9
    GBT50018_2025 = 10
    GB50017_2003 = 11
    GBJ17_1988 = 12
    JGJ99_2015 = 13
    JGJ99_1998 = 14
    GBT50010_2010 = 15
    GB50010_2002 = 16
    CUSTOM = 17
    CJJ112011_19 = 18

    UNASSIGNED = 0      # 兼容旧拼写


class SectionType(OsisEnum):
    """截面类型（PrepEnum::Section，值非连续，勿按顺序推）"""
    Unassigned = 0  # 未分配
    LShape = 1  # L形与倒L形
    TShape = 2  # T形与倒T形
    IShape = 3  # 工字形
    Circle = 4  # 圆形与圆管形
    Rectangle = 5  # 实腹与空腹矩形（可倒圆/斜角）
    RoundedEndShape = 6  # 实腹与空腹圆端形
    HollowSlab = 7  # 空心板梁
    SmallBox = 8  # 小箱梁
    TGirder = 9  # T梁
    ConventionalBox = 10  # 常规箱梁
    StreamedBox = 11  # 扁平箱梁
    DoubleSideBox = 12  # 双边箱梁
    RibbedSlab = 13  # 肋板式
    CustomShape = 14  # 常规自定义截面

    SteelBeamI = 21  # 工字钢梁截面
    SteelBeamBox = 22  # 箱型钢梁截面
    SteelBoxThreeCell = 23  # 单箱单/三室钢梁截面
    SteelBoxInclinedTF = 24  # 单箱单室斜顶板钢梁界面
    SteelCantiBox = 25  # 悬臂单箱单/双室钢梁界面
    SteelCantiBoxInclinedBF = 26  # 悬臂单箱单/双室斜底板钢梁截面
    SteelCustom = 27  # 钢梁自定义截面，采用几何点线形式输入
    SteelCustomPlate = 28  # 钢梁自定义截面，采用参数板形式输入

    CompositeSteelI = 41  # 钢-工字型组合截面
    CompositeSteelTrough = 42  # 钢-槽型组合截面
    CompositeSteelBox = 43  # 钢-箱型组合截面

    CompositeCustom = 61  # 自定义组合截面

    NumericalSection = 71  # 数值截面

    BUDoubleAngle1 = 81  # 双角钢截面
    BUDoubleC = 82  # 双槽钢截面
    BUDoubleH = 83  # 双H型钢截面
    BUDoubleCWeb1 = 84  # 双槽钢+腹板截面1
    BUDoubleCWeb2 = 85  # 双槽钢+腹板截面2
    BUHWithPlates = 86  # H型钢+双板截面
    BUDoubleAngle2 = 87  # 交叉角钢

    SteelL = 100  # 型钢-L型
    SteelC = 101  # 型钢-槽型
    SteelI = 102  # 型钢-工字型
    SteelBox = 103  # 型钢-箱型
    SteelT = 104  # 型钢-T型
    SteelCC = 105  # 型钢-双C型
    SteelCircularHollow = 106  # 型钢-圆管
    SteelZ = 107  # 型钢-Z型

    # ── 兼容旧命名（pyosis 0.x 曾用全大写）──
    UNASSIGNED = 0
    LSHAPE = 1
    TSHAPE = 2
    ISHAPE = 3
    CIRCLE = 4
    RECTANGLE = 5
    ROUNDEDEND = 6
    HOLLOWSLAB = 7
    SMALLBOX = 8
    TGIRDER = 9
    CONVENTIONALBOX = 10
    STREAMEDBOX = 11
    DOUBLESIDEBOX = 12
    RIBBEDSLAB = 13
    CUSTOM = 14
    STEELBEAMI = 21
    STEELBEAMBOX = 22
    STEELBOXTHREECELL = 23
    STEELBOXITF = 24
    STEELCANTIBOX = 25
    STEELCANTIBOXIBF = 26
    STEELCUSTOM = 27
    STEELCUSTOMPLATE = 28
    COMPOSITESTEELI = 41
    COMPOSITESTEELTROUGH = 42
    COMPOSITESTEELBOX = 43
    COMPOSITECUSTOM = 61
    NUMERICAL = 71
    BUDOUBLEANGLE = 81
    BUDOUBLEC = 82
    BUDOUBLEH = 83
    BUDOUBLECWEB1 = 84
    BUDOUBLECWEB2 = 85
    BUHWITHPLATES = 86
    BUDOUBLEANGLE2 = 87
    STEELL = 100
    STEELC = 101
    STEELI = 102
    STEELBOX = 103
    STEELT = 104
    STEELCC = 105
    STEELCIRCULARHOLLOW = 106
    STEELZ = 107


class LoadCaseType(OsisEnum):
    """荷载工况类型（PrepEnum::LoadCase）"""
    Unassigned = 0
    USER = 1      # 用户自定义荷载
    D = 2         # 恒荷载
    DC = 3        # 结构和非结构附属荷载
    DW = 4        # 铺装和设备荷载
    DD = 5        # 桩端摩擦力
    EP = 6        # 地面压力
    EH = 7        # 水平土压力
    EV = 8        # 竖向土压力
    ES = 9        # 覆盖土压力
    LS = 10       # 附加地面活荷载
    LSC = 11      # 平板挂车或履带车附加地面活荷载
    L = 12        # 活荷载
    LC = 13       # 平板挂车或履带车荷载
    LP = 14       # 超载
    IL = 15       # 汽车冲击力
    ILP = 16      # 超载冲击力
    CF = 17       # 汽车离心力
    BRK = 18      # 汽车制动力
    BK = 19       # 活荷载引起的纵向内力
    PL = 20       # 人群荷载
    PS = 21       # 预应力
    B = 22        # 浮力
    WP = 23       # 地下水压力
    FP = 24       # 流体压力
    SF = 25       # 流水压力
    WPR = 26      # 波压
    W = 27        # 风荷载
    WL = 28       # 与车辆活荷载同时作用的风荷载
    STL = 29      # 基础变位影响力
    CR = 30       # 徐变
    SH = 31       # 收缩
    T = 32        # 温度荷载
    TPG = 33      # 温度梯度
    CO = 34       # 冲击力
    CT = 35       # 车辆撞击力
    CV = 36       # 船只或漂流物撞击力
    E = 37        # 地震作用
    FR = 38       # 摩擦力
    IP = 39       # 冰压力
    CS = 40       # 施工阶段荷载
    ER = 41       # 施工荷载
    EL = 42       # 累积施工应力
    RS = 43       # 加劲肋收缩
    LR = 44       # 屋面活荷载
    S = 45        # 雪荷载
    R = 46        # 雨荷载
    W1 = 47       # 活载风
    W2 = 48       # 极限风
    WF1 = 49      # W1 引起的浪
    WF2 = 50      # W2 引起的浪
    FL = 51       # 疲劳荷载
    TG = 52       # 梯度温度
    CFS = 53      # 船舶的撞击作用
    CFV = 54      # 汽车撞击作用
    IF = 55       # 汽车冲击力
    CRL = 56      # 人群荷载
    CFD = 57      # 漂流物的撞击作用

    UNASSIGNED = 0  # 兼容旧拼写


class SplineType(OsisEnum):
    """样条曲线类型（PropEnum::Spline）
    0 = 未分配；名字即 spline3d 命令的类型写法。
    """
    Unassigned = 0
    GENERAL = 1     # 一般边界
    NATURAL = 2     # 自然边界
    ARC3D = 3       # 3D 圆弧
    ARC2D = 4       # 2D 圆弧

    UNASSIGNED = 0  # 兼容旧拼写
    General = 1     # 兼容旧命名
    Natural = 2     # 兼容旧命名
    Arc3D = 3       # 兼容旧命名
    Arc2D = 4       # 兼容旧命名


class TensionType(OsisEnum):
    """钢束张拉方式（LoadEnum::TensionType）

    不是命令流写法——C++ 用它区分先张/后张的类继承，print name 为空，
    名字只在 Python 侧做分类。
    """
    Unassigned = 0
    Pre = 1             # 先张法
    In = 2              # 后张法（体内）
    Ex = 3              # 后张法（体外）

    UNASSIGNED = 0      # 兼容旧拼写


class LiveGradeType(OsisEnum):
    """活载等级（LoadEnum::LiveGrade）"""
    Unassigned = 0
    HIGHWAY_I = 1        # 公路-I 级（车道荷载）
    HIGHWAY_II = 2       # 公路-II 级（车道荷载）
    VEHICLE = 3          # 车辆荷载
    CROWD = 4            # 人群荷载
    FATIGUE_I = 5        # 疲劳荷载 I
    FATIGUE_II = 6       # 疲劳荷载 II
    FATIGUE_III = 7      # 疲劳荷载 III
    UF = 8
    V = 9
    VG = 10
    NHWCD = 11
    NHWRQ = 12
    OHWRQ = 13
    CCD_A = 14           # 城-车道 A
    CCD_B = 15           # 城-车道 B
    CCL_A = 16           # 城-车辆 A
    CCL_B = 17           # 城-车辆 B
    CT160 = 18
    CT220 = 19
    CT300 = 20
    CT420 = 21
    CRQ = 22             # 城-人群

    UNASSIGNED = 0       # 兼容旧拼写


class LiveTypeForCustom(OsisEnum):
    """自定义活载类型（LoadEnum::LiveTypeForCustom）

    只在活载等级 grade 取自定义类取值时有效；C++ 侧 0 的拼写是 UNASSIGNEND。
    """
    Unassigned = 0
    VEHICLE = 1          # 车辆
    TRAIN = 2            # 列车
    CROWD = 3            # 人群


class AnalysisType(OsisEnum):
    """分析特性类型（PrepEnum::Analysis）

    分析类实体（活载等级、车道、活载工况等）都挂在 AnalysisBaseInfo 下，
    analysisType 标识它属于哪张列表。
    """
    Unassigned = 0
    Load = 1
    Buckling = 2
    SetlGrp = 3          # 沉降组
    Settlement = 4       # 沉降分析
    Damping = 5          # 阻尼特性
    SeisRspSpec = 6      # 反应谱函数
    Spectrum = 7         # 反应谱分析
    LiveGrade = 8        # 活载等级
    Lane = 9             # 车道
    Live = 10            # 活载工况
    Modal = 11
    LoadToMass = 12      # 荷载转质量
    Seastate = 13
    Transient = 14       # 时程分析
    LaneSurface = 15     # 车道面


class PropertyType(OsisEnum):
    """特性列表类型（PrepEnum::Property）

    属性类实体（收缩徐变、坐标系、P-U 曲线等）都挂在 PropertyBaseInfo 下，
    propertyType 标识它属于哪张列表。与 AnalysisType 是两个不同的枚举。
    """
    Unassigned = 0
    PUCurve = 1               # 力-位移曲线
    CreepShrink = 2           # 收缩徐变
    TheoreticalThickness = 3  # 单元理论厚度
    Spline = 4                # 样条曲线
    CoorSys = 5               # 坐标系
    ShellThickness = 6        # 壳厚度
    StrengthPrg = 7           # 强度进展特性


class SectionOffsetY(OsisEnum):
    """截面 Y 向偏心类型（SecEnum::SectionOffsetY）

    命令流 SecOff 只认 Left / Middle / Right，Manual 只能读出来——
    回写时 C++ 的解析分支里没有它。
    """
    Unassigned = -1
    Left = 0
    Middle = 1
    Right = 2
    Manual = 3           # 手动指定偏心值


class SectionOffsetZ(OsisEnum):
    """截面 Z 向偏心类型（SecEnum::SectionOffsetZ）

    命令流 SecOff 只认 Top / Center / Bottom，Manual 只能读出来——
    回写时 C++ 的解析分支里没有它。
    """
    Unassigned = -1
    Top = 0
    Center = 1
    Bottom = 2
    Manual = 3           # 手动指定偏心值


# ══════════════════════════════════════════════
# 便捷函数（等价于 XxxType.name_of）
# ══════════════════════════════════════════════

element_type_name = ElementType.name_of
boundary_type_name = BoundaryType.name_of
material_type_name = MaterialType.name_of
material_code_name = MaterialCode.name_of
section_type_name = SectionType.name_of
loadcase_type_name = LoadCaseType.name_of
spline_type_name = SplineType.name_of
live_grade_name = LiveGradeType.name_of
live_type_for_custom_name = LiveTypeForCustom.name_of
analysis_type_name = AnalysisType.name_of
property_type_name = PropertyType.name_of
section_offset_y_name = SectionOffsetY.name_of
section_offset_z_name = SectionOffsetZ.name_of


# ══════════════════════════════════════════════
# 约束自由度
# ══════════════════════════════════════════════

DOF_NAMES: tuple[str, ...] = ("DX", "DY", "DZ", "RX", "RY", "RZ", "RW")


def constraints_to_dict(constraints) -> dict[str, bool]:
    """7 位约束列表 → {DX: bool, ..., RW: bool}。

    C++ 侧透传的是固定顺序的整数列表，1 = 约束、0 = 释放。
    位数不足时按实际长度截断（主从约束只有 6 位）。
    """
    values = list(constraints or [])
    return {
        name: bool(int(values[i]))
        for i, name in enumerate(DOF_NAMES)
        if i < len(values)
    }


__all__ = [
    "OsisEnum",
    "ElementType", "BoundaryType", "MaterialType", "MaterialCode",
    "SectionType", "LoadCaseType", "SplineType", "TensionType",
    "LiveGradeType", "LiveTypeForCustom", "AnalysisType", "PropertyType",
    "SectionOffsetY", "SectionOffsetZ",
    "element_type_name", "boundary_type_name", "material_type_name",
    "material_code_name", "section_type_name", "loadcase_type_name",
    "spline_type_name", "live_grade_name", "live_type_for_custom_name",
    "analysis_type_name", "property_type_name",
    "section_offset_y_name", "section_offset_z_name",
    "DOF_NAMES", "constraints_to_dict",
]
