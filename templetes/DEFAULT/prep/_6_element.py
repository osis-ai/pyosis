"""单元"""

from pyosis.core.engine import OSISEngine

def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:
    """单元"""

    # ========== 原始命令流 ==========
    # Element,1,BEAM3D,1,2,1,4,4,1,1,0.000E+00,0,0.00,0;//建立单元，引用节点、材料、截面
    # Element,2,BEAM3D,2,3,1,4,4,1,1,0.000E+00,0,0.00,0
    # Element,3,BEAM3D,3,4,1,4,3,1,1,0.000E+00,0,0.00,0
    # Element,4,BEAM3D,4,5,1,3,7,1,1,0.000E+00,0,0.00,0
    # Element,5,BEAM3D,5,6,1,7,8,1,1,0.000E+00,0,0.00,0
    # Element,6,BEAM3D,6,7,1,8,9,1,1,0.000E+00,0,0.00,0
    # Element,7,BEAM3D,7,8,1,9,10,1,1,0.000E+00,0,0.00,0
    # Element,8,BEAM3D,8,9,1,10,11,1,1,0.000E+00,0,0.00,0
    # Element,9,BEAM3D,9,10,1,11,12,1,1,0.000E+00,0,0.00,0
    # Element,10,BEAM3D,10,11,1,12,13,1,1,0.000E+00,0,0.00,0
    # Element,11,BEAM3D,11,12,1,13,14,1,1,0.000E+00,0,0.00,0
    # Element,12,BEAM3D,12,13,1,14,15,1,1,0.000E+00,0,0.00,0
    # Element,13,BEAM3D,13,14,1,15,2,1,1,0.000E+00,0,0.00,0
    # Element,14,BEAM3D,14,15,1,2,1,1,1,0.000E+00,0,0.00,0
    # Element,15,BEAM3D,15,16,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,16,BEAM3D,16,17,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,17,BEAM3D,17,18,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,18,BEAM3D,18,19,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,19,BEAM3D,19,20,1,1,2,1,1,0.000E+00,0,0.00,0
    # Element,20,BEAM3D,20,21,1,2,16,1,1,0.000E+00,0,0.00,0
    # Element,21,BEAM3D,21,22,1,16,17,1,1,0.000E+00,0,0.00,0
    # Element,22,BEAM3D,22,23,1,17,18,1,1,0.000E+00,0,0.00,0
    # Element,23,BEAM3D,23,24,1,18,19,1,1,0.000E+00,0,0.00,0
    # Element,24,BEAM3D,24,25,1,19,20,1,1,0.000E+00,0,0.00,0
    # Element,25,BEAM3D,25,26,1,20,21,1,1,0.000E+00,0,0.00,0
    # Element,26,BEAM3D,26,27,1,21,22,1,1,0.000E+00,0,0.00,0
    # Element,27,BEAM3D,27,28,1,22,23,1,1,0.000E+00,0,0.00,0
    # Element,28,BEAM3D,28,29,1,23,3,1,1,0.000E+00,0,0.00,0
    # Element,29,BEAM3D,29,30,1,3,3,1,1,0.000E+00,0,0.00,0
    # Element,30,BEAM3D,30,31,1,3,3,1,1,0.000E+00,0,0.00,0
    # Element,31,BEAM3D,31,32,1,3,24,1,1,0.000E+00,0,0.00,0
    # Element,32,BEAM3D,32,33,1,24,25,1,1,0.000E+00,0,0.00,0
    # Element,33,BEAM3D,33,34,1,25,26,1,1,0.000E+00,0,0.00,0
    # Element,34,BEAM3D,34,35,1,26,27,1,1,0.000E+00,0,0.00,0
    # Element,35,BEAM3D,35,36,1,27,28,1,1,0.000E+00,0,0.00,0
    # Element,36,BEAM3D,36,37,1,28,29,1,1,0.000E+00,0,0.00,0
    # Element,37,BEAM3D,37,38,1,29,30,1,1,0.000E+00,0,0.00,0
    # Element,38,BEAM3D,38,39,1,30,31,1,1,0.000E+00,0,0.00,0
    # Element,39,BEAM3D,39,40,1,31,2,1,1,0.000E+00,0,0.00,0
    # Element,40,BEAM3D,40,41,1,2,1,1,1,0.000E+00,0,0.00,0
    # Element,41,BEAM3D,41,42,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,42,BEAM3D,42,43,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,43,BEAM3D,43,44,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,44,BEAM3D,44,45,1,1,1,1,1,0.000E+00,0,0.00,0
    # Element,45,BEAM3D,45,46,1,1,2,1,1,0.000E+00,0,0.00,0
    # Element,46,BEAM3D,46,47,1,2,32,1,1,0.000E+00,0,0.00,0
    # Element,47,BEAM3D,47,48,1,32,33,1,1,0.000E+00,0,0.00,0
    # Element,48,BEAM3D,48,49,1,33,34,1,1,0.000E+00,0,0.00,0
    # Element,49,BEAM3D,49,50,1,34,35,1,1,0.000E+00,0,0.00,0
    # Element,50,BEAM3D,50,51,1,35,36,1,1,0.000E+00,0,0.00,0
    # Element,51,BEAM3D,51,52,1,36,37,1,1,0.000E+00,0,0.00,0
    # Element,52,BEAM3D,52,53,1,37,38,1,1,0.000E+00,0,0.00,0
    # Element,53,BEAM3D,53,54,1,38,39,1,1,0.000E+00,0,0.00,0
    # Element,54,BEAM3D,54,55,1,39,40,1,1,0.000E+00,0,0.00,0
    # Element,55,BEAM3D,55,56,1,40,3,1,1,0.000E+00,0,0.00,0
    # Element,56,BEAM3D,56,57,1,3,4,1,1,0.000E+00,0,0.00,0
    # Element,57,BEAM3D,57,58,1,4,4,1,1,0.000E+00,0,0.00,0
    # Element,58,BEAM3D,58,59,1,4,4,1,1,0.000E+00,0,0.00,0
    # Element,1001,BEAM3D,2001,1001,1,5,5,1,1,0.000E+00,0,0.00,0
    # Element,1002,BEAM3D,2002,1002,1,6,6,1,1,0.000E+00,0,0.00,0
    # Element,1003,BEAM3D,2003,1003,1,6,6,1,1,0.000E+00,0,0.00,0
    # Element,1004,BEAM3D,2004,1004,1,5,5,1,1,0.000E+00,0,0.00,0
    # AsgnCompThk,6.790E-01,a,21;//理论厚度，引用单元标号
    # AsgnCompThk,6.079E-01,a,9,50
    # AsgnCompThk,7.246E-01,a,46
    # AsgnCompThk,6.497E-01,a,1to2,57to58
    # AsgnCompThk,7.190E-01,a,13
    # AsgnCompThk,5.551E-01,a,6
    # AsgnCompThk,5.943E-01,a,3,56
    # AsgnCompThk,5.454E-01,a,5
    # AsgnCompThk,5.402E-01,a,4
    # AsgnCompThk,5.686E-01,a,7
    # AsgnCompThk,5.862E-01,a,8,51
    # AsgnCompThk,6.958E-01,a,47
    # AsgnCompThk,6.579E-01,a,11
    # AsgnCompThk,6.320E-01,a,10
    # AsgnCompThk,5.389E-01,a,29to30
    # AsgnCompThk,6.869E-01,a,12
    # AsgnCompThk,2.560E+00,a,1002to1003
    # AsgnCompThk,8.105E-01,a,14,19,40,45
    # AsgnCompThk,8.853E-01,a,15to18,41to44
    # AsgnCompThk,7.162E-01,a,20
    # AsgnCompThk,6.462E-01,a,22
    # AsgnCompThk,6.179E-01,a,23
    # AsgnCompThk,1.584E+00,a,1001,1004
    # AsgnCompThk,5.691E-01,a,52
    # AsgnCompThk,5.507E-01,a,32
    # AsgnCompThk,5.938E-01,a,24
    # AsgnCompThk,5.746E-01,a,25
    # AsgnCompThk,5.465E-01,a,54
    # AsgnCompThk,5.806E-01,a,34
    # AsgnCompThk,5.603E-01,a,26
    # AsgnCompThk,5.495E-01,a,27
    # AsgnCompThk,5.419E-01,a,28
    # AsgnCompThk,7.181E-01,a,39
    # AsgnCompThk,5.422E-01,a,31
    # AsgnCompThk,5.634E-01,a,33
    # AsgnCompThk,6.025E-01,a,35
    # AsgnCompThk,6.271E-01,a,36
    # AsgnCompThk,6.539E-01,a,37
    # AsgnCompThk,6.843E-01,a,38
    # AsgnCompThk,6.627E-01,a,48
    # AsgnCompThk,6.335E-01,a,49
    # AsgnCompThk,5.563E-01,a,53
    # AsgnCompThk,5.406E-01,a,55
    # EleGrp,0_号块,c;//建立单元组名字
    # EleGrp,0_号块,a,14to19,40to45;//往单元组里面加数据，引用单元号，单元组名
    # EleGrp,11_边跨现浇段,c
    # EleGrp,11_边跨现浇段,a,1to3,56to58
    # EleGrp,12_边跨合拢段,c
    # EleGrp,12_边跨合拢段,a,4,55
    # EleGrp,13_中跨合拢段,c
    # EleGrp,13_中跨合拢段,a,29to30
    # EleGrp,1_号块,c
    # EleGrp,1_号块,a,13,20,39,46
    # EleGrp,2_号块,c
    # EleGrp,2_号块,a,12,21,38,47
    # EleGrp,3_号块,c
    # EleGrp,3_号块,a,11,22,37,48
    # EleGrp,4_号块,c
    # EleGrp,4_号块,a,10,23,36,49
    # EleGrp,5_号块,c
    # EleGrp,5_号块,a,9,24,35,50
    # EleGrp,6_号块,c
    # EleGrp,6_号块,a,8,25,34,51
    # EleGrp,7_号块,c
    # EleGrp,7_号块,a,7,26,33,52
    # EleGrp,8_号块,c
    # EleGrp,8_号块,a,6,27,32,53
    # EleGrp,9_号块,c
    # EleGrp,9_号块,a,5,28,31,54
    # EleGrp,BD刚束单元组1,c
    # EleGrp,BD刚束单元组1,a,1to7
    # EleGrp,BD刚束单元组2,c
    # EleGrp,BD刚束单元组2,a,1to8
    # EleGrp,BD刚束单元组3,c
    # EleGrp,BD刚束单元组3,a,1to9
    # EleGrp,BT刚束单元组1,c
    # EleGrp,BT刚束单元组1,a,1to5
    # EleGrp,BT刚束单元组2,c
    # EleGrp,BT刚束单元组2,a,1to6
    # EleGrp,BT刚束单元组3,c
    # EleGrp,BT刚束单元组3,a,1to7
    # EleGrp,ZT刚束单元组,c
    # EleGrp,ZT刚束单元组,a,27to32
    # EleGrp,钢束单元组F0,c
    # EleGrp,钢束单元组F0,a,14to19
    # EleGrp,钢束单元组F1,c
    # EleGrp,钢束单元组F1,a,13to20
    # EleGrp,钢束单元组F2,c
    # EleGrp,钢束单元组F2,a,12to21
    # EleGrp,钢束单元组F3,c
    # EleGrp,钢束单元组F3,a,11to22
    # EleGrp,钢束单元组F4,c
    # EleGrp,钢束单元组F4,a,10to23
    # EleGrp,钢束单元组F5,c
    # EleGrp,钢束单元组F5,a,9to24
    # EleGrp,钢束单元组F6,c
    # EleGrp,钢束单元组F6,a,8to25
    # EleGrp,钢束单元组F7,c
    # EleGrp,钢束单元组F7,a,7to26
    # EleGrp,钢束单元组F8,c
    # EleGrp,钢束单元组F8,a,6to27
    # EleGrp,钢束单元组F9,c
    # EleGrp,钢束单元组F9,a,5to28
    # EleGrp,跨中底板刚束单元组1,c
    # EleGrp,跨中底板刚束单元组1,a,28to31
    # EleGrp,跨中底板刚束单元组2,c
    # EleGrp,跨中底板刚束单元组2,a,27to32
    # EleGrp,跨中底板刚束单元组3,c
    # EleGrp,跨中底板刚束单元组3,a,26to33
    # EleGrp,跨中底板刚束单元组4,c
    # EleGrp,跨中底板刚束单元组4,a,25to34
    # EleGrp,跨中底板刚束单元组5,c
    # EleGrp,跨中底板刚束单元组5,a,24to35
    # EleGrp,跨中底板刚束单元组6,c
    # EleGrp,跨中底板刚束单元组6,a,23to36
    # EleGrp,跨中底板刚束单元组7,c
    # EleGrp,跨中底板刚束单元组7,a,22to37
    # EleGrp,跨中底板刚束单元组8,c
    # EleGrp,跨中底板刚束单元组8,a,21to38
    # EleGrp,桥墩,c
    # EleGrp,桥墩,a,1001to1004
    # EleGrp,上部主梁单元组,c
    # EleGrp,上部主梁单元组,a,1to58
    # EleGrp,右侧_BD刚束单元组1,c
    # EleGrp,右侧_BD刚束单元组1,a,52to58
    # EleGrp,右侧_BD刚束单元组2,c
    # EleGrp,右侧_BD刚束单元组2,a,51to58
    # EleGrp,右侧_BD刚束单元组3,c
    # EleGrp,右侧_BD刚束单元组3,a,50to58
    # EleGrp,右侧_BT刚束单元组1,c
    # EleGrp,右侧_BT刚束单元组1,a,54to58
    # EleGrp,右侧_BT刚束单元组2,c
    # EleGrp,右侧_BT刚束单元组2,a,53to58
    # EleGrp,右侧_BT刚束单元组3,c
    # EleGrp,右侧_BT刚束单元组3,a,52to58
    # EleGrp,右侧_钢束单元组F0,c
    # EleGrp,右侧_钢束单元组F0,a,40to45
    # EleGrp,右侧_钢束单元组F1,c
    # EleGrp,右侧_钢束单元组F1,a,39to46
    # EleGrp,右侧_钢束单元组F2,c
    # EleGrp,右侧_钢束单元组F2,a,38to47
    # EleGrp,右侧_钢束单元组F3,c
    # EleGrp,右侧_钢束单元组F3,a,37to48
    # EleGrp,右侧_钢束单元组F4,c
    # EleGrp,右侧_钢束单元组F4,a,36to49
    # EleGrp,右侧_钢束单元组F5,c
    # EleGrp,右侧_钢束单元组F5,a,35to50
    # EleGrp,右侧_钢束单元组F6,c
    # EleGrp,右侧_钢束单元组F6,a,34to51
    # EleGrp,右侧_钢束单元组F7,c
    # EleGrp,右侧_钢束单元组F7,a,33to52
    # EleGrp,右侧_钢束单元组F8,c
    # EleGrp,右侧_钢束单元组F8,a,32to53
    # EleGrp,右侧_钢束单元组F9,c
    # EleGrp,右侧_钢束单元组F9,a,31to54
    return [], []


if __name__ == "__main__":
    from ._0_engine import engine
    mats = engine.material.all()
    mat_nos = [m.no for m in mats]
    secs = engine.section.all()
    sec_nos = [s.no for s in secs]
    nodes = engine.node.all()
    node_nos = [n.no for n in nodes]
    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)
    print(elem_nos)
    print(elem_group_names)
    print(engine.element.all())
    print(engine.element.group.all())