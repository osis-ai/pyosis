"""后处理管理器 - 统一管理荷载组合、规范验算和结果显示

设计理念：
- 隐藏 HTTP 接口细节，提供原生 Python 风格 API
- 无状态设计，操作直接提交到 OSIS
- 按功能分为：荷载组合、规范验算、结果显示三个子模块
"""

from __future__ import annotations

from typing import Literal

from ..core import osis_run

from .combine import (
    osis_combine_create,
    osis_combine_post,
    osis_combine_solve,
    osis_combine_del,
)
from .design_check import (
    osis_code,
    osis_cd_ele_sel,
    osis_cd_ele_act,
    osis_cd_dl,
    osis_cd_pc,
    osis_cd_prs_ratio,
    osis_cd_csc_ratio,
    osis_cd_e,
    osis_cd_crack,
    osis_cd_auto_c2,
    osis_cd_crack_weld,
    osis_cd_geo_lco,
    osis_cd_check,
    osis_check_add,
    osis_check_solve,
    osis_check_del,
)
from .display import (
    osis_prn_eig,
    osis_pl_eig,
)


class PostManager:
    """后处理管理器

    统一管理荷载组合、规范验算和结果显示。

    用法:
        >>> from pyosis.post import post_manager
        >>> # 荷载组合
        >>> post_manager.create_combine("基本组合", "LC", "Concrete", "Basic", "OR")
        >>> post_manager.add_to_combine("基本组合", "自重工况", 1.2)
        >>> post_manager.solve_combines()
        >>> # 规范验算
        >>> post_manager.set_code("JTG18")
        >>> post_manager.select_elements("All")
        >>> post_manager.set_member_type("RC")
        >>> post_manager.add_check("UltM", "基本组合")
        >>> post_manager.solve_checks()
        >>> # 结果显示
        >>> post_manager.display_eigenvalue("Modal1")
        >>> post_manager.display_eigenvector("Modal1", 1, "MdXYZ")
    """

    # ═══════════════════════════════════════════
    # 荷载组合
    # ═══════════════════════════════════════════

    def create_combine(
        self,
        name: str,
        lc_or_env: Literal["LC", "Env"],
        sheet_type: Literal["General", "Concrete", "Steel", "Composite"],
        activate_type: Literal[
            "Activate", "Inactivate", "Basic", "Accidental", "Seismic",
            "Frequent", "Quasipermanent", "Standard",
            "Concreted1", "Concreted2", "ConcretePre1", "ConcretePre2",
            "SteelD", "SteelPre", "CompositeD", "CompositePre",
        ],
        operation_type: Literal["ADD", "OR", "ABS", "SRSS", "AND"],
        prompt: str | None = None,
    ) -> None:
        """创建荷载组合（声明荷载组合）

        Args:
            name: 包络名称
            lc_or_env: 工况或包络
                * LC — 工况
                * Env — 包络
            sheet_type: 表单类型
                * General — 一般
                * Concrete — 混凝土
                * Steel — 钢结构
                * Composite — 组合结构
            activate_type: 激活类型，如 Basic、Accidental、Seismic、Frequent 等
            operation_type: 操作类型
                * ADD — 相加
                * OR — 包络
                * ABS — 绝对值
                * SRSS — 平方之和开方
                * AND — 相加（最不利），仅允许包络
            prompt: 说明，可缺省

        Raises:
            RuntimeError: 创建失败时抛出异常
        """
        ok, err = osis_combine_create(name, lc_or_env, sheet_type, activate_type, operation_type, prompt)
        if not ok:
            raise RuntimeError(f"创建荷载组合 {name} 失败: {err}")

    def add_to_combine(
        self,
        combine_name: str,
        add_name: str,
        factor: float = 1.0,
    ) -> None:
        """往荷载组合中添加工况或包络

        Args:
            combine_name: 荷载组合名称
            add_name: 要加入的工况或包络名称
            factor: 系数，默认 1.0

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_combine_post("Combine", combine_name, add_name, factor)
        if not ok:
            raise RuntimeError(f"往组合 {combine_name} 添加 {add_name} 失败: {err}")

    def solve_combines(self) -> None:
        """计算组合和包络

        Raises:
            RuntimeError: 计算失败时抛出异常
        """
        ok, err = osis_combine_solve()
        if not ok:
            raise RuntimeError(f"计算荷载组合失败: {err}")

    def delete_combines(
        self,
        param: Literal["All", "General", "Concrete", "Steel", "Composite"] | str = "All",
    ) -> None:
        """删除荷载组合

        Args:
            param: 删除范围或目标名称
                * All — 删除全部
                * General / Concrete / Steel / Composite — 删除对应表单下全部
                * 亦可填指定荷载组合名称

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_combine_del(param)
        if not ok:
            raise RuntimeError(f"删除荷载组合 ({param}) 失败: {err}")

    # ═══════════════════════════════════════════
    # 规范验算 — 全局设置
    # ═══════════════════════════════════════════

    def set_code(
        self,
        code: Literal["JTG", "JTG18", "JTGD64"] = "JTG18",
    ) -> None:
        """设置验算规范

        Args:
            code: 规范代号
                * JTG — JTG 3362-2018
                * JTG18 — JTG 3362-2018（默认）
                * JTGD64 — JTG D64-2015

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_code(code)
        if not ok:
            raise RuntimeError(f"设置验算规范 {code} 失败: {err}")

    # ═══════════════════════════════════════════
    # 规范验算 — 单元选择与激活
    # ═══════════════════════════════════════════

    def select_elements(
        self,
        op: Literal["All", "None", "Inve", "S", "A", "U", "R"],
        *paras: str | int,
    ) -> None:
        """后处理选择单元

        Args:
            op: 操作
                * All — 全选
                * None — 全不选
                * Inve — 反选
                * S — 替换
                * A — 添加
                * U — 删除
                * R — 再选择
            *paras: 待操作的单元编号，支持 8to10 等形式；All、None、Inve 时可缺省

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_cd_ele_sel(op, *paras)
        if not ok:
            raise RuntimeError(f"后处理选择单元失败: {err}")

    def activate_elements(
        self,
        op: Literal["All", "Inve", "S", "A", "U", "R"],
        *paras: str | int,
    ) -> None:
        """后处理激活单元

        Args:
            op: 操作
                * All — 全激活
                * Inve — 反选
                * S — 替换
                * A — 添加
                * U — 删除
                * R — 再激活
            *paras: 待操作的单元编号，支持 8to10 等形式；All、Inve 时可缺省

        Raises:
            RuntimeError: 操作失败时抛出异常
        """
        ok, err = osis_cd_ele_act(op, *paras)
        if not ok:
            raise RuntimeError(f"后处理激活单元失败: {err}")

    # ═══════════════════════════════════════════
    # 规范验算 — 设计参数
    # ═══════════════════════════════════════════

    def set_design_level(
        self,
        level: Literal[1, 2, 3] = 1,
    ) -> None:
        """设置设计安全等级（需先选中单元）

        Args:
            level: 等级，1=一级、2=二级、3=三级

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_dl(level)
        if not ok:
            raise RuntimeError(f"设置设计安全等级 {level} 失败: {err}")

    def set_member_type(
        self,
        member_type: Literal["EPC", "APC", "BPC", "RC", "PierCap"] | None = None,
        construct_type: Literal["Pre", "Cast"] | None = None,
        tension_type: Literal["Pre", "Post"] | None = None,
    ) -> None:
        """设置构件类型、PC 构件施工方式及张拉方式（需先选中单元）

        Args:
            member_type: 构件类型
                * EPC — 全预应力
                * APC — A 类预应力
                * BPC — B 类预应力
                * RC — 钢筋混凝土
                * PierCap — 盖梁
            construct_type: 施工方式，Pre=预制，Cast=现浇；RC、PierCap 无需填写
            tension_type: 张拉方式，Pre=先张，Post=后张；RC、PierCap 无需填写

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_pc(member_type, construct_type, tension_type)
        if not ok:
            raise RuntimeError(f"设置构件类型失败: {err}")

    def set_prs_ratio(self, ratio: float = 1.0) -> None:
        """设置基于截面底缘起算多少倍 h 范围内预应力弯起钢筋参与抗剪验算（需先选中单元）

        Args:
            ratio: 倍数，取值范围 [0.0, 1.0]；默认 1.0

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_prs_ratio(ratio)
        if not ok:
            raise RuntimeError(f"设置预应力弯起钢筋参与抗剪验算比例失败: {err}")

    def set_csc_ratio(self, ratio: float = 0.8) -> None:
        """设置施工阶段混凝土强度折减系数（需先选中单元）

        Args:
            ratio: 折减系数，取值范围 [0.8, 1.0]；默认 0.8

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_csc_ratio(ratio)
        if not ok:
            raise RuntimeError(f"设置施工阶段混凝土强度折减系数失败: {err}")

    def set_environment(
        self,
        env_type: Literal[1, 2, 3, 4, 5, 6, 7] | None = None,
        grade: Literal["A", "B", "C", "D", "E", "E/F", "D/E/F"] | None = None,
    ) -> None:
        """设置环境类别和环境等级（需先选中单元）

        Args:
            env_type: 环境类别
                * 1 — 一般环境
                * 2 — 冻融环境
                * 3 — 海洋氯化物环境
                * 4 — 其他氯化物环境
                * 5 — 盐结晶环境
                * 6 — 化学腐蚀环境
                * 7 — 磨蚀环境
            grade: 环境等级，如 A、B、C、D、E、E/F、D/E/F 等

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_e(env_type, grade)
        if not ok:
            raise RuntimeError(f"设置环境类别和等级失败: {err}")

    def set_crack_params(
        self,
        c1: float | str | None = None,
        c2: float | str | None = None,
        c3: float | str | None = None,
        cover: float | str | None = None,
    ) -> None:
        """设置裂缝计算参数（需先选中单元）

        Args:
            c1: 参数 C1，须大于 0；默认 1.0
            c2: 参数 C2，须大于 0；默认 1.5
            c3: 参数 C3，须大于 0；默认 1.0
            cover: 混凝土保护层厚度，须 ≥ 0；默认 0.0

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_crack(c1, c2, c3, cover)
        if not ok:
            raise RuntimeError(f"设置裂缝计算参数失败: {err}")

    def auto_c2(self, para: Literal["My", "Mz", "Nx"]) -> None:
        """自动计算裂缝参数 C2（长期效应影响系数）（需先选中单元）

        Args:
            para: 只能为 My、Mz、Nx

        Raises:
            RuntimeError: 计算失败时抛出异常
        """
        ok, err = osis_cd_auto_c2(para)
        if not ok:
            raise RuntimeError(f"自动计算裂缝参数 C2 失败: {err}")

    def set_weld_skeleton(
        self,
        n_para: Literal[0, 1],
        factor: float = 1.3,
    ) -> None:
        """设置焊接钢筋骨架系数（需先选中单元）

        Args:
            n_para: 0 — 无焊接钢筋骨架（默认）；1 — 有焊接钢筋骨架
            factor: 焊接钢筋骨架系数，须大于 0；默认 1.3，仅在 n_para 为 1 时生效

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_crack_weld(n_para, factor)
        if not ok:
            raise RuntimeError(f"设置焊接钢筋骨架系数失败: {err}")

    def set_geo_length(
        self,
        ly: float,
        ky: float,
        lz: float,
        kz: float,
    ) -> None:
        """设置构件几何长度及计算长度系数（需先选中单元）

        Args:
            ly: 方向 y 几何长度，须大于 0；默认取单元长度
            ky: 方向 y 计算长度系数，须大于 0；默认 1.0
            lz: 方向 z 几何长度，须大于 0；默认取单元长度
            kz: 方向 z 计算长度系数，须大于 0；默认 1.0

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_geo_lco(ly, ky, lz, kz)
        if not ok:
            raise RuntimeError(f"设置构件几何长度及计算长度系数失败: {err}")

    def set_check_items(
        self,
        param: Literal["All", "None"] | str,
    ) -> None:
        """设置验算项开关（需先选中单元）

        Args:
            param:
                * All / all — 全部打开
                * None / none — 全部关闭
                * 亦可为 JSON 字符串，例如 '[{"UltM":1,"Shear":1}]'，其中 0 表示关闭、1 表示打开

        Raises:
            RuntimeError: 设置失败时抛出异常
        """
        ok, err = osis_cd_check(param)
        if not ok:
            raise RuntimeError(f"设置验算项开关失败: {err}")

    # ═══════════════════════════════════════════
    # 规范验算 — 验算作用
    # ═══════════════════════════════════════════

    def add_check(
        self,
        item: Literal[
            "UltM", "UltN", "Shear", "CrackS", "CrackL", "CrackWeb", "CrackWidth",
            "SSNC", "SSPC", "CSNC", "CSNT",
        ],
        combine_name: str,
    ) -> None:
        """添加验算作用

        Args:
            item: 验算项代号
                * UltM — 抗弯承载力
                * UltN — 轴压承载力
                * Shear — 抗剪承载力
                * CrackS — 短期裂缝
                * CrackL — 长期裂缝
                * CrackWeb — 腹板裂缝
                * CrackWidth — 裂缝宽度
                * SSNC — 施工阶段正截面
                * SSPC — 施工阶段斜截面
                * CSNC — 使用阶段正截面
                * CSNT — 使用阶段斜截面
            combine_name: 荷载组合名称（可为工况或包络）

        Raises:
            RuntimeError: 添加失败时抛出异常
        """
        ok, err = osis_check_add(item, combine_name)
        if not ok:
            raise RuntimeError(f"添加验算作用 {item} ({combine_name}) 失败: {err}")

    def solve_checks(self) -> None:
        """计算验算作用

        Raises:
            RuntimeError: 计算失败时抛出异常
        """
        ok, err = osis_check_solve()
        if not ok:
            raise RuntimeError(f"计算验算失败: {err}")

    def delete_checks(
        self,
        item: Literal[
            "UltM", "UltN", "Shear", "CrackS", "CrackL", "CrackWeb", "CrackWidth",
            "SSNC", "SSPC", "CSNC", "CSNT",
        ]
        | Literal["All", "all"]
        | str = "All",
        combine_name: str | None = None,
    ) -> None:
        """删除验算作用

        Args:
            item:
                * All / all — 删除所有验算
                * 具体验算项代号同 add_check
                * 传空字符串 "" 表示删除该 combine_name 下的全部验算作用
            combine_name: 荷载组合名称；item 为 All / all 时通常可省略

        Raises:
            RuntimeError: 删除失败时抛出异常
        """
        ok, err = osis_check_del(item, combine_name)
        if not ok:
            raise RuntimeError(f"删除验算作用 ({item}) 失败: {err}")

    # ═══════════════════════════════════════════
    # 快捷功能
    # ═══════════════════════════════════════════

    def combination_and_check(self):
        '''
        自动组合与验算
        '''
        ok, err = osis_run("CombinationAndCheck")
        if not ok:
            raise RuntimeError(f"自动组合与验算失败: {err}")
        
    # ═══════════════════════════════════════════
    # 结果显示
    # ═══════════════════════════════════════════

    def display_eigenvalue(
        self,
        name: str,
        index: int = 0,
    ) -> None:
        """显示自振模态 / 屈曲模态的特征值

        Args:
            name: 自振模态 / 屈曲模态工况名
            index: 表格编号
                * 自振模态：0, 1, 2
                * 屈曲模态：0

        Raises:
            RuntimeError: 显示失败时抛出异常
        """
        ok, err = osis_prn_eig(name, index)
        if not ok:
            raise RuntimeError(f"显示特征值 {name} 失败: {err}")

    def display_eigenvector(
        self,
        name: str,
        eigen_index: int = 1,
        comp: Literal["MdX", "MdY", "MdZ", "MdXY", "MdYZ", "MdXZ", "MdXYZ"] = "MdXYZ",
    ) -> None:
        """显示模态结果的特征向量

        Args:
            name: 模态工况名
            eigen_index: 模态阶数，1/2/.../n
            comp: 模态成分
                * MdX = X方向
                * MdY = Y方向
                * MdZ = Z方向
                * MdXY = XY平面
                * MdYZ = YZ平面
                * MdXZ = XZ平面
                * MdXYZ = 三维（默认）

        Raises:
            RuntimeError: 显示失败时抛出异常
        """
        ok, err = osis_pl_eig(name, eigen_index, comp)
        if not ok:
            raise RuntimeError(f"显示特征向量 {name} (第{eigen_index}阶) 失败: {err}")

    def __repr__(self) -> str:
        return "PostManager()"


# ═════════════════════════════════════════════
# 全局单例
# ═════════════════════════════════════════════

post_manager = PostManager()
