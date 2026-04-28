"""材料"""

from pyosis.core.engine import OSISEngine

def build_materials(engine: OSISEngine) -> list[int]:
    """材料"""

    material_nos = []

    # [Material] 混凝土
    # 原始命令: Material,1,C50,CONC,JTG3362_2018,C50,1,0.05
    # 参数:
    #   no=1
    #   strName=CONC
    #   eCode=JTG3362_2018
    #   eGrade=C50
    #   nCrepShrk=1
    #   dDmp=0.05
    engine.material.create_conc(no=1, strName="CONC", eCode="JTG3362_2018", eGrade="C50", nCrepShrk=1, dDmp=0.05)

    # [Material] 钢筋
    # 原始命令: Material,2,HRB400,REBAR,JTG3362_2018,HRB400,0.05
    # 参数:
    #   no=2
    #   strName=REBAR
    #   eCode=JTG3362_2018
    #   eGrade=HRB400
    #   dDmp=0.05
    engine.material.create_rebar(no=2, strName="REBAR", eCode="JTG3362_2018", eGrade="HRB400", dDmp=0.05)

    # [Material] 预应力
    # 原始命令: Material,3,Strand1860,PRESTRESSED,JTG3362_2018,Strand1860,0.05
    # 参数:
    #   no=3
    #   strName=PRESTRESSED
    #   eCode=JTG3362_2018
    #   eGrade=Strand1860
    #   dDmp=0.05
    engine.material.create_prestressed(no=3, strName="PRESTRESSED", eCode="JTG3362_2018", eGrade="Strand1860", dDmp=0.05)

    return []

if __name__ == "__main__":
    from ._0_engine import engine
    mat_nos = build_materials(engine)
    print(mat_nos)
    print(engine.material.all())