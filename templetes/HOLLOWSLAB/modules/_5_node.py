from pyosis.core.engine import OSISEngine

def build_nodes(engine: OSISEngine) -> list[int]:
    """创建节点，返回节点编号列表 [n1, n2, ..., n15]"""
    node = engine.node
    ns = []
    ns.append(node.create(0.0300,0.0000,0.0000))
    ns.append(node.create(0.4600,0.0000,0.0000))
    ns.append(node.create(0.6800,0.0000,0.0000))
    ns.append(node.create(1.6800,0.0000,0.0000))
    ns.append(node.create(2.8400,0.0000,0.0000))
    ns.append(node.create(4.0000,0.0000,0.0000))
    ns.append(node.create(6.0000,0.0000,0.0000))
    ns.append(node.create(8.0000,0.0000,0.0000))
    ns.append(node.create(10.0000,0.0000,0.0000))
    ns.append(node.create(12.0000,0.0000,0.0000))
    ns.append(node.create(13.1600,0.0000,0.0000))
    ns.append(node.create(14.3200,0.0000,0.0000))
    ns.append(node.create(15.3200,0.0000,0.0000))
    ns.append(node.create(15.5400,0.0000,0.0000))
    ns.append(node.create(15.9700,0.0000,0.0000))
    
    node_nos = [it.no for it in ns]
    return node_nos
