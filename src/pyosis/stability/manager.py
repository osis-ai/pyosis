"""稳定分析管理器 - 统一管理屈曲工况的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 支持屈曲工况的定义、删除、修改及荷载工况的添加/移除/替换
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .buckling import (
    osis_buckl_anal,
    osis_buckl_anal_del,
    osis_buckl_anal_mod,
    osis_buckl_anal_inc,
)
from ..core.client import osis_client


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


class BucklCaseInfo:
    """屈曲工况中的荷载工况信息"""
    
    def __init__(self, name: str, scalar: float, load_type: Literal[0, 1]):
        self.name = name
        self.scalar = scalar
        self.load_type = load_type
    
    def __repr__(self) -> str:
        return f"BucklCaseInfo(name={self.name!r}, scalar={self.scalar}, type={self.load_type})"

@dataclass(frozen=False)
class BucklCase:
    """屈曲工况对象"""
    accum: bool
    accumLCParas: dict
    analysisType: int
    lcParas: list[dict]
    modalNum: int
    name: str
    no: int
    relatedStages: list[int]
    @classmethod
    def _from_dict(cls, d: dict) -> BucklCase:
        return cls(
            accum=d.get("accum"), 
            accumLCParas=d.get("accumLCParas"), 
            analysisType=d.get("analysisType"), 
            lcParas=d.get("lcParas"), 
            modalNum=d.get("modalNum"), 
            name=d.get("name"), 
            no=d.get("no"), 
            relatedStages=d.get("relatedStages")
            )

# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class StabilityManager:
    """稳定分析管理器

    统一管理屈曲工况的创建、删除、修改及荷载工况管理。

    用法:
        >>> from pyosis.stability import stability_manager
        >>> # 创建屈曲工况
        >>> stability_manager.create("B1", num=5, accum=0, scalar=1.0, load_type=0)
        >>> # 添加荷载工况
        >>> stability_manager.include("B1", "a", "D", 1.0, 0)
        >>> # 替换荷载工况
        >>> stability_manager.replace("B1", "DC", 1.2, 0, "D", 1.0, 0)
        >>> # 删除屈曲工况
        >>> stability_manager.delete("B1")
    """

    def __init__(self) -> None:
        ...

    # ── 屈曲工况管理 ──────────────────────────────
    def _load(self) -> list[BucklCase]:
        """从服务端加载所有屈曲工况信息"""
        resp = osis_client("GetAllBucklingInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        buckl_cases = [BucklCase._from_dict(d) for d in resp.get("data", []) if "name" in d]
        return buckl_cases
    def get(self, name: str | list[str]) -> BucklCase | list[BucklCase | None] | None:
        """根据名称获取屈曲工况"""

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        resp = osis_client("GetBucklingInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        buckl_cases = [BucklCase._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(buckl_cases) == 0:
            return None
        elif len(buckl_cases) == 1:
            return buckl_cases[0]
        return buckl_cases

    def all(self) -> list[BucklCase]:
        """获取所有屈曲工况"""
        return self._load()

    def create(
        self,
        name: str,
        num: int = 1,
        accum: Literal[0, 1] = 0,
        scalar: float = 1.0,
        load_type: Literal[0, 1] = 0,
    ) -> None:
        """定义或修改屈曲工况。

        Args:
            name: 屈曲分析工况名称
            num: 模态数量
            accum: 当前施工阶段是否考虑合计，0=考虑，1=不考虑
            scalar: 缩放系数
            load_type: 荷载类型，1=可变，0=不变
        """
        ok, err = osis_buckl_anal(name, num, accum, scalar, load_type)
        if not ok:
            raise RuntimeError(f"创建/修改屈曲工况 {name} 失败: {err}")

    def delete(self, name: str) -> None:
        """删除屈曲工况。

        Args:
            name: 屈曲分析工况名称
        """
        ok, err = osis_buckl_anal_del(name)
        if not ok:
            raise RuntimeError(f"删除屈曲工况 {name} 失败: {err}")

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改屈曲工况编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_buckl_anal_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改屈曲工况编号 {old_no} -> {new_no} 失败: {err}")

    # ── 荷载工况管理 ──────────────────────────────

    def include(
        self,
        name: str,
        op: Literal["a", "r"],
        lc_name: str,
        scalar: float,
        lc_type: Literal[0, 1],
    ) -> None:
        """添加或移除参与屈曲分析的荷载工况。

        Args:
            name: 屈曲分析工况名称
            op: 操作类型，"a"=添加，"r"=移除
            lc_name: 荷载工况名称
            scalar: 系数
            lc_type: 荷载类型，1=可变，0=不变

        Examples:
            >>> # 添加荷载工况 D 到屈曲工况 B1
            >>> stability_manager.include("B1", "a", "D", 1.0, 0)

            >>> # 从屈曲工况 B1 移除荷载工况 D
            >>> stability_manager.include("B1", "r", "D", 1.0, 0)
        """
        ok, err = osis_buckl_anal_inc(name, op, lc_name, scalar, lc_type)
        if not ok:
            raise RuntimeError(f"{'添加' if op == 'a' else '移除'}荷载工况 {lc_name} {'到' if op == 'a' else '从'}屈曲工况 {name} 失败: {err}")

    def replace(
        self,
        name: str,
        new_lc: str,
        new_scalar: float,
        new_type: Literal[0, 1],
        old_lc: str,
        old_scalar: float,
        old_type: Literal[0, 1],
    ) -> None:
        """替换参与屈曲分析的荷载工况。

        Args:
            name: 屈曲分析工况名称
            new_lc: 新的荷载工况名称
            new_scalar: 新的系数
            new_type: 新的荷载类型，1=可变，0=不变
            old_lc: 被替换的荷载工况名称
            old_scalar: 被替换的系数
            old_type: 被替换的荷载类型，1=可变，0=不变

        Examples:
            >>> # 将屈曲工况 B1 中的 D 替换为 DC
            >>> stability_manager.replace("B1", "DC", 1.2, 0, "D", 1.0, 0)
        """
        ok, err = osis_buckl_anal_inc(
            name, "s", new_lc, new_scalar, new_type, old_lc, old_scalar, old_type
        )
        if not ok:
            raise RuntimeError(f"替换屈曲工况 {name} 中的荷载工况 {old_lc} -> {new_lc} 失败: {err}")

    def __repr__(self) -> str:
        return f"StabilityManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

stability_manager = StabilityManager()
