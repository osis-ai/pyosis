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
- **仅求解器模式（solver-only）** 额外需要带 `PySolver.dll` 的求解器安装目录（例如 `D:\OSIS_Solver\Rbin64`）。

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
sec = engine.section.create_circle("圆形截面", d=0.5, tw=0.02)

# 创建材料
mat = engine.material.create_conc("C30混凝土", eCode="JTG3362_2018", eGrade="C30")

# 创建节点
n1 = engine.node.create(0, 0, 0)
n2 = engine.node.create(15, 0, 0)

# 创建单元
elem = engine.element.create_beam3d(
    n1.no, n2.no, nMat=mat.no, nSec1=sec.no, nSec2=sec.no
)

# 创建边界
bd = engine.boundary.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1)
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

mat = material_manager.create_conc("C30", eCode="JTG3362_2018", eGrade="C30")
node = node_manager.create(0, 0, 0)
```

### 4. 使用 OSISSolver 直接启动求解器（仅求解器模式）

默认情况下 `OSISEngine()` 连接的是已经打开的 OSIS 图形界面进程。如果希望**不打开 GUI** 直接驱动求解器（例如无头批量计算、CI、服务端自动化），可以用 `OSISSolver` 通过 ctypes 直接加载求解器 DLL 并启动其 HTTP server：

```python
from pyosis.core.solver import OSISSolver
from pyosis.core.engine import OSISEngine

# 加载 <安装目录>/PySolver.dll 并启动 HTTP server（默认端口 18080）
solver = OSISSolver(osis_install_path=r"D:\OSIS_Solver\Rbin64")
engine = OSISEngine.from_solver(solver)

# 建工程（类型 101 = 桥梁分析），之后照常建模
engine.project.create(101, r"D:\work\my_bridge\my_bridge.sis")
engine.control.set_gravity_acceleration(9.8066)
# ... 截面 / 材料 / 节点 / 单元 ...
engine.solve()
```

仅求解器模式注意事项：

- `osis_install_path` 必须是包含 `PySolver.dll`（及其依赖 DLL）的目录。
- 求解器必须先有工程才能执行建模命令：先 `engine.project.create()` / `open()`。
- 崩溃 minidump 固定写入 `<安装目录>\Error\dmp\`（启动时自动创建）。

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

### 子管理器

部分管理器包含子管理器，通过属性访问：

```python
# 单元组
grp = engine.element.group.create("主梁单元")
grp.add([1, 2, 3])

# 边界组
bg = engine.boundary.group.create("桥台边界")
bg.add([1, 2])

# 各类边界条件
engine.boundary.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1)  # 一般支撑
engine.boundary.create_master_slave(nMast=1, nSlav=2, dDir=1)           # 主从约束
engine.boundary.create_release(nElem=1, iReleaseEnd=2)                  # 端部释放
engine.boundary.create_elstcspt(nNode=1, dK=[1e9, 1e9, 1e9, 0, 0, 0])  # 弹性支承
engine.boundary.create_general_elstcspt(nNode=1, bX=1, bY=1, bZ=1, dKx=1e9, dKy=1e9, dKz=1e9)  # 一般弹性支承
engine.boundary.create_rigid(nNode1=1, nNode2=2)                        # 刚性连接
engine.boundary.create_section_factor(nElem=1, iEnd=1)                  # 截面系数

# 钢束
prop = engine.tendon.prop.create_in(
    "15-10", mat_no=1, e_code="GBT5224_2014",
    diameter=15.2, n_num=10, d_pipe=0.09
)
shape = engine.tendon.shape.create_arc3d(
    "N1", n_num=2, prop="15-10",
    element_group="主梁单元", curve_name="curve1"
)

# 活载
grade = engine.live.grade.create("公路-I级")
lane = engine.live.lane.create("车道1")
case = engine.live.case.create("活载工况1")
```

### 属性与厚度管理

```python
# 坐标系
engine.prop.coord.create_local("CS1", origin=[0, 0, 0], x_axis=[1, 0, 0], y_axis=[0, 1, 0])

# 收缩徐变
engine.prop.creep_shrink.create("Creep1", eCode="JTG3362_2018", eGrade="C30")

# 阻尼
engine.prop.damping.create("Damping1", dDmp=0.05)

# P-U 曲线（用于土-结构相互作用）
engine.prop.pu_curve.create("PU1", data=[(0, 0), (0.01, 1000), (0.02, 1500)])

# 构件厚度分配
engine.prop.thickness.assign_element(nElem=1, dThick=0.3)

# 壳厚度特性
engine.thickness.create_uniform("Thick1", dThick=0.3)
engine.thickness.create_tapered("Thick2", dThick1=0.2, dThick2=0.4)
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
sec = engine.section.create_circle("截面1", d=0.5)

# 显式指定编号
sec = engine.section.create_circle("截面1", d=0.5, no=100)
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
    "钢材1", eCode="JTGD64_2015", eGrade="Q345", dDmp=0.05, no=1
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

## 更多资源

- [tests/](tests/)：包含各模块的示例代码
- [tests/_scratch_solve_probe.py](tests/_scratch_solve_probe.py)：仅求解器端到端示例（启动求解器 → 建工程 → 跑完十个建模模块 → 求解 → summary）
