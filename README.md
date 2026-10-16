[English](README.en.md) | [简体中文](README.md)

# pyosis

中交公路规划设计院自研 **OSIS** 桥隧分析平台的 Python 接口库。

pyosis 提供一套面向对象的 Python API，用于自动化创建桥梁/隧道有限元模型、执行分析求解以及后处理结果提取。

## 安装

PyPI 上 `pyosis` 已被占用，包名是 `osis-python`：

```bash
pip install osis-python
```

镜像站未同步时：

```bash
pip install osis-python -i https://pypi.org/simple
```

## 环境要求

- OSIS >= 5.1（转换器和运行时同时兼容 `N`/`Ele`/`Sec` 等缩写命令名）
- Python >= 3.8
- pandas（结果导出）
- **仅求解器模式（solver-only）** 额外需要含 `osisSdk.dll` 的求解器安装目录（例如 `D:\OSIS_Solver\Rbin64`）

> `osis_init` 需要许可文件 `osis.lic`（HMAC 签名）才能启动。查找顺序：环境变量 `OSIS_LICENSE_FILE` → `%ProgramData%\OSIS\osis.lic` → 安装目录下的 `osis.lic`。许可向 OSIS 供应方获取。

## 快速开始

`OSISEngine` 是 pyosis 的核心门面类，整合了所有模块的管理器，提供统一的项目级入口。建档、求解、取结果一次走完：

```python
from pyosis.core.engine import OSISEngine

engine = OSISEngine()      # 默认连接已打开的 OSIS 界面进程
engine.clear()

engine.control.set_gravity_acceleration(9.8066)
engine.control.set_calc_tendon(True)
engine.control.set_calc_creep(True)

# 截面 / 材料
sec = engine.section.create_circle(no=1, name="圆形截面", d=0.5)
mat = engine.material.create_conc(no=1, name="C30混凝土", code="JTG3362_2018", grade="C30")

# 节点 / 单元
n1 = engine.node.create(no=1, x=0, y=0, z=0)
n2 = engine.node.create(no=2, x=15, y=0, z=0)
elem = engine.element.create_beam3d(
    no=1, node1=n1.no, node2=n2.no, mat=mat.no, sec1=sec.no, sec2=sec.no
)

# 边界
bd = engine.boundary.create_general(no=1, x=1, y=1, z=1, rx=1, ry=1, rz=1, rw=1)
bd.assign("a", [n1.no])

# 荷载工况
lc = engine.load.create("自重", load_case_type="D")
lc.create_gravity()

# 求解
engine.solve()

# 取结果
df = engine.result.node_displacement("自重")
```

### 无头模式（仅求解器）

**不打开 GUI** 直接驱动求解器（无头批量计算、CI、服务端自动化）时，用 `OSISSolver` 通过 ctypes 加载求解器 DLL 并起 HTTP 服务：

```python
from pyosis.core.solver import OSISSolver
from pyosis.core.engine import OSISEngine

# 加载 <安装目录>/osisSdk.dll 并启动 HTTP 服务（默认端口 18080）
solver = OSISSolver(osis_install_path=r"D:\OSIS_Solver\Rbin64")
engine = OSISEngine.from_solver(solver)

# 建工程（类型 101 = 通用桥梁分析），之后照常建模
engine.project.create(101, r"D:\work\my_bridge\my_bridge.sis")
engine.control.set_gravity_acceleration(9.8066)
# ... 截面 / 材料 / 节点 / 单元 ...
engine.solve()
```

注意事项：

- `osis_install_path` 必须是含 `osisSdk.dll`（及其依赖 DLL）的目录。
- `port=0` 时由系统随机分配端口并回写到 `solver.port`。
- 求解器必须先有工程才能执行建模命令：先 `engine.project.create()` / `open()`。
- 崩溃时 dmp 文件写入 `<安装目录>\Error\dmp\`。

### 其他入口

`OSISEngine` 另有一批项目级便捷方法：

```python
# 项目管理
engine.new_project()           # 新建项目
engine.save_project()          # 保存当前项目
engine.open_project(path)      # 打开已有项目

# 模型信息
summary = engine.model_summary()  # 返回包含各管理器数量的字典

# 导入/导出
engine.export_apdl(path)       # 导出为 APDL 格式
engine.import_apdl(path)       # 从 APDL 格式导入

# 计算书结果
engine.output_result_for_calc_book()

# 矩阵定义
engine.matrix("矩阵1", [[1, 2],[3, 4]])
```

也可以绕过 Engine，直接导入各模块管理器：

```python
from pyosis.material import material_manager
from pyosis.node import node_manager

mat = material_manager.create_conc(no=1, name="C30", code="JTG3362_2018", grade="C30")
node = node_manager.create(no=None, x=0, y=0, z=0)
```

## 核心概念

### Manager 体系

pyosis 采用 Manager 模式组织代码，每个模块对应一个 Manager：

| 管理器 | 属性名 | 说明 |
|--------|--------|------|
| MaterialManager | `engine.material` | 材料（混凝土、钢材、预应力、钢筋等） |
| SectionManager | `engine.section` | 截面（箱梁、T梁、空心板、钢箱梁等） |
| NodeManager | `engine.node` | 节点 |
| ElementManager | `engine.element` | 单元（梁、桁架、弹簧、拉索、壳） |
| BoundaryManager | `engine.boundary` | 边界（一般支撑、主从、弹性支承等） |
| GeometryManager | `engine.geometry` | 几何实体（样条曲线、空间曲线等） |
| PropertyManager | `engine.prop` | 属性（坐标系、收缩徐变、阻尼、P-U曲线、构件厚度分配） |
| ThicknessManager | `engine.thickness` | 壳厚度特性 |
| LoadCaseManager | `engine.load` | 荷载工况 |
| StageManager | `engine.stage` | 施工阶段 |
| TendonManager | `engine.tendon` | 钢束（特性+形状） |
| LiveManager | `engine.live` | 活载（等级+车道+工况） |
| SettlementManager | `engine.settlement` | 沉降分析 |
| StabilityManager | `engine.stability` | 稳定分析 |
| DynamicManager | `engine.dynamic` | 动力分析 |
| ControlManager | `engine.control` | 全局控制参数 |
| ProjectManager | `engine.project` | 项目操作 |
| DisplayManager | `engine.display` | 显示控制（边界/荷载/钢束显隐、视图方向、显示开关） |
| ResultManager | `engine.result` | 结果导出（工况/包络/验算结果） |
| PostManager | `engine.post` | 后处理（荷载组合、规范验算） |

### 数据类对象

创建和查询操作返回数据类对象（dataclass），而非原始字典：

```python
elem = engine.element.get(1)
print(elem.no)          # 编号
print(elem.node_vec)    # 节点列表
print(elem.mat)         # 材料编号

# 对象支持操作（操作下沉）
lc = engine.load.get("自重")
lc.create_gravity()
lc.create_nforce(1, fx=1000)
```

### 枚举

所有类型编码集中在 `pyosis.core.enums`。每个成员的**名字就是 OSIS 命令流里的写法**，
成员可以直接当字符串用；值是接口 JSON 里的整数编码：

```python
from pyosis.core.enums import SectionType

SectionType.Rectangle.value      # 5              — OSIS 下发的编码
str(SectionType.Rectangle)       # "Rectangle"    — 命令流写法
SectionType.name_of(5)           # "Rectangle"
SectionType.of(404)              # SectionType.Unassigned — 未知编码回退
```

## 建模

### 子管理器

部分管理器包含子管理器，通过属性访问：

```python
# 单元组(一次调用完成 创建 + 添加单元)
engine.element.group.create("主梁单元", "c")            # 创建空组
engine.element.group.create("主梁单元", "a", "1to3")    # 添加单元 1-3

# 边界组
engine.boundary.group.create("桥台边界", "c")
engine.boundary.group.create("桥台边界", "a", "1to2")

# 各类边界条件
engine.boundary.create_general(no=1, x=1, y=1, z=1, rx=1, ry=1, rz=1, rw=1)           # 一般支撑
engine.boundary.create_master_slave(no=1, node=1, dx=1, dy=1, dz=1, rx=0, ry=1, rz=1, coincident=1)  # 主从约束
engine.boundary.create_rigid(no=1, node_i=1)                                               # 刚性连接
engine.boundary.create_elstcspt(no=1, coor="", x=0, dx=1e9, y=0, dy=1e9, z=0, dz=1e9)     # 弹性支承

# 钢束
prop = engine.tendon.prop.create_in(
    name="15-10", mat=3, code="GBT5224_2014",
    diameter=15.2, num=10, pipe=0.09,
)
shape = engine.tendon.shape.create_arc3d(
    name="N1", n_num=2, prop="15-10",
    element_group="主梁单元", curve_name="curve1"
)

# 活载：等级 -> 车道 -> 工况
engine.live.grade.create_highway("公路I级", code="JTGD60_2015", live_load_type="HIGHWAY_I")
engine.live.lane.create_ve("车道", length=19.1, wheel=1.8, orientation=1,
                           ref=0, ref_elems="主梁单元", offset_y=0.0, offset_z=0.0)
lc = engine.live.case.create("车道荷载包络", code="JTGD60_2015", sub_cmb_type=1)
lc.create_sub("车道荷载工况1", "公路I级", scalar=0.75, calc_mu=True,
              bridge_type="CUSTOM", mu_params=[6.586960], lane_names=["车道"])
```

### 属性与厚度

```python
# 坐标系（三点定义）
engine.prop.coord.create_three_point(
    no=1, p1x=0, p1y=0, p1z=0,
    p2x=1, p2y=0, p2z=0,
    p3x=0, p3y=1, p3z=0,
)

# 收缩徐变（no, name, code, fcuk, avg_humidity,
#          component_approximate_size, type_coeff, birth_by_shrinking, fly_ash_ratio）
engine.prop.creep_shrink.create(no=1, name="Creep1", avg_humidity=70.0,
                                type_coeff=5.0, birth_by_shrinking=3)

# 阻尼（Rayleigh 自定义系数）
engine.prop.damping.create_rayleigh_custom(name="Damping1", alpha=0.05, beta=0.005)

# P-U 曲线（no, name, curve_type, num, *values）
#   curve_type: 0=力，1=力矩
#   values 按点交错共 2*num 个：(位移, 力) (位移, 力) …
engine.prop.pu_curve.create(1, "PU1", 1, 2, 0.0, 0.0, 0.02, 1500.0)

# 构件厚度分配（thickness, op, *elems）
engine.prop.assign_component_thickness(0.3, "a", 1)

# 壳厚度（no, is_uniform, in_plane, out_plane, ...）
engine.thickness.create(no=1, is_uniform=0, in_plane=0.3, out_plane=0.3)
```

### 几何查询

```python
# 获取所有样条曲线
splines = engine.geometry.all()

# 获取指定样条曲线
spline = engine.geometry.get("curve1")

# 按类型筛选
arcs = [s for s in engine.geometry.all() if s.spline_type is SplineType.ARC3D]
```

### 显示控制

```python
# 边界 / 荷载 / 钢束显隐
engine.display.disp_ctrl("bc", "all", "all", 1)          # 显示所有边界
engine.display.disp_ctrl("lg", "nforce", "all", 0)       # 隐藏所有集中力
engine.display.disp_ctrl("td", "all", ["T1", "T2"], 1)   # 显示指定钢束

# 视图方向
engine.display.set_view("top")          # standard / top / right / front

# 显示开关
engine.display.set_plsm(1)              # 0 = 关，1 = 开
```

## 结果导出

求解完成后，可通过 `engine.result` 查询各类分析结果，所有方法均返回 pandas DataFrame。

结果统一走 PySolver 的 HTTP 路由（`/GetAll*`、`/Get*ByNames`），有界面和无界面模式取的是同一份数据，无需区分模式：

```python
# 节点位移（name 省略则返回全部工况）
df = engine.result.node_displacement("自重")

# 单元内力
df = engine.result.element_force("自重")

# 单元应力（by_part=True 按截面分块，额外带 part 列）
df = engine.result.element_stress("自重", by_part=True)

# 支座反力
df = engine.result.support_reaction("自重")

# 钢束（预应力）损失
df = engine.result.tendon_loss("自重")

# 模态（特征值/周期/频率）。模态挂在施工阶段上，结果名形如 _自振模态_<阶段名>，
# 首列是 name 而不是 loadCase
df = engine.result.modal()

# 包络：kind 取 displacement / force / stress / reaction
df = engine.result.envelope("基本组合包络", kind="force")
```

`name` 可传单个工况名或名字列表。名字查不到时默认只发 `UserWarning` 并返回空表——「名字写错」和「该名字下确实没有这类结果」无法区分，都会是空结果；需要严格报错时传 `strict=True`：

```python
df = engine.result.element_force("不存在的工况", strict=True)   # 抛 RuntimeError
```

包络结果的行按 (节点, 分量) 分，值给的是各分量自身极值拼成的包络向量——同一节点的各分量行数值相同，分量列是标签。`kind="reaction"` 额外带 `extreme`（Min/Max）与 `sys`（边界坐标系号）列。

### 列名从哪来

服务端**不做列名翻译**：它把软件结果表的表头（中文）和数值原样搬过来，翻译成 `ux`/`sxFx` 这类英文键的映射表在 pyosis 这边的 `src/pyosis/result/routes.py`。

所以求解器改了表头时，改一行 Python 重装即可。两种失配的表现：

- 认不出的列 → `UserWarning` 点名，该列跳过，其余照常
- 必需的列认不出来 → 直接 `RuntimeError`，并打出服务端实际给出的全部表头，照着在 `_COLUMNS` 里补一行即可

### 规范验算结果

验算结果尚无 HTTP 路由，仍走 `/output` 命令流导出：

```python
df = engine.result.check("混凝土", "正截面抗弯验算", "基本组合")

# 批量导出 Check 文件夹下所有验算结果
results = engine.result.check_all()
for name, df in results.items():
    print(f"{name}: {len(df)} 行")
```

### 从 0.8.1 迁移

`loadcase()` / `env()` **已删除**，不再保留兼容别名。这两种写法按结果类型逐个替换即可：

| 旧写法 | 新写法 |
|---|---|
| `loadcase(name, "LCND")` | `node_displacement(name)` |
| `loadcase(name, "LCEF")` | `element_force(name)` |
| `loadcase(name, "LCS")` | `element_stress(name)` |
| `loadcase(name, "LCBF")` | `support_reaction(name)` |
| `loadcase(name, "LCTL")` | `tendon_loss(name)` |
| `env(name, "EnvND")` | `envelope(name, "displacement")` |
| `env(name, "EnvEF")` | `envelope(name, "force")` |
| `env(name, "EnvS")` | `envelope(name, "stress")` |
| `env(name, "EnvBF")` | `envelope(name, "reaction")` |

`loadcase` 的 `LCED`（单元位移）与 `env` 的 `EnvES`（单元应变）没有对应路由，本次一并移除，不再支持。**列名也随之改变**：旧接口给的是 txt 表头（如 `Fx(N)`），新接口给的是路由的英文键（如 `fx`）。

## 批量执行与性能

大型模型逐条发命令时，主要开销是 OSIS 内部每条命令执行函数的初始化。把建模代码包进 `with batch():`，退出时块内**所有** OSIS 命令合并为**一次** `OSIS_Run` HTTP 请求发出：

```python
from pyosis import batch

with batch():
    engine.clear()
    engine.clc()
    engine.control.set_gravity_acceleration(9.8066)
    engine.material.create_conc(no=1, name="C50", ...)
    for i in range(1000):
        engine.node.create(no=i + 1, x=i * 0.1, y=0.0, z=0.0)
    for i in range(999):
        engine.element.create_beam3d(no=i + 1, node1=i + 1, node2=i + 2, ...)
```

要点：

- 支持嵌套 `with batch():`，仅最外层退出时统一冲刷；
- 块内的查询（`get`、`all`）会先自动冲刷缓冲再发起读取，保证读到正确结果；
- 块内若抛异常，自 `__enter__` 起入队的命令全部丢弃，原异常再抛出；
- 块内可手动调用 `flush()` 提前冲刷；
- `next_no()`（自动编号）在 batch 内直接抛错（它要回查服务器），请显式传入 `no=...`，或退出 batch 后再做自动编号。

`25m简支小箱梁中梁` 实测：未启用 batch 约 3000 次往返，启用后 3 次（clear + clc + 最终冲刷）。

### 链式调用

`get()` 返回的数据类对象支持零服务器往返的链式调用：

```python
with batch():
    lc = engine.load.create("Self-weight", load_case_type="D")
    lc.create_gravity()
    lc.create_nforce(node=1, fx=0, fy=-1000, fz=0)
    # ↑ 三条命令全部入队，OSIS_Run 请求只在块退出时发出一次
```

身份属性（`lc.no`、`lc.name`）不触发服务器交互；数据字段（`lc.type`、`lc.elements`）首次访问会物化（一次冲刷+查询），后续直接读缓存。

## .out → pyosis 转换器

pyosis 自带把 OSIS 命令流（`.out`）一键转换为可运行 pyosis 项目的工具：

```bash
python src/pyosis/transfer/out_to_python.py path/to/model.out path/to/output_project
```

> `/OSIS_Run` 的命令流切分器不剥离 `//` 行注释，注释行会与紧随其后的命令合并成一条非法命令。转换器发送前已剥除注释；自行拼接 `.out` 载荷时需预先去掉注释行，或改用生成的 `main.py` 走 `osis_run()`。

生成的项目结构：

```
output_project/
└── prep/
    ├── main.py           # 入口（batch 模式跑完所有 10 个模块）
    ├── _1_control.py     # 全局控制参数
    ├── _2_property.py    # 几何/坐标系/阻尼/收缩徐变等属性
    ├── _3_material.py    # 材料
    ├── _4_section.py     # 截面（含网格划分）
    ├── _5_node.py        # 节点
    ├── _6_element.py     # 单元
    ├── _7_boundary.py    # 边界条件
    ├── _8_loadcase.py    # 荷载工况
    ├── _9_analysis.py    # 分析设置（沉降/活载/动力/稳定）
    └── _10_stage.py      # 施工阶段
```

运行：

```bash
cd output_project
python prep/main.py            # 仅建模
python prep/main.py --solve    # 建模 + 求解
```

转换器特性：

- 同时识别长名（`Node`/`Element`/`Section`/`Material`/`LoadCase`/`Boundary`/`Stage`）和 OSIS 5.1 缩写名（`N`/`Ele`/`Sec`/`SecOff`/`SecMesh`/`Mat`/`LC`/`Bd`/`Stg`），自动归一化；
- `SectionMesh` 按手册 7.3.6.2 的新格式 `Index, PartID, MeshMethod, MeshSize` 生成（混凝土截面 `PartID=1`，模板组合截面 `PartID=2`）；
- `Spline3D` 按类型字段分发到 `engine.geometry.create_general` / `create_natural` / `create_arc2d` / `create_arc3d`；
- 暂未建模的命令用 `engine.run(...)` 原样透传给 OSIS，保证模型可执行；需要拆成 pyosis 调用时可人工改写。

## 完整建模示例

```python
from pyosis.core.engine import OSISEngine

engine = OSISEngine()
engine.clear()

# 控制参数
engine.control.set_gravity_acceleration(9.8066)
engine.control.set_calc_tendon(True)
engine.control.set_calc_concurrent_force(True)
engine.control.set_calc_shrink(True)
engine.control.set_calc_creep(True)
engine.control.set_calc_shear(True)
engine.control.set_calc_relaxation(True)
engine.control.set_mod_loc_coor(False)
engine.control.set_inc_tendon(True)
engine.control.set_nonlinear(geom=False, link=False)

# 截面
engine.section.create_circle(no=1, name="圆形截面1", d=0.219, tw=0.012)
engine.section.create_circle(no=2, name="圆形截面2", d=0.180, tw=0.008)

# 材料
engine.material.create_steel(
    no=2, name="钢材1", code="JTGD64_2015", grade="Q345", dmp=0.05,
)

# 节点
engine.node.create(no=1, x=0, y=5, z=0)
engine.node.create(no=2, x=15, y=5, z=0)
engine.node.create(no=3, x=7.5, y=0, z=0)
engine.node.create(no=4, x=20, y=0, z=0)

# 单元
engine.element.create_beam3d(no=1, node1=1, node2=3, mat=1, sec1=1, sec2=1)
engine.element.create_beam3d(no=2, node1=2, node2=3, mat=1, sec1=2, sec2=2)

# 边界
engine.boundary.create_general(no=1)
engine.boundary.get(1).assign("a", [1, 2])

# 荷载
lc = engine.load.create(
    "自定义工况1",
    load_case_type="USER",
    prompt="施加于节点3和4的两个力"
)
lc.create_nforce(3, fx=0, fy=-1000000, fz=0)
lc.create_nforce(4, fx=200000, fy=0, fz=0)

# 求解
engine.solve()
```

## 端到端示例

**仅求解器模式**：见 [`tests/pyosis_demo.py`](tests/pyosis_demo.py)，一个自包含的可运行示例，流程为

- 通过 `OSISSolver` 直接启动求解器（无需 GUI）
- 建模 25m 简支小箱梁示例（10 个 prep 模块）
- 执行 `engine.solve()`
- 导出节点位移 / 单元内力 / 支座反力 / 钢束损失 / 模态 / 四类包络到 CSV

输出写在仓库根目录的 `temp/demo_output/`（`temp/` 不进版本库）。

**GUI 模式**：单文件 demo [`tests/demo_gui.py`](tests/demo_gui.py) 由 `temp/xiaoxiangliang.out` 转换后的项目合并而来，在已打开的 OSIS 5.1+ GUI 上直接运行：

```bash
python tests/demo_gui.py            # 仅建模
python tests/demo_gui.py --solve    # 建模 + 求解
```

文件内含 engine 初始化、全部 10 个 `build_*` 函数（control/property/material/section/node/element/boundary/loadcase/analysis/stage）以及驱动函数 `build_model()`，整体包在 `with batch():` 内，约 250 条命令一次性通过 `OSIS_Run` 送到 OSIS。

重新生成单文件 demo 与多模块项目：

```bash
python temp/_merge_demo_gui.py                                                        # 生成 tests/demo_gui.py
python src/pyosis/transfer/out_to_python.py temp/xiaoxiangliang.out temp/output_py/xiaoxiangliang
```
