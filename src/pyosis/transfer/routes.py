"""命令流 → pyosis 路由表

转换规则（全局唯一，不再为单个命令写例外）:
    Cmd, f0, f1, f2, ... 的字段顺序必须与目标函数的位置参数顺序一致。

    key   = OSIS 命令名
    value = 目标，三种形态:
        "direct": str (engine 方法路径)
            生成: engine.method(f0, f1, ...)
        ("chain", get_path, method_name, key_index)
            第 key_index 个字段用于取对象，其余字段保持原序:
            生成: get(f[key_index]).method(f0, ..., f[key_index-1],
                                         f[key_index+1], ...)
        ("list", target, n_head)
            前 n_head 个字段按位置传，其余字段聚合成一个 list:
            生成: target(f0, ..., f[n_head-1], [f[n_head], f[n_head+1], ...])

字段重排/补位/旧格式升级一律通过修改对应的 Python 函数解决，不要在这里
增加 fixer。
"""

# 5.01 版 .out 使用缩写命令名，生成代码前统一归一化为全名
CMD_ALIASES = {
    "N": "Node",
    "NDel": "NodeDel",
    "NMod": "NodeMod",
    "Ele": "Element",
    "EleDel": "ElementDel",
    "EleMod": "ElementMod",
    "Sec": "Section",
    "SecDel": "SectionDel",
    "SecMod": "SectionMod",
    "SecOff": "SectionOffset",
    "SecMesh": "SectionMesh",
    "SecPt": "StressPoint",
    "Mat": "Material",
    "MatDel": "MaterialDel",
    "MatMod": "MaterialMod",
    "LC": "LoadCase",
    "LCDel": "LoadCaseDel",
    "Bd": "Boundary",
    "BdDel": "BoundaryDel",
    "Stg": "Stage",
    "StgDel": "StageDel",
    "StgIst": "StageIst",
    "StgRmv": "StageRmv",
}

ROUTES = {
    # ─── CONTROL ───
    "Acel": "engine.control.set_gravity_acceleration",
    "Unit": "engine.control.set_unit",
    "CalcTendon": "engine.control.set_calc_tendon",
    "CalcRebarGravity": "engine.control.set_calc_rebar_gravity",
    "CalcConForce": "engine.control.set_calc_concurrent_force",
    "CalcShrink": "engine.control.set_calc_shrink",
    "CalcCreep": "engine.control.set_calc_creep",
    "CalcShear": "engine.control.set_calc_shear",
    "CalcRlx": "engine.control.set_calc_relaxation",
    "ModLocCoor": "engine.control.set_mod_loc_coor",
    "IncTendon": "engine.control.set_inc_tendon",
    "IncRebar": "engine.control.set_inc_rebar",
    "ModOpt": "engine.dynamic.modal.set_modal_opt",
    "NL": "engine.control.set_nonlinear",
    "CnvTol": "engine.control.set_convergence_tolerance",
    "CnvConfig": "engine.control.set_convergence_tolerance",
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
    "SecPropMod": "engine.section.set_prop_mod",
    "SectionPropFactor": "engine.section.set_prop_factor",
    "SectionPart": ("chain", "engine.section.get", "add_part", 0),
    "StressPoint": ("chain", "engine.section.get", "set_stress_point", 0),
    "RebarL": ("chain", "engine.section.get", "add_rebar_l", 0),
    "RebarLDel": ("chain", "engine.section.get", "delete_rebar_l", 0),
    "RebarS": ("chain", "engine.section.get", "add_rebar_s", 0),
    "RebarSDel": ("chain", "engine.section.get", "delete_rebar_s", 0),
    "Rib": ("chain", "engine.section.get", "add_rib", 0),
    "RibMod": ("chain", "engine.section.get", "modify_rib", 0),
    "RibDel": ("chain", "engine.section.get", "delete_rib", 0),
    "ClearSectionRib": ("chain", "engine.section.get", "clear_ribs", 0),
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
    "EleGrp": "engine.element.group.create",        # 完整增删改查（c/a/s/r/aa/ra/m/d）
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
    "StrengthPrg": "engine.prop.strength_prog.create",
    "StrengthPrgDel": "engine.prop.strength_prog.delete",
    "StrengthPrgMod": "engine.prop.strength_prog.rename",

    # ─── GEOMETRY ───
    # 坐标序列要以 list 传(create 转发给 create_* 的 coordinates 形参),不能展平
    "Spline3D": ("list", "engine.geometry.create", 3),
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
    "Load": ("chain", "engine.load.get", "create", 1),
    # LoadDel/LoadMod: TYPE, LC, ... → engine.load.get(LC).delete/modify(TYPE, ...)
    "LoadDel": ("chain", "engine.load.get", "delete", 1),
    "LoadMod": ("chain", "engine.load.get", "modify", 1),
    "PlanarLoad": "engine.load.planar_load",
    "PlanarLoadCopy": "engine.load.planar_load_copy_flat",
    "PlanarLoadDel": "engine.load.planar_load_del",

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

    # ─── ENVIRONMENTAL ───
    "HydroCoeff": "engine.environmental.coeff.hydro_coeff",
    "HydroCoeffDel": "engine.environmental.coeff.delete",
    "HydroCoeffMod": "engine.environmental.coeff.rename",
    "SeastateOpt": "engine.environmental.analysis.sea_state_opt",
    "SeastAnal": "engine.environmental.analysis.create",
    "SeastAnalDel": "engine.environmental.analysis.delete",
    "SeastAnalMod": "engine.environmental.analysis.rename",
    "SeastAnalInc": "engine.environmental.analysis.inc",

    # ─── LIVE ───
    "LiveGrade": "engine.live.grade.create",
    "LiveGradeDel": "engine.live.grade.delete",
    "LiveGradeMod": "engine.live.grade.rename",
    "InflAlgo": "engine.live.lane.create",
    "InflAlgoDel": "engine.live.lane.delete",
    "InflAlgoMod": "engine.live.lane.rename",
    "LiveAnal": "engine.live.case.create",
    "LiveAnalDel": "engine.live.case.delete",
    "LiveAnalMod": "engine.live.case.rename",
    "LiveAnalFactor": ("chain", "engine.live.case.get", "set_trans_reduction_factors", 0),
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
    "LTMAnalInc": ("chain", "engine.dynamic.load_to_mass.get", "include", 0),
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
    "/Close": "engine.close",

    # ─── DISPLAY ───
    "DispCtrl": "engine.display.disp_ctrl",
    "/control": "engine.display.control",
    "Plsm": "engine.display.set_plsm",

    # ─── POST ───
    "Combine": "engine.post.create_combine",
    "Post": "engine.post.add_combine_entry",
    "CombineSolve": "engine.post.solve_combines",
    "CombineDel": "engine.post.delete_combines",
    "Code": "engine.post.set_code",
    "CdEleSel": "engine.post.select_elements",
    "CdEleAct": "engine.post.activate_elements",
    "CdDL": "engine.post.set_design_level",
    "CdPC": "engine.post.set_member_type",
    "CdPRSRatio": "engine.post.set_prs_ratio",
    "CdCSCRatio": "engine.post.set_csc_ratio",
    "CdE": "engine.post.set_environment",
    "CdCrack": "engine.post.set_crack_params",
    "CdAutoC2": "engine.post.auto_c2",
    "CdCrackWeld": "engine.post.set_weld_skeleton",
    "CdGeoLCo": "engine.post.set_geo_length",
    "CdCheck": "engine.post.set_check_items",
    "Check": "engine.post.add_check",
    "CheckSolve": "engine.post.solve_checks",
    "CheckDel": "engine.post.delete_checks",
    "PrnEig": "engine.post.display_eigenvalue",
    "PlEig": "engine.post.display_eigenvector",

    # ─── GENERAL ───
    "Clear": "engine.clear",
    "Solve": "engine.solve",
    "Replot": "engine.replot",
    "Clc": "engine.clc",
    "APDL": "engine.import_apdl",
    "Matrix": "engine.matrix",
}
