# tests/case_stage_manager.py

"""
StageManager 接口测试（手动运行版）
"""
from pyosis.stage import stage_manager


# 测试用编号列表
TEST_NOS = [9999, 9998, 9997, 9996]


def reset():
    """刷新缓存"""
    stage_manager.refresh()


def cleanup_test_stages():
    """清理测试残留数据"""
    for no in TEST_NOS:
        stg = stage_manager.get(no)
        if stg is not None:
            try:
                stage_manager.delete(no)
            except:
                pass


def test_get_all():
    """测试获取全部施工阶段"""
    reset()
    all_stgs = stage_manager.all()
    assert isinstance(all_stgs, list), f"应返回list，实际{type(all_stgs)}"
    print(f"✓ 获取全部施工阶段成功，共 {len(all_stgs)} 个")


def test_create():
    """测试创建施工阶段"""
    reset()
    cleanup_test_stages()

    stage_manager.create(9999, "测试阶段1", 3.0)
    stg = stage_manager.get(9999)
    assert stg is not None, "阶段9999应存在"
    assert stg.name == "测试阶段1", f"名称应为'测试阶段1'，实际'{stg.name}'"
    assert stg.duration == 3.0, f"持续时间应为3.0，实际'{stg.duration}'"
    stage_manager.delete(9999)
    print("✓ 创建施工阶段成功")


def test_create_multiple():
    """测试创建多个施工阶段"""
    reset()
    cleanup_test_stages()

    stage_manager.create(9999, "测试阶段1", 3.0)
    stage_manager.create(9998, "测试阶段2", 5.0)
    stage_manager.create(9997, "测试阶段3", 7.0)

    stg1 = stage_manager.get(9999)
    stg2 = stage_manager.get(9998)
    stg3 = stage_manager.get(9997)

    assert stg1 is not None and stg1.name == "测试阶段1"
    assert stg2 is not None and stg2.name == "测试阶段2"
    assert stg3 is not None and stg3.name == "测试阶段3"

    stage_manager.delete(9999)
    stage_manager.delete(9998)
    stage_manager.delete(9997)
    print("✓ 创建多个施工阶段成功")


def test_delete():
    """测试删除施工阶段"""
    reset()
    cleanup_test_stages()

    stage_manager.create(9999, "待删除阶段", 3.0)
    assert stage_manager.get(9999) is not None
    stage_manager.delete(9999)
    assert stage_manager.get(9999) is None, "阶段应已删除"
    print("✓ 删除施工阶段成功")


def test_get_multiple():
    """测试批量查询施工阶段"""
    reset()
    cleanup_test_stages()

    stage_manager.create(9999, "测试阶段1", 3.0)
    stage_manager.create(9998, "测试阶段2", 5.0)

    results = stage_manager.get([9999, 9998, 9997])
    assert len(results) == 3, "应返回3个结果"
    assert results[0] is not None and results[0].name == "测试阶段1"
    assert results[1] is not None and results[1].name == "测试阶段2"
    assert results[2] is None, "不存在的阶段应返回None"

    stage_manager.delete(9999)
    stage_manager.delete(9998)
    print("✓ 批量查询施工阶段成功")


def test_insert():
    """测试插入施工阶段"""
    reset()
    cleanup_test_stages()

    stage_manager.create(9999, "原阶段", 3.0)
    stage_manager.insert(9999, 1, "后插阶段", 5.0)

    stg = stage_manager.get(9999)
    assert stg is not None
    assert stg.name == "原阶段"

    # 注意：插入后需要刷新获取最新列表
    reset()
    all_stgs = stage_manager.all()
    names = [s.name for s in all_stgs]
    assert "后插阶段" in names, f"后插阶段应存在，实际: {names}"

    cleanup_test_stages()
    print("✓ 插入施工阶段成功")


if __name__ == "__main__":
    print("开始测试 StageManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_create,
        test_create_multiple,
        test_delete,
        test_get_multiple,
        test_insert,
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
