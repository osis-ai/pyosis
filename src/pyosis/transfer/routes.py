"""命令流 → pyosis 路由表

字典格式:
    key   = OSIS 命令名
    value = (kind, ...)
    kind:
        "direct":   str (engine 方法路径)
        "chain":    (engine_get_path, obj_method_name, skip_fields)
                    Cmd,fields[skip_fields=0]=key, fields[skip_fields+1:]=args
                    生成: engine.get(key).method(args...)
"""

ROUTES = {
    # ─── CONTROL ───
    "Acel": "engine.control.set_gravity_acceleration",
    "CalcTendon": "engine.control.set_calc_tendon",
    "CalcConForce": "engine.control.set_calc_concurrent_force",
    "CalcShrink": "engine.control.set_calc_shrink",
    "CalcCreep": "engine.control.set_calc_creep",
    "CalcShear": "engine.control.set_calc_shear",
    "CalcRlx": "engine.control.set_calc_relaxation",
    "ModLocCoor": "engine.control.set_mod_loc_coor",
    "IncTendon": "engine.control.set_inc_tendon",
    "ModOpt": "engine.dynamic.modal.set_modal_opt",
    "NL": "engine.control.set_nonlinear",
    "LnSrch": "engine.control.set_line_search",
    "AutoTs": "engine.control.set_auto_time_step",
    "NSUBST": "engine.control.set_substitution_steps",

    # ─── MATERIAL ───
    "Material": "engine.material.create",
    "MaterialDel": "engine.material.delete",
    "MaterialMod": "engine.material.renumber",

    # ─── SECTION ───
    "Section": "engine.section.create",
    "SectionDel": "engine.section.delete",
    "SectionMod": "engine.section.renumber",
    "SectionOffset": ("chain", "engine.section.get", "set_offset", 0),
    "SectionMesh": ("chain", "engine.section.get", "set_mesh", 0),
    "SectionMat": ("chain", "engine.section.get", "set_material", 0),
    "SectionPart": ("chain", "engine.section.get", "add_part", 0),
    "StressPoint": ("chain", "engine.section.get", "set_stress_point", 0),
    "RebarL": ("chain", "engine.section.get", "add_rebar_l", 0),
    "RebarLDel": ("chain", "engine.section.get", "delete_rebar", 0),
    "RebarS": ("chain", "engine.section.get", "add_rebar_s", 0),
    "RebarSDel": ("chain", "engine.section.get", "delete_rebar_s", 0),
    "Rib": ("chain", "engine.section.get", "add_rib", 0),
    "RibMod": ("chain", "engine.section.get", "modify_rib", 0),
    "RibDel": ("chain", "engine.section.get", "delete_rib", 0),
    "ClearSectionRib": ("chain", "engine.section.get", "delete_rib", 0),
    "RibLayout": ("chain", "engine.section.get", "add_rib_layout", 0),
    "RibLayoutDel": ("chain", "engine.section.get", "delete_rib_layout", 0),
    "SteelPlate": ("chain", "engine.section.get", "add_steel_plate", 0),

    # ─── NODE ───
    "Node": "engine.node.create",
    "NodeDel": "engine.node.delete",
    "NodeMod": "engine.node.renumber",

    # ─── ELEMENT ───
    "Element": "engine.element.create",
    "ElementDel": "engine.element.delete",
    "ElementMod": "engine.element.renumber",
    "EleGrp": "engine.element.group.create",        # 只有创建功能
    "TaperEle": "engine.element.taper_group.create",
    "TaperEleDel": "engine.element.taper_group.delete",
    "TaperEleMod": "engine.element.taper_group.rename",

    # ─── BOUNDARY ───
    "Boundary": "engine.boundary.create",
    "BoundaryDel": "engine.boundary.delete",
    "AsgnBd": ("chain", "engine.boundary.get", "assign", 0),
    "BdGrp": "engine.boundary.group.create",

    # ─── PROPERTY ───
    "CoorSys": "engine.prop.coord.create",
    "CoorSysDel": "engine.prop.coord.delete",
    "CoorSysMod": "engine.prop.coord.renumber",
    "AsgnCompThk": "engine.prop.assign_component_thickness",
    "CrpShrk": "engine.prop.creep_shrink.create",
    "CrpShrkDel": "engine.prop.creep_shrink.delete",
    "CrpShrkMod": "engine.prop.creep_shrink.renumber",
    "Damping": "engine.prop.damping.create",
    "DampingDel": "engine.prop.damping.delete",
    "DampingMod": "engine.prop.damping.rename",
    "PUCurve": "engine.prop.pu_curve.create",
    "PUCurveDel": "engine.prop.pu_curve.delete",
    "PUCurveMod": "engine.prop.pu_curve.renumber",

    # ─── GEOMETRY ───
    "Spline3D": "engine.geometry.create",
    "Spline3DDel": "engine.geometry.delete",

    # ─── THICKNESS ───
    "ShellThk": "engine.thickness.create",
    "ShellThkDel": "engine.thickness.delete",
    "ShellThkMod": "engine.thickness.renumber",

    # ─── LOADCASE ───
    "LoadCase": "engine.load.create",
    "LoadCaseDel": "engine.load.delete",
    "LCMod": "engine.load.rename",
    # Load 子命令:  Load,type,lcName,... →  engine.load.get(lcName).create(type, ...)
    "Load": ("chain", "engine.load.get", "create", 1, 1),  # skip=1(lcName), rest_prefix=1(type)
    "LoadDel": ("chain", "engine.load.get", "delete", 0),
    "LoadMod": ("chain", "engine.load.get", "modify", 0),

    # ─── TENDON ───
    "TdProp": "engine.tendon.prop.create",
    "TdPropDel": "engine.tendon.prop.delete",
    "TdPropMod": "engine.tendon.prop.rename",
    "TdShape": "engine.tendon.shape.create",
    "TdShapeDel": "engine.tendon.shape.delete",
    "TdShapeMod": "engine.tendon.shape.rename",
    "LayoutTS": ("chain", "engine.tendon.shape.get", "layout", 0),
    "BottomTS": ("chain", "engine.tendon.shape.get", "bottom", 0),
    "WipeTS": ("chain", "engine.tendon.shape.get", "wipe", 0),

    # ─── LIVE ───
    "LiveGrade": "engine.live.grade.create",
    "LiveGradeDel": "engine.live.grade.delete",
    "LiveGradeMod": "engine.live.grade.rename",
    "InflAlgo": "engine.live.lane.create",
    "InflAlgoDel": "engine.live.lane.delete",
    "InflAlgoMod": "engine.live.lane.rename",
    "LiveAnal": "engine.live.case.create",
    "LiveAnalDel": "engine.live.analysis.delete",
    "LiveAnalMod": "engine.live.analysis.rename",
    "LiveAnalFactor": ("chain", "engine.live.analysis.get", "set_trans_reduction_factors", 0),
    "LiveAnalInc": ("chain", "engine.live.case.get", "include", 0),
    "LiveAnalOpt": ("chain", "engine.live.case.get", "set_lane_count", 0),

    # ─── SETTLEMENT ───
    "SetlGrp": "engine.settlement.group.create",
    "SetlGrpDel": "engine.settlement.group.delete",
    "SetlGrpMod": "engine.settlement.group.rename",
    "SetlAnal": "engine.settlement.create",
    "SetlAnalDel": "engine.settlement.delete",
    "SetlAnalMod": "engine.settlement.rename",
    "SetlAnalInc": ("chain", "engine.settlement.get", "include", 0),

    # ─── STABILITY ───
    "BucklAnal": "engine.stability.create",
    "BucklAnalDel": "engine.stability.delete",
    "BucklAnalMod": "engine.stability.rename",
    "BucklAnalInc": ("chain", "engine.stability.get", "include", 0),

    # ─── DYNAMIC ───
    "LTMAnal": "engine.dynamic.load_to_mass.create",
    "LTMAnalDel": "engine.dynamic.load_to_mass.delete",
    "LTMAnalMod": "engine.dynamic.load_to_mass.rename",
    "LTMAnalInc": ("chain", "engine.dynamic.load_to_mass.get", "add", 0),
    "SeisRspSpec": "engine.dynamic.seismic.create",
    "SeisRspSpecDel": "engine.dynamic.seismic.delete",
    "SeisRspSpecMod": "engine.dynamic.seismic.rename",
    "RSpecAnal": "engine.dynamic.response_spectrum.create",
    "RSpecAnalDel": "engine.dynamic.response_spectrum.delete",
    "RSpecAnalMod": "engine.dynamic.response_spectrum.rename",

    # ─── STAGE ───
    "Stage": "engine.stage.create",
    "StageDel": "engine.stage.delete",
    "StageIst": "engine.stage.insert",
    "StageRmv": "engine.stage.remove",
    "StgEle": ("chain", "engine.stage.get", "define_element", 0),
    "StgBd": ("chain", "engine.stage.get", "define_boundary", 0),
    "StgLc": ("chain", "engine.stage.get", "define_loadcase", 0),
    "StgAnal": ("chain", "engine.stage.get", "define_analysis", 0),

    # ─── PROJECT ───
    "/Create": "engine.new_project",
    "/Open": "engine.open_project",
    "/Save": "engine.save_project",
    "/SaveAs": "engine.project.save_as",

    # ─── GENERAL ───
    "Clear": "engine.clear",
    "Solve": "engine.solve",
    "Replot": "engine.replot",
    "Clc": "engine.clc",
    "APDL": "engine.import_apdl",
    "Matrix": "engine.matrix",
}