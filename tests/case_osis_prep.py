# 本文件是前处理的示例
from pyosis.core.all_func import *
from pyosis.material import material_manager
from pyosis.section import section_manager
from pyosis.node import node_manager
from pyosis.element import element_manager
from pyosis.boundary import boundary_manager
from pyosis.load import loadcase_manager

osis_clear()

osis_acel(9.8066)
osis_calc_tendon(1)
osis_calc_con_force(1)
osis_calc_shrink(1)
osis_calc_creep(1)
osis_calc_shear(1)
osis_calc_rlx(1)
osis_mod_loc_coor(0)
osis_inc_tendon(1)
osis_nl(0, 0)
osis_ln_srch(0)
osis_auto_ts(0)
osis_mod_opt(0)


section_manager.create_circle("圆形截面1", D=0.219, Tw=0.012, no=1)
section_manager.create_circle("圆形截面2", D=0.180, Tw=0.008, no=2)
section_manager.create_circle("圆形截面3", D=0.114, Tw=0.005, no=3)
section_manager.create_circle("圆形截面4", D=0.089, Tw=0.004, no=4)
section_manager.create_circle("圆形截面5", D=0.045, Tw=0.003, no=5)

material_manager.create_steel(1, "钢材1", "JTGD64_2015", "Q345", 0.05)

# 固定节点（x,y单位：m）
node_manager.create(1, 0, 5, 0)
node_manager.create(2, 15, 5, 0)
# 荷载作用节点
node_manager.create(3, 7.5, 0, 0)
node_manager.create(4, 20, 0, 0)

element_manager.create_beam3d(1, 1, 3, 1, 4, 4, 1, 1, 0.00, 0, 0.00, 0)
element_manager.create_beam3d(2, 2, 3, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)
element_manager.create_beam3d(3, 2, 4, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)
element_manager.create_beam3d(4, 3, 4, 1, 5, 5, 1, 1, 0.00, 0, 0.00, 0)

boundary_manager.create_general(1, "", 1, 1, 1, 1, 1, 1, 1)
boundary_manager.get(1).assign("a", [1, 2])

loadcase_manager.create("自定义工况1", "USER", 1, "施加于节点3和4的两个力")
loadcase_manager.get("自定义工况1").create_nforce(0, -1000000, 0, 0, 0, 0, 3)
loadcase_manager.get("自定义工况1").create_nforce(200000, 0, 0, 0, 0, 0, 4)

osis_solve()


# isok, error, ef = osis_elem_force("自定义工况1", "EF", "BEAM3D")


# def dict_to_json_txt(data, filename):
#     """将字典以JSON格式写入文件"""
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4)
    
#     print(f"字典已写入文件: {filename}")

# # 使用
# dict_to_json_txt(ef, "output.json")
