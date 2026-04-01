# tests/case_element_manager.py

"""
注意：单元创建依赖节点和材料，需先确保测试环境中有可用的节点和材料。
"""
from pyosis.element import element_manager
from pyosis.node import node_manager
from pyosis.material import material_manager


# 测试用编号列表
TEST_ELEM_NOS = [9999, 9998, 9997, 9996, 9995, 9990, 9980, 9989]
TEST_NODE_NOS = [99901, 99902, 99903, 99904, 99905]
TEST_MAT_NO = 99901


def reset_all():
    """刷新所有缓存"""
    node_manager.refresh()
    material_manager.refresh()
    element_manager.refresh()


def cleanup_test_data():
    """清理测试残留数据"""
    # 清理单元
    for no in TEST_ELEM_NOS:
        elem = element_manager.get(no)
        if elem is not None:
            try:
                element_manager.delete(no)
            except:
                pass

    # 清理节点
    for no in TEST_NODE_NOS:
        nd = node_manager.get(no)
        if nd is not None:
            try:
                node_manager.delete(no)
            except:
                pass

    # 清理材料
    mat = material_manager.get(TEST_MAT_NO)
    if mat is not None:
        try:
            material_manager.delete(TEST_MAT_NO)
        except:
            pass


def setup_prerequisites():
    """创建单元测试所需的前置条件（节点和材料）"""
    # 确保节点存在
    for i, no in enumerate(TEST_NODE_NOS[:5]):
        if node_manager.get(no) is None:
            node_manager.create(no, float(i), float(i), float(i))

    # 确保材料存在
    if material_manager.get(TEST_MAT_NO) is None:
        material_manager.create_conc(
            TEST_MAT_NO, "测试材料",
            eCode="JTG3362_2018",
            eGrade="C30",
            nCrepShrk=1
        )


def test_get_all():
    """测试获取全部单元"""
    reset_all()
    all_elems = element_manager.all()
    assert isinstance(all_elems, list), f"应返回list，实际{type(all_elems)}"
    print(f"✓ 获取全部单元成功，共 {len(all_elems)} 个")


def test_count():
    """测试单元计数"""
    reset_all()
    count = element_manager.count()
    assert count >= 0
    assert isinstance(count, int)
    print(f"✓ 单元计数成功: {count}")


def test_get():
    """测试按编号查询单元"""
    reset_all()
    all_elems = element_manager.all()
    if all_elems:
        elem = element_manager.get(all_elems[0].no)
        assert elem is not None
        assert elem.no == all_elems[0].no
        print(f"✓ 按编号查询成功: 单元{elem.no}, 类型{elem.element_type}")


def test_create_beam3d():
    """测试创建梁单元"""
    reset_all()
    cleanup_test_data()
    setup_prerequisites()

    element_manager.create_beam3d(
        no=9999,
        node1=TEST_NODE_NOS[0],
        node2=TEST_NODE_NOS[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    elem = element_manager.get(9999)
    assert elem is not None, "单元9999应存在"
    assert elem.no == 9999
    assert elem.node_i == TEST_NODE_NOS[0]
    assert elem.node_j == TEST_NODE_NOS[1]
    element_manager.delete(9999)
    print("✓ 创建梁单元成功")


def test_create_truss():
    """测试创建桁架单元"""
    reset_all()
    cleanup_test_data()
    setup_prerequisites()

    element_manager.create_truss(
        no=9998,
        node1=TEST_NODE_NOS[0],
        node2=TEST_NODE_NOS[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    elem = element_manager.get(9998)
    assert elem is not None
    assert elem.no == 9998
    element_manager.delete(9998)
    print("✓ 创建桁架单元成功")


def test_create_spring():
    """测试创建弹簧单元"""
    reset_all()
    cleanup_test_data()
    setup_prerequisites()

    element_manager.create_spring(
        no=9997,
        node1=TEST_NODE_NOS[0],
        node2=TEST_NODE_NOS[1],
        bLinear=1,
        dx=100,
        dy=100,
        dz=100
    )
    elem = element_manager.get(9997)
    assert elem is not None
    assert elem.no == 9997
    element_manager.delete(9997)
    print("✓ 创建弹簧单元成功")


def test_create_cable():
    """测试创建拉索单元"""
    reset_all()
    cleanup_test_data()
    setup_prerequisites()

    element_manager.create_cable(
        no=9996,
        node1=TEST_NODE_NOS[0],
        node2=TEST_NODE_NOS[1],
        nMat=TEST_MAT_NO,
        nSec=1,
        eMethod="UL",
        dPara=10.0
    )
    elem = element_manager.get(9996)
    assert elem is not None
    assert elem.no == 9996
    element_manager.delete(9996)
    print("✓ 创建拉索单元成功")


def test_create_shell():
    """测试创建壳单元"""

    reset_all()
    cleanup_test_data()

    # 先确认节点和材料是否创建成功
    setup_prerequisites()

    for no in TEST_NODE_NOS[:3]:
        nd = node_manager.get(no)
        print(f"[DEBUG] 节点{no}: {nd}")

    mat = material_manager.get(TEST_MAT_NO)
    print(f"[DEBUG] 材料{TEST_MAT_NO}: {mat}")

    element_manager.create_shell(
        no=9995,
        node1=TEST_NODE_NOS[0],
        node2=TEST_NODE_NOS[1],
        node3=TEST_NODE_NOS[2],
        nMat=TEST_MAT_NO,
        nThk=1,
        bIsThin=1,
        node4=TEST_NODE_NOS[4]
    )
    elem = element_manager.get(9995)
    assert elem is not None
    element_manager.delete(9995)
    print("✓ 创建壳单元成功")


def test_renumber():
    """测试修改单元编号"""
    reset_all()
    cleanup_test_data()
    setup_prerequisites()

    # 先创建
    element_manager.create_beam3d(
        no=9990,
        node1=TEST_NODE_NOS[0],
        node2=TEST_NODE_NOS[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    elem = element_manager.get(9990)
    assert elem is not None, "单元9990应存在"

    # 修改编号
    element_manager.renumber(9990, 9980)
    assert element_manager.get(9990) is None, "旧编号9990应不存在"
    elem_new = element_manager.get(9980)
    assert elem_new is not None, "新编号9980应存在"
    assert elem_new.no == 9980
    element_manager.delete(9980)
    print("✓ 修改单元编号成功")


def test_delete():
    """测试删除单元"""
    reset_all()
    cleanup_test_data()
    setup_prerequisites()

    # 先创建
    element_manager.create_beam3d(
        no=9989,
        node1=TEST_NODE_NOS[0],
        node2=TEST_NODE_NOS[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    assert element_manager.get(9989) is not None

    # 再删除
    element_manager.delete(9989)
    assert element_manager.get(9989) is None, "单元应已删除"
    print("✓ 删除单元成功")


if __name__ == "__main__":
    print("开始测试 ElementManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_count,
        test_get,
        test_create_beam3d,
        test_create_truss,
        test_create_spring,
        test_create_cable,
        test_create_shell,
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