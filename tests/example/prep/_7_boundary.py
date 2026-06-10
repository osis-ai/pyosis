from pyosis.core.engine import OSISEngine
from typing import Tuple, Any


def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"边界属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> Tuple[list[int], list[str]]:
    """创建边界条件，返回边界编号列表 [bd1, bd2]
    
    边界编号（显式定义，幂等执行）：
    - 1: 桥台1 x向固定（UX, UY, UZ, RX, RZ约束，RY释放）
    - 2: 桥台2 x向滑动（UY, UZ, RX, RZ约束，UX、RY释放）
    """
    boundary = engine.boundary
    
    # 边界 1: x向固定（UX, UY, UZ, RX, RZ约束，RY释放）
    bd1 = boundary.create(1,"GENERAL",bX=1, bY=1, bZ=1, bRX=1, bRY=0, bRZ=1, bRW=0)
    _expect_attr(bd1,"no",1)
    bd1.assign("a", [node_nos[1]])  # 分配给节点2
    
    # 边界 2: x向滑动（UY, UZ, RX, RZ约束，UX、RY释放）
    bd2 = boundary.create(2,"GENERAL",bX=0, bY=1, bZ=1, bRX=1, bRY=0, bRZ=1, bRW=0)
    _expect_attr(bd2,"no",2)
    bd2.assign("a", [node_nos[13]])  # 分配给节点14
    

    bd3 = boundary.create(3,"MSTSLV",nNode=node_nos[1])
    _expect_attr(bd3,"no",3)

    bd4 = boundary.create(4,"RELEASE", Fxi_state=False, Fyi_state=True, Fzi_state=True, Mxi_state=True, Myi_state=False, Mzi_state=True, Mbi_state=False, Fxi=0, Fyi=0, Fzi=0, Mxi=0, Myi=0, Mzi=0, Mbi=0, Fxj_state=False, Fyj_state=True, Fzj_state=True, Mxj_state=True, Myj_state=False, Mzj_state=True, Mbj_state=False, Fxj=0, Fyj=0, Fzj=0, Mxj=0, Myj=0, Mzj=0, Mbj=0)
    _expect_attr(bd4,"no",4)

    bd5 = boundary.create(5,"ELSTCSPT",nCoor="", bX=1, DX=0, bY=1, DY=0, bZ=1, DZ=0, bRX=1, RX=0, bRY=0, RY=0, bRZ=1, RZ=0)
    _expect_attr(bd5,"no",5)

    bd6 = boundary.create(6,"GES",nCoor="", stiffness_matrix=[1e9, 0, 0, 0, 0, 0, 1e9, 0, 0, 0, 0, 0, 1e9, 0, 0, 0, 0, 0, 1e9, 0, 0])
    _expect_attr(bd6,"no",6)

    bd7 = boundary.create(7,"RIGID",nNodeI=node_nos[1])
    _expect_attr(bd7,"no",7)

    bds = boundary.all()
    if len(bds) != 7:
        raise Exception("获取所有创建的边界失败")
    boundary.get(bd7.no)
    boundary.delete(bd7.no)
    
    # 截面特性调整 临时 no=8，测完删除
    bd8 = boundary.create(8,"GENERAL",
        bX=0, bY=0, bZ=0,
        bRX=0, bRY=0, bRZ=0, bRW=0)
    _expect_attr(bd8, "no", 8)
    bd8.set_section_factor(
        1.0, 1.0, 1.0,
        1.0, 1.0, 1.0,
        1.0, 1.0,
    )
    got8 = boundary.get(8)
    if got8 is None:
        raise ValueError("set_section_factor 后 get(8) 失败")
    boundary.delete(8)
    if boundary.get(8) is not None:
        raise ValueError("delete(8) 后 get(8) 应返回 None")

    
    # 边界组
    bg1 = boundary.group.create("桥台1_永久_x向固定")
    _expect_attr(bg1,"name","桥台1_永久_x向固定")
    bg1.add([bd1.no])

    bg2 = boundary.group.create("桥台2_永久_x向滑动")
    _expect_attr(bg2,"name","桥台2_永久_x向滑动")
    bg2.add([bd2.no])

    # 边界组 replace 测试 — 临时组，不影响业务组
    bg_rep = boundary.group.create("_边界组替换测试")
    bg_rep.add([bd3.no, bd4.no])
    bg_rep = bg_rep.replace(["4by5"])  # 组内把边界 4 换成 5
    if set(bg_rep.boundary_nos) != {bd3.no, bd5.no}:
        raise ValueError(
            f"replace 后应为 {{{bd3.no}, {bd5.no}}}，实际 {bg_rep.boundary_nos}"
        )
    if bd4.no in bg_rep.boundary_nos:
        raise ValueError("replace 后不应再包含 bd4")
    boundary.group.delete("_边界组替换测试")
    if boundary.group.get("_边界组替换测试") is not None:
        raise ValueError("删除临时边界组后 get 应返回 None")


    # 边界组 remove / remove_all 测试 — 临时组，不影响业务组
    bg_test = boundary.group.create("_边界组移除测试")
    bg_test.add([bd3.no, bd4.no])
    if bd4.no not in bg_test.boundary_nos:
        raise ValueError(f"add 后应包含边界 {bd4.no}")
    bg_test = bg_test.remove([bd4.no])
    if bd4.no in bg_test.boundary_nos:
        raise ValueError(f"remove 后不应再包含边界 {bd4.no}")
    if bd3.no not in bg_test.boundary_nos:
        raise ValueError(f"remove 后应仍保留边界 {bd3.no}")
    bg_test = bg_test.add_all()
    expected = len(boundary.all())
    if bg_test.boundary_count != expected:
        raise ValueError(
            f"add_all 后应包含全部 {expected} 个边界，实际 {bg_test.boundary_count}"
        )
    # 边界组 remove_all 测试 — 临时组
    bg_test = bg_test.remove_all()
    if bg_test.boundary_count != 0:
        raise ValueError(f"remove_all 后应为 0 个边界，实际 {bg_test.boundary_count}")
    # 边界组 rename 测试 — 临时组
    bg_test = bg_test.rename("_边界组移除测试1")
    _expect_attr(bg_test, "name", "_边界组移除测试1")
    if boundary.group.get("_边界组移除测试") is not None:
        raise ValueError("rename 后旧名 '_边界组移除测试' 应不存在")
    if boundary.group.get("_边界组移除测试1") is None:
        raise ValueError("rename 后应能通过新名 get 到边界组")
    boundary.group.rename("_边界组移除测试1","_边界组移除测试2")
    if boundary.group.get("_边界组移除测试2") is None:
        raise ValueError("rename 后应能通过新名 get 到边界组")
    if boundary.group.get("_边界组移除测试1") is not None:
        raise ValueError("delete 后 get('_边界组移除测试2') 应返回 None")
    boundary.group.delete("_边界组移除测试2")


    boundary_group_name = [bg1.name, bg2.name]
    return [bd1.no, bd2.no], boundary_group_name

if __name__ == "__main__":
    from _0_engine import engine

    engine.boundary.clear()
    engine.boundary.group.clear()

    nodes = engine.node.all()
    print("nodes: ", nodes)
    node_nos = [n.no for n in nodes]
    
    bd_nos, bd_groups = build_boundaries(engine, node_nos)
    print(bd_nos)
    print(bd_groups)
    print(engine.boundary.all())
    print(engine.boundary.group.all())
