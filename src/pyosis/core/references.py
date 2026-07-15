"""
通用引用查询客户端封装

后端 C++ 暴露 /GetReferences 接口，根据 entityType 字符串分派
到对应 Info 类的 getRelated* 方法。
"""
from __future__ import annotations
from typing import Literal
from .client import osis_client
from .exceptions import DependencyError

# 支持的实体类型（与 C++ GetReferences.cpp 中的 if-else 分支对齐）
EntityType = Literal[
    "Material", "Section", "Node", "Element", "Boundary",
    "TendonShape", "TendonProp", "LoadCase", "LiveGrade", "LiveLane",
    "CoorSys", "CreepShrink", "PUCurve", "ShellThickness",
    "Damping", "Spline",
]


"""
通用引用查询客户端封装
后端 /GetReferences 统一字符串协议：{entityType, idKey("no"|"name"), idValue}
"""



def get_references(entity_type: str, *, no: int | None = None, name: str | None = None) -> dict[str, list]:
    """查询某个实体被哪些其他实体引用

    Args:
        entity_type: 实体类型，如 "Material" / "Node" / "TendonShape" / "LoadCase"
        no:  按编号寻址时传（Material/Section/Node/Element）
        name: 按名称寻址时传（TendonShape/LoadCase/...）
        no 与 name 二选一。

    Returns:
        引用关系字典，如 {"elements":[101,102], "loads":["自重"], ...}
        无依赖时返回空字典。

    Raises:
        ValueError: no/name 都没传，或都传了
        RuntimeError: 查询失败
    """
    if no is not None and name is not None:
        raise ValueError("no 与 name 只能传一个")
    if no is None and name is None:
        raise ValueError("必须提供 no 或 name")

    if no is not None:
        id_key, id_value = "no", str(no)
    else:
        id_key, id_value = "name", name

    resp = osis_client("GetReferences", {
        "entityType": entity_type,
        "idKey": id_key,
        "idValue": id_value,
    })
    if not resp.get("success"):
        raise RuntimeError(f"查询 {entity_type}({id_key}={id_value}) 引用失败: {resp.get('error')}")
    return resp.get("data") or {}


def raise_if_occupied(
    entity_type: str,
    deps: dict[str, list],
    *,
    no: int | None = None,
    name: str | None = None,
) -> None:
    """存在非空依赖时抛出 DependencyError。

    Args:
        entity_type: 实体类型，如 "Material" / "TendonShape"
        deps: get_references / get_dependencies 返回的依赖字典
        no: 按编号寻址时传
        name: 按名称寻址时传
    """
    non_empty = {k: v for k, v in deps.items() if v}
    if not non_empty:
        return
    if no is None and name is None:
        raise ValueError("必须提供 no 或 name")
    id_value = no if no is not None else name
    raise DependencyError(entity_type, id_value, non_empty)

