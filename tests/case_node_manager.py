# tests/case_node_manager.py

from pyosis.node import node_manager


# 测试用编号列表
TEST_NOS = [9999, 9998, 9997, 9990, 9980, 9989]


def reset():
    """刷新缓存"""
    node_manager.refresh()


def cleanup_test_nodes():
    """清理测试残留数据"""
    for no in TEST_NOS:
        nd = node_manager.get(no)
        if nd is not None:
            try:
                node_manager.delete(no)
            except:
                pass


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
    cleanup_test_nodes()

    node = node_manager.create(9999, 1.0, 2.0, 3.0)
    nd = node_manager.get(9999)
    assert nd is not None, "节点9999应存在"
    assert nd.no == 9999
    assert nd.x == 1.0
    assert nd.y == 2.0
    assert nd.z == 3.0
    assert nd.coord == (1.0, 2.0, 3.0)
    node_manager.delete(9999)
    print("✓ 创建节点成功")


def test_modify():
    """测试修改节点坐标"""
    reset()
    cleanup_test_nodes()

    # 先创建
    node_manager.create(9998, 0.0, 0.0, 0.0)
    nd = node_manager.get(9998)
    assert nd is not None
    assert nd.coord == (0.0, 0.0, 0.0)

    # 再修改坐标
    node_manager.modify(9998, 10.0, 20.0, 30.0)
    nd = node_manager.get(9998)
    assert nd is not None
    assert nd.coord == (10.0, 20.0, 30.0)
    node_manager.delete(9998)
    print("✓ 修改节点坐标成功")


def test_renumber():
    """测试修改节点编号"""
    reset()
    cleanup_test_nodes()

    # 先创建
    node_manager.create(9990, 5.0, 5.0, 5.0)
    nd = node_manager.get(9990)
    assert nd is not None, "节点9990应存在"
    assert nd.coord == (5.0, 5.0, 5.0)

    # 修改编号
    node_manager.renumber(9990, 9980)
    assert node_manager.get(9990) is None, "旧编号9990应不存在"
    nd_new = node_manager.get(9980)
    assert nd_new is not None, "新编号9980应存在"
    assert nd_new.coord == (5.0, 5.0, 5.0)
    node_manager.delete(9980)
    print("✓ 修改节点编号成功")


def test_delete():
    """测试删除节点"""
    reset()
    cleanup_test_nodes()

    # 先创建
    node_manager.create(9989, 1.0, 1.0, 1.0)
    assert node_manager.get(9989) is not None

    # 再删除
    node_manager.delete(9989)
    assert node_manager.get(9989) is None, "节点应已删除"
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