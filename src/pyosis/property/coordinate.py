'''
pyosis.property.coordinate 的 Docstring

空间坐标系
'''

from typing import Literal
from pyosis.core import REGISTRY

@REGISTRY.register("CoorSys")
def osis_coord_sys_three_point(nNo: int, eType: Literal["TRIPT"], dP1X: float, dP1Y: float, dP1Z: float, dP2X: float, dP2Y: float, dP2Z: float, dP3X: float, dP3Y: float, dP3Z: float) -> tuple[bool, str]:
    """
    创建或修改空间坐标系-三点式

    Args:
        nNo (int): 编号
        eType (Literal["TRIPT"]): 类型，Type=TRIPT
        dP1X (float): 原点坐标
        dP1Y (float): 原点坐标
        dP1Z (float): 原点坐标
        dP2X (float): x轴正方向上的任意点坐标
        dP2Y (float): x轴正方向上的任意点坐标
        dP2Z (float): x轴正方向上的任意点坐标
        dP3X (float): xoy平面上的任一点坐标
        dP3Y (float): xoy平面上的任一点坐标
        dP3Z (float): xoy平面上的任一点坐标

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("CoorSys")
def osis_coord_sys_two_point_rotation(nNo: int, eType: Literal["DBPT"], dP1X: float, dP1Y: float, dP1Z: float, dP2X: float, dP2Y: float, dP2Z: float, dAngle: float) -> tuple[bool, str]:
    """
    创建或修改空间坐标系-两点旋转式

    Args:
        nNo (int): 编号
        eType (Literal["DBPT"]): 类型，Type=DBPT
        dP1X (float): 点坐标
        dP1Y (float): 点坐标
        dP1Z (float): 点坐标
        dP2X (float): 点坐标
        dP2Y (float): 点坐标
        dP2Z (float): 点坐标
        dAngle (float): x轴的转角（角度）

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("CoorSysDel")
def osis_coord_sys_del(nNo: int) -> tuple[bool, str]:
    """
    删除空间坐标系

    Args:
        nNo (int): 编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("CoorSysMod")
def osis_coord_sys_mod(strOldIndex: str, strNewIndex: str) -> tuple[bool, str]:
    """
    修改编号

    Args:
        strOldIndex (str): 旧编号
        strNewIndex (str): 新编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

