"""OSIS Engine - pyosis 核心引擎类

整合 pyosis 各个模块的管理器，提供统一的项目级入口。

设计理念：
- 作为 pyosis 的中心门面（Facade），整合所有子管理器
- 不直接实现功能，只负责暴露子管理器的接口
- 简化用户代码，无需分别导入各个 manager

用法:
    >>> from pyosis.core.engine import OSISEngine
    >>> engine = OSISEngine()
    >>> engine.material.create_conc("C30", eCode="JTG3362_2018", eGrade="C30")
    >>> engine.node.create(0, 0, 0)
    >>> engine.element.create_beam3d(1, 2, nMat=1, nSec1=1, nSec2=1)
    >>> engine.control.run()  # 运行分析
    >>> engine.control.save_project()
"""

from __future__ import annotations

from ..material.manager import MaterialManager, material_manager
from ..section.manager import SectionManager, section_manager
from ..node.manager import NodeManager, node_manager
from ..element.manager import ElementManager, element_manager
from ..boundary.manager import BoundaryManager, boundary_manager
from ..load.manager import LoadCaseManager, loadcase_manager
from ..stage.manager import StageManager, stage_manager
from ..live.manager import LiveManager, live_manager
from ..control.manager import ControlManager, control_manager


class OSISEngine:
    """OSIS 核心引擎

    整合 pyosis 所有模块，提供统一的项目级接口。

    各子管理器通过属性访问：
        - material:  材料管理器
        - section:   截面管理器
        - node:      节点管理器
        - element:   单元管理器
        - boundary:  边界管理器
        - load:      荷载工况管理器
        - stage:     施工阶段管理器
        - live:      活载管理器
        - control:   控制管理器（全局参数、项目操作、分析控制）
    """

    def __init__(self) -> None:
        # 引用全局单例管理器
        self._material = material_manager
        self._section = section_manager
        self._node = node_manager
        self._element = element_manager
        self._boundary = boundary_manager
        self._load = loadcase_manager
        self._stage = stage_manager
        self._live = live_manager
        self._control = control_manager

    # ──────────────────────────────────────────
    # 子管理器属性
    # ──────────────────────────────────────────

    @property
    def material(self) -> MaterialManager:
        """材料管理器"""
        return self._material

    @property
    def section(self) -> SectionManager:
        """截面管理器"""
        return self._section

    @property
    def node(self) -> NodeManager:
        """节点管理器"""
        return self._node

    @property
    def element(self) -> ElementManager:
        """单元管理器"""
        return self._element

    @property
    def boundary(self) -> BoundaryManager:
        """边界管理器"""
        return self._boundary

    @property
    def load(self) -> LoadCaseManager:
        """荷载工况管理器"""
        return self._load

    @property
    def stage(self) -> StageManager:
        """施工阶段管理器"""
        return self._stage

    @property
    def live(self) -> LiveManager:
        """活载管理器"""
        return self._live

    @property
    def control(self) -> ControlManager:
        """控制管理器（全局参数、项目操作、分析控制）"""
        return self._control

    # ──────────────────────────────────────────
    # 便捷方法（直接委托给 control，保持向后兼容）
    # ──────────────────────────────────────────

    def run(self) -> None:
        """运行分析"""
        self._control.run()

    def save_project(self) -> None:
        """保存当前项目"""
        self._control.save_project()

    def model_summary(self) -> dict[str, int]:
        """获取模型汇总统计

        Returns:
            各组件数量的字典
        """
        return {
            "materials": self._material.count(),
            "sections": self._section.count(),
            "nodes": self._node.count(),
            "elements": self._element.count(),
            "boundaries": self._boundary.count(),
            "load_cases": self._load.count(),
            "stages": self._stage.count(),
        }

    def refresh_all(self) -> None:
        """强制刷新所有管理器的缓存"""
        self._material.refresh()
        self._section.refresh()
        self._node.refresh()
        self._element.refresh()
        self._boundary.refresh()
        self._load.refresh()
        self._stage.refresh()
        self._live.refresh()

    def __repr__(self) -> str:
        summary = self.model_summary()
        parts = [
            f"OSISEngine(",
            f"  materials={summary['materials']},",
            f"  sections={summary['sections']},",
            f"  nodes={summary['nodes']},",
            f"  elements={summary['elements']},",
            f"  boundaries={summary['boundaries']},",
            f"  load_cases={summary['load_cases']},",
            f"  stages={summary['stages']}",
            f")",
        ]
        return "\n".join(parts)
