"""
pyosis.core 的 Docstring
--------

OSISEngine中的函数，将会分发到各个模块，被再次封装，意图为：
- 避免麻烦的OSISEngine::GetInstance().OSIS_XXX调用方式
- 将各个模块分类开以实现逻辑清晰
- 将函数命名格式转换成python的常用格式，便于人与AI的理解
"""

from .command import REGISTRY, osis_run, set_run_mode
from .client import set_osis_port, set_osis_url
from .batch import batch, flush, batch_state, BatchError
from .basic_manager import BasicManager, LazyRef
from .exceptions import DependencyError
from .references import get_references, raise_if_occupied
from .sdk import health, sdk_version, list_commands, instance_info
from .enums import (
    OsisEnum,
    ElementType, BoundaryType, MaterialType, MaterialCode,
    SectionType, LoadCaseType, SplineType, TensionType,
    element_type_name, boundary_type_name, material_type_name,
    material_code_name, section_type_name, loadcase_type_name,
    DOF_NAMES, constraints_to_dict,
)
from .normalize import as_no, as_name
