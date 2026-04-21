from _0_engine import engine
from _3_material import mat_no
from _4_section import sec_no
from _5_node import node_no
from pyosis.element.interface import osis_element_group

element = engine.element
eles = []

# 封端区域：sec4 + sec4
eles.append(element.create_beam3d(node_no[0],  node_no[1],  mat_no[0], sec_no[3], sec_no[3], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[1],  node_no[2],  mat_no[0], sec_no[3], sec_no[3], 1, 1, 0.000E+00, 0, 0.00, 0))

# 过渡段：sec5 + sec1
eles.append(element.create_beam3d(node_no[2],  node_no[3],  mat_no[0], sec_no[4], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))

# 标准段：sec1 + sec1
eles.append(element.create_beam3d(node_no[3],  node_no[4],  mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[4],  node_no[5],  mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[5],  node_no[6],  mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[6],  node_no[7],  mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[7],  node_no[8],  mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[8],  node_no[9],  mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[9],  node_no[10], mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[10], node_no[11], mat_no[0], sec_no[0], sec_no[0], 1, 1, 0.000E+00, 0, 0.00, 0))

# 过渡段：sec1 + sec5
eles.append(element.create_beam3d(node_no[11], node_no[12], mat_no[0], sec_no[0], sec_no[4], 1, 1, 0.000E+00, 0, 0.00, 0))

# 封端区域：sec4 + sec4
eles.append(element.create_beam3d(node_no[12], node_no[13], mat_no[0], sec_no[3], sec_no[3], 1, 1, 0.000E+00, 0, 0.00, 0))
eles.append(element.create_beam3d(node_no[13], node_no[14], mat_no[0], sec_no[3], sec_no[3], 1, 1, 0.000E+00, 0, 0.00, 0))

elem_no = [it.no for it in eles]

# 分配构件理论厚度
engine.prop.assign_component_thickness(3.128E-01, "a", [elem_no[0], elem_no[1], elem_no[12], elem_no[13]])
engine.prop.assign_component_thickness(2.379E-01, "a", [elem_no[2], elem_no[11]])
engine.prop.assign_component_thickness(1.967E-01, "a", elem_no[3:10])

# 单元组
osis_element_group("封端混凝土单元", "c")
osis_element_group("封端混凝土单元", "a", [1, 14])
osis_element_group("钢束-1-N1线型单元", "c")
osis_element_group("钢束-1-N1线型单元", "a", ["1to14"])
osis_element_group("钢束-2-N2线型单元", "c")
osis_element_group("钢束-2-N2线型单元", "a", ["1to14"])
osis_element_group("主梁单元", "c")
osis_element_group("主梁单元", "a", ["1to14"])
