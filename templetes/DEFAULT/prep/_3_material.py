"""材料"""

from pyosis.core.engine import OSISEngine

def build_materials(engine: OSISEngine) -> list[int]:
    """材料"""

    # ========== 原始命令流 ==========
    # CrpShrk,1,收缩徐变,70.00,7,5.000,3;//定义收缩徐变特性参数，基本上伴随混凝土材料有
    # Material,1,C50,CONC,JTG3362_2018,C50,1,0.050;//定义混凝土材料,会引用收缩徐变特性参数编号
    # Material,2,钢绞线-1860,PRESTRESSED,JTG3362_2018,Strand1860,0.050;//定义钢绞线材料
    # Material,3,HRB400,REBAR,JTG3362_2018,HRB400,0.050;//定义钢筋
    return []


if __name__ == "__main__":
    from ._0_engine import engine
    mat_nos = build_materials(engine)
    print(mat_nos)
    print(engine.material.all())