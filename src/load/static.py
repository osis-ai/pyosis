"""
Interfaces of OSIS functions

========

静力荷载相关

"""


from typing import Literal
from ..core import REGISTRY


# @REGISTRY.register("Load")
# def osis_load(eLoadType: Literal["GRAVITY", "NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"], strLCName: str, params: Dict[str, Any]):
#     '''
#     创建荷载
    
#     Args:
#         eLoadType (str): 荷载类型，不区分大小写。 GRAVITY = 自重荷载，NFORCE = 节点荷载，LINE = 线荷载，DISPLACEMENT = 强迫位移，INITIAL = 初始内力，
#             UTEMP = 均匀温度荷载，GTEMP = 梯度温度荷载， PST = 预应力，CFORCE = 索力
#         strLCName (str): 工况名称
#         params (Dict[str, Any]): 对应荷载类型所需要的参数
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     pass

@REGISTRY.register("Load")
def osis_load_gravity(eType: str="GRAVITY", strLCName: str="自定义工况1", dXCoeff: float=1.0, dYCoeff: float=1.0, dZCoeff: float=1.0):
    '''
    创建或修改自重荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 GRAVITY
        strLCName (str): 荷载工况名称
        nEntity (int): 节点编号
        dXCoeff (float): 全局坐标系x方向的系数，将作用于重力加速度
        dYCoeff (float): 全局坐标系y方向的系数，将作用于重力加速度
        dZCoeff (float): 全局坐标系z方向的系数，将作用于重力加速度
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_nforce(eType: str="NFORCE", strLCName: str="自定义工况1", nEntity: int=1, dFx: float=100, dFy: float=0, dFz: float=0, dMx: float=0, dMy: float=0, dMz: float=0):
    '''
    创建或修改节点荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 NFORCE
        strLCName (str): 荷载工况名称
        nEntity (int): 节点编号
        dFx (float): 全局坐标系x方向的集中力
        dFy (float): 全局坐标系y方向的集中力
        dFz (float): 全局坐标系z方向的集中力
        dMx (float): 全局坐标系x方向的集中弯矩
        dMy (float): 全局坐标系y方向的集中弯矩
        dMz (float): 全局坐标系z方向的集中弯矩
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_line(eType: str="LINE", strLCName: str="自定义工况1", nEntity: int=1, eCoordSystem: Literal[0, 1]=1, eLoadType: Literal[0, 1]=1, 
                   dOffsetXI: float=0, dOffsetYI: float=0, dOffsetZI: float=0, dFXI: float=100, dFYI: float=100, dFZI: float=0, dMXI: float=0, dMYI: float=0, dMZI: float=0):
    '''
    创建或修改任意线荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 LINE
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eCoordSystem (int): 
            * 0-单元坐标系
            * 1-整体坐标系
        eLoadType (int):
            * 0-连续荷载
            * 1-离散荷载
        dOffsetXI (float):  I端偏移量X/L，输入范围[0,1]
        dOffsetYI (float):  I端Y轴偏移量
        dOffsetZI (float):  I端Z轴偏移量
        dFXI (float): I端坐标系x方向的集中力
        dFYI (float): I端坐标系y方向的集中力
        dFZI (float): I端坐标系z方向的集中力
        dMXI (float): I端坐标系x方向的集中弯矩
        dMYI (float): I端坐标系y方向的集中弯矩
        dMZI (float): I端坐标系z方向的集中弯矩
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_displacement(eType: str="DISPLACEMENT", strLCName: str="自定义工况1", nEntity: int=1, dDx: float=100, dDy: float=0, dDz: float=0, dRx: float=0, dRy: float=0, dRz: float=0):
    '''
    创建或修改强迫位移

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 DISPLACEMENT
        strLCName (str): 荷载工况名称
        nEntity (int): 节点编号
        dDx (float): 强制位移在坐标系x方向的分量
        dDy (float): 强制位移在坐标系y方向的分量
        dDz (float): 强制位移在坐标系z方向的分量
        dRx (float): 绕坐标系x轴的强制旋转角度分量
        dRy (float): 绕坐标系y轴的强制旋转角度分量
        dRz (float): 绕坐标系z轴的强制旋转角度分量
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_initial(eType: str="INITIAL", strLCName: str="自定义工况1", nEntity: int=1, dFXI: float=100, dFYI: float=100, dFZI: float=0, dMXI: float=0, dMYI: float=0, dMZI: float=0):
    '''
    创建或修改任初始内力

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 LINE
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        dFXI (float): I端坐标系x方向的集中力
        dFYI (float): I端坐标系y方向的集中力
        dFZI (float): I端坐标系z方向的集中力
        dMXI (float): I端坐标系x方向的集中弯矩
        dMYI (float): I端坐标系y方向的集中弯矩
        dMZI (float): I端坐标系z方向的集中弯矩
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_utemp(eType: str="UTEMP", strLCName: str="自定义工况1", nEntity: int=1, eDirect: Literal["X", "Y", "Z"]="X", dTemp: float=1.0, dLength: float=None):
    '''
    创建或修改均匀温度荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 UTEMP
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eDirect (str): 作用方向。单元坐标系X（轴向）/Y/Z方向温差，均匀升降温数值（正为升温）
            * X: 可用来模拟整体升降温荷载
            * Y: 可以用来模拟单元的横向梯度温度荷载
            * Z: 可以用来模拟单元的横向梯度温度荷载
        dTemp (float): 温差值，不影响系统温度
        dLength (float): Y/Z方向的长度，为 "" 则自动通过截面计算
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_gtemp(eType: str="UTEMP", strLCName: str="自定义工况1", nEntity: int=1, eDirect: Literal["Y", "Z"]="Y", eGTempType: Literal["R", "T", "C", "B"]="R", nNum: int=1, param: list=["", 10, 10, 0, 0]):
    '''
    创建或修改梯度温度荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 UTEMP
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eDirect (str): 局部方向
            * Y
            * Z
        eGTempType (str): 定义梁的参考位置
            * R
            * T
            * C
            * B
        nNum (int): 梯度温度荷载段数
        param (list): 每个梯度温度荷载段对应一组参数，多组参数直接全部按顺序填入param中即可
            - B (float): 考虑温度变化的宽度，宽度可设置为空("")
            - H1 (float): 参考位置至定义温度间距离
            - T1 (float): H1处对应温度
            - H2 (float): 参考位置至定义温度间距离
            - T2 (float): H2处对应温度
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_pst(eType: str="PST", strLCName: str="自定义工况1", strEntity: str="钢束1", eTensionType: Literal["BOTH", "BEG", "END"]="BOTH", eTensionForceType: Literal["ST", "IF"]="ST", dBeg: float=100, dEnd: float=100):
    '''
    创建或修改预应力荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 PST
        strLCName (str): 荷载工况名称
        strEntity (str): 钢束形状名称，由TdShape定义
        eTensionType (str): 张拉类型
            * BOTH = 两端张拉
            * BEG = 起点张拉
            * END = 终点张拉
        eTensionForceType (str): 张拉力类型
            * ST = 应力
            * IF = 内力
        dBeg (float): 起点应力或内力。eTensionType 为 END 填 None
        dEnd (float): 终点应力或内力。eTensionType 为 BEG 填 None
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_cforce(eType: str="CFORCE", strLCName: str="自定义工况1", nEntity: int=1, eLoadType: Literal["IN", "EX"]="IN", dForce: float=100):
    '''
    创建或修改索力

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 CFORCE
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eLoadType (str): 施加方式
            * In = 体内力
            * Ex = 体外力
        dForce (float): 索力数值
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LoadDel")
def osis_load_del(eType: Literal["GRAVITY", "NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"]="NFORCE", strLCName: str="自定义工况1", entity: int|str=1):
    '''
    删除荷载

    Args:
        eType (str): 荷载类型，不区分大小写
            * GRAVITY = 自重荷载
            * NFORCE = 节点荷载
            * LINE = 线荷载
            * DISPLACEMENT = 强迫位移荷载
            * INITIAL = 初始内力荷载
            * UTEMP = 均匀温度荷载
            * GTEMP = 梯度温度荷载
            * PST = 预应力荷载
            * CFORCE = 索力荷载
        strLCName (str): 荷载工况名称
        entity (int|str): 要删除的荷载所作用的节点/单元/钢束形状。eType 为 GRAVITY 时需要填 None

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LoadMod")
def osis_load_mod(eType: Literal["NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"]="NFORCE", strLCName: str="自定义工况1", oldEntity: int|str=1, newEntity: int|str=2):
    '''
    修改工况内荷载作用的单元或节点或钢束形状

    Args:
        eType (str): 荷载类型，不区分大小写
            * NFORCE = 节点荷载
            * LINE = 线荷载
            * DISPLACEMENT = 强迫位移荷载
            * INITIAL = 初始内力荷载
            * UTEMP = 均匀温度荷载
            * GTEMP = 梯度温度荷载
            * PST = 预应力荷载
            * CFORCE = 索力荷载
        strLCName (str): 荷载工况名称
        oldEntity (int|str): 旧编号
        newEntity (int|str): 新编号

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

