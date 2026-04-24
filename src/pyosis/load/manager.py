"""荷载管理器 - 统一管理荷载工况的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 无状态设计，每次从服务端加载（与 element/boundary manager 一致）

支持的荷载类型：
- 荷载工况（USER, D, DC, DW, DD, CS）
- 静力荷载（自重、节点荷载、线荷载、面荷载、强迫位移、初始内力、温度荷载、预应力、索力）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from ..core.client import osis_client
from .loadcase import (
    osis_loadcase,
    osis_loadcase_del,
    osis_loadcase_mod,
)
from .tendon import (
    osis_tendon_prop_in_area0,
    osis_tendon_prop_in_area1,
    osis_tendon_prop_ex_area0,
    osis_tendon_prop_ex_area1,
    osis_tendon_prop_pre_area0,
    osis_tendon_prop_pre_area1,
    osis_tendon_prop_del,
    osis_tendon_prop_mod,
    osis_tendon_shape_spl3d,
    osis_tendon_shape_arc3d,
    osis_tendon_shape_arc2d,
    osis_tendon_shape_del,
    osis_tendon_shape_mod,
    osis_layout_tendons,
    osis_wipe_tendons,
)
from .static import (
    osis_load_gravity,
    osis_load_nforce,
    osis_load_line,
    osis_load_surface_load,
    osis_load_surface_load_vector,
    osis_load_displacement,
    osis_load_initial,
    osis_load_utemp,
    osis_load_gtemp,
    osis_load_pst,
    osis_load_cforce,
    osis_load_del,
    osis_load_mod,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────

@dataclass(frozen=False)
class LoadCase:
    """荷载工况对象

    由 ``LoadCaseManager``（全局 ``loadcase_manager``）内部创建，用户不应直接实例化。
    """
    name: str
    load_case_type: str  # "USER", "D", "DC", "DW", "DD", "CS"
    scalar: float
    prompt: str
    related_stages: list[int] = field(default_factory=list)
    
    # 荷载数据
    gravity: dict | None = None                    # 自重荷载
    nforce: list[dict] = field(default_factory=list)    # 节点力
    point_force: list[dict] = field(default_factory=list)    # 节点荷载
    point_moment: list[dict] = field(default_factory=list)    # 节点弯矩
    line: list[dict] = field(default_factory=list)            # 线荷载
    element_surface: list[dict] = field(default_factory=list) # 面荷载
    displacement: list[dict] = field(default_factory=list)    # 强迫位移
    initial: list[dict] = field(default_factory=list)        # 初始内力
    uniform_temp: list[dict] = field(default_factory=list)   # 均匀温度
    gradient_temp: list[dict] = field(default_factory=list)  # 梯度温度
    prestressed: list[dict] = field(default_factory=list)    # 预应力
    cforce: list[dict] = field(default_factory=list)          # 索力

    @classmethod
    def _from_dict(cls, d: dict) -> LoadCase:
        """从接口 dict 构造 LoadCase 对象（内部使用）"""
        return cls(
            name=d.get("name"),
            load_case_type=d.get("type"),
            scalar=d.get("scalar"),
            prompt=d.get("prompt"),
            related_stages=d.get("relatedStages"),
            gravity=d.get("gravity"),
            nforce=d.get("nforce"),
            point_force=d.get("pointForce"),
            point_moment=d.get("pointMoment"),
            line=d.get("line"),
            element_surface=d.get("elementSurface"),
            displacement=d.get("displacement"),
            initial=d.get("initial"),
            uniform_temp=d.get("uniformTemp"),
            gradient_temp=d.get("gradientTemp"),
            prestressed=d.get("prestressed"),
            cforce=d.get("cforce"),
        )

    def _sync_from_dict(self, d: dict) -> None:
        """用 dict 同步当前对象（内部使用）"""
        self.name = d.get("name")
        self.load_case_type = d.get("type")
        self.scalar = d.get("scalar")
        self.prompt = d.get("prompt")
        self.related_stages = d.get("relatedStages")
        self.gravity = d.get("gravity")
        self.nforce = d.get("nforce")
        self.point_force = d.get("pointForce")
        self.point_moment = d.get("pointMoment")
        self.line = d.get("line")
        self.element_surface = d.get("elementSurface")
        self.displacement = d.get("displacement")
        self.initial = d.get("initial")
        self.uniform_temp = d.get("uniformTemp")
        self.gradient_temp = d.get("gradientTemp")
        self.prestressed = d.get("prestressed")
        self.cforce = d.get("cforce")

    def refresh(self) -> LoadCase:
        """刷新当前工况荷载明细并同步到对象属性"""
        resp = osis_client("GetLoadCaseInfoByNames", {"name": [self.name]})
        if not resp['success']:
            raise RuntimeError(f"刷新工况 {self.name} 失败: {resp['error']}")
        data = resp.get("data", [])
        if data and data[0]:
            self._sync_from_dict(data[0])
        return self

    def __repr__(self) -> str:
        return f"LoadCase(name={self.name!r}, type={self.load_case_type}, scalar={self.scalar}, prompt={self.prompt})"

    # ── 荷载添加 ──────────────────────────────

    def create_gravity(
            self,
            dXCoeff: float = 1.0,
            dYCoeff: float = 1.0,
            dZCoeff: float = 1.0,
    ) -> LoadCase:
        """添加自重荷载"""
        ok, err = osis_load_gravity("GRAVITY", self.name, dXCoeff, dYCoeff, dZCoeff)
        if not ok:
            raise RuntimeError(f"添加自重荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_nforce(
            self,
            nEntity: int,
            dFx: float = 100,
            dFy: float = 0,
            dFz: float = 0,
            dMx: float = 0,
            dMy: float = 0,
            dMz: float = 0,
    ) -> LoadCase:
        """添加节点荷载"""
        ok, err = osis_load_nforce("NFORCE", self.name, nEntity, dFx, dFy, dFz, dMx, dMy, dMz)
        if not ok:
            raise RuntimeError(f"添加节点荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_line_load(
            self,
            nEntity: int,
            eCoordSystem: Literal[0, 1] = 1,
            eLoadType: Literal[0, 1] = 1,
            dOffsetXI: float = 0.0,
            dOffsetYI: float = 0.0,
            dOffsetZI: float = 0.0,
            dFXI: float = 100,
            dFYI: float = 100,
            dFZI: float = 0,
            dMXI: float = 0,
            dMYI: float = 0,
            dMZI: float = 0,
            dOffsetXJ: float = 0.0,
            dOffsetYJ: float = 0.0,
            dOffsetZJ: float = 0.0,
            dFXJ: float = 100,
            dFYJ: float = 100,
            dFZJ: float = 0,
            dMXJ: float = 0,
            dMYJ: float = 0,
            dMZJ: float = 0,
    ) -> LoadCase:
        """添加线荷载"""
        ok, err = osis_load_line(
            "LINE", self.name, nEntity, eCoordSystem, eLoadType,
            dOffsetXI, dOffsetYI, dOffsetZI, dFXI, dFYI, dFZI, dMXI, dMYI, dMZI,
            dOffsetXJ, dOffsetYJ, dOffsetZJ, dFXJ, dFYJ, dFZJ, dMXJ, dMYJ, dMZJ,
        )
        if not ok:
            raise RuntimeError(f"添加线荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_displacement(
            self,
            nEntity: int,
            bDX: int = 1,
            dDX: float = 0.0,
            bDY: int = 0,
            dDY: float = 0.0,
            bDZ: int = 0,
            dDZ: float = 0.0,
            bRX: int = 0,
            dRX: float = 0.0,
            bRY: int = 0,
            dRY: float = 0.0,
            bRZ: int = 0,
            dRZ: float = 0.0,
    ) -> LoadCase:
        """添加强迫位移"""
        ok, err = osis_load_displacement(
            "DISPLACEMENT",
            self.name,
            nEntity,
            bDX, dDX,
            bDY, dDY,
            bDZ, dDZ,
            bRX, dRX,
            bRY, dRY,
            bRZ, dRZ,
        )
        if not ok:
            raise RuntimeError(f"添加强迫位移到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_uniform_temperature(
            self,
            nEntity: int,
            eDirect: Literal["X", "Y", "Z"] = "X",
            dTemp: float = 1.0,
            dLength: float = None,
    ) -> LoadCase:
        """添加均匀温度荷载"""
        ok, err = osis_load_utemp("UTEMP", self.name, nEntity, eDirect, dTemp, dLength)
        if not ok:
            raise RuntimeError(f"添加均匀温度荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_gradient_temperature(
            self,
            nEntity: int,
            eDirect: Literal["Y", "Z"] = "Y",
            eGTempType: Literal["R", "T", "C", "B"] = "R",
            nNum: int = 1,
            param: list = None,
    ) -> LoadCase:
        """添加梯度温度荷载"""
        if param is None:
            param = ["", 10, 10, 0, 0]
        ok, err = osis_load_gtemp("GTEMP", self.name, nEntity, eDirect, eGTempType, nNum, param)
        if not ok:
            raise RuntimeError(f"添加梯度温度荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_initial_force(
            self,
            nEntity: int,
            dFXI: float = 100,
            dFYI: float = 100,
            dFZI: float = 0,
            dMXI: float = 0,
            dMYI: float = 0,
            dMZI: float = 0,
            dFXJ: float = 0,
            dFYJ: float = 0,
            dFZJ: float = 0,
            dMXJ: float = 0,
            dMYJ: float = 0,
            dMZJ: float = 0,
    ) -> LoadCase:
        """添加初始内力荷载"""
        ok, err = osis_load_initial(
            "INITIAL",
            self.name,
            nEntity,
            dFXI,
            dFYI,
            dFZI,
            dMXI,
            dMYI,
            dMZI,
            dFXJ,
            dFYJ,
            dFZJ,
            dMXJ,
            dMYJ,
            dMZJ,
        )
        if not ok:
            raise RuntimeError(f"添加初始内力荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_prestress(
            self,
            strEntity: str,
            eTensionType: str = "BOTH",
            eTensionForceType: str = "ST",
            dBeg: float = 100,
            dEnd: float = 100,
    ) -> LoadCase:
        """添加预应力荷载"""
        ok, err = osis_load_pst("PST", self.name, strEntity, eTensionType, eTensionForceType, dBeg, dEnd)
        if not ok:
            raise RuntimeError(f"添加预应力荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_cable_force(
            self,
            nEntity: int,
            eLoadType: str = "IN",
            dForce: float = 100,
    ) -> LoadCase:
        """添加索力荷载"""
        ok, err = osis_load_cforce("CFORCE", self.name, nEntity, eLoadType, dForce)
        if not ok:
            raise RuntimeError(f"添加索力荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_surface_load(
            self,
            strEntity: str,
            strPlanei: str = "1",
            strDir: str = "X",
            strGlobalI: str = "0",
            strP1i: str = "0",
            strP2i: str = "0",
            strP3i: str = "0",
            strP4i: str = "0",
    ) -> LoadCase:
        """添加单元面荷载"""
        ok, err = osis_load_surface_load(
            "ESRFC", self.name, strEntity, strPlanei, strDir,
            strGlobalI, strP1i, strP2i, strP3i, strP4i
        )
        if not ok:
            raise RuntimeError(f"添加单元面荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_surface_load_vector(
            self,
            strEntity: str,
            strPlanei: str = "1",
            strDir: str = "VECTOR",
            strXi: str = "0",
            strYi: str = "0",
            strZi: str = "-1",
            strP1i: str = "0",
            strP2i: str = "0",
            strP3i: str = "0",
            strP4i: str = "0",
    ) -> LoadCase:
        """添加单元面荷载（方向向量定义）"""
        ok, err = osis_load_surface_load_vector(
            "ESRFC", self.name, strEntity, strPlanei, strDir,
            strXi, strYi, strZi, strP1i, strP2i, strP3i, strP4i
        )
        if not ok:
            raise RuntimeError(
                f"添加单元面荷载（方向向量）到工况 {self.name} 失败: {err}"
            )
        return self.refresh()

    # ── 荷载删除 ──────────────────────────────

    def delete(
            self,
            eType: str,
            entity: int | str | None = None
    ) -> None:
        """删除荷载"""
        t = eType.strip().upper()
        if t == "GRAVITY":
            ok, err = osis_load_del("GRAVITY", self.name, None)
        else:
            if entity is None:
                raise TypeError(
                    f"删除 {eType} 必须指定 entity=...（节点/单元/钢束等编号），禁止省略"
                )
            ok, err = osis_load_del(eType, self.name, entity)
        if not ok:
            raise RuntimeError(f"删除荷载失败: {err}")
        self.refresh()

    # ── 荷载修改 ──────────────────────────────
    def modify(
            self,
            eType: str,
            old_entity: int | str,
            new_entity: int | str,
    ) -> LoadCase:
        """修改工况内荷载的作用对象"""
        ok, err = osis_load_mod(eType, self.name, old_entity, new_entity)
        if not ok:
            raise RuntimeError(f"修改工况 {self.name} 中的荷载失败: {err}")
        return self.refresh()


# ──────────────────────────────────────────────
# Tendon 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class TendonProp:
    """钢束特性对象"""
    name: str
    tension_type: int
    tendon_mat_no: int
    area: float
    code: int
    tendon_d: int
    tendon_num: int
    pipe_d: float
    tension_coeff: float
    relaxation_coeff: float
    tendon_area: float
    related_tendon_shapes: list[str] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict) -> TendonProp:
        return cls(
            name=d.get("name"),
            tension_type=d.get("tensionType"),
            tendon_mat_no=d.get("tendonMatNO"),
            area=d.get("area"),
            code=d.get("code"),
            tendon_d=d.get("tendonD"),
            tendon_num=d.get("tendonNum"),
            pipe_d=d.get("pipeD"),
            tension_coeff=d.get("tensionCoeff"),
            relaxation_coeff=d.get("relaxationCoeff"),
            tendon_area=d.get("tendonArea"),
            related_tendon_shapes=d.get("relatedTendonShapes") or [],
        )

    def __repr__(self) -> str:
        return f"TendonProp(name={self.name!r}, type={self.tension_type})"


@dataclass(frozen=True)
class TendonShape:
    """钢束形状对象"""
    name: str
    tendon_num: int
    tendon_prop: str
    ele_grp: str
    shape_def_type: int
    layout_ref_type: int
    length: float
    related_loads: list[str] = field(default_factory=list)
    master_tendon_shape: str = ""

    @classmethod
    def _from_dict(cls, d: dict) -> TendonShape:
        return cls(
            name=d.get("name"),
            tendon_num=d.get("tendonNum"),
            tendon_prop=d.get("tendonProp"),
            ele_grp=d.get("eleGrp"),
            shape_def_type=d.get("shapeDefType"),
            layout_ref_type=d.get("layoutRefType"),
            length=d.get("length"),
            related_loads=d.get("relatedLoads") or [],
            master_tendon_shape=d.get("masterTendonShape") or "",
        )

    def __repr__(self) -> str:
        return f"TendonShape(name={self.name!r}, prop={self.tendon_prop})"


# ──────────────────────────────────────────────
# Tendon 子管理器
# ──────────────────────────────────────────────


class TendonPropManager:
    """钢束特性管理器"""

    def _load(self) -> list[TendonProp]:
        """从服务端加载所有钢束特性信息"""
        resp = osis_client("GetAllTendonPropInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        props = [
            TendonProp._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return props

    def create_in(
        self,
        name: str,
        n_mat: int,
        e_code: str,
        diameter: float,
        n_num: int,
        d_pipe: float,
        d_friction_coeff: float = 1.0,
        d_deviation_coeff: float = 1.0,
        d_starting_deform: float = 0.0,
        d_end_deform: float = 0.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建体内钢束特性（按规范输入面积）"""
        ok, err = osis_tendon_prop_in_area1(
            name, "IN", n_mat, 1, e_code, diameter, n_num, d_pipe,
            d_friction_coeff, d_deviation_coeff, d_starting_deform,
            d_end_deform, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def create_in_custom(
        self,
        name: str,
        n_mat: int,
        d_val: float,
        d_pipe: float,
        d_friction_coeff: float = 1.0,
        d_deviation_coeff: float = 1.0,
        d_starting_deform: float = 0.0,
        d_end_deform: float = 0.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建体内钢束特性（用户输入面积）"""
        ok, err = osis_tendon_prop_in_area0(
            name, "IN", n_mat, 0, d_val, d_pipe,
            d_friction_coeff, d_deviation_coeff, d_starting_deform,
            d_end_deform, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def create_ex(
        self,
        name: str,
        n_mat: int,
        e_code: str,
        diameter: float,
        n_num: int,
        d_pipe: float,
        d_friction_coeff: float = 1.0,
        d_starting_deform: float = 0.0,
        d_end_deform: float = 0.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建体外钢束特性（按规范输入面积）"""
        ok, err = osis_tendon_prop_ex_area1(
            name, "EX", n_mat, 1, e_code, diameter, n_num, d_pipe,
            d_friction_coeff, d_starting_deform, d_end_deform,
            d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def create_ex_custom(
        self,
        name: str,
        n_mat: int,
        d_val: float,
        d_pipe: float,
        d_friction_coeff: float = 1.0,
        d_starting_deform: float = 0.0,
        d_end_deform: float = 0.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建体外钢束特性（用户输入面积）"""
        ok, err = osis_tendon_prop_ex_area0(
            name, "EX", n_mat, 0, d_val, d_pipe,
            d_friction_coeff, d_starting_deform, d_end_deform,
            d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def create_pre(
        self,
        name: str,
        n_mat: int,
        e_code: str,
        diameter: float,
        n_num: int,
        d_delta_t: float = 10.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建先张法钢束特性（按规范输入面积）"""
        ok, err = osis_tendon_prop_pre_area1(
            name, "PRE", n_mat, 1, e_code, diameter, n_num,
            d_delta_t, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def create_pre_custom(
        self,
        name: str,
        n_mat: int,
        d_val: float,
        d_delta_t: float = 10.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建先张法钢束特性（用户输入面积）"""
        ok, err = osis_tendon_prop_pre_area0(
            name, "PRE", n_mat, 0, d_val,
            d_delta_t, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def delete(self, name: str) -> None:
        """删除钢束特性"""
        ok, err = osis_tendon_prop_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束特性 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        """重命名钢束特性"""
        ok, err = osis_tendon_prop_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束特性 {old_name} -> {new_name} 失败: {err}")

    def get(self, name: str | list[str]) -> TendonProp | list[TendonProp | None] | None:
        """根据名称获取钢束特性"""
        if isinstance(name, str):
            name = [name]
        elif not isinstance(name, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")

        resp = osis_client("GetTendonPropInfoByNames", {"name": name})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")

        props = [TendonProp._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(props) == 0:
            return None
        elif len(props) == 1:
            return props[0]
        return props

    def all(self) -> list[TendonProp]:
        """获取所有钢束特性"""
        return self._load()

    def count(self) -> int:
        """获取钢束特性数量"""
        return len(self._load())

    def __repr__(self) -> str:
        return f"TendonPropManager(count={self.count()})"


class TendonShapeManager:
    """钢束形状管理器"""

    def _load(self) -> list[TendonShape]:
        """从服务端加载所有钢束形状信息"""
        resp = osis_client("GetAllTendonShapeInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        shapes = [
            TendonShape._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return shapes

    def create_spl3d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        curve_name: str,
    ) -> None:
        """定义钢束形状-3D样条"""
        ok, err = osis_tendon_shape_spl3d(name, n_num, prop, element_group, "SPL3D", curve_name)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")

    def create_arc3d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        curve_name: str,
    ) -> None:
        """定义钢束形状-3D圆弧"""
        ok, err = osis_tendon_shape_arc3d(name, n_num, prop, element_group, "ARC3D", curve_name)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")

    def create_arc2d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        e_type: int,
        param: list,
    ) -> None:
        """定义钢束形状-2D圆弧"""
        ok, err = osis_tendon_shape_arc2d(name, n_num, prop, element_group, "ARC2D", e_type, param)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")

    def delete(self, name: str) -> None:
        """删除钢束形状"""
        ok, err = osis_tendon_shape_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束形状 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        """重命名钢束形状"""
        ok, err = osis_tendon_shape_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束形状 {old_name} -> {new_name} 失败: {err}")

    def layout(
        self,
        name: str,
        layout_type: Literal['GLOBAL', "ELEMENT"],
        n_ele: int,
        n_beg: int,
        n_dir: int,
        d_offset_x: float = 0.0,
        d_offset_y: float = 0.0,
        d_offset_z: float = 0.0,
    ) -> None:
        """布置钢束形状"""
        ok, err = osis_layout_tendons(name, layout_type, n_ele, n_beg, n_dir, d_offset_x, d_offset_y, d_offset_z)
        if not ok:
            raise RuntimeError(f"布置钢束 {name} 失败: {err}")

    def wipe(self, name: str) -> None:
        """擦除已布置钢束形状"""
        ok, err = osis_wipe_tendons(name)
        if not ok:
            raise RuntimeError(f"擦除钢束 {name} 失败: {err}")

    def get(self, name: str | list[str]) -> TendonShape | list[TendonShape | None] | None:
        """根据名称获取钢束形状"""
        if isinstance(name, str):
            name = [name]
        elif not isinstance(name, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")

        resp = osis_client("GetTendonShapeInfoByNames", {"name": name})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")

        shapes = [TendonShape._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(shapes) == 0:
            return None
        elif len(shapes) == 1:
            return shapes[0]
        return shapes

    def all(self) -> list[TendonShape]:
        """获取所有钢束形状"""
        return self._load()

    def count(self) -> int:
        """获取钢束形状数量"""
        return len(self._load())

    def __repr__(self) -> str:
        return f"TendonShapeManager(count={self.count()})"


# ──────────────────────────────────────────────
# Tendon 主管理器
# ──────────────────────────────────────────────


class TendonManager:
    """钢束管理器

    统一管理钢束特性和钢束形状。

    子管理器：
    - prop: TendonPropManager - 钢束特性
    - shape: TendonShapeManager - 钢束形状

    用法:
        >>> from pyosis.load import tendon_manager
        >>> # 钢束特性
        >>> tendon_manager.prop.create_in("15-10", mat_no, "GBT5224_2014", 15.2, 10, 0.09)
        >>> # 钢束形状
        >>> tendon_manager.shape.create_arc3d("N1", 2, "15-4", "主梁", "curve1")
        >>> tendon_manager.shape.layout("N1", "ELEMENT", 1, 0, 0)
    """

    def __init__(self) -> None:
        self._prop_manager = TendonPropManager()
        self._shape_manager = TendonShapeManager()

    @property
    def prop(self) -> TendonPropManager:
        """钢束特性管理器"""
        return self._prop_manager

    @property
    def shape(self) -> TendonShapeManager:
        """钢束形状管理器"""
        return self._shape_manager

    def __repr__(self) -> str:
        return f"TendonManager(props={self.prop.count()}, shapes={self.shape.count()})"


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class LoadCaseManager:
    """荷载工况管理器

    统一管理荷载工况的创建、删除、修改和查询。

    用法:
        >>> from pyosis.load import loadcase_manager
        >>> lc = loadcase_manager.create("工况1", "USER")
        >>> lc.name
        >>> all_lcs = loadcase_manager.all()
        >>> loadcase_manager.delete("工况1")
        """

    def __init__(self) -> None:
        pass

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> list[LoadCase]:
        """从服务端加载所有荷载工况信息（无缓存）"""
        resp = osis_client("GetAllLoadCaseInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        loadcases = [
            LoadCase._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]
        return loadcases

    # ── 增删改 ────────────────────────────────

    def create(
            self,
            name: str,
            load_case_type: str = "USER",
            scalar: float = 1.0,
            prompt: str = None,
    ) -> LoadCase:
        """创建荷载工况

        Args:
            name: 荷载工况名称
            load_case_type: 荷载工况类型
                USER = 用户定义的荷载
                D = 桥规中的荷编号1(结构重力)
                DC = 结构和非结构附属荷载
                DW = 铺装和设备荷载
                DD = 桩端摩擦力
                CS = 施工阶段荷载
            scalar: 系数，默认1.0
            prompt: 说明

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_loadcase(name, load_case_type, scalar, prompt)
        if not ok:
            raise RuntimeError(f"创建荷载工况 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除荷载工况

        Args:
            name: 荷载工况名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_loadcase_del(name)
        if not ok:
            raise RuntimeError(f"删除荷载工况 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> LoadCase:
        """重命名荷载工况

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_loadcase_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名荷载工况 {old_name} -> {new_name} 失败: {err}")
        return self.get(new_name)

    # ── 查询 ──────────────────────────────────

    def get(self, name: str | list[str]) -> LoadCase | list[LoadCase | None] | None:
        """根据名称获取单个或多个荷载工况

        Args:
            name: 荷载工况名称

        Returns:
            LoadCase 对象或数组；工况不存在返回 None
        """
        if isinstance(name, str):
            name = [name]
        elif not isinstance(name, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetLoadCaseInfoByNames", {"name": name})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        
        loadcases = [LoadCase._from_dict(d) if d else None for d in resp.get("data", [])]
        
        if len(loadcases) == 0:
            return None
        elif len(loadcases) == 1:
            return loadcases[0]
        return loadcases

    def all(self) -> list[LoadCase]:
        """获取所有荷载工况

        Returns:
            全部荷载工况列表
        """
        return self._load()

    def count(self) -> int:
        """获取荷载工况总数

        Returns:
            工况数量
        """
        return len(self._load())

    def __repr__(self) -> str:
        return f"LoadCaseManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

loadcase_manager = LoadCaseManager()
tendon_manager = TendonManager()
