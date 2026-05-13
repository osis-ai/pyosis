"""分析设置"""

from pyosis.core.engine import OSISEngine

def build_analysis(engine: OSISEngine, node_nos: list[int], elem_group_names: list[str]) -> tuple[list[str], list[str]]:
    """创建沉降分析和活载分析，返回(沉降工况名列表, 活载工况名列表)"""

    settle_names = []
    live_names = []

    engine.settlement.group.create('0', 5.000E-03, [2])

    engine.settlement.group.create('1', 5.000E-03, [23])

    engine.settlement.group.create('2', 5.000E-03, [45])

    engine.settlement.group.create('3', 5.000E-03, [67])

    engine.settlement.group.create('4', 5.000E-03, [89])

    engine.settlement.group.create('5', 5.000E-03, [110])

    st = engine.settlement.create('1个')
    settle_names.append(st.name)

    st.include('0', '1', '2', '3', '4', '5')

    engine.live.grade.create_highway('CH-CD', eCode='JTGD60_2015', eLiveLoadType='HIGHWAY_I')

    engine.live.lane.create_ve('1_', dLength=25.0000, wheel=1.80, eOriention=1, eRef=0, ref_elems='1_车道线单元组', offsetY=0.00000E+00, offsetZ=0.00000E+00)

    lc = engine.live.case.create('汽车', code='JTGD60_2015', sub_cmb_type=1)
    live_names.append(lc.name)

    lc.set_trans_reduction_factors([1.2000, 1.0000, 0.7800, 0.6700, 0.6000, 0.5500, 0.5200, 0.5000, 0.5000, 0.5000])

    lc.create_sub('汽车_sub1', 'CH-CD', scalar=0.71000, calc_mu=True, bridge_type='CUSTOM', mu_params=[3], lane_names=['1_'])

    lc.set_lane_count('汽车_sub1', 0, 1)

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