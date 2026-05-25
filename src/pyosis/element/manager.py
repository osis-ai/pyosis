"""单元管理器 - 统一管理单元的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护单元列表，通过 get 等方法查询，不暴露 HTTP 接口细节
- 按单元类型整型 ``type`` 解析为不同子类（与 boundary.manager 一致）

GetAllElementInfo 中 ``type``：1=BEAM3D，2=TRUSS，3=SPRING，4=CABLE，5=SHELL
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from enum import Enum
from ..core.client import osis_client
from .interface import (
    osis_element_beam3d,
    osis_element_truss,
    osis_element_spring,
    osis_element_cable,
    osis_element_shell,
    osis_element_del,
    osis_element_mod,
    osis_element_group,
    osis_taperele,
    osis_element_tapereledel,
    osis_element_taperelemod,
)


class ElementType(Enum):
    UNASSIGNED = 0
    BEAM3D = 1
    TRUSS = 2
    SPRING = 3
    CABLE = 4
    SHELL = 5



# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Element:
    """单元基类

    由 ElementManager 内部创建，用户不应直接实例化。
    """

    no: int
    element_type: ElementType  # BEAM3D, TRUSS, ...
    mat: int
    node_vec: list[int] = field(default_factory=list)   # 实际上就是 node_i 和 node_j
    node_i: int = 0
    node_j: int = 0
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    length: float = 0.0
    sec_vec: list[int] = field(default_factory=list)
    characters: list[int] = field(default_factory=list)
    loc_coor: dict[str, Any] | None = None
    weight: dict[str, Any] | None = None
    related_boundaries: list[int] = field(default_factory=list)
    related_loads: list[str] = field(default_factory=list)
    related_taper_eles: list[str] = field(default_factory=list)
    selected: bool = False
    plotted: bool = False

    @classmethod
    def _from_dict(cls, d: dict) -> Element:
        """从接口 dict 构造 Material 对象（内部使用）"""
        raw_type = int(d.get("type"))
        return cls(
            no=d.get("no"),
            element_type=ElementType(raw_type) if raw_type in [t.value for t in ElementType] else ElementType.UNASSIGNED,
            mat=d.get("mat"),
            node_vec=d.get("nodeVec"),
            node_i=d.get("nodeI"),
            node_j=d.get("nodeJ"),
            center=d.get("centerCoorPoint"),
            length=d.get("length"),
            sec_vec=d.get("secVec"),
            characters=d.get("characters"),
            loc_coor=d.get("locCoor"),
            related_boundaries=d.get("relatedBoundary"),
            related_loads=d.get("relatedLoad"),
            related_taper_eles=d.get("relatedTaperEles"),
            selected=d.get("selected"),
            plotted=d.get("ploted")
        )

    def __repr__(self) -> str:
        return f"Element(no={self.no}, type={self.element_type.name}, mat={self.mat}, nodes={self.node_vec})"


@dataclass(frozen=False)
class ElementGroup:
    """单元组对象

    由 ElementGroupManager 内部创建，用户不应直接实例化。
    字段与 HTTP 接口 GetAllElementGroupInfo 返回的 JSON 一一对应。
    """
    name: str                                    # 组名
    elements: list[int] = field(default_factory=list)      # 组内单元列表
    element_count: int = 0                       # 单元数量
    related_tendon_shapes: list[str] = field(default_factory=list)  # 关联的钢束形状
    related_tendon_shape_count: int = 0                             # 关联钢束形状数量
    related_lanes: list[str] = field(default_factory=list)          # 关联的车道
    related_lane_count: int = 0                                     # 关联车道数量
    related_stages: list[int] = field(default_factory=list)         # 关联的施工阶段
    related_stage_count: int = 0                                    # 关联施工阶段数量

    @classmethod
    def _from_dict(cls, d: dict) -> ElementGroup:
        """从接口 dict 构造 ElementGroup 对象（内部使用）"""
        return cls(
            name=d.get("groupName"),
            elements=list(d.get("elements")),
            element_count=d.get("elementCount"),
            related_tendon_shapes=list(d.get("relatedTendonShapes")),
            related_tendon_shape_count=d.get("relatedTendonShapeCount"),
            related_lanes=list(d.get("relatedLanes")),
            related_lane_count=d.get("relatedLaneCount"),
            related_stages=list(d.get("relatedStages")),
            related_stage_count=d.get("relatedStageCount"),
        )

    def _sync_from_dict(self, d: dict) -> None:
        """用 dict 同步当前对象（内部使用）"""
        self.name = d.get("groupName")
        self.elements = list(d.get("elements"))
        self.element_count = d.get("elementCount")
        self.related_tendon_shapes = list(d.get("relatedTendonShapes"))
        self.related_tendon_shape_count = d.get("relatedTendonShapeCount")
        self.related_lanes = list(d.get("relatedLanes"))
        self.related_lane_count = d.get("relatedLaneCount")
        self.related_stages = list(d.get("relatedStages"))
        self.related_stage_count = d.get("relatedStageCount")

    def refresh(self) -> ElementGroup:
        """刷新当前单元组对象并同步到对象属性"""
        resp = osis_client("GetElementGroupInfoByNames", {"name": [self.name]})
        if not resp['success']:
            raise RuntimeError(f"刷新单元组 {self.name} 失败: {resp['error']}")
        data = resp.get("data", [])
        if data and data[0]:
            self._sync_from_dict(data[0])
        return self

    def _execute(self, operation: str, param: list | None = None) -> None:
        """执行单元组底层操作（内部使用）"""
        ok, err = osis_element_group(self.name, operation, param)
        if not ok:
            raise RuntimeError(f"单元组操作 {self.name} ({operation}) 失败: {err}")

    def add(self, elements: list[int]) -> ElementGroup:
        """向单元组添加单元

        Args:
            elements: 单元编号列表

        Returns:
            更新后的 ElementGroup 对象
        """
        self._execute("a", elements)
        return self.refresh()

    def remove(self, elements: list[int]) -> ElementGroup:
        """从单元组移除单元

        Args:
            elements: 单元编号列表

        Returns:
            更新后的 ElementGroup 对象
        """
        self._execute("r", elements)
        return self.refresh()

    def replace(self, elements: list[int]) -> ElementGroup:
        """替换单元组内单元

        Args:
            elements: 新的单元编号列表

        Returns:
            更新后的 ElementGroup 对象
        """
        self._execute("s", elements)
        return self.refresh()

    def add_all(self) -> ElementGroup:
        """添加全部单元到组

        Returns:
            更新后的 ElementGroup 对象
        """
        self._execute("aa")
        return self.refresh()

    def remove_all(self) -> ElementGroup:
        """从组移除全部单元

        Returns:
            更新后的 ElementGroup 对象
        """
        self._execute("ra")
        return self.refresh()

    def rename(self, new_name: str) -> ElementGroup:
        """修改单元组名称

        Args:
            new_name: 新名称

        Returns:
            更新后的 ElementGroup 对象
        """
        self._execute("m", new_name)
        self.name = new_name
        return self.refresh()

    def __repr__(self) -> str:
        return f"ElementGroup(name={self.name!r}, elements={self.elements}, count={self.element_count})"

@dataclass(frozen=False)
class TaperEleGroup:
  """变截面单元组对象"""
  name: str = ""
  z_type: int = 0
  z_trans: float = 0.0
  z_pos: float = 0.0
  z_dis: float = 0.0
  y_type: int = 0
  y_trans: float = 0.0
  y_pos: float = 0.0
  y_dis: float = 0.0
  elements: list[int] = field(default_factory=list)
  @classmethod
  def _from_dict(cls, d: dict) -> TaperEleGroup:
      return cls(
          name=d.get("name"),
          z_type=d.get("zType"),
          z_trans=d.get("zTrans"),
          z_pos= d.get("zPos"),
          z_dis=d.get("zDis"),
          y_type=d.get("yType"),
          y_trans=d.get("yTrans"),
          y_pos=d.get("yPos"),
          y_dis=d.get("yDis"),
          elements=d.get("elements"),
      )

class ElementGroupManager:
    """单元组管理器

    统一管理单元组的创建、删除和查询。组成员操作在 ElementGroup 对象上进行。
    由 ElementManager 持有，不单独导出。

    用法:
        >>> from pyosis.element import element_manager
        >>> # 创建和查询
        >>> eg = element_manager.group.create("主梁单元")
        >>> eg = element_manager.group.get("主梁单元")
        >>> # 组成员操作（在对象上调用）
        >>> eg.add([1, 2, 3])
        >>> eg.remove([1])
        >>> eg.replace([4, 5])
    """

    def __init__(self) -> None:
        ...

    def _load(self) -> list[ElementGroup]:
        """从服务端加载所有单元组信息"""
        resp = osis_client("GetAllElementGroupInfo", {})
        if not resp["success"]:
            raise RuntimeError(resp["error"])
        
        groups = [
            ElementGroup._from_dict(d) 
            for d in resp.get("data", []) 
            if isinstance(d, dict) and "groupName" in d
        ]
        return groups

    # ── 增删改 ────────────────────────────────

    def create(self, name: str) -> ElementGroup:
        """创建单元组

        Args:
            name: 单元组名称

        Returns:
            ElementGroup: 创建的单元组对象
        """
        ok, err = osis_element_group(name, "c")
        if not ok:
            raise RuntimeError(f"创建单元组 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除单元组

        Args:
            name: 单元组名称
        """
        ok, err = osis_element_group(name, "d")
        if not ok:
            raise RuntimeError(f"删除单元组 {name} 失败: {err}")

    # ── 查询 ──────────────────────────────────

    def get(self, name: str | list[str]) -> ElementGroup | list[ElementGroup | None] | None:
        """根据名称获取单个或多个单元组

        Args:
            name: 单元组名称，支持单个名称或名称列表

        Returns:
            单个 ElementGroup 对象；如果传入列表则返回对象列表；
            不存在返回 None
        """

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetElementGroupInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        element_groups = [ElementGroup._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(element_groups) == 0:
            return None
        elif len(element_groups) == 1:
            return element_groups[0]
        return element_groups

    def all(self) -> list[ElementGroup]:
        """获取所有单元组

        Returns:
            全部单元组列表
        """
        return self._load()

    def count(self) -> int:
        """获取单元组总数

        Returns:
            单元组数量
        """
        return len(self._load())

    def __repr__(self) -> str:
        return f"ElementGroupManager()"


# ──────────────────────────────────────────────
# TaperEleGroup 管理类
# ──────────────────────────────────────────────

class TaperEleGroupManager:
    """变截面单元组信息"""

    def __init__(self) -> None:
        ...
    def _load(self) -> list[TaperEleGroup]:
        """从服务端加载所有变截面单元组信息"""
        resp = osis_client("GetAllTaperEleGroupInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        taper_ele_groups = [TaperEleGroup._from_dict(d) for d in resp.get("data", []) if "name" in d]
        return taper_ele_groups

    def create(
        self,
        name: str,
        z_type: Literal[0, 1],
        z_trans: float = 1.0,
        z_pos: Literal[0, 1] = 0,
        z_dis: float = 0.0,
        y_type: Literal[0, 1] = 0,
        y_trans: float = 1.0,
        y_pos: Literal[0, 1] = 0,
        y_dis: float = 0.0,
        *eles: str,

    ) -> TaperEleGroup:
        """
        生成或修改变截面单元组

        Args:
            name (str): 变截面单元组名称
            z_type (int): 截面Z向过渡类型，
                * 0=线性
                * 1=多项式
            z_trans (float): ZType=0时默认1.0
            z_pos (int):
                * 0=i
                * 1=j
                * ZType=0时默认i
            z_dis (float): 对称面距，ZType=0时默认0.0
            y_type (int): 截面Y向过渡类型
                * 0=线性
                * 1=多项式
            y_trans (float): YType=0时默认1.0
            y_pos (int):
                * 0=i
                * 1=j
                * YType=0时默认i
            y_dis (float): 对称面距，YType=0时默认0.0
            *eles (str): 单元组编号，示例：1,3,5to10

        Returns:
            tuple (bool, str): 返回一个元组，包含：
                - bool: 操作是否成功
                - str: 失败原因
        """
        ok, err = osis_taperele(
            name,
            z_type,
            z_trans,
            z_pos,
            z_dis,
            y_type,
            y_trans,
            y_pos,
            y_dis,
            *eles,
        )
        if not ok:
            raise RuntimeError(f"创建变截面单元组 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        ok, err = osis_element_tapereledel(name)
        if not ok:
            raise RuntimeError(f"删除变截面单元组 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> TaperEleGroup:
        ok, err = osis_element_taperelemod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名变截面单元组 {old_name} -> {new_name} 失败: {err}")
        return self.get(new_name)

    def get(self, name: str | list[str]) -> TaperEleGroup | list[TaperEleGroup | None] | None:
        """根据名称获取变截面单元组
        Args:
            name: 变截面单元组名称
            name: 变截面单元组名称，支持单个名称或名称列表
        Returns:
            TaperEleGroup | list[TaperEleGroup | None]: 变截面单元组对象
        """

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        resp = osis_client("GetTaperEleGroupInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")  
        taper_ele_groups = [
            TaperEleGroup._from_dict(d) if d else None
            for d in resp.get("data", [])
            if "name" in d
        ]
        if len(taper_ele_groups) == 0:
            return None
        elif len(taper_ele_groups) == 1:
            return taper_ele_groups[0]
        return taper_ele_groups

    def all(self) -> list[TaperEleGroup]:
        """获取所有变截面单元组"""
        return self._load()

    def __repr__(self) -> str:
        return f"TaperEleGroupManager()"

# ──────────────────────────────────────────────
# 单元管理类
# ──────────────────────────────────────────────


class ElementManager:
    """单元管理器

    统一管理单元的创建、删除、修改和查询。

    用法:
        >>> from pyosis.element import element_manager
        >>> elem = element_manager.create_beam3d(1, 2, nMat=1, nSec1=1, nSec2=1)
        >>> elem.no
        >>> elem.element_type
        >>> all_elems = element_manager.all()
        >>> element_manager.delete(elem.no)
        >>> element_manager.renumber(elem.no, 100)
        >>> 
        >>> # 单元组操作
        >>> element_manager.group.create("主梁单元")
        >>> element_manager.group.add("主梁单元", [1, 2, 3])
        >>> eg = element_manager.group.get("主梁单元")
    """

    def __init__(self) -> None:
        self._element_manager = ElementGroupManager()
        self._taper_ele_group_manager = TaperEleGroupManager() # 变截面单元组

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> list[Element]:
        """从服务端加载所有单元信息"""
        resp = osis_client("GetAllElementInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        elements = [
            Element._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "no" in d
        ]
        return elements

    def _next_no(self) -> int:
        """生成下一个可用单元编号"""
        elements = self._load()        
        if len(elements) == 0:
            return 1
        ele_no = [ele.no for ele in elements]
        return max(ele_no) + 1

    # ── 增删改 ────────────────────────────────

    def create_beam3d(
        self,
        node1: int,
        node2: int,
        nMat: int,
        nSec1: int,
        nSec2: int,
        nYTrans: Literal[1, 2, 3, 4] = 1,
        nZTrans: Literal[1, 2, 3, 4] = 1,
        dStrain: float = 0.0,
        bFlag: int = 0,
        dTheta: float = 0,
        bWarping: int = 0,
        no: int | None = None,
    ) -> Element:
        """创建梁柱单元"""
        if no is None:
            no = self._next_no()
        ok, err = osis_element_beam3d(
            no, "BEAM3D", node1, node2, nMat, nSec1, nSec2,
            nYTrans, nZTrans, dStrain, bFlag, dTheta, bWarping
        )
        if not ok:
            raise RuntimeError(f"创建梁单元 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_truss(
        self,
        node1: int,
        node2: int,
        nMat: int,
        nSec1: int,
        nSec2: int,
        dStrain: float = 0.0,
        no: int | None = None,
    ) -> Element:
        """创建桁架单元"""
        if no is None:
            no = self._next_no()
        ok, err = osis_element_truss(no, "TRUSS", node1, node2, nMat, nSec1, nSec2, dStrain)
        if not ok:
            raise RuntimeError(f"创建桁架单元 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_spring(
        self,
        node1: int,
        node2: int,
        bLinear: int = 1,
        dx: float = 10,
        dy: float = 10,
        dz: float = 10,
        rx: float = 10,
        ry: float = 10,
        rz: float = 10,
        dBeta: float = 0.0,
        no: int | None = None,
    ) -> Element:
        """创建弹簧单元"""
        if no is None:
            no = self._next_no()
        ok, err = osis_element_spring(
            no, "SPRING", node1, node2, bLinear, dx, dy, dz, rx, ry, rz, dBeta
        )
        if not ok:
            raise RuntimeError(f"创建弹簧单元 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_cable(
        self,
        node1: int,
        node2: int,
        nMat: int,
        nSec: int,
        eMethod: Literal["UL", "IF", "HF", "VF", "IS"] = "UL",
        dPara: float = 10.0,
        no: int | None = None,
    ) -> Element:
        """创建拉索单元"""
        if no is None:
            no = self._next_no()
        ok, err = osis_element_cable(no, "CABLE", node1, node2, nMat, nSec, eMethod, dPara)
        if not ok:
            raise RuntimeError(f"创建拉索单元 {no} 失败: {err}")
        return self.get(no)  # type: ignore[return-value]

    def create_shell(
        self,
        node1: int,
        node2: int,
        node3: int,
        nMat: int,
        nThk: int,
        bIsThin: int = 1,
        node4: int | None = None,
        no: int | None = None,
    ) -> Element:
        """创建壳单元"""
        if no is None:
            no = self._next_no()
        ok, err = osis_element_shell(no, "SHELL", bIsThin, nMat, nThk, node1, node2, node3, node4)
        if not ok:
            raise RuntimeError(f"创建壳单元 {no} 失败: {err}")
        return self.get(no)

    def delete(self, no: int) -> None:
        """删除单元"""
        ok, err = osis_element_del(no)
        if not ok:
            raise RuntimeError(f"删除单元 {no} 失败: {err}")

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改单元编号"""
        ok, err = osis_element_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改单元编号 {old_no} -> {new_no} 失败: {err}")
        return self.get(new_no)

    # 下面的函数可能没有必要，直接重新调用创建函数就能修改了
    # def modify(self, no: int, **kwargs) -> None:
    #     """修改单元,编号不存在会抛出异常,修改时需要提供完整参数"""
    #     ele = self.get(no)
    #     if ele is None:
    #         raise RuntimeError(f"单元 {no} 不存在，无法修改")

    #     element_type = kwargs.pop("element_type", None)

    #     if element_type is None:
    #         raise RuntimeError("必须提供 element_type 来指定单元类型")

    #     kwargs["no"] = no

    #     if element_type.upper() == "BEAM3D":
    #         self.create_beam3d(**kwargs)
    #     elif element_type.upper() == "TRUSS":
    #         self.create_truss(**kwargs)
    #     elif element_type.upper() == "SPRING":
    #         self.create_spring(**kwargs)
    #     elif element_type.upper() == "CABLE":
    #         self.create_cable(**kwargs)
    #     elif element_type.upper() == "SHELL":
    #         self.create_shell(**kwargs)
    #     else:
    #         raise RuntimeError(f"不支持的单元类型: {element_type}")

    #     return self.get(no)

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Element | list[Element | None] | None:
        """根据编号获取单个或多个单元 (O(k))"""
        if isinstance(no, int):
            no = [no]
        elif isinstance(no, list):
            ...
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")
        resp = osis_client("GetElementInfoByNos", {"no": no})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        eles = [Element._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(eles) == 0:     # 有问题
            return None
        elif len(eles) == 1:   # 只查了一个
            return eles[0]
        return eles
    
    def all(self) -> list[Element]:
        """获取所有单元"""
        elements  = self._load()
        return elements

    def count(self) -> int:
        """获取单元总数"""
        elements = self._load()
        return len(elements)


    # ── 子管理器 ──────────────────────────────

    @property
    def group(self) -> ElementGroupManager:
        """单元组管理器

        提供单元组的增删改查功能。

        用法:
            >>> element_manager.group.create("主梁1")
            >>> element_manager.group.add("主梁1", [1, 2])
            >>> element_manager.group.get("主梁1")
        """
        return self._element_manager

    @property
    def taper_group(self) -> TaperEleGroupManager:
        """变截面单元组管理器

        提供变截面单元组的查询功能。
        用法:
            >>> element_manager.taper_group.all()
            >>> element_manager.taper_group.get([1, 2, 3])
        """
        return self._taper_ele_group_manager

    def __repr__(self) -> str:
        return f"ElementManager()"

# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

element_manager = ElementManager()
