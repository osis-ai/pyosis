'''
pyosis.property.creep_shrink 的 Docstring

时间依存性材料属性
'''
from ..core import REGISTRY

@REGISTRY.register("CrpShrk")
def osis_creep_shrink(nNO: int=1, strName: str="收缩徐变1", dAvgHumidity: float=70.0, nBirthTime: int=7, dTypeCoeff: float=5.0, nBirthByShrinking: int=3):
    """
    设置收缩徐变

    Args:
        nNO (int): 收缩徐变特性编号
        strName (str): 特性名称
        dAvgHumidity (float): 年平均湿度（百分比）
        nBirthTime (int): 混凝土龄期（天）
        dTypeCoeff (float): 水泥种类系数
        nBirthByShrinking (int): 收缩开始时的混凝土龄期（天数）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register('CrpShrkDel')
def osis_creep_shrink_del(nNO: int=1):
    """删除收缩徐变特性

    Args:
        nNO (int): 收缩徐变特性编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('CrpShrkMod')
def osis_creep_shrink_mod(nOld: int=1, nNew: int=2):
    """修改一个收缩徐变特性的编号。收缩徐变特性编号存在时，交换

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
