"""端到端验证:直接加载 D:/OSIS 5/bin64 的 osisSdk.dll,测试 v0.7.6 新增封装。

覆盖:
- OSISSolver port=0 随机分配 + 实际端口回写(solver.py 修复)
- /sdk/version、/sdk/commands、GET /instance、/health(engine.sdk_version 等)
- 结果查询(engine.result.node_displacement / element_force / support_reaction /
  element_stress / tendon_loss / modal / envelope)及其列契约、strict 语义、
  表头对不上时的报错
- 老端点补齐(node.coordinates、material.all_prestressed、control.summary、
  section.all_longitudinal_rebar、tendon.prestress_loads)

工程建在 D:/pyosis_sync_test/。最小模型:悬臂梁 2 节点 1 单元,自重工况,1 施工阶段。
本模型没有钢束也没有模态分析,那两类的用例只验「空表不报错」;
钢束/模态的真实数值对照见 temp/_verify_routes_vs_output.py。
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

print("\n== 8. 结果 API 契约(统一走路由) ==", flush=True)

EXPECTED_COLS = {
    "node_displacement": {"loadCase", "source", "no", "ux", "uy", "uz",
                          "rx", "ry", "rz", "rw"},
    "element_force": {"loadCase", "source", "ele", "node", "fx", "fy", "fz",
                      "mx", "my", "mz", "mw"},
    "support_reaction": {"loadCase", "source", "no", "sys", "fx", "fy", "fz",
                         "mx", "my", "mz", "mw"},
    "element_stress": {"loadCase", "source", "ele", "node", "position", "point",
                       "sxFx", "sxMy", "sxMz", "sxComp", "syFy", "szFz", "tp", "cp"},
}


def _cols(name):
    df = getattr(engine.result, name)()
    missing = EXPECTED_COLS[name] - set(df.columns)
    assert not missing, f"{name} 缺列 {missing}，实际 {list(df.columns)}"
    return f"{len(df.columns)} 列齐全"


for _m in EXPECTED_COLS:
    check(f"result.{_m}() 列契约", lambda m=_m: _cols(m))


def _by_part():
    df = engine.result.element_stress("自重", by_part=True)
    assert "part" in df.columns, f"by_part=True 未带 part 列: {list(df.columns)}"
    return f"shape={df.shape}"


check("result.element_stress(by_part=True) 带 part 列", _by_part)

MISSING_NAME = "绝对不存在的工况"


def _strict():
    try:
        engine.result.node_displacement(MISSING_NAME, strict=True)
    except RuntimeError as e:
        assert MISSING_NAME in str(e), f"报错未点名: {e}"
        return "抛 RuntimeError 且点名"
    raise AssertionError("strict=True 未报错")


check("strict=True 查不到名字报错", _strict)


def _warn_empty():
    """名字写错与「包络名但服务端未支持」不可区分,都必须是空表 + 告警,不能静默"""
    import warnings as _w

    with _w.catch_warnings(record=True) as caught:
        _w.simplefilter("always")
        df = engine.result.node_displacement(MISSING_NAME)
    assert df.empty, f"不存在的工况竟然返回了 {len(df)} 行"
    assert any(issubclass(c.category, UserWarning) for c in caught), \
        f"空结果未告警: {[str(c.message) for c in caught]}"
    return f"空表 + {len(caught)} 条告警"


check("查不到名字默认空表 + 告警", _warn_empty)


def _semantic_silent():
    """有效名字下语义方法不该发任何告警"""
    import warnings as _w

    with _w.catch_warnings(record=True) as caught:
        _w.simplefilter("always")
        engine.result.node_displacement("自重")
    assert not caught, f"语义方法发出了告警: {[str(c.message) for c in caught]}"
    return "无告警"


check("语义方法在有效名字上不发告警", _semantic_silent)


def _no_legacy():
    """loadcase/env 已连同 /output 一起删除,不该还能调用"""
    for gone in ("loadcase", "env"):
        assert not hasattr(engine.result, gone), f"ResultManager 仍有 {gone}()"
    return "loadcase/env 已移除"


check("loadcase/env 已从 API 移除", _no_legacy)


# ── 新增结果类型:钢束损失、模态、包络 ──

def _empty_ok(method):
    """本模型没有钢束/模态分析:应为空表而不是报错"""
    df = getattr(engine.result, method)()
    assert df.empty, f"{method} 竟然有 {len(df)} 行"
    return "空表"


check("result.tendon_loss() 无钢束时为空表", lambda: _empty_ok("tendon_loss"))
check("result.modal() 无模态分析时为空表", lambda: _empty_ok("modal"))


ENV_COLS = {
    "displacement": {"loadCase", "source", "component", "no",
                     "ux", "uy", "uz", "rx", "ry", "rz", "rw"},
    "force": {"loadCase", "source", "component", "ele", "node",
              "fx", "fy", "fz", "mx", "my", "mz", "mw"},
    "stress": {"loadCase", "source", "component", "ele", "position", "point",
               "sxFx", "sxMy", "sxMz", "sxComp", "syFy", "szFz", "tp", "cp"},
    "reaction": {"loadCase", "source", "extreme", "component", "no", "sys",
                 "fx", "fy", "fz", "mx", "my", "mz", "mw"},
}


def _env_cols(kind):
    df = engine.result.envelope(kind=kind)
    missing = ENV_COLS[kind] - set(df.columns)
    assert not missing, f"包络 {kind} 缺列 {missing}，实际 {list(df.columns)}"
    return f"{len(df)} 行, {len(df.columns)} 列"


for _k in ENV_COLS:
    check(f"result.envelope(kind={_k!r}) 列契约", lambda k=_k: _env_cols(k))


def _env_bad_kind():
    try:
        engine.result.envelope(kind="应变")
    except ValueError as e:
        return f"抛 ValueError: {str(e)[:40]}"
    raise AssertionError("未知 kind 未报错")


check("result.envelope(kind=不存在的类型) 报错", _env_bad_kind)


# ── 表头对不上时必须报错,不能静默给少列的表 ──

def _bad_header_raises():
    """求解器改了表头时的兜底:必需列缺失要报错并打出实际表头"""
    from pyosis.result import routes

    saved = routes._COLUMNS["element_force"]
    try:
        # 抹掉一个必需列的表头映射,模拟「求解器把 Fz 改了名」
        routes._COLUMNS["element_force"] = {
            k: v for k, v in saved.items() if v != "fz"
        }
        try:
            engine.result.element_force("自重")
        except RuntimeError as e:
            assert "fz" in str(e), f"报错未点名缺哪个键: {e}"
            assert "表头" in str(e), f"报错未打出实际表头: {e}"
            return f"抛 RuntimeError 且点名: {str(e)[:60]}"
        raise AssertionError("必需列缺失竟然没报错")
    finally:
        routes._COLUMNS["element_force"] = saved


check("表头改了导致缺列时抛 RuntimeError", _bad_header_raises)


def _unknown_header_warns():
    """多出来的、认不出的列只告警不报错(求解器加了列不该让旧代码挂掉)"""
    from pyosis.result import routes

    cols = [{"name": n} for n in
            ("节点", "Ux", "Uy", "Uz", "Rx", "Ry", "Rz", "Rw", "外星列")]
    import warnings as _w

    with _w.catch_warnings(record=True) as caught:
        _w.simplefilter("always")
        keys = routes._translate(cols, "node_displacement")
    assert keys[-1] is None, f"认不出的列应映射成 None,实际 {keys[-1]!r}"
    assert keys[:8] == ["no", "ux", "uy", "uz", "rx", "ry", "rz", "rw"], f"已认得的列映射错了: {keys[:8]}"
    assert any("外星列" in str(c.message) for c in caught), \
        f"未告警未映射的列: {[str(c.message) for c in caught]}"
    return "认不出的列映射为 None + 告警点名"


check("认不出的列告警但不报错", _unknown_header_warns)

print(f"\n===== 结果: {len(PASS)} PASS / {len(FAIL)} FAIL =====")
for name, err in FAIL:
    print(f"  FAIL: {name}: {err[:120]}")
print("ALL OK" if not FAIL else "HAS FAILURES")
sys.exit(1 if FAIL else 0)
