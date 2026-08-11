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
from typing import Literal, Any
from enum import Enum

from ..core.client import osis_client
from ..core import get_references, raise_if_occupied
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
    osis_bottom_tendons,
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
        '''刷新当前工况荷载明细并同步到对象属性

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 接口调用失败时抛出异常
        '''
        resp = osis_client("GetLoadCaseInfoByNames", {"name": [self.name]})
        if not resp['success']:
            raise RuntimeError(f"刷新工况 {self.name} 失败: {resp['error']}")
        data = resp.get("data", [])
        if data and data[0]:
            self._sync_from_dict(data[0])
        return self

    # ── 荷载添加 ──────────────────────────────

    def create(self, type: str, *args: Any, **kwargs: Any) -> LoadCase | None:
        '''添加荷载（便捷入口，内部转发到对应 create_* 方法）

        type 决定具体荷载类型，对应关系：
            GRAVITY      -> create_gravity
            NFORCE       -> create_nforce
            LINE         -> create_line_load
            DISPLACEMENT -> create_displacement
            INITIAL      -> create_initial_force
            UTEMP        -> create_uniform_temperature
            GTEMP        -> create_gradient_temperature
            PST          -> create_prestress
            CFORCE       -> create_cable_force
            CONCENTRATED -> create_concentrated_force
            SURFACE      -> create_surface_load
            SURFACE_VEC  -> create_surface_load_vector
            PTF/PTM      -> create_concentrated_force (is_moment)

        Args:
            type (str): 荷载类型关键字
            *args: 透传给具体 create_* 方法
            **kwargs: 透传给具体 create_* 方法

        Returns:
            更新后的 LoadCase 对象

        Raises:
            ValueError: 未知的 type
            RuntimeError: 创建失败时抛出异常
        '''
        _creator = {
            "GRAVITY":      self.create_gravity,
            "NFORCE":       self.create_nforce,
            "LINE":         self.create_line_load,
            "DISPLACEMENT": self.create_displacement,
            "INITIAL":      self.create_initial_force,
            "UTEMP":        self.create_uniform_temperature,
            "GTEMP":        self.create_gradient_temperature,
            "PST":          self.create_prestress,
            "CFORCE":       self.create_cable_force,
            "CONCENTRATED": self.create_concentrated_force,
            # "PTF":          self.create_concentrated_force,
            # "PTM":          self.create_concentrated_force,
            "SURFACE":      self.create_surface_load,
            "SURFACE_VEC":  self.create_surface_load_vector,
        }
        type_key = type.strip().upper()

        if type_key in ("PTF", "PTM"):
            elem, e_coord, n_range, *rest = args
            forces = [list(rest[i: i + 6]) for i in range(0, len(rest), 6)]
            return self.create_concentrated_force(elem,e_coord,is_moment=(type_key == "PTM"),forces=forces)
        return _creator[type_key](*args, **kwargs)

    def create_gravity(
            self,
            x_coeff: float = 1.0,
            y_coeff: float = 1.0,
            z_coeff: float = 1.0,
    ) -> LoadCase:
        '''添加自重荷载

        Args:
            x_coeff (float): 全局坐标系x方向的系数，将作用于重力加速度
            y_coeff (float): 全局坐标系y方向的系数，将作用于重力加速度
            z_coeff (float): 全局坐标系z方向的系数，将作用于重力加速度

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_gravity("GRAVITY", self.name, x_coeff, y_coeff, z_coeff)
        if not ok:
            raise RuntimeError(f"添加自重荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_nforce(
            self,
            entity: int,
            fx: float = 100,
            fy: float = 0,
            fz: float = 0,
            mx: float = 0,
            my: float = 0,
            mz: float = 0,
    ) -> LoadCase:
        '''添加节点荷载

        Args:
            entity (int): 节点编号
            fx (float): 全局坐标系x方向的集中力
            fy (float): 全局坐标系y方向的集中力
            fz (float): 全局坐标系z方向的集中力
            mx (float): 全局坐标系x方向的集中弯矩
            my (float): 全局坐标系y方向的集中弯矩
            mz (float): 全局坐标系z方向的集中弯矩

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_nforce("NFORCE", self.name, entity, fx, fy, fz, mx, my, mz)
        if not ok:
            raise RuntimeError(f"添加节点荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_line_load(
            self,
            entity: int,
            coord_system: Literal[0, 1] = 1,
            load_type: Literal[0, 1] = 1,
            offset_x_i: float = 0.0,
            offset_y_i: float = 0.0,
            offset_z_i: float = 0.0,
            fx_i: float = 100,
            fy_i: float = 100,
            fz_i: float = 0,
            mx_i: float = 0,
            my_i: float = 0,
            mz_i: float = 0,
            offset_x_j: float = 0.0,
            offset_y_j: float = 0.0,
            offset_z_j: float = 0.0,
            fx_j: float = 100,
            fy_j: float = 100,
            fz_j: float = 0,
            mx_j: float = 0,
            my_j: float = 0,
            mz_j: float = 0,
    ) -> LoadCase:
        '''添加线荷载

        Args:
            entity (int): 单元编号
            coord_system (int): 坐标系
                * 0 = 单元坐标系
                * 1 = 整体坐标系
            load_type (int): 荷载类型
                * 0 = 连续荷载
                * 1 = 离散荷载
            offset_x_i (float): I端偏移量X/L，输入范围[0,1]
            offset_y_i (float): I端Y轴偏移量
            offset_z_i (float): I端Z轴偏移量
            fx_i (float): I端坐标系x方向的集中力
            fy_i (float): I端坐标系y方向的集中力
            fz_i (float): I端坐标系z方向的集中力
            mx_i (float): I端坐标系x方向的集中弯矩
            my_i (float): I端坐标系y方向的集中弯矩
            mz_i (float): I端坐标系z方向的集中弯矩
            offset_x_j (float): J端偏移量X/L，输入范围[0,1]
            offset_y_j (float): J端Y轴偏移量
            offset_z_j (float): J端Z轴偏移量
            fx_j (float): J端坐标系x方向的集中力
            fy_j (float): J端坐标系y方向的集中力
            fz_j (float): J端坐标系z方向的集中力
            mx_j (float): J端坐标系x方向的集中弯矩
            my_j (float): J端坐标系y方向的集中弯矩
            mz_j (float): J端坐标系z方向的集中弯矩

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_line(
            "LINE", self.name, entity, coord_system, load_type,
            offset_x_i, offset_y_i, offset_z_i, fx_i, fy_i, fz_i, mx_i, my_i, mz_i,
            offset_x_j, offset_y_j, offset_z_j, fx_j, fy_j, fz_j, mx_j, my_j, mz_j,
        )
        if not ok:
            raise RuntimeError(f"添加线荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_concentrated_force(
            self,
            entity: int,
            coord_system: Literal[0, 1] = 1,
            is_moment: bool = False,
            forces: list[list[float]] = None,
    ) -> LoadCase:
        '''添加任意节间集中力/力矩

        Args:
            entity (int): 单元编号
            coord_system (int): 坐标系
                * 0 = 单元坐标系
                * 1 = 整体坐标系
            is_moment (bool): 是否为集中力矩（True=力矩PTM，False=力PTF）
            forces (list): 各组力/力矩参数，按顺序填入：
                [offsetX, offsetY, offsetZ, Px, Py, Pz]
                每组包含6个参数：偏移量X/L, Y轴偏移量, Z轴偏移量, x方向力/力矩, y方向力/力矩, z方向力/力矩
                最多5组，例如：
                [[0.5, 0, 0, 100, 0, 0]]  # 1组力
                [[0.25, 0, 0, 50, 0, 0], [0.75, 0, 0, 50, 0, 0]]  # 2组力

        Returns:
            更新后的 LoadCase 对象

        Raises:
            ValueError: forces 组数不在 1~5 范围内或每组参数数量不为 6
            RuntimeError: 添加失败时抛出异常
        '''
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

        ok, err = osis_load_concentrated(
            "PTM" if is_moment else "PTF", self.name, entity, coord_system, nLoadRange, params
        )
        if not ok:
            force_type = "集中力矩" if is_moment else "集中力"
            raise RuntimeError(f"添加{force_type}到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_displacement(
            self,
            entity: int,
            bx: int = 1,
            dx: float = 0.0,
            by: int = 0,
            dy: float = 0.0,
            bz: int = 0,
            dz: float = 0.0,
            brx: int = 0,
            rx: float = 0.0,
            bry: int = 0,
            ry: float = 0.0,
            brz: int = 0,
            rz: float = 0.0,
    ) -> LoadCase:
        '''添加强迫位移

        Args:
            entity (int): 节点编号
            bx (int): UX方向，0 = 自由，1 = 强迫位移
            dx (float): 强制位移在坐标系x方向的分量
            by (int): UY方向，0 = 自由，1 = 强迫位移
            dy (float): 强制位移在坐标系y方向的分量
            bz (int): UZ方向，0 = 自由，1 = 强迫位移
            dz (float): 强制位移在坐标系z方向的分量
            brx (int): RX方向，0 = 自由，1 = 强迫位移
            rx (float): 绕坐标系x轴的强制旋转角度分量
            bry (int): RY方向，0 = 自由，1 = 强迫位移
            ry (float): 绕坐标系y轴的强制旋转角度分量
            brz (int): RZ方向，0 = 自由，1 = 强迫位移
            rz (float): 绕坐标系z轴的强制旋转角度分量

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_displacement(
            "DISPLACEMENT",self.name,entity,bx,dx,by,dy,bz,dz,brx,rx,bry,ry,brz,rz)
        if not ok:
            raise RuntimeError(f"添加强迫位移到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_uniform_temperature(
            self,
            entity: int,
            direct: Literal["X", "Y", "Z"] = "X",
            temp: float = 1.0,
            length: float = None,
    ) -> LoadCase:
        '''添加均匀温度荷载

        Args:
            entity (int): 单元编号
            direct (str): 作用方向。单元坐标系X（轴向）/Y/Z方向温差，均匀升降温数值（正为升温）
                * X: 可用来模拟整体升降温荷载
                * Y: 可以用来模拟单元的横向梯度温度荷载
                * Z: 可以用来模拟单元的横向梯度温度荷载
            temp (float): 温差值，不影响系统温度
            length (float): Y/Z方向的长度，为 None 则自动通过截面计算

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_utemp("UTEMP", self.name, entity, direct, temp, length)
        if not ok:
            raise RuntimeError(f"添加均匀温度荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_gradient_temperature(
            self,
            entity: int,
            direct: Literal["Y", "Z"] = "Y",
            g_temp_type: Literal["R", "T", "C", "B"] = "R",
            num: int = 1,
            *param: float | str,
    ) -> LoadCase:
        '''添加梯度温度荷载

        Args:
            entity (int): 单元编号
            direct (str): 局部方向
                * Y
                * Z
            g_temp_type (str): 定义梁的参考位置
                * R: 从梁截面建模位置到温度变化点的距离
                * T: 从梁顶到温度变化点的距离
                * C: 从截面中心到温度变化点的距离
                * B: 从梁底到温度变化点的距离
            num (int): 梯度温度荷载段数
            param (float|str): 每个梯度温度荷载段对应一组参数，多组参数直接全部按顺序填入param中即可
                - B (float): 考虑温度变化的宽度，宽度可设置为空("")
                - H1 (float): 参考位置至定义温度间距离
                - T1 (float): H1处对应温度
                - H2 (float): 参考位置至定义温度间距离
                - T2 (float): H2处对应温度

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        if len(param) == 1 and isinstance(param[0], list):
            plist = list(param[0])   # 手写: ..., 2, [1.24, 0.0, ...]
        else:
            plist = list(param)      # .out 平铺: ..., 2, 1.24, 0.0, ...
        ok, err = osis_load_gtemp(
            "GTEMP", self.name, entity, direct, g_temp_type, num, plist
        )
        if not ok:
            raise RuntimeError(f"添加梯度温度荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_initial_force(
            self,
            entity: int,
            fxi: float = 100,
            fyi: float = 100,
            fzi: float = 0,
            mxi: float = 0,
            myi: float = 0,
            mzi: float = 0,
            fxj: float = 0,
            fyj: float = 0,
            fzj: float = 0,
            mxj: float = 0,
            myj: float = 0,
            mzj: float = 0,
    ) -> LoadCase:
        '''添加初始内力荷载

        Args:
            entity (int): 单元编号
            fxi (float): I端局部坐标系x向轴力
            fyi (float): I端局部坐标系y向轴力
            fzi (float): I端局部坐标系z向轴力
            mxi (float): I端绕x弯矩
            myi (float): I端绕y弯矩
            mzi (float): I端绕z弯矩
            fxj (float): J端局部坐标系x向轴力
            fyj (float): J端局部坐标系y向轴力
            fzj (float): J端局部坐标系z向轴力
            mxj (float): J端绕x弯矩
            myj (float): J端绕y弯矩
            mzj (float): J端绕z弯矩

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_initial("INITIAL",self.name,entity,fxi,fyi,fzi,mxi,myi,mzi,fxj,fyj,fzj,mxj,myj,mzj)
        if not ok:
            raise RuntimeError(f"添加初始内力荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_prestress(
            self,
            entity: str,
            tension_type: Literal["BOTH", "BEG", "END"] = "BOTH",
            tension_force_type: Literal["ST", "IF"] = "ST",
            beg: float = 100,
            end: float = 100,
    ) -> LoadCase:
        '''添加预应力荷载

        Args:
            entity (str): 钢束形状名称，由 TdShape 定义
            tension_type (str): 张拉类型
                * BOTH = 两端张拉
                * BEG = 起点张拉
                * END = 终点张拉
            tension_force_type (str): 张拉力类型
                * ST = 应力
                * IF = 内力
            beg (float): 起点应力或内力。tension_type 为 END 时填 None
            end (float): 终点应力或内力。tension_type 为 BEG 时填 None

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_pst("PST", self.name,entity, tension_type, tension_force_type, beg, end)
        if not ok:
            raise RuntimeError(f"添加预应力荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_cable_force(
            self,
            entity: int,
            load_type: Literal["IN", "EX"] = "IN",
            force: float = 100,
    ) -> LoadCase:
        '''添加索力荷载

        Args:
            entity (int): 单元编号
            load_type (str): 施加方式
                * IN = 体内力
                * EX = 体外力
            force (float): 索力数值

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_cforce("CFORCE", self.name, entity, load_type, force)
        if not ok:
            raise RuntimeError(f"添加索力荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_surface_load(
            self,
            entity: str,
            plane: str = "1",
            direction: str = "X",
            coord_type: Literal["0", "1", "2"] = "0",
            p1: str = "0",
            p2: str = "0",
            p3: str = "0",
            p4: str = "0",
    ) -> LoadCase:
        '''添加单元面荷载，不考虑边中节点荷载插值

        Args:
            entity (str): 单元编号
            plane (str): 面位置，板壳单元默认输入1，实体单元输入1,2,3,4,5,6
            direction (str): 方向，X, Y, Z
            coord_type (str): 坐标系
                * 0 = 局部
                * 1 = 整体
                * 2 = 整体 + 投影
            p1 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2
            p2 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2
            p3 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2
            p4 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        ok, err = osis_load_surface_load(
            "ESRFC", self.name, entity, plane, direction,
            coord_type, p1, p2, p3, p4
        )
        if not ok:
            raise RuntimeError(f"添加单元面荷载到工况 {self.name} 失败: {err}")
        return self.refresh()

    def create_surface_load_vector(
            self,
            entity: str,
            plane: str = "1",
            direction: str = "VECTOR",
            vx: str = "0",
            vy: str = "0",
            vz: str = "-1",
            p1: str = "0",
            p2: str = "0",
            p3: str = "0",
            p4: str = "0",
    ) -> LoadCase:
        '''添加单元面荷载（方向向量定义），不考虑边中节点荷载插值

        Args:
            entity (str): 单元编号
            plane (str): 面位置，板壳单元默认输入1，实体单元输入1,2,3,4,5,6
            direction (str): 方向，默认为 VECTOR
            vx (str): VECTOR 的具体值
            vy (str): VECTOR 的具体值
            vz (str): VECTOR 的具体值
            p1 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2
            p2 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2
            p3 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2
            p4 (str): 对应 plane 的角节点荷载值，量纲为 M L^-1 T^-2

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 添加失败时抛出异常
        '''
        # raise Exception("暂不支持添加单元面荷载（方向向量）到工况")
        ok, err = osis_load_surface_load_vector(
            "ESRFC", self.name, entity, plane, direction,
            vx, vy, vz, p1, p2, p3, p4
        )
        if not ok:
            raise RuntimeError(
                f"添加单元面荷载（方向向量）到工况 {self.name} 失败: {err}"
            )
        return self.refresh()

    # ── 荷载删除 ──────────────────────────────

    def delete(
            self,
            load_type: Literal["GRAVITY", "NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"],
            entity: int | str | None = None
    ) -> None:
        '''删除荷载

        Args:
            load_type (str): 荷载类型
                * GRAVITY = 自重荷载
                * NFORCE = 节点荷载
                * LINE = 线荷载
                * DISPLACEMENT = 强迫位移荷载
                * INITIAL = 初始内力荷载
                * UTEMP = 均匀温度荷载
                * GTEMP = 梯度温度荷载
                * PST = 预应力荷载
                * CFORCE = 索力荷载
            entity (int|str): 要删除的荷载所作用的节点/单元/钢束形状编号。load_type 为 GRAVITY 时填 None

        Raises:
            TypeError: 删除非 GRAVITY 荷载时未指定 entity
            RuntimeError: 删除失败时抛出异常
        '''
        t = load_type.strip().upper()
        if t == "GRAVITY":
            ok, err = osis_load_del("GRAVITY", self.name, None)
        else:
            if entity is None:
                raise TypeError(
                    f"删除 {load_type} 必须指定 entity=...（节点/单元/钢束等编号），禁止省略"
                )
            ok, err = osis_load_del(load_type, self.name, entity)
        if not ok:
            raise RuntimeError(f"删除荷载失败: {err}")
        self.refresh()

    # ── 荷载修改 ──────────────────────────────
    def modify(
            self,
            load_type: Literal["NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"],
            old_entity: int | str,
            new_entity: int | str,
    ) -> LoadCase:
        '''修改工况内荷载的作用对象

        Args:
            load_type (str): 荷载类型
                * NFORCE = 节点荷载
                * LINE = 线荷载
                * DISPLACEMENT = 强迫位移荷载
                * INITIAL = 初始内力荷载
                * UTEMP = 均匀温度荷载
                * GTEMP = 梯度温度荷载
                * PST = 预应力荷载
                * CFORCE = 索力荷载
            old_entity (int|str): 旧编号
            new_entity (int|str): 新编号

        Returns:
            更新后的 LoadCase 对象

        Raises:
            RuntimeError: 修改失败时抛出异常
        '''
        ok, err = osis_load_mod(load_type, self.name, old_entity, new_entity)
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
        '''重命名钢束特性

        Args:
            new_name (str): 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        '''
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
        element: int = None,
        begin: Literal[0, 1] = 1,
        direction: Literal[0, 1] = 1,
        offset_x: float = None,
        offset_y: float = None,
        offset_z: float = None,
    ) -> None:
        '''布置钢束形状

        Args:
            layout_type (str): 分配钢束形状的方法
                * GLOBAL = 参考整体坐标系原点
                * ELEMENT = 参考单元分配
            < 下面的参数仅当 layout_type = "ELEMENT" 时要填 >
            element (int): 参考单元编号
            begin (int): 起点
                * 0 = i
                * 1 = j
            direction (int): 方向
                * 0 = i->j
                * 1 = j->i
            offset_x (float): x方向起点偏移
            offset_y (float): y方向起点偏移
            offset_z (float): z方向起点偏移

        Raises:
            RuntimeError: 布置失败时抛出异常
        '''
        ok, err = osis_layout_tendons(self.name, layout_type, element, begin, direction, offset_x, offset_y, offset_z)
        if not ok:
            raise RuntimeError(f"布置钢束 {self.name} 失败: {err}")

    def wipe(self) -> None:
        '''擦除已布置钢束形状

        Raises:
            RuntimeError: 擦除失败时抛出异常
        '''
        ok, err = osis_wipe_tendons(self.name)
        if not ok:
            raise RuntimeError(f"擦除钢束 {self.name} 失败: {err}")

    def bottom(self, bottom_layout: int, *bot: int) -> None:
        '''定义是否沿梁单元底板布置钢束形状

        Args:
            bottom_layout (int): 是否沿底板布置
                * 0 = 不沿底板布置
                * 1 = 沿底板布置
            bot (int): 底板布置钢束对应的样条曲线行号，数量不限
                （如 Bot_i, Bot_j, Bot_k, ...）

        Raises:
            RuntimeError: 设置底板布置失败时抛出异常
        '''
        ok, err = osis_bottom_tendons(self.name, bottom_layout, *bot)
        if not ok:
            raise RuntimeError(f"设置钢束 {self.name} 底板布置失败: {err}")

    def rename(self, new_name: str) -> None:
        '''重命名钢束形状

        Args:
            new_name (str): 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        '''
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

    def get_dependencies(self, name: str) -> dict[str, list]:
        """查询钢束特性被谁引用"""
        return get_references("TendonProp", name=name)

    def create(
        self,
        name: str,
        s_type: str,
        mat: int,
        area: int,
        *args: Any,
        **kwargs: Any,
    ) -> TendonProp:
        """创建钢束特性（便捷入口，内部转发到对应 create_* 方法）

        type 决定张拉方法（IN/EX/PRE），area 决定面积输入方式：
            * 0 = 用户输入面积
            * 1 = 按规范输入面积

        Args:
            name: 钢束特性名称
            s_type: 张拉方法，支持 "IN" / "EX" / "PRE"
            mat: 材料编号
            area: 面积输入方式
                * 0 = 用户输入面积（需传 val）
                * 1 = 按规范输入面积（需传 code/diameter/num）
            *args: 按位置传给对应 create_* 的参数
            **kwargs: 按关键字传给对应 create_* 的参数
                体内/体外钢束（IN/EX）：
                    * area=1: code, diameter, num, pipe, [friction_coeff, ...]
                    * area=0: val, pipe, [friction_coeff, ...]
                先张法钢束（PRE）：
                    * area=1: code, diameter, num, [delta_t, ...]
                    * area=0: val, [delta_t, ...]

        Raises:
            ValueError: 未知的 type 或非法的 area
            RuntimeError: 创建失败

                Examples:
            >>> from pyosis.load import tendon_manager
            >>> mat_no = 1
            >>> # 体内钢束，按规范
            >>> tendon_manager.prop.create("15-10", mat_no, "IN", 1,
            ...     code="GBT5224_2014", diameter=15.2, num=10, pipe=0.09)
            >>> # 体内钢束，用户输入面积
            >>> tendon_manager.prop.create("M1", mat_no, "IN", 0,
            ...     val=0.00014, pipe=0.09)
            >>> # 体外钢束
            >>> tendon_manager.prop.create("EX1", mat_no, "EX", 1,
            ...     code="GBT5224_2014", diameter=15.2, num=7, pipe=0.09)
            >>> # 先张法
            >>> tendon_manager.prop.create("P1", mat_no, "PRE", 1,
            ...     code="GBT5224_2014", diameter=12.7, num=5)
        """
        type_key = s_type.upper()
        if type_key not in ("IN", "EX", "PRE"):
            raise ValueError(
                f"未知张拉方法: {type!r}，支持: IN, EX, PRE"
            )
        if area not in (0, 1):
            raise ValueError(
                f"非法 area: {area!r}，支持: 0=用户输入面积, 1=按规范输入面积"
            )

        _creator = {
            ("IN",  0): self.create_in_custom,
            ("IN",  1): self.create_in,
            ("EX",  0): self.create_ex_custom,
            ("EX",  1): self.create_ex,
            ("PRE", 0): self.create_pre_custom,
            ("PRE", 1): self.create_pre,
        }
        return _creator[(type_key, area)](name, mat, *args, **kwargs)

    def create_in(
        self,
        name: str,
        mat: int,
        code: Literal["GBT5224_2014", "GBT20065_2016"],
        diameter: float,
        num: int,
        pipe: float,
        friction_coeff: float = 1.0,
        deviation_coeff: float = 1.0,
        starting_deform: float = 0.0,
        end_deform: float = 0.0,
        tensioning_coeff: float = 1.0,
        relaxation_coeff: float = 1.0,
    ) -> TendonProp:
        '''创建体内钢束特性（按规范输入面积）

        Args:
            name (str): 钢束特性名称
            mat (int): 材料编号
            code (str): 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter (float): 公称直径
            num (int): 每束钢束根数
            pipe (float): 管道直径
            friction_coeff (float): 摩擦系数
            deviation_coeff (float): 偏差系数
            starting_deform (float): 起点变形
            end_deform (float): 终点变形
            tensioning_coeff (float): 张拉系数
            relaxation_coeff (float): 松弛系数

        Returns:
            创建的 TendonProp 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_tendon_prop_in_area1(
            name, "IN", mat, 1, code, diameter, num, pipe,
            friction_coeff, deviation_coeff, starting_deform,
            end_deform, tensioning_coeff, relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def create_in_custom(
        self,
        name: str,
        mat: int,
        val: float,
        pipe: float,
        friction_coeff: float = 1.0,
        deviation_coeff: float = 1.0,
        starting_deform: float = 0.0,
        end_deform: float = 0.0,
        tensioning_coeff: float = 1.0,
        relaxation_coeff: float = 1.0,
    ) -> TendonProp:
        '''创建体内钢束特性（用户输入面积）

        Args:
            name (str): 钢束特性名称
            mat (int): 材料编号
            val (float): 用户输入的钢束面积
            pipe (float): 管道直径
            friction_coeff (float): 摩擦系数
            deviation_coeff (float): 偏差系数
            starting_deform (float): 起点变形
            end_deform (float): 终点变形
            tensioning_coeff (float): 张拉系数
            relaxation_coeff (float): 松弛系数

        Returns:
            创建的 TendonProp 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_tendon_prop_in_area0(
            name, "IN", mat, 0, val, pipe,
            friction_coeff, deviation_coeff, starting_deform,
            end_deform, tensioning_coeff, relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def create_ex(
        self,
        name: str,
        mat: int,
        code: Literal["GBT5224_2014", "GBT20065_2016"],
        diameter: float,
        num: int,
        pipe: float,
        friction_coeff: float = 1.0,
        starting_deform: float = 0.0,
        end_deform: float = 0.0,
        tensioning_coeff: float = 1.0,
        relaxation_coeff: float = 1.0,
    ) -> TendonProp:
        '''创建体外钢束特性（按规范输入面积）

        Args:
            name (str): 钢束特性名称
            mat (int): 材料编号
            code (str): 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter (float): 公称直径
            num (int): 每束钢束根数
            pipe (float): 管道直径
            friction_coeff (float): 摩擦系数
            starting_deform (float): 起点变形
            end_deform (float): 终点变形
            tensioning_coeff (float): 张拉系数
            relaxation_coeff (float): 松弛系数

        Returns:
            创建的 TendonProp 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_tendon_prop_ex_area1(
            name, "EX", mat, 1, code, diameter, num, pipe,
            friction_coeff, starting_deform, end_deform,
            tensioning_coeff, relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def create_ex_custom(
        self,
        name: str,
        mat: int,
        val: float,
        pipe: float,
        friction_coeff: float = 1.0,
        starting_deform: float = 0.0,
        end_deform: float = 0.0,
        tensioning_coeff: float = 1.0,
        relaxation_coeff: float = 1.0,
    ) -> TendonProp:
        '''创建体外钢束特性（用户输入面积）

        Args:
            name (str): 钢束特性名称
            mat (int): 材料编号
            val (float): 用户输入的钢束面积
            pipe (float): 管道直径
            friction_coeff (float): 摩擦系数
            starting_deform (float): 起点变形
            end_deform (float): 终点变形
            tensioning_coeff (float): 张拉系数
            relaxation_coeff (float): 松弛系数

        Returns:
            创建的 TendonProp 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_tendon_prop_ex_area0(
            name, "EX", mat, 0, val, pipe,
            friction_coeff, starting_deform, end_deform,
            tensioning_coeff, relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def create_pre(
        self,
        name: str,
        mat: int,
        code: Literal["GBT5224_2014", "GBT20065_2016"],
        diameter: float,
        num: int,
        delta_t: float = 10.0,
        pipe: float = 0.0,  # .out 第 9 字段，PRE 不使用
        tensioning_coeff: float = 1.0,
        relaxation_coeff: float = 1.0,
    ) -> TendonProp:
        '''创建先张法钢束特性（按规范输入面积）

        Args:
            name (str): 钢束特性名称
            mat (int): 材料编号
            code (str): 规范名
                * GBT5224_2014
                * GBT20065_2016
            diameter (float): 公称直径
            num (int): 每束钢束根数
            delta_t (float): 与台座温差
            pipe (float): 管道直径，PRE 不使用，仅为占位
            tensioning_coeff (float): 张拉系数
            relaxation_coeff (float): 松弛系数

        Returns:
            创建的 TendonProp 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_tendon_prop_pre_area1(
            name, "PRE", mat, 1, code, diameter, num,
            delta_t, tensioning_coeff, relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def create_pre_custom(
        self,
        name: str,
        mat: int,
        val: float,
        delta_t: float = 10.0,
        pipe: float = 0.0,  # .out 占位，PRE 不使用，不调入底层
        tensioning_coeff: float = 1.0,
        relaxation_coeff: float = 1.0,
    ) -> TendonProp:
        '''创建先张法钢束特性（用户输入面积）

        Args:
            name (str): 钢束特性名称
            mat (int): 材料编号
            val (float): 用户输入的钢束面积
            delta_t (float): 与台座温差
            pipe (float): 管道直径，PRE 不使用，仅为占位
            tensioning_coeff (float): 张拉系数
            relaxation_coeff (float): 松弛系数

        Returns:
            创建的 TendonProp 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_tendon_prop_pre_area0(
            name, "PRE", mat, 0, val,
            delta_t, tensioning_coeff, relaxation_coeff,
        )
        if not ok:
            raise RuntimeError(f"创建钢束特性 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        '''删除钢束特性

        Args:
            name (str): 钢束特性名称

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(name)
        raise_if_occupied("TendonProp", deps, name=name)
        ok, err = osis_tendon_prop_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束特性 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        '''重命名钢束特性

        Args:
            old_name (str): 旧名称
            new_name (str): 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        '''
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

    def clear(self)->None:
        """清空所有钢束特性"""
        try:
            [self.delete(tp.name) for tp in self.all()]
        except Exception as e:
            raise Exception(f"清空所有钢束特性失败: {e}，被占用,无法删除")

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

    def get_dependencies(self, name: str) -> dict[str, list]:
        """查询钢束形状被谁引用"""
        return get_references("TendonShape", name=name)

    def create(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        layout_type: str,
        *args: Any,
        **kwargs: Any,
    ) -> TendonShape:
        """创建钢束形状（便捷入口，内部转发到对应 create_* 方法）

        Args:
            name: 钢束形状名称
            type: 形状定义类型，支持：
                * "SPL3D" = 3D 样条（需传 curve_name）
                * "ARC3D" = 3D 圆弧（需传 curve_name）
                * "ARC2D" = 2D 圆弧（需传 e_type, param）
            n_num: 钢束数量
            prop: 钢束特性名称
            element_group: 作用的单元组
            *args: 按位置传给对应 create_* 的参数
                - SPL3D / ARC3D：下一个位置参数为 curve_name
                - ARC2D：下一组位置参数为 e_type, param
            **kwargs: 按关键字传给对应 create_* 的参数

        Note:
            SPL3D/ARC3D 与 ARC2D 后续参数差异大，强烈建议用 **kwargs
            关键字传参，避免位置参数顺序混淆。

        Raises:
            ValueError: 未知的 type
            RuntimeError: 创建失败

        Examples:
            >>> from pyosis.load import tendon_manager
            >>> # 3D 样条
            >>> tendon_manager.shape.create("N1", 2, "SPL3D", "15-4", "主梁单元",curve_name="curve1")
            >>> # 3D 圆弧
            >>> tendon_manager.shape.create("N2", 2, "ARC3D", "15-4", "主梁单元",curve_name="curve1")
            >>> # 2D 圆弧（距离参考）
            >>> tendon_manager.shape.create("N3", 2, "ARC2D", "15-4", "主梁单元",e_type=0, param=[0, "sv", 0, "pl"])
        """
        _creator = {
            "SPL3D": self.create_spl3d,
            "ARC3D": self.create_arc3d,
            "ARC2D": self.create_arc2d,
        }
        type_key = layout_type.upper()
        if type_key not in _creator:
            raise ValueError(
                f"未知钢束形状类型: {type!r}，支持: {', '.join(_creator)}"
            )
        return _creator[type_key](name, n_num, prop, element_group, *args, **kwargs)

    def create_spl3d(
        self,
        name: str,
        n_num: int,
        prop: str,
        element_group: str,
        curve_name: str,
    ) -> TendonShape:
        '''定义钢束形状-3D样条

        Args:
            name (str): 名称
            n_num (int): 钢束数量
            prop (str): 钢束特性
            element_group (str): 作用的单元组
            curve_name (str): 样条曲线名称

        Returns:
            创建的 TendonShape 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
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
        '''定义钢束形状-3D圆弧

        Args:
            name (str): 名称
            n_num (int): 钢束数量
            prop (str): 钢束特性
            element_group (str): 作用的单元组
            curve_name (str): 样条曲线名称

        Returns:
            创建的 TendonShape 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
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
        e_type: Literal[0, 1],
        *param: str | int | float,
    ) -> TendonShape:
        '''定义钢束形状-2D圆弧

        Args:
            name (str): 名称
            n_num (int): 钢束数量
            prop (str): 钢束特性
            element_group (str): 作用的单元组
            e_type (int): 参考类型
                * 0 = 距离
                * 1 = 坐标
            param (list): 参数列表
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

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        if len(param) == 1 and isinstance(param[0], list):
            plist = list(param[0])  # 兼容手写: create_arc2d(..., 1, [a, b])
        else:
            plist = list(param)  # .out 平铺: ..., 1, a, b
        ok, err = osis_tendon_shape_arc2d(
            name, n_num, prop, element_group, "ARC2D", e_type, plist
        )
        if not ok:
            raise RuntimeError(f"创建钢束形状 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        '''删除钢束形状

        Args:
            name (str): 钢束形状名称

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(name)
        raise_if_occupied("TendonShape", deps, name=name)
        ok, err = osis_tendon_shape_del(name)
        if not ok:
            raise RuntimeError(f"删除钢束形状 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> None:
        '''重命名钢束形状

        Args:
            old_name (str): 旧名称
            new_name (str): 新名称

        Raises:
            RuntimeError: 重命名失败时抛出异常
        '''
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

    def clear(self)->None:
        """清空所有钢束形状"""
        try:
            [self.delete(ts.name) for ts in self.all()]
        except Exception as e:
            raise Exception(f"清空所有钢束形状失败: {e}，被占用,无法删除")

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
        >>> mat_no = 1
        >>> # 钢束特性（需先存在对应材料）
        >>> tendon_prop = tendon_manager.prop.create_in("15-10", mat=mat_no, code="GBT5224_2014",diameter=15.2, num=10, pipe=0.09)
        >>> tendon_shape = tendon_manager.shape.create_arc3d("N1", 2, "15-4", "主梁单元", "curve1")
        >>> tendon_shape.layout("ELEMENT", 1, 0, 0, 0.0, 0.0, 0.0)
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
        """统计钢束特性和钢束形状的数量

        Returns:
            dict: 包含 props 和 shapes 计数的字典
        """
        return {
            "props": self.prop.count(),
            "shapes": self.shape.count()
        }

    def clear(self) -> None:
        """清空所有钢束形状和钢束特性（先清空形状，再清空特性）"""
        self.shape.clear()
        self.prop.clear()

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

    def get_dependencies(self, name: str) -> dict[str, list]:
        """查询荷载工况被谁引用"""
        return get_references("LoadCase", name=name)

    # ── 增删改 ────────────────────────────────

    def create(
            self,
            name: str,
            load_case_type: Literal["USER", "CS", "D", "PS", "EV", "EH", "SH", "CR", "B", "STL", "L", "IF", "CF", "LS", "BRK", "CRL", "FL", "W1", "W2", "SF", "IP", "WF1", "WF2", "T", "TG", "FR", "CFS", "CFD", "CFV", "E"] = "USER",
            scalar: float = 1.0,
            prompt: str | None = None,
    ) -> LoadCase:
        '''创建荷载工况

        Args:
            name (str): 荷载工况名称
            load_case_type (str): 荷载工况类型
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
            scalar (float): 系数，默认1.0
            prompt (str): 说明，默认 None

        Returns:
            创建的 LoadCase 对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        '''
        ok, err = osis_loadcase(name, load_case_type, scalar, prompt)
        if not ok:
            raise RuntimeError(f"创建荷载工况 {name} 失败: {err}")
        return self.get(name)

    def delete(self, name: str) -> None:
        '''删除荷载工况

        Args:
            name (str): 荷载工况名称

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(name)
        raise_if_occupied("LoadCase", deps, name=name)
        ok, err = osis_loadcase_del(name)
        if not ok:
            raise RuntimeError(f"删除荷载工况 {name} 失败: {err}")

    def rename(self, old_name: str, new_name: str) -> LoadCase:
        '''重命名荷载工况

        Args:
            old_name (str): 旧名称
            new_name (str): 新名称

        Returns:
            重命名后的 LoadCase 对象

        Raises:
            RuntimeError: 重命名失败时抛出异常
        '''
        ok, err = osis_loadcase_mod(old_name, new_name)
        if not ok:
            raise RuntimeError(f"重命名荷载工况 {old_name} -> {new_name} 失败: {err}")
        return self.get(new_name)

    # ── 查询 ──────────────────────────────────

    def get(self, name: str | list[str]) -> LoadCase | list[LoadCase | None] | None:
        '''根据名称获取单个或多个荷载工况

        Args:
            name (str|list): 荷载工况名称，支持单个名称或名称列表

        Returns:
            LoadCase 对象或数组；工况不存在返回 None

        Raises:
            TypeError: 名称类型不支持时抛出
            RuntimeError: 接口调用失败时抛出
        '''

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

    def clear(self)->None:
        """清空所有荷载工况"""
        try:
            [self.delete(lc.name) for lc in self.all()]
        except Exception as e:
            raise Exception(f"清空所有荷载工况失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return f"LoadCaseManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

loadcase_manager = LoadCaseManager()
tendon_manager = TendonManager()
