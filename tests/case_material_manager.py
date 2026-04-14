# tests/case_material_manager.py

"""
MaterialManager 接口测试（手动运行版）
"""
from pyosis.material import material_manager


def reset():
    """刷新缓存"""
    material_manager.refresh()


def cleanup_test_materials(created_nos: list[int]):
    """清理测试残留数据"""
    for no in created_nos:
        mat = material_manager.get(no)
        if mat is not None:
            try:
                material_manager.delete(no)
            except:
                pass


def test_get_all():
    """测试获取全部材料"""
    reset()
    all_mats = material_manager.all()
    assert isinstance(all_mats, list), f"应返回list，实际{type(all_mats)}"
    print(f"✓ 获取全部材料成功，共 {len(all_mats)} 个")


def test_create_conc():
    """测试创建混凝土"""
    reset()
    created_nos = []

    # 缺省 nCrepShrk
    mat = material_manager.create_conc("测试混凝土", eCode="JTG3362_2018", eGrade="C30")
    created_nos.append(mat.no)
    assert mat is not None
    assert mat.name == "测试混凝土", f"名称应为'测试混凝土'，实际'{mat.name}'"
    print(f"✓ 创建混凝土(缺省nCrepShrk)成功 (编号: {mat.no})")

    # 指定 nCrepShrk
    mat = material_manager.create_conc("测试混凝土2", eCode="JTG3362_2018", eGrade="C35", nCrepShrk=1)
    created_nos.append(mat.no)
    assert mat is not None
    assert mat.name == "测试混凝土2", f"名称应为'测试混凝土2'，实际'{mat.name}'"
    print(f"✓ 创建混凝土(指定nCrepShrk=1)成功 (编号: {mat.no})")

    cleanup_test_materials(created_nos)


def test_create_steel():
    """测试创建钢材"""
    reset()
    created_nos = []

    mat = material_manager.create_steel("测试钢材", eCode="JTGD64_2015", eGrade="Q345")
    created_nos.append(mat.no)
    assert mat is not None
    assert mat.name == "测试钢材"
    print(f"✓ 创建钢材成功 (编号: {mat.no})")

    cleanup_test_materials(created_nos)


def test_create_prestressed():
    """测试创建预应力材料"""
    reset()
    created_nos = []

    mat = material_manager.create_prestressed("测试预应力", eCode="JTG3362_2018", eGrade="Strand1860")
    created_nos.append(mat.no)
    assert mat is not None
    assert mat.name == "测试预应力"
    print(f"✓ 创建预应力材料成功 (编号: {mat.no})")

    cleanup_test_materials(created_nos)


def test_create_rebar():
    """测试创建钢筋"""
    reset()
    created_nos = []

    mat = material_manager.create_rebar("测试钢筋", eCode="JTG3362_2018", eGrade="HRB400")
    created_nos.append(mat.no)
    assert mat is not None
    assert mat.name == "测试钢筋"
    print(f"✓ 创建钢筋成功 (编号: {mat.no})")

    cleanup_test_materials(created_nos)


def test_create_custom():
    """测试创建自定义材料"""
    reset()
    created_nos = []

    mat = material_manager.create_custom("测试自定义", dE=2.1e11, dG=8.1e10, dMu=0.3, dUnitWeight=78500)
    created_nos.append(mat.no)
    assert mat is not None
    assert mat.name == "测试自定义"
    assert mat.e == 2.1e11
    assert mat.g == 8.1e10
    assert mat.mu == 0.3
    print(f"✓ 创建自定义材料成功 (编号: {mat.no})")

    cleanup_test_materials(created_nos)


def test_renumber():
    """测试修改材料编号"""
    reset()
    created_nos = []

    mat = material_manager.create_conc("待修改材料", eCode="JTG3362_2018", eGrade="C30", nCrepShrk=1)
    created_nos.append(mat.no)
    assert mat is not None
    old_no = mat.no
    new_no = old_no + 1
    material_manager.renumber(old_no, new_no)
    assert material_manager.get(old_no) is None, "旧编号应不存在"
    assert material_manager.get(new_no) is not None, "新编号应存在"
    assert material_manager.get(new_no).name == "待修改材料"
    created_nos.remove(old_no)
    created_nos.append(new_no)
    print(f"✓ 修改材料编号成功 ({old_no} -> {new_no})")

    cleanup_test_materials(created_nos)


def test_delete():
    """测试删除材料"""
    reset()
    created_nos = []

    mat = material_manager.create_conc("待删除材料", eCode="JTG3362_2018", eGrade="C30")
    created_nos.append(mat.no)
    material_manager.delete(mat.no)
    assert material_manager.get(mat.no) is None, "材料应已删除"
    print("✓ 删除材料成功")

    cleanup_test_materials(created_nos)


if __name__ == "__main__":
    print("开始测试 MaterialManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_create_conc,
        test_create_steel,
        test_create_prestressed,
        test_create_rebar,
        test_create_custom,
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
            import traceback
            traceback.print_exc()
            failed += 1
        except Exception as e:
            print(f"✗ {t.__name__} 异常: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 50)
    print(f"测试完成: {passed} 通过, {failed} 失败")