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

from ..core.client import osis_client
from .interface import (
    osis_element_beam3d,
    osis_element_truss,
    osis_element_spring,
    osis_element_cable,
    osis_element_shell,
    osis_element_del,
    osis_element_mod,
)


# 与服务端 type 字段对应（见 io/element_info）
ELEMENT_TYPE_NAMES: dict[int, str] = {
    1: "BEAM3D",
    2: "TRUSS",
    3: "SPRING",
    4: "CABLE",
    5: "SHELL",
}


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Element:
    """单元基类

    由 ElementManager 内部创建，用户不应直接实例化。
    """

    no: int
    raw_type: int
    element_type: str  # BEAM3D, TRUSS, ...
    mat: int
    node_vec: list[int] = field(default_factory=list)
    node_i: int = 0
    node_j: int = 0
    length: float = 0.0
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    sec_vec: list[int] = field(default_factory=list)
    characters: list[int] = field(default_factory=list)
    loc_coor: dict[str, Any] | None = None

    def __repr__(self) -> str:
        return f"Element(no={self.no}, type={self.element_type})"


@dataclass(frozen=True)
class Beam3dElement(Element):
    """梁柱单元（type=1）"""

    beta: float = 0.0
    beta_flag: bool = False
    comp_thk: float = 0.0
    is_taper: bool = False
    key_pt: int = -1
    strain: float = 0.0
    trans_vec: list[int] = field(default_factory=list)
    warp: bool = False
    section_details: list[dict[str, Any]] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Beam3dElement(no={self.no}, nodeI={self.node_i}, nodeJ={self.node_j}, mat={self.mat})"


@dataclass(frozen=True)
class TrussElement(Element):
    """桁架单元（type=2）"""

    def __repr__(self) -> str:
        return f"TrussElement(no={self.no}, nodeI={self.node_i}, nodeJ={self.node_j})"


@dataclass(frozen=True)
class SpringElement(Element):
    """弹簧单元（type=3）"""

    def __repr__(self) -> str:
        return f"SpringElement(no={self.no}, nodeI={self.node_i}, nodeJ={self.node_j})"


@dataclass(frozen=True)
class CableElement(Element):
    """拉索单元（type=4）"""

    def __repr__(self) -> str:
        return f"CableElement(no={self.no}, nodeI={self.node_i}, nodeJ={self.node_j})"


@dataclass(frozen=True)
class ShellElement(Element):
    """壳单元（type=5）"""

    is_thin: bool = True
    thickness: int = 0
    node_sum: int | None = None

    def __repr__(self) -> str:
        return f"ShellElement(no={self.no}, nodeVec={self.node_vec}, mat={self.mat})"


# ──────────────────────────────────────────────
# 管理类
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
    """

    def __init__(self) -> None:
        self._elements: list[Element] = []
        self._elem_map: dict[int, Element] = {}
        self._loaded: bool = False

    # ── 数据加载 ──────────────────────────────

    def _reload_get_as(self, no: int, expected_cls: type[Element], what: str) -> Element:
        """创建/修改后从服务端重载并返回指定类型对象（内部使用）。"""
        self._loaded = False
        self._load()
        elem = self._elem_map.get(no)
        if elem is None:
            raise RuntimeError(f"{what} {no} 成功但无法从服务端获取完整信息")
        if not isinstance(elem, expected_cls):
            raise RuntimeError(f"{what} {no} 成功但返回类型错误: {type(elem)}")
        return elem

    def _parse_element(self, d: dict) -> Element:
        """根据 ``type`` 整型解析为对应子类。"""
        raw = int(d.get("type", 0) or 0)
        name = ELEMENT_TYPE_NAMES.get(raw, "UNKNOWN")

        common: dict[str, Any] = dict(
            no=int(d["no"]),
            raw_type=raw,
            element_type=name,
            mat=int(d.get("mat", 0) or 0),
            node_vec=list(d.get("nodeVec") or []),
            node_i=int(d.get("nodeI", 0) or 0),
            node_j=int(d.get("nodeJ", 0) or 0),
            length=float(d.get("length", 0.0) or 0.0),
            center=tuple(d.get("center", [0.0, 0.0, 0.0])),
            sec_vec=list(d.get("secVec") or []),
            characters=list(d.get("characters") or []),
            loc_coor=d.get("locCoor"),
        )

        if raw == 1:
            return Beam3dElement(
                **common,
                beta=float(d.get("beta", 0.0) or 0.0),
                beta_flag=bool(d.get("betaFlag", False)),
                comp_thk=float(d.get("compThk", 0.0) or 0.0),
                is_taper=bool(d.get("isTaper", False)),
                key_pt=int(d.get("keyPt", -1) or -1),
                strain=float(d.get("strain", 0.0) or 0.0),
                trans_vec=list(d.get("transVec") or []),
                warp=bool(d.get("warp", False)),
                section_details=list(d.get("sectionDetails") or []),
            )
        if raw == 2:
            return TrussElement(**common)
        if raw == 3:
            return SpringElement(**common)
        if raw == 4:
            return CableElement(**common)
        if raw == 5:
            return ShellElement(
                **common,
                is_thin=bool(d.get("isThin", True)),
                thickness=int(d.get("thickness", 0) or 0),
                node_sum=None if d.get("nodeSum") in (None, "") else int(d["nodeSum"]),
            )
        return Element(**common)

    def _load(self) -> None:
        """从服务端加载所有单元信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllElementInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        self._elements = [
            self._parse_element(d) for d in resp.get("data", []) if isinstance(d, dict) and "no" in d
        ]
        self._elem_map = {elem.no: elem for elem in self._elements}
        self._loaded = True

    def refresh(self) -> None:
        """强制刷新缓存（模型变更后自动调用，也可手动调用）"""
        self._elements = []
        self._elem_map = {}
        self._loaded = False
        self._load()

    def _next_no(self) -> int:
        """生成下一个可用单元编号"""
        self._load()
        if not self._elements:
            return 1
        return max(elem.no for elem in self._elements) + 1

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
    ) -> Beam3dElement:
        """创建梁柱单元"""
        self.refresh()
        if no is None:
            no = self._next_no()
        ok, err = osis_element_beam3d(
            no, "BEAM3D", node1, node2, nMat, nSec1, nSec2,
            nYTrans, nZTrans, dStrain, bFlag, dTheta, bWarping
        )
        if not ok:
            raise RuntimeError(f"创建梁单元 {no} 失败: {err}")
        return self._reload_get_as(no, Beam3dElement, "创建梁单元")  # type: ignore[return-value]

    def create_truss(
        self,
        node1: int,
        node2: int,
        nMat: int,
        nSec1: int,
        nSec2: int,
        dStrain: float = 0.0,
        no: int | None = None,
    ) -> TrussElement:
        """创建桁架单元"""
        self.refresh()
        if no is None:
            no = self._next_no()
        ok, err = osis_element_truss(no, "TRUSS", node1, node2, nMat, nSec1, nSec2, dStrain)
        if not ok:
            raise RuntimeError(f"创建桁架单元 {no} 失败: {err}")
        return self._reload_get_as(no, TrussElement, "创建桁架单元")  # type: ignore[return-value]

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
    ) -> SpringElement:
        """创建弹簧单元"""
        self.refresh()
        if no is None:
            no = self._next_no()
        ok, err = osis_element_spring(
            no, "SPRING", node1, node2, bLinear, dx, dy, dz, rx, ry, rz, dBeta
        )
        if not ok:
            raise RuntimeError(f"创建弹簧单元 {no} 失败: {err}")
        return self._reload_get_as(no, SpringElement, "创建弹簧单元")  # type: ignore[return-value]

    def create_cable(
        self,
        node1: int,
        node2: int,
        nMat: int,
        nSec: int,
        eMethod: Literal["UL", "IF", "HF", "VF", "IS"] = "UL",
        dPara: float = 10.0,
        no: int | None = None,
    ) -> CableElement:
        """创建拉索单元"""
        self.refresh()
        if no is None:
            no = self._next_no()
        ok, err = osis_element_cable(no, "CABLE", node1, node2, nMat, nSec, eMethod, dPara)
        if not ok:
            raise RuntimeError(f"创建拉索单元 {no} 失败: {err}")
        return self._reload_get_as(no, CableElement, "创建拉索单元")  # type: ignore[return-value]

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
    ) -> ShellElement:
        """创建壳单元"""
        self.refresh()
        if no is None:
            no = self._next_no()
        ok, err = osis_element_shell(no, "SHELL", bIsThin, nMat, nThk, node1, node2, node3, node4)
        if not ok:
            raise RuntimeError(f"创建壳单元 {no} 失败: {err}")
        return self._reload_get_as(no, ShellElement, "创建壳单元")  # type: ignore[return-value]

    def delete(self, no: int) -> None:
        """删除单元"""
        ok, err = osis_element_del(no)
        if not ok:
            raise RuntimeError(f"删除单元 {no} 失败: {err}")
        self._loaded = False

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改单元编号"""
        ok, err = osis_element_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改单元编号 {old_no} -> {new_no} 失败: {err}")
        self._loaded = False

    def modify(self, no: int, **kwargs) -> None:
        """修改单元,编号不存在会抛出异常,修改时需要提供完整参数"""
        ele = self.get(no)
        if ele is None:
            raise RuntimeError(f"单元 {no} 不存在，无法修改")

        element_type = kwargs.pop("element_type", None)

        if element_type is None:
            raise RuntimeError("必须提供 element_type 来指定单元类型")

        kwargs["no"] = no

        if element_type == "BEAM3D":
            self.create_beam3d(**kwargs)
        elif element_type == "TRUSS":
            self.create_truss(**kwargs)
        elif element_type == "SPRING":
            self.create_spring(**kwargs)
        elif element_type == "CABLE":
            self.create_cable(**kwargs)
        elif element_type == "SHELL":
            self.create_shell(**kwargs)
        else:
            raise RuntimeError(f"不支持的单元类型: {element_type}")

        self._loaded = False

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Element | list[Element | None]:
        """根据编号获取单个或多个单元 (O(k))"""
        self._load()
        if isinstance(no, int):
            return self._elem_map.get(no)
        if isinstance(no, list):
            return [self._elem_map.get(n) for n in no]
        raise TypeError(f"不支持的编号类型: {type(no)}")

    def all(self) -> list[Element]:
        """获取所有单元"""
        self._load()
        return list(self._elements)

    def count(self) -> int:
        """获取单元总数"""
        self._load()
        return len(self._elements)

    def __repr__(self) -> str:
        self._load()
        return f"ElementManager(count={len(self._elements)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

element_manager = ElementManager()
