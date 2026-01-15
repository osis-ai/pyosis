'''
pyosis.property.pu_curve 的 Docstring

荷载-位移曲线
'''

from ..core import REGISTRY

@REGISTRY.register("PUCurve")
def osis_pu_curve(nIndex: int, strName: str, eType: int, nNum: int, displacement: list[float], force: list[float]):
    '''
    创建或修改荷载-位移曲线，荷载与位移需要唯一对应
    
    Args:
        nIndex (int): 位移-力（矩）曲线编号
        strName (str): 曲线名称
        eType (str): 
            * 0 = 力
            * 1 = 力矩
        nNum (int): 曲线点数
        displacement (list): i个点的位移值
        force (list): i个点的力（矩）值

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register('PUCurveDel')
def osis_pu_curve_del(nNO: int=1):
    """删除荷载-位移曲线

    Args:
        nNO (int): 荷载-位移曲线编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('PUCurveMod')
def osis_pu_curve_mod(nOld: int=1, nNew: int=2):
    """修改一个荷载-位移曲线的编号。荷载-位移曲线编号存在时，交换

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

