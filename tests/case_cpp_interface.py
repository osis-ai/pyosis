# tests/case_cpp_interface.py

"""
io 模块接口测试
"""
from pyosis.io import *


def test_coordinate():
    """测试获取节点坐标"""
    coord = Coordinate()
    print(f"\n=== Coordinate ===")
    print(f"success: {coord.success}")
    print(f"count: {len(coord)}")

    if coord.success and len(coord) > 0:
        first_id = coord.get_id_list()[0]
        print(f"first node id: {first_id}")
        print(f"get_by_id({first_id}): {coord.get_by_id(first_id)}")
        print(f"get_x({first_id}): {coord.get_x(first_id)}")
        print(f"get_y({first_id}): {coord.get_y(first_id)}")
        print(f"get_z({first_id}): {coord.get_z(first_id)}")
        print(f"get_xyz({first_id}): {coord.get_xyz(first_id)}")
        print(f"get_id_list(): {coord.get_id_list()}")


def test_group_info():
    """测试获取组信息"""
    grp = GroupInfo()
    print(f"\n=== GroupInfo ===")
    print(f"success: {grp.success}")
    print(f"count: {len(grp)}")

    if grp.success and len(grp) > 0:
        names = grp.get_name_list()
        print(f"group names: {names}")

        first_name = names[0]
        print(f"\n测试组名称 '{first_name}':")
        print(f"get_by_name('{first_name}'): {grp.get_by_name(first_name)}")
        print(f"get_tendon_count('{first_name}'): {grp.get_tendon_count(first_name)}")
        print(f"get_lane_count('{first_name}'): {grp.get_lane_count(first_name)}")
        print(f"get_stage_count('{first_name}'): {grp.get_stage_count(first_name)}")


def test_element_info():
    """测试获取单元信息"""
    elem = ElementInfo()
    print(f"\n=== ElementInfo ===")
    print(f"success: {elem.success}")
    print(f"count: {len(elem)}")

    if elem.success and len(elem) > 0:
        beams = elem.get_beams()
        trusses = elem.get_trusses()
        springs = elem.get_springs()
        cables = elem.get_cables()
        shells = elem.get_shells()
        print(f"beams: {len(beams)}, trusses: {len(trusses)}, springs: {len(springs)}, cables: {len(cables)}, shells: {len(shells)}")

        test_nos = elem.get_no_list()
        for no in test_nos:
            elem_type = elem.get_type(no)
            if elem_type == 1 and len(beams) > 0:
                print(f"\n--- Beam 单元 {no} ---")
                print(f"get_by_no({no}): {elem.get_by_no(no)}")
                print(f"get_type({no}): {elem.get_type(no)}")
                print(f"get_type_name({no}): {elem.get_type_name(no)}")
                print(f"get_material({no}): {elem.get_material(no)}")
                print(f"get_nodes({no}): {elem.get_nodes(no)}")
                print(f"get_length({no}): {elem.get_length(no)}")
                print(f"get_center({no}): {elem.get_center(no)}")
                print(f"get_characters({no}): {elem.get_characters(no)}")
                print(f"get_loc_coor({no}): {elem.get_loc_coor(no)}")
                print(f"get_taper({no}): {elem.get_taper(no)}")
                print(f"get_sec_vec({no}): {elem.get_sec_vec(no)}")
                print(f"get_trans_vec({no}): {elem.get_trans_vec(no)}")
                print(f"get_strain({no}): {elem.get_strain(no)}")
                print(f"get_beta({no}): {elem.get_beta(no)}")
                print(f"get_beta_flag({no}): {elem.get_beta_flag(no)}")
                print(f"get_key_pt({no}): {elem.get_key_pt(no)}")
                print(f"get_warp({no}): {elem.get_warp(no)}")
                print(f"get_comp_thk({no}): {elem.get_comp_thk(no)}")
                print(f"get_section_details({no}): {elem.get_section_details(no)}")
                break

        for no in test_nos:
            elem_type = elem.get_type(no)
            if elem_type == 2 and len(trusses) > 0:
                print(f"\n--- Truss 单元 {no} ---")
                print(f"get_type({no}): {elem.get_type_name(no)}")
                print(f"get_material({no}): {elem.get_material(no)}")
                print(f"get_nodes({no}): {elem.get_nodes(no)}")
                print(f"get_length({no}): {elem.get_length(no)}")
                print(f"get_section_details({no}): {elem.get_section_details(no)}")
                break

        for no in test_nos:
            elem_type = elem.get_type(no)
            if elem_type == 3 and len(springs) > 0:
                print(f"\n--- Spring 单元 {no} ---")
                print(f"get_type({no}): {elem.get_type_name(no)}")
                print(f"get_material({no}): {elem.get_material(no)}")
                print(f"get_nodes({no}): {elem.get_nodes(no)}")
                print(f"get_length({no}): {elem.get_length(no)}")
                print(f"is_linear({no}): {elem.is_linear(no)}")
                print(f"get_dof_prop({no}): {elem.get_dof_prop(no)}")
                break

        for no in test_nos:
            elem_type = elem.get_type(no)
            if elem_type == 4 and len(cables) > 0:
                print(f"\n--- Cable 单元 {no} ---")
                print(f"get_type({no}): {elem.get_type_name(no)}")
                print(f"get_material({no}): {elem.get_material(no)}")
                print(f"get_nodes({no}): {elem.get_nodes(no)}")
                print(f"get_length({no}): {elem.get_length(no)}")
                print(f"get_cable_method({no}): {elem.get_cable_method(no)}")
                print(f"get_cable_para({no}): {elem.get_cable_para(no)}")
                print(f"get_cable_section({no}): {elem.get_cable_section(no)}")
                print(f"get_cable_section_detail({no}): {elem.get_cable_section_detail(no)}")
                break

        for no in test_nos:
            elem_type = elem.get_type(no)
            if elem_type == 5 and len(shells) > 0:
                print(f"\n--- Shell 单元 {no} ---")
                print(f"get_type({no}): {elem.get_type_name(no)}")
                print(f"get_material({no}): {elem.get_material(no)}")
                print(f"get_nodes({no}): {elem.get_nodes(no)}")
                print(f"get_length({no}): {elem.get_length(no)}")
                print(f"get_center({no}): {elem.get_center(no)}")
                print(f"is_thin({no}): {elem.is_thin(no)}")
                print(f"get_thickness({no}): {elem.get_thickness(no)}")
                print(f"get_node_sum({no}): {elem.get_node_sum(no)}")
                break


def test_node_info():
    """测试获取节点信息"""
    node = NodeInfo()
    print(f"\n=== NodeInfo ===")
    print(f"success: {node.success}")
    print(f"count: {len(node)}")

    if node.success and len(node) > 0:
        first_no = node.get_no_list()[0]
        print(f"\n--- 节点 {first_no} ---")
        print(f"get_by_no({first_no}): {node.get_by_no(first_no)}")
        print(f"get_coordinate({first_no}): {node.get_coordinate(first_no)}")
        print(f"get_precision({first_no}): {node.get_precision(first_no)}")
        print(f"get_hash_value({first_no}): {node.get_hash_value(first_no)}")
        print(f"get_related_elements({first_no}): {node.get_related_elements(first_no)}")
        print(f"get_related_boundaries({first_no}): {node.get_related_boundaries(first_no)}")
        print(f"get_related_loads({first_no}): {node.get_related_loads(first_no)}")
        print(f"get_related_setl_grps({first_no}): {node.get_related_setl_grps(first_no)}")
        print(f"is_selected({first_no}): {node.is_selected(first_no)}")
        print(f"is_plotted({first_no}): {node.is_plotted(first_no)}")
        print(f"is_free({first_no}): {node.is_free(first_no)}")


def test_section_info():
    """测试获取截面信息"""
    sec = SectionInfo()
    print(f"\n=== SectionInfo ===")
    print(f"success: {sec.success}")
    print(f"count: {len(sec)}")

    if sec.success and len(sec) > 0:
        first_no = sec.get_no_list()[0]
        print(f"\n--- 截面 {first_no} ---")
        print(f"get_by_no({first_no}): {sec.get_by_no(first_no)}")
        print(f"get_name({first_no}): {sec.get_name(first_no)}")
        print(f"get_area({first_no}): {sec.get_area(first_no)}")

        one = SectionInfoByNo(first_no)
        print(f"\n=== SectionInfoByNo(secNo={first_no}) ===")
        print(f"success: {one.success}")
        print(f"section: {one.section}")

    defs = AllSectionDefinitions()
    print(f"\n=== AllSectionDefinitions ===")
    print(f"success: {defs.success}, count: {len(defs)}")

    usage = SectionUsage()
    print(f"\n=== SectionUsage ===")
    print(f"success: {usage.success}, by_element: {len(usage.by_element)}, by_section: {len(usage.by_section)}")
    if usage.success and usage.by_element:
        print(f"first by_element row: {usage.by_element[0]}")

def test_material_info():
    """测试获取材料信息"""
    mi = MaterialInfo()
    print("\n=== MaterialInfo ===")
    print("success:", mi.success, "count:", len(mi.data))
    for row in mi.data[:5]:
        print(row)

def test_boundary_info():
    """测试获取边界信息"""
    boundary = BoundaryInfo()
    print("\n=== BoundaryInfo ===")
    print(f"success: {boundary.success}")
    print(f"count: {len(boundary)}")

    if boundary.success and len(boundary) > 0:
        no_list = boundary.get_no_list()
        print(f"边界编号列表: {no_list}")

        for no in no_list:
            bd_type = boundary.get_type(no)
            print(f"\n--- 边界 {no} (类型: {boundary.get_type_name(no)}) ---")
            print(f"  get_by_no({no}): {boundary.get_by_no(no)}")
            print(f"  get_type({no}): {boundary.get_type(no)}")
            print(f"  get_type_name({no}): {boundary.get_type_name(no)}")
            print(f"  get_entity_vec({no}): {boundary.get_entity_vec(no)}")
            print(f"  is_occupied({no}): {boundary.is_occupied(no)}")
            print(f"  is_selected({no}): {boundary.is_selected(no)}")

            if bd_type == 1:
                print(f"  get_coor_no({no}): {boundary.get_coor_no(no)}")
                print(f"  get_constraints({no}): {boundary.get_constraints(no)}")
            elif bd_type == 2:
                print(f"  get_master_no({no}): {boundary.get_master_no(no)}")
                print(f"  get_constraints({no}): {boundary.get_constraints(no)}")
            elif bd_type == 4:
                print(f"  get_constraints({no}): {boundary.get_constraints(no)}")
                release_data = boundary.get_by_no(no)
                if "endIState" in release_data:
                    print(f"  endIState: {release_data['endIState']}")
                if "endJState" in release_data:
                    print(f"  endJState: {release_data['endJState']}")
                if "endI" in release_data:
                    print(f"  endI: {release_data['endI']}")
                if "endJ" in release_data:
                    print(f"  endJ: {release_data['endJ']}")
            elif bd_type == 5:
                print(f"  get_coor_no({no}): {boundary.get_coor_no(no)}")
                elastic_data = boundary.get_by_no(no)
                if "k" in elastic_data:
                    print(f"  k: {elastic_data['k']}")
                if "elasticK" in elastic_data:
                    print(f"  elasticK: {elastic_data['elasticK']}")
            elif bd_type == 6:
                print(f"  get_coor_no({no}): {boundary.get_coor_no(no)}")
                print(f"  get_stiffness_matrix({no}): {boundary.get_stiffness_matrix(no)}")
                print(f"  get_mass_matrix({no}): {boundary.get_mass_matrix(no)}")
                print(f"  get_damping_matrix({no}): {boundary.get_damping_matrix(no)}")
def test_prestressed_info():
    """测试获取预应力材料信息"""
    print("\n=== PrestressedMaterialInfo ===")
    pm = PrestressedMaterialInfo()
    print("success:", pm.success, "count:", len(pm.data))
    for row in pm.data[:5]:
        print(row)

    print("\n=== PrestressedLoadInfo ===")
    pl = PrestressedLoadInfo()
    print("success:", pl.success, "count:", len(pl.data))
    for row in pl.data[:5]:
        print(row)
    if pl.success:
        print("load case list:", pl.get_load_case_list())
        print("name list:", pl.get_name_list())


def test_tendon_info():
    """测试获取钢束信息"""
    print("\n=== TendonShapeInfo ===")
    ts = TendonShapeInfo()
    print("success:", ts.success, "count:", len(ts.data))
    for row in ts.data[:5]:
        print(row)
    if ts.success:
        print("name list:", ts.get_name_list())

    print("\n=== TendonPropInfo ===")
    tp = TendonPropInfo()
    print("success:", tp.success, "count:", len(tp.data))
    for row in tp.data[:5]:
        print(row)
    if tp.success:
        print("name list:", tp.get_name_list())


if __name__ == "__main__":
    print("开始测试 io 接口...")
    print("=" * 50)

    test_coordinate()
    test_group_info()
    test_element_info()
    test_node_info()
    test_section_info()
    print(get_project_directory())
    test_material_info()
    test_boundary_info()
    test_prestressed_info()
    test_tendon_info()
    print("\n" + "=" * 50)
    print("测试完成")