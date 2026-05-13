"""荷载工况"""

from pyosis.core.engine import OSISEngine

def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:
    """创建荷载工况和钢束，返回荷载工况名称列表"""

    lc_names = []

    engine.tendon.prop.create_in_custom('13_', n_mat=2, d_val=1.8200E-03, d_pipe=5.0000E-02, d_friction_coeff=1.7000E-01, d_deviation_coeff=1.5000E-03, d_starting_deform=6.0000E-03, d_end_deform=6.0000E-03, d_tensioning_coeff=1.0000E+00, d_relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in_custom('4_', n_mat=2, d_val=5.6000E-04, d_pipe=5.0000E-02, d_friction_coeff=1.7000E-01, d_deviation_coeff=1.5000E-03, d_starting_deform=6.0000E-03, d_end_deform=6.0000E-03, d_tensioning_coeff=1.0000E+00, d_relaxation_coeff=3.0000E-01)

    engine.tendon.prop.create_in_custom('5_', n_mat=2, d_val=7.0000E-04, d_pipe=5.0000E-02, d_friction_coeff=1.7000E-01, d_deviation_coeff=1.5000E-03, d_starting_deform=6.0000E-03, d_end_deform=6.0000E-03, d_tensioning_coeff=1.0000E+00, d_relaxation_coeff=3.0000E-01)

    shape = engine.tendon.shape.create_arc3d('1-N1', n_num=2, prop='5_', element_group='1-N1单元组', curve_name='钢束样条曲线_1-N1')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('1-N2', n_num=2, prop='5_', element_group='1-N2单元组', curve_name='钢束样条曲线_1-N2')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('1-N3', n_num=2, prop='4_', element_group='1-N3单元组', curve_name='钢束样条曲线_1-N3')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('1-N4', n_num=2, prop='4_', element_group='1-N4单元组', curve_name='钢束样条曲线_1-N4')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N1', n_num=2, prop='5_', element_group='2-N1单元组', curve_name='钢束样条曲线_2-N1')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N1-复制', n_num=2, prop='5_', element_group='2-N1-复制单元组', curve_name='钢束样条曲线_2-N1-复制')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N1-复制01', n_num=2, prop='5_', element_group='2-N1-复制01单元组', curve_name='钢束样条曲线_2-N1-复制01')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N2', n_num=2, prop='4_', element_group='2-N2单元组', curve_name='钢束样条曲线_2-N2')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N2-复制', n_num=2, prop='4_', element_group='2-N2-复制单元组', curve_name='钢束样条曲线_2-N2-复制')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N2-复制01', n_num=2, prop='4_', element_group='2-N2-复制01单元组', curve_name='钢束样条曲线_2-N2-复制01')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N3', n_num=2, prop='4_', element_group='2-N3单元组', curve_name='钢束样条曲线_2-N3')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N3-复制', n_num=2, prop='4_', element_group='2-N3-复制单元组', curve_name='钢束样条曲线_2-N3-复制')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N3-复制01', n_num=2, prop='4_', element_group='2-N3-复制01单元组', curve_name='钢束样条曲线_2-N3-复制01')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N4', n_num=2, prop='4_', element_group='2-N4单元组', curve_name='钢束样条曲线_2-N4')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N4-复制', n_num=2, prop='4_', element_group='2-N4-复制单元组', curve_name='钢束样条曲线_2-N4-复制')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('2-N4-复制01', n_num=2, prop='4_', element_group='2-N4-复制01单元组', curve_name='钢束样条曲线_2-N4-复制01')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('5-N1', n_num=2, prop='5_', element_group='5-N1单元组', curve_name='钢束样条曲线_5-N1')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('5-N2', n_num=2, prop='5_', element_group='5-N2单元组', curve_name='钢束样条曲线_5-N2')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('5-N3', n_num=2, prop='4_', element_group='5-N3单元组', curve_name='钢束样条曲线_5-N3')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('5-N4', n_num=2, prop='4_', element_group='5-N4单元组', curve_name='钢束样条曲线_5-N4')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D1-T1', n_num=2, prop='5_', element_group='D1-T1单元组', curve_name='钢束样条曲线_D1-T1')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D1-T2', n_num=1, prop='13_', element_group='D1-T2单元组', curve_name='钢束样条曲线_D1-T2')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D2-T1-复制', n_num=2, prop='5_', element_group='D2-T1-复制单元组', curve_name='钢束样条曲线_D2-T1-复制')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D2-T2-复制', n_num=1, prop='13_', element_group='D2-T2-复制单元组', curve_name='钢束样条曲线_D2-T2-复制')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D3-T1-复制01', n_num=2, prop='5_', element_group='D3-T1-复制01单元组', curve_name='钢束样条曲线_D3-T1-复制01')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D3-T2-复制01', n_num=1, prop='13_', element_group='D3-T2-复制01单元组', curve_name='钢束样条曲线_D3-T2-复制01')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D4-T1-复制02', n_num=2, prop='5_', element_group='D4-T1-复制02单元组', curve_name='钢束样条曲线_D4-T1-复制02')

    shape.layout('GLOBAL')

    shape = engine.tendon.shape.create_arc3d('D4-T2-复制02', n_num=1, prop='13_', element_group='D4-T2-复制02单元组', curve_name='钢束样条曲线_D4-T2-复制02')

    shape.layout('GLOBAL')

    lc = engine.load.create('墩顶现浇自重', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('二期_二期', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_line_load(nEntity=1, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=2, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=3, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=4, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=5, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=6, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=7, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=8, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=9, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=10, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=11, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=12, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=13, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=14, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=15, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=16, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=17, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=18, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=19, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=20, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=21, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=22, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=23, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=24, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=25, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=26, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=27, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=28, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=29, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=30, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=31, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=32, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=33, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=34, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=35, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=36, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=37, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=38, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=39, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=40, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=41, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=42, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=43, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=44, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=45, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=46, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=47, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=48, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=49, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=50, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=51, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=52, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=53, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=54, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=55, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=56, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=57, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=58, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=59, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=60, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=61, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=62, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=63, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=64, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=65, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=66, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=67, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=68, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=69, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=70, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=71, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=72, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=73, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=74, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=75, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=76, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=77, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=78, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=79, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=80, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=81, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=82, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=83, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=84, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=85, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=86, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=87, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=88, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=89, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=90, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=91, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=92, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=93, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=94, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=95, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=96, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=97, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=98, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=99, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=100, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=101, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=102, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=103, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=104, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=105, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=106, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=107, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=108, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=109, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc.create_line_load(nEntity=110, eCoordSystem=1, eLoadType=0, dOffsetXI=0.000, dOffsetYI=0.000, dOffsetZI=0.000, dFXI=0.0000E+00, dFYI=0.0000E+00, dFZI=-2.2000E+04, dMXI=0.0000E+00, dMYI=0.0000E+00, dMZI=0.0000E+00, dOffsetXJ=1.000, dOffsetYJ=0.000, dOffsetZJ=0.000, dFXJ=0.0000E+00, dFYJ=0.0000E+00, dFZJ=-2.2000E+04, dMXJ=0.0000E+00, dMYJ=0.0000E+00, dMZJ=0.0000E+00)

    lc = engine.load.create('局部降温_局部降温', load_case_type='TG', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gradient_temperature(1, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(2, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(3, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(4, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(5, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(6, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(7, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(8, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(9, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(10, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(11, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(12, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(13, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(14, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(15, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(16, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(17, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(18, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(19, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(20, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(21, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(22, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(23, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(24, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(25, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(26, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(27, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(28, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(29, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(30, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(31, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(32, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(33, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(34, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(35, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(36, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(37, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(38, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(39, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(40, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(41, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(42, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(43, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(44, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(45, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(46, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(47, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(48, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(49, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(50, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(51, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(52, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(53, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(54, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(55, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(56, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(57, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(58, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(59, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(60, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(61, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(62, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(63, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(64, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(65, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(66, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(67, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(68, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(69, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(70, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(71, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(72, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(73, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(74, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(75, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(76, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(77, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(78, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(79, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(80, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(81, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(82, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(83, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(84, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(85, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(86, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(87, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(88, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(89, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(90, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(91, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(92, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(93, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(94, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(95, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(96, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(97, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(98, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(99, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(100, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(101, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(102, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(103, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(104, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(105, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(106, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(107, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(108, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(109, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc.create_gradient_temperature(110, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, -2.75, -0.28, 0])

    lc = engine.load.create('局部升温_局部升温', load_case_type='TG', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gradient_temperature(1, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(2, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(3, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(4, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(5, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(6, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(7, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(8, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(9, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(10, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(11, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(12, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(13, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(14, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(15, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(16, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(17, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(18, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(19, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(20, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(21, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(22, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(23, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(24, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(25, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(26, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(27, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(28, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(29, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(30, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(31, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(32, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(33, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(34, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(35, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(36, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(37, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(38, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(39, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(40, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(41, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(42, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(43, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(44, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(45, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(46, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(47, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(48, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(49, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(50, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(51, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(52, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(53, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(54, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(55, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(56, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(57, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(58, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(59, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(60, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(61, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(62, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(63, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(64, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(65, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(66, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(67, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(68, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(69, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(70, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(71, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(72, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(73, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(74, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(75, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(76, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(77, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(78, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(79, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(80, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(81, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(82, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(83, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(84, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(85, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(86, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(87, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(88, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(89, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(90, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(91, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(92, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(93, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(94, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(95, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(96, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(97, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(98, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(99, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(100, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(101, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(102, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(103, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(104, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(105, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(106, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(107, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(108, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(109, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc.create_gradient_temperature(110, eDirect='Z', eGTempType='T', nNum=1, param=[3.3, 0, 5.5, -0.28, 0])

    lc = engine.load.create('温降_温降', load_case_type='T', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_uniform_temperature(1, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(2, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(3, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(4, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(5, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(6, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(7, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(8, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(9, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(10, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(11, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(12, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(13, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(14, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(15, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(16, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(17, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(18, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(19, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(20, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(21, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(22, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(23, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(24, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(25, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(26, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(27, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(28, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(29, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(30, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(31, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(32, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(33, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(34, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(35, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(36, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(37, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(38, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(39, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(40, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(41, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(42, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(43, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(44, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(45, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(46, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(47, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(48, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(49, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(50, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(51, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(52, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(53, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(54, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(55, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(56, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(57, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(58, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(59, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(60, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(61, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(62, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(63, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(64, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(65, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(66, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(67, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(68, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(69, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(70, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(71, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(72, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(73, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(74, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(75, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(76, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(77, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(78, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(79, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(80, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(81, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(82, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(83, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(84, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(85, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(86, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(87, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(88, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(89, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(90, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(91, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(92, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(93, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(94, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(95, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(96, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(97, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(98, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(99, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(100, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(101, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(102, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(103, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(104, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(105, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(106, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(107, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(108, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(109, eDirect='X', dTemp=-22.000)

    lc.create_uniform_temperature(110, eDirect='X', dTemp=-22.000)

    lc = engine.load.create('温升_温升', load_case_type='T', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_uniform_temperature(1, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(2, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(3, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(4, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(5, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(6, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(7, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(8, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(9, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(10, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(11, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(12, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(13, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(14, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(15, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(16, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(17, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(18, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(19, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(20, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(21, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(22, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(23, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(24, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(25, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(26, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(27, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(28, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(29, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(30, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(31, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(32, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(33, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(34, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(35, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(36, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(37, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(38, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(39, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(40, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(41, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(42, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(43, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(44, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(45, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(46, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(47, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(48, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(49, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(50, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(51, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(52, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(53, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(54, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(55, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(56, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(57, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(58, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(59, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(60, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(61, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(62, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(63, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(64, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(65, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(66, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(67, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(68, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(69, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(70, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(71, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(72, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(73, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(74, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(75, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(76, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(77, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(78, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(79, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(80, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(81, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(82, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(83, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(84, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(85, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(86, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(87, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(88, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(89, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(90, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(91, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(92, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(93, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(94, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(95, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(96, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(97, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(98, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(99, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(100, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(101, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(102, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(103, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(104, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(105, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(106, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(107, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(108, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(109, eDirect='X', dTemp=22.000)

    lc.create_uniform_temperature(110, eDirect='X', dTemp=22.000)

    lc = engine.load.create('预应力_负弯矩束-1', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('D1-T1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('D1-T2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('D4-T1-复制02', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('D4-T2-复制02', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力_负弯矩束-2', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('D2-T1-复制', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('D2-T2-复制', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力_负弯矩束-3', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('D3-T1-复制01', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('D3-T2-复制01', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预应力_正弯矩束', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_prestress('1-N1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('1-N2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('1-N3', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('1-N4', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N1-复制', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N1-复制01', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N2-复制', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N2-复制01', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N3', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N3-复制', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N3-复制01', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N4', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N4-复制', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('2-N4-复制01', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('5-N1', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('5-N2', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('5-N3', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc.create_prestress('5-N4', eTensionType='BOTH', eTensionForceType='ST', dBeg=1.395000E+09, dEnd=1.395000E+09)

    lc = engine.load.create('预制梁自重', load_case_type='CS', scalar=1.00000E+00)
    lc_names.append(lc.name)

    lc.create_gravity(0.000, 0.000, -1.040)

    lc = engine.load.create('自重_自重', load_case_type='CS', scalar=1.00000E+00)
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