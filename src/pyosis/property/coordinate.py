'''
pyosis.property.coordinate 的 Docstring

空间坐标系
'''

from typing import Literal
from pyosis.core import REGISTRY

@REGISTRY.register("CoorSys")
def osis_property_three_point(nNo: int, eType: Literal["TRIPT"], dP1X: float, dP1Y: float, dP1Z: float, dP2X: float, dP2Y: float, dP2Z: float, dP3X: float, dP3Y: float, dP3Z: float) -> tuple[bool, str]:
    """
    创建或修改空间坐标系

    Args:
        nNo (int): 编号
        eType (Literal["TRIPT"]): 类型，Type=TRIPT
        dP1X (float):
        dP1Y (float):
        dP1Z (float):
        dP2X (float):
        dP2Y (float):
        dP2Z (float):
        dP3X (float):
        dP3Y (float):
        dP3Z (float):

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("CoorSys")
def osis_property_two_point_rotation(nNo: int, eType: Literal["DBPT"], dP1X: float, dP1Y: float, dP1Z: float, dP2X: float, dP2Y: float, dP2Z: float, dAngle: float) -> tuple[bool, str]:
    """
    创建或修改空间坐标系

    Args:
        nNo (int): 编号
        eType (Literal["DBPT"]): 类型，Type=DBPT
        dP1X (float):
        dP1Y (float):
        dP1Z (float):
        dP2X (float):
        dP2Y (float):
        dP2Z (float):
        dAngle (float): x轴的转角（角度）

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("CoorSysDel")
def osis_property_coorsysdel(nNo: int) -> tuple[bool, str]:
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
def osis_property_coorsysmod(strOldIndex: str, strNewIndex: str) -> tuple[bool, str]:
    """
    修改编号

    Args:
        strOldIndex (str):
        strNewIndex (str):

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

