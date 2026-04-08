# tests/case_section_manager.py

"""
SectionManager 接口测试（手动运行版）
"""
from pyosis.section import section_manager


# 测试用编号列表
TEST_NOS = [
    # 基础测试（原有）
    9999, 9998, 9997, 9996, 9995, 9994, 9993, 9990, 9980, 9989,
    # 新增混凝土截面测试
    9901, 9902, 9903, 9904, 9905, 9906, 9907, 9908, 9909,
    # 新增钢截面测试
    9911, 9912, 9913, 9914, 9915, 9916,
]


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


# ──────────────────────────────────────────────
# 新增混凝土截面测试
# ──────────────────────────────────────────────

def test_create_smallbox():
    """测试创建小箱梁截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_smallbox(
        9901, "测试小箱梁",
        eGirderPos="MIDDLE", H=1.6, Bs=1.65, Bm=1.2, Bb=1.0,
        Tt=0.18, Tb=0.2, Tw=0.2
    )
    sec = section_manager.get(9901)
    assert sec is not None, "截面9901应存在"
    assert sec.name == "测试小箱梁"
    section_manager.delete(9901)
    print("✓ 创建小箱梁截面成功")


def test_create_hollowslab():
    """测试创建空心板截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_hollowslab(
        9902, "测试空心板",
        eGirderPos="MIDDLE", H=0.95, Bs=1.0, Bm=0.57, Tt=0.12, Tb=0.12, Tw=0.16
    )
    sec = section_manager.get(9902)
    assert sec is not None, "截面9902应存在"
    assert sec.name == "测试空心板"
    section_manager.delete(9902)
    print("✓ 创建空心板截面成功")


def test_create_rounded_end():
    """测试创建圆端形截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_rounded_end(
        9903, "测试圆端形",
        eFillingType="Solid", B=7.0, H=3.0, R=2.0
    )
    sec = section_manager.get(9903)
    assert sec is not None, "截面9903应存在"
    assert sec.name == "测试圆端形"
    section_manager.delete(9903)
    print("✓ 创建圆端形截面成功")


def test_create_conventionalbox():
    """测试创建常规箱梁截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_conventionalbox(
        9904, "测试常规箱梁",
        H=2.7, BtL=6.375, BtR=6.375, BbL=3.5, BbR=3.5, Bs=0.5,
        Tt=0.28, Tb=0.32, Tw1=0.5, Tw2=0.5, nCellNum=1
    )
    sec = section_manager.get(9904)
    assert sec is not None, "截面9904应存在"
    assert sec.name == "测试常规箱梁"
    section_manager.delete(9904)
    print("✓ 创建常规箱梁截面成功")


def test_create_flat_box():
    """测试创建扁平箱梁截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_flat_box(
        9905, "测试扁平箱梁","STREAMEDBOX",
        H=4.0, BtL=20.0, BtR=20.0, BbL=10.5, BbR=10.5, Bs=0.8,
        Tt=0.28, Tb1=0.27, Tb2=0.27, Tw=0.25, nCellNum=5
    )
    sec = section_manager.get(9905)
    assert sec is not None, "截面9905应存在"
    assert sec.name == "测试扁平箱梁"
    section_manager.delete(9905)
    print("✓ 创建扁平箱梁截面成功")


def test_create_double_side_box():
    """测试创建双边箱截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_double_side_box(
        9906, "测试双边箱",
        H=3.8, Bt=36.0, bt=14.8, Bs=2.1, Bb=4.4,
        tt=0.3, Tb1=0.3, Tb2=0.3, Tw=0.5, Bi=8.0
    )
    sec = section_manager.get(9906)
    assert sec is not None, "截面9906应存在"
    assert sec.name == "测试双边箱"
    section_manager.delete(9906)
    print("✓ 创建双边箱截面成功")


def test_create_ribbed_slab():
    """测试创建肋板式截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_ribbed_slab(
        9907, "测试肋板式",
        H=2.8, Bt=21.5, bt=17.7, Tt=0.3,
        b=0.2, h=1.25, b1=1.8, b2=0.2, x=1.5, y=0.3
    )
    sec = section_manager.get(9907)
    assert sec is not None, "截面9907应存在"
    assert sec.name == "测试肋板式"
    section_manager.delete(9907)
    print("✓ 创建肋板式截面成功")


def test_create_TGirder():
    """测试创建T梁截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_TGirder(
        9908, "测试T梁",
        eGirderPos="Middle", H=2.5, Bs=1.125, Bm=0.85, Bc=0.0,
        Tt1=0.16, Tt2=0.25, x=0.6, Tw=0.2,
        Bh=0.6, Hh=0.35, yh=0.25
    )
    sec = section_manager.get(9908)
    assert sec is not None, "截面9908应存在"
    assert sec.name == "测试T梁"
    section_manager.delete(9908)
    print("✓ 创建T梁截面成功")


def test_create_custom():
  """测试创建自定义截面"""
  reset()
  cleanup_test_sections()
  # 1. 先定义轮廓点矩阵
  from pyosis.common import osis_matrix
  contour_matrix = [
      [1, 0, 0],
      [2, 1, 0],
      [3, 1, 1],
      [4, 0, 1],
  ]
  osis_matrix("ContourMatrix", contour_matrix)
  # 2. 再创建自定义截面
  section_manager.create_custom(9909, "测试自定义", "ContourMatrix")
  sec = section_manager.get(9909)
  assert sec is not None, "截面9909应存在"
  assert sec.name == "测试自定义"
  section_manager.delete(9909)
  print("✓ 创建自定义截面成功")


# ──────────────────────────────────────────────
# 新增钢截面测试
# ──────────────────────────────────────────────

def test_create_steel_box():
    """测试创建箱型钢截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_steel_box(
        9911, "测试箱型钢",
        H=2.0, Bt=1.0, Bct=0.4, Bb=0.8, Bcb=0.3,
        Tt=0.02, Tb=0.02, Tw=0.015, SameLayout=1
    )
    sec = section_manager.get(9911)
    assert sec is not None, "截面9911应存在"
    assert sec.name == "测试箱型钢"
    section_manager.delete(9911)
    print("✓ 创建箱型钢截面成功")


def test_create_steel_box_three_cell():
    """测试创建单箱三室钢截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_steel_box_three_cell(
        9912, "测试单箱三室",
        H=3.0, Bt=12.0, Bb=6.0, i=0.02, a1=1.5, a2=1.2,
        Dt=0.5, Tt1=0.03, Tt2=0.025, Tb1=0.035, Db=0.5,
        Tb2=0.03, Tb3=0.025, Tw1=0.025, Dw=3.0,
        HasWeb=1, Tw2=0.02, WebRibPos="Both"
    )
    sec = section_manager.get(9912)
    assert sec is not None, "截面9912应存在"
    assert sec.name == "测试单箱三室"
    section_manager.delete(9912)
    print("✓ 创建单箱三室钢截面成功")


def test_create_steel_box_itf():
    """测试创建单箱单室斜顶板钢截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_steel_box_itf(
        9913, "测试斜顶板箱型",
        H=2.5, B=12.0, Bt=10.0, Bb=6.0, i=0.02,
        a1=10.0, a2=15.0, Dt=0.6, Tt1=0.03, Tt2=0.025, Tt3=0.02,
        Tb1=0.03, Db=0.5, Tb2=0.025, Tb3=0.02, Tw1=0.025
    )
    sec = section_manager.get(9913)
    assert sec is not None, "截面9913应存在"
    assert sec.name == "测试斜顶板箱型"
    section_manager.delete(9913)
    print("✓ 创建单箱单室斜顶板钢截面成功")


def test_create_steel_canti_box():
    """测试创建悬臂单箱双室钢截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_steel_canti_box(
        9914, "测试悬臂箱型",
        H=2.8, Bt=15.0, Bb=8.0, i=0.02, a=1.5, Dt=0.5,
        Tt1=0.03, Tt2=0.025, Tb1=0.035, Tw1=0.025,
        HasWeb=1, Tw2=0.02, WebRibPos="Both", h=0.3, t=0.015
    )
    sec = section_manager.get(9914)
    assert sec is not None, "截面9914应存在"
    assert sec.name == "测试悬臂箱型"
    section_manager.delete(9914)
    print("✓ 创建悬臂单箱双室钢截面成功")


def test_create_steel_canti_box_ibf():
    """测试创建悬臂单箱双室斜底板钢截面"""
    reset()
    cleanup_test_sections()

    section_manager.create_steel_canti_box_ibf(
        9915, "测试悬臂斜底板箱型",
        H=2.8, Bt=15.0, Bb=8.0, Bc=2.0, i=0.02, a=1.5, Dt=0.5,
        Tt1=0.03, Tt2=0.025, Tb1=0.035, Tb2=0.03,
        Tw1=0.025, HasWeb=1, Tw2=0.02, WebRibPos="Both", h=0.3, t=0.015
    )
    sec = section_manager.get(9915)
    assert sec is not None, "截面9915应存在"
    assert sec.name == "测试悬臂斜底板箱型"
    section_manager.delete(9915)
    print("✓ 创建悬臂单箱双室斜底板钢截面成功")


def test_create_steel_custom():
  """测试创建自定义钢梁截面"""
  reset()
  cleanup_test_sections()
  # 1. 先定义点和线矩阵
  from pyosis.common import osis_matrix
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
  section_manager.create_steel_custom(9916, "测试自定义钢", "PointMatrix", "LineMatrix")
  sec = section_manager.get(9916)
  assert sec is not None, "截面9916应存在"
  assert sec.name == "测试自定义钢"
  section_manager.delete(9916)
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
