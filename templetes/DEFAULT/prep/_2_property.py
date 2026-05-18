"""几何属性"""

from pyosis.core.engine import OSISEngine

def build_property(engine: OSISEngine) -> list[str]:
    """设置几何属性（钢束线型、车道线等）"""

    geo_names = []

    spline = engine.geometry.create_arc3d('钢束样条曲线_1-N1', 'TENDON', [0.2, 0, 1, 0, 8.1, 0, 0.31, 40, 16.1, 0, 0.31, 40, 24.7, 0, 1.15, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_1-N2', 'TENDON', [0.2, 0, 0.75, 0, 6.5, 0, 0.2, 40, 16.8, 0, 0.2, 40, 24.7, 0, 0.9, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_1-N3', 'TENDON', [0.2, 0, 0.5, 0, 4.9, 0, 0.09, 40, 18.3, 0, 0.09, 40, 24.7, 0, 0.65, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_1-N4', 'TENDON', [0.2, 0, 0.125, 0, 1.7, 0, 0.09, 30, 23.4, 0, 0.09, 30, 24.7, 0, 0.125, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N1', 'TENDON', [25.3, 0, 1.15, 0, 33.9, 0, 0.31, 40, 41.1, 0, 0.31, 40, 49.7, 0, 1.15, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N1-复制', 'TENDON', [50.3, 0, 1.15, 0, 58.9, 0, 0.31, 40, 66.1, 0, 0.31, 40, 74.7, 0, 1.15, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N1-复制01', 'TENDON', [75.3, 0, 1.15, 0, 83.9, 0, 0.31, 40, 91.1, 0, 0.31, 40, 99.7, 0, 1.15, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N2', 'TENDON', [25.3, 0, 0.9, 0, 33.2, 0, 0.2, 40, 41.8, 0, 0.2, 40, 49.7, 0, 0.9, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N2-复制', 'TENDON', [50.3, 0, 0.9, 0, 58.2, 0, 0.2, 40, 66.8, 0, 0.2, 40, 74.7, 0, 0.9, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N2-复制01', 'TENDON', [75.3, 0, 0.9, 0, 83.2, 0, 0.2, 40, 91.8, 0, 0.2, 40, 99.7, 0, 0.9, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N3', 'TENDON', [25.3, 0, 0.65, 0, 31.7, 0, 0.09, 40, 43.3, 0, 0.09, 40, 49.7, 0, 0.65, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N3-复制', 'TENDON', [50.3, 0, 0.65, 0, 56.7, 0, 0.09, 40, 68.3, 0, 0.09, 40, 74.7, 0, 0.65, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N3-复制01', 'TENDON', [75.3, 0, 0.65, 0, 81.7, 0, 0.09, 40, 93.3, 0, 0.09, 40, 99.7, 0, 0.65, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N4', 'TENDON', [25.3, 0, 0.125, 0, 26.6, 0, 0.09, 30, 48.4, 0, 0.09, 30, 49.7, 0, 0.125, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N4-复制', 'TENDON', [50.3, 0, 0.125, 0, 51.6, 0, 0.09, 30, 73.4, 0, 0.09, 30, 74.7, 0, 0.125, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_2-N4-复制01', 'TENDON', [75.3, 0, 0.125, 0, 76.6, 0, 0.09, 30, 98.4, 0, 0.09, 30, 99.7, 0, 0.125, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_5-N1', 'TENDON', [100.3, 0, 1.15, 0, 108.9, 0, 0.31, 40, 116.9, 0, 0.31, 40, 124.8, 0, 1, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_5-N2', 'TENDON', [100.3, 0, 0.9, 0, 108.2, 0, 0.2, 40, 118.5, 0, 0.2, 40, 124.8, 0, 0.75, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_5-N3', 'TENDON', [100.3, 0, 0.65, 0, 106.7, 0, 0.09, 40, 120.1, 0, 0.09, 40, 124.8, 0, 0.5, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_5-N4', 'TENDON', [100.3, 0, 0.125, 0, 101.6, 0, 0.09, 30, 123.3, 0, 0.09, 30, 124.8, 0, 0.125, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D1-T1', 'TENDON', [21, 0, 1.31, 0, 29, 0, 1.31, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D1-T2', 'TENDON', [18, 0, 1.31, 0, 32, 0, 1.31, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D2-T1-复制', 'TENDON', [46, 0, 1.31, 0, 54, 0, 1.31, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D2-T2-复制', 'TENDON', [43, 0, 1.31, 0, 57, 0, 1.31, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D3-T1-复制01', 'TENDON', [71, 0, 1.31, 0, 79, 0, 1.31, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D3-T2-复制01', 'TENDON', [68, 0, 1.31, 0, 82, 0, 1.31, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D4-T1-复制02', 'TENDON', [96, 0, 1.31, 0, 104, 0, 1.31, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('钢束样条曲线_D4-T2-复制02', 'TENDON', [93, 0, 1.31, 0, 107, 0, 1.31, 0])
    geo_names.append(spline.name)

    return geo_names


if __name__ == "__main__":
    from ._0_engine import engine
    geo_names = build_property(engine)
    print(geo_names)
    print(engine.geometry.all())