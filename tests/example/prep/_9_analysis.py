from typing import Any

from pyosis.core.engine import OSISEngine

def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"荷载工况属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

def build_settle_analysis(engine: OSISEngine, node_nos: list[int]) -> list[str]:
    """创建沉降分析"""
    st = engine.settlement
    support_nodes = [node_nos[0], node_nos[-1]]

    # 1) 业务沉降组
    eg_main = st.group.create("空心板支座沉降", -0.005, node_nos[0], node_nos[-1])
    got_main = st.group.get("空心板支座沉降")
    if got_main is None or got_main.name != "空心板支座沉降":
        raise ValueError("获取 '空心板支座沉降' 失败")

    # 2) 沉降荷载工况
    e = st.create("沉降分析工况")
    got_case = st.get("沉降分析工况")
    if got_case is None or got_case.name != "沉降分析工况":
        raise ValueError("获取 '沉降分析工况' 失败")

    # 3) 把沉降组纳入该工况
    e.include("a",eg_main.name)
    if eg_main.name not in (e.setl_grp_nos or []):
        raise ValueError(f"include 后应包含 {eg_main.name!r}")

    # 4) 测试 remove：临时沉降组，测完删除
    eg_test = st.group.create("_沉降测试组", -0.001, node_nos[0])
    got_test = st.group.get("_沉降测试组")
    if got_test is None or got_test.name != "_沉降测试组":
        raise ValueError("获取 '_沉降测试组' 失败")

    all_groups = st.group.all()
    if not any(g.name == "_沉降测试组" for g in all_groups):
        raise ValueError("st.group.all() 中应包含 '_沉降测试组'")
    if st.group.count() != 2:
        raise ValueError(f"st.group.count() 应为 2，实际 {st.group.count()}")

    e.include(eg_test.name)
    e.remove(eg_test.name)
    if eg_test.name in (e.setl_grp_nos or []):
        raise ValueError(f"remove 后仍包含 {eg_test.name!r}")
    if eg_main.name not in (e.setl_grp_nos or []):
        raise ValueError(f"remove 后应仍保留 {eg_main.name!r}")
    st.group.rename("_沉降测试组", "_沉降测试组1")
    if st.group.get("_沉降测试组") is not None:
        raise ValueError("rename 后旧名 '_沉降测试组' 应不存在")
    if st.group.get("_沉降测试组1") is None:
        raise ValueError("rename 后应能通过 '_沉降测试组1' 获取")

    st.group.delete("_沉降测试组1")
    if st.group.get("_沉降测试组1") is not None:
        raise ValueError("delete 后 '_沉降测试组1' 应不存在")
    if st.group.count() != 1:
        raise ValueError(f"删除测试组后 st.group.count() 应为 1，实际 {st.group.count()}")

    # 5) 沉降工况 rename / delete（临时工况，勿动「沉降分析工况」）
    e_temp = st.create("_沉降工况测试")
    got_temp = st.get("_沉降工况测试")
    new_temp_name = "_" + got_temp.name
    st.rename(got_temp.name, new_temp_name)
    got_renum = st.get(new_temp_name)
    if got_renum is None or got_renum.name != new_temp_name:
        raise ValueError(
            f"rename 后名称应为 {new_temp_name!r}，实际 {getattr(got_renum, 'name', None)!r}"
        )
    st.delete(new_temp_name)
    if st.get(new_temp_name) is not None:
        raise ValueError(f"delete 后 get({new_temp_name!r}) 应返回 None")
    if st.get("_沉降工况测试") is not None:
        raise ValueError("delete 后 get('_沉降工况测试') 应返回 None")
    # 6) 业务工况校验
    all_cases = st.all()
    if not any(c.name == "沉降分析工况" for c in all_cases):
        raise ValueError("st.all() 中应包含 '沉降分析工况'")
    if st.count() != len(all_cases):
        raise ValueError(f"st.count() 应为 1，实际 {st.count()}")

    return [e.name]

def build_buckling_analysis(engine: OSISEngine, loadcase_names: list[str]) -> list[str]:
    """创建屈曲分析工况（依赖 _8 的静力荷载工况名）"""
    (
        lc_barrier,
        lc_end_conc,
        lc_neg_temp,
        lc_pavement,
        lc_pst,
        lc_temp_drop,
        lc_temp_rise,
        lc_pos_temp,
        lc_dead,
    ) = loadcase_names

    stab = engine.stability
    [stab.delete(case.name) for case in stab.all()]
    buckl_name = "屈曲分析工况"

    # 1) 业务屈曲工况
    buck = stab.create(buckl_name, num=5, accum=0, scalar=1.0, load_type=0)
    buck.include("a", lc_dead, 1.0, 0)
    buck.include("a", lc_pst, 1.0, 0)

    # 2) get
    got = stab.get(buckl_name)
    if got is None:
        raise ValueError(f"获取 {buckl_name!r} 失败")

    # 3) all
    all_buckl = stab.all()
    if not any(b.name == buckl_name for b in all_buckl):
        raise ValueError(f"stab.all() 中应包含 {buckl_name!r}")

    # 4) replace
    test_name = "_屈曲replace测试"
    test_buck = stab.create(test_name, num=3, accum=0, scalar=1.0, load_type=0)
    test_buck.include("a", lc_temp_drop, 1.0, 0)
    got_test = stab.get(test_name)
    if got_test is None:
        raise ValueError(f"获取 {test_name!r} 失败")
    if not any(
            isinstance(p, dict)
            and (p.get("loadCase") == lc_temp_drop or p.get("name") == lc_temp_drop)
            for p in (got_test.lcParas or [])
    ):
        raise ValueError(
            f"include 后应包含 {lc_temp_drop!r}, lcParas={got_test.lcParas!r}"
        )
    test_buck.replace(lc_temp_rise, 1.0, 0, lc_temp_drop, 1.0, 0)
    got_test = stab.get(test_name)
    if got_test is None:
        raise ValueError(f"replace 后获取'{test_name!r}'失败")
    if got_test.name != test_name:
        raise ValueError(f"replace 后名称应为'{test_name!r}'，实际'{got_test.name!r}'")
    
    # 5) renumber
    stab.rename(got_test.name, "_"+got_test.name)
    got_renum = stab.get("_"+got_test.name)
    if got_renum is None or got_renum.name != "_"+got_test.name:
        raise ValueError(f"rename 后名称应为_{got_test.name}，实际 {getattr(got_renum, 'name', None)!r}")
    stab.delete(test_name)
    if stab.get(test_name) is not None:
        raise ValueError(f"delete 后 get({test_name!r}) 应返回 None")

    return [buckl_name]

def build_damping(engine: OSISEngine) -> list[str]:
    damp = engine.prop.damping

    # 振型阻尼
    damp.create_modal("阻尼-振型-测试", 0.05)
    got = damp.get("阻尼-振型-测试")
    if got is None:
        raise ValueError(f"获取'阻尼-振型-测试'失败")
    _expect_attr(got, "name", "阻尼-振型-测试")

    all_damp = damp.all()
    if not any(d.name == "阻尼-振型-测试" for d in all_damp):
        raise ValueError(f"damping.all() 中应包含 阻尼-振型-测试!r")

    damp.delete("阻尼-振型-测试")

    damp.create_rayleigh_custom("阻尼-Rayleigh-自定义-测试", alpha=0.5, beta=0.002)
    got = damp.get("阻尼-Rayleigh-自定义-测试")
    if got is None:
        raise ValueError(f"获取'阻尼-Rayleigh-自定义-测试'失败")
    _expect_attr(got, "name", "阻尼-Rayleigh-自定义-测试")
    damp.rename("阻尼-Rayleigh-自定义-测试","阻尼-Rayleigh-自定义-测试1")
    damp.all()
    damp.delete("阻尼-Rayleigh-自定义-测试1")

    damp_name = "阻尼-公式"
    damp.create_rayleigh_formula(damp_name, ksii=0.05, ksij=0.05, wi=1.0, wj=10.0,)
    return [damp_name]

def build_live_analysis(engine: OSISEngine, element_group_names: list[str]):
    """创建活载分析（活载等级、车道、工况）
    
    标识说明：
    - 活载等级：名称标识（非数字编号）
    - 车道：名称标识
    - 活载工况：名称标识
    """
    live = engine.live
    for case in live.case.all():
        got = live.case.get(case.name)
        if got is not None:
            for sub in list(got.sub_load_cases):
                got.delete_sub(sub.name)
        live.case.delete(case.name)
    for lane in live.lane.all():
        live.lane.delete(lane.name)
    for grade in live.grade.all():
        live.grade.delete(grade.name)
    # 活载等级（名称标识）
    grade1 = live.grade.create_highway("简支空心板移动荷载", code="JTGD60_2015", live_load_type="HIGHWAY_I")
    _expect_attr(grade1,"name","简支空心板移动荷载")

    grade2 = live.grade.create_vehicle("车辆荷载等级", code="JTGD60_2015", live_load_type="VEHICLE")
    _expect_attr(grade2,"name","车辆荷载等级")

    # grade3 = live.grade.create_crowd("人群荷载等级", code="JTGD60_2015", live_load_type="CROWD", bridge_type="BRIDGE_COMMON", para=10.0)
    # _expect_attr(grade3,"name","人群荷载等级")

    grade4 = live.grade.create_fatigue("疲劳荷载等级", code="JTGD60_2015", live_load_type="FATIGUE_I")
    _expect_attr(grade4,"name","疲劳荷载等级")

    grade5 = live.grade.create_custom(
        "自定义轴载", code="CUSTOM", live_load_type="VG",
        veh_grp_layout=[(0.0, 140.0), (3.5, 140.0)],
    )
    _expect_attr(grade5, "name", "自定义轴载")


    eg_end_conc, eg_tendon1, eg_tendon2, eg_main_beam, _ = element_group_names
    # 节点 1~14 纵向跨度（与主梁单元组 1~13 一致，不含重复单元 14）
    bridge_span = 15.51
    # 车道（名称标识）
    lane1 = live.lane.create_ve(
        name="车道", length=bridge_span, wheel=1.80, orientation=1, ref=0,
        ref_elems=eg_main_beam, offset_y=0.0, offset_z=0.0,
    )
    _expect_attr(lane1,"name","车道")

    lane2 = live.lane.create_tcb(
        "车道2", eg_main_beam, length=bridge_span, wheel=1.80, orientation=1, ref=0,
        ref_elems=eg_main_beam, offset_y=0.0, offset_z=0.0,
    )
    _expect_attr(lane2,"name","车道2")

    # 活载工况（名称标识）
    lc1 = live.case.create("车道荷载包络", "JTGD60_2015", 1)
    lc2 = live.case.create("车道荷载包络2", "JTGD60_2015", 1)

    live.case.get("车道荷载包络")
    if live.case.count() == 0:
        raise Exception("获取活载工况数量错误")
    # 横向布载折减系数
    lc1.set_trans_reduction_factors(1.2000, 1.0000, 0.7800, 0.6700, 0.6000, 0.5500, 0.5200, 0.5000, 0.5000, 0.5000)
    
    # 子工况
    lc1.create_sub(sub_name="车道荷载工况1",grade_name=grade1.name,scalar=1.0,calc_mu=True,bridge_type="CUSTOM",mu_params=[7.557770],lane_names=[lane1.name])
    lc2.create_sub(sub_name="车道荷载工况2",grade_name=grade2.name,scalar=1.0,calc_mu=True,bridge_type="CUSTOM",mu_params=[7.557770],lane_names=[lane2.name])
    
    lc2.modify_sub(
        sub_name="车道荷载工况2",
        grade_name=grade2.name,
        scalar=2.0,
        calc_mu=True,
        bridge_type="SIMPLE",
        mu_params=[bridge_span, 3.45e10, 0.5, 2500.0],  # 桥长、弹模、惯性矩、质量
        lane_names=[lane2.name],
    )

    lc2.rename_sub("车道荷载工况2", "车道荷载工况333")
    lc2.set_lane_count("车道荷载工况333", 0, 1)
    lc2.delete_sub("车道荷载工况333")
    
    # 加载车道数范围
    lc1.set_lane_count("车道荷载工况1", 0, 1)

    live.grade.rename("简支空心板移动荷载", "简支空心板移动荷载1")
    live.grade.get("简支空心板移动荷载1")
    live.grade.all()

    live.grade.delete(grade4.name)
    if live.grade.get(grade4.name) is not None:
        raise ValueError(f"delete({grade4.name!r}) 后 get 应返回 None")

    # 重命名车道
    live.lane.rename("车道2", "车道222")
    live.lane.get("车道222")
    live.lane.all()
    live.lane.count()
    # 删除车道
    live.lane.delete("车道222")
    if live.lane.get("车道222") is not None:
        raise ValueError("delete('车道222') 后 get 应返回 None")
    live.case.rename(lc2.name, "车道荷载包络2_重命名")
    got_lc2 = live.case.get("车道荷载包络2_重命名")
    if got_lc2 is None:
        raise ValueError("live.case.rename 后 get 失败")
    live_analysis_names = [lc1.name]
    return live_analysis_names

def build_rspec_analysis(engine: OSISEngine, damping_names: list[str]) -> list[str]:
    dynamic = engine.dynamic
    rsp = dynamic.seismic
    rspec = dynamic.response_spectrum

    test_spec_name = "_反应谱测试谱"
    test_case_name = "_反应谱工况测试"

    rsp.create_code(
        test_spec_name, "A", 9.8, code="JTGT2231_01_2020",
        intensity=0.05, site=0, delta_t=0.1,
    )

    rspec.create(
        test_case_name,
        spectrum=test_spec_name,
        damping_name=damping_names[0],
        num=5,
    )
    rspec.all()
    got = rspec.get(test_case_name)
    if got is None:
        raise ValueError(f"获取 {test_case_name!r} 失败")

    renamed_case_name = "_" + got.name
    rspec.rename(got.name, renamed_case_name)
    got2 = rspec.get(renamed_case_name)
    if got2 is None or got2.name != renamed_case_name:
        raise ValueError(
            f"rename 后名称应为 {renamed_case_name!r}，实际 {getattr(got2, 'name', None)!r}"
        )

    rspec.rename(renamed_case_name, test_case_name)
    got3 = rspec.get(test_case_name)
    if got3 is None or got3.name != test_case_name:
        raise ValueError(
            f"rename 回原名后应为 {test_case_name!r}，实际 {getattr(got3, 'name', None)!r}"
        )

    rspec.delete(test_case_name)
    if rspec.get(test_case_name) is not None:
        raise ValueError(f"delete 后 get({test_case_name!r}) 应返回 None")
    rsp.delete(test_spec_name)
    if rsp.get(test_spec_name) is not None:
        raise ValueError(f"delete 后 get({test_spec_name!r}) 应返回 None")

    biz_spec_name = "反应谱-运营谱"
    biz_rspec_name = "反应谱分析工况"
    rsp.create_code(
        biz_spec_name, "A", 9.8, code="JTGT2231_01_2020",
        intensity=0.05, site=0, delta_t=0.1,
    )
    rspec.create(
        biz_rspec_name,
        spectrum=biz_spec_name,
        damping_name=damping_names[0],
        num=5,
    )
    got_biz = rspec.get(biz_rspec_name)
    if got_biz is None:
        raise ValueError(f"获取 {biz_rspec_name!r} 失败")

    return [biz_rspec_name]

if __name__ == "__main__":
    from _0_engine import engine

    engine.settlement.clear()
    engine.settlement.group.clear()

    ele_groups = engine.element.group.all()
    print("element groups", ele_groups)
    elem_group_names = [g.name for g in ele_groups]

    # live_names = build_live_analysis(engine, elem_group_names)
    # print(live_names)
    # print(engine.live.case.all())
    _order = ["防撞护栏工况","封端混凝土工况","负温度梯度","铺装工况","预应力","整体降温","整体升温","正温度梯度","主梁单元自重",]
    by_name = {lc.name: lc.name for lc in engine.load.all()}
    if not by_name:
        raise Exception("荷载工况为空")
    lc_names = [by_name[n] for n in _order]
    buckling_names = build_buckling_analysis(engine, lc_names)

    # lc_names = [lc.name for lc in engine.load.all()]
    settle_names = build_settle_analysis(engine, [n.no for n in engine.node.all()])
    live_names = build_live_analysis(engine, elem_group_names)
    # buckling_names = build_buckling_analysis(engine, lc_names)
    build_damping(engine)
    print("settle", settle_names)
    print("live", live_names)
    print("buckling", buckling_names)