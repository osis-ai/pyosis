"""几何属性"""

from pyosis.core.engine import OSISEngine

def build_property(engine: OSISEngine) -> list[str]:
    """设置几何属性（钢束线型、车道线等）"""

    geo_names = []

    spline = engine.geometry.create_arc3d('BD1', 'TENDON', [0.2801, 0, -1.8, 0, 2.16733, 0, -2.02088, 10, 10.0001, 0, -2.08039, 0.05, 15.1985, 0, -2.19886, 10, 17.4321, 0, -1.80191, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('BD2', 'TENDON', [0.2801, 0, -1.8, 0, 2.4161, 0, -2.05, 10, 6.0001, 0, -2.05, 0.05, 10.0001, 0, -2.08039, 0.05, 14.0001, 0, -2.17155, 0.05, 19.2193, 0, -2.36979, 10, 21.4341, 0, -1.9761, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('BD3', 'TENDON', [0.28, 0, -1.8, 0, 2.416, 0, -2.05, 10, 6, 0, -2.05, 0.05, 10, 0, -2.08039, 0.05, 14, 0, -2.17155, 0.05, 18, 0, -2.32348, 0.05, 23.2926, 0, -2.60493, 8, 24.4245, 0, -2.4029, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('BT1', 'TENDON', [0.3, 0, -0.5, 0, 2.79, 0, -0.15, 8, 7.4, 0, -0.15, 8, 9.349, 0, -0.6, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('BT2', 'TENDON', [0.3, 0, -0.5, 0, 2.79, 0, -0.15, 8, 11.4, 0, -0.15, 8, 13.349, 0, -0.6, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('BT3', 'TENDON', [0.3, 0, -0.5, 0, 2.79, 0, -0.15, 8, 15.4, 0, -0.15, 8, 17.349, 0, -0.6, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F0', 'TENDON', [-4.85, 0, -2.93, 0, -2.114, 0, -1.35, 6, 0, 0, -1.35, 6, 2.114, 0, -1.35, 6, 4.85, 0, -2.93, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F1', 'TENDON', [-8.35, 0, -2.85, 0, -5.493, 0, -1.2, 8, 0, 0, -1.2, 8, 5.493, 0, -1.2, 8, 8.35, 0, -2.85, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F2', 'TENDON', [-11.85, 0, -2.55, 0, -9.252, 0, -1.05, 8, 0, 0, -1.05, 8, 9.252, 0, -1.05, 8, 11.85, 0, -2.55, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F3', 'TENDON', [-15.35, 0, -2.25, 0, -13.012, 0, -0.9, 6, 0, 0, -0.9, 6, 13.012, 0, -0.9, 6, 15.35, 0, -2.25, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F4', 'TENDON', [-18.85, 0, -2.05, 0, -16.599, 0, -0.75, 6, 0, 0, -0.75, 6, 16.599, 0, -0.75, 6, 18.85, 0, -2.05, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F5', 'TENDON', [-22.85, 0, -1.9, 0, -20.599, 0, -0.6, 6, 0, 0, -0.6, 6, 20.599, 0, -0.6, 6, 22.85, 0, -1.9, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F6', 'TENDON', [-26.85, 0, -1.75, 0, -24.599, 0, -0.45, 6, 0, 0, -0.45, 6, 24.599, 0, -0.45, 6, 26.85, 0, -1.75, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F7', 'TENDON', [-30.85, 0, -1.6, 0, -28.599, 0, -0.3, 6, 0, 0, -0.3, 6, 28.599, 0, -0.3, 6, 30.85, 0, -1.6, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('F8', 'TENDON', [-34.85, 0, -1.45, 0, -32.599, 0, -0.15, 6, 0, 0, -0.15, 6, 32.599, 0, -0.15, 6, 34.85, 0, -1.45, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T0', 'TENDON', [-5, 0, -0.4, 0, 0, 0, -0.4, 10, 5, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T1', 'TENDON', [-8.5, 0, -0.4, 0, 0, 0, -0.4, 10, 8.5, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T2', 'TENDON', [-12, 0, -0.4, 0, 0, 0, -0.4, 10, 12, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T3', 'TENDON', [-15.499, 0, -0.4, 0, -13.807, 0, -0.4, 10, -12.022, 0, -0.15, 10, 0, 0, -0.15, 10, 12.022, 0, -0.15, 10, 13.807, 0, -0.4, 10, 15.499, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T4', 'TENDON', [-18.999, 0, -0.4, 0, -17.307, 0, -0.4, 10, -15.522, 0, -0.15, 10, 0, 0, -0.15, 10, 15.522, 0, -0.15, 10, 17.307, 0, -0.4, 10, 18.999, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T5', 'TENDON', [-22.999, 0, -0.4, 0, -21.307, 0, -0.4, 10, -19.522, 0, -0.15, 10, 0, 0, -0.15, 10, 19.522, 0, -0.15, 10, 21.307, 0, -0.4, 10, 22.999, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T6', 'TENDON', [-27, 0, -0.4, 0, 0, 0, -0.4, 10, 27, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T7', 'TENDON', [-30.999, 0, -0.4, 0, -29.307, 0, -0.4, 10, -27.522, 0, -0.15, 10, 0, 0, -0.15, 10, 27.522, 0, -0.15, 10, 29.307, 0, -0.4, 10, 30.999, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T8', 'TENDON', [-34.999, 0, -0.4, 0, -33.307, 0, -0.4, 10, -31.522, 0, -0.15, 10, 0, 0, -0.15, 10, 31.522, 0, -0.15, 10, 33.307, 0, -0.4, 10, 34.999, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('T9', 'TENDON', [-38.999, 0, -0.4, 0, -37.307, 0, -0.4, 10, -35.522, 0, -0.15, 10, 0, 0, -0.15, 10, 35.522, 0, -0.15, 10, 37.307, 0, -0.4, 10, 38.999, 0, -0.4, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z1', 'TENDON', [-4.5, 0, -1.62659, 0, -2.068, 0, -2.05, 10, 0, 0, -2.05, 10, 2.068, 0, -2.05, 10, 4.5, 0, -1.62659, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z2', 'TENDON', [-8.5, 0, -1.69015, 0, -6.15505, 0, -2.10671, 10, -5.00005, 0, -2.08039, 0.1, -1.00005, 0, -2.05, 0.1, 1, 0, -2.05, 0.1, 6.24974, 0, -2.08988, 10, 8.5, 0, -1.69015, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z3', 'TENDON', [-12.4999, 0, -1.80449, 0, -10.2715, 0, -2.20053, 10, -4.9999, 0, -2.08039, 0.1, -0.999898, 0, -2.05, 0.1, 1.00015, 0, -2.05, 0.1, 5.00015, 0, -2.08039, 0.1, 9.00015, 0, -2.17155, 0.1, 10.1821, 0, -2.21614, 10, 12.5002, 0, -1.80449, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z4', 'TENDON', [-16.4978, 0, -1.95961, 0, -14.1197, 0, -2.38293, 10, -12.6367, 0, -2.3098, 0.1, -9.00245, 0, -2.17161, 0.1, -5.00017, 0, -2.0804, 0.1, -0.998463, 0, -2.05, 0.1, 1.00273, 0, -2.05, 0.1, 5.00443, 0, -2.0804, 0.1, 9.00671, 0, -2.17161, 0.1, 12.0463, 0, -2.28766, 0.1, 14.0856, 0, -2.38985, 10, 16.5023, 0, -1.95966, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z5', 'TENDON', [-20.4989, 0, -2.22549, 0, -18.2509, 0, -2.62672, 10, -16.4389, 0, -2.50626, 0.1, -13.0047, 0, -2.32364, 0.1, -9.00245, 0, -2.17161, 0.1, -5.00017, 0, -2.0804, 0.1, -0.998463, 0, -2.05, 0.1, 1.00273, 0, -2.05, 0.1, 5.00443, 0, -2.0804, 0.1, 9.00671, 0, -2.17161, 0.1, 13.009, 0, -2.32364, 0.1, 16.1167, 0, -2.48975, 0.1, 18.2455, 0, -2.62902, 10, 20.5023, 0, -2.22632, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z6', 'TENDON', [-24.0001, 0, -2.45752, 0, -21.6591, 0, -2.87243, 10, -20.0784, 0, -2.74673, 0.1, -17.0093, 0, -2.53647, 0.1, -13.007, 0, -2.32364, 0.1, -9.00473, 0, -2.17161, 0.1, -5.00246, 0, -2.0804, 0.1, -1.00075, 0, -2.05, 0.1, 1.00044, 0, -2.05, 0.1, 5.00215, 0, -2.0804, 0.1, 9.00443, 0, -2.17161, 0.1, 13.0067, 0, -2.32364, 0.1, 17.009, 0, -2.53647, 0.1, 18.6124, 0, -2.6465, 0.1, 21.6281, 0, -2.87797, 10, 23.9999, 0, -2.4576, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z7', 'TENDON', [-27.5001, 0, -2.73656, 0, -25.1518, 0, -3.15215, 10, -21.0115, 0, -2.8101, 0.1, -17.0093, 0, -2.53647, 0.1, -13.007, 0, -2.32364, 0.1, -9.00473, 0, -2.17161, 0.1, -5.00246, 0, -2.0804, 0.1, -1.00075, 0, -2.05, 0.1, 1.00044, 0, -2.05, 0.1, 5.00215, 0, -2.0804, 0.1, 9.00443, 0, -2.17161, 0.1, 13.0067, 0, -2.32364, 0.1, 17.009, 0, -2.53647, 0.1, 21.0112, 0, -2.8101, 0.1, 25.1518, 0, -3.15218, 10, 27.4999, 0, -2.73665, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('Z8', 'TENDON', [-30.9968, 0, -3.06213, 0, -28.5786, 0, -3.48953, 10, -24.5112, 0, -3.09942, 0.1, -21.0092, 0, -2.8101, 0.1, -17.007, 0, -2.53647, 0.1, -13.0047, 0, -2.32364, 0.1, -9.00245, 0, -2.17161, 0.1, -5.00017, 0, -2.0804, 0.1, -0.998463, 0, -2.05, 0.1, 1.00273, 0, -2.05, 0.1, 5.00443, 0, -2.0804, 0.1, 9.00671, 0, -2.17161, 0.1, 13.009, 0, -2.32364, 0.1, 17.0113, 0, -2.53647, 0.1, 21.0134, 0, -2.8101, 0.1, 24.5155, 0, -3.09942, 0.1, 28.5816, 0, -3.4894, 10, 30.9991, 0, -3.06213, 0])
    geo_names.append(spline.name)

    spline = engine.geometry.create_arc3d('ZT', 'TENDON', [-12.5, 0, -0.6, 0, -11, 0, -0.15, 10, 0, 0, -0.15, 10, 11, 0, -0.15, 10, 12.5, 0, -0.6, 0])
    geo_names.append(spline.name)

    return geo_names


if __name__ == "__main__":
    from ._0_engine import engine
    geo_names = build_property(engine)
    print(geo_names)
    print(engine.geometry.all())