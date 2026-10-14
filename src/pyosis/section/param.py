'''
pyosis.section.param 的 Docstring
'''

from typing import Any, Dict, Literal
from ..core import REGISTRY
# from ..common import get_project_directory

#SectionOffset,1,Middle,0.0000,Center,0.0000; SectionMesh,1,0,0.1000; 
@REGISTRY.register('SectionOffset')
def osis_section_offset(nSec: int=1, offsetTypeY: Literal["Left", "Middle", "Right"]="Middle", dOffsetValueY: float=0.0, offsetTypeZ: Literal["Top", "Center", "Bottom"]="Center", dOffsetValueZ: float=0.0):
    """设置截面偏移。

    Args:
        nSec (int): 截面编号。
        offsetTypeY (str): Y方向偏移类型，可选值：
            * Left: 左对齐
            * Middle: 居中对齐
            * Right: 右对齐
        dOffsetValueY (float): Y方向偏移值（单位：m）。
            偏移类型为 Manual 时生效。
        offsetTypeZ (str): Z方向偏移类型，可选值：
            * Top: 顶部对齐
            * Center: 居中对齐
            * Bottom: 底部对齐
        dOffsetValueZ (float): Z方向偏移值（单位：m）。
            偏移类型为 Manual 时生效。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 设置截面Y方向左对齐，Z方向底部对齐
        >>> result = section_offset(1, "Left", 0.0, "Bottom", 0.0)
        >>> print(result)
        (True, "")

        >>> # 设置截面Y方向右对齐，Z方向居中对齐
        >>> result = section_offset(1, "Right", 0.0, "Center", 0.0)
        >>> print(result)
        (True, "")

    """
    pass

@REGISTRY.register('SectionMesh')
def osis_section_mesh(nSec: int=1, nPartID: int=1, nMeshMethod: Literal[0, 1]=0, dMeshSize: float=0.0):
    """设置截面网格。

    Args:
        nSec (int): 截面编号。
        nPartID (int): 分部编号，混凝土截面需输入 1，模板组合截面输入 2。
        nMeshMethod (int): 定义截面网格划分方法，可选值：
            * 0 = 自动划分
            * 1 = 手动划分
        dMeshSize (float): 网格划分尺寸，在 nMeshMethod=1 时该项起作用

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    """
    pass

@REGISTRY.register('SectionMat')
def osis_section_mat(index: int=1, *mat_nos: int):
    """
    定义组合截面的分部材料（仅用于组合截面）

    对应 C++: SectionMat, nSec, 材料号...

    Args:
        index: 组合截面编号
        mat_nos: 各分部的材料编号。模板组合截面给 2 个，顺序为钢材、混凝土；
            自定义组合截面按分部顺序给 N 个。
            弹性模量比、密度比、泊松比由 OSIS 依据材料自动算出。

    Returns:
        tuple (bool, str): 是否成功、失败原因
    """
    pass

@REGISTRY.register('SectionDel')
def osis_section_del(nSec: int):
    """删除截面

    Args:
        nSec (int): 截面编号。

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('SectionMod')
def osis_section_mod(nOld: int, nNew: int):
    """修改截面

    Args:
        nOld (int): 旧截面编号
        nNew (int): 新截面编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

# StressPoint, SecIndex, PartID, PointIndex, CoordX, CoordY
# 简介：修改截面应力点
# SecIndex：截面编号
# PartID：分部编号，混凝土截面需输入1
# PointIndex：应力点编号
# CoordX：应力点x坐标
# CoordY：应力点y坐标
# 注：

@REGISTRY.register('StressPoint')
def osis_stress_point(nSec, nPartID, nPoint, dCoordX, dCoordY):
    '''
    修改截面应力点

    nSec (int): 截面编号
    nPartID (int): 分部编号，混凝土截面需输入1
    nPoint (int): 应力点编号
    dCoordX (int): 应力点 x 坐标
    dCoordY (int): 应力点 y 坐标

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("ExportSecPic")
def osis_export_section_pic(nSec: int):
    '''
    生成截面图片，会在 image/section/ 目录下生成一张 {nSec}.jpg

    Args:
        nSec (int): 要生成图片的截面编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass
