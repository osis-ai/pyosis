# tests/case_boundary_manager.py

import traceback

from pyosis.boundary.manager import (
    ElstcSptBoundary,
    GeneralBoundary,
    MstSlvBoundary,
    boundary_manager,
)


def cleanup_test_boundaries(created_nos: list[int]):
    """清理测试残留数据"""
    for no in created_nos:
        bd = boundary_manager.get(no)
        if bd is not None:
            try:
                boundary_manager.delete(no)
            except Exception:
                pass


def test_get_all():
    """测试获取全部边界"""

    all_bds = boundary_manager.all()
    assert isinstance(all_bds, list), f"应返回 list，实际 {type(all_bds)}"
    for bd in all_bds:
        assert hasattr(bd, "no") and hasattr(bd, "raw_type"), "应为 Boundary 及其子类实例"
    print(f"✓ 获取全部边界成功，共 {len(all_bds)} 个")


def test_create_general():
    """测试创建一般边界（返回 GeneralBoundary）"""

    created_nos: list[int] = []

    # 全约束
    bd = boundary_manager.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)
    assert isinstance(bd, GeneralBoundary), f"应返回 GeneralBoundary，实际 {type(bd)}"
    assert bd.boundary_type == "General"
    created_nos.append(bd.no)

    bd_check = boundary_manager.get(bd.no)
    assert bd_check is not None, f"边界 {bd.no} 应存在"
    assert isinstance(bd_check, GeneralBoundary)
    print(f"✓ 创建一般边界(全约束)成功, no={bd.no}")

    # 部分约束
    bd2 = boundary_manager.create_general(bX=1, bY=1, bZ=0, bRX=0, bRY=0, bRZ=0, bRW=0)
    assert isinstance(bd2, GeneralBoundary)
    created_nos.append(bd2.no)
    print(f"✓ 创建一般边界(部分约束)成功, no={bd2.no}")

    cleanup_test_boundaries(created_nos)


def test_create_elstcspt():
    """测试创建弹性支承（返回 ElstcSptBoundary）"""

    created_nos: list[int] = []

    bd = boundary_manager.create_elstcspt(
        bX=0, DX=1e10,
        bY=0, DY=1e10,
        bZ=1, DZ=1e13,
        bRX=1, RX=1e16,
        bRY=1, RY=1e16,
        bRZ=1, RZ=1e16,
    )
    assert isinstance(bd, ElstcSptBoundary), f"应返回 ElstcSptBoundary，实际 {type(bd)}"
    assert bd.boundary_type in ("ElstcSpt", "GeneralElstcSpt")
    # 部分服务端将弹性支承误标为 type=4，manager 会按 payload 解析为 ElstcSptBoundary
    created_nos.append(bd.no)

    bd_check = boundary_manager.get(bd.no)
    assert bd_check is not None, f"边界 {bd.no} 应存在"
    assert isinstance(bd_check, ElstcSptBoundary)
    print(f"✓ 创建弹性支承成功, no={bd.no}")

    cleanup_test_boundaries(created_nos)


def test_create_master_slave():
    """测试创建主从约束（返回 MstSlvBoundary）"""

    created_nos: list[int] = []

    bd = boundary_manager.create_master_slave(
        nNode=1,
        bX=1, bY=1, bZ=1,
        bRX=0, bRY=0, bRZ=0,
    )
    assert isinstance(bd, MstSlvBoundary), f"应返回 MstSlvBoundary，实际 {type(bd)}"
    assert bd.boundary_type == "MstSlv"
    assert bd.master_no == 1
    created_nos.append(bd.no)

    bd_check = boundary_manager.get(bd.no)
    assert bd_check is not None, f"边界 {bd.no} 应存在"
    assert isinstance(bd_check, MstSlvBoundary)
    print(f"✓ 创建主从约束成功, no={bd.no}, master_no={bd.master_no}")

    cleanup_test_boundaries(created_nos)


def test_delete():
    """测试删除边界"""

    created_nos: list[int] = []

    bd = boundary_manager.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)
    assert isinstance(bd, GeneralBoundary)
    created_nos.append(bd.no)
    assert boundary_manager.get(bd.no) is not None
    boundary_manager.delete(bd.no)

    assert boundary_manager.get(bd.no) is None, "边界应已删除"
    print("✓ 删除边界成功")

    cleanup_test_boundaries(created_nos)


def test_get_multiple():
    """测试批量查询边界"""

    created_nos: list[int] = []

    bd1 = boundary_manager.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)
    assert isinstance(bd1, GeneralBoundary)
    created_nos.append(bd1.no)
    bd2 = boundary_manager.create_elstcspt(bX=1, DX=1e10, bY=1, DY=1e10, bZ=1, DZ=1e13)
    assert isinstance(bd2, ElstcSptBoundary)
    created_nos.append(bd2.no)

    results = boundary_manager.get([bd1.no, bd2.no, 99999])
    assert len(results) == 3, "应返回 3 个结果"
    assert isinstance(results[0], GeneralBoundary)
    assert isinstance(results[1], ElstcSptBoundary)
    assert results[2] is None, "不存在的边界应返回 None"

    print("✓ 批量查询边界成功")

    cleanup_test_boundaries(created_nos)


def test_assign_general_boundary():
    """GeneralBoundary.assign：分配一般边界到节点（依赖模型中存在对应节点编号）"""

    created_nos: list[int] = []

    bd = boundary_manager.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1, bRW=1)
    assert isinstance(bd, GeneralBoundary)
    assert hasattr(bd, "assign")
    created_nos.append(bd.no)

    # 添加节点 1（需模型中存在该节点，与 test_create_master_slave 中 nNode=1 一致）
    bd.assign(eOP="a", param=[1])

    print(f"✓ GeneralBoundary.assign 成功, no={bd.no}")

    cleanup_test_boundaries(created_nos)


def test_assign_elstcspt_boundary():
    """ElstcSptBoundary.assign：分配节点弹性支撑到节点"""

    created_nos: list[int] = []

    bd = boundary_manager.create_elstcspt(
        bX=0, DX=1e10, bY=0, DY=1e10, bZ=1, DZ=1e13,
        bRX=1, RX=1e16, bRY=1, RY=1e16, bRZ=1, RZ=1e16,
    )
    assert isinstance(bd, ElstcSptBoundary)
    assert hasattr(bd, "assign")
    created_nos.append(bd.no)

    bd.assign(eOP="a", param=[1])

    print(f"✓ ElstcSptBoundary.assign 成功, no={bd.no}")

    cleanup_test_boundaries(created_nos)


def test_mstslv_no_assign_method():
    """主从约束不支持 assign（仅一般边界与弹性支承可分配节点）"""

    created_nos: list[int] = []

    bd = boundary_manager.create_master_slave(
        nNode=1, bX=1, bY=1, bZ=1, bRX=0, bRY=0, bRZ=0,
    )
    assert isinstance(bd, MstSlvBoundary)
    assert not hasattr(bd, "assign")
    created_nos.append(bd.no)

    print("✓ MstSlvBoundary 无 assign 方法（符合设计）")

    cleanup_test_boundaries(created_nos)


if __name__ == "__main__":
    print("开始测试 BoundaryManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_create_general,
        test_create_elstcspt,
        test_create_master_slave,
        test_delete,
        test_get_multiple,
        test_assign_general_boundary,
        test_assign_elstcspt_boundary,
        test_mstslv_no_assign_method,
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
