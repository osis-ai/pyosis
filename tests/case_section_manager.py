# tests/case_section_manager.py

"""
SectionManager 接口测试（手动运行版）
"""
from pyosis.section import section_manager


# 测试用编号列表
TEST_NOS = [9999, 9998, 9997, 9996, 9990, 9980, 9989]


def reset():
    """刷新缓存"""
    section_manager.refresh()


def cleanup_test_sections():
    """清理测试残留数据"""
    for no in TEST_NOS:
        sec = section_manager.get(no)
        if sec is not None:
            try:
                section_manager.delete(no)
            except:
                pass


def test_get_all():
    """测试获取全部截面"""
    reset()
    all_secs = section_manager.all()
    assert isinstance(all_secs, list), f"应返回list，实际{type(all_secs)}"
    print(f"✓ 获取全部截面成功，共 {len(all_secs)} 个")


def test_create_circle():
    """测试创建圆形截面"""
    reset()
    cleanup_test_sections()

    # 实心圆
    section_manager.create_circle(9999, "测试实心圆", eCircleType="Solid", D=0.5, Tw=0.0)
    sec = section_manager.get(9999)
    assert sec is not None, "截面9999应存在"
    assert sec.name == "测试实心圆", f"名称应为'测试实心圆'，实际'{sec.name}'"
    section_manager.delete(9999)
    print("✓ 创建实心圆形截面成功")

    # 空心圆
    section_manager.create_circle(9998, "测试空心圆", eCircleType="Hollow", D=0.5, Tw=0.02)
    sec = section_manager.get(9998)
    assert sec is not None
    assert sec.name == "测试空心圆"
    section_manager.delete(9998)
    print("✓ 创建空心圆形截面成功")


def test_create_Lshape():
    """测试创建L形截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_Lshape(9997, "测试L形", nDir=1, H=0.1, B=0.1, Tf1=0.016, Tf2=0.016)
    sec = section_manager.get(9997)
    assert sec is not None, "截面9997应存在"
    assert sec.name == "测试L形"
    section_manager.delete(9997)
    print("✓ 创建L形截面成功")


def test_create_Tshape():
    """测试创建T形截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_Tshape(9996, "测试T形", nDir=0, H=0.3, B=0.2, Tf=0.016, Tw=0.016)
    sec = section_manager.get(9996)
    assert sec is not None, "截面9996应存在"
    assert sec.name == "测试T形"
    section_manager.delete(9996)
    print("✓ 创建T形截面成功")


def test_create_Ishape():
    """测试创建I形截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_Ishape(9995, "测试I形", H=0.3, Bt=0.13, Bb=0.13, Tt=0.016, Tb=0.016, Tw=0.016)
    sec = section_manager.get(9995)
    assert sec is not None, "截面9995应存在"
    assert sec.name == "测试I形"
    section_manager.delete(9995)
    print("✓ 创建I形截面成功")


def test_create_rect():
    """测试创建矩形截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_rect(9994, "测试矩形", B=6.5, H=3.2)
    sec = section_manager.get(9994)
    assert sec is not None, "截面9994应存在"
    assert sec.name == "测试矩形"
    section_manager.delete(9994)
    print("✓ 创建矩形截面成功")


def test_create_steel_i():
    """测试创建工字形钢截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_steel_i(
        9993, "测试工字钢",
        H=0.3, Bt=0.13, Bb=0.13, Tt=0.016, Tb=0.016, Tw=0.016,
        WebRibPos="Both"
    )
    sec = section_manager.get(9993)
    assert sec is not None, "截面9993应存在"
    assert sec.name == "测试工字钢"
    section_manager.delete(9993)
    print("✓ 创建工字形钢截面成功")


def test_renumber():
    """测试修改截面编号"""
    reset()
    cleanup_test_sections()

    section_manager.create_circle(9990, "待修改截面", D=0.5)
    sec = section_manager.get(9990)
    assert sec is not None, f"截面9990应存在，实际get返回: {sec}"
    section_manager.renumber(9990, 9980)
    assert section_manager.get(9990) is None, "旧编号9990应不存在"
    assert section_manager.get(9980) is not None, "新编号9980应存在"
    assert section_manager.get(9980).name == "待修改截面"
    section_manager.delete(9980)
    print("✓ 修改截面编号成功")


def test_delete():
    """测试删除截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_circle(9989, "待删除截面", D=0.5)
    assert section_manager.get(9989) is not None
    section_manager.delete(9989)
    assert section_manager.get(9989) is None, "截面应已删除"
    print("✓ 删除截面成功")


def test_get_multiple():
    """测试批量查询截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_circle(9997, "测试圆1", D=0.5)
    section_manager.create_rect(9998, "测试矩形")

    results = section_manager.get([9997, 9998, 9999])
    assert len(results) == 3, "应返回3个结果"
    assert results[0] is not None and results[0].name == "测试圆1"
    assert results[1] is not None and results[1].name == "测试矩形"
    assert results[2] is None, "不存在的截面应返回None"

    section_manager.delete(9997)
    section_manager.delete(9998)
    print("✓ 批量查询截面成功")


if __name__ == "__main__":
    print("开始测试 SectionManager...")
    print("=" * 50)

    tests = [
        test_get_all,
        test_create_circle,
        test_create_Lshape,
        test_create_Tshape,
        test_create_Ishape,
        test_create_rect,
        test_create_steel_i,
        test_renumber,
        test_delete,
        test_get_multiple,
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
