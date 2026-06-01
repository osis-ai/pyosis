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
    related_loads: list[str] = field(default_factory=list)
    related_setl_grps: list[str] = field(default_factory=list)
    selected: bool = False
    plotted: bool = False
    free: bool = False

    # @property
    # def coord(self) -> tuple[float, float, float]:
    #     """节点坐标 (x, y, z)"""
    #     return (self.x, self.y, self.z)

    @classmethod
    def _from_dict(cls, d: dict) -> Node:
        """从接口 dict 构造 Node 对象（内部使用）"""
        return cls(
            no=d["no"],
            # x=d.get("coordinate")["x"],
            # y=d.get("coordinate")["y"],
            # z=d.get("coordinate")["z"],
            x=d.get("x"),
            y=d.get("y"),
            z=d.get("z"),
            precision=d.get("precision"),
            hash_value=d.get("hashValue"),
            related_elements=d.get("relatedElements"),
            related_boundaries=d.get("relatedBoundaries"),
            related_loads=d.get("relatedLoads"),
            related_setl_grps=d.get("relatedSetlGrps"),
            selected=d.get("selected"),
            plotted=d.get("ploted"),
            free=d.get("free"),
        )
    
    def __repr__(self) -> str:
        return f"Node(no={self.no}, x={self.x}, y={self.y}, z={self.z})"


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
        >>> node_manager.create(0, 0, 0, 1)           # 创建节点（指定编号）
        >>> node = node_manager.get(1)                # 按编号查询
        >>> print(node.coord)                         # (0.0, 0.0, 0.0)
        >>> all_nodes = node_manager.all()            # 获取全部节点
        >>> node_manager.delete(1)                    # 删除节点
        >>> node_manager.renumber(1, 100)             # 修改编号
        >>> node_manager.modify(100, 100, 0, 0)       # 修改节点坐标
    """

    def __init__(self) -> None:
        ...

    # ── 数据加载 ──────────────────────────────
    
    def _load(self) -> list[Node]:
        """从服务端加载所有节点信息（延迟加载，带缓存）"""
        resp = osis_client("GetAllNodeInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        nodes = [Node._from_dict(d) for d in resp.get("data", []) if "no" in d]
        return nodes
    
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

    # 该函数或许不需要，直接创建即可覆盖
    # def modify(self, no: int, x: float, y: float, z: float) -> None:
    #     """修改节点，编号不存在会自动创建

    #     Args:
    #         no: 节点编号
    #         x, y, z: 节点坐标

    #     Raises:
    #         RuntimeError: 修改失败时抛出异常
    #     """
    #     return self.create(x, y, z, no=no)  # 直接调用 create 接口，编号存在时会覆盖

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Node | list[Node] | None:
        """根据编号获取 N 个节点 (O(N))

        Args:
            no: 节点编号

        Returns:
            Node 对象；节点不存在返回 None
        """
        if isinstance(no, int):
            no = [no]
        elif isinstance(no, list):
            ...
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")
        resp = osis_client("GetNodeInfoByNos", {"no": no})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        nodes = [Node._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(nodes) == 0:     # 有问题
            return None
        elif len(nodes) == 1:   # 只查了一个
            return nodes[0]
        return nodes

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

    def clear(self)->None:
        """清空所有节点"""
        try:
            [self.delete(n.no) for n in self.all()]
        except Exception as e:
            raise Exception(f"清空所有节点失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        # self._load()
        return f"NodeManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

node_manager = NodeManager()
