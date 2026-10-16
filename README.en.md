[English](README.en.md) | [简体中文](README.md)

# pyosis

Python client library for **OSIS** Bridge & Tunnel Analysis Platform (developed by CCCC Highway Consultants Co., Ltd.).

pyosis provides an object-oriented Python API for automating the creation of bridge/tunnel finite element models, executing analysis solvers, and extracting post-processing results.

## Installation

`pyosis` is taken on PyPI — the distribution name is `osis-python`:

```bash
pip install osis-python
```

If your mirror hasn't synced yet:

```bash
pip install osis-python -i https://pypi.org/simple
```

## Requirements

- OSIS >= 5.1 (short-form command names like `N`/`Ele`/`Sec` are accepted by both the converter and runtime)
- Python >= 3.8
- pandas (result export)
- **Solver-only mode** additionally requires the solver distribution that ships `osisSdk.dll` (e.g. `D:\OSIS_Solver\Rbin64`)

> `osis_init` needs a license file (`osis.lic`, HMAC-signed) before anything runs. Search order: the `OSIS_LICENSE_FILE` environment variable, then `%ProgramData%\OSIS\osis.lic`, then `osis.lic` in the install directory. Obtain one from your OSIS vendor.

## Quick Start

`OSISEngine` is the core facade class of pyosis, integrating all module managers and providing a unified project-level entry point. This snippet builds a model, solves it, and reads a result in one go:

```python
from pyosis.core.engine import OSISEngine

engine = OSISEngine()      # connects to an already-running OSIS GUI process
engine.clear()

engine.control.set_gravity_acceleration(9.8066)
engine.control.set_calc_tendon(True)
engine.control.set_calc_creep(True)

# Sections / materials
sec = engine.section.create_circle(no=1, name="CircleSection", d=0.5)
mat = engine.material.create_conc(no=1, name="C30Concrete", code="JTG3362_2018", grade="C30")

# Nodes / elements
n1 = engine.node.create(no=1, x=0, y=0, z=0)
n2 = engine.node.create(no=2, x=15, y=0, z=0)
elem = engine.element.create_beam3d(
    no=1, node1=n1.no, node2=n2.no, mat=mat.no, sec1=sec.no, sec2=sec.no
)

# Boundaries
bd = engine.boundary.create_general(no=1, x=1, y=1, z=1, rx=1, ry=1, rz=1, rw=1)
bd.assign("a", [n1.no])

# Load case
lc = engine.load.create("Self-weight", load_case_type="D")
lc.create_gravity()

# Solve
engine.solve()

# Read a result
df = engine.result.node_displacement("Self-weight")
```

### Solver-Only Mode (No GUI)

To drive the solver **without opening the GUI** (headless batch runs, CI, server-side automation), `OSISSolver` loads the solver DLL via ctypes and launches its HTTP server:

```python
from pyosis.core.solver import OSISSolver
from pyosis.core.engine import OSISEngine

# Load <install>/osisSdk.dll and start the HTTP server (default port 18080)
solver = OSISSolver(osis_install_path=r"D:\OSIS_Solver\Rbin64")
engine = OSISEngine.from_solver(solver)

# Create a project (type 101 = bridge analysis), then build the model as usual
engine.project.create(101, r"D:\work\my_bridge\my_bridge.sis")
engine.control.set_gravity_acceleration(9.8066)
# ... build sections / materials / nodes / elements ...
engine.solve()
```

Notes:

- `osis_install_path` must be the directory containing `osisSdk.dll` (and its dependency DLLs).
- With `port=0` the OS assigns a free port, written back to `solver.port`.
- The solver needs a project to exist before model commands run: call `engine.project.create()` / `open()` first.
- Crash minidumps are written to `<install>\Error\dmp\`.

### Other Entry Points

`OSISEngine` also carries a set of project-level convenience methods:

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

You can also bypass the Engine convenience methods and import individual managers directly:

```python
from pyosis.material import material_manager
from pyosis.node import node_manager

mat = material_manager.create_conc(no=1, name="C30", code="JTG3362_2018", grade="C30")
node = node_manager.create(no=None, x=0, y=0, z=0)
```

## Core Concepts

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
| ControlManager | `engine.control` | Global control parameters |
| ProjectManager | `engine.project` | Project operations |
| DisplayManager | `engine.display` | Display control (show/hide boundaries, loads, tendons; view orientation; display switches) |
| ResultManager | `engine.result` | Result export (load case / envelope / check results) |
| PostManager | `engine.post` | Post-processing (load combinations, design checks) |

### Data Class Objects

Create and query operations return data class objects (dataclass) instead of raw dictionaries:

```python
elem = engine.element.get(1)
print(elem.no)          # ID
print(elem.node_vec)    # Node list
print(elem.mat)         # Material ID

# Objects support operations (operations sink down to the object)
lc = engine.load.get("Self-weight")
lc.create_gravity()
lc.create_nforce(1, fx=1000)
```

### Enums

All type codes live in `pyosis.core.enums`. Each member's **name is the OSIS command-stream
spelling**, so a member converts straight to a string; its value is the integer code the
interface JSON carries:

```python
from pyosis.core.enums import SectionType

SectionType.Rectangle.value      # 5              — code as sent by OSIS
str(SectionType.Rectangle)       # "Rectangle"    — command-stream spelling
SectionType.name_of(5)           # "Rectangle"
SectionType.of(404)              # SectionType.Unassigned — unknown code falls back
```

## Modelling

### Sub-Managers

Some managers contain sub-managers, accessed via attributes:

```python
# Element groups (create + add elements in one call)
engine.element.group.create("MainGirderElements", "c")            # create empty group
engine.element.group.create("MainGirderElements", "a", "1to3")    # add elements 1-3

# Boundary groups
engine.boundary.group.create("AbutmentBoundaries", "c")
engine.boundary.group.create("AbutmentBoundaries", "a", "1to2")

# Various boundary types
engine.boundary.create_general(no=1, x=1, y=1, z=1, rx=1, ry=1, rz=1, rw=1)           # General support
engine.boundary.create_master_slave(no=1, node=1, dx=1, dy=1, dz=1, rx=0, ry=1, rz=1, coincident=1)  # Master-slave
engine.boundary.create_rigid(no=1, node_i=1)                                               # Rigid link
engine.boundary.create_elstcspt(no=1, coor="", x=0, dx=1e9, y=0, dy=1e9, z=0, dz=1e9)     # Elastic support

# Tendons
prop = engine.tendon.prop.create_in(
    name="15-10", mat=3, code="GBT5224_2014",
    diameter=15.2, num=10, pipe=0.09,
)
shape = engine.tendon.shape.create_arc3d(
    name="N1", n_num=2, prop="15-10",
    element_group="MainGirderElements", curve_name="curve1"
)

# Live loads: grade -> lane -> case
engine.live.grade.create_highway("HighwayClassI", code="JTGD60_2015", live_load_type="HIGHWAY_I")
engine.live.lane.create_ve("Lane1", length=19.1, wheel=1.8, orientation=1,
                           ref=0, ref_elems="MainGirderElements", offset_y=0.0, offset_z=0.0)
lc = engine.live.case.create("LaneLoadEnvelope", code="JTGD60_2015", sub_cmb_type=1)
lc.create_sub("LaneLoadCase1", "HighwayClassI", scalar=0.75, calc_mu=True,
              bridge_type="CUSTOM", mu_params=[6.586960], lane_names=["Lane1"])
```

### Properties & Thickness

```python
# Coordinate systems (three-point definition)
engine.prop.coord.create_three_point(
    no=1, p1x=0, p1y=0, p1z=0,
    p2x=1, p2y=0, p2z=0,
    p3x=0, p3y=1, p3z=0,
)

# Creep and shrinkage (no, name, code, fcuk, avg_humidity,
#                      component_approximate_size, type_coeff, birth_by_shrinking, fly_ash_ratio)
engine.prop.creep_shrink.create(no=1, name="Creep1", avg_humidity=70.0,
                                type_coeff=5.0, birth_by_shrinking=3)

# Damping (Rayleigh coefficients)
engine.prop.damping.create_rayleigh_custom(name="Damping1", alpha=0.05, beta=0.005)

# P-U curve (no, name, curve_type, num, *values)
#   curve_type: 0 = force, 1 = moment
#   values interleave by point, 2*num of them: (disp, force) (disp, force) ...
engine.prop.pu_curve.create(1, "PU1", 1, 2, 0.0, 0.0, 0.02, 1500.0)

# Element thickness assignment (thickness, op, *elems)
engine.prop.assign_component_thickness(0.3, "a", 1)

# Shell thickness (no, is_uniform, in_plane, out_plane, ...)
engine.thickness.create(no=1, is_uniform=0, in_plane=0.3, out_plane=0.3)
```

### Geometry Queries

```python
# Get all splines
splines = engine.geometry.all()

# Get a specific spline
spline = engine.geometry.get("curve1")

# Filter by type
arcs = [s for s in engine.geometry.all() if s.spline_type is SplineType.ARC3D]
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

## Result Export

After solving, query analysis results through `engine.result`. All methods return pandas DataFrames.

Results go through PySolver's HTTP routes (`/GetAll*`, `/Get*ByNames`); GUI and headless modes read the same data, so no mode distinction is needed:

```python
# Node displacement (omit name to get every load case)
df = engine.result.node_displacement("Self-weight")

# Element forces
df = engine.result.element_force("Self-weight")

# Element stresses (by_part=True splits by section, adding a part column)
df = engine.result.element_stress("Self-weight", by_part=True)

# Support reactions
df = engine.result.support_reaction("Self-weight")

# Tendon (prestress) losses
df = engine.result.tendon_loss("Self-weight")

# Modal results (eigenvalues / periods / frequencies). Modal hangs off construction
# stages, not load cases; the result name looks like _自振模态_<stage> and the first
# column is `name`, not `loadCase`
df = engine.result.modal()

# Envelopes: kind is displacement / force / stress / reaction
df = engine.result.envelope("BasicCombinationEnvelope", kind="force")
```

`name` accepts a single load case name or a list of names. When a name resolves to nothing you get an empty table plus a `UserWarning` — a misspelled name and a name that simply has no such result are indistinguishable. Pass `strict=True` to raise instead:

```python
df = engine.result.element_force("no-such-case", strict=True)   # raises RuntimeError
```

Envelope rows are keyed by (node, component) and each row carries the envelope vector built from every component's own extreme — rows for different components at the same node hold identical values, and the component column is a label. `kind="reaction"` additionally carries `extreme` (Min/Max) and `sys` (boundary coordinate system number) columns.

### Where column names come from

The server does **not** translate column names: it passes through the software result table's headers (Chinese) and the values as-is. The mapping into English keys such as `ux`/`sxFx` lives on the pyosis side, in `src/pyosis/result/routes.py`.

So when the solver team renames a header, you edit one line of Python and reinstall. Two ways it can mismatch:

- An unrecognized column → `UserWarning` naming it, that column is skipped, the rest is fine
- A required column gone unrecognized → `RuntimeError`, printing every header the server actually sent; add one line to `_COLUMNS` to match

### Design Check Results

Design check results have no HTTP route yet and still go through the `/output` command stream:

```python
df = engine.result.check("混凝土", "正截面抗弯验算", "基本组合")

# Batch export all check results from Check folder
results = engine.result.check_all()
for name, df in results.items():
    print(f"{name}: {len(df)} rows")
```

### Migrating from 0.8.1

`loadcase()` / `env()` have been **removed** — no compatibility aliases remain. Replace them type by type:

| Old | New |
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

`loadcase`'s `LCED` (element displacement) and `env`'s `EnvES` (element strain) have no corresponding route and were dropped along with them. **Column names change too**: the old interfaces returned txt headers such as `Fx(N)`, the new ones return the route's English keys such as `fx`.

## Batch Execution & Performance

The main cost of building large models is OSIS initializing its command execution function for every single command. Wrap the modelling code in `with batch():` to merge **all** OSIS commands into a **single** `OSIS_Run` HTTP request when the block exits:

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

Notes:

- Nested `with batch():` is supported — the inner exit does not flush; only the outermost exit does.
- Intermediate reads (`get`, `all`) auto-flush the buffer first, so the data they return is correct.
- If the block raises, the commands buffered since `__enter__` are discarded and the original exception is re-raised.
- `flush()` can be called inside the block to force an early flush.
- `next_no()` (auto-numbering) raises inside `batch()` because it would need to query the server mid-batch; pass `no=...` explicitly, or run auto-numbering outside the batch.

Benchmark on the `25m简支小箱梁中梁` project: without `batch()` ~3000 round-trips; with `batch()` 3 (clear + clc + one final flush).

### Chained Method Calls

The dataclass returned by `get()` supports method chaining without server round-trips:

```python
with batch():
    lc = engine.load.create("Self-weight", load_case_type="D")
    lc.create_gravity()
    lc.create_nforce(node=1, fx=0, fy=-1000, fz=0)
    # ↑ all three commands are queued; the OSIS_Run request only fires at exit
```

Accessing identity attributes (`lc.no`, `lc.name`) does not touch the server. Accessing data fields (`lc.type`, `lc.elements`) materializes the object (one-time flush + query), then caches it.

## .out → pyosis Converter

pyosis ships a converter that turns an OSIS command stream (`.out`) into a runnable pyosis project:

```bash
python src/pyosis/transfer/out_to_python.py path/to/model.out path/to/output_project
```

> The `/OSIS_Run` command-stream splitter does not strip `//` line comments — a comment line is merged with the command that follows it into one bad command. The converter strips comments before sending; if you build a raw `.out` payload yourself, pre-process the file or use `osis_run()` through the generated `main.py`.

Generated layout:

```
output_project/
└── prep/
    ├── main.py          # Entry point (batch mode, runs all 10 modules)
    ├── _1_control.py    # Global control parameters
    ├── _2_property.py   # Geometry / coordinate / damping / creep properties
    ├── _3_material.py   # Materials
    ├── _4_section.py    # Sections (incl. mesh)
    ├── _5_node.py       # Nodes
    ├── _6_element.py    # Elements
    ├── _7_boundary.py   # Boundaries
    ├── _8_loadcase.py   # Load cases
    ├── _9_analysis.py   # Analysis settings (settlement / live / dynamic / stability)
    └── _10_stage.py     # Construction stages
```

Run it:

```bash
cd output_project
python prep/main.py            # build the model
python prep/main.py --solve    # build + solve
```

Notes on the converter:

- Both long-form command names (`Node`, `Element`, `Section`, `Material`, `LoadCase`, `Boundary`, `Stage`) and OSIS 5.1 short-form aliases (`N`, `Ele`, `Sec`/`SecOff`/`SecMesh`, `Mat`, `LC`, `Bd`, `Stg`) are recognized and normalized.
- `SectionMesh` is emitted with the new `Index, PartID, MeshMethod, MeshSize` layout (Section 7.3.6.2) — `PartID = 1` for concrete sections, `2` for templated composite sections.
- `Spline3D` is dispatched to `engine.geometry.create_general` / `create_natural` / `create_arc2d` / `create_arc3d` based on the type field.
- Commands that are not yet modeled are passed through verbatim via `engine.run(...)` so the model still runs; rewrite them into pyosis calls manually if needed.

## Complete Modelling Example

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
engine.section.create_circle(no=1, name="CircleSection1", d=0.219, tw=0.012)
engine.section.create_circle(no=2, name="CircleSection2", d=0.180, tw=0.008)

# Materials
engine.material.create_steel(
    no=2, name="Steel1", code="JTGD64_2015", grade="Q345", dmp=0.05
)

# Nodes
engine.node.create(no=1, x=0, y=5, z=0)
engine.node.create(no=2, x=15, y=5, z=0)
engine.node.create(no=3, x=7.5, y=0, z=0)
engine.node.create(no=4, x=20, y=0, z=0)

# Elements
engine.element.create_beam3d(no=1, node1=1, node2=3, mat=1, sec1=1, sec2=1)
engine.element.create_beam3d(no=2, node1=2, node2=3, mat=1, sec1=2, sec2=2)

# Boundaries
engine.boundary.create_general(no=1)
engine.boundary.get(1).assign("a", [1, 2])

# Loads
lc = engine.load.create(
    "CustomLoadCase1",
    load_case_type="USER",
    prompt="Two forces applied at nodes 3 and 4"
)
lc.create_nforce(3, fx=0, fy=-1000000, fz=0)
lc.create_nforce(4, fx=200000, fy=0, fz=0)

# Solve
engine.solve()
```

## End-to-End Demos

**Solver-only mode**: see [`tests/pyosis_demo.py`](tests/pyosis_demo.py) for a self-contained runnable example that:

- Starts the solver directly via `OSISSolver` (no GUI required)
- Builds the 25m 简支小箱梁 example model (10 prep modules)
- Runs `engine.solve()`
- Exports node displacement / element force / support reaction / tendon loss / modal / all four envelope families to CSV

Output goes to `temp/demo_output/` at the repository root (`temp/` is not tracked by git).

**GUI mode**: the single-file demo [`tests/demo_gui.py`](tests/demo_gui.py) is a merged version of the project generated from `temp/xiaoxiangliang.out`. Run it against an open OSIS 5.1+ GUI:

```bash
python tests/demo_gui.py            # build the model
python tests/demo_gui.py --solve    # build + solve
```

The file contains the engine setup, all 10 `build_*` functions (control / property / material / section / node / element / boundary / loadcase / analysis / stage), and a `build_model()` driver that wraps everything in `with batch():` — so ~250 commands hit OSIS in a single `OSIS_Run` request.

To regenerate both the single-file demo and the multi-module project:

```bash
python temp/_merge_demo_gui.py                                                        # -> tests/demo_gui.py
python src/pyosis/transfer/out_to_python.py temp/xiaoxiangliang.out temp/output_py/xiaoxiangliang
```
