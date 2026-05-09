"""单元"""

from pyosis.core.engine import OSISEngine

def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:
    """创建单元，返回单元编号列表和单元组名称列表"""

    elem_nos = []
    elem_group_names = []

    e = engine.element.create_beam3d(1, 2, 1, 4, 4, 1, 1, 0, 0, 0, 0, no=1)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(2, 3, 1, 4, 4, 1, 1, 0, 0, 0, 0, no=2)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(3, 4, 1, 4, 3, 1, 1, 0, 0, 0, 0, no=3)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(4, 5, 1, 3, 7, 1, 1, 0, 0, 0, 0, no=4)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(5, 6, 1, 7, 8, 1, 1, 0, 0, 0, 0, no=5)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(6, 7, 1, 8, 9, 1, 1, 0, 0, 0, 0, no=6)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(7, 8, 1, 9, 10, 1, 1, 0, 0, 0, 0, no=7)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(8, 9, 1, 10, 11, 1, 1, 0, 0, 0, 0, no=8)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(9, 10, 1, 11, 12, 1, 1, 0, 0, 0, 0, no=9)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(10, 11, 1, 12, 13, 1, 1, 0, 0, 0, 0, no=10)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(11, 12, 1, 13, 14, 1, 1, 0, 0, 0, 0, no=11)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(12, 13, 1, 14, 15, 1, 1, 0, 0, 0, 0, no=12)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(13, 14, 1, 15, 2, 1, 1, 0, 0, 0, 0, no=13)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(14, 15, 1, 2, 1, 1, 1, 0, 0, 0, 0, no=14)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(15, 16, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=15)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(16, 17, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=16)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(17, 18, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=17)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(18, 19, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=18)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(19, 20, 1, 1, 2, 1, 1, 0, 0, 0, 0, no=19)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(20, 21, 1, 2, 16, 1, 1, 0, 0, 0, 0, no=20)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(21, 22, 1, 16, 17, 1, 1, 0, 0, 0, 0, no=21)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(22, 23, 1, 17, 18, 1, 1, 0, 0, 0, 0, no=22)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(23, 24, 1, 18, 19, 1, 1, 0, 0, 0, 0, no=23)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(24, 25, 1, 19, 20, 1, 1, 0, 0, 0, 0, no=24)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(25, 26, 1, 20, 21, 1, 1, 0, 0, 0, 0, no=25)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(26, 27, 1, 21, 22, 1, 1, 0, 0, 0, 0, no=26)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(27, 28, 1, 22, 23, 1, 1, 0, 0, 0, 0, no=27)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(28, 29, 1, 23, 3, 1, 1, 0, 0, 0, 0, no=28)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(29, 30, 1, 3, 3, 1, 1, 0, 0, 0, 0, no=29)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(30, 31, 1, 3, 3, 1, 1, 0, 0, 0, 0, no=30)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(31, 32, 1, 3, 24, 1, 1, 0, 0, 0, 0, no=31)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(32, 33, 1, 24, 25, 1, 1, 0, 0, 0, 0, no=32)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(33, 34, 1, 25, 26, 1, 1, 0, 0, 0, 0, no=33)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(34, 35, 1, 26, 27, 1, 1, 0, 0, 0, 0, no=34)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(35, 36, 1, 27, 28, 1, 1, 0, 0, 0, 0, no=35)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(36, 37, 1, 28, 29, 1, 1, 0, 0, 0, 0, no=36)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(37, 38, 1, 29, 30, 1, 1, 0, 0, 0, 0, no=37)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(38, 39, 1, 30, 31, 1, 1, 0, 0, 0, 0, no=38)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(39, 40, 1, 31, 2, 1, 1, 0, 0, 0, 0, no=39)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(40, 41, 1, 2, 1, 1, 1, 0, 0, 0, 0, no=40)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(41, 42, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=41)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(42, 43, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=42)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(43, 44, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=43)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(44, 45, 1, 1, 1, 1, 1, 0, 0, 0, 0, no=44)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(45, 46, 1, 1, 2, 1, 1, 0, 0, 0, 0, no=45)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(46, 47, 1, 2, 32, 1, 1, 0, 0, 0, 0, no=46)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(47, 48, 1, 32, 33, 1, 1, 0, 0, 0, 0, no=47)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(48, 49, 1, 33, 34, 1, 1, 0, 0, 0, 0, no=48)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(49, 50, 1, 34, 35, 1, 1, 0, 0, 0, 0, no=49)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(50, 51, 1, 35, 36, 1, 1, 0, 0, 0, 0, no=50)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(51, 52, 1, 36, 37, 1, 1, 0, 0, 0, 0, no=51)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(52, 53, 1, 37, 38, 1, 1, 0, 0, 0, 0, no=52)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(53, 54, 1, 38, 39, 1, 1, 0, 0, 0, 0, no=53)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(54, 55, 1, 39, 40, 1, 1, 0, 0, 0, 0, no=54)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(55, 56, 1, 40, 3, 1, 1, 0, 0, 0, 0, no=55)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(56, 57, 1, 3, 4, 1, 1, 0, 0, 0, 0, no=56)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(57, 58, 1, 4, 4, 1, 1, 0, 0, 0, 0, no=57)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(58, 59, 1, 4, 4, 1, 1, 0, 0, 0, 0, no=58)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(2001, 1001, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=1001)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(2002, 1002, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=1002)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(2003, 1003, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=1003)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(2004, 1004, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=1004)
    elem_nos.append(e.no)

    engine.prop.assign_component_thickness(6.790E-01, op='a', elems=[21])

    engine.prop.assign_component_thickness(6.079E-01, op='a', elems=[9, 50])

    engine.prop.assign_component_thickness(7.246E-01, op='a', elems=[46])

    engine.prop.assign_component_thickness(6.497E-01, op='a', elems=['1to2', '57to58'])

    engine.prop.assign_component_thickness(7.190E-01, op='a', elems=[13])

    engine.prop.assign_component_thickness(5.551E-01, op='a', elems=[6])

    engine.prop.assign_component_thickness(5.943E-01, op='a', elems=[3, 56])

    engine.prop.assign_component_thickness(5.454E-01, op='a', elems=[5])

    engine.prop.assign_component_thickness(5.402E-01, op='a', elems=[4])

    engine.prop.assign_component_thickness(5.686E-01, op='a', elems=[7])

    engine.prop.assign_component_thickness(5.862E-01, op='a', elems=[8, 51])

    engine.prop.assign_component_thickness(6.958E-01, op='a', elems=[47])

    engine.prop.assign_component_thickness(6.579E-01, op='a', elems=[11])

    engine.prop.assign_component_thickness(6.320E-01, op='a', elems=[10])

    engine.prop.assign_component_thickness(5.389E-01, op='a', elems=['29to30'])

    engine.prop.assign_component_thickness(6.869E-01, op='a', elems=[12])

    engine.prop.assign_component_thickness(2.560E+00, op='a', elems=['1002to1003'])

    engine.prop.assign_component_thickness(8.105E-01, op='a', elems=[14, 19, 40, 45])

    engine.prop.assign_component_thickness(8.853E-01, op='a', elems=['15to18', '41to44'])

    engine.prop.assign_component_thickness(7.162E-01, op='a', elems=[20])

    engine.prop.assign_component_thickness(6.462E-01, op='a', elems=[22])

    engine.prop.assign_component_thickness(6.179E-01, op='a', elems=[23])

    engine.prop.assign_component_thickness(1.584E+00, op='a', elems=[1001, 1004])

    engine.prop.assign_component_thickness(5.691E-01, op='a', elems=[52])

    engine.prop.assign_component_thickness(5.507E-01, op='a', elems=[32])

    engine.prop.assign_component_thickness(5.938E-01, op='a', elems=[24])

    engine.prop.assign_component_thickness(5.746E-01, op='a', elems=[25])

    engine.prop.assign_component_thickness(5.465E-01, op='a', elems=[54])

    engine.prop.assign_component_thickness(5.806E-01, op='a', elems=[34])

    engine.prop.assign_component_thickness(5.603E-01, op='a', elems=[26])

    engine.prop.assign_component_thickness(5.495E-01, op='a', elems=[27])

    engine.prop.assign_component_thickness(5.419E-01, op='a', elems=[28])

    engine.prop.assign_component_thickness(7.181E-01, op='a', elems=[39])

    engine.prop.assign_component_thickness(5.422E-01, op='a', elems=[31])

    engine.prop.assign_component_thickness(5.634E-01, op='a', elems=[33])

    engine.prop.assign_component_thickness(6.025E-01, op='a', elems=[35])

    engine.prop.assign_component_thickness(6.271E-01, op='a', elems=[36])

    engine.prop.assign_component_thickness(6.539E-01, op='a', elems=[37])

    engine.prop.assign_component_thickness(6.843E-01, op='a', elems=[38])

    engine.prop.assign_component_thickness(6.627E-01, op='a', elems=[48])

    engine.prop.assign_component_thickness(6.335E-01, op='a', elems=[49])

    engine.prop.assign_component_thickness(5.563E-01, op='a', elems=[53])

    engine.prop.assign_component_thickness(5.406E-01, op='a', elems=[55])

    eg = engine.element.group.create('0_号块')
    elem_group_names.append(eg.name)

    eg.add(['14to19', '40to45'])

    eg = engine.element.group.create('11_边跨现浇段')
    elem_group_names.append(eg.name)

    eg.add(['1to3', '56to58'])

    eg = engine.element.group.create('12_边跨合拢段')
    elem_group_names.append(eg.name)

    eg.add([4, 55])

    eg = engine.element.group.create('13_中跨合拢段')
    elem_group_names.append(eg.name)

    eg.add(['29to30'])

    eg = engine.element.group.create('1_号块')
    elem_group_names.append(eg.name)

    eg.add([13, 20, 39, 46])

    eg = engine.element.group.create('2_号块')
    elem_group_names.append(eg.name)

    eg.add([12, 21, 38, 47])

    eg = engine.element.group.create('3_号块')
    elem_group_names.append(eg.name)

    eg.add([11, 22, 37, 48])

    eg = engine.element.group.create('4_号块')
    elem_group_names.append(eg.name)

    eg.add([10, 23, 36, 49])

    eg = engine.element.group.create('5_号块')
    elem_group_names.append(eg.name)

    eg.add([9, 24, 35, 50])

    eg = engine.element.group.create('6_号块')
    elem_group_names.append(eg.name)

    eg.add([8, 25, 34, 51])

    eg = engine.element.group.create('7_号块')
    elem_group_names.append(eg.name)

    eg.add([7, 26, 33, 52])

    eg = engine.element.group.create('8_号块')
    elem_group_names.append(eg.name)

    eg.add([6, 27, 32, 53])

    eg = engine.element.group.create('9_号块')
    elem_group_names.append(eg.name)

    eg.add([5, 28, 31, 54])

    eg = engine.element.group.create('BD刚束单元组1')
    elem_group_names.append(eg.name)

    eg.add(['1to7'])

    eg = engine.element.group.create('BD刚束单元组2')
    elem_group_names.append(eg.name)

    eg.add(['1to8'])

    eg = engine.element.group.create('BD刚束单元组3')
    elem_group_names.append(eg.name)

    eg.add(['1to9'])

    eg = engine.element.group.create('BT刚束单元组1')
    elem_group_names.append(eg.name)

    eg.add(['1to5'])

    eg = engine.element.group.create('BT刚束单元组2')
    elem_group_names.append(eg.name)

    eg.add(['1to6'])

    eg = engine.element.group.create('BT刚束单元组3')
    elem_group_names.append(eg.name)

    eg.add(['1to7'])

    eg = engine.element.group.create('ZT刚束单元组')
    elem_group_names.append(eg.name)

    eg.add(['27to32'])

    eg = engine.element.group.create('钢束单元组F0')
    elem_group_names.append(eg.name)

    eg.add(['14to19'])

    eg = engine.element.group.create('钢束单元组F1')
    elem_group_names.append(eg.name)

    eg.add(['13to20'])

    eg = engine.element.group.create('钢束单元组F2')
    elem_group_names.append(eg.name)

    eg.add(['12to21'])

    eg = engine.element.group.create('钢束单元组F3')
    elem_group_names.append(eg.name)

    eg.add(['11to22'])

    eg = engine.element.group.create('钢束单元组F4')
    elem_group_names.append(eg.name)

    eg.add(['10to23'])

    eg = engine.element.group.create('钢束单元组F5')
    elem_group_names.append(eg.name)

    eg.add(['9to24'])

    eg = engine.element.group.create('钢束单元组F6')
    elem_group_names.append(eg.name)

    eg.add(['8to25'])

    eg = engine.element.group.create('钢束单元组F7')
    elem_group_names.append(eg.name)

    eg.add(['7to26'])

    eg = engine.element.group.create('钢束单元组F8')
    elem_group_names.append(eg.name)

    eg.add(['6to27'])

    eg = engine.element.group.create('钢束单元组F9')
    elem_group_names.append(eg.name)

    eg.add(['5to28'])

    eg = engine.element.group.create('跨中底板刚束单元组1')
    elem_group_names.append(eg.name)

    eg.add(['28to31'])

    eg = engine.element.group.create('跨中底板刚束单元组2')
    elem_group_names.append(eg.name)

    eg.add(['27to32'])

    eg = engine.element.group.create('跨中底板刚束单元组3')
    elem_group_names.append(eg.name)

    eg.add(['26to33'])

    eg = engine.element.group.create('跨中底板刚束单元组4')
    elem_group_names.append(eg.name)

    eg.add(['25to34'])

    eg = engine.element.group.create('跨中底板刚束单元组5')
    elem_group_names.append(eg.name)

    eg.add(['24to35'])

    eg = engine.element.group.create('跨中底板刚束单元组6')
    elem_group_names.append(eg.name)

    eg.add(['23to36'])

    eg = engine.element.group.create('跨中底板刚束单元组7')
    elem_group_names.append(eg.name)

    eg.add(['22to37'])

    eg = engine.element.group.create('跨中底板刚束单元组8')
    elem_group_names.append(eg.name)

    eg.add(['21to38'])

    eg = engine.element.group.create('桥墩')
    elem_group_names.append(eg.name)

    eg.add(['1001to1004'])

    eg = engine.element.group.create('上部主梁单元组')
    elem_group_names.append(eg.name)

    eg.add(['1to58'])

    eg = engine.element.group.create('右侧_BD刚束单元组1')
    elem_group_names.append(eg.name)

    eg.add(['52to58'])

    eg = engine.element.group.create('右侧_BD刚束单元组2')
    elem_group_names.append(eg.name)

    eg.add(['51to58'])

    eg = engine.element.group.create('右侧_BD刚束单元组3')
    elem_group_names.append(eg.name)

    eg.add(['50to58'])

    eg = engine.element.group.create('右侧_BT刚束单元组1')
    elem_group_names.append(eg.name)

    eg.add(['54to58'])

    eg = engine.element.group.create('右侧_BT刚束单元组2')
    elem_group_names.append(eg.name)

    eg.add(['53to58'])

    eg = engine.element.group.create('右侧_BT刚束单元组3')
    elem_group_names.append(eg.name)

    eg.add(['52to58'])

    eg = engine.element.group.create('右侧_钢束单元组F0')
    elem_group_names.append(eg.name)

    eg.add(['40to45'])

    eg = engine.element.group.create('右侧_钢束单元组F1')
    elem_group_names.append(eg.name)

    eg.add(['39to46'])

    eg = engine.element.group.create('右侧_钢束单元组F2')
    elem_group_names.append(eg.name)

    eg.add(['38to47'])

    eg = engine.element.group.create('右侧_钢束单元组F3')
    elem_group_names.append(eg.name)

    eg.add(['37to48'])

    eg = engine.element.group.create('右侧_钢束单元组F4')
    elem_group_names.append(eg.name)

    eg.add(['36to49'])

    eg = engine.element.group.create('右侧_钢束单元组F5')
    elem_group_names.append(eg.name)

    eg.add(['35to50'])

    eg = engine.element.group.create('右侧_钢束单元组F6')
    elem_group_names.append(eg.name)

    eg.add(['34to51'])

    eg = engine.element.group.create('右侧_钢束单元组F7')
    elem_group_names.append(eg.name)

    eg.add(['33to52'])

    eg = engine.element.group.create('右侧_钢束单元组F8')
    elem_group_names.append(eg.name)

    eg.add(['32to53'])

    eg = engine.element.group.create('右侧_钢束单元组F9')
    elem_group_names.append(eg.name)

    eg.add(['31to54'])

    return elem_nos, elem_group_names


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