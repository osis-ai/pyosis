"""标识归一：把 C++ 侧忠实的 PREP 取值转成 Python 侧统一的“无此标识”。

C++ 不做加工，直接透传 PREP：
    - 按名称寻址的对象（截面种类、钢束、工况等）没有编号，no 返回 -1
    - 按编号寻址的对象（节点、单元、边界）没有名称，name 返回字符串 "-1"

Python 侧统一成 None，避免用户被 -1 / "-1" 这种哨兵值绊倒。
"""

from __future__ import annotations

#: C++ 侧表示“无此标识”的哨兵：数值 -1 与字符串 "-1"
_SENTINEL = -1


def as_no(value):
    """编号归一：None / -1 / -1.0 / "-1" / "-1.0" → None，其余原样返回。"""
    if value is None:
        return None
    if isinstance(value, bool):     # bool 是 int 子类，先排掉
        return value
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return None
        try:
            value = int(s)
        except ValueError:
            try:
                value = float(s)
            except ValueError:
                return value        # 非数值字符串：原样返回
    if isinstance(value, (int, float)) and value == _SENTINEL:
        return None
    return value


def as_name(value):
    """名称归一：None / "" / "-1" → None，其余原样返回。"""
    if value is None:
        return None
    s = str(value).strip()
    if s in ("", "-1"):
        return None
    return value


__all__ = ["as_no", "as_name"]
