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
    
    # 收缩徐变模型（编号 1，供 C50 使用）
    creep_shrink = engine.prop.creep_shrink.create(1, "收缩徐变", 75.00, 7, 5.000, 3)
    _expect_attr(creep_shrink, "no", 1)
    # 获取收缩徐变模型
    cs = engine.prop.creep_shrink.get(1)
    if cs is None:
      raise ValueError("creep_shrink.get(1) 返回 None")
    _expect_attr(cs, "no", 1)
    _expect_attr(cs, "name", "收缩徐变")
    engine.prop.creep_shrink.get(creep_shrink.no)
    # 获取全部收缩徐变模型
    all_cs = engine.prop.creep_shrink.all()
    if len(all_cs) != 1:
      raise ValueError(f"creep_shrink.all() 期望 1 条，实际 {len(all_cs)}")
    # 创建新的收缩徐变模型
    cs2 = engine.prop.creep_shrink.create(2, "测试收缩徐变", 70.0, 7, 5.0, 3)
    _expect_attr(cs2, "no", 2)
    # 重编号
    engine.prop.creep_shrink.renumber(2,3)
    # 删除
    engine.prop.creep_shrink.delete(3)
    if engine.prop.creep_shrink.get(3) is not None:
        raise ValueError("creep_shrink delete 后 get(3) 应为 None")
    if len(engine.prop.creep_shrink.all()) != 1:
      raise ValueError("删除 no=3 后应只剩 1 条")
    # 材料 1: C50 混凝土
    mat1 = material.create(1, "C50", "CONC", "JTG3362_2018", "C50", nCrepShrk=1, dDmp=0.050)
    _expect_attr(mat1, "name", "C50")

    # 材料 2: HRB400 钢筋
    mat2 = material.create(2, "HRB400", "REBAR", "JTG3362_2018", "HRB400", dDmp=0.050)
    _expect_attr(mat2, "name", "HRB400")

    # 材料 3: 钢绞线-1860
    mat3 = material.create(3, "钢绞线-1860", "PRESTRESSED", "JTG3362_2018", "Strand1860", dDmp=0.050)
    _expect_attr(mat3, "name", "钢绞线-1860")

    # 材料 4: 钢材1
    mat4 = material.create(4, "钢材1", "STEEL", "JTGD64_2015", "Q235")
    _expect_attr(mat4, "name", "钢材1")

    # 材料 5: 自定义材料
    mat5 = material.create(5, "自定义材料", "CUSTOM", dE=1, dG=0, dMu=0, dExpCoeff=0, dUnitWeight=0, dDensity=0, dDmp=0)
    _expect_attr(mat5, "name", "自定义材料")

    mats = material.all()
    if len(mats) <= 0:
        raise Exception("material.all() 为空")
    # 获取材料数量
    if material.count() != len(mats):
        raise ValueError("material.count() 不符")
    # 获取材料
    got = material.get(mat5.no)
    _expect_attr(got, "name", mat5.name)

    # 修改材料编码
    new_mat5 = material.renumber(mat5.no,mat5.no+1)
    _expect_attr(new_mat5, "no", mat5.no+1)

    # 获取全部材料
    all_mat = material.all()
    if len(all_mat) == 0:
        raise ValueError("material.all() 为空")

    # 删除材料
    no_list = [new_mat5.no]
    for no in no_list:
        material.delete(no)
    # 创建荷载-位移曲线
    engine.prop.pu_curve.create(99, "P-U曲线-测试", 0, 3, 0.0, 0.01, 0.02, 0.0, 100.0, 150.0)
    got = engine.prop.pu_curve.get(99)
    _expect_attr(got, "no", 99)
    all_pu = engine.prop.pu_curve.all()
    if len(all_pu) < 1:
        raise ValueError("pu_curve.all() 为空")
    # 重编号
    engine.prop.pu_curve.renumber(99,100)
    # 删除
    engine.prop.pu_curve.delete(100)
    if engine.prop.pu_curve.get(100) is not None:
        raise ValueError("pu_curve delete 后 get(100) 应为 None")
    return [mat1.no, mat2.no, mat3.no, mat4.no]

if __name__ == "__main__":
    from _0_engine import engine
    engine.material.clear()
    mat_nos = build_materials(engine)
    print(mat_nos)
    print(engine.material.all())
