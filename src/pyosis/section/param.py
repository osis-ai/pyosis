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
        offsetTypeZ (str): Z方向偏移类型，可选值：
            * Top: 顶部对齐
            * Center: 居中对齐
            * Bottom: 底部对齐
        dOffsetValueZ (float): Z方向偏移值（单位：m）。

    Note:
        "Manual" 自 4.9.5 起被系统淘汰，命令流拒收，故不在上列可选值内。

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

@REGISTRY.register("SecPropMod")
def osis_sec_prop_mod(
    sec_index: int,
    type: Literal["Part", "Comp"],
    part_id: int,
    area: float,
    sy: float,
    sz: float,
    ixx: float,
    iyy: float,
    izz: float,
    iww: float,
    cent_y: float,
    cent_z: float,
    dy: float,
    dz: float,
    peri_o: float,
    peri_i: float,
):
    """修改截面特性。

    Args:
        sec_index (int): 截面编号。
        type (str): 特性所属范围：
            * Part: 分部截面特性
            * Comp: 组合截面特性
        part_id (int): type=Part 时为对应分部的特性；type=Comp 时为从 Part1 到当前 part_id 的组合截面特性。
            仅有一个截面分部时，Part 与 Comp 均可使用。
        area (float): 截面面积。
        sy (float): 局部坐标系 y 轴方向的剪切常数。
        sz (float): 局部坐标系 z 轴方向的剪切常数。
        ixx (float): 绕局部坐标系 x 轴的惯性矩。
        iyy (float): 绕局部坐标系 y 轴的惯性矩。
        izz (float): 绕局部坐标系 z 轴的惯性矩。
        iww (float): 翅曲惯性矩。
        cent_y (float): 质心在局部坐标系 y 轴方向的坐标值。
        cent_z (float): 质心在局部坐标系 z 轴方向的坐标值。
        dy (float): 沿局部坐标系 y 轴方向的截面偏心。
        dz (float): 沿局部坐标系 z 轴方向的截面偏心。
        peri_o (float): 截面外轮廓周长。
        peri_i (float): 截面内轮廓周长。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SectionPropFactor")
def osis_section_prop_factor(
    n_sec: int,
    area_factor: float,
    sy_factor: float,
    sz_factor: float,
    ixx_factor: float,
    iyy_factor: float,
    izz_factor: float,
):
    """设置截面特性调整系数。

    文档 v5.0 收录，当前引擎尚未注册该命令，调用会被引擎拒为未知命令。

    Args:
        n_sec (int): 截面编号。
        area_factor (float): 面积调整系数。
        sy_factor (float): Y 向剪切常数调整系数。
        sz_factor (float): Z 向剪切常数调整系数。
        ixx_factor (float): X 轴抗扭惯性矩调整系数。
        iyy_factor (float): Y 轴抗弯惯性矩调整系数。
        izz_factor (float): Z 轴抗弯惯性矩调整系数。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
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
