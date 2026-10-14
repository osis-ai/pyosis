from typing import Literal

from pyosis.core import REGISTRY

@REGISTRY.register("ShellThk")
def osis_shell_thickness(nIndex: int, nIsUniform: Literal[0, 1], dInPlane: float, dOutPlane: float,
                         nHasOffset: Literal[0, 1] = 0, nIsRelative: Literal[0, 1] = 0,
                         dThkRatio: float = 1.0, dOffsetDistance: float = 0.0) -> tuple[bool, str]:
    """
    创建或修改板或壳的厚度特性

    Args:
        nIndex (int): 厚度特性编号
        nIsUniform (int): 面内面外厚度是否相同，1=相同，0=不同
        dInPlane (float): 面内厚度，大于 0
        dOutPlane (float): 面外厚度，大于 0。仅 nIsUniform=0 时有效
        nHasOffset (int): 是否有偏移
        nIsRelative (int): 偏移是否按相对值给定
        dThkRatio (float): 厚度比
        dOffsetDistance (float): 偏移距离

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("ShellThkDel")
def osis_shell_thickness_del(nIndex: int) -> tuple[bool, str]:
    """
    删除板或壳的厚度特性

    Args:
        nIndex (int): 厚度特性编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("ShellThkMod")
def osis_shell_thickness_mod(nOldIndex: str, nNewIndex: str) -> tuple[bool, str]:
    """
    修改编号

    Args:
        nOldIndex (str): 旧编号
        nNewIndex (str): 新编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

