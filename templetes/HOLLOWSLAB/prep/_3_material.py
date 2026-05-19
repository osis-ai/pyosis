from typing import Any

from pyosis.core.engine import OSISEngine

def _expect_attr(obj: Any, attr: str, expected: Any) -> None:
    if not hasattr(obj, attr):
        raise TypeError(f"对象没有属性 {attr!r}: {type(obj).__name__}")
    actual = getattr(obj, attr)
    if actual != expected:
        raise ValueError(f"材料属性 {attr} 不符: 期望 {expected!r}, 实际 {actual!r}")

def build_materials(engine: OSISEngine) -> list[int]:
    """创建材料，返回材料编号列表 [1, 2, 3]
    
    材料编号（显式定义，幂等执行）：
    - 1: C50 混凝土
    - 2: HRB400 钢筋  
    - 3: 1860MPa 钢绞线
    """
    material = engine.material
    
    # 收缩徐变模型（编号 1）
    creep_shrink = engine.prop.creep_shrink.create(1, "收缩徐变", 75.00, 7, 5.000, 3)
    _expect_attr(creep_shrink, "no", 1)

    # 材料 1: C50 混凝土
    mat1 = material.create_conc("C50", "JTG3362_2018", "C50", nCrepShrk=1, dDmp=0.050, no=1)
    _expect_attr(mat1, "name", "C50")

    # 材料 2: HRB400 钢筋
    mat2 = material.create_rebar("HRB400", "JTG3362_2018", "HRB400", dDmp=0.050, no=2)
    _expect_attr(mat2, "name", "HRB400")

    # 材料 3: 钢绞线-1860
    mat3 = material.create_prestressed("钢绞线-1860", "JTG3362_2018","Strand1860", dDmp=0.050, no=3)
    _expect_attr(mat3, "name", "钢绞线-1860")

    # 材料 4: 钢材1
    mat4 = material.create_steel("钢材1","JTGD64_2015","Q235")
    _expect_attr(mat4, "name", "钢材1")

    # 材料 5: 自定义材料
    mat5 = material.create_custom("自定义材料")
    _expect_attr(mat5, "name", "自定义材料")

    mats = material.all()
    if len(mats) <= 0:
        raise Exception("material.all() 为空")
    # 获取材料数量
    if material.count() != 5:
        raise ValueError("material.count() 不符，期望 5，实际 {material.count()}")
    # 获取材料
    got = material.get(mat5.no)
    _expect_attr(got, "name", mat5.name)

    # 修改材料编码
    new_mat5 = material.renumber(mat5.no,mat5.no+1)
    _expect_attr(new_mat5, "no", mat5.no+1)

    # 获取全部材料
    all_mat = material.all()
    if len(all_mat) != 5:
        raise ValueError("material.all() 为空，期望至少存在 5 条材料")

    # 删除材料
    no_list = [new_mat5.no]
    for no in no_list:
        material.delete(no)

    return [mat1.no, mat2.no, mat3.no, mat4.no]

if __name__ == "__main__":
    from _0_engine import engine
    mat_nos = build_materials(engine)
    print(mat_nos)
    print(engine.material.all())
