"""单元"""

from pyosis.core.engine import OSISEngine

def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:
    """单元"""

    element_nos = []

    # [Element] 梁单元
    # 原始命令: Element,1,BEAM3D,1,2,1,1,1
    # 参数:
    #   no=BEAM3D
    #   node1=1
    #   node2=2
    #   nMat=1
    #   nSec1=1
    #   nSec2=1
    engine.element.create_beam3d(no="BEAM3D", node1=1, node2=2, nMat=1, nSec1=1, nSec2=1)

    # [Element] 梁单元
    # 原始命令: Element,2,BEAM3D,2,3,1,1,1
    # 参数:
    #   no=BEAM3D
    #   node1=2
    #   node2=3
    #   nMat=1
    #   nSec1=1
    #   nSec2=1
    engine.element.create_beam3d(no="BEAM3D", node1=2, node2=3, nMat=1, nSec1=1, nSec2=1)

    # [Element] 梁单元
    # 原始命令: Element,3,BEAM3D,3,4,1,1,1
    # 参数:
    #   no=BEAM3D
    #   node1=3
    #   node2=4
    #   nMat=1
    #   nSec1=1
    #   nSec2=1
    engine.element.create_beam3d(no="BEAM3D", node1=3, node2=4, nMat=1, nSec1=1, nSec2=1)

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