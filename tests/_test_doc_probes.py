"""端到端核对:把《OSIS 命令帮助文档 v5.0》对齐后的争议点与新命令打到真引擎。

与 tests/_test_new_endpoints.py 同一套引导(osisSdk.dll + 随机端口)。
覆盖 memory osis-help-doc-sync-state 里的 4 个待核对项:
- LiveAnalInc 桥型拼写 AUX/BRIDGE_TYPE_CUSTOM vs 旧拼写 AUS/CUSTOM
- Element BEAM3D YTrans=4 是否合法
- ClearSectionRib 1 字段 vs 2 字段
- SeisRspSpecMod 按编号 vs 按名称
以及 v5.0 新增命令在引擎上的接受度:
CnvTol / SecPropMod / SectionPropFactor / StrengthPrg / PlanarLoad 家族 /
FP / ESRFC / UNISPT / LELNK / SOILSPRING / MSTSLV bCoincident / PST GroutAfter /
Material CONC StrengthPrg / HydroCoeff / SeastateOpt / SeastAnal / SeastAnalInc

工程建在 D:/pyosis_doc_probe/,只建模型不求解。
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
PROJ_PATH = str(PROJ_DIR / "probe.sis")

PASS: list[str] = []
FAIL: list[str] = []


def probe(label: str, cmd: str) -> bool:
    """发一条命令流,打印引擎原始应答"""
    ok, err = osis_run(cmd)
    tag = "OK " if ok else "ERR"
    line = f"  [{tag}] {label}: {cmd}"
    if not ok:
        line += f"  err={err}"
    print(line, flush=True)
    (PASS if ok else FAIL).append(label)
    return ok


def check(name: str, fn):
    try:
        out = fn()
        PASS.append(name)
        print(f"  [PASS] {name}" + (f" -> {out}" if out is not None else ""), flush=True)
    except Exception as e:
        FAIL.append(name)
        print(f"  [FAIL] {name}: {e}", flush=True)
        traceback.print_exc(limit=2)


print("== 1. 启动 solver ==", flush=True)
solver = OSISSolver(osis_install_path=OSIS_INSTALL, port=0)
engine = OSISEngine.from_solver(solver)
print(f"  port={solver.port}", flush=True)

print("\n== 2. 建工程 + 最小模型(悬臂梁) ==", flush=True)
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

print("\n== 3. 争议点核对 ==", flush=True)
probe("NL 新格式(仅 Geom)", "NL,1;")
probe("NL 旧格式(带 Link)", "NL,1,1;")
probe("CnvConfig(引擎名)", "CnvConfig,F,L2,0.0001;")
probe("CnvTol(文档名,应被拒)", "CnvTol,F,L2,0.0001;")
probe("BEAM3D YTrans=3(对照)", "Element,10,BEAM3D,1,2,1,1,1,3,1,0.0,0,0.0,0;")
probe("BEAM3D YTrans=4(文档只给1-3)", "Element,11,BEAM3D,1,2,1,1,1,4,1,0.0,0,0.0,0;")
probe("ClearSectionRib 1字段(文档语法行)", "ClearSectionRib,1;")
probe("ClearSectionRib 2字段(文档参数节/pyosis)", "ClearSectionRib,1,肋1;")
probe("SeisRspSpec 建谱", "SeisRspSpec,RS1,A,9.8,0,2,0.1,0.5,0.2,0.8;")
probe("SeisRspSpecMod 按名称", "SeisRspSpecMod,RS1,RS2;")
probe("SeisRspSpecMod 按编号", "SeisRspSpecMod,1,2;")

print("\n== 4. 活载桥型拼写 ==", flush=True)
probe("LiveGrade", "LiveGrade,G,JTGD60_2015,VEHICLE;")
probe("InflAlgo 车道", "InflAlgo,车道1,VE,4.0,1,0,主梁单元,0.5,0.0;")
probe("LiveAnal", "LiveAnal,活载1,JTGD60_2015,1;")
probe("LiveAnalInc CABLE_STAYED_AUX(文档)", "LiveAnalInc,活载1,a,子1,G,1.0,1,CABLE_STAYED_AUX,0.5,100,车道1;")
probe("LiveAnalInc CABLE_STAYED_AUS(旧)", "LiveAnalInc,活载1,a,子2,G,1.0,1,CABLE_STAYED_AUS,0.5,100,车道1;")
probe("LiveAnalInc BRIDGE_TYPE_CUSTOM(文档)", "LiveAnalInc,活载1,a,子3,G,1.0,1,BRIDGE_TYPE_CUSTOM,5.0,车道1;")
probe("LiveAnalInc CUSTOM(旧)", "LiveAnalInc,活载1,a,子4,G,1.0,1,CUSTOM,5.0,车道1;")

print("\n== 5. v5.0 新命令接受度 ==", flush=True)
probe("StrengthPrg ACI", "StrengthPrg,SP1,ACI,50000000,0.5,0.9;")
probe("Material CONC + StrengthPrg", "Mat,20,c20,CONC,JTG3362_2018,C50,,0.05,SP1;")
probe("SecPropMod", "SecPropMod,1,Part,1,0.5,0.1,0.1,1.0,2.0,3.0,4.0,0.0,0.0,0.0,0.0,5.0,4.0;")
probe("SectionPropFactor", "SectionPropFactor,1,1.0,1.0,1.0,1.0,1.0,1.0;")
probe("PlanarLoad Point", "PlanarLoad,PL1,说明,Point,0,0,100;")
probe("PlanarLoadCopy", "PlanarLoadCopy,PL1,X,2,0.5;")
probe("PlanarLoadDel", "PlanarLoadDel,PL1;")
probe("Load FP", "Load,FP,自重,1,1,X,0,1,2,3;")
probe("Load ESRFC(P4 缺省)", "Load,ESRFC,自重,1,1,X,0,1,2,3;")
probe("PST 带 GroutAfter", "Load,PST,自重,T1,BOTH,ST,100,100,2;")
probe("PST 不带 GroutAfter(对照)", "Load,PST,自重,T1,BEG,ST,100;")
probe("Bd UNISPT(T/X/ori)", "Bd,50,UNISPT,T,1000.0,X,1;")
probe("Bd UNISPT(ML/VECTOR)", "Bd,51,UNISPT,ML,1,VECTOR,0.0,0.0,1.0;")
probe("Bd LELNK", "Bd,52,LELNK,1,1e6,1,1e6,1,1e6,1,1e6,1,1e6,1,1e6,1,0,0,0,1,2;")
probe("Bd SOILSPRING 砂土", "Bd,53,SOILSPRING,,1,SAND,5.0,1.0,10.0,35.0;")
probe("Bd SOILSPRING 黏土(占位)", "Bd,54,SOILSPRING,,1,CLAY,5.0,1.0,10.0,,,50,0.01,0.5;")
probe("Bd MSTSLV 9字段(bCoincident 缺省)", "Bd,55,MSTSLV,2,1,1,1,1,1,1;")
probe("Bd MSTSLV 10字段(bCoincident=0)", "Bd,56,MSTSLV,2,1,1,1,1,1,1,0;")
probe("HydroCoeff", "HydroCoeff,H1,UD,1,0,1.0,1.2,1.2,1.0,1.0;")
probe("SeastateOpt", "SeastateOpt,50,0,1.025,Z;")
probe("SeastAnal", "SeastAnal,S1,H1;")
probe("SeastAnalInc WAVE", "SeastAnalInc,S1,a,WAVE,Airy,1.5,1,10.0,30.0;")
probe("SeastAnalInc WIND", "SeastAnalInc,S1,a,WIND,1,10.0,0,CONSTANT;")
probe("SeastAnalInc CURR", "SeastAnalInc,S1,s,CURR,1,-3.0,1,AUTO,5.0,CN,1,0.5,0.0,1.5,10.0;")

print("\n== 6. 保存(留档) ==", flush=True)
check("project.save", lambda: engine.project.save(PROJ_PATH))

print(f"\n==== 通过 {len(PASS)} / 失败 {len(FAIL)} ====")
print("失败项: " + (", ".join(FAIL) if FAIL else "无"))
