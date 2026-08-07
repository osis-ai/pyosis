"""pyosis 端到端示例:启动 solver -> 建工程 -> 建模 -> 求解 -> 导出结果。

整个 demo 自包含:10 个 prep 模块(control/property/material/section/node/element/
boundary/loadcase/analysis/stage)的代码全部内嵌在一个文件里,无需附带任何
外部模块。

用法:
    1) 安装 pyosis: pip install osis-python
    2) 准备 OSIS 求解器安装目录(如 D:\\OSIS_Solver\\Rbin64,带 PySolver.dll)
    3) python pyosis_demo.py

运行结束后在 ./demo_output/ 下生成:
    - proj/test.sis           工程文件
    - proj/test/Result/       求解器生成的二进制 .lcr/.env
    - proj/test/Temperary/    求解器生成的 .txt + 导出的 UTF-8-BOM CSV
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from pyosis.core.engine import OSISEngine
from pyosis.core.solver import OSISSolver

# ===== 1. 启动 solver + 建工程 =====
# OSIS 安装目录(含 PySolver.dll)。正反斜杠都行,Windows LoadLibrary 都接受。
OSIS_INSTALL = "D:/OSIS_Solver/Rbin64"

WORK_DIR = Path("./demo_output")
if WORK_DIR.exists():
    shutil.rmtree(WORK_DIR)
WORK_DIR.mkdir(parents=True, exist_ok=True)

PROJ_DIR = WORK_DIR / "proj"
PROJ_DIR.mkdir(parents=True, exist_ok=True)
PROJ_PATH = str(PROJ_DIR / "test.sis")

print("== 启动 solver ==", flush=True)
solver = OSISSolver(osis_install_path=OSIS_INSTALL)

print("== 建工程 type=101 桥梁分析 ==", flush=True)
engine = OSISEngine.from_solver(solver)
engine.project.create(101, PROJ_PATH)


# ===== 2. CONTROL 全局控制参数 =====
def setup_control(engine: OSISEngine) -> None:
    engine.control.set_gravity_acceleration(9.8066)
    engine.control.set_calc_tendon(1)
    engine.control.set_calc_concurrent_force(1)
    engine.control.set_calc_shrink(1)
    engine.control.set_calc_creep(1)
    engine.control.set_calc_shear(1)
    engine.control.set_calc_relaxation(1)
    engine.control.set_mod_loc_coor(0)
    engine.control.set_inc_tendon(1)
    engine.control.set_nonlinear(0, 0)
    engine.control.set_line_search(0)
    engine.control.set_auto_time_step(0)
    engine.control.set_substitution_steps(1, 20)
    engine.dynamic.modal.set_modal_opt(0)


# ===== 3. PROPERTY 几何属性 =====
def build_property(engine: OSISEngine) -> None:
    engine.geometry.create("钢束-1-N1", "ARC3D", "TENDON", 0.16, 0.0, -0.25, 0.0, 8.50394, 0.0, -0.98, 30.0, 16.4161, 0.0, -0.98, 30.0, 24.76, 0.0, -0.25, 0.0)
    engine.geometry.create("钢束-2-N2", "ARC3D", "TENDON", 0.16, 0.0, -0.5, 0.0, 6.90373, 0.0, -1.09, 30.0, 18.0163, 0.0, -1.09, 30.0, 24.76, 0.0, -0.5, 0.0)
    engine.geometry.create("钢束-3-N3", "ARC3D", "TENDON", 0.16, 0.0, -0.75, 0.0, 5.30352, 0.0, -1.2, 30.0, 19.6165, 0.0, -1.2, 30.0, 24.76, 0.0, -0.75, 0.0)
    engine.geometry.create("钢束-4-N4", "ARC3D", "TENDON", 0.16, 0.0, -1.0, 0.0, 3.70332, 0.0, -1.31, 30.0, 21.2167, 0.0, -1.31, 30.0, 24.76, 0.0, -1.0, 0.0)
    engine.geometry.create("钢束-5-N5", "ARC3D", "TENDON", 0.16, 0.0, -1.245, 0.0, 2.02136, 0.0, -1.31, 30.0, 22.8986, 0.0, -1.31, 30.0, 24.76, 0.0, -1.245, 0.0)


# ===== 4. MATERIAL 材料 =====
def build_materials(engine: OSISEngine) -> None:
    engine.prop.creep_shrink.create(1, "收缩徐变", 75.0, 7, 5.0, 3)
    engine.material.create(1, "C50", "CONC", "JTG3362_2018", "C50", 1, 0.05)
    engine.material.create(2, "HRB400", "REBAR", "JTG3362_2018", "HRB400", 0.05)
    engine.material.create(3, "钢绞线-1860", "PRESTRESSED", "JTG3362_2018", "Strand1860", 0.05)


# ===== 5. SECTION 截面 =====
def build_sections(engine: OSISEngine) -> None:
    for no, name in [(1, "标准截面"), (2, "墩顶截面"), (3, "加厚截面"),
                     (4, "墩顶截面"), (5, "加厚截面")]:
        engine.section.create(no, name, "SMALLBOX", "Middle", 1.4, 1.65, 1.2, 0.0, 1.0, 0.18, 0.2, 0.2, 3.5, 0.18, 0.25, 0.2, 0.15, 0.25, 0.05, 0.05, 0, 0.0, 0.0, 0.05)
        engine.section.get(no).set_offset("Middle", 0.0, "Top", 0.0)
        engine.section.get(no).set_mesh(0, 0.1)


# ===== 6. NODE 节点 =====
def build_nodes(engine: OSISEngine) -> None:
    coords = [(1, 0.04, 0.0, 0.0), (2, 0.5, 0.0, 0.0), (3, 0.84, 0.0, 0.0),
              (4, 2.84, 0.0, 0.0), (5, 4.5, 0.0, 0.0), (6, 6.5, 0.0, 0.0),
              (7, 8.5, 0.0, 0.0), (8, 10.5, 0.0, 0.0), (9, 12.5, 0.0, 0.0),
              (10, 14.5, 0.0, 0.0), (11, 16.5, 0.0, 0.0), (12, 18.5, 0.0, 0.0),
              (13, 20.5, 0.0, 0.0), (14, 22.16, 0.0, 0.0), (15, 24.16, 0.0, 0.0),
              (16, 24.5, 0.0, 0.0), (17, 24.96, 0.0, 0.0)]
    for no, x, y, z in coords:
        engine.node.create(no, x, y, z)


# ===== 7. ELEMENT 单元 + 组 =====
def build_elements(engine: OSISEngine) -> None:
    # BEAM3D(no, type_str, n1, n2, mat, sec1, sec2, nYTrans, nZTrans, dStrain, bFlag, dTheta, bWarping)
    elements = [
        (1, "BEAM3D", 1, 2, 1, 4, 4, 1, 1, 0.0, 0, 0.0, 0),
        (2, "BEAM3D", 2, 3, 1, 4, 4, 1, 1, 0.0, 0, 0.0, 0),
        (3, "BEAM3D", 3, 4, 1, 5, 1, 1, 1, 0.0, 0, 0.0, 0),
        (4, "BEAM3D", 4, 5, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (5, "BEAM3D", 5, 6, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (6, "BEAM3D", 6, 7, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (7, "BEAM3D", 7, 8, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (8, "BEAM3D", 8, 9, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (9, "BEAM3D", 9, 10, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (10, "BEAM3D", 10, 11, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (11, "BEAM3D", 11, 12, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (12, "BEAM3D", 12, 13, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (13, "BEAM3D", 13, 14, 1, 1, 1, 1, 1, 0.0, 0, 0.0, 0),
        (14, "BEAM3D", 14, 15, 1, 1, 5, 1, 1, 0.0, 0, 0.0, 0),
        (15, "BEAM3D", 15, 16, 1, 4, 4, 1, 1, 0.0, 0, 0.0, 0),
        (16, "BEAM3D", 16, 17, 1, 4, 4, 1, 1, 0.0, 0, 0.0, 0),
    ]
    for elem in elements:
        engine.element.create(*elem)

    # 构件厚度分配
    engine.prop.assign_component_thickness(0.3108, "a", "1to2", "15to16")
    engine.prop.assign_component_thickness(0.2768, "a", 3, 14)
    engine.prop.assign_component_thickness(0.2429, "a", "4to13")

    # 单元组
    grp_defs = [("钢束-1-N1线型单元", [(1, "1to16")]),
                ("钢束-2-N2线型单元", [(2, "1to16")]),
                ("钢束-3-N3线型单元", [(3, "1to16")]),
                ("钢束-4-N4线型单元", [(4, "1to16")]),
                ("钢束-5-N5线型单元", [(5, "1to16")]),
                ("主梁单元",           [(6, "1to16")])]
    for name, ops in grp_defs:
        engine.element.group.create(name, "c")
        for _, ids in ops:
            engine.element.group.create(name, "a", ids)


# ===== 8. BOUNDARY 边界 =====
def build_boundaries(engine: OSISEngine) -> None:
    engine.boundary.create(1, "GENERAL", "", 1, 1, 1, 1, 0, 1, 0)
    engine.boundary.get(1).assign("a", 2)
    engine.boundary.create(2, "GENERAL", "", 0, 1, 1, 1, 0, 1, 0)
    engine.boundary.get(2).assign("a", 16)

    engine.boundary.group.create("桥台1_永久_x向固定", "c")
    engine.boundary.group.create("桥台1_永久_x向固定", "a", 1)
    engine.boundary.group.create("桥台2_永久_x向滑动", "c")
    engine.boundary.group.create("桥台2_永久_x向滑动", "a", 2)


# ===== 9. LOADCASE 荷载工况 =====
def build_loadcases(engine: OSISEngine) -> None:
    # 钢束特性(IN, mat_no, ?, code, diameter, num, pipe, friction, dev, eps_l, eps_r, tension, relax)
    tendon_props = [
        ("15-10", 10, "GBT5224_2014", 15.2, 10, 0.09, 0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
        ("15-3",  3,  "GBT5224_2014", 15.2, 3,  0.055, 0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
        ("15-4",  4,  "GBT5224_2014", 15.2, 4,  0.055, 0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
        ("15-5",  5,  "GBT5224_2014", 15.2, 5,  0.055, 0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
        ("15-6",  6,  "GBT5224_2014", 15.2, 6,  0.07,  0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
        ("15-7",  7,  "GBT5224_2014", 15.2, 7,  0.07,  0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
        ("15-8",  8,  "GBT5224_2014", 15.2, 8,  0.07,  0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
        ("15-9",  9,  "GBT5224_2014", 15.2, 9,  0.09,  0.17, 0.0015, 0.006, 0.006, 1.0, 0.3),
    ]
    for name, num, code, dia, n, pipe, fric, dev, e1, e2, ten, rel in tendon_props:
        engine.tendon.prop.create(name, "IN", 3, 1, code, dia, n, pipe, fric, dev, e1, e2, ten, rel)

    # 钢束形状 + 布置
    shapes = [
        ("N1", "15-4", "钢束-1-N1线型单元", "钢束-1-N1"),
        ("N2", "15-4", "钢束-2-N2线型单元", "钢束-2-N2"),
        ("N3", "15-4", "钢束-3-N3线型单元", "钢束-3-N3"),
        ("N4", "15-5", "钢束-4-N4线型单元", "钢束-4-N4"),
        ("N5", "15-5", "钢束-5-N5线型单元", "钢束-5-N5"),
    ]
    for name, prop_name, grp_name, curve in shapes:
        engine.tendon.shape.create(name, 2, prop_name, grp_name, "ARC3D", curve)
        engine.tendon.shape.get(name).layout("ELEMENT", 1, 0, 0, 0.0, 0.0, 0.0)

    # 端横梁荷载(CS)
    engine.load.create("端横梁荷载工况", "CS", 1.0)
    lc = engine.load.get("端横梁荷载工况")
    lc.create("NFORCE", 2,  0.0, 0.0, -20030.0, 0.0, 0.0, 0.0)
    lc.create("NFORCE", 16, 0.0, 0.0, -20030.0, 0.0, 0.0, 0.0)

    # 防撞护栏(CS)—— 16 个单元线荷载(逐字复刻 case)
    engine.load.create("防撞护栏工况", "CS", 1.0)
    lc = engine.load.get("防撞护栏工况")
    lc.create("LINE", 1,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 2,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 3,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 4,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 5,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 6,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 7,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 8,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 9,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 10, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 11, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 12, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 13, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 14, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 15, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 16, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -2120.0, 0.0, 0.0, 0.0)

    # 负温度梯度(TG)—— 逐字复刻 case
    engine.load.create("负温度梯度", "TG", 1.0)
    lc = engine.load.get("负温度梯度")
    lc.create("GTEMP", 1,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.164, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 2,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.164, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 3,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 4,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 5,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 6,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 7,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 8,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 9,  "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 10, "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 11, "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 12, "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 13, "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.017, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 14, "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.164, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 15, "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.164, -0.1, -2.75, -0.4, 0.0)
    lc.create("GTEMP", 16, "Z", "T", 2, 2.4, 0.0, -7.0, -0.1, -2.75, 1.164, -0.1, -2.75, -0.4, 0.0)

    # 铺装(CS)—— 16 个线荷载(逐字复刻 case)
    engine.load.create("铺装工况", "CS", 1.0)
    lc = engine.load.get("铺装工况")
    lc.create("LINE", 1,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 2,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 3,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 4,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 5,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 6,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 7,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 8,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 9,  0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 10, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 11, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 12, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 13, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 14, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 15, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)
    lc.create("LINE", 16, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -10850.0, 0.0, 0.0, 0.0)

    # 预应力(CS)
    engine.load.create("预应力", "CS", 1.0)
    lc = engine.load.get("预应力")
    lc.create("PST", "N1", "BOTH", "ST", 1395000000.0, 1395000000.0)
    lc.create("PST", "N2", "BOTH", "ST", 1395000000.0, 1395000000.0)
    lc.create("PST", "N3", "BOTH", "ST", 1395000000.0, 1395000000.0)
    lc.create("PST", "N4", "BOTH", "ST", 1395000000.0, 1395000000.0)
    lc.create("PST", "N5", "BOTH", "ST", 1395000000.0, 1395000000.0)

    # 整体降温(T)
    engine.load.create("整体降温", "T", 1.0)
    lc = engine.load.get("整体降温")
    for elem in range(1, 17):
        lc.create("UTEMP", elem, "X", -20.0)

    # 整体升温(T)
    engine.load.create("整体升温", "T", 1.0)
    lc = engine.load.get("整体升温")
    for elem in range(1, 17):
        lc.create("UTEMP", elem, "X", 20.0)

    # 正温度梯度(TG)—— 逐字复刻 case
    engine.load.create("正温度梯度", "TG", 1.0)
    lc = engine.load.get("正温度梯度")
    lc.create("GTEMP", 1,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.164, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 2,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.164, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 3,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 4,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 5,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 6,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 7,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 8,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 9,  "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 10, "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 11, "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 12, "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 13, "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.017, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 14, "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.164, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 15, "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.164, -0.1, 5.5, -0.4, 0.0)
    lc.create("GTEMP", 16, "Z", "T", 2, 2.4, 0.0, 14.0, -0.1, 5.5, 1.164, -0.1, 5.5, -0.4, 0.0)

    # 主梁自重(CS)
    engine.load.create("主梁单元自重", "CS", 1.0)
    lc = engine.load.get("主梁单元自重")
    lc.create("GRAVITY", 0.0, 0.0, -1.04)


# ===== 10. ANALYSIS 分析设置 =====
def build_analysis(engine: OSISEngine) -> None:
    engine.live.grade.create("简支小箱梁移动荷载", "JTGD60_2015", "HIGHWAY_I")
    engine.live.lane.create("车道", "VE", 24.0, 1.8, 1, 0, "主梁单元", 0.0, 0.0)
    engine.live.case.create("车道荷载包络", "JTGD60_2015", 1)
    lc = engine.live.case.get("车道荷载包络")
    lc.set_trans_reduction_factors(1.2, 1.0, 0.78, 0.67, 0.6, 0.55, 0.52, 0.5, 0.5, 0.5)
    lc.include("a", "车道荷载工况1", "简支小箱梁移动荷载", 1.0, 1, "CUSTOM", 4.91172, "车道")
    lc.set_lane_count("车道荷载工况1", 0, 1)


# ===== 11. STAGE 施工阶段 =====
def build_stages(engine: OSISEngine) -> None:
    engine.stage.create(1, "CS1_主梁预制、张拉预应力", 7.0)
    s1 = engine.stage.get(1)
    s1.define_element(1, 1, "主梁单元", 7.0, 0)
    s1.define_boundary(1, 1, "桥台1_永久_x向固定")
    s1.define_boundary(1, 1, "桥台2_永久_x向滑动")
    s1.define_loadcase(1, 1, "", "主梁单元自重")
    s1.define_loadcase(1, 1, "", "预应力")
    s1.define_loadcase(1, 1, "", "端横梁荷载工况")

    engine.stage.create(2, "CS2_存梁", 60.0)

    engine.stage.create(3, "CS3_二期恒载", 30.0)
    s3 = engine.stage.get(3)
    s3.define_loadcase(1, 1, "", "铺装工况")
    s3.define_loadcase(1, 1, "", "防撞护栏工况")

    engine.stage.create(4, "CS4_徐变十年", 3650.0)

    engine.stage.create(5, "CS5_运营阶段", 0.0)
    s5 = engine.stage.get(5)
    s5.define_loadcase(1, 1, "", "整体升温")
    s5.define_loadcase(1, 1, "", "整体降温")
    s5.define_loadcase(1, 1, "", "正温度梯度")
    s5.define_loadcase(1, 1, "", "负温度梯度")
    s5.define_analysis(1, "LIVE", "车道荷载包络")


# ===== 12. 跑 + summary + 导出 =====
def main() -> None:
    setup_control(engine)
    build_property(engine)
    build_materials(engine)
    build_sections(engine)
    build_nodes(engine)
    build_elements(engine)
    build_boundaries(engine)
    build_loadcases(engine)
    build_analysis(engine)
    build_stages(engine)

    print("\n== 模型 summary ==", flush=True)
    def _count(mgr):
        try: return len(mgr.all())
        except Exception as e: return f"<err: {e}>"
    for label, mgr in [
        ("material ", engine.material),
        ("section  ", engine.section),
        ("node     ", engine.node),
        ("element  ", engine.element),
        ("boundary ", engine.boundary),
        ("load     ", engine.load),
        ("stage    ", engine.stage),
    ]:
        print(f"  {label}: {_count(mgr)}", flush=True)

    print("\n== save ==", flush=True)
    engine.project.save(PROJ_PATH)

    print("\n== solve ==", flush=True)
    engine.solve()
    print("== solve done ==", flush=True)

    # ===== 13. 导出结果到 CSV =====
    # 求解器在 PROJ_DIR/test/Result/ 下生成 .lcr/.env(二进制),/output 命令
    # 会在 PROJ_DIR/test/Temperary/ 下生成可读的 .txt。这里把 .txt 读成 DataFrame
    # 导出成 UTF-8-BOM 的 CSV,Excel/记事本打开中文不乱码。
    result_dir = PROJ_DIR / "test" / "Result"
    temperary_dir = PROJ_DIR / "test" / "Temperary"
    if not result_dir.is_dir():
        print(f"\n(无 {result_dir})", flush=True)
        return

    print(f"\n== 导出 CSV 到 {temperary_dir} ==", flush=True)
    exported = 0
    for fname in sorted(result_dir.iterdir()):
        base = fname.stem
        ext = fname.suffix.lower()
        types = (("LCND", "LCEF"), ("EnvND", "EnvEF"))[ext == ".env"]
        for rt in types:
            try:
                r = engine.result.loadcase(base, rt) if ext == ".lcr" else engine.result.env(base, rt)
                csv_path = temperary_dir / f"{base}_{rt}.csv"
                r.to_csv(csv_path, index=False, encoding="utf-8-sig")
                exported += 1
                print(f"  {base}/{rt}: shape={r.shape}, -> {csv_path.name}", flush=True)
            except Exception as e:
                print(f"  {base}/{rt}: <err: {str(e)[:80]}>", flush=True)

    print(f"\n  共导出 {exported} 个 CSV 到 {temperary_dir}", flush=True)


if __name__ == "__main__":
    main()
    print(f"\n== 工程 {PROJ_PATH} ==", flush=True)
    print("== CSV 结果 ./demo_output/proj/test/Temperary/*.csv (UTF-8-BOM,Excel/记事本直开) ==", flush=True)
    print("ALL OK", flush=True)