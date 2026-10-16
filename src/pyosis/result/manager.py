"""结果管理器

结果只有一条取数路径:PySolver 的 HTTP 路由（见 routes.py），有头/无头模式共用。
每个物理结果类型对应一个语义方法,返回 pandas DataFrame。

规范验算尚无路由,是唯一还走 /output 命令流的部分（见 check.py）。
"""
from __future__ import annotations

from typing import Literal

import pandas as pd

from . import routes
# 隔离区:验算待 HTTP 路由补齐后连同 check.py 一并删除
from .check import osis_check_result


class ResultManager:
    """结果管理器

    统一管理荷载工况结果、包络结果、规范验算结果的导出。
    所有方法返回 pandas DataFrame，便于后续数据分析和可视化。
    """

    # ═══════════════════════════════════════════
    # 结果查询（HTTP 路由，唯一数据源）
    # ═══════════════════════════════════════════

    def node_displacement(
        self,
        name: str | list[str] | None = None,
        strict: bool = False,
    ) -> pd.DataFrame:
        """查询求解后节点位移

        走 /GetAllNodeDisplacement、/GetNodeDisplacementByNames 端点，
        优先从结果文件读，文件失败回落内存。

        Args:
            name: 工况名（str 或 list[str]）；None 时返回全部工况。
                包络/并发名需服务端支持后才能解析，目前传入只会得到空表。
            strict: 显式指定 name 却一行都没查到时报错（默认只告警）。
                名字写错与「包络名但服务端尚未支持」目前无法区分，都会是空结果。

        Returns:
            结果 DataFrame（列: loadCase, source, no, ux, uy, uz, rx, ry, rz, rw）

        Raises:
            RuntimeError: 查询失败，或 strict=True 时名字查不到
        """
        return routes.node_displacement_df(name, strict)

    def element_force(
        self,
        name: str | list[str] | None = None,
        strict: bool = False,
    ) -> pd.DataFrame:
        """查询求解后单元内力

        走 /GetAllElementForce、/GetElementForceByNames 端点，
        优先从结果文件读，文件失败回落内存。

        Args:
            name: 工况名（str 或 list[str]）；None 时返回全部工况。
                包络/并发名需服务端支持后才能解析，目前传入只会得到空表。
            strict: 显式指定 name 却一行都没查到时报错（默认只告警）

        Returns:
            结果 DataFrame（列: loadCase, source, ele, node, fx, fy, fz, mx, my, mz, mw）

        Raises:
            RuntimeError: 查询失败，或 strict=True 时名字查不到
        """
        return routes.element_force_df(name, strict)

    def element_stress(
        self,
        name: str | list[str] | None = None,
        by_part: bool = False,
        strict: bool = False,
    ) -> pd.DataFrame:
        """查询求解后单元应力

        走 /GetAllElementStress、/GetElementStressByNames 端点，
        优先从结果文件读，文件失败回落内存。

        Args:
            name: 工况名（str 或 list[str]）；None 时返回全部工况。
                包络/并发名需服务端支持后才能解析，目前传入只会得到空表。
            by_part: False（默认）展平全截面 points；True 展平按截面分块的
                parts 并额外带 part 列
            strict: 显式指定 name 却一行都没查到时报错（默认只告警）

        Returns:
            结果 DataFrame（列: loadCase, source, [part,] ele, node, position,
            point, sxFx, sxMy, sxMz, sxComp, syFy, szFz, tp, cp）

        Raises:
            RuntimeError: 查询失败，或 strict=True 时名字查不到
        """
        return routes.element_stress_df(name, by_part=by_part, strict=strict)

    def support_reaction(
        self,
        name: str | list[str] | None = None,
        strict: bool = False,
    ) -> pd.DataFrame:
        """查询求解后支座反力

        走 /GetAllSupportReaction、/GetSupportReactionByNames 端点，
        优先从结果文件读，文件失败回落内存。

        Args:
            name: 工况名（str 或 list[str]）；None 时返回全部工况。
                包络/并发名需服务端支持后才能解析，目前传入只会得到空表。
            strict: 显式指定 name 却一行都没查到时报错（默认只告警）

        Returns:
            结果 DataFrame（列: loadCase, source, no, sys, fx, fy, fz, mx, my, mz, mw）

        Raises:
            RuntimeError: 查询失败，或 strict=True 时名字查不到
        """
        return routes.support_reaction_df(name, strict)

    def tendon_loss(
        self,
        name: str | list[str] | None = None,
        strict: bool = False,
    ) -> pd.DataFrame:
        """查询求解后钢束（预应力）损失

        走 /GetAllTendonLoss、/GetTendonLossByNames 端点，
        优先从结果文件读，文件失败回落内存。

        Args:
            name: 工况名（str 或 list[str]）；None 时返回全部工况
            strict: 显式指定 name 却一行都没查到时报错（默认只告警）

        Returns:
            结果 DataFrame（列: loadCase, source, tendon, tendonName, ele,
            position, coord, effP, lostFriction, lostAnchorage, lostThermal,
            lostElastic, lostRelax, lostCreepShrink, lostTotal）

        Raises:
            RuntimeError: 查询失败，或 strict=True 时名字查不到
        """
        return routes.tendon_loss_df(name, strict)

    def modal(
        self,
        name: str | list[str] | None = None,
        strict: bool = False,
    ) -> pd.DataFrame:
        """查询模态结果（特征值、周期、频率）

        走 /GetAllModal、/GetModalByNames 端点。模态挂在施工阶段上,不按荷载
        工况组织,结果名形如 ``_自振模态_<阶段名>``,由服务端从 Result/*.modal
        枚举,没有单独的列表接口。

        Args:
            name: 模态结果名（str 或 list[str]）；None 时返回全部
            strict: 显式指定 name 却一行都没查到时报错（默认只告警）

        Returns:
            结果 DataFrame（列: name, kind, mode, period, freq, omega, eigenvalue）
            首列是模态结果名 ``name``,不是 ``loadCase``。

        Raises:
            RuntimeError: 查询失败，或 strict=True 时名字查不到
        """
        return routes.modal_df(name, strict)

    def envelope(
        self,
        name: str | list[str] | None = None,
        kind: Literal["displacement", "force", "stress", "reaction"] = "force",
        strict: bool = False,
    ) -> pd.DataFrame:
        """查询包络结果

        走 /GetAllEnvelope*、/GetEnvelope*ByNames 端点。

        行按 (节点, 分量) 分,值给的是各分量自身极值拼成的包络向量 —— 同一节点的
        各分量行数值相同,分量列是标签。

        Args:
            name: 包络名（str 或 list[str]）；None 时返回全部包络
            kind: 结果类型
                * displacement — 节点位移
                * force        — 单元内力
                * stress       — 单元应力
                * reaction     — 边界反力（额外带 extreme/no/sys 列）
            strict: 显式指定 name 却一行都没查到时报错（默认只告警）

        Returns:
            结果 DataFrame（列: loadCase, source, component, ...）

        Raises:
            RuntimeError: 查询失败，或 strict=True 时名字查不到
            ValueError: kind 不是上面四种
        """
        return routes.envelope_df(name, kind, strict)

    # ═══════════════════════════════════════════
    # 规范验算结果（隔离区:尚无路由）
    # ═══════════════════════════════════════════

    def check(
        self,
        sheet_type: Literal[
            "一般", "混凝土", "施工阶段荷载包络"
        ],
        check_item: Literal[
            "正截面抗弯验算",
            "斜截面抗剪验算",
            "正截面抗压验算",
            "PC抗扭验算",
            "PS正截面短期抗裂验算",
            "PC正截面长期抗裂验算",
            "PC顶底板斜截面抗裂验算",
            "PC腹板斜截面抗裂验算",
            "裂缝宽度验算",
            "挠度验算",
            "PC正截面压应力验算",
            "PC斜截面主压应力验算",
            "PC钢束拉应力验算",
            "PC施工阶段正截面压应力验算",
            "PC施工阶段正截面拉应力验算",
            "正截面杭拉/压承载力验算",
            "PC斜载面抗裂验算",
            "PC使用阶段正截面压应力验算",
            "PC使用阶段斜载面主压应力验算",
            "RC施工阶段正截面压应力验算",
            "RC施工阶段中性轴处主拉应力验算",
            "RC施工阶段受拉钢筋拉应力验算",
        ],
        check_name: str,
    ) -> pd.DataFrame:
        """导出规范验算结果

        Args:
            sheet_type: 表格名称
                * 一般
                * 混凝土
                * 施工阶段荷载包络
            check_item: 验算类型
                * 正截面抗弯验算
                * 斜截面抗剪验算
                * 正截面抗压验算
                * PC抗扭验算
                * PS正截面短期抗裂验算
                * PC正截面长期抗裂验算
                * PC顶底板斜截面抗裂验算
                * PC腹板斜截面抗裂验算
                * 裂缝宽度验算
                * 挠度验算
                * PC正截面压应力验算
                * PC斜截面主压应力验算
                * PC钢束拉应力验算
                * PC施工阶段正截面压应力验算
                * PC施工阶段正截面拉应力验算
                * 正截面杭拉/压承载力验算
                * PC斜载面抗裂验算
                * PC使用阶段正截面压应力验算
                * PC使用阶段斜载面主压应力验算
                * RC施工阶段正截面压应力验算
                * RC施工阶段中性轴处主拉应力验算
                * RC施工阶段受拉钢筋拉应力验算
            check_name: 验算名称

        Returns:
            结果 DataFrame

        Raises:
            RuntimeError: 导出失败时抛出异常
        """
        ok, err, df = osis_check_result(sheet_type, check_item, check_name)
        if not ok:
            raise RuntimeError(
                f"导出验算结果 {sheet_type}/{check_item}/{check_name} 失败: {err}"
            )
        return df

    def check_all(
        self,
        project_dir: str | None = None,
    ) -> dict[str, pd.DataFrame]:
        """全量导出验算结果

        自动扫描项目目录下 Check 文件夹中的所有 .lcc 文件，
        逐个解析并导出为 DataFrame。

        Args:
            project_dir: 项目目录路径，不指定时自动从 OSIS 获取

        Returns:
            字典，键为 lcc 文件名，值为对应的验算结果 DataFrame

        Raises:
            RuntimeError: 获取项目目录失败时抛出异常

        Example:
            >>> results = engine.result.check_all()
            >>> for name, df in results.items():
            ...     print(f"{name}: {len(df)} rows")
        """
        from pathlib import Path

        if project_dir is None:
            from ..project import interface
            project_dir = interface.get_project_directory()
            if not project_dir:
                raise RuntimeError("获取项目目录失败，请检查 OSIS 是否已登录")

        check_path = Path(project_dir) / "Check"
        if not check_path.exists():
            raise RuntimeError(f"Check 目录不存在: {check_path}")

        lcc_files = [f for f in check_path.glob("*.lcc")]
        if not lcc_files:
            return {}

        results: dict[str, pd.DataFrame] = {}
        for lcc_file in lcc_files:
            filename = lcc_file.stem
            # 文件名格式: sheetType_checkItem_checkName
            # 最多分割 3 部分，保留名字中的下划线
            parts = filename.split("_", 2)
            if len(parts) != 3:
                continue  # 跳过格式不正确的文件

            try:
                df = self.check(*parts)
                results[filename] = df
            except RuntimeError:
                # 跳过导出失败的验算项，继续处理其他文件
                continue

        return results

    def __repr__(self) -> str:
        return "ResultManager()"


# ═════════════════════════════════════════════
# 全局单例
# ═════════════════════════════════════════════

result_manager = ResultManager()
