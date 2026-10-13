"""车辆管理器 —— OSIS 里没有独立的“车辆”实体，车辆就是活载等级。

osisPREP 只有 LiveGradeInfo，没有 VehicleInfo。所以“车辆”= 活载等级中
属于车辆/列车的那部分，判据与 C++ 侧一致：

    grade == LiveGrade::VEHICLE(3)
    或 liveTypeForCustom ∈ {VEHICLE(1), TRAIN(2)}   （自定义车辆 / 列车）

数据来源两个：
    - /GetAllGradeInfo        —— 活载等级表（主来源）
    - /GetAllLiveInfo         —— 活载工况的 subLoadCases[].liveGrade / liveGradeEnum

用法:
    from pyosis.live import vehicle_manager
    vehicle_manager.names()          # 所有车辆名
    vehicle_manager.all()            # LiveGrade 对象列表
    vehicle_manager.names_in_use()   # 活载工况里实际用到的车辆名
"""

from __future__ import annotations

from ..core.client import osis_client
from .manager import (
    LiveGrade,
    LIVE_GRADE_VEHICLE,
    LIVE_TYPE_CUSTOM_VEHICLE,
    LIVE_TYPE_CUSTOM_TRAIN,
)


class VehicleManager:
    """车辆管理器（活载等级中属于车辆的视图）"""

    # ── 数据加载 ──────────────────────────────

    def _load_grades(self) -> list[LiveGrade]:
        """拉取全部活载等级（未过滤）"""
        resp = osis_client("GetAllGradeInfo", {})
        if not resp.get("success"):
            raise RuntimeError(f"{resp.get('error', 'GetAllGradeInfo 失败')}")
        return [
            LiveGrade._from_dict(d)
            for d in resp.get("data", [])
            if isinstance(d, dict) and "name" in d
        ]

    def all(self) -> list[LiveGrade]:
        """所有车辆（活载等级里属于车辆/列车的）

        Returns:
            list[LiveGrade]: 车辆活载等级列表

        Raises:
            RuntimeError: 查询失败时抛出异常
        """
        return [g for g in self._load_grades() if g.is_vehicle]

    def names(self) -> list[str]:
        """所有车辆的名称"""
        return [g.name for g in self.all()]

    def get(self, name: str | list[str]) -> LiveGrade | list[LiveGrade | None] | None:
        """按名称获取车辆（同样的名称语义：不存在返回 None）

        Args:
            name: 单个名称或名称列表

        Returns:
            LiveGrade / list[LiveGrade | None] / None
        """
        names = [name] if isinstance(name, str) else list(name)
        by_name = {g.name: g for g in self.all()}
        found = [by_name.get(n) for n in names]
        if len(found) == 1:
            return found[0]
        return found

    def count(self) -> int:
        """车辆总数"""
        return len(self.all())

    # ── 工况中实际使用 ────────────────────────

    def names_in_use(self) -> list[str]:
        """活载工况里实际引用到的车辆名（去重，保持出现顺序）。

        来源 /GetAllLiveInfo 的 subLoadCases[].liveGrade / liveGradeEnum，
        与活载等级表的车辆判据交叉验证，避免把人群/疲劳等级误算进来。
        """
        vehicle_names = set(self.names())
        resp = osis_client("GetAllLiveInfo", {})
        if not resp.get("success"):
            raise RuntimeError(f"{resp.get('error', 'GetAllLiveInfo 失败')}")

        out: list[str] = []
        seen: set[str] = set()
        for case in resp.get("data") or []:
            if not isinstance(case, dict):
                continue
            for sub in case.get("subLoadCases") or []:
                if not isinstance(sub, dict):
                    continue
                name = sub.get("liveGrade")
                enum = sub.get("liveGradeEnum")
                if not name:
                    continue
                if enum == LIVE_GRADE_VEHICLE or name in vehicle_names:
                    if name not in seen:
                        seen.add(name)
                        out.append(name)
        return out

    def __repr__(self) -> str:
        return "VehicleManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

vehicle_manager = VehicleManager()
