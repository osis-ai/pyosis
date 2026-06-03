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
    prop = engine.prop
    
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
    # 创建三点坐标系
    prop.coord.create_three_point(
        99,
        n1.x, n1.y, n1.z,
        n2.x, n2.y, n2.z,
        n1.x, 1.0, 0.0,   # 第三点 y 方向偏移 1m，避免共线
    )
    prop.coord.renumber("99","100")
    # ── 坐标系 all / get / clear 测试 ──
    coord = prop.coord
    all_coords = coord.all()
    if len(all_coords) != 1:
        raise ValueError(f"coord.all() 期望 1 条，实际 {len(all_coords)}")
    c100 = coord.get(100)
    if c100 is None:
        raise ValueError("coord.get(100) 返回 None")
    _expect_attr(c100, "no", 100)
    _expect_attr(c100, "coor_sys_type", "TRIPT")
    if c100.p1.x != n1.x or c100.p2.x != n2.x:
        raise ValueError("坐标系点位与节点不一致")
    c_none = coord.get(999)
    if c_none is not None:
        raise ValueError("coord.get(999) 应为 None")
    cs = coord.get([100, 999])
    if cs[0].no != 100 or cs[1] is not None:
        raise ValueError("coord.get([100, 999]) 返回不符合预期")
    # 测 clear，会删掉 no=100
    coord.clear()
    if len(coord.all()) != 0:
        raise ValueError("coord.clear() 后应为空")
    # prop.coord.delete(100)
    # 测试：两点+旋转角空间坐标系（沿桥轴 n1→n2，编号 98）
    prop.coord.create_two_point_rotation(
        98,
        n1.x, n1.y, n1.z,
        n2.x, n2.y, n2.z,
        0.0,
    )
    prop.coord.renumber("98", "97")
    prop.coord.delete(97)
    # 获取所有节点
    nodes = node.all()
    if node.count() != len(nodes) or nodes == 0:
        raise ValueError("node.all()和len(nodes)数量不一致")
    # 获取指定编号的节点
    got = node.get(n15.no)
    _expect_attr(got, "no", n15.no)

    new_no = n15.no + 100
    node.renumber(n15.no, new_no)
    if node.get(n15.no) is not None:
        raise ValueError("renumber 后旧编号 get 应为 None")

    node.delete(new_no)
    if node.get(new_no) is not None:
        raise ValueError("delete 后 get 应为 None")



    return [n1.no, n2.no, n3.no, n4.no, n5.no, n6.no, n7.no,
            n8.no, n9.no, n10.no, n11.no, n12.no, n13.no, n14.no]

if __name__ == "__main__":
    from _0_engine import engine
    engine.node.clear()
    node_nos = build_nodes(engine)
    print(node_nos)
    print(engine.node.all())
