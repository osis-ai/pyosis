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

from dataclasses import dataclass

from ..core.client import osis_client
from .loadcase import (
    osis_loadcase,
    osis_loadcase_del,
    osis_loadcase_mod,
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


@dataclass(frozen=True)
class LoadCaseManager:
    """荷载工况对象（对应某一荷载工况及其下荷载操作面）

    由 LoadManager 内部创建，用户不应直接实例化。
    """

    name: str
    load_case_type: str  # "USER", "D", "DC", "DW", "DD", "CS"
    scalar: float = 1.0
    prompt: str = ""

    @classmethod
    def _from_dict(cls, d: dict) -> LoadCaseManager:
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
    ) -> LoadCaseManager:
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
        return self

    def create_nforce(
        self,
        nEntity: int,
        dFx: float = 100,
        dFy: float = 0,
        dFz: float = 0,
        dMx: float = 0,
        dMy: float = 0,
        dMz: float = 0,
    ) -> None:
        """添加节点荷载

        Args:
            nEntity: 节点编号
            dFx: 全局坐标系x方向的集中力
            dFy: 全局坐标系y方向的集中力
            dFz: 全局坐标系z方向的集中力
            dMx: 全局坐标系x方向的集中弯矩
            dMy: 全局坐标系y方向的集中弯矩
            dMz: 全局坐标系z方向的集中弯矩

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_nforce("NFORCE", self.name, nEntity, dFx, dFy, dFz, dMx, dMy, dMz)
        if not ok:
            raise RuntimeError(f"添加节点荷载到工况 {self.name} 失败: {err}")
        
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
    ) -> LoadCaseManager:
        """添加线荷载

        Args:
            nEntity: 单元编号
            dFXI, dFYI, dFZI: I端集中力
            dMXI, dMYI, dMZI: I端集中弯矩
            dFXJ, dFYJ, dFZJ: J端集中力（可缺省，等同于I端）
            dMXJ, dMYJ, dMZJ: J端集中弯矩（可缺省，等同于I端）

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        if dFXJ is None:
            dFXJ = dFXI
        if dFYJ is None:
            dFYJ = dFYI
        ok, err = osis_load_line(
            "LINE", self.name, nEntity, 1, 1,
            0, 0, 0, dFXI, dFYI, dFZI, dMXI, dMYI, dMZI,
            0, 0, 0, dFXJ, dFYJ, dFZJ, dMXJ, dMYJ, dMZJ,
        )
        if not ok:
            raise RuntimeError(f"添加线荷载到工况 {self.name} 失败: {err}")
        return self
    def create_displacement(
        self,
        nEntity: int,
        dDx: float = 0,
        dDy: float = 0,
        dDz: float = 0,
        dRx: float = 0,
        dRy: float = 0,
        dRz: float = 0,
    ) -> None:
        """添加强迫位移

        Args:
            nEntity: 节点编号
            dDx, dDy, dDz: 强制位移在坐标系各方向的分量
            dRx, dRy, dRz: 绕坐标系各轴的强制旋转角度分量

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_load_displacement("DISPLACEMENT", self.name, nEntity, dDx, dDy, dDz, dRx, dRy, dRz)
        if not ok:
            raise RuntimeError(f"添加强迫位移到工况 {self.name} 失败: {err}")
        return self
    def create_temperature_uniform(
        self,
        nEntity: int,
        dTemp: float,
        eDirect: str = "X",
    ) -> LoadCaseManager:
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
        return self
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
        
    # ── 荷载修改 ──────────────────────────────
    def modify(
        self,
        eType: str,
        old_entity: int | str,
        new_entity: int | str,
    ) -> LoadCaseManager:
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
        return self
    # ── 荷载查询 ──────────────────────────────
    def get(self) -> dict:
        """查询当前工况下的所有荷载数据

        Returns:
            接口返回的该工况荷载数据

        Raises:
            RuntimeError: 接口调用失败时抛出异常
        """
        resp = osis_client("GetAllLoadCaseInfo", {"loadCase": self.name})
        if isinstance(resp, tuple):
            raise RuntimeError(f"查询工况 {self.name} 的荷载失败: {resp[1]}")
        data = resp.get("data", {})
        return data if isinstance(data, dict) else {}

# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class LoadManager:
    """荷载工况管理器

    统一管理荷载工况和荷载的创建、删除、修改和查询。

    用法:
        >>> from pyosis.load import load_manager
        >>> load_manager.create_loadcase("工况1", "USER")                        # 创建荷载工况
        >>> load_manager.add_gravity("工况1", 1.0, 1.0, 1.0)                   # 添加自重荷载
        >>> load_manager.add_nforce("工况1", 1, 100, 0, 0, 0, 0, 0)            # 添加节点荷载
        >>> lc = load_manager.get("工况1")                                     # 按名称查询
        >>> all_lcs = load_manager.all()                                       # 获取全部工况
        >>> load_manager.rename("工况1", "新工况1")                            # 重命名工况
        >>> load_manager.delete_loadcase("新工况1")                             # 删除荷载工况
    """
    #     lc = load_manager.create("工况1", "USER")
    #   if lc:
    #       lc.create_nforce(1, 100, 0, 0, 0, 0, 0)
    #       lc.delete(eType="NFORCE", entity=1)
    #       lc.delete(eType="GRAVITY")
    #   lc2 = load_manager.rename("工况1", "新工况1")
    #   load_manager.delete("新工况1")
    def __init__(self) -> None:
        self._loadcases: list[LoadCaseManager] = []
        self._lc_map: dict[str, LoadCaseManager] = {}  # 按名称索引：O(1) 查询
        self._loaded: bool = False

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有荷载工况信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllLoadCaseInfo", {})
        if isinstance(resp, tuple):
            raise RuntimeError(f"加载荷载工况信息失败: {resp[1]}")
        self._loadcases = [
            LoadCaseManager._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "name" in d
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
        name: str,
        load_case_type: str = "USER",
        scalar: float = 1.0,
        prompt: str = None,
    ) -> LoadCaseManager | None:
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
        # if prompt is None:
        #     prompt = ""
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

    def rename(self, old_name: str, new_name: str)  -> LoadCaseManager | None:
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

    def get(self, name: str | list[str]) -> LoadCaseManager | list[LoadCaseManager | None]:
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

    def all(self) -> list[LoadCaseManager]:
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

    def __repr__(self) -> str:
        self._load()
        return f"LoadManager(count={len(self._loadcases)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

load_manager = LoadManager()
