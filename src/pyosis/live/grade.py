from typing import Dict, Any, Literal
from ..core import REGISTRY


@REGISTRY.register("LiveGrade")
def osis_livegrade_highway(strName: str="活载-HIGHWAY", eCode: Literal["JTGD60_2015"]="JTGD60_2015", eLiveLoadType: Literal["HIGHWAY_I", "HIGHWAY_II"]="HIGHWAY_I"):
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
def osis_livegrade_vehicle(strName: str="活载-VEHICLE", eCode: str="JTGD60_2015", eLiveLoadType: Literal["VEHICLE"]="VEHICLE"):
    '''
    定义活载-车辆荷载

    Args:
        strName (str): 名称
        eCode (str): 规范类型，不区分大小写，固定为 JTGD60_2015
        eLiveLoadType (str): 活载类型，不区分大小写，固定为 VEHICLE
    
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

@REGISTRY.register("LiveGrade")
def osis_livegrade_custom(strName: str, eCode: Literal["CUSTOM"] = "CUSTOM", eLiveLoadType: Literal["VG"] = "VG", nGrpNum: int = 1,
                          veh_grp_layout=[]):
    """定义或修改活载等级。

    Args:
        strName: 活载名称
        eCode: 规范类型，固定为 CUSTOM
        eLiveLoadType: 活载类型，轴载组为 VG
        nGrpNum: 轴载组数
        veh_grp_layout: 距左侧轴的轴距, 轴载

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("LiveGrade")
def osis_livegrade_custom_vehicle(strName: str, eCode: Literal["CUSTOM"] = "CUSTOM",
                                  eLiveLoadType: Literal["V"] = "V", VehLayout: list = None):
    """定义或修改自定义车辆活载。

    命令流：LiveGrade, Name, CUSTOM, V, 轴距, 轴载, ...

    Args:
        strName (str): 活载名称
        eCode (str): 规范类型，固定为 CUSTOM
        eLiveLoadType (str): 活载类型，固定为 V
        VehLayout (list): 各轴的（距左侧轴的轴距, 轴载），按顺序平铺填入
            [轴距1, 轴载1, 轴距2, 轴载2, ...]

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("LiveGrade")
def osis_livegrade_custom_nhwcd(strName: str, eCode: Literal["CUSTOM"] = "CUSTOM",
                                eLiveLoadType: Literal["NHWCD"] = "NHWCD",
                                qk: float = 0.0, L1: float = 0.0, Pk1: float = 0.0,
                                L2: float = 0.0, Pk2: float = 0.0):
    """定义或修改新公路车道荷载。

    命令流：LiveGrade, Name, CUSTOM, NHWCD, qk, L1, Pk1, L2, Pk2

    Args:
        strName (str): 活载名称
        eCode (str): 规范类型，固定为 CUSTOM
        eLiveLoadType (str): 活载类型，固定为 NHWCD
        qk (float): 均布荷载
        L1 (float): 跨径1
        Pk1 (float): 小于等于 L1 时的集中荷载值
        L2 (float): 跨径2
        Pk2 (float): 大于等于 L2 时的集中荷载值；L1 与 L2 之间内插

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("LiveGrade")
def osis_livegrade_custom_nhwrq(strName: str, eCode: Literal["CUSTOM"] = "CUSTOM",
                                eLiveLoadType: Literal["NHWRQ"] = "NHWRQ",
                                B: float = 0.0, L1: float = 0.0, P1: float = 0.0,
                                L2: float = 0.0, P2: float = 0.0):
    """定义或修改新公路人群荷载。

    命令流：LiveGrade, Name, CUSTOM, NHWRQ, B, L1, P1, L2, P2

    Args:
        strName (str): 活载名称
        eCode (str): 规范类型，固定为 CUSTOM
        eLiveLoadType (str): 活载类型，固定为 NHWRQ
        B (float): 人群横向宽度
        L1 (float): 跨径1
        P1 (float): 小于等于 L1 时的人群压强值
        L2 (float): 跨径2
        P2 (float): 大于等于 L2 时的人群压强值；L1 与 L2 之间内插

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("LiveGrade")
def osis_livegrade_custom_ohwrq(strName: str, eCode: Literal["CUSTOM"] = "CUSTOM",
                                eLiveLoadType: Literal["OHWRQ"] = "OHWRQ", P: float = 0.0):
    """定义或修改旧公路人群荷载。

    命令流：LiveGrade, Name, CUSTOM, OHWRQ, P

    Args:
        strName (str): 活载名称
        eCode (str): 规范类型，固定为 CUSTOM
        eLiveLoadType (str): 活载类型，固定为 OHWRQ
        P (float): 人群荷载值

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("LiveGradeDel")
def osis_livegrade_del(strName: str):
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
    修改名称
    
    Args:
        strOldName (str): 旧名称
        strOldName (str): 新名称

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass
