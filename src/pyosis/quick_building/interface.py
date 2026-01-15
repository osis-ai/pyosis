'''
pyosis.quick_building.py.interface 的 Docstring
'''
from typing import Tuple, Literal
from ..core import *
# 未开发完

# def log_to_file(msg,fn = "D:/log.txt"):
#     fp = open("D:/log.txt", "a", encoding="utf-8")
#     fp.write(msg)
#     print(msg)
#     fp.write('\r\n')
#     fp.close()

def osis_set_qb_bridge_type(eBridgeType: Literal["HOLLOWSLAB", "SMALLBOXBEAM", "TBEAM", "CONTINUOUSSMALLBOXBEAM", "CONTINUOUSTBEAM"]):
    '''
    快速建模设置桥梁类型

    Args:
        eBridgeType (str): 桥梁类型
            * HOLLOWSLAB = 空心板
            * SMALLBOXBEAM = 小箱梁
            * TBEAM = T梁
            * CONTINUOUSSMALLBOXBEAM = 连续小箱梁
            * CONTINUOUSTBEAM = 连续T梁
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    if eBridgeType == "HOLLOWSLAB":
        return osis_run("/create,134")
    elif eBridgeType == "SMALLBOXBEAM":
        return osis_run("/create,132")
    elif eBridgeType == "TBEAM":
        return osis_run("/create,133")
    elif eBridgeType == "CONTINUOUSSMALLBOXBEAM":
        return osis_run("/create,112")
    elif eBridgeType == "CONTINUOUSTBEAM":
        return osis_run("/create,113")

    else:
        return False, "不支持的桥梁类型！"


def osis_set_qb_overall(eBridgeType: Literal["HOLLOWSLAB", "SMALLBOXBEAM", "TBEAM", "CONTINUOUSSMALLBOXBEAM", "CONTINUOUSTBEAM"], spans: list=[30], bIsElasticConnection: bool=False, 
                    dKxOfAbutment1: float=0, dKyOfAbutment1: float=0, dKzOfAbutment1: float=0, 
                    dKxOfAbutment2: float=0, dKyOfAbutment2: float=0, dKzOfAbutment2: float=0, dElasticLength: float=0.3) -> Tuple[bool, str]:
    '''
    快速建模设置桥梁总体数据

    Args:
        eBridgeType (str): 桥梁类型
            * HOLLOWSLAB = 空心板
            * SMALLBOXBEAM = 小箱梁
            * TBEAM = T梁
            * CONTINUOUSSMALLBOXBEAM = 连续小箱梁
            * CONTINUOUSTBEAM = 连续T梁
        spans (list): 跨径数据。对于 HOLLOWSLAB/SMALLBOXBEAM/TBEAM 只需要填一段即可, 对于 CONTINUOUSSMALLBOXBEAM/CONTINUOUSTBEAM 需要填写多段
        bIsElasticConnection (bool): 是否采用弹性连接
        dKxOfAbutment1 (float): Kx = 竖向，桥台一弹性连接刚度
        dKyOfAbutment1 (float): Ky = 横向，桥台一弹性连接刚度
        dKzOfAbutment1 (float): Kz = 纵向，桥台一弹性连接刚度
        dKxOfAbutment2 (float): Kx = 竖向，桥台二弹性连接刚度
        dKyOfAbutment2 (float): Ky = 横向，桥台二弹性连接刚度
        dKzOfAbutment2 (float): Kz = 纵向，桥台二弹性连接刚度

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    e = OSISEngine.GetInstance()
    return e.OSIS_QBOverall(eBridgeType, spans, bIsElasticConnection, 
                            dKxOfAbutment1, dKyOfAbutment1, dKzOfAbutment1, 
                            dKxOfAbutment2, dKyOfAbutment2, dKzOfAbutment2, dElasticLength)

def osis_set_qb_portrait(eBridgeType: Literal["HOLLOWSLAB", "SMALLBOXBEAM", "TBEAM", "CONTINUOUSSMALLBOXBEAM", "CONTINUOUSTBEAM"], dEleLengthMin: float=0.5, dEleLengthMax: float=2.0, 
                      S1: float=0.04, L1: float=0.8, F1: float=2.0, Tb: float=0.3, Tw: float=0.3, D1: float=0.54):
    '''
    快速建模设置桥梁纵向参数等

    Args:
        eBridgeType (str): 桥梁类型
            * HOLLOWSLAB = 空心板
            * SMALLBOXBEAM = 小箱梁
            * TBEAM = T梁
            * CONTINUOUSSMALLBOXBEAM = 连续小箱梁
            * CONTINUOUSTBEAM = 连续T梁
        dEleLengthMin (float): 单元尺寸参数，单元尺寸最小值
        dEleLengthMax (float): 单元尺寸参数，单元尺寸最大值
        S1 (float): 纵向参数，左梁端至跨径线长度
        L1 (float): 纵向参数，左端横梁长度
        F1 (float): 纵向参数，左渐变段长度
        Tb (float): 纵向参数，加厚截面底板厚度
        Tw (float): 纵向参数，加厚截面腹板厚度
        D1 (float): 设置参数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    e = OSISEngine.GetInstance()
    return e.OSIS_QBPortrait(eBridgeType, dEleLengthMin, dEleLengthMax, S1, L1, F1, Tb, Tw, D1)

def osis_set_qb_load(eBridgeType: Literal["HOLLOWSLAB", "SMALLBOXBEAM", "TBEAM", "CONTINUOUSSMALLBOXBEAM", "CONTINUOUSTBEAM"],     # 这个函数跟实际接口相比有简化，便于AI调用
                  dDeadLoadFactor: float=1, dPavementIntensity: float=10850, dRailIntensity: float=2120, dSidewalkIntensity: float=0, dCrowdLoad: float=0,
                  dSideBeamPointLoad: float=23770, dMiddleBeamPointLoad: float=0, 
                  dTransVehDistribution: float=1, dFundFreq: float=0, dWarming: float=20, dCooling: float=-20, 
                  T1: float=14.0, T2: float=5.5, dSupSettle: float=0):
    '''
    快速建模设置桥梁荷载
    
    Args:
        eBridgeType (str): 桥梁类型
            * HOLLOWSLAB = 空心板
            * SMALLBOXBEAM = 小箱梁
            * TBEAM = T梁
            * CONTINUOUSSMALLBOXBEAM = 连续小箱梁
            * CONTINUOUSTBEAM = 连续T梁
        dDeadLoadFactor (float): 自重系数（恒载参数），为0表示不设置。单位：N/m
        dPavementIntensity (float): 铺装荷载集度（恒载参数），为0表示不设置。单位：N/m
        dRailIntensity (float): 防撞护栏荷载集度（恒载参数），为0表示不设置。单位：N/m
        dSidewalkIntensity (float): 人行道荷载集度（恒载参数），为0表示不设置。单位：N/m
        dCrowdLoad (float): 人行道人群荷载（恒载参数），为0表示不设置。单位：N/m
        dSideBeamPointLoad (float): 端横隔板集中荷载（恒载参数），为0表示不设置。单位：N
        dMiddleBeamPointLoad (float): 中横隔板集中荷载（恒载参数），为0表示不设置。单位：N
        dTransVehDistribution (float): 移动荷载横向分布系数，为0表示不设置移动荷载
        dFundFreq (float): 结构基频，dTransVehDistribution不为0时有效，不为0则为用户自定义基频，为0则使用规范公式。单位：Hz
        dWarming (float): 温度作用整体升温。不考虑温度作用时要和dCooling一起设置为0
        dCooling (float): 温度作用整体降温。不考虑温度作用时要和dWarming一起设置为0
        T1 (float): 温度梯度 T1。不考虑温度梯度时要和T2一起设置为0
        T2 (float): 温度梯度 T2。不考虑温度梯度时要和T1一起设置为0
        dSupSettle (float): 支座沉降（沉降荷载参数），为0表示不设置。单位：m

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    bHaveDeadLoad: bool = (dDeadLoadFactor != 0)
    bHavePavement: bool = (dPavementIntensity != 0)
    bHaveRail: bool = (dRailIntensity != 0)
    bHaveSidewalk: bool = (dSidewalkIntensity != 0 or dCrowdLoad != 0) 
    bHaveSideBeam: bool = (dSideBeamPointLoad != 0)
    bHaveMiddleBeam: bool = (dMiddleBeamPointLoad != 0)
    bHaveMovingLoad: bool = (dTransVehDistribution != 0)
    bHaveTemperEff: bool = (dWarming != 0 and dCooling != 0)
    bHaveTemperGradient: bool = (T1 != 0 and T2 != 0)
    bHaveSupSettle: bool = (dSupSettle != 0)
    bIsSelfDefine: bool = (dFundFreq != 0)
    e = OSISEngine.GetInstance()
    return e.OSIS_QBLoad(eBridgeType,
                         bHaveDeadLoad, bHavePavement, bHaveRail, bHaveSidewalk, bHaveSideBeam, bHaveMiddleBeam,
                         bHaveMovingLoad, bHaveTemperEff, bHaveTemperGradient, bHaveSupSettle,
                         dDeadLoadFactor, dPavementIntensity, dRailIntensity, dSidewalkIntensity, dCrowdLoad,
                         dSideBeamPointLoad, dMiddleBeamPointLoad, 
                         dTransVehDistribution, bIsSelfDefine, dFundFreq, dWarming, dCooling, 
                         T1, T2, dSupSettle)

def osis_set_qb_tendon(eBridgeType: Literal["HOLLOWSLAB", "SMALLBOXBEAM", "TBEAM", "CONTINUOUSSMALLBOXBEAM", "CONTINUOUSTBEAM"], 
                    tendonInfo: list[dict]=[{"name": "N1", "prop": "15-5", "Le": 0.16, "He": 1.350, "A": 5, "Hm": 0.465, "R": 45, "stress": 1.395e9, "tieNums": 2},
                                            {"name": "N2", "prop": "15-5", "Le": 0.16, "He": 1.10, "A": 5, "Hm": 0.34, "R": 45, "stress": 1.395e9, "tieNums": 2},
                                            {"name": "N3", "prop": "15-6", "Le": 0.16, "He": 0.850, "A": 5, "Hm": 0.215, "R": 45, "stress": 1.395e9, "tieNums": 2},
                                            {"name": "N4", "prop": "15-6", "Le": 0.16, "He": 0.60, "A": 5, "Hm": 0.09, "R": 45, "stress": 1.395e9, "tieNums": 2},
                                            {"name": "N5", "prop": "15-5", "Le": 0.16, "He": 0.1550, "A": 2, "Hm": 0.09, "R": 45, "stress": 1.395e9, "tieNums": 2}]):
    '''
    快速建模设置桥梁钢束
    
    Args:
        eBridgeType (str): 桥梁类型
            * HOLLOWSLAB = 空心板
            * SMALLBOXBEAM = 小箱梁
            * TBEAM = T梁
            * CONTINUOUSSMALLBOXBEAM = 连续小箱梁
            * CONTINUOUSTBEAM = 连续T梁
        tendonInfo (list): 每条钢束的信息，由多个dict组成，每个dict包含：
            - name (str): 钢束名称
            - prop (str): 钢束属性，可选项：[15-2, 15-3, 15-4, ..., 15-10]
            - Le (float): 起点距边缘混凝土距离Le(m)
            - He (float): 起点距底缘距离He(m)
            - A (float): 起弯角度A(度)
            - Hm (float): 钢束中段距底缘距高Hm(m)
            - R (float): 钢束半径R(m)
            - stress (float): 张拉应力(Pa)
            - tieNums (int): 钢束束数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    e = OSISEngine.GetInstance()
    return e.OSIS_QBTendon(eBridgeType, tendonInfo)

def osis_set_qb_stage(eBridgeType: Literal["HOLLOWSLAB", "SMALLBOXBEAM", "TBEAM", "CONTINUOUSSMALLBOXBEAM", "CONTINUOUSTBEAM"], 
                   stageInfo: list[dict]=[{"stageNum": 1, "name": "主梁预制、张拉预应力", "state": "结构自重激活,横隔板荷载激活,预应力荷载", "duration": "90", "age": "7"},
                                          {"stageNum": 2, "name": "存梁", "state": "收缩徐变", "duration": "30", "age": ""},
                                          {"stageNum": 3, "name": "二期恒载", "state": "铺装、护栏、人行道等二期恒载激活", "duration": "30", "age": ""},
                                          {"stageNum": 4, "name": "徐变十年", "state": "持续十年时间", "duration": "3650", "age": ""},
                                          {"stageNum": 5, "name": "运营阶段", "state": "移动荷载、温度荷载、风荷载等运营阶段的荷载", "duration": "3650", "age": ""}]):
    '''
    快速建模设置桥梁施工阶段
    
    Args:
        eBridgeType (str): 桥梁类型
            * HOLLOWSLAB = 空心板
            * SMALLBOXBEAM = 小箱梁
            * TBEAM = T梁
            * CONTINUOUSSMALLBOXBEAM = 连续小箱梁
            * CONTINUOUSTBEAM = 连续T梁
        stageInfo (list): 每条施工阶段的信息，由多个dict组成，每个dict包含：
            - stageNum (int): 施工阶段编号
            - name (str): 施工阶段描述
            - state (str): 荷载状态
            - duration (str): 持续时间(天)，无具体数值填 ""
            - age (str): 龄期(天)，无具体数值填 ""

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    e = OSISEngine.GetInstance()
    return e.OSIS_QBStage(eBridgeType, stageInfo)

def osis_create_qb_bridge():
    '''
    开始创建桥梁

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    return osis_run("/control,quickCreateModel")
    # return osis_execute_qb("quickCreateModel")


## 老的写法，快速建模简化版

def create_simply_small_box_beam(dSpan: float) -> Tuple[bool, str]:
    '''
    快速建模-创建小箱梁

    Args:
        dSpan (float): 跨径
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    osis_run("/create,132")
    osis_run("/control,quickCreateModel")
    return True, ""

def create_simply_Tbeam(dSpan: float) -> Tuple[bool, str]:
    '''
    快速建模-创建T梁

    Args:
        dSpan (float): 跨径
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    osis_run("/create,133")
    osis_run("/control,quickCreateModel")
    return True, ""

def create_simply_hollow_slab(dSpan: float) -> Tuple[bool, str]:
    '''
    快速建模-创建空心板

    Args:
        dSpan (float): 跨径
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    osis_run("/create,134")
    osis_run("/control,quickCreateModel")
    return True, ""

def create_simply_continuous_Tbeam(dSpan: float) -> Tuple[bool, str]:
    '''
    快速建模-创建连续T梁

    Args:
        dSpan (float): 跨径
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    osis_run("/create,113")
    osis_run("/control,quickCreateModel")
    return True, ""

def create_simply_continuous_small_box(dSpan: float) -> Tuple[bool, str]:
    '''
    快速建模-创建连续小箱梁

    Args:
        dSpan (float): 跨径
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    osis_run("/create,112")
    osis_run("/control,quickCreateModel")
    return True, ""
