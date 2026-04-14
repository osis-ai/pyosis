# tests/case_stage_manager.py

"""
StageManager 接口测试（手动运行版）
"""
import traceback

from pyosis.stage import stage_manager


def cleanup_test_stages(created_nos: list[int]):
    """清理测试残留数据"""
    for no in created_nos:
        stg = stage_manager.get(no)
        if stg is not None:
            try:
                stage_manager.delete(no)
            except:
                pass


def test_get_all():
    """测试获取全部施工阶段"""
    stage_manager.refresh()
    all_stgs = stage_manager.all()
    assert isinstance(all_stgs, list), f"应返回list，实际{type(all_stgs)}"
    print(f"✓ 获取全部施工阶段成功，共 {len(all_stgs)} 个")


def test_create():
    """测试创建施工阶段"""
    stage_manager.refresh()
    created_nos: list[int] = []

    stg = stage_manager.create("测试阶段1", 3.0)
    assert stg is not None, "应返回阶段对象"
    created_nos.append(stg.no)

    stg_check = stage_manager.get(stg.no)
    assert stg_check is not None, f"阶段{stg.no}应存在"
    assert stg_check.name == "测试阶段1", f"名称应为'测试阶段1'，实际'{stg_check.name}'"
    assert stg_check.duration == 3.0, f"持续时间应为3.0，实际'{stg_check.duration}'"
    print(f"✓ 创建施工阶段成功, no={stg.no}")

    cleanup_test_stages(created_nos)


def test_create_multiple():
    """测试创建多个施工阶段"""
    stage_manager.refresh()
    created_nos: list[int] = []

    stg1 = stage_manager.create("测试阶段1", 3.0)
    created_nos.append(stg1.no)
    stg2 = stage_manager.create("测试阶段2", 5.0)
    created_nos.append(stg2.no)
    stg3 = stage_manager.create("测试阶段3", 7.0)
    created_nos.append(stg3.no)

    stg1_check = stage_manager.get(stg1.no)
    stg2_check = stage_manager.get(stg2.no)
    stg3_check = stage_manager.get(stg3.no)

    assert stg1_check is not None and stg1_check.name == "测试阶段1"
    assert stg2_check is not None and stg2_check.name == "测试阶段2"
    assert stg3_check is not None and stg3_check.name == "测试阶段3"

    print(f"✓ 创建多个施工阶段成功, nos={created_nos}")

    cleanup_test_stages(created_nos)


def test_delete():
    """测试删除施工阶段"""
    stage_manager.refresh()
    created_nos: list[int] = []

    stg = stage_manager.create("待删除阶段", 3.0)
    created_nos.append(stg.no)
    assert stage_manager.get(stg.no) is not None
    stage_manager.delete(stg.no)
    assert stage_manager.get(stg.no) is None, "阶段应已删除"
    print("✓ 删除施工阶段成功")

    cleanup_test_stages(created_nos)


def test_get_multiple():
    """测试批量查询施工阶段"""
    stage_manager.refresh()
    created_nos: list[int] = []

    stg1 = stage_manager.create("测试阶段1", 3.0)
    created_nos.append(stg1.no)
    stg2 = stage_manager.create("测试阶段2", 5.0)
    created_nos.append(stg2.no)

    results = stage_manager.get([stg1.no, stg2.no, 99999])
    assert len(results) == 3, "应返回3个结果"
    assert results[0] is not None and results[0].name == "测试阶段1"
    assert results[1] is not None and results[1].name == "测试阶段2"
    assert results[2] is None, "不存在的阶段应返回None"

    print(f"✓ 批量查询施工阶段成功")

    cleanup_test_stages(created_nos)


def test_insert():
    """测试插入施工阶段"""
    stage_manager.refresh()
    created_nos: list[int] = []

    stg1 = stage_manager.create("原阶段", 3.0)
    created_nos.append(stg1.no)

    stg2 = stage_manager.insert(stg1.no, 1, "后插阶段", 5.0)
    created_nos.append(stg2.no)

    stg1_check = stage_manager.get(stg1.no)
    assert stg1_check is not None
    assert stg1_check.name == "原阶段"

    print(f"✓ 插入施工阶段成功")

    cleanup_test_stages(created_nos)


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
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 50)
    print(f"测试完成: {passed} 通过, {failed} 失败")
