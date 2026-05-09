"""全局控制参数"""

from pyosis.core.engine import OSISEngine

def setup_control(engine: OSISEngine) -> None:
    """设置全局控制参数"""

    engine.control.set_gravity_acceleration(9.8066)
    engine.control.set_calc_tendon(True)
    engine.control.set_calc_concurrent_force(True)
    engine.control.set_calc_shrink(True)
    engine.control.set_calc_creep(True)
    engine.control.set_calc_shear(True)
    engine.control.set_calc_relaxation(True)
    engine.control.set_mod_loc_coor(False)
    engine.control.set_inc_tendon(True)
    engine.control.set_nonlinear(geom=False, link=False)
    engine.control.set_line_search(False)
    engine.control.set_auto_time_step(False)
    engine.control.set_modal_opt(0)


if __name__ == "__main__":
    from ._0_engine import engine
    setup_control(engine)