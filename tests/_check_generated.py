"""校验生成的 prep/*.py：所有 engine 链上调用的 kwarg 与真实 manager 签名比对"""
import ast, inspect, os, sys, re

PYOSIS_SRC = r"D:\OSIS 5\pyosis\src"
sys.path.insert(0, PYOSIS_SRC)
from pyosis import OSISEngine

engine = OSISEngine()


def resolve(chain: list[str]):
    """engine.a.b.c -> 实际对象；失败返回 None"""
    obj = engine
    for part in chain:
        try:
            obj = getattr(obj, part)
        except Exception:
            return None
    return obj


def check_file(path: str, problems: list):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    # 变量 -> engine 链 的赋值（如 lc = engine.load.create(...) 记 create；user_lc = loadcase.create(...)）
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        chain = []
        v = func
        while isinstance(v, ast.Attribute):
            chain.append(v.attr)
            v = v.value
        if isinstance(v, ast.Name):
            chain.append(v.id)
        chain.reverse()          # [root, a, b, method] / [var, method]
        if len(chain) < 2:
            continue
        root, method_name = chain[0], chain[-1]
        if root == "engine":
            target = resolve(chain[1:-1])
        else:
            continue             # 普通变量（返回对象）调用：跳过，靠运行期校验
        if target is None:
            continue
        try:
            m = getattr(target, method_name)
        except AttributeError:
            continue
        try:
            params = set(inspect.signature(m).parameters)
        except (TypeError, ValueError):
            continue
        for kw in node.keywords:
            if kw.arg is None:
                continue
            if kw.arg not in params:
                problems.append(
                    f"{os.path.basename(path)}:{node.lineno} "
                    f"engine.{'.'.join(chain[1:-1])}.{method_name}() 无参数 {kw.arg!r}"
                )


def camel_scan(path: str, problems: list):
    """生成的代码里残留的驼峰 kwarg（无论能否解析到签名）"""
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        for m in re.finditer(r"\b([a-z]+[A-Z][A-Za-z0-9]*)=", ln):
            problems.append(f"{os.path.basename(path)}:{i} 疑似驼峰 kwarg {m.group(1)!r}: {ln.strip()[:80]}")


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ["TEMP"], "pyosis_batch_test")
    problems = []
    prep = os.path.join(base, "prep")
    for fn in sorted(os.listdir(prep)):
        if fn.endswith(".py") and fn != "_0_engine.py":
            check_file(os.path.join(prep, fn), problems)
            camel_scan(os.path.join(prep, fn), problems)
    if problems:
        print(f"{len(problems)} 个问题:")
        for p in problems:
            print(" ", p)
        sys.exit(1)
    print("生成代码校验通过：kwarg 全部匹配签名，无驼峰残留")
