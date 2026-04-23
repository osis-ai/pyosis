"""沉降分析管理器 - 统一管理沉降组和沉降荷载工况

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 两级结构：SettlementManager 管理 Settlement 实例
- Settlement 实例代表一个沉降工况，包含沉降组管理方法
"""

from __future__ import annotations

from typing import Literal

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
# Settlement 类
# ──────────────────────────────────────────────


class Settlement:
    """沉降工况实例

    代表一个沉降荷载工况，同时提供沉降组的管理方法。

    用法:
        >>> from pyosis.settlement import settlement_manager
        >>> s = settlement_manager.create("S1")
        >>> # 创建沉降组
        >>> s.create("N1", -0.001, [1, 2, 3])
        >>> # 将沉降组关联到当前工况
        >>> s.include("N1", "N2")
        >>> # 从当前工况移除沉降组
        >>> s.remove("N1")
        >>> # 删除沉降组
        >>> s.delete("N2")
    """

    def __init__(self, name: str) -> None:
        self.name = name

    # ── 沉降组管理 ──────────────────────────────

    def create(self, name: str, val: float, nodes: list[int]) -> None:
        """创建或修改沉降组。

        Args:
            name: 组名
            val: 沉降量
            nodes: 沉降节点列表，创建时必须指定至少一个节点

        Examples:
            >>> # 创建包含节点 1, 2, 3 的沉降组
            >>> s.create("N1", -0.001, [1, 2, 3])

            >>> # 修改沉降组为只包含节点 1
            >>> s.create("N1", -0.001, [1])

        Note:
            - 创建时必须指定节点
            - 重复使用组名会修改现有沉降组
        """
        ok, err = osis_setl_grp(name, val, nodes)
        if not ok:
            raise RuntimeError(f"创建/修改沉降组 {name} 失败: {err}")

    def delete(self, name: str) -> None:
        """删除沉降组。

        Args:
            name: 组名
        """
        ok, err = osis_setl_grp_del(name)
        if not ok:
            raise RuntimeError(f"删除沉降组 {name} 失败: {err}")

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改沉降组编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_setl_grp_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改沉降组编号 {old_no} -> {new_no} 失败: {err}")

    # ── 工况关联管理 ──────────────────────────────

    def include(self, *group_names: str) -> None:
        """将沉降组添加至当前工况。

        Args:
            group_names: 沉降组名称列表

        Examples:
            >>> # 添加单个沉降组
            >>> s.include("N1")

            >>> # 添加多个沉降组
            >>> s.include("N1", "N2")
        """
        if not group_names:
            return
        ok, err = osis_setl_anal_inc(self.name, "a", list(group_names))
        if not ok:
            raise RuntimeError(f"添加沉降组到工况 {self.name} 失败: {err}")

    def remove(self, *group_names: str) -> None:
        """从当前工况移除沉降组。

        Args:
            group_names: 沉降组名称列表

        Examples:
            >>> # 移除单个沉降组
            >>> s.remove("N1")

            >>> # 移除多个沉降组
            >>> s.remove("N1", "N2")
        """
        if not group_names:
            return
        ok, err = osis_setl_anal_inc(self.name, "r", list(group_names))
        if not ok:
            raise RuntimeError(f"从工况 {self.name} 移除沉降组失败: {err}")

    def __repr__(self) -> str:
        return f"Settlement(name={self.name!r})"


# ──────────────────────────────────────────────
# SettlementManager 类
# ──────────────────────────────────────────────


class SettlementManager:
    """沉降工况管理器

    统一管理沉降荷载工况的创建、删除、修改。

    用法:
        >>> from pyosis.settlement import settlement_manager
        >>> # 创建沉降工况
        >>> s = settlement_manager.create("S1")
        >>> # 删除沉降工况
        >>> settlement_manager.delete("S1")
    """

    def __init__(self) -> None:
        ...

    def create(self, name: str) -> Settlement:
        """创建沉降荷载工况。

        Args:
            name: 沉降荷载工况名称

        Returns:
            Settlement: 沉降工况实例
        """
        ok, err = osis_setl_anal(name)
        if not ok:
            raise RuntimeError(f"创建沉降荷载工况 {name} 失败: {err}")
        return Settlement(name)

    def delete(self, name: str) -> None:
        """删除沉降荷载工况。

        Args:
            name: 沉降荷载工况名称
        """
        ok, err = osis_setl_anal_del(name)
        if not ok:
            raise RuntimeError(f"删除沉降荷载工况 {name} 失败: {err}")

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改沉降荷载工况编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_setl_anal_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改沉降荷载工况编号 {old_no} -> {new_no} 失败: {err}")

    def all(self) -> list[Settlement]:
        return []

    def __repr__(self) -> str:
        return f"SettlementManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

settlement_manager = SettlementManager()
