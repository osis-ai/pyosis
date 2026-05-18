"""施工阶段"""

from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:
    """创建施工阶段"""

    stg = engine.stage.create(1, '预制梁', 90.0)

    stg.define_element(1, 1, '预制', nBirth=3.0, ePart=0)

    stg.define_boundary(1, 1, '临时')

    stg.define_boundary(1, 1, '永久-边支座')

    stg.define_loadcase(1, 1, "", '预制梁自重')

    stg.define_loadcase(1, 1, "", '预应力_正弯矩束')

    stg = engine.stage.create(2, '墩顶现浇', 30.0)

    stg.define_element(1, 1, '现浇', nBirth=3.0, ePart=0)

    stg.define_loadcase(1, 1, "", '墩顶现浇自重')

    stg = engine.stage.create(3, '负弯矩1', 1.0)

    stg.define_loadcase(1, 1, "", '预应力_负弯矩束-1')

    stg = engine.stage.create(4, '负弯矩2', 1.0)

    stg.define_loadcase(1, 1, "", '预应力_负弯矩束-2')

    stg.define_loadcase(1, 1, "", '预应力_负弯矩束-3')

    stg = engine.stage.create(5, '转连续', 1.0)

    stg.define_boundary(1, 1, '永久-中支座')

    stg.define_boundary(1, 0, '临时')

    stg = engine.stage.create(6, '二期', 30.0)

    stg.define_loadcase(1, 1, "", '二期_二期')

    stg = engine.stage.create(7, '成桥', 3000.0)

    stg = engine.stage.create(8, '运营', 0.0)

    stg.define_loadcase(1, 1, "", '温升_温升')

    stg.define_loadcase(1, 1, "", '温降_温降')

    stg.define_loadcase(1, 1, "", '局部升温_局部升温')

    stg.define_loadcase(1, 1, "", '局部降温_局部降温')

    stg.define_analysis(1, 'LIVE', '汽车')

    stg.define_analysis(1, 'SETL', '1个')



if __name__ == "__main__":
    from ._0_engine import engine
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    bd_groups = engine.boundary.group.all()
    bd_group_names = [bg.name for bg in bd_groups]
    lcs = engine.load.all()
    lc_names = [lc.name for lc in lcs]
    build_stages(engine, elem_group_names, bd_group_names, lc_names, [], [])