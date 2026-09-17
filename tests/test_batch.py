"""batch 批量执行单元测试（全程 mock HTTP，无需 OSIS 服务端）

覆盖：
- with 内批量建节点/单元：命令合并发送，请求数远小于命令数
- get() 批模式返回 LazyRef：身份属性零查询，真实属性访问才物化
- 链式调用（loadcase_manager.get(...).create_*）：物化一次后全部排队
- 自动编号批内报错（基类守卫），批外行为不变
- 异常丢弃缓冲 / 冲刷失败 BatchError / 嵌套 batch
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pyosis.core.client as client_mod


class FakeOSISServer:
    """内存版假 OSIS：执行 OSIS_Run 命令流、应答查询接口"""

    def __init__(self):
        self.nodes: dict[int, dict] = {}
        self.elements: dict[int, dict] = {}
        self.loadcases: dict[str, dict] = {}
        self.requests: list[tuple[str, int]] = []   # (接口名, 命令条数)
        self.fail_next_run = False

    # -- HTTP 层 --
    def post(self, url, data=None, headers=None, timeout=None, **kw):
        ep = url.split("/")[-1]
        payload = json.loads(data.decode("utf-8")) if isinstance(data, bytes) else json.loads(data or "{}")
        self.requests.append((ep, payload.get("strCmd", "").count(";")))
        return self._Resp(self._route(ep, payload))

    class _Resp:
        def __init__(self, obj):
            self._obj = obj
            self.status_code = 200
            self.ok = True
            self.content = b"x"
            self.text = ""

        def json(self):
            return self._obj

    def _route(self, ep, payload) -> dict:
        if ep == "OSIS_Run":
            if self.fail_next_run:
                return {"success": False, "error": "节点不存在"}
            for cmd in filter(None, payload.get("strCmd", "").split(";")):
                parts = cmd.split(",")
                if parts[0] == "Node":
                    self.nodes[int(parts[1])] = {
                        "no": int(parts[1]), "x": float(parts[2]),
                        "y": float(parts[3]), "z": float(parts[4]),
                    }
                elif parts[0] == "Element":
                    self.elements[int(parts[1])] = {"no": int(parts[1])}
                elif parts[0] == "LoadCase":
                    self.loadcases[parts[1]] = {
                        "name": parts[1], "type": parts[2],
                        "scalar": float(parts[3]) if len(parts) > 3 else 1.0,
                        "prompt": "",
                    }
            return {"success": True, "error": ""}
        if ep == "GetAllNodeInfo":
            return {"success": True, "data": list(self.nodes.values())}
        if ep == "GetNodeInfoByNos":
            return {"success": True,
                    "data": [self.nodes.get(n) for n in payload.get("no", [])]}
        if ep == "GetAllElementInfo":
            return {"success": True, "data": list(self.elements.values())}
        if ep == "GetElementInfoByNos":
            return {"success": True,
                    "data": [self.elements.get(n) for n in payload.get("no", [])]}
        if ep == "GetLoadCaseInfoByNames":
            return {"success": True,
                    "data": [self.loadcases.get(n) for n in payload.get("name", [])]}
        return {"success": True, "data": []}


server = FakeOSISServer()
client_mod.session.post = server.post


from pyosis.core.batch import batch, flush, batch_state, BatchError  # noqa: E402
from pyosis.core.basic_manager import LazyRef  # noqa: E402
from pyosis.node import node_manager  # noqa: E402
from pyosis.element import element_manager  # noqa: E402
from pyosis.load import loadcase_manager  # noqa: E402


def test_bulk_create():
    """with 内批量建节点+单元：命令合并发送"""
    server.requests.clear()
    with batch():
        for i in range(50):
            node_manager.create(i + 1, float(i), 0.0, 0.0)      # 显式编号
        for i in range(30):
            element_manager.create_beam3d(i + 1, i + 1, i + 2, 1, 1, 1)
        assert server.requests == []                            # 全程 0 请求
    assert server.requests == [("OSIS_Run", 80)], server.requests
    assert len(server.nodes) == 50 and len(server.elements) == 30
    print("test_bulk_create: OK（80 条命令 1 次请求）")


def test_lazy_ref():
    """get() 批模式返回 LazyRef：身份零查询，真实属性才物化"""
    server.requests.clear()
    with batch():
        node_manager.create(500, 1.5, 2.5, 3.5)
        ref = node_manager.get(500)
        assert isinstance(ref, LazyRef)
        assert ref.no == 500                    # 身份属性：零查询
        assert server.requests == []
        assert ref.x == 1.5 and ref.y == 2.5    # 真实属性：物化（冲刷+查询）
        kinds = [r[0] for r in server.requests]
        assert kinds == ["OSIS_Run", "GetNodeInfoByNos"], kinds
        again = node_manager.get(500)
        assert again.x == 1.5                   # 已物化，直接读缓存对象
    print("test_lazy_ref: OK")


def test_chained_loadcase():
    """链式调用：get 后连续 create_*，幽灵方法全程零请求纯排队"""
    server.requests.clear()
    server.loadcases.clear()
    with batch():
        lc = loadcase_manager.create("LC1", "USER")
        assert server.requests == []            # create 尾部 get 返回 LazyRef，零查询
        lc.create_nforce(1)                     # 方法访问 → 幽灵实例直接排队
        lc.create_gravity()
        lc.create_cable_force(15)
        assert server.requests == []            # 全程零请求
    # 退出冲刷：LoadCase + NFORCE + GRAVITY + CFORCE 共 4 条，1 次请求
    assert server.requests == [("OSIS_Run", 4)], server.requests
    print("test_chained_loadcase: OK（4 条命令链式全程零查询）")


def test_auto_number_guarded_in_batch():
    """自动编号批内报错（基类守卫），批外行为不变"""
    server.nodes.clear()
    try:
        with batch():
            node_manager.create(None, 0.0, 0.0, 0.0)
        raise AssertionError("batch 内自动编号应当报错")
    except RuntimeError as ex:
        assert "自动编号" in str(ex)
    # 批外自动编号正常
    no = node_manager.create(None, 7.0, 0.0, 0.0).no
    assert no == 1, no
    print("test_auto_number_guarded_in_batch: OK")


def test_outside_batch_unchanged():
    """批外逐条执行（现状行为不变）"""
    server.requests.clear()
    node_manager.create(1000, 9.0, 0.0, 0.0)
    kinds = [r[0] for r in server.requests]
    assert kinds == ["OSIS_Run", "GetNodeInfoByNos"], kinds
    print("test_outside_batch_unchanged: OK", kinds)


def test_materialize_missing_raises():
    """物化时对象不存在：报错并说明主键"""
    with batch():
        ref = node_manager.get(4321)
        try:
            ref.x
            raise AssertionError("物化不存在的对象应当报错")
        except RuntimeError as ex:
            assert "4321" in str(ex)
    print("test_materialize_missing_raises: OK")


def test_exception_discards_buffer():
    """异常退出：丢弃本次缓冲，抛原异常"""
    server.requests.clear()
    n_before = len(server.nodes)
    try:
        with batch():
            node_manager.create(6000, 0.0, 0.0, 0.0)
            raise ValueError("用户异常")
    except ValueError:
        pass
    assert server.requests == [] and not batch_state.buffer
    assert len(server.nodes) == n_before
    print("test_exception_discards_buffer: OK")


def test_flush_error_raises_batch_error():
    """冲刷失败：抛 BatchError（不重试不二分）"""
    try:
        with batch():
            node_manager.create(7000, 0.0, 0.0, 0.0)
            server.fail_next_run = True
            flush()                       # with 内手动冲刷 → 失败
            raise AssertionError("应当抛 BatchError")
    except BatchError as ex:
        assert "节点不存在" in str(ex)
        assert not batch_state.buffer
    finally:
        server.fail_next_run = False
    print("test_flush_error_raises_batch_error: OK")


def test_nested_batch():
    """嵌套：内层退出不冲刷，最外层统一冲刷"""
    server.requests.clear()
    with batch():
        with batch():
            node_manager.create(8000, 0.0, 0.0, 0.0)
        assert server.requests == []
        node_manager.create(8001, 0.0, 0.0, 0.0)
    assert server.requests == [("OSIS_Run", 2)], server.requests
    print("test_nested_batch: OK")


if __name__ == "__main__":
    test_bulk_create()
    test_lazy_ref()
    test_chained_loadcase()
    test_auto_number_guarded_in_batch()
    test_outside_batch_unchanged()
    test_materialize_missing_raises()
    test_exception_discards_buffer()
    test_flush_error_raises_batch_error()
    test_nested_batch()
    print("\n全部 batch 单测通过")
