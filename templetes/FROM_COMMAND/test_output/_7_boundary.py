"""边界条件"""

from pyosis.core.engine import OSISEngine

def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:
    """边界条件"""

    boundary_nos = []

    # [Boundary] 一般支撑
    # 原始命令: Boundary,1,GENERAL,0,1,1,1,1,1,1,1
    # 参数:
    #   no=GENERAL
    #   nCoor=0
    #   bX=1
    #   bY=1
    #   bZ=1
    #   bRX=1
    #   bRY=1
    #   bRZ=1
    #   bRW=1
    engine.boundary.create_general(no="GENERAL", nCoor=0, bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)

    # [Boundary] 一般支撑
    # 原始命令: Boundary,2,GENERAL,0,0,1,1,1,1,1,1
    # 参数:
    #   no=GENERAL
    #   nCoor=0
    #   bX=0
    #   bY=1
    #   bZ=1
    #   bRX=1
    #   bRY=1
    #   bRZ=1
    #   bRW=1
    engine.boundary.create_general(no="GENERAL", nCoor=0, bX=0, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)

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