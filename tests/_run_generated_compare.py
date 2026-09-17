"""对 4 个生成的项目跑 main.py（假 OSIS），对比 开/关 batch 的 OSIS_Run 请求数"""
import sys, os, json, runpy, types, io, contextlib, traceback

PYOSIS_SRC = r"D:\OSIS 5\pyosis\src"
BASE = os.path.join(os.environ["TEMP"], "pyosis_batch_test")
sys.path.insert(0, PYOSIS_SRC)

import pyosis
import pyosis.core.client as client_mod

REQS = []

class Resp:
    status_code, ok, content, text = 200, True, b"x", ""
    def __init__(self, obj): self._j = obj
    def json(self): return self._j

class Rec(dict):
    """万能记录：缺失键按启发式返回默认值（仅供 mock 运行验证）"""
    def __missing__(self, k):
        lk = str(k).lower()
        if lk.endswith('s') or lk.endswith('list') or lk.endswith('vec'):
            return []
        if lk in ('no', 'type', 'num', 'count', 'index', 'stage'):
            return 1
        if lk.startswith(('is', 'has', 'b', 'selected', 'plotted')):
            return False
        if lk[-1:] in 'xyz' or lk.endswith(('value', 'coeff', 'length', 'area', 'width', 'height', 'temp', 'dur', 'birth', 'death', 'time', 'e', 'mu', 'rho', 'force', 'moment', 'angle', 'ratio')):
            return 0.0
        return ""
    def get(self, k, default=None):
        if k in self:
            return super().get(k, default)
        if default is not None:
            return default
        return self.__missing__(k)

def fake_post(url, data=None, headers=None, timeout=None, **kw):
    ep = url.split("/")[-1]
    payload = json.loads(data.decode("utf-8") if isinstance(data, bytes) else (data or "{}"))
    REQS.append((ep, payload.get("strCmd", "").count(";")))
    if ep == "OSIS_Run":
        return Resp({"success": True, "error": ""})
    keys = payload.get("no") or payload.get("name") or []
    recs = [Rec(no=(int(k) if str(k).isdigit() else 1), name=str(k), type=1, elements=[], nodes=[]) for k in keys]
    return Resp({"success": True, "data": recs})

client_mod.session.post = fake_post

def run(proj: str, with_batch: bool):
    REQS.clear()
    # 清理上一项目的模块缓存，确保每个项目跑自己的代码
    for k in [k for k in sys.modules if k.startswith('prep') or k == 'main']:
        del sys.modules[k]
    real = pyosis.batch
    if not with_batch:
        nullc = type("null", (), {"__enter__": lambda s: None, "__exit__": lambda s, *a: None})
        pyosis.batch = lambda: nullc()
    try:
        old = sys.argv, sys.path
        sys.argv = ["main.py"]
        if proj not in sys.path:
            sys.path.insert(0, proj)
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(os.path.join(proj, "main.py"), run_name="__main__")
        sys.argv, sys.path = old
    except SystemExit:
        pass
    finally:
        pyosis.batch = real
    runs = [r for r in REQS if r[0] == "OSIS_Run"]
    return len(runs), sum(r[1] for r in runs)

fail = 0
for name in sorted(os.listdir(BASE)):
    proj = os.path.join(BASE, name)
    if not os.path.isdir(os.path.join(proj, "prep")):
        continue
    try:
        n_on, c_on = run(proj, True)
        n_off, c_off = run(proj, False)
        print(f"{name}: batch开 {n_on} 次请求/{c_on} 条命令 | batch关 {n_off} 次请求/{c_off} 条命令 | 压缩 {n_off/max(n_on,1):.0f}x")
    except Exception:
        fail += 1
        print(f"{name}: 运行失败")
        traceback.print_exc(limit=3)
print("\n失败项目数:", fail)
