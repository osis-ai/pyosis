'''
pyosis.property.damping 的 Docstring

阻尼模型
'''

from ..core import REGISTRY

@REGISTRY.register('DampingDel')
def osis_damping_del(strName: str):
    """删除阻尼模型

    Args:
        strName (str): 阻尼模型的名称

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('DampingMod')
def osis_damping_mod(strOld: str, strNew: str):
    """修改一个阻尼模型的名称。阻尼模型名称存在时，交换

    Args:
        strOld (str): 旧编号
        strNew (str): 新编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

