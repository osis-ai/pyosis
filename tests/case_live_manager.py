# tests/case_live_manager.py

"""
活载管理测试
"""
from pyosis.live import (
    live_manager,
    osis_livegrade_highway,
    osis_livegrade_vehicle,
    osis_livegrade_crowd,
    osis_livegrade_fatigue,
    osis_livegrade_del,
    osis_livegrade_mod,
    osis_live_analysis,
    osis_live_analysis_del,
    osis_live_analysis_mod,
    osis_live_analysis_inc,
    osis_live_analysis_inc_mod,
    osis_live_analysis_factor,
    osis_live_analysis_option,
    osis_lane_ve,
    osis_lane_del,
    osis_lane_mod,
)


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
            osis_lane_del(lane)
        except:
            pass

    # 清理活载工况
    for analysis in TEST_ANALYSIS:
        try:
            osis_live_analysis_del(analysis)
        except:
            pass

    # 清理活载等级
    for grade in TEST_GRADES:
        try:
            osis_livegrade_del(grade)
        except:
            pass


# ──────────────────────────────────────────────
# 活载等级测试 (grade.py)
# ──────────────────────────────────────────────

def test_livegrade_highway():
    """测试公路活载"""
    cleanup_test_live()

    ok, err = osis_livegrade_highway("测试公路-I", eCode="JTGD60_2015", eLiveLoadType="HIGHWAY_I")
    assert ok, f"创建公路活载失败: {err}"
    print("✓ 创建公路活载成功")

    # 清理
    osis_livegrade_del("测试公路-I")


def test_livegrade_vehicle():
    """测试车辆荷载"""
    cleanup_test_live()

    ok, err = osis_livegrade_vehicle("测试车辆", eCode="JTGD60_2015", eLiveLoadType="VEHICLE")
    assert ok, f"创建车辆荷载失败: {err}"
    print("✓ 创建车辆荷载成功")

    # 清理
    osis_livegrade_del("测试车辆")


def test_livegrade_crowd():
    """测试人群荷载"""
    cleanup_test_live()

    ok, err = osis_livegrade_crowd(
        "测试人群", eCode="JTGD60_2015", eLiveLoadType="CROWD",
        eBridgeType="BRIDGE_COMMON", dPara=10.0
    )
    assert ok, f"创建人群荷载失败: {err}"
    print("✓ 创建人群荷载成功")

    # 清理
    osis_livegrade_del("测试人群")


def test_livegrade_fatigue():
    """测试疲劳模型"""
    cleanup_test_live()

    ok, err = osis_livegrade_fatigue(
        "测试疲劳", eCode="JTGD60_2015", eLiveLoadType="FATIGUE_I"
    )
    assert ok, f"创建疲劳模型失败: {err}"
    print("✓ 创建疲劳模型成功")

    # 清理
    osis_livegrade_del("测试疲劳")


def test_livegrade_mod():
    """测试修改活载等级名称"""
    cleanup_test_live()

    # 先创建
    ok, err = osis_livegrade_highway("旧名称", eCode="JTGD60_2015", eLiveLoadType="HIGHWAY_I")
    assert ok, f"创建公路活载失败: {err}"

    # 再修改
    ok, err = osis_livegrade_mod("旧名称", "新名称")
    assert ok, f"修改活载等级名称失败: {err}"
    print("✓ 修改活载等级名称成功")

    # 清理
    osis_livegrade_del("新名称")


# ──────────────────────────────────────────────
# 活载工况测试 (analysis.py)
# ──────────────────────────────────────────────

def test_live_analysis():
    """测试活载工况定义"""
    cleanup_test_live()

    ok, err = osis_live_analysis("测试工况", "JTGD60_2015", 1)
    assert ok, f"创建活载工况失败: {err}"
    print("✓ 创建活载工况成功")

    # 清理
    osis_live_analysis_del("测试工况")


def test_live_analysis_mod():
    """测试修改活载工况名称"""
    cleanup_test_live()

    # 先创建
    ok, err = osis_live_analysis("旧工况", "JTGD60_2015", 1)
    assert ok, f"创建活载工况失败: {err}"

    # 再修改
    ok, err = osis_live_analysis_mod("旧工况", "新工况")
    assert ok, f"修改活载工况名称失败: {err}"
    print("✓ 修改活载工况名称成功")

    # 清理
    osis_live_analysis_del("新工况")


def test_live_analysis_inc():
    """测试活载子工况"""
    cleanup_test_live()

    # 先创建活载等级和车道
    osis_livegrade_highway("测试公路-I", eCode="JTGD60_2015", eLiveLoadType="HIGHWAY_I")
    osis_lane_ve("测试车道", "VE", 30.0, 1, 0, 0, ["主梁单元组", 2.5, 0.0])
    osis_live_analysis("测试工况", "JTGD60_2015", 1)

    # 添加子工况
    ok, err = osis_live_analysis_inc(
        "测试工况", "a", "子工况1", "测试公路-I",
        1.0, 1, "SIMPLE", [30.0, 3.5e10, 0.1, 1000.0],
        ["测试车道"]
    )
    assert ok, f"添加子工况失败: {err}"
    print("✓ 添加活载子工况成功")

    # 清理
    cleanup_test_live()


def test_live_analysis_factor():
    """测试横向折减系数"""
    cleanup_test_live()

    # 先创建工况
    osis_live_analysis("测试工况", "JTGD60_2015", 1)

    # 设置横向折减系数
    ok, err = osis_live_analysis_factor("测试工况", 1.0, 0.85, 0.7)
    assert ok, f"设置横向折减系数失败: {err}"
    print("✓ 设置横向折减系数成功")

    # 清理
    osis_live_analysis_del("测试工况")


def test_live_analysis_option():
    """测试加载车道数"""
    cleanup_test_live()

    # 先创建工况和子工况
    osis_livegrade_highway("测试公路-I", eCode="JTGD60_2015", eLiveLoadType="HIGHWAY_I")
    osis_live_analysis("测试工况", "JTGD60_2015", 1)
    osis_live_analysis_inc(
        "测试工况", "a", "子工况1", "测试公路-I",
        1.0, 1, "SIMPLE", [30.0, 3.5e10, 0.1, 1000.0],
        []
    )

    # 设置加载车道数
    ok, err = osis_live_analysis_option("测试工况", "子工况1", 1, 3)
    assert ok, f"设置加载车道数失败: {err}"
    print("✓ 设置加载车道数成功")

    # 清理
    cleanup_test_live()


# ──────────────────────────────────────────────
# 车道测试 (lane.py)
# ──────────────────────────────────────────────

def test_lane_ve():
    """测试车道单元法"""
    cleanup_test_live()

    ok, err = osis_lane_ve(
        "测试车道", "VE", 30.0, 1, 0, 0,
        ["主梁单元组", 2.5, 0.0]
    )
    assert ok, f"创建车道失败: {err}"
    print("✓ 创建车道成功")

    # 清理
    osis_lane_del("测试车道")


def test_lane_mod():
    """测试修改车道名称"""
    cleanup_test_live()

    # 先创建
    ok, err = osis_lane_ve(
        "旧车道", "VE", 30.0, 1, 0, 0,
        ["主梁单元组", 2.5, 0.0]
    )
    assert ok, f"创建车道失败: {err}"

    # 再修改
    ok, err = osis_lane_mod("旧车道", "新车道")
    assert ok, f"修改车道名称失败: {err}"
    print("✓ 修改车道名称成功")

    # 清理
    osis_lane_del("新车道")


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
