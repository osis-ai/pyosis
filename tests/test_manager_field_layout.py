"""管理器字段布局离线测试：不连接 OSIS，只抓取将要发出的命令串。

覆盖命令流字段序与 manager 形参序不一致的场景：型钢截面、扁平箱梁、
先张法钢束、VECTOR 单向支承、土弹簧、Inflow eRef=1、PLANE/DISTRB、
屈曲/荷载转换 OP、SeisRspSpec 导入、强度进展曲线。
"""
from __future__ import annotations

import contextlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pyosis.core import REGISTRY
from pyosis.core.command import REGISTRY as CMD_REGISTRY
import pyosis.boundary.manager as bm
import pyosis.dynamic.manager as dm
import pyosis.live.manager as lvm
import pyosis.load.manager as lm
import pyosis.property.strength_prog as sp
import pyosis.section.manager as sm
import pyosis.stability.manager as stm

CAPTURED: list[str] = []


@contextlib.contextmanager
def capture(module, *names):
    """把模块里的 osis_* 底层函数替换为命令串捕获器，返回捕获列表。"""
    saved = {}
    try:
        for name in names:
            orig = getattr(module, name)
            saved[name] = orig

            def inner(*args, _f=orig, **kwargs):
                info = CMD_REGISTRY.commands[_f.__name__]
                cmd, _ = CMD_REGISTRY._process_arguments(
                    info["func"], info["cmd_name"], *args, **kwargs
                )
                CAPTURED.append(cmd)
                return (True, "")

            setattr(module, name, inner)
        yield CAPTURED
    finally:
        for name, orig in saved.items():
            setattr(module, name, orig)


def _manager(cls, **stub):
    obj = cls()
    for k, v in stub.items():
        setattr(obj, k, v)
    return obj


# ── 截面 ──────────────────────────────────────────────────────

def _section(no: int = 1):
    """Section 是 dataclass 实体，这里只借用实例方法，不构造完整字段。"""
    s = sm.Section.__new__(sm.Section)
    s.no = no
    return s


def test_section_mesh_param_order():
    """set_mesh 形参序与 SectionMesh, Index, PartID, MeshMethod, MeshSize 一致"""
    with capture(sm, "osis_section_mesh"):
        _section(1).set_mesh(2, 1, 0.25)
    assert CAPTURED == ["SectionMesh,1,2,1,0.25;"], CAPTURED
    CAPTURED.clear()


def test_section_part_param_order():
    """add_part 的 PartGeoType 保持在命令流原位置，不做前置"""
    with capture(sm, "osis_section_part_polygon", "osis_section_part_line"):
        _section(2).add_part(1, "Concrete", 3e10, 0.2, 2.5, "Polygon", "M1", "W1")
        _section(2).add_part(2, "Steel", 2e11, 0.3, 7.8, "Line", "P1", "L1", "W2")
    assert CAPTURED == [
        "SectionPart,2,1,Concrete,30000000000.0,0.2,2.5,Polygon,M1,W1;",
        "SectionPart,2,2,Steel,200000000000.0,0.3,7.8,Line,P1,L1,W2;",
    ], CAPTURED
    CAPTURED.clear()


def test_shaped_steel_manual_and_catalog():
    m = _manager(sm.SectionManager, get=lambda n: n)
    with capture(sm, "osis_section_shaped_steel_l", "osis_section_shaped_steel_l_catalog"):
        m.create(1, "S1", "SteelL", 0, 0.1, 0.1, 0.016, 0.016)
        m.create(2, "S2", "SteelL", 1, "GB_YB", "L20")
    assert CAPTURED == [
        "Section,1,S1,SteelL,0,0.1,0.1,0.016,0.016;",
        "Section,2,S2,SteelL,1,GB_YB,L20;",
    ], CAPTURED
    CAPTURED.clear()


def test_flat_box_alias_by_field_count():
    """文档扁平箱梁 Type=ConventionalBox，51 字段应走 STREAMEDBOX。"""
    flat = list(range(51))
    m = _manager(sm.SectionManager, get=lambda n: n)
    with capture(sm, "osis_section_streamed_box"):
        m.create(1, "FB", "ConventionalBox", *flat)
    assert CAPTURED and CAPTURED[0].startswith("Section,1,FB,STREAMEDBOX,"), CAPTURED
    CAPTURED.clear()


def test_legacy_steel_i_and_box_migrate():
    """旧 .out 的 STEELI/STEELBOX 按字段数迁移到钢梁截面。"""
    m = _manager(sm.SectionManager, get=lambda n: n)
    with capture(sm, "osis_section_steel_i", "osis_section_steel_box"):
        m.create(1, "S1", "STEELI", 2.0, 1.0, 1.0, 0.02, 0.02, 0.012, "Both")
        m.create(2, "S2", "STEELBOX", 2.0, 1.0, 0.2, 1.0, 0.2, 0.02, 0.02, 0.012, 1)
    assert CAPTURED[0].startswith("Section,1,S1,STEELBEAMI,"), CAPTURED
    assert CAPTURED[1].startswith("Section,2,S2,STEELBEAMBOX,"), CAPTURED
    CAPTURED.clear()


# ── 钢束 / 荷载 ───────────────────────────────────────────────

def test_pre_tendon_has_no_pipe():
    m = _manager(lm.TendonPropManager, get=lambda n: n)
    with capture(lm, "osis_tendon_prop_pre_area0", "osis_tendon_prop_pre_area1"):
        m.create("P1", "PRE", 1, 0, 0.00014, 7.0, 0.8, 0.7)
        m.create("P2", "PRE", 1, 1, "GBT5224", 12.7, 5, 7.0, 0.8, 0.7)
    assert CAPTURED == [
        "TdProp,P1,PRE,1,0,0.00014,7.0,0.8,0.7;",
        "TdProp,P2,PRE,1,1,GBT5224,12.7,5,7.0,0.8,0.7;",
    ], CAPTURED
    CAPTURED.clear()


def test_plane_load_flat_points():
    lc = lm.LoadCase("LC1", 1, 1.0, "")
    lc.refresh = lambda: lc
    with capture(lm, "osis_load_plane"):
        lc.create(
            "PLANE", "PL1", "SHELL",
            0, 0, 0, 1, 0, 0, 0, 1, 0, 0.01, 1, "EG1", 1,
            "SurfaceN", "NoProjection", 0, "X",
        )
    assert CAPTURED == [
        "Load,Plane,LC1,PL1,SHELL,0,0,0,1,0,0,0,1,0,0.01,1,EG1,1,"
        "SurfaceN,NoProjection,0,X;"
    ], CAPTURED
    CAPTURED.clear()


def test_distrb_point_count():
    lc = lm.LoadCase("LC1", 1, 1.0, "")
    lc.refresh = lambda: lc
    with capture(lm, "osis_load_distrb"):
        lc.create("DISTRB", 3, 0, 0, 0, 2, *range(1, 19))
    assert CAPTURED[0] == "Load,DISTRB,LC1,3,0,0,0,2," + ",".join(map(str, range(1, 19))) + ";", CAPTURED
    CAPTURED.clear()


# ── 边界 ──────────────────────────────────────────────────────

def test_unispt_vector_positional():
    m = _manager(bm.BoundaryManager, get=lambda n: n)
    with capture(bm, "osis_boundary_unispt"):
        m.create(2, "UNISPT", "N", 1000.0, "VECTOR", 1.0, 0.0, 0.0)
    assert CAPTURED == ["Boundary,2,UNISPT,N,1000.0,VECTOR,1.0,0.0,0.0;"], CAPTURED
    CAPTURED.clear()


def test_soilspring_sand_empty_tail():
    m = _manager(bm.BoundaryManager, get=lambda n: n)
    with capture(bm, "osis_boundary_soilspring"):
        m.create(1, "SOILSPRING", 0, 1, "SAND", 0.0, 1.0, 18.0, 30.0, "", "", "")
    assert CAPTURED == ["Boundary,1,SOILSPRING,,1,SAND,0.0,1.0,18.0,30.0,,,;"], CAPTURED
    CAPTURED.clear()


def test_stage_boundary_optional_pos():
    """StgBd 的 pos 缺省时不进命令流，显式传入时追加在 grp 之后"""
    info = CMD_REGISTRY.commands["osis_stage_boundary"]
    func, name = info["func"], info["cmd_name"]
    cmd, _ = CMD_REGISTRY._process_arguments(func, name, 1, 1, 1, "边界组")
    assert cmd == "StgBd,1,1,1,边界组;", cmd
    cmd, _ = CMD_REGISTRY._process_arguments(func, name, 1, 1, 1, "边界组", 0)
    assert cmd == "StgBd,1,1,1,边界组,0;", cmd


# ── 车道 / 活载 ───────────────────────────────────────────────

def test_infl_algo_ref1_manager_emits_two_params():
    m = _manager(lvm.LaneManager, get=lambda n: n)
    with capture(lvm, "osis_lane_ve", "osis_lane_tcb"):
        m.create("L1", "VE", 120.0, 1, 1, 1, "EG", "SP1")
        m.create("L2", "TCB", "EGT", 40.0, 1, 1, 1, "EG", "SP1")
    assert CAPTURED == [
        "InflAlgo,L1,VE,120.0,1,1,1,EG,SP1;",
        "InflAlgo,L2,TCB,EGT,40.0,1,1,1,EG,SP1;",
    ], CAPTURED
    CAPTURED.clear()


def test_live_anal_inc_muflag_zero_keeps_first_lane():
    case = lvm.LiveCase(1, "L1", list(lvm.AnalysisType)[0], 0, False, 10)
    case.refresh = lambda: case
    with capture(lvm, "osis_live_analysis_inc"):
        case.include("a", "SUB1", "G1", 1.0, 0, "LANE1", "LANE2")
    assert CAPTURED == ["LiveAnalInc,L1,a,SUB1,G1,1.0,0,LANE1,LANE2;"], CAPTURED
    CAPTURED.clear()


# ── 动力 / 稳定 / 强度进展 ────────────────────────────────────

def test_buckl_inc_substitute():
    b = stm.BucklCase(
        accum=0, accumLCParas={}, analysisType=0, lcParas=[],
        modalNum=5, name="B1", no=1, relatedStages=[],
    )
    with capture(stm, "osis_buckl_anal_inc"):
        b.include("s", "LC2", 1.2, 0, "LC1", 1.0, 0)
    assert CAPTURED == ["BucklAnalInc,B1,s,LC2,1.2,0,LC1,1.0,0;"], CAPTURED
    CAPTURED.clear()


def test_ltm_inc_dispatch_op():
    m = dm.LoadToMass(name="M1", no=1)
    with capture(dm, "osis_ltm_anal_inc"):
        m.include("a", "LC1", 2.0, 9.806, 1, 1, 1, 1, 1, 1)
        m.include("r", "LC1")
    assert CAPTURED[0] == "LTMAnalInc,M1,a,LC1,2.0,9.806,1,1,1,1,1,1;", CAPTURED
    assert CAPTURED[1].startswith("LTMAnalInc,M1,r,LC1,"), CAPTURED
    CAPTURED.clear()


def test_seis_import_num_before_spectrum():
    m = _manager(dm.SeisRspSpecManager, get=lambda n: n)
    with capture(dm, "osis_seis_rsp_spec_import"):
        m.create("RS1", "A", 9.806, 0, 2, 0.1, 0.5, 0.2, 0.8)
        m.create("RS1", "A", 9.806, 0, [(0.1, 0.5), (0.2, 0.8)])
    assert CAPTURED == [
        "SeisRspSpec,RS1,A,9.806,0,2,0.1,0.5,0.2,0.8;",
        "SeisRspSpec,RS1,A,9.806,0,2,0.1,0.5,0.2,0.8;",
    ], CAPTURED
    CAPTURED.clear()


def test_strength_prog_custom_flat_curve():
    m = sp.StrengthProgManager()
    with capture(sp, "osis_strength_prog_custom"):
        m.create("SP1", "CUSTOM", 1.0, 1, 20, 2, 3e10, 28, 50, 3, 3.2e10)
        m.create_custom("SP1", 1.0, curve=[1, 20, 2, 3e10, 28, 50, 3, 3.2e10])
    assert CAPTURED[0] == CAPTURED[1], CAPTURED
    assert CAPTURED[0].startswith("StrengthPrg,SP1,CUSTOM,1.0,1.0,20.0,"), CAPTURED
    CAPTURED.clear()


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        CAPTURED.clear()
        try:
            fn()
            print(f"{fn.__name__}: OK")
        except AssertionError as e:
            failed += 1
            print(f"{fn.__name__}: FAIL {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} 通过")
    sys.exit(1 if failed else 0)
