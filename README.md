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
- **Solver-only mode** additionally requires the solver distribution that ships `PySolver.dll` (e.g. `D:\OSIS_Solver\Rbin64`).

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
sec = engine.section.create_circle("CircleSection", d=0.5, tw=0.02)

# Create materials
mat = engine.material.create_conc("C30Concrete", eCode="JTG3362_2018", eGrade="C30")

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

### 2. Engine Convenience Methods

`OSISEngine` provides project-level convenience methods:

```python
# Project management
engine.new_project()           # Create new project
engine.save_project()          # Save current project
engine.open_project(path)      # Open existing project

# Model information
summary = engine.model_summary()  # Returns dict with all manager counts

# Import/Export
engine.export_apdl(path)       # Export to APDL format
engine.import_apdl(path)       # Import from APDL format

# Result output for calculation book
engine.output_result_for_calc_book()

# Matrix output
engine.matrix("matrix_1", [[1, 2],[3, 4]])
```

### 3. Using Managers Directly

If you don't need the convenience methods of Engine, you can also import individual managers directly:

```python
from pyosis.material import material_manager
from pyosis.node import node_manager

mat = material_manager.create_conc("C30", eCode="JTG3362_2018", eGrade="C30")
node = node_manager.create(0, 0, 0)
```

### 4. Using OSISSolver — Start the Solver Directly (Solver-Only Mode)

By default, `OSISEngine()` connects to an already-running OSIS GUI process. If you want to drive the solver **without opening the GUI** (e.g. for headless batch runs, CI, or server-side automation), use `OSISSolver` to load the solver DLL directly via ctypes and launch its HTTP server:

```python
from pyosis.core.solver import OSISSolver
from pyosis.core.engine import OSISEngine

# Load <install>/PySolver.dll and start the HTTP server (default port 18080)
solver = OSISSolver(osis_install_path=r"D:\OSIS_Solver\Rbin64")
engine = OSISEngine.from_solver(solver)

# Create a project (type 101 = bridge analysis), then build the model as usual
engine.project.create(101, r"D:\work\my_bridge\my_bridge.sis")
engine.control.set_gravity_acceleration(9.8066)
# ... build sections / materials / nodes / elements ...
engine.solve()
```

Notes on solver-only mode:

- `osis_install_path` must be the directory containing `PySolver.dll` (and its dependency DLLs).
- The solver needs a project to exist before model commands run: call `engine.project.create()` / `open()` first.
- Crash minidumps are written to `<install>\Error\dmp\` (created on startup).

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
| GeometryManager | `engine.geometry` | Geometric entities (splines, spatial curves) |
| PropertyManager | `engine.prop` | Properties (coordinate systems, creep/shrinkage, damping, P-U curves, element thickness assignments) |
| ThicknessManager | `engine.thickness` | Shell thickness properties |
| LoadCaseManager | `engine.load` | Load cases |
| StageManager | `engine.stage` | Construction stages |
| TendonManager | `engine.tendon` | Tendons (properties + shapes) |
| LiveManager | `engine.live` | Live loads (grades + lanes + cases) |
| SettlementManager | `engine.settlement` | Settlement analysis |
| StabilityManager | `engine.stability` | Stability analysis |
| DynamicManager | `engine.dynamic` | Dynamic analysis |
| PostManager | `engine.post` | Post-processing (load combinations, design checks) |
| ResultManager | `engine.result` | Result export (load case / envelope / check results) |
| ControlManager | `engine.control` | Global control parameters |
| ProjectManager | `engine.project` | Project operations |
| DisplayManager | `engine.display` | Display control (show/hide boundaries, loads, tendons; view orientation; display switches) |

### Sub-Managers

Some managers contain sub-managers, accessed via attributes:

```python
# Element groups
grp = engine.element.group.create("MainGirderElements")
grp.add([1, 2, 3])

# Boundary groups
bg = engine.boundary.group.create("AbutmentBoundaries")
bg.add([1, 2])

# Various boundary types
engine.boundary.create_general(bX=1, bY=1, bZ=1, bRX=1, bRY=1, bRZ=1)  # General support
engine.boundary.create_master_slave(nMast=1, nSlav=2, dDir=1)           # Master-slave
engine.boundary.create_release(nElem=1, iReleaseEnd=2)                  # End release
engine.boundary.create_elstcspt(nNode=1, dK=[1e9, 1e9, 1e9, 0, 0, 0])  # Elastic support
engine.boundary.create_general_elstcspt(nNode=1, bX=1, bY=1, bZ=1, dKx=1e9, dKy=1e9, dKz=1e9)  # General elastic
engine.boundary.create_rigid(nNode1=1, nNode2=2)                        # Rigid link
engine.boundary.create_section_factor(nElem=1, iEnd=1)                  # Section factor

# Tendons
prop = engine.tendon.prop.create_in(
    "15-10", mat_no=1, e_code="GBT5224_2014",
    diameter=15.2, n_num=10, d_pipe=0.09
)
shape = engine.tendon.shape.create_arc3d(
    "N1", n_num=2, prop="15-10",
    element_group="MainGirderElements", curve_name="curve1"
)

# Live loads
grade = engine.live.grade.create("HighwayClassI")
lane = engine.live.lane.create("Lane1")
case = engine.live.case.create("LiveLoadCase 1")
```

### Display Control

```python
# Show/hide boundaries, loads and tendons
engine.display.disp_ctrl("bc", "all", "all", 1)          # Show all boundaries
engine.display.disp_ctrl("lg", "nforce", "all", 0)       # Hide all concentrated forces
engine.display.disp_ctrl("td", "all", ["T1", "T2"], 1)   # Show specific tendons

# View orientation
engine.display.set_view("top")          # standard / top / right / front

# Display switch
engine.display.set_plsm(1)              # 0 = off, 1 = on
```

### Property & Thickness Management

```python
# Coordinate systems
engine.prop.coord.create_local("CS1", origin=[0, 0, 0], x_axis=[1, 0, 0], y_axis=[0, 1, 0])

# Creep and shrinkage
engine.prop.creep_shrink.create("Creep1", eCode="JTG3362_2018", eGrade="C30")

# Damping
engine.prop.damping.create("Damping1", dDmp=0.05)

# P-U curve (for soil-structure interaction)
engine.prop.pu_curve.create("PU1", data=[(0, 0), (0.01, 1000), (0.02, 1500)])

# Element thickness assignment
engine.prop.thickness.assign_element(nElem=1, dThick=0.3)

# Shell thickness properties
engine.thickness.create_uniform("Thick1", dThick=0.3)
engine.thickness.create_tapered("Thick2", dThick1=0.2, dThick2=0.4)
```

### Geometry Queries

The `GeometryManager` supports querying geometric entities:

```python
# Get all splines
splines = engine.geometry.all("spline")

# Get a specific spline
spline = engine.geometry.get("spline", name="curve1")

# Filter by type
arcs = engine.geometry.filter("spline", spline_type="ARC3D")
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
sec = engine.section.create_circle("Section1", d=0.5)

# Explicit number
sec = engine.section.create_circle("Section1", d=0.5, no=100)
```

## Result Export

After solving, you can export various analysis results using `engine.result`. All export methods return pandas DataFrames:

```python
# Export load case results (element forces)
df = engine.result.loadcase("Self-weight", "LCEF")

# Export envelope results (element forces)
df = engine.result.env("BasicCombinationEnvelope", "EnvEF")

# Export design check results
df = engine.result.check(
    "混凝土", "正截面抗弯验算", "基本组合"
)

# Batch export all check results from Check folder
results = engine.result.check_all()
for name, df in results.items():
    print(f"{name}: {len(df)} rows")
```

Supported result types:
- **Load case**: `LCEF` (element force), `LCED` (element displacement), `LCND` (node displacement), `LCBF` (boundary reaction), `LCTL` (tendon loss), `LCS` (element stress)
- **Envelope**: `EnvBF` (boundary reaction), `EnvEF` (element force), `EnvES` (element strain), `EnvS` (element stress), `EnvND` (node displacement)

Requires `pandas` to be installed: `python -m install pandas`

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
engine.section.create_circle("CircleSection1", d=0.219, tw=0.012, no=1)
engine.section.create_circle("CircleSection2", d=0.180, tw=0.008, no=2)

# Materials
engine.material.create_steel(
    "Steel1", eCode="JTGD64_2015", eGrade="Q345", dDmp=0.05, no=1
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
    "CustomLoadCase1",
    load_case_type="USER",
    prompt="Two forces applied at nodes 3 and 4"
)
lc.create_nforce(3, dFx=0, dFy=-1000000, dFz=0)
lc.create_nforce(4, dFx=200000, dFy=0, dFz=0)

# Solve
engine.solve()
```

## End-to-End Demo

See [`tests/pyosis_demo.py`](tests/pyosis_demo.py) for a runnable end-to-end example that:

- Starts the solver directly via `OSISSolver` (no GUI required)
- Builds the 25m 简支小箱梁 example model (10 prep modules)
- Runs `engine.solve()`
- Exports LCND / LCEF / EnvND / EnvEF results to CSV

The demo reuses the prep modules from `tests/output/output_py/25m简支小箱梁中梁-solveronly/`, so it serves both as a smoke test and a copy-paste template.
