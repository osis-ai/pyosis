"""动力分析管理器 - 统一管理荷载转换质量、模态分析和地震反应谱

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 支持荷载转换质量、自振模态分析、地震反应谱分析
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .load_to_mass import (
    osis_ltm_anal,
    osis_ltm_anal_del,
    osis_ltm_anal_mod,
    osis_ltm_anal_inc,
)
from .modal import osis_mod_opt
from .seismic import (
    osis_seis_rsp_spec_import,
    osis_seis_rsp_spec_code,
    osis_seis_rsp_spec_del,
    osis_seis_rsp_spec_mod,
    osis_rspec_anal,
    osis_rspec_anal_del,
    osis_rspec_anal_mod,
)
from ..core.client import osis_client

@dataclass(frozen=False)
class LoadToMassLcPara:
  """荷载转换质量中的单个荷载工况参数"""
  load_case: str
  mass_factor: float
  g: float
  mass_dir: list[int] = field(default_factory=lambda: [1, 1, 1])  # [X, Y, Z]
  trans_node_force: bool = True   # transNForce
  trans_beam_force: bool = True   # transBForce
  trans_surface_force: bool = False  # transSForce
  @classmethod
  def _from_dict(cls, d: dict) -> LoadToMassLcPara:
      return cls(
          load_case=d.get("loadCase"),
          mass_factor=d.get("massFactor"),
          g=d.get("G"),
          mass_dir=list(d.get("massDir") or [1, 1, 1]),
          trans_node_force=bool(d.get("transNForce")),
          trans_beam_force=bool(d.get("transBForce")),
          trans_surface_force=bool(d.get("transSForce")),
      )
# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────
@dataclass(frozen=False)
class LoadToMass:
    name: str
    no: int
    analysis_type: int = 0
    ok: bool = False
    related_stages: list[int] = field(default_factory=list)
    lc_paras_count: int = 0
    lc_paras: list[LoadToMassLcPara] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict) -> LoadToMass:
        return cls(
            name=d.get("name"),
            no=d.get("no"),
            analysis_type=d.get("analysisType", 0),
            ok=bool(d.get("ok")),
            related_stages=list(d.get("relatedStages") or []),
            lc_paras_count=d.get("lcParasCount", 0),
            lc_paras=[
                LoadToMassLcPara._from_dict(p)
                for p in (d.get("lcParas") or [])
                if isinstance(p, dict)
            ],
        )

class LoadToMassManager:
    """荷载转换质量管理器
    统一管理荷载转换质量的创建、删除、修改和查询。

    """
    def __init__(self) -> None:
        ...
    def _load(self) -> list[LoadToMass]:
        """从服务端加载所有荷载转换质量信息"""
        resp = osis_client("GetAllLoadToMassInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        ltm = [LoadToMass._from_dict(d) for d in resp.get("data", [])]
        return ltm

    def get(self, name: str | list[str]) -> LoadToMass | list[LoadToMass | None] | None:
        """根据名称获取荷载转换质量"""

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        resp = osis_client("GetLoadToMassInfoByNames", {"name": names})
        if not resp['success']: 
            raise RuntimeError(f"{resp['error']}")
        ltm = [LoadToMass._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(ltm) == 0:
            return None
        elif len(ltm) == 1:
            return ltm[0]
        return ltm
        
    def all(self) -> list[LoadToMass]:
        """获取所有荷载转换质量"""
        return self._load()

    def create_ltm(self, name: str) -> None:
        """创建或修改荷载转换质量总体信息。

        Args:
            name: 荷载转换质量标识名称
        Note:
            - 无论荷载工况是否被激活，均可转化为质量
        """
        ok, err = osis_ltm_anal(name)
        if not ok:
            raise RuntimeError(f"创建荷载转换质量 {name} 失败: {err}")

    def delete_ltm(self, name: str) -> None:
        """删除荷载转换质量。

        Args:
            name: 荷载转换质量标识名称
        """
        ok, err = osis_ltm_anal_del(name)
        if not ok:
            raise RuntimeError(f"删除荷载转换质量 {name} 失败: {err}")

    def renumber_ltm(self, old_no: int, new_no: int) -> None:
        """修改荷载转换质量编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_ltm_anal_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改荷载转换质量编号 {old_no} -> {new_no} 失败: {err}")

    def add_ltm(
        self,
        name: str,
        lc_name: str,
        mass_factor: float,
        g: float,
        bx: Literal[0, 1] = 1,
        by: Literal[0, 1] = 1,
        bz: Literal[0, 1] = 1,
        bnf: Literal[0, 1] = 1,
        bbf: Literal[0, 1] = 1,
        bsf: Literal[0, 1] = 1,
    ) -> None:
        """添加荷载转换质量项。

        Args:
            name: 荷载转换质量标识
            lc_name: 荷载工况名称
            mass_factor: 质量系数
            g: 重力加速度值
            bx: 质量方向，0=不考虑X向，1=考虑X向
            by: 质量方向，0=不考虑Y向，1=考虑Y向
            bz: 质量方向，0=不考虑Z向，1=考虑Z向
            bnf: 0=不转换节点荷载，1=转换节点荷载
            bbf: 0=不转换梁荷载，1=转换梁荷载
            bsf: 0=不转换面荷载，1=转换面荷载

        Note:
            - 无论荷载工况是否被激活，均可转化为质量
        """
        ok, err = osis_ltm_anal_inc(
            name, "a", lc_name, mass_factor, g, bx, by, bz, bnf, bbf, bsf
        )
        if not ok:
            raise RuntimeError(f"添加荷载转换质量项 {lc_name} 到 {name} 失败: {err}")

    def remove_ltm(self, name: str, lc_name: str) -> None:
        """移除荷载转换质量项。

        Args:
            name: 荷载转换质量标识
            lc_name: 荷载工况名称
        """
        ok, err = osis_ltm_anal_inc(name, "r", lc_name, 0.0, 0.0)
        if not ok:
            raise RuntimeError(f"移除荷载转换质量项 {lc_name} 从 {name} 失败: {err}")

class ModOptManager:
    """模态分析管理器"""
    def set_modal_opt(self, num: int = 1) -> None:
        """定义模态分析所需的特征值最大数目。

        Args:
            num: 需要计算的特征值最大数目，缺省值：1
        """
        ok, err = osis_mod_opt(num)
        if not ok:
            raise RuntimeError(f"设置模态分析选项失败: {err}")

@dataclass(frozen=False)
class SeisRspSpec:
    A: float #水平地震动峰值加速度系数
    Cd: float #阻尼调整系数
    Ci: float #重要性系数
    Cs: float #场地系数
    Smax: float #谱值上限
    Tg: float #特征周期
    Tmax: float #曲线计算最长周期
    analysisType: int #分析类型枚举
    bridgeType: int #桥梁类别枚举
    characPeriod: int #分区特征周期相关
    co: list[float] #规范系数向量
    code: int #采用的抗震规范类型
    curve: list[dict] #反应谱离散点
    dataType: int #谱数据类型枚举
    dataTypeName: str #数据类型名称
    deltaT: float #周期间隔
    directionHorizontal: bool #水平/竖向谱方向
    fortificationIntensity:int #设防烈度
    fortificationLevel: bool #设防水准
    g: float #重力加速度
    inputType: bool #输入类型开关
    isLongSpan: bool #是否大跨/特殊桥分类
    kind: str #规范生成谱
    ksi: float #阻尼比
    name: str #反应谱函数名称
    no: int #特性编号
    relatedAnalysis: list[str] #关联的分析工况名称列表
    relatedStages: list #关联的施工阶段编号列表
    site: int #场地类别

    @classmethod
    def _from_dict(cls, d: dict) -> SeisRspSpec:
        return cls(
            A=d.get("A"),
            Cd=d.get("Cd"),
            Ci=d.get("Ci"),
            Cs=d.get("Cs"),
            Smax=d.get("Smax"),
            Tg=d.get("Tg"),
            Tmax=d.get("Tmax"),
            analysisType=d.get("analysisType"),
            bridgeType=d.get("bridgeType"),
            characPeriod=d.get("characPeriod"),
            co=d.get("co"),
            code=d.get("code"),
            curve=d.get("curve"),
            dataType=d.get("dataType"),
            dataTypeName=d.get("dataTypeName"),
            deltaT=d.get("deltaT"),
            directionHorizontal=d.get("directionHorizontal"),
            fortificationIntensity=d.get("fortificationIntensity"),
            fortificationLevel=d.get("fortificationLevel"),
            g=d.get("g"),
            inputType=d.get("inputType"),
            isLongSpan=d.get("isLongSpan"),
            kind=d.get("kind"),
            ksi=d.get("ksi"),
            name=d.get("name"),
            no=d.get("no"),
            relatedAnalysis=d.get("relatedAnalysis"),
            relatedStages=d.get("relatedStages"),
            site=d.get("site"),
        )

class SeisRspSpecManager:
    """地震反应谱管理器
    统一管理地震反应谱的创建、删除、修改和查询。
    """
    def __init__(self):
        pass

    def _load(self) -> list[SeisRspSpec]:
        """从服务端加载所有地震反应谱信息"""
        resp = osis_client("GetAllSeisRspSpecInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        rsp = [SeisRspSpec._from_dict(d) for d in resp.get("data", [])]
        return rsp

    def get(self, name: str | list[str]) -> SeisRspSpec | list[SeisRspSpec | None] | None:
        """根据名称获取地震反应谱"""

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        resp = osis_client("GetSeisRspSpecByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        rsp = [SeisRspSpec._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(rsp) == 0:
            return None
        elif len(rsp) == 1:
            return rsp[0]
        return rsp

    def all(self) -> list[SeisRspSpec]:
        """获取所有地震反应谱"""
        return self._load()

    def create_rsp_spec(
            self,
            name: str,
            spec_type: Literal["N", "A", "V", "D"],
            g: float,
            spectrum_data: list[tuple[float, float]],
    ) -> None:
        """创建导入类型地震反应谱。

        Args:
            name: 反应谱名称
            spec_type: 谱类型，N=无量纲加速度谱，A=加速度谱，V=速度谱，D=位移谱
            g: 输入g值
            spectrum_data: 反应谱数据列表，每个元素为 (周期, 谱值) 元组
        """
        if spectrum_data and isinstance(spectrum_data[0], tuple):
            n_num = len(spectrum_data)
            flat = [v for pair in spectrum_data for v in pair]
        else:
            flat = list(spectrum_data)
            n_num = len(flat) // 2
        ok, err = osis_seis_rsp_spec_import(name, spec_type, g, 0, n_num, flat)
        if not ok:
            raise RuntimeError(f"创建地震反应谱 {name} 失败: {err}")

    def create_rsp_spec_code(
            self,
            name: str,
            spec_type: Literal["N", "A", "V", "D"],
            g: float,
            input_type: int,
            code: str = "JTGT_2231_01_2020",
            bridge_type: Literal["A", "B", "C", "D"] = "A",
            is_long_span: Literal[0, 1] = 0,
            level: Literal[0, 1] = 0,
            intensity: float = 0.2,
            site: Literal[0, 1, 2, 3, 4] = 2,
            direction: Literal[0, 1] = 0,
            period: float = 0.35,
            ksi: float = 0.05,
            t: float = 6.0,
            delta_t: float = 0.01,
    ) -> None:
        """创建按规范生成类型地震反应谱。

        Args:
            name: 反应谱名称
            spec_type: 谱类型，N=无量纲加速度谱，A=加速度谱，V=速度谱，D=位移谱
            g: 输入g值
            input_type:类型，1 = 按规范生成
            code: 规范名称，如 "JTGT_2231_01_2020"
            bridge_type: 桥梁类别，A/B/C/D
            is_long_span: 0=非高速公路和一级公路上的B类大桥特大桥，1=高速公路和一级公路上的B类大桥特大桥
            level: 设防水准，0=E1，1=E2
            intensity: 设防烈度
            site: 场地类型，0=I0, 1=I1, 2=Ⅱ, 3=Ⅲ, 4=Ⅳ
            direction: 方向，0=水平，1=竖直
            period: 分区特征周期
            ksi: 阻尼比
            t: 最长周期
            delta_t: 周期间隔
        """
        ok, err = osis_seis_rsp_spec_code(
            name, spec_type, g, input_type,
            code, bridge_type, is_long_span, level, intensity,
            site, direction, period, ksi, t, delta_t
        )
        if not ok:
            raise RuntimeError(f"创建规范地震反应谱 {name} 失败: {err}")

    def delete_rsp_spec(self, name: str) -> None:
        """删除地震反应谱。

        Args:
            name: 反应谱名称
        """
        ok, err = osis_seis_rsp_spec_del(name)
        if not ok:
            raise RuntimeError(f"删除地震反应谱 {name} 失败: {err}")

    def renumber_rsp_spec(self, old_no: int, new_no: int) -> None:
        """修改地震反应谱编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        ok, err = osis_seis_rsp_spec_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改地震反应谱编号 {old_no} -> {new_no} 失败: {err}")

@dataclass(frozen=False)
class RspecAnal:
    analysisType: int #分析类型枚举
    angle: float #水平地震动的入射角度，单位为度（°）
    cmb: int #振型组合方法枚举值
    cmbName: str #组合方法名称
    damping: str #阻尼模型名称
    directionHorizontal: bool #水平/竖向谱方向开关
    interpolateLinear: bool #谱荷载插值方法开关
    modalNum: int #组合的模态数量
    name: str #工况名称
    no: int #特性编号
    relatedStages: list[int] #关联的施工阶段编号列表
    scalar: float #工况缩放系数
    seisSpec: str #反应谱荷载名称，关联的地震反应谱
    
    @classmethod
    def _from_dict(cls, d: dict) -> RspecAnal:
        return cls(
            analysisType=d.get("analysisType"),
            angle=d.get("angle"),
            cmb=d.get("cmb"),
            cmbName=d.get("cmbName"),
            damping=d.get("damping"),
            directionHorizontal=d.get("directionHorizontal"),
            interpolateLinear=d.get("interpolateLinear"),
            modalNum=d.get("modalNum"),
            name=d.get("name"),
            no=d.get("no"),
            relatedStages=d.get("relatedStages"),
            scalar=d.get("scalar"),
            seisSpec=d.get("seisSpec"),
        )

class RspecAnalManager:
    """反应谱工况管理器
    统一管理反应谱工况的创建、删除、修改和查询。
    """
    def __init__(self):
        ...

    def _load(self) -> list[RspecAnal]:
        """从服务端加载所有反应谱工况信息"""
        resp = osis_client("GetAllSeisRespSpecInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        rsp = [RspecAnal._from_dict(d) for d in resp.get("data", [])]
        return rsp

    def get(self, name: str | list[str]) -> RspecAnal | list[RspecAnal | None] | None:
        """根据名称获取反应谱工况"""

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        resp = osis_client("GetSeisRespSpecByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        rsp = [RspecAnal._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(rsp) == 0:
            return None
        elif len(rsp) == 1:
            return rsp[0]
        return rsp

    def all(self) -> list[RspecAnal]:
        """获取所有反应谱工况"""
        return self._load()

    def create_rspec_anal(
            self,
            name: str,
            spectrum: str,
            direction: Literal[1, 0] = 1,
            angle: float = 0.0,
            scalar: float = 1.0,
            interpolated: Literal[1, 0] = 1,
            cmb: Literal["SRSS", "CQC"] = "CQC",
            damping_name: str = "",
            num: int = 1,
    ) -> None:
        """定义或修改反应谱工况。

        Args:
            name: 工况名称
            spectrum: 反应谱荷载名称
            direction: 方向，1=水平，0=竖向
            angle: 水平地震动的入射角度，单位为度（°）
            scalar: 工况缩放系数
            interpolated: 谱荷载插值方法，1=线性，0=对数
            cmb: 结构振型响应的组合方法，SRSS/CQC
            damping_name: 阻尼模型名称
            num: 组合的模态数量
        """
        ok, err = osis_rspec_anal(
            name, direction, angle, scalar, spectrum,
            interpolated, cmb, damping_name, num
        )
        if not ok:
            raise RuntimeError(f"创建反应谱工况 {name} 失败: {err}")

    def delete_rspec_anal(self, name: str) -> None:
        """删除反应谱工况。

        Args:
            name: 工况名称
        """
        ok, err = osis_rspec_anal_del(name)
        if not ok:
            raise RuntimeError(f"删除反应谱工况 {name} 失败: {err}")

    def renumber_rspec_anal(self, old_no: int, new_no: int) -> None:
        """修改反应谱工况编号。

        Args:
            old_no: 旧编号
            new_no: 新编号
        """
        raise RuntimeError(f"暂不支持修改反应谱工况编号")
        ok, err = osis_rspec_anal_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改反应谱工况编号 {old_no} -> {new_no} 失败: {err}")

class DynamicManager:
    """动力分析管理器

    统一管理荷载转换质量、自振模态分析和地震反应谱分析。

    用法:
    >>> from pyosis.dynamic import dynamic_manager
    >>> # 荷载转换质量
    >>> dynamic_manager.load_to_mass.create_ltm("LTM1")
    >>> dynamic_manager.load_to_mass.add_ltm("LTM1", "D", 1.0, 9.806)
    >>> # 模态分析
    >>> dynamic_manager.mod_opt.set_modal_opt(10)
    >>> # 地震反应谱
    >>> data = [(0.1, 0.5), (0.2, 0.8)]
    >>> dynamic_manager.seis_rsp_spec_mod.create_rsp_spec("RS1", "A", 9.806, data)
    >>> # 反应谱工况
    >>> dynamic_manager.rspec_anal.create_rspec_anal("RA1", "RS1", num=10)
    """

    def __init__(self) -> None:
        self._load_to_mass = LoadToMassManager()
        self._mod_opt = ModOptManager()
        self._seis_rsp_spec = SeisRspSpecManager()
        self._rspec_anal = RspecAnalManager()

    @property
    def load_to_mass(self)-> LoadToMassManager:
        return self._load_to_mass

    @property
    def mod_opt(self) -> ModOptManager:
        return self._mod_opt

    @property
    def seis_rsp_spec_mod(self) -> SeisRspSpecManager:
        return self._seis_rsp_spec

    @property
    def rspec_anal(self) -> RspecAnalManager:
        return self._rspec_anal


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

dynamic_manager = DynamicManager()
