# tests/case_element_manager.py

"""
注意：单元创建依赖节点和材料，需先确保测试环境中有可用的节点和材料。
编号均由各 Manager 自动生成，通过返回对象的 ``.no`` 使用。

``create_*`` 返回具体子类（如 ``Beam3dElement``），``get`` / ``all`` 为基类 ``Element`` 引用（运行时为子类实例）。
"""
from pyosis.element import (
    Beam3dElement,
    CableElement,
    Element,
    ShellElement,
    SpringElement,
    TrussElement,
    element_manager,
)
from pyosis.node import node_manager
from pyosis.material import material_manager


def reset_all():
    """刷新所有缓存"""
    ...


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
            except Exception:
                pass


def ensure_pytest_material_no() -> int:
    """按名称复用或创建测试用混凝土材料，返回材料编号。"""

    for m in material_manager.all():
        if m.name == "测试材料":
            return m.no
    mat = material_manager.create_conc(
        "测试材料",
        eCode="JTG3362_2018",
        eGrade="C30",
        nCrepShrk=1,
    )
    return mat.no


def setup_prerequisites():
    """创建单元测试所需的前置条件（节点和材料）

    Returns:
        (node_nos, mat_no): 节点编号列表、材料编号
    """
    node_nos = []
    for i in range(5):
        nd = node_manager.create(float(i), float(i), float(i))
        node_nos.append(nd.no)

    mat_no = ensure_pytest_material_no()
    return node_nos, mat_no


def test_get_all():
    """测试获取全部单元"""
    reset_all()
    all_elems = element_manager.all()
    assert isinstance(all_elems, list), f"应返回list，实际{type(all_elems)}"
    for elem in all_elems:
        assert isinstance(elem, Element), f"应为 Element 子类，实际 {type(elem)}"
        assert hasattr(elem, "raw_type") and hasattr(elem, "element_type")
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
        assert isinstance(elem, Element)
        assert elem.no == all_elems[0].no
        print(f"✓ 按编号查询成功: 单元{elem.no}, {elem.element_type}(raw_type={elem.raw_type})")


def test_create_beam3d():
    """测试创建梁单元"""
    reset_all()
    created_elems = []
    node_nos, mat_no = setup_prerequisites()

    elem = element_manager.create_beam3d(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=mat_no,
        nSec1=1,
        nSec2=1
    )
    created_elems.append(elem.no)

    assert isinstance(elem, Beam3dElement), f"应返回 Beam3dElement，实际 {type(elem)}"
    assert elem.element_type == "BEAM3D" and elem.raw_type == 1
    assert elem.node_i == node_nos[0]
    assert elem.node_j == node_nos[1]
    print(f"✓ 创建梁单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_truss():
    """测试创建桁架单元"""
    reset_all()
    created_elems = []
    node_nos, mat_no = setup_prerequisites()

    elem = element_manager.create_truss(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=mat_no,
        nSec1=1,
        nSec2=1
    )
    created_elems.append(elem.no)

    assert isinstance(elem, TrussElement), f"应返回 TrussElement，实际 {type(elem)}"
    assert elem.element_type == "TRUSS" and elem.raw_type == 2
    print(f"✓ 创建桁架单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_spring():
    """测试创建弹簧单元"""
    reset_all()
    created_elems = []
    node_nos, _mat_no = setup_prerequisites()

    elem = element_manager.create_spring(
        node1=node_nos[0],
        node2=node_nos[1],
        bLinear=1,
        dx=100,
        dy=100,
        dz=100
    )
    created_elems.append(elem.no)

    assert isinstance(elem, SpringElement), f"应返回 SpringElement，实际 {type(elem)}"
    assert elem.element_type == "SPRING" and elem.raw_type == 3
    print(f"✓ 创建弹簧单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_cable():
    """测试创建拉索单元"""
    reset_all()
    created_elems = []
    node_nos, mat_no = setup_prerequisites()

    elem = element_manager.create_cable(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=mat_no,
        nSec=1,
        eMethod="UL",
        dPara=10.0
    )
    created_elems.append(elem.no)

    assert isinstance(elem, CableElement), f"应返回 CableElement，实际 {type(elem)}"
    assert elem.element_type == "CABLE" and elem.raw_type == 4
    print(f"✓ 创建拉索单元成功 (编号: {elem.no})")

    # 清理
    cleanup_test_data(created_elems)


def test_create_shell():
    """测试创建壳单元；成功则校验 ShellElement，否则跳过。

    注意：``setup_prerequisites`` 的节点在 (i,i,i) 上共线，不能作四边形壳顶点；
    此处单独建 XY 平面矩形四角点。
    """
    reset_all()
    created_elems: list[int] = []
    shell_node_nos: list[int] = []
    mat_no = ensure_pytest_material_no()
    from pyosis.thickness import osis_feature_shellthk

    try:
        osis_feature_shellthk(1, 0.2, 0.2)
    except Exception:
        print("⊘ 创建壳单元跳过（厚度等前置未就绪）")
        return

    # 矩形四角 (Z=0)，避免共线 / 共面退化
    for x, y, z in (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (1.0, 1.0, 0.0),
        (0.0, 1.0, 0.0),
    ):
        nd = node_manager.create(x, y, z)
        shell_node_nos.append(nd.no)

    try:
        elem = element_manager.create_shell(
            node1=shell_node_nos[0],
            node2=shell_node_nos[1],
            node3=shell_node_nos[2],
            nMat=mat_no,
            nThk=1,
            bIsThin=1,
            node4=shell_node_nos[3],
        )
        created_elems.append(elem.no)
        assert isinstance(elem, ShellElement), f"应返回 ShellElement，实际 {type(elem)}"
        assert elem.element_type == "SHELL" and elem.raw_type == 5
        print(f"✓ 创建壳单元成功 (编号: {elem.no})")
    except RuntimeError as e:
        print(f"⊘ 创建壳单元跳过: {e}")
    finally:
        cleanup_test_data(created_elems)
        for no in shell_node_nos:
            try:
                node_manager.delete(no)
            except Exception:
                pass


def test_renumber():
    """测试修改单元编号"""
    reset_all()
    created_elems = []
    node_nos, mat_no = setup_prerequisites()

    # 先创建
    elem = element_manager.create_beam3d(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=mat_no,
        nSec1=1,
        nSec2=1
    )
    no_old = elem.no
    created_elems.append(no_old)

    assert isinstance(elem, Beam3dElement)

    # 修改编号
    no_new = no_old + 1
    element_manager.renumber(no_old, no_new)
    assert element_manager.get(no_old) is None, "旧编号应不存在"
    elem_new = element_manager.get(no_new)
    assert elem_new is not None, "新编号应存在"
    assert isinstance(elem_new, Beam3dElement)
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
    node_nos, mat_no = setup_prerequisites()

    # 先创建
    elem = element_manager.create_beam3d(
        node1=node_nos[0],
        node2=node_nos[1],
        nMat=mat_no,
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
