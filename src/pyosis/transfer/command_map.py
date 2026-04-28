"""命令流 → pyosis Engine API 映射表

本模块维护 OSIS 命令流与 pyosis 管理类 API 之间的双向映射。
映射键为 (命令名, 子类型)，其中子类型用于区分多态命令。

用法:
    from pyosis.transfer import CMD_MAP
    
    # 查询命令映射
    info = CMD_MAP[("Boundary", "GENERAL")]
    print(info.engine_method)  # "engine.boundary.create_general"
    print(info.params)         # ["no", "nCoor", "bX", "bY", ...]
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict


@dataclass
class CommandMapping:
    """命令映射信息"""
    engine_method: str          # Engine API 方法路径，如 "engine.material.create_conc"
    params: List[str]           # 参数名列表，按命令流中参数出现的顺序
    description: str            # 命令描述
    creates_object: bool = False    # 是否创建新对象（用于编号追踪）
    object_type: Optional[str] = None   # 对象类型（material/node/element/boundary/section/loadcase）
    returns_list: bool = False      # 返回值是否为列表（用于函数返回语句）
    is_group_op: bool = False       # 是否为组操作（单元组、边界组等）
    needs_context: bool = False     # 是否需要上下文（如 element.group 需要 element 前缀）


# ──────────────────────────────────────────────
# 命令映射表
# ──────────────────────────────────────────────

CMD_MAP: Dict[Tuple[str, Optional[str]], CommandMapping] = {
    # ============================================
    # CONTROL - 全局控制参数
    # ============================================
    ("Acel", None): CommandMapping(
        engine_method="engine.control.set_gravity_acceleration",
        params=["dG"],
        description="重力加速度",
    ),
    ("CalcTendon", None): CommandMapping(
        engine_method="engine.control.set_calc_tendon",
        params=["bFlag"],
        description="是否计算预应力",
    ),
    ("CalcConForce", None): CommandMapping(
        engine_method="engine.control.set_calc_concurrent_force",
        params=["bFlag"],
        description="是否计算并发反力",
    ),
    ("CalcShrink", None): CommandMapping(
        engine_method="engine.control.set_calc_shrink",
        params=["bFlag"],
        description="是否计算收缩",
    ),
    ("CalcCreep", None): CommandMapping(
        engine_method="engine.control.set_calc_creep",
        params=["bFlag"],
        description="是否计算徐变",
    ),
    ("CalcShear", None): CommandMapping(
        engine_method="engine.control.set_calc_shear",
        params=["bFlag"],
        description="是否计算剪切",
    ),
    ("CalcRlx", None): CommandMapping(
        engine_method="engine.control.set_calc_relaxation",
        params=["bFlag"],
        description="是否计算钢束松弛",
    ),
    ("ModLocCoor", None): CommandMapping(
        engine_method="engine.control.set_mod_loc_coor",
        params=["bFlag"],
        description="是否修改变截面单元局部坐标轴",
    ),
    ("IncTendon", None): CommandMapping(
        engine_method="engine.control.set_inc_tendon",
        params=["bFlag"],
        description="是否考虑钢束自重",
    ),
    
    # ============================================
    # MATERIAL - 材料
    # ============================================
    ("Material", "CONC"): CommandMapping(
        engine_method="engine.material.create_conc",
        params=["no", "strName", "eCode", "eGrade", "nCrepShrk", "dDmp"],
        description="混凝土材料",
        creates_object=True,
        object_type="material",
        returns_list=True,
    ),
    ("Material", "STEEL"): CommandMapping(
        engine_method="engine.material.create_steel",
        params=["no", "strName", "eCode", "eGrade", "dDmp"],
        description="钢材",
        creates_object=True,
        object_type="material",
        returns_list=True,
    ),
    ("Material", "PRESTRESSED"): CommandMapping(
        engine_method="engine.material.create_prestressed",
        params=["no", "strName", "eCode", "eGrade", "dDmp"],
        description="预应力材料",
        creates_object=True,
        object_type="material",
        returns_list=True,
    ),
    ("Material", "REBAR"): CommandMapping(
        engine_method="engine.material.create_rebar",
        params=["no", "strName", "eCode", "eGrade", "dDmp"],
        description="钢筋",
        creates_object=True,
        object_type="material",
        returns_list=True,
    ),
    ("Material", "CUSTOM"): CommandMapping(
        engine_method="engine.material.create_custom",
        params=["no", "strName", "dE", "dG", "dMu", "dExpCoeff", "dUnitWeight", "dDensity", "dDmp"],
        description="自定义材料",
        creates_object=True,
        object_type="material",
        returns_list=True,
    ),
    ("MaterialDel", None): CommandMapping(
        engine_method="engine.material.delete",
        params=["no"],
        description="删除材料",
    ),
    ("MaterialMod", None): CommandMapping(
        engine_method="engine.material.renumber",
        params=["old_no", "new_no"],
        description="修改材料编号",
    ),
    
    # ============================================
    # NODE - 节点
    # ============================================
    ("Node", None): CommandMapping(
        engine_method="engine.node.create",
        params=["no", "x", "y", "z"],
        description="创建节点",
        creates_object=True,
        object_type="node",
        returns_list=True,
    ),
    ("NodeDel", None): CommandMapping(
        engine_method="engine.node.delete",
        params=["no"],
        description="删除节点",
    ),
    ("NodeMod", None): CommandMapping(
        engine_method="engine.node.renumber",
        params=["old_no", "new_no"],
        description="修改节点编号",
    ),
    
    # ============================================
    # ELEMENT - 单元
    # ============================================
    ("Element", "BEAM3D"): CommandMapping(
        engine_method="engine.element.create_beam3d",
        params=["no", "node1", "node2", "nMat", "nSec1", "nSec2", "nYTrans", "nZTrans", "dStrain", "bFlag", "dTheta", "bWarping"],
        description="梁单元",
        creates_object=True,
        object_type="element",
        returns_list=True,
    ),
    ("Element", "TRUSS"): CommandMapping(
        engine_method="engine.element.create_truss",
        params=["no", "node1", "node2", "nMat", "nSec1", "nSec2", "dStrain"],
        description="桁架单元",
        creates_object=True,
        object_type="element",
        returns_list=True,
    ),
    ("Element", "SPRING"): CommandMapping(
        engine_method="engine.element.create_spring",
        params=["no", "node1", "node2", "bLinear", "dx", "dy", "dz", "rx", "ry", "rz", "dBeta"],
        description="弹簧单元",
        creates_object=True,
        object_type="element",
        returns_list=True,
    ),
    ("Element", "CABLE"): CommandMapping(
        engine_method="engine.element.create_cable",
        params=["no", "node1", "node2", "nMat", "nSec", "eMethod", "dPara"],
        description="拉索单元",
        creates_object=True,
        object_type="element",
        returns_list=True,
    ),
    ("Element", "SHELL"): CommandMapping(
        engine_method="engine.element.create_shell",
        params=["no", "bIsThin", "nMat", "nThk", "node1", "node2", "node3", "node4"],
        description="壳单元",
        creates_object=True,
        object_type="element",
        returns_list=True,
    ),
    ("ElementDel", None): CommandMapping(
        engine_method="engine.element.delete",
        params=["no"],
        description="删除单元",
    ),
    ("ElementMod", None): CommandMapping(
        engine_method="engine.element.renumber",
        params=["old_no", "new_no"],
        description="修改单元编号",
    ),
    ("EleGrp", None): CommandMapping(
        engine_method="engine.element.group",
        params=["strName", "eOP", "param"],
        description="单元组操作",
        is_group_op=True,
        needs_context=True,
    ),
    
    # ============================================
    # BOUNDARY - 边界
    # ============================================
    ("Boundary", "GENERAL"): CommandMapping(
        engine_method="engine.boundary.create_general",
        params=["no", "nCoor", "bX", "bY", "bZ", "bRX", "bRY", "bRZ", "bRW"],
        description="一般支撑",
        creates_object=True,
        object_type="boundary",
        returns_list=True,
    ),
    ("Boundary", "MSTSLV"): CommandMapping(
        engine_method="engine.boundary.create_master_slave",
        params=["no", "nNode", "bX", "bY", "bZ", "bRX", "bRY", "bRZ"],
        description="主从约束",
        creates_object=True,
        object_type="boundary",
        returns_list=True,
    ),
    ("Boundary", "RELEASE"): CommandMapping(
        engine_method="engine.boundary.create_release",
        params=["no", "Fxi_state", "Fyi_state", "Fzi_state", "Mxi_state", "Myi_state", "Mzi_state", "Mbi_state",
                "Fxi", "Fyi", "Fzi", "Mxi", "Myi", "Mzi", "Mbi",
                "Fxj_state", "Fyj_state", "Fzj_state", "Mxj_state", "Myj_state", "Mzj_state", "Mbj_state",
                "Fxj", "Fyj", "Fzj", "Mxj", "Myj", "Mzj", "Mbj"],
        description="释放梁端约束",
        creates_object=True,
        object_type="boundary",
        returns_list=True,
    ),
    ("Boundary", "ELSTCSPT"): CommandMapping(
        engine_method="engine.boundary.create_elstcspt",
        params=["no", "nCoor", "bX", "DX", "bY", "DY", "bZ", "DZ", "bRX", "RX", "bRY", "RY", "bRZ", "RZ"],
        description="弹性支承",
        creates_object=True,
        object_type="boundary",
        returns_list=True,
    ),
    ("Boundary", "RIGID"): CommandMapping(
        engine_method="engine.boundary.create_rigid",
        params=["no", "nNodeI"],
        description="刚性连接",
        creates_object=True,
        object_type="boundary",
        returns_list=True,
    ),
    ("Boundary", "GES"): CommandMapping(
        engine_method="engine.boundary.create_general_elstcspt",
        params=["no", "nCoor"],
        description="一般弹性支承",
        creates_object=True,
        object_type="boundary",
        returns_list=True,
    ),
    ("Boundary", "SECF"): CommandMapping(
        engine_method="engine.boundary.create_section_factor",
        params=["no", "Area", "Sy", "Sz", "Ixx", "Iyy", "Izz", "Iww", "W"],
        description="截面系数",
        creates_object=True,
        object_type="boundary",
        returns_list=True,
    ),
    ("BoundaryDel", None): CommandMapping(
        engine_method="engine.boundary.delete",
        params=["no"],
        description="删除边界",
    ),
    ("AsgnBd", None): CommandMapping(
        engine_method="engine.boundary.assign",
        params=["nBd", "eOP", "param"],
        description="分配边界",
    ),
    ("BdGrp", None): CommandMapping(
        engine_method="engine.boundary.group",
        params=["strName", "eOP", "param"],
        description="边界组操作",
        is_group_op=True,
        needs_context=True,
    ),
    
    # ============================================
    # SECTION - 截面（混凝土截面）
    # ============================================
    ("Section", "LSHAPE"): CommandMapping(
        engine_method="engine.section.create_Lshape",
        params=["no", "strName", "nDir", "H", "B", "Tf1", "Tf2"],
        description="L形截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "CIRCLE"): CommandMapping(
        engine_method="engine.section.create_circle",
        params=["no", "strName", "eCircleType", "D", "Tw"],
        description="圆形截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "TSHAPE"): CommandMapping(
        engine_method="engine.section.create_Tshape",
        params=["no", "strName", "nDir", "H", "B", "Tf", "Tw"],
        description="T形截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "ISHAPE"): CommandMapping(
        engine_method="engine.section.create_Ishape",
        params=["no", "strName", "H", "Bt", "Bb", "Tt", "Tb", "Tw"],
        description="I形截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "RECT"): CommandMapping(
        engine_method="engine.section.create_rect",
        params=["no", "strName", "H", "B"],
        description="矩形截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "HOLLOWSLAB"): CommandMapping(
        engine_method="engine.section.create_hollowslab",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb", "HoleW", "HoleH", "HoleNum", "HoleType"],
        description="空心板截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "CONVENTIONALBOX"): CommandMapping(
        engine_method="engine.section.create_conventionalbox",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb", "Bf", "Tf", "HoleW", "HoleH"],
        description="常规箱梁截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "FLATBOX"): CommandMapping(
        engine_method="engine.section.create_flat_box",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb"],
        description="扁平箱梁截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "SMALLBOX"): CommandMapping(
        engine_method="engine.section.create_smallbox",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb"],
        description="小箱梁截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "RIBBEDSLAB"): CommandMapping(
        engine_method="engine.section.create_ribbed_slab",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb", "Bf", "Tf"],
        description="肋板截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "TGIRDER"): CommandMapping(
        engine_method="engine.section.create_TGirder",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb"],
        description="T梁截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "DOUBLE_SIDEBOX"): CommandMapping(
        engine_method="engine.section.create_double_side_box",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb"],
        description="双边箱截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "ROUNDEDEND"): CommandMapping(
        engine_method="engine.section.create_rounded_end",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb", "R"],
        description="圆端形截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    # 钢截面
    ("Section", "STEELI"): CommandMapping(
        engine_method="engine.section.create_steel_i",
        params=["no", "strName", "H", "Bt", "Bb", "Tt", "Tb", "Tw"],
        description="钢I形截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "STEELBOX"): CommandMapping(
        engine_method="engine.section.create_steel_box",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb"],
        description="钢箱梁截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "STEELBOX3CELL"): CommandMapping(
        engine_method="engine.section.create_steel_box_three_cell",
        params=["no", "strName", "H", "B", "Tw", "Tt", "Tb", "Bf", "Tf"],
        description="钢箱梁三室截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    ("Section", "CUSTOM"): CommandMapping(
        engine_method="engine.section.create_custom",
        params=["no", "strName"],
        description="自定义截面",
        creates_object=True,
        object_type="section",
        returns_list=True,
    ),
    # 截面操作
    ("SectionDel", None): CommandMapping(
        engine_method="engine.section.delete",
        params=["no"],
        description="删除截面",
    ),
    ("SectionMod", None): CommandMapping(
        engine_method="engine.section.renumber",
        params=["old_no", "new_no"],
        description="修改截面编号",
    ),
    
    # ============================================
    # PROPERTY - 属性
    # ============================================
    # 坐标系
    ("CoorSys", "TRIPT"): CommandMapping(
        engine_method="engine.prop.coord.create_three_point",
        params=["no", "p1x", "p1y", "p1z", "p2x", "p2y", "p2z", "p3x", "p3y", "p3z"],
        description="三点坐标系",
    ),
    ("CoorSys", "DBPT"): CommandMapping(
        engine_method="engine.prop.coord.create_two_point_rotation",
        params=["no", "p1x", "p1y", "p1z", "p2x", "p2y", "p2z", "angle"],
        description="两点旋转坐标系",
    ),
    ("CoorSysDel", None): CommandMapping(
        engine_method="engine.prop.coord.delete",
        params=["no"],
        description="删除坐标系",
    ),
    # 收缩徐变
    ("CrpShrk", None): CommandMapping(
        engine_method="engine.prop.creep_shrink.create",
        params=["no", "name", "avg_humidity", "birth_time", "type_coeff", "shrink_birth"],
        description="收缩徐变特性",
    ),
    ("CrpShrkDel", None): CommandMapping(
        engine_method="engine.prop.creep_shrink.delete",
        params=["no"],
        description="删除收缩徐变特性",
    ),
    # 阻尼
    ("Damping", "MODAL"): CommandMapping(
        engine_method="engine.prop.damping.create_modal",
        params=["name", "ksi"],
        description="振型阻尼",
    ),
    ("Damping", "RYL"): CommandMapping(
        engine_method="engine.prop.damping.create_rayleigh_custom",
        params=["name", "alpha", "beta"],
        description="Rayleigh阻尼",
    ),
    ("DampingDel", None): CommandMapping(
        engine_method="engine.prop.damping.delete",
        params=["name"],
        description="删除阻尼",
    ),
    # P-U曲线
    ("PUCurve", None): CommandMapping(
        engine_method="engine.prop.pu_curve.create",
        params=["no", "name", "type", "n_point", "displacements", "forces"],
        description="P-U曲线",
    ),
    ("PUCurveDel", None): CommandMapping(
        engine_method="engine.prop.pu_curve.delete",
        params=["no"],
        description="删除P-U曲线",
    ),
    # 构件厚度
    ("AsgnCompThk", None): CommandMapping(
        engine_method="engine.prop.assign_component_thickness",
        params=["dThick", "eOP", "param"],
        description="分配构件厚度",
    ),
    
    # ============================================
    # GEOMETRY - 几何
    # ============================================
    ("Spline3D", "ARC2D"): CommandMapping(
        engine_method="engine.geometry.create_arc2d",
        params=["name", "param"],
        description="2D圆弧样条",
        creates_object=True,
        object_type="geometry",
    ),
    ("Spline3D", "ARC3D"): CommandMapping(
        engine_method="engine.geometry.create_arc3d",
        params=["name", "param"],
        description="3D圆弧样条",
        creates_object=True,
        object_type="geometry",
    ),
    ("Spline3D", "SPL3D"): CommandMapping(
        engine_method="engine.geometry.create_general",
        params=["name", "param"],
        description="3D一般样条",
        creates_object=True,
        object_type="geometry",
    ),
    ("Spline3D", "NATURAL"): CommandMapping(
        engine_method="engine.geometry.create_natural",
        params=["name", "param"],
        description="自然样条",
        creates_object=True,
        object_type="geometry",
    ),
    ("Spline3DDel", None): CommandMapping(
        engine_method="engine.geometry.delete",
        params=["name"],
        description="删除样条曲线",
    ),
    
    # ============================================
    # STAGE - 施工阶段
    # ============================================
    ("Stage", None): CommandMapping(
        engine_method="engine.stage.create",
        params=["no", "name", "duration", "pre_stage_no"],
        description="创建施工阶段",
        creates_object=True,
        object_type="stage",
        returns_list=True,
    ),
    ("StageDel", None): CommandMapping(
        engine_method="engine.stage.delete",
        params=["no"],
        description="删除施工阶段",
    ),
    
    # ============================================
    # LOADCASE - 荷载工况
    # ============================================
    ("LoadCase", None): CommandMapping(
        engine_method="engine.load.create",
        params=["strName", "eLoadCaseType", "dScalar", "strPrompt"],
        description="创建荷载工况",
        creates_object=True,
        object_type="loadcase",
        returns_list=True,
    ),
    ("LoadCaseDel", None): CommandMapping(
        engine_method="engine.load.delete",
        params=["strName"],
        description="删除荷载工况",
    ),
    ("LCMod", None): CommandMapping(
        engine_method="engine.load.rename",
        params=["strOldName", "strNewName"],
        description="修改荷载工况名称",
    ),
    
    # ============================================
    # GENERAL - 通用操作
    # ============================================
    ("Clear", None): CommandMapping(
        engine_method="engine.clear",
        params=[],
        description="清空项目",
    ),
    ("Solve", None): CommandMapping(
        engine_method="engine.solve",
        params=[],
        description="求解",
    ),
    ("Replot", None): CommandMapping(
        engine_method="engine.replot",
        params=[],
        description="重绘",
    ),
    ("Clc", None): CommandMapping(
        engine_method="engine.clc",
        params=[],
        description="清屏",
    ),
    
    # ============================================
    # PROJECT - 项目操作
    # ============================================
    ("/Create", None): CommandMapping(
        engine_method="engine.new_project",
        params=["type", "filepath"],
        description="新建项目",
    ),
    ("/Open", None): CommandMapping(
        engine_method="engine.open_project",
        params=["filepath"],
        description="打开项目",
    ),
    ("/Save", None): CommandMapping(
        engine_method="engine.save_project",
        params=[],
        description="保存项目",
    ),
    ("/SaveAs", None): CommandMapping(
        engine_method="engine.project.save_as",
        params=["filepath"],
        description="另存为",
    ),
}


# 多态命令路由配置：命令名 → 子类型字段索引
DISPATCHER_CONFIG: Dict[str, int] = {
    "Material": 3,      # Material,no,name,TYPE,code,grade,...
    "Element": 2,       # Element,no,TYPE,...
    "Boundary": 2,      # Boundary,no,TYPE,...
    "Section": 2,       # Section,no,TYPE,...
    "Spline3D": 1,      # Spline3D,TYPE,...
    "CoorSys": 1,       # CoorSys,TYPE,...
}


def lookup_command(cmd_name: str, parts: List[str]) -> Optional[CommandMapping]:
    """查询命令映射
    
    对于多态命令，根据 dispatcher 配置自动识别子类型。
    
    Args:
        cmd_name: 命令名，如 "Boundary", "Node"
        parts: 命令分割后的参数列表
        
    Returns:
        CommandMapping 对象，如果未找到则返回 None
    """
    # 先尝试单态命令
    key = (cmd_name, None)
    if key in CMD_MAP:
        return CMD_MAP[key]
    
    # 尝试多态命令
    if cmd_name in DISPATCHER_CONFIG:
        field_idx = DISPATCHER_CONFIG[cmd_name]
        if field_idx < len(parts):
            sub_type = parts[field_idx].upper()
            key = (cmd_name, sub_type)
            if key in CMD_MAP:
                return CMD_MAP[key]
    
    return None


def list_all_commands() -> List[Tuple[str, Optional[str], str]]:
    """列出所有已映射的命令
    
    Returns:
        [(命令名, 子类型, 描述), ...]
    """
    result = []
    for (cmd_name, sub_type), mapping in CMD_MAP.items():
        type_str = f"/{sub_type}" if sub_type else ""
        result.append((cmd_name, sub_type, f"{cmd_name}{type_str}: {mapping.description}"))
    return result
