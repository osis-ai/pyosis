"""求解后结果的无头查询

对应 HTTP 端点（优先从结果文件读,文件失败回落内存）:
- /GetAllNodeDisplacement、/GetNodeDisplacementByNames   节点位移
- /GetAllElementForce、/GetElementForceByNames           单元内力
- /GetAllElementStress、/GetElementStressByNames         单元应力
- /GetAllSupportReaction、/GetSupportReactionByNames     支座反力

与 loadcase/env 走 OSIS_Run 命令流 + txt 导出的路径不同,这组端点
直接读求解器结果,无需 GUI 参与,适合无头批量提取。

除 /GetAllElementStress 外,每个工况返回:
    {"loadCase": 工况名, "source": "file"|"memory",
     "nodes": [...] / "elements": [...]}
单元应力额外带 "parts": {"<partId>": [应力点…]}（按截面分块）。
"""
from __future__ import annotations

from ..core.client import osis_client

try:
    import pandas as pd
    _HAS_PANDAS = True
except ImportError:
    _HAS_PANDAS = False


def _query_all(endpoint: str) -> list[dict]:
    resp = osis_client(endpoint, {})
    if not resp.get("success"):
        raise RuntimeError(f"{resp.get('error', endpoint + ' 失败')}")
    return [d for d in resp.get("data") or [] if isinstance(d, dict) and d]


def _query_by_names(endpoint: str, names: str | list[str]) -> list[dict]:
    if isinstance(names, str):
        names = [names]
    resp = osis_client(endpoint, {"name": [str(n) for n in names]})
    if not resp.get("success"):
        raise RuntimeError(f"{resp.get('error', endpoint + ' 失败')}")
    # C++ 端查不到的工况返回空对象,过滤掉
    return [d for d in resp.get("data") or [] if isinstance(d, dict) and d]


# ═════════════════════════════════════════════
# 原始 dict 查询
# ═════════════════════════════════════════════

def get_node_displacement(name: str | list[str] | None = None) -> list[dict]:
    """查询求解后节点位移

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况

    Returns:
        list[dict]: 每个工况 {"loadCase", "source", "nodes": [{no, ux..rz, rw}]}
    """
    if name is None:
        return _query_all("GetAllNodeDisplacement")
    return _query_by_names("GetNodeDisplacementByNames", name)


def get_element_force(name: str | list[str] | None = None) -> list[dict]:
    """查询求解后单元内力

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况

    Returns:
        list[dict]: 每个工况 {"loadCase", "source",
                     "elements": [{ele, node, fx..mz, mw}]}
    """
    if name is None:
        return _query_all("GetAllElementForce")
    return _query_by_names("GetElementForceByNames", name)


def get_support_reaction(name: str | list[str] | None = None) -> list[dict]:
    """查询求解后支座反力

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况

    Returns:
        list[dict]: 每个工况 {"loadCase", "source",
                     "nodes": [{no, sys, fx..mz, mw}]}
    """
    if name is None:
        return _query_all("GetAllSupportReaction")
    return _query_by_names("GetSupportReactionByNames", name)


def get_element_stress(name: str | list[str] | None = None) -> list[dict]:
    """查询求解后单元应力

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况

    Returns:
        list[dict]: 每个工况 {"loadCase", "source",
                     "points": [{ele, node, position, point,
                                 sxFx, sxMy, sxMz, sxComp, syFy, szFz, tp, cp}],
                     "parts": {"<partId>": [同上 point 行]}}
        parts 为按截面分块的应力点，points 是全截面合并表。
    """
    if name is None:
        return _query_all("GetAllElementStress")
    return _query_by_names("GetElementStressByNames", name)


# ═════════════════════════════════════════════
# DataFrame 展平
# ═════════════════════════════════════════════

def _flatten(cases: list[dict], rows_key: str) -> "pd.DataFrame":
    """把 [{loadCase, source, rows_key: [...]}, ...] 展平成单表。

    行内附带 loadCase/source 两列,便于多工况合并分析。
    """
    if not _HAS_PANDAS:
        raise ImportError("结果导出功能依赖 pandas，请先安装：pip install pandas")
    rows = []
    for case in cases:
        meta = {"loadCase": case.get("loadCase"), "source": case.get("source")}
        for r in case.get(rows_key) or []:
            rows.append({**meta, **r})
    return pd.DataFrame(rows)


def node_displacement_df(name: str | list[str] | None = None) -> "pd.DataFrame":
    """节点位移 DataFrame（列: loadCase, source, no, ux, uy, uz, rx, ry, rz, rw）"""
    return _flatten(get_node_displacement(name), "nodes")


def element_force_df(name: str | list[str] | None = None) -> "pd.DataFrame":
    """单元内力 DataFrame（列: loadCase, source, ele, node, fx, fy, fz, mx, my, mz, mw）"""
    return _flatten(get_element_force(name), "elements")


def support_reaction_df(name: str | list[str] | None = None) -> "pd.DataFrame":
    """支座反力 DataFrame（列: loadCase, source, no, sys, fx, fy, fz, mx, my, mz, mw）"""
    return _flatten(get_support_reaction(name), "nodes")


def element_stress_df(
    name: str | list[str] | None = None,
    by_part: bool = False,
) -> "pd.DataFrame":
    """单元应力 DataFrame

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况
        by_part: False（默认）展平全截面 points；True 展平 parts 并额外带 part 列

    Returns:
        列: loadCase, source, [part,] ele, node, position, point,
            sxFx, sxMy, sxMz, sxComp, syFy, szFz, tp, cp
    """
    if not _HAS_PANDAS:
        raise ImportError("结果导出功能依赖 pandas，请先安装：pip install pandas")
    cases = get_element_stress(name)
    rows = []
    for case in cases:
        meta = {"loadCase": case.get("loadCase"), "source": case.get("source")}
        if by_part:
            for part_id, pts in (case.get("parts") or {}).items():
                for r in pts or []:
                    rows.append({**meta, "part": part_id, **r})
        else:
            for r in case.get("points") or []:
                rows.append({**meta, **r})
    return pd.DataFrame(rows)
