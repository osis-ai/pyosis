'''
pyosis.stage.overall 的 Docstring
'''

from typing import Literal
from ..core import REGISTRY


@REGISTRY("Stage")
def stage(nIndex: int, strLCName: str, nDuration: int):
    """创建或修改施工阶段

    Args:
        nIndex (int): 编号。当前版本的施工阶段编号必须连续
        strLCName (str):所赋给的施工阶段名称
        nDuration (int): 当前施工阶段持续时间

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Notes:
        施工阶段将按照编号顺序升序排列
    """
    pass

@REGISTRY("StageDel")
def stage_del(nIndex: int):
    """删除施工阶段

    Args:
        nIndex (int): 施工阶段编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
        
    """
    pass

@REGISTRY("StageIst")
def stage_insert(nInsertRef: int, nPos: Literal[0, 1], strLCName: str, nDuration: int):
    """插入施工阶段

    Args:
        nInsertRef (int): 插入的参考位置，编号
        nPos (int): 
            * 0 = 前插
            * 1 = 后插
        strLCName (str): 所插入的施工阶段名称
        nDuration (int): 当前施工阶段持续时间

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    
    Notes:
        插入的施工阶段编号只能默认

    Example:
        >>> result = stage_insert(1, 0, "阶段5-前插", 3.0)  # 在编号为1的施工阶段前插入新的施工阶段
        >>> (True, "")
        >>>

    """
    pass

@REGISTRY("StageRmv")
def stage_remove(nIndex: int):
    """移除插入的施工阶段

    Args:
        nIndex (int): 施工阶段编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
    

