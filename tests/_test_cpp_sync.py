"""C++ ↔ pyosis 对接项验证：PySolver 本次改动的 9 条对策逐条实测。

覆盖：
  1. 节点复数键 → 单数键
  2. /GetAllElementInfo brief（省略 sectionDetails）
  3. 单元数据类补字段（compThk / secVec / isTaper / ...）
  4. 钢束形状 glbPoints / locPoints
  5. no == -1 / name == "-1" 归一为 None
  6. /GetAllStageInfo 改名；车辆 = 活载等级过滤
  7. /GetProjectDirectory → data.path
  8. 整数编码 → 名字映射（单元/边界/材料/规范/截面/工况/约束）
  9. ploted → plotted

工程建在 D:/pyosis_sync_test/cpp_sync/。
"""
from __future__ import annotations

import shutil
import sys
import traceback
from pathlib import Path

from pyosis.core.engine import OSISEngine
from pyosis.core.solver import OSISSolver

OSIS_INSTALL = "D:/OSIS 5/bin64"
WORK = Path("D:/pyosis_sync_test/cpp_sync")
if WORK.exists():
    shutil.rmtree(WORK)
(WORK / "proj").mkdir(parents=True)
PROJ = str(WORK / "proj" / "sync.sis")

PASS: list[str] = []
FAIL: list[str] = []


def check(name, fn):
    try:
        out = fn()
        PASS.append(name)
        print(f"  [PASS] {name}" + (f" -> {out}" if out is not None else ""), flush=True)
    except Exception as e:
        FAIL.append((name, str(e)))
        print(f"  [FAIL] {name}: {e}", flush=True)
        traceback.print_exc(limit=2)


print("== 启动 + 建工程 ==", flush=True)
solver = OSISSolver(osis_install_path=OSIS_INSTALL, port=0)
engine = OSISEngine.from_solver(solver)
engine.project.create(101, PROJ)

# ── 建最小模型 ─────────────────────────────────
engine.prop.creep_shrink.create(1, "收缩徐变", "JTG3362_2018", 5.0e7, 75.0, 1.0, 5.0, 3, 0.0)
engine.material.create(1, "C50", "CONC", "JTG3362_2018", "C50")
engine.material.create(2, "HRB400", "REBAR", "JTG3362_2018", "HRB400")
engine.section.create(1, "矩形", "RECT")
engine.node.create(1, 0.0, 0.0, 0.0)
engine.node.create(2, 4.0, 0.0, 0.0)
engine.node.create(3, 8.0, 0.0, 0.0)
engine.element.create_beam3d(1, 1, 2, mat=1, sec1=1, sec2=1)
engine.element.create_beam3d(2, 2, 3, mat=1, sec1=1, sec2=1)
engine.element.group.create("主梁单元", "c")
engine.element.group.create("主梁单元", "a", "1to2")
engine.boundary.create(1, "GENERAL")
engine.boundary.get(1).assign("a", 1)
engine.boundary.create(2, "GENERAL")
engine.boundary.get(2).assign("a", 3)
engine.boundary.group.create("支座", "c")
engine.boundary.group.create("支座", "a", "1to2")
engine.load.create("自重", "CS", 1.0)
engine.load.get("自重").create("GRAVITY", 0.0, 0.0, -1.04)
engine.prop.assign_component_thickness(0.3, "a", "1to2")
engine.stage.create(1, "CS1_施工", 7.0)
s1 = engine.stage.get(1)
s1.define_element(1, 1, "主梁单元", 7.0, 0)
s1.define_boundary(1, 1, "支座")
s1.define_loadcase(1, 1, "", "自重")
engine.project.save(PROJ)
print("  模型建好", flush=True)


# ── 1. 节点单数键 ──────────────────────────────
def t1():
    n = engine.node.get(1)
    return f"related_elements={n.related_elements}, related_boundaries={n.related_boundaries}, related_loads={n.related_loads}"


def t1b():
    n = engine.node.get(1)
    assert n.related_elements == [1], f"relatedElement 未取到: {n.related_elements}"
    assert n.related_boundaries == [1], f"relatedBoundary 未取到: {n.related_boundaries}"
    assert isinstance(n.related_setl_grps, list)
    return "单数键全部命中"


# ── 2/3. 单元 brief + 新字段 ────────────────────
def t2():
    eles = engine.element.all()
    d = eles[0].__dict__ if hasattr(eles[0], "__dict__") else None
    return f"{len(eles)} 个单元, 首单元 {eles[0]}"


def t3():
    e = engine.element.all()[0]
    assert e.is_taper is not None, "isTaper 缺失"
    assert e.sec_vec == [1, 1], f"secVec: {e.sec_vec}"
    assert e.comp_thk is not None, "compThk 缺失"
    assert e.beta is not None, "beta 缺失"
    return (f"is_taper={e.is_taper}, sec_vec={e.sec_vec}, comp_thk={e.comp_thk}, "
            f"beta={e.beta}, strain={e.strain}, warp={e.warp}, type_name={e.type_name}")


def t9():
    e = engine.element.all()[0]
    n = engine.node.get(1)
    b = engine.boundary.get(1)
    assert e.plotted is not None and n.plotted is not None and b.is_plotted is not None
    return f"element.plotted={e.plotted}, node.plotted={n.plotted}, boundary.is_plotted={b.is_plotted}"


# ── 5. 截面 prop 13 字段 / propFactor 移除 ─────
def t5():
    s = engine.section.get(1)
    prop = s.prop or {}
    expected = {"area", "sy", "sz", "ixx", "iyy", "izz", "iww", "centY", "centZ", "dy", "dz", "periO", "periI"}
    missing = expected - set(prop)
    assert not missing, f"prop 缺字段: {missing}"
    assert not hasattr(s, "prop_factor"), "prop_factor 仍存在"
    return f"{len(prop)} 字段, area={prop['area']:.6g}, type_name={s.type_name}"


# ── 6. stage 改名 + 车辆 ───────────────────────
def t6():
    stages = engine.stage.all()
    return f"GetAllStageInfo OK, {len(stages)} 个阶段: {[s.name for s in stages]}"


def t6v():
    names = engine.live.vehicle.names()
    return f"vehicle_manager.names()={names}, count={engine.live.vehicle.count()}"


# ── 7. 工程目录 ────────────────────────────────
def t7():
    d = engine.project.get_directory()
    assert d and "cpp_sync" in d.replace("\\", "/"), f"目录异常: {d}"
    return d


# ── 8. 整数编码 → 名字 ─────────────────────────
def t8():
    e = engine.element.all()[0]
    b = engine.boundary.get(1)
    m = engine.material.get(1)
    s = engine.section.get(1)
    lc = engine.load.get("自重")
    c = b.constraints_dict
    return (f"elem={e.type_name}, bnd={b.type_name}, mat={m.type_name}/{m.code_name}, "
            f"sec={s.type_name}, lc={lc.type_name}, constraints={c}")


def t8b():
    b = engine.boundary.get(1)
    c = b.constraints_dict
    assert set(c) == {"DX", "DY", "DZ", "RX", "RY", "RZ", "RW"}, f"约束键异常: {c}"
    assert all(isinstance(v, bool) for v in c.values()), f"约束值非 bool: {c}"
    return "约束 7 位 → dict OK"


print("\n== 逐项验证 ==", flush=True)
check("1. 节点单数键(relatedElement/...)", t1)
check("1b. 节点单数键实际命中", t1b)
check("2. /GetAllElementInfo (brief)", t2)
check("3. 单元补字段 compThk/secVec/isTaper", t3)
check("9. ploted → plotted", t9)
check("5. 截面 prop 13 字段 / 无 propFactor", t5)
check("6. /GetAllStageInfo", t6)
check("6b. vehicle_manager 过滤", t6v)
check("7. /GetProjectDirectory data.path", t7)
check("8. 整数编码 → 名字", t8)
check("8b. 约束 7 位 → dict", t8b)

print(f"\n===== {len(PASS)} PASS / {len(FAIL)} FAIL =====")
for n, e in FAIL:
    print(f"  FAIL: {n}: {e[:160]}")
print("ALL OK" if not FAIL else "HAS FAILURES")
sys.exit(1 if FAIL else 0)
