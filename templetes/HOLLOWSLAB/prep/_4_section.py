from typing import Any

from pyosis.core.engine import OSISEngine
from pyosis.general import osis_matrix
from pyosis.material.manager import Material


def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"截面属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

def build_sections(engine: OSISEngine, mat_nos: list[int]) -> list[int]:
    """创建截面，返回截面编号列表 [1, 2, 3, 4, 5]

    截面编号（显式定义，幂等执行）：
    - 1: 标准截面（MIDDLE）
    - 2: 墩顶截面（MIDDLE）
    - 3: 加厚截面（MIDDLE）
    - 4: 墩顶截面（MIDDLE）
    - 5: 加厚截面（MIDDLE）
    """
    section = engine.section
    # 创建L形截面
    l_section = section.create_Lshape("L形截面",1,1.0,2.0,0.016,0.035)
    _expect_attr(l_section, "name", "L形截面")

    # 创建圆形截面1
    circle_sec1 = section.create_circle("圆形截面1","Hollow",0.5,0.2)
    _expect_attr(circle_sec1, "name", "圆形截面1")

    # 创建圆形截面2
    circle_sec2 = section.create_circle("圆形截面2","Solid",1.5,1.2)
    _expect_attr(circle_sec2, "name", "圆形截面2")

    # 创建T形截面1
    t_sec1 = section.create_Tshape("T形截面1",0,0.3,0.2,0.016,0.025)
    _expect_attr(t_sec1, "name", "T形截面1")

    # 创建T形截面2
    t_sec2 = section.create_Tshape("T形截面2", 1, 0.3, 0.2, 0.016, 0.025)
    _expect_attr(t_sec2, "name", "T形截面2")

    # 创建I形截面
    i_sec1 = section.create_Ishape("I形截面",0.3,0.13,0.24,0.016,0.018,0.019)
    _expect_attr(i_sec1, "name", "I形截面")

    # 创建矩形截面1
    rect_sec1 = section.create_rect("矩形截面1","Chamfer","Solid",6.5,3.2,1.5,0.5,0.5,1.0,1.0,0.5,0.25,False, 1.0,0.5,0.25,False,1.2,0.8, 0.2)
    _expect_attr(rect_sec1, "name", "矩形截面1")

    # 创建矩形截面2
    rect_sec2 = section.create_rect("矩形截面2", "Fillet", "Hollow", 6.6, 3.3, 1.6, 0.6, 0.6, 1.2, 1.2, 0.6, 0.26,
                                    False, 1.1, 0.6, 0.26, False, 1.3, 0.9, 0.3)
    _expect_attr(rect_sec2, "name", "矩形截面2")

    # 创建工字形钢截面1
    si_sec1 = section.create_steel_i("工字形钢截面1", 3, 10, 10, 1, 1, 1, "Left")
    _expect_attr(si_sec1,"name","工字形钢截面1")

    # 创建工字形钢截面2
    si_sec2 = section.create_steel_i("工字形钢截面2", 4, 12, 12, 1, 1, 1, "Right")
    _expect_attr(si_sec2,"name","工字形钢截面2")

    # 创建工字形钢截面3
    si_sec3 = section.create_steel_i("工字形钢截面3", 5, 15, 15, 1, 1, 1, "Both")
    _expect_attr(si_sec3,"name","工字形钢截面3")
    # 加劲肋
    si_sec3.add_rib_t("T形加劲肋", 0.1, 0.01, 0.01, 0.01)
    si_sec3.add_rib_u("U形加劲肋", 0.15, 0.08, 0.08, 0.012, 0.004)
    si_sec3.add_rib_l("L形加劲肋", "LL", 0.15, 0.08, 0.012, 0.004)
    si_sec3.modify_rib("T形加劲肋", "T1形加劲肋")
    si_sec3.delete_rib("U形加劲肋")

    # 创建箱型钢截面1
    sb_sec1 = section.create_steel_box("箱型钢截面1", 1.0,2.0,0.5,2.0,0.5,0.2,0.2,2.0,1)
    _expect_attr(sb_sec1,"name","箱型钢截面1")
    # 加劲肋布置信息
    sb_sec1.add_rib_flat("扁平加劲肋", 0.15, 0.012)
    sb_sec1.add_rib_layout("STEEL", "BottomFlange", 1, "扁平加劲肋", 0.1, 0.3, 3)

    sb_sec1.delete_rib_layout("STEEL", "BottomFlange", 1)
    sb_sec1.clear_ribs()
    # set_material：仅用于组合截面
    conc_no = mat_nos[0]
    steel_no = mat_nos[3]
    comp_sec = section.create_composite_steel_i(
        name="工字型钢组合截面",
        bt=2.0, bc=0.5,
        tt1=0.2, tt2=0.22, tt3=0.25,
        tc1=0.18, tc2=0.16,
        b1=0.3, b2=0.4,
        x1=0.05, x2=0.05, x3=0.05,
        girder_num="SINGLE",
        h1=1.5, bf1=0.6, bb1=0.6, tf1=0.02, tb1=0.02, tw1=0.012,
        web_rib_pos1="BOTH",
        middle_same_with_side=1,
    )
    comp_sec.set_material(steel_no, conc_no)
    trough_sec = section.create_composite_steel_trough(
        name="槽型钢组合截面",
        bt=2.0, bc=0.5,
        tt1=0.2, tt2=0.22, tt3=0.25,
        tc1=0.18, tc2=0.16,
        b1=0.3, b2=0.4,
        x1=0.05, x2=0.05, x3=0.05,
        h1=1.2, bb=0.5, bf1=0.4, tf1=0.02, tb=0.02, tw1=0.012,
        right_same_with_left=1,
        has_steel_i=0,
    )
    trough_sec.set_material(steel_no, conc_no)
    
    box_comp = section.create_composite_steel_box(
        name="箱型钢组合截面",
        bt=2.0, bc=0.5,
        tt1=0.2, tt2=0.22, tt3=0.25,
        tc1=0.18, tc2=0.16,
        b1=0.3, b2=0.4,
        x1=0.05, x2=0.05, x3=0.05,
        girder_num="SINGLE",
        h1=1.5, bf1=0.8, bct=0.1, bb=0.8, bcb=0.1,
        tf1=0.02, tb=0.02, tw1=0.012,
        same_layout=1,
    )
    box_comp.set_material(steel_no, conc_no)
    # Part 1：混凝土面域（可布置钢筋）
    osis_matrix("CompContour1", [
      [1, 0.0, 0.0],
      [1, 1.0, 0.0],
      [1, 1.0, 0.2],
      [1, 0.0, 0.2],
    ])
    osis_matrix("CompContourWidth1", [[0.25], [0.25], [0.25], [0.25]])
    # 自定义组合截面(待实现)
    # comp_custom = section.create_composite_custom(
    #   name="自定义组合截面",
    #   part_num=2,
    #   base_e=3.55e10,
    #   base_mu=0.2,
    # )
    # comp_custom.add_composite_part_polygon(
    #   1, "Concrete",
    #   3.55e10, 0.2, 25.0,
    #   "CompContour1", "CompContourWidth1",
    # )
    # # Part 2：钢线域（不可布置钢筋）
    # osis_matrix("CompPoint2", [
    #   [1, 0.0, 0.0],
    #   [2, 1.0, 0.0],
    # ])
    # osis_matrix("CompLine2", [
    #   [1, 1],
    #   [1, 2],
    # ])
    # osis_matrix("CompWidth2", [[0.02]])
    # comp_custom.add_composite_part_line(
    #   2, "Steel",
    #   2.06e11, 0.3, 78.5,
    #   "CompPoint2", "CompLine2", "CompWidth2",
    # )
    # comp_custom.set_material(steel_no, conc_no)
    # 创建箱型钢截面2
    sb_sec2 = section.create_steel_box("箱型钢截面2", 2.0,2.0,0.5,2.0,0.5,0.2,0.2,2.0, 1)
    _expect_attr(sb_sec2,"name","箱型钢截面2")
    # 加劲肋布置信息

    # 创建三室钢截面1
    tc_sec1 = section.create_steel_box_three_cell("三室钢截面1",2.5,12.0,12.0,0.02,1.0,1.0,0.5,0.016,0.016,0.014,0.4,0.012,0.012,0.012,2.0,1,2.0,"Left")
    _expect_attr(tc_sec1,"name","三室钢截面1")

    # 创建三室钢截面2
    tc_sec2 = section.create_steel_box_three_cell("三室钢截面2",2.5,12.0,12.0,0.02,1.0,1.0,0.5,0.016,0.016,0.014,0.4,0.012,0.012,0.012,2.0,1,2.0,"Right")
    _expect_attr(tc_sec2,"name","三室钢截面2")

    # 创建三室钢截面3
    tc_sec3 = section.create_steel_box_three_cell("三室钢截面3",2.5,12.0,12.0,0.02,1.0,1.0,0.5,0.016,0.016,0.014,0.4,0.012,0.012,0.012,2.0,1,2.0,"Both")
    _expect_attr(tc_sec3,"name","三室钢截面3")

    # 创建单箱单室斜顶板钢截面
    sbi_section = section.create_steel_box_itf("单箱单室斜顶板钢截面", 2.5, 12.0, 10.0, 8.0, 0.02, 1.0, 1.0, 0.5, 0.016, 0.016, 0.014, 0.014, 0.4, 0.012, 0.012, 0.012)
    _expect_attr(sbi_section,"name","单箱单室斜顶板钢截面")

    # 创建双室钢截面1
    scb_sec1 = section.create_steel_canti_box("双室钢截面1", 2.5, 12.0, 10.0, 0.02, 1.0, 0.5, 0.016, 0.016, 0.014, 0.012, 1, 0.012, "Left", 0.3, 0.012)
    _expect_attr(scb_sec1,"name","双室钢截面1")

    # 创建双室钢截面2
    scb_sec2 = section.create_steel_canti_box("双室钢截面2",2.5, 12.0, 10.0, 0.02, 1.0, 0.5, 0.016, 0.016, 0.014, 0.012, 1, 0.012,"Right",0.2,0.015)
    _expect_attr(scb_sec2,"name","双室钢截面2")

    # 创建双室钢截面3
    scb_sec3 = section.create_steel_canti_box("双室钢截面3",2.5, 12.0, 10.0, 0.02, 1.0, 0.5, 0.016, 0.016, 0.014, 0.012, 1, 0.012,"Both",0.3,0.012)
    _expect_attr(scb_sec3,"name","双室钢截面3")

    # 创建双室斜底板钢截面1
    scbi_sec1 = section.create_steel_canti_box_ibf(
        "双室斜底板钢截面1",
        h=2.8, bt=15.0, bb=8.0, bc=2.0,
        i=0.02, a=1.5, dt=0.5,
        tt1=0.03, tt2=0.025, tb1=0.035, tb2=0.03,
        tw1=0.025, has_web=1, tw2=0.02,
        web_rib_pos="Both", h_end=0.3, t_end=0.015,
    )
    _expect_attr(scbi_sec1,"name","双室斜底板钢截面1")

    # 创建三角形钢截面
    matrix = [[1, 2, 20], [2, 3, 25], [3, 4, 30], [4, 1, 25]]
    osis_matrix("PointMatrix", matrix)
    osis_matrix("LineMatrix", matrix)
    csc_section = section.create_steel_custom("三角形钢截面", "PointMatrix", "LineMatrix")
    _expect_attr(csc_section,"name","三角形钢截面")

    # 创建自定义钢梁截面
    cscp_section = section.create_steel_custom_plate("自定义钢梁截面", ["TopFlange"])
    _expect_attr(cscp_section,"name","自定义钢梁截面")

    cscp_section.add_steel_plate(
        "STEEL", "TopFlange",
        0.0, 0.0, 1.0, 0.0, 0.02,
        1, 1, 0.0, "Both",
    )

    # 创建小箱梁截面
    small_section = section.create_smallbox("小箱梁截面", "MIDDLE", 1.6, 1.65, 1.2, 0.0, 1.0, 0.18, 0.2, 0.2, 4.0, 0.18, 0.25, 0.2, 0.15, 0.25, 0.05, 0.05, False, 0.0, 0.0, 0.05)
    _expect_attr(small_section,"name","小箱梁截面")

    # 创建空心板截面
    ch_section = section.create_hollowslab("空心板截面", "MIDDLE", 0.95, 1.0, 0.57, 0.05, 0.12, 0.12, 0.16, 0.12, 0.16, 0.38, 0.15, 0.08, 0.12, 0.08, 0.05, 0.05, 0.08, 0.08, 0.12)
    _expect_attr(ch_section,"name","空心板截面")

    # 创建圆端形截面
    cre_section = section.create_rounded_end("圆端形截面", "Solid", 7.0, 3.0, 2.0, False, 4.0, 1.0, 0.5, 0.25, 1.0, 0.5, 0.25)
    _expect_attr(cre_section,"name","圆端形截面")

    # 创建常规箱梁截面
    ctb_section = section.create_conventionalbox("常规箱梁截面", 2.7, 6.375, 6.375, 3.5, 3.5, 0.5, 0.28, 0.32, 0.5, 0.5, 1, 5.05, 4.5, 5.05, 5.05, 1.5, 0.7, 0.0, 0.0, 1.0, 0.5, 0.5, 0.35, 0.6, 0.3, 1.0, 0.5, 0.6, 0.3, 2.875, 0.2, 1.325, 0.7, 0.4, True, 2.875, 0.2, 1.325, 0.7, 0.4, "Integral", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    _expect_attr(ctb_section,"name","常规箱梁截面")

    # 创建扁平箱梁截面
    cfb_section = section.create_streamed_box(
        "扁平箱梁截面",4.0,20.0,20.0,
        10.5,10.5,0.8,0.28,0.27,
        0.27,0.25,0.5,0.27,0.4,
        5,4.7,6.85,6.0,
        6.85,0.6,0.6,1.0,
        0.7,0.2,0.2,1.0,0.7,0.6,
        0.3,0.5,0.7,0.5,0.3,4.0,
        0.2,0.5,0.7,0.4,True,
        4.0,0.2,0.5,0.7,0.4,"Integral",
        0.0,0.0,0.0,0.0,0.0,0.5,0.2
)
    _expect_attr(cfb_section,"name","扁平箱梁截面")

    # 创建双边箱截面
    dsb_sec = section.create_double_side_box("双边箱截面", 3.8, 36.0, 14.8, 2.1, 4.4, 0.3, 0.3, 0.3, 0.5, 1.0, 1.0, 8.0, 1.0, 0.6, 1.0, 0.7, 0.6, 0.3, 1.0, 0.7, 0.3, "Integral", 0.0, 0.0, 0.0)
    _expect_attr(dsb_sec,"name","双边箱截面")

    # 创建肋板式截面
    r_sec = section.create_ribbed_slab("肋板式截面",2.8,21.5,17.7,0.3,0.2,1.25,1.8,0.2,1.5,0.3,"Integral",0.0,0.0,0.0,)
    _expect_attr(r_sec,"name","肋板式截面")

    # 创建T梁截面left
    t_sec1 = section.create_TGirder("T梁截面left","Left",2.5,1.125,0.85,0.0,0.16,0.25,0.6,0.2,0.6,0.35,0.25,False,0.0,0.0,0.05)
    _expect_attr(t_sec1,"name","T梁截面left")
    # 创建T梁截面right
    t_sec2 = section.create_TGirder("T梁截面right", "Right", 2.5, 1.125, 0.85, 0.0, 0.16, 0.25, 0.6, 0.2, 0.6, 0.35, 0.25,
                                    False, 0.0, 0.0, 0.05)
    _expect_attr(t_sec2,"name","T梁截面right")
    # 创建T梁截面middle
    t_sec3 = section.create_TGirder("T梁截面middle", "Middle", 2.5, 1.125, 0.85, 0.0, 0.16, 0.25, 0.6, 0.2, 0.6, 0.35, 0.25,
                                    False, 0.0, 0.0, 0.05)
    _expect_attr(t_sec3,"name","T梁截面middle")

    # 创建自定义截面
    contour_matrix = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 1],
        [1, 0, 1],
    ]
    osis_matrix("ContourMatrix", contour_matrix)
    c_sec = section.create_custom("自定义截面", contour_matrix="ContourMatrix")
    _expect_attr(c_sec,"name","自定义截面")

    # 修改截面编号
    old_no = c_sec.no
    new_no = old_no + 1
    c_sec.renumber(new_no)
    _expect_attr(section.get(new_no), "name", "自定义截面")
    section.get(new_no)
    # 删除截面
    section.delete(new_no)
    
    # 数值截面
    circle_sec1.create_numerical(
        99,
        "数值截面-测试",
        "0.50",       # strArea 面积
        0.0, 0.0,     # dSy, dSz
        0.0, 0.01, 0.01, 0.0,  # dIxx, dIyy, dIzz, dIww
        0.0, 0.0,     # dCentY, dCentZ
        0.0, 0.0,     # dDy, dDz
        2.0, 0.0,     # dPeriO, dPeriI
    )
    got = section.get(99)
    _expect_attr(got, "name", "数值截面-测试")
    section.delete(99)

    all_section = section.all()
    if len(all_section) == 0:
        raise ValueError("section.all() 为空")


    # 截面 1: 标准截面
    sec1 = section.create_hollowslab(
        "标准截面", "MIDDLE",
        0.9500, 1.0000, 0.5700, 0.0500,
        0.1200, 0.1200, 0.1600, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0500, 0.0500, 0.0800, 0.0800, 0.1200,
        no=1
    )
    _expect_attr(sec1,"name","标准截面")

    sec1.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec1.set_mesh(0, 0.1000)

    # 点号、x、y 按 OSIS/截面默认应力点编号修改
    sec1.set_stress_point(1, 0.0, 0.0)   

    # 截面 2: 墩顶截面
    sec2 = section.create_hollowslab(
        "墩顶截面", "MIDDLE",
        0.9500, 1.0000, 0.6200, 0.0000,
        0.1200, 0.2500, 0.3200, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0000, 0.0500, 0.0000, 0.0800, 0.1200,
        no=2
    )
    _expect_attr(sec2,"name","墩顶截面")
    sec2.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec2.set_mesh(0, 0.1000)

    # 截面 3: 加厚截面
    sec3 = section.create_hollowslab(
        "加厚截面", "MIDDLE",
        0.9500, 1.0000, 0.5700, 0.0500,
        0.1200, 0.2500, 0.2400, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0500, 0.0500, 0.0800, 0.0800, 0.1200,
        no=3
    )
    _expect_attr(sec3,"name","加厚截面")
    sec3.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec3.set_mesh(0, 0.1000)

    # 截面 4: 墩顶截面（复制）
    sec4 = section.create_hollowslab(
        "墩顶截面", "MIDDLE",
        0.9500, 1.0000, 0.6200, 0.0000,
        0.1200, 0.2500, 0.3200, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0000, 0.0500, 0.0000, 0.0800, 0.1200,
        no=4
    )
    _expect_attr(sec4,"name","墩顶截面")
    sec4.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec4.set_mesh(0, 0.1000)

    # 截面 5: 加厚截面（复制）
    sec5 = section.create_hollowslab(
        "加厚截面", "MIDDLE",
        0.9500, 1.0000, 0.5700, 0.0500,
        0.1200, 0.2500, 0.2400, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0500, 0.0500, 0.0800, 0.0800, 0.1200,
        no=5
    )
    _expect_attr(sec5,"name","加厚截面")
    sec5.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec5.set_mesh(0, 0.1000)

    # 钢筋
    mat_no = mat_nos[1] # 钢筋材料
    # 纵向钢筋
    sec1.add_rebar_point(1, mat_no, 0.0, 0.0, "D16")
    sec1.add_rebar_point(2, mat_no, 0.0, 0.0, "D16")
    sec1.add_rebar_line_a(2, mat_no, "Left", 0.0, "Top", 0.0, 1, 0.1, "D16")
    sec1.delete_rebar(2)
    sec1.add_rebar_line_b(3, mat_no, 0.0, 0.0, 1.0, 0.0, 1, 1, 0.1)
   # 抗剪钢筋
    sec1.add_rebar_s_bent_up(mat_no, 0.1, 0.01, 1)
    sec1.add_rebar_s_shear_stirrup(mat_no, 0.1, 0.01)
    sec1.add_rebar_s_web_vertical(mat_no, 0.1, 0.01, 1, 1, 1)
    sec1.add_rebar_s_torsional_stirrup(mat_no, 0.1, 0.01, 0.01)
    sec1.delete_rebar_s("BentUpRebar")
    
    # sec1.add_rebar_circle(
    #   n_rebar_no=4,
    #   n_material_no=mat_no,
    #   d_center_y=0.0,
    #   d_center_z=0.0,
    #   d_radius=0.30,
    #   n_method=1,
    #   n_num=8,
    #   d_interval=0.0,
    #   diameter="D16",
    # )
    # sec1.delete_rebar(4)

    sec1.add_rebar_line_a(8, mat_no, "Left", 0.0, "Top", 0.0, 1, 0.1, "D16")

    return [sec1.no, sec2.no, sec3.no, sec4.no, sec5.no]

if __name__ == "__main__":
    from ._0_engine import engine
    sec_nos = build_sections(engine)
    print(sec_nos)
    print(engine.section.all())
