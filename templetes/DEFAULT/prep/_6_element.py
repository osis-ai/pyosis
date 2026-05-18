"""单元"""

from pyosis.core.engine import OSISEngine

def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:
    """创建单元，返回单元编号列表和单元组名称列表"""

    elem_nos = []
    elem_group_names = []

    e = engine.element.create_beam3d(1, 2, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=1)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(2, 3, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=2)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(3, 4, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=3)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(4, 5, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=4)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(5, 6, 1, 1190001, 1190002, 1, 1, 0, 0, 0, 0, no=5)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(6, 7, 1, 1200001, 1200002, 1, 1, 0, 0, 0, 0, no=6)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(7, 8, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=7)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(8, 9, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=8)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(9, 10, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=9)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(10, 11, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=10)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(11, 12, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=11)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(12, 13, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=12)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(13, 14, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=13)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(14, 15, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=14)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(15, 16, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=15)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(16, 17, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=16)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(17, 18, 1, 1090001, 1090002, 1, 1, 0, 0, 0, 0, no=17)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(18, 19, 1, 1100001, 1100002, 1, 1, 0, 0, 0, 0, no=18)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(19, 20, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=19)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(20, 21, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=20)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(21, 22, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=21)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(22, 23, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=22)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(23, 24, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=23)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(24, 25, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=24)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(25, 26, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=25)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(26, 27, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=26)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(27, 28, 1, 1170001, 1170002, 1, 1, 0, 0, 0, 0, no=27)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(28, 29, 1, 1180001, 1180002, 1, 1, 0, 0, 0, 0, no=28)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(29, 30, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=29)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(30, 31, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=30)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(31, 32, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=31)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(32, 33, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=32)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(33, 34, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=33)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(34, 35, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=34)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(35, 36, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=35)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(36, 37, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=36)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(37, 38, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=37)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(38, 39, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=38)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(39, 40, 1, 1070001, 1070002, 1, 1, 0, 0, 0, 0, no=39)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(40, 41, 1, 1080001, 1080002, 1, 1, 0, 0, 0, 0, no=40)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(41, 42, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=41)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(42, 43, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=42)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(43, 44, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=43)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(44, 45, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=44)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(45, 46, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=45)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(46, 47, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=46)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(47, 48, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=47)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(48, 49, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=48)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(49, 50, 1, 1150001, 1150002, 1, 1, 0, 0, 0, 0, no=49)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(50, 51, 1, 1160001, 1160002, 1, 1, 0, 0, 0, 0, no=50)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(51, 52, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=51)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(52, 53, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=52)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(53, 54, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=53)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(54, 55, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=54)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(55, 56, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=55)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(56, 57, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=56)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(57, 58, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=57)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(58, 59, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=58)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(59, 60, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=59)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(60, 61, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=60)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(61, 62, 1, 1050001, 1050002, 1, 1, 0, 0, 0, 0, no=61)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(62, 63, 1, 1060001, 1060002, 1, 1, 0, 0, 0, 0, no=62)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(63, 64, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=63)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(64, 65, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=64)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(65, 66, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=65)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(66, 67, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=66)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(67, 68, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=67)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(68, 69, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=68)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(69, 70, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=69)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(70, 71, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=70)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(71, 72, 1, 1130001, 1130002, 1, 1, 0, 0, 0, 0, no=71)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(72, 73, 1, 1140001, 1140002, 1, 1, 0, 0, 0, 0, no=72)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(73, 74, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=73)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(74, 75, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=74)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(75, 76, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=75)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(76, 77, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=76)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(77, 78, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=77)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(78, 79, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=78)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(79, 80, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=79)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(80, 81, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=80)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(81, 82, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=81)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(82, 83, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=82)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(83, 84, 1, 1030001, 1030002, 1, 1, 0, 0, 0, 0, no=83)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(84, 85, 1, 1040001, 1040002, 1, 1, 0, 0, 0, 0, no=84)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(85, 86, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=85)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(86, 87, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=86)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(87, 88, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=87)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(88, 89, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=88)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(89, 90, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=89)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(90, 91, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=90)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(91, 92, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=91)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(92, 93, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=92)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(93, 94, 1, 1110001, 1110002, 1, 1, 0, 0, 0, 0, no=93)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(94, 95, 1, 1120001, 1120002, 1, 1, 0, 0, 0, 0, no=94)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(95, 96, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=95)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(96, 97, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=96)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(97, 98, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=97)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(98, 99, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=98)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(99, 100, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=99)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(100, 101, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=100)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(101, 102, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=101)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(102, 103, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=102)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(103, 104, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=103)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(104, 105, 1, 5, 5, 1, 1, 0, 0, 0, 0, no=104)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(105, 106, 1, 1010001, 1010002, 1, 1, 0, 0, 0, 0, no=105)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(106, 107, 1, 1020001, 1020002, 1, 1, 0, 0, 0, 0, no=106)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(107, 108, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=107)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(108, 109, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=108)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(109, 110, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=109)
    elem_nos.append(e.no)

    e = engine.element.create_beam3d(110, 111, 1, 6, 6, 1, 1, 0, 0, 0, 0, no=110)
    elem_nos.append(e.no)

    engine.prop.assign_component_thickness(2.505E-01, op='a', elems=[5, 18, 27, 40, 49, 62, 71, 84, 93, 106])

    engine.prop.assign_component_thickness(2.603E-01, op='a', elems=['1to4', '19to26', '41to48', '63to70', '85to92', '107to110'])

    engine.prop.assign_component_thickness(2.306E-01, op='a', elems=[6, 17, 28, 39, 50, 61, 72, 83, 94, 105])

    engine.prop.assign_component_thickness(2.206E-01, op='a', elems=['7to16', '29to38', '51to60', '73to82', '95to104'])

    eg = engine.element.group.create('1-N1单元组')
    elem_group_names.append(eg.name)

    eg.add(['1to21'])

    eg = engine.element.group.create('1-N2单元组')
    elem_group_names.append(eg.name)

    eg.add(['1to21'])

    eg = engine.element.group.create('1-N3单元组')
    elem_group_names.append(eg.name)

    eg.add(['1to21'])

    eg = engine.element.group.create('1-N4单元组')
    elem_group_names.append(eg.name)

    eg.add(['1to21'])

    eg = engine.element.group.create('1_车道线单元组')
    elem_group_names.append(eg.name)

    eg.add(['1to110'])

    eg = engine.element.group.create('2-N1-复制01单元组')
    elem_group_names.append(eg.name)

    eg.add(['68to87'])

    eg = engine.element.group.create('2-N1-复制单元组')
    elem_group_names.append(eg.name)

    eg.add(['46to65'])

    eg = engine.element.group.create('2-N1单元组')
    elem_group_names.append(eg.name)

    eg.add(['24to43'])

    eg = engine.element.group.create('2-N2-复制01单元组')
    elem_group_names.append(eg.name)

    eg.add(['68to87'])

    eg = engine.element.group.create('2-N2-复制单元组')
    elem_group_names.append(eg.name)

    eg.add(['46to65'])

    eg = engine.element.group.create('2-N2单元组')
    elem_group_names.append(eg.name)

    eg.add(['24to43'])

    eg = engine.element.group.create('2-N3-复制01单元组')
    elem_group_names.append(eg.name)

    eg.add(['68to87'])

    eg = engine.element.group.create('2-N3-复制单元组')
    elem_group_names.append(eg.name)

    eg.add(['46to65'])

    eg = engine.element.group.create('2-N3单元组')
    elem_group_names.append(eg.name)

    eg.add(['24to43'])

    eg = engine.element.group.create('2-N4-复制01单元组')
    elem_group_names.append(eg.name)

    eg.add(['68to87'])

    eg = engine.element.group.create('2-N4-复制单元组')
    elem_group_names.append(eg.name)

    eg.add(['46to65'])

    eg = engine.element.group.create('2-N4单元组')
    elem_group_names.append(eg.name)

    eg.add(['24to43'])

    eg = engine.element.group.create('5-N1单元组')
    elem_group_names.append(eg.name)

    eg.add(['90to110'])

    eg = engine.element.group.create('5-N2单元组')
    elem_group_names.append(eg.name)

    eg.add(['90to110'])

    eg = engine.element.group.create('5-N3单元组')
    elem_group_names.append(eg.name)

    eg.add(['90to110'])

    eg = engine.element.group.create('5-N4单元组')
    elem_group_names.append(eg.name)

    eg.add(['90to110'])

    eg = engine.element.group.create('ALL')
    elem_group_names.append(eg.name)

    eg.add(['1to110'])

    eg = engine.element.group.create('D1-T1单元组')
    elem_group_names.append(eg.name)

    eg.add(['16to29'])

    eg = engine.element.group.create('D1-T2单元组')
    elem_group_names.append(eg.name)

    eg.add(['14to31'])

    eg = engine.element.group.create('D2-T1-复制单元组')
    elem_group_names.append(eg.name)

    eg.add(['38to51'])

    eg = engine.element.group.create('D2-T2-复制单元组')
    elem_group_names.append(eg.name)

    eg.add(['36to53'])

    eg = engine.element.group.create('D3-T1-复制01单元组')
    elem_group_names.append(eg.name)

    eg.add(['60to73'])

    eg = engine.element.group.create('D3-T2-复制01单元组')
    elem_group_names.append(eg.name)

    eg.add(['58to75'])

    eg = engine.element.group.create('D4-T1-复制02单元组')
    elem_group_names.append(eg.name)

    eg.add(['82to95'])

    eg = engine.element.group.create('D4-T2-复制02单元组')
    elem_group_names.append(eg.name)

    eg.add(['80to97'])

    eg = engine.element.group.create('现浇')
    elem_group_names.append(eg.name)

    eg.add(['22to23', '44to45', '66to67', '88to89'])

    eg = engine.element.group.create('预制')
    elem_group_names.append(eg.name)

    eg.add(['1to21', '24to43', '46to65', '68to87', '90to110'])

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