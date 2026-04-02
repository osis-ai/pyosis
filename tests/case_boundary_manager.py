# tests/case_boundary_manager.py

from pyosis.boundary import boundary_manager


# 测试用编号列表
TEST_NOS = [9999, 9998, 9997, 9996, 9990, 9989]


def reset():
    """刷新缓存"""
    boundary_manager.refresh()


def cleanup_test_boundaries():
    """清理测试残留数据"""
    for no in TEST_NOS:
        bd = boundary_manager.get(no)
        if bd is not None:
            try:
                boundary_manager.delete(no)
            except:
                pass


def test_get_all():
    """测试获取全部边界"""
    reset()
    all_bds = boundary_manager.all()
    assert isinstance(all_bds, list), f"应返回list，实际{type(all_bds)}"
    print(f"✓ 获取全部边界成功，共 {len(all_bds)} 个")


def test_create_general():
    """测试创建一般边界"""
    reset()
    cleanup_test_boundaries()

    # 全约束
    boundary_manager.create_general(9999, bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)
    bd = boundary_manager.get(9999)
    assert bd is not None, "边界9999应存在"
    boundary_manager.delete(9999)
    print("✓ 创建一般边界(全约束)成功")

    # 部分约束
    boundary_manager.create_general(9998, bX=1, bY=1, bZ=0, bRX=0, bRY=0, bRZ=0, bRW=0)
    bd = boundary_manager.get(9998)
    assert bd is not None
    boundary_manager.delete(9998)
    print("✓ 创建一般边界(部分约束)成功")


def test_create_elstcspt():
    """测试创建弹性支承"""
    reset()
    cleanup_test_boundaries()

    boundary_manager.create_elstcspt(
        9997,
        bX=0, DX=1e10,
        bY=0, DY=1e10,
        bZ=1, DZ=1e13,
        bRX=1, RX=1e16,
        bRY=1, RY=1e16,
        bRZ=1, RZ=1e16,
    )
    bd = boundary_manager.get(9997)
    assert bd is not None, "边界9997应存在"
    boundary_manager.delete(9997)
    print("✓ 创建弹性支承成功")


def test_create_master_slave():
    """测试创建主从约束"""
    reset()
    cleanup_test_boundaries()

    boundary_manager.create_master_slave(
        9996,
        nNode=1,
        bX=1, bY=1, bZ=1,
        bRX=0, bRY=0, bRZ=0,
    )
    bd = boundary_manager.get(9996)
    assert bd is not None, "边界9996应存在"
    boundary_manager.delete(9996)
    print("✓ 创建主从约束成功")


def test_delete():
    """测试删除边界"""
    reset()
    cleanup_test_boundaries()

    boundary_manager.create_general(9989, bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)
    assert boundary_manager.get(9989) is not None
    boundary_manager.delete(9989)
    assert boundary_manager.get(9989) is None, "边界应已删除"
    print("✓ 删除边界成功")


def test_get_multiple():
    """测试批量查询边界"""
    reset()
    cleanup_test_boundaries()

    boundary_manager.create_general(9999, bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)
    boundary_manager.create_elstcspt(9998, bX=1, DX=1e10, bY=1, DY=1e10, bZ=1, DZ=1e13)

    results = boundary_manager.get([9999, 9998, 9997])
    assert len(results) == 3, "应返回3个结果"
    assert results[2] is None, "不存在的边界应返回None"

    boundary_manager.delete(9999)
    boundary_manager.delete(9998)
    print("✓ 批量查询边界成功")


if __name__ == "__main__":
    print("开始测试 BoundaryManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_create_general,
        test_create_elstcspt,
        test_create_master_slave,
        test_delete,
        test_get_multiple,
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
