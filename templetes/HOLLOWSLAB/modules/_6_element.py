from pyosis.core.engine import OSISEngine
from typing import Tuple

def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> Tuple[list[int], list[str]]:
    """创建单元，返回单元编号列表 [e1, e2, ..., e14]"""
    element = engine.element
    eles = []
    
    # 封端区域：sec4 + sec4
    eles.append(element.create_beam3d(node_nos[0],  node_nos[1],  mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[1],  node_nos[2],  mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0))
    
    # 过渡段：sec5 + sec1
    eles.append(element.create_beam3d(node_nos[2],  node_nos[3],  mat_nos[0], sec_nos[4], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    
    # 标准段：sec1 + sec1
    eles.append(element.create_beam3d(node_nos[3],  node_nos[4],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[4],  node_nos[5],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[5],  node_nos[6],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[6],  node_nos[7],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[7],  node_nos[8],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[8],  node_nos[9],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[9],  node_nos[10], mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[10], node_nos[11], mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0))
    
    # 过渡段：sec1 + sec5
    eles.append(element.create_beam3d(node_nos[11], node_nos[12], mat_nos[0], sec_nos[0], sec_nos[4], 1, 1, 0.000E+00, 0, 0.00, 0))
    
    # 封端区域：sec4 + sec4
    eles.append(element.create_beam3d(node_nos[12], node_nos[13], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0))
    eles.append(element.create_beam3d(node_nos[13], node_nos[14], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0))
    
    elem_nos = [it.no for it in eles]
    
    # 分配构件理论厚度
    engine.prop.assign_component_thickness(3.128E-01, "a", [elem_nos[0], elem_nos[1], elem_nos[12], elem_nos[13]])
    engine.prop.assign_component_thickness(2.379E-01, "a", [elem_nos[2], elem_nos[11]])
    engine.prop.assign_component_thickness(1.967E-01, "a", elem_nos[3:10])
    
    # 单元组
    element.group("封端混凝土单元", "c")
    element.group("封端混凝土单元", "a", [1, 14])
    element.group("钢束-1-N1线型单元", "c")
    element.group("钢束-1-N1线型单元", "a", elem_nos[0:13])
    element.group("钢束-2-N2线型单元", "c")
    element.group("钢束-2-N2线型单元", "a", elem_nos[0:13])
    element.group("主梁单元", "c")
    element.group("主梁单元", "a", elem_nos[0:13])
    
    elem_groups_names = ["封端混凝土单元", "钢束-1-N1线型单元", "钢束-2-N2线型单元", "主梁单元"]      # group相关功能未完成，先这样临时替代
    return elem_nos, elem_groups_names

# if __name__ == "__main__":
#     from _0_engine import engine
#     elem_nos = build_elements(engine)
#     print(elem_nos)
#     print(engine.elem_nos.all())
