from typing import Any

from pyosis.core.engine import OSISEngine

def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"荷载工况属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:
    """创建荷载工况和钢束，返回荷载工况名称列表
    
    荷载工况名称：
    - "防撞护栏工况": 防撞护栏（CS）
    - "封端混凝土工况": 封端混凝土（CS）
    - "负温度梯度": 负温度梯度（TG）
    - "铺装工况": 铺装（CS）
    - "预应力": 预应力（CS）
    - "整体降温": 整体降温（T）
    - "整体升温": 整体升温（T）
    - "正温度梯度": 正温度梯度（TG）
    - "主梁单元自重": 主梁单元自重（CS）
    """
    tendon = engine.tendon
    loadcase = engine.load
    dynamic = engine.dynamic
    
    # ── 钢束特性──
    tp1 = tendon.prop.create_in(
        "15-10", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=10, pipe=9.0000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp1,"name","15-10")

    tp2 = tendon.prop.create_in(
        "15-3", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=3, pipe=5.5000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp2,"name","15-3")

    tp4 = tendon.prop.create_in(
        "15-4", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=4, pipe=5.5000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp4,"name","15-4")

    tp5 = tendon.prop.create_in(
        "15-5", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=5, pipe=5.5000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp5,"name","15-5")

    tp6 = tendon.prop.create_in(
        "15-6", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=6, pipe=7.0000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp6,"name","15-6")

    tp7 = tendon.prop.create_in(
        "15-7", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=7, pipe=7.0000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp7,"name","15-7")

    tp8 = tendon.prop.create_in(
        "15-8", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=8, pipe=7.0000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp8,"name","15-8")

    tp9 = tendon.prop.create_in(
        "15-9", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=9, pipe=9.0000E-02,
        friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03,
        starting_deform=6.0000E-03, end_deform=6.0000E-03,
        tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01,
    )
    _expect_attr(tp9,"name","15-9")

    tp10 = tendon.prop.create_in_custom(
        "15-10", mat=mat_nos[2], val=1.395000E+09, pipe=1.7000E-01,
    )
    _expect_attr(tp10,"name","15-10")

    tp11 = tendon.prop.create_ex(
        "15-11", mat=mat_nos[2], code="GBT5224_2014",
        diameter=15.2, num=1, pipe=1.7000E-01,
    )
    _expect_attr(tp11,"name","15-11")

    tp12 = tendon.prop.create_ex_custom(
        "15-12", mat=mat_nos[2], val=1.395000E+09, pipe=1.7000E-01,
    )
    _expect_attr(tp12,"name","15-12")

    tp13 = tendon.prop.create_pre(
        "15-13", mat=mat_nos[2], code="GBT5224_2014", diameter=15.2, num=10,
    )
    _expect_attr(tp13,"name","15-13")

    tp14 = tendon.prop.create_pre_custom(
        "15-14", mat=mat_nos[2], val=1.395000E+09, delta_t=1.7000E-01,
    )
    _expect_attr(tp14,"name","15-14")

    tendon.prop.rename("15-10","15-100")
    _expect_attr(tendon.prop.get("15-100"),"name","15-100")

    # 钢束特性数量
    tendon.prop.count()
    # 获取钢束特性
    tendon.prop.get("15-100")
    # 删除钢束特性
    tendon.prop.delete("15-100")
    # 全部钢束特性
    tps = tendon.prop.all()
    if len(tps) == 0:
        raise Exception("获取所有钢束特性失败")

    tendon_spline1,tendon_spline2,natural_tendon_name,tendon_vert_name,tendon_plan_name = geo_names
    _, tendon_eg_1, tendon_eg_2, _ = elem_group_names

    shape3 = tendon.shape.create_spl3d("N3", 2, "15-4", tendon_eg_1, natural_tendon_name)
    _expect_attr(shape3,"name","N3")

    shape5 = tendon.shape.create_arc2d("N5",1,"15-4",tendon_eg_1,1,[tendon_vert_name, tendon_plan_name],)
    _expect_attr(shape5,"name","N5")

    tendon.shape.all()
    tendon.shape.count()
    tendon.shape.get(shape5.name)

    tendon.shape.rename(shape5.name, "N555")
    _expect_attr(tendon.shape.get("N555"),"name","N555")
    tendon.shape.delete(shape5.name)

    # 钢束形状（名称标识）
    shape1 = tendon.shape.create_arc3d("N1", 2, "15-4", tendon_eg_1, tendon_spline1)
    _expect_attr(shape1,"name","N1")
    shape2 = tendon.shape.create_arc3d("N2", 2, "15-4", tendon_eg_2, tendon_spline2)
    _expect_attr(shape2,"name","N2")

    # 布置钢束
    shape1.layout("ELEMENT", 1, 0, 0, 0.0, 0.0, 0.0)
    shape2.layout("ELEMENT", 1, 0, 0, 0.0, 0.0, 0.0)
    shape3.layout("ELEMENT", 1, 0, 0, 0.0, 0.0, 0.0)
    # 清除钢束形状
    shape3.wipe()
    # ── 荷载工况──
    # 1: 防撞护栏工况（CS）
    lc_barrier = loadcase.create("防撞护栏工况", "CS")
    for e in elem_nos:
        lc_barrier.create_line_load(
            e, 0, 0, 
            0.0, 0.0, 0.0, 0.0, 0.0, -2.1200E+03, 0.0, 0.0, 0.0,
            1.0, 0.0, 0.0, 0.0, 0.0, -2.1200E+03, 0.0, 0.0, 0.0,
        )
    user_lc = loadcase.create("荷载工况-用户定义的荷载","USER")
    _expect_attr(user_lc,"name","荷载工况-用户定义的荷载")

    lc_cs = loadcase.create("测试工况-CS-施工阶段荷载", "CS")
    _expect_attr(lc_cs, "name", "测试工况-CS-施工阶段荷载")

    lc_d = loadcase.create("测试工况-D-结构重力", "D")
    _expect_attr(lc_d, "name", "测试工况-D-结构重力")

    lc_ps = loadcase.create("测试工况-PS-预加力", "PS")
    _expect_attr(lc_ps, "name", "测试工况-PS-预加力")

    lc_ev = loadcase.create("测试工况-EV-土的重力", "EV")
    _expect_attr(lc_ev, "name", "测试工况-EV-土的重力")

    lc_eh = loadcase.create("测试工况-EH-土侧压力", "EH")
    _expect_attr(lc_eh, "name", "测试工况-EH-土侧压力")

    lc_sh = loadcase.create("测试工况-SH-收缩", "SH")
    _expect_attr(lc_sh, "name", "测试工况-SH-收缩")

    lc_cr = loadcase.create("测试工况-CR-徐变", "CR")
    _expect_attr(lc_cr, "name", "测试工况-CR-徐变")

    lc_b = loadcase.create("测试工况-B-水浮力", "B")
    _expect_attr(lc_b, "name", "测试工况-B-水浮力")

    lc_stl = loadcase.create("测试工况-STL-基础变位", "STL")
    _expect_attr(lc_stl, "name", "测试工况-STL-基础变位")

    lc_l = loadcase.create("测试工况-L-汽车荷载", "L")
    _expect_attr(lc_l, "name", "测试工况-L-汽车荷载")

    lc_if = loadcase.create("测试工况-IF-汽车冲击力", "IF")
    _expect_attr(lc_if, "name", "测试工况-IF-汽车冲击力")

    lc_cf = loadcase.create("测试工况-CF-汽车离心力", "CF")
    _expect_attr(lc_cf, "name", "测试工况-CF-汽车离心力")

    lc_ls = loadcase.create("测试工况-LS-汽车引起的土侧压力", "LS")
    _expect_attr(lc_ls, "name", "测试工况-LS-汽车引起的土侧压力")

    lc_brk = loadcase.create("测试工况-BRK-汽车制动力", "BRK")
    _expect_attr(lc_brk, "name", "测试工况-BRK-汽车制动力")

    lc_crl = loadcase.create("测试工况-CRL-人群荷载", "CRL")
    _expect_attr(lc_crl, "name", "测试工况-CRL-人群荷载")

    lc_fl = loadcase.create("测试工况-FL-疲劳荷载", "FL")
    _expect_attr(lc_fl, "name", "测试工况-FL-疲劳荷载")

    lc_w1 = loadcase.create("测试工况-W1-活载风", "W1")
    _expect_attr(lc_w1, "name", "测试工况-W1-活载风")

    lc_w2 = loadcase.create("测试工况-W2-极限风", "W2")
    _expect_attr(lc_w2, "name", "测试工况-W2-极限风")

    lc_sf = loadcase.create("测试工况-SF-流水压力", "SF")
    _expect_attr(lc_sf, "name", "测试工况-SF-流水压力")

    lc_ip = loadcase.create("测试工况-IP-冰压力", "IP")
    _expect_attr(lc_ip, "name", "测试工况-IP-冰压力")

    lc_wf1 = loadcase.create("测试工况-WF1-W1引起的波浪力", "WF1")
    _expect_attr(lc_wf1, "name", "测试工况-WF1-W1引起的波浪力")

    lc_wf2 = loadcase.create("测试工况-WF2-W2引起的波浪力", "WF2")
    _expect_attr(lc_wf2, "name", "测试工况-WF2-W2引起的波浪力")

    lc_t = loadcase.create("测试工况-T-均匀温度", "T")
    _expect_attr(lc_t, "name", "测试工况-T-均匀温度")

    lc_tg = loadcase.create("测试工况-TG-梯度温度", "TG")
    _expect_attr(lc_tg, "name", "测试工况-TG-梯度温度")

    lc_fr = loadcase.create("测试工况-FR-支座摩阻力", "FR")
    _expect_attr(lc_fr, "name", "测试工况-FR-支座摩阻力")

    lc_cfs = loadcase.create("测试工况-CFS-船舶撞击", "CFS")
    _expect_attr(lc_cfs, "name", "测试工况-CFS-船舶撞击")

    lc_cfd = loadcase.create("测试工况-CFD-漂流物撞击", "CFD")
    _expect_attr(lc_cfd, "name", "测试工况-CFD-漂流物撞击")

    lc_cfv = loadcase.create("测试工况-CFV-汽车撞击", "CFV")
    _expect_attr(lc_cfv, "name", "测试工况-CFV-汽车撞击")

    lc_e = loadcase.create("测试工况-E-地震作用", "E")
    _expect_attr(lc_e, "name", "测试工况-E-地震作用")

    user_lc.create_gravity(0.0, 0.0, -1.000)
    user_lc.create_nforce(1, 0.0, 0.0, -1000000.0, 0.0, 0.0, 0.0)
    user_lc.create_line_load(1, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -1000000.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1000000.0, 0.0, 0.0, 0.0)
    user_lc.create_concentrated_force(1, 0, False, [[0.0, 0.0, 0.0, 1000000.0, 0.0, 0.0]])
    user_lc.create_displacement(1, 1, 0.001, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0)
    user_lc.create_uniform_temperature(1, "X", -20.000)
    user_lc.create_gradient_temperature(elem_nos[0],"Z","T",2,[1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    user_lc.create_initial_force(1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    user_lc.create_prestress(shape1.name, "BOTH", "ST", 1.395000E+09, 1.395000E+09)
    lc_barrier.create_cable_force(15, "IN",1.0e6)
    # 修改荷载工况
    user_lc.modify(eType="NFORCE", old_entity=1, new_entity=2)

    # 面荷载 — 依赖 _6 中已创建的壳单元
    shells = [e for e in engine.element.all() if e.element_type.name == "SHELL"]
    if not shells:
        raise ValueError("create_surface_load 测试需要壳单元，请确认 _6 已 create_shell")
    shell_no = shells[0].no

    user_lc.create_surface_load(
        strEntity=str(shell_no),
        strPlanei="1",
        strDir="X",
        strGlobalI="0",
        strP1i="0", strP2i="0", strP3i="0", strP4i="0",
    )
     # 删除荷载（LoadCase.delete）
    user_lc.delete("ESRFC", entity=str(shell_no))
    # user_lc.create_surface_load_vector(
    #     strEntity=str(shell_no),
    #     strPlanei="1",
    #     strXi="0", strYi="0", strZi="-1",
    #     strP1i="0", strP2i="0", strP3i="0", strP4i="0",
    # )
    lc1 = loadcase.create("荷载工况-桥规中的荷编号1-结构重力", "D")
    _expect_attr(lc1,"name","荷载工况-桥规中的荷编号1-结构重力")

    lc2 = loadcase.create("荷载工况-结构和非结构附属荷载", "DC")
    _expect_attr(lc2,"name","荷载工况-结构和非结构附属荷载")

    lc3 = loadcase.create("荷载工况-铺装和设备荷载", "DW")
    _expect_attr(lc3,"name","荷载工况-铺装和设备荷载")

    lc4 = loadcase.create("荷载工况-桩端摩擦力", "DD")
    _expect_attr(lc4,"name","荷载工况-桩端摩擦力")

    # 2: 封端混凝土工况（CS）
    lc5 = loadcase.create("封端混凝土工况", "CS")
    lc5.create_line_load(
        elem_nos[0], 0, 0, 
        0.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
    )
    lc5.create_line_load(
        elem_nos[13], 0, 0, 
        0.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
    )
    
    # 3: 负温度梯度（TG）
    lc_neg_temp = loadcase.create("负温度梯度", "TG")
    lc_neg_temp.create_gradient_temperature(elem_nos[0],  "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[1],  "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[2],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[3],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[4],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[5],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[6],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[7],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[8],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[9],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[10], "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[11], "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.603, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[12], "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[13], "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    
    # 4: 铺装工况（CS）
    lc_pavement = loadcase.create("铺装工况", "CS")
    for e in elem_nos:
        lc_pavement.create_line_load(
            e, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0850E+04, 0.0, 0.0, 0.0,
            1.0, 0.0, 0.0, 0.0, 0.0, -1.0850E+04, 0.0, 0.0, 0.0,
        )
    
    # 5: 预应力（CS）
    lc_pst = loadcase.create("预应力", "CS")
    lc_pst.create_prestress(shape1.name, "BOTH", "ST", 1.395000E+09, 1.395000E+09)
    lc_pst.create_prestress(shape2.name, "BOTH", "ST", 1.395000E+09, 1.395000E+09)
    
    # 6: 整体降温（T）
    lc_temp_drop = loadcase.create("整体降温", "T")
    for e in elem_nos:
        lc_temp_drop.create_uniform_temperature(e, "X", -20.000)
    
    # 7: 整体升温（T）
    lc_temp_rise = loadcase.create("整体升温", "T")
    for e in elem_nos:
        lc_temp_rise.create_uniform_temperature(e, "X", 20.000)
    
    # 8: 正温度梯度（TG）
    lc_pos_temp = loadcase.create("正温度梯度", "TG")
    lc_pos_temp.create_gradient_temperature(elem_nos[0],  "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[1],  "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[2],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[3],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[4],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[5],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[6],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[7],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[8],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[9],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[10], "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[11], "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.603, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[12], "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[13], "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    
    # 9: 主梁单元自重（CS）
    lc_dead = loadcase.create("主梁单元自重", "CS")
    lc_dead.create_gravity(0.0, 0.0, -1.000)

    # 荷载质量转换
    ltm1 = dynamic.load_to_mass.create("荷载转换质量1")
    dynamic.load_to_mass.create("荷载转换质量2")
    ltm1.add(lc1.name, 1.0, 9.806)
    ltm = dynamic.load_to_mass.get("荷载转换质量1")
    _expect_attr(ltm, "name", "荷载转换质量1")
    if ltm.get(lc1.name) is None:
        raise ValueError(f"add 后应包含 {lc1.name!r}")
    # remove 测试
    ltm.remove(lc1.name)
    ltm = dynamic.load_to_mass.get("荷载转换质量1")
    if ltm is None:
        raise ValueError("remove 后 get 失败")
    if ltm.get(lc1.name) is not None:
        raise ValueError(f"remove 后不应再包含 {lc1.name!r}")
    # 后续 delete / rename
    dynamic.load_to_mass.rename(ltm.name, "_荷载转换质量1")
    dynamic.load_to_mass.delete("_荷载转换质量1")
    ltms = dynamic.load_to_mass.all()
    if len(ltms) != 1:
        raise ValueError(f"期望剩余 1 个荷载转换质量，实际 {len(ltms)}")
    # 模态分析
    dynamic.modal.set_modal_opt(5)
    
    # 地震反应谱
    rsp = dynamic.seismic
    rsp_import_name = "_反应谱导入测试"
    rsp.create(rsp_import_name, "A", 9.8, [(0.1, 0.5), (0.2, 0.8), (0.5, 1.2), (1.0, 0.9)])

    got_import = rsp.get(rsp_import_name)
    if got_import is None or got_import.name != rsp_import_name:
        raise ValueError(f"获取 {rsp_import_name!r} 失败")
    rsp.delete(rsp_import_name)
    rsp_name = "_反应谱测试"
    rsp.create_code(rsp_name,
      "A",
      9.8,
      code="JTGT2231_01_2020",
      bridge_type="A",
      is_long_span=0,
      level=0,
      intensity=0.05,
      site=0,
      direction=0,
      period=0.35,
      ksi=0.05,
      t=6.0,
      delta_t=0.1,)
    got = rsp.get(rsp_name)
    if got is None or got.name != rsp_name:
        raise ValueError(f"获取 {rsp_name!r} 失败")
    rsp.rename(got.name, "_" + got.name)
    got2 = rsp.get("_" + got.name)
    if got2 is None or got2.name != "_" + got.name:
        raise ValueError("rename 后名称不符")
    rsp.all()
    rsp.delete(rsp_name)

    all_lc = loadcase.all()
    if loadcase.count() != len(all_lc):
        raise ValueError("loadcase.count() 与 all() 不一致")
    got_lc = loadcase.get(lc_dead.name)
    if got_lc is None or got_lc.name != lc_dead.name:
        raise ValueError("loadcase.get 失败")

    return [
        lc_barrier.name,
        lc5.name,
        lc_neg_temp.name,
        lc_pavement.name,
        lc_pst.name,
        lc_temp_drop.name,
        lc_temp_rise.name,
        lc_pos_temp.name,
        lc_dead.name,
    ]

if __name__ == "__main__":
    from _0_engine import engine

    engine.tendon.shape.clear()
    engine.load.clear()
    engine.dynamic.clear()

    # 从 engine 获取已有数据
    mats = engine.material.all()
    print("materials: ", mats)
    mat_nos = [m.no for m in mats]
    elems = engine.element.all()
    print("elements: ", elems)
    elem_nos = [e.no for e in elems]
    elem_groups = engine.element.group.all()
    print("element groups: ", elem_groups)
    elem_group_names = [eg.name for eg in elem_groups]

    from _2_property import build_property

    geo_names = build_property(engine)
    print("geo_names:", geo_names)
    
    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)
    print(lc_names)
    print(engine.load.all())
