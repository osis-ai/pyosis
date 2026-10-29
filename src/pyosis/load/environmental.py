"""
Interfaces of OSIS functions

========

环境荷载相关

水动力系数表（HydroCoeff）与海况分析（SeastAnal）。
海况分析下可挂波浪、海流、风三类荷载（SeastAnalInc）。

"""

from typing import Literal

from ..core import REGISTRY


# ──────────────────────────────────────────────
# 水动力系数表
# ──────────────────────────────────────────────


@REGISTRY.register("HydroCoeff")
def osis_hydro_coeff(
    strIndex: str,
    eType: Literal["UD"],
    nUseCleanValForFouled: int,
    nModCmDiff: int,
    coeffs: list = None,
):
    """
    创建水动力系数表

    命令流：HydroCoeff, Index, Type, UseCleanValForFouled, ModCmDiff,
            Diameter_i, Cd_i, CdT_i, Cm_i, CmT_i, ...

    Args:
        strIndex (str): 水动力系数表索引（Index）
        eType (str): 类型
            * UD = 用户定义
        nUseCleanValForFouled (int): 是否考虑构件粗糙度
            * 0 = 不考虑构件粗糙度
            * 1 = 考虑构件粗糙度
        nModCmDiff (int): 是否修正惯性项系数
            * 0 = 不修正惯性项系数
            * 1 = 修正惯性项系数
        coeffs (list): 各直径对应的系数，按直径逐组平铺填入：
            [Diameter_1, Cd_1, CdT_1, Cm_1, CmT_1,
             Diameter_2, Cd_2, CdT_2, Cm_2, CmT_2, ...]
            每组 5 个参数：直径, 拖曳力系数, 横向拖曳力系数,
            惯性力系数, 横向惯性力系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("HydroCoeffDel")
def osis_hydro_coeff_del(strIndex: str):
    """
    删除水动力系数表

    命令流：HydroCoeffDel, Index

    Args:
        strIndex (str): 水动力系数表索引（Index）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("HydroCoeffMod")
def osis_hydro_coeff_mod(strOldIndex: str, strNewIndex: str):
    """
    修改水动力系数表索引

    命令流：HydroCoeffMod, OldName, NewName

    Args:
        strOldIndex (str): 原索引（OldName）
        strNewIndex (str): 新索引（NewName）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


# ──────────────────────────────────────────────
# 海况分析
# ──────────────────────────────────────────────


@REGISTRY.register("SeastAnal")
def osis_seast_anal(
    strIndex: str,
    strHydroCoeff: str,
    strTransientAnalConfig: str = None,
):
    """
    创建海况分析

    命令流：SeastAnal, Index, HydroCoeff, TransientAnalConfig

    Args:
        strIndex (str): 海况分析索引（Index）
        strHydroCoeff (str): 水动力系数表索引（HydroCoeff），
            索引到 HydroCoeff 命令配置的对象
        strTransientAnalConfig (str): 瞬态分析选项（TransientAnalConfig），
            索引到 ImplConfig 命令配置的对象；可缺省，缺省时只进行相位扫描

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("SeastAnalMod")
def osis_seast_anal_mod(strOldIndex: str, strNewIndex: str):
    """
    修改海况分析索引

    命令流：SeastAnalMod, oldIndex, newIndex

    Args:
        strOldIndex (str): 原索引（oldIndex）
        strNewIndex (str): 新索引（newIndex）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("SeastAnalDel")
def osis_seast_anal_del(strIndex: str):
    """
    删除海况分析

    命令流：SeastAnalDel, Index

    Args:
        strIndex (str): 海况分析索引（Index）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("SeastAnalInc")
def osis_seast_anal_inc_wave(
    strIndex: str,
    eOP: Literal["a", "s", "d"],
    eType: Literal["WAVE"] = "WAVE",
    eWaveTheory: Literal["Airy", "Stokes"] = None,
    dHeight: float = None,
    nIsPeriod: int = None,
    dVal: float = None,
    dDirection: float = None,
    dKinematicFactor: float = None,
    nWaveOrder: int = None,
    eCrestUnit: Literal["Degrees", "Length", "Time"] = None,
    dInitialCrestPos: float = None,
    dStepsize: float = None,
    nNumOfCrestPos: int = None,
    eCriticalCriterion: Literal["MM", "MS", "MU", "MD"] = None,
    nIsOverride: int = None,
    dStillWaterDepthOverride: float = None,
    dMudlineElevationOverride: float = None,
    nMinMember: int = None,
    nMaxMember: int = None,
):
    """
    添加/替换/删除海况分析下的波浪荷载

    命令流：SeastAnalInc, Index, OP, Type, WaveTheory, Height, IsPeriod, Val,
            Direction, KinematicFactor, WaveOrder, CrestUnit, InitialCrestPos,
            Stepsize, NumOfCrestPos, CriticalCriterion, IsOverride,
            StillWaterDepthOverride, MudlineElevationOverride, MinMember, MaxMember

    eOP = d（删除）时只写 Index、OP、Type 三项，其余参数留空。

    Args:
        strIndex (str): 海况分析索引（Index）
        eOP (str): 操作
            * a = 添加
            * s = 替换
            * d = 删除
        eType (str): 类型，固定为 WAVE = 波浪
        eWaveTheory (str): 波浪理论
            * Airy
            * Stokes
        dHeight (float): 波高
        nIsPeriod (int): 是否周期定义
            * 1 = 是
            * 0 = 否
        dVal (float): nIsPeriod = 1 时为周期，否则为波长
        dDirection (float): 波浪入射角度
        dKinematicFactor (float): 传播系数
        nWaveOrder (int): 波浪阶数
        eCrestUnit (str): 相位单位
            * Degrees
            * Length
            * Time
        dInitialCrestPos (float): 初始相位
        dStepsize (float): 步长
        nNumOfCrestPos (int): 步数
        eCriticalCriterion (str): 临界荷载准则
            * MM
            * MS
            * MU
            * MD
        nIsOverride (int): 是否重写静水深度或泥面高程
            * 1 = 重写
            * 0 = 不重写
        dStillWaterDepthOverride (float): nIsOverride = 1 时重写静水深度
        dMudlineElevationOverride (float): nIsOverride = 1 时重写泥面高程
        nMinMember (int): 最小自适应分段数量
        nMaxMember (int): 最大自适应分段数量

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("SeastAnalInc")
def osis_seast_anal_inc_current(
    strIndex: str,
    eOP: Literal["a", "s", "d"],
    eType: Literal["CURR"] = "CURR",
    nHasMudlineoverride: int = None,
    dCurrentMudlineoverride: float = None,
    nAppVel: int = None,
    eBlockingOption: Literal["NONE", "USER", "AUTO"] = None,
    dPara: float = None,
    eStretching: Literal["CN", "LN", "NL"] = None,
    nHasMinInline: int = None,
    dMinInlineSpeed: float = None,
    profiles: list = None,
):
    """
    添加/替换/删除海况分析下的海流荷载

    命令流：SeastAnalInc, Index, OP, Type, HasMudlineoverride,
            CurrentMudlineoverride, AppVel, BlockingOption, Para, Stretching,
            HasMinInline, MinInlineSpeed, Height_i, Speed_i, Direction_i, ...

    eOP = d（删除）时只写 Index、OP、Type 三项，其余参数留空。

    Args:
        strIndex (str): 海况分析索引（Index）
        eOP (str): 操作
            * a = 添加
            * s = 替换
            * d = 删除
        eType (str): 类型，固定为 CURR = 海流
        nHasMudlineoverride (int): 是否覆盖海流独立泥面高程
            * 0 = 不覆盖
            * 1 = 覆盖
        dCurrentMudlineoverride (float): 覆盖的海流泥面高程（m）
        nAppVel (int): 是否计算视波速
            * 0 = 不计算视波速
            * 1 = 计算视波速
        eBlockingOption (str): 阻塞选项
            * NONE = 无阻塞
            * USER = 用户指定输入因子
            * AUTO = 自动计算
        dPara (float): eBlockingOption = USER 时为阻塞折减因子（0.0~1.0）；
            eBlockingOption = AUTO 时为阻塞高程
        eStretching (str): 拉伸方式
            * CN = 常数拉伸
            * LN = 线性拉伸
            * NL = 非线性拉伸
        nHasMinInline (int): 是否启用最小顺流修正
            * 0 = 不启用
            * 1 = 启用
        dMinInlineSpeed (float): 最小顺流速度（m/s）
        profiles (list): 各高度处的流速剖面，按高度逐组平铺填入：
            [Height_1, Speed_1, Direction_1,
             Height_2, Speed_2, Direction_2, ...]
            每组 3 个参数：泥面以上高度（m）, 流速（m/s）, 流向角度

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("SeastAnalInc")
def osis_seast_anal_inc_wind(
    strIndex: str,
    eOP: Literal["a", "s", "d"],
    eType: Literal["WIND"] = "WIND",
    nIsVelocity: int = None,
    dVal: float = None,
    dDirection: float = None,
    eWindHeightVariation: Literal[
        "CONSTANT", "21AP", "AP07", "AP08", "AP09", "AP10", "AP11", "AP12", "AP13"
    ] = None,
    dSpecialParameter: float = None,
    nIsOverride: int = None,
    dStillWaterDepthOverride: float = None,
    dMudlineElevationOverride: float = None,
):
    """
    添加/替换/删除海况分析下的风荷载

    命令流：SeastAnalInc, Index, OP, Type, IsVelocity, Val, Direction,
            WindHeightVariation, SpecialParameter, IsOverride,
            StillWaterDepthOverride, MudlineElevationOverride

    eOP = d（删除）时只写 Index、OP、Type 三项，其余参数留空。

    Args:
        strIndex (str): 海况分析索引（Index）
        eOP (str): 操作
            * a = 添加
            * s = 替换
            * d = 删除
        eType (str): 类型，固定为 WIND = 风
        nIsVelocity (int): 是否输入风速
            * 1 = 输入风速
            * 0 = 输入风压
        dVal (float): nIsVelocity = 1 时为风速，否则为风压
        dDirection (float): 风入射角度
        eWindHeightVariation (str): 风高变化准则
            * CONSTANT
            * 21AP
            * AP07
            * AP08
            * AP09
            * AP10
            * AP11
            * AP12
            * AP13
        dSpecialParameter (float): eWindHeightVariation = CONSTANT 时该参数缺省；
            = 21AP 时为平均周期；= APXX 时为参考高度
        nIsOverride (int): 是否重写静水深度及泥面高程
            * 1 = 重写
            * 0 = 不重写
        dStillWaterDepthOverride (float): nIsOverride = 1 时重写静水深度
        dMudlineElevationOverride (float): nIsOverride = 1 时重写泥面高程

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


@REGISTRY.register("SeastateOpt")
def osis_seastate_opt(dWaterDepth: float, dMudlineElevation: float, dWaterDensity: float, eVerticalDirection: Literal["Z"] = "Z"):
    """
    海况全局参数

    命令流：SeastateOpt, WaterDepth, MudlineElevation, WaterDensity, VerticalDirection

    Args:
        dWaterDepth (float): 水深
        dMudlineElevation (float): 泥面高程
        dWaterDensity (float): 水密度
        eVerticalDirection (str): 指定竖直方向，暂时仅支持 Z

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass


# ──────────────────────────────────────────────
# 内部工具
# ──────────────────────────────────────────────


def _flatten_groups(items: list | None, size: int, label: str) -> list:
    """将分组列表或平铺列表统一展平（内部使用）

    items 支持 [[v1, v2, ...], ...] 分组形式，也支持 [v1, v2, ...] 平铺形式，
    每组必须包含 size 个参数。

    Raises:
        ValueError: 分组内参数数量不为 size，或平铺数量不是 size 的整数倍
    """
    if not items:
        return []
    if any(isinstance(it, (list, tuple)) for it in items):
        flat = []
        for it in items:
            if not isinstance(it, (list, tuple)) or len(it) != size:
                raise ValueError(f"{label} 必须按每组 {size} 个参数填入，当前为 {it!r}")
            flat.extend(it)
        return flat
    if len(items) % size != 0:
        raise ValueError(f"{label} 必须按每组 {size} 个参数平铺填入，当前数量为 {len(items)}")
    return list(items)


def _check_payload(op: str, payload: dict) -> None:
    """校验荷载参数是否与命令流字段位置对齐（内部使用）

    命令流按位置读参数，None 表示该字段不写入，
    中间断档会把后面的值读到前一个字段的位置上。

    Raises:
        ValueError: 删除操作携带了荷载参数，或添加/替换时参数断档
    """
    if op == "d":
        extra = [k for k, v in payload.items() if v is not None]
        if extra:
            raise ValueError(f"删除操作不应携带荷载参数: {', '.join(extra)}")
        return
    gap = False
    for key, value in payload.items():
        if value is None:
            gap = True
        elif gap:
            raise ValueError(
                f"荷载参数 {key} 之前的字段未填写，命令流按位置读参数会造成错位，请补齐前面的字段"
            )


# ──────────────────────────────────────────────
# 水动力系数表管理器
# ──────────────────────────────────────────────


class HydroCoeffManager:
    """水动力系数表管理器

    统一管理水动力系数表的创建、删除和改名。

    用法:
        >>> from pyosis.load import environmental_manager
        >>> environmental_manager.coeff.create(1, 1, 0, [[1.0, 1.2, 1.2, 1.0, 1.0]])
        >>> environmental_manager.coeff.rename(1, 2)
        >>> environmental_manager.coeff.delete(2)
    """

    def create(
        self,
        index: str,
        use_clean_val_for_fouled: int,
        mod_cm_diff: int,
        coeffs: list,
    ) -> None:
        """创建水动力系数表

        Args:
            index (str): 水动力系数表索引
            use_clean_val_for_fouled (int): 是否考虑构件粗糙度
                * 0 = 不考虑构件粗糙度
                * 1 = 考虑构件粗糙度
            mod_cm_diff (int): 是否修正惯性项系数
                * 0 = 不修正惯性项系数
                * 1 = 修正惯性项系数
            coeffs (list): 各直径对应的系数，支持两种形式：
                * 分组：[[Diameter_1, Cd_1, CdT_1, Cm_1, CmT_1], ...]
                * 平铺：[Diameter_1, Cd_1, CdT_1, Cm_1, CmT_1, ...]
                每组 5 个参数：直径, 拖曳力系数, 横向拖曳力系数,
                惯性力系数, 横向惯性力系数，至少一组

        Raises:
            ValueError: coeffs 为空或每组参数数量不为 5
            RuntimeError: 创建失败时抛出异常
        """
        flat = _flatten_groups(coeffs, 5, "coeffs")
        if not flat:
            raise ValueError("coeffs 不能为空，至少需要一组 [直径, Cd, CdT, Cm, CmT]")
        ok, err = osis_hydro_coeff(index, "UD", use_clean_val_for_fouled, mod_cm_diff, flat)
        if not ok:
            raise RuntimeError(f"创建水动力系数表 {index} 失败: {err}")

    def delete(self, index: str) -> None:
        """删除水动力系数表

        Args:
            index (str): 水动力系数表索引

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_hydro_coeff_del(index)
        if not ok:
            raise RuntimeError(f"删除水动力系数表 {index} 失败: {err}")

    def rename(self, old_index: str, new_index: str) -> None:
        """修改水动力系数表索引

        Args:
            old_index (str): 原索引
            new_index (str): 新索引

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_hydro_coeff_mod(old_index, new_index)
        if not ok:
            raise RuntimeError(f"修改水动力系数表索引 {old_index} -> {new_index} 失败: {err}")

    def hydro_coeff(
        self,
        index: str,
        type: Literal["UD"],
        use_clean_val_for_fouled: int,
        mod_cm_diff: int,
        *quintuples,
    ) -> None:
        """HydroCoeff 命令流直通：平铺的直径/系数五元组转发到 create

        Args:
            index (str): 水动力系数表索引
            type (str): 类型，当前仅支持 UD
            use_clean_val_for_fouled (int): 是否考虑构件粗糙度
            mod_cm_diff (int): 是否修正惯性项系数
            *quintuples: 平铺的 Diameter_i, Cd_i, CdT_i, Cm_i, CmT_i 字段

        Raises:
            ValueError: 类型不是 UD
            RuntimeError: 创建失败时抛出异常
        """
        if str(type).strip().upper() != "UD":
            raise ValueError(f"未知水动力系数表类型: {type!r}，当前仅支持 UD")
        self.create(index, use_clean_val_for_fouled, mod_cm_diff, list(quintuples))

    def __repr__(self) -> str:
        return "HydroCoeffManager()"


# ──────────────────────────────────────────────
# 海况分析管理器
# ──────────────────────────────────────────────


class SeastAnalManager:
    """海况分析管理器

    统一管理海况分析的创建、删除、改名，以及波浪/海流/风荷载的增删改。
    一个海况分析下每种荷载最多只有一个。

    用法:
        >>> from pyosis.load import environmental_manager
        >>> environmental_manager.analysis.create("S1", "1")
        >>> environmental_manager.analysis.include_wave("S1", wave_theory="Airy", height=1.5)
        >>> environmental_manager.analysis.delete("S1")
    """

    def create(
        self,
        index: str,
        hydro_coeff: str,
        transient_anal_config: str | None = None,
    ) -> None:
        """创建海况分析

        Args:
            index (str): 海况分析索引
            hydro_coeff (str): 水动力系数表索引，索引到 HydroCoeff 配置的对象
            transient_anal_config (str|None): 瞬态分析选项，索引到 ImplConfig
                配置的对象；可缺省，缺省时只进行相位扫描

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_seast_anal(index, hydro_coeff, transient_anal_config)
        if not ok:
            raise RuntimeError(f"创建海况分析 {index} 失败: {err}")

    def delete(self, index: str) -> None:
        """删除海况分析

        Args:
            index (str): 海况分析索引

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_seast_anal_del(index)
        if not ok:
            raise RuntimeError(f"删除海况分析 {index} 失败: {err}")

    def rename(self, old_index: str, new_index: str) -> None:
        """修改海况分析索引

        Args:
            old_index (str): 原索引
            new_index (str): 新索引

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_seast_anal_mod(old_index, new_index)
        if not ok:
            raise RuntimeError(f"修改海况分析索引 {old_index} -> {new_index} 失败: {err}")

    def include(
        self,
        index: str,
        load_type: Literal["WAVE", "CURR", "WIND"],
        op: Literal["a", "s", "d"] = "a",
        **params,
    ) -> None:
        """向海况分析添加/替换/删除荷载

        Args:
            index (str): 海况分析索引
            load_type (str): 荷载类型
                * WAVE = 波浪荷载
                * CURR = 海流荷载
                * WIND = 风荷载
            op (str): 操作
                * a = 添加
                * s = 替换
                * d = 删除（此时不填任何荷载参数）
            **params: 按荷载类型转交 include_wave / include_current / include_wind
                的荷载参数

        Raises:
            ValueError: 未知荷载类型
            RuntimeError: 操作失败时抛出异常
        """
        handlers = {
            "WAVE": self.include_wave,
            "CURR": self.include_current,
            "WIND": self.include_wind,
        }
        type_key = load_type.strip().upper()
        if type_key not in handlers:
            raise ValueError(
                f"未知环境荷载类型: {load_type!r}，支持: {', '.join(handlers)}"
            )
        handlers[type_key](index, op=op, **params)

    def include_wave(
        self,
        index: str,
        op: Literal["a", "s", "d"] = "a",
        wave_theory: Literal["Airy", "Stokes"] = None,
        height: float = None,
        is_period: int = None,
        val: float = None,
        direction: float = None,
        kinematic_factor: float = None,
        wave_order: int = None,
        crest_unit: Literal["Degrees", "Length", "Time"] = None,
        initial_crest_pos: float = None,
        stepsize: float = None,
        num_of_crest_pos: int = None,
        critical_criterion: Literal["MM", "MS", "MU", "MD"] = None,
        is_override: int = None,
        still_water_depth_override: float = None,
        mudline_elevation_override: float = None,
        min_member: int = None,
        max_member: int = None,
    ) -> None:
        """添加/替换/删除海况分析下的波浪荷载

        荷载参数按命令流顺序连续填写，None 表示该字段不写入，
        中间断档会造成后续字段错位，调用时会被拦下。

        Args:
            index (str): 海况分析索引
            op (str): 操作
                * a = 添加
                * s = 替换
                * d = 删除（此时不填任何荷载参数）
            wave_theory (str): 波浪理论
                * Airy
                * Stokes
            height (float): 波高
            is_period (int): 是否周期定义
                * 1 = 是
                * 0 = 否
            val (float): is_period = 1 时为周期，否则为波长
            direction (float): 波浪入射角度
            kinematic_factor (float): 传播系数
            wave_order (int): 波浪阶数
            crest_unit (str): 相位单位
                * Degrees
                * Length
                * Time
            initial_crest_pos (float): 初始相位
            stepsize (float): 步长
            num_of_crest_pos (int): 步数
            critical_criterion (str): 临界荷载准则
                * MM
                * MS
                * MU
                * MD
            is_override (int): 是否重写静水深度或泥面高程
                * 1 = 重写
                * 0 = 不重写
            still_water_depth_override (float): is_override = 1 时重写静水深度
            mudline_elevation_override (float): is_override = 1 时重写泥面高程
            min_member (int): 最小自适应分段数量
            max_member (int): 最大自适应分段数量

        Raises:
            ValueError: 删除操作携带了荷载参数，或添加/替换时参数断档
            RuntimeError: 操作失败时抛出异常
        """
        _check_payload(op, dict(
            wave_theory=wave_theory,
            height=height,
            is_period=is_period,
            val=val,
            direction=direction,
            kinematic_factor=kinematic_factor,
            wave_order=wave_order,
            crest_unit=crest_unit,
            initial_crest_pos=initial_crest_pos,
            stepsize=stepsize,
            num_of_crest_pos=num_of_crest_pos,
            critical_criterion=critical_criterion,
            is_override=is_override,
            still_water_depth_override=still_water_depth_override,
            mudline_elevation_override=mudline_elevation_override,
            min_member=min_member,
            max_member=max_member,
        ))
        ok, err = osis_seast_anal_inc_wave(
            index, op, "WAVE",
            wave_theory, height, is_period, val, direction, kinematic_factor,
            wave_order, crest_unit, initial_crest_pos, stepsize, num_of_crest_pos,
            critical_criterion, is_override, still_water_depth_override,
            mudline_elevation_override, min_member, max_member,
        )
        if not ok:
            raise RuntimeError(f"{'删除' if op == 'd' else '添加'}波浪荷载到海况分析 {index} 失败: {err}")

    def include_current(
        self,
        index: str,
        op: Literal["a", "s", "d"] = "a",
        has_mudline_override: int = None,
        current_mudline_override: float = None,
        app_vel: int = None,
        blocking_option: Literal["NONE", "USER", "AUTO"] = None,
        para: float = None,
        stretching: Literal["CN", "LN", "NL"] = None,
        has_min_inline: int = None,
        min_inline_speed: float = None,
        profiles: list = None,
    ) -> None:
        """添加/替换/删除海况分析下的海流荷载

        荷载参数按命令流顺序连续填写，None 表示该字段不写入，
        中间断档会造成后续字段错位，调用时会被拦下。

        Args:
            index (str): 海况分析索引
            op (str): 操作
                * a = 添加
                * s = 替换
                * d = 删除（此时不填任何荷载参数）
            has_mudline_override (int): 是否覆盖海流独立泥面高程
                * 0 = 不覆盖
                * 1 = 覆盖
            current_mudline_override (float): 覆盖的海流泥面高程（m）
            app_vel (int): 是否计算视波速
                * 0 = 不计算视波速
                * 1 = 计算视波速
            blocking_option (str): 阻塞选项
                * NONE = 无阻塞
                * USER = 用户指定输入因子
                * AUTO = 自动计算
            para (float): blocking_option = USER 时为阻塞折减因子（0.0~1.0）；
                blocking_option = AUTO 时为阻塞高程
            stretching (str): 拉伸方式
                * CN = 常数拉伸
                * LN = 线性拉伸
                * NL = 非线性拉伸
            has_min_inline (int): 是否启用最小顺流修正
                * 0 = 不启用
                * 1 = 启用
            min_inline_speed (float): 最小顺流速度（m/s）
            profiles (list): 各高度处的流速剖面，支持两种形式：
                * 分组：[[Height_1, Speed_1, Direction_1], ...]
                * 平铺：[Height_1, Speed_1, Direction_1, ...]
                每组 3 个参数：泥面以上高度（m）, 流速（m/s）, 流向角度

        Raises:
            ValueError: 删除操作携带了荷载参数，或添加/替换时参数断档，或 profiles 每组参数数量不为 3
            RuntimeError: 操作失败时抛出异常
        """
        _check_payload(op, dict(
            has_mudline_override=has_mudline_override,
            current_mudline_override=current_mudline_override,
            app_vel=app_vel,
            blocking_option=blocking_option,
            para=para,
            stretching=stretching,
            has_min_inline=has_min_inline,
            min_inline_speed=min_inline_speed,
            profiles=profiles,
        ))
        flat = _flatten_groups(profiles, 3, "profiles")
        ok, err = osis_seast_anal_inc_current(
            index, op, "CURR",
            has_mudline_override, current_mudline_override, app_vel,
            blocking_option, para, stretching, has_min_inline, min_inline_speed,
            flat,
        )
        if not ok:
            raise RuntimeError(f"{'删除' if op == 'd' else '添加'}海流荷载到海况分析 {index} 失败: {err}")

    def include_wind(
        self,
        index: str,
        op: Literal["a", "s", "d"] = "a",
        is_velocity: int = None,
        val: float = None,
        direction: float = None,
        wind_height_variation: Literal[
            "CONSTANT", "21AP", "AP07", "AP08", "AP09", "AP10", "AP11", "AP12", "AP13"
        ] = None,
        special_parameter: float = None,
        is_override: int = None,
        still_water_depth_override: float = None,
        mudline_elevation_override: float = None,
    ) -> None:
        """添加/替换/删除海况分析下的风荷载

        荷载参数按命令流顺序连续填写，None 表示该字段不写入，
        中间断档会造成后续字段错位，调用时会被拦下。

        Args:
            index (str): 海况分析索引
            op (str): 操作
                * a = 添加
                * s = 替换
                * d = 删除（此时不填任何荷载参数）
            is_velocity (int): 是否输入风速
                * 1 = 输入风速
                * 0 = 输入风压
            val (float): is_velocity = 1 时为风速，否则为风压
            direction (float): 风入射角度
            wind_height_variation (str): 风高变化准则
                * CONSTANT
                * 21AP
                * AP07
                * AP08
                * AP09
                * AP10
                * AP11
                * AP12
                * AP13
            special_parameter (float): wind_height_variation = CONSTANT 时该参数缺省；
                = 21AP 时为平均周期；= APXX 时为参考高度
            is_override (int): 是否重写静水深度及泥面高程
                * 1 = 重写
                * 0 = 不重写
            still_water_depth_override (float): is_override = 1 时重写静水深度
            mudline_elevation_override (float): is_override = 1 时重写泥面高程

        Raises:
            ValueError: 删除操作携带了荷载参数，或添加/替换时参数断档
            RuntimeError: 操作失败时抛出异常
        """
        _check_payload(op, dict(
            is_velocity=is_velocity,
            val=val,
            direction=direction,
            wind_height_variation=wind_height_variation,
            special_parameter=special_parameter,
            is_override=is_override,
            still_water_depth_override=still_water_depth_override,
            mudline_elevation_override=mudline_elevation_override,
        ))
        ok, err = osis_seast_anal_inc_wind(
            index, op, "WIND",
            is_velocity, val, direction, wind_height_variation, special_parameter,
            is_override, still_water_depth_override, mudline_elevation_override,
        )
        if not ok:
            raise RuntimeError(f"{'删除' if op == 'd' else '添加'}风荷载到海况分析 {index} 失败: {err}")

    def inc(self, index: str, op: Literal["a", "s", "d"], load_type: str, *rest) -> None:
        """SeastAnalInc 命令流直通分发：按荷载类型转发平铺字段

        Args:
            index (str): 海况分析索引
            op (str): 操作，a = 添加、s = 替换、d = 删除
            load_type (str): 荷载类型，WAVE / CURR / WIND
            *rest: 平铺的荷载字段，字段序同命令流（CURR 尾部的
                Height_i, Speed_i, Direction_i 三元组自动收进 profiles）

        Raises:
            ValueError: 未知荷载类型
        """
        type_key = str(load_type).strip().upper()
        if type_key == "WAVE":
            self.include_wave(index, op, *rest)
        elif type_key == "CURR":
            self.include_current(index, op, *rest[:8], profiles=list(rest[8:]) or None)
        elif type_key == "WIND":
            self.include_wind(index, op, *rest)
        else:
            raise ValueError(f"未知环境荷载类型: {load_type!r}，支持 WAVE / CURR / WIND")

    def sea_state_opt(
        self,
        water_depth: float,
        mudline_elevation: float,
        water_density: float,
        vertical_direction: Literal["Z"] = "Z",
    ) -> None:
        """设置海况全局参数

        Args:
            water_depth (float): 水深
            mudline_elevation (float): 泥面高程
            water_density (float): 水密度
            vertical_direction (str): 指定竖直方向，暂时仅支持 Z

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_seastate_opt(water_depth, mudline_elevation, water_density, vertical_direction)
        if not ok:
            raise RuntimeError(f"设置海况全局参数失败: {err}")

    def __repr__(self) -> str:
        return "SeastAnalManager()"


# ──────────────────────────────────────────────
# 环境荷载主管理器
# ──────────────────────────────────────────────


class EnvironmentalManager:
    """环境荷载管理器

    统一管理水动力系数表与海况分析。

    子管理器：
    - coeff: HydroCoeffManager - 水动力系数表
    - analysis: SeastAnalManager - 海况分析

    用法:
        >>> from pyosis.load import environmental_manager
        >>> environmental_manager.coeff.create("1", 1, 0, [[1.0, 1.2, 1.2, 1.0, 1.0]])
        >>> environmental_manager.analysis.create("S1", "1")
    """

    def __init__(self) -> None:
        self._coeff_manager = HydroCoeffManager()
        self._analysis_manager = SeastAnalManager()

    @property
    def coeff(self) -> HydroCoeffManager:
        """水动力系数表管理器"""
        return self._coeff_manager

    @property
    def analysis(self) -> SeastAnalManager:
        """海况分析管理器"""
        return self._analysis_manager

    def __repr__(self) -> str:
        return "EnvironmentalManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

environmental_manager = EnvironmentalManager()
