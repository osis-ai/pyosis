from ..core.client import osis_client
from .response import OSISParse


class SectionInfo(OSISParse):
    """
    GetAllSectionInfo 接口返回封装

    预期返回:
        {
            "success": true,
            "data": [
                {
                    "no": int,
                    "name": str,
                    "type": int,
                    "area": float,
                    "sy": float,
                    "sz": float,
                    "ixx": float,
                    "iyy": float,
                    "izz": float,
                    "iww": float,
                    "centY": float,
                    "centZ": float,
                    "dy": float,
                    "dz": float,
                    "periO": float,
                    "periI": float
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllSectionInfo", {}))
        self._sec_map: dict[int, dict] = {sec["no"]: sec for sec in self.data if "no" in sec}

    def get_by_no(self, no: int) -> dict | None:
        return self._sec_map.get(no)

    def get_no_list(self) -> list[int]:
        return [s.get("no") for s in self.data if s.get("no") is not None]

    def get_name(self, no: int) -> str | None:
        sec = self.get_by_no(no)
        return sec.get("name") if sec else None

    def get_area(self, no: int) -> float | None:
        sec = self.get_by_no(no)
        return sec.get("area") if sec else None


def get_all_section_info() -> SectionInfo:
    return SectionInfo()

class AllSectionDefinitions(SectionInfo):
    """
    GetAllSectionDefinitions：截面库中全部已定义截面（字段与 GetAllSectionInfo 相同）

    预期返回 data 为与 SectionInfo 相同的列表结构。
    """

    def __init__(self) -> None:
        OSISParse.__init__(self, osis_client("GetAllSectionDefinitions", {}))
        self._sec_map: dict[int, dict] = {sec["no"]: sec for sec in self.data if "no" in sec}


def get_all_section_definitions() -> AllSectionDefinitions:
    return AllSectionDefinitions()


class SectionUsage(OSISParse):
    """
    GetAllSectionUsage：单元对截面的引用关系

    预期返回:
        {
            "success": true,
            "data": {
                "byElement": [
                    {"elementNo": int, "elementType": int, "sectionNos": [int, ...]},
                    ...
                ],
                "bySection": [
                    {"secNo": int, "elementNos": [int, ...]},
                    ...
                ]
            }
        }
    """

    def __init__(self) -> None:
        super().__init__(osis_client("GetAllSectionUsage", {}))

    @property
    def by_element(self) -> list:
        d = self.raw.get("data")
        if isinstance(d, dict):
            return d.get("byElement", [])
        return []

    @property
    def by_section(self) -> list:
        d = self.raw.get("data")
        if isinstance(d, dict):
            return d.get("bySection", [])
        return []

    def __len__(self) -> int:
        return len(self.by_element)

    def __repr__(self) -> str:
        return (
            f"SectionUsage(success={self._success}, "
            f"by_element={len(self.by_element)}, by_section={len(self.by_section)})"
        )


def get_all_section_usage() -> SectionUsage:
    return SectionUsage()

class SectionInfoByNo(OSISParse):
    """
    GetSectionInfo 接口返回封装（按编号单查）
    预期返回:
        {"success": true, "data": {...单个截面...}}
    """

    def __init__(self, sec_no: int):
        super().__init__(osis_client("GetSectionInfo", {"secNo": sec_no}))
        self._sec: dict | None = self.raw.get("data") if isinstance(self.raw, dict) else None

    @property
    def section(self) -> dict | None:
        return self._sec


def get_section_info(sec_no: int) -> SectionInfoByNo:
    return SectionInfoByNo(sec_no)
