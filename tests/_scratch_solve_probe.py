"""scratch: 直接调 OSISSolver/OSISEngine(python→solver,不经 UI) 完整建模 + 求解 + summary 示例。

用法:
    python tests/_scratch_solve_probe.py

流程:
    1) OSISSolver 用 ctypes 加载 Rbin64/PySolver.dll 并起 HTTP server(18080)
    2) OSISEngine 接上 solver, /create 建工程
    3) 依次执行 _1_control.._10_stage 十个 prep 模块(走 manager API,不 engine.run)
    4) engine.solve() 求解
    5) 打印求解前后 summary + 结果抽查

注意事项:
    - 依赖 25m简支小箱梁中梁-solveronly 那套 output 里的 prep 模块
    - CWD 不在 Rbin64 也能跑(SetProjectExeDir 已修正材料库路径)
"""
import os
import sys

sys.path.insert(0, r"d:\OSIS 5\pyosis\src")
for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(k, None)

# 求解器 JSON 是 UTF-8,控制台也统一成 UTF-8,免得 GBK stdout 出乱码
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

CASE_DIR = r"D:\OSIS 5\pyosis\tests\output\output_py\25m简支小箱梁中梁-solveronly"
sys.path.insert(0, CASE_DIR)

import main as case_main
from _0_engine import engine

print("== build ==", flush=True)
case_main.main()
print("== build done ==", flush=True)


def _count(mgr, label):
    all_fn = getattr(mgr, "all", None)
    if not callable(all_fn):
        return f"{label}: <no .all()>"
    try:
        items = all_fn()
        return f"{label}: {len(items)}"
    except Exception as e:
        return f"{label}: <error: {e}>"


print("\n== summary (求解前) ==", flush=True)
for label, mgr in [
    ("material ", engine.material),
    ("section  ", engine.section),
    ("node     ", engine.node),
    ("element  ", engine.element),
    ("boundary ", engine.boundary),
    ("loadcase ", engine.load),
    ("stage    ", engine.stage),
]:
    print("  " + _count(mgr, label), flush=True)

print("\n== solve ==", flush=True)
engine.solve()
print("== solve done ==", flush=True)

# 求解后再看关键结果:节点/单元抽查
print("\n== 结果抽查 ==", flush=True)
for desc, fn in [
    ("node.all 前3", lambda: engine.node.all()[:3]),
    ("element.all 前3", lambda: engine.element.all()[:3]),
]:
    try:
        print(f"  {desc}: {fn()}", flush=True)
    except Exception as e:
        print(f"  {desc}: <error: {e}>", flush=True)

print("\nALL OK", flush=True)
