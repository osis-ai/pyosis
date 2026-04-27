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

### 2. 直接使用 Manager

如果不需要 Engine 的便捷方法，也可以直接导入各模块管理器：

```python
from pyosis.material import material_manager
from pyosis.node import node_manager

mat = material_manager.create_conc("C30", eCode="JTG3362_2018", eGrade="C30")
node = node_manager.create(0, 0, 0)
```

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

需要安装 pandas：`pip install pandas`

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

## 注意事项

1. **需要先登录 OSIS**：执行代码前请确保 OSIS 软件已启动并登录，pyosis 通过 HTTP 与 OSIS 通信。
2. **异常处理**：所有操作失败时会抛出 `RuntimeError`，建议在实际工程中加上异常处理。
3. **无状态设计**：Manager 不缓存数据，频繁调用 `all()` 等查询方法会产生网络开销，在循环中建议谨慎使用。
4. **编号唯一性**：显式指定 `no` 时，如果编号已存在，行为取决于 OSIS 底层实现（通常覆盖或报错）。
5. **命令模式**：在 OSIS 命令模式下执行代码时，可直接发送 Python 代码块；在 IDE 中执行时，需确保 OSIS 已运行。

## 更多资源

- [tests/](tests/)：包含各模块的示例代码
- [templetes/](templetes/)：包含完整桥梁建模模板项目
