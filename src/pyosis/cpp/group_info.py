# cpp/group_info.py

import json
from ..core.client import osis_client
from .response import OSISParse


class GroupInfo(OSISParse):
    """
    GetAllGroupInfo 接口返回封装
    
    返回格式:
        {"data": [{"groupName": str, "relatedTendonShapeCount": int, ...}, ...]}
    """
    
    def __init__(self):
        super().__init__(osis_client("GetAllGroupInfo",{}))
        self._group_map: dict[str, dict] = {g["groupName"]: g for g in self.data}

    def get_by_name(self, name: str) -> dict | None:
        """
        根据组名称获取组信息

        Args:
            name: 组名称

        Returns:
            组信息 dict，包含 groupName, relatedTendonShapeCount, relatedLaneCount, relatedStageCount 字段；未找到返回 None
        """
        return self._group_map.get(name)

    def get_name_list(self) -> list:
        """
        获取所有组名称列表

        Returns:
            组名称列表
        """
        return [g.get("groupName") for g in self.data]

    def get_tendon_count(self, name: str) -> int | None:
        """
        根据组名称获取关联的筋腱形状数量

        Args:
            name: 组名称

        Returns:
            关联筋腱形状数量；组不存在返回 None
        """
        g = self.get_by_name(name)
        return g.get("relatedTendonShapeCount") if g else None

    def get_lane_count(self, name: str) -> int | None:
        """
        根据组名称获取关联的车道数量

        Args:
            name: 组名称

        Returns:
            关联车道数量；组不存在返回 None
        """
        g = self.get_by_name(name)
        return g.get("relatedLaneCount") if g else None

    def get_stage_count(self, name: str) -> int | None:
        """
        根据组名称获取关联的施工阶段数量

        Args:
            name: 组名称

        Returns:
            关联施工阶段数量；组不存在返回 None
        """
        g = self.get_by_name(name)
        return g.get("relatedStageCount") if g else None


def get_all_group_info() -> GroupInfo:
    return GroupInfo()