# tests/case_material_manager.py

"""
MaterialManager 接口测试（手动运行版）
"""
from pyosis.material import material_manager


# 测试用编号列表
TEST_NOS = [9999, 9998, 9997, 9996, 9995, 9994, 9990, 9980, 9989]


def reset():
    """刷新缓存"""
    material_manager.refresh()


def cleanup_test_materials():
    """清理测试残留数据"""
    for no in TEST_NOS:
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
    cleanup_test_materials()

    # 缺省 nCrepShrk
    material_manager.create_conc(9999, "测试混凝土", eCode="JTG3362_2018", eGrade="C30")
    mat = material_manager.get(9999)
    assert mat is not None, "材料9999应存在"
    assert mat.name == "测试混凝土", f"名称应为'测试混凝土'，实际'{mat.name}'"
    material_manager.delete(9999)
    print("✓ 创建混凝土(缺省nCrepShrk)成功")

    # 指定 nCrepShrk
    material_manager.create_conc(9998, "测试混凝土2", eCode="JTG3362_2018", eGrade="C35", nCrepShrk=1)
    mat = material_manager.get(9998)
    assert mat is not None
    assert mat.name == "测试混凝土2", f"名称应为'测试混凝土2'，实际'{mat.name}'"
    material_manager.delete(9998)
    print("✓ 创建混凝土(指定nCrepShrk=1)成功")


def test_create_steel():
    """测试创建钢材"""
    reset()
    cleanup_test_materials()

    material_manager.create_steel(9997, "测试钢材", eCode="JTGD64_2015", eGrade="Q345")
    mat = material_manager.get(9997)
    assert mat is not None
    assert mat.name == "测试钢材"
    material_manager.delete(9997)
    print("✓ 创建钢材成功")


def test_create_prestressed():
    """测试创建预应力材料"""
    reset()
    cleanup_test_materials()

    material_manager.create_prestressed(9996, "测试预应力", eCode="JTG3362_2018", eGrade="Strand1860")
    mat = material_manager.get(9996)
    assert mat is not None
    assert mat.name == "测试预应力"
    material_manager.delete(9996)
    print("✓ 创建预应力材料成功")


def test_create_rebar():
    """测试创建钢筋"""
    reset()
    cleanup_test_materials()

    material_manager.create_rebar(9995, "测试钢筋", eCode="JTG3362_2018", eGrade="HRB400")
    mat = material_manager.get(9995)
    assert mat is not None
    assert mat.name == "测试钢筋"
    material_manager.delete(9995)
    print("✓ 创建钢筋成功")


def test_create_custom():
    """测试创建自定义材料"""
    reset()
    cleanup_test_materials()

    material_manager.create_custom(9994, "测试自定义", dE=2.1e11, dG=8.1e10, dMu=0.3, dUnitWeight=78500)
    mat = material_manager.get(9994)
    assert mat is not None
    assert mat.name == "测试自定义"
    assert mat.e == 2.1e11
    assert mat.g == 8.1e10
    assert mat.mu == 0.3
    material_manager.delete(9994)
    print("✓ 创建自定义材料成功")


def test_renumber():
    """测试修改材料编号"""
    reset()
    cleanup_test_materials()

    material_manager.create_conc(9990, "待修改材料", eCode="JTG3362_2018", eGrade="C30", nCrepShrk=1)
    mat = material_manager.get(9990)
    assert mat is not None, f"材料9990应存在，实际get返回: {mat}"
    material_manager.renumber(9990, 9980)
    assert material_manager.get(9990) is None, "旧编号9990应不存在"
    assert material_manager.get(9980) is not None, "新编号9980应存在"
    assert material_manager.get(9980).name == "待修改材料"
    material_manager.delete(9980)
    print("✓ 修改材料编号成功")


def test_delete():
    """测试删除材料"""
    reset()
    cleanup_test_materials()

    material_manager.create_conc(9989, "待删除材料", eCode="JTG3362_2018", eGrade="C30")
    assert material_manager.get(9989) is not None
    material_manager.delete(9989)
    assert material_manager.get(9989) is None, "材料应已删除"
    print("✓ 删除材料成功")


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
            failed += 1
        except Exception as e:
            print(f"✗ {t.__name__} 异常: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"测试完成: {passed} 通过, {failed} 失败")