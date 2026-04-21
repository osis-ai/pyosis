from _0_engine import engine

material = engine.material
n_creep_shrink = 1
engine.prop.creep_shrink.create(n_creep_shrink, "收缩徐变", 75.00, 7, 5.000, 3)
mat1 = material.create_conc("C50", "JTG3362_2018", "C50", n_creep_shrink, 0.050)
mat2 = material.create_rebar("HRB400", "JTG3362_2018", "HRB400", 0.050)
mat3 = material.create_prestressed("钢绞线-1860", "JTG3362_2018","Strand1860", 0.050)

mat_no = [mat1.no, mat2.no, mat3.no]
