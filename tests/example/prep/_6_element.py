from pyosis.core.engine import OSISEngine
from typing import Tuple, Any

from pyosis.general import osis_matrix


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
    # 创建四节点壳单元（面荷载 ESRFC 需要第 4 节点）
    x1, x2 = 15.3200, 15.5400
    y_off = 0.5
    shell_thk_no = 1
    thk = engine.thickness
    thk.create(shell_thk_no, 0.30, 0.30)
    got_thk = thk.get(shell_thk_no)
    if got_thk is None:
        raise ValueError(f"thickness.get({shell_thk_no}) 返回 None")
    _expect_attr(got_thk, "no", shell_thk_no)
    _expect_attr(got_thk, "in_plane", 0.30)
    _expect_attr(got_thk, "out_plane", 0.30)
    n_top_r = engine.node.create(x2, y_off, 0.0)
    n_top_l = engine.node.create(x1, y_off, 0.0)
    e_shell = element.create_shell(
        node_nos[12],   # 节点 13，左下
        node_nos[13],   # 节点 14，右下
        n_top_r.no,     # 右上
        mat_nos[0],
        shell_thk_no,
        bIsThin=1,
        node4=n_top_l.no,  # 左上
        no=19,
    )
    _expect_attr(e_shell, "no", 19)
    all_thk = thk.all()
    if not any(t.no == shell_thk_no for t in all_thk):
        raise ValueError(f"thickness.all() 中应包含编号 {shell_thk_no}")
    if thk.count() < 1:
        raise ValueError("thickness.count() 应 >= 1")
    batch = thk.get([shell_thk_no, 999])
    if not isinstance(batch, list) or batch[0] is None or batch[0].no != shell_thk_no:
        raise ValueError("thickness.get([shell_thk_no, 999]) 第一项不符合预期")
    if batch[1] is not None:
        raise ValueError("thickness.get([..., 999]) 第二项应为 None")
    # 临时编号：测 renumber / delete / get
    thk.create(99, 0.25, 0.25)
    got99 = thk.get(99)
    if got99 is None or got99.in_plane != 0.25:
        raise ValueError("create(99) 后 get(99) 失败")
    thk.renumber("99", "100")
    got100 = thk.get(100)
    if got100 is None or got100.no != 100:
        raise ValueError("renumber 后 get(100) 失败")
    if thk.get(99) is not None:
        raise ValueError("renumber 后 get(99) 应为 None")
    thk.delete(100)
    if thk.get(100) is not None:
        raise ValueError("delete(100) 后 get(100) 应为 None")
    
    element.all()
    element.renumber(e15.no, e15.no + 1 )
    element.get(e15.no + 1)
    element.delete(e17.no)
    if element.get(e17.no) is not None:
      raise ValueError(f"delete({e17.no}) 后 get 应返回 None")
    element.count()

    # 变截面单元组(临时资源，测完全部 delete)
    taper_name = "_变截面测试组"
    taper_name_new = "_变截面测试组2"
    # 1) Custom 过渡截面对（对齐 OSIS 命令流：30001/30002 模式）
    osis_matrix("TaperC1", [
        [1, 0.0, 0.0],
        [1, 1.0, 0.0],
        [1, 1.0, 0.5],
        [1, 0.0, 0.5],
    ])
    osis_matrix("TaperC2", [
        [1, 0.0, 0.0],
        [1, 1.0, 0.0],
        [1, 1.0, 0.4],
        [1, 0.0, 0.4],
    ])
    sec_t1 = engine.section.create_custom("_过渡截面1", contour_matrix="TaperC1", no=301)
    sec_t2 = engine.section.create_custom("_过渡截面2", contour_matrix="TaperC2", no=302)
    sec_t1.set_offset("Middle", 0.0, "Top", 0.0)
    sec_t2.set_offset("Middle", 0.0, "Top", 0.0)
    # 2) 独立节点链 + 2 根变截面梁（i/j 均为 301→302，且 ≥2 个单元）
    n_t1 = engine.node.create(0.0, -1.0, 0.0)
    n_t2 = engine.node.create(1.0, -1.0, 0.0)
    n_t3 = engine.node.create(2.0, -1.0, 0.0)
    e_t1 = element.create_beam3d(
        n_t1.no, n_t2.no,
        mat_nos[0], 301, 302,
        1, 1, 0.0, 0, 0.0, 0, no=20,
    )
    e_t2 = element.create_beam3d(
        n_t2.no, n_t3.no,
        mat_nos[0], 301, 302,
        1, 1, 0.0, 0, 0.0, 0, no=21,
    )
    _expect_attr(e_t1, "no", 20)
    _expect_attr(e_t2, "no", 21)
    # 3) create
    tg = element.taper_group.create(taper_name,"0",1.0, "0", 0.0,"0", 1.0, "0", 0.0,"20", "21")
    _expect_attr(tg, "name", taper_name)
    # 4) get
    got_tg = element.taper_group.get(taper_name)
    if got_tg is None:
        raise ValueError(f"taper_group.get({taper_name!r}) 失败")
    _expect_attr(got_tg, "name", taper_name)
    if got_tg.elements != [20, 21]:
        raise ValueError(f"taper_group 应包含单元 [20, 21]，实际 {got_tg.elements!r}")
    # 5) all
    all_tg = element.taper_group.all()
    if not any(g.name == taper_name for g in all_tg):
        raise ValueError(f"taper_group.all() 应包含 {taper_name!r}")
    # 6) rename
    tg_renamed = element.taper_group.rename(taper_name, taper_name_new)
    _expect_attr(tg_renamed, "name", taper_name_new)
    if element.taper_group.get(taper_name) is not None:
        raise ValueError("rename 后旧名称 get 应返回 None")
    got_tg2 = element.taper_group.get(taper_name_new)
    if got_tg2 is None:
        raise ValueError(f"rename 后 get({taper_name_new!r}) 失败")
    # 7) delete 变截面组
    element.taper_group.delete(taper_name_new)
    if element.taper_group.get(taper_name_new) is not None:
        raise ValueError("taper_group.delete 后 get 应返回 None")
    # 8) 清理临时单元 / 节点 / 截面
    element.delete(20)
    element.delete(21)
    if element.get(20) is not None or element.get(21) is not None:
        raise ValueError("临时变截面单元 delete 后 get 应返回 None")
    engine.node.delete(n_t1.no)
    engine.node.delete(n_t2.no)
    engine.node.delete(n_t3.no)
    engine.section.delete(301)
    engine.section.delete(302)

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
    from _0_engine import engine

    # 1) 先删钢束形状（释放对单元组的占用）
    engine.tendon.shape.clear()
    # 2) 再删单元组
    engine.element.group.clear()

    # 3) 最后删单元
    engine.element.clear()
    # 4) 单元删完后再清壳厚度特性
    engine.thickness.clear()

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
