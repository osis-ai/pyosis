from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, element_group_names: list[str], boundary_group_names: list[str], loadcase_names: list[str], settle_analysis_names: list[str], live_analysis_names: list[str]) -> None:
    """创建施工阶段
    
    阶段编号：
    - 1: CS1_主梁预制、张拉预应力
    - 2: CS2_存梁
    - 3: CS3_二期恒载
    - 4: CS4_徐变十年
    - 5: CS5_运营阶段
    
    Args:
        element_group_names: 单元组名称
        bd_group_names: 边界组名称
        loadcase_names: 荷载工况名称
        settle_analysis_names: 沉降分析工况名称
        live_analysis_names: 移动荷载分析工况名称
    """
    stage = engine.stage
    
    eg_end_conc, eg_tendon1, eg_tendon2, eg_main_beam = element_group_names
    bg_abutment1, bg_abutment2 = boundary_group_names
    lc_barrier, lc_end_conc, lc_neg_temp, lc_pavement, lc_pst, lc_temp_drop, lc_temp_rise, lc_pos_temp, lc_dead = loadcase_names

    la_lane, = live_analysis_names
    
    # Stage 1: 主梁预制、张拉预应力（编号 1）
    stg1 = stage.create(no=1, name="CS1_主梁预制、张拉预应力", duration=7.0)
    stg1.define_element(1, 1, eg_main_beam, 7.0, 0)
    stg1.define_boundary(1, 1, bg_abutment1)
    stg1.define_boundary(1, 1, bg_abutment2)
    stg1.define_loadcase(1, 1, "", lc_dead)
    stg1.define_loadcase(1, 1, "", lc_pst)
    stg1.define_loadcase(1, 1, "", lc_end_conc)
    
    # Stage 2: 存梁（编号 2）
    stage.create(no=2, name="CS2_存梁", duration=60.0)
    
    # Stage 3: 二期恒载（编号 3）
    stg3 = stage.create(no=3, name="CS3_二期恒载", duration=30.0)
    stg3.define_loadcase(1, 1, "", lc_pavement)
    stg3.define_loadcase(1, 1, "", lc_barrier)
    
    # Stage 4: 徐变十年（编号 4）
    stage.create(no=4, name="CS4_徐变十年", duration=3650.0)
    
    # Stage 5: 运营阶段（编号 5）
    stg5 = stage.create(no=5, name="CS5_运营阶段", duration=0.0)
    stg5.define_loadcase(1, 1, "", lc_temp_rise)
    stg5.define_loadcase(1, 1, "", lc_temp_drop)
    stg5.define_loadcase(1, 1, "", lc_pos_temp)
    stg5.define_loadcase(1, 1, "", lc_neg_temp)
    stg5.define_analysis(1, "LIVE", la_lane)

if __name__ == "__main__":
    from ._0_engine import engine
    
    ele_groups = engine.element.group.all()
    print("element groups", ele_groups)
    elem_group_names = [g.name for g in ele_groups]

    bd_groups = engine.boundary.group.all()
    print("boundary groups", bd_groups)
    bd_group_names = [g.name for g in bd_groups]
    
    loadcases = engine.load.all()
    print("loadcases", loadcases)
    lc_names = [lc.name for lc in loadcases]

    settles = engine.settlement.all()
    print("settlements", settles)
    settle_analysis = [sa.name for sa in settles]

    lives = engine.live.case.all()
    print("lives", lives)
    live_analysis = [la.name for la in lives]
    
    build_stages(engine, elem_group_names, bd_group_names, lc_names, settle_analysis, live_analysis)
    print(engine.stage.all())
