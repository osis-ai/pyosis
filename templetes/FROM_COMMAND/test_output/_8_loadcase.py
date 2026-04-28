"""荷载工况"""

from pyosis.core.engine import OSISEngine

def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:
    """荷载工况"""

    # [LoadCase] LoadCase
    # 原始命令: LoadCase,自重,D,1.0,结构自重
    # 参数:
    #   strName=自重
    #   eLoadCaseType=D
    #   dScalar=1.0
    #   strPrompt=结构自重
    engine.load.create(strName="自重", eLoadCaseType="D", dScalar=1, strPrompt="结构自重")

    # [LoadCase] LoadCase
    # 原始命令: LoadCase,活载,CS,1.0,施工荷载
    # 参数:
    #   strName=活载
    #   eLoadCaseType=CS
    #   dScalar=1.0
    #   strPrompt=施工荷载
    engine.load.create(strName="活载", eLoadCaseType="CS", dScalar=1, strPrompt="施工荷载")

    return []

if __name__ == "__main__":
    from ._0_engine import engine
    mats = engine.material.all()
    mat_nos = [m.no for m in mats]
    elems = engine.element.all()
    elem_nos = [e.no for e in elems]
    elem_groups = engine.element.group.all()
    elem_group_names = [eg.name for eg in elem_groups]
    geos = engine.geometry.all()
    geo_names = [s.name for s in geos]
    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)
    print(lc_names)
    print(engine.load.all())