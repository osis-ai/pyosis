"""属性管理器 - 统一管理坐标系、收缩徐变、阻尼、荷载-位移曲线等属性

用法:
    >>> from pyosis.property import property_manager
    >>> property_manager.coord.create_three_point(1, 0, 0, 0, 10, 0, 0, 0, 10, 0)
    >>> property_manager.creep_shrink.create(1, "CS1", 70.0, 7, 5.0, 3)
    >>> property_manager.damping.create_modal("Damp1", 0.05)
    >>> property_manager.pu_curve.create(1, "PU1", 0, 3, 0.0, 0.01, 0.02, 0.0, 100.0, 150.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional, Any

from .coordinate import (
    osis_coord_sys_three_point,
    osis_coord_sys_two_point_rotation,
    osis_coord_sys_del,
    osis_coord_sys_mod,
)
from .creep_shrink import (
    osis_creep_shrink,
    osis_creep_shrink_del,
    osis_creep_shrink_mod,
)
from .damping import (
    osis_damping_modal,
    osis_damping_rayleigh_custom,
    osis_damping_rayleigh_formula,
    osis_damping_del,
    osis_damping_mod,
)
from .pu_curve import (
    osis_pu_curve,
    osis_pu_curve_del,
    osis_pu_curve_mod,
)
from .component_thickness import osis_assign_component_thickness
from ..core.client import osis_client
from ..core import get_references, raise_if_occupied

@dataclass(frozen=False)
class Point3D:
    x: float
    y: float
    z: float

    @classmethod
    def _from_dict(cls, d: dict | None) -> Optional["Point3D"]:
        if not d:
            return None
        return cls(
            x=float(d.get("x", 0.0)),
            y=float(d.get("y", 0.0)),
            z=float(d.get("z", 0.0)),
        )


@dataclass(frozen=False)
class Coordinate:
    """空间坐标系对象"""
    no: int
    name: str
    coor_sys_type: str
    property_type: int
    p1: Point3D
    p2: Optional[Point3D] = None
    p3: Optional[Point3D] = None
    angle1: Optional[float] = None
    angle2: Optional[float] = None
    related_boundary: list[int] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict) -> "Coordinate":
        return cls(
            no=d.get("no"),
            name=d.get("name", ""),
            coor_sys_type=d.get("coorSysType", ""),
            property_type=d.get("propertyType", 0),
            p1=Point3D._from_dict(d.get("p1")) or Point3D(0.0, 0.0, 0.0),
            p2=Point3D._from_dict(d.get("p2")),
            p3=Point3D._from_dict(d.get("p3")),
            angle1=d.get("angle1"),
            angle2=d.get("angle2"),
            related_boundary=list(d.get("relatedBoundary", [])),
        )

    def __repr__(self) -> str:
        return f"Coordinate(no={self.no}, name={self.name!r}, type={self.coor_sys_type})"

# ──────────────────────────────────────────────
# 子管理器
# ──────────────────────────────────────────────


class CoordinateManager:
    """坐标系管理器"""

    def create(
        self,
        no: int,
        type: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        '''创建或修改空间坐标系（便捷入口，内部转发到对应 create_* 方法）

        type 路由映射：
            * "TRIPT" -> create_three_point
            * "DBPT"  -> create_two_point_rotation

        Args:
            no (int): 坐标系编号
            type (str): 坐标系类型
            *args: 按位置传给对应 create_* 的参数
            **kwargs: 按关键字传给对应 create_* 的参数

        Raises:
            ValueError: 未知 type
            RuntimeError: 创建失败时抛出

        Examples:
            >>> property_manager.coord.create(1, "TRIPT",
            ...     0, 0, 0, 10, 0, 0, 0, 10, 0)
            >>> property_manager.coord.create(2, "DBPT",
            ...     0, 0, 0, 10, 0, 0, angle=90.0)
        '''
        _creator = {
            "TRIPT": self.create_three_point,
            "DBPT":  self.create_two_point_rotation,
        }
        type_key = type.upper()
        if type_key not in _creator:
            raise ValueError(
                f"未知坐标系类型: {type!r}，支持: {', '.join(_creator)}"
            )
        return _creator[type_key](no, *args, **kwargs)

    def create_three_point(
        self,
        no: int,
        p1x: float, p1y: float, p1z: float,
        p2x: float, p2y: float, p2z: float,
        p3x: float, p3y: float, p3z: float,
    ) -> None:
        '''创建或修改三点空间坐标系

        Args:
            no (int): 坐标系编号
            p1x, p1y, p1z (float): 第 1 点坐标（原点）
            p2x, p2y, p2z (float): 第 2 点坐标（x 轴正方向上的任意点）
            p3x, p3y, p3z (float): 第 3 点坐标（xoy 平面上的任一点）

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_coord_sys_three_point(
            no, "TRIPT",
            p1x, p1y, p1z, p2x, p2y, p2z, p3x, p3y, p3z,
        )
        if not ok:
            raise RuntimeError(f"创建坐标系 {no} 失败: {err}")

    def create_two_point_rotation(
        self,
        no: int,
        p1x: float, p1y: float, p1z: float,
        p2x: float, p2y: float, p2z: float,
        angle: float,
    ) -> None:
        '''创建或修改两点+旋转角空间坐标系

        Args:
            no (int): 坐标系编号
            p1x, p1y, p1z (float): 第 1 点坐标
            p2x, p2y, p2z (float): 第 2 点坐标
            angle (float): x 轴的转角（角度）

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_coord_sys_two_point_rotation(
            no, "DBPT",
            p1x, p1y, p1z, p2x, p2y, p2z, angle,
        )
        if not ok:
            raise RuntimeError(f"创建坐标系 {no} 失败: {err}")

    def get_dependencies(self, no: int) -> dict[str, list]:
        '''查询坐标系被谁引用'''
        return get_references("CoorSys", no=no)

    def delete(self, no: int) -> None:
        '''删除坐标系

        Args:
            no (int): 坐标系编号

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(no)
        raise_if_occupied("CoorSys", deps, no=no)
        ok, err = osis_coord_sys_del(no)
        if not ok:
            raise RuntimeError(f"删除坐标系 {no} 失败: {err}")

    def renumber(self, old: str, new: str) -> None:
        '''修改坐标系编号

        Args:
            old (str): 旧编号
            new (str): 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        '''
        ok, err = osis_coord_sys_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改坐标系编号 {old} -> {new} 失败: {err}")

    def all(self) -> list[Coordinate]:
        '''获取全部空间坐标系

        Returns:
            全部 Coordinate 对象列表

        Raises:
            RuntimeError: 接口调用失败时抛出
        '''
        resp = osis_client("GetAllCoorSysInfo", {})
        if not resp.get("success"):
            raise RuntimeError(resp.get("error", "GetAllCoorSysInfo 失败"))
        return [
            Coordinate._from_dict(d)
            for d in resp.get("data", [])
            if isinstance(d, dict) and "no" in d
        ]

    def get(self, no: int | list[int]) -> Coordinate | list[Coordinate | None] | None:
        '''根据编号获取空间坐标系

        Args:
            no (int|list): 坐标系编号或编号列表

        Returns:
            单个 Coordinate 对象或对象列表；不存在返回 None

        Raises:
            TypeError: 不支持的编号类型
            RuntimeError: 接口调用失败时抛出
        '''
        if isinstance(no, int):
            nos = [no]
        elif isinstance(no, list):
            nos = no
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")

        resp = osis_client("GetCoorSysInfoByNos", {"no": nos})
        if not resp.get("success"):
            raise RuntimeError(resp.get("error", "GetCoorSysInfoByNos 失败"))

        coords = [
            Coordinate._from_dict(d) if isinstance(d, dict) and d.get("no") is not None else None
            for d in resp.get("data", [])
        ]

        if len(coords) == 0:
            return None
        elif len(coords) == 1:
            return coords[0]
        return coords

    def clear(self) -> None:
        '''清空所有空间坐标系'''
        try:
            [self.delete(c.no) for c in self.all()]
        except Exception as e:
            raise Exception(f"清空所有空间坐标系失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return "CoordinateManager()"

@dataclass(frozen=False)
class CreepShrink:
    """收缩徐变对象"""
    avg_humidity: float
    birth_by_shrinking: int
    birth_time: int
    name: str
    no: int
    shrink_birth: int
    related_material: list[int]
    type_coeff: float
    @classmethod
    def _from_dict(cls, d: dict) -> CreepShrink:
        """从接口 dict 构造 CreepShrink 对象（内部使用）"""
        return cls(
            avg_humidity=d.get("avgHumidity"),
            birth_by_shrinking=d.get("birthByShrinking"),
            birth_time=d.get("birthTime"),
            name=d.get("name"),
            no=d.get("no"),
            shrink_birth=d.get("shrinkBirth"),
            related_material=list(d.get("relatedMaterial") or []),
            type_coeff = d.get("typeCoeff"),
        )

class CreepShrinkManager:
    '''收缩徐变管理器'''
    def all(self):
        '''获取全部收缩徐变特性

        Returns:
            全部 CreepShrink 对象列表

        Raises:
            RuntimeError: 接口调用失败时抛出
        '''
        resp = osis_client("GetAllCreepShrinkInfo",{})
        if not resp["success"]:
            raise RuntimeError(resp["error"])
        creep_shrinks = [CreepShrink._from_dict(d) for d in resp.get("data", []) if "no" in d]
        return creep_shrinks

    def get(self, no:int | list[int]):
        '''根据编号获取收缩徐变特性

        Args:
            no (int|list): 编号或编号列表

        Returns:
            单个 CreepShrink 对象或对象列表；不存在返回 None

        Raises:
            TypeError: 不支持的编号类型
            RuntimeError: 接口调用失败时抛出
        '''
        if isinstance(no, int):
            no = [no]
        elif not isinstance(no, list):
            raise TypeError(f"不支持的编号类型: {type(no)}")

        resp = osis_client("GetCreepShrinkInfoByNos", {"no": no})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")

        creep_shrinks = [CreepShrink._from_dict(d) if d else None for d in resp.get("data", [])]

        if len(creep_shrinks) == 0:
            return None
        elif len(creep_shrinks) == 1:
            return creep_shrinks[0]
        return creep_shrinks

    def create(
        self,
        no: int = 1,
        name: str = "收缩徐变1",
        avg_humidity: float = 70.0,
        birth_time: int = 7,
        type_coeff: float = 5.0,
        shrink_birth: int = 3,
    ) -> CreepShrink:
        '''创建或修改收缩徐变特性

        Args:
            no (int): 收缩徐变特性编号
            name (str): 特性名称
            avg_humidity (float): 年平均湿度（百分比）
            birth_time (int): 混凝土龄期（天）
            type_coeff (float): 水泥种类系数
            shrink_birth (int): 收缩开始时的混凝土龄期（天数）

        Returns:
            创建的 CreepShrink 对象

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_creep_shrink(
            no, name, avg_humidity, birth_time, type_coeff, shrink_birth,
        )
        if not ok:
            raise RuntimeError(f"创建收缩徐变特性 {no} 失败: {err}")
        return self.get(no)

    def get_dependencies(self, no: int) -> dict[str, list]:
        """查询收缩徐变特性被谁引用"""
        return get_references("CreepShrink", no=no)

    def delete(self, no: int) -> None:
        '''删除收缩徐变特性

        Args:
            no (int): 收缩徐变特性编号

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(no)
        raise_if_occupied("CreepShrink", deps, no=no)
        ok, err = osis_creep_shrink_del(no)
        if not ok:
            raise RuntimeError(f"删除收缩徐变特性 {no} 失败: {err}")

    def renumber(self, old: int, new: int) -> None:
        '''修改收缩徐变特性编号。收缩徐变特性编号存在时，交换

        Args:
            old (int): 旧编号
            new (int): 新编号

        Raises:
            RuntimeError: 修改失败时抛出异常
        '''
        ok, err = osis_creep_shrink_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改收缩徐变编号 {old} -> {new} 失败: {err}")

    def clear(self) -> None:
        '''清空所有收缩徐变特性'''
        try:
            [self.delete(c.no) for c in self.all()]
        except Exception as e:
            raise Exception(f"清空所有收缩徐变特性失败: {e}，被占用,无法删除")

    def count(self) -> int:
        '''获取收缩徐变特性数量

        Returns:
            收缩徐变特性数量
        '''
        objs = self.all()
        return len(objs)

    def __repr__(self) -> str:
        return "CreepShrinkManager()"


@dataclass(frozen=False)
class Damping:
    """阻尼模型对象"""
    analysisType: int
    dampingType: int
    kind: str
    ksi: float
    name: str
    no: int
    relatedAnalysis: list[str]
    relatedStages: list[str]
    @classmethod
    def _from_dict(cls, d: dict) -> Damping:
        return cls(
            analysisType=d.get("analysisType"),
            dampingType=d.get("dampingType"),
            kind=d.get("kind"), ksi=d.get("ksi"),
            name=d.get("name"), no=d.get("no"),
            relatedAnalysis=d.get("relatedAnalysis"),
            relatedStages=d.get("relatedStages"))

class DampingManager:
    '''阻尼管理器'''

    def create(
        self,
        name: str,
        type: str,
        *args: Any,
        **kwargs: Any,
    ) -> Damping:
        '''创建或修改阻尼模型（便捷入口，内部转发到对应 create_* 方法）

        type 路由映射：
            * "modal" -> create_modal
            * "ryl"   -> create_rayleigh_custom（当 method=1）
                       或 create_rayleigh_formula（当 method=0）

        Args:
            name (str): 阻尼模型名称
            type (str): 阻尼类型
            *args: 按位置传给对应 create_* 的参数
                - "modal": 下一个位置参数为 ksi
                - "ryl": 下一个位置参数为 method (1=自定义, 0=公式)
            **kwargs: 按关键字传给对应 create_* 的参数

        Raises:
            ValueError: 未知 type
            RuntimeError: 创建失败

        Examples:
            >>> property_manager.damping.create("D1", "modal", 0.05)
            >>> property_manager.damping.create("D2", "ryl", 1, alpha=0.1, beta=0.01)
            >>> property_manager.damping.create("D3", "ryl", 0,
            ...     ksii=0.05, ksij=0.05, wi=1.0, wj=5.0)
        '''
        _supported_types = {"MODAL", "RYL"}
        type_key = type.upper()
        if type_key not in _supported_types:
            raise ValueError(
                f"未知阻尼类型: {type!r}，支持: {', '.join(sorted(_supported_types))}"
            )
        if type_key == "modal":
            return self.create_modal(name, *args, **kwargs)
        # type_key == "ryl"
        method = args[0] if args else kwargs.get("method")
        _supported_methods = {0: "根据公式计算因子", 1: "自定义因子"}
        if method not in _supported_methods:
            raise ValueError(
                f"type='ryl' 时必须指定 method: "
                f"{', '.join(f'{k}={v}' for k, v in sorted(_supported_methods.items()))}"
            )
        if args:
            args = args[1:]
        kwargs.pop("method", None)
        if method == 1:
            return self.create_rayleigh_custom(name, *args, **kwargs)
        return self.create_rayleigh_formula(name, *args, **kwargs)

    def create_modal(self, name: str, ksi: float) -> Damping:
        '''创建或修改振型阻尼

        Args:
            name (str): 阻尼模型的名称
            ksi (float): 振型阻尼数值

        Returns:
            创建的 Damping 对象

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_damping_modal(name, "modal", ksi)
        if not ok:
            raise RuntimeError(f"创建振型阻尼 {name} 失败: {err}")
        return self.get(name)

    def create_rayleigh_custom(
        self, name: str, alpha: float, beta: float,
    ) -> Damping:
        '''创建或修改Rayleigh阻尼（自定义因子）

        Args:
            name (str): 阻尼模型的名称
            alpha (float): 质量因子
            beta (float): 刚度因子

        Returns:
            创建的 Damping 对象

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_damping_rayleigh_custom(name, "ryl", 1, alpha, beta)
        if not ok:
            raise RuntimeError(f"创建Rayleigh阻尼 {name} 失败: {err}")
        return self.get(name)

    def create_rayleigh_formula(
        self,
        name: str,
        ksii: float, ksij: float,
        wi: float, wj: float,
    ) -> Damping:
        '''创建或修改Rayleigh阻尼（根据公式计算因子）

        Args:
            name (str): 阻尼模型的名称
            ksii (float): 阻尼比
            ksij (float): 阻尼比
            wi (float): 圆频率
            wj (float): 圆频率

        Returns:
            创建的 Damping 对象

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        ok, err = osis_damping_rayleigh_formula(name, "ryl", 0, ksii, ksij, wi, wj)
        if not ok:
            raise RuntimeError(f"创建Rayleigh阻尼 {name} 失败: {err}")
        return self.get(name)

    def get_dependencies(self, name: str) -> dict[str, list]:
        '''查询阻尼模型被谁引用'''
        return get_references("Damping", name=name)

    def delete(self, name: str) -> None:
        '''删除阻尼模型

        Args:
            name (str): 阻尼模型的名称

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(name)
        raise_if_occupied("Damping", deps, name=name)
        ok, err = osis_damping_del(name)
        if not ok:
            raise RuntimeError(f"删除阻尼模型 {name} 失败: {err}")

    def rename(self, old: str, new: str) -> None:
        '''修改阻尼模型名称。阻尼模型名称存在时，交换

        Args:
            old (str): 原阻尼名称
            new (str): 新阻尼名称

        Raises:
            RuntimeError: 重命名失败时抛出
        '''
        ok, err = osis_damping_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改阻尼名称 {old} -> {new} 失败: {err}")

    def _load(self) -> list[Damping]:
        '''从服务端加载所有阻尼模型信息'''
        resp = osis_client("GetAllDampingInfo", {})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        dampings = [Damping._from_dict(d) for d in resp.get("data", []) if "name" in d]
        return dampings

    def get(self, name: str | list[str]) -> Damping | list[Damping | None] | None:
        '''根据名称获取阻尼模型

        Args:
            name (str|list): 阻尼模型名称，支持单个名称或名称列表

        Returns:
            单个 Damping 对象或对象列表；不存在返回 None

        Raises:
            TypeError: 不支持的名称类型
            RuntimeError: 接口调用失败时抛出
        '''
        if isinstance(name, list):
            names = [str(x) for x in name]
        else:
            names = [str(name)]
        if not isinstance(names, list):
            raise TypeError(f"不支持的名称类型: {type(name)}")
        resp = osis_client("GetDampingInfoByNames", {"name": names})
        if not resp['success']:
            raise RuntimeError(f"{resp['error']}")
        dampings = [Damping._from_dict(d) if d else None for d in resp.get("data", [])]
        if len(dampings) == 0:
            return None
        elif len(dampings) == 1:
            return dampings[0]
        return dampings

    def all(self) -> list[Damping]:
        '''获取所有阻尼模型

        Returns:
            全部 Damping 对象列表
        '''
        return self._load()

    def clear(self)->None:
        '''清空所有阻尼模型'''
        try:
            [self.delete(d.name) for d in self.all()]
        except Exception as e:
            raise Exception(f"清空所有阻尼模型失败: {e}，被占用,无法删除")

    def count(self) -> int:
        '''获取阻尼模型数量

        Returns:
            阻尼模型数量
        '''
        objs = self.all()
        return len(objs)

    def __repr__(self) -> str:
        return "DampingManager()"

@dataclass(frozen=False)
class PuCurve:
    """荷载-位移曲线对象"""
    no: int
    name: str
    property_type: int
    curve_type: int          # 0=力, 1=力矩
    num: int
    displacement: list[float]
    force: list[float]
    related_element: list[int]
    @classmethod
    def _from_dict(cls, d: dict) -> "PuCurve":
        return cls(
            no=d.get("no"),
            name=d.get("name", ""),
            property_type=d.get("propertyType", 0),
            curve_type=d.get("curveType", 0),
            num=d.get("num", 0),
            displacement=list(d.get("displacement", [])),
            force=list(d.get("force", [])),
            related_element=list(d.get("relatedElement", [])),
        )
    def __repr__(self) -> str:
        return f"PuCurve(no={self.no}, name={self.name!r}, type={self.curve_type})"

class PuCurveManager:
    '''荷载-位移曲线管理器'''

    def create(
        self,
        no: int,
        name: str,
        curve_type: Literal[0, 1],
        num: int,
        *values: float,
    ) -> None:
        '''创建或修改荷载-位移曲线，荷载与位移需要唯一对应

        Args:
            no (int): 位移-力（矩）曲线编号
            name (str): 曲线名称
            curve_type (int): 曲线类型
                * 0 = 力
                * 1 = 力矩
            num (int): 曲线点数
            values (float): 前 num 个为位移值，后 num 个为力（矩）值，共 2*num 个

        Raises:
            RuntimeError: 创建失败时抛出
        '''
        displacement = [float(x) for x in values[:num]]
        force = [float(x) for x in values[num:2 * num]]
        ok, err = osis_pu_curve(no, name, curve_type, num, displacement, force)
        if not ok:
            raise RuntimeError(f"创建荷载-位移曲线 {no} 失败: {err}")

    def get_dependencies(self, no: int) -> dict[str, list]:
        '''查询荷载-位移曲线被谁引用'''
        return get_references("PUCurve", no=no)

    def delete(self, no: int) -> None:
        '''删除位移-内力曲线

        Args:
            no (int): 位移-力（矩）曲线编号

        Raises:
            DependencyError: 存在依赖项时
            RuntimeError: 删除失败时抛出异常
        '''
        deps = self.get_dependencies(no)
        raise_if_occupied("PUCurve", deps, no=no)
        ok, err = osis_pu_curve_del(no)
        if not ok:
            raise RuntimeError(f"删除荷载-位移曲线 {no} 失败: {err}")

    def renumber(self, old: int, new: int) -> None:
        '''修改荷载-位移曲线编号。曲线编号存在时，交换

        Args:
            old (int): 旧编号
            new (int): 新编号

        Raises:
            RuntimeError: 修改失败时抛出
        '''
        ok, err = osis_pu_curve_mod(old, new)
        if not ok:
            raise RuntimeError(f"修改荷载-位移曲线编号 {old} -> {new} 失败: {err}")

    def all(self) -> list[PuCurve]:
        '''获取全部荷载-位移曲线

        Returns:
            全部 PuCurve 对象列表

        Raises:
            RuntimeError: 接口调用失败时抛出
        '''
        resp = osis_client("GetAllPuCurveInfo", {})
        if not resp.get("success"):
            raise RuntimeError(resp.get("error", "GetAllPuCurveInfo 失败"))
        return [
            PuCurve._from_dict(d)
            for d in resp.get("data", [])
            if isinstance(d, dict) and "no" in d
        ]

    def get(self, no: int | list[int]) -> PuCurve | list[PuCurve | None] | None:
        '''根据编号获取荷载-位移曲线

        Args:
            no (int|list): 曲线编号或编号列表

        Returns:
            单个 PuCurve 对象或对象列表；不存在返回 None

        Raises:
            TypeError: 不支持的编号类型
            RuntimeError: 接口调用失败时抛出
        '''
        if isinstance(no, int):
            nos = [no]
        elif isinstance(no, list):
            nos = no
        else:
            raise TypeError(f"不支持的编号类型: {type(no)}")
        resp = osis_client("GetPuCurveInfoByNos", {"no": nos})
        if not resp.get("success"):
            raise RuntimeError(resp.get("error", "GetPuCurveInfoByNos 失败"))
        curves = [
            PuCurve._from_dict(d) if isinstance(d, dict) and d.get("no") is not None else None
            for d in resp.get("data", [])
        ]
        if len(curves) == 0:
            return None
        if len(curves) == 1:
            return curves[0]
        return curves

    def clear(self) -> None:
        '''清空所有荷载-位移曲线'''
        try:
            [self.delete(c.no) for c in self.all()]
        except Exception as e:
            raise Exception(f"清空所有荷载-位移曲线失败: {e}，被占用,无法删除")

    def __repr__(self) -> str:
        return "PuCurveManager()"


# ──────────────────────────────────────────────
# 主管理器
# ──────────────────────────────────────────────


class PropertyManager:
    """属性管理器

    统一管理坐标系、收缩徐变、阻尼、荷载-位移曲线等属性。

    各子管理器通过属性访问：
        - coord:        坐标系管理器
        - creep_shrink: 收缩徐变管理器
        - damping:      阻尼管理器
        - pu_curve:     荷载-位移曲线管理器
    """

    def __init__(self) -> None:
        self._coord = CoordinateManager()
        self._creep_shrink = CreepShrinkManager()
        self._damping = DampingManager()
        self._pu_curve = PuCurveManager()

    @property
    def coord(self) -> CoordinateManager:
        """坐标系管理器"""
        return self._coord

    @property
    def creep_shrink(self) -> CreepShrinkManager:
        """收缩徐变管理器"""
        return self._creep_shrink

    @property
    def damping(self) -> DampingManager:
        """阻尼管理器"""
        return self._damping

    @property
    def pu_curve(self) -> PuCurveManager:
        """荷载-位移曲线管理器"""
        return self._pu_curve

    def assign_component_thickness(
        self,
        thickness: float,
        op: Literal["a", "s", "r"],
        *elems: str | int,
    ) -> None:
        '''分配或重置单个单元的理论厚度，用于定义收缩徐变特性

        Args:
            thickness (float): 构件理论厚度
            op (str): 操作
                * a = 添加
                * s = 替换
                * r = 移除
            *elems (str|int): 待分配单元的编号。定义、修改、删除 elem 支持的格式：*to*

        Raises:
            RuntimeError: 分配失败时抛出
        '''
        ok, err = osis_assign_component_thickness(thickness, op, *elems)
        if not ok:
            raise RuntimeError(f"分配构件厚度失败: {err}")

    def count(self) -> dict[str, int]:
        '''统计各子管理器的对象数量

        Returns:
            dict: 包含各子管理器对象数量的字典
        '''
        return {
            # "coords": self._coord.count(),
            "creep_shrinks": self._creep_shrink.count(),
            "dampings": self._damping.count(),
            # "pu_curves": self._pu_curve.count(),
        }


    def clear(self)->None:
        '''清空所有属性对象（坐标系、收缩徐变、阻尼、荷载-位移曲线）'''
        self.coord.clear()
        self.creep_shrink.clear()
        self.damping.clear()
        self.pu_curve.clear()

    def __repr__(self) -> str:
        return "PropertyManager()"


# ──────────────────────────────────────────────
# 全局单例
# ──────────────────────────────────────────────

property_manager = PropertyManager()
