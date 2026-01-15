from typing import Dict, Any, Literal
from ..core import REGISTRY

# @REGISTRY.register("LiveGrade")
# def osis_live_grade(strName: str, 
#                     eCode: Literal["JTGD60_2015", "CUSTOM"], 
#                     eLiveLoadType: Literal["HIGHWAY_I", "HIGHWAY_II", "VEHICLE", "CROWD", "FATIGUE_I", "FATIGUE_II", "FATIGUE_III"], 
#                     params: Dict[str, Any]):
#     '''
#     定义活载

#     Args:
#         strName (str): 名称
#         eCode (str): 规范类型，JTGD60_2015，不区分大小写
#         eLiveLoadType (str): 活载类型，不区分大小写
#         params (dict): 附加参数
#             - CROWD: eBridgeType=桥类型, dPara=人群横向宽度
#             - FATIGUE_II: dCenterDis=车辆中心间距
    
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     e = OSISEngine.GetInstance()
#     eCode = eCode.upper()
#     eLiveLoadType = eLiveLoadType.upper()
#     return e.OSIS_LiveGrade(strName, eCode, eLiveLoadType, params)
@REGISTRY.register("LiveGrade")
def osis_livegrade_highway(strName: str="活载-HIGHWAY", eCode: str="JTGD60_2015", eLiveLoadType: Literal["HIGHWAY_I", "HIGHWAY_II"]="HIGHWAY_I"):
    '''
    定义活载-公路活载

    Args:
        strName (str): 名称
        eCode (str): 规范类型，不区分大小写，固定为 JTGD60_2015
        eLiveLoadType (str): 活载类型，不区分大小写
            * HIGHWAY_I: 公路I级
            * HIGHWAY_II: 公路II级
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LiveGrade")
def osis_livegrade_highway(strName: str="活载-HIGHWAY", eCode: str="JTGD60_2015", eLiveLoadType: Literal["VEHICLE"]="VEHICLE"):
    '''
    定义活载-车辆荷载

    Args:
        strName (str): 名称
        eCode (str): 规范类型，不区分大小写，固定为 JTGD60_2015
        eLiveLoadType (str): 活载类型，不区分大小写，固定为 VEHICLE

        dPara (float): 人群横向宽度
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LiveGrade")
def osis_livegrade_crowd(strName: str="活载-CROWD", eCode: str="JTGD60_2015", eLiveLoadType: str="CROWD", eBridgeType: Literal["BRIDGE_COMMON", "BRIDGE_CROWD_WITH", "BRIDGE_CROWD_ONLY"]="BRIDGE_COMMON", dPara: float=10):
    '''
    定义活载-人群荷载

    Args:
        strName (str): 名称
        eCode (str): 规范类型，JTGD60_2015，不区分大小写
        eLiveLoadType (str): 活载类型，不区分大小写，固定为 CROWD
        eBridgeType (str): 桥类型，不区分大小写
            * BRIDGE_COMMON 一般桥
            * BRIDGE_CROWD_WITH 行人密集桥
            * BRIDGE_CROWD_ONLY 专用行人桥
        dPara (float): 人群横向宽度
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LiveGrade")
def osis_livegrade_fatigue(strName: str="活载-FATIGUE", eCode: str="JTGD60_2015", eLiveLoadType: Literal["FATIGUE_I", "FATIGUE_II", "FATIGUE_III"]="FATIGUE_I",  dPara: float=None):
    '''
    定义活载-疲劳模型

    Args:
        strName (str): 名称
        eCode (str): 规范类型，JTGD60_2015，不区分大小写
        eLiveLoadType (str): 活载类型，不区分大小写
            * FATIGUE_I 疲劳模型I
            * FATIGUE_II 疲劳模型II
            * FATIGUE_III 疲劳模型III
        dPara (float): 车辆中心间距，仅 eLiveLoadType 为 FATIGUE_II 时需要填写
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LiveGradeDel")
def osis_livegrade_del(strName: str="活载1"):
    '''
    删除活载等级
    
    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LiveGradeMod")
def osis_livegrade_mod(strOldName: str, strNewName: str):
    '''
    修改编号
    
    Args:
        strOldName (str): 旧名称
        strOldName (str): 新名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass
