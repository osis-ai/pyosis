# tests/case_stage_manager.py

"""
StageManager 接口测试（手动运行版）
"""
import traceback

from pyosis.stage import stage_manager
from pyosis.element import osis_element_group, element_manager
from pyosis.boundary import boundary_manager
from pyosis.load import loadcase_manager

# 测试用固定名称（与 stage 测试中的字符串一致）
_TEST_ELE_GROUP = "墩"
_TEST_BD_GROUP = "固结"
_TEST_LC_NAME = "自定义工况1"


def setup_test_data():
    """创建测试所需的前置数据。

    仅把**本次实际新建成功**的资源记入 created，以便 teardown 删除；
    若模型中已存在同名资源，则复用，不记入 created（避免误删用户数据）。
    """
    created = {"element_groups": [], "boundary_groups": [], "load_cases": []}

    # 单元组
    ok, err = element_manager.group.create(_TEST_ELE_GROUP)
    if ok:
        created["element_groups"].append(_TEST_ELE_GROUP)
    else:
        err_s = str(err or "")
        if "已存在" not in err_s:
            raise RuntimeError(f"单元组创建失败: {err}")

    # 边界组（group 失败时抛 RuntimeError）
    try:
        boundary_manager.group.create(_TEST_BD_GROUP)
        created["boundary_groups"].append(_TEST_BD_GROUP)
    except RuntimeError as e:
        if "已存在" not in str(e):
            raise

    # 荷载工况
    try:
        lc = loadcase_manager.create(_TEST_LC_NAME, 'USER')
        if lc is not None:
            created["load_cases"].append(_TEST_LC_NAME)
    except RuntimeError as e:
        if "已存在" not in str(e) and "存在" not in str(e):
            raise

    return created


def teardown_test_data(created: dict):
    """清理测试创建的前置数据"""
    for name in created["element_groups"]:
        element_manager.group.delete(name)

    for name in created["boundary_groups"]:
        boundary_manager.group.delete(name)

    for name in created["load_cases"]:
        if loadcase_manager.get(name) is not None:
            loadcase_manager.delete(name)


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

    all_stgs = stage_manager.all()
    assert isinstance(all_stgs, list), f"应返回list，实际{type(all_stgs)}"
    print(f"✓ 获取全部施工阶段成功，共 {len(all_stgs)} 个")


def test_create():
    """测试创建施工阶段"""

    created_nos: list[int] = []

    stg = stage_manager.create(1, "阶段1", 3.0)
    assert stg is not None, "应返回阶段对象"
    created_nos.append(stg.no)

    stg_check = stage_manager.get(stg.no)
    assert stg_check is not None, f"阶段{stg.no}应存在"
    assert stg_check.duration == 3.0, f"持续时间应为3.0，实际'{stg_check.duration}'"
    print(f"✓ 创建施工阶段成功, no={stg.no}")

    cleanup_test_stages(created_nos)


def test_create_multiple():
    """测试创建多个施工阶段"""

    created_nos: list[int] = []

    stg1 = stage_manager.create(2, "阶段2", 3.0)
    created_nos.append(stg1.no)
    stg2 = stage_manager.create(5.0)
    created_nos.append(stg2.no)
    stg3 = stage_manager.create(7.0)
    created_nos.append(stg3.no)

    stg1_check = stage_manager.get(stg1.no)
    stg2_check = stage_manager.get(stg2.no)
    stg3_check = stage_manager.get(stg3.no)

    assert stg1_check is not None and stg1_check.duration == 3.0
    assert stg2_check is not None and stg2_check.duration == 5.0
    assert stg3_check is not None and stg3_check.duration == 7.0

    print(f"✓ 创建多个施工阶段成功, nos={created_nos}")

    cleanup_test_stages(created_nos)


def test_delete():
    """测试删除施工阶段"""

    created_nos: list[int] = []

    stg = stage_manager.create(3, "阶段3", 3.0)
    created_nos.append(stg.no)
    assert stage_manager.get(stg.no) is not None
    stage_manager.delete(stg.no)
    assert stage_manager.get(stg.no) is None, "阶段应已删除"
    print("✓ 删除施工阶段成功")

    cleanup_test_stages(created_nos)


def test_get_multiple():
    """测试批量查询施工阶段"""

    created_nos: list[int] = []

    stg1 = stage_manager.create(4, "阶段4", 3.0)
    created_nos.append(stg1.no)
    stg2 = stage_manager.create(5.0)
    created_nos.append(stg2.no)

    results = stage_manager.get([stg1.no, stg2.no, 99999])
    assert len(results) == 3, "应返回3个结果"
    assert results[0] is not None and results[0].duration == 3.0
    assert results[1] is not None and results[1].duration == 5.0
    assert results[2] is None, "不存在的阶段应返回None"

    print(f"✓ 批量查询施工阶段成功")

    cleanup_test_stages(created_nos)


def test_insert():
    """测试插入施工阶段"""

    created_nos: list[int] = []

    stg1 = stage_manager.create(5, "阶段5", 3.0)
    created_nos.append(stg1.no)

    stg2 = stage_manager.insert(stg1.no, 1, 5.0)
    created_nos.append(stg2.no)

    stg1_check = stage_manager.get(stg1.no)
    assert stg1_check is not None

    print(f"✓ 插入施工阶段成功")

    cleanup_test_stages(created_nos)


def test_count():
    """测试获取施工阶段总数"""

    initial_count = stage_manager.count()

    stg = stage_manager.create(6, "阶段6", 3.0)
    try:
        new_count = stage_manager.count()
        assert new_count == initial_count + 1, f"计数应为{initial_count + 1}，实际{new_count}"
        print(f"✓ 获取施工阶段总数成功, count={new_count}")
    finally:
        stage_manager.delete(stg.no)


def test_remove():
    """测试移除插入的施工阶段"""

    created_nos: list[int] = []

    stg1 = stage_manager.create(7, "阶段7", 3.0)
    created_nos.append(stg1.no)
    stg2 = stage_manager.insert(stg1.no, 1, 5.0)
    created_nos.append(stg2.no)

    assert stage_manager.get(stg2.no) is not None, "插入的阶段应存在"
    stage_manager.remove(stg2.no)
    assert stage_manager.get(stg2.no) is None, "阶段应已移除"

    print(f"✓ 移除施工阶段成功")

    cleanup_test_stages(created_nos)


def test_activate_element():
    """测试激活单元"""

    created_stgs: list[int] = []
    test_data = setup_test_data()

    try:
        stg = stage_manager.create(8, "阶段8", 3.0)
        created_stgs.append(stg.no)

        stage_manager.activate_element(stg.no, "墩", 5.0)
        print(f"✓ 激活单元成功")
    finally:
        for no in created_stgs:
            try:
                stage_manager.delete(no)
            except:
                pass
        teardown_test_data(test_data)


def test_deactivate_element():
    """测试钝化单元"""

    created_stgs: list[int] = []
    test_data = setup_test_data()

    try:
        stg = stage_manager.create(9, "阶段9", 3.0)
        created_stgs.append(stg.no)

        stage_manager.deactivate_element(stg.no, "墩")
        print(f"✓ 钝化单元成功")
    finally:
        for no in created_stgs:
            try:
                stage_manager.delete(no)
            except:
                pass
        teardown_test_data(test_data)


def test_activate_boundary():
    """测试激活边界"""

    created_stgs: list[int] = []
    test_data = setup_test_data()

    try:
        stg = stage_manager.create(10, "阶段10", 3.0)
        created_stgs.append(stg.no)

        stage_manager.activate_boundary(stg.no, "固结")
        print(f"✓ 激活边界成功")
    finally:
        for no in created_stgs:
            try:
                stage_manager.delete(no)
            except:
                pass
        teardown_test_data(test_data)


def test_deactivate_boundary():
    """测试钝化边界"""

    created_stgs: list[int] = []
    test_data = setup_test_data()

    try:
        stg = stage_manager.create(11, "阶段11", 3.0)
        created_stgs.append(stg.no)

        stage_manager.deactivate_boundary(stg.no, "固结")
        print(f"✓ 钝化边界成功")
    finally:
        for no in created_stgs:
            try:
                stage_manager.delete(no)
            except:
                pass
        teardown_test_data(test_data)


def test_activate_loadcase():
    """测试激活荷载工况"""

    created_stgs: list[int] = []
    test_data = setup_test_data()

    try:
        stg = stage_manager.create(12, "阶段12", 3.0)
        created_stgs.append(stg.no)

        stage_manager.activate_loadcase(stg.no, "", "自定义工况1")
        print(f"✓ 激活荷载工况成功")
    finally:
        for no in created_stgs:
            try:
                stage_manager.delete(no)
            except:
                pass
        teardown_test_data(test_data)


def test_deactivate_loadcase():
    """测试钝化荷载工况"""

    created_stgs: list[int] = []
    test_data = setup_test_data()

    try:
        stg = stage_manager.create(13, "阶段13", 3.0)
        created_stgs.append(stg.no)

        stage_manager.deactivate_loadcase(stg.no, "", "自定义工况1")
        print(f"✓ 钝化荷载工况成功")
    finally:
        for no in created_stgs:
            try:
                stage_manager.delete(no)
            except:
                pass
        teardown_test_data(test_data)


def test_activate_analysis():
    """测试激活分析工况"""

    created_stgs: list[int] = []

    try:
        stg = stage_manager.create(14, "阶段14", 3.0)
        created_stgs.append(stg.no)

        stage_manager.activate_analysis(stg.no, "MODAL")
        print(f"✓ 激活分析工况成功")
    finally:
        for no in created_stgs:
            try:
                stage_manager.delete(no)
            except:
                pass


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
        test_count,
        test_refresh,
        test_remove,
        test_activate_element,
        test_deactivate_element,
        test_activate_boundary,
        test_deactivate_boundary,
        test_activate_loadcase,
        test_deactivate_loadcase,
        test_activate_analysis,
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
