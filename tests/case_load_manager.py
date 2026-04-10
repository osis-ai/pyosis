# tests/case_load_manager.py

"""
LoadManager / LoadCaseManager 接口测试（手动运行版）

说明：添加荷载前须先存在对应荷载工况；节点力相关用例假定模型中存在节点 1、2。
"""

from pyosis.load import load_manager


# 测试用荷载工况名称（cleanup 会尝试全部删除）
TEST_NAMES = [
    "PyTest_LoadCase_Create",
    "PyTest_LoadCase_Renamed",
    "PyTest_LoadCase_M1",
    "PyTest_LoadCase_M2",
    "PyTest_LoadCase_Del",
    "PyTest_LoadCase_LoadOps",
]

TEST_NODE = 1
TEST_NODE_OTHER = 2


def reset():
    """刷新缓存"""
    load_manager.refresh()


def cleanup_test_loadcases():
    """清理测试残留数据"""
    for name in TEST_NAMES:
        lc = load_manager.get(name)
        if lc is not None:
            try:
                load_manager.delete(name)
            except:
                pass


def _lc_for_name(name: str):
    """创建工况后解析 LoadCaseManager """
    load_manager.create(name, "USER")
    lc = load_manager.get(name)
    if lc is None:
        load_manager.refresh()
        lc = load_manager.get(name)
    assert lc is not None, f"工况{name}应存在"
    return lc


# ──────────────────────────────────────────────
# LoadManager（荷载工况）
# ──────────────────────────────────────────────


def test_get_all():
    """测试获取全部荷载工况"""
    reset()
    all_lcs = load_manager.all()
    assert isinstance(all_lcs, list), f"应返回list，实际{type(all_lcs)}"
    print(f"✓ 获取全部荷载工况成功，共 {len(all_lcs)} 个")


def test_count_matches_all():
    """测试 count 与 all 长度一致"""
    reset()
    assert load_manager.count() == len(load_manager.all()), "count 应等于 len(all())"
    print("✓ count 与 all 一致")


def test_get_missing_returns_none():
    """测试查询不存在的工况"""
    reset()
    assert load_manager.get("__surely_missing_loadcase__") is None, "不存在的工况应返回 None"
    print("✓ 查询不存在工况返回 None")


def test_create_loadcase():
    """测试创建荷载工况"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_Create"
    lc = load_manager.create(name, "USER", 1.0, "pytest")
    if lc is None:
        load_manager.refresh()
        lc = load_manager.get(name)
    assert lc is not None, "创建后应能取得 LoadCaseManager"
    assert lc.name == name, f"名称应为'{name}'，实际'{lc.name}'"

    # load_manager.delete(name)
    # assert load_manager.get(name) is None, "删除后应查不到该工况"
    print("✓ 创建荷载工况成功")


def test_rename_loadcase():
    """测试重命名荷载工况"""
    reset()
    cleanup_test_loadcases()

    old = "PyTest_LoadCase_Create"
    new = "PyTest_LoadCase_Renamed"
    _lc_for_name(old)
    lc_new = load_manager.rename(old, new)
    if lc_new is None:
        load_manager.refresh()
        lc_new = load_manager.get(new)
    assert lc_new is not None and lc_new.name == new
    assert load_manager.get(old) is None, "旧名称应不存在"

    load_manager.delete(new)
    print("✓ 重命名荷载工况成功")


def test_delete_loadcase():
    """测试删除荷载工况"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_Del"
    _lc_for_name(name)
    assert load_manager.get(name) is not None
    load_manager.delete(name)
    assert load_manager.get(name) is None, "工况应已删除"
    print("✓ 删除荷载工况成功")


def test_get_multiple():
    """测试批量查询荷载工况"""
    reset()
    cleanup_test_loadcases()

    m1 = "PyTest_LoadCase_M1"
    m2 = "PyTest_LoadCase_M2"
    _lc_for_name(m1)
    _lc_for_name(m2)

    results = load_manager.get([m1, m2, "__missing__"])
    assert len(results) == 3, "应返回3个结果"
    assert results[0] is not None and results[0].name == m1
    assert results[1] is not None and results[1].name == m2
    assert results[2] is None, "不存在的工况应返回None"

    load_manager.delete(m1)
    load_manager.delete(m2)
    print("✓ 批量查询荷载工况成功")


# ──────────────────────────────────────────────
# LoadCaseManager（工况下的荷载）
# ──────────────────────────────────────────────


def test_loadcase_create_gravity():
    """测试添加自重荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    gravity = lc.create_gravity(1.0, 1.0, 1.0)
    assert gravity.name == name, "创建自重载荷失败,名称不匹配"
    load_manager.delete(name)
    print("✓ 添加自重荷载成功")


def test_loadcase_get_load_data():
    """测试查询工况下荷载数据"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    data = lc.get()
    assert isinstance(data, dict), f"荷载数据应为 dict，实际{type(data)}"
    load_manager.delete(name)
    print("✓ 查询工况荷载数据成功")


def test_loadcase_delete_nforce_requires_entity():
    """测试删除节点力必须指定 entity"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    try:
        lc.delete("NFORCE")
    except TypeError:
        pass
    else:
        raise AssertionError("应对省略 entity 的 NFORCE 删除抛出 TypeError")
    load_manager.delete(name)
    print("✓ 删除 NFORCE 缺少 entity 时抛出 TypeError")


def test_loadcase_create_delete_nforce():
    """测试节点力添加与删除（依赖模型存在节点 TEST_NODE）"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    lc.create_nforce(TEST_NODE, 100.0, 0, 0, 0, 0, 0)
    lc.delete("NFORCE", entity=TEST_NODE)
    load_manager.delete(name)
    print("✓ 节点力添加与删除成功")


def test_loadcase_modify_nforce():
    """测试修改节点力作用节点（依赖节点 TEST_NODE、TEST_NODE_OTHER）"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    lc.create_nforce(TEST_NODE, 50.0, 0, 0, 0, 0, 0)
    lc.modify("NFORCE", TEST_NODE, TEST_NODE_OTHER)
    lc.delete("NFORCE", entity=TEST_NODE_OTHER)
    load_manager.delete(name)
    print("✓ 修改节点力作用节点成功")


def test_loadcase_delete_gravity():
    """测试删除自重荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    lc.create_gravity(1.0, 1.0, 1.0)
    lc.delete("GRAVITY")
    load_manager.delete(name)
    print("✓ 删除自重荷载成功")


if __name__ == "__main__":
    print("开始测试 LoadManager / LoadCaseManager...")
    print("=" * 50)

    tests = [
        # LoadManager
        test_get_all,
        test_count_matches_all,
        test_get_missing_returns_none,
        test_create_loadcase,
        test_rename_loadcase,
        test_delete_loadcase,
        test_get_multiple,
        # # LoadCaseManager
        test_loadcase_create_gravity,
        test_loadcase_get_load_data,
        test_loadcase_delete_nforce_requires_entity,
        test_loadcase_create_delete_nforce,
        test_loadcase_modify_nforce,
        test_loadcase_delete_gravity,
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