# tests/case_element_manager.py

"""
注意：单元创建依赖节点和材料，需先确保测试环境中有可用的节点和材料。
"""
from pyosis.element import element_manager
from pyosis.node import node_manager
from pyosis.material import material_manager


# 测试用材料编号
TEST_MAT_NO = 99901


def reset_all():
    """刷新所有缓存"""
    node_manager.refresh()
    material_manager.refresh()
    element_manager.refresh()


def cleanup_test_data(created_nos: list[int]):
    """清理测试残留数据

    Args:
        created_nos: 需要清理的单元编号列表
    """
    for no in created_nos:
        elem = element_manager.get(no)
        if elem is not None:
            try:
                element_manager.delete(no)
            except:
                pass


def setup_prerequisites():
    """创建单元测试所需的前置条件（节点和材料）

    Returns:
        创建的节点编号列表
    """
    node_nos = []
    for i in range(5):
        no = node_manager.create(float(i), float(i), float(i))
        node_nos.append(no)

    # 确保材料存在
    if material_manager.get(TEST_MAT_NO) is None:
        material_manager.create_conc(
            TEST_MAT_NO, "测试材料",
            eCode="JTG3362_2018",
            eGrade="C30",
            nCrepShrk=1
        )

    return node_nos


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
    created_elems = []
    node_nos = setup_prerequisites()

    elem = element_manager.create_beam3d(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    created_elems.append(elem.no)

    assert elem is not None
    assert elem.no is not None
    assert elem.node_i == node_nos[0]
    assert elem.node_j == node_nos[1]
    print(f"✓ 创建梁单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_truss():
    """测试创建桁架单元"""
    reset_all()
    created_elems = []
    node_nos = setup_prerequisites()

    elem = element_manager.create_truss(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    created_elems.append(elem.no)

    assert elem is not None
    assert elem.no is not None
    print(f"✓ 创建桁架单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_spring():
    """测试创建弹簧单元"""
    reset_all()
    created_elems = []
    node_nos = setup_prerequisites()

    elem = element_manager.create_spring(
        node1=node_nos[0],
        node2=node_nos[1],
        bLinear=1,
        dx=100,
        dy=100,
        dz=100
    )
    created_elems.append(elem.no)

    assert elem is not None
    assert elem.no is not None
    print(f"✓ 创建弹簧单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_cable():
    """测试创建拉索单元"""
    reset_all()
    created_elems = []
    node_nos = setup_prerequisites()

    elem = element_manager.create_cable(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=TEST_MAT_NO,
        nSec=1,
        eMethod="UL",
        dPara=10.0
    )
    created_elems.append(elem.no)

    assert elem is not None
    assert elem.no is not None
    print(f"✓ 创建拉索单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_shell():
    """测试创建壳单元（OSIS暂不支持，跳过）"""
    print("⊘ 创建壳单元跳过（OSIS暂不支持）")


def test_renumber():
    """测试修改单元编号"""
    reset_all()
    created_elems = []
    node_nos = setup_prerequisites()

    # 先创建
    elem = element_manager.create_beam3d(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    no_old = elem.no
    created_elems.append(no_old)

    assert elem is not None

    # 修改编号
    no_new = no_old + 1
    element_manager.renumber(no_old, no_new)
    assert element_manager.get(no_old) is None, "旧编号应不存在"
    elem_new = element_manager.get(no_new)
    assert elem_new is not None, "新编号应存在"
    assert elem_new.no == no_new
    created_elems.remove(no_old)
    created_elems.append(no_new)
    print(f"✓ 修改单元编号成功 ({no_old} -> {no_new})")

    # 清理
    cleanup_test_data(created_elems)


def test_delete():
    """测试删除单元"""
    reset_all()
    created_elems = []
    node_nos = setup_prerequisites()

    # 先创建
    elem = element_manager.create_beam3d(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=TEST_MAT_NO,
        nSec1=1,
        nSec2=1
    )
    no = elem.no
    created_elems.append(no)
    assert element_manager.get(no) is not None

    # 再删除
    element_manager.delete(no)
    assert element_manager.get(no) is None, "单元应已删除"
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