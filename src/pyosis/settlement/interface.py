"""
pyosis.settlement.interface 的 Docstring

沉降分析底层命令接口
"""

from typing import Literal
from ..core import REGISTRY


@REGISTRY.register("SetlGrp")
def osis_setl_grp(strName: str, dVal: float, nodes: list[int] | None = None):
    """创建或修改沉降组。

    Args:
        strName (str): 组名
        dVal (float): 沉降量
        nodes (list[int]): 沉降节点列表，创建时必须指定节点

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 创建包含节点 1, 2 的沉降组
        >>> result = osis_setl_grp("N1", -0.001, [1, 2])
        >>> print(result)
        (True, "")

        >>> # 修改沉降组为只包含节点 1（相当于删除节点 2）
        >>> result = osis_setl_grp("N1", -0.001, [1])
        >>> print(result)
        (True, "")

    Note:
        - 创建时必须指定节点，不能仅指定名称和沉降量
        - 重复使用组名会修改现有沉降组
    """
    pass


@REGISTRY.register("SetlGrpDel")
def osis_setl_grp_del(strName: str):
    """删除沉降组。

    Args:
        strName (str): 组名

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SetlGrpMod")
def osis_setl_grp_mod(nOld: int, nNew: int):
    """修改沉降组编号。

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SetlAnal")
def osis_setl_anal(strName: str):
    """编辑沉降荷载工况。

    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SetlAnalDel")
def osis_setl_anal_del(strName: str):
    """删除沉降荷载工况。

    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SetlAnalMod")
def osis_setl_anal_mod(nOld: int, nNew: int):
    """修改沉降荷载工况编号。

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("SetlAnalInc")
def osis_setl_anal_inc(strName: str, strOp: Literal["a", "r"], load_cases: list[str]):
    """添加或移除参与沉降分析工况的沉降组。

    Args:
        strName (str): 沉降荷载工况名称
        strOp (str): 操作类型
            * "a" = 添加
            * "r" = 移除
        load_cases (list[str]): 沉降组名称列表

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 向沉降工况 S1 添加沉降组 N1, N2
        >>> result = osis_setl_anal_inc("S1", "a", ["N1", "N2"])
        >>> print(result)
        (True, "")

        >>> # 从沉降工况 S1 移除沉降组 N1
        >>> result = osis_setl_anal_inc("S1", "r", ["N1"])
        >>> print(result)
        (True, "")

    Note:
        - 使用前先通过 osis_setl_anal 定义沉降荷载工况
    """
    pass
