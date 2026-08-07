[English](README.md) | [简体中文](README.zh-CN.md)

# pyosis

中交公路规划设计院自研 **OSIS** 桥隧分析平台的 Python 接口库。

pyosis 提供了一套面向对象的 Python API，用于自动化创建桥梁/隧道有限元模型、执行分析求解以及后处理结果提取。

## 安装

由于 `pyosis` 在 PyPI 上存在重名，请使用以下方式安装：

```bash
pip install osis-python
```

如果镜像站未同步，可使用：

```bash
pip install osis-python -i https://pypi.org/simple
```

## 环境要求

- OSIS >= 5.0（包含所需的 Python 运行环境）
- Python >= 3.8
- **仅求解器模式（solver-only）** 额外显式提供 OSIS 求解器的安装目录（例如 `D:\OSIS_Solver`）。

## 快速开始

### 1. 使用 OSISEngine（推荐）

`OSISEngine` 是 pyosis 的核心门面类（Facade），整合了所有模块的管理器，提供统一的项目级入口：

```python
from pyosis.core.engine import OSISEngine

engine = OSISEngine()

# 清空项目
engine.clear()

# 设置全局参数
engine.control.set_gravity_acceleration(9.8066)
engine.control.set_calc_tendon(True)
engine.control.set_calc_creep(True)

# 创建截面
sec = engine.section.create_circle(no=1, name="圆形截面", d=0.5)

# 创建材料
mat = engine.material.create_conc(no=1, name="C30混凝土", code="JTG3362_2018", grade="C30")

# 创建节点
n1 = engine.node.create(no=1, x=0, y=0, z=0)
n2 = engine.node.create(no=2, x=15, y=0, z=0)

# 创建单元
elem = engine.element.create_beam3d(
    no=1, node1=n1.no, node2=n2.no, nMat=mat.no, nSec1=sec.no, nSec2=sec.no
)

# 创建边界
bd = engine.boundary.create_general(no=1, x=1, y=1, z=1, rx=1, ry=1, rz=1, rw=1)
bd.assign("a", [n1.no])

# 创建荷载工况并添加荷载
lc = engine.load.create("自重", load_case_type="D")
lc.create_gravity()

# 求解
engine.solve()
```

### 2. Engine 便捷方法

`OSISEngine` 提供项目级别的便捷方法：

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

# 矩阵定义
engine.matrix("矩阵1", [[1, 2],[3, 4]])
```

### 3. 直接使用 Manager

如果不需要 Engine 的便捷方法，也可以直接导入各模块管理器：

```python
from pyosis.material import material_manager
from pyosis.node import node_manager

mat = material_manager.create_conc(no=1, name="C30", code="JTG3362_2018", grade="C30")
node = node_manager.create(0, 0, 0)
```

### 4. 使用 OSISSolver 直接启动求解器（仅求解器模式）

默认情况下 `OSISEngine()` 连接的是已经打开的 OSIS 图形界面进程。如果希望**不打开 GUI** 直接驱动求解器（例如无头批量计算、CI、服务端自动化），可以用 `OSISSolver` 单独启动 OSIS 求解器。
```python
from pyosis.core.solver import OSISSolver
from pyosis.core.engine import OSISEngine

# 加载 <安装目录> 
solver = OSISSolver(osis_install_path=r"D:\OSIS_Solver")
engine = OSISEngine.from_solver(solver)

# 建工程（类型 101 = 通用桥梁分析），之后照常建模
engine.project.create(101, r"D:\work\my_bridge\my_bridge.sis")
engine.control.set_gravity_acceleration(9.8066)
# ... 截面 / 材料 / 节点 / 单元 ...
engine.solve()
```

仅求解器模式注意事项：

- 求解器必须先有工程才能执行建模命令：先 `engine.project.create()` / `open()`。
- 崩溃时 dmp 文件将固定写入 `<安装目录>\Error\dmp\`。

## 核心架构

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
| PostManager | `engine.post` | 后处理（荷载组合、规范验算） |
| ResultManager | `engine.result` | 结果导出（工况/包络/验算结果） |
| ControlManager | `engine.control` | 全局控制参数 |
| ProjectManager | `engine.project` | 项目操作 |
| DisplayManager | `engine.display` | 显示控制（边界/荷载/钢束显隐、视图方向、显示开关） |

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
engine.boundary.create_master_slave(no=1, node=1, dx=1, dy=1, dz=1, rx=0, ry=1, rz=1, coincident=2)  # 主从约束
engine.boundary.create_rigid(no=1, nNodeI=1)                                               # 刚性连接
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

# 活载
grade = engine.live.grade.create(name="公路-I级", code="JTGD60_2015", type="HIGHWAY_I")
lane = engine.live.lane.create(name="车道1", type="VE")
case = engine.live.case.create(name="活载工况1", code="JTGD60_2015")
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

### 属性与厚度管理

```python
# 坐标系（三点定义）
engine.prop.coord.create_three_point(
    no=1, p1x=0, p1y=0, p1z=0,
    p2x=1, p2y=0, p2z=0,
    p3x=0, p3y=1, p3z=0,
)

# 收缩徐变（no, name, avg_humidity, birth_time, type_coeff, shrink_birth）
engine.prop.creep_shrink.create(no=1, name="Creep1", avg_humidity=70.0,
                                birth_time=7, type_coeff=5.0, shrink_birth=3)

# 阻尼（Rayleigh 自定义系数）
engine.prop.damping.create_rayleigh_custom(name="Damping1", alpha=0.05, beta=0.005)

# P-U 曲线（no, name, curve_type, num, values）
#   curve_type: 1=水平位移推力 2=竖向位移推力 3=竖向力位移
engine.prop.pu_curve.create(no=1, name="PU1", curve_type=1, num=3, values=[0, 0.01, 1000, 0.02, 1500])

# 构件厚度分配（thickness, op, *elems）
engine.prop.assign_component_thickness(thickness=0.3, op="a", elems=[1])

# 壳厚度（no, in_plane, out_plane）
engine.thickness.create(no=1, in_plane=0.3, out_plane=0.3)
```

### 几何查询

`GeometryManager` 支持几何实体查询：

```python
# 获取所有样条曲线
splines = engine.geometry.all("spline")

# 获取指定样条曲线
spline = engine.geometry.get("spline", name="curve1")

# 按类型筛选
arcs = engine.geometry.filter("spline", spline_type="ARC3D")
```

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
lc.create_nforce(1, dFx=1000)
```

### 显式编号

部分 `create_*` 函数支持通过 `no` 参数显式指定编号，不指定时自动分配：

```python
# 自动分配编号
sec = engine.section.create_circle(name="截面1", d=0.5)

# 显式指定编号
sec = engine.section.create_circle(name="截面1", d=0.5, no=100)
```

## 结果导出

求解完成后，可通过 `engine.result` 导出各类分析结果，所有导出方法均返回 pandas DataFrame：

```python
# 导出荷载工况结果（单元内力）
df = engine.result.loadcase("自重", "LCEF")

# 导出包络结果（单元内力）
df = engine.result.env("基本组合包络", "EnvEF")

# 导出规范验算结果
df = engine.result.check(
    "混凝土", "正截面抗弯验算", "基本组合"
)

# 批量导出 Check 文件夹下所有验算结果
results = engine.result.check_all()
for name, df in results.items():
    print(f"{name}: {len(df)} 行")
```

支持的结果类型：
- **荷载工况**：`LCEF`（单元内力）、`LCED`（单元位移）、`LCND`（节点位移）、`LCBF`（边界反力）、`LCTL`（钢束损失）、`LCS`（单元应力）
- **包络**：`EnvBF`（边界反力）、`EnvEF`（单元内力）、`EnvES`（单元应变）、`EnvS`（单元应力）、`EnvND`（节点位移）

需要安装 pandas：`python -m install pandas`

## 完整示例

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
engine.section.create_circle("圆形截面1", d=0.219, tw=0.012, no=1)
engine.section.create_circle("圆形截面2", d=0.180, tw=0.008, no=2)

# 材料
engine.material.create_steel(
    no=2, name="钢材1", code="JTGD64_2015", grade="Q345", dmp=0.05,
)

# 节点
engine.node.create(0, 5, 0, no=1)
engine.node.create(15, 5, 0, no=2)
engine.node.create(7.5, 0, 0, no=3)
engine.node.create(20, 0, 0, no=4)

# 单元
engine.element.create_beam3d(1, 3, nMat=1, nSec1=1, nSec2=1, no=1)
engine.element.create_beam3d(2, 3, nMat=1, nSec1=2, nSec2=2, no=2)

# 边界
engine.boundary.create_general(no=1)
engine.boundary.get(1).assign("a", [1, 2])

# 荷载
lc = engine.load.create(
    "自定义工况1",
    load_case_type="USER",
    prompt="施加于节点3和4的两个力"
)
lc.create_nforce(3, dFx=0, dFy=-1000000, dFz=0)
lc.create_nforce(4, dFx=200000, dFy=0, dFz=0)

# 求解
engine.solve()
```

## 端到端示例

见 [`tests/pyosis_demo.py`](tests/pyosis_demo.py):一个可运行的端到端示例,完成以下流程:

- 通过 `OSISSolver` 直接启动求解器(无需 GUI)
- 建模 25m 简支小箱梁示例(10 个 prep 模块)
- 执行 `engine.solve()`
- 导出 LCND / LCEF / EnvND / EnvEF 结果到 CSV

该 demo 复用了 `tests/output/output_py/25m简支小箱梁中梁-solveronly/` 的 prep 模块,既可作为冒烟测试,也可作为可复制粘贴的模板。

