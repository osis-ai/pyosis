# tests/case_load_manager.py

"""
``loadcase_manager``（``LoadCaseManager`` 单例）与 ``LoadCase`` 接口测试（手动运行版）

说明：添加荷载前须先存在对应荷载工况；节点力相关用例假定模型中存在节点 1、2。
"""
from pyosis.element import element_manager
from pyosis.load import loadcase_manager
from case_element_manager import ensure_pytest_material_no
from pyosis.node import node_manager
from pyosis.io.prestressed_info import TendonShapeInfo


def _setup_shell_element_for_surface_test() -> tuple[int, list[int]]:
    """创建 Shell 单元及节点，供单元面荷载（含方向向量）测试使用。

    Returns:
        (shell_elem_no, node_nos): 壳单元编号、四个角点节点编号列表
    """


    n1 = node_manager.create(0.0, 0.0, 0.0)
    n2 = node_manager.create(1.0, 0.0, 0.0)
    n3 = node_manager.create(1.0, 1.0, 0.0)
    n4 = node_manager.create(0.0, 1.0, 0.0)
    node_nos = [n1.no, n2.no, n3.no, n4.no]

    mat_no = ensure_pytest_material_no()

    from pyosis.thickness import osis_feature_shellthk
    osis_feature_shellthk(1, 0.2, 0.2)

    shell = element_manager.create_shell(
        node1=node_nos[0],
        node2=node_nos[1],
        node3=node_nos[2],
        nMat=mat_no,
        nThk=1,
        bIsThin=1,
        node4=node_nos[3],
    )
    return shell.no, node_nos


def _teardown_shell_element_for_surface_test(shell_no: int, node_nos: list[int]) -> None:
    """删除面荷载测试用 Shell 与节点。"""
    try:
        element_manager.delete(shell_no)
    except Exception:
        pass
    for no in node_nos:
        try:
            node_manager.delete(no)
        except Exception:
            pass


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

def cleanup_test_loadcases():
    """清理测试残留数据"""
    for name in TEST_NAMES:
        lc = loadcase_manager.get(name)
        if lc is not None:
            try:
                loadcase_manager.delete(name)
            except:
                pass


def _lc_for_name(name: str):
    """创建指定名称的荷载工况并返回 ``LoadCase``。"""
    loadcase_manager.create(load_case_type="USER", name=name)
    lc = loadcase_manager.get(name)
    if lc is None:

        lc = loadcase_manager.get(name)
    assert lc is not None, f"工况{name}应存在"
    return lc


# ──────────────────────────────────────────────
# loadcase_manager（LoadCaseManager：工况列表与创建/删除/重命名）
# ──────────────────────────────────────────────


def test_get_all():
    """测试获取全部荷载工况"""
    reset()
    all_lcs = loadcase_manager.all()
    assert isinstance(all_lcs, list), f"应返回list，实际{type(all_lcs)}"
    print(f"✓ 获取全部荷载工况成功，共 {len(all_lcs)} 个")


def test_count_matches_all():
    """测试 count 与 all 长度一致"""
    reset()
    assert loadcase_manager.count() == len(loadcase_manager.all()), "count 应等于 len(all())"
    print("✓ count 与 all 一致")


def test_get_missing_returns_none():
    """测试查询不存在的工况"""
    reset()
    assert loadcase_manager.get("__surely_missing_loadcase__") is None, "不存在的工况应返回 None"
    print("✓ 查询不存在工况返回 None")


def test_create_loadcase():
    """测试创建荷载工况（显式指定名称）"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_Create"
    lc = loadcase_manager.create(load_case_type="USER", scalar=1.0, prompt="pytest", name=name)
    if lc is None:

        lc = loadcase_manager.get(name)
    assert lc is not None, "创建后应能取得 LoadCase"
    assert lc.name == name, f"名称应为'{name}'，实际'{lc.name}'"

    # loadcase_manager.delete(name)
    # assert loadcase_manager.get(name) is None, "删除后应查不到该工况"
    print("✓ 创建荷载工况成功")


def test_create_loadcase_without_name():
    """测试创建荷载工况时不传 name（由管理器自动生成 LC_ 前缀名称）"""
    reset()

    lc = loadcase_manager.create(
        load_case_type="USER",
        scalar=1.0,
        prompt="pytest_auto_name",
    )
    assert lc is not None, "不传 name 时应返回 LoadCase"
    assert lc.name.startswith("LC_"), f"自动名称应以 LC_ 开头，实际: {lc.name!r}"
    assert len(lc.name) == 15, f"LC_ + 12 位 hex 共 15 字符，实际 len={len(lc.name)}: {lc.name!r}"

    again = loadcase_manager.get(lc.name)
    assert again is not None and again.name == lc.name, "应用自动名称能再次查询到该工况"

    loadcase_manager.delete(lc.name)
    assert loadcase_manager.get(lc.name) is None, "删除后应查不到该工况"

    print(f"✓ 不传 name 创建荷载工况成功: {lc.name}")


def test_rename_loadcase():
    """测试重命名荷载工况"""
    reset()
    cleanup_test_loadcases()

    old = "PyTest_LoadCase_Create"
    new = "PyTest_LoadCase_Renamed"
    _lc_for_name(old)
    lc_new = loadcase_manager.rename(old, new)
    if lc_new is None:

        lc_new = loadcase_manager.get(new)
    assert lc_new is not None and lc_new.name == new
    assert loadcase_manager.get(old) is None, "旧名称应不存在"

    loadcase_manager.delete(new)
    print("✓ 重命名荷载工况成功")


def test_delete_loadcase():
    """测试删除荷载工况"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_Del"
    _lc_for_name(name)
    assert loadcase_manager.get(name) is not None
    loadcase_manager.delete(name)
    assert loadcase_manager.get(name) is None, "工况应已删除"
    print("✓ 删除荷载工况成功")


def test_get_multiple():
    """测试批量查询荷载工况"""
    reset()
    cleanup_test_loadcases()

    m1 = "PyTest_LoadCase_M1"
    m2 = "PyTest_LoadCase_M2"
    _lc_for_name(m1)
    _lc_for_name(m2)

    results = loadcase_manager.get([m1, m2, "__missing__"])
    assert len(results) == 3, "应返回3个结果"
    assert results[0] is not None and results[0].name == m1
    assert results[1] is not None and results[1].name == m2
    assert results[2] is None, "不存在的工况应返回None"

    loadcase_manager.delete(m1)
    loadcase_manager.delete(m2)
    print("✓ 批量查询荷载工况成功")


# ──────────────────────────────────────────────
# LoadCase（工况下的荷载增删改查）
# ──────────────────────────────────────────────


def test_loadcase_create_gravity():
    """测试添加自重荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    lc_after = lc.create_gravity(1.0, 1.0, 1.0)
    assert lc_after.name == name, "创建自重荷载后应仍为同一工况，名称一致"
    loadcase_manager.delete(name)
    print("✓ 添加自重荷载成功")


def test_loadcase_get_load_data():
    """测试查询工况下荷载数据"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    lc.refresh()
    assert lc.name == name
    loadcase_manager.delete(name)
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
    loadcase_manager.delete(name)
    print("✓ 删除 NFORCE 缺少 entity 时抛出 TypeError")


def test_loadcase_create_delete_nforce():
    """测试节点力添加与删除（依赖模型存在节点 TEST_NODE）"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    lc.create_nforce(TEST_NODE, 100.0, 0, 0, 0, 0, 0)
    lc.delete("NFORCE", entity=TEST_NODE)
    loadcase_manager.delete(name)
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
    loadcase_manager.delete(name)
    print("✓ 修改节点力作用节点成功")


def test_loadcase_delete_gravity():
    """测试删除自重荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    lc.create_gravity(1.0, 1.0, 1.0)
    lc.delete("GRAVITY")
    loadcase_manager.delete(name)
    print("✓ 删除自重荷载成功")


def test_loadcase_create_line_load():
    """测试添加线荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_line_load(
        nEntity=10,
        dFXI=0, dFYI=-5,
        dOffsetXI=0.001,  # I端偏移量（非零）
        dOffsetXJ=1.0      # J端偏移量（要与I端不同）
    )
    assert result is lc, "create_line_load 应返回 self"
    loadcase_manager.delete(name)
    print("✓ 添加线荷载成功")


def test_loadcase_create_displacement():
    """测试添加强迫位移（依赖模型存在节点 TEST_NODE；命令为 15 段 b,d 格式）"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    # 单方向位移：内部应对应为 bDX=1, dDX=0.01，其余 b=0
    result = lc.create_displacement(nEntity=TEST_NODE, dDx=0.01)
    assert result is lc
    assert result.name == name, "应返回同一 LoadCase（链式 self）"
    lc.delete("DISPLACEMENT", entity=TEST_NODE)
    loadcase_manager.delete(name)
    print("✓ 添加强迫位移成功")


def test_loadcase_create_uniform_temperature():
    """测试添加均匀温度荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_uniform_temperature(nEntity=10, dTemp=20)
    assert result is lc, "create_uniform_temperature 应返回 self"
    lc.delete("UTEMP", entity=10)
    loadcase_manager.delete(name)
    print("✓ 添加均匀温度荷载成功")


def test_loadcase_create_gradient_temperature():
    """测试添加梯度温度荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_gradient_temperature(nEntity=10, param=[0.4, 10, 10, 0, 0])
    assert result is lc, "create_gradient_temperature 应返回 self"
    lc.delete("GTEMP", entity=10)
    loadcase_manager.delete(name)
    print("✓ 添加梯度温度荷载成功")


def test_loadcase_create_initial_force():
    """测试添加初始内力荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_initial_force(nEntity=10, dFXI=100, dFYI=0)
    assert result is lc, "create_initial_force 应返回 self"
    lc.delete("INITIAL", entity=10)
    loadcase_manager.delete(name)
    print("✓ 添加初始内力荷载成功")


def test_loadcase_create_prestress():
    """测试添加预应力荷载（使用当前模型中已有的一条钢束形状名称）"""
    reset()
    cleanup_test_loadcases()

    try:
        ts = TendonShapeInfo()
        shape_names = [n for n in ts.get_name_list() if n]
    except Exception:
        shape_names = []

    if not shape_names:
        print("○ 预应力荷载测试跳过（当前模型无钢束形状，请先在 OSIS 中定义钢束形状）")
        return

    str_entity = shape_names[0]
    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    ok = False
    try:
        result = lc.create_prestress(strEntity=str_entity, dBeg=100, dEnd=100)
        assert result is lc, "create_prestress 应返回 self"
        lc.delete("PST", entity=str_entity)
        ok = True
    except RuntimeError as e:
        print(f"○ 预应力荷载测试跳过: {e}")
    finally:
        try:
            loadcase_manager.delete(name)
        except Exception:
            pass

    if ok:
        print("✓ 添加预应力荷载成功")


def test_loadcase_create_cable_force():
    """测试添加索力荷载"""
    reset()
    cleanup_test_loadcases()

    from pyosis.element import element_manager
    from pyosis.node import node_manager

    n1 = node_manager.create(0.0, 0.0, 0.0)
    n2 = node_manager.create(1.0, 0.0, 0.0)
    mat_no = ensure_pytest_material_no()

    truss = element_manager.create_truss(
        node1=n1.no,
        node2=n2.no,
        nMat=mat_no,
        nSec1=1,
        nSec2=1,
    )

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_cable_force(nEntity=truss.no, eLoadType="IN", dForce=100)
    assert result is lc, "create_cable_force 应返回 self"
    lc.delete("CFORCE", entity=truss.no)
    loadcase_manager.delete(name)

    try:
        element_manager.delete(truss.no)
    except Exception:
        pass
    for no in (n1.no, n2.no):
        try:
            node_manager.delete(no)
        except Exception:
            pass

    print("✓ 添加索力荷载成功")


def test_loadcase_create_surface_load():
    """测试添加单元面荷载"""
    reset()
    cleanup_test_loadcases()

    shell_no, node_nos = _setup_shell_element_for_surface_test()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)

    result = lc.create_surface_load(
        strEntity=str(shell_no),
        strPlanei="1",
        strDir="X",
        strGlobalI="0",
        strP1i="0", strP2i="0", strP3i="0", strP4i="0"
    )
    assert result is lc, "create_surface_load 应返回 self"

    lc.delete("ESRFC", entity=str(shell_no))
    _teardown_shell_element_for_surface_test(shell_no, node_nos)
    loadcase_manager.delete(name)
    print("✓ 添加单元面荷载成功")


def test_loadcase_create_surface_load_vector():
    """测试添加单元面荷载（方向向量），作用在 Shell 单元上（与面荷载标量测试共用几何）"""
    reset()
    cleanup_test_loadcases()

    shell_no, node_nos = _setup_shell_element_for_surface_test()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_surface_load_vector(
        strEntity=str(shell_no),
        strPlanei="1",
    )
    assert result is lc, "create_surface_load_vector 应返回 self"
    lc.delete("ESRFC", entity=str(shell_no))
    _teardown_shell_element_for_surface_test(shell_no, node_nos)
    loadcase_manager.delete(name)
    print("✓ 添加单元面荷载（方向向量）成功")


if __name__ == "__main__":
    print("开始测试 loadcase_manager（LoadCaseManager）与 LoadCase...")
    print("=" * 50)

    tests = [
        # loadcase_manager
        test_get_all,
        test_count_matches_all,
        test_get_missing_returns_none,
        test_create_loadcase,
        test_create_loadcase_without_name,
        test_rename_loadcase,
        test_delete_loadcase,
        test_get_multiple,
        # LoadCase
        test_loadcase_create_gravity,
        test_loadcase_get_load_data,
        test_loadcase_delete_nforce_requires_entity,
        test_loadcase_create_delete_nforce,
        test_loadcase_modify_nforce,
        test_loadcase_delete_gravity,
        test_loadcase_create_line_load,
        test_loadcase_create_displacement,
        test_loadcase_create_uniform_temperature,
        test_loadcase_create_gradient_temperature,
        test_loadcase_create_initial_force,
        test_loadcase_create_prestress,
        test_loadcase_create_cable_force,
        test_loadcase_create_surface_load,
        test_loadcase_create_surface_load_vector,
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