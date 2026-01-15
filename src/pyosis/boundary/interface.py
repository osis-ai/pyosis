"""
Interfaces of OSIS functions

========

"""


from typing import Literal
from ..core import REGISTRY

# @REGISTRY.register("Boundary")
# def osis_boundary(nBd: int=1, eBoundaryType: Literal["GENERAL", "MSTSLV", "RELEASE", "ELSTCSPT"]="GENERAL", params: Dict[str, Any]={}):
#     '''
#     创建边界
    
#     Args:
#         nBd (int): 边界编号
#         eBoundaryType (str): 边界类型，不区分大小写。GENERAL = 一般边界，MSTSLV = 主从约束，RELEASE = 释放梁端约束，ELSTCSPT = 节点弹性支承
#         params (Dict[str, Any]): 对应边界类型所需要的参数
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     pass

@REGISTRY.register("Boundary")
def osis_boundary_general(nBd: int, eBoundaryType: Literal["GENERAL"]="GENERAL", nCoor: int = -1, bX: bool = 1, bY: bool = 1, bZ: bool = 1, bRX: bool = 1, bRY: bool = 1, bRZ: bool = 1, bRW: bool = 1):
    '''
    定义或修改一般边界
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 GENERAL
        nCoor (int): 局部坐标系编号，-1代表缺省
        bX (bool): 0 = 释放，1 = 约束
        bY (bool): 0 = 释放，1 = 约束
        bZ (bool): 0 = 释放，1 = 约束
        bRX (bool): 0 = 释放，1 = 约束
        bRY (bool): 0 = 释放，1 = 约束
        bRZ (bool): 0 = 释放，1 = 约束
        bRW (bool): 0 = 释放，1 = 约束
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("AsgnBd")
def osis_assign_boundary(nBd: int=1, eOP: Literal["a", "s", "r", "aa", "ra"]="a", param: list=[]):
    '''
    分配边界给节点(一般支撑，节点弹性支撑)
    
    Args:
        nBd (int): 边界编号
        eOP (str): 操作
            * a = 添加
            * s = 替换
            * r = 移除
            * aa = 添加全部
            * ra = 移除全部
        param (list): 待操作的编号，支持的格式：*，*to*，*by*（仅用于替换）。
            例子：[2,3,5,"8to10"] ["2by3","5by6","8by10"] 重合的编号自动忽略
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("BdGrp")
def osis_boundary_group(strName: str, eOP: Literal["c", "a", "s", "r", "aa", "ra", "m", "d"], param: list=[]):
    '''
    添加或移除边界组
    
    Args:
        strName (str): 边界组名
        eOP (str): 操作
            * c = 创建
            * a = 添加
            * s = 替换
            * r = 移除
            * aa = 添加全部
            * ra = 移除全部
            * m = 修改组名
            * d = 删除
        param (list): 待操作的编号，支持的格式：*, *to*; *by*，仅用于替换。
            例子：[2,3,5,"8to10"] ["2by3","5by6","8by10"] 重合的编号自动忽略

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass
