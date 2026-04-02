# tests/case_load_manager.py

"""
LoadManager 接口测试（手动运行版）
"""
from pyosis.load import load_manager


# 测试用名称列表
TEST_NAMES = ["TestLoadCase1", "TestLoadCase2", "TestLoadCase3", "待删除"]


def reset():
    """刷新缓存"""
    load_manager.refresh()


def cleanup_test_loadcases():
    """清理测试残留数据"""
    for name in TEST_NAMES:
        lc = load_manager.get(name)
        if lc is not None:
            try:
                load_manager.delete_loadcase(name)
            except:
                pass


def test_get_all():
    """测试获取全部荷载工况"""
    reset()
    all_lcs = load_manager.all()
    assert isinstance(all_lcs, list), f"应返回list，实际{type(all_lcs)}"
    print(f"✓ 获取全部荷载工况成功，共 {len(all_lcs)} 个")


def test_create_loadcase():
    """测试创建荷载工况"""
    reset()
    cleanup_test_loadcases()

    load_manager.create_loadcase("TestLoadCase1", "USER", 1.0, "测试工况")
    lc = load_manager.get("TestLoadCase1")
    assert lc is not None, "工况TestLoadCase1应存在"
    assert lc.name == "TestLoadCase1", f"名称应为'TestLoadCase1'，实际'{lc.name}'"
    load_manager.delete_loadcase("TestLoadCase1")
    print("✓ 创建荷载工况成功")


if __name__ == "__main__":
    print("开始测试 LoadManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_create_loadcase,
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
