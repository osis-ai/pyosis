"""截面管理器 - 统一管理截面的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 按截面类型分化数据结构，子类包含 type 特有的 definition
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
import shutil
import uuid

from ..core.client import osis_client
from ..common import get_project_directory

from .common import (
    osis_section_Lshape,
    osis_section_circle,
    osis_section_Tshape,
    osis_section_Ishape,
    osis_section_smallbox,
    osis_section_rect,
    osis_section_hollowslab,
    osis_section_rounded_end,
    osis_section_conventionalbox,
    osis_section_flat_box,
    osis_section_double_side_box,
    osis_section_ribbed_slab,
    osis_section_TGirder,
    osis_section_custom,
)
from .steel import (
    osis_section_steel_i,
    osis_section_steel_box,
    osis_section_steel_box_three_cell,
    osis_section_steel_box_itf,
    osis_section_steel_canti_box,
    osis_section_steel_canti_box_ibf,
    osis_section_steel_custom,
    osis_section_steel_custom_plate,
)
from .param import (
    osis_section_offset,
    osis_section_mesh,
    osis_section_del,
    osis_section_mod,
    osis_export_section_pic,
)

@dataclass(frozen=True)
class SectionBBox:
    """截面外包框"""

    min_x: float = 0.0
    min_y: float = 0.0
    max_x: float = 0.0
    max_y: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "SectionBBox | None":
        if not isinstance(d, dict):
            return None
        return cls(
            min_x=d.get("minX", 0.0),
            min_y=d.get("minY", 0.0),
            max_x=d.get("maxX", 0.0),
            max_y=d.get("maxY", 0.0),
        )


@dataclass(frozen=True)
class SectionOffset:
    """截面偏移"""

    type_y: int = 0
    type_z: int = 0
    value_y: float = 0.0
    value_z: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "SectionOffset | None":
        if not isinstance(d, dict):
            return None
        return cls(
            type_y=d.get("typeY", 0),
            type_z=d.get("typeZ", 0),
            value_y=d.get("valueY", 0.0),
            value_z=d.get("valueZ", 0.0),
        )


@dataclass(frozen=True)
class SectionProp:
    """截面几何性质"""

    area: float = 0.0
    cent_y: float = 0.0
    cent_z: float = 0.0
    dy: float = 0.0
    dz: float = 0.0
    iww: float = 0.0
    ixx: float = 0.0
    iyy: float = 0.0
    izz: float = 0.0
    peri_i: float = 0.0
    peri_o: float = 0.0
    sy: float = 0.0
    sz: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "SectionProp | None":
        if not isinstance(d, dict):
            return None
        return cls(
            area=d.get("area", 0.0),
            cent_y=d.get("centY", 0.0),
            cent_z=d.get("centZ", 0.0),
            dy=d.get("dy", 0.0),
            dz=d.get("dz", 0.0),
            iww=d.get("iww", 0.0),
            ixx=d.get("ixx", 0.0),
            iyy=d.get("iyy", 0.0),
            izz=d.get("izz", 0.0),
            peri_i=d.get("periI", 0.0),
            peri_o=d.get("periO", 0.0),
            sy=d.get("sy", 0.0),
            sz=d.get("sz", 0.0),
        )


@dataclass(frozen=True)
class SectionPropFactor:
    """截面性质放大系数"""

    area_factor: float = 1.0
    ixx_factor: float = 1.0
    iyy_factor: float = 1.0
    izz_factor: float = 1.0
    sy_factor: float = 1.0
    sz_factor: float = 1.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "SectionPropFactor | None":
        if not isinstance(d, dict):
            return None
        return cls(
            area_factor=d.get("areaFactor", 1.0),
            ixx_factor=d.get("ixxFactor", 1.0),
            iyy_factor=d.get("iyyFactor", 1.0),
            izz_factor=d.get("izzFactor", 1.0),
            sy_factor=d.get("syFactor", 1.0),
            sz_factor=d.get("szFactor", 1.0),
        )


@dataclass(frozen=True)
class SectionStressPoint:
    """截面应力点"""

    x: float = 0.0
    y: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "SectionStressPoint | None":
        if not isinstance(d, dict):
            return None
        return cls(
            x=d.get("x", 0.0),
            y=d.get("y", 0.0),
        )


# ──────────────────────────────────────────────
# Definition 子类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class BoxDefinition:
    """箱梁定义（type=10）"""

    cell_num: int = 0
    cell1_width: float = 0.0
    cell2_width: float = 0.0
    cell3_width: float = 0.0
    cell4_width: float = 0.0
    tt1: float = 0.0
    tt2: float = 0.0
    tt3: float = 0.0
    tt5: float = 0.0
    tt6: float = 0.0
    xi1: float = 0.0
    xi2: float = 0.0
    xi3: float = 0.0
    xi4: float = 0.0
    xi5: float = 0.0
    xi6: float = 0.0
    xi7: float = 0.0
    yi4: float = 0.0
    yi7: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "BoxDefinition | None":
        if not isinstance(d, dict):
            return None
        return cls(
            cell_num=d.get("CellNum", 0),
            cell1_width=d.get("Cell1Width", 0.0),
            cell2_width=d.get("Cell2Width", 0.0),
            cell3_width=d.get("Cell3Width", 0.0),
            cell4_width=d.get("Cell4Width", 0.0),
            tt1=d.get("Tt1", 0.0),
            tt2=d.get("Tt2", 0.0),
            tt3=d.get("Tt3", 0.0),
            tt5=d.get("Tt5", 0.0),
            tt6=d.get("Tt6", 0.0),
            xi1=d.get("xi1", 0.0),
            xi2=d.get("xi2", 0.0),
            xi3=d.get("xi3", 0.0),
            xi4=d.get("xi4", 0.0),
            xi5=d.get("xi5", 0.0),
            xi6=d.get("xi6", 0.0),
            xi7=d.get("xi7", 0.0),
            yi4=d.get("yi4", 0.0),
            yi7=d.get("yi7", 0.0),
        )


@dataclass(frozen=True)
class CantileverDefinition:
    """悬臂定义"""

    bc_l: float = 0.0
    bc_r: float = 0.0
    tc_l: float = 0.0
    tc_r: float = 0.0
    bc1_l: float = 0.0
    bc1_r: float = 0.0
    tc1_l: float = 0.0
    tc1_r: float = 0.0
    tc2_l: float = 0.0
    tc2_r: float = 0.0
    cantilever_symmetry: bool = False

    @classmethod
    def _from_dict(cls, d: dict | None) -> "CantileverDefinition | None":
        if not isinstance(d, dict):
            return None
        return cls(
            bc_l=d.get("BcL", 0.0),
            bc_r=d.get("BcR", 0.0),
            tc_l=d.get("TcL", 0.0),
            tc_r=d.get("TcR", 0.0),
            bc1_l=d.get("Bc1L", 0.0),
            bc1_r=d.get("Bc1R", 0.0),
            tc1_l=d.get("Tc1L", 0.0),
            tc1_r=d.get("Tc1R", 0.0),
            tc2_l=d.get("Tc2L", 0.0),
            tc2_r=d.get("Tc2R", 0.0),
            cantilever_symmetry=bool(d.get("CantileverSymmetry")),
        )


@dataclass(frozen=True)
class RectDefinition:
    """矩形定义"""

    b: float = 0.0
    h: float = 0.0
    r: float = 0.0
    xo1: float = 0.0
    yo1: float = 0.0
    edge_transition: int = 0
    filling_type: int = 0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "RectDefinition | None":
        if not isinstance(d, dict):
            return None
        return cls(
            b=d.get("B", 0.0),
            h=d.get("H", 0.0),
            r=d.get("R", 0.0),
            xo1=d.get("xo1", 0.0),
            yo1=d.get("yo1", 0.0),
            edge_transition=d.get("EdgeTransition", 0),
            filling_type=d.get("FillingType", 0),
        )


@dataclass(frozen=True)
class HollowDefinition:
    """空腹矩形内部挖空定义"""

    t1: float = 0.0
    t2: float = 0.0
    xi1: float = 0.0
    yi1: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "HollowDefinition | None":
        if not isinstance(d, dict):
            return None
        return cls(
            t1=d.get("t1", 0.0),
            t2=d.get("t2", 0.0),
            xi1=d.get("xi1", 0.0),
            yi1=d.get("yi1", 0.0),
        )


@dataclass(frozen=True)
class DiaphragmDefinition:
    """隔板定义"""

    has_diaphragm: bool = False
    tw: float = 0.0
    xi2: float = 0.0
    yi2: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "DiaphragmDefinition | None":
        if not isinstance(d, dict):
            return None
        return cls(
            has_diaphragm=bool(d.get("HasDiaphragm")),
            tw=d.get("tw", 0.0),
            xi2=d.get("xi2", 0.0),
            yi2=d.get("yi2", 0.0),
        )


@dataclass(frozen=True)
class GrooveDefinition:
    """凹槽定义"""

    has_groove: bool = False
    b1: float = 0.0
    b2: float = 0.0
    h: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "GrooveDefinition | None":
        if not isinstance(d, dict):
            return None
        return cls(
            has_groove=bool(d.get("HasGroove")),
            b1=d.get("b1", 0.0),
            b2=d.get("b2", 0.0),
            h=d.get("h", 0.0),
        )


@dataclass(frozen=True)
class FilletDefinition:
    """倒角定义"""

    r1: float = 0.0
    r2: float = 0.0

    @classmethod
    def _from_dict(cls, d: dict | None) -> "FilletDefinition | None":
        if not isinstance(d, dict):
            return None
        return cls(
            r1=d.get("R1", 0.0),
            r2=d.get("R2", 0.0),
        )


# ──────────────────────────────────────────────
# Section 基类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Section:
    """截面基类

    由 SectionManager 内部创建，用户不应直接实例化。
    get() / all() 返回此类型。

    外层 13 个属性：no, name, type, height, modelingPointX, modelingPointY,
    boundary, offset, prop, propFactor, relatedElements, stressPoints, definition
    """

    no: int
    name: str
    type: int
    height: float = 0.0
    modeling_point_x: float = 0.0
    modeling_point_y: float = 0.0
    boundary: SectionBBox | None = None
    offset: SectionOffset | None = None
    prop: SectionProp | None = None
    prop_factor: SectionPropFactor | None = None
    related_elements: list[int] = field(default_factory=list)
    stress_points: list[SectionStressPoint] = field(default_factory=list)
    definition: dict = field(default_factory=dict)

    @property
    def boundary_type(self) -> str:
        """截面边界类型名称"""
        return "Unknown"

    def __repr__(self) -> str:
        return f"Section(no={self.no}, type={self.boundary_type}, raw_type={self.type})"

    # ── 实例方法 ──────────────────────────────

    def set_offset(
        self,
        offset_type_y: Literal["Left", "Middle", "Right", "Manual"] = "Middle",
        d_offset_value_y: float = 0.0,
        offset_type_z: Literal["Top", "Center", "Bottom", "Manual"] = "Center",
        d_offset_value_z: float = 0.0,
    ) -> None:
        """设置截面偏移。"""
        ok, err = osis_section_offset(
            self.no, offset_type_y, d_offset_value_y, offset_type_z, d_offset_value_z
        )
        if not ok:
            raise RuntimeError(f"设置截面 {self.no} 偏移失败: {err}")

    def set_mesh(
        self,
        n_mesh_method: Literal[0, 1] = 0,
        d_mesh_size: float = 0.0,
    ) -> None:
        """设置截面网格。"""
        ok, err = osis_section_mesh(self.no, n_mesh_method, d_mesh_size)
        if not ok:
            raise RuntimeError(f"设置截面 {self.no} 网格失败: {err}")

    def export_pic(self, path: str | None = None) -> str:
        """生成截面图片并保存。"""
        ok, err = osis_export_section_pic(self.no)
        if not ok:
            raise RuntimeError(f"生成截面 {self.no} 图片失败: {err}")

        if path:
            try:
                project_dir = get_project_directory()
                if not project_dir:
                    raise RuntimeError("无法获取项目路径")
                default_path = project_dir + f"Image/section/_{self.no}.jpg"
                shutil.move(default_path, path)
                return path
            except Exception as e:
                raise RuntimeError(f"图片保存到 {path} 失败: {e}")

        return ""


# ──────────────────────────────────────────────
# Section 子类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class ConventionalBoxSection(Section):
    """常规箱梁截面（type=10）

    definition 包含：Box, Cantilever, Fillet, Total
    """

    box: BoxDefinition | None = None
    cantilever: CantileverDefinition | None = None
    fillet: FilletDefinition | None = None

    @property
    def boundary_type(self) -> str:
        return "ConventionalBox"


@dataclass(frozen=True)
class RectSection(Section):
    """矩形截面（type=5）

    definition 包含：Diaphragm, Groove, Hollow, Fillet, Total
    """

    diaphragm: DiaphragmDefinition | None = None
    groove: GrooveDefinition | None = None
    hollow: HollowDefinition | None = None
    fillet: FilletDefinition | None = None

    @property
    def boundary_type(self) -> str:
        return "Rect"


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class SectionManager:
    """截面管理器

    统一管理截面的创建、删除、修改和查询。

    用法:
        >>> from pyosis.section import section_manager
        >>> sec = section_manager.create_circle(D=0.5, Tw=0.02)
        >>> sec = section_manager.create_rect(B=6.5, H=3.2)
        >>> sec = section_manager.get(1)
        >>> all_secs = section_manager.all()
        >>> section_manager.delete(1)
        >>> section_manager.renumber(2, 100)
    """

    def __init__(self) -> None:
        self._sections: list[Section] = []
        self._sec_map: dict[int, Section] = {}
        self._loaded: bool = False

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有截面信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllSectionInfo", {})
        if not resp["success"]:
            raise RuntimeError(resp["error"])

        self._sections = [
            self._parse_section(d)
            for d in resp.get("data", [])
            if isinstance(d, dict) and "no" in d
        ]
        self._sec_map = {sec.no: sec for sec in self._sections}
        self._loaded = True

    def _parse_section(self, d: dict) -> Section:
        """根据 raw_type 解析并返回对应子类型的截面对象。"""
        raw_type = d.get("type")
        def_dict = d.get("definition") if isinstance(d.get("definition"), dict) else {}

        # 解析通用嵌套对象
        boundary = SectionBBox._from_dict(d.get("boundary"))
        offset = SectionOffset._from_dict(d.get("offset"))
        prop = SectionProp._from_dict(d.get("prop"))
        prop_factor = SectionPropFactor._from_dict(d.get("propFactor"))

        # 解析应力点
        stress_points = [
            sp
            for sp in (d.get("stressPoints") or [])
            if isinstance(sp, dict)
        ]

        # 通用参数
        common = dict(
            no=d.get("no", 0),
            name=d.get("name", ""),
            type=raw_type,
            height=d.get("height", 0.0),
            modeling_point_x=d.get("modelingPointX"),
            modeling_point_y=d.get("modelingPointY"),
            boundary=boundary,
            offset=offset,
            prop=prop,
            prop_factor=prop_factor,
            related_elements=list(d.get("relatedElements") or []),
            stress_points=[SectionStressPoint._from_dict(sp) for sp in stress_points],
            definition=def_dict,
        )

        if raw_type == 10:  # ConventionalBox
            return ConventionalBoxSection(
                **common,
                box=BoxDefinition._from_dict(def_dict.get("Box")),
                cantilever=CantileverDefinition._from_dict(def_dict.get("Cantilever")),
                fillet=FilletDefinition._from_dict(def_dict.get("Fillet")),
            )

        if raw_type == 5:  # Rect
            return RectSection(
                **common,
                diaphragm=DiaphragmDefinition._from_dict(def_dict.get("Diaphragm")),
                groove=GrooveDefinition._from_dict(def_dict.get("Groove")),
                hollow=HollowDefinition._from_dict(def_dict.get("Hollow")),
                fillet=FilletDefinition._from_dict(def_dict.get("Fillet")),
            )

        return Section(**common)

    def _invalidate(self) -> None:
        """标记缓存失效"""
        self._loaded = False

    def refresh(self) -> None:
        """强制刷新缓存"""
        self._sections = []
        self._sec_map = {}
        self._loaded = False
        self._load()

    def _next_section_no(self) -> int:
        """分配新截面编号"""
        self._load()
        if not self._sections:
            return 1
        return max(sec.no for sec in self._sections) + 1

    def _reload_get(self, no: int, what: str) -> Section:
        """创建/修改后从服务端重载并返回截面对象。"""
        self._invalidate()
        self._load()
        sec = self._sec_map.get(no)
        if sec is None:
            raise RuntimeError(f"{what} {no} 成功但无法从服务端获取完整信息")
        return sec

    # ── 增删改 ────────────────────────────────

    def create_Lshape(
        self,
        n_dir: Literal[0, 1] = 1,
        h: float = 0.1,
        b: float = 0.1,
        tf1: float = 0.016,
        tf2: float = 0.016,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建L形截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_Lshape(no, name, "LSHAPE", n_dir, h, b, tf1, tf2)
        if not ok:
            raise RuntimeError(f"创建L形截面 {no} 失败: {err}")
        return self._reload_get(no, "创建L形截面")

    def create_circle(
        self,
        e_circle_type: Literal["Hollow", "Solid"] = "Solid",
        d: float = 0.5,
        tw: float = 0.02,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建圆形截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_circle(no, name, "CIRCLE", e_circle_type, d, tw)
        if not ok:
            raise RuntimeError(f"创建圆形截面 {no} 失败: {err}")
        return self._reload_get(no, "创建圆形截面")

    def create_Tshape(
        self,
        n_dir: Literal[0, 1] = 1,
        h: float = 0.3,
        b: float = 0.2,
        tf: float = 0.016,
        tw: float = 0.016,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建T形截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_Tshape(no, name, "TSHAPE", n_dir, h, b, tf, tw)
        if not ok:
            raise RuntimeError(f"创建T形截面 {no} 失败: {err}")
        return self._reload_get(no, "创建T形截面")

    def create_Ishape(
        self,
        h: float = 0.3,
        bt: float = 0.13,
        bb: float = 0.13,
        tt: float = 0.016,
        tb: float = 0.016,
        tw: float = 0.016,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建I形截面（工字形截面）"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_Ishape(no, name, "ISHAPE", h, bt, bb, tt, tb, tw)
        if not ok:
            raise RuntimeError(f"创建I形截面 {no} 失败: {err}")
        return self._reload_get(no, "创建I形截面")

    def create_rect(
        self,
        b: float = 6.5,
        h: float = 3.2,
        transition_type: Literal["Chamfer", "Fillet"] = "Fillet",
        sec_type: Literal["Solid", "Hollow"] = "Solid",
        no: int | None = None,
        name: str | None = None,
        **kwargs,
    ) -> Section:
        """创建矩形截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_rect(no, name, "RECT", transition_type, sec_type, b, h, **kwargs)
        if not ok:
            raise RuntimeError(f"创建矩形截面 {no} 失败: {err}")
        return self._reload_get(no, "创建矩形截面")

    def create_steel_i(
        self,
        h: float,
        bt: float,
        bb: float,
        tt: float,
        tb: float,
        tw: float,
        web_rib_pos: Literal["Left", "Right", "Both"],
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建工字形钢截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_i(no, name, "STEELI", h, bt, bb, tt, tb, tw, web_rib_pos)
        if not ok:
            raise RuntimeError(f"创建工字形钢截面 {no} 失败: {err}")
        return self._reload_get(no, "创建工字形钢截面")

    def create_steel_box(
        self,
        h: float,
        bt: float,
        bct: float,
        bb: float,
        bcb: float,
        tt: float,
        tb: float,
        tw: float,
        same_layout: Literal[0, 1],
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建箱型钢截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_box(no, name, "STEELBOX", h, bt, bct, bb, bcb, tt, tb, tw, same_layout)
        if not ok:
            raise RuntimeError(f"创建箱型钢截面 {no} 失败: {err}")
        return self._reload_get(no, "创建箱型钢截面")

    def create_steel_box_three_cell(
        self,
        h: float,
        bt: float,
        bb: float,
        i: float,
        a1: float,
        a2: float,
        dt: float,
        tt1: float,
        tt2: float,
        tb1: float,
        db: float,
        tb2: float,
        tb3: float,
        tw1: float,
        dw: float,
        has_web: Literal[0, 1],
        tw2: float,
        web_rib_pos: Literal["Left", "Right", "Both"],
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建单箱单/三室钢截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_box_three_cell(
            no, name, "STEELBOXTHREECELL", h, bt, bb, i, a1, a2, dt,
            tt1, tt2, tb1, db, tb2, tb3, tw1, dw, has_web, tw2, web_rib_pos,
        )
        if not ok:
            raise RuntimeError(f"创建三室箱型钢截面 {no} 失败: {err}")
        return self._reload_get(no, "创建三室箱型钢截面")

    def create_steel_box_itf(
        self,
        h: float,
        b: float,
        bt: float,
        bb: float,
        i: float,
        a1: float,
        a2: float,
        dt: float,
        tt1: float,
        tt2: float,
        tt3: float,
        tb1: float,
        db: float,
        tb2: float,
        tb3: float,
        tw1: float,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建单箱单室斜顶板钢截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_box_itf(
            no, name, "STEELBOXITF", h, b, bt, bb, i, a1, a2, dt,
            tt1, tt2, tt3, tb1, db, tb2, tb3, tw1,
        )
        if not ok:
            raise RuntimeError(f"创建单箱单室斜顶板截面 {no} 失败: {err}")
        return self._reload_get(no, "创建顶底腹板加劲箱型钢截面")

    def create_steel_canti_box(
        self,
        h: float,
        bt: float,
        bb: float,
        i: float,
        a: float,
        dt: float,
        tt1: float,
        tt2: float,
        tb1: float,
        tw1: float,
        has_web: Literal[0, 1],
        tw2: float,
        web_rib_pos: Literal["Left", "Right", "Both"],
        eh: float,
        et: float,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建悬臂单箱单/双室钢截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_canti_box(
            no, name, "STEELCANTIBOX", h, bt, bb, i, a, dt,
            tt1, tt2, tb1, tw1, has_web, tw2, web_rib_pos, eh, et,
        )
        if not ok:
            raise RuntimeError(f"创建悬臂箱型钢截面 {no} 失败: {err}")
        return self._reload_get(no, "创建悬臂箱型钢截面")

    def create_steel_canti_box_ibf(
        self,
        h: float,
        bt: float,
        bb: float,
        bc: float,
        i: float,
        a: float,
        dt: float,
        tt1: float,
        tt2: float,
        tb1: float,
        tb2: float,
        tw1: float,
        has_web: Literal[0, 1],
        tw2: float,
        web_rib_pos: Literal["Left", "Right", "Both"],
        eh: float,
        et: float,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建悬臂单箱单/双室斜底板钢截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_canti_box_ibf(
            no, name, "STEELCANTIBOXIBF", h, bt, bb, bc, i, a, dt,
            tt1, tt2, tb1, tb2, tw1, has_web, tw2, web_rib_pos, eh, et,
        )
        if not ok:
            raise RuntimeError(f"创建悬臂箱型钢截面(加劲肋) {no} 失败: {err}")
        return self._reload_get(no, "创建悬臂箱型钢截面(加劲肋)")

    def create_steel_custom(
        self,
        point_matrix: str,
        line_matrix: str,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建自定义钢梁截面（通过点线关系输入）"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_custom(no, name, "STEELCUSTOM", point_matrix, line_matrix)
        if not ok:
            raise RuntimeError(f"创建自定义钢梁截面 {no} 失败: {err}")
        return self._reload_get(no, "创建自定义钢梁截面")

    def create_steel_custom_plate(
        self,
        plate_positions: list[str],
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建自定义钢梁截面（通过参数板输入）"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_steel_custom_plate(no, name, "STEELCUSTOMPLATE", plate_positions)
        if not ok:
            raise RuntimeError(f"创建自定义钢梁参数板截面 {no} 失败: {err}")
        return self._reload_get(no, "创建自定义钢梁截面(参数板)")

    def create_smallbox(
        self,
        e_girder_pos: Literal["LEFT", "MIDDLE", "RIGHT"] = "MIDDLE",
        h: float = 1.6,
        bs: float = 1.65,
        bm: float = 1.2,
        bc: float = 0.0,
        bb: float = 1.0,
        tt: float = 0.18,
        tb: float = 0.2,
        tw: float = 0.2,
        i: float = 4.0,
        tc: float = 0.18,
        tc1: float = 0.25,
        x: float = 0.2,
        xi1: float = 0.15,
        tt1: float = 0.25,
        xi2: float = 0.05,
        yi2: float = 0.05,
        b_slope: bool = False,
        i1: float = 0.0,
        i2: float = 0.0,
        r: float = 0.05,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建小箱梁截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_smallbox(
            no, name, "SMALLBOX", e_girder_pos, h, bs, bm, bc, bb,
            tt, tb, tw, i, tc, tc1, x, xi1, tt1, xi2, yi2, b_slope, i1, i2, r,
        )
        if not ok:
            raise RuntimeError(f"创建小箱梁截面 {no} 失败: {err}")
        return self._reload_get(no, "创建小箱梁截面")

    def create_hollowslab(
        self,
        e_girder_pos: Literal["LEFT", "MIDDLE", "RIGHT"] = "MIDDLE",
        h: float = 0.95,
        bs: float = 1.0,
        bm: float = 0.57,
        bj: float = 0.05,
        tt: float = 0.12,
        tb: float = 0.12,
        tw: float = 0.16,
        tc: float = 0.12,
        tc1: float = 0.16,
        bc: float = 0.38,
        xi1: float = 0.15,
        yi1: float = 0.08,
        xi2: float = 0.12,
        yi2: float = 0.08,
        xo3: float = 0.05,
        yo3: float = 0.05,
        xo4: float = 0.08,
        yo4: float = 0.08,
        h1: float = 0.12,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建空心板截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_hollowslab(
            no, name, "HOLLOWSLAB", e_girder_pos, h, bs, bm, bj,
            tt, tb, tw, tc, tc1, bc, xi1, yi1, xi2, yi2,
            xo3, yo3, xo4, yo4, h1,
        )
        if not ok:
            raise RuntimeError(f"创建空心板截面 {no} 失败: {err}")
        return self._reload_get(no, "创建空心板截面")

    def create_rounded_end(
        self,
        e_filling_type: Literal["Solid", "Hollow"] = "Solid",
        b: float = 7.0,
        h: float = 3.0,
        r: float = 2.0,
        b_has_diaphragm: bool = False,
        b_inner: float = 4.0,
        t: float = 1.0,
        xi1: float = 0.5,
        yi1: float = 0.25,
        tw: float = 1.0,
        xi2: float = 0.5,
        yi2: float = 0.25,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建圆端形截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_rounded_end(
            no, name, "ROUNDEDEND", e_filling_type, b, h, r,
            b_has_diaphragm, b_inner, t, xi1, yi1, tw, xi2, yi2,
        )
        if not ok:
            raise RuntimeError(f"创建圆端形截面 {no} 失败: {err}")
        return self._reload_get(no, "创建圆端形截面")

    def create_conventionalbox(
        self,
        h: float = 2.7,
        bt_l: float = 6.375,
        bt_r: float = 6.375,
        bb_l: float = 3.5,
        bb_r: float = 3.5,
        bs: float = 0.5,
        tt: float = 0.28,
        tb: float = 0.32,
        tw1: float = 0.5,
        tw2: float = 0.5,
        n_cell_num: int = 1,
        bi1: float = 5.05,
        bi2: float = 4.5,
        bi3: float = 5.05,
        bi4: float = 5.05,
        xi1: float = 1.5,
        tt1: float = 0.7,
        xi2: float = 0.0,
        tt2: float = 0.0,
        xi3: float = 1.0,
        yi3: float = 0.5,
        xi4: float = 0.5,
        tt4: float = 0.35,
        xi5: float = 0.6,
        yi5: float = 0.3,
        xi6: float = 1.0,
        tt6: float = 0.5,
        xi7: float = 0.6,
        yi7: float = 0.3,
        bc_l: float = 2.875,
        tc_l: float = 0.2,
        bc1_l: float = 1.325,
        tc1_l: float = 0.7,
        tc2_l: float = 0.4,
        b_symmetry: bool = True,
        bc_r: float = 2.875,
        tc_r: float = 0.2,
        bc1_r: float = 1.325,
        tc1_r: float = 0.7,
        tc2_r: float = 0.4,
        e_slope_type: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
        i3: float = 0.0,
        i4: float = 0.0,
        r1: float = 0.0,
        r2: float = 0.0,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建常规箱梁截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_conventionalbox(
            no, name, "CONVENTIONALBOX", h, bt_l, bt_r, bb_l, bb_r, bs,
            tt, tb, tw1, tw2, n_cell_num, bi1, bi2, bi3, bi4,
            xi1, tt1, xi2, tt2, xi3, yi3, xi4, tt4, xi5, yi5, xi6, tt6, xi7, yi7,
            bc_l, tc_l, bc1_l, tc1_l, tc2_l, b_symmetry, bc_r, tc_r, bc1_r, tc1_r, tc2_r,
            e_slope_type, i, i1, i2, i3, i4, r1, r2,
        )
        if not ok:
            raise RuntimeError(f"创建常规箱梁截面 {no} 失败: {err}")
        return self._reload_get(no, "创建常规箱梁截面")

    def create_flat_box(
        self,
        e_section_type: Literal["STREAMEDBOX"] = "STREAMEDBOX",
        h: float = 4.0,
        bt_l: float = 20.0,
        bt_r: float = 20.0,
        bb_l: float = 10.5,
        bb_r: float = 10.5,
        bs: float = 0.8,
        tt: float = 0.28,
        tb1: float = 0.27,
        tb2: float = 0.27,
        tw: float = 0.25,
        ttj: float = 0.5,
        tbj: float = 0.27,
        twj: float = 0.4,
        n_cell_num: int = 5,
        bi1: float = 4.7,
        bi2: float = 6.85,
        bi3: float = 6.0,
        bi4: float = 6.85,
        xi1: float = 0.6,
        tt1: float = 0.6,
        xi2: float = 1.0,
        tt2: float = 0.7,
        xi3: float = 0.2,
        yi3: float = 0.2,
        xi4: float = 1.0,
        tt4: float = 0.7,
        xi5: float = 0.6,
        yi5: float = 0.3,
        xi6: float = 0.5,
        tt6: float = 0.7,
        xi7: float = 0.5,
        yi7: float = 0.3,
        bc_l: float = 4.0,
        tc_l: float = 0.2,
        bc1_l: float = 0.5,
        tc1_l: float = 0.7,
        tc2_l: float = 0.4,
        b_symmetry: bool = True,
        bc_r: float = 4.0,
        tc_r: float = 0.2,
        bc1_r: float = 0.5,
        tc1_r: float = 0.7,
        tc2_r: float = 0.4,
        e_slope_type: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
        i3: float = 0.0,
        i4: float = 0.0,
        r1: float = 0.5,
        r2: float = 0.2,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建扁平箱梁截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_flat_box(
            no, name, e_section_type, h, bt_l, bt_r, bb_l, bb_r, bs,
            tt, tb1, tb2, tw, ttj, tbj, twj, n_cell_num, bi1, bi2, bi3, bi4,
            xi1, tt1, xi2, tt2, xi3, yi3, xi4, tt4, xi5, yi5, xi6, tt6, xi7, yi7,
            bc_l, tc_l, bc1_l, tc1_l, tc2_l, b_symmetry, bc_r, tc_r, bc1_r, tc1_r, tc2_r,
            e_slope_type, i, i1, i2, i3, i4, r1, r2,
        )
        if not ok:
            raise RuntimeError(f"创建扁平箱梁截面 {no} 失败: {err}")
        return self._reload_get(no, "创建扁平箱梁截面")

    def create_double_side_box(
        self,
        h: float = 3.8,
        bt: float = 36.0,
        bt_sub: float = 14.8,
        bs: float = 2.1,
        bb: float = 4.4,
        tt: float = 0.3,
        tb1: float = 0.3,
        tb2: float = 0.3,
        tw: float = 0.5,
        b_wind: float = 1.0,
        n_wind: float = 1.0,
        bi: float = 8.0,
        xi1: float = 1.0,
        tt1: float = 0.6,
        xi2: float = 1.0,
        tt2: float = 0.7,
        xi3: float = 0.6,
        yi3: float = 0.3,
        xo4: float = 1.0,
        tt4: float = 0.7,
        b1: float = 0.3,
        e_slope_type: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建双边箱截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_double_side_box(
            no, name, "DOUBLESIDEBOX", h, bt, bt_sub, bs, bb,
            tt, tb1, tb2, tw, b_wind, n_wind, bi, xi1, tt1, xi2, tt2,
            xi3, yi3, xo4, tt4, b1, e_slope_type, i, i1, i2,
        )
        if not ok:
            raise RuntimeError(f"创建双边箱截面 {no} 失败: {err}")
        return self._reload_get(no, "创建双边箱截面")

    def create_ribbed_slab(
        self,
        h: float = 2.8,
        bt: float = 21.5,
        bt_sub: float = 17.7,
        tt: float = 0.3,
        b: float = 0.2,
        eh: float = 1.25,
        b1: float = 1.8,
        b2: float = 0.2,
        x: float = 1.5,
        y: float = 0.3,
        e_slope_type: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建肋板式截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_ribbed_slab(
            no, name, "RIBBEDSLAB", h, bt, bt_sub, tt, b, eh, b1, b2, x, y, e_slope_type, i, i1, i2,
        )
        if not ok:
            raise RuntimeError(f"创建肋板式截面 {no} 失败: {err}")
        return self._reload_get(no, "创建肋板式截面")

    def create_TGirder(
        self,
        e_girder_pos: Literal["Left", "Middle", "Right"] = "Middle",
        h: float = 2.5,
        bs: float = 1.125,
        bm: float = 0.85,
        bc: float = 0.0,
        tt1: float = 0.16,
        tt2: float = 0.25,
        x: float = 0.6,
        tw: float = 0.2,
        bh: float = 0.6,
        hh: float = 0.35,
        yh: float = 0.25,
        b_slope: bool = False,
        i1: float = 0.0,
        i2: float = 0.0,
        r: float = 0.05,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建T梁截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_TGirder(
            no, name, "TGIRDER", e_girder_pos, h, bs, bm, bc,
            tt1, tt2, x, tw, bh, hh, yh, b_slope, i1, i2, r,
        )
        if not ok:
            raise RuntimeError(f"创建T梁截面 {no} 失败: {err}")
        return self._reload_get(no, "创建T梁截面")

    def create_custom(
        self,
        contour_matrix: str,
        no: int | None = None,
        name: str | None = None,
    ) -> Section:
        """创建自定义截面"""
        self._invalidate()
        if no is None:
            no = self._next_section_no()
        if name is None:
            name = f"SEC_{uuid.uuid4().hex[:12]}"
        ok, err = osis_section_custom(no, name, "CUSTOM", contour_matrix)
        if not ok:
            raise RuntimeError(f"创建自定义截面 {no} 失败: {err}")
        return self._reload_get(no, "创建自定义截面")

    def delete(self, no: int) -> None:
        """删除截面"""
        ok, err = osis_section_del(no)
        if not ok:
            raise RuntimeError(f"删除截面 {no} 失败: {err}")
        self._invalidate()

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改截面编号"""
        ok, err = osis_section_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改截面编号 {old_no} -> {new_no} 失败: {err}")
        self._invalidate()

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Section | list[Section | None]:
        """根据编号获取单个或多个截面 (O(k))"""
        self._load()
        if isinstance(no, int):
            return self._sec_map.get(no)
        if isinstance(no, list):
            return [self._sec_map.get(n) for n in no]
        raise TypeError(f"不支持的编号类型: {type(no)}")

    def all(self) -> list[Section]:
        """获取所有截面"""
        self._load()
        return list(self._sections)

    def count(self) -> int:
        """获取截面总数"""
        self._load()
        return len(self._sections)

    def __repr__(self) -> str:
        self._load()
        return f"SectionManager(count={len(self._sections)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

section_manager = SectionManager()
