from pyosis.core.engine import OSISEngine

def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:
    """创建荷载工况和钢束，返回荷载工况名称列表
    
    荷载工况名称：
    - "防撞护栏工况": 防撞护栏（CS）
    - "封端混凝土工况": 封端混凝土（CS）
    - "负温度梯度": 负温度梯度（TG）
    - "铺装工况": 铺装（CS）
    - "预应力": 预应力（CS）
    - "整体降温": 整体降温（T）
    - "整体升温": 整体升温（T）
    - "正温度梯度": 正温度梯度（TG）
    - "主梁单元自重": 主梁单元自重（CS）
    """
    tendon = engine.tendon
    loadcase = engine.load
    
    # ── 钢束特性──
    tendon.prop.create_in("15-10", mat_nos[2], "GBT5224_2014", 15.2, 10, 9.0000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    tendon.prop.create_in("15-3",  mat_nos[2], "GBT5224_2014", 15.2, 3,  5.5000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    tendon.prop.create_in("15-4",  mat_nos[2], "GBT5224_2014", 15.2, 4,  5.5000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    tendon.prop.create_in("15-5",  mat_nos[2], "GBT5224_2014", 15.2, 5,  5.5000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    tendon.prop.create_in("15-6",  mat_nos[2], "GBT5224_2014", 15.2, 6,  7.0000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    tendon.prop.create_in("15-7",  mat_nos[2], "GBT5224_2014", 15.2, 7,  7.0000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    tendon.prop.create_in("15-8",  mat_nos[2], "GBT5224_2014", 15.2, 8,  7.0000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    tendon.prop.create_in("15-9",  mat_nos[2], "GBT5224_2014", 15.2, 9,  9.0000E-02, 1.7000E-01, 1.5000E-03, 6.0000E-03, 6.0000E-03, 1.0000E+00, 3.0000E-01)
    
    tendon_geo1, tendon_geo2 = geo_names
    _, tendon_eg_1, tendon_eg_2, _ = elem_group_names
    # 钢束形状（名称标识）
    shape1 = tendon.shape.create_arc3d("N1", 2, "15-4", tendon_eg_1, tendon_geo1)
    shape2 = tendon.shape.create_arc3d("N2", 2, "15-4", tendon_eg_2, tendon_geo2)
    
    # 布置钢束
    shape1.layout("ELEMENT", 1, 0, 0, 0.0, 0.0, 0.0)
    shape2.layout("ELEMENT", 1, 0, 0, 0.0, 0.0, 0.0)
    
    
    # ── 荷载工况──
    # 1: 防撞护栏工况（CS）
    lc_barrier = loadcase.create("防撞护栏工况", "CS")
    for e in elem_nos:
        lc_barrier.create_line_load(
            e, 0, 0, 
            0.0, 0.0, 0.0, 0.0, 0.0, -2.1200E+03, 0.0, 0.0, 0.0,
            1.0, 0.0, 0.0, 0.0, 0.0, -2.1200E+03, 0.0, 0.0, 0.0,
        )
    
    # 2: 封端混凝土工况（CS）
    lc_end_conc = loadcase.create("封端混凝土工况", "CS")
    lc_end_conc.create_line_load(
        elem_nos[0], 0, 0, 
        0.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
    )
    lc_end_conc.create_line_load(
        elem_nos[13], 0, 0, 
        0.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 0.0, 0.0, -4.4900E+03, 0.0, 0.0, 0.0,
    )
    
    # 3: 负温度梯度（TG）
    lc_neg_temp = loadcase.create("负温度梯度", "TG")
    lc_neg_temp.create_gradient_temperature(elem_nos[0],  "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[1],  "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[2],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[3],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[4],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[5],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[6],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[7],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[8],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[9],  "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[10], "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.454, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[11], "Z", "T", 2, [1.113, 0.000, -7.000, -0.100, -2.750, 0.603, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[12], "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    lc_neg_temp.create_gradient_temperature(elem_nos[13], "Z", "T", 2, [1.240, 0.000, -7.000, -0.100, -2.750, 0.721, -0.100, -2.750, -0.400, 0.000])
    
    # 4: 铺装工况（CS）
    lc_pavement = loadcase.create("铺装工况", "CS")
    for e in elem_nos:
        lc_pavement.create_line_load(
            e, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0850E+04, 0.0, 0.0, 0.0,
            1.0, 0.0, 0.0, 0.0, 0.0, -1.0850E+04, 0.0, 0.0, 0.0,
        )
    
    # 5: 预应力（CS）
    lc_pst = loadcase.create("预应力", "CS")
    lc_pst.create_prestress(shape1.name, "BOTH", "ST", 1.395000E+09, 1.395000E+09)
    lc_pst.create_prestress(shape2.name, "BOTH", "ST", 1.395000E+09, 1.395000E+09)
    
    # 6: 整体降温（T）
    lc_temp_drop = loadcase.create("整体降温", "T")
    for e in elem_nos:
        lc_temp_drop.create_uniform_temperature(e, "X", -20.000)
    
    # 7: 整体升温（T）
    lc_temp_rise = loadcase.create("整体升温", "T")
    for e in elem_nos:
        lc_temp_rise.create_uniform_temperature(e, "X", 20.000)
    
    # 8: 正温度梯度（TG）
    lc_pos_temp = loadcase.create("正温度梯度", "TG")
    lc_pos_temp.create_gradient_temperature(elem_nos[0],  "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[1],  "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[2],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[3],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[4],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[5],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[6],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[7],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[8],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[9],  "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[10], "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.454, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[11], "Z", "T", 2, [1.113, 0.000, 14.000, -0.100, 5.500, 0.603, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[12], "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    lc_pos_temp.create_gradient_temperature(elem_nos[13], "Z", "T", 2, [1.240, 0.000, 14.000, -0.100, 5.500, 0.721, -0.100, 5.500, -0.400, 0.000])
    
    # 9: 主梁单元自重（CS）
    lc_dead = loadcase.create("主梁单元自重", "CS")
    lc_dead.create_gravity(0.0, 0.0, -1.000)
    
    return [
        lc_barrier.name, lc_end_conc.name, lc_neg_temp.name,
        lc_pavement.name, lc_pst.name, lc_temp_drop.name,
        lc_temp_rise.name, lc_pos_temp.name, lc_dead.name,
    ]

if __name__ == "__main__":
    from ._0_engine import engine
    
    # 从 engine 获取已有数据
    mats = engine.material.all()
    print("materials: ", mats)
    mat_nos = [m.no for m in mats]
    elems = engine.element.all()
    print("elements: ", elems)
    elem_nos = [e.no for e in elems]
    elem_groups = engine.element.group.all()
    print("element groups: ", elem_groups)
    elem_group_names = [eg.name for eg in elem_groups]
    
    # print("geometrys: ", geoms)
    geo_names = ["钢束-1-N1", "钢束-2-N2"]  # 几何名称固定
    
    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)
    print(lc_names)
    print(engine.load.all())
