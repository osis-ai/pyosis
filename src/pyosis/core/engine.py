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
    >>> engine.solve()         # 求解工程
    >>> engine.save_project()  # 保存项目
"""

from __future__ import annotations

import os
from typing import Any

from .apdl_sync import ApdlSyncResult, ApdlSessionStore, perform_apdl_sync
from ..material.manager import MaterialManager, material_manager
from ..section.manager import SectionManager, section_manager
from ..node.manager import NodeManager, node_manager
from ..element.manager import ElementManager, element_manager
from ..boundary.manager import BoundaryManager, boundary_manager
from ..load.manager import LoadCaseManager, TendonManager, loadcase_manager, tendon_manager
from ..stage.manager import StageManager, stage_manager
from ..live.manager import LiveManager, live_manager
from ..control.manager import ControlManager, control_manager
from ..project.manager import ProjectManager, project_manager
from ..geometry.manager import GeometryManager, geometry_manager
from ..property.manager import PropertyManager, property_manager
from ..thickness.manager import ThicknessManager, thickness_manager
from ..settlement.manager import SettlementManager, settlement_manager
from ..stability.manager import StabilityManager, stability_manager
from ..dynamic.manager import DynamicManager, dynamic_manager
from ..post.manager import PostManager, post_manager
from ..result.manager import ResultManager, result_manager
from ..general.interface import (
    osis_matrix,
    output_result_for_calc_book,
    osis_replot,
    osis_clear,
    osis_clc,
    osis_solve,
)
from .command import osis_run
from .client import set_osis_port, set_osis_url


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
        - tendon:    钢束管理器（含 prop/shape 子管理器）
        - live:      活载管理器（含 grade/lane/case 子管理器）
        - geometry:  几何管理器（三维样条曲线）
        - property:  属性管理器（坐标系、收缩徐变、阻尼等）
        - thickness: 厚度管理器（壳厚度特性）
        - control:   控制管理器（全局参数、分析设置）
        - project:   项目管理器（创建、打开、保存项目）
        - settlement: 沉降分析管理器
        - stability: 稳定分析管理器（屈曲分析）
        - dynamic:   动力分析管理器（荷载转换质量、模态、反应谱）
        - post:      后处理管理器（荷载组合、规范验算、结果显示）
        - result:    结果导出管理器（工况结果、包络结果、验算结果）

    通用操作可直接通过 engine 调用：
        - run(), solve(), replot(), clear(), clc()
        - matrix(), output_result_for_calc_book()
    """

    def __init__(self, port=None, url="http://localhost") -> None:
        '''
        Args:
            port (int): OSIS 端口号，为 `None` 自动尝试加载 `OSIS_HTTP_PORT` 环境变量，加载失败将设为默认值 18080
            url (str): OSIS 网址
        '''
        # 引用全局单例管理器
        self._project = project_manager

        ### 前处理 ###
        self._control = control_manager
        self._geometry = geometry_manager
        self._property = property_manager
        self._thickness = thickness_manager
        self._material = material_manager
        self._section = section_manager
        self._node = node_manager
        self._element = element_manager
        self._boundary = boundary_manager
        self._load = loadcase_manager
        self._tendon = tendon_manager
        self._live = live_manager
        self._settlement = settlement_manager
        self._stability = stability_manager
        self._dynamic = dynamic_manager
        self._stage = stage_manager

        ### 后处理 ###
        self._post = post_manager
        self._result = result_manager

        # OSIS端口与网址
        if port is None:
            self._port = os.environ.get("OSIS_HTTP_PORT", 18080)     # 如果设置了环境变量
        else:
            self._port = port
        self._url = url
        set_osis_url(self._url)
        set_osis_port(self._port)
        self._apdl_session = ApdlSessionStore()

    # ──────────────────────────────────────────
    # 子管理器属性
    # ──────────────────────────────────────────

    @property
    def project(self) -> ProjectManager:
        """项目管理器（创建、打开、保存项目）"""
        return self._project
    
    ### 前处理 ###

    @property
    def control(self) -> ControlManager:
        """控制管理器（全局参数、分析设置）"""
        return self._control

    @property
    def geometry(self) -> GeometryManager:
        """几何管理器（三维样条曲线）"""
        return self._geometry
    
    @property
    def prop(self) -> PropertyManager:
        """属性管理器（坐标系、收缩徐变、阻尼等）"""
        return self._property
    
    @property
    def thickness(self) -> ThicknessManager:
        """厚度管理器（壳厚度特性）"""
        return self._thickness
    
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
    def tendon(self) -> TendonManager:
        """钢束管理器"""
        return self._tendon

    @property
    def live(self) -> LiveManager:
        """活载管理器"""
        return self._live

    @property
    def settlement(self) -> SettlementManager:
        """沉降分析管理器"""
        return self._settlement
    
    @property
    def stability(self) -> StabilityManager:
        """稳定分析管理器（屈曲分析）"""
        return self._stability

    @property
    def dynamic(self) -> DynamicManager:
        """动力分析管理器（荷载转换质量、模态、反应谱）"""
        return self._dynamic
    
    @property
    def stage(self) -> StageManager:
        """施工阶段管理器"""
        return self._stage

    ### 后处理 ###

    @property
    def post(self) -> PostManager:
        """后处理管理器（荷载组合、规范验算、结果显示）"""
        return self._post

    @property
    def result(self) -> ResultManager:
        """结果导出管理器（工况结果、包络结果、验算结果）"""
        return self._result

    # ──────────────────────────────────────────
    # 通用操作（直接暴露 general 和 core 的函数）
    # ──────────────────────────────────────────

    def run(self, cmd: str = "") -> None:
        """执行 OSIS 命令流

        Args:
            cmd: 命令流字符串
            mode: 运行模式，"stash" 暂存 / "exec" 执行

        Returns:
            (success, error) 元组
        """
        ok, err = osis_run(cmd)
        if not ok:
            raise RuntimeError(f"执行失败: {err}")

    def solve(self) -> None:
        """求解工程"""
        ok, err = osis_solve()
        if not ok:
            raise RuntimeError(f"求解失败: {err}")

    def replot(self) -> None:
        """重新绘制窗口"""
        ok, err = osis_replot()
        if not ok:
            raise RuntimeError(f"重绘失败: {err}")

    def clear(self) -> None:
        """清空项目"""
        ok, err = osis_clear()
        if not ok:
            raise RuntimeError(f"清空项目失败: {err}")

    def clc(self) -> None:
        """清屏"""
        ok, err = osis_clc()
        if not ok:
            raise RuntimeError(f"清屏失败: {err}")

    def matrix(self, name: str, data: Any) -> str:
        """定义矩阵（用于自定义截面等）

        Args:
            name: 矩阵变量名
            data: 矩阵数据（列表/数值）

        Returns:
            (success, error) 元组
        """
        ok, err = osis_matrix(name, data)
        if not ok:
            raise RuntimeError(f"定义失败: {err}")
        return name

    def output_result_for_calc_book(self) -> dict:
        """输出计算书所需结果"""
        return output_result_for_calc_book()

    # ──────────────────────────────────────────
    # 便捷方法（委托给 project manager）
    # ──────────────────────────────────────────

    def save_project(self) -> None:
        """保存当前项目"""
        self._project.save()

    def new_project(self, type: int = 1, filepath: str = "") -> None:
        """新建项目

        Args:
            type: 项目类型，默认 1
            filepath: 项目文件路径
        """
        self._project.create(type, filepath)

    def open_project(self, filepath: str) -> None:
        """打开项目

        Args:
            filepath: 项目文件路径
        """
        self._project.open(filepath)

    # ──────────────────────────────────────────
    # 便捷方法（委托给 control manager）
    # ──────────────────────────────────────────
    def export_apdl(self, path: str | None = None) -> None:
        """导出前处理状态为 .out 文件
        
        Args:
            path: 路径，可缺省。格式：C:\\Temp\\OSIS.out
        """
        self.control.export_apdl(path)

    def import_apdl(self, path: str) -> None:
        """读取 .out / .sml 文件

        Args:
            path (str): 完整文件名
         
        Notes: 
            path 中如果不输入绝对路径的话，默认使用程序执行文件所在的路径，比如“D:\\Rbin\\X.sml”。
        """
        self.control.import_apdl(path)

    # ──────────────────────────────────────────
    # 模型汇总
    # ──────────────────────────────────────────

    def model_summary(self) -> dict[str, int]:
        """获取模型汇总统计

        Returns:
            各组件数量的字典
        """
        return {
            # "controls":   # 没必要
            "geometries": self._geometry.count(),
            "properties": self.prop.count(),
            # "thickness": self._thickness.count(),
            "materials": self._material.count(),
            "sections": self._section.count(),
            "nodes": self._node.count(),
            "elements": self._element.count(),
            "boundaries": self._boundary.count(),
            "loadcases": self._load.count(),
            "tendon_props": self._tendon.prop.count(),
            "tendon_shapes": self._tendon.shape.count(),
            "lives": self._live.count(),
            "settlements": self._settlement.count(),
            "stabilities": self._stability.count(),
            "dynamic": self._dynamic.count(),
            "stages": self._stage.count(),
        }

    def __repr__(self) -> str:
        # summary = self.model_summary()
        # parts = [
        #     f"OSISEngine(",
        #     f"  materials={summary['materials']},",
        #     f"  sections={summary['sections']},",
        #     f"  nodes={summary['nodes']},",
        #     f"  elements={summary['elements']},",
        #     f"  boundaries={summary['boundaries']},",
        #     f"  load_cases={summary['load_cases']},",
        #     f"  stages={summary['stages']}",
        #     f")",
        # ]
        # return "\n".join(parts)
        return f"OSISEngine(project_path={self.project.get_directory()})"

    def sync_apdl(
            self,
            path: str | None = None,
    ) -> ApdlSyncResult:
        """通过 APDL 导出从 OSIS 同步数据。OSIS 界面操作后调用。"""
        return perform_apdl_sync(self, path)
