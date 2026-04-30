"""材料管理器 - 统一管理材料的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护材料列表，通过 get 等方法查询，不暴露 HTTP 接口细节

支持的材料类型：CONC（混凝土）、STEEL（钢材）、PRESTRESSED（预应力）、REBAR（钢筋）、CUSTOM（自定义）
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from enum import Enum
from ..core.client import osis_client
from .interface import (
    osis_material_conc,
    osis_material_steel,
    osis_material_prestressed,
    osis_material_rebar,
    osis_material_custom,
    osis_material_del,
    osis_material_mod,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────

class MaterialType(Enum):
    UNASSIGNED = 0      # 未定义
    CONC = 1            # 混凝土
    STEEL = 2           # 钢材
    Prestressed = 3     # 预应力
    Rebar = 4           # 钢筋
    Custom = 5          # 自定义

@dataclass(frozen=True)
class Material:
    """材料对象

    由 MaterialManager 内部创建，用户不应直接实例化。
    """

    no: int
    name: str
    material_type: MaterialType # "CONC", "STEEL", "PRESTRESSED", "REBAR", "CUSTOM"
    code: str                   # 规范名
    grade: str                  # 材料等级
    e: float                    # 弹性模量(Pa)
    g: float                    # 剪切模量(Pa)
    mu: float                   # 泊松比
    exp_coeff: float            # 线膨胀系数(1 / ℃)
    unit_weight: float          # 容重(N / m ^ 3)
    density: float              # 质量密度(kg / m ^ 3)
    damping: float              # 阻尼比
    creep_shrink_no: int        # 收缩徐变编号

    @classmethod
    def _from_dict(cls, d: dict) -> Material:
        """从接口 dict 构造 Material 对象（内部使用）"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            material_type=d.get("materialType"),
            code=d.get("code"),
            grade=d.get("grade"),
            e=d.get("e"),
            g=d.get("g"),
            mu=d.get("mu"),
            exp_coeff=d.get("expCoeff"),
            unit_weight=d.get("unitWeight"),
            density=d.get("density"),
            damping=d.get("damping"),

            # 临时使用
            creep_shrink_no=d.get("creepShrinkNo"),
        )

    def __repr__(self) -> str:
        return f"Material(no={self.no}, name={self.name!r}, type={self.material_type.name})"

# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class MaterialManager:
    """材料管理器

    统一管理材料的创建、删除、修改和查询。

    用法:
        >>> from pyosis.material import material_manager
        >>> mat = material_manager.create_conc("C30混凝土", eCode="JTG3362_2018", eGrade="C30")  # 创建混凝土（自动编号）
        >>> mat.no                                                               # 访问编号
        >>> all_mats = material_manager.all()                                      # 获取全部材料
        >>> material_manager.delete(mat.no)                                        # 删除材料
        >>> material_manager.renumber(mat.no, 100)                                 # 修改编号
    """

    def __init__(self) -> None:
        ...

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> list[Material]:
        """从服务端加载所有材料信息"""
        resp = osis_client("GetAllMaterialInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        materials = [
            Material._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "no" in d
        ]

        return materials

    def _next_no(self) -> int:
        """生成下一个可用材料编号

        取已有材料编号的最大值+1，如果没有材料则从1开始。
        """
        materials = self._load()
        mat_no = [mat.no for mat in materials]
        if len(mat_no) == 0:
            return 1
        return max(mat_no) + 1

    # ── 增删改 ────────────────────────────────

    def create_conc(
        self,
        name: str,
        eCode: Literal["JTG3362_2018", "JTGD62_2004"],
        eGrade: Literal["C15", "C20", "C25", "C30", "C35", "C40", "C45", "C50", "C55", "C60", "C65", "C70", "C75", "C80"],
        nCrepShrk: int | None = None,
        dDmp: float = 0.0,
        no: int | None = None,
    ) -> Material:
        """创建混凝土材料

        Args:
            name: 材料名称
            eCode: 材料标准代码，可选值：
                - JTG3362_2018
                - JTGD62_2004
            eGrade: 材料等级牌号，可选值：
                C15, C20, C25, C30, C35, C40, C45, C50, C55, C60, C65, C70, C75, C80
            no: 材料编号，不指定时自动生成（取最大编号+1）
            nCrepShrk: 收缩徐变特性编号，可缺省
            dDmp: 材料阻尼比

        Returns:
            创建的材料对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_material_conc(no, name, "CONC", eCode, eGrade, nCrepShrk, dDmp)
        if not ok:
            raise RuntimeError(f"创建混凝土材料 {no} 失败: {err}")
        return self.get(no)

    def create_steel(
        self,
        name: str,
        eCode: Literal["JTGD64_2015"],
        eGrade: Literal["Q235", "Q345", "Q390", "Q420"],
        dDmp: float = 0.0,
        no: int | None = None,
    ) -> Material:
        """创建钢材

        Args:
            name: 材料名称
            eCode: 材料标准代码，可选值：
                - JTGD64_2015
            eGrade: 材料等级牌号，可选值：
                Q235, Q345, Q390, Q420
            no: 材料编号，不指定时自动生成（取最大编号+1）
            dDmp: 材料阻尼比

        Returns:
            创建的材料对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_material_steel(no, name, "STEEL", eCode, eGrade, dDmp)
        if not ok:
            raise RuntimeError(f"创建钢材 {no} 失败: {err}")
        return self.get(no)

    def create_prestressed(
        self,
        name: str,
        eCode: Literal["JTG3362_2018", "JTGD62_2004"],
        eGrade: str,
        dDmp: float = 0.0,
        no: int | None = None,
    ) -> Material:
        """创建预应力材料

        Args:
            name: 材料名称
            eCode: 材料标准代码，可选值：
                - JTG3362_2018
                - JTGD62_2004
            eGrade: 材料等级牌号，根据材料标准可选：
                - JTG3362_2018: Strand1720, Strand1860, Strand1960, Wire1470, Wire1570,
                  Wire1770, Wire1860, Rebar785, Rebar930, Rebar1080
                - JTGD62_2004: Strand1860, Wire1670, Wire1770, Rebar785, Rebar930
            no: 材料编号，不指定时自动生成（取最大编号+1）
            dDmp: 材料阻尼比

        Returns:
            创建的材料对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_material_prestressed(no, name, "PRESTRESSED", eCode, eGrade, dDmp)
        if not ok:
            raise RuntimeError(f"创建预应力材料 {no} 失败: {err}")
        return self.get(no)

    def create_rebar(
        self,
        name: str,
        eCode: Literal["JTG3362_2018", "JTGD62_2004"],
        eGrade: Literal["HPB300", "HRB400", "HRBF400", "RRB400", "HRB500"] | Literal["R235", "HRB335", "HRB400", "KL400"],
        dDmp: float = 0.0,
        no: int | None = None,
    ) -> Material:
        """创建钢筋材料

        Args:
            name: 材料名称
            eCode: 材料标准代码，可选值：
                - JTG3362_2018
                - JTGD62_2004
            eGrade: 材料等级牌号，根据材料标准可选：
                - JTG3362_2018: HPB300, HRB400, HRBF400, RRB400, HRB500
                - JTGD62_2004: R235, HRB335, HRB400, KL400
            no: 材料编号，不指定时自动生成（取最大编号+1）
            dDmp: 材料阻尼比

        Returns:
            创建的材料对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_material_rebar(no, name, "REBAR", eCode, eGrade, dDmp)
        if not ok:
            raise RuntimeError(f"创建钢筋材料 {no} 失败: {err}")
        return self.get(no)

    def create_custom(
        self,
        name: str,
        no: int | None = None,
        dE: float = 0,
        dG: float = 0,
        dMu: float = 0,
        dExpCoeff: float = 0,
        dUnitWeight: float = 0,
        dDensity: float = 0,
        dDmp: float = 0,
    ) -> Material:
        """创建自定义材料

        Args:
            name: 材料名称
            no: 材料编号，不指定时自动生成（取最大编号+1）
            dE: 弹性模量(Pa)
            dG: 剪切模量(Pa)
            dMu: 泊松比
            dExpCoeff: 线膨胀系数(1/摄氏度)
            dUnitWeight: 容重(N/m^3)
            dDensity: 质量密度(kg/m^3)
            dDmp: 材料阻尼比

        Returns:
            创建的材料对象

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_material_custom(
            no, name, "CUSTOM", dE, dG, dMu, dExpCoeff, dUnitWeight, dDensity, dDmp
        )
        if not ok:
            raise RuntimeError(f"创建自定义材料 {no} 失败: {err}")
        return self.get(no)

    def delete(self, no: int) -> None:
        """删除材料

        Args:
            no: 材料编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_material_del(no)
        if not ok:
            raise RuntimeError(f"删除材料 {no} 失败: {err}")

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改材料编号

        Args:
            old_no: 旧编号
            new_no: 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_material_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改材料编号 {old_no} -> {new_no} 失败: {err}")
        return self.get(new_no)

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int], expected_cls: type[Material]=Material) -> Material | list[Material | None]:     # todo: rewrite
        """根据编号获取单个或多个材料 (O(k))

        Args:
            no: 材料编号

        Returns:
            Material 对象或数组；材料不存在返回 None
        """
        if isinstance(no, int):
            no = [no]
        elif isinstance(no, list):
            ...
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")
        resp = osis_client("GetMaterialInfoByNos", {"no": no})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        mats = [expected_cls._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(mats) == 0:     # 有问题
            return None
        elif len(mats) == 1:   # 只查了一个
            return mats[0]
        return mats

    def all(self) -> list[Material]:
        """获取所有材料

        Returns:
            全部材料列表
        """
        materials = self._load()
        return materials

    def count(self) -> int:
        """获取材料总数

        Returns:
            材料数量
        """
        materials = self._load()
        return len(materials)

    def __repr__(self) -> str:
        return f"MaterialManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

material_manager = MaterialManager()
