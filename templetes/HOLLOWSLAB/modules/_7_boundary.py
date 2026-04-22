from pyosis.core.engine import OSISEngine
from typing import Tuple

def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> Tuple[list[int], list[str]]:
    """创建边界条件，返回边界编号列表 [bd1, bd2]"""
    boundary = engine.boundary
    
    # 边界1：x向固定（UX, UY, UZ, RX, RZ约束，RY释放）
    bd1 = boundary.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=0, bRZ=1, bRW=0, no=1)
    bd1.assign("a", [node_nos[1]])  # 分配给节点2
    
    # 边界2：x向滑动（UY, UZ, RX, RZ约束，UX、RY释放）
    bd2 = boundary.create_general(bX=0, bY=1, bZ=1, bRX=1, bRY=0, bRZ=1, bRW=0, no=2)
    bd2.assign("a", [node_nos[13]])  # 分配给节点14
    
    # 边界组
    boundary.group("桥台1_永久_x向固定", "c")
    boundary.group("桥台1_永久_x向固定", "a", [1])
    boundary.group("桥台2_永久_x向滑动", "c")
    boundary.group("桥台2_永久_x向滑动", "a", [2])
    
    boundary_group_name = ["桥台1_永久_x向固定", "桥台2_永久_x向滑动"]      # 边界组未完成，先这样临时替代
    return [bd1.no, bd2.no], boundary_group_name
