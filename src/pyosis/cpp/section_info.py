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
