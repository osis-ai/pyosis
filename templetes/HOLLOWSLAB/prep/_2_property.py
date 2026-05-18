from pyosis.core.engine import OSISEngine

from typing import Any

def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"几何曲线属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

def build_property(engine: OSISEngine) -> list[str]:
    """设置几何属性（钢束线型等）"""
    geometry = engine.geometry
    # 样条曲线一般边界LIVE
    general_live = geometry.create_general("样条曲线一般边界LIVE","LIVE",[
        0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        2.0, 0.0, 0.0, 1.0, 0.0, 0.0
    ])
    _expect_attr(general_live, "name", "样条曲线一般边界LIVE")
    # 样条曲线一般边界TENDON
    general_tendon = geometry.create_general("样条曲线一般边界TENDON","TENDON",[
        0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        2.0, 0.0, 0.0, 1.0, 0.0, 0.0
    ])
    _expect_attr(general_tendon, "name", "样条曲线一般边界TENDON")
    # 自然边界LIVE
    natural_live = geometry.create_natural("自然边界LIVE","LIVE",[
        0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        2.0, 0.0, 0.0, 3.0, 0.0, 0.0,
        4.0, 0.0, 0.0, 5.0, 0.0, 0.0
    ])
    _expect_attr(natural_live, "name", "自然边界LIVE")

    # 自然边界TENDON
    natural_tendon = geometry.create_natural("自然边界TENDON","TENDON",[
        0.0, 0.0, 0.0, 1.5, 0.0, 0.0,
        2.5, 0.0, 0.0, 3.5, 0.0, 0.0,
        4.5, 0.0, 0.0, 5.5, 0.0, 0.0
    ])
    _expect_attr(natural_tendon, "name", "自然边界TENDON")

    # 2D圆弧TENDON
    arc2d = geometry.create_arc2d("2D圆弧TENDON","TENDON",[
        0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        2.0, 0.0, 0.0, 1.0, 0.0, 0.0
    ])
    _expect_attr(arc2d, "name", "2D圆弧TENDON")

    # 创建钢束线型，create_arc3d 返回 Spline 对象
    spline1 = geometry.create_arc3d("钢束-1-N1", "TENDON", [
        1.50000E-01, 0.00000E+00, -7.50000E-01, 0.00000,
        1.72307E+00, 0.00000E+00, -8.60000E-01, 20.00000,
        1.42169E+01, 0.00000E+00, -8.60000E-01, 20.00000,
        1.57900E+01, 0.00000E+00, -7.50000E-01, 0.00000,
    ])
    _expect_attr(spline1, "name", "钢束-1-N1")

    # 三维样条曲线-arc3d
    spline2 = geometry.create_arc3d("钢束-2-N2", "TENDON", [
        1.50000E-01, 0.00000E+00, -3.50000E-01, 0.00000,
        2.67550E+00, 0.00000E+00, -7.50000E-01, 10.00000,
        1.32645E+01, 0.00000E+00, -7.50000E-01, 10.00000,
        1.57900E+01, 0.00000E+00, -3.50000E-01, 0.00000,
    ])
    _expect_attr(spline2, "name", "钢束-2-N2")

    # 三维样条曲线-arc2d
    arc2d1 = geometry.create_arc2d(
      "钢束-1-N1-竖弯",
      "TENDON",
      [
          1.50000e-01, -7.50000e-01, 2.00000e01,
          1.72307e00, -8.60000e-01, 2.00000e01,
          1.42169e01, -8.60000e-01, 2.00000e01,
          1.57900e01, -7.50000e-01, 2.00000e01,
      ],
    )
    _expect_attr(arc2d1, "name", "钢束-1-N1-竖弯")

    arc2d2 = geometry.create_arc2d(
      "钢束-1-N1-平弯",
      "TENDON",
      [
          0.0300, 0.0, 1.0e4,
          7.5000, 0.0, 1.0e4,
          15.3200, 0.0, 1.0e4,
      ],
    )
    _expect_attr(arc2d2, "name", "钢束-1-N1-平弯")

    all_geometry = geometry.all()
    if len(all_geometry) <= 0:
        raise ValueError("geometry.all() 为空，期望至少存在 1 条几何曲线")

    # 删除
    geometry.delete("样条曲线一般边界LIVE")
    geometry.delete("样条曲线一般边界TENDON")
    geometry.delete("自然边界LIVE")
    geometry.delete("2D圆弧TENDON")

    # 从 Spline 对象获取名称和坐标
    geo_names = [spline1.name,spline2.name,natural_tendon.name,arc2d1.name,arc2d2.name]
    
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
