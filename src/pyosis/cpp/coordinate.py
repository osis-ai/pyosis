# cpp/coordinate.py

import json

from .response import OSISResponse
from ..core.client import osis_client


class CoordinateResponse(OSISResponse):
    """
    GetCoordinate 接口返回封装
    
    返回格式:
        {"success": true, "data": [{"id": int, "x": float, "y": float, "z": float}, ...]}
    """
    
    def __init__(self):
        super().__init__(osis_client("GetCoordinate",{}))
        self._node_map: dict[int, dict] = {node["id"]: node for node in self.data}

    def get_by_id(self, node_id: int) -> dict | None:
        """
        根据节点 ID 获取节点坐标信息

        Args:
            node_id: 节点编号

        Returns:
            节点坐标 dict，包含 id, x, y, z 字段；未找到返回 None
        """
        return self._node_map.get(node_id)

    def get_id_list(self) -> list:
        """
        获取所有节点 ID 列表

        Returns:
            节点编号列表
        """
        return [node.get("id") for node in self.data]

    def get_x(self, node_id: int) -> float | None:
        """
        根据节点 ID 获取 X 坐标

        Args:
            node_id: 节点编号

        Returns:
            X 坐标值；节点不存在返回 None
        """
        node = self.get_by_id(node_id)
        return node.get("x") if node else None

    def get_y(self, node_id: int) -> float | None:
        """
        根据节点 ID 获取 Y 坐标

        Args:
            node_id: 节点编号

        Returns:
            Y 坐标值；节点不存在返回 None
        """
        node = self.get_by_id(node_id)
        return node.get("y") if node else None

    def get_z(self, node_id: int) -> float | None:
        """
        根据节点 ID 获取 Z 坐标

        Args:
            node_id: 节点编号

        Returns:
            Z 坐标值；节点不存在返回 None
        """
        node = self.get_by_id(node_id)
        return node.get("z") if node else None

    def get_xyz(self, node_id: int) -> tuple | None:
        """
        根据节点 ID 获取 (X, Y, Z) 坐标元组

        Args:
            node_id: 节点编号

        Returns:
            (x, y, z) 元组；节点不存在返回 None
        """
        node = self.get_by_id(node_id)
        if node:
            return node.get("x"), node.get("y"), node.get("z")
        return None


def get_coordinate() -> CoordinateResponse:
    return CoordinateResponse()