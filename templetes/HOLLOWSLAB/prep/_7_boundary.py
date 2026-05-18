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
    bd1 = boundary.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=0, bRZ=1, bRW=0, no=1)
    _expect_attr(bd1,"no",1)
    bd1.assign("a", [node_nos[1]])  # 分配给节点2
    
    # 边界 2: x向滑动（UY, UZ, RX, RZ约束，UX、RY释放）
    bd2 = boundary.create_general(bX=0, bY=1, bZ=1, bRX=1, bRY=0, bRZ=1, bRW=0, no=2)
    _expect_attr(bd2,"no",2)
    bd2.assign("a", [node_nos[13]])  # 分配给节点14
    

    bd3 = boundary.create_master_slave(nNode=node_nos[1], no=3)
    _expect_attr(bd3,"no",3)

    bd4 = boundary.create_release(no=4, Fxi_state=False, Fyi_state=True, Fzi_state=True, Mxi_state=True, Myi_state=False, Mzi_state=True, Mbi_state=False, Fxi=0, Fyi=0, Fzi=0, Mxi=0, Myi=0, Mzi=0, Mbi=0, Fxj_state=False, Fyj_state=True, Fzj_state=True, Mxj_state=True, Myj_state=False, Mzj_state=True, Mbj_state=False, Fxj=0, Fyj=0, Fzj=0, Mxj=0, Myj=0, Mzj=0, Mbj=0)
    _expect_attr(bd4,"no",4)

    bd5 = boundary.create_elstcspt(nCoor="", bX=1, DX=0, bY=1, DY=0, bZ=1, DZ=0, bRX=1, RX=0, bRY=0, RY=0, bRZ=1, RZ=0, no=5)
    _expect_attr(bd5,"no",5)

    bd6 = boundary.create_general_elstcspt(nCoor="", stiffness_matrix=[1e9, 0, 0, 0, 0, 0, 1e9, 0, 0, 0, 0, 0, 1e9, 0, 0, 0, 0, 0, 1e9, 0, 0], no=6)
    _expect_attr(bd6,"no",6)

    bd7 = boundary.create_rigid(nNodeI=node_nos[1], no=7)
    _expect_attr(bd7,"no",7)

    bds = boundary.all()
    if len(bds) != 7:
        raise Exception("获取所有创建的边界失败")
    boundary.get(bd7.no)
    boundary.delete(bd7.no)
    
    # 边界组
    bg1 = boundary.group.create("桥台1_永久_x向固定")
    _expect_attr(bg1,"name","桥台1_永久_x向固定")
    bg1.add([bd1.no])

    bg2 = boundary.group.create("桥台2_永久_x向滑动")
    _expect_attr(bg2,"name","桥台2_永久_x向滑动")
    bg2.add([bd2.no])

    boundary_group_name = [bg1.name, bg2.name]
    return [bd1.no, bd2.no], boundary_group_name

if __name__ == "__main__":
    from ._0_engine import engine
    nodes = engine.node.all()
    print("nodes: ", nodes)
    node_nos = [n.no for n in nodes]
    
    bd_nos, bd_groups = build_boundaries(engine, node_nos)
    print(bd_nos)
    print(bd_groups)
    print(engine.boundary.all())
    print(engine.boundary.group.all())
