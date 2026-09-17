"""对比两种执行方式的耗时（需 OSIS 已打开）：
  A) osis_run 整份 .out 原文一次性发送（.out 自带 clear;clc; 头）
  B) 生成的 prep/main.py（batch：clear+clc 后全部命令一次冲刷）
"""
import sys, os, re, io, time, runpy, contextlib

sys.path.insert(0, r"D:\OSIS 5\pyosis\src")
from pyosis.core.command import osis_run

OUT = r"D:\OSIS 5\pyosis\tests\output\xiaoxiangliang.out"
PROJ = r"D:\OSIS 5\pyosis\tests\output\output_py\xiaoxiangliang\prep"


def run_raw() -> float:
    raw = open(OUT, encoding="utf-8").read()
    # OSIS_Run 不剥离 // 注释行（注释会吞掉下一条命令），客户端先剥掉
    raw = "".join(
        l for l in raw.splitlines(keepends=True)
        if not l.lstrip().startswith("//")
    )
    t0 = time.perf_counter()
    ok, err = osis_run(raw, timeout=600)
    dt = time.perf_counter() - t0
    print(f"A) osis_run 整文件: {dt:7.3f}s   ok={ok}  {err[:120]}")
    return dt


def run_batch() -> float:
    for k in [k for k in sys.modules if re.match(r"_\d", k)]:
        del sys.modules[k]
    if PROJ not in sys.path:
        sys.path.insert(0, PROJ)
    mod = runpy.run_path(os.path.join(PROJ, "main.py"))
    t0 = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        mod["build_model"]()
    dt = time.perf_counter() - t0
    print(f"B) batch  main.py : {dt:7.3f}s")
    return dt


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ta = tb = 0.0
    for i in range(n):
        ta += run_raw()
        tb += run_batch()
    if n > 1:
        print(f"\n平均({n} 次): A={ta/n:.3f}s  B={tb/n:.3f}s")
