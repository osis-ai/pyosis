# tests/test_cpp_interface.py

"""
cpp 模块接口测试
"""
from pyosis.common import get_project_directory
from src.pyosis.cpp import (
    get_coordinate,
    get_all_group_info,
    get_all_element_info,
    get_all_node_info,
)


def test_coordinate():
    """测试获取节点坐标"""
    resp = get_coordinate()
    print(f"\n=== GetCoordinate ===")
    print(f"success: {resp.success}")
    print(f"count: {len(resp)}")

    if resp.success and len(resp) > 0:
        # 测试按 ID 获取
        first_id = resp.get_id_list()[0]
        print(f"first node id: {first_id}")
        print(f"get_by_id({first_id}): {resp.get_by_id(first_id)}")
        print(f"get_x({first_id}): {resp.get_x(first_id)}")
        print(f"get_y({first_id}): {resp.get_y(first_id)}")
        print(f"get_z({first_id}): {resp.get_z(first_id)}")
        print(f"get_xyz({first_id}): {resp.get_xyz(first_id)}")
        print(f"get_id_list(): {resp.get_id_list()}")


def test_group_info():
    """测试获取组信息"""
    resp = get_all_group_info()
    print(f"\n=== GetAllGroupInfo ===")
    print(f"success: {resp.success}")
    print(f"count: {len(resp)}")

    if resp.success and len(resp) > 0:
        names = resp.get_name_list()
        print(f"group names: {names}")

        # 测试按名称获取
        first_name = names[0]
        print(f"\n测试组名称 '{first_name}':")
        print(f"get_by_name('{first_name}'): {resp.get_by_name(first_name)}")
        print(f"get_tendon_count('{first_name}'): {resp.get_tendon_count(first_name)}")
        print(f"get_lane_count('{first_name}'): {resp.get_lane_count(first_name)}")
        print(f"get_stage_count('{first_name}'): {resp.get_stage_count(first_name)}")


def test_element_info():
    """测试获取单元信息"""
    resp = get_all_element_info()
    print(f"\n=== GetAllElementInfo ===")
    print(f"success: {resp.success}")
    print(f"count: {len(resp)}")

    if resp.success and len(resp) > 0:
        # 按类型筛选
        beams = resp.get_beams()
        trusses = resp.get_trusses()
        springs = resp.get_springs()
        cables = resp.get_cables()
        shells = resp.get_shells()
        print(f"beams: {len(beams)}, trusses: {len(trusses)}, springs: {len(springs)}, cables: {len(cables)}, shells: {len(shells)}")

        # 获取第一个单元详情（遍历每种类型找一个存在的）
        test_nos = resp.get_no_list()
        for no in test_nos:
            elem_type = resp.get_type(no)
            if elem_type == 1 and len(beams) > 0:  # Beam
                print(f"\n--- Beam 单元 {no} ---")
                print(f"get_by_no({no}): {resp.get_by_no(no)}")
                print(f"get_type({no}): {resp.get_type(no)}")
                print(f"get_type_name({no}): {resp.get_type_name(no)}")
                print(f"get_material({no}): {resp.get_material(no)}")
                print(f"get_nodes({no}): {resp.get_nodes(no)}")
                print(f"get_length({no}): {resp.get_length(no)}")
                print(f"get_center({no}): {resp.get_center(no)}")
                print(f"get_characters({no}): {resp.get_characters(no)}")
                print(f"get_loc_coor({no}): {resp.get_loc_coor(no)}")
                print(f"get_taper({no}): {resp.get_taper(no)}")
                print(f"get_sec_vec({no}): {resp.get_sec_vec(no)}")
                print(f"get_trans_vec({no}): {resp.get_trans_vec(no)}")
                print(f"get_strain({no}): {resp.get_strain(no)}")
                print(f"get_beta({no}): {resp.get_beta(no)}")
                print(f"get_beta_flag({no}): {resp.get_beta_flag(no)}")
                print(f"get_key_pt({no}): {resp.get_key_pt(no)}")
                print(f"get_warp({no}): {resp.get_warp(no)}")
                print(f"get_comp_thk({no}): {resp.get_comp_thk(no)}")
                print(f"get_section_details({no}): {resp.get_section_details(no)}")
                break

        for no in test_nos:
            elem_type = resp.get_type(no)
            if elem_type == 2 and len(trusses) > 0:  # Truss
                print(f"\n--- Truss 单元 {no} ---")
                print(f"get_type({no}): {resp.get_type_name(no)}")
                print(f"get_material({no}): {resp.get_material(no)}")
                print(f"get_nodes({no}): {resp.get_nodes(no)}")
                print(f"get_length({no}): {resp.get_length(no)}")
                print(f"get_section_details({no}): {resp.get_section_details(no)}")
                break

        for no in test_nos:
            elem_type = resp.get_type(no)
            if elem_type == 3 and len(springs) > 0:  # Spring
                print(f"\n--- Spring 单元 {no} ---")
                print(f"get_type({no}): {resp.get_type_name(no)}")
                print(f"get_material({no}): {resp.get_material(no)}")
                print(f"get_nodes({no}): {resp.get_nodes(no)}")
                print(f"get_length({no}): {resp.get_length(no)}")
                print(f"is_linear({no}): {resp.is_linear(no)}")
                print(f"get_dof_prop({no}): {resp.get_dof_prop(no)}")
                break

        for no in test_nos:
            elem_type = resp.get_type(no)
            if elem_type == 4 and len(cables) > 0:  # Cable
                print(f"\n--- Cable 单元 {no} ---")
                print(f"get_type({no}): {resp.get_type_name(no)}")
                print(f"get_material({no}): {resp.get_material(no)}")
                print(f"get_nodes({no}): {resp.get_nodes(no)}")
                print(f"get_length({no}): {resp.get_length(no)}")
                print(f"get_cable_method({no}): {resp.get_cable_method(no)}")
                print(f"get_cable_para({no}): {resp.get_cable_para(no)}")
                print(f"get_cable_section({no}): {resp.get_cable_section(no)}")
                print(f"get_cable_section_detail({no}): {resp.get_cable_section_detail(no)}")
                break

        for no in test_nos:
            elem_type = resp.get_type(no)
            if elem_type == 5 and len(shells) > 0:  # Shell
                print(f"\n--- Shell 单元 {no} ---")
                print(f"get_type({no}): {resp.get_type_name(no)}")
                print(f"get_material({no}): {resp.get_material(no)}")
                print(f"get_nodes({no}): {resp.get_nodes(no)}")
                print(f"get_length({no}): {resp.get_length(no)}")
                print(f"get_center({no}): {resp.get_center(no)}")
                print(f"is_thin({no}): {resp.is_thin(no)}")
                print(f"get_thickness({no}): {resp.get_thickness(no)}")
                print(f"get_node_sum({no}): {resp.get_node_sum(no)}")
                break


def test_node_info():
    """测试获取节点信息"""
    resp = get_all_node_info()
    print(f"\n=== GetAllNodeInfo ===")
    print(f"success: {resp.success}")
    print(f"count: {len(resp)}")

    if resp.success and len(resp) > 0:
        first_no = resp.get_no_list()[0]
        print(f"\n--- 节点 {first_no} ---")
        print(f"get_by_no({first_no}): {resp.get_by_no(first_no)}")
        print(f"get_coordinate({first_no}): {resp.get_coordinate(first_no)}")
        print(f"get_precision({first_no}): {resp.get_precision(first_no)}")
        print(f"get_hash_value({first_no}): {resp.get_hash_value(first_no)}")
        print(f"get_related_elements({first_no}): {resp.get_related_elements(first_no)}")
        print(f"get_related_boundaries({first_no}): {resp.get_related_boundaries(first_no)}")
        print(f"get_related_loads({first_no}): {resp.get_related_loads(first_no)}")
        print(f"get_related_setl_grps({first_no}): {resp.get_related_setl_grps(first_no)}")
        print(f"is_selected({first_no}): {resp.is_selected(first_no)}")
        print(f"is_plotted({first_no}): {resp.is_plotted(first_no)}")
        print(f"is_free({first_no}): {resp.is_free(first_no)}")


if __name__ == "__main__":
    print("开始测试 cpp 接口...")
    print("=" * 50)

    test_coordinate()
    test_group_info()
    test_element_info()
    test_node_info()
    print(get_project_directory())

    print("\n" + "=" * 50)
    print("测试完成")