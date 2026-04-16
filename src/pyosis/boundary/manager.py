"""边界管理器 - 统一管理边界的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护边界列表，通过 get 等方法查询，不暴露 HTTP 接口细节
- 按边界类型分化数据结构，create_* 返回具体子类型

支持的边界类型：GENERAL（一般边界）、MSTSLV（主从约束）、RELEASE（释放梁端约束）、
ELSTCSPT（弹性支承）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from ..core.client import osis_client
from .interface import (
    osis_boundary_general,
    osis_boundary_elstcspt,
    osis_boundary_master_slave,
    osis_boundary_release,
    osis_boundary_group,
    osis_boundary_del,
    osis_assign_boundary,
)


def _assign_boundary_to_nodes(
    no: int,
    eOP: Literal["a", "s", "r", "aa", "ra"],
    param: list,
) -> None:
    """分配边界给节点（一般支撑、节点弹性支撑），内部实现。"""
    ok, err = osis_assign_boundary(no, eOP, param)
    if not ok:
        raise RuntimeError(f"分配边界 {no} 到节点 {param} 失败: {err}")


def _dict_looks_like_elstcspt(d: dict) -> bool:
    """区分 type=4 时实为弹性支承还是梁端释放（部分服务端误将弹性支承标为 4）。

    参见 ``io.boundary_info``：弹性支承含 ``k`` / ``elasticK``；释放约束含 ``endIState`` / ``endJState``。
    """
    if d.get("elasticK") is not None:
        return True
    k = d.get("k")
    if isinstance(k, list) and len(k) > 0:
        return True
    if d.get("endIState") is not None or d.get("endJState") is not None:
        return False
    c = d.get("constraints") or []
    if isinstance(c, list) and len(c) == 7:
        return True
    return False


# ──────────────────────────────────────────────
# Boundary 基类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Boundary:
    """边界基类

    由 BoundaryManager 内部创建，用户不应直接实例化。
    get() / all() 返回此类型。
    """

    no: int
    name: str = ""
    boundary_type: str = ""
    raw_type: int = 0
    entity_vec: list[int] = field(default_factory=list)
    is_occupied: bool = False
    is_ploted: bool = False
    is_selected: bool = False

    def __repr__(self) -> str:
        return f"Boundary(no={self.no}, type={self.boundary_type})"


# ──────────────────────────────────────────────
# General 边界
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class GeneralBoundary(Boundary):
    """一般边界

    constraints[7]: [UX, UY, UZ, RX, RY, RZ, RW]
        0 = 释放，1 = 约束
    coor_no: 局部坐标系编号，None 表示无局部坐标系
    """

    constraints: list[int] = field(default_factory=list)  # 固定7个
    coor_no: int | None = None

    def __repr__(self) -> str:
        return f"GeneralBoundary(no={self.no}, constraints={self.constraints}, coor_no={self.coor_no})"

    @property
    def ux(self) -> int:
        return self.constraints[0] if len(self.constraints) > 0 else 0

    @property
    def uy(self) -> int:
        return self.constraints[1] if len(self.constraints) > 1 else 0

    @property
    def uz(self) -> int:
        return self.constraints[2] if len(self.constraints) > 2 else 0

    @property
    def rx(self) -> int:
        return self.constraints[3] if len(self.constraints) > 3 else 0

    @property
    def ry(self) -> int:
        return self.constraints[4] if len(self.constraints) > 4 else 0

    @property
    def rz(self) -> int:
        return self.constraints[5] if len(self.constraints) > 5 else 0

    @property
    def rw(self) -> int:
        return self.constraints[6] if len(self.constraints) > 6 else 0

    def assign(
        self,
        eOP: Literal["a", "s", "r", "aa", "ra"] = "a",
        param: list | None = None,
    ) -> None:
        """分配边界给节点（一般支撑）。

        对应 ``pyosis.boundary.osis_assign_boundary``。

        Args:
            eOP: 操作 — a=添加，s=替换，r=移除，aa=添加全部，ra=移除全部
            param: 待操作的编号，支持 ``*``、``*to*``、``*by*``（仅用于替换）。
                例：``[2, 3, 5, "8to10"]``、``["2by3", "5by6", "8by10"]``；重合编号自动忽略。
        """
        _assign_boundary_to_nodes(self.no, eOP, param if param is not None else [])


# ──────────────────────────────────────────────
# MstSlv 边界（主从约束）
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class MstSlvBoundary(Boundary):
    """主从约束

    constraints[6]: [UX, UY, UZ, RX, RY, RZ]
        0 = 释放，1 = 约束
    master_no: 主节点编号
    """

    constraints: list[int] = field(default_factory=list)  # 固定6个
    master_no: int | None = None

    def __repr__(self) -> str:
        return f"MstSlvBoundary(no={self.no}, master_no={self.master_no}, constraints={self.constraints})"

    @property
    def ux(self) -> int:
        return self.constraints[0] if len(self.constraints) > 0 else 0

    @property
    def uy(self) -> int:
        return self.constraints[1] if len(self.constraints) > 1 else 0

    @property
    def uz(self) -> int:
        return self.constraints[2] if len(self.constraints) > 2 else 0

    @property
    def rx(self) -> int:
        return self.constraints[3] if len(self.constraints) > 3 else 0

    @property
    def ry(self) -> int:
        return self.constraints[4] if len(self.constraints) > 4 else 0

    @property
    def rz(self) -> int:
        return self.constraints[5] if len(self.constraints) > 5 else 0


# ──────────────────────────────────────────────
# Release 边界（释放梁端约束）
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class ReleaseBoundary(Boundary):
    """释放梁端约束

    I端(7) + J端(7) = 14个约束状态/值
    state: 0 = 释放，1 = 约束
    value: 0-1 表示释放后残余约束能力的百分比
    """

    i_state: list[int] = field(default_factory=list)   # I端约束状态 [7]
    i_values: list[float] = field(default_factory=list)  # I端约束值 [7]
    j_state: list[int] = field(default_factory=list)   # J端约束状态 [7]
    j_values: list[float] = field(default_factory=list)  # J端约束值 [7]

    def __repr__(self) -> str:
        return f"ReleaseBoundary(no={self.no})"


# ──────────────────────────────────────────────
# ElstcSpt 边界（弹性支承）
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class ElstcSptBoundary(Boundary):
    """弹性支承（弹簧单元）

    constraints[7]: [UX, UY, UZ, RX, RY, RZ, RW]
        0 = 弹性，1 = 固定
    stiffness: 各方向的弹性刚度值
    """

    constraints: list[int] = field(default_factory=list)  # 固定7个
    coor_no: int | None = None
    # 弹性刚度值（从接口填充）
    DX: float | None = None
    DY: float | None = None
    DZ: float | None = None
    RX: float | None = None
    RY: float | None = None
    RZ: float | None = None

    def __repr__(self) -> str:
        return f"ElstcSptBoundary(no={self.no}, constraints={self.constraints})"

    def assign(
        self,
        eOP: Literal["a", "s", "r", "aa", "ra"] = "a",
        param: list | None = None,
    ) -> None:
        """分配边界给节点（节点弹性支撑）。

        对应 ``pyosis.boundary.osis_assign_boundary``。

        Args:
            eOP: 操作 — a=添加，s=替换，r=移除，aa=添加全部，ra=移除全部
            param: 待操作的编号，支持 ``*``、``*to*``、``*by*``（仅用于替换）。
                例：``[2, 3, 5, "8to10"]``、``["2by3", "5by6", "8by10"]``；重合编号自动忽略。
        """
        _assign_boundary_to_nodes(self.no, eOP, param if param is not None else [])


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class BoundaryManager:
    """边界管理器

    统一管理边界的创建、删除和查询。

    用法:
        >>> from pyosis.boundary import boundary_manager
        >>> bd = boundary_manager.create_general(bX=1, bY=1, bZ=1, bRX=0, bRY=0, bRZ=0)  # 返回 GeneralBoundary
        >>> sp = boundary_manager.create_elstcspt(DX=1e10, DY=1e10, DZ=1e10)              # 返回 ElstcSptBoundary
        >>> ms = boundary_manager.create_master_slave(nNode=1, bX=1, bY=1, bZ=1)          # 返回 MstSlvBoundary
        >>> bd = boundary_manager.get(1)                                                   # 返回基类 Boundary
        >>> all_bds = boundary_manager.all()                                                # 返回基类 Boundary 列表
        >>> boundary_manager.delete(bd.no)                                                 # 删除边界
    """

    def __init__(self) -> None:
        self._boundaries: list[Boundary] = []  # 基类引用
        self._bd_map: dict[int, Boundary] = {}  # 按编号索引
        self._loaded: bool = False

    # ── 数据加载 ──────────────────────────────

    def _reload_get_as(self, no: int, expected_cls: type[Boundary], what: str) -> Boundary:
        """创建/修改后从服务端重载并返回指定类型对象（内部使用）。"""
        self._loaded = False
        self._load()
        bd = self._bd_map.get(no)
        if bd is None:
            raise RuntimeError(f"{what} {no} 成功但无法从服务端获取完整信息")
        if not isinstance(bd, expected_cls):
            raise RuntimeError(f"{what} {no} 成功但返回类型错误: {type(bd)}")
        return bd

    def _load(self) -> None:
        """从服务端加载所有边界信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllBoundaryInfo", {})
        if isinstance(resp, tuple):
            raise RuntimeError(f"加载边界信息失败: {resp[1]}")

        self._boundaries = []
        self._bd_map = {}

        for d in resp.get("data", []):
            if not isinstance(d, dict) or "no" not in d:
                continue
            bd = self._parse_boundary(d)
            self._boundaries.append(bd)
            self._bd_map[bd.no] = bd

        self._loaded = True

    def _parse_boundary(self, d: dict) -> Boundary:
        """根据 raw_type 解析并返回对应子类型的边界对象"""
        raw_type = int(d.get("type", 0) or 0)

        coor_raw = d.get("coorNO", None)
        coor_no = None if coor_raw in (None, -1, "-1", "") else int(coor_raw)

        master_raw = d.get("masterNO", None)
        master_no = None if master_raw in (None, -1, "-1", "") else int(master_raw)

        common = dict(
            no=int(d.get("no", 0) or 0),
            name=str(d.get("name", "") or ""),
            raw_type=raw_type,
            entity_vec=list(d.get("entityVec", []) or []),
            is_occupied=bool(d.get("isOccupied", False)),
            is_ploted=bool(d.get("isPloted", False)),
            is_selected=bool(d.get("isSelected", False)),
        )

        if raw_type == 1:  # General
            constraints = list(d.get("constraints", []) or [])
            return GeneralBoundary(
                **common,
                boundary_type="General",
                constraints=constraints,
                coor_no=coor_no,
            )

        elif raw_type == 2:  # MstSlv
            constraints = list(d.get("constraints", []) or [])
            return MstSlvBoundary(
                **common,
                boundary_type="MstSlv",
                constraints=constraints,
                master_no=master_no,
            )

        elif raw_type == 4:
            constraints = list(d.get("constraints", []) or [])
            # type=4 在部分后端中与弹性支承混用，按 payload 字段区分
            if _dict_looks_like_elstcspt(d):
                return ElstcSptBoundary(
                    **common,
                    boundary_type="ElstcSpt",
                    constraints=constraints,
                    coor_no=coor_no,
                )
            # Release（梁端释放）
            i_state = constraints[:7] if len(constraints) >= 7 else constraints + [0] * (7 - len(constraints))
            j_state = constraints[7:14] if len(constraints) >= 14 else [0] * max(0, 14 - len(constraints))
            return ReleaseBoundary(
                **common,
                boundary_type="Release",
                i_state=i_state,
                i_values=[],  # Release 的 value 数据需另行获取
                j_state=j_state,
                j_values=[],
            )

        elif raw_type == 5:  # ElstcSpt
            constraints = list(d.get("constraints", []) or [])
            return ElstcSptBoundary(
                **common,
                boundary_type="ElstcSpt",
                constraints=constraints,
                coor_no=coor_no,
            )

        elif raw_type == 6:  # GeneralElstcSpt
            constraints = list(d.get("constraints", []) or [])
            return ElstcSptBoundary(
                **common,
                boundary_type="GeneralElstcSpt",
                constraints=constraints,
                coor_no=coor_no,
            )

        else:
            # 未知类型，返回基类
            return Boundary(**common, boundary_type="Unknown")

    def refresh(self) -> None:
        """强制刷新缓存（模型变更后自动调用，也可手动调用）"""
        self._boundaries = []
        self._bd_map = {}
        self._loaded = False
        self._load()

    def _next_no(self) -> int:
        """生成下一个可用边界编号

        取已有边界编号的最大值+1，如果没有边界则从1开始。
        """
        self._load()
        if not self._boundaries:
            return 1
        return max(bd.no for bd in self._boundaries) + 1

    # ── 增删改 ────────────────────────────────

    def create_general(
        self,
        nCoor: int = None,
        bX: bool = 1,
        bY: bool = 1,
        bZ: bool = 1,
        bRX: bool = 1,
        bRY: bool = 1,
        bRZ: bool = 1,
        bRW: bool = 1,
        no: int | None = None,
    ) -> GeneralBoundary:
        """创建一般边界

        Args:
            nCoor: 局部坐标系编号，"" 代表缺省
            bX: UX方向，0=释放，1=约束
            bY: UY方向，0=释放，1=约束
            bZ: UZ方向，0=释放，1=约束
            bRX: RX方向，0=释放，1=约束
            bRY: RY方向，0=释放，1=约束
            bRZ: RZ方向，0=释放，1=约束
            bRW: RW方向，0=释放，1=约束
            no: 边界编号，不指定时自动生成（取最大编号+1）

        Returns:
            GeneralBoundary 对象（包含完整的 constraints 和 coor_no）

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        if nCoor is None:
            nCoor = ""
        ok, err = osis_boundary_general(no, "GENERAL", nCoor, bX, bY, bZ, bRX, bRY, bRZ, bRW)
        if not ok:
            raise RuntimeError(f"创建一般边界 {no} 失败: {err}")
        return self._reload_get_as(no, GeneralBoundary, "创建一般边界")  # type: ignore[return-value]

    def create_elstcspt(
        self,
        bX: bool = 1,
        DX: float = 1e13,
        bY: bool = 1,
        DY: float = 1e13,
        bZ: bool = 1,
        DZ: float = 1e13,
        bRX: bool = 1,
        RX: float = 1e16,
        bRY: bool = 1,
        RY: float = 1e16,
        bRZ: bool = 1,
        RZ: float = 1e16,
        nCoor: int = None,
        no: int | None = None,
    ) -> ElstcSptBoundary:
        """创建弹簧单元弹性支承

        Args:
            bX: UX方向，0=弹性，1=固定
            DX: 坐标系X轴方向的弹性支承刚度
            bY: UY方向，0=弹性，1=固定
            DY: 坐标系Y轴方向的弹性支承刚度
            bZ: UZ方向，0=弹性，1=固定
            DZ: 坐标系Z轴方向的弹性支承刚度
            bRX: RX方向，0=弹性，1=固定
            RX: 绕坐标系X轴方向的转动弹性刚度
            bRY: RY方向，0=弹性，1=固定
            RY: 绕坐标系Y轴方向的转动弹性刚度
            bRZ: RZ方向，0=弹性，1=固定
            RZ: 绕坐标系Z轴方向的转动弹性刚度
            nCoor: 局部坐标系编号，固定使用""缺省
            no: 边界编号，不指定时自动生成（取最大编号+1）

        Returns:
            ElstcSptBoundary 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        if nCoor is None:
            nCoor = ""
        ok, err = osis_boundary_elstcspt(
            no, "ELSTCSPT", nCoor, bX, DX, bY, DY, bZ, DZ, bRX, RX, bRY, RY, bRZ, RZ
        )
        if not ok:
            raise RuntimeError(f"创建弹性支承 {no} 失败: {err}")
        return self._reload_get_as(no, ElstcSptBoundary, "创建弹性支承")  # type: ignore[return-value]

    def create_master_slave(
        self,
        nNode: int,
        bX: bool = 1,
        bY: bool = 1,
        bZ: bool = 1,
        bRX: bool = 1,
        bRY: bool = 1,
        bRZ: bool = 1,
        no: int | None = None,
    ) -> MstSlvBoundary:
        """创建主从约束

        Args:
            nNode: 主节点编号
            bX: UX方向，0=释放，1=约束
            bY: UY方向，0=释放，1=约束
            bZ: UZ方向，0=释放，1=约束
            bRX: RX方向，0=释放，1=约束
            bRY: RY方向，0=释放，1=约束
            bRZ: RZ方向，0=释放，1=约束
            no: 边界编号，不指定时自动生成（取最大编号+1）

        Returns:
            MstSlvBoundary 对象（包含 master_no 和 constraints）

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_master_slave(no, "MSTSLV", nNode, bX, bY, bZ, bRX, bRY, bRZ)
        if not ok:
            raise RuntimeError(f"创建主从约束 {no} 失败: {err}")
        return self._reload_get_as(no, MstSlvBoundary, "创建主从约束")  # type: ignore[return-value]

    def create_release(
        self,
        Fxi_state: bool,
        Fyi_state: bool,
        Fzi_state: bool,
        Mxi_state: bool,
        Myi_state: bool,
        Mzi_state: bool,
        Mbi_state: bool,
        Fxi: float,
        Fyi: float,
        Fzi: float,
        Mxi: float,
        Myi: float,
        Mzi: float,
        Mbi: float,
        Fxj_state: bool,
        Fyj_state: bool,
        Fzj_state: bool,
        Mxj_state: bool,
        Myj_state: bool,
        Mzj_state: bool,
        Mbj_state: bool,
        Fxj: float,
        Fyj: float,
        Fzj: float,
        Mxj: float,
        Myj: float,
        Mzj: float,
        Mbj: float,
        no: int | None = None,
    ) -> ReleaseBoundary:
        """创建释放梁端约束

        Args:
            Fxi_state等: 端部约束状态，0=释放，1=约束
            Fxi等: 约束值，0-1之间，表示释放后残余的约束能力的百分比
            no: 边界编号，不指定时自动生成（取最大编号+1）

        Returns:
            ReleaseBoundary 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """

        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_release(
            no, "RELEASE",
            Fxi_state, Fyi_state, Fzi_state, Mxi_state, Myi_state, Mzi_state, Mbi_state,
            Fxi, Fyi, Fzi, Mxi, Myi, Mzi, Mbi,
            Fxj_state, Fyj_state, Fzj_state, Mxj_state, Myj_state, Mzj_state, Mbj_state,
            Fxj, Fyj, Fzj, Mxj, Myj, Mzj, Mbj,
        )
        if not ok:
            raise RuntimeError(f"创建释放梁端约束 {no} 失败: {err}")
        return self._reload_get_as(no, ReleaseBoundary, "创建释放梁端约束")  # type: ignore[return-value]

    def delete(self, no: int) -> None:
        """删除边界

        Args:
            no: 边界编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_boundary_del(no)
        if not ok:
            raise RuntimeError(f"删除边界 {no} 失败: {err}")
        self._loaded = False

    # ── 边界组 ─────────────────────────────────

    def group(
        self,
        name: str,
        eOP: Literal["c", "a", "s", "r", "aa", "ra", "m", "d"],
        param: list = [],
    ) -> None:
        """边界组操作封装

        对应 `pyosis.boundary.osis_boundary_group`。

        Args:
            name: 边界组名
            eOP: 操作
                - c: 创建
                - a: 添加
                - s: 替换
                - r: 移除
                - aa: 添加全部
                - ra: 移除全部
                - m: 修改组名（param 里给新名字）
                - d: 删除
            param: 参数列表（编号列表，或区间表达式等；m 操作时放新组名）
        """
        ok, err = osis_boundary_group(name, eOP, param)
        if not ok:
            raise RuntimeError(f"边界组操作失败 name={name} eOP={eOP} param={param}: {err}")
        # 组操作不改变边界本体，但为了保险（有些实现会影响可见性/占用），使缓存失效
        self._loaded = False

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Boundary | list[Boundary | None]:
        """根据编号获取单个或多个边界 (O(k))

        Args:
            no: 边界编号

        Returns:
            Boundary 对象或数组；边界不存在返回 None
        """
        self._load()
        if isinstance(no, int):
            return self._bd_map.get(no)
        elif isinstance(no, list):
            return [self._bd_map.get(n) for n in no]
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")

    def all(self) -> list[Boundary]:
        """获取所有边界

        Returns:
            全部边界列表
        """
        self._load()
        return list(self._boundaries)

    def count(self) -> int:
        """获取边界总数

        Returns:
            边界数量
        """
        self._load()
        return len(self._boundaries)

    def __repr__(self) -> str:
        self._load()
        return f"BoundaryManager(count={len(self._boundaries)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

boundary_manager = BoundaryManager()
