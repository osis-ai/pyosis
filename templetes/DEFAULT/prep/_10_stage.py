"""施工阶段"""

from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:
    """创建施工阶段"""

    stg = engine.stage.create(1, '桥墩施工', 30.0)

    stg.define_element(1, 1, '桥墩', nBirth=7.0, ePart=0)

    stg.define_boundary(1, 1, '墩底固结')

    stg.define_loadcase(1, 1, "", '自重')

    stg = engine.stage.create(2, '现浇_0号块', 37.0)

    stg.define_element(1, 1, '0_号块', nBirth=7.0, ePart=0)

    stg.define_boundary(1, 1, '主墩临时支持')

    stg.define_loadcase(1, 1, "", '预应力1')

    stg.define_loadcase(1, 1, "", '自重1')

    stg = engine.stage.create(3, '安装挂篮1', 2.0)

    stg.define_loadcase(1, 1, "", '挂篮重1')

    stg = engine.stage.create(4, '现浇_1号块', 5.0)

    stg.define_element(1, 1, '1_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重2')

    stg = engine.stage.create(5, '张拉钢束2', 1.0)

    stg.define_loadcase(1, 1, "", '预应力2')

    stg = engine.stage.create(6, '安装挂篮2', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重1')

    stg.define_loadcase(1, 1, "", '挂篮重2')

    stg = engine.stage.create(7, '现浇_2号块', 5.0)

    stg.define_element(1, 1, '2_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重2')

    stg = engine.stage.create(8, '张拉钢束3', 1.0)

    stg.define_loadcase(1, 1, "", '预应力3')

    stg = engine.stage.create(9, '安装挂篮3', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重2')

    stg.define_loadcase(1, 1, "", '挂篮重3')

    stg = engine.stage.create(10, '现浇_3号块', 5.0)

    stg.define_element(1, 1, '3_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重3')

    stg = engine.stage.create(11, '张拉钢束4', 1.0)

    stg.define_loadcase(1, 1, "", '预应力4')

    stg = engine.stage.create(12, '安装挂篮4', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重3')

    stg.define_loadcase(1, 1, "", '挂篮重4')

    stg = engine.stage.create(13, '现浇_4号块', 5.0)

    stg.define_element(1, 1, '4_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重4')

    stg = engine.stage.create(14, '张拉钢束5', 1.0)

    stg.define_loadcase(1, 1, "", '预应力5')

    stg = engine.stage.create(15, '安装挂篮5', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重4')

    stg.define_loadcase(1, 1, "", '挂篮重5')

    stg = engine.stage.create(16, '现浇_5号块', 5.0)

    stg.define_element(1, 1, '5_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重5')

    stg = engine.stage.create(17, '张拉钢束6', 1.0)

    stg.define_loadcase(1, 1, "", '预应力6')

    stg = engine.stage.create(18, '安装挂篮6', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重5')

    stg.define_loadcase(1, 1, "", '挂篮重6')

    stg = engine.stage.create(19, '现浇_6号块', 5.0)

    stg.define_element(1, 1, '6_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重6')

    stg = engine.stage.create(20, '张拉钢束7', 1.0)

    stg.define_loadcase(1, 1, "", '预应力7')

    stg = engine.stage.create(21, '安装挂篮7', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重6')

    stg.define_loadcase(1, 1, "", '挂篮重7')

    stg = engine.stage.create(22, '现浇_7号块', 5.0)

    stg.define_element(1, 1, '7_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重7')

    stg = engine.stage.create(23, '张拉钢束8', 1.0)

    stg.define_loadcase(1, 1, "", '预应力8')

    stg = engine.stage.create(24, '安装挂篮8', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重7')

    stg.define_loadcase(1, 1, "", '挂篮重8')

    stg = engine.stage.create(25, '现浇_8号块', 5.0)

    stg.define_element(1, 1, '8_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重8')

    stg = engine.stage.create(26, '张拉钢束9', 1.0)

    stg.define_loadcase(1, 1, "", '预应力9')

    stg = engine.stage.create(27, '安装挂篮9', 2.0)

    stg.define_loadcase(1, 0, "", '挂篮重8')

    stg.define_loadcase(1, 1, "", '挂篮重9')

    stg = engine.stage.create(28, '现浇_9号块', 5.0)

    stg.define_element(1, 1, '9_号块', nBirth=1.0, ePart=0)

    stg.define_loadcase(1, 1, "", '自重9')

    stg = engine.stage.create(29, '张拉钢束10', 1.0)

    stg.define_loadcase(1, 1, "", '预应力10')

    stg = engine.stage.create(30, '拆除挂篮9', 1.0)

    stg.define_loadcase(1, 0, "", '挂篮重9')

    stg = engine.stage.create(31, '边跨现浇现浇合拢', 10)

    stg.define_element(1, 1, '11_边跨现浇段', nBirth=1, ePart=0)

    stg.define_element(1, 1, '12_边跨合拢段', nBirth=1, ePart=0)

    stg.define_boundary(1, 1, '边墩临时支持')

    stg.define_loadcase(1, 1, "", '边跨预应力1')

    stg.define_loadcase(1, 1, "", '边跨预应力2')

    stg.define_loadcase(1, 1, "", '自重10')

    stg.define_loadcase(1, 1, "", '合拢压重1')

    stg.define_loadcase(1, 1, "", '合拢压重2')

    stg = engine.stage.create(32, '中跨现浇现浇合拢', 10)

    stg.define_element(1, 1, '13_中跨合拢段', nBirth=1, ePart=0)

    stg.define_loadcase(1, 1, "", '自重11')

    stg.define_loadcase(1, 1, "", '中跨预应力1')

    stg.define_loadcase(1, 1, "", '中跨预应力2')

    stg.define_loadcase(1, 0, "", '合拢压重1')

    stg.define_loadcase(1, 0, "", '合拢压重2')

    stg = engine.stage.create(33, '体系转换', 1.0)

    stg.define_boundary(1, 0, '主墩临时支持')

    stg.define_boundary(1, 1, '成桥支座')

    stg = engine.stage.create(34, '二期', 20.0)

    stg.define_loadcase(1, 1, "", '二期1')

    stg = engine.stage.create(35, '成桥20天', 20.0)

    stg = engine.stage.create(36, '成桥十年', 3650.0)

    stg = engine.stage.create(37, '运营', 0.0)

    stg.define_loadcase(1, 1, "", '温度梯度_降')

    stg.define_loadcase(1, 1, "", '整体降温')

    stg.define_loadcase(1, 1, "", '整体升温')

    stg.define_loadcase(1, 1, "", '温度梯度_升')

    stg.define_analysis(1, 'SETL', '支座沉降')

    stg.define_analysis(1, 'LIVE', '移动荷载工况1')



if __name__ == "__main__":
    from ._0_engine import engine
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    bd_groups = engine.boundary.group.all()
    bd_group_names = [bg.name for bg in bd_groups]
    lcs = engine.load.all()
    lc_names = [lc.name for lc in lcs]
    build_stages(engine, elem_group_names, bd_group_names, lc_names, [], [])