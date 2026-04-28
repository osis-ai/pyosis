from pyosis.core.engine import OSISEngine

def build_property(engine: OSISEngine) -> list[str]:
    """设置几何属性（钢束线型等）"""
    geometry = engine.geometry
    
    # 创建钢束线型，create_arc3d 返回 Spline 对象
    spline1 = geometry.create_arc3d("钢束-1-N1", "TENDON", [
        1.50000E-01, 0.00000E+00, -7.50000E-01, 0.00000,
        1.72307E+00, 0.00000E+00, -8.60000E-01, 20.00000,
        1.42169E+01, 0.00000E+00, -8.60000E-01, 20.00000,
        1.57900E+01, 0.00000E+00, -7.50000E-01, 0.00000,
    ])
    spline2 = geometry.create_arc3d("钢束-2-N2", "TENDON", [
        1.50000E-01, 0.00000E+00, -3.50000E-01, 0.00000,
        2.67550E+00, 0.00000E+00, -7.50000E-01, 10.00000,
        1.32645E+01, 0.00000E+00, -7.50000E-01, 10.00000,
        1.57900E+01, 0.00000E+00, -3.50000E-01, 0.00000,
    ])
    
    # 从 Spline 对象获取名称和坐标
    geo_names = [spline1.name, spline2.name]
    
    return geo_names

if __name__ == "__main__":
    from ._0_engine import engine
    geo_names = build_property(engine)
    print(geo_names)
    print(engine.geometry.all())
    # # 验证：查询并打印样条曲线坐标
    # splines = engine.geometry.all()
    # for sp in splines:
    #     print(f"\n{sp.name}: {sp.spline_type.name}")
    #     for pt in sp.points:
    #         print(f"  {pt}")
