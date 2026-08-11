"""沉降分析管理器 - 统一管理沉降工况和沉降组

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 无状态设计，每次从服务端加载（与 element/boundary manager 一致）

子管理器：
- group: SettlementGroupManager - 沉降组
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from ..core.client import osis_client
from .interface import (
    osis_setl_grp,
    osis_setl_grp_del,
    osis_setl_grp_mod,
    osis_setl_anal,
    osis_setl_anal_del,
    osis_setl_anal_mod,
    osis_setl_anal_inc,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class SettlementGroup:
    """沉降组对象

    由 SettlementGroupManager 内部创建，用户不应直接实例化。
    """
    name: str                                                       # 组名
    setl: float                                                     # 沉降数值
    nodes: list[int] = field(default_factory=list)                  # 施加沉降的节点列表
    related_settlements: list[str] = field(default_factory=list)    # 关联的沉降工况名称列表

    @classmethod
    def _from_dict(cls, d: dict) -> SettlementGroup:
        """从接口 dict 构造 SettlementGroup 对象（内部使用）"""
        return cls(
            name=d.get("name"),
            setl=d.get("setl"),
            nodes=list(d.get("nodes", [])),
            related_settlements=list(d.get("relatedSettlements", [])),
        )

    def __repr__(self) -> str:
        return f"SettlementGroup(name={self.name!r}, setl={self.setl}, nodes={self.nodes})"


@dataclass(frozen=False)
class Settlement:
    """沉降工况对象

    由 SettlementManager 内部创建，用户不应直接实例化。
    """
    no: int                             # 编号
    name: str                           # 名称
    analysis_type: int                  # 分析类型
    related_stages: list[int] = field(default_factory=list)     # 关联的施工阶段编号列表
    related_stage_count: int = 0        # 关联施工阶段数量
    setl_grp_nos: list[str] = field(default_factory=list)       # 沉降组名称列表
    setl_grp_count: int = 0             # 沉降组数量
    # groups: list[SettlementGroup] = field(default_factory=list)  # 沉降组详细列表

    @classmethod
    def _from_dict(cls, d: dict) -> Settlement:
        """从接口 dict 构造 Settlement 对象（内部使用）"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            analysis_type=d.get("analysisType"),
            related_stages=d.get("relatedStages") or [],
            related_stage_count=d.get("relatedStageCount"),
            setl_grp_nos=d.get("setlGrpNO") or [],
            setl_grp_count=d.get("setlGrpCount"),
            # groups=[SettlementGroup._from_dict(g) for g in d.get("groups", []) if isinstance(g, dict)],
        )

    def _sync_from_dict(self, d: dict) -> None:
        """用接口返回的 dict 同步当前对象属性（内部使用）"""
        self.no = d.get("no")
        self.name = d.get("name")
        self.analysis_type = d.get("analysisType")
        self.related_stages = d.get("relatedStages") or []
        self.related_stage_count = d.get("relatedStageCount")
        self.setl_grp_nos = d.get("setlGrpNO") or []
        self.setl_grp_count = d.get("setlGrpCount")
        # self.groups = [SettlementGroup._from_dict(g) for g in d.get("groups", []) if isinstance(g, dict)]

    def refresh(self) -> Settlement:
        """从服务端刷新当前沉降工况数据并同步到对象属性

        Returns:
            刷新后的 Settlement 对象（链式调用）

        Raises:
            RuntimeError: 刷新失败时抛出异常
        """
        resp = osis_client("GetSettlementInfoByNames", {"name": [self.name]})
        if not resp['success']:
            raise RuntimeError(f"刷新沉降工况 {self.name} 失败: {resp['error']}")
        data = resp.get("data", [])
        if data and data[0]:
            self._sync_from_dict(data[0])
        return self

    def include(self, op:Literal["a", "r"], *group_names: str) -> Settlement:
        """向当前沉降工况添加或移除沉降组

        Args:
            op (str): 操作类型，"a"=添加，"r"=移除
            *group_names (str): 一个或多个沉降组名称

        Returns:
            更新后的 Settlement 对象（链式调用）

        Examples:
            >>> s = settlement_manager.get("S1")
            >>> s.include("a", "N1", "N2")  # 向 S1 添加沉降组 N1, N2
            >>> s.include("r", "N1")        # 从 S1 移除沉降组 N1

        Notes:
            - 使用前需先通过 create() 创建沉降荷载工况
        """
        if not group_names:
            return self
        ok, err = osis_setl_anal_inc(self.name, op, *group_names)
        if not ok:
            raise RuntimeError(f"添加沉降组到工况 {self.name} 失败: {err}")
        return self.refresh()

    def remove(self, *group_names: str) -> Settlement:
        """从当前沉降工况移除一个或多个沉降组

        Args:
            *group_names (str): 一个或多个沉降组名称

        Returns:
            更新后的 Settlement 对象（链式调用）
        """
        if not group_names:
            return self
        ok, err = osis_setl_anal_inc(self.name, "r", *group_names)
        if not ok:
            raise RuntimeError(f"从工况 {self.name} 移除沉降组失败: {err}")
        return self.refresh()

    def __repr__(self) -> str:
        return f"Settlement(name={self.name!r}, groups={self.setl_grp_count})"


# ──────────────────────────────────────────────
# SettlementGroupManager
# ──────────────────────────────────────────────


class SettlementGroupManager:
    """沉降组管理器

    统一管理沉降组的创建、删除和查询。由 SettlementManager 持有，不单独导出。

    用法:
        >>> from pyosis.settlement import settlement_manager
        >>> sg = settlement_manager.group.create("N1", -0.001, 1, 2, 3)
        >>> sg = settlement_manager.group.get("N1")
        >>> settlement_manager.group.delete("N1")
    """

    def _load(self) -> list[SettlementGroup]:
        """从服务端加载所有沉降组信息"""
        resp = osis_client("GetAllSetlGrpInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        groups = [
            SettlementGroup._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return groups

    def create(
        self,
        name: str,
        val: float,
        *nodes: int,
    ) -> SettlementGroup:
        """创建或修改沉降组

        Args:
            name (str): 组名
            val (float): 沉降量
            *nodes (int): 沉降节点列表，创建时必须指定至少一个节点

        Returns:
            返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

        Examples:
            >>> # 创建包含节点 1, 2 的沉降组
            >>> sg = settlement_manager.group.create("N1", -0.001, 1, 2)
            >>> # 修改沉降组为只包含节点 1（相当于删除节点 2）
            >>> sg = settlement_manager.group.create("N1", -0.001, 1)

        Notes:
            - 创建时必须指定节点，不能仅指定名称和沉降量
            - 重复使用同名组会修改现有沉降组
        """
        ok, err = osis_setl_grp(name, val, *nodes)
        if not ok:
            raise RuntimeError(f"创建沉降组 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除沉降组

        Args:
            name (str): 组名

        Returns:
            返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
        """
        ok, err = osis_setl_grp_del(name)
        if not ok:
            raise RuntimeError(f"删除沉降组 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        """修改沉降组名称

        Args:
            old_name (str): 旧名称
            new_name (str): 新名称

        Returns:
            返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
        """
        ok, err = osis_setl_grp_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"修改沉降组名称 {old_name} -> {new_name} 失败: {err}")

    def get(self, name: str | list[str]) -> SettlementGroup | list[SettlementGroup | None] | None:
        """根据名称获取单个或多个沉降组

        Args:
            name (str | list[str]): 沉降组名称，支持单个名称或名称列表

        Returns:
            SettlementGroup | list[SettlementGroup | None] | None:
                单个 SettlementGroup 对象；如果传入列表则返回对象列表；
                不存在返回 None

        Raises:
            RuntimeError: 查询失败时抛出异常
        """
        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")

        resp = osis_client("GetSetlGrpInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")

        groups = [SettlementGroup._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(groups) == 0:
            return None
        elif len(groups) == 1:
            return groups[0]
        return groups

    def all(self) -> list[SettlementGroup]:
        """获取所有沉降组"""
        return self._load()

    def count(self) -> int:
        """获取沉降组总数"""
        return len(self._load())

    def clear(self)->None:
        """清空所有沉降组"""
        try:
            [self.delete(sg.name) for sg in self.all()]
        except Exception as e:
            raise Exception(f"清空所有沉降组失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return f"SettlementGroupManager()"


# ──────────────────────────────────────────────
# SettlementManager
# ──────────────────────────────────────────────


class SettlementManager:
    """沉降工况管理器

    统一管理沉降荷载工况的创建、删除、修改和查询。

    用法:
        >>> from pyosis.settlement import settlement_manager
        >>> s = settlement_manager.create("S1")
        >>> s = settlement_manager.get("S1")
        >>> # 沉降组操作
        >>> sg = settlement_manager.group.create("N1", -0.001, 1, 2, 3)
        >>> s.include("N1")
        >>> settlement_manager.delete("S1")
    """

    def __init__(self) -> None:
        self._group_manager = SettlementGroupManager()

    @property
    def group(self) -> SettlementGroupManager:
        """沉降组管理器"""
        return self._group_manager

    def _load(self) -> list[Settlement]:
        """从服务端加载所有沉降工况信息"""
        resp = osis_client("GetAllSettlementInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        settlements = [
            Settlement._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return settlements

    def create(self, name: str) -> Settlement:
        """创建沉降荷载工况

        Args:
            name (str): 沉降荷载工况名称

        Returns:
            返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
        """
        ok, err = osis_setl_anal(name)
        if not ok:
            raise RuntimeError(f"创建沉降荷载工况 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除沉降荷载工况

        Args:
            name (str): 沉降荷载工况名称

        Returns:
            返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
        """
        ok, err = osis_setl_anal_del(name)
        if not ok:
            raise RuntimeError(f"删除沉降荷载工况 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        """修改沉降荷载工况名称

        Args:
            old_name (str): 旧名称
            new_name (str): 新名称

        Returns:
            返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
        """
        ok, err = osis_setl_anal_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"修改沉降荷载工况名称 {old_name} -> {new_name} 失败: {err}")

    def get(self, name: str | list[str]) -> Settlement | list[Settlement | None] | None:
        """根据名称获取单个或多个沉降工况

        Args:
            name (str | list[str]): 沉降荷载工况名称，支持单个名称或名称列表

        Returns:
            Settlement | list[Settlement | None] | None:
                单个 Settlement 对象；如果传入列表则返回对象列表；
                不存在返回 None

        Raises:
            RuntimeError: 查询失败时抛出异常
        """

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")

        resp = osis_client("GetSettlementInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")

        settlements = [Settlement._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(settlements) == 0:
            return None
        elif len(settlements) == 1:
            return settlements[0]
        return settlements

    def all(self) -> list[Settlement]:
        """获取所有沉降工况"""
        return self._load()

    def count(self) -> int:
        """获取沉降工况总数"""
        return len(self._load())

    def clear(self) -> None:
        """清空所有沉降工况和沉降组"""
        try:
            [self.delete(s.name) for s in self.all()]
            self.group.clear()
        except Exception as e:
            raise Exception(f"清空沉降分析失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return f"SettlementManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

settlement_manager = SettlementManager()
