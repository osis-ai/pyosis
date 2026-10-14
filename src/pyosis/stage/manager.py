"""施工阶段管理器 - 统一管理施工阶段的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 无状态设计，每次从服务端加载（与 element/boundary manager 一致）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from ..core.client import osis_client
from ..core.basic_manager import BasicManager
from ..core.enums import analysis_type_name
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
class StageElementGroup:
    """阶段里的单元组

    激活和钝化各一份，用 activated 区分。
    """
    name: str
    activated: bool                    # True=激活, False=钝化
    birth: int | float | None = None   # 龄期
    part: int | None = None            # 组合结构分部：0=全部, 1=钢材, 2=混凝土

    @classmethod
    def _from_dict(cls, d: dict, activated: bool) -> "StageElementGroup":
        return cls(
            name=d.get("name"),
            activated=activated,
            birth=d.get("birth"),
            part=d.get("part"),
        )


@dataclass(frozen=True)
class StageBoundaryGroup:
    """阶段里的边界组

    激活和钝化各一份，用 activated 区分。
    """
    name: str
    activated: bool                    # True=激活, False=钝化
    position: str | None = None        # "beforeDeformation" / "afterDeformation"

    @classmethod
    def _from_dict(cls, d: dict, activated: bool) -> "StageBoundaryGroup":
        return cls(
            name=d.get("name"),
            activated=activated,
            position=d.get("position"),
        )


@dataclass(frozen=True)
class StageLoadCase:
    """阶段里的荷载工况"""
    name: str                          # 荷载工况名 lcName
    activated: bool                    # 是否激活
    ref_lc_name: str | None = None     # 上一阶段的参考工况 preRefLcName
    time: float | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> "StageLoadCase":
        return cls(
            name=d.get("lcName"),
            activated=bool(d.get("isActivated")),
            ref_lc_name=d.get("preRefLcName"),
            time=d.get("time"),
        )


@dataclass(frozen=True)
class StageAnalysisCase:
    """阶段里的分析工况"""
    name: str                          # 分析工况名 analName
    category: int                      # 分析类型（AnalysisType）
    activated: bool = True

    @property
    def category_name(self) -> str:
        """分析类型名（如 "Modal" / "Live"）；未知编码返回 ""。"""
        return analysis_type_name(self.category)

    @classmethod
    def _from_dict(cls, d: dict) -> "StageAnalysisCase":
        return cls(
            name=d.get("analName"),
            category=d.get("category"),
            activated=bool(d.get("isActivated", True)),
        )


@dataclass(frozen=True)
class StageEffectCase:
    """阶段作用工况汇总里的一条"""
    name: str
    status: str                        # "active" / "inactive"
    category: str                      # "loadCase" / "analysisCase" / "modal"
    time: float | None = None
    ref_lc_name: str | None = None
    analysis_category: int | None = None   # category == "analysisCase" 时的分析类型

    @property
    def activated(self) -> bool:
        return self.status == "active"

    @classmethod
    def _from_dict(cls, d: dict) -> "StageEffectCase":
        return cls(
            name=d.get("name"),
            status=d.get("status"),
            category=d.get("category"),
            time=d.get("time"),
            ref_lc_name=d.get("preRefLcName"),
            analysis_category=d.get("analysisCategory"),
        )


@dataclass(frozen=True)
class StageEffectCases:
    """阶段的作用工况汇总（接口 effectCases）

    load_cases / analysis_cases 与 Stage 上同名的两个字段是同一批数据的另一种视图，
    激活状态用 status 字符串表达；模态开关只在这里出现。
    """
    load_cases: list[StageEffectCase] = field(default_factory=list)
    analysis_cases: list[StageEffectCase] = field(default_factory=list)
    calc_vibration_mode: bool = False
    modal: StageEffectCase | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> "StageEffectCases":
        def _cases(key: str) -> list[StageEffectCase]:
            return [
                StageEffectCase._from_dict(x)
                for x in d.get(key) or []
                if isinstance(x, dict)
            ]

        modal = d.get("modal")
        return cls(
            load_cases=_cases("loadCases"),
            analysis_cases=_cases("analysisCases"),
            calc_vibration_mode=bool(d.get("calcVibrationMode")),
            modal=StageEffectCase._from_dict(modal) if isinstance(modal, dict) else None,
        )


@dataclass(frozen=True)
class Stage:
    """施工阶段对象

    由 StageManager 内部创建，用户不应直接实例化。
    """

    no: int
    name: str
    duration: float
    accumulation: float
    pre_stage_no: int
    element_groups: list[StageElementGroup] = field(default_factory=list)
    boundary_groups: list[StageBoundaryGroup] = field(default_factory=list)
    load_cases: list[StageLoadCase] = field(default_factory=list)
    analysis_cases: list[StageAnalysisCase] = field(default_factory=list)
    effect_cases: StageEffectCases | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> Stage:
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            duration=d.get("duration"),
            accumulation=d.get("accumulation"),
            pre_stage_no=d.get("preStageNo"),
            element_groups=cls._group_list(
                d.get("elementGroups"), StageElementGroup
            ),
            boundary_groups=cls._group_list(
                d.get("boundaryGroups"), StageBoundaryGroup
            ),
            load_cases=[
                StageLoadCase._from_dict(x)
                for x in d.get("loadCases") or []
                if isinstance(x, dict)
            ],
            analysis_cases=[
                StageAnalysisCase._from_dict(x)
                for x in d.get("analysisCases") or []
                if isinstance(x, dict)
            ],
            effect_cases=(
                StageEffectCases._from_dict(d["effectCases"])
                if isinstance(d.get("effectCases"), dict)
                else None
            ),
        )

    @staticmethod
    def _group_list(groups_data, group_cls) -> list:
        """从 elementGroups / boundaryGroups 嵌套结构展开成带 activated 的列表"""
        if not isinstance(groups_data, dict):
            return []
        groups: list = []
        for key, activated in (("active", True), ("inactive", False)):
            for item in groups_data.get(key) or []:
                if isinstance(item, dict):
                    groups.append(group_cls._from_dict(item, activated))
        return groups

    def define_element(
        self,
        op: Literal[1, 0],
        type: Literal[1, 0],
        group_name: str,
        birth: int | float | None = None,
        part: Literal[0, 1, 2]=None
    ) -> None:
        """通过单元组激活/钝化单元

        Args:
            op (int): 操作
                * 1 = 添加
                * 0 = 移除
            type (int):
                * 1 = 激活
                * 0 = 钝化
            group_name (str): 待操作的单元组名称
            birth (int): 龄期。eOP = 0 时需要设置为 None
            part (int): 组合结构的分部，可缺省（None）
                * 0 = 全部激活
                * 1 = 仅钢材部分
                * 2 = 仅混凝土部分

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_stage_element(self.no, op, type, group_name, birth, part)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 定义单元组 {group_name} 失败: {err}")

    def define_boundary(
        self,
        op: Literal[1, 0],
        type: Literal[1, 0],
        group_name: str
    ) -> None:
        """通过边界组激活/钝化边界

        Args:
            op (int): 操作
                * 1 = 添加
                * 0 = 移除
            type (int):
                * 1 = 激活
                * 0 = 钝化
            group_name (str): 待操作的边界组名称
            
        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_stage_boundary(self.no, op, type, group_name)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 定义边界组 {group_name} 失败: {err}")

    def define_loadcase(
        self,
        op: Literal[1, 0],
        type: Literal[1, 0],
        ref_lc_name: str, 
        lc_name: str
    ) -> None:
        """激活/钝化荷载工况

        Args:
            op (int): 操作
                * 1 = 添加
                * 0 = 移除
           type (int):
                * 1 = 激活
                * 0 = 钝化
            ref_lc_name (str): 参考当前施工阶段内的工况名称
            lc_name (str): 待操作的荷载工况名称
            
        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_stage_loadcase(self.no, op, type, ref_lc_name, lc_name)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 激活荷载工况 {lc_name} 失败: {err}")

    def define_analysis(
        self,
        op: Literal[1, 0],
        type: Literal["MODAL", "SETL", "RSPEC", "LIVE", "BUCKLE"],
        lc_name: str | None = None,
    ) -> None:
        """激活分析工况,分析工况默认在每个施工阶段的静力工况之后，不同分析工况无先后顺序

        Args:
            op (int): 操作
                * 1 = 添加
                * 0 = 移除
            type: 分析类型
                MODAL = 模态分析
                SETL = 沉降分析
                RSPEC = 反应谱
                LIVE = 活载分析
                BUCKLE = 屈曲分析
            lc_name: 荷载工况名称。MODAL 不需要，留 None 时命令流里不带该参数

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_stage_analysis(self.no, op, type, lc_name)
        if not ok:
            raise RuntimeError(f"阶段 {self.no} 激活分析工况 {type} 失败: {err}")


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class StageManager(BasicManager):
    """施工阶段管理器

    统一管理施工阶段的创建、删除、修改和查询。

    用法:
        >>> from pyosis.stage import stage_manager
        >>> stg = stage_manager.create(1, "阶段1", 3)                       # 创建施工阶段
        >>> stg = stage_manager.get(1)                                      # 按编号查询
        >>> all_stgs = stage_manager.all()                                  # 获取全部阶段
        >>> stage_manager.delete(1)                                         # 删除阶段
    """
    _entity_class = Stage
    _entity_key_attr = "no"

    def __init__(self) -> None:
        pass

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> list[Stage]:
        """从服务端加载所有施工阶段信息（无缓存）"""
        resp = osis_client("GetAllStageInfo", {})
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
        duration: int | float,
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
        ref_no: int,
        position: Literal[0, 1],
        name: str,
        duration: float | int,
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
        
        # batch 模式：返回延迟对象（零查询），访问真实属性时才物化
        lazy = self._batch_lazy(no)
        if lazy is not None:
            return lazy
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

    def clear(self)->None:
        """清空所有施工阶段"""
        try:
            [self.delete(s.no) for s in self.all()]
        except Exception as e:
            raise Exception(f"清空所有施工阶段失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return f"StageManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

stage_manager = StageManager()
