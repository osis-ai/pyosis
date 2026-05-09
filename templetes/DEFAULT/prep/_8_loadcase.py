"""荷载工况"""

from pyosis.core.engine import OSISEngine

def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:
    """创建荷载工况和钢束，返回荷载工况名称列表"""

    lc_names = []

    engine.tendon.prop.create_in('15-19', n_mat=2, e_code='GBT5224_2014', diameter=15.2, n_num=19, d_pipe=1.0000E-01, d_friction_coeff=1.7000E-01, d_deviation_coeff=1.5000E-03, d_starting_deform=6.0000E-03, d_end_deform=6.0000E-03, d_tensioning_coeff=1.0000E+00, d_relaxation_coeff=3.0000E-01)

    shape = engine.tendon.shape.create_arc3d('BD1-1', n_num=2, prop='15-19', element_group='BD刚束单元组1', curve_name='BD1')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BD1-2', n_num=2, prop='15-19', element_group='右侧_BD刚束单元组1', curve_name='BD1')

    shape.layout('ELEMENT', 58, 1, 1, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BD2-1', n_num=2, prop='15-19', element_group='BD刚束单元组2', curve_name='BD2')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BD2-2', n_num=2, prop='15-19', element_group='右侧_BD刚束单元组2', curve_name='BD2')

    shape.layout('ELEMENT', 58, 1, 1, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BD3-1', n_num=2, prop='15-19', element_group='BD刚束单元组3', curve_name='BD3')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BD3-2', n_num=2, prop='15-19', element_group='右侧_BD刚束单元组3', curve_name='BD3')

    shape.layout('ELEMENT', 58, 1, 1, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BT1-1', n_num=2, prop='15-19', element_group='BT刚束单元组1', curve_name='BT1')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BT1-2', n_num=2, prop='15-19', element_group='右侧_BT刚束单元组1', curve_name='BT1')

    shape.layout('ELEMENT', 58, 1, 1, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BT2-1', n_num=2, prop='15-19', element_group='BT刚束单元组2', curve_name='BT2')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BT2-2', n_num=2, prop='15-19', element_group='右侧_BT刚束单元组2', curve_name='BT2')

    shape.layout('ELEMENT', 58, 1, 1, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BT3-1', n_num=2, prop='15-19', element_group='BT刚束单元组3', curve_name='BT3')

    shape.layout('ELEMENT', 1, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('BT3-2', n_num=2, prop='15-19', element_group='右侧_BT刚束单元组3', curve_name='BT3')

    shape.layout('ELEMENT', 58, 1, 1, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F0-1', n_num=2, prop='15-19', element_group='钢束单元组F0', curve_name='F0')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F0-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F0', curve_name='F0')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F1-1', n_num=2, prop='15-19', element_group='钢束单元组F1', curve_name='F1')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F1-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F1', curve_name='F1')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F2-1', n_num=2, prop='15-19', element_group='钢束单元组F2', curve_name='F2')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F2-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F2', curve_name='F2')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F3-1', n_num=2, prop='15-19', element_group='钢束单元组F3', curve_name='F3')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F3-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F3', curve_name='F3')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F4-1', n_num=2, prop='15-19', element_group='钢束单元组F4', curve_name='F4')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F4-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F4', curve_name='F4')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F5-1', n_num=2, prop='15-19', element_group='钢束单元组F5', curve_name='F5')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F5-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F5', curve_name='F5')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F6-1', n_num=2, prop='15-19', element_group='钢束单元组F6', curve_name='F6')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F6-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F6', curve_name='F6')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F7-1', n_num=2, prop='15-19', element_group='钢束单元组F7', curve_name='F7')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F7-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F7', curve_name='F7')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F8-1', n_num=2, prop='15-19', element_group='钢束单元组F8', curve_name='F8')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('F8-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F8', curve_name='F8')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T0-1', n_num=2, prop='15-19', element_group='钢束单元组F0', curve_name='T0')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T0-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F0', curve_name='T0')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T1-1', n_num=2, prop='15-19', element_group='钢束单元组F1', curve_name='T1')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T1-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F1', curve_name='T1')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T2-1', n_num=2, prop='15-19', element_group='钢束单元组F2', curve_name='T2')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T2-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F2', curve_name='T2')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T3-1', n_num=2, prop='15-19', element_group='钢束单元组F3', curve_name='T3')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T3-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F3', curve_name='T3')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T4-1', n_num=2, prop='15-19', element_group='钢束单元组F4', curve_name='T4')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T4-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F4', curve_name='T4')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T5-1', n_num=2, prop='15-19', element_group='钢束单元组F5', curve_name='T5')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T5-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F5', curve_name='T5')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T6-1', n_num=2, prop='15-19', element_group='钢束单元组F6', curve_name='T6')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T6-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F6', curve_name='T6')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T7-1', n_num=2, prop='15-19', element_group='钢束单元组F7', curve_name='T7')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T7-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F7', curve_name='T7')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T8-1', n_num=2, prop='15-19', element_group='钢束单元组F8', curve_name='T8')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T8-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F8', curve_name='T8')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T9-1', n_num=2, prop='15-19', element_group='钢束单元组F9', curve_name='T9')

    shape.layout('ELEMENT', 17, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('T9-2', n_num=2, prop='15-19', element_group='右侧_钢束单元组F9', curve_name='T9')

    shape.layout('ELEMENT', 43, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z1-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组1', curve_name='Z1')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z2-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组2', curve_name='Z2')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z3-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组3', curve_name='Z3')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z4-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组4', curve_name='Z4')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z5-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组5', curve_name='Z5')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z6-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组6', curve_name='Z6')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z7-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组7', curve_name='Z7')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('Z8-1', n_num=2, prop='15-19', element_group='跨中底板刚束单元组8', curve_name='Z8')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    shape = engine.tendon.shape.create_arc3d('ZT-1', n_num=2, prop='15-19', element_group='ZT刚束单元组', curve_name='ZT')

    shape.layout('ELEMENT', 29, 0, 0, 0.000000E+00, 0.000000E+00, 0.000000E+00)

    lc = engine.load.create('边跨预应力1', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('BD1-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BD2-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BD3-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BT1-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BT2-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BT3-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('边跨预应力2', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('BD1-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BD2-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BD3-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BT1-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BT2-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('BT3-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('二期1', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(1, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(2, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(3, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(4, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(5, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(6, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(7, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(8, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(9, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(10, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(11, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(12, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(13, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(14, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(15, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(16, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(17, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(18, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(19, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(20, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(21, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(22, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(23, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(24, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(25, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(26, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(27, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(28, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(29, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(30, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(31, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(32, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(33, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(34, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(35, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(36, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(37, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(38, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(39, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(40, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(41, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(42, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(43, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(44, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(45, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(46, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(47, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(48, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(49, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(50, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(51, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(52, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(53, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(54, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(55, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(56, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(57, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(58, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(59, 0.0000E+00, 0.0000E+00, -8.1670E+04, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重1', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(14, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(20, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(40, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(46, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重10', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc = engine.load.create('挂篮重11', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc = engine.load.create('挂篮重12', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc = engine.load.create('挂篮重13', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc = engine.load.create('挂篮重2', load_case_type='USER', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(13, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(21, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(39, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(47, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重3', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(12, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(22, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(38, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(48, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重4', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(11, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(23, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(37, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(49, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重5', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(10, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(24, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(36, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(50, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重6', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(9, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(25, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(35, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(51, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重7', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(8, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(26, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(34, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(52, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重8', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(7, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(27, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(33, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(53, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('挂篮重9', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(6, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(28, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(32, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(54, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('合拢压重1', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(5, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(55, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('合拢压重2', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_nforce(29, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc.create_nforce(31, 0.0000E+00, 0.0000E+00, -4.5000E+05, 0.0000E+00, 0.0000E+00, 0.0000E+00)

    lc = engine.load.create('合拢压重3', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc = engine.load.create('温度梯度_降', load_case_type='TG', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gradient_temperature(1, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(2, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(3, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(4, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(5, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(6, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(7, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(8, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(9, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(10, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(11, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(12, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(13, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(14, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(15, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(16, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(17, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(18, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(19, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(20, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(21, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(22, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(23, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(24, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(25, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(26, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(27, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(28, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(29, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(30, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(31, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(32, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(33, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(34, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(35, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(36, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(37, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(38, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(39, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(40, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(41, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(42, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(43, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(44, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(45, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(46, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(47, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(48, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(49, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(50, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(51, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(52, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(53, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(54, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(55, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(56, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(57, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc.create_gradient_temperature(58, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, -7, -0.1, -2.75, 0, -0.1, -2.75, -0.4, 0])

    lc = engine.load.create('温度梯度_升', load_case_type='TG', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gradient_temperature(1, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(2, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(3, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(4, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(5, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(6, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(7, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(8, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(9, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(10, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(11, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(12, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(13, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(14, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(15, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(16, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(17, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(18, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(19, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(20, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(21, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(22, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(23, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(24, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(25, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(26, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(27, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(28, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(29, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(30, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(31, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(32, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(33, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(34, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(35, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(36, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(37, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(38, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(39, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(40, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(41, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(42, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(43, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(44, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(45, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(46, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(47, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(48, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(49, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(50, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(51, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(52, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(53, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(54, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(55, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(56, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(57, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc.create_gradient_temperature(58, eDirect='Z', eGTempType='T', nNum=2, param=[0, 0, 14, -0.1, 5.5, 0, -0.1, 5.5, -0.4, 0])

    lc = engine.load.create('预应力1', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F0-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F0-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T0-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T0-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力10', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('T9-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T9-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力2', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F1-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F1-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T1-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T1-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力3', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F2-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F2-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T2-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T2-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力4', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F3-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F3-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T3-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T3-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力5', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F4-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F4-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T4-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T4-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力6', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F5-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F5-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T5-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T5-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力7', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F6-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F6-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T6-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T6-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力8', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F7-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F7-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T7-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T7-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力9', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('F8-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('F8-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T8-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('T8-2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('整体降温', load_case_type='T', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_uniform_temperature(1, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(2, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(3, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(4, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(5, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(6, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(7, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(8, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(9, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(10, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(11, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(12, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(13, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(14, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(15, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(16, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(17, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(18, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(19, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(20, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(21, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(22, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(23, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(24, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(25, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(26, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(27, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(28, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(29, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(30, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(31, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(32, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(33, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(34, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(35, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(36, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(37, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(38, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(39, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(40, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(41, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(42, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(43, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(44, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(45, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(46, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(47, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(48, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(49, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(50, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(51, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(52, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(53, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(54, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(55, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(56, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(57, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(58, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(1001, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(1002, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(1003, eDirect='X', dTemp=-30.000)

    lc.create_uniform_temperature(1004, eDirect='X', dTemp=-30.000)

    lc = engine.load.create('整体升温', load_case_type='T', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_uniform_temperature(1, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(2, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(3, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(4, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(5, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(6, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(7, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(8, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(9, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(10, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(11, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(12, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(13, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(14, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(15, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(16, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(17, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(18, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(19, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(20, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(21, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(22, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(23, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(24, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(25, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(26, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(27, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(28, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(29, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(30, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(31, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(32, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(33, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(34, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(35, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(36, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(37, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(38, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(39, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(40, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(41, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(42, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(43, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(44, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(45, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(46, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(47, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(48, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(49, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(50, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(51, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(52, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(53, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(54, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(55, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(56, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(57, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(58, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(1001, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(1002, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(1003, eDirect='X', dTemp=30.000)

    lc.create_uniform_temperature(1004, eDirect='X', dTemp=30.000)

    lc = engine.load.create('中跨预应力1', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('Z1-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('Z2-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('Z3-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('Z4-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('Z5-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('Z6-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('Z7-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('Z8-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('中跨预应力2', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('ZT-1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('自重', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重1', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重10', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重11', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重12', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重13', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重2', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重3', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重4', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重5', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重6', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重7', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重8', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重9', load_case_type='D', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    return lc_names


if __name__ == "__main__":
    from ._0_engine import engine
    mats = engine.material.all()
    mat_nos = [m.no for m in mats]
    elems = engine.element.all()
    elem_nos = [e.no for e in elems]
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    geos = engine.geometry.all()
    geo_names = [s.name for s in geos]
    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)
    print(lc_names)
    print(engine.load.all())