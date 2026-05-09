"""材料"""

from pyosis.core.engine import OSISEngine

def build_materials(engine: OSISEngine) -> list[int]:
    """创建材料，返回材料编号列表"""

    mat_nos = []

    engine.prop.creep_shrink.create(
        no=1, name='收缩徐变', avg_humidity=70.00,
        birth_time=7, type_coeff=5.000, shrink_birth=3
    )

    mat = engine.material.create_conc(
        'C50', eCode='JTG3362_2018', eGrade='C50',
        nCrepShrk=1, dDmp=0.050, no=1
    )
    mat_nos.append(mat.no)

    mat = engine.material.create_prestressed(
        '钢绞线-1860', eCode='JTG3362_2018', eGrade='Strand1860', dDmp=0.050, no=2
    )
    mat_nos.append(mat.no)

    mat = engine.material.create_rebar(
        'HRB400', eCode='JTG3362_2018', eGrade='HRB400', dDmp=0.050, no=3
    )
    mat_nos.append(mat.no)

    return mat_nos


if __name__ == "__main__":
    from ._0_engine import engine
    mat_nos = build_materials(engine)
    print(mat_nos)
    print(engine.material.all())