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
from enum import IntEnum

from ..core.client import osis_client
from ..core import get_references, raise_if_occupied
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
        op: Literal["a", "s", "r", "aa", "ra"] = "a",
        *param: int | str,
    ) -> None:
        """分配边界给节点"""
        if len(param) == 1 and isinstance(param[0], list):
            nodes = param[0]
        else:
            nodes = list(param)
        ok, err = osis_assign_boundary(self.no, op, nodes)
        if not ok:
            raise RuntimeError(f"分配边界 {self.no} 到节点 {nodes} 失败: {err}")


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

    def _execute(self, operation: Literal["c", "a", "s", "r", "aa", "ra", "m", "d"], *param: str | int) -> None:
        """执行边界组底层操作（内部使用）"""
        ok, err = osis_boundary_group(self.name, operation, *param)
        if not ok:
            raise RuntimeError(f"边界组操作 {self.name} ({operation}) 失败: {err}")

    def add(self, *boundaries: int) -> BoundaryGroup:
        """向边界组添加边界

        Args:
            boundaries: 边界编号列表

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("a", *boundaries)
        return self.refresh()

    def remove(self, *boundaries: int) -> BoundaryGroup:
        """从边界组移除边界

        Args:
            boundaries: 边界编号列表

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("r", *boundaries)
        return self.refresh()

    def replace(self, *boundaries: int) -> BoundaryGroup:
        """替换边界组内边界

        Args:
            boundaries: 新的边界编号列表

        Returns:
            更新后的 BoundaryGroup 对象
        """
        self._execute("s", *boundaries)
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
        self._execute("m", new_name)
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
        >>> bg.add(1, 2)
        >>> bg.remove(1)
        >>> bg.replace("3by4")   # 组内把边界 3 替换为 4
    """

    def __init__(self) -> None:
        ...

    def _load(self) -> list[BoundaryGroup]:
        '''从服务端加载所有边界组信息'''
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

    def create(self, name: str, op:Literal["c", "a", "s", "r", "aa", "ra", "m", "d"], *param) -> BoundaryGroup:
        '''创建边界组并返回刷新后的对象

        Args:
            name: 边界组名称
            op: 操作类型
                * c = 创建
                * a = 添加
                * s = 替换
                * r = 移除
                * aa = 添加全部
                * ra = 移除全部
                * m = 修改组名
                * d = 删除
            *param: 待操作的编号，支持格式：*，*to*；*by*（仅用于替换）。
                例子：[2,3,5,"8to10"] ["2by3","5by6","8by10"] 重合的编号自动忽略

        Returns:
            BoundaryGroup: 创建（或刷新后的）边界组对象
        '''
        ok, err = osis_boundary_group(name, op, *param)
        if not ok:
            raise RuntimeError(f"创建边界组 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        '''删除边界组

        Args:
            name: 边界组名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        '''
        ok, err = osis_boundary_group(name, "d")
        if not ok:
            raise RuntimeError(f"删除边界组 {name} 失败: {err}")
        
    def rename(self, old_name, new_name) -> None:
        '''修改边界组名称

        Args:
            old_name: 原边界组名称
            new_name: 新边界组名称
        '''
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
        '''获取所有边界组'''
        return self._load()

    def count(self) -> int:
        '''获取边界组总数'''
        return len(self._load())

    def clear(self) -> None:
        '''清空所有边界组

        逐个删除服务端的所有边界组；若任一边界组被占用则抛出异常。
        '''
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
        >>> bg.add(1, 2)
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
        """返回下一个可用的边界编号（当前最大编号 + 1，空模型为 1）"""
        boundaries = self._load()
        if not boundaries:
            return 1
        return max(bd.no for bd in boundaries) + 1

    def get_dependencies(self, no: int) -> dict[str, list]:
        """查询边界被哪些对象引用（用于删除前检查占用情况）

        Args:
            no: 边界编号

        Returns:
            dict[str, list]: 依赖项字典，键为引用类型，值为引用编号列表
        """
        return get_references("Boundary", no=no)

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
            >>> boundary_manager.create(None, "GENERAL", x=1, y=1, z=1)
            >>> boundary_manager.create(1, "MSTSLV", node=10)
            >>> boundary_manager.create(2, "RIGID", node_i=5)
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
        return _creator[type_key](no, *args, **kwargs)

    def create_general(
        self,
        no: int | None,
        coor: int | str = "",
        x: bool = 1,
        y: bool = 1,
        z: bool = 1,
        rx: bool = 1,
        ry: bool = 1,
        rz: bool = 1,
        rw: bool = 1,
    ) -> GeneralBoundary:
        '''创建一般支撑边界

        在指定节点上约束 7 个自由度（UX/UY/UZ/RX/RY/RZ/RW），
        可基于局部坐标系或全局坐标系。

        Args:
            no: 边界编号，None 时自动分配
            coor: 局部坐标系编号，"" 代表缺省（使用全局坐标系）
            x: UX 方向约束标志，0 = 释放，1 = 约束
            y: UY 方向约束标志，0 = 释放，1 = 约束
            z: UZ 方向约束标志，0 = 释放，1 = 约束
            rx: RX 方向约束标志，0 = 释放，1 = 约束
            ry: RY 方向约束标志，0 = 释放，1 = 约束
            rz: RZ 方向约束标志，0 = 释放，1 = 约束
            rw: RW（翘曲）方向约束标志，0 = 释放，1 = 约束

        Returns:
            GeneralBoundary 对象

        Examples:
            >>> boundary_manager.create_general(None, x=1, y=1, z=1)
        '''
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_general(no, "GENERAL", coor or "", x, y, z, rx, ry, rz, rw)
        if not ok:
            raise RuntimeError(f"创建一般边界 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_master_slave(
        self,
        no: int | None,
        node: int,
        dx: bool = 1,
        dy: bool = 1,
        dz: bool = 1,
        rx: bool = 1,
        ry: bool = 1,
        rz: bool = 1,
        coincident: int | None = 1,
    ) -> MstSlvBoundary:
        '''创建主从约束

        将已分配本边界的从节点与指定的主节点在 6 个自由度上耦合，
        常用于模拟桥梁支座、铰接等连接关系。

        Args:
            no: 边界编号，None 时自动分配
            node: 主节点编号
            dx: UX 方向耦合标志，0 = 释放，1 = 约束
            dy: UY 方向耦合标志，0 = 释放，1 = 约束
            dz: UZ 方向耦合标志，0 = 释放，1 = 约束
            rx: RX 方向耦合标志，0 = 释放，1 = 约束
            ry: RY 方向耦合标志，0 = 释放，1 = 约束
            rz: RZ 方向耦合标志，0 = 释放，1 = 约束
            coincident: 0 = 仅同位移约束；1 = 完全主从约束（含转动耦合），默认 1

        Returns:
            MstSlvBoundary 对象

        Examples:
            >>> boundary_manager.create_master_slave(None, node=10, coincident=1)
        '''
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_master_slave(no, "MSTSLV", node, dx, dy, dz, rx, ry, rz,coincident)
        if not ok:
            raise RuntimeError(f"创建主从约束 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_release(
        self,
        no: int | None,
        fxi_state: bool,fyi_state: bool,fzi_state: bool,
        mxi_state: bool,myi_state: bool,mzi_state: bool,mbi_state: bool,
        fxi: float,fyi: float,fzi: float,
        mxi: float,myi: float,mzi: float,mbi: float,
        fxj_state: bool,fyj_state: bool,fzj_state: bool,
        mxj_state: bool,myj_state: bool,mzj_state: bool,mbj_state: bool,
        fxj: float,fyj: float,fzj: float,
        mxj: float,myj: float,mzj: float,mbj: float,
    ) -> ReleaseBoundary:
        '''创建释放梁端约束

        在梁单元的 I 端和 J 端分别释放 7 个自由度（FX/FY/FZ/MX/MY/MZ/MB），
        每个自由度通过 _state（0 = 完全释放，1 = 完全约束）和对应 _value（0-1 之间，
        表示释放后残余约束能力的百分比）共同控制。

        Args:
            no: 边界编号，None 时自动分配
            fxi_state: I 端 FX（轴力）状态，0 = 释放，1 = 约束
            fyi_state: I 端 FY（剪力）状态，0 = 释放，1 = 约束
            fzi_state: I 端 FZ（剪力）状态，0 = 释放，1 = 约束
            mxi_state: I 端 MX（扭矩）状态，0 = 释放，1 = 约束
            myi_state: I 端 MY（弯矩）状态，0 = 释放，1 = 约束
            mzi_state: I 端 MZ（弯矩）状态，0 = 释放，1 = 约束
            mbi_state: I 端 MB（双力矩）状态，0 = 释放，1 = 约束
            fxi: I 端 FX 部分约束残余百分比（0-1）
            fyi: I 端 FY 部分约束残余百分比（0-1）
            fzi: I 端 FZ 部分约束残余百分比（0-1）
            mxi: I 端 MX 部分约束残余百分比（0-1）
            myi: I 端 MY 部分约束残余百分比（0-1）
            mzi: I 端 MZ 部分约束残余百分比（0-1）
            mbi: I 端 MB 部分约束残余百分比（0-1）
            fxj_state: J 端 FX 状态，0 = 释放，1 = 约束
            fyj_state: J 端 FY 状态，0 = 释放，1 = 约束
            fzj_state: J 端 FZ 状态，0 = 释放，1 = 约束
            mxj_state: J 端 MX 状态，0 = 释放，1 = 约束
            myj_state: J 端 MY 状态，0 = 释放，1 = 约束
            mzj_state: J 端 MZ 状态，0 = 释放，1 = 约束
            mbj_state: J 端 MB 状态，0 = 释放，1 = 约束
            fxj: J 端 FX 部分约束残余百分比（0-1）
            fyj: J 端 FY 部分约束残余百分比（0-1）
            fzj: J 端 FZ 部分约束残余百分比（0-1）
            mxj: J 端 MX 部分约束残余百分比（0-1）
            myj: J 端 MY 部分约束残余百分比（0-1）
            mzj: J 端 MZ 部分约束残余百分比（0-1）
            mbj: J 端 MB 部分约束残余百分比（0-1）

        Returns:
            ReleaseBoundary 对象

        Examples:
            >>> boundary_manager.create_release(None, 1,1,1,1,1,1,1,
            ...     1.0,1.0,1.0,1.0,1.0,1.0,1.0,
            ...     0,0,0,1,1,1,1,
            ...     0.0,0.0,0.0,1.0,1.0,1.0,1.0)
        '''
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_release(
            no, "RELEASE",
            fxi_state, fyi_state, fzi_state, mxi_state, myi_state, mzi_state, mbi_state,
            fxi, fyi, fzi, mxi, myi, mzi, mbi,
            fxj_state, fyj_state, fzj_state, mxj_state, myj_state, mzj_state, mbj_state,
            fxj, fyj, fzj, mxj, myj, mzj, mbj,
        )
        if not ok:
            raise RuntimeError(f"创建释放梁端约束 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_elstcspt(
        self,
        no: int | None,
        coor: int | str = "",
        x: bool = 1,
        dx: float | int = 1e13,
        y: bool = 1,
        dy: float | int = 1e13,
        z: bool = 1,
        dz: float | int = 1e13,
        rx: bool = 1,
        drx: float | int = 1e16,
        ry: bool = 1,
        dry: float | int = 1e16,
        rz: bool = 1,
        drz: float | int = 1e16,
    ) -> ElstcSptBoundary:
        '''创建节点弹性支承

        在节点 6 个自由度上分别设置弹性约束或固定约束。
        每个方向由一个标志位（0 = 弹性，1 = 固定）和对应的弹性刚度组成。
        注：弹性支撑与一般边界固定的自由度相同，且弹性支撑其余自由度上约束为零时，
        二者结果完全相同，不存在数值差异。

        Args:
            no: 边界编号，None 时自动分配
            coor: 局部坐标系编号，"" 代表缺省
            x: UX 方向，0 = 弹性，1 = 固定
            dx: 坐标系 X 轴方向的弹性支承刚度
            y: UY 方向，0 = 弹性，1 = 固定
            dy: 坐标系 Y 轴方向的弹性支承刚度
            z: UZ 方向，0 = 弹性，1 = 固定
            dz: 坐标系 Z 轴方向的弹性支承刚度
            rx: RX 方向，0 = 弹性，1 = 固定
            drx: 绕坐标系 X 轴方向的转动弹性刚度
            ry: RY 方向，0 = 弹性，1 = 固定
            dry: 绕坐标系 Y 轴方向的转动弹性刚度
            rz: RZ 方向，0 = 弹性，1 = 固定
            drz: 绕坐标系 Z 轴方向的转动弹性刚度

        Returns:
            ElstcSptBoundary 对象

        Examples:
            >>> boundary_manager.create_elstcspt(None)
        '''
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_elstcspt(
            no, "ELSTCSPT", coor or "", x, dx, y, dy, z, dz, rx, drx, ry, dry, rz, drz
        )
        if not ok:
            raise RuntimeError(f"创建弹性支承 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_general_elstcspt(
            self,
            no: int | None ,
            coor: int | str = "",
            *params: float | int,
            stiffness_matrix: list[float] | None = None,
            mass_matrix: list[float] | None = None,
            damping_matrix: list[float] | None = None,
    ) -> GeneralElstcSptBoundary:
        """创建一般弹性支承

        支持两种调用方式:
            1) OSIS 平铺（与命令流一致）::
                create(6, "GES", "", K11, K12, ..., K66, bM, bC, ...)
                → create_general_elstcspt("", K11, K12, ..., bM, bC, no=6)

            2) 列表写法（手写脚本）::
                create(6, "GES", coor="", stiffness_matrix=[...])

        Args:
            no: 边界编号，None 时自动分配
            coor: 局部坐标系编号，"" 代表缺省
            *params: OSIS 平铺参数（K11..K66, bM, [M..], bC, [C..]）
            stiffness_matrix: 6x6 刚度矩阵上三角元素（21 个值）
            mass_matrix: 6x6 质量矩阵上三角元素（21 个值），可选
            damping_matrix: 6x6 阻尼矩阵上三角元素（21 个值），可选

        Returns:
            GeneralElstcSptBoundary 对象
        """
        if no is None:
            no = self._next_no()

        if params:
            flat = params
        else:
            flat = list(stiffness_matrix or [])
            if mass_matrix:
                flat.append(1)
                flat.extend(mass_matrix)
            else:
                flat.append(0)
            if damping_matrix:
                flat.append(1)
                flat.extend(damping_matrix)
            else:
                flat.append(0)

        ok, err = osis_boundary_general_elstcspt(
            no, "GES", coor or "", *flat
        )
        if not ok:
            raise RuntimeError(f"创建一般弹性支承 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_rigid(
        self,
        no: int | None,
        node_i: int,
    ) -> Boundary:
        '''创建刚性连接

        将主节点 node_i 与通过 assign 分配的从节点绑定为刚性区域，
        刚性区域内所有节点的 6 个自由度保持完全一致。

        Args:
            no: 边界编号，None 时自动分配
            node_i: 节点1编号（刚性区域的主节点）

        Returns:
            Boundary 对象

        Notes:
            用于形成刚性区域的从节点号 node_j, node_k, ..., node_l 由 assign 方法定义。
        '''
        if no is None:
            no = self._next_no()
        ok, err = osis_boundary_rigid(no, "RIGID", node_i)
        if not ok:
            raise RuntimeError(f"创建刚性连接 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def delete(self, no: int) -> None:
        """删除边界

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        """
        deps = self.get_dependencies(no)
        raise_if_occupied("Boundary", deps, no=no)
        ok, err = osis_boundary_del(no)
        if not ok:
            raise RuntimeError(f"删除边界 {no} 失败: {err}")

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Boundary | list[Boundary | None] | None:
        '''根据编号获取单个或多个边界（O(k)）

        内部调用接口 GetBoundaryInfoByNos。

        Args:
            no: 边界编号，支持单个 int 或编号列表

        Returns:
            单个 Boundary 对象；如果传入列表则按顺序返回对象列表；
            不存在返回 None
        '''
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
        '''获取所有边界'''
        return self._load()

    def count(self) -> int:
        '''获取边界总数'''
        return len(self._load())

    def clear(self) -> None:
        '''清空所有边界

        逐个删除服务端的所有边界；若任一边界被占用则抛出异常。
        '''
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
            >>> bg = boundary_manager.group.create("桥台1")
            >>> bg.add(1, 2)
            >>> bg = boundary_manager.group.get("桥台1")
        """
        return self._group_manager

    def __repr__(self) -> str:
        return f"BoundaryManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

boundary_manager = BoundaryManager()
