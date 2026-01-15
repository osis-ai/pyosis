from typing import Dict, Any, Literal
from ..core import REGISTRY

@REGISTRY.register("InflAlgo")
def osis_lane_ve(strName: str, eType: Literal["VE"], dLength: float, eOriention: Literal[-1, 0, 1], eRef: Literal[0, 1], param: list):
    # Name, type, length, vehOri, ref, par1,par2, par3
    '''
    InflAlgo 的 Docstring
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("InflAlgo")
def osis_lane_tcb(strName: str, eType: Literal["TCB"], ESel: str, dLength: float, eOriention: Literal[-1, 0, 1], eRef: Literal[0, 1], param: list):
    '''
    InflAlgo 的 Docstring
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("InflAlgoDel")
def osis_lane_del(strName: str):
    '''
    删除车道线
    
    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("InflAlgoMod")
def osis_lane_mod(strOldName: str, strNewName: str):
    '''
    修改车道线名称
    
    Args:
        strOldName (str): 旧名称
        strOldName (str): 新名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass
