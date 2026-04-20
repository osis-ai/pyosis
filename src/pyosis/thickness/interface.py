from pyosis.core import REGISTRY

@REGISTRY.register("ShellThk")
def osis_shell_thickness(nIndex: int, dInPlane: float, dOutPlane: float) -> tuple[bool, str]:
    """
    创建或修改板或壳的厚度特性

    Args:
        nIndex (int): 厚度特性编号
        dInPlane (float): 面内厚度
        dOutPlane (float): 面外厚度

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

