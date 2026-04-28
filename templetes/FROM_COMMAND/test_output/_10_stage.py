"""施工阶段"""

from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:
    """施工阶段"""

    # [TODO] 未识别命令: Stage,1,第一阶段,a,1to3
    # 提示: 未映射命令


if __name__ == "__main__":
    from ._0_engine import engine
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    bd_groups = engine.boundary.group.all()
    bd_group_names = [bg.name for bg in bd_groups]
    lcs = engine.load.all()
    lc_names = [lc.name for lc in lcs]
    live_names = []
    settle_names = []
    build_stages(engine, elem_group_names, bd_group_names, lc_names, settle_names, live_names)