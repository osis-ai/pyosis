from typing import Dict, Any, Literal
from ..core import REGISTRY

@REGISTRY.register("LiveAnal")
def osis_live_analysis(strName: str, strCode: str, eSubCmbType: Literal[1, 0]):
    '''
    定义或修改活载工况

    Args:
        strName (str): 活载工况名
        strCode (str): 规范名，计算冲击系数和横向折减
        eSubCmbType (int): 子工况组合类型
            * 1 = 单独（包络）
            * 0 = 组合（相加）
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("LiveAnalDel")
def osis_live_analysis_del(strName: str):
    '''
    删除活载工况
    
    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("LiveAnalMod")
def osis_live_analysis_mod(strOldName: str, strNewName: str):
    '''
    修改活载工况名称
    
    Args:
        strOldName (str): 旧名称
        strOldName (str): 新名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("LiveAnalInc")
def osis_live_analysis_inc(strName: str, eOP: Literal["a", "m"], strLiveSubName: str, strLiveGradeName: str, dFactor: int, bFlage: bool, 
                           eBridgeType: Literal['SIMPLE', "CONTINUOUS", "ARCH", "CABLE_STAYED", "CABLE_STAYED_AUS", "SUSPENSION", "CUSTOM"], param: list['int'], lane: list['str']):
    # Name, OP, LiveSub, LiveGrade, factor, muFlag,  bridgeType, para_i..., LaneLoad_i, LaneLoad_j, ... 
    '''
    定义活载工况，加入或修改子工况
    
    Args:
        strName (str): 活载工况名称
        eOP (str): 操作
            * a = 添加
            * m = 修改
        strLiveSubName (str): 子工况名称
        strLiveGradeName (str): 活载名（osis_livegrade定义）
        dFactor (int): 缩放系数
        bFlag: 是否考虑冲击系数
            * 1 = 考虑
            * 0 = 不考虑
        eBridgeType (str): 按照计算冲击系数划分的桥型
            * SIMPLE                = 简支梁桥
            * CONTINUOUS            = 连续梁桥
            * ARCH                  = 拱桥
            * CABLE_STAYED          = 斜拉桥（无辅助墩）
            * CABLE_STAYED_AUS      = 斜拉桥（有辅助墩）
            * SUSPENSION            = 悬索桥
            * CUSTOM = 自定义，用户直接输入基频
        param (list): 计算冲击系数的参数或冲击系数
            * SIMPLE	            = 桥长、弹模、惯性矩、质量
            * CONTINUOUS	        = 基频计算常数a、基频计算常数b、桥长、弹模、惯性矩、质量
            * ARCH	                = 拱厚变化系数、拱桥矢跨比、桥长、弹模、惯性矩，质量
            * CABLE_STAYED	        = 计算常数、主跨跨径
            * CABLE_STAYED_AUX	    = 计算常数、主跨跨径
            * SUSPENSION	        = 主跨跨径、弹模、惯性矩、主缆水平拉力、质量
            * CUSTOM	            = 用户直接输入基频

        lane (list): 车道线名

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("LiveAnalInc")
def osis_live_analysis_inc_mod(strName: str, eOP: Literal["d", "mn"], strLiveSubName: str, strNewName: str=None):
    # Name, OP, LiveSub, LiveGrade, factor, muFlag,  bridgeType, para_i..., LaneLoad_i, LaneLoad_j, ... 
    '''
    定义活载工况，删除或修改子工况
    
    Args:
        strName (str): 活载工况名称
        eOP (str): 操作
            * d = 删除
            * mn = 修改名称
        strLiveSubName (str): 子工况名称
        strNewName (str): 新的名称，eOP = d 时不需要

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass
