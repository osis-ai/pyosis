from typing import Literal
from ..core import REGISTRY


@REGISTRY.register("Section")
def osis_section_numerical(nSec: int, strName: str, eType: Literal["Numerical"], strArea: str, dSy: float, dSz: float, dIxx: float, dIyy: float, dIzz: float, dIww: float, dCentY: float, dCentZ: float, dDy: float, dDz: float, dPeriO: float, dPeriI: float) -> tuple[bool, str]:
    """
    定义或修改数值截面

    Args:
        nSec (int): 编号
        strName (str): 截面名
        eType (str): 数值截面类型，可选值
            * Numerical:数值截面
        strArea (str): 截面面积
        dSy (float): 局部坐标系y轴方向的剪切常数
        dSz (float): 局部坐标系z轴方向的剪切常数
        dIxx (float): 绕局部坐标系x轴的惯性矩
        dIyy (float): 绕局部坐标系y轴的惯性矩
        dIzz (float): 绕局部坐标系z轴的惯性矩
        dIww (float): 翘曲惯性矩
        dCentY (float): 质心在局部坐标系y轴方向的坐标值
        dCentZ (float): 质心在局部坐标系z轴方向的坐标值
        dDy (float): 沿局部坐标系y轴方向的截面偏心
        dDz (float): 沿局部坐标系z轴方向的截面偏心
        dPeriO (float): 截面外轮廓周长
        dPeriI (float): 截面内轮廓周长

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass