"""边界管理器 - 统一管理边界的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护边界列表，通过 get 等方法查询，不暴露 HTTP 接口细节

支持的边界类型：GENERAL（一般边界）、MSTSLV（主从约束）、RELEASE（释放梁端约束）、
ELSTCSPT（弹性支承）
"""

from __future__ import annotations
from typing import Literal

from dataclasses import dataclass

from ..core.client import osis_client
from .interface import (
    osis_boundary_general,
    osis_boundary_elstcspt,
    osis_boundary_master_slave,
    osis_boundary_release,
    osis_boundary_del,
    osis_assign_boundary,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Boundary:
    """边界对象

    由 BoundaryManager 内部创建，用户不应直接实例化。
    """

    no: int
    name: str = ""
    boundary_type: str = ""  # "General", "MstSlv", "Release", "ElstcSpt", "GeneralElstcSpt"
    entity_vec: list[int] | None = None
    is_occupied: bool = False

    @classmethod
    def _from_dict(cls, d: dict) -> Boundary:
        """从接口 dict 构造 Boundary 对象（内部使用）"""
        type_names = {
            1: "General",
            2: "MstSlv",
            3: "Rigid",
            4: "Release",
            5: "ElstcSpt",
            6: "GeneralElstcSpt",
        }
        return cls(
            no=d.get("no", 0),
            name=d.get("name", ""),
            boundary_type=type_names.get(d.get("type", 0), "Unknown"),
            entity_vec=d.get("entityVec", []),
            is_occupied=d.get("isOccupied", False),
        )

    def assign(self, eOP: Literal["a", "s", "r", "aa", "ra"]="a", param: list=[]):
        '''
        ## 分配边界给节点(一般支撑，节点弹性支撑)
        pyosis.boundary.osis_assign_boundary
        
        Args:
            eOP (str): 操作
                * a = 添加
                * s = 替换
                * r = 移除
                * aa = 添加全部
                * ra = 移除全部
            param (list): 待操作的编号，支持的格式：*，*to*，*by*（仅用于替换）。
                例子：[2,3,5,"8to10"] ["2by3","5by6","8by10"] 重合的编号自动忽略
        Returns:
            tuple (bool, str): 是否成功，失败原因
        '''
        ok, err = osis_assign_boundary(self.no, eOP, param)
        if not ok:
            raise RuntimeError(f"分配边界 {self.no} 到节点 {param} 失败: {err}")

# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class BoundaryManager:
    """边界管理器

    统一管理边界的创建、删除和查询。

    用法:
        >>> from pyosis.boundary import boundary_manager
        >>> bd = boundary_manager.create_general(bX=1, bY=1, bZ=1, bRX=0, bRY=0, bRZ=0)  # 创建一般边界（编号自动生成）
        >>> sp = boundary_manager.create_elstcspt(DX=1e10, DY=1e10, DZ=1e10)              # 创建弹性支承
        >>> ms = boundary_manager.create_master_slave(nNode=1, bX=1, bY=1, bZ=1)         # 创建主从约束
        >>> bd = boundary_manager.get(1)                                                # 按编号查询
        >>> all_bds = boundary_manager.all()                                           # 获取全部边界
        >>> boundary_manager.delete(bd.no)                                             # 删除边界
    """

    def __init__(self) -> None:
        self._boundaries: list[Boundary] = []
        self._bd_map: dict[int, Boundary] = {}  # 按编号索引：O(1) 查询
        self._loaded: bool = False

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有边界信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllBoundaryInfo", {})
        if isinstance(resp, tuple):
            raise RuntimeError(f"加载边界信息失败: {resp[1]}")
        self._boundaries = [
            Boundary._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "no" in d
        ]

        # 构建索引：编号 -> 边界对象 (O(1) 查询)
        self._bd_map = {bd.no: bd for bd in self._boundaries}

        self._loaded = True

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
    ) -> Boundary:
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
            创建的边界对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        self.refresh()
        if no is None:
            no = self._next_no()
        if nCoor is None:
            nCoor = ""
        ok, err = osis_boundary_general(no, "GENERAL", nCoor, bX, bY, bZ, bRX, bRY, bRZ, bRW)
        if not ok:
            raise RuntimeError(f"创建一般边界 {no} 失败: {err}")
        self._loaded = False
        return Boundary(no=no, name="", boundary_type="General")

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
    ) -> Boundary:
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
            创建的边界对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        self.refresh()
        if no is None:
            no = self._next_no()
        if nCoor is None:
            nCoor = ""
        ok, err = osis_boundary_elstcspt(
            no, "ELSTCSPT", nCoor, bX, DX, bY, DY, bZ, DZ, bRX, RX, bRY, RY, bRZ, RZ
        )
        if not ok:
            raise RuntimeError(f"创建弹性支承 {no} 失败: {err}")
        self._loaded = False
        return Boundary(no=no, name="", boundary_type="ElstcSpt")

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
    ) -> Boundary:
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
            创建的边界对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        self.refresh()
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_master_slave(no, "MSTSLV", nNode, bX, bY, bZ, bRX, bRY, bRZ)
        if not ok:
            raise RuntimeError(f"创建主从约束 {no} 失败: {err}")
        self._loaded = False
        return Boundary(no=no, name="", boundary_type="MstSlv")

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
    ) -> Boundary:
        """创建释放梁端约束

        Args:
            Fxi_state等: 端部约束状态，0=释放，1=约束
            Fxi等: 约束值，0-1之间，表示释放后残余的约束能力的百分比
            no: 边界编号，不指定时自动生成（取最大编号+1）

        Returns:
            创建的边界对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        self.refresh()
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
        self._loaded = False
        return Boundary(no=no, name="", boundary_type="Release")

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
