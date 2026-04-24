from pyosis.core.engine import OSISEngine

def build_settle_analysis(engine: OSISEngine, node_nos: list[int]):
    """创建沉降分析（当前模板未定义沉降组）"""
    settle_analysis_names = []
    
    return settle_analysis_names


def build_live_analysis(engine: OSISEngine, element_group_names: list[str]):
    """创建活载分析（活载等级、车道、工况）
    
    标识说明：
    - 活载等级：名称标识（非数字编号）
    - 车道：名称标识
    - 活载工况：名称标识
    """
    live = engine.live
    
    # 活载等级（名称标识）
    grade1 = live.grade.create_highway("简支空心板移动荷载", "JTGD60_2015", "HIGHWAY_I")
    
    eg_end_conc, eg_tendon1, eg_tendon2, eg_main_beam = element_group_names
    # 车道（名称标识）
    lane1 = live.lane.create_ve(
        name="车道",
        dLength=15.0800,
        wheel=1.80,
        eOriention=1,
        eRef=0,
        ref_elems=eg_main_beam,
        offsetY=0.0,
        offsetZ=0.0,
    )
    
    # 活载工况（名称标识）
    livecase_lane = live.case.create("车道荷载包络", "JTGD60_2015", 1)
    # 横向布载折减系数
    livecase_lane.set_trans_reduction_factors([1.2000, 1.0000, 0.7800, 0.6700, 0.6000, 0.5500, 0.5200, 0.5000, 0.5000, 0.5000])
    
    # 子工况
    livecase_lane.create_sub(
        sub_name="车道荷载工况1",
        grade_name=grade1.name,
        scalar=1.0,
        calc_mu=True,
        bridge_type="CUSTOM",
        mu_params=[7.557770],
        lane_names=[lane1.name],
    )
    
    # 加载车道数范围
    livecase_lane.set_lane_count("车道荷载工况1", 0, 1)

    live_analysis_names = [livecase_lane.name, ]
    return live_analysis_names

if __name__ == "__main__":
    from _0_engine import engine
    
    ele_groups = engine.element.group.all()
    print("element groups", ele_groups)
    elem_group_names = [g.name for g in ele_groups]
    
    live_names = build_live_analysis(engine, elem_group_names)
    print(live_names)
    print(engine.live.case.all())
