"""活载管理器 - 统一管理活载等级、车道和活载的查询

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护活载列表，通过 get 等方法查询，不暴露 HTTP 接口细节

支持的活载类型：
- 活载等级（LiveGrade）：公路I级、公路II级、车辆荷载、疲劳荷载、人群荷载等
- 车道（Lane）：车道几何信息
- 活载（Live）：活载工况组合，包含多个子工况
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from ..core.client import osis_client
from .grade import (
    osis_livegrade_highway,
    osis_livegrade_vehicle,
    osis_livegrade_crowd,
    osis_livegrade_fatigue,
    osis_livegrade_del,
    osis_livegrade_mod,
)
from .analysis import (
    osis_live_analysis,
    osis_live_analysis_del,
    osis_live_analysis_mod,
    osis_live_analysis_inc,
    osis_live_analysis_inc_mod,
    osis_live_analysis_factor,
    osis_live_analysis_option,
)
from .lane import (
    osis_lane_ve,
    osis_lane_tcb,
    osis_lane_del,
    osis_lane_mod,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class LiveGrade:
    """活载等级对象"""

    name: str
    code: int
    grade: int
    crowd_bridge_type: int = 0
    crowd_width: float = 0.0
    fatigue_ii_veichle_center_dis: float = 0.0
    related_live_anal: list[str] = ""

    @classmethod
    def _from_dict(cls, d: dict) -> LiveGrade:
        return cls(
            name=d.get("name", ""),
            code=d.get("code", 0),
            grade=d.get("grade", 0),
            crowd_bridge_type=d.get("crowdBridgeType", 0),
            crowd_width=d.get("crowdWidth", 0.0),
            fatigue_ii_veichle_center_dis=d.get("fatigueIIVeichleCenterDis", 0.0),
            related_live_anal=d.get("relatedLiveAnal", []),
        )


@dataclass(frozen=True)
class Lane:
    """车道对象"""

    name: str
    length: float
    wheel_width: float
    veh_ori: int
    lane_def_method: bool
    ref_long_ele_grp: str
    spline_3d_name: str
    offset: list[float]
    related_anal: list[str]

    @classmethod
    def _from_dict(cls, d: dict) -> Lane:
        return cls(
            name=d.get("name", ""),
            length=d.get("length", 0.0),
            wheel_width=d.get("wheelWidth", 0.0),
            veh_ori=d.get("vehOri", 0),
            lane_def_method=d.get("laneDefMethod", False),
            ref_long_ele_grp=d.get("refLongEleGrp", ""),
            spline_3d_name=d.get("spline3DName", ""),
            offset=d.get("offset", [0.0, 0.0, 0.0]),
            related_anal=d.get("relatedAnal", []),
        )


@dataclass(frozen=True)
class SubLoadCase:
    """活载子工况"""

    name: str
    live_grade: str
    min_lanes: int
    max_lanes: int
    scalar: float
    is_calc_mu: bool
    mu_bridge_type: int
    lane_vkt: list[str]
    master_live_anal: str

    @classmethod
    def _from_dict(cls, d: dict) -> SubLoadCase:
        return cls(
            name=d.get("name", ""),
            live_grade=d.get("liveGrade", ""),
            min_lanes=d.get("minLanes", 0),
            max_lanes=d.get("maxLanes", 0),
            scalar=d.get("scalar", 1.0),
            is_calc_mu=d.get("isCalcMu", False),
            mu_bridge_type=d.get("muBridgeType", 0),
            lane_vkt=d.get("laneVkt", []),
            master_live_anal=d.get("masterLiveAnal", ""),
        )


@dataclass(frozen=True)
class Live:
    """活载对象"""

    name: str
    code: int
    cmb_type: bool
    max_lanes_allowed: int
    trans_reduction_factors: list[float]
    sub_load_cases: list[SubLoadCase]

    @classmethod
    def _from_dict(cls, d: dict) -> Live:
        return cls(
            name=d.get("name", ""),
            code=d.get("code", 0),
            cmb_type=d.get("cmbType", False),
            max_lanes_allowed=d.get("maxLanesAllowed", 0),
            trans_reduction_factors=d.get("transReductionFactors", []),
            sub_load_cases=[
                SubLoadCase._from_dict(s) for s in d.get("subLoadCases", [])
            ],
        )

    def create(
        self,
        sub_name: str,
        grade_name: str,
        scalar: float = 1.0,
        calc_mu: bool = True,
        bridge_type: Literal["SIMPLE", "CONTINUOUS", "ARCH", "CABLE_STAYED", "CABLE_STAYED_AUS", "SUSPENSION", "CUSTOM"] = "SIMPLE",
        mu_params: list[float] | None = None,
        lane_names: list[str] | None = None,
    ) -> Live:
        """添加活载子工况

        Args:
            sub_name: 子工况名称
            grade_name: 活载等级名称
            scalar: 缩放系数
            calc_mu: 是否考虑冲击系数
            bridge_type: 桥型（用于计算冲击系数）
                * SIMPLE = 简支梁桥, 冲击系数: 桥长、弹模、惯性矩、质量
                * CONTINUOUS = 连续梁桥, 冲击系数: 基频计算常数a、基频计算常数b、桥长、弹模、惯性矩、质量
                * ARCH = 拱桥, 冲击系数: 拱厚变化系数、拱桥矢跨比、桥长、弹模、惯性矩，质量
                * CABLE_STAYED = 斜拉桥（无辅助墩）, 冲击系数: 计算常数、主跨跨径
                * CABLE_STAYED_AUX = 斜拉桥（有辅助墩）, 冲击系数: 计算常数、主跨跨径
                * SUSPENSION = 悬索桥, 冲击系数: 主跨跨径、弹模、惯性矩、主缆水平拉力、质量
                * BRIDGE_TYPE_CUSTOM = 自定义, 冲击系数: 用户直接输入基频
            mu_params: 冲击系数计算参数（根据桥型不同参数不同），1-5个
            lane_names: 车道线名称列表

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        if mu_params is None:
            mu_params = []
        if lane_names is None:
            lane_names = []

        ok, err = osis_live_analysis_inc(
            self.name, "a", sub_name, grade_name,
            scalar, 1 if calc_mu else 0, bridge_type, mu_params, lane_names
        )
        if not ok:
            raise RuntimeError(f"添加子工况 {sub_name} 到活载工况 {self.name} 失败: {err}")

    def delete(self, sub_name: str) -> None:
        """删除活载子工况

        Args:
            sub_name: 子工况名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_live_analysis_inc_mod(self.name, "d", sub_name)
        if not ok:
            raise RuntimeError(f"从活载工况 {self.name} 删除子工况 {sub_name} 失败: {err}")

    def rename(self, old_sub_name: str, new_sub_name: str) -> None:
        """重命名活载子工况

        Args:
            old_sub_name: 旧子工况名称
            new_sub_name: 新子工况名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_live_analysis_inc_mod(self.name, "mn", old_sub_name, new_sub_name)
        if not ok:
            raise RuntimeError(f"重命名子工况 {old_sub_name} -> {new_sub_name} 失败: {err}")

    def set_trans_reduction_factors(self, factors: list[float]) -> None:
        """设置活载工况的横向布载折减系数

        Args:
            factors: 折减系数列表，最多10个

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_live_analysis_factor(self.name, *factors)
        if not ok:
            raise RuntimeError(f"设置横向折减系数失败: {err}")

    def set_lane_count(self, sub_name: str, min_lanes: int, max_lanes: int) -> None:
        """设置活载子工况的加载车道数范围

        Args:
            sub_name: 子工况名称
            min_lanes: 最少车道数
            max_lanes: 最多车道数

        Note:
            不调用此函数则默认min = 0，max = 最多车道数

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_live_analysis_option(self.name, sub_name, min_lanes, max_lanes)
        if not ok:
            raise RuntimeError(f"设置加载车道数失败: {err}")

# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class LiveManager:
    """活载管理器

    统一管理活载等级、车道和活载的查询。

    用法:
        >>> from pyosis.live import live_manager
        >>> live_manager.load()                               # 加载所有活载数据
        >>> all_grades = live_manager.all_grades()             # 获取所有活载等级
        >>> all_lanes = live_manager.all_lanes()               # 获取所有车道
        >>> all_lives = live_manager.all_lives()              # 获取所有活载
        >>> grade = live_manager.get_grade("活载等级1")        # 按名称获取活载等级
        >>> lane = live_manager.get_lane("车道1")              # 按名称获取车道
        >>> live = live_manager.get_live("活载1")              # 按名称获取活载
    """

    def __init__(self) -> None:
        self._loaded: bool = False
        self._live_grades: list[LiveGrade] = []
        self._lanes: list[Lane] = []
        self._lives: list[Live] = []
        self._grade_map: dict[str, LiveGrade] = {}
        self._lane_map: dict[str, Lane] = {}
        self._live_map: dict[str, Live] = {}

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有活载数据（延迟加载，带缓存）"""
        if self._loaded:
            return

        resp = osis_client("GetAllLiveLoadInfo", {})
        if isinstance(resp, tuple):
            raise RuntimeError(f"加载活载数据失败: {resp[1]}")

        data = resp.get("data", {})

        # 解析活载等级
        self._live_grades = [
            LiveGrade._from_dict(d) for d in data.get("liveGrades", [])
        ]
        self._grade_map = {g.name: g for g in self._live_grades}

        # 解析车道
        self._lanes = [Lane._from_dict(d) for d in data.get("lanes", [])]
        self._lane_map = {l.name: l for l in self._lanes}

        # 解析活载
        self._lives = [
            Live._from_dict(d) for d in data.get("liveInfos", [])
        ]
        self._live_map = {l.name: l for l in self._lives}

        self._loaded = True

    def refresh(self) -> None:
        """强制刷新缓存"""
        self._loaded = False
        self._live_grades = []
        self._lanes = []
        self._lives = []
        self._grade_map = {}
        self._lane_map = {}
        self._live_map = {}
        self._load()

    def load(self) -> None:
        """显式加载数据（也可直接调用查询方法，会自动加载）"""
        self._load()

    # ── 活载等级增删改 ────────────────────────────────

    def create_grade_highway(
        self,
        name: str,
        eCode: Literal["JTGD60_2015"] = "JTGD60_2015",
        eLiveLoadType: Literal["HIGHWAY_I", "HIGHWAY_II"] = "HIGHWAY_I",
    ) -> LiveGrade:
        """创建公路活载等级

        Args:
            name: 活载等级名称
            eCode: 规范类型，默认 JTGD60_2015
            eLiveLoadType: 活载类型，HIGHWAY_I=公路I级，HIGHWAY_II=公路II级

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_livegrade_highway(name, eCode, eLiveLoadType)
        if not ok:
            raise RuntimeError(f"创建公路活载等级 {name} 失败: {err}")
        self._loaded = False
        return self.get_grade(name)

    def create_grade_vehicle(
        self,
        name: str,
        eCode: Literal["JTGD60_2015"] = "JTGD60_2015",
    ) -> LiveGrade:
        """创建车辆荷载等级

        Args:
            name: 活载等级名称
            eCode: 规范类型，默认 JTGD60_2015

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_livegrade_vehicle(name, eCode, "VEHICLE")
        if not ok:
            raise RuntimeError(f"创建车辆荷载等级 {name} 失败: {err}")
        self._loaded = False
        return self.get_grade(name)

    def create_grade_crowd(
        self,
        name: str,
        eBridgeType: Literal["BRIDGE_COMMON", "BRIDGE_CROWD_WITH", "BRIDGE_CROWD_ONLY"] = "BRIDGE_COMMON",
        dPara: float = 10.0,
    ) -> LiveGrade:
        """创建人群荷载等级

        Args:
            name: 活载等级名称
            eBridgeType: 桥类型，BRIDGE_COMMON=一般桥，BRIDGE_CROWD_WITH=行人密集桥，BRIDGE_CROWD_ONLY=专用行人桥
            dPara: 人群横向宽度

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_livegrade_crowd(name, "JTGD60_2015", "CROWD", eBridgeType, dPara)
        if not ok:
            raise RuntimeError(f"创建人群荷载等级 {name} 失败: {err}")
        self._loaded = False
        return self.get_grade(name)

    def create_grade_fatigue(
        self,
        name: str,
        eLiveLoadType: Literal["FATIGUE_I", "FATIGUE_II", "FATIGUE_III"] = "FATIGUE_I",
        dPara: float | None = None,
    ) -> LiveGrade:
        """创建疲劳荷载等级

        Args:
            name: 活载等级名称
            eLiveLoadType: 疲劳模型类型，FATIGUE_I/II/III
            dPara: 车辆中心间距，仅 FATIGUE_II 时需要填写

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_livegrade_fatigue(name, "JTGD60_2015", eLiveLoadType, dPara)
        if not ok:
            raise RuntimeError(f"创建疲劳荷载等级 {name} 失败: {err}")
        self._loaded = False
        return self.get_grade(name)

    def delete_grade(self, name: str) -> None:
        """删除活载等级

        Args:
            name: 活载等级名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_livegrade_del(name)
        if not ok:
            raise RuntimeError(f"删除活载等级 {name} 失败: {err}")
        self._loaded = False

    def rename_grade(self, old_name: str, new_name: str) -> None:
        """重命名活载等级

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_livegrade_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名活载等级 {old_name} -> {new_name} 失败: {err}")
        self._loaded = False

    # ── 车道增删改 ────────────────────────────────

    def create_lane_ve(
        self,
        name: str,
        dLength: float,
        wheel: int = 1,
        eOriention: Literal[-1, 0, 1] = 0,
        eRef: Literal[0, 1] = 0,
        spline_name: str | None = None,
        ref_elems: str | None = None,
        offsetY: float = 0.0,
        offsetZ: float = 0.0,
    ) -> Lane:
        """创建车道（车道单元法 VE）

        Args:
            name: 车道名称
            dLength: 桥梁跨度（m）
            wheel: 轮距（默认1）
            eOriention: 车辆移动方向
                * -1=向后
                * 0=往返
                * 1=向前
            eRef: 车道参照方式，
                * 0=单元组
                * 1=样条曲线
            spline_name: 样条曲线名称（eRef=1时使用）
            ref_elems: 参照单元组名称列表（纵梁）（eRef=0时使用）
            offsetY: 局部坐标系下Y方向偏移量（m）（eRef=0时使用）
            offsetZ: 局部坐标系下Z方向偏移量（m）（eRef=0时使用）

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if eRef == 0:
            if not ref_elems:
                raise RuntimeError(f"参照单元组名称 ref_elems 不能为空")
            param = [ref_elems, offsetY, offsetZ]
        else:
            if not spline_name:
                raise RuntimeError(f"样条曲线名称 spline_name 不能为空")
            param = [spline_name]

        ok, err = osis_lane_ve(name, "VE", dLength, wheel, eOriention, eRef, param)
        if not ok:  
            raise RuntimeError(f"创建车道 {name} 失败: {err}")
        self._loaded = False
        return self.get_lane(name)

    def create_lane_tcb(
        self,
        name: str,
        crossbeam_elems: str,
        dLength: float,
        wheel: int = 1,
        eOriention: Literal[-1, 0, 1] = 0,
        eRef: Literal[0, 1] = 0,
        spline_name: str | None = None,
        ref_elems: str | None = None,
        offsetY: float = 0.0,
        offsetZ: float = 0.0,
    ) -> Lane:
        """创建车道（横向联系梁法 TCB）

        Args:
            name: 车道名称
            crossbeam_elems: 横梁单元组名称
            dLength: 桥梁跨度（m）
            wheel: 轮距（默认1）
            eOriention: 车辆移动方向
            eRef: 车道参照方式，0=单元组，1=样条曲线
            ref_elems: 参照纵梁单元组名称（eRef=0时使用）
            offsetY: Y方向偏移量（m）
            offsetZ: Z方向偏移量（m）
            spline_name: 样条曲线名称（eRef=1时使用）

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if eRef == 0:
            if not ref_elems:
                raise RuntimeError(f"参照单元组名称 ref_elems 不能为空")
            param = [ref_elems, offsetY, offsetZ]
        else:
            if not spline_name:
                raise RuntimeError(f"样条曲线名称 spline_name 不能为空")
            param = [spline_name]

        ok, err = osis_lane_tcb(name, "TCB", crossbeam_elems, dLength, wheel, eOriention, eRef, param)
        if not ok:
            raise RuntimeError(f"创建车道 {name} 失败: {err}")
        self._loaded = False
        return self.get_lane(name)

    def delete_lane(self, name: str) -> None:
        """删除车道

        Args:
            name: 车道名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_lane_del(name)
        if not ok:
            raise RuntimeError(f"删除车道 {name} 失败: {err}")
        self._loaded = False

    def rename_lane(self, old_name: str, new_name: str) -> None:
        """重命名车道

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_lane_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名车道 {old_name} -> {new_name} 失败: {err}")
        self._loaded = False

    # ── 活载工况增删改 ────────────────────────────────

    def create_live(
        self,
        name: str,
        code: Literal["JTGD60_2015"] = "JTGD60_2015",
        sub_cmb_type: Literal[0, 1] = 1,
    ) -> Live:
        """创建活载工况

        Args:
            name: 活载工况名称
            code: 规范名
            sub_cmb_type: 子工况组合类型，1=单独（包络），0=组合（相加）

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_live_analysis(name, code, sub_cmb_type)
        if not ok:
            raise RuntimeError(f"创建活载工况 {name} 失败: {err}")
        self._loaded = False
        return self.get_live(name)

    def delete_live(self, name: str) -> None:
        """删除活载工况

        Args:
            name: 活载工况名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_live_analysis_del(name)
        if not ok:
            raise RuntimeError(f"删除活载工况 {name} 失败: {err}")
        self._loaded = False

    def rename_live(self, old_name: str, new_name: str) -> None:
        """重命名活载工况

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_live_analysis_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名活载工况 {old_name} -> {new_name} 失败: {err}")
        self._loaded = False

    # ── 查询 ──────────────────────────────────

    def all_grades(self) -> list[LiveGrade]:
        """获取所有活载等级"""
        self._load()
        return list(self._live_grades)

    def all_lanes(self) -> list[Lane]:
        """获取所有车道"""
        self._load()
        return list(self._lanes)

    def all_lives(self) -> list[Live]:
        """获取所有活载"""
        self._load()
        return list(self._lives)

    def get_grade(self, name: str) -> Optional[LiveGrade]:
        """根据名称获取活载等级"""
        self._load()
        return self._grade_map.get(name)

    def get_lane(self, name: str) -> Optional[Lane]:
        """根据名称获取车道"""
        self._load()
        return self._lane_map.get(name)

    def get_live(self, name: str) -> Optional[Live]:
        """根据名称获取活载"""
        self._load()
        return self._live_map.get(name)

    def count_grades(self) -> int:
        """获取活载等级数量"""
        self._load()
        return len(self._live_grades)

    def count_lanes(self) -> int:
        """获取车道数量"""
        self._load()
        return len(self._lanes)

    def count_lives(self) -> int:
        """获取活载数量"""
        self._load()
        return len(self._lives)

    def __repr__(self) -> str:
        self._load()
        return f"LiveManager(grades={len(self._live_grades)}, lanes={len(self._lanes)}, lives={len(self._lives)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

live_manager = LiveManager()