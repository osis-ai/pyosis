"""第二轮探针:在新编译的引擎上复核争议点与定长字段数。

修复第一轮探针自身的夹具缺陷:
- InflAlgo 改用 eRef=1(单元组+样条曲线)并先定义 Spline3D
- ClearSectionRib 先建 Rib 再两种字段数各试
- ESRFC/FP 先建壳单元(厚度+4节点+SHELL)
- UNISPT ML 先建 PUCurve
- PST 先建 TdProp+TdShape+LayoutTS
- SeastAnalInc 按引擎要求探索 WAVE/WIND/CURR 的定长字段
- CnvTol 的 Norm 枚举变体、SectionPropFactor 名称变体
- 桥型拼写 AUX/CUSTOM/AUS/BRIDGE_TYPE_CUSTOM 的最终裁定
"""
from __future__ import annotations

import shutil
import traceback
from pathlib import Path

from pyosis.core.command import osis_run
from pyosis.core.engine import OSISEngine
from pyosis.core.solver import OSISSolver

OSIS_INSTALL = "D:/OSIS 5/bin64"

WORK_DIR = Path("D:/pyosis_doc_probe")
if WORK_DIR.exists():
    shutil.rmtree(WORK_DIR)
PROJ_DIR = WORK_DIR / "proj"
PROJ_DIR.mkdir(parents=True)
PROJ_PATH = str(PROJ_DIR / "probe2.sis")

PASS: list[str] = []
FAIL: list[str] = []


def probe(label: str, cmd: str, quiet_ok: bool = False) -> bool:
    ok, err = osis_run(cmd)
    tag = "OK " if ok else "ERR"
    line = f"  [{tag}] {label}: {cmd}"
    if not ok:
        line += f"  err={err}"
    print(line, flush=True)
    (PASS if ok else FAIL).append(label)
    return ok


print("== 1. 启动 solver ==", flush=True)
solver = OSISSolver(osis_install_path=OSIS_INSTALL, port=0)
engine = OSISEngine.from_solver(solver)
print(f"  port={solver.port}", flush=True)

print("\n== 2. 基础模型 ==", flush=True)
engine.project.create(101, PROJ_PATH)
engine.control.set_gravity_acceleration(9.8066)
engine.material.create(1, "C50", "CONC", "JTG3362_2018", "C50")
engine.section.create(1, "矩形", "RECT")
engine.node.create(1, 0.0, 0.0, 0.0)
engine.node.create(2, 4.0, 0.0, 0.0)
engine.element.create_beam3d(1, 1, 2, mat=1, sec1=1, sec2=1)
engine.boundary.create(1, "GENERAL")
engine.boundary.get(1).assign("a", 1)
engine.element.group.create("主梁单元", "c")
engine.element.group.create("主梁单元", "a", 1)
engine.load.create("自重", "CS", 1.0)
engine.load.get("自重").create("GRAVITY", 0.0, 0.0, -1.04)
# 壳单元夹具:厚度 + 4 节点 + SHELL
probe("ShellThk", "ShellThk,1,1,0.2,0.2;")
probe("Node 3-4", "Node,3,4.0,0.0,3.0;")
probe("Node 4", "Node,4,0.0,0.0,3.0;")
probe("Element SHELL", "Element,20,SHELL,1,1,1,1,2,3,4;")
probe("Spline3D 线1", "Spline3D,线1,NATURAL,LIVE,0,0,0,1,0,0,2,0,0;")
probe("PUCurve 1", "PUCurve,1,pu1,0,2,0.0,0.0,1.0,100.0;")
probe("Rib Flat", "Rib,1,Flat,肋1,0.1,0.01;")

print("\n== 3. 争议点复核(新引擎) ==", flush=True)
probe("NL 旧格式(带 Link)", "NL,1,1;")
probe("CnvConfig F/L2", "CnvConfig,F,L2,0.0001;")
probe("CnvTol(文档名,应被拒)", "CnvTol,F,L2,0.0001;")
probe("CnvConfig F/2(应被拒)", "CnvConfig,F,2,0.0001;")
probe("SectionPropFactor", "SectionPropFactor,1,1.0,1.0,1.0,1.0,1.0,1.0;")
probe("SecPropFactor(备选名)", "SecPropFactor,1,1.0,1.0,1.0,1.0,1.0,1.0;")
probe("SeisRspSpec 建谱", "SeisRspSpec,RS1,A,9.8,0,2,0.1,0.5,0.2,0.8;")
probe("SeisRspSpecMod 按名称", "SeisRspSpecMod,RS1,RS2;")
probe("SeisRspSpecMod 按编号", "SeisRspSpecMod,1,2;")
probe("ClearSectionRib 1字段", "ClearSectionRib,1;")
probe("Rib Flat 再建(供2字段测试)", "Rib,1,Flat,肋2,0.1,0.01;")
probe("ClearSectionRib 2字段", "ClearSectionRib,1,肋2;")

print("\n== 4. 桥型拼写最终裁定 ==", flush=True)
probe("InflAlgo 车道(单元组+样条)", "InflAlgo,车道1,VE,4.0,1,1,主梁单元,线1;")
probe("LiveAnal", "LiveAnal,活载1,JTGD60_2015,1;")
probe("LiveAnalInc CABLE_STAYED_AUX", "LiveAnalInc,活载1,a,子1,G,1.0,1,CABLE_STAYED_AUX,0.5,100,车道1;")
probe("LiveAnalInc CABLE_STAYED_AUS", "LiveAnalInc,活载1,a,子2,G,1.0,1,CABLE_STAYED_AUS,0.5,100,车道1;")
probe("LiveAnalInc CUSTOM", "LiveAnalInc,活载1,a,子3,G,1.0,1,CUSTOM,5.0,车道1;")
probe("LiveAnalInc BRIDGE_TYPE_CUSTOM", "LiveAnalInc,活载1,a,子4,G,1.0,1,BRIDGE_TYPE_CUSTOM,5.0,车道1;")

print("\n== 5. 面荷载/流体压力(作用于壳) ==", flush=True)
probe("Load ESRFC on SHELL", "Load,ESRFC,自重,20,1,X,0,1,2,3;")
probe("Load FP on SHELL", "Load,FP,自重,20,1,X,0,1,2,3;")

print("\n== 6. UNISPT ML(需 PUCurve) ==", flush=True)
probe("Bd UNISPT ML/X", "Bd,51,UNISPT,ML,1,X,1;")
probe("Bd UNISPT ML/VECTOR", "Bd,52,UNISPT,ML,1,VECTOR,0.0,0.0,1.0;")

print("\n== 7. PST(先建钢束) ==", flush=True)
probe("TdProp", "TdProp,1,prop,EX,2,1,GBT5224_2014,10.8,7,0.21,0.22,0.042,0.5,0.3,0.3;")
probe("TdShape SPL3D", "TdShape,T1,1,1,主梁单元,SPL3D,线1;")
probe("LayoutTS GLOBAL", "LayoutTS,T1,GLOBAL;")
probe("PST 带 GroutAfter", "Load,PST,自重,T1,BOTH,ST,100,100,2;")
probe("PST 不带 GroutAfter", "Load,PST,自重,T1,BEG,ST,100;")

print("\n== 8. SeastAnalInc 定长字段探索 ==", flush=True)
probe("HydroCoeff", "HydroCoeff,H1,UD,1,0,1.0,1.2,1.2,1.0,1.0;")
probe("SeastAnal S2", "SeastAnal,S2,H1;")
probe("WAVE 17字段载荷(文档)", "SeastAnalInc,S2,a,WAVE,Airy,1.5,1,10.0,30.0,1.0,2,Degrees,0.0,0.1,10,MM,0,0,0,1,2;")
probe("WAVE 18字段载荷(多补一个)", "SeastAnalInc,S3,a,WAVE,Airy,1.5,1,10.0,30.0,1.0,2,Degrees,0.0,0.1,10,MM,0,0,0,1,2,0;")
probe("SeastAnal S4", "SeastAnal,S4,H1;")
probe("WIND 8字段载荷", "SeastAnalInc,S4,a,WIND,1,10.0,0,CONSTANT,0,0,0,0;")
probe("WIND 8字段载荷(SpecialParameter 空)", "SeastAnalInc,S5,a,WIND,1,10.0,0,CONSTANT,,0,0,0;")
probe("SeastAnal S6", "SeastAnal,S6,H1;")
probe("CURR a 11字段载荷", "SeastAnalInc,S6,a,CURR,1,-3.0,1,AUTO,5.0,CN,1,0.5,0.0,1.5,10.0;")

print("\n== 9. 保存(留档) ==", flush=True)
try:
    engine.project.save(PROJ_PATH)
    print("  [PASS] project.save", flush=True)
except Exception as e:
    print(f"  [FAIL] project.save: {e}", flush=True)

print(f"\n==== 通过 {len(PASS)} / 失败 {len(FAIL)} ====")
print("失败项: " + (", ".join(FAIL) if FAIL else "无"))
