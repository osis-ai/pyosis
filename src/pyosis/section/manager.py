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
            raise RuntimeError(f"创建箱型钢截面 {no} 失败: {err}")
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
