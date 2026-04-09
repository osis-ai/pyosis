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
def osis_boundary_general(nBd: int, eBoundaryType: Literal["GENERAL"]="GENERAL", nCoor: int = "", bX: bool = 1, bY: bool = 1, bZ: bool = 1, bRX: bool = 1, bRY: bool = 1, bRZ: bool = 1, bRW: bool = 1):
    '''
    ## 定义或修改一般边界
    pyosis.boundary.osis_boundary_general
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 GENERAL
        nCoor (int): 局部坐标系编号，"" 代表缺省
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
@REGISTRY.register("Boundary")
def osis_boundary_elstcspt(nBd: int, eBoundaryType: Literal["ELSTCSPT"]="ELSTCSPT", nCoor: int = "", bX: bool = 1, DX: int = 1e13, bY: bool = 1, DY: int = 1e13, bZ: bool = 1, DZ: int = 1e13, bRX: bool = 1, RX: int = 1e16, bRY: bool = 1, RY: int = 1e16, bRZ: bool = 1, RZ: int = 1e16):
    '''
    定义或修改弹簧单元弹性支承
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 ELSTCSPT
        nCoor (int): 局部坐标系编号，固定使用""缺省
        bX：UX方向，0 = 弹性，1 = 固定
        DX：坐标系X轴方向的弹性支承刚度
        bY：UY方向，0 = 弹性，1 = 固定
        DY：坐标系Y轴方向的弹性支承刚度
        bZ：UZ方向，0 = 弹性，1 = 固定
        DZ：坐标系Z轴方向的弹性支承刚度
        bRX：RX方向，0 = 弹性，1 = 固定
        RX：绕坐标系X轴方向的转动弹性刚度
        bRY：RY方向，0 = 弹性，1 = 固定
        RY：绕坐标系Y轴方向的转动弹性刚度
        bRZ：RZ方向，0 = 弹性，1 = 固定
        RZ：绕坐标系Z轴方向的转动弹性刚度
        注：弹性支撑与一般边界固定的自由度相同，且弹性支撑其余自由度上约束为零时，二者结果完全相同，不存在数值差异
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("Boundary")
def osis_boundary_master_slave(nBd: int, eBoundaryType: Literal["MSTSLV"]="MSTSLV", nNode: int = 1, bX: bool = 1, bY: bool = 1, bZ: bool = 1, bRX: bool = 1, bRY: bool = 1, bRZ: bool = 1):
    '''
    ## 定义或修改主从约束
    pyosis.boundary.osis_boundary_master_slave
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 MSTSLV
        nNode (int): 主节点编号
        bDX (bool): 0 = 释放，1 = 约束
        bDY (bool): 0 = 释放，1 = 约束
        bDZ (bool): 0 = 释放，1 = 约束
        bRX (bool): 0 = 释放，1 = 约束
        bRY (bool): 0 = 释放，1 = 约束
        bRZ (bool): 0 = 释放，1 = 约束
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Boundary")
def osis_boundary_release(nBd: int, eBoundaryType: Literal["RELEASE"], 
                          Fxi_state: bool, Fyi_state: bool, Fzi_state: bool, Mxi_state: bool, Myi_state: bool, Mzi_state: bool, Mbi_state: bool,
                          Fxi: float,      Fyi: float,      Fzi: float,      Mxi: float,      Myi: float,      Mzi: float,      Mbi: float,
                          Fxj_state: bool, Fyj_state: bool, Fzj_state: bool, Mxj_state: bool, Myj_state: bool, Mzj_state: bool, Mbj_state: bool,
                          Fxj: float,      Fyj: float,      Fzj: float,      Mxj: float,      Myj: float,      Mzj: float,      Mbj: float):
    '''
    ## 定义或修改释放梁端约束
    pyosis.boundary.osis_boundary_release
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 MSTSLV
        \\*_state (bool): 
            * 0 = 释放
            * 1 = 约束
        F\\*i and M\\*i (float): 部分约束的大小，0-1之间，表示释放后残余的约束能力的百分比
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

# @REGISTRY.register("Boundary")
# def osis_boundary_elastic_support(nBd: int, eBoundaryType: Literal["ELSTCSPT"], nCoor: int, bX: float, bY: float, bZ: float, bRX: float, bRY: float, bRZ: float):
#     '''
#     ## 定义或修改节点弹性支撑
#     pyosis.boundary.osis_boundary_elastic_support
    
#     Args:
#         nBd (int): 编号
#         eBoundaryType (str): 固定为 ELSTCSPT
#         nCoor (int): 局部坐标系编号
#         dDX (float): 坐标系 X 轴方向的弹性支承刚度
#         dDY (float): 坐标系 Y 轴方向的弹性支承刚度
#         dDZ (float): 坐标系 Z 轴方向的弹性支承刚度
#         dRX (float): 绕坐标系 X 轴方向的转动弹性刚度
#         dRY (float): 绕坐标系 Y 轴方向的转动弹性刚度
#         dRZ (float): 绕坐标系 Z 轴方向的转动弹性刚度
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     pass

@REGISTRY.register("AsgnBd")
def osis_assign_boundary(nBd: int=1, eOP: Literal["a", "s", "r", "aa", "ra"]="a", param: list=[]):
    '''
    ## 分配边界给节点(一般支撑，节点弹性支撑)
    pyosis.boundary.osis_assign_boundary
    
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
    ## 添加或移除边界组
    pyosis.boundary.osis_boundary_group
    
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

@REGISTRY.register("BoundaryDel")
def osis_boundary_del(nIndex:int)->tuple[bool, str]:
    """
    删除边界
    Args:
        nIndex: 边界编号

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass