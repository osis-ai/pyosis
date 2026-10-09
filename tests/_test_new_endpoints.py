"""端到端验证:直接加载 D:/OSIS 5/bin64 的 PySolver.dll,测试 v0.7.6 新增封装。

覆盖:
- OSISSolver port=0 随机分配 + 实际端口回写(solver.py 修复)
- /sdk/version、/sdk/commands、GET /instance、/health(engine.sdk_version 等)
- 无头结果查询 6 端点(engine.result.node_displacement / element_force / support_reaction)
- 老端点补齐(node.coordinates、material.all_prestressed、control.summary、
  section.all_longitudinal_rebar、tendon.prestress_loads)

工程建在 D:/pyosis_sync_test/。最小模型:悬臂梁 2 节点 1 单元,自重工况,1 施工阶段。
"""
from __future__ import annotations

import shutil
import sys
import traceback
from pathlib import Path

from pyosis.core.engine import OSISEngine
from pyosis.core.solver import OSISSolver

OSIS_INSTALL = "D:/OSIS 5/bin64"

WORK_DIR = Path("D:/pyosis_sync_test")
if WORK_DIR.exists():
    shutil.rmtree(WORK_DIR)
PROJ_DIR = WORK_DIR / "proj"
PROJ_DIR.mkdir(parents=True)
PROJ_PATH = str(PROJ_DIR / "test.sis")

PASS: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    """跑一个用例,打印结果,失败不中断"""
    try:
        out = fn()
        PASS.append(name)
        print(f"  [PASS] {name}" + (f" -> {out}" if out is not None else ""), flush=True)
    except Exception as e:
        FAIL.append((name, str(e)))
        print(f"  [FAIL] {name}: {e}", flush=True)
        traceback.print_exc(limit=2)


print("== 1. 启动 solver (port=0 随机分配) ==", flush=True)
solver = OSISSolver(osis_install_path=OSIS_INSTALL, port=0)
check("solver.port 随机分配回写(>0 且 != 0)", lambda: f"port={solver.port}, url={solver.url}"
      if solver.port > 0 else (_ for _ in ()).throw(RuntimeError(f"port={solver.port}")))

engine = OSISEngine.from_solver(solver)

print("\n== 2. /sdk 与 /instance 新端点 ==", flush=True)
check("engine.is_alive() (/health)", lambda: engine.is_alive())
check("engine.sdk_version() (/sdk/version)", lambda: engine.sdk_version())
check("engine.instance_info() (GET /instance)", lambda: engine.instance_info())
check("engine.list_commands() 建工程前 (/sdk/commands)", lambda: engine.list_commands())

print("\n== 3. 建工程 D:/pyosis_sync_test/proj/test.sis ==", flush=True)
engine.project.create(101, PROJ_PATH)
check("project.create + get_directory", lambda: engine.project.get_directory())
check("engine.list_commands() 建工程后", lambda: engine.list_commands())

print("\n== 4. 最小模型:悬臂梁 ==", flush=True)
engine.control.set_gravity_acceleration(9.8066)
engine.material.create(1, "C50", "CONC", "JTG3362_2018", "C50")
engine.material.create(3, "钢绞线-1860", "PRESTRESSED", "JTG3362_2018", "Strand1860", 0.05)
engine.section.create(1, "矩形", "RECT")
engine.node.create(1, 0.0, 0.0, 0.0)
engine.node.create(2, 4.0, 0.0, 0.0)
engine.element.create_beam3d(1, 1, 2, mat=1, sec1=1, sec2=1)
engine.boundary.create(1, "GENERAL")
engine.boundary.get(1).assign("a", 1)
engine.element.group.create("主梁单元", "c")
engine.element.group.create("主梁单元", "a", 1)
engine.boundary.group.create("支座", "c")
engine.boundary.group.create("支座", "a", 1)
engine.load.create("自重", "CS", 1.0)
engine.load.get("自重").create("GRAVITY", 0.0, 0.0, -1.04)
engine.stage.create(1, "CS1_悬臂梁", 7.0)
s1 = engine.stage.get(1)
s1.define_element(1, 1, "主梁单元", 7.0, 0)
s1.define_boundary(1, 1, "支座")
s1.define_loadcase(1, 1, "", "自重")

print("\n== 5. 老端点补齐封装 ==", flush=True)
check("node.coordinates() (/GetCoordinate)", lambda: engine.node.coordinates())
check("material.all_prestressed()", lambda: [m.name for m in engine.material.all_prestressed()])
check("control.summary() (/GetAnalysisControlSummary)", lambda: engine.control.summary())
check("section.all_longitudinal_rebar()", lambda: len(engine.section.all_longitudinal_rebar()))
check("tendon.prestress_loads()", lambda: len(engine.tendon.prestress_loads()))

print("\n== 6. 保存 + 求解 ==", flush=True)
engine.project.save(PROJ_PATH)
engine.solve()
print("  solve done", flush=True)

print("\n== 7. 无头结果查询(新端点) ==", flush=True)
check("result.node_displacement() 全部", lambda: len(engine.result.node_displacement()))
check("result.element_force() 全部", lambda: len(engine.result.element_force()))
check("result.support_reaction() 全部", lambda: len(engine.result.support_reaction()))


def _by_name():
    df = engine.result.node_displacement("自重")
    assert not df.empty, "按名查询为空"
    row = df.iloc[0]
    return f"loadCase={row['loadCase']}, source={row['source']}, node{int(row['no'])} uz={row['uz']:.6g}"


def _df():
    df = engine.result.support_reaction()
    assert len(df) > 0, "DataFrame 为空"
    return f"shape={df.shape}, cols={list(df.columns)}"


check("result.node_displacement('自重') 按名", _by_name)
check("result.support_reaction() DataFrame", _df)


def _physics():
    """支座竖向反力 ≈ 自重合计(γ=9.8066 仅 z 向 -1.04 系数,粗校验非零即可)"""
    df = engine.result.support_reaction()
    fz = df.iloc[0]["fz"]
    assert abs(fz) > 1e-9, f"支座反力 fz={fz},应为非零"
    return f"fz={fz:.6g}"


check("支座反力非零(物理合理性)", _physics)

print(f"\n===== 结果: {len(PASS)} PASS / {len(FAIL)} FAIL =====")
for name, err in FAIL:
    print(f"  FAIL: {name}: {err[:120]}")
print("ALL OK" if not FAIL else "HAS FAILURES")
sys.exit(1 if FAIL else 0)
