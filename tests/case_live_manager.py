# tests/case_live_manager.py

"""
活载管理测试
"""
from pyosis.live import live_manager


# ──────────────────────────────────────────────
# 测试名称列表
# ──────────────────────────────────────────────

TEST_GRADES = ["测试公路-I", "测试车辆", "测试人群", "测试疲劳"]
TEST_ANALYSIS = ["测试工况"]
TEST_LANES = ["测试车道"]


# ──────────────────────────────────────────────
# 清理函数
# ──────────────────────────────────────────────

def cleanup_test_live():
    """清理测试残留数据"""
    # 清理车道
    for lane in TEST_LANES:
        try:
            live_manager.lane.delete(lane)
        except:
            pass

    # 清理活载工况
    for analysis in TEST_ANALYSIS:
        try:
            live_manager.case.delete(analysis)
        except:
            pass

    # 清理活载等级
    for grade in TEST_GRADES:
        try:
            live_manager.grade.delete(grade)
        except:
            pass


# ──────────────────────────────────────────────
# 活载等级测试
# ──────────────────────────────────────────────

def test_livegrade_highway():
    """测试公路活载"""
    cleanup_test_live()

    grade = live_manager.grade.create_highway("测试公路-I", "JTGD60_2015", "HIGHWAY_I")
    assert grade is not None
    assert grade.name == "测试公路-I"
    print("✓ 创建公路活载成功")

    # 清理
    live_manager.grade.delete("测试公路-I")


def test_livegrade_vehicle():
    """测试车辆荷载"""
    cleanup_test_live()

    grade = live_manager.grade.create_vehicle("测试车辆", "JTGD60_2015")
    assert grade is not None
    assert grade.name == "测试车辆"
    print("✓ 创建车辆荷载成功")

    # 清理
    live_manager.grade.delete("测试车辆")


def test_livegrade_crowd():
    """测试人群荷载"""
    cleanup_test_live()

    grade = live_manager.grade.create_crowd("测试人群", "BRIDGE_COMMON", 10.0)
    assert grade is not None
    assert grade.name == "测试人群"
    print("✓ 创建人群荷载成功")

    # 清理
    live_manager.grade.delete("测试人群")


def test_livegrade_fatigue():
    """测试疲劳模型"""
    cleanup_test_live()

    grade = live_manager.grade.create_fatigue("测试疲劳", "FATIGUE_I")
    assert grade is not None
    assert grade.name == "测试疲劳"
    print("✓ 创建疲劳模型成功")

    # 清理
    live_manager.grade.delete("测试疲劳")


def test_livegrade_mod():
    """测试修改活载等级名称"""
    cleanup_test_live()

    # 先创建
    grade = live_manager.grade.create_highway("旧名称", "JTGD60_2015", "HIGHWAY_I")
    assert grade is not None

    # 再修改
    live_manager.grade.rename("旧名称", "新名称")
    print("✓ 修改活载等级名称成功")

    # 清理
    live_manager.grade.delete("新名称")


# ──────────────────────────────────────────────
# 活载工况测试
# ──────────────────────────────────────────────

def test_live_analysis():
    """测试活载工况定义"""
    cleanup_test_live()

    live_case = live_manager.case.create("测试工况", "JTGD60_2015", 1)
    assert live_case is not None
    assert live_case.name == "测试工况"
    print("✓ 创建活载工况成功")

    # 清理
    live_manager.case.delete("测试工况")


def test_live_analysis_mod():
    """测试修改活载工况名称"""
    cleanup_test_live()

    # 先创建
    live_case = live_manager.case.create("旧工况", "JTGD60_2015", 1)
    assert live_case is not None

    # 再修改
    live_manager.case.rename("旧工况", "新工况")
    print("✓ 修改活载工况名称成功")

    # 清理
    live_manager.case.delete("新工况")


def test_live_analysis_inc():
    """测试活载子工况"""
    cleanup_test_live()

    # 先创建活载等级和车道
    grade = live_manager.grade.create_highway("测试公路-I", "JTGD60_2015", "HIGHWAY_I")
    lane = live_manager.lane.create_ve("测试车道", 30.0, ref_elems="主梁单元组", offsetY=2.5)
    live_case = live_manager.case.create("测试工况", "JTGD60_2015", 1)

    # 添加子工况
    live_case.create_sub(
        sub_name="子工况1",
        grade_name="测试公路-I",
        scalar=1.0,
        calc_mu=True,
        bridge_type="SIMPLE",
        mu_params=[30.0, 3.5e10, 0.1, 1000.0],
        lane_names=["测试车道"],
    )
    print("✓ 添加活载子工况成功")

    # 清理
    cleanup_test_live()


def test_live_analysis_factor():
    """测试横向折减系数"""
    cleanup_test_live()

    # 先创建工况
    live_case = live_manager.case.create("测试工况", "JTGD60_2015", 1)

    # 设置横向折减系数
    live_case.set_trans_reduction_factors([1.0, 0.85, 0.7])
    print("✓ 设置横向折减系数成功")

    # 清理
    live_manager.case.delete("测试工况")


def test_live_analysis_option():
    """测试加载车道数"""
    cleanup_test_live()

    # 先创建工况和子工况
    grade = live_manager.grade.create_highway("测试公路-I", "JTGD60_2015", "HIGHWAY_I")
    live_case = live_manager.case.create("测试工况", "JTGD60_2015", 1)
    live_case.create_sub(
        sub_name="子工况1",
        grade_name="测试公路-I",
        calc_mu=True,
        bridge_type="SIMPLE",
        mu_params=[30.0, 3.5e10, 0.1, 1000.0],
    )

    # 设置加载车道数
    live_case.set_lane_count("子工况1", 1, 3)
    print("✓ 设置加载车道数成功")

    # 清理
    cleanup_test_live()


# ──────────────────────────────────────────────
# 车道测试
# ──────────────────────────────────────────────

def test_lane_ve():
    """测试车道单元法"""
    cleanup_test_live()

    lane = live_manager.lane.create_ve(
        "测试车道", 30.0,
        ref_elems="主梁单元组", offsetY=2.5,
    )
    assert lane is not None
    assert lane.name == "测试车道"
    print("✓ 创建车道成功")

    # 清理
    live_manager.lane.delete("测试车道")


def test_lane_mod():
    """测试修改车道名称"""
    cleanup_test_live()

    # 先创建
    lane = live_manager.lane.create_ve(
        "旧车道", 30.0,
        ref_elems="主梁单元组", offsetY=2.5,
    )
    assert lane is not None

    # 再修改
    live_manager.lane.rename("旧车道", "新车道")
    print("✓ 修改车道名称成功")

    # 清理
    live_manager.lane.delete("新车道")


# ──────────────────────────────────────────────
# 主函数
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("开始测试 Live 模块...")
    print("=" * 50)

    tests = [
        # 活载等级
        test_livegrade_highway,
        test_livegrade_vehicle,
        test_livegrade_crowd,
        test_livegrade_fatigue,
        test_livegrade_mod,
        # 活载工况
        test_live_analysis,
        test_live_analysis_mod,
        test_live_analysis_inc,
        test_live_analysis_factor,
        test_live_analysis_option,
        # 车道
        test_lane_ve,
        test_lane_mod,
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
