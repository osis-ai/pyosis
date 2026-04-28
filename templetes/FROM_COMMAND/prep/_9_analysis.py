"""分析设置"""

from pyosis.core.engine import OSISEngine


def build_live_analysis(engine: OSISEngine, elem_group_names) -> list[str]:
    """创建活载分析，返回活载分析名称列表
    
    活载分析：
    - 车道荷载包络
    """
    live = engine.live
    
    # 创建活载等级
    live.grade.create("简支空心板移动荷载", "JTGD60_2015", "HIGHWAY_I")
    
    # 创建活载分析
    live.case.create("车道荷载工况1")
    
    return ["车道荷载包络"]


if __name__ == "__main__":
    from ._0_engine import engine
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    live_names = build_live_analysis(engine, elem_group_names)
    print(live_names)
