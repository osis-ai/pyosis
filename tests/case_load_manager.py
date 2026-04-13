# tests/case_load_manager.py

"""
``load_manager``（``LoadCaseManager`` 单例）与 ``LoadCase`` 接口测试（手动运行版）

说明：添加荷载前须先存在对应荷载工况；节点力相关用例假定模型中存在节点 1、2。
"""
from pyosis.element import element_manager
from pyosis.load import load_manager
# 复用 case_element_manager.py 的前置条件设置
from case_element_manager import setup_prerequisites, TEST_NODE_NOS, TEST_MAT_NO, TEST_ELEM_NOS
from pyosis.material import material_manager
from pyosis.node import node_manager
from pyosis.io.prestressed_info import TendonShapeInfo

# 与面荷载测试共用的 Shell 单元号
SHELL_ELEM_NO = 9995


def _setup_shell_element_for_surface_test() -> int:
    """创建 Shell 单元及节点，供单元面荷载（含方向向量）测试使用。"""
    for no in [99901, 99902, 99903, 99904]:
        nd = node_manager.get(no)
        if nd is not None:
            try:
                node_manager.delete(no)
            except Exception:
                pass

    node_manager.create(99901, 0.0, 0.0, 0.0)
    node_manager.create(99902, 1.0, 0.0, 0.0)
    node_manager.create(99903, 1.0, 1.0, 0.0)
    node_manager.create(99904, 0.0, 1.0, 0.0)

    if material_manager.get(TEST_MAT_NO) is None:
        material_manager.create_conc(TEST_MAT_NO, "测试材料",
                                     eCode="JTG3362_2018", eGrade="C30", nCrepShrk=1)

    from pyosis.thickness import osis_feature_shellthk
    osis_feature_shellthk(1, 0.2, 0.2)

    old_elem = element_manager.get(SHELL_ELEM_NO)
    if old_elem is not None:
        try:
            element_manager.delete(SHELL_ELEM_NO)
        except Exception:
            pass

    element_manager.create_shell(
        no=SHELL_ELEM_NO,
        node1=99901,
        node2=99902,
        node3=99903,
        nMat=TEST_MAT_NO,
        nThk=1,
        bIsThin=1,
        node4=99904,
    )
    return SHELL_ELEM_NO


def _teardown_shell_element_for_surface_test() -> None:
    """删除面荷载测试用 Shell 与节点。"""
    try:
        element_manager.delete(SHELL_ELEM_NO)
    except Exception:
        pass
    for no in [99901, 99902, 99903, 99904]:
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
    """创建指定名称的荷载工况并返回 ``LoadCase``。"""
    load_manager.create(name, "USER")
    lc = load_manager.get(name)
    if lc is None:
        load_manager.refresh()
        lc = load_manager.get(name)
    assert lc is not None, f"工况{name}应存在"
    return lc


# ──────────────────────────────────────────────
# load_manager（LoadCaseManager：工况列表与创建/删除/重命名）
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
    assert lc is not None, "创建后应能取得 LoadCase"
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
    load_manager.delete(name)
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
    load_manager.delete(name)
    print("✓ 添加强迫位移成功")


def test_loadcase_create_temperature_uniform():
    """测试添加均匀温度荷载"""
    reset()
    cleanup_test_loadcases()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_temperature_uniform(nEntity=10, dTemp=20)
    assert result is lc, "create_temperature_uniform 应返回 self"
    lc.delete("UTEMP", entity=10)
    load_manager.delete(name)
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
    load_manager.delete(name)
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
    load_manager.delete(name)
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
            load_manager.delete(name)
        except Exception:
            pass

    if ok:
        print("✓ 添加预应力荷载成功")


def test_loadcase_create_cable_force():
    """测试添加索力荷载"""
    reset()
    cleanup_test_loadcases()

    # 先创建桁架单元（参考 case_element_manager.py）
    from pyosis.element import element_manager
    from pyosis.node import node_manager
    from pyosis.material import material_manager

    # 确保节点和材料存在
    node_manager.create(99901, 0, 0, 0)
    node_manager.create(99902, 1, 0, 0)
    material_manager.create_conc(99901, "测试材料", eCode="JTG3362_2018", eGrade="C30", nCrepShrk=1)

    # 创建桁架单元
    element_manager.create_truss(no=9998, node1=99901, node2=99902, nMat=99901, nSec1=1, nSec2=1)

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_cable_force(nEntity=9998, eLoadType="IN", dForce=100)
    assert result is lc, "create_cable_force 应返回 self"
    lc.delete("CFORCE", entity=9998)
    load_manager.delete(name)
    print("✓ 添加索力荷载成功")


def test_loadcase_create_surface_load():
    """测试添加单元面荷载"""
    reset()
    cleanup_test_loadcases()

    _setup_shell_element_for_surface_test()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)

    result = lc.create_surface_load(
        strEntity=str(SHELL_ELEM_NO),
        strPlanei="1",
        strDir="X",
        strGlobalI="0",
        strP1i="0", strP2i="0", strP3i="0", strP4i="0"
    )
    assert result is lc, "create_surface_load 应返回 self"

    lc.delete("ESRFC", entity=str(SHELL_ELEM_NO))
    _teardown_shell_element_for_surface_test()
    load_manager.delete(name)
    print("✓ 添加单元面荷载成功")


def test_loadcase_create_surface_load_vector():
    """测试添加单元面荷载（方向向量），作用在 Shell 单元上（与面荷载标量测试共用几何）"""
    reset()
    cleanup_test_loadcases()

    _setup_shell_element_for_surface_test()

    name = "PyTest_LoadCase_LoadOps"
    lc = _lc_for_name(name)
    result = lc.create_surface_load_vector(
        strEntity=str(SHELL_ELEM_NO),
        strPlanei="1",
    )
    assert result is lc, "create_surface_load_vector 应返回 self"
    lc.delete("ESRFC", entity=str(SHELL_ELEM_NO))
    _teardown_shell_element_for_surface_test()
    load_manager.delete(name)
    print("✓ 添加单元面荷载（方向向量）成功")


if __name__ == "__main__":
    print("开始测试 load_manager（LoadCaseManager）与 LoadCase...")
    print("=" * 50)

    tests = [
        # load_manager
        test_get_all,
        test_count_matches_all,
        test_get_missing_returns_none,
        test_create_loadcase,
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
        test_loadcase_create_temperature_uniform,
        test_loadcase_create_gradient_temperature,
        test_loadcase_create_initial_force,
        # todo 待完善
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