"""engine 方法签名内省（transfer 专用）。

供两处使用:
    - generator: 把长参数列表的调用生成为关键字实参,参数重排不再破坏生成的脚本
    - out_to_python: 取方法 docstring 首行作为生成代码的注释

engine 属性是 property 描述符,链式调用中间还有 .get(...) 返回的实体对象,
所以这里按" property 返回注解 → 管理器类 → get 注解 → 实体类"逐层解析,
全程不实例化任何管理器。
"""

from __future__ import annotations

import inspect
import sys
from typing import Any


def _eval_annotation(target: Any, owner: Any = None) -> list[type]:
    """把返回注解规整成类列表(展开 Optional/Union/list 等泛型)。

    target 为字符串注解时(from __future__ annotations 下必然如此),
    在 owner 函数所属模块的命名空间里求值。
    """
    ann = target
    if isinstance(ann, str):
        mod = sys.modules.get(getattr(owner, "__module__", "")) if owner is not None else None
        ns = dict(vars(mod)) if mod is not None else {}
        try:
            ann = eval(ann, ns)  # noqa: S307 - 注解来自本仓库代码
        except Exception:
            return []
    out: list[type] = []
    if isinstance(ann, type):
        out.append(ann)
    else:
        for arg in getattr(ann, "__args__", ()) or ():
            if isinstance(arg, type):
                out.append(arg)
            else:
                for inner in getattr(arg, "__args__", ()) or ():
                    if isinstance(inner, type):
                        out.append(inner)
    return out


def _walk_class(cls: type, name: str) -> Any:
    """在类(含基类)上找属性;property 描述符取其 fget 继续向下解析。"""
    attr = vars(cls).get(name)
    if attr is None:
        return None
    if isinstance(attr, property):
        return attr.fget
    return attr


def _return_class_of(func: Any) -> type | None:
    """取函数返回注解中的第一个类(property.fget → 管理器类等)。"""
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return None
    if sig.return_annotation is inspect.Parameter.empty:
        return None
    for cls in _eval_annotation(sig.return_annotation, func):
        return cls
    return None


def resolve_callable(engine: object, dotted: str) -> Any:
    """解析 'engine.section.get' / 'engine.prop.creep_shrink.create' 等点路径。

    实例属性直接 getattr(property 已实例化解析);类级回退按
    "property → fget → 返回注解类" 逐层下钻,全程不实例化。失败返回 None。
    """
    parts = dotted.split(".")
    if len(parts) < 2 or parts[0] != "engine":
        return None

    # 1) 实例直取
    try:
        obj: Any = engine
        for p in parts[1:]:
            obj = getattr(obj, p)
        if callable(obj):
            return obj
    except AttributeError:
        pass

    # 2) 类级解析(OSISEngine 上的 property 需经 fget → 返回注解类下钻)
    from pyosis.core.engine import OSISEngine

    obj: Any = OSISEngine
    for p in parts[1:]:
        if isinstance(obj, type):
            obj = _walk_class(obj, p)
        else:
            # 上一段解析出的是 getter 函数:落到其返回注解类上继续找
            cls = _return_class_of(obj) if callable(obj) else None
            obj = _walk_class(cls, p) if cls is not None else None
        if obj is None:
            return None
        if isinstance(obj, (staticmethod, classmethod)):
            obj = obj.__func__
    return obj if callable(obj) else None


def resolve_chain_method(engine: object, get_path: str, method_name: str) -> Any:
    """解析链式路由的终点方法: engine.<mgr>.get(k).<method>。

    get 的返回注解给出实体类(Section/LoadCase/...),再在其上找 method。
    """
    get_func = resolve_callable(engine, get_path)
    if get_func is None:
        return None
    try:
        sig = inspect.signature(get_func)
    except (ValueError, TypeError):
        return None
    if sig.return_annotation is inspect.Parameter.empty:
        return None
    for cls in _eval_annotation(sig.return_annotation, get_func):
        target = vars(cls).get(method_name)
        if target is not None and callable(target):
            return target
    return None


def positional_param_names(func: Any) -> tuple[str, ...] | None:
    """取函数的显式位置参数名;带 *args/**kwargs 或解析失败时返回 None。

    类上取到的方法带 self,跳过;返回 None 表示调用方应保持位置实参生成。
    """
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return None
    names: list[str] = []
    for p in sig.parameters.values():
        if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
            return None
        if p.kind is p.POSITIONAL_ONLY:
            return None
        if p.kind is p.KEYWORD_ONLY:
            continue
        names.append(p.name)
    if names and names[0] in ("self", "cls"):
        names = names[1:]
    return tuple(names)
