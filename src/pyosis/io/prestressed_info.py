# io/prestressed_info.py

from ..core.client import osis_client
from .response import OSISParse


class PrestressedMaterialInfo(OSISParse):
    """
    GetAllPrestressedMaterialInfo 接口返回封装
    获取所有预应力材料信息

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
                    "prestressedGrade": int,
                    "fpk": float,
                    "fpd": float,
                    "fppd": float,
                    ...
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllPrestressedMaterialInfo", {}))
        self._mat_map = {
            m["no"]: m for m in self.data if isinstance(m, dict) and "no" in m
        }

    def get_by_no(self, no: int) -> dict | None:
        return self._mat_map.get(no)

    def get_no_list(self) -> list[int]:
        return [m.get("no") for m in self.data if m.get("no") is not None]


class PrestressedLoadInfo(OSISParse):
    """
    GetAllPrestressedLoadInfo 接口返回封装
    获取所有预应力荷载信息

    预期返回:
        {
            "success": true,
            "data": [
                {
                    "name": str,              # 钢束形状名称
                    "tensionMethod": int,     # 张拉方式
                    "tensionMethodName": str, # BOTH/BEG/END
                    "tensionForce": int,     # 张拉力类型
                    "tensionForceName": str, # ST/IF
                    "beg": float,
                    "end": float,
                    "relatedLoadCase": str,
                    "loadCase": str,
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllPrestressedLoadInfo", {}))
        self._load_map = {
            item["loadCase"]: item for item in self.data
            if isinstance(item, dict) and "loadCase" in item
        }

    def get_by_load_case(self, load_case: str) -> list[dict]:
        return [item for item in self.data
                if isinstance(item, dict) and item.get("loadCase") == load_case]

    def get_load_case_list(self) -> list[str]:
        return list(set(item.get("loadCase") for item in self.data
                       if isinstance(item, dict) and "loadCase" in item))

    def get_name_list(self) -> list[str]:
        return [item.get("name") for item in self.data
                if isinstance(item, dict) and "name" in item]


class TendonShapeInfo(OSISParse):
    """
    GetAllTendonShapeInfo 接口返回封装
    获取所有钢束几何形状信息

    预期返回:
        {
            "success": true,
            "data": [
                {
                    "name": str,
                    "tendonNum": int,
                    "tendonProp": str,
                    "eleGrp": str,
                    "shapeDefType": int,
                    "layoutRefType": int,
                    "length": float,
                    "relatedLoads": list[str],
                    "masterTendonShape": str,
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllTendonShapeInfo", {}))
        self._shape_map = {
            item["name"]: item for item in self.data
            if isinstance(item, dict) and "name" in item
        }

    def get_by_name(self, name: str) -> dict | None:
        return self._shape_map.get(name)

    def get_name_list(self) -> list[str]:
        return [item.get("name") for item in self.data
                if isinstance(item, dict) and "name" in item]


class TendonPropInfo(OSISParse):
    """
    GetAllTendonPropInfo 接口返回封装
    获取所有钢束属性信息

    预期返回:
        {
            "success": true,
            "data": [
                {
                    "name": str,
                    "tensionType": int,
                    "tendonMatNO": int,
                    "area": float,
                    "code": int,
                    "tendonD": int,
                    "tendonNum": int,
                    "pipeD": float,
                    "tensionCoeff": float,
                    "relaxationCoeff": float,
                    "relatedTendonShapes": list[str],
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllTendonPropInfo", {}))
        self._prop_map = {
            item["name"]: item for item in self.data
            if isinstance(item, dict) and "name" in item
        }

    def get_by_name(self, name: str) -> dict | None:
        return self._prop_map.get(name)

    def get_name_list(self) -> list[str]:
        return [item.get("name") for item in self.data
                if isinstance(item, dict) and "name" in item]