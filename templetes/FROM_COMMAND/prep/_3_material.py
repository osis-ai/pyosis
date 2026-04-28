"""材料"""

from pyosis.core.engine import OSISEngine


def build_materials(engine: OSISEngine) -> list[int]:
    """创建材料，返回材料编号列表 [1, 2, 3]
    
    材料编号（显式定义，幂等执行）：
    - 1: C50 混凝土
    - 2: HRB400 钢筋
    - 3: 1860MPa 钢绞线
    """
    material = engine.material
    
    # 收缩徐变模型（编号 1）
    engine.prop.creep_shrink.create(1, "收缩徐变", 75.00, 7, 5.000, 3)
    
    # 材料 1: C50 混凝土
    mat1 = material.create_conc("C50", "JTG3362_2018", "C50", nCrepShrk=1, dDmp=0.050, no=1)
    
    # 材料 2: HRB400 钢筋
    mat2 = material.create_rebar("HRB400", "JTG3362_2018", "HRB400", dDmp=0.050, no=2)
    
    # 材料 3: 钢绞线-1860
    mat3 = material.create_prestressed("钢绞线-1860", "JTG3362_2018", "Strand1860", dDmp=0.050, no=3)
    
    return [mat1.no, mat2.no, mat3.no]


if __name__ == "__main__":
    from ._0_engine import engine
    mat_nos = build_materials(engine)
    print(mat_nos)
    print(engine.material.all())
