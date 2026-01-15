"""
Interfaces of OSIS functions

========

钢束相关

"""

from typing import Literal
from ..core import REGISTRY

@REGISTRY.register("TdProp")
def osis_tendon_prop_pre_area0(strName: str="钢束特性1", eType: str="PRE", nMat: int=1, bArea: Literal[0]=0, dVal: float=10, dDeltaT: float=10, dPipe: float=10, dTensioningCoeff: float=1.0, dRelaxationCoeff: float=1.0):
    '''
    钢束特性-先张法-用户输入面积
    
    Args:
        strName (str): 钢束特性名称 
        eType (str): 钢束特性类型，固定为PRE
        nMat (int): 材料编号
        bArea (int): 0 = 用户输入，固定为0
        dVal (float): 用户输入的钢束面积
        dDeltaT (float): 与台座温差
        dPipe (float): 管道直径
        dTensioningCoeff (float): 张拉系数
        dTelaxationCoeff (float): 松弛系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdProp")
def osis_tendon_prop_pre_area1(strName: str="钢束特性1", eType: str="PRE", nMat: int=1, bArea: Literal[1]=1, eCode: Literal["GBT5224_2014", "GBT20065_2016"]="GBT5224_2014", 
                               dDiameter: float=1, nNum: int=10, dDeltaT: float=10, dPipe: float=10, dTensioningCoeff: float=1.0, dRelaxationCoeff: float=1.0):
    '''
    钢束特性-先张法-按规范输入面积
    
    Args:
        strName (str): 钢束特性名称 
        eType (str): 钢束特性类型，固定为PRE
        nMat (int): 材料编号
        bArea (int): 1 = 按规范输入，固定为1
        eCode (str): 规范名
            * GBT5224_2014
            * GBT20065_2016
        dDiameter (float): 公称直径
        nNum (int)：每束钢束根数
        dDeltaT (float): 与台座温差
        dPipe (float): 管道直径
        dTensioningCoeff (float): 张拉系数
        dTelaxationCoeff (float): 松弛系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdProp")
def osis_tendon_prop_in_area0(strName: str="钢束特性1", eType: str="IN", nMat: int=1, bArea: Literal[0]=0, eCode: Literal["GBT5224_2014", "GBT20065_2016"]="GBT5224_2014", 
                               dDiameter: float=1, nNum: int=10, dDeltaT: float=10, dPipe: float=10, 
                               dFrictionCoeff: float=1.0, dDeviationCoeff: float=1.0, dStartingDefor: float=0.0, dEndDefor: float=0.0, dTensioningCoeff: float=1, dRelaxationCoeff: float=1.0):
    '''
    钢束特性-先张法-用户输入
    
    Args:
        strName (str): 钢束特性名称 
        eType (str): 钢束特性类型，固定为IN
        nMat (int): 材料编号
        bArea (int): 0 = 用户输入，固定为0
        dVal (float): 用户输入的钢束面积
        dPipe (float): 管道直径
        frictionCoeff (float): 摩擦系数
        deviationCoeff (float): 偏差系数
        startingDefor (float): 起点变形
        endDefor (float): 终点变形
        dTensioningCoeff (float): 张拉系数
        dTelaxationCoeff (float): 松弛系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdProp")
def osis_tendon_prop_in_area1(strName: str="钢束特性1", eType: str="IN", nMat: int=1, bArea: Literal[1]=1, eCode: Literal["GBT5224_2014", "GBT20065_2016"]="GBT5224_2014", 
                               dDiameter: float=1, nNum: int=10, dDeltaT: float=10, dPipe: float=10, 
                               dFrictionCoeff: float=1.0, dDeviationCoeff: float=1.0, dStartingDefor: float=0.0, dEndDefor: float=0.0, dTensioningCoeff: float=1, dRelaxationCoeff: float=1.0):
    '''
    钢束特性-先张法-按规范输入面积
    
    Args:
        strName (str): 钢束特性名称 
        eType (str): 钢束特性类型，固定为IN
        nMat (int): 材料编号
        bArea (int): 1 = 按规范输入，固定为1
        eCode (str): 规范名
            * GBT5224_2014
            * GBT20065_2016
        dDiameter (float): 公称直径
        nNum (int)：每束钢束根数
        dPipe (float): 管道直径
        frictionCoeff (float): 摩擦系数
        deviationCoeff (float): 偏差系数
        startingDefor (float): 起点变形
        endDefor (float): 终点变形
        dTensioningCoeff (float): 张拉系数
        dTelaxationCoeff (float): 松弛系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdProp")
def osis_tendon_prop_ex_area0(strName: str="钢束特性1", eType: str="EX", nMat: int=1, bArea: Literal[0]=0, eCode: Literal["GBT5224_2014", "GBT20065_2016"]="GBT5224_2014", 
                               dDiameter: float=1, nNum: int=10, dDeltaT: float=10, dPipe: float=10, 
                               dFrictionCoeff: float=1.0, dStartingDefor: float=0.0, dEndDefor: float=0.0, dTensioningCoeff: float=1, dRelaxationCoeff: float=1.0):
    '''
    钢束特性-后张法体外-用户输入
    
    Args:
        strName (str): 钢束特性名称 
        eType (str): 钢束特性类型，固定为EX
        nMat (int): 材料编号
        bArea (int): 0 = 用户输入，固定为0
        dVal (float): 用户输入的钢束面积
        dPipe (float): 管道直径
        frictionCoeff (float): 摩擦系数
        startingDefor (float): 起点变形
        endDefor (float): 终点变形
        dTensioningCoeff (float): 张拉系数
        dTelaxationCoeff (float): 松弛系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdProp")
def osis_tendon_prop_ex_area1(strName: str="钢束特性1", eType: str="EX", nMat: int=1, bArea: Literal[1]=1, eCode: Literal["GBT5224_2014", "GBT20065_2016"]="GBT5224_2014", 
                               dDiameter: float=1, nNum: int=10, dDeltaT: float=10, dPipe: float=10, 
                               dFrictionCoeff: float=1.0, dStartingDefor: float=0.0, dEndDefor: float=0.0, dTensioningCoeff: float=1, dRelaxationCoeff: float=1.0):
    '''
    钢束特性-后张法体外-按规范输入面积
    
    Args:
        strName (str): 钢束特性名称 
        eType (str): 钢束特性类型，固定为EX
        nMat (int): 材料编号
        bArea (int): 1 = 按规范输入，固定为1
        eCode (str): 规范名
            * GBT5224_2014
            * GBT20065_2016
        dDiameter (float): 公称直径
        nNum (int)：每束钢束根数
        dPipe (float): 管道直径
        frictionCoeff (float): 摩擦系数
        startingDefor (float): 起点变形
        endDefor (float): 终点变形
        dTensioningCoeff (float): 张拉系数
        dTelaxationCoeff (float): 松弛系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdPropDel")
def osis_tendon_prop_del(strName: str="钢束特性1"):
    '''
    删除钢束特性
    
    Args:
        strName (str): 钢束特性名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdPropMod")
def osis_tendon_prop_mod(strOldName: str="钢束特性1", strNewName: str="钢束特性2"):
    '''
    定义或修改荷载工况

    Args:
        strOldName (str): 旧名称
        strNewName (str): 新名称
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdShape")
def osis_tendon_shape_spl3d(strName: str="钢束形状1", nNum: int=10, strProp: str="钢束特性1", strElementGroup: str="单元组1", strLayoutType: Literal["SPL3D"]="SPL3D", strCurveName: str="样条曲线1"):
    '''
    定义钢束形状-3D样条

    Args:
        strName (str): 名称
        nNum (int): 钢束数量
        strProp (str): 钢束特性
        strElementGroup (str): 作用的单元组
        strLayoutType (str): 形状类型，固定为SPL3D
        strCurveName (str): 样条曲线名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdShape")
def osis_tendon_shape_arc3d(strName: str="钢束形状1", nNum: int=10, strProp: str="钢束特性1", strElementGroup: str="单元组1", strLayoutType: Literal["ARC3D"]="ARC3D", strCurveName: str="样条曲线1"):
    '''
    定义钢束形状-3D圆弧

    Args:
        strName (str): 名称
        nNum (int): 钢束数量
        strProp (str): 钢束特性
        strElementGroup (str): 作用的单元组
        strLayoutType (str): 形状类型，固定为ARC3D
        strCurveName (str): 样条曲线名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdShape")
def osis_tendon_shape_arc2d(strName: str="钢束形状1", nNum: int=10, strProp: str="钢束特性1", strElementGroup: str="单元组1", strLayoutType: Literal["ARC2D"]="ARC2D", eType: Literal[0, 1]=1, param: list=["样条曲线1", "样条曲线2"]):
    '''
    定义钢束形状-2D圆弧

    Args:
        strName (str): 名称
        nNum (int): 钢束数量
        strProp (str): 钢束特性
        strElementGroup (str): 作用的单元组
        strLayoutType (str): 形状类型，固定为ARC3D
        eType (int): 参考类型
            * 0 = 距离
            * 1 = 坐标
        param (list): 
            - eType = 0 时需要填入：
                竖弯参考位置-梁顶缘线，
                竖弯样条曲线名称，
                平弯参考位置-梁中心线，
                平弯样条曲线名称
            - eType = 1 时需要填入：
                竖弯样条曲线名称，
                平弯样条曲线名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdShapeDel")
def osis_tendon_shape_del(strName: str="钢束形状1"):
    '''
    删除钢束形状

    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("TdShapeMod")
def osis_tendon_shape_mod(strOldName: str="钢束形状1", strNewName: str="钢束形状2"):
    '''
    修改钢束形状

    Args:
        strOldName (str): 钢束形状名称
        strNewName (str): 新名称
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LayoutTS")
def osis_layout_tendons(strShapeName: str="钢束形状1", eLayoutType: Literal["ELEMENT"]="ELEMENT", nEle: int=1, nBeg: Literal[0, 1]=0, nDir: Literal[0, 1]=0, dOffsetX: float=0.0, dOffsetY: float=0.0, dOffsetZ: float=0.0):
    '''
    修改钢束形状

    Args:
        strShapeName (str): 钢束形状名称
        eLayoutType (str): 分配钢束形状的方法，ELEMENT = 参考单元分配
        nEle (int): 参考单元编号
        nBeg (int): 起点
            * 0 = i
            * 1 = j
        nDir (int): 方向
            * 0 = i->j
            * 1 = j->i
        dOffsetX (float): x方向起点偏移
        dOffsetY (float): y方向起点偏移
        dOffsetZ (float): z方向起点偏移
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("WipeTS")
def osis_wipe_tendons(strShapeName: str="钢束形状1"):
    '''
    擦除已布置钢束形状

    Args:
        strShapeName (str): 钢束形状名称
       
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass
