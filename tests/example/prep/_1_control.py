from pyosis.core.engine import OSISEngine

def setup_control(engine: OSISEngine) -> None:
    """设置全局控制参数"""
    control = engine.control
    control.set_gravity_acceleration(9.8066)
    control.set_calc_tendon(True)
    control.set_calc_concurrent_force(True)
    control.set_calc_shrink(True)
    control.set_calc_creep(True)
    control.set_calc_shear(True)
    control.set_calc_relaxation(True)
    control.set_mod_loc_coor(False)
    control.set_inc_tendon(True)
    control.set_nonlinear(False, False)
    control.set_line_search(False)
    control.set_auto_time_step(True)
    control.set_substitution_steps(1, 20)
    control.set_modal_opt(0)

if __name__ == "__main__":
    from _0_engine import engine
    setup_control(engine)