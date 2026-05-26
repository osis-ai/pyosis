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
def osis_boundary_master_slave(nBd: int, eBoundaryType: Literal["MSTSLV"]="MSTSLV", nNode: int = 1, bX: bool = 1, bY: bool = 1, bZ: bool = 1, bRX: bool = 1, bRY: bool = 1, bRZ: bool = 1, bCoincident: bool = 1):
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
        bCoincident: 0 = 仅同位移约束，默认1
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Boundary")
def osis_boundary_rigid(nBd: int, eBoundaryType: Literal["RIGID"], nNodeI: int):
    '''
    ## 定义或修改刚性连接
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 RIGID 
        nNodeI (int): 节点1编号

    Notes: 用于形成刚性区域的节点号nodeJ, nodeK, ... , nodeL由osis_assign_boundary定义
        
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
        eBoundaryType (str): 固定为 RELEASE
        \\*_state (bool): 
            * 0 = 完全释放
            * 1 = 完全约束
        F\\*i and M\\*i (float): 部分约束的大小，0-1之间，表示释放后残余的约束能力的百分比
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
def osis_boundary_general_elstcspt(
    nBd: int,
    eBoundaryType: Literal["GES"],
    nCoor: int | str,
    *params: float,
):
    '''
    ## 定义或修改一般弹性支承
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 GES
        nCoor (int | str): 局部坐标系编号，"" 代表缺省
        *params (float): 变长参数序列，按以下顺序排列：
            K11,K12,K13,K14,K15,K16,
            K22,K23,K24,K25,K26,
            K33,K34,K35,K36,
            K44,K45,K46,
            K55,K56,
            K66,
            bM,
            [M11,M12,...,M66（当bM=1时）],
            bC,
            [C11,C12,...,C66（当bC=1时）]
            其中 Kij/Mij/Cij 为上三角矩阵元素，必须全部给出。
            bM/bC: 0=不考虑，1=考虑
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("Boundary")
def osis_boundary_section_factor(
    nBd: int,
    eBoundaryType: Literal["SECF"],
    Area: float,
    Sy: float,
    Sz: float,
    Ixx: float,
    Iyy: float,
    Izz: float,
    Iww: float,
    W: float,
):
    '''
    ## 修改截面特性
    
    Args:
        nBd (int): 边界编号
        eBoundaryType (str): 固定为 SECF
        Area (float): 面积调整系数
        Sy (float): Y向剪切常数调整系数
        Sz (float): Z向剪切常数调整系数
        Ixx (float): X轴抗扭惯性矩调整系数
        Iyy (float): Y轴抗弯惯性矩调整系数
        Izz (float): Z轴抗弯惯性矩调整系数
        Iww (float): 翘曲惯性矩调整系数
        W (float): 自重调整系数
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


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