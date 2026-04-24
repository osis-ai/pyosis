from pyosis.core.engine import OSISEngine
from typing import Tuple

def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> Tuple[list[int], list[str]]:
    """创建单元，返回单元编号列表 [e1, e2, ..., e14]
    
    单元编号（显式定义，幂等执行）：
    - 1-2: 封端区域（sec4 + sec4）
    - 3: 过渡段左（sec5 + sec1）
    - 4-11: 标准段（sec1 + sec1）
    - 12: 过渡段右（sec1 + sec5）
    - 13-14: 封端区域（sec4 + sec4）
    """
    element = engine.element
    
    # 封端区域：sec4 + sec4
    e1  = element.create_beam3d(node_nos[0], node_nos[1], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=1)
    e2  = element.create_beam3d(node_nos[1], node_nos[2], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=2)
    
    # 过渡段：sec5 + sec1
    e3  = element.create_beam3d(node_nos[2], node_nos[3], mat_nos[0], sec_nos[4], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=3)
    
    # 标准段：sec1 + sec1
    e4  = element.create_beam3d(node_nos[3],  node_nos[4],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=4)
    e5  = element.create_beam3d(node_nos[4],  node_nos[5],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=5)
    e6  = element.create_beam3d(node_nos[5],  node_nos[6],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=6)
    e7  = element.create_beam3d(node_nos[6],  node_nos[7],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=7)
    e8  = element.create_beam3d(node_nos[7],  node_nos[8],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=8)
    e9  = element.create_beam3d(node_nos[8],  node_nos[9],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=9)
    e10 = element.create_beam3d(node_nos[9],  node_nos[10], mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=10)
    e11 = element.create_beam3d(node_nos[10], node_nos[11], mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=11)
    
    # 过渡段：sec1 + sec5
    e12 = element.create_beam3d(node_nos[11], node_nos[12], mat_nos[0], sec_nos[0], sec_nos[4], 1, 1, 0.000E+00, 0, 0.00, 0, no=12)
    
    # 封端区域：sec4 + sec4
    e13 = element.create_beam3d(node_nos[12], node_nos[13], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=13)
    e14 = element.create_beam3d(node_nos[13], node_nos[14], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=14)
    
    elem_nos = [e1.no, e2.no, e3.no, e4.no, e5.no, e6.no, e7.no,
                e8.no, e9.no, e10.no, e11.no, e12.no, e13.no, e14.no]
    
    # 分配构件理论厚度
    engine.prop.assign_component_thickness(3.128E-01, "a", [elem_nos[0], elem_nos[1], elem_nos[12], elem_nos[13]])
    engine.prop.assign_component_thickness(2.379E-01, "a", [elem_nos[2], elem_nos[11]])
    engine.prop.assign_component_thickness(1.967E-01, "a", elem_nos[3:11])
    
    # 单元组
    eg1 = element.group.create("封端混凝土单元")
    eg1.add([1, 14])
    eg2 = element.group.create("钢束-1-N1线型单元")
    eg2.add(elem_nos[0:13])
    eg3 = element.group.create("钢束-2-N2线型单元")
    eg3.add(elem_nos[0:13])
    eg4 = element.group.create("主梁单元")
    eg4.add(elem_nos[0:13])
    
    elem_groups_names = [eg1.name, eg2.name, eg3.name, eg4.name]
    return elem_nos, elem_groups_names

if __name__ == "__main__":
    from ._0_engine import engine
    mats = engine.material.all()
    print("materials: ", mats)
    mat_nos = [m.no for m in mats]
    secs = engine.section.all()
    print("sections: ", secs)
    sec_nos = [s.no for s in secs]
    nodes = engine.node.all()
    print("nodes: ", nodes)
    node_nos = [n.no for n in nodes]

    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)
    print(elem_nos)
    print(elem_group_names)
    print(engine.element.all())
    print(engine.element.group.all())
