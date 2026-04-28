"""节点"""

from pyosis.core.engine import OSISEngine

def build_nodes(engine: OSISEngine) -> list[int]:
    """节点"""

    node_nos = []

    # [Node] Node
    # 原始命令: Node,1,0.0,0.0,0.0
    # 参数:
    #   no=1
    #   x=0.0
    #   y=0.0
    #   z=0.0
    engine.node.create(no=1, x=0, y=0, z=0)

    # [Node] Node
    # 原始命令: Node,2,5.0,0.0,0.0
    # 参数:
    #   no=2
    #   x=5.0
    #   y=0.0
    #   z=0.0
    engine.node.create(no=2, x=5, y=0, z=0)

    # [Node] Node
    # 原始命令: Node,3,10.0,0.0,0.0
    # 参数:
    #   no=3
    #   x=10.0
    #   y=0.0
    #   z=0.0
    engine.node.create(no=3, x=10, y=0, z=0)

    # [Node] Node
    # 原始命令: Node,4,15.0,0.0,0.0
    # 参数:
    #   no=4
    #   x=15.0
    #   y=0.0
    #   z=0.0
    engine.node.create(no=4, x=15, y=0, z=0)

    return node_nos

if __name__ == "__main__":
    from ._0_engine import engine
    node_nos = build_nodes(engine)
    print(node_nos)
    print(engine.node.all())