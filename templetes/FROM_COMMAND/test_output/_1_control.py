"""全局控制参数"""

from pyosis.core.engine import OSISEngine

def setup_control(engine: OSISEngine) -> None:
    """全局控制参数"""

    # [Acel] Acel
    # 原始命令: Acel,9.8066
    # 参数:
    #   dG=9.8066
    engine.control.set_gravity_acceleration(dG=9.8066)

    # [CalcTendon] CalcTendon
    # 原始命令: CalcTendon,1
    # 参数:
    #   bFlag=1
    engine.control.set_calc_tendon(bFlag=1)

    # [CalcConForce] CalcConForce
    # 原始命令: CalcConForce,1
    # 参数:
    #   bFlag=1
    engine.control.set_calc_concurrent_force(bFlag=1)

    # [CalcShrink] CalcShrink
    # 原始命令: CalcShrink,1
    # 参数:
    #   bFlag=1
    engine.control.set_calc_shrink(bFlag=1)

    # [CalcCreep] CalcCreep
    # 原始命令: CalcCreep,1
    # 参数:
    #   bFlag=1
    engine.control.set_calc_creep(bFlag=1)

    # [CalcShear] CalcShear
    # 原始命令: CalcShear,1
    # 参数:
    #   bFlag=1
    engine.control.set_calc_shear(bFlag=1)

    # [CalcRlx] CalcRlx
    # 原始命令: CalcRlx,1
    # 参数:
    #   bFlag=1
    engine.control.set_calc_relaxation(bFlag=1)

    # [ModLocCoor] ModLocCoor
    # 原始命令: ModLocCoor,0
    # 参数:
    #   bFlag=0
    engine.control.set_mod_loc_coor(bFlag=0)

    # [IncTendon] IncTendon
    # 原始命令: IncTendon,1
    # 参数:
    #   bFlag=1
    engine.control.set_inc_tendon(bFlag=1)

    return

if __name__ == "__main__":
    from ._0_engine import engine
    setup_control(engine)