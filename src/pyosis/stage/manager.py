"""施工阶段管理器 - 统一管理施工阶段的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护施工阶段列表，通过 get 等方法查询，不暴露 HTTP 接口细节
"""

from __future__ import annotations

import uuid

from dataclasses import dataclass, field
from typing import Literal

from ..core.client import osis_client
from .overall import (
    stage,
    stage_del,
    stage_insert,
    stage_remove,
)
from .define import (
    stage_element,
    stage_boundary,
    stage_loadcase,
    stage_analysis,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class ElementGroup:
    """单元组"""
    name: str = ""
    birth: float = 0.0
    part: int = 0


@dataclass(frozen=True)
class BoundaryGroup:
    """边界组"""
    name: str = ""
    position: str = ""


@dataclass(frozen=True)
class LoadCase:
    """荷载工况"""
    name: str = ""


@dataclass(frozen=True)
class AnalysisCase:
    """分析工况"""
    name: str = ""


@dataclass(frozen=True)
class Stage:
    """施工阶段对象

    由 StageManager 内部创建，用户不应直接实例化。
    """

    no: int
    name: str = ""
    duration: float = 0.0
    accumulation: float = 0.0
    pre_stage_no: int = -1
    element_groups: list[ElementGroup] = field(default_factory=list)
    boundary_groups: list[BoundaryGroup] = field(default_factory=list)
    load_cases: list[LoadCase] = field(default_factory=list)
    analysis_cases: list[AnalysisCase] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict) -> Stage:
        """从接口 dict 构造 Stage 对象（内部使用）"""
        element_groups = [
            ElementGroup(
                name=e.get("name", ""),
                birth=e.get("birth", 0.0),
                part=e.get("part", 0),
            )
            for e in d.get("elementGroups", []) if isinstance(e, dict)
        ]
        boundary_groups = [
            BoundaryGroup(
                name=b.get("name", ""),
                position=b.get("position", ""),
            )
            for b in d.get("boundaryGroups", []) if isinstance(b, dict)
        ]
        load_cases = [
            LoadCase(name=lc.get("name", ""))
            for lc in d.get("loadCases", []) if isinstance(lc, dict)
        ]
        analysis_cases = [
            AnalysisCase(name=a.get("name", ""))
            for a in d.get("analysisCases", []) if isinstance(a, dict)
        ]
        return cls(
            no=d.get("no", 0),
            name=d.get("name", ""),
            duration=d.get("duration", 0.0),
            accumulation=d.get("accumulation", 0.0),
            pre_stage_no=d.get("preStageNo", -1),
            element_groups=element_groups,
            boundary_groups=boundary_groups,
            load_cases=load_cases,
            analysis_cases=analysis_cases,
        )


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class StageManager:
    """施工阶段管理器

    统一管理施工阶段的创建、删除、修改和查询。

    用法:
        >>> from pyosis.stage import stage_manager
        >>> stg = stage_manager.create(3.0)                                 # 创建施工阶段（编号名称自动生成）
        >>> stg = stage_manager.create(3.0, name="墩身施工")                 # 创建施工阶段（指定名称）
        >>> stage_manager.activate_element(stg.no, "墩", 5.0)               # 激活单元
        >>> stage_manager.deactivate_element(stg.no, "墩")                 # 钝化单元
        >>> stage_manager.activate_boundary(stg.no, "固结")                  # 激活边界
        >>> stage_manager.deactivate_boundary(stg.no, "固结")                # 钝化边界
        >>> stage_manager.activate_loadcase(stg.no, "", "自定义工况1")      # 激活荷载工况
        >>> stage_manager.deactivate_loadcase(stg.no, "", "自定义工况1")    # 钝化荷载工况
        >>> stage_manager.activate_analysis(stg.no, "MODAL")               # 激活分析工况
        >>> stg2 = stage_manager.get(stg.no)                                # 按编号查询
        >>> all_stgs = stage_manager.all()                                  # 获取全部阶段
        >>> stage_manager.delete(stg.no)                                    # 删除阶段
        >>> stg3 = stage_manager.insert(stg.no, 1, 3.0)                    # 插入阶段（编号名称自动生成）
    """

    def __init__(self) -> None:
        self._stages: list[Stage] = []
        self._stage_map: dict[int, Stage] = {}  # 按编号索引：O(1) 查询
        self._loaded: bool = False

    def _reload_get_as(self, no: int, expected_cls: type[Stage], what: str) -> Stage:
        """创建/修改后从服务端重载并返回指定类型对象（内部使用）。"""
        self._loaded = False
        self._load()
        stg = self._stage_map.get(no)
        if stg is None:
            raise RuntimeError(f"{what} {no} 成功但无法从服务端获取完整信息")
        if not isinstance(stg, expected_cls):
            raise RuntimeError(f"{what} {no} 成功但返回类型错误: {type(stg)}")
        return stg

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有施工阶段信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetStageInfo", {})
        if isinstance(resp, tuple):
            raise RuntimeError(f"加载施工阶段信息失败: {resp[1]}")
        self._stages = [
            Stage._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "no" in d
        ]

        # 构建索引：编号 -> 施工阶段对象 (O(1) 查询)
        self._stage_map = {stg.no: stg for stg in self._stages}

        self._loaded = True

    def refresh(self) -> None:
        """强制刷新缓存（模型变更后自动调用，也可手动调用）"""
        self._stages = []
        self._stage_map = {}
        self._loaded = False
        self._load()

    def _next_no(self) -> int:
        """生成下一个可用施工阶段编号

        取已有阶段编号的最大值+1，如果没有阶段则从1开始。
        """
        self._load()
        if not self._stages:
            return 1
        return max(stg.no for stg in self._stages) + 1

    # ── 增删改 ────────────────────────────────

    def create(
        self,
        duration: int,
        no: int | None = None,
        name: str | None = None,
    ) -> Stage:
        """创建施工阶段

        Args:
            duration: 持续时间（天）
            no: 阶段编号，不指定时自动生成（取最大编号+1）
            name: 施工阶段名称，不指定时自动生成（格式为"ST_{uuid}"）

        Returns:
            创建的施工阶段对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        self.refresh()
        if no is None:
            no = self._next_no()
        if name is None:
            name = f"ST_{uuid.uuid4().hex[:12]}"
        ok, err = stage(no, name, duration)
        if not ok:
            raise RuntimeError(f"创建施工阶段 {no} 失败: {err}")
        return self._reload_get_as(no, Stage, "创建施工阶段")

    def delete(self, no: int) -> None:
        """删除施工阶段

        Args:
            no: 阶段编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = stage_del(no)
        if not ok:
            raise RuntimeError(f"删除施工阶段 {no} 失败: {err}")
        self._loaded = False

    def insert(
        self,
        ref_no: int,
        position: Literal[0, 1],
        duration: float,
        no: int | None = None,
        name: str | None = None,
    ) -> Stage:
        """插入施工阶段

        Args:
            ref_no: 参考位置编号
            position: 0=前插，1=后插
            duration: 持续时间（天）
            no: 阶段编号，不指定时自动生成（取最大编号+1）
            name: 所插入的施工阶段名称，不指定时自动生成（格式为"ST_{uuid}"）

        Returns:
            创建的施工阶段对象

        Raises:
            RuntimeError: 插入失败时抛出异常
        """
        self.refresh()
        if no is None:
            no = self._next_no()
        if name is None:
            name = f"ST_{uuid.uuid4().hex[:12]}"
        ok, err = stage_insert(ref_no, position, name, duration)
        if not ok:
            raise RuntimeError(f"在 {ref_no} 处插入施工阶段失败: {err}")
        return self._reload_get_as(no, Stage, "插入施工阶段")

    def remove(self, no: int) -> None:
        """移除插入的施工阶段

        Args:
            no: 阶段编号

        Raises:
            RuntimeError: 移除失败时抛出异常
        """
        ok, err = stage_remove(no)
        if not ok:
            raise RuntimeError(f"移除施工阶段 {no} 失败: {err}")
        self._loaded = False

    def activate_element(
        self,
        no: int,
        ele_group_name: str,
        birth: float = None,
        part: Literal[0, 1, 2] = None,
    ) -> None:
        """通过单元组激活单元

        Args:
            no: 施工阶段编号
            ele_group_name: 单元组名称
            birth: 龄期
            part: 组合结构分部；缺省为 0
                0 = 全部激活
                1 = 仅钢材部分
                2 = 仅混凝土部分

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        if part is None:
            part = 0
        ok, err = stage_element(no, 1, 1, ele_group_name, birth, part)
        if not ok:
            raise RuntimeError(f"阶段 {no} 激活单元组 {ele_group_name} 失败: {err}")
        self._loaded = False

    def deactivate_element(
        self,
        no: int,
        ele_group_name: str,
    ) -> None:
        """通过单元组钝化单元

        Args:
            no: 施工阶段编号
            ele_group_name: 单元组名称

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = stage_element(no, 0, 0, ele_group_name, None, None)
        if not ok:
            raise RuntimeError(f"阶段 {no} 钝化单元组 {ele_group_name} 失败: {err}")
        self._loaded = False

    def activate_boundary(
        self,
        no: int,
        bd_group_name: str,
    ) -> None:
        """通过边界组激活边界

        Args:
            no: 施工阶段编号
            bd_group_name: 边界组名称

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = stage_boundary(no, 1, 1, bd_group_name)
        if not ok:
            raise RuntimeError(f"阶段 {no} 激活边界组 {bd_group_name} 失败: {err}")
        self._loaded = False

    def deactivate_boundary(
        self,
        no: int,
        bd_group_name: str,
    ) -> None:
        """通过边界组钝化边界

        Args:
            no: 施工阶段编号
            bd_group_name: 边界组名称

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = stage_boundary(no, 0, 0, bd_group_name)
        if not ok:
            raise RuntimeError(f"阶段 {no} 钝化边界组 {bd_group_name} 失败: {err}")
        self._loaded = False

    def activate_loadcase(
        self,
        no: int,
        ref_lc_name: str,
        lc_name: str,
    ) -> None:
        """激活荷载工况

        Args:
            no: 施工阶段编号
            ref_lc_name: 参考当前施工阶段内的工况名称
            lc_name: 待激活的荷载工况名称

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = stage_loadcase(no, 1, 1, ref_lc_name, lc_name)
        if not ok:
            raise RuntimeError(f"阶段 {no} 激活荷载工况 {lc_name} 失败: {err}")
        self._loaded = False

    def deactivate_loadcase(
        self,
        no: int,
        ref_lc_name: str,
        lc_name: str,
    ) -> None:
        """钝化荷载工况

        Args:
            no: 施工阶段编号
            ref_lc_name: 参考当前施工阶段内的工况名称
            lc_name: 待钝化的荷载工况名称

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = stage_loadcase(no, 0, 0, ref_lc_name, lc_name)
        if not ok:
            raise RuntimeError(f"阶段 {no} 钝化荷载工况 {lc_name} 失败: {err}")
        self._loaded = False

    def activate_analysis(
        self,
        no: int,
        eType: Literal["MODAL", "SETL", "RSPEC", "LIVE", "BUCKLE"],
        lc_name: str = None,
    ) -> None:
        """激活分析工况

        Args:
            no: 施工阶段编号
            eType: 分析类型
                MODAL = 模态分析
                SETL = 沉降分析
                RSPEC = 反应谱
                LIVE = 活载分析
                BUCKLE = 屈曲分析
            lc_name: 荷载工况名称（部分分析类型需要）

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        if lc_name is None:
            lc_name = ""
        ok, err = stage_analysis(no, 1, eType, lc_name)
        if not ok:
            raise RuntimeError(f"阶段 {no} 激活分析工况 {eType} 失败: {err}")
        self._loaded = False

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Stage | list[Stage | None]:
        """根据编号获取单个或多个施工阶段 (O(k))

        Args:
            no: 施工阶段编号

        Returns:
            Stage 对象或数组；阶段不存在返回 None
        """
        self._load()
        if isinstance(no, int):
            return self._stage_map.get(no)
        elif isinstance(no, list):
            return [self._stage_map.get(n) for n in no]
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")

    def all(self) -> list[Stage]:
        """获取所有施工阶段

        Returns:
            全部阶段列表
        """
        self._load()
        return list(self._stages)

    def count(self) -> int:
        """获取施工阶段总数

        Returns:
            阶段数量
        """
        self._load()
        return len(self._stages)

    def __repr__(self) -> str:
        self._load()
        return f"StageManager(count={len(self._stages)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

stage_manager = StageManager()
