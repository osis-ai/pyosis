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
from enum import Enum

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
    osis_load_concentrated,
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

    属性:
        name: 荷载工况名称
        load_case_type: 荷载工况类型
            USER = 用户定义的荷载
            D = 桥规中的荷编号1(结构重力)
            DC = 结构和非结构附属荷载
            DW = 铺装和设备荷载
            DD = 桩端摩擦力
            CS = 施工阶段荷载
        scalar: 系数
        prompt: 说明
        related_stages: 关联的施工阶段编号列表
        gravity: 自重荷载数据
        nforce: 节点力荷载列表
        point_force: 节点荷载列表
        point_moment: 节点弯矩列表
        line: 线荷载列表
        element_surface: 面荷载列表
        displacement: 强迫位移列表
        initial: 初始内力列表
        uniform_temp: 均匀温度荷载列表
        gradient_temp: 梯度温度荷载列表
        prestressed: 预应力荷载列表
        cforce: 索力荷载列表
    """
    name: str                                          # 荷载工况名称
    load_case_type: str                                # 荷载工况类型
    scalar: float                                      # 系数
    prompt: str                                        # 说明
    related_stages: list[int] = field(default_factory=list)  # 关联的施工阶段编号列表
    
    # 荷载数据
    gravity: dict | None = None                        # 自重荷载
    nforce: list[dict] = field(default_factory=list)   # 节点力
    point_force: list[dict] = field(default_factory=list)    # 节点荷载
    point_moment: list[dict] = field(default_factory=list)   # 节点弯矩
    line: list[dict] = field(default_factory=list)     # 线荷载
    element_surface: list[dict] = field(default_factory=list)  # 面荷载
    displacement: list[dict] = field(default_factory=list)   # 强迫位移
    initial: list[dict] = field(default_factory=list)  # 初始内力
    uniform_temp: list[dict] = field(default_factory=list)   # 均匀温度
    gradient_temp: list[dict] = field(default_factory=list)  # 梯度温度
    prestressed: list[dict] = field(default_factory=list)    # 预应力
    cforce: list[dict] = field(default_factory=list)   # 索力

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

    # ── 荷载添加 ──────────────────────────────

    def create_gravity(
            self,
            dXCoeff: float = 1.0,
            dYCoeff: float = 1.0,
            dZCoeff: float = 1.0,
    ) -> LoadCase:
        """添加自重荷载

        Args:
            dXCoeff: 全局坐标系x方向的系数，将作用于重力加速度
            dYCoeff: 全局坐标系y方向的系数，将作用于重力加速度
            dZCoeff: 全局坐标系z方向的系数，将作用于重力加速度

        Returns:
            更新后的 LoadCase 对象
        """
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
            更新后的 LoadCase 对象
        """
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
        """添加线荷载

        Args:
            nEntity: 单元编号
            eCoordSystem: 坐标系
                * 0 = 单元坐标系
                * 1 = 整体坐标系
            eLoadType: 荷载类型
                * 0 = 连续荷载
                * 1 = 离散荷载
            dOffsetXI: I端偏移量X/L，输入范围[0,1]
            dOffsetYI: I端Y轴偏移量
            dOffsetZI: I端Z轴偏移量
            dFXI: I端坐标系x方向的集中力
            dFYI: I端坐标系y方向的集中力
            dFZI: I端坐标系z方向的集中力
            dMXI: I端坐标系x方向的集中弯矩
            dMYI: I端坐标系y方向的集中弯矩
            dMZI: I端坐标系z方向的集中弯矩
            dOffsetXJ: J端偏移量X/L，输入范围[0,1]
            dOffsetYJ: J端Y轴偏移量
            dOffsetZJ: J端Z轴偏移量
            dFXJ: J端坐标系x方向的集中力
            dFYJ: J端坐标系y方向的集中力
            dFZJ: J端坐标系z方向的集中力
            dMXJ: J端坐标系x方向的集中弯矩
            dMYJ: J端坐标系y方向的集中弯矩
            dMZJ: J端坐标系z方向的集中弯矩

        Returns:
            更新后的 LoadCase 对象
        """
        ok, err = osis_load_line(
            "LINE", self.name, nEntity, eCoordSystem, eLoadType,
            dOffsetXI, dOffsetYI, dOffsetZI, dFXI, dFYI, dFZI, dMXI, dMYI, dMZI,
            dOffsetXJ, dOffsetYJ, dOffsetZJ, dFXJ, dFYJ, dFZJ, dMXJ, dMYJ, dMZJ,
        )
        if not ok:
            raise RuntimeError(f"添加线荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_concentrated_force(
            self,
            nEntity: int,
            eCoordSystem: Literal[0, 1] = 1,
            is_moment: bool = False,
            forces: list[list[float]] = None,
    ) -> LoadCase:
        """添加任意节间集中力/力矩

        Args:
            nEntity: 单元编号
            eCoordSystem: 坐标系
                * 0 = 单元坐标系
                * 1 = 整体坐标系
            is_moment: 是否为集中力矩（True=力矩PTM，False=力PTF）
            forces: 各组力/力矩参数列表，每组为 [offsetX, offsetY, offsetZ, Px, Py, Pz]
                最多5组，例如：
                [[0.5, 0, 0, 100, 0, 0]]  # 1组力
                [[0.25, 0, 0, 50, 0, 0], [0.75, 0, 0, 50, 0, 0]]  # 2组力

        Returns:
            更新后的 LoadCase 对象
        """
        if forces is None:
            forces = []
        
        nLoadRange = len(forces)
        if nLoadRange < 1 or nLoadRange > 5:
            raise ValueError(f"forces 组数必须在 1~5 之间，当前为 {nLoadRange}")
        
        # 展平参数列表
        params = []
        for force in forces:
            if len(force) != 6:
                raise ValueError(f"每组力/力矩必须包含6个参数 [offsetX, offsetY, offsetZ, Px, Py, Pz]，当前为 {len(force)}")
            params.extend(force)
        
        eType = "PTM" if is_moment else "PTF"
        ok, err = osis_load_concentrated(
            eType, self.name, nEntity, eCoordSystem, nLoadRange, params
        )
        if not ok:
            force_type = "集中力矩" if is_moment else "集中力"
            raise RuntimeError(f"添加{force_type}到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_displacement(
            self,
            nEntity: int,
            bX: int = 1,
            Dx: float = 0.0,
            bY: int = 0,
            Dy: float = 0.0,
            bZ: int = 0,
            Dz: float = 0.0,
            bRx: int = 0,
            Rx: float = 0.0,
            bRy: int = 0,
            Ry: float = 0.0,
            bRz: int = 0,
            Rz: float = 0.0,
    ) -> LoadCase:
        """添加强迫位移

        Args:
            nEntity：节点编号
            bX：UX方向，0 = 自由，1 = 强迫位移
            Dx：强制位移在坐标系x方向的分量
            bY：UY方向，0 = 自由，1 = 强迫位移
            Dy：强制位移在坐标系y方向的分量
            bZ：UZ方向，0 = 自由，1 = 强迫位移
            Dz：强制位移在坐标系z方向的分量
            bRx：RX方向，0 = 自由，1 = 强迫位移
            Rx：绕坐标系x轴的强制旋转角度分量
            bRy：RY方向，0 = 自由，1 = 强迫位移
            Ry：绕坐标系y轴的强制旋转角度分量
            bRz：RZ方向，0 = 自由，1 = 强迫位移
            Rz：绕坐标系z轴的强制旋转角度分量

        Returns:
            更新后的 LoadCase 对象
        """
        ok, err = osis_load_displacement(
            "DISPLACEMENT",self.name,nEntity,bX,Dx,bY,Dy,bZ,Dz,bRx,Rx,bRy,Ry,bRz,Rz)
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
        """添加均匀温度荷载

        Args:
            nEntity: 单元编号
            eDirect: 作用方向
                * X: 可用来模拟整体升降温荷载
                * Y: 可以用来模拟单元的横向梯度温度荷载
                * Z: 可以用来模拟单元的横向梯度温度荷载
            dTemp: 温差值，不影响系统温度
            dLength: Y/Z方向的长度，为None则自动通过截面计算

        Returns:
            更新后的 LoadCase 对象
        """
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
        """添加梯度温度荷载

        Args:
            nEntity: 单元编号
            eDirect: 局部方向
                * Y
                * Z
            eGTempType: 定义梁的参考位置
                * R
                * T
                * C
                * B
            nNum: 梯度温度荷载段数
            param: 每个梯度温度荷载段对应一组参数，多组参数直接全部按顺序填入param中即可
                - B (float): 考虑温度变化的宽度，宽度可设置为空("")
                - H1 (float): 参考位置至定义温度间距离
                - T1 (float): H1处对应温度
                - H2 (float): 参考位置至定义温度间距离
                - T2 (float): H2处对应温度

        Returns:
            更新后的 LoadCase 对象
        """
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
        """添加初始内力荷载

        Args:
            nEntity: 单元编号
            dFXI, dFYI, dFZI: I端局部坐标系x/y/z向轴力
            dMXI, dMYI, dMZI: I端绕x/y/z弯矩
            dFXJ, dFYJ, dFZJ: J端局部坐标系x/y/z向轴力
            dMXJ, dMYJ, dMZJ: J端绕x/y/z弯矩

        Returns:
            更新后的 LoadCase 对象
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
        return self.refresh()

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
            strEntity: 钢束形状名称，由TdShape定义
            eTensionType: 张拉类型
                * BOTH = 两端张拉
                * BEG = 起点张拉
                * END = 终点张拉
            eTensionForceType: 张拉力类型
                * ST = 应力
                * IF = 内力
            dBeg: 起点应力或内力。eTensionType为END时填None
            dEnd: 终点应力或内力。eTensionType为BEG时填None

        Returns:
            更新后的 LoadCase 对象
        """
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
        """添加索力荷载

        Args:
            nEntity: 单元编号
            eLoadType: 施加方式
                * IN = 体内力
                * EX = 体外力
            dForce: 索力数值

        Returns:
            更新后的 LoadCase 对象
        """
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
        """添加单元面荷载，不考虑边中节点荷载插值

        Args:
            strEntity: 单元编号
            strPlanei: 面位置，板壳单元默认输入1，实体单元输入1,2,3,4,5,6
            strDir: 方向，默认为X
            strGlobalI: 坐标系
                * 0 = 局部
                * 1 = 整体
                * 2 = 整体 + 投影
            strP1i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
            strP2i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
            strP3i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
            strP4i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2

        Returns:
            更新后的 LoadCase 对象
        """
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
        """添加单元面荷载（方向向量定义），不考虑边中节点荷载插值

        Args:
            strEntity: 单元编号
            strPlanei: 面位置，板壳单元默认输入1，实体单元输入1,2,3,4,5,6
            strDir: 方向，默认为VECTOR
            strXi: VECTOR的具体值
            strYi: VECTOR的具体值
            strZi: VECTOR的具体值
            strP1i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
            strP2i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
            strP3i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
            strP4i: 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2

        Returns:
            更新后的 LoadCase 对象
        """
        # raise Exception("暂不支持添加单元面荷载（方向向量）到工况")
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
        """删除荷载

        Args:
            eType: 荷载类型
                * GRAVITY = 自重荷载
                * NFORCE = 节点荷载
                * LINE = 线荷载
                * DISPLACEMENT = 强迫位移荷载
                * INITIAL = 初始内力荷载
                * UTEMP = 均匀温度荷载
                * GTEMP = 梯度温度荷载
                * PST = 预应力荷载
                * CFORCE = 索力荷载
            entity: 要删除的荷载所作用的节点/单元/钢束形状编号。eType为GRAVITY时填None

        Raises:
            TypeError: 删除非GRAVITY荷载时未指定entity
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
        self.refresh()

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
                * NFORCE = 节点荷载
                * LINE = 线荷载
                * DISPLACEMENT = 强迫位移荷载
                * INITIAL = 初始内力荷载
                * UTEMP = 均匀温度荷载
                * GTEMP = 梯度温度荷载
                * PST = 预应力荷载
                * CFORCE = 索力荷载
            old_entity: 旧编号
            new_entity: 新编号

        Returns:
            更新后的 LoadCase 对象
        """
        ok, err = osis_load_mod(eType, self.name, old_entity, new_entity)
        if not ok:
            raise RuntimeError(f"修改工况 {self.name} 中的荷载失败: {err}")
        return self.refresh()
    
    def __repr__(self) -> str:
        return f"LoadCase(name={self.name!r}, type={self.load_case_type}, scalar={self.scalar}, prompt={self.prompt})"


# ──────────────────────────────────────────────
# Tendon 数据类
# ──────────────────────────────────────────────

class TensionType(Enum):
    Unassigned = 0
    Pre = 1             # 先张法
    In = 2              # 后张法（体内）
    Ex = 3              # 后张法（体外）


@dataclass(frozen=False)
class TendonProp:
    """钢束特性对象

    对应接口 GetAllTendonPropInfo / GetTendonPropInfoByNames 返回的数据。
    """
    name: str                          # 钢束特性名称
    tension_type: TensionType          # 张拉类型：1=先张法, 2=后张法体内, 3=后张法体外
    tendon_mat_no: int                 # 钢束材料编号
    area: float                        # 钢束面积
    code: int                          # 规范代码
    tendon_d: int                      # 公称直径
    tendon_num: int                    # 每束钢束根数
    pipe_d: float                      # 管道直径
    tension_coeff: float               # 张拉系数
    relaxation_coeff: float            # 松弛系数
    tendon_area: float                 # 单根钢束面积
    related_tendon_shapes: list[str] = field(default_factory=list)  # 关联的钢束形状名称列表

    @classmethod
    def _from_dict(cls, d: dict) -> TendonProp:
        """从接口 dict 构造 TendonProp 对象（内部使用）"""
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
            related_tendon_shapes=d.get("relatedTendonShapes"),
        )

    def rename(self, new_name: str) -> None:
        """重命名钢束特性

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_tendon_prop_mod(self.name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束特性 {self.name} -> {new_name} 失败: {err}")
        self.name = new_name

    def __repr__(self) -> str:
        return f"TendonProp(name={self.name!r}, type={self.tension_type.name}, tendon_mat_no={self.tendon_mat_no}, area={self.area}, code={self.code})"
    
    


@dataclass(frozen=False)
class TendonShape:
    """钢束形状对象

    对应接口 GetAllTendonShapeInfo / GetTendonShapeInfoByNames 返回的数据。
    """
    name: str                          # 钢束形状名称
    tendon_num: int                    # 钢束数量
    tendon_prop: str                   # 钢束特性名称
    ele_grp: str                       # 作用的单元组名称
    shape_def_type: int                # 形状定义类型
    layout_ref_type: int               # 布置参考类型
    length: float                      # 钢束长度
    related_loads: list[str] = field(default_factory=list)  # 关联的荷载工况名称列表
    master_tendon_shape: str = ""      # 主钢束形状名称

    @classmethod
    def _from_dict(cls, d: dict) -> TendonShape:
        """从接口 dict 构造 TendonShape 对象（内部使用）"""
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

    def layout(
        self,
        layout_type: Literal['GLOBAL', "ELEMENT"],
        n_ele: int = None,
        n_beg: int = None,
        n_dir: int = None,
        d_offset_x: float = None,
        d_offset_y: float = None,
        d_offset_z: float = None,
    ) -> None:
        """布置钢束形状"""
        ok, err = osis_layout_tendons(self.name, layout_type, n_ele, n_beg, n_dir, d_offset_x, d_offset_y, d_offset_z)
        if not ok:
            raise RuntimeError(f"布置钢束 {self.name} 失败: {err}")

    def wipe(self) -> None:
        """擦除已布置钢束形状"""
        ok, err = osis_wipe_tendons(self.name)
        if not ok:
            raise RuntimeError(f"擦除钢束 {self.name} 失败: {err}")

    def rename(self, new_name: str) -> None:
        """重命名钢束形状

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_tendon_shape_mod(self.name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束形状 {self.name} -> {new_name} 失败: {err}")
        self.name = new_name

    def __repr__(self) -> str:
        return f"TendonShape(name={self.name!r}, tendon_num={self.tendon_num}, prop={self.tendon_prop}, ele_grp={self.ele_grp})"


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
    ) -> TendonProp:
        """创建体内钢束特性（按规范输入面积）

        Args:
            name: 钢束特性名称
            n_mat: 材料编号
            e_code: 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter: 公称直径
            n_num: 每束钢束根数
            d_pipe: 管道直径
            d_friction_coeff: 摩擦系数
            d_deviation_coeff: 偏差系数
            d_starting_deform: 起点变形
            d_end_deform: 终点变形
            d_tensioning_coeff: 张拉系数
            d_relaxation_coeff: 松弛系数

        Returns:
            创建的 TendonProp 对象
        """
        ok, err = osis_tendon_prop_in_area1(
            name, "IN", n_mat, 1, e_code, diameter, n_num, d_pipe,
            d_friction_coeff, d_deviation_coeff, d_starting_deform,
            d_end_deform, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

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
    ) -> TendonProp:
        """创建体内钢束特性（用户输入面积）

        Args:
            name: 钢束特性名称
            n_mat: 材料编号
            d_val: 用户输入的钢束面积
            d_pipe: 管道直径
            d_friction_coeff: 摩擦系数
            d_deviation_coeff: 偏差系数
            d_starting_deform: 起点变形
            d_end_deform: 终点变形
            d_tensioning_coeff: 张拉系数
            d_relaxation_coeff: 松弛系数

        Returns:
            创建的 TendonProp 对象
        """
        ok, err = osis_tendon_prop_in_area0(
            name, "IN", n_mat, 0, d_val, d_pipe,
            d_friction_coeff, d_deviation_coeff, d_starting_deform,
            d_end_deform, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

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
    ) -> TendonProp:
        """创建体外钢束特性（按规范输入面积）

        Args:
            name: 钢束特性名称
            n_mat: 材料编号
            e_code: 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter: 公称直径
            n_num: 每束钢束根数
            d_pipe: 管道直径
            d_friction_coeff: 摩擦系数
            d_starting_deform: 起点变形
            d_end_deform: 终点变形
            d_tensioning_coeff: 张拉系数
            d_relaxation_coeff: 松弛系数

        Returns:
            创建的 TendonProp 对象
        """
        ok, err = osis_tendon_prop_ex_area1(
            name, "EX", n_mat, 1, e_code, diameter, n_num, d_pipe,
            d_friction_coeff, d_starting_deform, d_end_deform,
            d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

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
    ) -> TendonProp:
        """创建体外钢束特性（用户输入面积）

        Args:
            name: 钢束特性名称
            n_mat: 材料编号
            d_val: 用户输入的钢束面积
            d_pipe: 管道直径
            d_friction_coeff: 摩擦系数
            d_starting_deform: 起点变形
            d_end_deform: 终点变形
            d_tensioning_coeff: 张拉系数
            d_relaxation_coeff: 松弛系数

        Returns:
            创建的 TendonProp 对象
        """
        ok, err = osis_tendon_prop_ex_area0(
            name, "EX", n_mat, 0, d_val, d_pipe,
            d_friction_coeff, d_starting_deform, d_end_deform,
            d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

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
    ) -> TendonProp:
        """创建先张法钢束特性（按规范输入面积）

        Args:
            name: 钢束特性名称
            n_mat: 材料编号
            e_code: 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter: 公称直径
            n_num: 每束钢束根数
            d_delta_t: 与台座温差
            d_tensioning_coeff: 张拉系数
            d_relaxation_coeff: 松弛系数

        Returns:
            创建的 TendonProp 对象
        """
        ok, err = osis_tendon_prop_pre_area1(
            name, "PRE", n_mat, 1, e_code, diameter, n_num,
            d_delta_t, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def create_pre_custom(
        self,
        name: str,
        n_mat: int,
        d_val: float,
        d_delta_t: float = 10.0,
        d_tensioning_coeff: float = 1.0,
        d_relaxation_coeff: float = 1.0,
    ) -> TendonProp:
        """创建先张法钢束特性（用户输入面积）

        Args:
            name: 钢束特性名称
            n_mat: 材料编号
            d_val: 用户输入的钢束面积
            d_delta_t: 与台座温差
            d_tensioning_coeff: 张拉系数
            d_relaxation_coeff: 松弛系数

        Returns:
            创建的 TendonProp 对象
        """
        ok, err = osis_tendon_prop_pre_area0(
            name, "PRE", n_mat, 0, d_val,
            d_delta_t, d_tensioning_coeff, d_relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除钢束特性

        Args:
            name: 钢束特性名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_tendon_prop_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束特性 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        """重命名钢束特性

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_tendon_prop_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束特性 {old_name} -> {new_name} 失败: {err}")

    def get(self, name: str | list[str]) -> TendonProp | list[TendonProp | None] | None:
        """根据名称获取钢束特性

        Args:
            name: 钢束特性名称，支持单个名称或名称列表

        Returns:
            单个 TendonProp 对象；如果传入列表则返回对象列表；
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

        resp = osis_client("GetTendonPropInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")

        props = [TendonProp._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(props) == 0:
            return None
        elif len(props) == 1:
            return props[0]
        return props

    def all(self) -> list[TendonProp]:
        """获取所有钢束特性

        Returns:
            全部 TendonProp 对象列表
        """
        return self._load()

    def count(self) -> int:
        """获取钢束特性数量

        Returns:
            钢束特性数量
        """
        return len(self._load())

    def __repr__(self) -> str:
        return f"TendonPropManager(count={self.count()})"


class TendonShapeManager:
    """钢束形状管理器

    统一管理钢束形状的创建、删除、修改和查询。
    """

    def _load(self) -> list[TendonShape]:
        """从服务端加载所有钢束形状信息（内部使用）

        Returns:
            TendonShape 对象列表
        """
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
    ) -> TendonShape:
        """定义钢束形状-3D样条

        Args:
            name: 名称
            n_num: 钢束数量
            prop: 钢束特性
            element_group: 作用的单元组
            curve_name: 样条曲线名称

        Returns:
            创建的 TendonShape 对象
        """
        ok, err = osis_tendon_shape_spl3d(name, n_num, prop, element_group, "SPL3D", curve_name)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")
        return self.get(name)

    def create_arc3d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        curve_name: str,
    ) -> TendonShape:
        """定义钢束形状-3D圆弧

        Args:
            name: 名称
            n_num: 钢束数量
            prop: 钢束特性
            element_group: 作用的单元组
            curve_name: 样条曲线名称

        Returns:
            创建的 TendonShape 对象
        """
        ok, err = osis_tendon_shape_arc3d(name, n_num, prop, element_group, "ARC3D", curve_name)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")
        return self.get(name)

    def create_arc2d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        e_type: int,
        param: list,
    ) -> TendonShape:
        """定义钢束形状-2D圆弧

        Args:
            name: 名称
            n_num: 钢束数量
            prop: 钢束特性
            element_group: 作用的单元组
            e_type: 参考类型
                * 0 = 距离
                * 1 = 坐标
            param: 参数列表
                - e_type = 0 时需要填入：
                    竖弯参考位置-梁顶缘线，
                    竖弯样条曲线名称，
                    平弯参考位置-梁中心线，
                    平弯样条曲线名称
                - e_type = 1 时需要填入：
                    竖弯样条曲线名称，
                    平弯样条曲线名称

        Returns:
            创建的 TendonShape 对象
        """
        ok, err = osis_tendon_shape_arc2d(name, n_num, prop, element_group, "ARC2D", e_type, param)
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        """删除钢束形状

        Args:
            name: 钢束形状名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_tendon_shape_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束形状 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        """重命名钢束形状

        Args:
            old_name: 旧名称
            new_name: 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        """
        ok, err = osis_tendon_shape_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名钢束形状 {old_name} -> {new_name} 失败: {err}")

    def get(self, name: str | list[str]) -> TendonShape | list[TendonShape | None] | None:
        """根据名称获取钢束形状

        Args:
            name: 钢束形状名称，支持单个名称或名称列表

        Returns:
            单个 TendonShape 对象；如果传入列表则返回对象列表；
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

        resp = osis_client("GetTendonShapeInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")

        shapes = [TendonShape._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(shapes) == 0:
            return None
        elif len(shapes) == 1:
            return shapes[0]
        return shapes

    def all(self) -> list[TendonShape]:
        """获取所有钢束形状

        Returns:
            全部 TendonShape 对象列表
        """
        return self._load()

    def count(self) -> int:
        """获取钢束形状数量

        Returns:
            钢束形状数量
        """
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
        >>> prop = tendon_manager.prop.create_in("15-10", mat_no, "GBT5224_2014", 15.2, 10, 0.09)
        >>> # 钢束形状
        >>> shape = tendon_manager.shape.create_arc3d("N1", 2, "15-4", "主梁", "curve1")
        >>> shape.layout("ELEMENT", 1, 0, 0)
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

    def count(self):
        return {
            "props": self.prop.count(),
            "shapes": self.shape.count()
        }

    def __repr__(self) -> str:
        return f"TendonManager()"


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
            prompt: str | None = None,
    ) -> LoadCase:
        """创建荷载工况

        Args:
            name: 荷载工况名称
            load_case_type: 荷载工况类型
                USER = 用户定义的荷载
                CS = 施工阶段荷载
                D = 结构重力
                PS = 预加力
                EV = 土的重量
                EH = 土侧压力
                SH = 收缩
                CR = 徐变
                B = 水浮力
                STL = 基础变位
                L = 汽车荷载
                IF = 汽车冲击力
                CF = 汽车离心率
                LS = 汽车引起的土侧压力
                BRK = 汽车制动力
                CRL = 人群荷载
                FL = 疲劳荷载
                W1 = 活载风
                W2 = 极限风
                SF = 流水压力
                IP = 冰压力
                WF1 = W1引起的波浪力
                WF2 = W2引起的波浪力
                T = 均匀温度
                TG = 梯度温度
                FR = 支座摩阻力
                CFS = 船舶的撞击作用
                CFD = 漂流物的撞击作用
                CFV = 汽车撞击作用
                E = 地震作用
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

        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        
        resp = osis_client("GetLoadCaseInfoByNames", {"name": names})
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
