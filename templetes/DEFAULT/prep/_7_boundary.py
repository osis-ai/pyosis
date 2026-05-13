"""边界条件"""

from pyosis.core.engine import OSISEngine

def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:
    """创建边界条件，返回边界编号列表和边界组名称列表"""

    bd_nos = []
    bd_group_names = []

    bd = engine.boundary.create_general(nCoor="", bRY=0, bRW=0, no=1)
    bd_nos.append(bd.no)

    bd.assign('a', [67])

    bd = engine.boundary.create_general(nCoor="", bX=0, bRY=0, bRW=0, no=2)
    bd_nos.append(bd.no)

    bd.assign('a', [23, 45, 89])

    bd = engine.boundary.create_general(nCoor="", bRY=0, bRW=0, no=3)
    bd_nos.append(bd.no)

    bd.assign('a', [21, 43, 65, 87, 91])

    bd = engine.boundary.create_general(nCoor="", bX=0, bRY=0, bRW=0, no=4)
    bd_nos.append(bd.no)

    bd.assign('a', [25, 47, 69])

    bd = engine.boundary.create_general(nCoor="", bX=0, bRY=0, bRW=0, no=5)
    bd_nos.append(bd.no)

    bd.assign('a', [2, 110])

    bg = engine.boundary.group.create('临时')
    bd_group_names.append(bg.name)

    bg.add(['3to4'])

    bg = engine.boundary.group.create('永久-边支座')
    bd_group_names.append(bg.name)

    bg.add([5])

    bg = engine.boundary.group.create('永久-中支座')
    bd_group_names.append(bg.name)

    bg.add(['1to2'])

    return bd_nos, bd_group_names


if __name__ == "__main__":
    from ._0_engine import engine
    nodes = engine.node.all()
    node_nos = [n.no for n in nodes]
    bd_nos, bd_groups = build_boundaries(engine, node_nos)
    print(bd_nos)
    print(bd_groups)
    print(engine.boundary.all())
    print(engine.boundary.group.all())