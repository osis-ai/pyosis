"""边界条件"""

from pyosis.core.engine import OSISEngine

def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:
    """创建边界条件，返回边界编号列表和边界组名称列表"""

    bd_nos = []
    bd_group_names = []

    bd = engine.boundary.create_general(nCoor="", no=1)
    bd_nos.append(bd.no)

    bd.assign('a', ['2001to2004'])

    bd = engine.boundary.create_master_slave(nNode=1002, bRY=0, no=3)
    bd_nos.append(bd.no)

    bd.assign('a', [17])

    bd = engine.boundary.create_master_slave(nNode=1003, bX=0, bRY=0, no=4)
    bd_nos.append(bd.no)

    bd.assign('a', [43])

    bd = engine.boundary.create_master_slave(nNode=1002, no=6)
    bd_nos.append(bd.no)

    bd.assign('a', [16, 18])

    bd = engine.boundary.create_master_slave(nNode=1003, no=7)
    bd_nos.append(bd.no)

    bd.assign('a', [42, 44])

    bd = engine.boundary.create_master_slave(nNode=1001, bX=0, bRY=0, no=8)
    bd_nos.append(bd.no)

    bd.assign('a', [2])

    bd = engine.boundary.create_master_slave(nNode=1004, bX=0, bRY=0, no=9)
    bd_nos.append(bd.no)

    bd.assign('a', [58])

    bg = engine.boundary.group.create('边墩临时支持')
    bd_group_names.append(bg.name)

    bg.add([8, 9])

    bg = engine.boundary.group.create('成桥支座')
    bd_group_names.append(bg.name)

    bg.add(['2to5'])

    bg = engine.boundary.group.create('墩底固结')
    bd_group_names.append(bg.name)

    bg.add([1])

    bg = engine.boundary.group.create('主墩临时支持')
    bd_group_names.append(bg.name)

    bg.add([6, 7])

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