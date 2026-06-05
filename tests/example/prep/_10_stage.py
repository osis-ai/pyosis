from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, element_group_names: list[str], boundary_group_names: list[str], loadcase_names: list[str], settle_analysis_names: list[str], live_analysis_names: list[str], buckling_analysis_names: list[str], damping_names: list[str], rspec_analysis_names: list[str]) -> None:
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
        buckling_analysis_names: 屈曲分析工况名称
        damping_names: 阻尼名称（预留，当前未使用）
        rspec_analysis_names: 反应谱分析工况名称
    """
    stage = engine.stage
    eg_end_conc, eg_tendon1, eg_tendon2, eg_main_beam = element_group_names
    bg_abutment1, bg_abutment2 = boundary_group_names
    lc_barrier, lc_end_conc, lc_neg_temp, lc_pavement, lc_pst, lc_temp_drop, lc_temp_rise, lc_pos_temp, lc_dead = loadcase_names

    la_lane, = live_analysis_names
    buckl_name, = buckling_analysis_names
    rspec_name, = rspec_analysis_names
    # Stage 1: 主梁预制、张拉预应力（编号 1）
    stg1 = stage.create(no=1, name="CS1_主梁预制、张拉预应力", duration=7.0)
    stg1.define_element(1, 1, eg_main_beam, 7.0, 0)
    stg1.define_boundary(1, 1, bg_abutment1)
    stg1.define_boundary(1, 1, bg_abutment2)
    stg1.define_loadcase(1, 1, "", lc_dead)
    stg1.define_loadcase(1, 1, "", lc_pst)
    stg1.define_loadcase(1, 1, "", lc_end_conc)
    stg1.define_analysis(1, "SETL", settle_analysis_names[0])
    
    # Stage 2: 存梁（编号 2）
    stage.create(no=2, name="CS2_存梁", duration=60.0)
    
    # Stage 3: 二期恒载（编号 3）
    stg3 = stage.create(no=3, name="CS3_二期恒载", duration=30.0)
    stg3.define_loadcase(1, 1, "", lc_pavement)
    stg3.define_loadcase(1, 1, "", lc_barrier)
    
    # Stage 4: 徐变（编号 4）
    stage.create(no=4, name="CS4_徐变", duration=3650.0)
    stage.delete(4)
    if stage.get(4) is not None:
        raise ValueError("delete(4) 后 get(4) 应返回 None")
    # insert：在阶段 3 后插入临时阶段（编号应为 4）
    stg_ins = stage.insert("_阶段插入测试", ref_no=3, position=1, duration=1.0)
    if stg_ins is None or stg_ins.name != "_阶段插入测试":
        raise ValueError("insert 失败")
    got4 = stage.get(4)
    if got4 is None or got4.name != "_阶段插入测试":
        raise ValueError(f"insert 后 get(4) 应为 '_阶段插入测试'，实际 {getattr(got4, 'name', None)!r}")
    # get
    got1 = stage.get(1)
    if got1 is None or got1.name != "CS1_主梁预制、张拉预应力":
        raise ValueError("get(1) 失败")
    if settle_analysis_names[0] not in got1.analysis_cases:
        raise ValueError(
            f"stg1 应含沉降分析 {settle_analysis_names[0]!r}, 实际 {got1.analysis_cases!r}"
        )
    if eg_main_beam not in got1.element_groups:
        raise ValueError(
            f"element_groups 应含 {eg_main_beam!r}, 实际 {got1.element_groups!r}"
        )
    
    # all
    all_stg = stage.all()
    if not any(s.name == "_阶段插入测试" for s in all_stg):
        raise ValueError("all() 中应包含 '_阶段插入测试'")
    if len(all_stg) != 4:
        raise ValueError(f"insert 后应有 4 个阶段，实际 {len(all_stg)}")
    # remove：仅移除 insert 插入的阶段
    stage.remove(4)
    if stage.get(4) is not None:
        raise ValueError("remove(4) 后 get(4) 应返回 None")
    if any(s.name == "_阶段插入测试" for s in stage.all()):
        raise ValueError("remove 后 all() 不应再包含 '_阶段插入测试'")
    # 恢复业务阶段 4
    stage.create(no=4, name="CS4_徐变", duration=3650.0)
    
    # Stage 5: 运营阶段（编号 5）
    stg5 = stage.create(no=5, name="CS5_运营阶段", duration=0.0)
    stg5.define_loadcase(1, 1, "", lc_temp_rise)
    stg5.define_loadcase(1, 1, "", lc_temp_drop)
    stg5.define_loadcase(1, 1, "", lc_pos_temp)
    stg5.define_loadcase(1, 1, "", lc_neg_temp)
    stg5.define_analysis(1, "LIVE", la_lane)
    # stg5.define_analysis(1, "MODAL")
    stg5.define_analysis(1, "RSPEC", rspec_name)
    stg5.define_analysis(1, "BUCKLE", buckl_name)

    got5 = stage.get(5)
    if got5 is None or got5.name != "CS5_运营阶段":
        raise ValueError("get(5) 失败")
    if la_lane not in got5.analysis_cases:
        raise ValueError(
            f"stg5 应含活载分析 {la_lane!r}, 实际 {got5.analysis_cases!r}"
        )
    if rspec_name not in got5.analysis_cases:
        raise ValueError(
            f"stg5 应含反应谱分析 {rspec_name!r}, 实际 {got5.analysis_cases!r}"
        )
    if buckl_name not in got5.analysis_cases:
        raise ValueError(
            f"stg5 应含屈曲分析 {buckl_name!r}, 实际 {got5.analysis_cases!r}"
        )
if __name__ == "__main__":
    from _0_engine import engine

    # [engine.stage.delete(stg.no) for stg in engine.stage.all()]
    engine.stage.clear()

    elem_group_names = [g.name for g in engine.element.group.all()]
    bd_group_names = [g.name for g in engine.boundary.group.all()]

    _lc_order = [
        "防撞护栏工况", "封端混凝土工况", "负温度梯度", "铺装工况", "预应力",
        "整体降温", "整体升温", "正温度梯度", "主梁单元自重",
    ]
    by_lc = {lc.name: lc.name for lc in engine.load.all()}
    if not by_lc:
        raise Exception("荷载工况为空")
    lc_names = [by_lc[n] for n in _lc_order]

    settle_analysis = ["沉降分析工况"]
    live_analysis = ["车道荷载包络"]

    build_stages(
        engine, elem_group_names, bd_group_names, lc_names,
        settle_analysis, live_analysis,
        ["屈曲分析工况"], [], ["反应谱分析工况"],
    )
    print(engine.stage.all())
