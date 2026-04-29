"""分析设置"""

from pyosis.core.engine import OSISEngine

def build_live_analysis(engine: OSISEngine, elem_group_names) -> list[str]:
    """分析设置"""

    # ========== 原始命令流 ==========
    # SetlGrp,沉降组1,-1.000E-02,2001;//创建沉降组，引用节点号
    # SetlGrp,沉降组2,-1.000E-02,2002
    # SetlGrp,沉降组3,-1.000E-02,2003
    # SetlGrp,沉降组4,-1.000E-02,2004
    # SetlAnal,支座沉降;//创建沉降工况
    # SetlAnalInc,支座沉降,a,沉降组1,沉降组2,沉降组3,沉降组4;//添加沉降工况至沉降组，引用沉降组、沉降工况
    # LiveGrade,荷载1,JTGD60_2015,HIGHWAY_I;//创建移动荷载
    # InflAlgo,车道一,VE,80.0000,1,0,上部主梁单元组,0.00000E+00,0.00000E+00;//定义车道线，该方法引用单元组名称
    # LiveAnal,移动荷载工况1,JTGD60_2015,0;//定义活载工况
    # LiveAnalInc,移动荷载工况1,a,子工况1,荷载1,2.69100,1,CUSTOM,4.000000,车道一;//往活载工况里面加子工况，引用活载工况名
    return []


if __name__ == "__main__":
    from ._0_engine import engine
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    live_names = build_live_analysis(engine, elem_group_names)
    print(live_names)