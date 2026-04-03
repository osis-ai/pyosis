"""
Interfaces of OSIS functions

========

荷载组合相关

"""
from typing import Literal
from ..core import REGISTRY


# ──────────────────────────────────────────────
# 类型定义
# ──────────────────────────────────────────────

SheetType = Literal["General", "Concrete", "Steel", "Composite"]

ActivateType = Literal[
    "Activate", "Inactivate", "Basic", "Accidental", "Seismic",
    "Frequent", "Quasipermanent", "Standard",
    "Concreted1", "Concreted2", "ConcretePre1", "ConcretePre2",
    "SteelD", "SteelPre", "CompositeD", "CompositePre"
]

OperationType = Literal["ADD", "OR", "ABS", "SRSS"]

LCOrEnv = Literal["LC", "Env"]


# ──────────────────────────────────────────────
# OSIS 接口
# ──────────────────────────────────────────────


@REGISTRY.register("Combine")
def osis_combine_create(
    name: str,
    lc_or_env: LCOrEnv,
    operation_type: OperationType,
    activate_type: ActivateType,
    sheet_type: SheetType,
    prompt: str = "",
) -> tuple[bool, str]:
    """创建荷载组合

    Args:
        name (str): 组合名称
        lc_or_env (str): LC=工况, Env=包络
        operation_type (str): ADD/OR/ABS/SRSS
        activate_type (str): 激活类型
        sheet_type (str): 表单类型
        prompt (str): 说明

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("CombineDel")
def osis_combine_del(name: str) -> tuple[bool, str]:
    """删除荷载组合

    Args:
        name (str): 组合名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("CombineMod")
def osis_combine_mod(
    old_name: str,
    new_name: str = None,
    activate_type: ActivateType = None,
) -> tuple[bool, str]:
    """修改荷载组合

    Args:
        old_name (str): 旧名称
        new_name (str): 新名称
        activate_type (str): 激活类型

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass