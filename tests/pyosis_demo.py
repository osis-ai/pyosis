"""pyosis 端到端示例:复用 case 的 prep 模块建模 -> 求解 -> 导出结果。

整个 demo 复用 tests/output/output_py/25m简支小箱梁中梁-solveronly/ 这个
case(已验证能完整跑通:10 个 prep 模块 + solve),demo 只做三件事:
  1) 通过 case 的 _0_engine.py 启动 solver + 建工程
  2) 调用 case 的 main() 跑建模 + save
  3) 从 Result/ 下已生成的 .lcr/.env 文件导出 CSV 结果

用法:
    1) 安装 pyosis: pip install osis-python
    2) 准备 OSIS 求解器安装目录(如 D:\\OSIS_Solver\\Rbin64,带 PySolver.dll)
    3) python pyosis_demo.py

运行结束后在 ./demo_output/ 下生成:
    - proj/test.sis           工程文件
    - proj/test/Result/       求解器生成的结果文件
    - results/<工况>_<类型>.csv  导出成 CSV 的各工况结果
    - summary.json             各工况导出结果汇总
"""
from __future__ import annotations

import os
import sys
import json
import shutil
from pathlib import Path

# 让本地 pyosis(src/)优先于 site-packages(开发时用)。
# 同事正式安装后这行可删,pip 装的 osis-python 会自然生效。
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

# 清掉系统代理(走本机回环,避免被外网 tinyproxy 劫走)
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)

# 求解器 JSON 是 UTF-8,stdout 也用 UTF-8 避免中文乱码
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# 把 case 目录加进 sys.path,导入它的模块(case 自带 _0_engine.py 启动 solver + 建工程)
CASE_DIR = str(Path(__file__).resolve().parent / "output" / "output_py" / "25m简支小箱梁中梁-solveronly")
if not os.path.isdir(CASE_DIR):
    raise FileNotFoundError(
        f"找不到 case 目录 {CASE_DIR}。"
        f"请确认 demo_output 旁边有 output_py/25m简支小箱梁中梁-solveronly/ 这个 case。"
    )
sys.path.insert(0, CASE_DIR)

# ===== 1. case 的 _0_engine.py 已经做了:启动 OSISSolver + 建工程 =====
import _0_engine as _case_engine   # 启动 solver、建工程,导出 engine 单例
import main as case_main            # case 入口:clear + 10 个 prep 模块 + save

case_engine = _case_engine.engine

# ===== 2. 跑建模 =====
print("\n== 调用 case.main() 跑建模 ==", flush=True)
case_main.main()


# ===== 3. 求解 =====
print("\n== solve ==", flush=True)
case_engine.solve()
print("== solve done ==", flush=True)


# ===== 4. 导出结果 =====
PROJ_DIR = Path(CASE_DIR) / "proj"
result_dir = PROJ_DIR / "test" / "Result"
out_dir = Path(__file__).resolve().parent / "demo_output" / "results"
out_dir.mkdir(parents=True, exist_ok=True)

if not result_dir.is_dir():
    print(f"\n(无 {result_dir},无结果可导出)", flush=True)
else:
    print(f"\n== 导出 Result/ 下结果到 {out_dir} ==", flush=True)
    results_summary = {}
    for fname in sorted(result_dir.iterdir()):
        base = fname.stem            # 去掉 .lcr/.env 后缀作为 loadcase 名
        ext = fname.suffix.lower()
        if ext == ".lcr":
            results_summary[base] = {}
            for rt in ("LCND", "LCEF"):
                try:
                    df = case_engine.result.loadcase(base, rt)
                    csv = out_dir / f"{base}_{rt}.csv"
                    df.to_csv(csv, index=False, encoding="utf-8-sig")
                    results_summary[base][rt] = {
                        "shape": list(df.shape),
                        "columns": list(df.columns),
                        "csv": str(csv),
                    }
                    print(f"  {base}/{rt}: shape={df.shape}, -> {csv.name}", flush=True)
                except Exception as e:
                    print(f"  {base}/{rt}: <err: {str(e)[:80]}>", flush=True)
                    results_summary[base][rt] = {"error": str(e)}
        elif ext == ".env":
            results_summary[base] = {}
            for rt in ("EnvND", "EnvEF"):
                try:
                    df = case_engine.result.env(base, rt)
                    csv = out_dir / f"{base}_{rt}.csv"
                    df.to_csv(csv, index=False, encoding="utf-8-sig")
                    results_summary[base][rt] = {
                        "shape": list(df.shape),
                        "columns": list(df.columns),
                        "csv": str(csv),
                    }
                    print(f"  {base}/{rt}: shape={df.shape}, -> {csv.name}", flush=True)
                except Exception as e:
                    print(f"  {base}/{rt}: <err: {str(e)[:80]}>", flush=True)
                    results_summary[base][rt] = {"error": str(e)}

    summary_path = out_dir.parent / "summary.json"
    summary_path.write_text(
        json.dumps(results_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n== summary.json -> {summary_path} ==", flush=True)

print(f"\n== 工程 {PROJ_DIR / 'test.sis'} ==", flush=True)
print(f"== 结果 {out_dir} ==", flush=True)
print("ALL OK", flush=True)