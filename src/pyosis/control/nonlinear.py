from ..core import REGISTRY

@REGISTRY.register("NL")
def osis_nl(bGeom: int=0):
    '''
    非线性控制开关（非线性连接单元在转换时强制打开，无需参数）

    Args:
        bGeom (bool):
            * 0 = 关闭几何非线性开关
            * 1 = 打开几何非线性开关、大位移大转角

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("CnvConfig")
def osis_cnv_config(Criteria: str="F", Norm: str="L2", Val: float=1e-4):
    '''
    非线性收敛准则

    文档与旧命令流写作 CnvTol，引擎注册名为 CnvConfig。

    Args:
        Criteria (str): 收敛准则，F = 力收敛
        Norm (str): L2 = 二范数
        Val (float): 收敛阈值，须大于 0

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LnSrch")
def osis_ln_srch(bFlag: int=0):
    '''
    求解设置线性搜索开关（软件默认关闭）

    Args:
        bFlag (bool): 0=非线性搜索，1=线性搜索

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("AutoTs")
def osis_auto_ts(bFlag: int=0):
    '''
    是否定义自动计算时间荷载步（软件默认关闭）

    Args:
        bFlag (bool): 0=不自动计算时间荷载步，1=自动计算时间荷载步

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("NSUBST")
def osis_NSUBST(NLS: int, NSBMX: int):
    '''
    指定荷载步数和最大荷载子步数
    
    NLS (int): 设置荷载步
    NSBMX (int): 最大的荷载子步

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

# @REGISTRY.register("ModOpt")        # 暂时先放在这
# def osis_mod_opt(nMod: int=1):
#     '''
#     定义模态分析所需的特征值最大数目
    
#     Args:
#         nMod (int): 需要计算的特征值最大数目（缺省值：1）

#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     pass