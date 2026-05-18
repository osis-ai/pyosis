from typing import Any

from pyosis.core.engine import OSISEngine

def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"节点属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

def build_nodes(engine: OSISEngine) -> list[int]:
    """创建节点，返回节点编号列表 [1, 2, ..., 15]
    
    节点编号（显式定义，幂等执行）：
    - 1-15: 沿桥梁纵向的节点
    """
    node = engine.node
    
    # 显式编号创建节点
    n1  = node.create(0.0300, 0.0000, 0.0000, no=1)
    _expect_attr(n1, "no", 1)
    n2  = node.create(0.4600, 0.0000, 0.0000, no=2)
    _expect_attr(n2, "no", 2)
    n3  = node.create(0.6800, 0.0000, 0.0000, no=3)
    _expect_attr(n3, "no", 3)
    n4  = node.create(1.6800, 0.0000, 0.0000, no=4)
    _expect_attr(n4, "no", 4)
    n5  = node.create(2.8400, 0.0000, 0.0000, no=5)
    _expect_attr(n5, "no", 5)
    n6  = node.create(4.0000, 0.0000, 0.0000, no=6)
    _expect_attr(n6, "no", 6)
    n7  = node.create(6.0000, 0.0000, 0.0000, no=7)
    _expect_attr(n7, "no", 7)
    n8  = node.create(8.0000, 0.0000, 0.0000, no=8)
    _expect_attr(n8, "no", 8)
    n9  = node.create(10.0000, 0.0000, 0.0000, no=9)
    _expect_attr(n9, "no", 9)
    n10 = node.create(12.0000, 0.0000, 0.0000, no=10)
    _expect_attr(n10, "no", 10)
    n11 = node.create(13.1600, 0.0000, 0.0000, no=11)
    _expect_attr(n11, "no", 11)
    n12 = node.create(14.3200, 0.0000, 0.0000, no=12)
    _expect_attr(n12, "no", 12)
    n13 = node.create(15.3200, 0.0000, 0.0000, no=13)
    _expect_attr(n13, "no", 13)
    n14 = node.create(15.5400, 0.0000, 0.0000, no=14)
    _expect_attr(n14, "no", 14)
    n15 = node.create(15.9700, 0.0000, 0.0000, no=15)
    _expect_attr(n15, "no", 15)
    # 获取所有节点
    nodes = node.all()
    if len(nodes) != 15:
        raise ValueError("node.all()应存在 15 条节点")
    # 获取指定编号的节点
    node_by_no = node.get(n15.no)
    _expect_attr(node_by_no, "no", n15.no)
    # 删除节点
    node.delete(n15.no)
    if len(node.all()) != 14:
        raise ValueError("node.all应存在 14 条节点")


    return [n1.no, n2.no, n3.no, n4.no, n5.no, n6.no, n7.no,
            n8.no, n9.no, n10.no, n11.no, n12.no, n13.no, n14.no]

if __name__ == "__main__":
    from ._0_engine import engine
    node_nos = build_nodes(engine)
    print(node_nos)
    print(engine.node.all())
