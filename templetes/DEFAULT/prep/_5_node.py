"""节点"""

from pyosis.core.engine import OSISEngine

def build_nodes(engine: OSISEngine) -> list[int]:
    """创建节点，返回节点编号列表"""

    node_nos = []

    n = engine.node.create(0.0800, 0.0000, 0.0000, no=1)
    node_nos.append(n.no)

    n = engine.node.create(0.3800, 0.0000, 0.0000, no=2)
    node_nos.append(n.no)

    n = engine.node.create(0.5800, 0.0000, 0.0000, no=3)
    node_nos.append(n.no)

    n = engine.node.create(1.3300, 0.0000, 0.0000, no=4)
    node_nos.append(n.no)

    n = engine.node.create(2.0800, 0.0000, 0.0000, no=5)
    node_nos.append(n.no)

    n = engine.node.create(2.8300, 0.0000, 0.0000, no=6)
    node_nos.append(n.no)

    n = engine.node.create(3.5800, 0.0000, 0.0000, no=7)
    node_nos.append(n.no)

    n = engine.node.create(4.5000, 0.0000, 0.0000, no=8)
    node_nos.append(n.no)

    n = engine.node.create(6.5000, 0.0000, 0.0000, no=9)
    node_nos.append(n.no)

    n = engine.node.create(8.5000, 0.0000, 0.0000, no=10)
    node_nos.append(n.no)

    n = engine.node.create(10.5000, 0.0000, 0.0000, no=11)
    node_nos.append(n.no)

    n = engine.node.create(12.5000, 0.0000, 0.0000, no=12)
    node_nos.append(n.no)

    n = engine.node.create(14.5000, 0.0000, 0.0000, no=13)
    node_nos.append(n.no)

    n = engine.node.create(16.5000, 0.0000, 0.0000, no=14)
    node_nos.append(n.no)

    n = engine.node.create(18.5000, 0.0000, 0.0000, no=15)
    node_nos.append(n.no)

    n = engine.node.create(20.5000, 0.0000, 0.0000, no=16)
    node_nos.append(n.no)

    n = engine.node.create(21.5000, 0.0000, 0.0000, no=17)
    node_nos.append(n.no)

    n = engine.node.create(22.2500, 0.0000, 0.0000, no=18)
    node_nos.append(n.no)

    n = engine.node.create(23.0000, 0.0000, 0.0000, no=19)
    node_nos.append(n.no)

    n = engine.node.create(23.7500, 0.0000, 0.0000, no=20)
    node_nos.append(n.no)

    n = engine.node.create(24.5000, 0.0000, 0.0000, no=21)
    node_nos.append(n.no)

    n = engine.node.create(24.7000, 0.0000, 0.0000, no=22)
    node_nos.append(n.no)

    n = engine.node.create(25.0000, 0.0000, 0.0000, no=23)
    node_nos.append(n.no)

    n = engine.node.create(25.3000, 0.0000, 0.0000, no=24)
    node_nos.append(n.no)

    n = engine.node.create(25.5000, 0.0000, 0.0000, no=25)
    node_nos.append(n.no)

    n = engine.node.create(26.2500, 0.0000, 0.0000, no=26)
    node_nos.append(n.no)

    n = engine.node.create(27.0000, 0.0000, 0.0000, no=27)
    node_nos.append(n.no)

    n = engine.node.create(27.7500, 0.0000, 0.0000, no=28)
    node_nos.append(n.no)

    n = engine.node.create(28.5000, 0.0000, 0.0000, no=29)
    node_nos.append(n.no)

    n = engine.node.create(29.5000, 0.0000, 0.0000, no=30)
    node_nos.append(n.no)

    n = engine.node.create(31.5000, 0.0000, 0.0000, no=31)
    node_nos.append(n.no)

    n = engine.node.create(33.5000, 0.0000, 0.0000, no=32)
    node_nos.append(n.no)

    n = engine.node.create(35.5000, 0.0000, 0.0000, no=33)
    node_nos.append(n.no)

    n = engine.node.create(37.5000, 0.0000, 0.0000, no=34)
    node_nos.append(n.no)

    n = engine.node.create(39.5000, 0.0000, 0.0000, no=35)
    node_nos.append(n.no)

    n = engine.node.create(41.5000, 0.0000, 0.0000, no=36)
    node_nos.append(n.no)

    n = engine.node.create(43.5000, 0.0000, 0.0000, no=37)
    node_nos.append(n.no)

    n = engine.node.create(45.5000, 0.0000, 0.0000, no=38)
    node_nos.append(n.no)

    n = engine.node.create(46.5000, 0.0000, 0.0000, no=39)
    node_nos.append(n.no)

    n = engine.node.create(47.2500, 0.0000, 0.0000, no=40)
    node_nos.append(n.no)

    n = engine.node.create(48.0000, 0.0000, 0.0000, no=41)
    node_nos.append(n.no)

    n = engine.node.create(48.7500, 0.0000, 0.0000, no=42)
    node_nos.append(n.no)

    n = engine.node.create(49.5000, 0.0000, 0.0000, no=43)
    node_nos.append(n.no)

    n = engine.node.create(49.7000, 0.0000, 0.0000, no=44)
    node_nos.append(n.no)

    n = engine.node.create(50.0000, 0.0000, 0.0000, no=45)
    node_nos.append(n.no)

    n = engine.node.create(50.3000, 0.0000, 0.0000, no=46)
    node_nos.append(n.no)

    n = engine.node.create(50.5000, 0.0000, 0.0000, no=47)
    node_nos.append(n.no)

    n = engine.node.create(51.2500, 0.0000, 0.0000, no=48)
    node_nos.append(n.no)

    n = engine.node.create(52.0000, 0.0000, 0.0000, no=49)
    node_nos.append(n.no)

    n = engine.node.create(52.7500, 0.0000, 0.0000, no=50)
    node_nos.append(n.no)

    n = engine.node.create(53.5000, 0.0000, 0.0000, no=51)
    node_nos.append(n.no)

    n = engine.node.create(54.5000, 0.0000, 0.0000, no=52)
    node_nos.append(n.no)

    n = engine.node.create(56.5000, 0.0000, 0.0000, no=53)
    node_nos.append(n.no)

    n = engine.node.create(58.5000, 0.0000, 0.0000, no=54)
    node_nos.append(n.no)

    n = engine.node.create(60.5000, 0.0000, 0.0000, no=55)
    node_nos.append(n.no)

    n = engine.node.create(62.5000, 0.0000, 0.0000, no=56)
    node_nos.append(n.no)

    n = engine.node.create(64.5000, 0.0000, 0.0000, no=57)
    node_nos.append(n.no)

    n = engine.node.create(66.5000, 0.0000, 0.0000, no=58)
    node_nos.append(n.no)

    n = engine.node.create(68.5000, 0.0000, 0.0000, no=59)
    node_nos.append(n.no)

    n = engine.node.create(70.5000, 0.0000, 0.0000, no=60)
    node_nos.append(n.no)

    n = engine.node.create(71.5000, 0.0000, 0.0000, no=61)
    node_nos.append(n.no)

    n = engine.node.create(72.2500, 0.0000, 0.0000, no=62)
    node_nos.append(n.no)

    n = engine.node.create(73.0000, 0.0000, 0.0000, no=63)
    node_nos.append(n.no)

    n = engine.node.create(73.7500, 0.0000, 0.0000, no=64)
    node_nos.append(n.no)

    n = engine.node.create(74.5000, 0.0000, 0.0000, no=65)
    node_nos.append(n.no)

    n = engine.node.create(74.7000, 0.0000, 0.0000, no=66)
    node_nos.append(n.no)

    n = engine.node.create(75.0000, 0.0000, 0.0000, no=67)
    node_nos.append(n.no)

    n = engine.node.create(75.3000, 0.0000, 0.0000, no=68)
    node_nos.append(n.no)

    n = engine.node.create(75.5000, 0.0000, 0.0000, no=69)
    node_nos.append(n.no)

    n = engine.node.create(76.2500, 0.0000, 0.0000, no=70)
    node_nos.append(n.no)

    n = engine.node.create(77.0000, 0.0000, 0.0000, no=71)
    node_nos.append(n.no)

    n = engine.node.create(77.7500, 0.0000, 0.0000, no=72)
    node_nos.append(n.no)

    n = engine.node.create(78.5000, 0.0000, 0.0000, no=73)
    node_nos.append(n.no)

    n = engine.node.create(79.5000, 0.0000, 0.0000, no=74)
    node_nos.append(n.no)

    n = engine.node.create(81.5000, 0.0000, 0.0000, no=75)
    node_nos.append(n.no)

    n = engine.node.create(83.5000, 0.0000, 0.0000, no=76)
    node_nos.append(n.no)

    n = engine.node.create(85.5000, 0.0000, 0.0000, no=77)
    node_nos.append(n.no)

    n = engine.node.create(87.5000, 0.0000, 0.0000, no=78)
    node_nos.append(n.no)

    n = engine.node.create(89.5000, 0.0000, 0.0000, no=79)
    node_nos.append(n.no)

    n = engine.node.create(91.5000, 0.0000, 0.0000, no=80)
    node_nos.append(n.no)

    n = engine.node.create(93.5000, 0.0000, 0.0000, no=81)
    node_nos.append(n.no)

    n = engine.node.create(95.5000, 0.0000, 0.0000, no=82)
    node_nos.append(n.no)

    n = engine.node.create(96.5000, 0.0000, 0.0000, no=83)
    node_nos.append(n.no)

    n = engine.node.create(97.2500, 0.0000, 0.0000, no=84)
    node_nos.append(n.no)

    n = engine.node.create(98.0000, 0.0000, 0.0000, no=85)
    node_nos.append(n.no)

    n = engine.node.create(98.7500, 0.0000, 0.0000, no=86)
    node_nos.append(n.no)

    n = engine.node.create(99.5000, 0.0000, 0.0000, no=87)
    node_nos.append(n.no)

    n = engine.node.create(99.7000, 0.0000, 0.0000, no=88)
    node_nos.append(n.no)

    n = engine.node.create(100.0000, 0.0000, 0.0000, no=89)
    node_nos.append(n.no)

    n = engine.node.create(100.3000, 0.0000, 0.0000, no=90)
    node_nos.append(n.no)

    n = engine.node.create(100.5000, 0.0000, 0.0000, no=91)
    node_nos.append(n.no)

    n = engine.node.create(101.2500, 0.0000, 0.0000, no=92)
    node_nos.append(n.no)

    n = engine.node.create(102.0000, 0.0000, 0.0000, no=93)
    node_nos.append(n.no)

    n = engine.node.create(102.7500, 0.0000, 0.0000, no=94)
    node_nos.append(n.no)

    n = engine.node.create(103.5000, 0.0000, 0.0000, no=95)
    node_nos.append(n.no)

    n = engine.node.create(104.5000, 0.0000, 0.0000, no=96)
    node_nos.append(n.no)

    n = engine.node.create(106.5000, 0.0000, 0.0000, no=97)
    node_nos.append(n.no)

    n = engine.node.create(108.5000, 0.0000, 0.0000, no=98)
    node_nos.append(n.no)

    n = engine.node.create(110.5000, 0.0000, 0.0000, no=99)
    node_nos.append(n.no)

    n = engine.node.create(112.5000, 0.0000, 0.0000, no=100)
    node_nos.append(n.no)

    n = engine.node.create(114.5000, 0.0000, 0.0000, no=101)
    node_nos.append(n.no)

    n = engine.node.create(116.5000, 0.0000, 0.0000, no=102)
    node_nos.append(n.no)

    n = engine.node.create(118.5000, 0.0000, 0.0000, no=103)
    node_nos.append(n.no)

    n = engine.node.create(120.5000, 0.0000, 0.0000, no=104)
    node_nos.append(n.no)

    n = engine.node.create(121.4200, 0.0000, 0.0000, no=105)
    node_nos.append(n.no)

    n = engine.node.create(122.1700, 0.0000, 0.0000, no=106)
    node_nos.append(n.no)

    n = engine.node.create(122.9200, 0.0000, 0.0000, no=107)
    node_nos.append(n.no)

    n = engine.node.create(123.6700, 0.0000, 0.0000, no=108)
    node_nos.append(n.no)

    n = engine.node.create(124.4200, 0.0000, 0.0000, no=109)
    node_nos.append(n.no)

    n = engine.node.create(124.6200, 0.0000, 0.0000, no=110)
    node_nos.append(n.no)

    n = engine.node.create(124.9200, 0.0000, 0.0000, no=111)
    node_nos.append(n.no)

    return node_nos


if __name__ == "__main__":
    from ._0_engine import engine
    node_nos = build_nodes(engine)
    print(node_nos)
    print(engine.node.all())