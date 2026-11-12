"""transfer 转换器离线测试：字段与位置参数严格对应、命令名归一、编码。

不依赖 OSIS 服务端：只做「命令流文本 → Python 调用行」的纯文本转换。
断言直接写出完整调用行，便于逐列核对命令流字段与实参。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pyosis.transfer.generator import generate_lines
from pyosis.transfer.out_to_python import _read_out_text
from pyosis.transfer.parser import parse_text


def _gen(text: str):
    return generate_lines(parse_text(text))


# ── 通用规则：字段 = 位置参数 ─────────────────────────────────

def test_creep_shrink_new9_positional():
    """CrpShrk 9 字段原序生成，无关键字实参"""
    lines = _gen("CrpShrk,3,新,JTG3362_2018,4.5e7,60,1,5,3,0;\n")
    assert lines == [
        'engine.prop.creep_shrink.create(3, "新", "JTG3362_2018", '
        "45000000.0, 60, 1, 5, 3, 0)"
    ], lines


def test_section_mesh_part_id_first():
    """SectionMesh, Index, PartID, MeshMethod, MeshSize → set_mesh(PartID, Method, Size)"""
    lines = _gen("SecMesh,1,1,0,0.1;\n")
    assert lines == ["engine.section.get(1).set_mesh(1, 0, 0.1)"], lines


def test_section_part_geo_type_in_place():
    """SectionPart 的 PartGeoType 保持在命令流中的位置，不做前置"""
    lines = _gen("SectionPart,2,1,Concrete,3e10,0.2,2.5,Polygon,M1,M2;\n")
    assert lines == [
        'engine.section.get(2).add_part(1, "Concrete", 30000000000.0, '
        '0.2, 2.5, "Polygon", "M1", "M2")'
    ], lines


def test_infl_algo_ref0_three_params():
    """InflAlgo VE ref=0: par1..par3 → 三个尾部位置参数"""
    lines = _gen("InflAlgo,L1,VE,120,1,1,0,EG,0,0;\n")
    assert lines == [
        'engine.live.lane.create("L1", "VE", 120, 1, 1, 0, "EG", 0, 0)'
    ], lines


def test_infl_algo_ref1_ve_no_placeholder():
    """InflAlgo VE ref=1: 命令流只有 par1/par2，转换器不补空位"""
    lines = _gen("InflAlgo,L2,VE,120,1,1,1,EG,SP1;\n")
    assert lines == [
        'engine.live.lane.create("L2", "VE", 120, 1, 1, 1, "EG", "SP1")'
    ], lines


def test_infl_algo_ref1_tcb_no_placeholder():
    lines = _gen("InflAlgo,L4,TCB,EGT,40,1,1,1,EG,SP1;\n")
    assert lines == [
        'engine.live.lane.create("L4", "TCB", "EGT", 40, 1, 1, 1, "EG", "SP1")'
    ], lines


def test_long_signature_stays_positional():
    """长签名不再自动生成关键字实参"""
    lines = _gen("CrpShrk,3,新,JTG3362_2018,4.5e7,60,1,5,3,0;\n")
    assert "=" not in lines[0], lines


def test_short_signature_positional():
    lines = _gen("Node,1,1.0,2.0,3.0;\n")
    assert lines == ["engine.node.create(1, 1.0, 2.0, 3.0)"], lines


def test_varargs_passthrough():
    """*args 透传型（Material 等）按原序展开"""
    lines = _gen("Material,1,C50,CONC,JTG3362_2018,C50,1,0.05;\n")
    assert lines == [
        'engine.material.create(1, "C50", "CONC", "JTG3362_2018", "C50", 1, 0.05)'
    ], lines


# ── 回归：此前已对齐的命令 ────────────────────────────────────

def test_buckl_inc_substitute_uses_include():
    lines = _gen("BucklAnalInc,B1,s,LC2,1.2,0,LC1,1,0;\n")
    assert lines == [
        'engine.stability.get("B1").include("s", "LC2", 1.2, 0, "LC1", 1, 0)'
    ], lines


def test_ltm_inc_routes_op_to_include():
    lines = _gen("LTMAnalInc,M1,a,LC1,2.0,9.806,1,1,1,1,1,1;\n")
    assert lines == [
        'engine.dynamic.load_to_mass.get("M1").include('
        '"a", "LC1", 2.0, 9.806, 1, 1, 1, 1, 1, 1)'
    ], lines


def test_seis_rsp_import_num_before_spectrum():
    lines = _gen("SeisRspSpec,RS1,A,9.806,0,2,0.1,0.5,0.2,0.8;\n")
    assert lines == [
        'engine.dynamic.seismic.create("RS1", "A", 9.806, 0, 2, '
        "0.1, 0.5, 0.2, 0.8)"
    ], lines


def test_plane_load_flat_points():
    lines = _gen(
        "Load,Plane,LC1,PL1,SHELL,0,0,0,1,0,0,0,1,0,0.01,1,EG1,1,"
        "SurfaceN,NoProjection,0,X;\n"
    )
    assert lines == [
        'engine.load.get("LC1").create("Plane", "PL1", "SHELL", 0, 0, 0, '
        '1, 0, 0, 0, 1, 0, 0.01, 1, "EG1", 1, "SurfaceN", "NoProjection", 0, "X")'
    ], lines


def test_shaped_steel_catalog_fields():
    lines = _gen("Section,2,S2,SteelL,1,GB_YB,L20;\n")
    assert lines == [
        'engine.section.create(2, "S2", "SteelL", 1, "GB_YB", "L20")'
    ], lines


def test_pre_tendon_has_no_pipe_placeholder():
    lines = _gen("TdProp,P1,PRE,1,1,GBT5224,12.7,5,7.0,0.8,0.7;\n")
    assert lines == [
        'engine.tendon.prop.create("P1", "PRE", 1, 1, "GBT5224", '
        "12.7, 5, 7.0, 0.8, 0.7)"
    ], lines


# ── 编码 ──────────────────────────────────────────────────────

def test_read_utf8_out(tmp_path=None):
    """UTF-8 .out（实测 5.1 导出格式）不乱码"""
    from tempfile import mkdtemp
    p = Path(mkdtemp()) / "m.out"
    p.write_text("Mat,1,混凝土C五十,CONC;\n", encoding="utf-8")
    assert "混凝土C五十" in _read_out_text(p)


def test_read_gbk_out_falls_through():
    """GBK .out（旧版导出格式）按 UTF-8 解码失败后回落 GBK"""
    from tempfile import mkdtemp
    p = Path(mkdtemp()) / "m.out"
    p.write_text("Mat,1,混凝土C五十,CONC;\n", encoding="gbk")
    assert "混凝土C五十" in _read_out_text(p)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"{fn.__name__}: OK")
        except AssertionError as e:
            failed += 1
            print(f"{fn.__name__}: FAIL {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} 通过")
    sys.exit(1 if failed else 0)
