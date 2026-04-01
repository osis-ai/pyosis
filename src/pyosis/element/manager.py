"""单元管理器 - 统一管理单元的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护单元列表，通过 get 等方法查询，不暴露 HTTP 接口细节

支持的单元类型：BEAM3D、TRUSS、SPRING、CABLE、SHELL
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

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


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Element:
    """单元对象

    由 ElementManager 内部创建，用户不应直接实例化。
    """

    no: int
    element_type: str  # "BEAM3D", "TRUSS", "SPRING", "CABLE", "SHELL"
    mat: int
    node_vec: list[int] = field(default_factory=list)
    node_i: int = 0
    node_j: int = 0
    length: float = 0.0
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    sec_vec: list[int] = field(default_factory=list)
    characters: str = ""

    @classmethod
    def _from_dict(cls, d: dict) -> Element:
        """从接口 dict 构造 Element 对象（内部使用）"""
        return cls(
            no=d["no"],
            element_type=d.get("type", "UNKNOWN"),
            mat=d.get("mat", 0),
            node_vec=d.get("nodeVec", []),
            node_i=d.get("nodeI", 0),
            node_j=d.get("nodeJ", 0),
            length=d.get("length", 0.0),
            center=tuple(d.get("center", [0.0, 0.0, 0.0])),
            sec_vec=d.get("secVec", []),
            characters=d.get("characters", ""),
        )


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class ElementManager:
    """单元管理器

    统一管理单元的创建、删除、修改和查询。

    用法:
        >>> from pyosis.element import element_manager
        >>> element_manager.create_beam3d(1, 1, 2, nMat=1, nSec1=1, nSec2=1)  # 创建梁单元
        >>> element = element_manager.get(1)                                   # 按编号查询
        >>> all_elems = element_manager.all()                                  # 获取全部单元
        >>> element_manager.delete(1)                                          # 删除单元
        >>> element_manager.renumber(1, 100)                                   # 修改编号
    """

    def __init__(self) -> None:
        self._elements: list[Element] = []
        self._elem_map: dict[int, Element] = {}  # 按编号索引：O(1) 查询
        self._loaded: bool = False

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有单元信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllElementInfo", {})
        if isinstance(resp, tuple):
            raise RuntimeError(f"加载单元信息失败: {resp[1]}")
        self._elements = [
            Element._from_dict(d) for d in resp.get("data", []) if "no" in d
        ]

        # 构建索引：编号 -> 单元对象 (O(1) 查询)
        self._elem_map = {elem.no: elem for elem in self._elements}

        self._loaded = True

    def refresh(self) -> None:
        """强制刷新缓存（模型变更后自动调用，也可手动调用）"""
        self._elements = []
        self._elem_map = {}
        self._loaded = False
        self._load()

    # ── 增删改 ────────────────────────────────

    def create_beam3d(
        self,
        no: int,
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
    ) -> None:
        """创建梁柱单元

        Args:
            no: 单元编号
            node1: 节点1编号
            node2: 节点2编号
            nMat: 材料编号
            nSec1: 截面1编号
            nSec2: 截面2编号
            nYTrans: y轴截面变化次方，可选值：1, 2, 3, 4
            nZTrans: z轴截面变化次方，可选值：1, 2, 3, 4
            dStrain: 应变值，默认为 0.0
            bFlag: 轴向转角定义方式，0=beta角，1=关键点
            dTheta: 轴向转角参数
            bWarping: 翘曲效应标志，0=不考虑，1=考虑

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_element_beam3d(
            no, "BEAM3D", node1, node2, nMat, nSec1, nSec2,
            nYTrans, nZTrans, dStrain, bFlag, dTheta, bWarping
        )
        if not ok:
            raise RuntimeError(f"创建梁单元 {no} 失败: {err}")
        self._loaded = False

    def create_truss(
        self,
        no: int,
        node1: int,
        node2: int,
        nMat: int,
        nSec1: int,
        nSec2: int,
        dStrain: float = 0.0,
    ) -> None:
        """创建桁架单元

        Args:
            no: 单元编号
            node1: 节点1编号
            node2: 节点2编号
            nMat: 材料编号
            nSec1: 截面1编号
            nSec2: 截面2编号
            dStrain: 应变值，默认为 0.0

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_element_truss(no, "TRUSS", node1, node2, nMat, nSec1, nSec2, dStrain)
        if not ok:
            raise RuntimeError(f"创建桁架单元 {no} 失败: {err}")
        self._loaded = False

    def create_spring(
        self,
        no: int,
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
    ) -> None:
        """创建弹簧单元

        Args:
            no: 单元编号
            node1: 节点1编号
            node2: 节点2编号
            bLinear: 弹簧类型，1=线性，0=非线性
            dx: x方向参数（刚度或力-位移曲线编号）
            dy: y方向参数
            dz: z方向参数
            rx: 绕x轴旋转参数
            ry: 绕y轴旋转参数
            rz: 绕z轴旋转参数
            dBeta: 轴向转角

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_element_spring(
            no, "SPRING", node1, node2, bLinear, dx, dy, dz, rx, ry, rz, dBeta
        )
        if not ok:
            raise RuntimeError(f"创建弹簧单元 {no} 失败: {err}")
        self._loaded = False

    def create_cable(
        self,
        no: int,
        node1: int,
        node2: int,
        nMat: int,
        nSec: int,
        eMethod: Literal["UL", "IF", "HF", "VF", "IS"] = "UL",
        dPara: float = 10.0,
    ) -> None:
        """创建拉索单元

        Args:
            no: 单元编号
            node1: 节点1编号
            node2: 节点2编号
            nMat: 材料编号
            nSec: 截面编号
            eMethod: 拉索参数定义方法，可选值：UL, IF, HF, VF, IS
            dPara: 拉索参数值

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_element_cable(no, "CABLE", node1, node2, nMat, nSec, eMethod, dPara)
        if not ok:
            raise RuntimeError(f"创建拉索单元 {no} 失败: {err}")
        self._loaded = False

    def create_shell(
        self,
        no: int,
        node1: int,
        node2: int,
        node3: int,
        nMat: int,
        nThk: int,
        bIsThin: int = 1,
        node4: int | None = None,
    ) -> None:
        """创建壳单元

        Args:
            no: 单元编号
            node1: 节点1编号
            node2: 节点2编号
            node3: 节点3编号
            nMat: 材料编号
            nThk: 厚度编号
            bIsThin: 壳类型，1=薄壳，0=厚壳
            node4: 节点4编号（可选，四边形壳需要）

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_element_shell(no, "SHELL", bIsThin, nMat, nThk, node1, node2, node3, node4)
        if not ok:
            raise RuntimeError(f"创建壳单元 {no} 失败: {err}")
        self._loaded = False

    def delete(self, no: int) -> None:
        """删除单元

        Args:
            no: 单元编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_element_del(no)
        if not ok:
            raise RuntimeError(f"删除单元 {no} 失败: {err}")
        self._loaded = False

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改单元编号

        Args:
            old_no: 旧编号
            new_no: 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_element_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改单元编号 {old_no} -> {new_no} 失败: {err}")
        self._loaded = False

    def modify(self, no: int, **kwargs) -> None:
        """修改单元，编号不存在会自动创建，修改时需要提供完整参数

        Args:
            no: 单元编号
            kwargs: 完整的单元属性

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ele = self.get(no)
        if ele is None:
            raise RuntimeError(f"单元 {no} 不存在，无法修改")

        # 👇 关键：先取出类型，剩下的参数才传给创建函数
        element_type = kwargs.pop("element_type", None)

        if element_type is None:
            raise RuntimeError("必须提供 element_type 来指定单元类型")

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
        """根据编号获取单个或多个单元 (O(k))

        Args:
            no: 单元编号

        Returns:
            Element 对象或数组；单元不存在返回 None
        """
        self._load()
        if isinstance(no, int):
            return self._elem_map.get(no)
        elif isinstance(no, list):
            return [self._elem_map.get(n) for n in no]
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")

    def all(self) -> list[Element]:
        """获取所有单元

        Returns:
            全部单元列表
        """
        self._load()
        return list(self._elements)

    def count(self) -> int:
        """获取单元总数

        Returns:
            单元数量
        """
        self._load()
        return len(self._elements)

    def __repr__(self) -> str:
        self._load()
        return f"ElementManager(count={len(self._elements)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

element_manager = ElementManager()
