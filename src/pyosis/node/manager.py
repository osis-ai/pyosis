"""节点管理器 - 统一管理节点的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护节点列表，通过 get/query 等方法查询
- 集成 io 层功能，提供完整的节点查询 API
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..core.client import osis_client
from .interface import osis_node, osis_node_del, osis_node_mod


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Load:
    """节点上的荷载"""

    load_case: str
    load_type: int


@dataclass(frozen=True)
class Node:
    """节点对象

    由 NodeManager 内部创建，用户不应直接实例化。
    """

    no: int
    x: float
    y: float
    z: float
    precision: int = 0
    hash_value: int = 0
    related_elements: list[int] = field(default_factory=list)
    related_boundaries: list[int] = field(default_factory=list)
    related_loads: list[Load] = field(default_factory=list)
    related_setl_grps: list[str] = field(default_factory=list)
    is_selected: bool = False
    is_plotted: bool = False
    is_free: bool = False

    # @property
    # def coord(self) -> tuple[float, float, float]:
    #     """节点坐标 (x, y, z)"""
    #     return (self.x, self.y, self.z)

    @classmethod
    def _from_dict(cls, d: dict) -> Node:
        """从接口 dict 构造 Node 对象（内部使用）"""
        return cls(
            no=d["no"],
            x=d["x"],
            y=d["y"],
            z=d["z"],
            precision=d.get("precision", 0),
            hash_value=d.get("hashValue", 0),
            related_elements=d.get("relatedElements",[]) or [],
            related_boundaries=d.get("relatedBoundaries",[]) or [],
            related_loads=d.get("relatedLoads",[]) or [],
            related_setl_grps=d.get("relatedSetlGrps",[]) or [],
            is_selected=d.get("isSelected", False),
            is_plotted=d.get("isPloted", False),
            is_free=d.get("isFree", False),
        )


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class NodeManager:
    """节点管理器

    统一管理节点的创建、删除、修改和查询。
    内部维护节点列表，通过 get/query 等方法查询。

    用法:
        >>> from pyosis.node import node_manager
        >>> node_manager.create(0, 0, 0)              # 创建节点（自动生成编号）
        >>> node_manager.create(1, 0, 0, 0)           # 创建节点（指定编号）
        >>> node = node_manager.get(1)                # 按编号查询
        >>> print(node.coord)                         # (0.0, 0.0, 0.0)
        >>> all_nodes = node_manager.all()            # 获取全部节点
        >>> node_manager.delete(1)                    # 删除节点
        >>> node_manager.renumber(1, 100)             # 修改编号
        >>> node_manager.modify(100, 100, 0, 0)       # 修改节点坐标
    """

    def __init__(self) -> None:
        # self._nodes: list[Node] = []
        # self._node_map: dict[int, Node] = {}  # 按编号索引：O(1) 查询
        # self._element_map: dict[int, list[Node]] = {}  # 按单元反向索引
        # self._loaded: bool = False
        ...

    # ── 数据加载 ──────────────────────────────

    # def _reload_get(self, no: int, what: str) -> Node:
    #     """创建/修改后从服务端重载并返回节点对象（内部使用）。"""
    #     self._loaded = False
    #     self._load()
    #     nd = self._node_map.get(no)
    #     if nd is None:
    #         raise RuntimeError(f"{what} {no} 成功但无法从服务端获取完整信息")
    #     return nd

    def _load(self) -> list[Node]:
        """从服务端加载所有节点信息（延迟加载，带缓存）"""
        resp = osis_client("GetAllNodeInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        nodes = [Node._from_dict(d) for d in resp.get("data", []) if "no" in d]
        return nodes
        # 构建索引：编号 -> 节点对象 (O(1) 查询)
        # self._node_map = {node.no: node for node in self._nodes}

        # # 构建反向索引：单元编号 -> 关联的节点列表 (O(k) 过滤)
        # self._element_map = {}
        # for node in self._nodes:
        #     for elem_no in node.related_elements:
        #         if elem_no not in self._element_map:
        #             self._element_map[elem_no] = []
        #         self._element_map[elem_no].append(node)

        # self._loaded = True

    # def refresh(self) -> None:
    #     """强制刷新缓存（模型变更后自动调用，也可手动调用）"""
    #     self._nodes = []
    #     self._node_map = {}
    #     # self._element_map = {}
    #     self._loaded = False
    #     self._load()

    # ── 增删改 ────────────────────────────────

    def _next_no(self) -> int:
        """生成下一个可用节点编号

        取已有节点编号的最大值+1，如果没有节点则从1开始。
        """
        nodes = self._load()
        node_no = [n.no for n in nodes]
        if len(node_no) == 0:
            return 1
        return max(node_no) + 1

    def create(self, x: float, y: float, z: float, no: int | None = None) -> Node:
        """创建节点

        Args:
            x, y, z: 节点坐标
            no: 节点编号，不指定时自动生成（取最大编号+1）

        Returns:
            创建的节点对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_node(no, x, y, z)
        if not ok:
            raise RuntimeError(f"创建节点 {no} 失败: {err}")
        return self.get(no)

    def delete(self, no: int) -> None:
        """删除节点

        Args:
            no: 节点编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_node_del(no)
        if not ok:
            raise RuntimeError(f"删除节点 {no} 失败: {err}")
        # self._loaded = False

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改节点编号

        Args:
            old_no: 旧编号
            new_no: 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_node_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改节点编号 {old_no} -> {new_no} 失败: {err}")
        # self._loaded = False

    def modify(self, no: int, x: float, y: float, z: float) -> None:
        """修改节点，编号不存在会自动创建

        Args:
            no: 节点编号
            x, y, z: 节点坐标

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        self.create(x, y, z, no=no)  # 直接调用 create 接口，编号存在时会覆盖

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Node | list[Node] | None:
        """根据编号获取单个节点 (O(1))

        Args:
            no: 节点编号

        Returns:
            Node 对象；节点不存在返回 None
        """
        nodes = self._load()
        if isinstance(no, int):
            return next((obj for obj in nodes if obj.no == no), None)
        if isinstance(no, list):
            return [next((obj for obj in nodes if obj.no == it), None) for it in no]
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")

    def all(self) -> list[Node]:
        """获取所有节点

        Returns:
            全部节点列表
        """
        nodes = self._load()
        return nodes

    def count(self) -> int:
        """获取节点总数

        Returns:
            节点数量
        """
        nodes = self._load()
        return len(nodes)

    def __repr__(self) -> str:
        # self._load()
        return f"NodeManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

node_manager = NodeManager()
