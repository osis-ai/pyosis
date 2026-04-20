from ..core import REGISTRY

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

@REGISTRY.register("CalcShear")
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