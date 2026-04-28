"""截面管理器 - 统一管理截面的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- Section 基类与 HTTP 接口字段一一对应
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
import uuid

from ..core.client import osis_client

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


# ──────────────────────────────────────────────
# Section 基类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Section:
    """截面基类

    由 SectionManager 内部创建，用户不应直接实例化。
    字段与 HTTP 接口 GetAllSectionInfo 返回的 JSON 一一对应。
    """

    no: int                              # 截面编号
    name: str = ""                       # 截面名称
    type: int = 0                        # 截面类型
    prop: dict | None = None             # 截面属性
    prop_factor: dict | None = None      # 截面因子
    offset_type_y: int = 0               # 偏移类型 Y
    offset_value_y: float = 0.0          # 偏移值 Y
    offset_type_z: int = 0               # 偏移类型 Z
    offset_value_z: float = 0.0          # 偏移值 Z
    stress_points: list[dict] = field(default_factory=list)  # 应力点
    boundary: dict | None = None         # 边界
    height: float = 0.0                  # 高度
    modeling_point_x: float = 0.0        # 模型点 X
    modeling_point_y: float = 0.0        # 模型点 Y
    contour: list[dict] = field(default_factory=list)        # 轮廓
    has_concrete_section: bool = False   # 是否有混凝土截面
    has_steel_section: bool = False      # 是否有钢截面
    related_elements: list[int] = field(default_factory=list) # 相关元素

    @classmethod
    def _from_dict(cls, d: dict) -> Section:
        """从接口 dict 构造 Section 对象（内部使用）"""
        return cls(
            no=d.get("no"),
            name=d.get("name"),
            type=d.get("type"),
            prop=d.get("prop"),
            prop_factor=d.get("propFactor"),
            offset_type_y=d.get("offsetTypeY"),
            offset_value_y=d.get("offsetValueY"),
            offset_type_z=d.get("offsetTypeZ"),
            offset_value_z=d.get("offsetValueZ"),
            stress_points=list(d.get("stressPoints")),
            boundary=d.get("boundary"),
            height=d.get("height"),
            modeling_point_x=d.get("modelingPointX"),
            modeling_point_y=d.get("modelingPointY"),
            contour=list(d.get("contour")),
            has_concrete_section=d.get("hasConcreteSection"),
            has_steel_section=d.get("hasSteelSection"),
            related_elements=list(d.get("relatedElement")),
        )

    def __repr__(self) -> str:
        return f"Section(no={self.no}, name={self.name!r}, type={self.type})"

    # ── 实例方法 ──────────────────────────────

    def set_offset(
        self,
        offset_type_y: Literal["Left", "Middle", "Right", "Manual"] = "Middle",
        offset_value_y: float = 0.0,
        offset_type_z: Literal["Top", "Center", "Bottom", "Manual"] = "Center",
        offset_value_z: float = 0.0,
    ) -> None:
        """设置截面偏移。"""
        ok, err = osis_section_offset(
            self.no, offset_type_y, offset_value_y, offset_type_z, offset_value_z
        )
        if not ok:
            raise RuntimeError(f"设置截面 {self.no} 偏移失败: {err}")

    def set_mesh(
        self,
        mesh_method: Literal[0, 1] = 0,
        mesh_size: float = 0.0,
    ) -> None:
        """设置截面网格。"""
        ok, err = osis_section_mesh(self.no, mesh_method, mesh_size)
        if not ok:
            raise RuntimeError(f"设置截面 {self.no} 网格失败: {err}")
        
    def export(self):
        """生成截面图片，会在 image/section/ 目录下生成一张 {nSec}.jpg"""
        ok, err = osis_export_section_pic(self.no)
        if not ok:
            raise RuntimeError(f"导出截面 {self.no} 图片失败: {err}")


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class SectionManager:
    """截面管理器

    统一管理截面的创建、删除、修改和查询。

    用法:
        >>> from pyosis.section import section_manager
        >>> sec = section_manager.create_circle("圆形截面", d=0.5, tw=0.02)
        >>> sec = section_manager.create_rect("矩形截面", b=6.5, h=3.2)
        >>> sec = section_manager.get(1)
        >>> all_secs = section_manager.all()
        >>> section_manager.delete(1)
        >>> section_manager.renumber(2, 100)
    """

    def __init__(self) -> None:
        ...

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> list[Section]:
        """从服务端加载所有截面信息"""
        resp = osis_client("GetAllSectionInfo", {})
        if not resp["success"]:
            raise RuntimeError(resp["error"])

        data = resp.get("data", [])
        sections = [Section._from_dict(d) for d in data if isinstance(d, dict) and "no" in d]
        return sections

    def _next_no(self) -> int:
        """分配新截面编号"""
        sections = self._load()
        sec_no = [n.no for n in sections]
        if len(sec_no) == 0:
            return 1
        return max(sec_no) + 1

    # ── 增删改 ────────────────────────────────

    def create_Lshape(
        self,
        name: str,
        n_dir: Literal[0, 1] = 1,
        h: float = 0.1,
        b: float = 0.1,
        tf1: float = 0.016,
        tf2: float = 0.016,
        no: int | None = None,
    ) -> Section:
        """创建L形截面(LShape)。

        Args:
            name: 截面名称
            n_dir: L形截面方向，0=左下向，1=左上向
            h: 截面总高度
            b: 截面总宽度
            tf1: 竖肢厚度
            tf2: 横肢厚度
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_Lshape(no, name, "LSHAPE", n_dir, h, b, tf1, tf2)
        if not ok:
            raise RuntimeError(f"创建L形截面 {no} 失败: {err}")
        return self.get(no)

    def create_circle(
        self,
        name: str,
        e_circle_type: Literal["Hollow", "Solid"] = "Solid",
        d: float = 0.5,
        tw: float = 0.02,
        no: int | None = None,
    ) -> Section:
        """创建圆形截面(Circle)。

        Args:
            name: 截面名称
            e_circle_type: 截面类型，Hollow=空腹，Solid=实腹
            d: 圆形截面直径
            tw: 空腹截面的壁厚（仅当 e_circle_type 为 Hollow 时生效）
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_circle(no, name, "CIRCLE", e_circle_type, d, tw)
        if not ok:
            raise RuntimeError(f"创建圆形截面 {no} 失败: {err}")
        return self.get(no)

    def create_Tshape(
        self,
        name: str,
        n_dir: Literal[0, 1] = 1,
        h: float = 0.3,
        b: float = 0.2,
        tf: float = 0.016,
        tw: float = 0.016,
        no: int | None = None,
    ) -> Section:
        """创建T形截面(TShape)。

        Args:
            name: 截面名称
            n_dir: 截面方向，0=T形，1=倒T形
            h: 截面总高度
            b: 翼缘宽度
            tf: 翼缘厚度
            tw: 腹板厚度
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_Tshape(no, name, "TSHAPE", n_dir, h, b, tf, tw)
        if not ok:
            raise RuntimeError(f"创建T形截面 {no} 失败: {err}")
        return self.get(no)

    def create_Ishape(
        self,
        name: str,
        h: float = 0.3,
        bt: float = 0.13,
        bb: float = 0.13,
        tt: float = 0.016,
        tb: float = 0.016,
        tw: float = 0.016,
        no: int | None = None,
    ) -> Section:
        """创建I形截面（工字形截面）(IShape)。

        Args:
            name: 截面名称
            h: 截面总高度
            bt: 上翼缘宽度
            bb: 下翼缘宽度
            tt: 上翼缘厚度
            tb: 下翼缘厚度
            tw: 腹板厚度
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_Ishape(no, name, "ISHAPE", h, bt, bb, tt, tb, tw)
        if not ok:
            raise RuntimeError(f"创建I形截面 {no} 失败: {err}")
        return self.get(no)

    def create_rect(
        self,
        name: str,
        transition_type: Literal["Chamfer", "Fillet"] = "Fillet",
        sec_type: Literal["Solid", "Hollow"] = "Solid",
        b: float = 6.5,
        h: float = 3.2,
        xo1: float = 1.0,
        yo1: float = 0.5,
        r: float = 0.5,
        t1: float = 1.0,
        t2: float = 1.0,
        xi1: float = 0.5,
        yi1: float = 0.25,
        has_diaphragm: bool = False,
        tw: float = 1.0,
        xi2: float = 0.5,
        yi2: float = 0.25,
        has_groove: bool = False,
        b1: float = 1.2,
        b2: float = 0.8,
        h_groove: float = 0.2,
        no: int | None = None,
    ) -> Section:
        """创建矩形截面(RECT)。

        Args:
            name: 截面名称
            transition_type: 倒角类型，Chamfer=斜倒角，Fillet=圆倒角
            sec_type: 截面类型，Solid=实腹，Hollow=空腹
            b: 截面宽度
            h: 截面高度
            xo1: 斜倒角宽度
            yo1: 斜倒角高度
            r: 圆倒角半径
            t1: 壁厚1
            t2: 壁厚2
            xi1: 内倒角宽度
            yi1: 内倒角高度
            has_diaphragm: 是否有隔板
            tw: 隔板厚度
            xi2: 隔板倒角宽度
            yi2: 隔板倒角高度
            has_groove: 是否有凹槽
            b1: 凹槽上口宽度
            b2: 凹槽下口宽度
            h_groove: 凹槽深度
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_rect(
            no, name, "RECT", transition_type, sec_type, b, h,
            xo1, yo1, r, t1, t2, xi1, yi1, has_diaphragm, tw, xi2, yi2,
            has_groove, b1, b2, h_groove,
        )
        if not ok:
            raise RuntimeError(f"创建矩形截面 {no} 失败: {err}")
        return self.get(no)

    def create_steel_i(
        self,
        name: str,
        h: float = 0.0,
        bt: float = 0.0,
        bb: float = 0.0,
        tt: float = 0.0,
        tb: float = 0.0,
        tw: float = 0.0,
        web_rib_pos: Literal["Left", "Right", "Both"] = "Both",
        no: int | None = None,
    ) -> Section:
        """创建工字形钢截面(STEELI)。

        Args:
            name: 截面名称
            h: 梁高
            bt: 上翼缘宽度
            bb: 下翼缘宽度
            tt: 上翼缘厚度
            tb: 下翼缘厚度
            tw: 腹板厚度
            web_rib_pos: 加劲肋位置，Left=左侧，Right=右侧，Both=两侧
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_steel_i(no, name, "STEELI", h, bt, bb, tt, tb, tw, web_rib_pos)
        if not ok:
            raise RuntimeError(f"创建工字形钢截面 {no} 失败: {err}")
        return self.get(no)

    def create_steel_box(
        self,
        name: str,
        h: float = 0.0,
        bt: float = 0.0,
        bct: float = 0.0,
        bb: float = 0.0,
        bcb: float = 0.0,
        tt: float = 0.0,
        tb: float = 0.0,
        tw: float = 0.0,
        same_layout: Literal[0, 1] = 1,
        no: int | None = None,
    ) -> Section:
        """创建箱型钢截面(STEELBOX)。

        Args:
            name: 截面名称
            h: 梁高
            bt: 上翼缘宽度
            bct: 上翼缘悬出宽
            bb: 下翼缘宽度
            bcb: 下翼缘悬出宽
            tt: 上翼缘厚度
            tb: 下翼缘厚度
            tw: 腹板厚度
            same_layout: 下翼缘加劲肋是否与上翼缘相同，1=相同，0=不同
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_steel_box(no, name, "STEELBOX", h, bt, bct, bb, bcb, tt, tb, tw, same_layout)
        if not ok:
            raise RuntimeError(f"创建箱型钢截面 {no} 失败: {err}")
        return self.get(no)

    def create_steel_box_three_cell(
        self,
        name: str,
        h: float = 0.0,
        bt: float = 0.0,
        bb: float = 0.0,
        i: float = 0.0,
        a1: float = 0.0,
        a2: float = 0.0,
        dt: float = 0.0,
        tt1: float = 0.0,
        tt2: float = 0.0,
        tb1: float = 0.0,
        db: float = 0.0,
        tb2: float = 0.0,
        tb3: float = 0.0,
        tw1: float = 0.0,
        dw: float = 0.0,
        has_web: Literal[0, 1] = 1,
        tw2: float = 0.0,
        web_rib_pos: Literal["Left", "Right", "Both"] = "Both",
        no: int | None = None,
    ) -> Section:
        """创建单箱单/三室钢截面(STEELBOXTHREECELL)。

        Args:
            name: 截面名称
            h: 梁高
            bt: 上翼缘宽度
            bb: 下翼缘宽度
            i: 顶面横坡
            a1: 边腹板倾角
            a2: 斜底板倾角
            dt: 顶点变厚点至起点距离
            tt1: 顶板厚度1
            tt2: 顶板厚度2
            tb1: 底板厚度
            db: 斜底板变厚点至起点距离
            tb2: 斜底板厚度1
            tb3: 斜底板厚度2
            tw1: 边腹板厚度
            dw: 中腹板至主梁中心线距离
            has_web: 是否有中腹板，1=有，0=无
            tw2: 中腹板厚度
            web_rib_pos: 加劲肋位置，Left=左侧，Right=右侧，Both=两侧
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_steel_box_three_cell(
            no, name, "STEELBOXTHREECELL", h, bt, bb, i, a1, a2, dt,
            tt1, tt2, tb1, db, tb2, tb3, tw1, dw, has_web, tw2, web_rib_pos,
        )
        if not ok:
            raise RuntimeError(f"创建三室箱型钢截面 {no} 失败: {err}")
        return self.get(no)

    def create_steel_box_itf(
        self,
        name: str,
        h: float = 0.0,
        b: float = 0.0,
        bt: float = 0.0,
        bb: float = 0.0,
        i: float = 0.0,
        a1: float = 0.0,
        a2: float = 0.0,
        dt: float = 0.0,
        tt1: float = 0.0,
        tt2: float = 0.0,
        tt3: float = 0.0,
        tb1: float = 0.0,
        db: float = 0.0,
        tb2: float = 0.0,
        tb3: float = 0.0,
        tw1: float = 0.0,
        no: int | None = None,
    ) -> Section:
        """创建单箱单室斜顶板钢截面(STEELBOXITF)。

        Args:
            name: 截面名称
            h: 梁高
            b: 梁宽
            bt: 顶板宽度
            bb: 平底板宽度
            i: 顶面横坡
            a1: 斜顶板倾角
            a2: 斜底板倾角
            dt: 顶板变厚点至起点距离
            tt1: 顶板厚度1
            tt2: 顶板厚度2
            tt3: 斜顶板厚度
            tb1: 底板厚度
            db: 斜底板变厚点至起点距离
            tb2: 斜底板厚度1
            tb3: 斜底板厚度2
            tw1: 边腹板厚
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_steel_box_itf(
            no, name, "STEELBOXITF", h, b, bt, bb, i, a1, a2, dt,
            tt1, tt2, tt3, tb1, db, tb2, tb3, tw1,
        )
        if not ok:
            raise RuntimeError(f"创建单箱单室斜顶板截面 {no} 失败: {err}")
        return self.get(no)

    def create_steel_canti_box(
        self,
        name: str,
        h: float = 0.0,
        bt: float = 0.0,
        bb: float = 0.0,
        i: float = 0.0,
        a: float = 0.0,
        dt: float = 0.0,
        tt1: float = 0.0,
        tt2: float = 0.0,
        tb1: float = 0.0,
        tw1: float = 0.0,
        has_web: Literal[0, 1] = 1,
        tw2: float = 0.0,
        web_rib_pos: Literal["Left", "Right", "Both"] = "Both",
        h_end: float = 0.0,
        t_end: float = 0.0,
        no: int | None = None,
    ) -> Section:
        """创建悬臂单箱单/双室钢截面(STEELCANTIBOX)。

        Args:
            name: 截面名称
            h: 梁高
            bt: 顶板宽度
            bb: 平底板宽度
            i: 顶面横坡
            a: 边腹板倾角
            dt: 顶板变厚点至起点距离
            tt1: 顶板厚度1
            tt2: 顶板厚度2
            tb1: 底板厚度
            tw1: 边腹板厚度
            has_web: 是否有中腹板，1=有，0=无
            tw2: 中腹板厚度
            web_rib_pos: 加劲肋位置，Left=左侧，Right=右侧，Both=两侧
            h_end: 悬臂端封板高
            t_end: 悬臂端封板厚
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_steel_canti_box(
            no, name, "STEELCANTIBOX", h, bt, bb, i, a, dt,
            tt1, tt2, tb1, tw1, has_web, tw2, web_rib_pos, h_end, t_end,
        )
        if not ok:
            raise RuntimeError(f"创建悬臂箱型钢截面 {no} 失败: {err}")
        return self.get(no)

    def create_steel_canti_box_ibf(
        self,
        name: str,
        h: float = 0.0,
        bt: float = 0.0,
        bb: float = 0.0,
        bc: float = 0.0,
        i: float = 0.0,
        a: float = 0.0,
        dt: float = 0.0,
        tt1: float = 0.0,
        tt2: float = 0.0,
        tb1: float = 0.0,
        tb2: float = 0.0,
        tw1: float = 0.0,
        has_web: Literal[0, 1] = 1,
        tw2: float = 0.0,
        web_rib_pos: Literal["Left", "Right", "Both"] = "Both",
        h_end: float = 0.0,
        t_end: float = 0.0,
        no: int | None = None,
    ) -> Section:
        """创建悬臂单箱单/双室斜底板钢截面(STEELCANTIBOXIBF)。

        Args:
            name: 截面名称
            h: 梁高
            bt: 顶板宽度
            bb: 平底板宽度
            bc: 悬臂长
            i: 顶面横坡
            a: 边腹板倾角
            dt: 顶板变厚点至起点距离
            tt1: 顶板厚度1
            tt2: 顶板厚度2
            tb1: 底板厚度
            tb2: 斜底板厚度
            tw1: 边腹板厚度
            has_web: 是否有中腹板，1=有，0=无
            tw2: 中腹板厚度
            web_rib_pos: 加劲肋位置，Left=左侧，Right=右侧，Both=两侧
            h_end: 悬臂端封板高
            t_end: 悬臂端封板厚
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_steel_canti_box_ibf(
            no, name, "STEELCANTIBOXIBF", h, bt, bb, bc, i, a, dt,
            tt1, tt2, tb1, tb2, tw1, has_web, tw2, web_rib_pos, h_end, t_end,
        )
        if not ok:
            raise RuntimeError(f"创建悬臂箱型钢截面(加劲肋) {no} 失败: {err}")
        return self.get(no)

    def create_steel_custom(
        self,
        name: str,
        point_matrix: str = "",
        line_matrix: str = "",
        no: int | None = None,
    ) -> Section:
        """创建自定义钢梁截面（通过点线关系输入）(STEELCUSTOM)。

        Args:
            name: 截面名称
            point_matrix: 几何点矩阵名称（需先用 osis_matrix 定义）
            line_matrix: 几何线矩阵名称（需先用 osis_matrix 定义）
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_steel_custom(no, name, "STEELCUSTOM", point_matrix, line_matrix)
        if not ok:
            raise RuntimeError(f"创建自定义钢梁截面 {no} 失败: {err}")
        return self.get(no)

    def create_steel_custom_plate(
        self,
        name: str,
        plate_positions: list[str] | None = None,
        no: int | None = None,
    ) -> Section:
        """创建自定义钢梁截面（通过参数板输入）(STEELCUSTOMPLATE)。

        Args:
            name: 截面名称
            plate_positions: 板件位置列表
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        if plate_positions is None:
            plate_positions = []
        ok, err = osis_section_steel_custom_plate(no, name, "STEELCUSTOMPLATE", plate_positions)
        if not ok:
            raise RuntimeError(f"创建自定义钢梁参数板截面 {no} 失败: {err}")
        return self.get(no)

    def create_smallbox(
        self,
        name: str,
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
    ) -> Section:
        """创建小箱梁截面(SMALLBOX)。

        Args:
            name: 截面名称
            e_girder_pos: 截面位置，LEFT=左边梁，MIDDLE=中梁，RIGHT=右边梁
            h: 箱梁高度
            bs: 边翼板宽
            bm: 中梁半宽
            bc: 现浇湿接缝半宽
            bb: 底板宽
            tt: 顶板厚
            tb: 底板厚
            tw: 腹板厚
            i: 腹板倾斜比
            tc: 边梁悬臂端部厚
            tc1: 边梁悬臂根部厚
            x: 中梁翼板倒角宽
            xi1: 倒角1宽（顶板）
            tt1: 倒角1根部厚
            xi2: 倒角2宽（底板）
            yi2: 倒角2高
            b_slope: 是否输入横坡
            i1: 顶左坡
            i2: 顶右坡
            r: 底板倒角圆弧半径
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_smallbox(
            no, name, "SMALLBOX", e_girder_pos, h, bs, bm, bc, bb,
            tt, tb, tw, i, tc, tc1, x, xi1, tt1, xi2, yi2, b_slope, i1, i2, r,
        )
        if not ok:
            raise RuntimeError(f"创建小箱梁截面 {no} 失败: {err}")
        return self.get(no)

    def create_hollowslab(
        self,
        name: str,
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
    ) -> Section:
        """创建空心板截面(HOLLOWSLAB)。

        Args:
            name: 截面名称
            e_girder_pos: 截面位置，LEFT=左边梁，MIDDLE=中梁，RIGHT=右边梁
            h: 板高
            bs: 边板宽（e_girder_pos=MIDDLE 时设置为空）
            bm: 中梁半宽
            bj: 铰缝上端缩进宽
            tt: 顶板厚
            tb: 底板厚
            tw: 腹板下端厚
            tc: 边板悬臂端部厚
            tc1: 边板悬臂根部厚
            bc: 边板悬臂厚
            xi1: 倒角1宽（顶板）
            yi1: 倒角1高
            xi2: 倒角2宽（底板）
            yi2: 倒角2高
            xo3: 倒角3宽（上端）
            yo3: 倒角3高
            xo4: 倒角4宽（下端）
            yo4: 倒角4高
            h1: 下端竖直段高
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_hollowslab(
            no, name, "HOLLOWSLAB", e_girder_pos, h, bs, bm, bj,
            tt, tb, tw, tc, tc1, bc, xi1, yi1, xi2, yi2,
            xo3, yo3, xo4, yo4, h1,
        )
        if not ok:
            raise RuntimeError(f"创建空心板截面 {no} 失败: {err}")
        return self.get(no)

    def create_rounded_end(
        self,
        name: str,
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
    ) -> Section:
        """创建圆端形截面(ROUNDEDEND)。

        Args:
            name: 截面名称
            e_filling_type: 填充类型，Solid=实腹，Hollow=空腹
            b: 截面宽
            h: 截面高
            r: 圆弧半径
            b_has_diaphragm: 是否有隔板
            b_inner: 内宽
            t: 壁厚
            xi1: 内倒角宽
            yi1: 内倒角高
            tw: 隔板厚
            xi2: 隔板倒角宽
            yi2: 隔板倒角高
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_rounded_end(
            no, name, "ROUNDEDEND", e_filling_type, b, h, r,
            b_has_diaphragm, b_inner, t, xi1, yi1, tw, xi2, yi2,
        )
        if not ok:
            raise RuntimeError(f"创建圆端形截面 {no} 失败: {err}")
        return self.get(no)

    def create_conventionalbox(
        self,
        name: str,
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
    ) -> Section:
        """创建常规箱梁截面(CONVENTIONALBOX)。

        Args:
            name: 截面名称
            h: 截面高度
            bt_l: 设计线左顶板宽
            bt_r: 设计线右顶板宽
            bb_l: 设计线左底板宽
            bb_r: 设计线右底板宽
            bs: 悬臂根部至边腹板顶内侧宽度
            tt: 顶板厚
            tb: 底板厚
            tw1: 边腹板厚
            tw2: 中腹板厚
            n_cell_num: 箱室个数
            bi1~bi4: 箱室1~4宽度
            xi1~xi7, yi3~yi7, tt1~tt6: 各倒角参数
            bc_l, tc_l, bc1_l, tc1_l, tc2_l: 左悬臂参数
            b_symmetry: 右侧是否对称
            bc_r, tc_r, bc1_r, tc1_r, tc2_r: 右悬臂参数
            e_slope_type: 横坡类型
            i~i4: 各坡度参数
            r1, r2: 倒角圆弧半径
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_conventionalbox(
            no, name, "CONVENTIONALBOX", h, bt_l, bt_r, bb_l, bb_r, bs,
            tt, tb, tw1, tw2, n_cell_num, bi1, bi2, bi3, bi4,
            xi1, tt1, xi2, tt2, xi3, yi3, xi4, tt4, xi5, yi5, xi6, tt6, xi7, yi7,
            bc_l, tc_l, bc1_l, tc1_l, tc2_l, b_symmetry, bc_r, tc_r, bc1_r, tc1_r, tc2_r,
            e_slope_type, i, i1, i2, i3, i4, r1, r2,
        )
        if not ok:
            raise RuntimeError(f"创建常规箱梁截面 {no} 失败: {err}")
        return self.get(no)

    def create_flat_box(
        self,
        name: str,
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
    ) -> Section:
        """创建扁平箱梁截面(FLATBOX)。

        Args:
            name: 截面名称
            h: 截面高度
            bt_l: 设计线左顶板宽
            bt_r: 设计线右顶板宽
            bb_l: 设计线左底板宽
            bb_r: 设计线右底板宽
            bs: 悬臂根部至边腹板顶内侧宽度
            tt: 顶板厚
            tb1: 底板厚
            tb2: 斜底板厚
            tw: 腹板厚
            ttj: 加强室顶板厚
            tbj: 加强室底板厚
            twj: 加强室腹板厚
            n_cell_num: 箱室个数
            bi1~bi4: 箱室1~4宽度
            xi1~xi7, yi3~yi7, tt1~tt6: 各倒角参数
            bc_l, tc_l, bc1_l, tc1_l, tc2_l: 左悬臂参数
            b_symmetry: 右侧是否对称
            bc_r, tc_r, bc1_r, tc1_r, tc2_r: 右悬臂参数
            e_slope_type: 横坡类型
            i~i4: 各坡度参数
            r1, r2: 倒角圆弧半径
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_flat_box(
            no, name, "FLATBOX", h, bt_l, bt_r, bb_l, bb_r, bs,
            tt, tb1, tb2, tw, ttj, tbj, twj, n_cell_num, bi1, bi2, bi3, bi4,
            xi1, tt1, xi2, tt2, xi3, yi3, xi4, tt4, xi5, yi5, xi6, tt6, xi7, yi7,
            bc_l, tc_l, bc1_l, tc1_l, tc2_l, b_symmetry, bc_r, tc_r, bc1_r, tc1_r, tc2_r,
            e_slope_type, i, i1, i2, i3, i4, r1, r2,
        )
        if not ok:
            raise RuntimeError(f"创建扁平箱梁截面 {no} 失败: {err}")
        return self.get(no)

    def create_double_side_box(
        self,
        name: str,
        h: float = 3.8,
        bt: float = 36.0,
        bt_bottom: float = 14.8,
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
    ) -> Section:
        """创建双边箱截面(DOUBLESIDEBOX)。

        Args:
            name: 截面名称
            h: 梁高
            bt: 顶板顶宽
            bt_bottom: 顶板底宽
            bs: 边箱实心段顶板宽
            bb: 底板宽
            tt: 顶板厚
            tb1: 底板厚
            tb2: 斜底板厚
            tw: 腹板厚
            b_wind: 风嘴上部水平宽度
            n_wind: 风嘴上部竖向高度
            bi: 室内宽
            xi1: 倒角1宽(顶板边)
            tt1: 倒角1根部厚
            xi2: 倒角2宽(顶板中)
            tt2: 倒角2根部厚
            xi3: 倒角3宽(底板中)
            yi3: 倒角3高
            xo4: 倒角4宽(顶板)
            tt4: 倒角4根部厚
            b1: 腹板内侧倒角宽
            e_slope_type: 横坡类型
            i: 整体转梁横坡
            i1: 顶左坡
            i2: 顶右坡
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_double_side_box(
            no, name, "DOUBLESIDEBOX", h, bt, bt_bottom, bs, bb,
            tt, tb1, tb2, tw, b_wind, n_wind, bi, xi1, tt1, xi2, tt2,
            xi3, yi3, xo4, tt4, b1, e_slope_type, i, i1, i2,
        )
        if not ok:
            raise RuntimeError(f"创建双边箱截面 {no} 失败: {err}")
        return self.get(no)

    def create_ribbed_slab(
        self,
        name: str,
        h: float = 2.8,
        bt: float = 21.5,
        bt_bottom: float = 17.7,
        tt: float = 0.3,
        b: float = 0.2,
        h_rib: float = 1.25,
        b1: float = 1.8,
        b2: float = 0.2,
        x: float = 1.5,
        y: float = 0.3,
        e_slope_type: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
        no: int | None = None,
    ) -> Section:
        """创建肋板式截面(RIBBEDSLAB)。

        Args:
            name: 截面名称
            h: 截面高度
            bt: 顶板顶宽
            bt_bottom: 顶板底宽
            tt: 顶板厚
            b: 风嘴上部水平宽度
            h_rib: 风嘴上部竖向宽度
            b1: 边肋底宽
            b2: 边肋内侧倒角宽
            x: 顶板倒角宽
            y: 顶板倒角高
            e_slope_type: 横坡类型
            i: 整体转梁横坡
            i1: 顶左坡
            i2: 顶右坡
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_ribbed_slab(
            no, name, "RIBBEDSLAB", h, bt, bt_bottom, tt, b, h_rib, b1, b2, x, y, e_slope_type, i, i1, i2,
        )
        if not ok:
            raise RuntimeError(f"创建肋板式截面 {no} 失败: {err}")
        return self.get(no)

    def create_TGirder(
        self,
        name: str,
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
    ) -> Section:
        """创建T梁截面(TGIRDER)。

        Args:
            name: 截面名称
            e_girder_pos: 截面位置，Left=左边梁，Middle=中梁，Right=右边梁
            h: 梁高
            bs: 边翼板宽
            bm: 中梁半宽
            bc: 现浇湿接缝半宽
            tt1: 翼板厚
            tt2: 翼板根部厚
            x: 翼板倒角宽
            tw: 腹板厚度
            bh: 马蹄宽度
            hh: 马蹄高度
            yh: 马蹄倒角高
            b_slope: 是否输入横坡
            i1: 顶左坡
            i2: 顶右坡
            r: 顶板处倒角半径
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_TGirder(
            no, name, "TGIRDER", e_girder_pos, h, bs, bm, bc,
            tt1, tt2, x, tw, bh, hh, yh, b_slope, i1, i2, r,
        )
        if not ok:
            raise RuntimeError(f"创建T梁截面 {no} 失败: {err}")
        return self.get(no)

    def create_custom(
        self,
        name: str,
        contour_matrix: str = "",
        no: int | None = None,
    ) -> Section:
        """创建自定义截面(CUSTOM)。

        Args:
            name: 截面名称
            contour_matrix: 轮廓点矩阵名称（需先用 osis_matrix 定义）
            no: 截面编号，不填则自动分配
        """
        if no is None:
            no = self._next_no()
        ok, err = osis_section_custom(no, name, "CUSTOM", contour_matrix)
        if not ok:
            raise RuntimeError(f"创建自定义截面 {no} 失败: {err}")
        return self.get(no)

    def delete(self, no: int) -> None:
        """删除截面"""
        ok, err = osis_section_del(no)
        if not ok:
            raise RuntimeError(f"删除截面 {no} 失败: {err}")
        

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改截面编号"""
        ok, err = osis_section_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改截面编号 {old_no} -> {new_no} 失败: {err}")
        

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int], expected_cls: type[Section]=Section) -> Section | list[Section | None]:
        """根据编号获取单个或多个截面 (O(k))"""
        if isinstance(no, int):
            no = [no]
        elif isinstance(no, list):
            ...
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")
        resp = osis_client("GetSectionInfoByNos", {"no": no})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        secs = [expected_cls._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(secs) == 0:
            return None
        elif len(secs) == 1:
            return secs[0]
        return secs
    
    def all(self) -> list[Section]:
        """获取所有截面"""
        return self._load()

    def count(self) -> int:
        """获取截面总数"""
        return len(self._load())

    def __repr__(self) -> str:
        return f"SectionManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

section_manager = SectionManager()
