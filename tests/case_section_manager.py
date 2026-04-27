# tests/case_section_manager.py

"""
SectionManager 接口测试（手动运行版）
"""
from pyosis.section import section_manager


def reset():
    """刷新缓存"""

def cleanup_test_sections():
    """预留钩子：本文件依赖自动编号，各用例创建后自行 delete。"""
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
    sec = section_manager.create_circle(e_circle_type="Solid", d=0.5, tw=0.0)
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_"), f"名称应以'SEC_'开头，实际'{sec.name}'"
    section_manager.delete(sec.no)
    print("✓ 创建实心圆形截面成功")

    # 空心圆
    sec = section_manager.create_circle(e_circle_type="Hollow", d=0.5, tw=0.02)
    assert sec is not None
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建空心圆形截面成功")


def test_create_Lshape():
    """测试创建L形截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_Lshape(n_dir=1, h=0.1, b=0.1, tf1=0.016, tf2=0.016)
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建L形截面成功")


def test_create_Tshape():
    """测试创建T形截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_Tshape(n_dir=0, h=0.3, b=0.2, tf=0.016, tw=0.016)
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建T形截面成功")


def test_create_Ishape():
    """测试创建I形截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_Ishape(h=0.3, bt=0.13, bb=0.13, tt=0.016, tb=0.016, tw=0.016)
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建I形截面成功")


def test_create_rect():
    """测试创建矩形截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_rect(b=6.5, h=3.2)
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建矩形截面成功")


def test_create_steel_i():
    """测试创建工字形钢截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_steel_i(
        h=0.3, bt=0.13, bb=0.13, tt=0.016, tb=0.016, tw=0.016,
        web_rib_pos="Both",
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建工字形钢截面成功")


def test_renumber():
    """测试修改截面编号"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_circle(d=0.5)
    assert sec is not None
    old_no = sec.no
    section_manager.renumber(old_no, 9980)
    assert section_manager.get(old_no) is None, "旧编号应不存在"
    assert section_manager.get(9980) is not None, "新编号9980应存在"
    assert section_manager.get(9980).name == sec.name, "重编号后名称应保持不变"
    section_manager.delete(9980)
    print("✓ 修改截面编号成功")


def test_delete():
    """测试删除截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_circle(d=0.5)
    no = sec.no
    assert section_manager.get(no) is not None
    section_manager.delete(no)
    assert section_manager.get(no) is None, "截面应已删除"
    print("✓ 删除截面成功")


def test_get_multiple():
    """测试批量查询截面"""
    reset()
    cleanup_test_sections()

    sec1 = section_manager.create_circle(d=0.5)
    n1 = sec1.no
    name1 = sec1.name
    sec2 = section_manager.create_rect(b=6.5, h=3.2)
    n2 = sec2.no
    name2 = sec2.name

    results = section_manager.get([n1, n2, 999999999])
    assert len(results) == 3, "应返回3个结果"
    assert results[0] is not None and results[0].name == name1
    assert results[1] is not None and results[1].name == name2
    assert results[2] is None, "不存在的截面应返回None"

    section_manager.delete(n1)
    section_manager.delete(n2)
    print("✓ 批量查询截面成功")


# ──────────────────────────────────────────────
# 新增混凝土截面测试
# ──────────────────────────────────────────────

def test_create_smallbox():
    """测试创建小箱梁截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_smallbox(
        e_girder_pos="MIDDLE", h=1.6, bs=1.65, bm=1.2, bb=1.0,
        tt=0.18, tb=0.2, tw=0.2,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建小箱梁截面成功")


def test_create_hollowslab():
    """测试创建空心板截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_hollowslab(
        e_girder_pos="MIDDLE", h=0.95, bs=1.0, bm=0.57, tt=0.12, tb=0.12, tw=0.16,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建空心板截面成功")


def test_create_rounded_end():
    """测试创建圆端形截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_rounded_end(
        e_filling_type="Solid", b=7.0, h=3.0, r=2.0,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建圆端形截面成功")


def test_create_conventionalbox():
    """测试创建常规箱梁截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_conventionalbox(
        h=2.7, bt_l=6.375, bt_r=6.375, bb_l=3.5, bb_r=3.5, bs=0.5,
        tt=0.28, tb=0.32, tw1=0.5, tw2=0.5, n_cell_num=1,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建常规箱梁截面成功")


def test_create_flat_box():
    """测试创建扁平箱梁截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_flat_box(
        h=4.0, bt_l=20.0, bt_r=20.0, bb_l=10.5, bb_r=10.5, bs=0.8,
        tt=0.28, tb1=0.27, tb2=0.27, tw=0.25, n_cell_num=5,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建扁平箱梁截面成功")


def test_create_double_side_box():
    """测试创建双边箱截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_double_side_box(
        h=3.8, bt=36.0, bt_sub=14.8, bs=2.1, bb=4.4,
        tt=0.3, tb1=0.3, tb2=0.3, tw=0.5, bi=8.0,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建双边箱截面成功")


def test_create_ribbed_slab():
    """测试创建肋板式截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_ribbed_slab(
        h=2.8, bt=21.5, bt_sub=17.7, tt=0.3,
        b=0.2, eh=1.25, b1=1.8, b2=0.2, x=1.5, y=0.3,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建肋板式截面成功")


def test_create_TGirder():
    """测试创建T梁截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_TGirder(
        e_girder_pos="Middle", h=2.5, bs=1.125, bm=0.85, bc=0.0,
        tt1=0.16, tt2=0.25, x=0.6, tw=0.2,
        bh=0.6, hh=0.35, yh=0.25,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建T梁截面成功")


def test_create_custom():
    """测试创建自定义截面"""
    reset()
    cleanup_test_sections()
    # 1. 先定义轮廓点矩阵
    from pyosis.control import osis_matrix
    contour_matrix = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 1],
        [1, 0, 1],
    ]
    osis_matrix("ContourMatrix", contour_matrix)
    # 2. 再创建自定义截面
    sec = section_manager.create_custom("ContourMatrix")
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建自定义截面成功")


# ──────────────────────────────────────────────
# 新增钢截面测试
# ──────────────────────────────────────────────

def test_create_steel_box():
    """测试创建箱型钢截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_steel_box(
        h=2.0, bt=1.0, bct=0.4, bb=0.8, bcb=0.3,
        tt=0.02, tb=0.02, tw=0.015, same_layout=1,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建箱型钢截面成功")


def test_create_steel_box_three_cell():
    """测试创建单箱三室钢截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_steel_box_three_cell(
        h=3.0, bt=12.0, bb=6.0, i=0.02, a1=1.5, a2=1.2,
        dt=0.5, tt1=0.03, tt2=0.025, tb1=0.035, db=0.5,
        tb2=0.03, tb3=0.025, tw1=0.025, dw=3.0,
        has_web=1, tw2=0.02, web_rib_pos="Both",
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建单箱三室钢截面成功")


def test_create_steel_box_itf():
    """测试创建单箱单室斜顶板钢截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_steel_box_itf(
        h=2.5, b=12.0, bt=10.0, bb=6.0, i=0.02,
        a1=10.0, a2=15.0, dt=0.6, tt1=0.03, tt2=0.025, tt3=0.02,
        tb1=0.03, db=0.5, tb2=0.025, tb3=0.02, tw1=0.025,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建单箱单室斜顶板钢截面成功")


def test_create_steel_canti_box():
    """测试创建悬臂单箱双室钢截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_steel_canti_box(
        h=2.8, bt=15.0, bb=8.0, i=0.02, a=1.5, dt=0.5,
        tt1=0.03, tt2=0.025, tb1=0.035, tw1=0.025,
        has_web=1, tw2=0.02, web_rib_pos="Both", eh=0.3, et=0.015,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建悬臂单箱双室钢截面成功")


def test_create_steel_canti_box_ibf():
    """测试创建悬臂单箱双室斜底板钢截面"""
    reset()
    cleanup_test_sections()

    sec = section_manager.create_steel_canti_box_ibf(
        h=2.8, bt=15.0, bb=8.0, bc=2.0, i=0.02, a=1.5, dt=0.5,
        tt1=0.03, tt2=0.025, tb1=0.035, tb2=0.03,
        tw1=0.025, has_web=1, tw2=0.02, web_rib_pos="Both", eh=0.3, et=0.015,
    )
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建悬臂单箱双室斜底板钢截面成功")


def test_create_steel_custom():
    """测试创建自定义钢梁截面"""
    reset()
    cleanup_test_sections()
    # 1. 先定义点和线矩阵
    from pyosis.control import osis_matrix
    point_matrix = [
        [1, 0, 0],
        [2, 1, 0],
        [3, 1, 1],
        [4, 0, 1],
    ]
    line_matrix = [
        [1, 2, 0.02],
        [2, 3, 0.02],
        [3, 4, 0.02],
        [4, 1, 0.02],
    ]
    osis_matrix("PointMatrix", point_matrix)
    osis_matrix("LineMatrix", line_matrix)
    # 2. 再创建自定义钢截面
    sec = section_manager.create_steel_custom("PointMatrix", "LineMatrix")
    assert sec is not None, "截面应已创建"
    assert sec.name.startswith("SEC_")
    section_manager.delete(sec.no)
    print("✓ 创建自定义钢梁截面成功")

if __name__ == "__main__":
    print("开始测试 SectionManager...")
    print("=" * 50)
    tests = [
        # 基础测试
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
        # 新增混凝土截面测试
        test_create_smallbox,
        test_create_hollowslab,
        test_create_rounded_end,
        test_create_conventionalbox,
        test_create_flat_box,
        test_create_double_side_box,
        test_create_ribbed_slab,
        test_create_TGirder,
        test_create_custom,
        # 新增钢截面测试
        test_create_steel_box,
        test_create_steel_box_three_cell,
        test_create_steel_box_itf,
        test_create_steel_canti_box,
        test_create_steel_canti_box_ibf,
        test_create_steel_custom,
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
