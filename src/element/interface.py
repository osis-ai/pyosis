"""
Interfaces of OSIS functions

========

"""


from typing import Any, Dict, Literal
from ..core import OSISEngine, REGISTRY


# @REGISTRY.register("Element")
# def osis_element(nEle: int, eElementType: Literal["BEAM3D", "TRUSS", "SPRING", "CABLE", "SHELL"], params: Dict[str, Any]):
#     '''
#     创建单元
    
#     Args:
#         nEle (int): 单元编号
#         eElementType (str): 单元类型，不区分大小写。BEAM3D = 梁柱单元，TRUSS = 桁架单元，SPRING = 弹簧单元，CABLE = 拉索单元，SHELL = 壳单元
#         params (Dict[str, Any]): 对应单元类型所需要的参数
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     e = OSISEngine.GetInstance()
#     eElementType = eElementType.upper()
#     return e.OSIS_Element(nEle, eElementType, params)

@REGISTRY.register("Element")
def osis_element_beam3d(nEle: int, eElementType: str="BEAM3D", nNode1: int=1, nNode2: int=2, nMat: int=1, nSec1: int=1, nSec2: int=1, 
                        nYTrans: Literal[1, 2, 3, 4]=1, nZTrans: Literal[1, 2, 3, 4]=1, dStrain: float=0.0, bFlag: bool=0, dTheta: float=0, bWarping: bool=0):
    '''
    创建梁柱单元
    
    Args:
        nEle (int): 单元编号。从 1 开始编号，所有类型的单元均使用同一编号序列。
        eElementType (str): 不能修改，固定为 BEAM3D，不区分大小写
        nNode1 (int): 节点1编号
        nNode2 (int): 节点2编号
        nMat (int): 材料编号
        nSec1 (int): 截面1编号
        nSec2 (int): 截面2编号
        nYTrans (int): y轴截面变化次方，可选值：1, 2, 3, 4
        nZTrans (int): z轴截面变化次方，可选值：1, 2, 3, 4
        dStrain (float): 应变值。默认为 0.00
        bFlag (int): 轴向转角定义方式：
            * 0: 使用beta角定义
            * 1: 使用关键点定义
        dTheta (float): 轴向转角参数：
            * bFlag=0时: 轴向转角(beta角)
            * bFlag=1时: 关键点
        bWarping (int): 翘曲效应标志：
            * 1: 考虑翘曲
            * 0: 不考虑翘曲
        
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Element")
def osis_element_truss(nEle: int=1, eElementType: str="TRUSS", nNode1: int=1, nNode2: int=2, nMat: int=1, nSec1: int=1, nSec2: int=1, dStrain: float=0.0):
    '''
    创建桁架单元
    
    Args:
        nEle (int): 单元编号。从 1 开始编号，所有类型的单元均使用同一编号序列。
        eElementType (str): 不能修改，固定为 TRUSS，不区分大小写
        nNode1 (int): 节点1编号
        nNode2 (int): 节点2编号
        nMat (int): 材料编号
        nSec1 (int): 截面1编号
        nSec2 (int): 截面2编号
        dStrain (float): 应变值，默认为 0.00
        
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Element")
def osis_element_spring(nEle: int=1, eElementType: str="SPRING", nNode1: int=1, nNode2: int=2, bLinear: int=1, dx: float=10, dy: float=10, dz: float=10, rx: float=10, ry: float=10, rz: float=10, dBeta: float=0.0):
    '''
    创建弹簧单元
    
    Args:
        nEle (int): 单元编号。从 1 开始编号，所有类型的单元均使用同一编号序列。
        eElementType (str): 不能修改，固定为 SPRING，不区分大小写
        nNode1 (int): 节点1编号
        nNode2 (int): 节点2编号
        bLinear (int): 弹簧类型标志：
            * 1: 线性弹簧
            * 0: 非线性弹簧
        dx (float/int): x方向自由度参数：
            * 线性弹簧(bLinear=1): 局部坐标系下dx方向的刚度值
            * 非线性弹簧(bLinear=0): 局部坐标系下dx方向的力-位移曲线编号(PUCurve定义)
        dy (float/int): y方向自由度参数：
            * 线性弹簧(bLinear=1): 局部坐标系下dy方向的刚度值
            * 非线性弹簧(bLinear=0): 局部坐标系下dy方向的力-位移曲线编号(PUCurve定义)
        dz (float/int): z方向自由度参数：
            * 线性弹簧(bLinear=1): 局部坐标系下dz方向的刚度值
            * 非线性弹簧(bLinear=0): 局部坐标系下dz方向的力-位移曲线编号(PUCurve定义)
        rx (float/int): 绕x轴旋转自由度参数：
            * 线性弹簧(bLinear=1): 局部坐标系下rx方向的刚度值
            * 非线性弹簧(bLinear=0): 局部坐标系下rx方向的力-位移曲线编号(PUCurve定义)
        ry (float/int): 绕y轴旋转自由度参数：
            * 线性弹簧(bLinear=1): 局部坐标系下ry方向的刚度值
            * 非线性弹簧(bLinear=0): 局部坐标系下ry方向的力-位移曲线编号(PUCurve定义)
        rz (float/int): 绕z轴旋转自由度参数：
            * 线性弹簧(bLinear=1): 局部坐标系下rz方向的刚度值
            * 非线性弹簧(bLinear=0): 局部坐标系下rz方向的力-位移曲线编号(PUCurve定义)
        dBeta (float): 轴向转角(beta角)。默认为 0。
        
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Element")
def osis_element_cable(nEle: int=1, eElementType: str="CABLE", nNode1: int=1, nNode2: int=2, nMat: int=1, nSec: int=1, eMethod: Literal["UL", "IF", "HF", "VF", "IS"]="UL", dPara: float="10.0"):
    '''
    创建弹簧单元
    
    Args:
        nEle (int): 单元编号。从 1 开始编号，所有类型的单元均使用同一编号序列。
        eElementType (str): 不能修改，固定为 CABLE，不区分大小写
        nNode1 (int): 节点1编号。
        nNode2 (int): 节点2编号。
        nMat (int): 材料编号。
        nSec (int): 截面编号。
        eMethod (str): 拉索参数定义方法，可选值：
            * UL: 无应力长度控制
            * IF: 初拉力控制
            * HF: 水平力控制
            * VF: 竖向力控制
            * IS: 初应变控制
        dPara (float): 拉索参数值，根据eMethod的不同代表：
            * UL: 无应力长度
            * IF: 初拉力大小
            * HF: 水平力大小
            * VF: 竖向力大小
            * IS: 初应变值
        
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Element")
def osis_element_shell(nEle: int=1, eElementType: str="CABLE", bIsThin: bool=1, nMat: int=1, nThk: int=1, nNode1: int=1, nNode2: int=2, nNode3: int=3, nNode4: int = None):
    '''
    创建弹簧单元
    
    Args:
        nEle (int): 单元编号。从 1 开始编号，所有类型的单元均使用同一编号序列。
        eElementType (str): 不能修改，固定为 SHELL，不区分大小写
        bIsThin (bool): 
        nMat (int): 材料编号。
        nThk (int): 
        nNode1 (int): 节点1编号。
        nNode1 (int): 节点2编号。
        nNode1 (int): 节点3编号。
        nNode1 (int): 节点4编号，可缺省
        
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("ElementDel")
def osis_element_del(nEle: int=1):
    """删除一个单元

    Args:
        nEle (int): 单元编号，从 1 开始计数

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("ElementMod")
def osis_element_mod(nOld: int=1, nNew: int=2):
    """修改一个单元的编号。单元编号存在时，交换

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register("EleGrp")
def osis_element_group(strName: str="单元组1", eOP: Literal["c", "a", "s", "r", "aa", "ra", "m", "d"]='a', param: list=[1]):
    '''
    分配边界给节点(一般支撑，节点弹性支撑)
    
    Args:
        strName (str): 边界编号
        eOP (str): 操作
            * c = 创建
            * a = 添加
            * s = 替换
            * r = 移除
            * aa = 添加全部
            * ra = 移除全部
            * m = 修改组名
            * d = 删除
        param (list): 待操作的编号，支持的格式：*，*to*；*by*，仅用于替换。例子：[2,3,5,8to10] [2by3,5by6,8by10] 重合的编号自动忽略
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

