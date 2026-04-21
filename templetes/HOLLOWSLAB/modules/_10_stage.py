from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, lc_names: list[str]) -> None:
    """创建施工阶段
    
    Args:
        lc_names: 荷载工况名称列表，顺序对应：
            [barrier, end_conc, neg_temp, pavement, pst, temp_drop, temp_rise, pos_temp, dead]
    """
    stage = engine.stage
    
    lc_barrier, lc_end_conc, lc_neg_temp, lc_pavement, lc_pst, lc_temp_drop, lc_temp_rise, lc_pos_temp, lc_dead = lc_names
    
    # Stage 1: 主梁预制、张拉预应力
    stg1 = stage.create(1, 7.0, no=1, name="CS1_主梁预制、张拉预应力")
    stg1.define_element(1, 1, "主梁单元", 7.0, 0)
    stg1.define_boundary(1, 1, "桥台1_永久_x向固定")
    stg1.define_boundary(1, 1, "桥台2_永久_x向滑动")
    stg1.define_loadcase(1, 1, "", lc_dead)
    stg1.define_loadcase(1, 1, "", lc_pst)
    stg1.define_loadcase(1, 1, "", lc_end_conc)
    
    # Stage 2: 存梁
    stage.create(2, 60.0, no=2, name="CS2_存梁")
    
    # Stage 3: 二期恒载
    stg3 = stage.create(3, 30.0, no=3, name="CS3_二期恒载")
    stg3.define_loadcase(1, 1, "", lc_pavement)
    stg3.define_loadcase(1, 1, "", lc_barrier)
    
    # Stage 4: 徐变十年
    stage.create(4, 3650.0, no=4, name="CS4_徐变十年")
    
    # Stage 5: 运营阶段
    stg5 = stage.create(5, 0.0, no=5, name="CS5_运营阶段")
    stg5.define_loadcase(1, 1, "", lc_temp_rise)
    stg5.define_loadcase(1, 1, "", lc_temp_drop)
    stg5.define_loadcase(1, 1, "", lc_pos_temp)
    stg5.define_loadcase(1, 1, "", lc_neg_temp)
    stg5.define_analysis(1, 1, "LIVE", "车道荷载包络")
