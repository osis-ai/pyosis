"""
pyosis.post.display 的 Docstring

显示命令接口
"""

from typing import Literal
from ..core import REGISTRY


@REGISTRY.register("PrnEig")
def osis_prn_eig(strName: str, nIndex: int = 0):
    """显示自振模态 / 屈曲模态的特征值。

    Args:
        strName (str): 自振模态 / 屈曲模态工况名
        nIndex (int): 表格编号
            * 自振模态：0, 1, 2
            * 屈曲模态：0

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 显示屈曲模态的特征值（稳定系数）
        >>> result = osis_prn_eig("Buckl1", 0)
        >>> print(result)
        (True, "")

        >>> # 显示自振模态的特征值
        >>> result = osis_prn_eig("Modal1", 0)
        >>> print(result)
        (True, "")
    """
    pass


@REGISTRY.register("PlEig")
def osis_pl_eig(
    strName: str,
    nEigenIndex: int = 1,
    strComp: Literal["MdX", "MdY", "MdZ", "MdXY", "MdYZ", "MdXZ", "MdXYZ"] = "MdXYZ",
):
    """显示模态结果的特征向量。

    Args:
        strName (str): 模态工况名
        nEigenIndex (int): 模态阶数，1/2/.../n
        strComp (str): 模态成分
            * MdX = X方向
            * MdY = Y方向
            * MdZ = Z方向
            * MdXY = XY平面
            * MdYZ = YZ平面
            * MdXZ = XZ平面
            * MdXYZ = 三维（默认）

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 显示第1阶模态的三维特征向量
        >>> result = osis_pl_eig("Modal1", 1, "MdXYZ")
        >>> print(result)
        (True, "")

        >>> # 显示第2阶模态的X方向特征向量
        >>> result = osis_pl_eig("Modal1", 2, "MdX")
        >>> print(result)
        (True, "")
    """
    pass
