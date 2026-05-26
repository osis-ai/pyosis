"""
Interfaces of OSIS functions

========

荷载工况相关

"""
from typing import Literal
from ..core import REGISTRY


@REGISTRY.register("LoadCase")
def osis_loadcase(strName: str="自定义工况1", eLoadCaseType: Literal["USER", "CS", "D", "PS", "EV", "EH", "SH", "CR", "B", "STL",
    "L", "IF", "CF", "LS", "BRK", "CRL", "FL", "W1", "W2", "SF", "IP",
    "WF1", "WF2", "T", "TG", "FR",
    "CFS", "CFD", "CFV", "E"]="USER", dScalar: float=1.0, strPrompt: str =None):
    '''
    创建荷载工况

    Args:
        strName (str): 荷载工况名称
        eLoadCaseType (str): 荷载工况类型，不区分大小写。 
            * USER = 用户定义的荷载
            * CS = 施工阶段荷载
            * D = 结构重力
            * PS = 预加力
            * EV = 土的重量
            * EH = 土侧压力
            * SH = 收缩
            * CR = 徐变
            * B = 水浮力
            * STL = 基础变位
            * L = 汽车荷载
            * IF = 汽车冲击力
            * CF = 汽车离心率
            * LS = 汽车引起的土侧压力
            * BRK = 汽车制动力
            * CRL = 人群荷载
            * FL = 疲劳荷载
            * W1 = 活载风
            * W2 = 极限风
            * SF = 流水压力
            * IP = 冰压力
            * WF1 = W1引起的波浪力
            * WF2 = W2引起的波浪力
            * T = 均匀温度
            * TG = 梯度温度
            * FR = 支座摩阻力
            * CFS = 船舶的撞击作用
            * CFD = 漂流物的撞击作用
            * CFV = 汽车撞击作用
            * E = 地震作用
        dScalar (float): 系数，默认1.0
        strPrompt (str): 说明，默认 None
    Returns:
        tuple (bool, str): 是否成功，失败原因
    
    Example:
        osis_loadcase("自重工况","USER",1.0,"Load")
    '''
    pass

@REGISTRY.register('LoadCaseDel')
def osis_loadcase_del(strName: str):
    '''
    删除荷载工况

    Args:
        strName (str): 荷载工况名称
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LCMod")
def osis_loadcase_mod(strOldName: str, strNewName: str):
    '''
    定义或修改荷载工况

    Args:
        strOldName (str): 旧名称
        strNewName (str): 新名称
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass