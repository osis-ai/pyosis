# tests/case_node_manager.py

from pyosis.node import node_manager


def reset():
    """刷新缓存"""
    node_manager.refresh()


def test_get_all():
    """测试获取全部节点"""
    reset()
    all_nodes = node_manager.all()
    assert isinstance(all_nodes, list), f"应返回list，实际{type(all_nodes)}"
    print(f"✓ 获取全部节点成功，共 {len(all_nodes)} 个")


def test_count():
    """测试节点计数"""
    reset()
    count = node_manager.count()
    assert count >= 0
    assert isinstance(count, int)
    print(f"✓ 节点计数成功: {count}")


def test_get():
    """测试按编号查询节点"""
    reset()
    all_nodes = node_manager.all()
    if all_nodes:
        nd = node_manager.get(all_nodes[0].no)
        assert nd is not None
        assert nd.no == all_nodes[0].no
        print(f"✓ 按编号查询成功: 节点{nd.no}, 坐标{nd.coord}")


def test_create():
    """测试创建节点"""
    reset()

    nd = node_manager.create(1.0, 2.0, 3.0)
    assert nd is not None
    assert nd.x == 1.0
    assert nd.y == 2.0
    assert nd.z == 3.0
    assert nd.coord == (1.0, 2.0, 3.0)
    node_manager.delete(nd.no)
    print(f"✓ 创建节点成功 (编号: {nd.no})")


def test_modify():
    """测试修改节点坐标"""
    reset()

    # 先创建
    nd = node_manager.create(0.0, 0.0, 0.0)
    assert nd is not None
    assert nd.coord == (0.0, 0.0, 0.0)

    # 再修改坐标
    node_manager.modify(nd.no, 10.0, 20.0, 30.0)
    nd = node_manager.get(nd.no)
    assert nd is not None
    assert nd.coord == (10.0, 20.0, 30.0)
    node_manager.delete(nd.no)
    print("✓ 修改节点坐标成功")


def test_renumber():
    """测试修改节点编号"""
    reset()

    # 先创建
    nd = node_manager.create(5.0, 5.0, 5.0)
    no_old = nd.no
    assert nd is not None
    assert nd.coord == (5.0, 5.0, 5.0)

    # 修改编号
    no_new = no_old + 1
    node_manager.renumber(no_old, no_new)
    assert node_manager.get(no_old) is None, "旧编号应不存在"
    nd_new = node_manager.get(no_new)
    assert nd_new is not None, "新编号应存在"
    assert nd_new.coord == (5.0, 5.0, 5.0)
    node_manager.delete(no_new)
    print(f"✓ 修改节点编号成功 ({no_old} -> {no_new})")


def test_delete():
    """测试删除节点"""
    reset()

    # 先创建
    nd = node_manager.create(1.0, 1.0, 1.0)
    assert node_manager.get(nd.no) is not None

    # 再删除
    node_manager.delete(nd.no)
    assert node_manager.get(nd.no) is None, "节点应已删除"
    print("✓ 删除节点成功")


if __name__ == "__main__":
    print("开始测试 NodeManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_count,
        test_get,
        test_create,
        test_modify,
        test_renumber,
        test_delete,
    ]

    passed = 0
    failed = 0

    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"✗ {t.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {t.__name__} 异常: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"测试完成: {passed} 通过, {failed} 失败")