"""
GUI 模式端到端 demo（xiaoxiangliang.out 生成的模型，合并为单文件）。

需要 OSIS 5.1+ GUI 已启动；脚本会自动清空当前工程再重建。
整段建模包在 with batch(): 内，一次 OSIS_Run 完成约 250 条命令。

用法：
    python tests/demo_gui.py             # 仅建模
    python tests/demo_gui.py --solve     # 建模后求解
"""

from pyosis import batch

# ----- _0_engine.py -----
from pyosis.core.engine import OSISEngine

engine = OSISEngine()

# 自动打开OSIS等操作暂未实现
# 目前需要手动打开OSIS并创建项目

# ----- _1_control.py -----
"""全局控制参数"""

from pyosis.core.engine import OSISEngine

def setup_control(engine: OSISEngine) -> None:
    """设置全局控制参数"""

    engine.control.set_gravity_acceleration(9.8066)
    engine.control.set_calc_tendon(True)
    engine.control.set_calc_concurrent_force(True)
    engine.control.set_calc_shrink(True)
    engine.control.set_calc_creep(True)
    engine.control.set_calc_shear(True)
    engine.control.set_calc_relaxation(True)
    engine.control.set_mod_loc_coor(False)
    engine.control.set_calc_rebar_gravity(False)
    engine.control.set_inc_rebar(True)
    engine.control.set_inc_tendon(True)
    engine.control.set_nonlinear(geom=False, link=False)
    engine.control.set_line_search(False)
    engine.control.set_auto_time_step(False)
    engine.control.set_substitution_steps(1, 20)
    engine.control.set_modal_opt(0)# ----- _2_property.py -----
"""几何属性"""

from pyosis.core.engine import OSISEngine

def build_property(engine: OSISEngine) -> list[str]:
    """设置几何属性（钢束线型、车道线等）"""

    geo_names = []

    spline = engine.geometry.create_arc3d('钢束-1-N1', 'TENDON', [0.16, 0, -0.3, 0, 6.90373, 0, -0.89, 30, 13.0163, 0, -0.89, 30, 19.76, 0, -0.3, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束-2-N2', 'TENDON', [0.16, 0, -0.55, 0, 5.30352, 0, -1, 30, 14.6165, 0, -1, 30, 19.76, 0, -0.55, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束-3-N3', 'TENDON', [0.16, 0, -0.8, 0, 3.70332, 0, -1.11, 30, 16.2167, 0, -1.11, 30, 19.76, 0, -0.8, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束-4-N4', 'TENDON', [0.16, 0, -1.045, 0, 2.02136, 0, -1.11, 30, 17.8986, 0, -1.11, 30, 19.76, 0, -1.045, 0])
    geo_names.append(spline.name)

    return geo_names# ----- _3_material.py -----
"""材料"""

from pyosis.core.engine import OSISEngine

def build_materials(engine: OSISEngine) -> list[int]:
    """创建材料，返回材料编号列表"""

    mat_nos = []

    engine.prop.creep_shrink.create(
        no=1, name='收缩徐变', avg_humidity=75.00,
        birth_time=7, type_coeff=5.000, shrink_birth=3
    )

    mat = engine.material.create_conc(
        no=1, name='C50', code='JTG3362_2018', grade='C50',
        crep_shrk=1, dmp=0.050
    )
    mat_nos.append(mat.no)

    mat = engine.material.create_rebar(
        no=2, name='HRB400', code='JTG3362_2018', grade='HRB400', dmp=0.050
    )
    mat_nos.append(mat.no)

    mat = engine.material.create_prestressed(
        no=3, name='钢绞线-1860', code='JTG3362_2018', grade='Strand1860', dmp=0.050
    )
    mat_nos.append(mat.no)

    return mat_nos# ----- _4_section.py -----
"""截面"""

from pyosis.core.engine import OSISEngine

def build_sections(engine: OSISEngine) -> list[int]:
    """创建截面，返回截面编号列表"""

    sec_nos = []

    sec = engine.section.create_smallbox(
        1, '标准截面', 'Middle', 1.2,
        1.65, 1.2, 0, 1,
        0.18, 0.2, 0.2, 4,
        0.18, 0.25, 0.2, 0.15,
        0.25, 0.05, 0.05, 0,
        0, 0, 0.05,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000, part_id=1
    )

    sec = engine.section.create_smallbox(
        2, '墩顶截面', 'Middle', 1.2,
        1.65, 1.2, 0, 1,
        0.18, 0.3, 0.3, 4,
        0.18, 0.25, 0.2, 0.15,
        0.25, 0.05, 0.05, 0,
        0, 0, 0.05,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000, part_id=1
    )

    sec = engine.section.create_smallbox(
        3, '加厚截面', 'Middle', 1.2,
        1.65, 1.2, 0, 1,
        0.18, 0.3, 0.3, 4,
        0.18, 0.25, 0.2, 0.15,
        0.25, 0.05, 0.05, 0,
        0, 0, 0.05,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000, part_id=1
    )

    sec = engine.section.create_smallbox(
        4, '墩顶截面', 'Middle', 1.2,
        1.65, 1.2, 0, 1,
        0.18, 0.3, 0.3, 4,
        0.18, 0.25, 0.2, 0.15,
        0.25, 0.05, 0.05, 0,
        0, 0, 0.05,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000, part_id=1
    )

    sec = engine.section.create_smallbox(
        5, '加厚截面', 'Middle', 1.2,
        1.65, 1.2, 0, 1,
        0.18, 0.3, 0.3, 4,
        0.18, 0.25, 0.2, 0.15,
        0.25, 0.05, 0.05, 0,
        0, 0, 0.05,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000, part_id=1
    )

    sec = engine.section.create_smallbox(
        6, '墩顶截面', 'Middle', 1.2,
        1.65, 1.2, 0, 1,
        0.18, 0.3, 0.3, 4,
        0.18, 0.25, 0.2, 0.15,
        0.25, 0.05, 0.05, 0,
        0, 0, 0.05,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000, part_id=1
    )

    sec = engine.section.create_smallbox(
        7, '加厚截面', 'Middle', 1.2,
        1.65, 1.2, 0, 1,
        0.18, 0.3, 0.3, 4,
        0.18, 0.25, 0.2, 0.15,
        0.25, 0.05, 0.05, 0,
        0, 0, 0.05,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000, part_id=1
    )

    return sec_nos# ----- _5_node.py -----
"""节点"""

from pyosis.core.engine import OSISEngine

def build_nodes(engine: OSISEngine) -> list[int]:
    """创建节点，返回节点编号列表"""

    node_nos = []

    n = engine.node.create(1, 0.0400, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(2, 0.4500, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(3, 0.8400, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(4, 2.8400, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(5, 4.0000, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(6, 6.0000, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(7, 8.0000, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(8, 10.0000, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(9, 12.0000, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(10, 14.0000, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(11, 16.0000, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(12, 17.1600, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(13, 19.1600, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(14, 19.5500, 0.0000, 0.0000)
    node_nos.append(n.no)

    n = engine.node.create(15, 19.9600, 0.0000, 0.0000)
    node_nos.append(n.no)

    return node_nos# ----- _6_element.py -----
"""单元"""

from pyosis.core.engine import OSISEngine

def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:
    """创建单元，返回单元编号列表和单元组名称列表"""

    elem_nos = []
    elem_group_names = []

    e = engine.element.create_beam3d(1, 1, 2, 1, 6, 6, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(2, 2, 3, 1, 6, 6, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(3, 3, 4, 1, 7, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(4, 4, 5, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(5, 5, 6, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(6, 6, 7, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(7, 7, 8, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(8, 8, 9, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(9, 9, 10, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(10, 10, 11, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(11, 11, 12, 1, 1, 1, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(12, 12, 13, 1, 1, 7, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(13, 13, 14, 1, 6, 6, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(14, 14, 15, 1, 6, 6, 1, 1, 0, 0, 0, 0)
    elem_nos.append(e.no)

    engine.prop.assign_component_thickness(2.399E-01, 'a', '4to11')

    engine.prop.assign_component_thickness(3.022E-01, 'a', '1to2', '13to14')

    engine.prop.assign_component_thickness(2.710E-01, 'a', 3, 12)

    eg = engine.element.group.create('主梁单元', 'c')
    elem_group_names.append(eg.name)

    eg.add('1to14')

    eg = engine.element.group.create('钢束-1-N1线型单元', 'c')
    elem_group_names.append(eg.name)

    eg.add('1to14')

    eg = engine.element.group.create('钢束-2-N2线型单元', 'c')
    elem_group_names.append(eg.name)

    eg.add('1to14')

    eg = engine.element.group.create('钢束-3-N3线型单元', 'c')
    elem_group_names.append(eg.name)

    eg.add('1to14')

    eg = engine.element.group.create('钢束-4-N4线型单元', 'c')
    elem_group_names.append(eg.name)

    eg.add('1to14')

    return elem_nos, elem_group_names# ----- _7_boundary.py -----
"""边界条件"""

from pyosis.core.engine import OSISEngine

def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:
    """创建边界条件，返回边界编号列表和边界组名称列表"""

    bd_nos = []
    bd_group_names = []

    bd = engine.boundary.create_general(coor="", ry=0, rw=0, no=1)
    bd_nos.append(bd.no)

    bd.assign('a', [2])

    bd = engine.boundary.create_general(coor="", x=0, ry=0, rw=0, no=2)
    bd_nos.append(bd.no)

    bd.assign('a', [14])

    bg = engine.boundary.group.create('桥台1_永久_x向固定', 'c')
    bd_group_names.append(bg.name)

    bg.add(1)

    bg = engine.boundary.group.create('桥台2_永久_x向滑动', 'c')
    bd_group_names.append(bg.name)

    bg.add(2)

    return bd_nos, bd_group_names# ----- _8_loadcase.py -----
"""荷载工况"""

from pyosis.core.engine import OSISEngine

def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:
    """创建荷载工况和钢束，返回荷载工况名称列表"""

    lc_names = []

    engine.tendon.prop.create_in('15-10', mat=3, code='GBT5224_2014', diameter=15.2, num=10, pipe=9.0000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in('15-3', mat=3, code='GBT5224_2014', diameter=15.2, num=3, pipe=5.5000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in('15-4', mat=3, code='GBT5224_2014', diameter=15.2, num=4, pipe=5.5000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in('15-5', mat=3, code='GBT5224_2014', diameter=15.2, num=5, pipe=5.5000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in('15-6', mat=3, code='GBT5224_2014', diameter=15.2, num=6, pipe=7.0000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in('15-7', mat=3, code='GBT5224_2014', diameter=15.2, num=7, pipe=7.0000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in('15-8', mat=3, code='GBT5224_2014', diameter=15.2, num=8, pipe=7.0000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in('15-9', mat=3, code='GBT5224_2014', diameter=15.2, num=9, pipe=9.0000E-02, friction_coeff=1.7000E-01, deviation_coeff=1.5000E-03, starting_deform=6.0000E-03, end_deform=6.0000E-03, tensioning_coeff=1.0000E+00, relaxation_coeff=3.0000E-01)

    shape = engine.tendon.shape.create_arc3d('N1', n_num=2, prop='15-4', element_group='钢束-1-N1线型单元', curve_name='钢束-1-N1')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('N2', n_num=2, prop='15-4', element_group='钢束-2-N2线型单元', curve_name='钢束-2-N2')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('N3', n_num=2, prop='15-5', element_group='钢束-3-N3线型单元', curve_name='钢束-3-N3')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('N4', n_num=2, prop='15-5', element_group='钢束-4-N4线型单元', curve_name='钢束-4-N4')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    lc = engine.load.create('主梁单元自重', load_case_type='CS', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('整体升温', load_case_type='T', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_uniform_temperature(1, direct='X', temp=20.000)

    lc.create_uniform_temperature(2, direct='X', temp=20.000)

    lc.create_uniform_temperature(3, direct='X', temp=20.000)

    lc.create_uniform_temperature(4, direct='X', temp=20.000)

    lc.create_uniform_temperature(5, direct='X', temp=20.000)

    lc.create_uniform_temperature(6, direct='X', temp=20.000)

    lc.create_uniform_temperature(7, direct='X', temp=20.000)

    lc.create_uniform_temperature(8, direct='X', temp=20.000)

    lc.create_uniform_temperature(9, direct='X', temp=20.000)

    lc.create_uniform_temperature(10, direct='X', temp=20.000)

    lc.create_uniform_temperature(11, direct='X', temp=20.000)

    lc.create_uniform_temperature(12, direct='X', temp=20.000)

    lc.create_uniform_temperature(13, direct='X', temp=20.000)

    lc.create_uniform_temperature(14, direct='X', temp=20.000)

    lc = engine.load.create('整体降温', load_case_type='T', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_uniform_temperature(1, direct='X', temp=-20.000)

    lc.create_uniform_temperature(2, direct='X', temp=-20.000)

    lc.create_uniform_temperature(3, direct='X', temp=-20.000)

    lc.create_uniform_temperature(4, direct='X', temp=-20.000)

    lc.create_uniform_temperature(5, direct='X', temp=-20.000)

    lc.create_uniform_temperature(6, direct='X', temp=-20.000)

    lc.create_uniform_temperature(7, direct='X', temp=-20.000)

    lc.create_uniform_temperature(8, direct='X', temp=-20.000)

    lc.create_uniform_temperature(9, direct='X', temp=-20.000)

    lc.create_uniform_temperature(10, direct='X', temp=-20.000)

    lc.create_uniform_temperature(11, direct='X', temp=-20.000)

    lc.create_uniform_temperature(12, direct='X', temp=-20.000)

    lc.create_uniform_temperature(13, direct='X', temp=-20.000)

    lc.create_uniform_temperature(14, direct='X', temp=-20.000)

    lc = engine.load.create('正温度梯度', load_case_type='TG', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_gradient_temperature(1, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.165, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(2, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.165, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(3, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(4, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(5, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(6, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(7, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(8, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(9, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(10, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(11, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.018, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(12, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.165, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(13, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.165, -0.1, 5.5, -0.4, 0)

    lc.create_gradient_temperature(14, 'Z', 'T', 2, 2.4, 0, 14, -0.1, 5.5, 1.165, -0.1, 5.5, -0.4, 0)

    lc = engine.load.create('端横梁荷载工况', load_case_type='CS', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_nforce(2, 0.0000E+00, 0.0000E+00, -2.0030E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(14, 0.0000E+00, 0.0000E+00, -2.0030E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('负温度梯度', load_case_type='TG', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_gradient_temperature(1, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.165, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(2, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.165, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(3, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(4, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(5, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(6, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(7, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(8, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(9, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(10, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(11, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.018, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(12, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.165, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(13, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.165, -0.1, -2.75, -0.4, 0)

    lc.create_gradient_temperature(14, 'Z', 'T', 2, 2.4, 0, -7, -0.1, -2.75, 1.165, -0.1, -2.75, -0.4, 0)

    lc = engine.load.create('铺装工况', load_case_type='CS', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_line_load(entity=1, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=2, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=3, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=4, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=5, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=6, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=7, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=8, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=9, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=10, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=11, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=12, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=13, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=14, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-1.0850E+04, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-1.0850E+04, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc = engine.load.create('防撞护栏工况', load_case_type='CS', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_line_load(entity=1, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=2, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=3, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=4, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=5, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=6, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=7, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=8, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=9, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=10, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=11, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=12, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=13, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc.create_line_load(entity=14, coord_system=0, load_type=0, offset_x_i=0.000, offset_y_i=0.000, offset_z_i=0.000, fx_i=0.0000E+00, fy_i=0.0000E+00, fz_i=-2.1200E+03, mx_i=0.0000E+00, my_i=0.0000E+00, mz_i=0.0000E+00, offset_x_j=1.000, offset_y_j=0.000, offset_z_j=0.000, fx_j=0.0000E+00, fy_j=0.0000E+00, fz_j=-2.1200E+03, mx_j=0.0000E+00, my_j=0.0000E+00, mz_j=0.0000E+00)

    lc = engine.load.create('预应力', load_case_type='CS', scalar=1.00000)
    lc_names.append(lc.name)

    lc.create_prestress('N1', tension_type='BOTH', tension_force_type='ST', beg=1.395000E+09, end=1.395000E+09)

    lc.create_prestress('N2', tension_type='BOTH', tension_force_type='ST', beg=1.395000E+09, end=1.395000E+09)

    lc.create_prestress('N3', tension_type='BOTH', tension_force_type='ST', beg=1.395000E+09, end=1.395000E+09)

    lc.create_prestress('N4', tension_type='BOTH', tension_force_type='ST', beg=1.395000E+09, end=1.395000E+09)

    return lc_names# ----- _9_analysis.py -----
"""分析设置"""

from pyosis.core.engine import OSISEngine

def build_analysis(engine: OSISEngine, node_nos: list[int], elem_group_names: list[str]) -> tuple[list[str], list[str]]:
    """创建沉降分析和活载分析，返回(沉降工况名列表, 活载工况名列表)"""

    settle_names = []
    live_names = []

    engine.live.grade.create_highway('简支小箱梁移动荷载', code='JTGD60_2015', live_load_type='HIGHWAY_I')

    engine.live.lane.create_ve('车道', length=19.1000, wheel=1.80, orientation=1, ref=0, ref_elems='主梁单元', offset_y=0.00000E+00, offset_z=0.00000E+00)

    lc = engine.live.case.create('车道荷载包络', code='JTGD60_2015', sub_cmb_type=1)
    live_names.append(lc.name)

    lc.set_trans_reduction_factors([1.2000, 1.0000, 0.7800, 0.6700, 0.6000, 0.5500, 0.5200, 0.5000, 0.5000, 0.5000])

    lc.create_sub('车道荷载工况1', '简支小箱梁移动荷载', scalar=0.75000, calc_mu=True, bridge_type='CUSTOM', mu_params=[6.586960], lane_names=['车道'])

    lc.set_lane_count('车道荷载工况1', 0, 1)

    return settle_names, live_names# ----- _10_stage.py -----
"""施工阶段"""

from pyosis.core.engine import OSISEngine

def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:
    """创建施工阶段"""

    stg = engine.stage.create(1, 'CS1_主梁预制、张拉预应力', 7.0)

    stg.define_element(1, 1, '主梁单元', birth=7.0, part=0)

    stg.define_boundary(1, 1, '桥台1_永久_x向固定')

    stg.define_boundary(1, 1, '桥台2_永久_x向滑动')

    stg.define_loadcase(1, 1, "", '主梁单元自重')

    stg.define_loadcase(1, 1, "", '预应力')

    stg.define_loadcase(1, 1, "", '端横梁荷载工况')

    stg = engine.stage.create(2, 'CS2_存梁', 60.0)

    stg = engine.stage.create(3, 'CS3_二期恒载', 30.0)

    stg.define_loadcase(1, 1, "", '铺装工况')

    stg.define_loadcase(1, 1, "", '防撞护栏工况')

    stg = engine.stage.create(4, 'CS4_徐变十年', 3650.0)

    stg = engine.stage.create(5, 'CS5_运营阶段', 0.0)

    stg.define_loadcase(1, 1, "", '整体升温')

    stg.define_loadcase(1, 1, "", '整体降温')

    stg.define_loadcase(1, 1, "", '正温度梯度')

    stg.define_loadcase(1, 1, "", '负温度梯度')

    stg.define_analysis(1, 'LIVE', '车道荷载包络')

def build_model() -> "OSISEngine":
    """按 1-10 步建模（清空 + 全 batch）。所有命令在 with 退出时一次性发送。"""
    print("清空项目...")
    print("=" * 50)
    print("开始建模")
    print("=" * 50)

    with batch():
        # 0. 清空
        engine.clear()
        engine.clc()

        # 1. 控制
        print("\n[1/10] 控制参数")
        setup_control(engine)

        # 2. 几何
        print("[2/10] 几何")
        geo_names = build_property(engine)

        # 3. 材料
        print("[3/10] 材料")
        mat_nos = build_materials(engine)

        # 4. 截面
        print("[4/10] 截面")
        sec_nos = build_sections(engine)

        # 5. 节点
        print("[5/10] 节点")
        node_nos = build_nodes(engine)

        # 6. 单元
        print("[6/10] 单元")
        elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)

        # 7. 边界
        print("[7/10] 边界")
        bd_nos, bd_group_names = build_boundaries(engine, node_nos)

        # 8. 荷载工况
        print("[8/10] 荷载工况")
        lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)

        # 9. 分析设置
        print("[9/10] 分析设置")
        settle_names, live_names = build_analysis(engine, node_nos, elem_group_names)

        # 10. 施工阶段
        print("[10/10] 施工阶段")
        build_stages(engine, elem_group_names, bd_group_names, lc_names, settle_names, live_names)

    print("\n" + "=" * 50)
    print("建模完成")
    print("=" * 50)
    print("提示: 调用 engine.solve() 求解")
    return engine


if __name__ == "__main__":
    engine = build_model()
