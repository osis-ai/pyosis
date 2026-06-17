"""活载管理器 - 统一管理活载等级、车道和活载工况的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 无状态设计，每次从服务端加载（与 element/boundary manager 一致）

子管理器：
- grade: LiveGradeManager - 活载等级
- lane: LaneManager - 车道
- case: LiveCaseManager - 活载工况
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Any

from ..core.client import osis_client
from .grade import (
    osis_livegrade_highway,
    osis_livegrade_vehicle,
    osis_livegrade_crowd,
    osis_livegrade_fatigue,
    osis_livegrade_del,
    osis_livegrade_mod, osis_livegrade_custom,
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
    """活载等级对象
    
    对应接口 GetAllLiveGradeInfo / GetGradeInfoByNames 返回的数据。
    活载等级定义了车辆荷载、人群荷载、疲劳荷载等的规范参数。
    """
    no: int                              # 编号
    name: str                            # 名称
    code: int                            # 规范代码
    grade: int                           # 等级代码（如 HIGHWAY_I=1, HIGHWAY_II=2）
    crowd_bridge_type: int               # 人群荷载桥型
    crowd_width: float                   # 人群横向宽度（m）
    fatigue_ii_veichle_center_dis: float # 疲劳II模型车辆中心间距（m）
    related_live_anal: list[str] = field(default_factory=list)  # 关联的活载分析名称列表
    related_stages: list[int] = field(default_factory=list)     # 关联的施工阶段编号列表
    custom_layout: list[list[float]] = field(default_factory=list)  # 自定义布载矩阵
    code_data_qk_pk5_pk50: dict = field(default_factory=dict)       # 公路荷载规范数据 {qk, pk_5, pk_50}
    code_data_vehicle_5x2: list[list[float]] = field(default_factory=list)  # 车辆荷载 5x2 矩阵
    code_data_crowd_w50_w150: dict = field(default_factory=dict)    # 人群荷载规范数据 {w_50, w_150}
    code_data_fatigueII_6x2: list[list[float]] = field(default_factory=list)  # 疲劳II模型 6x2 矩阵
    code_data_fatigueIII_4x2: list[list[float]] = field(default_factory=list)  # 疲劳III模型 4x2 矩阵

    @classmethod
    def _from_dict(cls, d: dict) -> LiveGrade:
        """从接口 dict 构造 LiveGrade 对象（内部使用）"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            code=d.get("code"),
            grade=d.get("grade"),
            crowd_bridge_type=d.get("crowdBridgeType"),
            crowd_width=d.get("crowdWidth"),
            fatigue_ii_veichle_center_dis=d.get("fatigueIIVeichleCenterDis"),
            related_live_anal=d.get("relatedLiveAnal"),
            related_stages=d.get("relatedStages"),
            custom_layout=d.get("customLayout"),
            code_data_qk_pk5_pk50=d.get("codeData_qk_pk5_pk50"),
            code_data_vehicle_5x2=d.get("codeData_vehicle_5x2"),
            code_data_crowd_w50_w150=d.get("codeData_crowd_w50_w150"),
            code_data_fatigueII_6x2=d.get("codeData_fatigueII_6x2"),
            code_data_fatigueIII_4x2=d.get("codeData_fatigueIII_4x2"),
        )

    def __repr__(self) -> str:
        return f"LiveGrade(name={self.name!r}, code={self.code}, grade={self.grade})"


@dataclass(frozen=True)
class Lane:
    """车道对象
    
    对应接口 GetAllLaneInfo / GetLaneInfoByNames 返回的数据。
    车道定义了车辆移动的路径和影响线计算方法。
    """
    no: int                              # 编号
    name: str                            # 名称
    length: float                        # 桥梁跨度（m）
    wheel_width: float                   # 轮距（m）
    veh_ori: int                         # 车辆移动方向：-1=向后, 0=往返, 1=向前
    infl_algo_type: int                  # 影响线算法类型
    lane_def_method: bool                # 车道定义方法：True=样条曲线, False=单元组
    ref_long_ele_grp: str                # 参照纵梁单元组名称（lane_def_method=False 时）
    spline_3d_name: str                  # 3D样条曲线名称（lane_def_method=True 时）
    offset: list[float] = field(default_factory=list)     # 偏移量 [X, Y, Z]（m）
    related_anal: list[str] = field(default_factory=list) # 关联的分析名称列表
    related_stages: list[int] = field(default_factory=list)  # 关联的施工阶段编号列表

    @classmethod
    def _from_dict(cls, d: dict) -> Lane:
        """从接口 dict 构造 Lane 对象（内部使用）"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            length=d.get("length"),
            wheel_width=d.get("wheelWidth"),
            veh_ori=d.get("vehOri"),
            infl_algo_type=d.get("inflAlgoType"),
            lane_def_method=d.get("laneDefMethod"),
            ref_long_ele_grp=d.get("refLongEleGrp"),
            spline_3d_name=d.get("spline3DName"),
            offset=d.get("offset") or [],
            related_anal=d.get("relatedAnal") or [],
            related_stages=d.get("relatedStages") or [],
        )

    def __repr__(self) -> str:
        return f"Lane(name={self.name!r}, length={self.length})"


@dataclass(frozen=True)
class SubLoadCase:
    """活载子工况
    
    属于 LiveCase 的组成部分，定义了具体的加载方案。
    包含活载等级、车道分配、冲击系数等参数。
    """
    name: str                            # 子工况名称
    live_grade: str                      # 活载等级名称
    live_grade_enum: int                 # 活载等级枚举值
    min_lanes: int                       # 最少加载车道数
    max_lanes: int                       # 最多加载车道数
    master_live_anal: str                # 主活载分析名称
    freq: float                          # 频率（Hz）
    lane_vkt: list[str] = field(default_factory=list)  # 车道名称列表
    scalar: float = 1.0                  # 缩放系数
    is_calc_mu: bool = False             # 是否计算冲击系数
    mu_bridge_type: int = 0              # 冲击系数桥型
    mu_paras: list[float] = field(default_factory=list)  # 冲击系数计算参数

    @classmethod
    def _from_dict(cls, d: dict) -> SubLoadCase:
        """从接口 dict 构造 SubLoadCase 对象（内部使用）"""
        return cls(
            name=d.get("name"),
            live_grade=d.get("liveGrade"),
            live_grade_enum=d.get("liveGradeEnum"),
            min_lanes=d.get("minLanes"),
            max_lanes=d.get("maxLanes"),
            master_live_anal=d.get("masterLiveAnal"),
            freq=d.get("freq"),
            lane_vkt=d.get("laneVkt"),
            scalar=d.get("scalar"),
            is_calc_mu=d.get("isCalcMu"),
            mu_bridge_type=d.get("muBridgeType"),
            mu_paras=d.get("muParas"),
        )


@dataclass(frozen=False)
class LiveCase:
    """活载工况对象
    
    对应接口 GetAllLiveInfo / GetLiveInfoByNames 返回的数据。
    活载工况由多个子工况组成，可设置横向折减系数和加载车道范围。
    
    属性:
        no: 工况编号
        name: 工况名称
        code: 规范代码
        cmb_type: 子工况组合类型，True=单独（包络），False=组合（相加）
        max_lanes_allowed: 允许的最大车道数
        trans_reduction_factors: 横向布载折减系数列表，最多10个
        sub_load_cases: 子工况列表
        related_stages: 关联的施工阶段编号列表
    """
    no: int                              # 编号
    name: str                            # 名称
    code: int                            # 规范代码
    cmb_type: bool                       # 组合类型：True=包络, False=相加
    max_lanes_allowed: int               # 允许的最大车道数
    trans_reduction_factors: list[float] = field(default_factory=list)  # 横向折减系数
    sub_load_cases: list[SubLoadCase] = field(default_factory=list)     # 子工况列表
    related_stages: list[int] = field(default_factory=list)             # 关联的施工阶段

    @classmethod
    def _from_dict(cls, d: dict) -> LiveCase:
        """从接口 dict 构造 LiveCase 对象（内部使用）"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            code=d.get("code"),
            cmb_type=d.get("cmbType"),
            max_lanes_allowed=d.get("maxLanesAllowed"),
            trans_reduction_factors=d.get("transReductionFactors"),
            sub_load_cases=[SubLoadCase._from_dict(s) for s in d.get("subLoadCases", []) if isinstance(s, dict)],
            related_stages=d.get("relatedStages"),
        )

    def _sync_from_dict(self, d: dict) -> None:
        """用 dict 同步当前对象属性（内部使用）"""
        self.no = d.get("no")
        self.name = d.get("name")
        self.code = d.get("code")
        self.cmb_type = d.get("cmbType")
        self.max_lanes_allowed = d.get("maxLanesAllowed")
        self.trans_reduction_factors = d.get("transReductionFactors") or []
        self.sub_load_cases = [SubLoadCase._from_dict(s) for s in d.get("subLoadCases", []) if isinstance(s, dict)]
        self.related_stages = d.get("relatedStages") or []

    def refresh(self) -> LiveCase:
        """从服务端刷新当前活载工况数据并同步到对象属性
        
        Returns:
            刷新后的 LiveCase 对象
        """
        resp = osis_client("GetLiveInfoByNames", {"name": [self.name]})
        if not resp['success']:
            raise RuntimeError(f"刷新活载工况 {self.name} 失败: {resp['error']}")
        data = resp.get("data", [])
        if data and data[0]:
            self._sync_from_dict(data[0])
        return self

    def include(
        self,
        op: Literal["a", "m", "d", "mn"],
        sub_name: str,
        *args: str,
    ) -> LiveCase | None:
        """活载子工况增删改（对应 OSIS 命令 LiveAnalInc）。

        Args:
            op: 操作类型
                * "a"/"m": args = (grade, scalar, mu_flag, bridge_type, mu_params..., lane1, lane2, ...)
                * "d":      无
                * "mn":     args = (new_name,)
            sub_name: 子工况名称
            args: 命令流平铺的剩余字段

        Returns:
            更新后的 LiveCase 对象
        """
        if op in ("a", "m"):
            _MU_PARAM_COUNT = {
                "SIMPLE": 4,
                "CONTINUOUS": 6,
                "ARCH": 5,
                "CABLE_STAYED": 2,
                "CABLE_STAYED_AUS": 2,
                "SUSPENSION": 5,
                "CUSTOM": 1,
            }
            grade_name, scalar, mu_flag = args[0], float(args[1]), int(args[2])
            rest = args[4:]
            if mu_flag == 1:
                bridge_type = args[3] or "SIMPLE"
                mu_count = _MU_PARAM_COUNT.get(bridge_type, 1)
                mu_params: list[float] = [float(x) for x in rest[:mu_count]]
                lane_names: list[str] = list(rest[mu_count:])
            else:
                mu_params, lane_names = [], list(rest)
            bridge_type = args[3] if mu_flag == 1 else None
            if op == "a":
                return self.create_sub(
                    sub_name, grade_name, scalar, bool(mu_flag), bridge_type,
                    mu_params, lane_names,
                )
            return self.modify_sub(
                sub_name, grade_name, scalar, bool(mu_flag), bridge_type,
                mu_params, lane_names,
            )
        elif op == "mn":
            return self.rename_sub(sub_name, args[0] if args else "")
        elif op == "d":
            return self.delete_sub(sub_name)
        return None

    def create_sub(
        self,
        sub_name: str,
        grade_name: str,
        scalar: int = 1,
        calc_mu: bool = 1,
        bridge_type: Literal["SIMPLE", "CONTINUOUS", "ARCH", "CABLE_STAYED", "CABLE_STAYED_AUS", "SUSPENSION", "CUSTOM"] = "CUSTOM",
        mu_params: list[float] | None = None,
        lane_names: list[str] | None = None,
    ) -> LiveCase:
        """添加活载子工况

        Args:
            sub_name: 子工况名称
            grade_name: 活载等级名称
            scalar: 缩放系数，默认 1.0
            calc_mu: 是否计算冲击系数，默认 1
            bridge_type: 桥型（用于计算冲击系数）
                - SIMPLE: 简支梁桥
                - CONTINUOUS: 连续梁桥
                - ARCH: 拱桥
                - CABLE_STAYED: 斜拉桥（无辅助墩）
                - CABLE_STAYED_AUS: 斜拉桥（有辅助墩）
                - SUSPENSION: 悬索桥
                - CUSTOM: 自定义，直接输入基频
            mu_params: 冲击系数计算参数列表（根据桥型不同参数不同）
                * SIMPLE	            = 桥长、弹模、惯性矩、质量
                * CONTINUOUS	        = 基频计算常数a、基频计算常数b、桥长、弹模、惯性矩、质量
                * ARCH	                = 拱厚变化系数、拱桥矢跨比、桥长、弹模、惯性矩，质量
                * CABLE_STAYED	        = 计算常数、主跨跨径
                * CABLE_STAYED_AUX	    = 计算常数、主跨跨径
                * SUSPENSION	        = 主跨跨径、弹模、惯性矩、主缆水平拉力、质量
                * CUSTOM	            = 用户直接输入基频
            lane_names: 车道名称列表

        Returns:
            更新后的 LiveCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        if calc_mu:
            ok, err = osis_live_analysis_inc(
                self.name, "a", sub_name, grade_name,
                scalar, 1, bridge_type, mu_params, lane_names
            )
        else:
            ok, err = osis_live_analysis_inc(
                self.name, "a", sub_name, grade_name,
                scalar, 0, None, None, lane_names
            )
            
        if not ok:
            raise RuntimeError(f"添加子工况 {sub_name} 到活载工况 {self.name} 失败: {err}")
        return self.refresh()
    
    def modify_sub(
        self,
        sub_name: str,
        grade_name: str,
        scalar: float = 1.0,
        calc_mu: bool = 1,
        bridge_type: Literal["SIMPLE", "CONTINUOUS", "ARCH", "CABLE_STAYED", "CABLE_STAYED_AUS", "SUSPENSION", "CUSTOM"] = "SIMPLE",
        mu_params: list[float] | None = None,
        lane_names: list[str] | None = None,
    ) -> LiveCase:
        """添加活载子工况

        Args:
            sub_name: 子工况名称
            grade_name: 活载等级名称
            scalar: 缩放系数，默认 1.0
            calc_mu: 是否计算冲击系数，默认 1
            bridge_type: 桥型（用于计算冲击系数）
                - SIMPLE: 简支梁桥
                - CONTINUOUS: 连续梁桥
                - ARCH: 拱桥
                - CABLE_STAYED: 斜拉桥（无辅助墩）
                - CABLE_STAYED_AUS: 斜拉桥（有辅助墩）
                - SUSPENSION: 悬索桥
                - CUSTOM: 自定义，直接输入基频
            mu_params: 冲击系数计算参数列表（根据桥型不同参数不同）
                * SIMPLE	            = 桥长、弹模、惯性矩、质量
                * CONTINUOUS	        = 基频计算常数a、基频计算常数b、桥长、弹模、惯性矩、质量
                * ARCH	                = 拱厚变化系数、拱桥矢跨比、桥长、弹模、惯性矩，质量
                * CABLE_STAYED	        = 计算常数、主跨跨径
                * CABLE_STAYED_AUX	    = 计算常数、主跨跨径
                * SUSPENSION	        = 主跨跨径、弹模、惯性矩、主缆水平拉力、质量
                * CUSTOM	            = 用户直接输入基频
            lane_names: 车道名称列表

        Returns:
            更新后的 LiveCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        if calc_mu:
            ok, err = osis_live_analysis_inc(
                self.name, "m", sub_name, grade_name,
                scalar, 1, bridge_type, mu_params, lane_names
            )
        else:
            ok, err = osis_live_analysis_inc(
                self.name, "m", sub_name, grade_name,
                scalar, 0, None, None, lane_names
            )
            
        if not ok:
            raise RuntimeError(f"添加子工况 {sub_name} 到活载工况 {self.name} 失败: {err}")
        return self.refresh()

    def delete_sub(self, sub_name: str) -> None:
        """删除活载子工况

        Args:
            sub_name: 要删除的子工况名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_live_analysis_inc_mod(self.name, "d", sub_name)
        if not ok:
            raise RuntimeError(f"从活载工况 {self.name} 删除子工况 {sub_name} 失败: {err}")
        self.refresh()

    def rename_sub(self, old_sub_name: str, new_sub_name: str) -> None:
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
        self.refresh()

    def set_trans_reduction_factors(self, *factors: float) -> None:
        """设置活载工况的横向布载折减系数

        Args:
            factors: 折减系数列表，最多10个，不足10个按最后一个系数补齐

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_live_analysis_factor(self.name, *factors)
        if not ok:
            raise RuntimeError(f"设置横向折减系数失败: {err}")
        self.refresh()

    def set_lane_count(self, sub_name: str, min_lanes: int, max_lanes: int) -> None:
        """设置活载子工况的加载车道数范围

        Args:
            sub_name: 子工况名称
            min_lanes: 最少加载车道数
            max_lanes: 最多加载车道数

        Note:
            不调用此方法则默认 min=0, max=最多车道数

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_live_analysis_option(self.name, sub_name, min_lanes, max_lanes)
        if not ok:
            raise RuntimeError(f"设置加载车道数失败: {err}")
        self.refresh()

    def __repr__(self) -> str:
        return f"LiveCase(name={self.name!r}, sub_cases={len(self.sub_load_cases)})"


# ──────────────────────────────────────────────
# 子管理器
# ──────────────────────────────────────────────


class LiveGradeManager:
    """活载等级管理器
    
    统一管理活载等级的创建、删除、修改和查询。
    活载等级包括：公路活载、车辆荷载、人群荷载、疲劳荷载等。
    """

    def _load(self) -> list[LiveGrade]:
        """从服务端加载所有活载等级信息（内部使用）
        
        Returns:
            LiveGrade 对象列表
        """
        resp = osis_client("GetAllGradeInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        grades = [
            LiveGrade._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return grades

    def create(
        self,
        name: str,
        code: str,
        type: str,
        *args: Any,
        **kwargs: Any,
    ) -> LiveGrade:
        """创建活载等级（便捷入口，内部转发到对应 create_* 方法）

        位置参顺序: name, code, type, *create_* 剩余位置参

        type 路由映射：
            * "HIGHWAY_I"   → create_highway
            * "HIGHWAY_II"  → create_highway
            * "VEHICLE"     → create_vehicle
            * "CROWD"       → create_crowd
            * "FATIGUE_I"   → create_fatigue
            * "FATIGUE_II"  → create_fatigue
            * "FATIGUE_III" → create_fatigue
            * "VG"          → create_custom

        Args:
            name: 活载等级名称
            code: 规范类型
                * "JTGD60_2015" = 公路规范
                * "CUSTOM"      = 自定义规范
            type: 活载类型
            *args: 按位置传给对应 create_* 的剩余参数
            **kwargs: 按关键字传给对应 create_* 的参数

        Raises:
            ValueError: 未知 type
            RuntimeError: 创建失败

        Examples:
            >>> live_manager.grade.create("活载-VEHICLE", "JTGD60_2015", "VEHICLE", "VEHICLE")
            >>> live_manager.grade.create("公路I级", "JTGD60_2015", "HIGHWAY_I", "HIGHWAY_I")
            >>> live_manager.grade.create("自定义", "CUSTOM", "VG", "VG", 2,
            ...     [(1.5, 100), (3.0, 100)])
            >>> live_manager.grade.create("疲劳I", "JTGD60_2015", "FATIGUE_I",
            ...     live_load_type="FATIGUE_I")
        """
        _creator = {
            "HIGHWAY_I":   self.create_highway,
            "HIGHWAY_II":  self.create_highway,
            "VEHICLE":     self.create_vehicle,
            "CROWD":       self.create_crowd,
            "FATIGUE_I":   self.create_fatigue,
            "FATIGUE_II":  self.create_fatigue,
            "FATIGUE_III": self.create_fatigue,
            "VG":          self.create_custom,
        }
        type_key = type.upper()
        if type_key not in _creator:
            raise ValueError(
                f"未知活载类型: {type!r}，"
                f"支持: {', '.join(_creator)}"
            )
        return _creator[type_key](name, code, *args, **kwargs)

    def create_highway(
        self,
        name: str,
        code: Literal["JTGD60_2015"] = "JTGD60_2015",
        live_load_type: Literal["HIGHWAY_I", "HIGHWAY_II"] = "HIGHWAY_I",
    ) -> LiveGrade:
        """创建公路活载等级

        Args:
            name: 活载等级名称（对应 strName）
            code: 规范类型（对应 eCode），默认 JTGD60_2015
            live_load_type: 活载类型（对应 eLiveLoadType）
                - HIGHWAY_I: 公路I级
                - HIGHWAY_II: 公路II级

        Returns:
            创建的 LiveGrade 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_livegrade_highway(name, code, live_load_type)
        if not ok:
            raise RuntimeError(f"创建公路活载等级 {name} 失败: {err}")
        return self.get(name)

    def create_vehicle(
        self,
        name: str,
        code: Literal["JTGD60_2015"] = "JTGD60_2015",
        live_load_type: Literal["VEHICLE"] = "VEHICLE",
    ) -> LiveGrade:
        """创建车辆荷载等级

        Args:
            name: 活载等级名称（对应 strName）
            code: 规范类型（对应 eCode），默认 JTGD60_2015
            live_load_type: 活载类型（对应 eLiveLoadType），固定为 VEHICLE

        Returns:
            创建的 LiveGrade 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_livegrade_vehicle(name, code, live_load_type)
        if not ok:
            raise RuntimeError(f"创建车辆荷载等级 {name} 失败: {err}")
        return self.get(name)

    def create_crowd(
        self,
        name: str,
        code: Literal["JTGD60_2015"] = "JTGD60_2015",
        live_load_type: Literal["CROWD"] = "CROWD",
        bridge_type: Literal["BRIDGE_COMMON", "BRIDGE_CROWD_WITH", "BRIDGE_CROWD_ONLY"] = "BRIDGE_COMMON",
        para: float = 10.0,
    ) -> LiveGrade:
        """创建人群荷载等级

        Args:
            name: 活载等级名称（对应 strName）
            code: 规范类型（对应 eCode），默认 JTGD60_2015
            live_load_type: 活载类型（对应 eLiveLoadType），固定为 CROWD
            bridge_type: 桥类型（对应 eBridgeType）
                - BRIDGE_COMMON: 一般桥
                - BRIDGE_CROWD_WITH: 行人密集桥
                - BRIDGE_CROWD_ONLY: 专用行人桥
            para: 人群横向宽度（m）（对应 dPara），默认 10.0

        Returns:
            创建的 LiveGrade 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        raise RuntimeError(f"暂不支持创建LiveGrade对象")
        # TODO 需要修改DB文件grade字段值
        ok, err = osis_livegrade_crowd(name, code, live_load_type, bridge_type, para)
        if not ok:
            raise RuntimeError(f"创建人群荷载等级 {name} 失败: {err}")
        return self.get(name)

    def create_fatigue(
        self,
        name: str,
        code: Literal["JTGD60_2015"] = "JTGD60_2015",
        live_load_type: Literal["FATIGUE_I", "FATIGUE_II", "FATIGUE_III"] = "FATIGUE_I",
        para: float | None = None,
    ) -> LiveGrade:
        """创建疲劳荷载等级

        Args:
            name: 活载等级名称（对应 strName）
            code: 规范类型（对应 eCode），默认 JTGD60_2015
            live_load_type: 疲劳模型类型（对应 eLiveLoadType）
                - FATIGUE_I: 疲劳模型I
                - FATIGUE_II: 疲劳模型II（需要 para）
                - FATIGUE_III: 疲劳模型III
            para: 车辆中心间距（m）（对应 dPara），仅 FATIGUE_II 时需要

        Returns:
            创建的 LiveGrade 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_livegrade_fatigue(name, code, live_load_type, para)
        if not ok:
            raise RuntimeError(f"创建疲劳荷载等级 {name} 失败: {err}")
        return self.get(name)

    def create_custom(self,
        name: str,
        code: Literal["CUSTOM"] = "CUSTOM",
        live_load_type: Literal["VG"] = "VG",
        grp_num: int = 1,
        veh_grp_layout: list[tuple[float, float]] = (),
    ) -> LiveGrade:
        """创建自定义活载等级

        Args:
            name: 活载等级名称（对应 strName）
            code: 规范类型（对应 eCode），固定为 CUSTOM
            live_load_type: 活载类型（对应 eLiveLoadType），轴载组为 VG
            grp_num: 轴载组数（对应 nGrpNum）
            veh_grp_layout: 距左侧轴的轴距, 轴载

        Returns:
            创建的 LiveGrade 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        layout_flat: list[float] = []
        for pair in veh_grp_layout:
            if len(pair) != 2:
                raise ValueError(
                    f"veh_grp_layout 每项须为 (轴距, 轴载)，当前: {pair!r}"
                )
            layout_flat.extend((float(pair[0]), float(pair[1])))
        ok, err = osis_livegrade_custom(
            name, code, live_load_type, grp_num, layout_flat
        )
        if not ok:
            raise RuntimeError(f"创建自定义活载等级 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除活载等级

        Args:
            name: 活载等级名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_livegrade_del(name)
        if not ok:
            raise RuntimeError(f"删除活载等级 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
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

    def get(self, name: str | list[str]) -> LiveGrade | list[LiveGrade | None] | None:
        """根据名称获取活载等级

        Args:
            name: 活载等级名称，支持单个名称或名称列表

        Returns:
            单个 LiveGrade 对象；如果传入列表则返回对象列表；
            不存在返回 None

        Raises:
            TypeError: 名称类型不支持时抛出
            RuntimeError: 接口调用失败时抛出
        """

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetGradeInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        grades = [LiveGrade._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(grades) == 0:
            return None
        elif len(grades) == 1:
            return grades[0]
        return grades

    def all(self) -> list[LiveGrade]:
        """获取所有活载等级

        Returns:
            全部 LiveGrade 对象列表
        """
        return self._load()

    def count(self) -> int:
        """获取活载等级数量

        Returns:
            活载等级数量
        """
        return len(self._load())

    def clear(self)->None:
        """清空所有活载等级"""
        try:
            [self.delete(lg.name) for lg in self.all()]
        except Exception as e:
            raise Exception(f"清空所有活载等级失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return f"LiveGradeManager()"


class LaneManager:
    """车道管理器
    
    统一管理车道的创建、删除、修改和查询。
    支持两种影响线算法：车道单元法（VE）和横向联系梁法（TCB）。
    """

    def _load(self) -> list[Lane]:
        """从服务端加载所有车道信息（内部使用）
        
        Returns:
            Lane 对象列表
        """
        resp = osis_client("GetAllLaneInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        lanes = [
            Lane._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return lanes

    def create(
        self,
        name: str,
        type: str,
        *args: Any,
        **kwargs: Any,
    ) -> Lane:
        """创建车道（便捷入口，内部转发到对应 create_* 方法）

        type 路由映射：
            * "VE"  → create_ve
            * "TCB" → create_tcb

        Args:
            name: 车道名称
            type: 影响线算法
            *args: 按位置传给对应 create_* 的参数
            **kwargs: 按关键字传给对应 create_* 的参数

        Raises:
            ValueError: 未知 type
            RuntimeError: 创建失败

        Examples:
            >>> live_manager.lane.create("车道1", "VE", length=30.0, wheel=1.8, ref_elems="主梁", offset_y=2.5)
            >>> live_manager.lane.create("重车道", "TCB", crossbeam_elems="横梁", length=30.0, wheel=1.8, ref_elems="主梁")
        """
        _creator = {
            "VE":  self.create_ve,
            "TCB": self.create_tcb,
        }
        type_key = type.upper()
        if type_key not in _creator:
            raise ValueError(
                f"未知影响线算法: {type!r}，支持: {', '.join(_creator)}"
            )
        return _creator[type_key](name, *args, **kwargs)

    def create_ve(
        self,
        name: str,
        length: float = None,
        wheel: float = 0,
        orientation: Literal[-1, 0, 1] = 0,
        ref: Literal[0, 1] = 0,
        ref_elems: str | None = None,
        offset_y: float = 0.0,
        offset_z: float = 0.0,
        spline_name: str | None = None,
    ) -> Lane:
        """创建车道（车道单元法 VE）

        适用于主梁为梁单元的桥梁结构，车辆沿纵向路径移动。

        Args:
            name: 车道名称
            length: 桥梁跨度（m）
            wheel: 轮距
            orientation: 车辆移动方向
                - -1: 向后
                - 0: 往返（默认）
                - 1: 向前
            ref: 车道参照方式
                - 0: 参照单元组（默认）
                - 1: 参照样条曲线
            ref_elems: 参照纵梁单元组名称（ref=0 时必填）
            offset_y: Y方向偏移量（m），默认 0.0
            offset_z: Z方向偏移量（m），默认 0.0
            spline_name: 样条曲线名称（ref=1 时必填）

        Returns:
            创建的 Lane 对象

        Raises:
            RuntimeError: 参数校验失败或创建失败时抛出
        """
        if ref == 0:
            if not ref_elems:
                raise RuntimeError(f"参照单元组名称 ref_elems 不能为空")
            param = [ref_elems, offset_y, offset_z]
        else:
            if not spline_name:
                raise RuntimeError(f"样条曲线名称 spline_name 不能为空")
            param = [spline_name]

        ok, err = osis_lane_ve(name, "VE", length, wheel, orientation, ref, param)
        if not ok:
            raise RuntimeError(f"创建车道 {name} 失败: {err}")
        return self.get(name)

    def create_tcb(
        self,
        name: str,
        crossbeam_elems: str,
        length: float = None,
        wheel: float = 0,
        orientation: Literal[-1, 0, 1] = 0,
        ref: Literal[0, 1] = 0,
        ref_elems: str | None = None,
        offset_y: float = 0.0,
        offset_z: float = 0.0,
        spline_name: str | None = None,
    ) -> Lane:
        """创建车道（横向联系梁法 TCB）

        适用于由主梁+横梁组成的空间传力结构，荷载先分配给横梁再传递至主梁。

        Args:
            name: 车道名称
            crossbeam_elems: 横梁单元组名称
            length: 桥梁跨度（m）
            wheel: 轮距
            orientation: 车辆移动方向
                - -1: 向后
                - 0: 往返（默认）
                - 1: 向前
            ref: 车道参照方式
                - 0: 参照单元组（默认）
                - 1: 参照样条曲线
            ref_elems: 参照纵梁单元组名称（ref=0 时必填）
            offset_y: Y方向偏移量（m），默认 0.0
            offset_z: Z方向偏移量（m），默认 0.0
            spline_name: 样条曲线名称（ref=1 时必填）

        Returns:
            创建的 Lane 对象

        Raises:
            RuntimeError: 参数校验失败或创建失败时抛出
        """
        if ref == 0:
            if not ref_elems:
                raise RuntimeError(f"参照单元组名称 ref_elems 不能为空")
            param = [ref_elems, offset_y, offset_z]
        else:
            if not spline_name:
                raise RuntimeError(f"样条曲线名称 spline_name 不能为空")
            param = [spline_name]

        ok, err = osis_lane_tcb(name, "TCB", crossbeam_elems, length, wheel, orientation, ref, param)
        if not ok:
            raise RuntimeError(f"创建车道 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除车道

        Args:
            name: 车道名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_lane_del(name)
        if not ok:
            raise RuntimeError(f"删除车道 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
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

    def get(self, name: str | list[str]) -> Lane | list[Lane | None] | None:
        """根据名称获取车道

        Args:
            name: 车道名称，支持单个名称或名称列表

        Returns:
            单个 Lane 对象；如果传入列表则返回对象列表；
            不存在返回 None

        Raises:
            TypeError: 名称类型不支持时抛出
            RuntimeError: 接口调用失败时抛出
        """

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetLaneInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        lanes = [Lane._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(lanes) == 0:
            return None
        elif len(lanes) == 1:
            return lanes[0]
        return lanes

    def all(self) -> list[Lane]:
        """获取所有车道

        Returns:
            全部 Lane 对象列表
        """
        return self._load()

    def count(self) -> int:
        """获取车道数量

        Returns:
            车道数量
        """
        return len(self._load())

    def clear(self)->None:
        """清空所有车道"""
        try:
            [self.delete(l.name) for l in self.all()]
        except Exception as e:
            raise Exception(f"清空所有车道失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return f"LaneManager()"


class LiveCaseManager:
    """活载工况管理器
    
    统一管理活载工况的创建、删除、修改和查询。
    活载工况包含多个子工况，每个子工况对应一种加载方案。
    """

    def _load(self) -> list[LiveCase]:
        """从服务端加载所有活载工况信息（内部使用）
        
        Returns:
            LiveCase 对象列表
        """
        resp = osis_client("GetAllLiveInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        lives = [
            LiveCase._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return lives

    def create(
        self,
        name: str,
        code: Literal["JTGD60_2015"] = "JTGD60_2015",
        sub_cmb_type: Literal[0, 1] = 1,
    ) -> LiveCase:
        """创建活载工况

        Args:
            name: 活载工况名称
            code: 规范名，默认 JTGD60_2015
            sub_cmb_type: 子工况组合类型
                - 1: 单独（包络，默认）
                - 0: 组合（相加）

        Returns:
            创建的 LiveCase 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_live_analysis(name, code, sub_cmb_type)
        if not ok:
            raise RuntimeError(f"创建活载工况 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除活载工况

        Args:
            name: 活载工况名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_live_analysis_del(name)
        if not ok:
            raise RuntimeError(f"删除活载工况 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
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

    def get(self, name: str | list[str]) -> LiveCase | list[LiveCase | None] | None:
        """根据名称获取活载工况

        Args:
            name: 活载工况名称，支持单个名称或名称列表

        Returns:
            单个 LiveCase 对象；如果传入列表则返回对象列表；
            不存在返回 None

        Raises:
            TypeError: 名称类型不支持时抛出
            RuntimeError: 接口调用失败时抛出
        """

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetLiveInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        lives = [LiveCase._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(lives) == 0:
            return None
        elif len(lives) == 1:
            return lives[0]
        return lives

    def all(self) -> list[LiveCase]:
        """获取所有活载工况

        Returns:
            全部 LiveCase 对象列表
        """
        return self._load()

    def count(self) -> int:
        """获取活载工况数量

        Returns:
            活载工况数量
        """
        return len(self._load())

    def clear(self)->None:
        """清空所有荷载工况"""
        try:
            [self.delete(lc.name) for lc in self.all()]
        except Exception as e:
            raise Exception(f"清空所有荷载工况失败: {e}")

    def __repr__(self) -> str:
        return f"LiveCaseManager()"


# ──────────────────────────────────────────────
# 主管理器
# ──────────────────────────────────────────────


class LiveManager:
    """活载管理器

    统一管理活载等级、车道和活载工况。通过子管理器属性访问具体功能：

    - ``grade``: 活载等级管理器（LiveGradeManager）
    - ``lane``: 车道管理器（LaneManager）
    - ``case``: 活载工况管理器（LiveCaseManager）

        用法示例::

        >>> from pyosis.live import live_manager
        >>>
        >>> # 创建活载等级
        >>> grade = live_manager.grade.create_highway("简支空心板移动荷载",code="JTGD60_2015",live_load_type="HIGHWAY_I")
        >>>
        >>> # 创建车道（VE 车道单元法）
        >>> lane = live_manager.lane.create_ve(name="车道1",length=30.0,wheel=1.80,orientation=1,ref=0,ref_elems="主梁单元",offset_y=2.5,offset_z=0.0)
        >>>
        >>> # 创建活载工况并添加子工况
        >>> live_case = live_manager.case.create("活载工况1", "JTGD60_2015", 1)
        >>> live_case.create_sub(sub_name="子工况1",grade_name="简支空心板移动荷载",scalar=1,calc_mu=True,bridge_type="SIMPLE",mu_params=[30.0, 3.45e10, 0.5, 2500.0],lane_names=["车道1"])
    """

    def __init__(self) -> None:
        self._grade_manager = LiveGradeManager()
        self._lane_manager = LaneManager()
        self._case_manager = LiveCaseManager()

    @property
    def grade(self) -> LiveGradeManager:
        """活载等级管理器
        
        提供活载等级的增删改查功能。
        
        用法::
            
            >>> live_manager.grade.create_highway("公路I级")
            >>> live_manager.grade.all()
            >>> live_manager.grade.get("公路I级")
        """
        return self._grade_manager

    @property
    def lane(self) -> LaneManager:
        """车道管理器
        
        提供车道的增删改查功能。
        
        用法::
            
            >>> live_manager.lane.create_ve("车道1", 30.0, ref_elems="主梁")
            >>> live_manager.lane.all()
            >>> live_manager.lane.get("车道1")
        """
        return self._lane_manager

    @property
    def case(self) -> LiveCaseManager:
        """活载工况管理器
        
        提供活载工况的增删改查功能。
        
        用法::
            
            >>> live_manager.case.create("活载工况1")
            >>> live_manager.case.all()
            >>> live_manager.case.get("活载工况1")
        """
        return self._case_manager

    def count(self) -> dict[str, int]:
        """获取活载各组件数量
        
        Returns:
            活载等级、车道、活载工况数量的字典
        """
        return {
            "grades": self._grade_manager.count(),
            "lanes": self._lane_manager.count(),
            "cases": self._case_manager.count(),
        }

    def clear(self) -> None:
        try:
            self.case.clear()  # 先删工况
            self.lane.clear()  # 再删车道
            self.grade.clear()  # 最后删等级
        except Exception as e:
            raise Exception(f"清空所有活载管理器失败: {e}")

    def __repr__(self) -> str:
        return f"LiveManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

live_manager = LiveManager()
