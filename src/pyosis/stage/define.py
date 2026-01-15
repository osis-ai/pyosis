'''
pyosis.stage.define 的 Docstring
'''

from typing import Literal
from ..core import REGISTRY

@REGISTRY.register("StgEle")
def stage_element(nIndex: int, eOP: Literal[1, 0], eType: Literal[1, 0], strEleGroupName: str, nBirth: int, ePart: Literal[0, 1, 2]=None):
    """通过单元组激活单元

    Args:
        nIndex (int): 施工阶段编号
        eOP (int): 操作
            * 1 = 添加
            * 0 = 移除
        eType (int): 
            * 1 = 激活
            * 0 = 钝化
        strEleGroupName (str): 待操作的单元组名称
        nBirth (int): 龄期。eOP = 0 时需要设置为 None
        ePart (int): 组合结构的分部，可缺省（None）
            * 0 = 全部激活
            * 1 = 仅钢材部分
            * 2 = 仅混凝土部分
        
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Notes:
        施工阶段将按照编号顺序升序排列
    """
    pass

@REGISTRY.register("StgBd")
def stage_boundary(nIndex: int, eOP: Literal[1, 0], eType: Literal[1, 0], strEleGroupName: str):
    """通过边界组激活/钝化边界

    Args:
        nIndex (int): 施工阶段编号
        eOP (int): 操作
            * 1 = 添加
            * 0 = 移除
        eType (int): 
            * 1 = 激活
            * 0 = 钝化
        strEleGroupName (str): 待操作的单元组名称
        
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Notes:
        施工阶段将按照编号顺序升序排列
    """
    pass

@REGISTRY.register("StgLc")
def stage_loadcase(nIndex: int, eOP: Literal[1, 0], eType: Literal[1, 0], strRefLCName: str, strLCName: str):
    """激活/钝化荷载工况

    Args:
        nIndex (int): 施工阶段编号
        eOP (int): 操作
            * 1 = 添加
            * 0 = 移除
        eType (int): 
            * 1 = 激活
            * 0 = 钝化
        strRefLCName (str): 参考当前施工阶段内的工况名称
        strLCName (str): 待操作的荷载工况名称
        
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    
    Example:
        >>> stage(1,"阶段1",3.0)
        >>> stage_element(1,1,1,"墩",5.0,0)
        >>> stage_boundary(1,1,1,"固结")
        >>> stage_loadcase(1,1,1,"","自定义工况1")
        >>> result = stage_loadcase(1,1,1,"自定义工况1","自定义工况2")  # 在 自定义工况1 之后插入一个激活的 自定义工况2
        >>> (True, "")
    """
    pass

@REGISTRY.register("StgAnal")
def stage_analysis(nIndex: int, eOP: Literal[1, 0], eType: Literal["MODAL", "SETL", "RSPEC", "LIVE", "BUCKLE"], strLCName: str):
    """激活分析工况,分析工况默认在每个施工阶段的静力工况之后，不同分析工况无先后顺序

    Args:
        nIndex (int): 施工阶段编号
        eOP (int): 操作
            * 1 = 添加
            * 0 = 移除
        eType (int): 类型
            * MODAL
            * SETL
            * RSPEC
            * LIVE
            * BUCKLE
        strLCName (str): 待操作的荷载工况名称
        
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    
    Example:
        >>> stage(1,"阶段1",3.0)
        >>> stage_element(1,1,1,"墩",5.0,0)
        >>> stage_boundary(1,1,1,"固结")
        >>> stage_analysis(1,1,"MODAL")
        >>> stage_analysis(1,1,"RSPEC","反应谱1")
        >>> stage_analysis(1,1,"SETL","沉降分析")
        >>> result = stage_analysis(1,1,"LIVE","活载分析")
        >>> (True, "")
    """
    pass
