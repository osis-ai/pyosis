"""厚度管理器 - 统一管理板或壳的厚度特性

用法:
    >>> from pyosis.thickness import thickness_manager
    >>> thickness_manager.create(1, 0, 0.3, 0.3)
    >>> thickness_manager.delete(1)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .interface import (
    osis_shell_thickness,
    osis_shell_thickness_del,
    osis_shell_thickness_mod,
)
from ..core.client import osis_client
from ..core import get_references, raise_if_occupied


@dataclass(frozen=True)
class Thickness:
    no: int
    in_plane: float
    out_plane: float
    related_elements: list[int] = field(default_factory=list)
    # 以下字段 C++ 侧目前还没往 JSON 里放，先按接口契约留好位置
    is_uniform: bool | None = None
    has_offset: bool | None = None
    is_relative: bool | None = None
    thk_ratio: float | None = None
    offset_distance: float | None = None
    @classmethod
    def _from_dict(cls, d: dict) -> "Thickness":
        return cls(
            no=d.get("no"),
            in_plane=d.get("inPlane", 0.0),
            out_plane=d.get("outPlane", 0.0),
            related_elements=list(d.get("relatedElement") or []),
            is_uniform=d.get("isUniform"),
            has_offset=d.get("hasOffset"),
            is_relative=d.get("isRelative"),
            thk_ratio=d.get("thkRatio"),
            offset_distance=d.get("offsetDistance"),
        )

class ThicknessManager:
    '''厚度管理器

    统一管理板或壳的厚度特性的创建、删除、修改与查询。
    '''

    def _load(self) -> list[Thickness]:
        '''从服务端加载所有板/壳厚度特性'''
        resp = osis_client("GetAllShellThicknessInfo", {})
        if not resp.get("success"):
            raise RuntimeError(resp.get("error", "GetAllShellThicknessInfo 失败"))
        return [
            Thickness._from_dict(d)
            for d in resp.get("data", [])
            if isinstance(d, dict) and d.get("no") is not None
        ]

    def get(self, no: int | list[int]) -> Thickness | list[Thickness | None] | None:
        '''根据编号获取单个或多个厚度特性

        Args:
            no (int | list[int]): 厚度特性编号，支持单个编号或编号列表

        Returns:
            单个 Thickness 对象；如果传入列表则返回对象列表；不存在返回 None
        '''
        nos = [no] if isinstance(no, int) else no
        resp = osis_client("GetShellThicknessInfoByNos", {"no": nos})
        if not resp.get("success"):
            raise RuntimeError(resp.get("error"))
        items = [
            Thickness._from_dict(d) if isinstance(d, dict) and d.get("no") is not None else None
            for d in resp.get("data", [])
        ]
        if len(items) == 0:
            return None
        if len(items) == 1:
            return items[0]
        return items

    def all(self) -> list[Thickness]:
        '''获取所有厚度特性'''
        return self._load()

    def count(self) -> int:
        '''获取厚度特性总数'''
        return len(self._load())

    def clear(self) -> None:
        '''清空所有厚度特性'''
        try:
            [self.delete(t.no) for t in self.all()]
        except Exception as e:
            raise Exception(f"清空所有厚度特性失败: {e}，被占用,无法删除")

    def create(
        self,
        no: int,
        is_uniform: Literal[0, 1],
        in_plane: float,
        out_plane: float,
        has_offset: Literal[0, 1] = 0,
        is_relative: Literal[0, 1] = 0,
        thk_ratio: float = 1.0,
        offset_distance: float = 0.0,
    ) -> None:
        '''创建或修改板或壳的厚度特性

        参数顺序与命令流 ShellThk 一致。

        Args:
            no (int): 厚度特性编号
            is_uniform (int): 面内面外厚度是否相同，1=相同，0=不同
            in_plane (float): 面内厚度，大于 0
            out_plane (float): 面外厚度，大于 0。仅 is_uniform=0 时有效
            has_offset (int): 是否有偏移
            is_relative (int): 偏移是否按相对值给定
            thk_ratio (float): 厚度比
            offset_distance (float): 偏移距离

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_shell_thickness(
            no, is_uniform, in_plane, out_plane,
            has_offset, is_relative, thk_ratio, offset_distance,
        )
        if not ok:
            raise RuntimeError(f"创建厚度特性 {no} 失败: {err}")

    def get_dependencies(self, no: int) -> dict[str, list]:
        '''查询壳厚度被哪些对象引用

        Args:
            no (int): 厚度特性编号

        Returns:
            dict[str, list]: 引用该厚度特性的对象列表
        '''
        return get_references("ShellThickness", no=no)

    def delete(self, no: int) -> None:
        '''删除板或壳的厚度特性

        Args:
            no (int): 厚度特性编号

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(no)
        raise_if_occupied("ShellThickness", deps, no=no)
        ok, err = osis_shell_thickness_del(no)
        if not ok:
            raise RuntimeError(f"删除厚度特性 {no} 失败: {err}")

    def renumber(self, old: str, new: str) -> None:
        '''修改厚度特性编号

        Args:
            old (str): 旧编号
            new (str): 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        '''
        ok, err = osis_shell_thickness_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改厚度特性编号 {old} -> {new} 失败: {err}")

    def __repr__(self) -> str:
        return "ThicknessManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

thickness_manager = ThicknessManager()
