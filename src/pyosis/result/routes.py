"""求解结果查询 —— 唯一的取数入口

对应 HTTP 端点（优先从结果文件读,文件失败回落内存）:
- /GetAllNodeDisplacement、/GetNodeDisplacementByNames    节点位移
- /GetAllElementForce、/GetElementForceByNames            单元内力
- /GetAllElementStress、/GetElementStressByNames          单元应力
- /GetAllSupportReaction、/GetSupportReactionByNames      支座反力
- /GetAllTendonLoss、/GetTendonLossByNames                钢束损失
- /GetAllModal、/GetModalByNames                          模态
- /GetAllEnvelope{Displacement,Force,Stress,Reaction}     包络

这组端点由 PySolver 的 HttpRouteManager 注册,有头/无头两种模式服务的是同一份
路由表,因此这里的结果与界面模式无关。历史上另有一条 /output 命令流 + txt 导出的
路径,已废弃并隔离在 result.py/loadcase.py/env.py 中,待路由补齐后删除。

## 服务端返回的形状

每个工况一项::

    {"loadCase": "预应力", "source": "file",
     "columns": [{"name": "节点", "unit": 0}, {"name": "Ux", "unit": 1}, ...],
     "rows":    [[1, 0.0, ...], [2, -5.1e-06, ...]],
     "parts":   {"0": [[...]], ...}}          # 仅内力/应力有,按截面分块

**服务端不做列名翻译**:columns 里的 name 就是软件结果表的表头(中文),单位后缀
已剥掉。表头是显示文本,求解器会随模型和界面改它(同一张应力表在不同模型里叫过
"单元编号"也叫过"单元号"),所以翻译放在本模块的 _COLUMNS 里 —— 改名只要改一行
Python 重装,不用重编 DLL。认不出来的表头会告警,必需的列缺失会直接报错,不会
静默给出一张少列的表。

数值已在服务端按该列单位换算成工程单位(与软件导出 txt、界面显示一致)。unit 是
``yilEnumType::UnitType`` 的枚举值,仅作诊断,本模块不用。

source 是诊断信息而非稳定契约:同一次调用可能因结果文件是否落盘而在 file/memory
之间翻转,也可能缺失,不要用业务逻辑依赖它。
"""
from __future__ import annotations

import re
import warnings

import pandas as pd

from ..core.client import osis_client

# 编号类列:值可能是字符串,统一成整型,免得同一个键在两条路上类型不同
_ID_KEYS = frozenset({"no", "ele", "node", "sys"})


def _atoi(text: str) -> int:
    """取开头的整数,与 C 的 atoi 一致（"1)" → 1）"""
    m = re.match(r"[+-]?\d+", text)
    return int(m.group()) if m else 0


def _derive_stress(rows: list[dict]) -> None:
    """应力的两处派生列（就地改）

    - 单元号在表里是字符串,转整型
    - 位置形如 "I(1)"/"J(2)",由括号里的数推出节点号
    """
    for row in rows:
        if isinstance(row.get("ele"), str):
            row["ele"] = _atoi(row["ele"])
        pos = row.get("position") or ""
        bracket = pos.find("(")
        row["node"] = _atoi(pos[bracket + 1:]) if bracket >= 0 else 0


# 每个结果类型一张 表头 → 键 的表,外加必需的键。
# 只收实际见过的表头,不预先猜同义词 —— 猜错了会把另一个量悄悄映射成这个键。
# 求解器改了表头时按报错信息往这里加一行即可。
_COLUMNS: dict[str, dict[str, str]] = {
    "node_displacement": {
        "节点": "no",
        "Ux": "ux", "Uy": "uy", "Uz": "uz",
        "Rx": "rx", "Ry": "ry", "Rz": "rz", "Rw": "rw",
    },
    # 单元表里的「节点」是单元上的节点号,不是节点表的节点号
    "element_force": {
        "单元": "ele", "节点": "node",
        "Fx": "fx", "Fy": "fy", "Fz": "fz",
        "Mx": "mx", "My": "my", "Mz": "mz", "Mb": "mw",
    },
    "element_stress": {
        # 同一张表在别的模型里叫过「单元号/截面位置(节点)/Sx压/受拉/受压」,一并收着
        "单元编号": "ele", "单元号": "ele",
        "验算位置": "position", "截面位置": "position", "位置": "position",
        "应力点": "point",
        "SxFx": "sxFx", "SxMy": "sxMy", "SxMz": "sxMz",
        "Sx组合": "sxComp", "Sx压": "sxComp",
        "SyFy": "syFy", "SzFz": "szFz",
        "主拉": "tp", "主压": "cp", "受拉": "tp", "受压": "cp",
    },
    "support_reaction": {
        "节点": "no", "边界坐标系编号": "sys", "边界坐标系号": "sys",
        "Fx": "fx", "Fy": "fy", "Fz": "fz",
        "Mx": "mx", "My": "my", "Mz": "mz", "Mb": "mw",
    },
    "tendon_loss": {
        "钢束号": "tendon", "钢束名": "tendonName",
        "单元号": "ele", "单元": "ele",
        "位置": "position", "钢束线坐标": "coord",
        "有效预应力": "effP",
        "摩擦损失": "lostFriction", "锚具回缩损失": "lostAnchorage",
        "温差损失": "lostThermal", "弹性压缩损失": "lostElastic",
        "松弛损失": "lostRelax", "收缩徐变损失": "lostCreepShrink",
        "总损失": "lostTotal",
    },
    "modal": {
        "模态号": "mode", "振型编号": "mode",
        "周期": "period", "工程频率": "freq", "圆频率": "omega",
        "特征值": "eigenvalue",
    },
    "envelope_displacement": {
        "工况": "component", "工况名称": "component",
        "节点": "no",
        "Ux": "ux", "Uy": "uy", "Uz": "uz",
        "Rx": "rx", "Ry": "ry", "Rz": "rz", "Rw": "rw",
    },
    "envelope_force": {
        "工况": "component", "工况名称": "component",
        "单元": "ele", "节点": "node",
        "Fx": "fx", "Fy": "fy", "Fz": "fz",
        "Mx": "mx", "My": "my", "Mz": "mz", "Mb": "mw",
    },
    "envelope_stress": {
        "工况": "component", "工况名称": "component",
        "单元编号": "ele", "单元号": "ele",
        "验算位置": "position", "截面位置": "position", "位置": "position",
        "应力点": "point",
        "SxFx": "sxFx", "SxMy": "sxMy", "SxMz": "sxMz",
        "Sx组合": "sxComp", "Sx压": "sxComp",
        "SyFy": "syFy", "SzFz": "szFz",
        "主拉": "tp", "主压": "cp", "受拉": "tp", "受压": "cp",
    },
    # 包络反力的「工况」是极值方向(Min/Max),「边界」才是分量(1-Fx),
    # 与其它包络表「工况」放分量的叫法不同,所以键也不同
    "envelope_reaction": {
        "工况": "extreme", "边界": "component",
        "节点": "no", "边界坐标系编号": "sys", "边界坐标系号": "sys",
        "Fx": "fx", "Fy": "fy", "Fz": "fz",
        "Mx": "mx", "My": "my", "Mz": "mz", "Mb": "mw",
    },
}

# 每个结果类型必须出现的键。缺了就报错 —— 少一列的表比报错难查得多。
_REQUIRED: dict[str, tuple[str, ...]] = {
    "node_displacement": ("no", "ux", "uy", "uz", "rx", "ry", "rz", "rw"),
    "element_force": ("ele", "node", "fx", "fy", "fz", "mx", "my", "mz", "mw"),
    "element_stress": (
        "ele", "position", "point",
        "sxFx", "sxMy", "sxMz", "sxComp", "syFy", "szFz", "tp", "cp",
    ),
    "support_reaction": ("no", "sys", "fx", "fy", "fz", "mx", "my", "mz", "mw"),
    "tendon_loss": ("tendon", "tendonName", "ele", "effP", "lostTotal"),
    "modal": ("mode", "period", "freq", "omega", "eigenvalue"),
    "envelope_displacement": ("component", "no"),
    "envelope_force": ("component", "ele", "node"),
    "envelope_stress": ("component", "ele", "position"),
    "envelope_reaction": ("extreme", "component", "no", "sys"),
}

# 派生列:类型 → 在展平后对每行做的加工
_DERIVE = {"element_stress": _derive_stress}

# 包络四类各自的 (全部, 按名) 端点
_ENVELOPE_ENDPOINTS = {
    "displacement": ("GetAllEnvelopeDisplacement", "GetEnvelopeDisplacementByNames"),
    "force": ("GetAllEnvelopeForce", "GetEnvelopeForceByNames"),
    "stress": ("GetAllEnvelopeStress", "GetEnvelopeStressByNames"),
    "reaction": ("GetAllEnvelopeReaction", "GetEnvelopeReactionByNames"),
}


def _query_all(endpoint: str) -> list[dict]:
    resp = osis_client(endpoint, {})
    if not resp.get("success"):
        raise RuntimeError(f"{resp.get('error', endpoint + ' 失败')}")
    return [d for d in resp.get("data") or [] if isinstance(d, dict) and d]


def _query_by_names(
    endpoint: str, names: str | list[str], strict: bool = False
) -> list[dict]:
    if isinstance(names, str):
        names = [names]
    requested = [str(n) for n in names]
    resp = osis_client(endpoint, {"name": requested})
    if not resp.get("success"):
        raise RuntimeError(f"{resp.get('error', endpoint + ' 失败')}")

    # 服务端查不到的名字返回空对象（HttpRouteManager 的 ByNames 助手），过滤掉
    data = [d for d in resp.get("data") or [] if isinstance(d, dict) and d]

    # 名字写错、与「包络/并发名但服务端尚未支持」在这里表现完全一样:都是空结果。
    # 不出声的话用户只会拿到一张空表，无从判断是没数据还是名字不对。
    found = {d.get("loadCase") for d in data}
    missing = [n for n in requested if n not in found]
    if missing:
        msg = (
            f"{endpoint} 未返回这些名字的结果: {', '.join(missing)}。"
            f"可能是工况名不存在，也可能是包络/并发名而服务端尚未支持该查询。"
        )
        if strict:
            raise RuntimeError(msg)
        # 指向用户调用处:本函数 → get_* → *_df → ResultManager 的方法 → 用户，
        # 共 5 层。直接调本模块 get_* 时会上溯过头,但消息自带端点与名字,仍可读
        warnings.warn(msg, UserWarning, stacklevel=5)
    return data


# ═════════════════════════════════════════════
# 原始 dict 查询
# ═════════════════════════════════════════════

def get_node_displacement(
    name: str | list[str] | None = None, strict: bool = False
) -> list[dict]:
    """查询求解后节点位移

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        list[dict]: 每个工况 {"loadCase", "source", "columns", "rows"}
    """
    if name is None:
        return _query_all("GetAllNodeDisplacement")
    return _query_by_names("GetNodeDisplacementByNames", name, strict)


def get_element_force(
    name: str | list[str] | None = None, strict: bool = False
) -> list[dict]:
    """查询求解后单元内力

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        list[dict]: 每个工况 {"loadCase", "source", "columns", "rows", "parts"}
        parts 为按截面分块的行,与 rows 同列。
    """
    if name is None:
        return _query_all("GetAllElementForce")
    return _query_by_names("GetElementForceByNames", name, strict)


def get_support_reaction(
    name: str | list[str] | None = None, strict: bool = False
) -> list[dict]:
    """查询求解后支座反力

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        list[dict]: 每个工况 {"loadCase", "source", "columns", "rows"}
    """
    if name is None:
        return _query_all("GetAllSupportReaction")
    return _query_by_names("GetSupportReactionByNames", name, strict)


def get_element_stress(
    name: str | list[str] | None = None, strict: bool = False
) -> list[dict]:
    """查询求解后单元应力

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        list[dict]: 每个工况 {"loadCase", "source", "columns", "rows", "parts"}
        parts 为按截面分块的行,与 rows 同列。
    """
    if name is None:
        return _query_all("GetAllElementStress")
    return _query_by_names("GetElementStressByNames", name, strict)


def get_tendon_loss(
    name: str | list[str] | None = None, strict: bool = False
) -> list[dict]:
    """查询求解后钢束损失

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        list[dict]: 每个工况 {"loadCase", "source", "columns", "rows"}
    """
    if name is None:
        return _query_all("GetAllTendonLoss")
    return _query_by_names("GetTendonLossByNames", name, strict)


def get_modal(
    name: str | list[str] | None = None, strict: bool = False
) -> list[dict]:
    """查询模态结果

    Args:
        name: 模态结果名（形如 ``_自振模态_<阶段名>``）;None 时返回全部
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        list[dict]: 每份结果 {"name", "kind", "columns", "rows"}
        name 是模态结果名而非工况名,所以本函数没有 loadCase 键,
        按名查询时的不存在告警也不适用。
    """
    if name is None:
        return _query_all("GetAllModal")
    return _query_by_names("GetModalByNames", name, strict)


def get_envelope(
    name: str | list[str] | None = None,
    kind: str = "force",
    strict: bool = False,
) -> list[dict]:
    """查询包络结果

    Args:
        name: 包络名;None 时返回全部包络
        kind: displacement / force / stress / reaction
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        list[dict]: 每个包络 {"loadCase", "source", "columns", "rows"}
    """
    if kind not in _ENVELOPE_ENDPOINTS:
        raise ValueError(
            f"未知的包络类型 {kind!r}，可选: {', '.join(_ENVELOPE_ENDPOINTS)}"
        )
    all_ep, by_name_ep = _ENVELOPE_ENDPOINTS[kind]
    if name is None:
        return _query_all(all_ep)
    return _query_by_names(by_name_ep, name, strict)


# ═════════════════════════════════════════════
# 表头翻译 + DataFrame 展平
# ═════════════════════════════════════════════

def _translate(columns: list, kind: str) -> list[str]:
    """表头 → 英文键,并把必需列缺失报出来

    Args:
        columns: 服务端给的 [{"name", "unit"}, ...]
        kind: _COLUMNS 里的结果类型

    Raises:
        RuntimeError: 必需列缺失（多半是求解器改了表头）
    """
    aliases = _COLUMNS[kind]
    names = [c.get("name") if isinstance(c, dict) else str(c) for c in columns]
    keys = [aliases.get(n) for n in names]

    unknown = [n for n, k in zip(names, keys) if k is None]
    if unknown:
        warnings.warn(
            f"结果表里这些列没有对应的键，已跳过: {', '.join(unknown)}。"
            f"若是求解器改了表头，在 pyosis/result/routes.py 的 _COLUMNS"
            f"[{kind!r}] 里补一行即可。",
            UserWarning,
            stacklevel=5,
        )

    missing = [k for k in _REQUIRED[kind] if k not in keys]
    if missing:
        raise RuntimeError(
            f"{kind} 结果表缺少必需的列: {', '.join(missing)}。"
            f"服务端实际给出的表头是: {', '.join(names)}。"
            f"多半是求解器改了表头，在 pyosis/result/routes.py 的 _COLUMNS"
            f"[{kind!r}] 里对齐即可。"
        )
    return keys


def _rows_to_dicts(case: dict, kind: str) -> list[dict]:
    """一个工况的 rows（值数组）按 columns 翻成 [{键: 值}, ...]"""
    keys = _translate(case.get("columns") or [], kind)
    rows = []
    for values in case.get("rows") or []:
        row = {}
        for key, value in zip(keys, values):
            if key is None:
                continue
            if key in _ID_KEYS and isinstance(value, str):
                value = _atoi(value)
            row[key] = value
        rows.append(row)
    derive = _DERIVE.get(kind)
    if derive is not None:
        derive(rows)
    return rows


def _to_df(
    cases: list[dict], kind: str, rows_key: str = "rows"
) -> pd.DataFrame:
    """把 [{loadCase, source, columns, rows}, ...] 展平成单表

    行内附带 loadCase/source 两列,便于多工况合并分析。
    """
    rows = []
    for case in cases:
        meta = {"loadCase": case.get("loadCase"), "source": case.get("source")}
        for r in _rows_to_dicts(case, kind):
            rows.append({**meta, **r})
    return pd.DataFrame(rows)


def _by_part_df(cases: list[dict], kind: str) -> pd.DataFrame:
    """展平 parts（按截面分块）,额外带 part 列"""
    rows = []
    for case in cases:
        meta = {"loadCase": case.get("loadCase"), "source": case.get("source")}
        for part_id, part_rows in (case.get("parts") or {}).items():
            # parts 的行与 rows 同列,但只有列定义在主对象上
            part_case = {
                "columns": case.get("columns"),
                "rows": part_rows,
            }
            for r in _rows_to_dicts(part_case, kind):
                rows.append({**meta, "part": part_id, **r})
    return pd.DataFrame(rows)


def node_displacement_df(
    name: str | list[str] | None = None, strict: bool = False
) -> pd.DataFrame:
    """节点位移 DataFrame（列: loadCase, source, no, ux, uy, uz, rx, ry, rz, rw）"""
    return _to_df(get_node_displacement(name, strict), "node_displacement")


def element_force_df(
    name: str | list[str] | None = None, strict: bool = False
) -> pd.DataFrame:
    """单元内力 DataFrame（列: loadCase, source, ele, node, fx, fy, fz, mx, my, mz, mw）"""
    return _to_df(get_element_force(name, strict), "element_force")


def support_reaction_df(
    name: str | list[str] | None = None, strict: bool = False
) -> pd.DataFrame:
    """支座反力 DataFrame（列: loadCase, source, no, sys, fx, fy, fz, mx, my, mz, mw）"""
    return _to_df(get_support_reaction(name, strict), "support_reaction")


def element_stress_df(
    name: str | list[str] | None = None,
    by_part: bool = False,
    strict: bool = False,
) -> pd.DataFrame:
    """单元应力 DataFrame

    Args:
        name: 工况名（str 或 list[str]）;None 时返回全部工况
        by_part: False（默认）展平全截面 rows；True 展平 parts 并额外带 part 列
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        列: loadCase, source, [part,] ele, node, position, point,
            sxFx, sxMy, sxMz, sxComp, syFy, szFz, tp, cp
        node 不在服务端的表里,由 position（形如 "I(1)"）推出。
    """
    cases = get_element_stress(name, strict)
    if by_part:
        return _by_part_df(cases, "element_stress")
    return _to_df(cases, "element_stress")


def tendon_loss_df(
    name: str | list[str] | None = None, strict: bool = False
) -> pd.DataFrame:
    """钢束损失 DataFrame

    列: loadCase, source, tendon, tendonName, ele, position, coord, effP,
        lostFriction, lostAnchorage, lostThermal, lostElastic, lostRelax,
        lostCreepShrink, lostTotal
    """
    return _to_df(get_tendon_loss(name, strict), "tendon_loss")


def modal_df(
    name: str | list[str] | None = None, strict: bool = False
) -> pd.DataFrame:
    """模态 DataFrame（列: name, kind, mode, period, freq, omega, eigenvalue）

    注意第一列是模态结果名 ``name``,不是 ``loadCase`` —— 模态挂在阶段上,
    不按荷载工况组织。
    """
    cases = get_modal(name, strict)
    rows = []
    for case in cases:
        meta = {"name": case.get("name"), "kind": case.get("kind")}
        for r in _rows_to_dicts(case, "modal"):
            rows.append({**meta, **r})
    return pd.DataFrame(rows)


def envelope_df(
    name: str | list[str] | None = None,
    kind: str = "force",
    strict: bool = False,
) -> pd.DataFrame:
    """包络 DataFrame

    Args:
        name: 包络名;None 时返回全部
        kind: displacement / force / stress / reaction
        strict: 显式指定 name 却查不到时抛 RuntimeError（默认只告警）

    Returns:
        列随 kind 变: loadCase, source, component, ...（reaction 还有 extreme/no/sys）
        同一节点的各分量行数值相同 —— 软件自己的包络表就是这样:行按
        (节点, 分量) 分,值给的是各分量自身极值拼成的包络向量,分量列是标签。
    """
    return _to_df(get_envelope(name, kind, strict), f"envelope_{kind}")
