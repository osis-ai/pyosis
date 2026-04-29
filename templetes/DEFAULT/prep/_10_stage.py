"""施工阶段"""

from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:
    """施工阶段"""

    # ========== 原始命令流 ==========
    # Stage,1,桥墩施工,30.0;//定义施工阶段名称
    # StgEle,1,1,1,桥墩,7.0,0;//激活单元组，引用单元组名
    # StgBd,1,1,1,墩底固结;//激活边界组，引用边界组名
    # StgLc,1,1,1,,自重;//激活荷载工况，引用荷载工况名
    # Stage,2,现浇_0号块,37.0
    # StgEle,2,1,1,0_号块,7.0,0
    # StgBd,2,1,1,主墩临时支持
    # StgLc,2,1,1,,预应力1
    # StgLc,2,1,1,,自重1
    # Stage,3,安装挂篮1,2.0
    # StgLc,3,1,1,,挂篮重1
    # Stage,4,现浇_1号块,5.0
    # StgEle,4,1,1,1_号块,1.0,0
    # StgLc,4,1,1,,自重2
    # Stage,5,张拉钢束2,1.0
    # StgLc,5,1,1,,预应力2
    # Stage,6,安装挂篮2,2.0
    # StgLc,6,1,0,,挂篮重1
    # StgLc,6,1,1,,挂篮重2
    # Stage,7,现浇_2号块,5.0
    # StgEle,7,1,1,2_号块,1.0,0
    # StgLc,7,1,1,,自重2
    # Stage,8,张拉钢束3,1.0
    # StgLc,8,1,1,,预应力3
    # Stage,9,安装挂篮3,2.0
    # StgLc,9,1,0,,挂篮重2
    # StgLc,9,1,1,,挂篮重3
    # Stage,10,现浇_3号块,5.0
    # StgEle,10,1,1,3_号块,1.0,0
    # StgLc,10,1,1,,自重3
    # Stage,11,张拉钢束4,1.0
    # StgLc,11,1,1,,预应力4
    # Stage,12,安装挂篮4,2.0
    # StgLc,12,1,0,,挂篮重3
    # StgLc,12,1,1,,挂篮重4
    # Stage,13,现浇_4号块,5.0
    # StgEle,13,1,1,4_号块,1.0,0
    # StgLc,13,1,1,,自重4
    # Stage,14,张拉钢束5,1.0
    # StgLc,14,1,1,,预应力5
    # Stage,15,安装挂篮5,2.0
    # StgLc,15,1,0,,挂篮重4
    # StgLc,15,1,1,,挂篮重5
    # Stage,16,现浇_5号块,5.0
    # StgEle,16,1,1,5_号块,1.0,0
    # StgLc,16,1,1,,自重5
    # Stage,17,张拉钢束6,1.0
    # StgLc,17,1,1,,预应力6
    # Stage,18,安装挂篮6,2.0
    # StgLc,18,1,0,,挂篮重5
    # StgLc,18,1,1,,挂篮重6
    # Stage,19,现浇_6号块,5.0
    # StgEle,19,1,1,6_号块,1.0,0
    # StgLc,19,1,1,,自重6
    # Stage,20,张拉钢束7,1.0
    # StgLc,20,1,1,,预应力7
    # Stage,21,安装挂篮7,2.0
    # StgLc,21,1,0,,挂篮重6
    # StgLc,21,1,1,,挂篮重7
    # Stage,22,现浇_7号块,5.0
    # StgEle,22,1,1,7_号块,1.0,0
    # StgLc,22,1,1,,自重7
    # Stage,23,张拉钢束8,1.0
    # StgLc,23,1,1,,预应力8
    # Stage,24,安装挂篮8,2.0
    # StgLc,24,1,0,,挂篮重7
    # StgLc,24,1,1,,挂篮重8
    # Stage,25,现浇_8号块,5.0
    # StgEle,25,1,1,8_号块,1.0,0
    # StgLc,25,1,1,,自重8
    # Stage,26,张拉钢束9,1.0
    # StgLc,26,1,1,,预应力9
    # Stage,27,安装挂篮9,2.0
    # StgLc,27,1,0,,挂篮重8
    # StgLc,27,1,1,,挂篮重9
    # Stage,28,现浇_9号块,5.0
    # StgEle,28,1,1,9_号块,1.0,0
    # StgLc,28,1,1,,自重9
    # Stage,29,张拉钢束10,1.0
    # StgLc,29,1,1,,预应力10
    # Stage,30,拆除挂篮9,1.0
    # StgLc,30,1,0,,挂篮重9
    # Stage,31,边跨现浇现浇合拢,10
    # StgEle,31,1,1,11_边跨现浇段,1,0
    # StgEle,31,1,1,12_边跨合拢段,1,0
    # StgBd,31,1,1,边墩临时支持
    # StgLc,31,1,1,,边跨预应力1
    # StgLc,31,1,1,,边跨预应力2
    # StgLc,31,1,1,,自重10
    # StgLc,31,1,1,,合拢压重1
    # StgLc,31,1,1,,合拢压重2
    # Stage,32,中跨现浇现浇合拢,10
    # StgEle,32,1,1,13_中跨合拢段,1,0
    # StgLc,32,1,1,,自重11
    # StgLc,32,1,1,,中跨预应力1
    # StgLc,32,1,1,,中跨预应力2
    # StgLc,32,1,0,,合拢压重1
    # StgLc,32,1,0,,合拢压重2
    # Stage,33,体系转换,1.0
    # StgBd,33,1,0,主墩临时支持
    # StgBd,33,1,1,成桥支座
    # Stage,34,二期,20.0
    # StgLc,34,1,1,,二期1
    # Stage,35,成桥20天,20.0
    # Stage,36,成桥十年,3650.0
    # Stage,37,运营,0.0
    # StgLc,37,1,1,,温度梯度_降
    # StgLc,37,1,1,,整体降温
    # StgLc,37,1,1,,整体升温
    # StgLc,37,1,1,,温度梯度_升
    # StgAnal,37,1,SETL,支座沉降;//激活沉降分析，引用沉降工况名
    # StgAnal,37,1,LIVE,移动荷载工况1;//激活移动荷载分析，引用移动荷载工况名

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