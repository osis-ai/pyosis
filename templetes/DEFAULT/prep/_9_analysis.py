"""分析设置"""

from pyosis.core.engine import OSISEngine

def build_analysis(engine: OSISEngine, node_nos: list[int], elem_group_names: list[str]) -> tuple[list[str], list[str]]:
    """创建沉降分析和活载分析，返回(沉降工况名列表, 活载工况名列表)"""

    settle_names = []
    live_names = []

    engine.settlement.group.create('沉降组1', -1.000E-02, [2001])

    engine.settlement.group.create('沉降组2', -1.000E-02, [2002])

    engine.settlement.group.create('沉降组3', -1.000E-02, [2003])

    engine.settlement.group.create('沉降组4', -1.000E-02, [2004])

    st = engine.settlement.create('支座沉降')
    settle_names.append(st.name)

    st.include('沉降组1', '沉降组2', '沉降组3', '沉降组4')

    engine.live.grade.create_highway('荷载1', eCode='JTGD60_2015', eLiveLoadType='HIGHWAY_I')

    engine.live.lane.create_ve('车道一', dLength=80.0000, wheel=1.8, eOriention=1, eRef=0, ref_elems='上部主梁单元组', offsetY=0.00000E+00, offsetZ=0.00000E+00)

    lc = engine.live.case.create('移动荷载工况1', code='JTGD60_2015', sub_cmb_type=0)
    live_names.append(lc.name)

    lc.create_sub('子工况1', '荷载1', scalar=2.69100, calc_mu=True, bridge_type='CUSTOM', mu_params=[4], lane_names=['车道一'])

    return settle_names, live_names


if __name__ == "__main__":
    from ._0_engine import engine
    nodes = engine.node.all()
    node_nos = [n.no for n in nodes]
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    settle_names, live_names = build_analysis(engine, node_nos, elem_group_names)
    print(settle_names)
    print(live_names)