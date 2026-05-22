"""
pyosis.dynamic.load_to_mass 的 Docstring

荷载转换质量底层命令接口
"""

from typing import Literal
from ..core import REGISTRY


@REGISTRY.register("LTMAnal")
def osis_ltm_anal(strName: str):
    """创建或修改荷载转换质量总体信息。

    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Note:
        - 无论荷载工况是否被激活，均可转化为质量
    """
    pass


@REGISTRY.register("LTMAnalDel")
def osis_ltm_anal_del(strName: str):
    """删除荷载转换质量。

    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("LTMAnalMod")
def osis_ltm_anal_mod(old_name: str, new_name: str):
    """修改荷载转换质量名称。

    Args:
        old_name (str): 旧名称
        new_name (str): 新名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("LTMAnalInc")
def osis_ltm_anal_inc(
    strName: str,
    strOp: Literal["a", "r"],
    strLcName: str,
    dMassFactor: float,
    dG: float,
    bX: Literal[0, 1] = 1,
    bY: Literal[0, 1] = 1,
    bZ: Literal[0, 1] = 1,
    bNF: Literal[0, 1] = 1,
    bBF: Literal[0, 1] = 1,
    bSF: Literal[0, 1] = 1,
):
    """创建或修改荷载转换质量项。

    Args:
        strName (str): 荷载转换质量标识
        strOp (str): 操作类型，"a"=添加，"r"=移除
        strLcName (str): 荷载工况名称
        dMassFactor (float): 质量系数
        dG (float): 重力加速度值
        bX (int): 质量方向，0=不考虑X向参与，1=考虑X向参与
        bY (int): 质量方向，0=不考虑Y向参与，1=考虑Y向参与
        bZ (int): 质量方向，0=不考虑Z向参与，1=考虑Z向参与
        bNF (int): 0=不转换节点荷载，1=转换节点荷载
        bBF (int): 0=不转换梁荷载，1=转换梁荷载
        bSF (int): 0=不转换面荷载，1=转换面荷载

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 添加荷载转换质量项
        >>> result = osis_ltm_anal_inc("LTM1", "a", "D", 1.0, 9.806, 1, 1, 1, 1, 1, 1)
        >>> print(result)
        (True, "")

        >>> # 移除荷载转换质量项
        >>> result = osis_ltm_anal_inc("LTM1", "r", "D", 1.0, 9.806)
        >>> print(result)
        (True, "")

    Note:
        - 无论荷载工况是否被激活，均可转化为质量
    """
    pass
