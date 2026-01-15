"""
Interfaces of OSIS functions

========

"""


from ..core import OSISEngine, REGISTRY

@REGISTRY.register("Acel")
def osis_acel(dG: float = 9.8066):
    '''
    定义或修改重力加速度值
    
    Args:
        dG (float): 重力加速度值
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("CalcTendon")
def osis_calc_tendon(bFlag: int=1):
    '''
    是否计算预应力
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("CalcConForce")
def osis_calc_con_force(bFlag: int=1):
    '''
    是否计算并发反力
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("CalcShrink")
def osis_calc_shrink(bFlag: int=1):
    '''
    是否计算收缩
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("CalcCreep")
def osis_calc_creep(bFlag: int=1):
    '''
    是否计算徐变
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("CalcCreep")
def osis_calc_shear(bFlag: int=1):
    '''
    是否计算剪切
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("CalcRlx")
def osis_calc_rlx(bFlag: int=1):
    '''
    是否计算钢束松弛
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("ModLocCoor")
def osis_mod_loc_coor(bFlag: int=1):
    '''
    是否修改变截面单元局部坐标轴来计算内力/应力
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("IncTendon")
def osis_inc_tendon(bFlag: int=1):
    '''
    是否考虑钢束自重及钢束对截面几何特性的影响
    
    Args:
        bFlag (bool): 1=开，0=关

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

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

@REGISTRY.register("ModOpt")
def osis_mod_opt(nMod: int=1):
    '''
    定义模态分析所需的特征值最大数目
    
    Args:
        nMod (int): 需要计算的特征值最大数目（缺省值：1）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass
