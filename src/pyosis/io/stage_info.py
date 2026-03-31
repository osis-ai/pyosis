# cpp/stage_info.py

from ..core.client import osis_client
from .response import OSISParse


class StageInfo(OSISParse):
    """
    GetAllStageInfo 接口返回封装

    返回格式:
        {
            "success": true,
            "data": [
                {
                    "no": int,          # 阶段编号
                    "name": str,        # 阶段名称
                    "duration": float,  # 持续时间
                    "accumulation": float,  # 累积时间
                    "preStageNo": int,  # 前置阶段编号，-1表示无前置阶段
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetStageInfo", {}))
        self._stage_map: dict[int, dict] = {
            s["no"]: s for s in self.data if isinstance(s, dict) and "no" in s
        }

    def get_by_no(self, no: int) -> dict | None:
        """
        根据阶段编号获取阶段信息

        Args:
            no: 阶段编号

        Returns:
            阶段信息 dict；未找到返回 None
        """
        return self._stage_map.get(no)

    def get_no_list(self) -> list[int]:
        """
        获取所有阶段编号列表

        Returns:
            阶段编号列表
        """
        return [s.get("no") for s in self.data if s.get("no") is not None]

    def get_name(self, no: int) -> str | None:
        """
        根据阶段编号获取阶段名称

        Args:
            no: 阶段编号

        Returns:
            阶段名称；未找到返回 None
        """
        stage = self.get_by_no(no)
        return stage.get("name") if stage else None

    def get_duration(self, no: int) -> float | None:
        """
        根据阶段编号获取持续时间

        Args:
            no: 阶段编号

        Returns:
            持续时间（天）；未找到返回 None
        """
        stage = self.get_by_no(no)
        return stage.get("duration") if stage else None

    def get_accumulation(self, no: int) -> float | None:
        """
        根据阶段编号获取累积时间

        Args:
            no: 阶段编号

        Returns:
            累积时间（天）；未找到返回 None
        """
        stage = self.get_by_no(no)
        return stage.get("accumulation") if stage else None

    def get_pre_stage_no(self, no: int) -> int | None:
        """
        根据阶段编号获取前置阶段编号

        Args:
            no: 阶段编号

        Returns:
            前置阶段编号；-1表示无前置阶段；未找到返回 None
        """
        stage = self.get_by_no(no)
        return stage.get("preStageNo") if stage else None
