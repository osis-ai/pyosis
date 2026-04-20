'''
pyosis.property.damping 的 Docstring

阻尼模型
'''

from ..core import REGISTRY

# 5.4.1. Damping::振型阻尼
# Damping, Name, Type, Ksi
# 简介：创建或修改振型阻尼
# Name：阻尼名称
# Type：阻尼类型，Type=modal
# Ksi：振型阻尼数值
# 注：

# 5.4.2. Damping::瑞利阻尼
# Damping, Name, Type, Method, Alpha, Beta
# 简介：创建或修改Rayleigh阻尼
# Name：阻尼名称
# Type：阻尼类型，Type=ryl
# Method：阻尼输入方法，Method=1自定义因子
# Alpha：质量因子
# Beta：刚度因子
# 注：

# Damping, Name, Type, Method, Ksii, Ksij, Wi, Wj
# 简介：创建或修改Rayleigh阻尼
# Name：阻尼名称
# Type：阻尼类型，Type=ryl
# Method：阻尼输入方法，Method=0根据公式计算因子
# Ksii：阻尼比
# Ksij：阻尼比
# Wi：圆频率
# Wj：圆频率
# 注：

@REGISTRY.register("Damping")
def osis_damping_modal(strName, eType, dKsi):
    '''
    创建或修改振型阻尼
    
    Args:
        strName (str): 阻尼模型的名称
        eType (str): 阻尼类型, 固定为 "modal"
        dKsi (float): 振型阻尼数值

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("Damping")
def osis_damping_rayleigh_custom(strName, eType, bMethod, dAlpha, dBeta):
    '''
    创建或修改Rayleigh阻尼,自定义因子
    
    Args:
        strName (str): 阻尼模型的名称
        eType (str): 阻尼类型, 固定为 "ryl"
        bMethod (int): 阻尼输入方法
            * 1=自定义因子
        dAlpha (float): 质量因子
        dBeta (float): 刚度因子

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("Damping")
def osis_damping_rayleigh_formula(strName, eType, bMethod, dKsii, dKsij, dWi, dWj):
    '''
    创建或修改Rayleigh阻尼,根据公式计算因子
    
    Args:
        strName (str): 阻尼模型的名称
        eType (str): 阻尼类型, 固定为 "ryl"
        bMethod (int): 阻尼输入方法
            * 0=自定义因子
        dKsii (float): 阻尼比
        dKsij (float): 阻尼比
        dWi (float): 圆频率
        dWj (float): 圆频率

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

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

