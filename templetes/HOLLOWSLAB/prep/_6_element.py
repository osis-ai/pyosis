from pyosis.core.engine import OSISEngine
from typing import Tuple, Any


def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"单元属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

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
    _expect_attr(e1,"no",1)
    e2  = element.create_beam3d(node_nos[1], node_nos[2], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=2)
    _expect_attr(e2,"no",2)
    # 过渡段：sec5 + sec1
    e3  = element.create_beam3d(node_nos[2], node_nos[3], mat_nos[0], sec_nos[4], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=3)
    _expect_attr(e3,"no",3)
    # 标准段：sec1 + sec1
    e4  = element.create_beam3d(node_nos[3],  node_nos[4],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=4)
    _expect_attr(e4,"no",4)
    e5  = element.create_beam3d(node_nos[4],  node_nos[5],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=5)
    _expect_attr(e5,"no",5)
    e6  = element.create_beam3d(node_nos[5],  node_nos[6],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=6)
    _expect_attr(e6,"no",6)
    e7  = element.create_beam3d(node_nos[6],  node_nos[7],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=7)
    _expect_attr(e7,"no",7)
    e8  = element.create_beam3d(node_nos[7],  node_nos[8],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=8)
    _expect_attr(e8,"no",8)
    e9  = element.create_beam3d(node_nos[8],  node_nos[9],  mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=9)
    _expect_attr(e9,"no",9)
    e10 = element.create_beam3d(node_nos[9],  node_nos[10], mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=10)
    _expect_attr(e10,"no",10)
    e11 = element.create_beam3d(node_nos[10], node_nos[11], mat_nos[0], sec_nos[0], sec_nos[0], 1, 1, 0.000E+00, 0, 0.00, 0, no=11)
    _expect_attr(e11,"no",11)
    # 过渡段：sec1 + sec5
    e12 = element.create_beam3d(node_nos[11], node_nos[12], mat_nos[0], sec_nos[0], sec_nos[4], 1, 1, 0.000E+00, 0, 0.00, 0, no=12)
    _expect_attr(e12,"no",12)
    # 封端区域：sec4 + sec4
    e13 = element.create_beam3d(node_nos[12], node_nos[13], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=13)
    _expect_attr(e13,"no",13)
    e14 = element.create_beam3d(node_nos[12], node_nos[13], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=14)
    _expect_attr(e14,"no",14)
    e15 = element.create_beam3d(node_nos[12], node_nos[13], mat_nos[0], sec_nos[3], sec_nos[3], 1, 1, 0.000E+00, 0, 0.00, 0, no=15)
    _expect_attr(e15,"no",15)
    e16 = element.create_truss(
        node_nos[12], node_nos[13],
        mat_nos[0], sec_nos[3], sec_nos[3], no=16
    )
    _expect_attr(e16,"no",16)
    e17 = element.create_spring(
        node_nos[12], node_nos[13],
        1, 10, 10, 10, 10, 10, 10, 0.0,17
    )
    _expect_attr(e17,"no",17)

    e18 = element.create_cable(
        node_nos[12], node_nos[13],
        mat_nos[0], sec_nos[3], "UL",18
    )
    _expect_attr(e18,"no",18)
    # 创建壳单元
    x_mid = 0.5 * (14.3200 + 15.3200)
    y_off = 0.5
    n_shell = engine.node.create(x_mid, y_off, 0.0, no=15)
    shell_thk_no = 1
    engine.thickness.create(shell_thk_no, 0.30, 0.30)
    element.create_shell(
    node_nos[12],
    node_nos[13],
    n_shell.no,
    mat_nos[0],
    shell_thk_no,
    bIsThin=1,
    )
    # thickness delete 测试：临时编号，测完即删
    engine.thickness.create(99, 0.25, 0.25)
    engine.thickness.renumber("99","100")
    engine.thickness.delete(100)
    
    element.all()
    element.renumber(e15.no, e15.no + 1 )
    element.get(e15.no + 1)
    element.delete(e17.no)
    if element.get(e17.no) is not None:
      raise ValueError(f"delete({e17.no}) 后 get 应返回 None")
    element.count()

    elem_nos = [e1.no, e2.no, e3.no, e4.no, e5.no, e6.no, e7.no,
                e8.no, e9.no, e10.no, e11.no, e12.no, e13.no, e14.no, e18.no, e16.no]
    
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
    # 添加单元组
    eg5 = element.group.create("封端混凝土单元5")
    # 添加单元
    eg5.add([1, 14])
    # 替换单元
    new_eg5 = eg5.replace(["14by13"])
    if new_eg5.elements != [1, 13]:
      raise ValueError(f"替换后应为 ['14by13']，实际 {new_eg5.elements}")
    # 移除单元
    new_eg5.remove([13])
    _expect_attr(new_eg5, "element_count", 1)
    if 13 in new_eg5.elements:
      raise ValueError("单元 13 应已从封端混凝土单元组移除")
    if 1 not in new_eg5.elements:
      raise ValueError("单元 1 应仍在封端混凝土单元组中")

    # 添加全部单元
    eg5_group = new_eg5.add_all()
    _expect_attr(eg5_group, "element_count", len(element.all()))
    # 移除全部单元
    eg5_group.remove_all()
    _expect_attr(eg5_group, "element_count", 0)
    # 重命名单元组
    eg5_group.rename("封端混凝土单元6")
    _expect_attr(eg5_group, "name", "封端混凝土单元6")

    # 获取全部单元组
    all_groups = element.group.all()
    if element.group.count() != len(all_groups):
      raise ValueError(
          f"count() 与 all() 数量不一致: count={element.group.count()}, all={len(all_groups)}"
      )
    # 获取单元组
    got = element.group.get("封端混凝土单元6")
    _expect_attr(got, "name", "封端混凝土单元6")
    # 删除单元组
    element.group.delete("封端混凝土单元6")
    if element.group.count() != 4:
      raise ValueError(f"删除后单元组数量应为 4，实际 {element.group.count()}")
    if "封端混凝土单元6" in [g.name for g in element.group.all()]:
      raise ValueError("封端混凝土单元6 应已从单元组列表中删除")

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
