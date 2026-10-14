'''
pyosis.property.pu_curve 的 Docstring

荷载-位移曲线
'''

from ..core import REGISTRY

@REGISTRY.register("PUCurve")
def osis_pu_curve(nIndex: int, strName: str, eType: int, nNum: int, curve: list[float]):
    '''
    创建或修改荷载-位移曲线，荷载与位移需要唯一对应

    命令流里位移与力（矩）按点交错排列，共 2*nNum 个数。

    Args:
        nIndex (int): 位移-力（矩）曲线编号
        strName (str): 曲线名称
        eType (str):
            * 0 = 力
            * 1 = 力矩
        nNum (int): 曲线点数
        curve (list): 位移与力（矩）交错排列，共 2*nNum 个：第1点为位移、力，第2点为位移、力……

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register('PUCurveDel')
def osis_pu_curve_del(nNO: int):
    """删除位移-内力曲线

    Args:
        nNO (int): 位移-力（矩）曲线编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('PUCurveMod')
def osis_pu_curve_mod(nOld: int, nNew: int):
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

