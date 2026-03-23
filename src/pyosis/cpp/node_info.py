# cpp/node_info.py

from ..core.client import osis_client
from .response import OSISResponse


class NodeInfoResponse(OSISResponse):
    """
    GetAllNodeInfo 接口返回封装

    返回格式:
        {
            "success": true,
            "data": [
                {
                    "no": int,
                    "x": float, "y": float, "z": float,
                    "precision": int,
                    "hashValue": int,
                    "relatedElements": [int, ...],
                    "relatedBoundaries": [int, ...],
                    "relatedLoads": [{"loadCase": str, "loadType": int}, ...],
                    "relatedSetlGrps": [str, ...],
                    "isSelected": bool,
                    "isPloted": bool,
                    "isFree": bool
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllNodeInfo",{}))
        self._node_map: dict[int, dict] = {node["no"]: node for node in self.data}

    def get_by_no(self, no: int) -> dict | None:
        """
        根据节点编号获取节点信息

        Args:
            no: 节点编号

        Returns:
            节点信息 dict；未找到返回 None
        """
        return self._node_map.get(no)

    def get_no_list(self) -> list:
        """
        获取所有节点编号列表

        Returns:
            节点编号列表
        """
        return [n.get("no") for n in self.data]

    def get_coordinate(self, no: int) -> tuple | None:
        """
        根据节点编号获取节点坐标

        Args:
            no: 节点编号

        Returns:
            (x, y, z) 元组；节点不存在返回 None
        """
        node = self.get_by_no(no)
        if node:
            return (node.get("x"), node.get("y"), node.get("z"))
        return None

    def get_related_elements(self, no: int) -> list | None:
        """
        根据节点编号获取关联的单元编号列表

        Args:
            no: 节点编号

        Returns:
            关联单元编号列表；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("relatedElements") if node else None

    def get_related_boundaries(self, no: int) -> list | None:
        """
        根据节点编号获取关联的边界编号列表

        Args:
            no: 节点编号

        Returns:
            关联边界编号列表；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("relatedBoundaries") if node else None

    def is_selected(self, no: int) -> bool | None:
        """
        根据节点编号判断节点是否被选中

        Args:
            no: 节点编号

        Returns:
            是否选中；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("isSelected") if node else None

    def is_free(self, no: int) -> bool | None:
        """
        根据节点编号判断节点是否自由

        Args:
            no: 节点编号

        Returns:
            是否自由；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("isFree") if node else None

    def get_precision(self, no: int) -> float | None:
        """
        根据节点编号获取节点精度

        Args:
            no: 节点编号

        Returns:
            节点精度值；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("precision") if node else None

    def get_hash_value(self, no: int) -> int | None:
        """
        根据节点编号获取节点哈希值

        Args:
            no: 节点编号

        Returns:
            哈希值；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("hashValue") if node else None

    def is_plotted(self, no: int) -> bool | None:
        """
        根据节点编号判断节点是否绘图

        Args:
            no: 节点编号

        Returns:
            是否绘图；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("isPloted") if node else None

    def get_related_loads(self, no: int) -> list | None:
        """
        根据节点编号获取关联的荷载列表

        Args:
            no: 节点编号

        Returns:
            关联荷载列表，每个元素为 {"loadCase": str, "loadType": int}；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("relatedLoads") if node else None

    def get_related_setl_grps(self, no: int) -> list | None:
        """
        根据节点编号获取关联的沉降组列表

        Args:
            no: 节点编号

        Returns:
            关联沉降组名称列表；节点不存在返回 None
        """
        node = self.get_by_no(no)
        return node.get("relatedSetlGrps") if node else None


def get_all_node_info() -> NodeInfoResponse:
    return NodeInfoResponse()