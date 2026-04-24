from pyosis.core.engine import OSISEngine

def setup_property(engine: OSISEngine) -> list[str]:
    """设置几何属性（钢束线型等）"""
    geometry = engine.geometry
    geometry.create_arc3d("钢束-1-N1", "TENDON", [1.50000E-01,0.00000E+00,-7.50000E-01,0.00000,
                                                1.72307E+00,0.00000E+00,-8.60000E-01,20.00000,
                                                1.42169E+01,0.00000E+00,-8.60000E-01,20.00000,
                                                1.57900E+01,0.00000E+00,-7.50000E-01,0.00000])
    geometry.create_arc3d("钢束-2-N2", "TENDON", [1.50000E-01,0.00000E+00,-3.50000E-01,0.00000,
                                                2.67550E+00,0.00000E+00,-7.50000E-01,10.00000,
                                                1.32645E+01,0.00000E+00,-7.50000E-01,10.00000,
                                                1.57900E+01,0.00000E+00,-3.50000E-01,0.00000])
    geo_names = ["钢束-1-N1", "钢束-2-N2"]          # 暂时先这样
    return geo_names

if __name__ == "__main__":
    from ._0_engine import engine
    geo_names = setup_property(engine)
    print(geo_names)
