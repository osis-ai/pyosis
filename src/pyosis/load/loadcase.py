"""
Interfaces of OSIS functions

========

荷载工况相关

"""
from typing import Literal
from ..core import REGISTRY


@REGISTRY.register("LoadCase")
def osis_loadcase(strName: str="自定义工况1", eLoadCaseType: Literal["USER", "D", "DC", "DW", "DD", "CS"]="USER", dScalar: float=1.0, strPrompt: str =""):
    '''
    创建荷载工况

    Args:
        strName (str): 荷载工况名称
        eLoadCaseType (str): 荷载工况类型，不区分大小写。 
            * USER = 用户定义的荷载
            * D = 桥规(JTJ 021-89)中的荷编号1(结构重力)
            * DC = 结构和非结构附属荷载
            * DW = 铺装和设备荷载
            * DD = 桩端摩擦力
            * CS = 施工阶段荷载
        dScalar (float): 系数，默认1.0
        strPrompt (str): 说明，默认空
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register('LoadCaseDel')
def osis_loadcase_del(strName: str="自定义工况1"):
    '''
    删除荷载工况

    Args:
        strName (str): 荷载工况名称
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LCMod")
def osis_loadcase_mod(strOldName: str="自定义工况1", strNewName: str="自定义工况2"):
    '''
    定义或修改荷载工况

    Args:
        strOldName (str): 旧名称
        strNewName (str): 新名称
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass