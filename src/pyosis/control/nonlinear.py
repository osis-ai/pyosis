from ..core import REGISTRY

@REGISTRY.register("NL")
def osis_nl(bGeom: int=0, bLink: int=0):
    '''
    非线性控制开关

    Args:
        bGeom (bool): 
            * 0 = 关闭几何非线性开关
            * 1 = 打开几何非线性开关、大位移大转角
        bLink (bool): 
            * 0 = 不考虑非线性连接单元
            * 1 = 考虑非线性连接单元

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LnSrch")
def osis_ln_srch(bFlag: int=1):
    '''
    求解设置线性搜索开关
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("AutoTs")
def osis_auto_ts(bFlag: int=1):
    '''
    是否定义自动计算时间荷载步
    
    Args:
        bFlag (bool): 1=开，0=关

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

@REGISTRY.register("ModOpt")        # 暂时先放在这
def osis_mod_opt(nMod: int=1):
    '''
    定义模态分析所需的特征值最大数目
    
    Args:
        nMod (int): 需要计算的特征值最大数目（缺省值：1）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass