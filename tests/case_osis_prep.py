# 本文件是前处理的示例
from pyosis.core.engine import OSISEngine

engine = OSISEngine()

engine.clear()

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

engine.section.create_circle("圆形截面1", d=0.219, tw=0.012, no=1)
engine.section.create_circle("圆形截面2", d=0.180, tw=0.008, no=2)
engine.section.create_circle("圆形截面3", d=0.114, tw=0.005, no=3)
engine.section.create_circle("圆形截面4", d=0.089, tw=0.004, no=4)
engine.section.create_circle("圆形截面5", d=0.045, tw=0.003, no=5)

engine.material.create_steel("钢材1", eCode="JTGD64_2015", eGrade="Q345", dDmp=0.05, no=1)

# 固定节点（x,y单位：m）
engine.node.create(0, 5, 0, no=1)
engine.node.create(15, 5, 0, no=2)
# 荷载作用节点
engine.node.create(7.5, 0, 0, no=3)
engine.node.create(20, 0, 0, no=4)

engine.element.create_beam3d(1, 3, nMat=1, nSec1=4, nSec2=4, no=1)
engine.element.create_beam3d(2, 3, nMat=1, nSec1=5, nSec2=5, no=2)
engine.element.create_beam3d(2, 4, nMat=1, nSec1=5, nSec2=5, no=3)
engine.element.create_beam3d(3, 4, nMat=1, nSec1=5, nSec2=5, no=4)

bd = engine.boundary.create_general(no=1)
bd.assign("a", [1, 2])

lc = engine.load.create(
    "自定义工况1",
    load_case_type="USER",
    scalar=1.0,
    prompt="施加于节点3和4的两个力"
)
lc.create_nforce(3, dFx=0, dFy=-1000000, dFz=0, dMx=0, dMy=0, dMz=0)
lc.create_nforce(4, dFx=200000, dFy=0, dFz=0, dMx=0, dMy=0, dMz=0)

engine.solve()


# isok, error, ef = osis_elem_force("自定义工况1", "EF", "BEAM3D")


# def dict_to_json_txt(data, filename):
#     """将字典以JSON格式写入文件"""
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4)
#     
#     print(f"字典已写入文件: {filename}")

# # 使用
# dict_to_json_txt(ef, "output.json")
