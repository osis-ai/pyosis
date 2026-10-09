"""transfer 转换器离线测试:旧 CrpShrk 的 fcuk 推断、关键字实参生成、编码顺序。

不依赖 OSIS 服务端:generate_lines 的 ctx 传 engine=None 时只做文本转换
(此时不生成关键字实参),签名内省用真实 OSISEngine 类(不连接)。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pyosis.core.engine import OSISEngine
from pyosis.transfer.generator import generate_lines
from pyosis.transfer.out_to_python import _read_out_text, _scan_creep_grades
from pyosis.transfer.parser import parse_text

ENGINE = OSISEngine.__new__(OSISEngine)  # 不走 __init__(避免动端口/URL)


def _gen(text: str, with_engine: bool = True):
    cmds = parse_text(text)
    ctx = {"engine": ENGINE if with_engine else None, "creep_grades": _scan_creep_grades(cmds)}
    return generate_lines(cmds, ctx)


# ── fcuk 推断 ──────────────────────────────────────────────────

def test_old8_single_grade_gets_fcuk():
    """旧 8 字段(rest) CrpShrk:唯一引用材料 C50 → fcuk=5e7"""
    lines = _gen(
        "CrpShrk,1,徐变,70,3,5,0,1,1;\n"
        "Material,1,C50,CONC,JTG3362_2018,C50,1,0.05;\n"
    )
    crp = next(l for l in lines if "creep_shrink.create" in l)
    assert "fcuk=50000000" in crp.replace(".0", ""), crp


def test_old6_single_grade():
    """旧 6 字段 CrpShrk:C40 → fcuk=4e7,补齐 Code/尺寸/粉煤灰"""
    lines = _gen(
        "CrpShrk,2,徐变40,60,5,5,3;\n"
        "Mat,9,C40,CONC,JTG3362_2018,C40,2;\n"
    )
    crp = next(l for l in lines if "creep_shrink.create" in l)
    assert "fcuk=40000000" in crp.replace(".0", ""), crp
    assert '"JTG3362_2018"' in crp and "fly_ash_ratio=0" in crp, crp


def test_mixed_grades_warns_and_keeps_default():
    """多等级共用一个特性:保持 50MPa 并输出告警注释"""
    lines = _gen(
        "CrpShrk,2,共用,60,5,5,3;\n"
        "Mat,1,C40,CONC,JTG3362_2018,C40,2;\n"
        "Mat,2,C55,CONC,JTG3362_2018,C55,2;\n"
    )
    crp = next(l for l in lines if "creep_shrink.create" in l)
    assert "fcuk=50000000" in crp.replace(".0", ""), crp
    warn = next(l for l in lines if l.startswith("# 注意:") and "CrpShrk 2" in l)
    assert "C40/C55" in warn, warn


def test_unreferenced_creep_warns():
    """无材料引用:保持默认并告警"""
    lines = _gen("CrpShrk,5,没人用,60,5,5,3;\n")
    assert any(l.startswith("# 注意:") and "未找到引用" in l for l in lines), lines


def test_new9_passthrough():
    """新 9 字段:原样透传(不加 Code/不推断 fcuk)"""
    lines = _gen("CrpShrk,3,新,JTG3362_2018,4.5e7,60,1,5,3,0;\n")
    crp = next(l for l in lines if "creep_shrink.create" in l)
    assert "fcuk=45000000.0" in crp, crp


# ── 关键字实参 ─────────────────────────────────────────────────

def test_long_signature_kwargs():
    """长签名(≥5 形参)生成关键字实参"""
    lines = _gen("CrpShrk,3,新,JTG3362_2018,4.5e7,60,1,5,3,0;\n")
    crp = next(l for l in lines if "creep_shrink.create" in l)
    assert "name=" in crp and "avg_humidity=" in crp, crp


def test_short_signature_positional():
    """短签名保持位置实参"""
    lines = _gen("Node,1,1.0,2.0,3.0;\n")
    assert lines == ["engine.node.create(1, 1.0, 2.0, 3.0)"], lines


def test_varargs_stays_positional():
    """*args 透传型(如 material.create)保持位置实参"""
    lines = _gen("Material,1,C50,CONC,JTG3362_2018,C50,1,0.05;\n")
    assert "code=" not in lines[0], lines


# ── 编码 ──────────────────────────────────────────────────────

def test_read_utf8_out(tmp_path=None):
    """UTF-8 .out(实测 5.1 导出格式)不乱码"""
    from tempfile import mkdtemp
    p = Path(mkdtemp()) / "m.out"
    p.write_text("Mat,1,混凝土C五十,CONC;\n", encoding="utf-8")
    assert "混凝土C五十" in _read_out_text(p)


def test_read_gbk_out_falls_through():
    """GBK .out(旧版导出格式)按 UTF-8 解码失败后回落 GBK"""
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
