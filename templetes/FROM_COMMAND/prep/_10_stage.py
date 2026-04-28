"""施工阶段"""

from pyosis.core.engine import OSISEngine


def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:
    """创建施工阶段
    
    施工阶段：
    - CS1: 主梁预制、张拉预应力（7天）
    - CS2: 存梁（60天）
    - CS3: 二期恒载（30天）
    - CS4: 徐变十年（3650天）
    - CS5: 运营阶段（0天）
    """
    stage = engine.stage
    
    # CS1: 主梁预制、张拉预应力
    stage.create("CS1_主梁预制、张拉预应力", age=7.0, no=1)
    stage.get(1).add_element(elem_group_names[3], age=7.0)
    stage.get(1).add_boundary(bd_group_names[0])
    stage.get(1).add_boundary(bd_group_names[1])
    stage.get(1).add_loadcase("主梁单元自重")
    stage.get(1).add_loadcase("预应力")
    stage.get(1).add_loadcase("封端混凝土工况")
    
    # CS2: 存梁
    stage.create("CS2_存梁", age=60.0, no=2)
    
    # CS3: 二期恒载
    stage.create("CS3_二期恒载", age=30.0, no=3)
    stage.get(3).add_loadcase("铺装工况")
    stage.get(3).add_loadcase("防撞护栏工况")
    
    # CS4: 徐变十年
    stage.create("CS4_徐变十年", age=3650.0, no=4)
    
    # CS5: 运营阶段
    stage.create("CS5_运营阶段", age=0.0, no=5)
    stage.get(5).add_loadcase("整体升温")
    stage.get(5).add_loadcase("整体降温")
    stage.get(5).add_loadcase("正温度梯度")
    stage.get(5).add_loadcase("负温度梯度")
    stage.get(5).add_analysis("LIVE", "车道荷载包络")


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
