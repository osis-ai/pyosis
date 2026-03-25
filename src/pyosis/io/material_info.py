# cpp/material_info.py

from ..core.client import osis_client
from .response import OSISParse


class MaterialInfo(OSISParse):
    """
    GetAllMaterialInfo 接口返回封装

    预期返回:
        {
            "success": true,
            "data": [
                {
                    "no": int,
                    "name": str,
                    "materialType": int,
                    "code": int,
                    "e": float,
                    "g": float,
                    ...
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllMaterialInfo", {}))
        self._mat_map: dict[int, dict] = {
            m["no"]: m for m in self.data if isinstance(m, dict) and "no" in m
        }

    def get_by_no(self, no: int) -> dict | None:
        return self._mat_map.get(no)

    def get_no_list(self) -> list[int]:
        return [m.get("no") for m in self.data if m.get("no") is not None]