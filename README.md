# pyosis

中交公路规划设计院自研OSIS桥隧分析平台的Python接口库`pyosis`

## Installation
由于`pyosis`存在重名，请您采用以下方式安装：
```bash
pip install osis-python
```
如果您的镜像站未同步`pyosis`，请使用以下命令：
```bash
pip install osis-python -i https://pypi.org/simple
```

## Usage

首先需要安装最新版OSIS(>=5.0)，并配置好python环境变量。pyosis需要python3.11版本以上的环境。并且，您需要在环境变量中设置`PYTHONHOME`为您python的安装目录，例如：`C:\Program Files\python`，设置`PYTHONIOENCODING`为`utf-8`。然后在`path`中分别添加`%PYTHONHOME%`和`%PYTHONHOME%\Scripts`两个条目。


您的脚本应放置于OSIS安装目录下的python文件夹中，例如：`C:\Program Files\osis\python`。假设存在一个名为`test_osis.py`的脚本，其内容如下：

```python
import json
from pyosis.core import osis_run    # 导入需要的功能
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

osis_section_circle(1, "圆形截面1", "CIRCLE", "Hollow", 0.219, 0.012)
osis_section_circle(2, "圆形截面2", "CIRCLE", "Hollow", 0.180, 0.008)
osis_section_circle(3, "圆形截面3", "CIRCLE", "Hollow", 0.114, 0.005)
osis_section_circle(4, "圆形截面4", "CIRCLE", "Hollow", 0.089, 0.004)
osis_section_circle(5, "圆形截面5", "CIRCLE", "Hollow", 0.045, 0.003)

osis_material_steel(1, "钢材1", "STEEL", "JTGD64_2015", "Q345", 0.05)

# 固定节点（x,y单位：m）
osis_node(1, 0, 5, 0)
osis_node(2, 15, 5, 0)
# 荷载作用节点
osis_node(3, 7.5, 0, 0)
osis_node(4, 20, 0, 0)

osis_element_beam3d(1, "BEAM3D", 1, 3, 1, 4, 4, 1, 1, 0.00, 0, 0.00, 0)
osis_element_beam3d(2, "BEAM3D", 2, 3, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)
osis_element_beam3d(3, "BEAM3D", 2, 4, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)
osis_element_beam3d(4, "BEAM3D", 3, 4, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)


osis_boundary_general(1, "GENERAL", "", 1, 1, 1, 1, 1, 1, 1)
osis_assign_boundary(1, "a", [1, 2])

osis_loadcase("自定义工况1", "USER", 1, "施加于节点3和4的两个力")
osis_load_nforce("NFORCE", "自定义工况1", 3, 0, -1000000, 0, 0, 0, 0)
osis_load_nforce("NFORCE", "自定义工况1", 4, 200000, 0, 0, 0, 0, 0)

osis_solve()

osis_run()      # 让OSIS执行所有前处理命令

isok, error, ef = osis_elem_force("自定义工况1", "EF", "BEAM3D")


def dict_to_json_txt(data, filename):
    """将字典以JSON格式写入文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    print(f"字典已写入文件: {filename}")

# 使用
dict_to_json_txt(ef, "output.json")
```

在OSIS中选择并运行这个脚本，如果一切正常的话，您将会看到OSIS开始了计算，并在`C:\Program Files\osis`下生成了一个名为`output.json`的文件，其中包含了OSIS计算内力的结果。
