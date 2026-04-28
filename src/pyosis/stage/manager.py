"""施工阶段管理器 - 统一管理施工阶段的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 无状态设计，每次从服务端加载（与 element/boundary manager 一致）
- 单元组、边界组、荷载工况、分析工况列表仅保留名称
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from ..core.client import osis_client
from .overall import (
    osis_stage,
    osis_stage_del,
    osis_stage_insert,
    osis_stage_remove,
)
from .define import (
    osis_stage_element,
    osis_stage_boundary,
    osis_stage_loadcase,
    osis_stage_analysis,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Stage:
    """施工阶段对象

    由 StageManager 内部创建，用户不应直接实例化。
    单元组、边界组、荷载工况、分析工况列表仅保留名称。
    """

    no: int
    name: str
    duration: float
    accumulation: float
    pre_stage_no: int
    element_groups: list[str] = field(default_factory=list)
    boundary_groups: list[str] = field(default_factory=list)
    load_cases: list[str] = field(default_factory=list)
    analysis_cases: list[str] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict) -> Stage:
        """从接口 dict 构造 Stage 对象（内部使用）"""
        element_groups = [
            e.get("name")
            for e in d.get("elementGroups", [])
            if isinstance(e, dict) and "name" in e
        ]
        boundary_groups = [
            b.get("name")
            for b in d.get("boundaryGroups", [])
            if isinstance(b, dict) and "name" in b
        ]
        load_cases = [
            lc.get("lcName")
            for lc in d.get("loadCases", [])
            if isinstance(lc, dict) and "lcName" in lc
        ]
        analysis_cases = [
            a.get("analName")
            for a in d.get("analysisCases", [])
            if isinstance(a, dict) and "analName" in a
        ]
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            duration=d.get("duration"),
            accumulation=d.get("accumulation"),
            pre_stage_no=d.get("preStageNo"),
            element_groups=element_groups,
            boundary_groups=boundary_groups,
            load_cases=load_cases,
            analysis_cases=analysis_cases,
        )

    def define_element(
        self,
        eOP: Literal[1, 0], 
        eType: Literal[1, 0], 
        strGroupName: str, 
        nBirth: int | None = None, 
        ePart: Literal[0, 1, 2]=None
    ) -> None:
        """通过单元组激活/钝化单元

        Args:
            eOP (int): 操作
                * 1 = 添加
                * 0 = 移除
            eType (int): 
                * 1 = 激活
                * 0 = 钝化
            strGroupName (str): 待操作的单元组名称
            nBirth (int): 龄期。eOP = 0 时需要设置为 None
            ePart (int): 组合结构的分部，可缺省（None）
                * 0 = 全部激活
                * 1 = 仅钢材部分
                * 2 = 仅混凝土部分

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_stage_element(self.no, eOP, eType, strGroupName, nBirth, ePart)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 定义单元组 {strGroupName} 失败: {err}")

    def define_boundary(
        self,
        eOP: Literal[1, 0], 
        eType: Literal[1, 0], 
        strGroupName: str
    ) -> None:
        """通过边界组激活/钝化边界

        Args:
            eOP (int): 操作
                * 1 = 添加
                * 0 = 移除
            eType (int): 
                * 1 = 激活
                * 0 = 钝化
            strGroupName (str): 待操作的边界组名称
            
        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_stage_boundary(self.no, eOP, eType, strGroupName)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 定义边界组 {strGroupName} 失败: {err}")

    def define_loadcase(
        self,
        eOP: Literal[1, 0], 
        eType: Literal[1, 0], 
        ref_lc_name: str, 
        lc_name: str
    ) -> None:
        """激活/钝化荷载工况

        Args:
            eOP (int): 操作
                * 1 = 添加
                * 0 = 移除
            eType (int): 
                * 1 = 激活
                * 0 = 钝化
            ref_lc_name (str): 参考当前施工阶段内的工况名称
            lc_name (str): 待操作的荷载工况名称
            
        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_stage_loadcase(self.no, eOP, eType, ref_lc_name, lc_name)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 激活荷载工况 {lc_name} 失败: {err}")

    def define_analysis(
        self,
        eOP: Literal[1, 0], 
        eType: Literal["MODAL", "SETL", "RSPEC", "LIVE", "BUCKLE"],
        lc_name: str,
    ) -> None:
        """激活分析工况,分析工况默认在每个施工阶段的静力工况之后，不同分析工况无先后顺序

        Args:
            eOP (int): 操作
                * 1 = 添加
                * 0 = 移除
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
        ok, err = osis_stage_analysis(self.no, eOP, eType, lc_name)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 激活分析工况 {eType} 失败: {err}")


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class StageManager:
    """施工阶段管理器

    统一管理施工阶段的创建、删除、修改和查询。

    用法:
        >>> from pyosis.stage import stage_manager
        >>> stg = stage_manager.create(1, "阶段1", 3)                       # 创建施工阶段
        >>> stg = stage_manager.get(1)                                      # 按编号查询
        >>> all_stgs = stage_manager.all()                                  # 获取全部阶段
        >>> stage_manager.delete(1)                                         # 删除阶段
    """

    def __init__(self) -> None:
        pass

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> list[Stage]:
        """从服务端加载所有施工阶段信息（无缓存）"""
        resp = osis_client("GetStageInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        stages = [
            Stage._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "no" in d
        ]
        return stages

    # ── 增删改 ────────────────────────────────

    def create(     
        self,
        no: int,    # 施工阶段编号必须连续，不做自动编号
        name: str,
        duration: int,
    ) -> Stage:
        """创建施工阶段

        Args:
            no: 阶段编号。施工阶段编号必须连续，不做自动编号
            name: 施工阶段名称
            duration: 持续时间（天）

        Returns:
            创建的施工阶段对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_stage(no, name, duration)
        if not ok:
            raise RuntimeError(f"创建施工阶段 {no} 失败: {err}")
        return self.get(no)

    def delete(self, no: int) -> None:
        """删除施工阶段

        Args:
            no: 阶段编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_stage_del(no)
        if not ok:
            raise RuntimeError(f"删除施工阶段 {no} 失败: {err}")

    def insert(
        self,
        name: str,
        ref_no: int,
        position: Literal[0, 1],
        duration: float,
    ) -> Stage:
        """插入施工阶段

        Args:
            ref_no: 参考位置编号
            position: 0=前插，1=后插
            name: 所插入的施工阶段名称
            duration: 持续时间（天）

        Returns:
            创建的施工阶段对象

        Raises:
            RuntimeError: 插入失败时抛出异常
        """
        ok, err = osis_stage_insert(ref_no, position, name, duration)
        if not ok:
            raise RuntimeError(f"在 {ref_no} 处插入施工阶段失败: {err}")
        return self.get(ref_no + position)

    def remove(self, no: int) -> None:
        """移除插入的施工阶段

        Args:
            no: 阶段编号

        Raises:
            RuntimeError: 移除失败时抛出异常
        """
        ok, err = osis_stage_remove(no)
        if not ok:
            raise RuntimeError(f"移除施工阶段 {no} 失败: {err}")

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Stage | list[Stage | None] | None:
        """根据编号获取单个或多个施工阶段

        Args:
            no: 施工阶段编号

        Returns:
            Stage 对象或数组；阶段不存在返回 None
        """
        if isinstance(no, int):
            no = [no]
        elif not isinstance(no, list):
            raise TypeError(f"不支持的编号类型: {type(no)}")
        
        resp = osis_client("GetStageInfoByNos", {"no": no})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        stages = [Stage._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(stages) == 0:
            return None
        elif len(stages) == 1:
            return stages[0]
        return stages

    def all(self) -> list[Stage]:
        """获取所有施工阶段

        Returns:
            全部阶段列表
        """
        return self._load()

    def count(self) -> int:
        """获取施工阶段总数

        Returns:
            阶段数量
        """
        return len(self._load())

    def __repr__(self) -> str:
        return f"StageManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

stage_manager = StageManager()
