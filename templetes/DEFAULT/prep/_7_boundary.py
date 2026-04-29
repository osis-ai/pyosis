"""边界条件"""

from pyosis.core.engine import OSISEngine

def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:
    """边界条件"""

    # ========== 原始命令流 ==========
    # Boundary,1,GENERAL,,1,1,1,1,1,1,1;//建立边界，GENERAL类型
    # AsgnBd,1,a,2001to2004;//往边界施加对象，引用边界号，该类型引用节点号
    # Boundary,3,MSTSLV,1002,1,1,1,1,0,1;//建立边界，MSTSLV类型，该类型会引用节点号，为主节点
    # AsgnBd,3,a,17;//往边界施加对象，引用边界号，该类型引用节点号，为从节点
    # Boundary,4,MSTSLV,1003,0,1,1,1,0,1
    # AsgnBd,4,a,43
    # Boundary,6,MSTSLV,1002,1,1,1,1,1,1
    # AsgnBd,6,a,16,18
    # Boundary,7,MSTSLV,1003,1,1,1,1,1,1
    # AsgnBd,7,a,42,44
    # Boundary,8,MSTSLV,1001,0,1,1,1,0,1
    # AsgnBd,8,a,2
    # Boundary,9,MSTSLV,1004,0,1,1,1,0,1
    # AsgnBd,9,a,58
    # BdGrp,边墩临时支持,c;//建立边界组名字
    # BdGrp,边墩临时支持,a,8,9;//往边界组里面加数据，引用边界号，边界组组名
    # BdGrp,成桥支座,c
    # BdGrp,成桥支座,a,2to5
    # BdGrp,墩底固结,c
    # BdGrp,墩底固结,a,1
    # BdGrp,主墩临时支持,c
    # BdGrp,主墩临时支持,a,6,7
    return [], []


if __name__ == "__main__":
    from ._0_engine import engine
    nodes = engine.node.all()
    node_nos = [n.no for n in nodes]
    bd_nos, bd_groups = build_boundaries(engine, node_nos)
    print(bd_nos)
    print(bd_groups)
    print(engine.boundary.all())
    print(engine.boundary.group.all())