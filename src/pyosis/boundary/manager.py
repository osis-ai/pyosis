"""边界管理器 - 统一管理边界的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 按边界类型分化数据结构
- 无状态设计，每次从服务端加载（与 element.manager 一致）

支持的边界类型：
- GENERAL（一般边界，type=1）
- MSTSLV（主从约束，type=2）
- RELEASE（释放梁端约束，type=4）
- ELSTCSPT（弹性支承，type=5）
- GENERALELSTCSPT（一般弹性支承，type=6）

注：截面特性调整（SECF）为独立功能，不属于边界类型
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from enum import Enum, IntEnum

from ..core.client import osis_client
from .interface import (
    osis_boundary_general,
    osis_boundary_elstcspt,
    osis_boundary_master_slave,
    osis_boundary_release,
    osis_boundary_general_elstcspt,
    osis_boundary_rigid,
    osis_boundary_section_factor,
    osis_boundary_group,
    osis_boundary_del,
    osis_assign_boundary,
)


# ──────────────────────────────────────────────
# 枚举类型
# ──────────────────────────────────────────────

class BoundaryType(IntEnum):
    """边界类型枚举"""
    UNASSIGNED = 0
    GENERAL = 1				    # 一般支撑
    MSTSLV = 2				    # 主从约束
    RELEASE = 3				    # 释放梁端约束
    ELSTCSPT = 4				# 节点弹性支承
    GENERALELSTCSPT = 5		    # 一般弹性支承
    RIGID = 6				    # 刚性连接


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Boundary:
    """边界基类

    由 BoundaryManager 内部创建，用户不应直接实例化。
    """
    no: int
    name: str = ""
    boundary_type: BoundaryType = BoundaryType.GENERAL
    entity_vec: list[int] = field(default_factory=list)
    is_occupied: bool = False
    is_selected: bool = False
    is_ploted: bool = False

    @classmethod
    def _from_dict(cls, d: dict) -> Boundary:
        """从接口 dict 构造 Boundary 对象（内部使用）"""
        raw_type = int(d.get("type"))
        
        # 根据类型创建具体子类
        if raw_type == BoundaryType.GENERAL:
            return GeneralBoundary._from_dict(d)
        elif raw_type == BoundaryType.MSTSLV:
            return MstSlvBoundary._from_dict(d)
        elif raw_type == BoundaryType.RELEASE:
            return ReleaseBoundary._from_dict(d)
        elif raw_type == BoundaryType.ELSTCSPT:
            return ElstcSptBoundary._from_dict(d)
        elif raw_type == BoundaryType.GENERALELSTCSPT:
            return GeneralElstcSptBoundary._from_dict(d)
        else:
            # 未知类型返回基类
            return cls(
                no=d.get("no"),
                name=d.get("name"),
                boundary_type=BoundaryType(raw_type) if raw_type in [t.value for t in BoundaryType] else BoundaryType.GENERAL,
                entity_vec=list(d.get("entityVec")),
                is_occupied=d.get("isOccupied"),
                is_selected=d.get("isSelected"),
                is_ploted=d.get("isPloted"),
            )
    
    def set_section_factor(
        self,
        area: float,
        sy: float,
        sz: float,
        ixx: float,
        iyy: float,
        izz: float,
        iww: float,
        weight: float,
    ):
        """边界截面特性调整

        Args:
            area: 面积调整系数
            sy: Y向剪切常数调整系数
            sz: Z向剪切常数调整系数
            ixx: X轴抗扭惯性矩调整系数
            iyy: Y轴抗弯惯性矩调整系数
            izz: Z轴抗弯惯性矩调整系数
            iww: 翘曲惯性矩调整系数
            weight: 自重调整系数
            no: 截面编号，None 时自动分配

        Returns:
            SectionFactorBoundary 对象
        """
        ok, err = osis_boundary_section_factor(
            self.no, "SECF", area, sy, sz, ixx, iyy, izz, iww, weight
        )
        if not ok:
            raise RuntimeError(f"边界 {self.no} 的截面特性修改失败: {err}")

    def __repr__(self) -> str:
        return f"Boundary(no={self.no}, type={self.boundary_type.name})"
    
    
    def assign(
        self,
        eOP: Literal["a", "s", "r", "aa", "ra"] = "a",
        param: list | None = None,
    ) -> None:
        """分配边界给节点"""
        ok, err = osis_assign_boundary(self.no, eOP, param if param is not None else [])
        if not ok:
            raise RuntimeError(f"分配边界 {self.no} 到节点 {param} 失败: {err}")


@dataclass(frozen=True)
class GeneralBoundary(Boundary):
    """一般边界
    
    constraints[7]: [UX, UY, UZ, RX, RY, RZ, RW]
        0 = 释放，1 = 约束
    coor_no: 局部坐标系编号
    """
    constraints: list[int] = field(default_factory=list)  # 7个约束
    coor_no: int | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> GeneralBoundary:
        """从接口 dict 构造 GeneralBoundary 对象"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            boundary_type=BoundaryType.GENERAL,
            entity_vec=list(d.get("entityVec")),
            is_occupied=d.get("isOccupied"),
            is_selected=d.get("isSelected"),
            is_ploted=d.get("isPloted"),
            constraints=list(d.get("constraints")),
            coor_no=d.get("coorNO"),
        )

    def __repr__(self) -> str:
        return f"GeneralBoundary(no={self.no}, constraints={self.constraints})"

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


@dataclass(frozen=True)
class MstSlvBoundary(Boundary):
    """主从约束
    
    constraints[6]: [UX, UY, UZ, RX, RY, RZ]
        0 = 释放，1 = 约束
    master_no: 主节点编号
    """
    constraints: list[int] = field(default_factory=list)  # 6个约束
    master_no: int | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> MstSlvBoundary:
        """从接口 dict 构造 MstSlvBoundary 对象"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            boundary_type=BoundaryType.MSTSLV,
            entity_vec=list(d.get("entityVec")),
            is_occupied=d.get("isOccupied"),
            is_selected=d.get("isSelected"),
            is_ploted=d.get("isPloted"),
            constraints=list(d.get("constraints")),
            master_no=d.get("masterNO"),
        )

    def __repr__(self) -> str:
        return f"MstSlvBoundary(no={self.no}, master_no={self.master_no})"


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

    @classmethod
    def _from_dict(cls, d: dict) -> ReleaseBoundary:
        """从接口 dict 构造 ReleaseBoundary 对象"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            boundary_type=BoundaryType.RELEASE,
            entity_vec=list(d.get("entityVec")),
            is_occupied=d.get("isOccupied"),
            is_selected=d.get("isSelected"),
            is_ploted=d.get("isPloted"),
            i_state=list(d.get("endIState")),
            i_values=list(d.get("endI")),
            j_state=list(d.get("endJState")),
            j_values=list(d.get("endJ")),
        )

    def __repr__(self) -> str:
        return f"ReleaseBoundary(no={self.no})"


@dataclass(frozen=True)
class ElstcSptBoundary(Boundary):
    """弹性支承
    
    constraints[7]: [UX, UY, UZ, RX, RY, RZ, RW]
        0 = 弹性，1 = 固定
    k[7]: 各方向的弹性刚度值
    """
    constraints: list[int] = field(default_factory=list)  # 7个
    coor_no: int | None = None
    k_values: list[float] = field(default_factory=list)  # 7个刚度值
    elastic_k: list[dict] = field(default_factory=list)  # 弹性刚度详细信息

    @classmethod
    def _from_dict(cls, d: dict) -> ElstcSptBoundary:
        """从接口 dict 构造 ElstcSptBoundary 对象"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            boundary_type=BoundaryType.ELSTCSPT,
            entity_vec=list(d.get("entityVec")),
            is_occupied=d.get("isOccupied"),
            is_selected=d.get("isSelected"),
            is_ploted=d.get("isPloted"),
            # constraints=list(d.get("constraints")),
            coor_no=d.get("coorNO"),
            k_values=list(d.get("k")),
            elastic_k=list(d.get("elasticK")),
        )

    def __repr__(self) -> str:
        return f"ElstcSptBoundary(no={self.no}, constraints={self.constraints})"


@dataclass(frozen=True)
class GeneralElstcSptBoundary(Boundary):
    """一般弹性支承
    
    6x6 刚度矩阵
    flagM: 是否有质量矩阵
    flagC: 是否有阻尼矩阵
    """
    coor_no: int | None = None
    flag_m: bool = False
    flag_c: bool = False
    stiffness_matrix: list[list[float]] = field(default_factory=list)  # 6x6
    mass_matrix: list[list[float]] = field(default_factory=list)      # 6x6，可选
    damping_matrix: list[list[float]] = field(default_factory=list)   # 6x6，可选

    @classmethod
    def _from_dict(cls, d: dict) -> GeneralElstcSptBoundary:
        """从接口 dict 构造 GeneralElstcSptBoundary 对象"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            boundary_type=BoundaryType.GENERALELSTCSPT,
            entity_vec=list(d.get("entityVec")),
            is_occupied=d.get("isOccupied"),
            is_selected=d.get("isSelected"),
            is_ploted=d.get("isPloted"),
            coor_no=d.get("coorNO"),
            flag_m=d.get("flagM"),
            flag_c=d.get("flagC"),
            stiffness_matrix=list(d.get("stiffnessMatrix")),
            # mass_matrix=list(d.get("massMatrix")),
            # damping_matrix=list(d.get("dampingMatrix")),
        )

    def __repr__(self) -> str:
        return f"GeneralElstcSptBoundary(no={self.no})"


@dataclass(frozen=False)
class BoundaryGroup:
    """边界组对象

    由 BoundaryGroupManager 内部创建，用户不应直接实例化。
    提供组成员增删改查操作。
    """
    name: str
    boundary_nos: list[int] = field(default_factory=list)
    boundary_count: int = 0
    related_stages: list[int] = field(default_factory=list)
    related_stage_count: int = 0
    relied_nodes: list[int] = field(default_factory=list)
    relied_elements: list[int] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict) -> BoundaryGroup:
        """从接口 dict 构造 BoundaryGroup 对象"""
        return cls(
            name=d.get("groupName"),
            boundary_nos=list(d.get("boundaryNos")),
            boundary_count=d.get("boundaryCount"),
            related_stages=list(d.get("relatedStages")),
            related_stage_count=d.get("relatedStageCount"),
            relied_nodes=list(d.get("reliedNodes")),
            relied_elements=list(d.get("reliedElements")),
        )

    def _sync_from_dict(self, d: dict) -> None:
        """用 dict 同步当前对象（内部使用）"""
        self.name = d.get("groupName")
        self.boundary_nos = list(d.get("boundaryNos"))
        self.boundary_count = d.get("boundaryCount")
        self.related_stages = list(d.get("relatedStages"))
        self.related_stage_count = d.get("relatedStageCount")
        self.relied_nodes = list(d.get("reliedNodes"))
        self.relied_elements = list(d.get("reliedElements"))

    def refresh(self) -> BoundaryGroup:
        """刷新当前边界组对象并同步到对象属性"""
        resp = osis_client("GetBoundaryGroupInfoByNames", {"name": [self.name]})
        if not resp['success']:
            raise RuntimeError(f"刷新边界组 {self.name} 失败: {resp['error']}")
        data = resp.get("data", [])
        if data and data[0]:
            self._sync_from_dict(data[0])
        return self

    def _execute(self, operation: str, param: list | None = None) -> None:
        """执行边界组底层操作（内部使用）"""
        ok, err = osis_boundary_group(self.name, operation, param)
        if not ok:
            raise RuntimeError(f"边界组操作 {self.name} ({operation}) 失败: {err}")

    def add(self, boundaries: list[int]) -> BoundaryGroup:
        """向边界组添加边界

        Args:
            boundaries: 边界编号列表

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("a", boundaries)
        return self.refresh()

    def remove(self, boundaries: list[int]) -> BoundaryGroup:
        """从边界组移除边界

        Args:
            boundaries: 边界编号列表

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("r", boundaries)
        return self.refresh()

    def replace(self, boundaries: list[int]) -> BoundaryGroup:
        """替换边界组内边界

        Args:
            boundaries: 新的边界编号列表

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("s", boundaries)
        return self.refresh()

    def add_all(self) -> BoundaryGroup:
        """添加全部边界到组

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("aa")
        return self.refresh()

    def remove_all(self) -> BoundaryGroup:
        """从组移除全部边界

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("ra")
        return self.refresh()

    def rename(self, new_name: str) -> BoundaryGroup:
        """修改边界组名称

        Args:
            new_name: 新名称

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("m", [new_name])
        self.name = new_name
        return self.refresh()

    def __repr__(self) -> str:
        return f"BoundaryGroup(name={self.name!r}, boundaries={self.boundary_nos})"


# ──────────────────────────────────────────────
# BoundaryGroup 管理类
# ──────────────────────────────────────────────


class BoundaryGroupManager:
    """边界组管理器

    统一管理边界组的创建、删除和查询。组成员操作在 BoundaryGroup 对象上进行。
    由 BoundaryManager 持有，不单独导出。

    用法:
        >>> from pyosis.boundary import boundary_manager
        >>> # 创建和查询
        >>> bg = boundary_manager.group.create("桥台1")
        >>> bg = boundary_manager.group.get("桥台1")
        >>> # 组成员操作（在对象上调用）
        >>> bg.add([1, 2])
        >>> bg.remove([1])
        >>> bg.replace([3, 4])
    """

    def __init__(self) -> None:
        ...

    def _load(self) -> list[BoundaryGroup]:
        """从服务端加载所有边界组信息"""
        resp = osis_client("GetAllBoundaryGroupInfo", {})
        if not resp["success"]:
            raise RuntimeError(resp["error"])
        
        groups = [
            BoundaryGroup._from_dict(d) 
            for d in resp.get("data", []) 
            if isinstance(d, dict) and "groupName" in d
        ]
        return groups

    # ── 增删改 ────────────────────────────────

    def create(self, name: str) -> BoundaryGroup:
        """创建边界组

        Args:
            name: 边界组名称

        Returns:
            创建的 BoundaryGroup 对象
        """
        ok, err = osis_boundary_group(name, "c")
        if not ok:
            raise RuntimeError(f"创建边界组 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除边界组

        Args:
            name: 边界组名称
        """
        ok, err = osis_boundary_group(name, "d")
        if not ok:
            raise RuntimeError(f"删除边界组 {name} 失败: {err}")
        
    def rename(self, old_name, new_name) -> None:
        """修改边界组名"""
        ok, err = osis_boundary_group(old_name, "m", [new_name])
        if not ok:
            raise RuntimeError(f"修改边界组名  {old_name} -> {new_name} 失败:  失败: {err}")
        return self.get(new_name)

    # ── 查询 ──────────────────────────────────
    
    def get(self, name: str | list[str]) -> BoundaryGroup | list[BoundaryGroup | None] | None:
        """根据名称获取单个或多个边界组

        Args:
            name: 边界组名称，支持单个名称或名称列表

        Returns:
            单个 BoundaryGroup 对象；如果传入列表则返回对象列表；
            不存在返回 None
        """

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetBoundaryGroupInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        boundary_groups = [BoundaryGroup._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(boundary_groups) == 0:
            return None
        elif len(boundary_groups) == 1:
            return boundary_groups[0]
        return boundary_groups
    
    def all(self) -> list[BoundaryGroup]:
        """获取所有边界组"""
        return self._load()

    def count(self) -> int:
        """获取边界组总数"""
        return len(self._load())

    def clear(self) -> None:
        """清空所有边界组"""
        try:
            [self.delete(bg.name) for bg in self.all()]
        except Exception as e:
            raise Exception(f"清空所有边界组失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return f"BoundaryGroupManager()"


# ──────────────────────────────────────────────
# 边界管理类
# ──────────────────────────────────────────────


class BoundaryManager:
    """边界管理器

    统一管理边界的创建、删除、修改和查询。

    用法:
        >>> from pyosis.boundary import boundary_manager
        >>> bd = boundary_manager.create_general(bX=1, bY=1, bZ=1, no=1)
        >>> bd = boundary_manager.get(1)
        >>> all_bds = boundary_manager.all()
        >>> # 边界组操作
        >>> bg = boundary_manager.group.create("桥台1")
        >>> bg.add([1, 2])
        >>> bg = boundary_manager.group.get("桥台1")
    """

    def __init__(self) -> None:
        self._group_manager = BoundaryGroupManager()

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> list[Boundary]:
        """从服务端加载所有边界信息（无缓存）"""
        resp = osis_client("GetAllBoundaryInfo", {})
        if not resp["success"]:
            raise RuntimeError(f"{resp['error']}")
        
        boundaries = [
            Boundary._from_dict(d) 
            for d in resp.get("data", []) 
            if isinstance(d, dict) and "no" in d
        ]
        return boundaries

    def _next_no(self) -> int:
        """生成下一个可用边界编号"""
        boundaries = self._load()
        if not boundaries:
            return 1
        return max(bd.no for bd in boundaries) + 1

    # ── 增删改 ────────────────────────────────
    def create(self, no: int | None, type: str, *args: Any, **kwargs: Any) -> Boundary:
        """创建边界（便捷入口，内部转发到对应 create_* 方法）

        Args:
            no: 边界编号，None 则自动分配
            type: 边界类型，"GENERAL" / "MSTSLV" / "RELEASE" /
                  "ELSTCSPT" / "GES" / "RIGID"
            *args: 按位置传给对应 create_* 的参数
            **kwargs: 按关键字传给对应 create_* 的参数

        Raises:
            ValueError: 未知的 type
            RuntimeError: 创建失败

        Examples:
            >>> boundary_manager.create(None, "GENERAL", bX=1, bY=1, bZ=1)
            >>> boundary_manager.create(1, "MSTSLV", nNode=10)
            >>> boundary_manager.create(2, "RIGID", nNodeI=5)
        """
        _creator = {
            "GENERAL": self.create_general,
            "MSTSLV": self.create_master_slave,
            "RELEASE": self.create_release,
            "ELSTCSPT": self.create_elstcspt,
            "GES": self.create_general_elstcspt,
            "RIGID": self.create_rigid,
        }
        type_key = type.upper()
        if type_key not in _creator:
            raise ValueError(
                f"未知边界类型: {type!r}，支持: {', '.join(_creator)}"
            )
        return _creator[type_key](*args, no=no, **kwargs)

    def create_general(
        self,
        nCoor: int | str = "",
        bX: Literal[0, 1] = 1,
        bY: Literal[0, 1] = 1,
        bZ: Literal[0, 1] = 1,
        bRX: Literal[0, 1] = 1,
        bRY: Literal[0, 1] = 1,
        bRZ: Literal[0, 1] = 1,
        bRW: Literal[0, 1] = 1,
        no: int | None = None,
    ) -> GeneralBoundary:
        """创建一般边界"""
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_general(no, "GENERAL", nCoor or "", bX, bY, bZ, bRX, bRY, bRZ, bRW)
        if not ok:
            raise RuntimeError(f"创建一般边界 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_master_slave(
        self,
        nNode: int,
        bX: Literal[0, 1] = 1,
        bY: Literal[0, 1] = 1,
        bZ: Literal[0, 1] = 1,
        bRX: Literal[0, 1] = 1,
        bRY: Literal[0, 1] = 1,
        bRZ: Literal[0, 1] = 1,
        no: int | None = None,
        bCoincident: int | None = 1,
    ) -> MstSlvBoundary:
        """创建主从约束"""
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_master_slave(no, "MSTSLV", nNode, bX, bY, bZ, bRX, bRY, bRZ,bCoincident)
        if not ok:
            raise RuntimeError(f"创建主从约束 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

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
        """创建释放梁端约束"""
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
        return self.get(no)  # type: ignore[return-value]

    def create_elstcspt(
        self,
        nCoor: int | str = "",
        bX: Literal[0, 1] = 1,
        DX: float = 1e13,
        bY: Literal[0, 1] = 1,
        DY: float = 1e13,
        bZ: Literal[0, 1] = 1,
        DZ: float = 1e13,
        bRX: Literal[0, 1] = 1,
        RX: float = 1e16,
        bRY: Literal[0, 1] = 1,
        RY: float = 1e16,
        bRZ: Literal[0, 1] = 1,
        RZ: float = 1e16,
        no: int | None = None,
    ) -> ElstcSptBoundary:
        """创建弹性支承"""
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_elstcspt(
            no, "ELSTCSPT", nCoor or "", bX, DX, bY, DY, bZ, DZ, bRX, RX, bRY, RY, bRZ, RZ
        )
        if not ok:
            raise RuntimeError(f"创建弹性支承 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_general_elstcspt(
        self,
        nCoor: int | str = "",
        stiffness_matrix: list[float] | None = None,
        mass_matrix: list[float] | None = None,
        damping_matrix: list[float] | None = None,
        no: int | None = None,
    ) -> GeneralElstcSptBoundary:
        """创建一般弹性支承

        Args:
            nCoor: 局部坐标系编号，"" 代表缺省
            stiffness_matrix: 6x6 刚度矩阵上三角元素（21个值），必须全部给出
                顺序：K11,K12,K13,K14,K15,K16,K22,K23,K24,K25,K26,K33,K34,K35,K36,K44,K45,K46,K55,K56,K66
            mass_matrix: 6x6 质量矩阵上三角元素（21个值），可选
            damping_matrix: 6x6 阻尼矩阵上三角元素（21个值），可选
            no: 边界编号，None 时自动分配

        Returns:
            GeneralElstcSptBoundary 对象
        """
        if no is None:
            no = self._next_no()
        if stiffness_matrix is None:
            stiffness_matrix = []
        
        # 构建参数序列
        params = list(stiffness_matrix)
        
        # 质量矩阵
        if mass_matrix:
            params.append(1)  # bM = 1
            params.extend(mass_matrix)
        else:
            params.append(0)  # bM = 0
        
        # 阻尼矩阵
        if damping_matrix:
            params.append(1)  # bC = 1
            params.extend(damping_matrix)
        else:
            params.append(0)  # bC = 0
        
        ok, err = osis_boundary_general_elstcspt(
            no, "GES", nCoor or "", *params
        )
        if not ok:
            raise RuntimeError(f"创建一般弹性支承 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_rigid(
        self,
        nNodeI: int,
        no: int | None = None,
    ) -> Boundary:
        """创建刚性连接

        Args:
            nNodeI: 节点1编号（刚性区域的主节点）
            no: 边界编号，None 时自动分配

        Returns:
            Boundary 对象

        Notes:
            用于形成刚性区域的节点号 nodeJ, nodeK, ..., nodeL 由 assign 方法定义
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_rigid(no, "RIGID", nNodeI)
        if not ok:
            raise RuntimeError(f"创建刚性连接 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def delete(self, no: int) -> None:
        """删除边界"""
        ok, err = osis_boundary_del(no)
        if not ok:
            raise RuntimeError(f"删除边界 {no} 失败: {err}")

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Boundary | list[Boundary | None] | None:
        """根据编号获取单个或多个边界 (O(k))
        
        接口：GetBoundaryInfoByNos
        """
        if isinstance(no, int):
            no = [no]
        elif not isinstance(no, list):
            raise TypeError(f"不支持的编号类型: {type(no)}")
        
        resp = osis_client("GetBoundaryInfoByNos", {"no": no})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        boundaries = [Boundary._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(boundaries) == 0:
            return None
        elif len(boundaries) == 1:
            return boundaries[0]
        return boundaries

    def all(self) -> list[Boundary]:
        """获取所有边界"""
        return self._load()

    def count(self) -> int:
        """获取边界总数"""
        return len(self._load())

    def clear(self) -> None:
        """清空所有边界"""
        try:
            [self.delete(b.no) for b in self.all()]
        except Exception as e:
            raise Exception(f"清空所有边界失败: {e}，被占用,无法删除")

    # ── 子管理器 ──────────────────────────────

    @property
    def group(self) -> BoundaryGroupManager:
        """边界组管理器

        提供边界组的增删改查功能。

        用法:
            >>> boundary_manager.group.create("桥台1")
            >>> boundary_manager.group.add("桥台1", [1, 2])
            >>> boundary_manager.group.get("桥台1")
        """
        return self._group_manager

    def __repr__(self) -> str:
        return f"BoundaryManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

boundary_manager = BoundaryManager()
