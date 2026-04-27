[简体中文](README.zh-CN.md) | [English](README.md)

# pyosis

Python client library for **OSIS** Bridge & Tunnel Analysis Platform (developed by CCCC Highway Consultants Co., Ltd.).

pyosis provides an object-oriented Python API for automating the creation of bridge/tunnel finite element models, executing analysis solvers, and extracting post-processing results.

## Installation

Due to naming conflicts on PyPI, please install using:

```bash
pip install osis-python
```

If your mirror hasn't synced yet, use:

```bash
pip install osis-python -i https://pypi.org/simple
```

## Requirements

- OSIS >= 5.0 (includes the required Python runtime environment)
- Python >= 3.8

## Quick Start

### 1. Using OSISEngine (Recommended)

`OSISEngine` is the core facade class of pyosis, integrating all module managers and providing a unified project-level entry point:

```python
from pyosis.core.engine import OSISEngine

engine = OSISEngine()

# Clear project
engine.clear()

# Set global parameters
engine.control.set_gravity_acceleration(9.8066)
engine.control.set_calc_tendon(True)
engine.control.set_calc_creep(True)

# Create sections
sec = engine.section.create_circle("Circle Section", d=0.5, tw=0.02)

# Create materials
mat = engine.material.create_conc("C30 Concrete", eCode="JTG3362_2018", eGrade="C30")

# Create nodes
n1 = engine.node.create(0, 0, 0)
n2 = engine.node.create(15, 0, 0)

# Create elements
elem = engine.element.create_beam3d(
    n1.no, n2.no, nMat=mat.no, nSec1=sec.no, nSec2=sec.no
)

# Create boundaries
bd = engine.boundary.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1)
bd.assign("a", [n1.no])

# Create load case and add loads
lc = engine.load.create("Self-weight", load_case_type="D")
lc.create_gravity()

# Solve
engine.solve()
```

### 2. Using Managers Directly

If you don't need the convenience methods of Engine, you can also import individual managers directly:

```python
from pyosis.material import material_manager
from pyosis.node import node_manager

mat = material_manager.create_conc("C30", eCode="JTG3362_2018", eGrade="C30")
node = node_manager.create(0, 0, 0)
```

## Core Architecture

### Manager System

pyosis adopts a Manager pattern to organize code. Each module corresponds to a Manager:

| Manager | Attribute | Description |
|---------|-----------|-------------|
| MaterialManager | `engine.material` | Materials (concrete, steel, prestressed, rebar, etc.) |
| SectionManager | `engine.section` | Sections (box girder, T-girder, hollow slab, steel box, etc.) |
| NodeManager | `engine.node` | Nodes |
| ElementManager | `engine.element` | Elements (beam, truss, spring, cable, shell) |
| BoundaryManager | `engine.boundary` | Boundaries (general support, master-slave, elastic support, etc.) |
| LoadCaseManager | `engine.load` | Load cases |
| StageManager | `engine.stage` | Construction stages |
| TendonManager | `engine.tendon` | Tendons (properties + shapes) |
| LiveManager | `engine.live` | Live loads (grades + lanes + cases) |
| SettlementManager | `engine.settlement` | Settlement analysis |
| StabilityManager | `engine.stability` | Stability analysis |
| DynamicManager | `engine.dynamic` | Dynamic analysis |
| PostManager | `engine.post` | Post-processing |
| ControlManager | `engine.control` | Global control parameters |
| ProjectManager | `engine.project` | Project operations |

### Sub-Managers

Some managers contain sub-managers, accessed via attributes:

```python
# Element groups
grp = engine.element.group.create("Main Girder Elements")
grp.add([1, 2, 3])

# Boundary groups
bg = engine.boundary.group.create("Abutment Boundaries")
bg.add([1, 2])

# Tendons
prop = engine.tendon.prop.create_in(
    "15-10", mat_no=1, e_code="GBT5224_2014",
    diameter=15.2, n_num=10, d_pipe=0.09
)
shape = engine.tendon.shape.create_arc3d(
    "N1", n_num=2, prop="15-10",
    element_group="Main Girder Elements", curve_name="curve1"
)

# Live loads
grade = engine.live.grade.create("Highway-Class I")
lane = engine.live.lane.create("Lane 1")
case = engine.live.case.create("Live Load Case 1")
```

### Data Class Objects

Create and query operations return data class objects (dataclass) instead of raw dictionaries:

```python
elem = engine.element.get(1)
print(elem.no)          # ID
print(elem.node_vec)    # Node list
print(elem.mat)         # Material ID

# Objects support operations (operations下沉 to object)
lc = engine.load.get("Self-weight")
lc.create_gravity()
lc.create_nforce(1, dFx=1000)
```

### Explicit Numbering

Some `create_*` functions support explicit numbering via the `no` parameter. If not specified, the number is automatically assigned:

```python
# Auto-assigned number
sec = engine.section.create_circle("Section 1", d=0.5)

# Explicit number
sec = engine.section.create_circle("Section 1", d=0.5, no=100)
```

## Complete Example

```python
from pyosis.core.engine import OSISEngine

engine = OSISEngine()
engine.clear()

# Control parameters
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

# Sections
engine.section.create_circle("Circle Section 1", d=0.219, tw=0.012, no=1)
engine.section.create_circle("Circle Section 2", d=0.180, tw=0.008, no=2)

# Materials
engine.material.create_steel(
    "Steel 1", eCode="JTGD64_2015", eGrade="Q345", dDmp=0.05, no=1
)

# Nodes
engine.node.create(0, 5, 0, no=1)
engine.node.create(15, 5, 0, no=2)
engine.node.create(7.5, 0, 0, no=3)
engine.node.create(20, 0, 0, no=4)

# Elements
engine.element.create_beam3d(1, 3, nMat=1, nSec1=1, nSec2=1, no=1)
engine.element.create_beam3d(2, 3, nMat=1, nSec1=2, nSec2=2, no=2)

# Boundaries
engine.boundary.create_general(no=1)
engine.boundary.get(1).assign("a", [1, 2])

# Loads
lc = engine.load.create(
    "Custom Load Case 1",
    load_case_type="USER",
    prompt="Two forces applied at nodes 3 and 4"
)
lc.create_nforce(3, dFx=0, dFy=-1000000, dFz=0)
lc.create_nforce(4, dFx=200000, dFy=0, dFz=0)

# Solve
engine.solve()
```

## Important Notes

1. **OSIS must be running**: Before executing code, ensure the OSIS software is launched and logged in. pyosis communicates with OSIS via HTTP.
2. **Exception handling**: All operations throw `RuntimeError` on failure. It is recommended to add exception handling in production code.
3. **Stateless design**: Managers do not cache data. Frequent calls to `all()` and other query methods incur network overhead. Use cautiously in loops.
4. **Number uniqueness**: When explicitly specifying `no`, if the number already exists, the behavior depends on the OSIS underlying implementation (usually overwrites or raises an error).
5. **Command mode**: When executing code in OSIS command mode, you can directly send Python code blocks. When executing in an IDE, ensure OSIS is running.

## More Resources

- [tests/](tests/): Example code for each module
- [templetes/](templetes/): Complete bridge modeling template projects
