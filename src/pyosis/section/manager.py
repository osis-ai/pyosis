"""截面管理器 - 统一管理截面的增删改查

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 返回数据类对象而非 HTTP 元组
- 内部维护截面列表，通过 get 等方法查询，不暴露 HTTP 接口细节

支持的截面类型：
- 混凝土截面：LSHAPE, CIRCLE, TSHAPE, ISHAPE, SMALLBOX, RECT, HOLLOWSLAB, ROUNDEDEND,
  CONVENTIONALBOX, FLATBOX, DOUBLESIDEBOX, RIBBEDSLAB, TGIRDER, CUSTOM
- 钢截面：STEELI, STEELBOX, STEELBOXTHREECELL, STEELBOXITF, STEELCANTIBOX,
  STEELCANTIBOXIBF, STEELCUSTOM, STEELCUSTOMPLATE
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

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
    osis_section_del,
    osis_section_mod,
)


# ──────────────────────────────────────────────
# 数据类
# ──────────────────────────────────────────────


@dataclass(frozen=True)
class Section:
    """截面对象

    由 SectionManager 内部创建，用户不应直接实例化。
    """

    no: int
    name: str
    section_type: str  # "LSHAPE", "CIRCLE", "TSHAPE", "ISHAPE", "SMALLBOX", "RECT",
                        # "HOLLOWSLAB", "ROUNDEDEND", "CONVENTIONALBOX", "FLATBOX",
                        # "DOUBLESIDEBOX", "RIBBEDSLAB", "TGIRDER", "CUSTOM",
                        # "STEELI", "STEELBOX", "STEELBOXTHREECELL", "STEELBOXITF",
                        # "STEELCANTIBOX", "STEELCANTIBOXIBF", "STEELCUSTOM", "STEELCUSTOMPLATE"

    @classmethod
    def _from_dict(cls, d: dict) -> Section:
        """从接口 dict 构造 Section 对象（内部使用）"""
        return cls(
            no=d.get("no", 0),
            name=d.get("name", ""),
            section_type=d.get("sectionType", ""),
        )


# ──────────────────────────────────────────────
# 管理类
# ──────────────────────────────────────────────


class SectionManager:
    """截面管理器

    统一管理截面的创建、删除、修改和查询。

    用法:
        >>> from pyosis.section import section_manager
        >>> section_manager.create_circle(1, "圆形截面", D=0.5, Tw=0.02)          # 创建圆形截面
        >>> section_manager.create_rect(2, "矩形截面", B=6.5, H=3.2)              # 创建矩形截面
        >>> section_manager.create_steel_i(3, "工字钢", H=0.3, Bt=0.13, ...)       # 创建工字形钢截面
        >>> sec = section_manager.get(1)                                         # 按编号查询
        >>> all_secs = section_manager.all()                                     # 获取全部截面
        >>> section_manager.delete(1)                                            # 删除截面
        >>> section_manager.renumber(2, 100)                                     # 修改编号
    """

    def __init__(self) -> None:
        self._sections: list[Section] = []
        self._sec_map: dict[int, Section] = {}  # 按编号索引：O(1) 查询
        self._loaded: bool = False

    # ── 数据加载 ──────────────────────────────

    def _load(self) -> None:
        """从服务端加载所有截面信息（延迟加载，带缓存）"""
        if self._loaded:
            return
        resp = osis_client("GetAllSectionInfo", {})
        if isinstance(resp, tuple):
            raise RuntimeError(f"加载截面信息失败: {resp[1]}")
        self._sections = [
            Section._from_dict(d) for d in resp.get("data", []) if isinstance(d, dict) and "no" in d
        ]

        # 构建索引：编号 -> 截面对象 (O(1) 查询)
        self._sec_map = {sec.no: sec for sec in self._sections}

        self._loaded = True

    def refresh(self) -> None:
        """强制刷新缓存（模型变更后自动调用，也可手动调用）"""
        self._sections = []
        self._sec_map = {}
        self._loaded = False
        self._load()

    # ── 增删改 ────────────────────────────────

    def create_Lshape(
        self,
        no: int,
        name: str,
        nDir: Literal[0, 1] = 1,
        H: float = 0.1,
        B: float = 0.1,
        Tf1: float = 0.016,
        Tf2: float = 0.016,
    ) -> None:
        """创建L形截面

        Args:
            no: 截面编号
            name: 截面名称
            nDir: L形截面方向，0=左下向，1=左上向
            H: 截面总高度
            B: 截面总宽度
            Tf1: 竖肢厚度
            Tf2: 横肢厚度

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_Lshape(no, name, "LSHAPE", nDir, H, B, Tf1, Tf2)
        if not ok:
            raise RuntimeError(f"创建L形截面 {no} 失败: {err}")
        self._loaded = False

    def create_circle(
        self,
        no: int,
        name: str,
        eCircleType: Literal["Hollow", "Solid"] = "Solid",
        D: float = 0.5,
        Tw: float = 0.02,
    ) -> None:
        """创建圆形截面

        Args:
            no: 截面编号
            name: 截面名称
            eCircleType: 截面类型，Hollow=空腹截面，Solid=实腹截面
            D: 圆形截面直径
            Tw: 空腹截面的壁厚

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_circle(no, name, "CIRCLE", eCircleType, D, Tw)
        if not ok:
            raise RuntimeError(f"创建圆形截面 {no} 失败: {err}")
        self._loaded = False

    def create_Tshape(
        self,
        no: int,
        name: str,
        nDir: Literal[0, 1] = 1,
        H: float = 0.3,
        B: float = 0.2,
        Tf: float = 0.016,
        Tw: float = 0.016,
    ) -> None:
        """创建T形截面

        Args:
            no: 截面编号
            name: 截面名称
            nDir: 截面方向，0=T形，1=倒T形
            H: 截面总高度
            B: 翼缘宽度
            Tf: 翼缘厚度
            Tw: 腹板厚度

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_Tshape(no, name, "TSHAPE", nDir, H, B, Tf, Tw)
        if not ok:
            raise RuntimeError(f"创建T形截面 {no} 失败: {err}")
        self._loaded = False

    def create_Ishape(
        self,
        no: int,
        name: str,
        H: float = 0.3,
        Bt: float = 0.13,
        Bb: float = 0.13,
        Tt: float = 0.016,
        Tb: float = 0.016,
        Tw: float = 0.016,
    ) -> None:
        """创建I形截面（工字形截面）

        Args:
            no: 截面编号
            name: 截面名称
            H: 截面总高度
            Bt: 上翼缘宽度
            Bb: 下翼缘宽度
            Tt: 上翼缘厚度
            Tb: 下翼缘厚度
            Tw: 腹板厚度

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_Ishape(no, name, "ISHAPE", H, Bt, Bb, Tt, Tb, Tw)
        if not ok:
            raise RuntimeError(f"创建I形截面 {no} 失败: {err}")
        self._loaded = False

    def create_rect(
        self,
        no: int,
        name: str,
        B: float = 6.5,
        H: float = 3.2,
        TransitionType: Literal["Chamfer", "Fillet"] = "Fillet",
        SecType: Literal["Solid", "Hollow"] = "Solid",
        **kwargs,
    ) -> None:
        """创建矩形截面

        Args:
            no: 截面编号
            name: 截面名称
            B: 截面宽度
            H: 截面高度
            TransitionType: 倒角类型，Chamfer=斜倒角，Fillet=圆倒角
            SecType: 截面类型，Solid=实腹截面，Hollow=空腹截面
            **kwargs: 其他可选参数（xo1, yo1, R, t1, t2, xi1, yi1, HasDiaphragm,
                      tw, xi2, yi2, HasGroove, b1, b2, h）

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_rect(no, name, "RECT", TransitionType, SecType, B, H, **kwargs)
        if not ok:
            raise RuntimeError(f"创建矩形截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_i(
        self,
        no: int,
        name: str,
        H: float,
        Bt: float,
        Bb: float,
        Tt: float,
        Tb: float,
        Tw: float,
        WebRibPos: Literal["Left", "Right", "Both"],
    ) -> None:
        """创建工字形钢截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 梁高
            Bt: 上翼缘宽度
            Bb: 下翼缘宽度
            Tt: 上翼缘厚度
            Tb: 下翼缘厚度
            Tw: 腹板厚度
            WebRibPos: 加劲肋位置，Left=左侧，Right=右侧，Both=两侧

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_i(no, name, "STEELI", H, Bt, Bb, Tt, Tb, Tw, WebRibPos)
        if not ok:
            raise RuntimeError(f"创建工字形钢截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_box(
        self,
        no: int,
        name: str,
        H: float,
        Bt: float,
        Bct: float,
        Bb: float,
        Bcb: float,
        Tt: float,
        Tb: float,
        Tw: float,
        SameLayout: Literal[0, 1],
    ) -> None:
        """创建箱型钢截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 梁高
            Bt: 上翼缘宽度
            Bct: 上翼缘悬出宽
            Bb: 下翼缘宽度
            Bcb: 下翼缘悬出宽
            Tt: 上翼缘厚度
            Tb: 下翼缘厚度
            Tw: 腹板厚度
            SameLayout: 下翼缘加劲肋是否与上翼缘相同，1=相同，0=不同

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_box(no, name, "STEELBOX", H, Bt, Bct, Bb, Bcb, Tt, Tb, Tw, SameLayout)
        if not ok:
            raise NotImplementedError(f"OSIS暂不支持创建箱型钢截面")
            # raise RuntimeError(f"创建箱型钢截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_box_three_cell(
        self,
        no: int,
        name: str,
        H: float,
        Bt: float,
        Bb: float,
        i: float,
        a1: float,
        a2: float,
        Dt: float,
        Tt1: float,
        Tt2: float,
        Tb1: float,
        Db: float,
        Tb2: float,
        Tb3: float,
        Tw1: float,
        Dw: float,
        HasWeb: Literal[0, 1],
        Tw2: float,
        WebRibPos: Literal["Left", "Right", "Both"],
    ) -> None:
        """创建单箱单/三室钢截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 梁高
            Bt: 上翼缘宽度
            Bb: 下翼缘宽度
            i: 顶面横坡
            a1: 边腹板倾角
            a2: 斜底板倾角
            Dt: 顶点变厚点至起点距离
            Tt1: 顶板厚度1
            Tt2: 顶板厚度2
            Tb1: 底板厚度
            Db: 斜底板变厚点至起点距离
            Tb2: 斜底板厚度1
            Tb3: 斜底板厚度2
            Tw1: 边腹板厚度
            Dw: 中腹板至主梁中心线距离
            HasWeb: 是否有中腹板，1=有中腹板，0=无中腹板
            Tw2: 中腹板厚度
            WebRibPos: 加劲肋位置，Left=左侧，Right=右侧，Both=两侧

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_box_three_cell(
            no, name, "STEELBOXTHREECELL", H, Bt, Bb, i, a1, a2, Dt,
            Tt1, Tt2, Tb1, Db, Tb2, Tb3, Tw1, Dw, HasWeb, Tw2, WebRibPos
        )
        if not ok:
            raise RuntimeError(f"创建单箱单/三室钢截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_box_itf(
        self,
        no: int,
        name: str,
        H: float,
        B: float,
        Bt: float,
        Bb: float,
        i: float,
        a1: float,
        a2: float,
        Dt: float,
        Tt1: float,
        Tt2: float,
        Tt3: float,
        Tb1: float,
        Db: float,
        Tb2: float,
        Tb3: float,
        Tw1: float,
    ) -> None:
        """创建单箱单室斜顶板钢截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 梁高
            B: 梁宽
            Bt: 顶板宽度
            Bb: 平底板宽度
            i: 顶面横坡
            a1: 斜顶板倾角
            a2: 斜底板倾角
            Dt: 顶板变厚点至起点距离
            Tt1: 顶板厚度1
            Tt2: 顶板厚度2
            Tt3: 斜顶板厚度
            Tb1: 底板厚度
            Db: 斜底板变厚点至起点距离
            Tb2: 斜底板厚度1
            Tb3: 斜底板厚度2
            Tw1: 边腹板厚度

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_box_itf(
            no, name, "STEELBOXITF", H, B, Bt, Bb, i, a1, a2, Dt,
            Tt1, Tt2, Tt3, Tb1, Db, Tb2, Tb3, Tw1
        )
        if not ok:
            raise NotImplementedError (f"OSIS暂不支持创建单箱单室斜顶板截面")
            raise RuntimeError(f"创建单箱单室斜顶板截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_canti_box(
        self,
        no: int,
        name: str,
        H: float,
        Bt: float,
        Bb: float,
        i: float,
        a: float,
        Dt: float,
        Tt1: float,
        Tt2: float,
        Tb1: float,
        Tw1: float,
        HasWeb: Literal[0, 1],
        Tw2: float,
        WebRibPos: Literal["Left", "Right", "Both"],
        h: float,
        t: float,
    ) -> None:
        """创建悬臂单箱单/双室钢截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 梁高
            Bt: 顶板宽度
            Bb: 平底板宽度
            i: 顶面横坡
            a: 边腹板倾角
            Dt: 顶板变厚点至起点距离
            Tt1: 顶板厚度1
            Tt2: 顶板厚度2
            Tb1: 底板厚度
            Tw1: 边腹板厚度
            HasWeb: 是否有中腹板，1=有中腹板，0=无中腹板
            Tw2: 中腹板厚度
            WebRibPos: 加劲肋位置
            h: 悬臂端封板高
            t: 悬臂端封板厚

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_canti_box(
            no, name, "STEELCANTIBOX", H, Bt, Bb, i, a, Dt,
            Tt1, Tt2, Tb1, Tw1, HasWeb, Tw2, WebRibPos, h, t
        )
        if not ok:
            raise RuntimeError(f"创建悬臂单箱单/双室截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_canti_box_ibf(
        self,
        no: int,
        name: str,
        H: float,
        Bt: float,
        Bb: float,
        Bc: float,
        i: float,
        a: float,
        Dt: float,
        Tt1: float,
        Tt2: float,
        Tb1: float,
        Tb2: float,
        Tw1: float,
        HasWeb: Literal[0, 1],
        Tw2: float,
        WebRibPos: Literal["Left", "Right", "Both"],
        h: float,
        t: float,
    ) -> None:
        """创建悬臂单箱单/双室斜底板钢截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 梁高
            Bt: 顶板宽度
            Bb: 平底板宽度
            Bc: 悬臂长
            i: 顶面横坡
            a: 边腹板倾角
            Dt: 顶板变厚点至起点距离
            Tt1: 顶板厚度1
            Tt2: 顶板厚度2
            Tb1: 底板厚度
            Tb2: 斜底板厚度
            Tw1: 边腹板厚度
            HasWeb: 是否有中腹板，1=有中腹板，0=无中腹板
            Tw2: 中腹板厚度
            WebRibPos: 加劲肋位置
            h: 悬臂端封板高
            t: 悬臂端封板厚

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_canti_box_ibf(
            no, name, "STEELCANTIBOXIBF", H, Bt, Bb, Bc, i, a, Dt,
            Tt1, Tt2, Tb1, Tb2, Tw1, HasWeb, Tw2, WebRibPos, h, t
        )
        if not ok:
            raise RuntimeError(f"创建悬臂单箱单/双室斜底板截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_custom(
        self,
        no: int,
        name: str,
        point_matrix: str,
        line_matrix: str,
    ) -> None:
        """创建自定义钢梁截面（通过点线关系输入）

        Args:
            no: 截面编号
            name: 截面名称
            point_matrix: 几何点矩阵名称，需先用 osis_matrix 定义
            line_matrix: 几何线矩阵名称，需先用 osis_matrix 定义

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_custom(no, name, "STEELCUSTOM", point_matrix, line_matrix)
        if not ok:
            raise NotImplementedError(f"OSIS暂不支持创建自定义钢梁截面")
            # raise RuntimeError(f"创建自定义钢梁截面 {no} 失败: {err}")
        self._loaded = False

    def create_steel_custom_plate(
        self,
        no: int,
        name: str,
        plate_positions: list[str],
    ) -> None:
        """创建自定义钢梁截面（通过参数板输入）

        Args:
            no: 截面编号
            name: 截面名称
            plate_positions: 指定该截面拥有的板件列表，如 ["TopFlange", "BottomFlange", "SideWeb"]

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_steel_custom_plate(no, name, "STEELCUSTOMPLATE", plate_positions)
        if not ok:
            raise RuntimeError(f"创建自定义钢梁参数板截面 {no} 失败: {err}")
        self._loaded = False

    def create_smallbox(
        self,
        no: int,
        name: str,
        eGirderPos: Literal["LEFT", "MIDDLE", "RIGHT"] = "MIDDLE",
        H: float = 1.6,
        Bs: float = 1.65,
        Bm: float = 1.2,
        Bc: float = 0.0,
        Bb: float = 1.0,
        Tt: float = 0.18,
        Tb: float = 0.2,
        Tw: float = 0.2,
        i: float = 4.0,
        Tc: float = 0.18,
        Tc1: float = 0.25,
        x: float = 0.2,
        xi1: float = 0.15,
        Tt1: float = 0.25,
        xi2: float = 0.05,
        yi2: float = 0.05,
        bSlope: bool = False,
        i1: float = 0.0,
        i2: float = 0.0,
        R: float = 0.05,
    ) -> None:
        """创建小箱梁截面

        Args:
            no: 截面编号
            name: 截面名称
            eGirderPos: 截面位置，Left=左边梁，Middle=中梁，Right=右边梁
            H: 箱梁高度
            Bs: 边翼板宽
            Bm: 中梁半宽
            Bc: 现浇湿接缝半宽
            Bb: 底板宽
            Tt: 顶板厚
            Tb: 底板厚
            Tw: 腹板厚
            i: 腹板倾斜比
            Tc: 边梁悬臂端部厚
            Tc1: 边梁悬臂根部厚
            x: 中梁翼板倒角宽
            xi1: 倒角1宽（顶板）
            Tt1: 倒角1根部厚
            xi2: 倒角2宽（底板）
            yi2: 倒角2高
            bSlope: 是否输入横坡
            i1: 顶左坡
            i2: 顶右坡
            R: 底板倒角圆弧半径

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_smallbox(
            no, name, "SMALLBOX", eGirderPos, H, Bs, Bm, Bc, Bb,
            Tt, Tb, Tw, i, Tc, Tc1, x, xi1, Tt1, xi2, yi2, bSlope, i1, i2, R
        )
        if not ok:
            raise RuntimeError(f"创建小箱梁截面 {no} 失败: {err}")
        self._loaded = False

    def create_hollowslab(
        self,
        no: int,
        name: str,
        eGirderPos: Literal["LEFT", "MIDDLE", "RIGHT"] = "MIDDLE",
        H: float = 0.95,
        Bs: float = 1.0,
        Bm: float = 0.57,
        Bj: float = 0.05,
        Tt: float = 0.12,
        Tb: float = 0.12,
        Tw: float = 0.16,
        Tc: float = 0.12,
        Tc1: float = 0.16,
        Bc: float = 0.38,
        xi1: float = 0.15,
        yi1: float = 0.08,
        xi2: float = 0.12,
        yi2: float = 0.08,
        xo3: float = 0.05,
        yo3: float = 0.05,
        xo4: float = 0.08,
        yo4: float = 0.08,
        h1: float = 0.12,
    ) -> None:
        """创建空心板截面

        Args:
            no: 截面编号
            name: 截面名称
            eGirderPos: 截面位置，Left=左边梁，Middle=中梁，Right=右边梁
            H: 板高
            Bs: 边板宽
            Bm: 中梁半宽
            Bj: 铰缝上端缩进宽
            Tt: 顶板厚
            Tb: 底板厚
            Tw: 腹板下端厚
            Tc: 边板悬臂端部厚
            Tc1: 边板悬臂根部厚
            Bc: 边板悬臂厚
            xi1: 倒角1宽（顶板）
            yi1: 倒角1高
            xi2: 倒角2宽（底板）
            yi2: 倒角2高
            xo3: 倒角3宽（上端）
            yo3: 倒角3高
            xo4: 倒角4宽（下端）
            yo4: 倒角4高
            h1: 下端竖直段高

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_hollowslab(
            no, name, "HOLLOWSLAB", eGirderPos, H, Bs, Bm, Bj,
            Tt, Tb, Tw, Tc, Tc1, Bc, xi1, yi1, xi2, yi2,
            xo3, yo3, xo4, yo4, h1
        )
        if not ok:
            raise RuntimeError(f"创建空心板截面 {no} 失败: {err}")
        self._loaded = False

    def create_rounded_end(
        self,
        no: int,
        name: str,
        eFillingType: Literal["Solid", "Hollow"] = "Solid",
        B: float = 7.0,
        H: float = 3.0,
        R: float = 2.0,
        bHasDiaphragm: bool = False,
        b: float = 4.0,
        t: float = 1.0,
        xi1: float = 0.5,
        yi1: float = 0.25,
        tw: float = 1.0,
        xi2: float = 0.5,
        yi2: float = 0.25,
    ) -> None:
        """创建圆端形截面

        Args:
            no: 截面编号
            name: 截面名称
            eFillingType: 填充类型，Solid=实腹，Hollow=空腹
            B: 截面宽
            H: 截面高
            R: 圆弧半径
            bHasDiaphragm: 是否有隔板
            b: 内宽
            t: 壁厚
            xi1: 内倒角宽
            yi1: 内倒角高
            tw: 隔板厚
            xi2: 隔板倒角宽
            yi2: 隔板倒角高

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_rounded_end(
            no, name, "ROUNDEDEND", eFillingType, B, H, R,
            bHasDiaphragm, b, t, xi1, yi1, tw, xi2, yi2
        )
        if not ok:
            raise RuntimeError(f"创建圆端形截面 {no} 失败: {err}")
        self._loaded = False

    def create_conventionalbox(
        self,
        no: int,
        name: str,
        H: float = 2.7,
        BtL: float = 6.375,
        BtR: float = 6.375,
        BbL: float = 3.5,
        BbR: float = 3.5,
        Bs: float = 0.5,
        Tt: float = 0.28,
        Tb: float = 0.32,
        Tw1: float = 0.5,
        Tw2: float = 0.5,
        nCellNum: int = 1,
        Bi1: float = 5.05,
        Bi2: float = 4.5,
        Bi3: float = 5.05,
        Bi4: float = 5.05,
        xi1: float = 1.5,
        Tt1: float = 0.7,
        xi2: float = 0.0,
        Tt2: float = 0.0,
        xi3: float = 1.0,
        yi3: float = 0.5,
        xi4: float = 0.5,
        Tt4: float = 0.35,
        xi5: float = 0.6,
        yi5: float = 0.3,
        xi6: float = 1.0,
        Tt6: float = 0.5,
        xi7: float = 0.6,
        yi7: float = 0.3,
        BcL: float = 2.875,
        TcL: float = 0.2,
        Bc1L: float = 1.325,
        Tc1L: float = 0.7,
        Tc2L: float = 0.4,
        bSymmetry: bool = True,
        BcR: float = 2.875,
        TcR: float = 0.2,
        Bc1R: float = 1.325,
        Tc1R: float = 0.7,
        Tc2R: float = 0.4,
        eSlopeType: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
        i3: float = 0.0,
        i4: float = 0.0,
        R1: float = 0.0,
        R2: float = 0.0,
    ) -> None:
        """创建常规箱梁截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 截面高度
            BtL: 设计线左顶板宽
            BtR: 设计线右顶板宽
            BbL: 设计线左底板宽
            BbR: 设计线右底板宽
            Bs: 悬臂根部至边腹板顶内侧宽度
            Tt: 顶板厚
            Tb: 底板厚
            Tw1: 边腹板厚
            Tw2: 中腹板厚
            nCellNum: 箱室个数
            Bi1~Bi4: 箱室1~4宽度
            xi1~yi7: 各种倒角参数
            BcL/TcL等: 左悬臂参数
            bSymmetry: 右侧是否对称
            BcR/TcR等: 右悬臂参数
            eSlopeType: 横坡类型
            i/i1~i4: 横坡参数
            R1/R2: 倒角圆弧半径

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_conventionalbox(
            no, name, "CONVENTIONALBOX", H, BtL, BtR, BbL, BbR, Bs,
            Tt, Tb, Tw1, Tw2, nCellNum, Bi1, Bi2, Bi3, Bi4,
            xi1, Tt1, xi2, Tt2, xi3, yi3, xi4, Tt4, xi5, yi5, xi6, Tt6, xi7, yi7,
            BcL, TcL, Bc1L, Tc1L, Tc2L, bSymmetry, BcR, TcR, Bc1R, Tc1R, Tc2R,
            eSlopeType, i, i1, i2, i3, i4, R1, R2
        )
        if not ok:
            raise NotImplementedError(
                f"OSIS 暂不支持创建常规箱梁截面"
            )
            # raise RuntimeError(f"创建常规箱梁截面 {no} 失败: {err}")
        self._loaded = False

    def create_flat_box(
        self,
        no: int,
        name: str,
        H: float = 4.0,
        BtL: float = 20.0,
        BtR: float = 20.0,
        BbL: float = 10.5,
        BbR: float = 10.5,
        Bs: float = 0.8,
        Tt: float = 0.28,
        Tb1: float = 0.27,
        Tb2: float = 0.27,
        Tw: float = 0.25,
        Ttj: float = 0.5,
        Tbj: float = 0.27,
        Twj: float = 0.4,
        nCellNum: int = 5,
        Bi1: float = 4.7,
        Bi2: float = 6.85,
        Bi3: float = 6.0,
        Bi4: float = 6.85,
        xi1: float = 0.6,
        Tt1: float = 0.6,
        xi2: float = 1.0,
        Tt2: float = 0.7,
        xi3: float = 0.2,
        yi3: float = 0.2,
        xi4: float = 1.0,
        Tt4: float = 0.7,
        xi5: float = 0.6,
        yi5: float = 0.3,
        xi6: float = 0.5,
        Tt6: float = 0.7,
        xi7: float = 0.5,
        yi7: float = 0.3,
        BcL: float = 4.0,
        TcL: float = 0.2,
        Bc1L: float = 0.5,
        Tc1L: float = 0.7,
        Tc2L: float = 0.4,
        bSymmetry: bool = True,
        BcR: float = 4.0,
        TcR: float = 0.2,
        Bc1R: float = 0.5,
        Tc1R: float = 0.7,
        Tc2R: float = 0.4,
        eSlopeType: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
        i3: float = 0.0,
        i4: float = 0.0,
        R1: float = 0.5,
        R2: float = 0.2,
    ) -> None:
        """创建扁平箱梁截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 截面高度
            BtL: 设计线左顶板宽
            BtR: 设计线右顶板宽
            BbL: 设计线左底板宽
            BbR: 设计线右底板宽
            Bs: 悬臂根部至边腹板顶内侧宽度
            Tt: 顶板厚
            Tb1: 底板厚
            Tb2: 斜底板厚
            Tw: 腹板厚
            Ttj: 加强室顶板厚
            Tbj: 加强室底板厚
            Twj: 加强室腹板厚
            nCellNum: 箱室个数
            Bi1~Bi4: 箱室1~4宽度
            xi1~yi7: 各种倒角参数
            BcL/TcL等: 左悬臂参数
            bSymmetry: 右侧是否对称
            BcR/TcR等: 右悬臂参数
            eSlopeType: 横坡类型
            i/i1~i4: 横坡参数
            R1/R2: 倒角圆弧半径

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_flat_box(
            no, name, "FLATBOX", H, BtL, BtR, BbL, BbR, Bs,
            Tt, Tb1, Tb2, Tw, Ttj, Tbj, Twj, nCellNum, Bi1, Bi2, Bi3, Bi4,
            xi1, Tt1, xi2, Tt2, xi3, yi3, xi4, Tt4, xi5, yi5, xi6, Tt6, xi7, yi7,
            BcL, TcL, Bc1L, Tc1L, Tc2L, bSymmetry, BcR, TcR, Bc1R, Tc1R, Tc2R,
            eSlopeType, i, i1, i2, i3, i4, R1, R2
        )
        if not ok:
            raise NotImplementedError (f"OSIS 暂不支持创建扁平箱梁截面")
            # raise RuntimeError(f"创建扁平箱梁截面 {no} 失败: {err}")
        self._loaded = False

    def create_double_side_box(
        self,
        no: int,
        name: str,
        H: float = 3.8,
        Bt: float = 36.0,
        bt: float = 14.8,
        Bs: float = 2.1,
        Bb: float = 4.4,
        tt: float = 0.3,
        Tb1: float = 0.3,
        Tb2: float = 0.3,
        Tw: float = 0.5,
        b: float = 1.0,
        n: float = 1.0,
        Bi: float = 8.0,
        xi1: float = 1.0,
        Tt1: float = 0.6,
        xi2: float = 1.0,
        Tt2: float = 0.7,
        xi3: float = 0.6,
        yi3: float = 0.3,
        xo4: float = 1.0,
        Tt4: float = 0.7,
        b1: float = 0.3,
        eSlopeType: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
    ) -> None:
        """创建双边箱截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 梁高
            Bt: 顶板顶宽
            bt: 顶板底宽
            Bs: 边箱实心段顶板宽
            Bb: 底板宽
            tt: 顶板厚
            Tb1: 底板厚
            Tb2: 斜底板厚
            Tw: 腹板厚
            b: 风嘴上部水平宽度
            n: 风嘴上部竖向高度
            Bi: 室内宽
            xi1~Tt4: 倒角参数
            b1: 腹板内侧倒角宽
            eSlopeType: 横坡类型
            i/i1/i2: 横坡参数

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_double_side_box(
            no, name, "DOUBLESIDEBOX", H, Bt, bt, Bs, Bb,
            tt, Tb1, Tb2, Tw, b, n, Bi, xi1, Tt1, xi2, Tt2,
            xi3, yi3, xo4, Tt4, b1, eSlopeType, i, i1, i2
        )
        if not ok:
            raise NotImplementedError (f"OSIS暂不支持创建双边箱截面")
            # raise RuntimeError(f"创建双边箱截面 {no} 失败: {err}")
        self._loaded = False

    def create_ribbed_slab(
        self,
        no: int,
        name: str,
        H: float = 2.8,
        Bt: float = 21.5,
        bt: float = 17.7,
        Tt: float = 0.3,
        b: float = 0.2,
        h: float = 1.25,
        b1: float = 1.8,
        b2: float = 0.2,
        x: float = 1.5,
        y: float = 0.3,
        eSlopeType: Literal["Integral", "CastInPlace"] = "Integral",
        i: float = 0.0,
        i1: float = 0.0,
        i2: float = 0.0,
    ) -> None:
        """创建肋板式截面

        Args:
            no: 截面编号
            name: 截面名称
            H: 截面高度
            Bt: 顶板顶宽
            bt: 顶板底宽
            Tt: 顶板厚
            b: 风嘴上部水平宽度
            h: 风嘴上部竖向宽度
            b1: 边肋底宽
            b2: 边肋内侧倒角宽
            x: 顶板倒角宽
            y: 顶板倒角高
            eSlopeType: 横坡类型
            i: 整体转梁横坡
            i1: 顶左坡
            i2: 顶右坡

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_ribbed_slab(
            no, name, "RIBBEDSLAB", H, Bt, bt, Tt, b, h, b1, b2, x, y, eSlopeType, i, i1, i2
        )
        if not ok:
            raise NotImplementedError(f"OSIS暂不支持创建肋板式截面")
            raise RuntimeError(f"创建肋板式截面 {no} 失败: {err}")
        self._loaded = False

    def create_TGirder(
        self,
        no: int,
        name: str,
        eGirderPos: Literal["Left", "Middle", "Right"] = "Middle",
        H: float = 2.5,
        Bs: float = 1.125,
        Bm: float = 0.85,
        Bc: float = 0.0,
        Tt1: float = 0.16,
        Tt2: float = 0.25,
        x: float = 0.6,
        Tw: float = 0.2,
        Bh: float = 0.6,
        Hh: float = 0.35,
        yh: float = 0.25,
        bSlope: bool = False,
        i1: float = 0.0,
        i2: float = 0.0,
        R: float = 0.05,
    ) -> None:
        """创建T梁截面

        Args:
            no: 截面编号
            name: 截面名称
            eGirderPos: 截面位置，Left=左边梁，Middle=中梁，Right=右边梁
            H: 梁高
            Bs: 边翼板宽
            Bm: 中梁半宽
            Bc: 现浇湿接缝半宽
            Tt1: 翼板厚
            Tt2: 翼板根部厚
            x: 翼板倒角宽
            Tw: 腹板厚度
            Bh: 马蹄宽度
            Hh: 马蹄高度
            yh: 马蹄倒角高
            bSlope: 指定是否输入横坡
            i1: 顶左坡
            i2: 顶右坡
            R: 顶板处倒角半径

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_TGirder(
            no, name, "TGIRDER", eGirderPos, H, Bs, Bm, Bc,
            Tt1, Tt2, x, Tw, Bh, Hh, yh, bSlope, i1, i2, R
        )
        if not ok:
            raise RuntimeError(f"创建T梁截面 {no} 失败: {err}")
        self._loaded = False

    def create_custom(
        self,
        no: int,
        name: str,
        contour_matrix: str,
    ) -> None:
        """创建自定义截面

        Args:
            no: 截面编号
            name: 截面名称
            contour_matrix: 轮廓点矩阵名称，需先用 osis_matrix 定义
                矩阵格式：n*3矩阵，第一列为点所在的轮廓线编号，
                第二列为点的x坐标，第三列为点的y坐标

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_section_custom(no, name, "CUSTOM", contour_matrix)
        if not ok:
            raise NotImplementedError(f"OSIS暂不支持创建自定义截面")
            # raise RuntimeError(f"创建自定义截面 {no} 失败: {err}")
        self._loaded = False

    def delete(self, no: int) -> None:
        """删除截面

        Args:
            no: 截面编号

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_section_del(no)
        if not ok:
            raise RuntimeError(f"删除截面 {no} 失败: {err}")
        self._loaded = False

    def renumber(self, old_no: int, new_no: int) -> None:
        """修改截面编号

        Args:
            old_no: 旧编号
            new_no: 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        """
        ok, err = osis_section_mod(old_no, new_no)
        if not ok:
            raise RuntimeError(f"修改截面编号 {old_no} -> {new_no} 失败: {err}")
        self._loaded = False

    # ── 查询 ──────────────────────────────────

    def get(self, no: int | list[int]) -> Section | list[Section | None]:
        """根据编号获取单个或多个截面 (O(k))

        Args:
            no: 截面编号

        Returns:
            Section 对象或数组；截面不存在返回 None
        """
        self._load()
        if isinstance(no, int):
            return self._sec_map.get(no)
        elif isinstance(no, list):
            return [self._sec_map.get(n) for n in no]
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")

    def all(self) -> list[Section]:
        """获取所有截面

        Returns:
            全部截面列表
        """
        self._load()
        return list(self._sections)

    def count(self) -> int:
        """获取截面总数

        Returns:
            截面数量
        """
        self._load()
        return len(self._sections)

    def __repr__(self) -> str:
        self._load()
        return f"SectionManager(count={len(self._sections)})"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

section_manager = SectionManager()
