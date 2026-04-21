"""荷载管理器 - 统一管理荷载工况的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护荷载工况列表，通过 get 等方法查询，不暴露 HTTP 接口细节

支持的荷载类型：
- 荷载工况（USER, D, DC, DW, DD, CS）
- 静力荷载（自重、节点荷载、线荷载、面荷载、强迫位移、初始内力、温度荷载、预应力、索力）
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from ..core.client import osis_client
from .loadcase import (
    osis_loadcase,
    osis_loadcase_del,
    osis_loadcase_mod,
)
from .tendon import (
    osis_tendon_prop_in_area1,
    osis_tendon_prop_ex_area1,
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
    """荷载工况对象（对应某一荷载工况及其下荷载操作）

    由 ``LoadCaseManager``（全局 ``loadcase_manager``）内部创建，用户不应直接实例化。
    """
    # 基本属性
    name: str
    load_case_type: str  # "USER", "D", "DC", "DW", "DD", "CS"
    scalar: float = 1.0
    prompt: str = ""
    
    # ── 荷载数据（从 GetLoadCaseDetail 填充）─────────────────────────────
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
    related_stages: list[str] = field(default_factory=list)  # 关联施工阶段

    def _sync_from_detail(self, detail: dict) -> None:
        """用 GetLoadCaseDetail 返回的 data 同步当前对象（内部使用）。"""
        self.cforce = detail.get("cforce", []) or []
        self.displacement = detail.get("displacement", []) or []
        self.element_surface = detail.get("elementSurface", []) or []
        self.gradient_temp = detail.get("gradientTemp", []) or []
        self.gravity = detail.get("gravity")
        self.initial = detail.get("initial", []) or []
        self.line = detail.get("line", []) or []
        self.name = detail.get("name", "")
        self.nforce = detail.get("nforce", [])
        self.point_force = detail.get("pointForce", []) or []
        self.point_moment = detail.get("pointMoment", []) or []
        self.prestressed = detail.get("prestressed", []) or []
        self.prompt = detail.get("prompt", "")
        self.related_stages = detail.get("relatedStages", [])
        self.scalar = detail.get("scalar", 0.0)
        self.load_case_type = detail.get("type", "USER")
        self.uniform_temp  = detail.get("uniformTemp", [])

    def refresh_detail(self) -> LoadCase:
        """刷新当前工况荷载明细并同步到对象属性。"""
        self._sync_from_detail(self.get())
        return self


    @classmethod
    def _from_dict(cls, d: dict) -> LoadCase:
        """从接口 dict 构造 LoadCase 对象（内部使用）"""
        return cls(
            name=d.get("name", ""),
            load_case_type=d.get("type", "USER"),
            scalar=d.get("scalar", 1.0),
            prompt=d.get("prompt", ""),
        )

    # ── 荷载添加 ──────────────────────────────

    def create_gravity(
            self,
            dXCoeff: float = 1.0,
            dYCoeff: float = 1.0,
            dZCoeff: float = 1.0,
    ) -> LoadCase:
        """添加自重荷载

        Args:
            dXCoeff: 全局坐标系x方向的系数
            dYCoeff: 全局坐标系y方向的系数
            dZCoeff: 全局坐标系z方向的系数

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_gravity("GRAVITY", self.name, dXCoeff, dYCoeff, dZCoeff)
        if not ok:
            raise RuntimeError(f"添加自重荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

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
        """添加节点荷载

        Args:
            nEntity: 节点编号
            dFx: 全局坐标系x方向的集中力
            dFy: 全局坐标系y方向的集中力
            dFz: 全局坐标系z方向的集中力
            dMx: 全局坐标系x方向的集中弯矩
            dMy: 全局坐标系y方向的集中弯矩
            dMz: 全局坐标系z方向的集中弯矩

        Returns:
            当前荷载工况对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_nforce("NFORCE", self.name, nEntity, dFx, dFy, dFz, dMx, dMy, dMz)
        if not ok:
            raise RuntimeError(f"添加节点荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

    def create_line_load(
            self,
            nEntity: int,
            dFXI: float,
            dFYI: float,
            dFZI: float = 0,
            dMXI: float = 0,
            dMYI: float = 0,
            dMZI: float = 0,
            dFXJ: float = None,
            dFYJ: float = None,
            dFZJ: float = 0,
            dMXJ: float = 0,
            dMYJ: float = 0,
            dMZJ: float = 0,
            dOffsetXI: float = 0.0,
            dOffsetYI: float = 0.0,
            dOffsetZI: float = 0.0,
            dOffsetXJ: float = 1.0,  # 默认1.0，与dOffsetXI不同
            dOffsetYJ: float = 0.0,
            dOffsetZJ: float = 0.0,
    ) -> LoadCase:
        """添加线荷载
        ...
        """
        if dFXJ is None:
            dFXJ = dFXI
        if dFYJ is None:
            dFYJ = dFYI
        ok, err = osis_load_line(
            "LINE", self.name, nEntity, 1, 1,
            dOffsetXI, dOffsetYI, dOffsetZI, dFXI, dFYI, dFZI, dMXI, dMYI, dMZI,
            dOffsetXJ, dOffsetYJ, dOffsetZJ, dFXJ, dFYJ, dFZJ, dMXJ, dMYJ, dMZJ,
        )
        if not ok:
            raise RuntimeError(f"添加线荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

    def create_displacement(
            self,
            nEntity: int,
            dDx: float = 0,
            dDy: float = 0,
            dDz: float = 0,
            dRx: float = 0,
            dRy: float = 0,
            dRz: float = 0,
            eps: float = 1e-15,
    ) -> LoadCase:
        ok, err = osis_load_displacement(
            "DISPLACEMENT",
            self.name,
            nEntity,
            1 if abs(dDx) > eps else 0, dDx,
            1 if abs(dDy) > eps else 0, dDy,
            1 if abs(dDz) > eps else 0, dDz,
            1 if abs(dRx) > eps else 0, dRx,
            1 if abs(dRy) > eps else 0, dRy,
            1 if abs(dRz) > eps else 0, dRz,
        )
        if not ok:
            raise RuntimeError(f"添加强迫位移到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

    def create_uniform_temperature(
            self,
            nEntity: int,
            dTemp: float,
            eDirect: str = "X",
    ) -> LoadCase:
        """添加均匀温度荷载

        Args:
            nEntity: 单元编号
            dTemp: 温差值（正为升温）
            eDirect: 作用方向，X=整体升降温，Y/Z=横向梯度温度

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_utemp("UTEMP", self.name, nEntity, eDirect, dTemp)
        if not ok:
            raise RuntimeError(f"添加均匀温度荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

    def create_gradient_temperature(
            self,
            nEntity: int,
            eDirect: str = "Y",
            eGTempType: str = "R",
            nNum: int = 1,
            param: list = ["", 10, 10, 0, 0],
    ) -> LoadCase:
        """添加梯度温度荷载

        Args:
            nEntity: 单元编号
            eDirect: 局部方向
                * Y
                * Z
            eGTempType: 定义梁的参考位置
                * R = 从梁截面建模位置到温度变化点的距离
                * T = 从梁顶到温度变化点的距离
                * C = 从截面中心到温度变化点的距离
                * B = 从梁底到温度变化点的距离
            nNum: 梯度温度荷载段数
            param: 每个梯度温度荷载段对应一组参数 [B, H1, T1, H2, T2]

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_gtemp("GTEMP", self.name, nEntity, eDirect, eGTempType, nNum, param)
        if not ok:
            raise RuntimeError(f"添加梯度温度荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

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
        """添加初始内力荷载

        Args:
            nEntity: 单元编号
            dFXI, dFYI, dFZI: I 端轴力（局部坐标）
            dMXI, dMYI, dMZI: I 端弯矩
            dFXJ, dFYJ, dFZJ: J 端轴力（局部坐标）
            dMXJ, dMYJ, dMZJ: J 端弯矩

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
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
        return self.refresh_detail()

    # def create_initial_force(
    #     self,
    #     nEntity: int,
    #     dFXI: float = 100,
    #     dFYI: float = 100,
    #     dFZI: float = 0,
    #     dMXI: float = 0,
    #     dMYI: float = 0,
    #     dMZI: float = 0,
    # ) -> LoadCaseManager:
    #     """添加初始内力荷载
    #
    #     Args:
    #         nEntity: 单元编号
    #         dFXI, dFYI, dFZI: I端集中力
    #         dMXI, dMYI, dMZI: I端集中弯矩
    #
    #     Raises:
    #         RuntimeError: 添加失败时抛出异常
    #     """
    #     ok, err = osis_load_initial("INITIAL", self.name, nEntity, dFXI, dFYI, dFZI, dMXI, dMYI, dMZI)
    #     if not ok:
    #         raise RuntimeError(f"添加初始内力荷载到工况 {self.name} 失败: {err}")
    #     return self

    def create_prestress(
            self,
            strEntity: str,
            eTensionType: str = "BOTH",
            eTensionForceType: str = "ST",
            dBeg: float = 100,
            dEnd: float = 100,
    ) -> LoadCase:
        """添加预应力荷载

        Args:
            strEntity: 钢束形状名称
            eTensionType: 张拉类型，BOTH/BEG/END
            eTensionForceType: 张拉力类型，ST=应力/IF=内力
            dBeg: 起点应力或内力
            dEnd: 终点应力或内力

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_pst("PST", self.name, strEntity, eTensionType, eTensionForceType, dBeg, dEnd)
        if not ok:
            raise RuntimeError(f"添加预应力荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

    def create_cable_force(
            self,
            nEntity: int,
            eLoadType: str = "IN",
            dForce: float = 100,
    ) -> LoadCase:
        """添加索力荷载

        Args:
            nEntity: 单元编号
            eLoadType: 施加方式，IN=体内力/EX=体外力
            dForce: 索力数值

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_cforce("CFORCE", self.name, nEntity, eLoadType, dForce)
        if not ok:
            raise RuntimeError(f"添加索力荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

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
        """添加单元面荷载

        Args:
            strEntity: 单元编号
            strPlanei: 面位置，板壳单元默认1，实体单元输入1,2,3,4,5,6
            strDir: 方向，默认为 VECTOR
            strGlobalI: 0=局部/1=整体/2=整体+投影
            strP1i~strP4i: 对应角节点荷载值

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_surface_load(
            "ESRFC", self.name, strEntity, strPlanei, strDir,
            strGlobalI, strP1i, strP2i, strP3i, strP4i
        )
        if not ok:
            raise RuntimeError(f"添加单元面荷载到工况 {self.name} 失败: {err}")
        return self.refresh_detail()

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
        """添加单元面荷载（方向向量定义）

        Args:
            strEntity: 单元编号
            strPlanei: 面位置，板壳单元默认1，实体单元输入1,2,3,4,5,6
            strDir: 方向，默认为 VECTOR
            strXi, strYi, strZi: VECTOR的具体值
            strP1i~strP4i: 对应角节点荷载值

        Raises:
            RuntimeError: 添加失败时抛出异常，消息包含服务端返回的具体原因
        """
        ok, err = osis_load_surface_load_vector(
            "ESRFC", self.name, strEntity, strPlanei, strDir,
            strXi, strYi, strZi, strP1i, strP2i, strP3i, strP4i
        )
        if not ok:
            raise RuntimeError(
                f"添加单元面荷载（方向向量）到工况 {self.name} 失败: {err}"
            )
        return self.refresh_detail()

    # ── 荷载删除 ──────────────────────────────

    def delete(
            self,
            eType: str,
            entity: int | str | None = None
    ) -> None:
        """删除荷载
        * ``GRAVITY``：工况级自重，无需也不使用 ``entity``（若传入会被忽略）。
        * 其余类型：必须传入 ``entity=`` 节点/单元/钢束等编号，禁止省略以免误删。
        Args:
            eType: 荷载类型
                GRAVITY, NFORCE, LINE, DISPLACEMENT, INITIAL, UTEMP, GTEMP, PST, CFORCE
            entity: 作用的 节点/单元/钢束形状 编号

        Raises:
            TypeError: 非 GRAVITY 但未提供 entity
            RuntimeError: 删除失败时抛出异常
        """
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
        # 同步：删除成功后刷新当前工况荷载明细，避免实例属性滞后
        self.refresh_detail()

    # ── 荷载修改 ──────────────────────────────
    def modify(
            self,
            eType: str,
            old_entity: int | str,
            new_entity: int | str,
    ) -> LoadCase:
        """修改工况内荷载的作用对象

        Args:
            eType: 荷载类型
                NFORCE, LINE, DISPLACEMENT, INITIAL, UTEMP, GTEMP, PST, CFORCE
            old_entity: 旧节点/单元/钢束形状编号或名称
            new_entity: 新节点/单元/钢束形状编号或名称

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_load_mod(eType, self.name, old_entity, new_entity)
        if not ok:
            raise RuntimeError(f"修改工况 {self.name} 中的荷载失败: {err}")
        # 同步：修改成功后刷新当前工况荷载明细，避免实例属性滞后
        return self.refresh_detail()

    # ── 荷载查询 ──────────────────────────────
    def get(self) -> dict:
        """查询当前工况下的所有荷载数据

        Returns:
            接口返回的该工况荷载数据

        Raises:
            RuntimeError: 接口调用失败时抛出异常
        """
        load_case_name = self.name
        resp = osis_client("GetLoadCaseDetail", {"loadCaseName": load_case_name})
        if isinstance(resp, tuple):
            raise RuntimeError(f"查询工况 {load_case_name} 的荷载失败: {resp[1]}")
        data = resp.get("data", {})
        return data if isinstance(data, dict) else {}


# ──────────────────────────────────────────────
# Tendon 管理器
# ──────────────────────────────────────────────


class TendonManager:
    """钢束管理器

    统一管理钢束特性、钢束形状和钢束布置。
    """

    # ── 钢束特性 ──────────────────────────────

    def create_prop_in(
        self,
        name: str,
        n_mat: int,
        e_code: str,
        diameter: float,
        n_num: int,
        d_delta_t: float,
        d_pipe: float,
        d_friction_coeff: float = 1.0,
        d_deviation_coeff: float = 1.0,
        d_starting_deform: float = 0.0,
        d_end_deform: float = 0.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建体内钢束特性（按规范输入面积）
        
        Args:
            name (str): 钢束特性名称
            n_mat (int): 材料编号
            e_code (str): 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter (float): 公称直径
            n_num (int): 每束钢束根数
            d_delta_t (float): 与台座温差
            d_pipe (float): 管道直径
            d_friction_coeff (float): 摩擦系数
            d_deviation_coeff (float): 偏差系数
            d_starting_deform (float): 起点变形
            d_end_deform (float): 终点变形
            d_tensioning_coeff (float): 张拉系数
            d_relaxation_coeff (float): 松弛系数
        """
        ok, err = osis_tendon_prop_in_area1(
            name, "IN", n_mat, 1, e_code, diameter, n_num,
            d_delta_t, d_pipe, d_friction_coeff, d_deviation_coeff,
            d_starting_deform, d_end_deform, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def create_prop_ex(
        self,
        name: str,
        n_mat: int,
        e_code: str,
        diameter: float,
        n_num: int,
        d_delta_t: float,
        d_pipe: float,
        d_friction_coeff: float = 1.0,
        d_starting_deform: float = 0.0,
        d_end_deform: float = 0.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建体外钢束特性（按规范输入面积）
        
        Args:
            name (str): 钢束特性名称
            n_mat (int): 材料编号
            e_code (str): 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter (float): 公称直径
            n_num (int): 每束钢束根数
            d_delta_t (float): 与台座温差
            d_pipe (float): 管道直径
            d_friction_coeff (float): 摩擦系数
            d_starting_deform (float): 起点变形
            d_end_deform (float): 终点变形
            d_tensioning_coeff (float): 张拉系数
            d_relaxation_coeff (float): 松弛系数
        """
        ok, err = osis_tendon_prop_ex_area1(
            name, "EX", n_mat, 1, e_code, diameter, n_num,
            d_delta_t, d_pipe, d_friction_coeff, d_starting_deform,
            d_end_deform, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def create_prop_pre(
        self,
        name: str,
        n_mat: int,
        e_code: str,
        diameter: float,
        n_num: int,
        d_delta_t: float = 0.0,
        d_pipe: float = 0.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> None:
        """创建先张法钢束特性（按规范输入面积）
        
        Args:
            name (str): 钢束特性名称
            n_mat (int): 材料编号
            e_code (str): 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter (float): 公称直径
            n_num (int): 每束钢束根数
            d_delta_t (float): 与台座温差
            d_pipe (float): 管道直径
            d_tensioning_coeff (float): 张拉系数
            d_relaxation_coeff (float): 松弛系数
        """
        ok, err = osis_tendon_prop_pre_area1(
            name, "PRE", n_mat, 1, e_code, diameter, n_num,
            d_delta_t, d_pipe, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")

    def delete_prop(self, name: str) -> None:
        """删除钢束特性
        
        Args:
            name (str): 钢束特性名称
        """
        ok, err = osis_tendon_prop_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束特性 {name} 失败: {err}")

    def rename_prop(self, old_name: str, new_name: str) -> None:
        """修改钢束特性名称

        Args:
            old_name (str): 旧名称
            new_name (str): 新名称
        """
        ok, err = osis_tendon_prop_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束特性 {old_name} -> {new_name} 失败: {err}")

    # ── 钢束形状 ──────────────────────────────

    def create_shape_spl3d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        curve_name: str,
    ) -> None:
        """定义钢束形状-3D样条

        Args:
            name (str): 名称
            n_num (int): 钢束数量
            prop (str): 钢束特性
            element_group (str): 作用的单元组
            curve_name (str): 样条曲线名称
        """
        ok, err = osis_tendon_shape_spl3d(name, n_num, prop, element_group, "SPL3D", curve_name)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")

    def create_shape_arc3d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        curve_name: str,
    ) -> None:
        """定义钢束形状-3D圆弧

        Args:
            name (str): 名称
            n_num (int): 钢束数量
            prop (str): 钢束特性
            element_group (str): 作用的单元组
            curve_name (str): 样条曲线名称
        """
        ok, err = osis_tendon_shape_arc3d(name, n_num, prop, element_group, "ARC3D", curve_name)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")

    def create_shape_arc2d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        e_type: int,
        param: list,
    ) -> None:
        """定义钢束形状-2D圆弧

        Args:
            name (str): 名称
            n_num (int): 钢束数量
            prop (str): 钢束特性
            element_group (str): 作用的单元组
            e_type (int): 参考类型
                * 0 = 距离
                * 1 = 坐标
            param (list):
                - e_type = 0 时需要填入：
                    竖弯参考位置-梁顶缘线，
                    竖弯样条曲线名称，
                    平弯参考位置-梁中心线，
                    平弯样条曲线名称
                - e_type = 1 时需要填入：
                    竖弯样条曲线名称，
                    平弯样条曲线名称
        """
        ok, err = osis_tendon_shape_arc2d(name, n_num, prop, element_group, "ARC2D", e_type, param)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")

    def delete_shape(self, name: str) -> None:
        """删除钢束形状

        Args:
            name (str): 名称
        """
        ok, err = osis_tendon_shape_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束形状 {name} 失败: {err}")

    def rename_shape(self, old_name: str, new_name: str) -> None:
        """修改钢束形状名称

        Args:
            old_name (str): 钢束形状名称
            new_name (str): 新名称
        """
        ok, err = osis_tendon_shape_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束形状 {old_name} -> {new_name} 失败: {err}")

    # ── 钢束布置 ──────────────────────────────

    def layout(
        self,
        name: str,
        layout_type: str,
        n_ele: int,
        n_beg: int,
        n_dir: int,
        d_offset_x: float = 0.0,
        d_offset_y: float = 0.0,
        d_offset_z: float = 0.0,
    ) -> None:
        """布置钢束形状

        Args:
            name (str): 钢束形状名称
            layout_type (str): 分配钢束形状的方法
                * GLOBAL = 参考整体坐标系原点
                * ELEMENT = 参考单元分配
            n_ele (int): 参考单元编号（ELEMENT模式时）
            n_beg (int): 起点
                * 0 = i
                * 1 = j
            n_dir (int): 方向
                * 0 = i->j
                * 1 = j->i
            d_offset_x (float): x方向起点偏移
            d_offset_y (float): y方向起点偏移
            d_offset_z (float): z方向起点偏移
        """
        ok, err = osis_layout_tendons(name, layout_type, n_ele, n_beg, n_dir, d_offset_x, d_offset_y, d_offset_z)
        if not ok:
            raise RuntimeError(f"布置钢束 {name} 失败: {err}")

    def wipe(self, name: str) -> None:
        """擦除已布置钢束形状
        
        Args:
            name (str): 钢束形状名称
        """
        ok, err = osis_wipe_tendons(name)
        if not ok:
            raise RuntimeError(f"擦除钢束 {name} 失败: {err}")

    def __repr__(self) -> str:
        return "TendonManager()"


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class LoadCaseManager:
    """荷载工况管理器

    统一管理荷载工况和荷载的创建、删除、修改和查询。

    用法:
        >>> from pyosis.load import loadcase_manager
        >>> lc = loadcase_manager.create("工况1", "USER")
        >>> lc.name

        # 添加/删除自重（GRAVITY 不需要 entity=）
        >>> _ = lc.create_gravity(1.0, 1.0, 1.0)
        >>> lc.delete("GRAVITY")
        
        # 重命名/删除工况
        >>> lc2 = loadcase_manager.rename("工况1", "新工况1")
        >>> lc2.name

        >>> loadcase_manager.delete("新工况1")

        """

    def __init__(self) -> None:
        self._loadcases: list[LoadCase] = []
        self._lc_map: dict[str, LoadCase] = {}  # 按名称索引：O(1) 查询
        self._loaded: bool = False
        self._tendon = TendonManager()

    @property
    def tendon(self) -> TendonManager:
        """钢束管理器"""
        return self._tendon

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有荷载工况信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllLoadCaseInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        self._loadcases = [
            LoadCase._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
        ]

        # 构建索引：名称 -> 荷载工况对象 (O(1) 查询)
        self._lc_map = {lc.name: lc for lc in self._loadcases}

        self._loaded = True

    def refresh(self) -> None:
        """强制刷新缓存（模型变更后自动调用，也可手动调用）"""
        self._loadcases = []
        self._lc_map = {}
        self._loaded = False
        self._load()

    # ── 荷载工况管理 ──────────────────────────────

    def create(
            self,
            load_case_type: str = "USER",
            scalar: float = 1.0,
            prompt: str = None,
            name: str = None,
    ) -> LoadCase | None:
        """创建荷载工况

        Args:
            load_case_type: 荷载工况类型
                USER = 用户定义的荷载
                D = 桥规中的荷编号1(结构重力)
                DC = 结构和非结构附属荷载
                DW = 铺装和设备荷载
                DD = 桩端摩擦力
                CS = 施工阶段荷载
            scalar: 系数，默认1.0
            prompt: 说明
            name: 荷载工况名称

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if name is None:
            name = f"LC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_loadcase(name, load_case_type, scalar, prompt)
        if not ok:
            raise RuntimeError(f"创建荷载工况 {name} 失败: {err}")
        self._loaded = False
        self._load()
        return self._lc_map.get(name)

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
        self._loaded = False

    def rename(self, old_name: str, new_name: str) -> LoadCase | None:
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
        self._loaded = False
        self._load()
        return self._lc_map.get(new_name)

    # ── 查询 ──────────────────────────────────

    def get(self, name: str | list[str]) -> list[LoadCase | None] | LoadCase | None:
        """根据名称获取单个或多个荷载工况 (O(k))

        Args:
            name: 荷载工况名称

        Returns:
            LoadCase 对象或数组；工况不存在返回 None
        """
        self._load()
        if isinstance(name, str):
            return self._lc_map.get(name)
        elif isinstance(name, list):
            return [self._lc_map.get(n) for n in name]
        else:
            raise TypeError(f"不支持的名称类型: {type(name)}")

    def all(self) -> list[LoadCase]:
        """获取所有荷载工况

        Returns:
            全部荷载工况列表
        """
        self._load()
        return list(self._loadcases)

    def count(self) -> int:
        """获取荷载工况总数

        Returns:
            工况数量
        """
        self._load()
        return len(self._loadcases)


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

loadcase_manager = LoadCaseManager()
