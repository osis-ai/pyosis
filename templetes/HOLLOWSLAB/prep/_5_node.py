from pyosis.core.engine import OSISEngine

def build_nodes(engine: OSISEngine) -> list[int]:
    """创建节点，返回节点编号列表 [1, 2, ..., 15]
    
    节点编号（显式定义，幂等执行）：
    - 1-15: 沿桥梁纵向的节点
    """
    node = engine.node
    
    # 显式编号创建节点
    n1  = node.create(0.0300, 0.0000, 0.0000, no=1)
    n2  = node.create(0.4600, 0.0000, 0.0000, no=2)
    n3  = node.create(0.6800, 0.0000, 0.0000, no=3)
    n4  = node.create(1.6800, 0.0000, 0.0000, no=4)
    n5  = node.create(2.8400, 0.0000, 0.0000, no=5)
    n6  = node.create(4.0000, 0.0000, 0.0000, no=6)
    n7  = node.create(6.0000, 0.0000, 0.0000, no=7)
    n8  = node.create(8.0000, 0.0000, 0.0000, no=8)
    n9  = node.create(10.0000, 0.0000, 0.0000, no=9)
    n10 = node.create(12.0000, 0.0000, 0.0000, no=10)
    n11 = node.create(13.1600, 0.0000, 0.0000, no=11)
    n12 = node.create(14.3200, 0.0000, 0.0000, no=12)
    n13 = node.create(15.3200, 0.0000, 0.0000, no=13)
    n14 = node.create(15.5400, 0.0000, 0.0000, no=14)
    n15 = node.create(15.9700, 0.0000, 0.0000, no=15)
    
    return [n1.no, n2.no, n3.no, n4.no, n5.no, n6.no, n7.no,
            n8.no, n9.no, n10.no, n11.no, n12.no, n13.no, n14.no, n15.no]

if __name__ == "__main__":
    from ._0_engine import engine
    node_nos = build_nodes(engine)
    print(node_nos)
    print(engine.node.all())
