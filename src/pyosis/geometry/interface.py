"""
Interfaces of OSIS functions

========

"""
from ..core import REGISTRY

from typing import Literal, List, Tuple, Optional

@REGISTRY.register('Spline3D')
def osis_spline3d_general(strName: str, type: str, eOwner: Literal["LIVE", "TENDON"], 
                          *coordinates: float):
    """创建或修改三维样条曲线（一般边界/GENERAL）。
    
    用于定义具有显式切向控制的三维空间曲线，每个控制点需指定坐标和切向量。

    Args:
        strName (str): 曲线名称。
        type (str): 固定取值:GENERAL
        eOwner (str): 用途
            * LIVE = 用于活载的车道线定义
            * TENDON = 用于钢束定义
        *coordinates (float): 变长坐标序列，严格按 x, y, z, vx, vy, vz 顺序交替排列。
            表示各控制点的三维坐标 (x,y,z) 和切向量 (vx,vy,vz)。
            格式示例：x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, ...

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
            
    Example:
        >>> osis_spline3d_general("Lane1", "LIVE", 
        ...     0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        ...     1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        ...     2.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    """
    pass

@REGISTRY.register('Spline3D')
def osis_spline3d_natural(strName: str, type: str, eOwner: Literal["LIVE", "TENDON"], 
                          *coordinates: float):
    """创建或修改三维样条曲线（自然边界/NATURAL）。
    
    端点二阶导数为零，用于生成光滑路径，无需指定切向量，每个控制点需指定坐标和曲率半径。

    Args:
        strName (str): 曲线名称。
        type (str): 固定取值:NATURAL
        eOwner (str): 用途
            * LIVE = 用于活载的车道线定义
            * TENDON = 用于钢束定义
        *coordinates (float): 变长坐标序列，严格按 x, y, z顺序交替排列。
            表示各控制点的三维坐标 (x,y,z) 。
            格式示例：x1, y1, z1, x2, y2, z2, ...

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Spline3D')
def osis_spline3d_arc2d(strName: str, type: str, eOwner: str, *coordinates: float):
    """创建或修改三维样条曲线（2D圆弧/ARC2D）。
    
    用于生成二维平面内的圆弧曲线，通常用于钢束平面束型定义。

    Args:
        strName (str): 曲线名称。
        type (str): 固定取值:ARC2D
        eOwner：用途，TENDON = 用于钢束定义
        *coordinates (float): 变长坐标序列，严格按 x, y, R 顺序交替排列。
            表示各控制点的二维坐标 (x,y) 和该点处的圆弧半径 R。
            格式示例：x1, y1, R1, x2, y2, R2, ...
            注：z 坐标默认为 0 或由上下文确定，严格保持与原指令 x, y, R 参数格式一致。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Spline3D')
def osis_spline3d_arc3d(strName: str, type: str, eOwner: str, *coordinates: float):
    """创建或修改三维样条曲线（3D圆弧/ARC3D）。
    
    用于生成三维空间内的圆弧曲线。

    Args:
        strName (str): 曲线名称。
        type (str): 固定取值:ARC3D
        eOwner：用途，TENDON = 用于钢束定义
        *coordinates (float): 变长坐标序列，严格按 x, y, z, R 顺序交替排列。
            表示各控制点的三维坐标 (x,y,z) 和该点处的圆弧半径 R。
            格式示例：x1, y1, z1, R1, x2, y2, z2, R2, ...

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Spline3D')
def osis_spline3d_del(strName: str):
    """删除三维样条曲线。

    Args:
        strName (str): 要删除的曲线名称。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
