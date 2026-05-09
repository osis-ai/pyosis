"""截面"""

from pyosis.core.engine import OSISEngine

def build_sections(engine: OSISEngine) -> list[int]:
    """创建截面，返回截面编号列表"""

    sec_nos = []

    sec = engine.section.create_conventionalbox(
        '支点截面', 4.8, 6.375, 6.375,
        3.5, 3.5, 0.8, 0.5,
        0.9, 0.8, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.7, 0.8, 0.5, 0.5,
        1, 0.5, 0.5, 0.25,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=1,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '根部截面', 4.553, 6.375, 6.375,
        3.5, 3.5, 0.75, 0.28,
        0.572, 0.75, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=2,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '标准截面', 2.2, 6.375, 6.375,
        3.5, 3.5, 0.5, 0.28,
        0.3, 0.5, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=3,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '端横梁截面', 2.2, 6.375, 6.375,
        3.5, 3.5, 0.75, 0.28,
        0.6, 0.75, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        0.848, 0.8, 0.5, 0.28,
        1, 0.5, 0.01, 0.01,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=4,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_rect(
        '截面', 'Fillet', 'Solid', 6.5,
        2, 1, 0.5, 0.5,
        1, 1, 0.5, 0.25,
        0, 1, 0.5, 0.25,
        0, 1.2, 0.8, 0.2,
        no=5,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Center', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_rect(
        '中墩截面', 'Fillet', 'Solid', 6.5,
        4, 1, 0.5, 0.5,
        1, 1, 0.5, 0.25,
        0, 1, 0.5, 0.25,
        0, 1.2, 0.8, 0.2,
        no=6,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Center', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_7', 2.2073, 6.375, 6.375,
        3.5, 3.5, 0.5139, 0.28,
        0.3008, 0.5008, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=7,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_8', 2.2654, 6.375, 6.375,
        3.5, 3.5, 0.5417, 0.28,
        0.3076, 0.5069, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=8,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_9', 2.3816, 6.375, 6.375,
        3.5, 3.5, 0.5694, 0.28,
        0.321, 0.5193, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=9,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_10', 2.5559, 6.375, 6.375,
        3.5, 3.5, 0.5972, 0.28,
        0.3411, 0.5378, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=10,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_11', 2.7883, 6.375, 6.375,
        3.5, 3.5, 0.625, 0.28,
        0.368, 0.5625, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=11,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_12', 3.0787, 6.375, 6.375,
        3.5, 3.5, 0.6528, 0.28,
        0.4016, 0.5934, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=12,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_13', 3.3806, 6.375, 6.375,
        3.5, 3.5, 0.6771, 0.28,
        0.4365, 0.6254, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=13,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_14', 3.7269, 6.375, 6.375,
        3.5, 3.5, 0.7014, 0.28,
        0.4765, 0.6622, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=14,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组1_15', 4.1177, 6.375, 6.375,
        3.5, 3.5, 0.7257, 0.28,
        0.5217, 0.7038, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=15,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_16', 4.0319, 6.375, 6.375,
        3.5, 3.5, 0.7243, 0.28,
        0.5118, 0.6946, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=16,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_17', 3.576, 6.375, 6.375,
        3.5, 3.5, 0.6985, 0.28,
        0.4591, 0.6462, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=17,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_18', 3.1852, 6.375, 6.375,
        3.5, 3.5, 0.6728, 0.28,
        0.4139, 0.6047, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=18,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_19', 2.8595, 6.375, 6.375,
        3.5, 3.5, 0.6471, 0.28,
        0.3762, 0.5701, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=19,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_20', 2.599, 6.375, 6.375,
        3.5, 3.5, 0.6176, 0.28,
        0.3461, 0.5424, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=20,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_21', 2.4244, 6.375, 6.375,
        3.5, 3.5, 0.5882, 0.28,
        0.3259, 0.5238, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=21,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_22', 2.2997, 6.375, 6.375,
        3.5, 3.5, 0.5588, 0.28,
        0.3115, 0.5106, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=22,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组2_23', 2.2249, 6.375, 6.375,
        3.5, 3.5, 0.5294, 0.28,
        0.3029, 0.5026, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=23,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_24', 2.2326, 6.375, 6.375,
        3.5, 3.5, 0.5294, 0.28,
        0.3038, 0.5035, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=24,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_25', 2.3303, 6.375, 6.375,
        3.5, 3.5, 0.5588, 0.28,
        0.3151, 0.5138, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=25,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_26', 2.4931, 6.375, 6.375,
        3.5, 3.5, 0.5882, 0.28,
        0.3339, 0.5311, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=26,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_27', 2.7211, 6.375, 6.375,
        3.5, 3.5, 0.6176, 0.28,
        0.3602, 0.5554, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=27,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_28', 3.0142, 6.375, 6.375,
        3.5, 3.5, 0.6471, 0.28,
        0.3941, 0.5865, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=28,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_29', 3.3241, 6.375, 6.375,
        3.5, 3.5, 0.6728, 0.28,
        0.4299, 0.6194, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=29,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_30', 3.6839, 6.375, 6.375,
        3.5, 3.5, 0.6985, 0.28,
        0.4715, 0.6577, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=30,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组3_31', 4.0935, 6.375, 6.375,
        3.5, 3.5, 0.7243, 0.28,
        0.5189, 0.7012, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=31,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_32', 4.2988, 6.375, 6.375,
        3.5, 3.5, 0.7257, 0.28,
        0.5426, 0.723, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=32,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_33', 3.834, 6.375, 6.375,
        3.5, 3.5, 0.7014, 0.28,
        0.4889, 0.6736, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=33,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_34', 3.4273, 6.375, 6.375,
        3.5, 3.5, 0.6771, 0.28,
        0.4419, 0.6304, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=34,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_35', 3.0787, 6.375, 6.375,
        3.5, 3.5, 0.6528, 0.28,
        0.4016, 0.5934, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=35,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_36', 2.7883, 6.375, 6.375,
        3.5, 3.5, 0.625, 0.28,
        0.368, 0.5625, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=36,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_37', 2.5559, 6.375, 6.375,
        3.5, 3.5, 0.5972, 0.28,
        0.3411, 0.5378, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=37,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_38', 2.4002, 6.375, 6.375,
        3.5, 3.5, 0.5694, 0.28,
        0.3231, 0.5213, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=38,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_39', 2.289, 6.375, 6.375,
        3.5, 3.5, 0.5417, 0.28,
        0.3103, 0.5095, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=39,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    sec = engine.section.create_conventionalbox(
        '_组4_40', 2.2222, 6.375, 6.375,
        3.5, 3.5, 0.5139, 0.28,
        0.3026, 0.5024, 0.5, 1,
        5.05, 4.5, 5.05, 5.05,
        1.8, 0.88, 0.5, 0.28,
        1, 0.5, 0.5, 0.3,
        0.6, 0.3, 1, 0.5,
        0.6, 0.3, 2.875, 0.2,
        0, 0.8, 0.8, 1,
        2.875, 0.2, 1.325, 0.7,
        0.4, 'Integral', 0, 0,
        0, 0, 0, 0,
        0, no=40,
    )
    sec_nos.append(sec.no)

    sec.set_offset(
        offset_type_y='Middle', offset_value_y=0.0000,
        offset_type_z='Top', offset_value_z=0.0000
    )

    sec.set_mesh(
        mesh_method=0, mesh_size=0.1000
    )

    return sec_nos


if __name__ == "__main__":
    from ._0_engine import engine
    sec_nos = build_sections(engine)
    print(sec_nos)
    print(engine.section.all())