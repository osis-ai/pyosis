"""
pyosis.stability.buckling 的 Docstring

稳定分析底层命令接口
"""

from typing import Literal
from ..core import REGISTRY


@REGISTRY.register("BucklAnal")
def osis_buckl_anal(strName: str, nNum: int=1, nAccum: Literal[0, 1]=0, dScalar: float=1.0, nType: Literal[0, 1]=0):
    """定义或修改屈曲工况。

    Args:
        strName (str): 屈曲分析工况名称
        nNum (int): 模态数量
        nAccum (int): 当前施工阶段是否考虑合计，0=考虑，1=不考虑
        dScalar (float): 缩放系数
        nType (int): 荷载类型，1=可变，0=不变

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("BucklAnalDel")
def osis_buckl_anal_del(strName: str):
    """删除屈曲工况。

    Args:
        strName (str): 屈曲分析工况名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("BucklAnalMod")
def osis_buckl_anal_mod(ole_name: str, new_name: str):
    """修改屈曲工况名称。

    Args:
        ole_name (str): 旧名称
        new_name (str): 新名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("BucklAnalInc")
def osis_buckl_anal_inc(
    strName: str, 
    strOp: Literal["a", "r", "s"], 
    strLcNew: str, 
    dScalarNew: float, 
    nTypeNew: Literal[0, 1],
    strLcOld: str=None, 
    dScalarOld: float=None, 
    nTypeOld: Literal[0, 1]=None
):
    """添加、移除或替换参与屈曲分析的荷载工况。

    Args:
        strName (str): 屈曲分析工况名称
        strOp (str): 操作类型
            * "a" = 添加
            * "r" = 移除
            * "s" = 替换
        strLcNew (str): 荷载工况名称（添加/移除/新替换的工况）
        dScalarNew (float): 系数（添加/移除/新替换的系数）
        nTypeNew (int): 类型（添加/移除/新替换的类型），1=可变，0=不变
        strLcOld (str): 被替换的荷载工况名称（仅替换操作需要）
        dScalarOld (float): 被替换的系数（仅替换操作需要）
        nTypeOld (int): 被替换的类型（仅替换操作需要），1=可变，0=不变

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 添加荷载工况
        >>> result = osis_buckl_anal_inc("B1", "a", "D", 1.0, 0)
        >>> print(result)
        (True, "")

        >>> # 移除荷载工况
        >>> result = osis_buckl_anal_inc("B1", "r", "D", 1.0, 0)
        >>> print(result)
        (True, "")

        >>> # 替换荷载工况（将 D 替换为 DC）
        >>> result = osis_buckl_anal_inc("B1", "s", "DC", 1.2, 0, "D", 1.0, 0)
        >>> print(result)
        (True, "")

    Note:
        - 添加/移除操作时，strLcOld/dScalarOld/nTypeOld 参数可忽略
        - 替换操作时，strLcOld/dScalarOld/nTypeOld 参数必填
    """
    pass
