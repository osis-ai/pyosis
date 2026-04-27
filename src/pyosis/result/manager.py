"""结果管理器 - 统一管理程序运行结果的导出

设计理念：
- 隐藏底层命令接口细节，提供原生 Python 风格 API
- 导出结果为 pandas DataFrame，便于后续分析处理
- 无状态设计，每次调用实时从 OSIS 服务端提取结果

用法:
    >>> from pyosis.result import result_manager
    >>> # 导出荷载工况结果
    >>> df = result_manager.loadcase("自重", "LCEF")
    >>> # 导出包络结果
    >>> df = result_manager.env("基本组合包络", "EnvEF")
    >>> # 导出验算结果
    >>> df = result_manager.check("混凝土", "正截面抗弯验算", "基本组合")
"""

from __future__ import annotations

from typing import Literal

try:
    import pandas as pd
    _HAS_PANDAS = True
except ImportError:
    _HAS_PANDAS = False

from .loadcase import osis_loadcase_result
from .env import osis_env_result
from .check import osis_check_result


class ResultManager:
    """结果管理器

    统一管理荷载工况结果、包络结果、规范验算结果的导出。
    所有方法返回 pandas DataFrame，便于后续数据分析和可视化。
    """

    def _ensure_pandas(self) -> None:
        """确保 pandas 已安装"""
        if not _HAS_PANDAS:
            raise ImportError(
                "结果导出功能依赖 pandas，请先安装：pip install pandas"
            )

    # ═══════════════════════════════════════════
    # 荷载工况结果
    # ═══════════════════════════════════════════

    def loadcase(
        self,
        name: str,
        result_type: Literal[
            "LCEF", "LCED", "LCND", "LCBF", "LCTL", "LCS"
        ],
    ) -> pd.DataFrame:
        """导出荷载工况结果

        Args:
            name: 荷载工况名称
            result_type: 结果类型
                * LCEF — 单元内力
                * LCED — 单元位移
                * LCND — 节点位移
                * LCBF — 边界反力
                * LCTL — 钢束损失
                * LCS  — 单元应力

        Returns:
            结果 DataFrame

        Raises:
            ImportError: 未安装 pandas 时抛出
            RuntimeError: 导出失败时抛出异常
        """
        self._ensure_pandas()
        ok, err, df = osis_loadcase_result(name, result_type)
        if not ok:
            raise RuntimeError(f"导出工况结果 {name} ({result_type}) 失败: {err}")
        return df

    # ═══════════════════════════════════════════
    # 包络 / 并发结果
    # ═══════════════════════════════════════════

    def env(
        self,
        name: str,
        result_type: Literal[
            "EnvBF", "EnvEF", "EnvES", "EnvS", "EnvND"
        ],
    ) -> pd.DataFrame:
        """导出包络 / 并发结果

        Args:
            name: 包络 / 并发工况名称
            result_type: 结果类型
                * EnvBF — 边界反力
                * EnvEF — 单元内力
                * EnvES — 单元应变
                * EnvS  — 单元应力
                * EnvND — 节点位移

        Returns:
            结果 DataFrame

        Raises:
            ImportError: 未安装 pandas 时抛出
            RuntimeError: 导出失败时抛出异常
        """
        self._ensure_pandas()
        ok, err, df = osis_env_result(name, result_type)
        if not ok:
            raise RuntimeError(f"导出包络结果 {name} ({result_type}) 失败: {err}")
        return df

    # ═══════════════════════════════════════════
    # 规范验算结果
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
            ImportError: 未安装 pandas 时抛出
            RuntimeError: 导出失败时抛出异常
        """
        self._ensure_pandas()
        ok, err, df = osis_check_result(sheet_type, check_item, check_name)
        if not ok:
            raise RuntimeError(
                f"导出验算结果 {sheet_type}/{check_item}/{check_name} 失败: {err}"
            )
        return df

    # ═══════════════════════════════════════════
    # 验算结果全量导出
    # ═══════════════════════════════════════════

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
            ImportError: 未安装 pandas 时抛出
            RuntimeError: 获取项目目录失败时抛出异常

        Example:
            >>> results = engine.result.check_all()
            >>> for name, df in results.items():
            ...     print(f"{name}: {len(df)} rows")
        """
        self._ensure_pandas()

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
