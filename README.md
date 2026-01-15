[简体中文](README.zh-CN.md) | [English](README.md)

# pyosis

Python client library for OSIS Bridge Analysis Platform

## Installation

Due to naming conflicts on PyPI, please install using:

```bash
pip install osis-python
```

If your mirror hasn't synced yet, use:

```bash
pip install osis-python -i https://pypi.org/simple
```

## Usage

First, install the latest version of OSIS (>=5.0) and configure the Python environment variables. pyosis requires Python 3.11 or higher. You need to set PYTHONHOME in the environment variables to your Python installation directory, e.g., C:\Program Files\python, and set PYTHONIOENCODING to utf-8. Then add %PYTHONHOME% and %PYTHONHOME%\Scripts to the Path variable.

Your scripts should be placed in the python folder under the OSIS installation directory, e.g., C:\Program Files\osis\python. Suppose there is a script named test_osis.py with the following content:


```python
import json
from pyosis.core import osis_run    # Import required functions
from pyosis.control import *
from pyosis.general import *
from pyosis.section import *
from pyosis.material import *
from pyosis.node import *
from pyosis.element import *
from pyosis.boundary import *
from pyosis.load import *
from pyosis.post import *

osis_clear()

osis_acel(9.8066)
osis_calc_tendon(1)
osis_calc_con_force(1)
osis_calc_shrink(1)
osis_calc_creep(1)
osis_calc_shear(1)
osis_calc_rlx(1)
osis_mod_loc_coor(0)
osis_inc_tendon(1)
osis_nl(0, 0)
osis_ln_srch(0)
osis_auto_ts(0)
osis_mod_opt(0)

osis_section_circle(1, "Circle Section 1", "CIRCLE", "Hollow", 0.219, 0.012)
osis_section_circle(2, "Circle Section 2", "CIRCLE", "Hollow", 0.180, 0.008)
osis_section_circle(3, "Circle Section 3", "CIRCLE", "Hollow", 0.114, 0.005)
osis_section_circle(4, "Circle Section 4", "CIRCLE", "Hollow", 0.089, 0.004)
osis_section_circle(5, "Circle Section 5", "CIRCLE", "Hollow", 0.045, 0.003)

osis_material_steel(1, "Steel 1", "STEEL", "JTGD64_2015", "Q345", 0.05)

# Fixed nodes (x, y units: m)
osis_node(1, 0, 5, 0)
osis_node(2, 15, 5, 0)
# Load application nodes
osis_node(3, 7.5, 0, 0)
osis_node(4, 20, 0, 0)

osis_element_beam3d(1, "BEAM3D", 1, 3, 1, 4, 4, 1, 1, 0.00, 0, 0.00, 0)
osis_element_beam3d(2, "BEAM3D", 2, 3, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)
osis_element_beam3d(3, "BEAM3D", 2, 4, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)
osis_element_beam3d(4, "BEAM3D", 3, 4, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)

osis_boundary_general(1, "GENERAL", "", 1, 1, 1, 1, 1, 1, 1)
osis_assign_boundary(1, "a", [1, 2])

osis_loadcase("Custom Load Case 1", "USER", 1, "Two forces applied at nodes 3 and 4")
osis_load_nforce("NFORCE", "Custom Load Case 1", 3, 0, -1000000, 0, 0, 0, 0)
osis_load_nforce("NFORCE", "Custom Load Case 1", 4, 200000, 0, 0, 0, 0, 0)

osis_solve()

osis_run()      # Let OSIS execute all preprocessing commands

isok, error, ef = osis_elem_force("Custom Load Case 1", "EF", "BEAM3D")

def dict_to_json_txt(data, filename):
    """Write dictionary to file in JSON format"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    print(f"Dictionary written to file: {filename}")

# Usage
dict_to_json_txt(ef, "output.json")
```

Select and run this script in OSIS. If everything is normal, you will see OSIS start the calculation and generate a file named output.json in C:\Program Files\osis, containing the internal force results from OSIS. (Not yet completed)
