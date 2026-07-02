"""
测试删除占用逻辑（DependencyError / get_references）

验证 Material / Section / Node / Element / TendonShape / LoadCase
被占用时 delete 抛出 DependencyError，解除依赖后可正常删除。

使用方式:
    python tests/test_delete_occupied.py

前置条件: OSIS 已打开并创建项目。
"""

from __future__ import annotations

from dataclasses import dataclass

from pyosis.core import DependencyError, get_references
from pyosis.core.engine import OSISEngine


@dataclass
class ModelCtx:
    """测试模型中的关键编号与名称。"""
    elem_no: int
    node_used: int
    node_free: int
    bd_no: int
    tendon_free: str
    tendon_used: str
    lc_free: str
    lc_used: str
    lc_ps: str
    stage_no: int
    tendon_prop: str
    spline_name: str


def _assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _non_empty_deps(deps: dict[str, list]) -> dict[str, list]:
    result = {}
    for kind, refs in deps.items():
        if refs:
            result[kind] = refs
    return result


def _deps_contain(deps: dict[str, list], key: str, value) -> None:
    refs = deps.get(key, [])
    _assert_true(value in refs, f"依赖 {key} 应包含 {value!r}，实际: {deps}")


def _expect_dependency_error(delete_fn, entity_type: str) -> None:
    """执行 delete，期望抛出 DependencyError 并打印报错。"""
    caught = None
    try:
        delete_fn()
    except DependencyError as err:
        caught = err
        print(f"  报错: {err}")
    else:
        raise AssertionError(f"删除被占用 {entity_type} 应抛出 DependencyError")

    _assert_true(caught.entity_type == entity_type, f"entity_type 应为 {entity_type!r}")
    _assert_true(len(caught.dependencies) > 0, "dependencies 不应为空")


def _setup_model(engine: OSISEngine) -> ModelCtx:
    """创建测试模型。"""
    mat = engine.material
    sec = engine.section
    node = engine.node
    elem = engine.element
    boundary = engine.boundary
    load = engine.load
    stage = engine.stage
    tendon = engine.tendon
    geometry = engine.geometry
    # 创建材料
    mat.create(1, "C50-占用", "CONC", "JTG3362_2018", "C50")
    mat.create(2, "C50-空闲", "CONC", "JTG3362_2018", "C50")
    mat.create(3, "钢绞线", "PRESTRESSED", "JTG3362_2018", "Strand1860")
    # 创建截面
    sec.create(1, "截面-占用", "CIRCLE", "Solid", 0.5, 0.25)
    sec.create(2, "截面-空闲", "CIRCLE", "Solid", 0.3, 0.15)
    # 创建节点
    node.create(1, 0.0, 0.0, 0.0)
    node.create(2, 1.0, 0.0, 0.0)
    node.create(99, 10.0, 0.0, 0.0)
    # 创建单元
    elem.create(1, "beam3d", 1, 2, 1, 1, 1)
    # 创建边界
    bd = boundary.create(10, "GENERAL", x=1, y=1, z=1, rx=1, ry=0, rz=1, rw=0)
    bd.assign("a", 1)
    # 创建荷载工况
    lc_node = load.create("节点荷载工况", "USER")
    lc_node.create_nforce(1, dFx=1000.0)
    # 创建单元荷载工况
    lc_elem = load.create("单元荷载工况", "USER")
    lc_elem.create_line_load(
        1, 0, 0,
        0.0, 0.0, 0.0, 0.0, 0.0, -1000.0, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 0.0, 0.0, -1000.0, 0.0, 0.0, 0.0,
    )
    # 创建钢束特性
    tendon.prop.create_in(
        "tp-test", mat=3, code="GBT5224_2014",
        diameter=15.2, num=1, pipe=0.09,
    )
    # 创建钢束线型
    geometry.create("钢束线型", "arc3d", "TENDON",
        0.0, 0.0, 0.0, 0.0,
        0.33, 0.0, 0.0, 1.0,
        0.67, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 0.0,
    )
    # 创建单元组
    eg = engine.element.group.create("占用测试单元组", "c")
    eg.add(1)

    tendon_free = "空闲钢束"
    tendon_used = "占用测试钢束"
    tendon.shape.create_arc3d(tendon_free, 1, "tp-test", "占用测试单元组", "钢束线型")
    tendon.shape.create_arc3d(tendon_used, 1, "tp-test", "占用测试单元组", "钢束线型")
    # 创建预应力工况
    lc_ps = "预应力工况"
    load.create(lc_ps, "PS").create_prestress(tendon_used, "BOTH", "ST", 1.0e6, 1.0e6)
    # 创建空闲荷载工况
    lc_free = "空闲荷载工况"
    lc_used = "阶段占用工况"
    load.create(lc_free, "CS")
    load.create(lc_used, "CS")
    # 创建阶段
    stg = stage.create(1, "测试阶段", 7)
    stg.define_loadcase(1, 1, "", lc_used)

    return ModelCtx(
        elem_no=1,
        node_used=1,
        node_free=99,
        bd_no=10,
        tendon_free=tendon_free,
        tendon_used=tendon_used,
        lc_free=lc_free,
        lc_used=lc_used,
        lc_ps=lc_ps,
        stage_no=1,
        tendon_prop="tp-test",
        spline_name="钢束线型",
    )


# 查询引用
def test_refs_node_free(ctx: ModelCtx) -> None:
    deps = _non_empty_deps(get_references("Node", no=ctx.node_free))
    _assert_true(len(deps) == 0, f"空闲节点不应有依赖，实际: {deps}")

# 节点被占用
def test_refs_node_occupied(ctx: ModelCtx) -> None:
    deps = _non_empty_deps(get_references("Node", no=ctx.node_used))
    _deps_contain(deps, "elements", ctx.elem_no)
    _deps_contain(deps, "boundaries", ctx.bd_no)
    _assert_true(len(deps.get("loads", [])) > 0, f"节点 1 应有 loads 依赖，实际: {deps}")

# 单元被占用
def test_refs_element_occupied(ctx: ModelCtx) -> None:
    deps = _non_empty_deps(get_references("Element", no=ctx.elem_no))
    _assert_true(len(deps.get("loads", [])) > 0, f"单元 1 应有 loads 依赖，实际: {deps}")

# 钢束形状被占用
def test_refs_tendon_shape_free(ctx: ModelCtx) -> None:
    deps = _non_empty_deps(get_references("TendonShape", name=ctx.tendon_free))
    _assert_true(len(deps) == 0, f"空闲钢束形状不应有依赖，实际: {deps}")

# 钢束形状被占用
def test_refs_tendon_shape_occupied(ctx: ModelCtx) -> None:
    deps = _non_empty_deps(get_references("TendonShape", name=ctx.tendon_used))
    _assert_true(len(deps.get("loads", [])) > 0, f"被占用钢束形状应有 loads 依赖，实际: {deps}")

# 荷载工况被占用
def test_refs_loadcase_free(ctx: ModelCtx) -> None:
    deps = _non_empty_deps(get_references("LoadCase", name=ctx.lc_free))
    _assert_true(len(deps) == 0, f"空闲荷载工况不应有依赖，实际: {deps}")

# 荷载工况被占用
def test_refs_loadcase_occupied(ctx: ModelCtx) -> None:
    deps = _non_empty_deps(get_references("LoadCase", name=ctx.lc_used))
    _deps_contain(deps, "stages", ctx.stage_no)


# 查询依赖
def test_get_dependencies_empty(engine: OSISEngine, ctx: ModelCtx) -> None:
    checks = [
        ("Material", engine.material.get_dependencies(2)),
        ("Section", engine.section.get_dependencies(2)),
        ("Node", engine.node.get_dependencies(ctx.node_free)),
        ("TendonShape", engine.tendon.shape.get_dependencies(ctx.tendon_free)),
        ("LoadCase", engine.load.get_dependencies(ctx.lc_free)),
    ]
    for label, deps in checks:
        non_empty = _non_empty_deps(deps)
        _assert_true(len(non_empty) == 0, f"空闲 {label} 不应有依赖，实际: {non_empty}")

# 删除空闲
def test_delete_unoccupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    engine.material.delete(2)
    engine.section.delete(2)
    engine.node.delete(ctx.node_free)
    engine.tendon.shape.delete(ctx.tendon_free)
    engine.load.delete(ctx.lc_free)

    _assert_true(engine.material.get(2) is None, "删除空闲材料后 get(2) 应为 None")
    _assert_true(engine.section.get(2) is None, "删除空闲截面后 get(2) 应为 None")
    _assert_true(engine.node.get(ctx.node_free) is None, "删除空闲节点后 get 应为 None")
    _assert_true(engine.tendon.shape.get(ctx.tendon_free) is None, "删除空闲钢束后 get 应为 None")
    _assert_true(engine.load.get(ctx.lc_free) is None, "删除空闲工况后 get 应为 None")


# 查询依赖被占用
def test_get_dependencies_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    mat_deps = _non_empty_deps(engine.material.get_dependencies(1))
    sec_deps = _non_empty_deps(engine.section.get_dependencies(1))
    node_deps = _non_empty_deps(engine.node.get_dependencies(ctx.node_used))
    elem_deps = _non_empty_deps(engine.element.get_dependencies(ctx.elem_no))
    tendon_deps = _non_empty_deps(engine.tendon.shape.get_dependencies(ctx.tendon_used))
    lc_deps = _non_empty_deps(engine.load.get_dependencies(ctx.lc_used))
    prop_deps = _non_empty_deps(engine.tendon.prop.get_dependencies(ctx.tendon_prop))
    spline_deps = _non_empty_deps(engine.geometry.get_dependencies(ctx.spline_name))
    bd_deps = _non_empty_deps(engine.boundary.get_dependencies(ctx.bd_no))

    _deps_contain(mat_deps, "elements", ctx.elem_no)
    _deps_contain(sec_deps, "elements", ctx.elem_no)
    _deps_contain(node_deps, "elements", ctx.elem_no)
    _assert_true(len(elem_deps.get("loads", [])) > 0, f"单元应有 loads 依赖，实际: {elem_deps}")
    _assert_true(len(tendon_deps.get("loads", [])) > 0, f"钢束应有 loads 依赖，实际: {tendon_deps}")
    _deps_contain(lc_deps, "stages", ctx.stage_no)
    _assert_true(len(prop_deps.get("tendonShapes", [])) > 0, f"钢束特性应有 tendonShapes 依赖，实际: {prop_deps}")
    _assert_true(len(spline_deps.get("tendonShapes", [])) > 0, f"样条曲线应有 tendonShapes 依赖，实际: {spline_deps}")
    _deps_contain(bd_deps, "entities", ctx.node_used)

# 删除材料被占用
def test_delete_material_occupied(engine: OSISEngine) -> None:
    def do_delete() -> None:
        engine.material.delete(1)
    _expect_dependency_error(do_delete, "Material")
    _assert_true(engine.material.get(1) is not None, "删除失败后材料 1 应仍存在")

# 删除截面被占用
def test_delete_section_occupied(engine: OSISEngine) -> None:
    def do_delete() -> None:
        engine.section.delete(1)
    _expect_dependency_error(do_delete, "Section")
    _assert_true(engine.section.get(1) is not None, "删除失败后截面 1 应仍存在")

# 删除节点被占用
def test_delete_node_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    def do_delete() -> None:
        engine.node.delete(ctx.node_used)
    _expect_dependency_error(do_delete, "Node")
    _assert_true(engine.node.get(ctx.node_used) is not None, "删除失败后节点 1 应仍存在")

# 删除单元被占用
def test_delete_element_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    def do_delete() -> None:
        engine.element.delete(ctx.elem_no)
    _expect_dependency_error(do_delete, "Element")
    _assert_true(engine.element.get(ctx.elem_no) is not None, "删除失败后单元 1 应仍存在")

# 删除钢束形状被占用
def test_delete_tendon_shape_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    def do_delete() -> None:
        engine.tendon.shape.delete(ctx.tendon_used)
    _expect_dependency_error(do_delete, "TendonShape")
    _assert_true(engine.tendon.shape.get(ctx.tendon_used) is not None, "删除失败后钢束形状应仍存在")

# 删除钢束特性被占用
def test_delete_tendon_prop_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    def do_delete() -> None:
        engine.tendon.prop.delete(ctx.tendon_prop)
    _expect_dependency_error(do_delete, "TendonProp")
    _assert_true(engine.tendon.prop.get(ctx.tendon_prop) is not None, "删除失败后钢束特性应仍存在")

# 删除边界被占用
def test_delete_boundary_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    def do_delete() -> None:
        engine.boundary.delete(ctx.bd_no)
    _expect_dependency_error(do_delete, "Boundary")
    _assert_true(engine.boundary.get(ctx.bd_no) is not None, "删除失败后边界应仍存在")

# 删除样条曲线被占用
def test_delete_spline_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    def do_delete() -> None:
        engine.geometry.delete(ctx.spline_name)
    _expect_dependency_error(do_delete, "Spline")
    _assert_true(engine.geometry.get(ctx.spline_name) is not None, "删除失败后样条曲线应仍存在")

# 删除荷载工况被占用
def test_delete_loadcase_occupied(engine: OSISEngine, ctx: ModelCtx) -> None:
    def do_delete() -> None:
        engine.load.delete(ctx.lc_used)
    _expect_dependency_error(do_delete, "LoadCase")
    _assert_true(engine.load.get(ctx.lc_used) is not None, "删除失败后工况应仍存在")

# 清空被占用
def test_clear_when_occupied(engine: OSISEngine) -> None:
    try:
        engine.material.clear()
    except Exception as err:
        print(f"  报错: {err}")
        _assert_true("被占用" in str(err), f"clear 异常信息应包含「被占用」，实际: {err}")
    else:
        raise AssertionError("clear 应抛出异常")


# 解除占用后删除
def test_delete_after_release(engine: OSISEngine, ctx: ModelCtx) -> None:
    """按依赖顺序解除占用，依次删除各实体。"""
    # 1) 施工阶段引用荷载工况
    engine.stage.delete(ctx.stage_no)
    _assert_true(len(_non_empty_deps(engine.load.get_dependencies(ctx.lc_used))) == 0,
                 "删除阶段后工况应无依赖")
    engine.load.delete(ctx.lc_used)

    # 2) 预应力荷载引用钢束形状
    engine.load.delete(ctx.lc_ps)
    _assert_true(len(_non_empty_deps(engine.tendon.shape.get_dependencies(ctx.tendon_used))) == 0,
                 "删除预应力工况后钢束应无依赖")
    engine.load.delete("节点荷载工况")
    engine.load.delete("单元荷载工况")

    # 3) 单元引用材料/截面/节点
    engine.element.delete(ctx.elem_no)
    _assert_true(len(_non_empty_deps(engine.material.get_dependencies(1))) == 0, "删除单元后材料应无依赖")
    _assert_true(len(_non_empty_deps(engine.section.get_dependencies(1))) == 0, "删除单元后截面应无依赖")
    node_deps = _non_empty_deps(engine.node.get_dependencies(ctx.node_used))
    _assert_true(
        ctx.elem_no not in node_deps.get("elements", []),
        f"删除单元后节点不应再被单元引用，实际: {node_deps}",
    )

    # 4) 边界、钢束特性、几何、单元组
    bd = engine.boundary.get(ctx.bd_no)
    if bd is not None:
        bd.assign("r", ctx.node_used)
    engine.boundary.delete(ctx.bd_no)
    node_deps = _non_empty_deps(engine.node.get_dependencies(ctx.node_used))
    _assert_true(len(node_deps) == 0, f"解除边界后节点应无依赖，实际: {node_deps}")
    engine.tendon.shape.delete(ctx.tendon_used)
    engine.tendon.prop.delete(ctx.tendon_prop)
    _assert_true(
        len(_non_empty_deps(engine.geometry.get_dependencies(ctx.spline_name))) == 0,
        "删除钢束形状后样条曲线应无依赖",
    )
    engine.geometry.delete(ctx.spline_name)
    engine.element.group.delete("占用测试单元组")

    engine.material.delete(1)
    engine.material.delete(3)
    engine.section.delete(1)
    engine.node.delete(ctx.node_used)
    engine.node.delete(2)

    _assert_true(engine.material.get(1) is None, "解除占用后删除材料 1 应成功")
    _assert_true(engine.section.get(1) is None, "解除占用后删除截面 1 应成功")
    _assert_true(engine.node.get(ctx.node_used) is None, "解除占用后删除节点 1 应成功")


def run_test(name: str, fn, *args) -> bool:
    try:
        fn(*args)
        print(f"[PASS] {name}")
        return True
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        return False


def main() -> None:
    engine = OSISEngine()
    print("清空项目...")
    engine.clear()

    ctx = _setup_model(engine)
    print(
        f"已创建测试模型: 单元 #{ctx.elem_no} 引用材料/截面/节点，"
        f"钢束 {ctx.tendon_used!r}，工况 {ctx.lc_used!r}\n"
    )

    tests = [
        ("get_references Node（空闲）", test_refs_node_free, ctx),
        ("get_references Node（被占用）", test_refs_node_occupied, ctx),
        ("get_references Element（被占用）", test_refs_element_occupied, ctx),
        ("get_references TendonShape（空闲）", test_refs_tendon_shape_free, ctx),
        ("get_references TendonShape（被占用）", test_refs_tendon_shape_occupied, ctx),
        ("get_references LoadCase（空闲）", test_refs_loadcase_free, ctx),
        ("get_references LoadCase（被占用）", test_refs_loadcase_occupied, ctx),
        ("get_dependencies（空闲）", test_get_dependencies_empty, engine, ctx),
        ("delete（空闲）", test_delete_unoccupied, engine, ctx),
        ("get_dependencies（被占用）", test_get_dependencies_occupied, engine, ctx),
        ("delete Material（被占用，应报错）", test_delete_material_occupied, engine),
        ("delete Section（被占用，应报错）", test_delete_section_occupied, engine),
        ("delete Node（被占用，应报错）", test_delete_node_occupied, engine, ctx),
        ("delete Element（被占用，应报错）", test_delete_element_occupied, engine, ctx),
        ("delete TendonShape（被占用，应报错）", test_delete_tendon_shape_occupied, engine, ctx),
        ("delete TendonProp（被占用，应报错）", test_delete_tendon_prop_occupied, engine, ctx),
        ("delete Boundary（被占用，应报错）", test_delete_boundary_occupied, engine, ctx),
        ("delete Spline（被占用，应报错）", test_delete_spline_occupied, engine, ctx),
        ("delete LoadCase（被占用，应报错）", test_delete_loadcase_occupied, engine, ctx),
        ("clear Material（存在占用，应报错）", test_clear_when_occupied, engine),
        ("delete（解除占用后）", test_delete_after_release, engine, ctx),
    ]

    passed = 0
    for name, fn, *args in tests:
        if run_test(name, fn, *args):
            passed += 1

    total = len(tests)
    failed = total - passed
    print("\n" + "=" * 50)
    print(f"完成: {passed} 通过, {failed} 失败, 共 {total} 项")
    print("=" * 50)

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
