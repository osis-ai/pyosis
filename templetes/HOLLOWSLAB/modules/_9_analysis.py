from pyosis.core.engine import OSISEngine

def build_live_analysis(engine: OSISEngine) -> None:
    """创建活载分析（活载等级、车道、工况）"""
    live = engine.live
    
    # 活载等级
    grade1 = live.create_grade_highway("简支空心板移动荷载", "JTGD60_2015", "HIGHWAY_I")
    
    # 车道
    lane1 = live.create_lane_ve(
        name="车道",
        dLength=15.0800,
        wheel=1.80,
        eOriention=1,
        eRef=0,
        ref_elems=["主梁单元"],
        offsetY=0.0,
        offsetZ=0.0,
    )
    
    # 活载工况
    live_lane = live.create_live("车道荷载包络", "JTGD60_2015", 1)
    
    # 横向布载折减系数
    live_lane.set_trans_reduction_factors([1.2000, 1.0000, 0.7800, 0.6700, 0.6000, 0.5500, 0.5200, 0.5000, 0.5000, 0.5000])
    
    # 子工况
    live_lane.create(
        sub_name="车道荷载工况1",
        grade_name=grade1.name,
        scalar=1.0,
        calc_mu=True,
        bridge_type="CUSTOM",
        mu_params=[7.557770],
        lane_names=[lane1.name],
    )
    
    # 加载车道数范围
    live_lane.set_lane_count("车道荷载工况1", 0, 1)
