"""manager 基类：batch 模式的延迟对象（LazyRef）与编号记账基础设施

batch 模式下的 get() 语义：
- 返回 LazyRef 延迟对象，零服务器交互
- 身份属性 name / no 直接返回主键（链式调用 engine.XXX.get(1).create_XXX
  只需要身份，全程不查询）
- 访问其他任意属性/方法时才"物化"：先自动冲刷缓冲，再查询服务器取回
  真实对象，之后完全代理真实对象（每个 LazyRef 只物化一次）

manager 接入方式（每个 manager 两处小改动，与具体命令无关）：
    class NodeManager(BasicManager):
        def _next_no(self) -> int:
            return self._batched_next_no(          # 1) 自动编号批内记账
                lambda: max((n.no for n in self._load()), default=0))

        def get(self, no):
            ...编号归一化与类型检查...
            lazy = self._batch_lazy(no)            # 2) batch 模式返回 LazyRef
            if lazy is not None:
                return lazy
            ...原有服务器查询逻辑...
"""

from __future__ import annotations

import functools
from contextlib import contextmanager
from typing import Any

from .batch import batch_state


class LazyRef:
    """batch 模式下 get() 的延迟对象

    由 BasicManager._batch_lazy 创建，用户不应直接实例化。
    - 身份属性（name/no）零查询直通
    - 方法访问 → 绑定到"幽灵实例"（类型正确、仅注入身份字段），
      调用即排队命令，零服务器交互——链式调用 get().create_xxx() 的关键
    - 数据字段访问 → 物化（冲刷 + 服务器查询）后返回真实值
    """

    __slots__ = ("_manager", "_key", "_real", "_ghost")

    def __init__(self, manager: "BasicManager", key: Any) -> None:
        object.__setattr__(self, "_manager", manager)
        object.__setattr__(self, "_key", key)
        object.__setattr__(self, "_real", None)
        object.__setattr__(self, "_ghost", None)

    # ── 身份属性：零查询直通 ──────────────────

    @property
    def name(self) -> Any:
        """对象名称（即 get 的主键），物化后返回真实值"""
        return self._key if self._real is None else self._real.name

    @property
    def no(self) -> Any:
        """对象编号（即 get 的主键），物化后返回真实值"""
        return self._key if self._real is None else self._real.no

    # ── 幽灵实例与物化 ────────────────────────

    def _ghost_method(self, attr: str):
        """方法访问：绑定到幽灵实例（真类型 + 身份字段），调用即排队"""
        if self._ghost is None:
            cls = self._ghost_class()
            ghost = object.__new__(cls)          # 不走 __init__（缺服务器数据）
            # 身份字段双保险（object.__setattr__ 兼容 frozen dataclass）
            object.__setattr__(ghost, "name", self._key)
            object.__setattr__(ghost, "no", self._key)
            object.__setattr__(self, "_ghost", ghost)
        return getattr(self._ghost, attr)

    def _ghost_class(self) -> type:
        m = self._manager
        return getattr(type(m), "_entity_class", None) or type(m).get.__globals__.get(
            type(m).__name__.replace("Manager", ""), object
        )

    def _materialize(self) -> Any:
        """冲刷缓冲并从服务器取回真实对象（每个 LazyRef 只执行一次）"""
        if self._real is None:
            with self._manager._no_lazy():
                real = self._manager.get(self._key)
            if real is None:
                raise RuntimeError(
                    f"batch 延迟对象物化失败：{type(self._manager).__name__} 中不存在 {self._key!r}"
                )
            object.__setattr__(self, "_real", real)
        return self._real

    def __getattr__(self, attr: str) -> Any:
        # 方法 → 幽灵实例（零查询，链式调用直接排队）
        cls = getattr(type(self._manager), "_entity_class", None)
        if cls is not None and callable(getattr(cls, attr, None)):
            return self._ghost_method(attr)
        # 数据字段 → 物化后取真实值
        return getattr(self._materialize(), attr)

    def __repr__(self) -> str:
        if self._real is not None:
            return repr(self._real)
        return f"LazyRef({type(self._manager).__name__}, {self._key!r})"


class BasicManager:
    """所有 manager 的基类（batch 延迟对象 + 自动编号守卫）

    子类可声明（用于 LazyRef 的链式调用优化，方法访问零查询直通排队）：
    - _entity_class: 该 manager 管理的数据类（如 ElementGroup）
    - _entity_key_attr: 身份字段名（"name" 或 "no"，默认 "name"）
    """

    _entity_class: type | None = None
    _entity_key_attr: str = "name"
    _no_lazy_flag: bool = False

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # 自动包装子类定义的 _next_no：batch 模式下直接报错（自动编号需要
        # 拉全量查询，会打断批量；批内请显式传编号）。子类无需任何配合代码。
        orig = cls.__dict__.get("_next_no")
        if orig is not None and not getattr(orig, "_batch_guarded", False):
            @functools.wraps(orig)
            def _next_no(self, *args, **kw):
                if batch_state.active:
                    raise RuntimeError(
                        "batch 模式下不支持自动编号（查询最大编号会打断批量）："
                        "请显式传入编号，或退出 batch 后再使用自动编号"
                    )
                return orig(self, *args, **kw)

            _next_no._batch_guarded = True
            cls._next_no = _next_no

    # ── 原有骨架保留（兼容旧引用） ─────────────

    def create(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def all(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def clear(self, *args, **kwargs):
        pass

    # ── 子类工具方法 ──────────────────────────

    def _batch_lazy(self, keys: list) -> Any:
        """batch 模式下为 get() 构造延迟对象

        Args:
            keys: 已归一化的主键列表（调用方完成类型检查与归一化后传入）

        Returns:
            单个 LazyRef（keys 长度为 1）或 LazyRef 列表；
            非 batch 模式（或物化过程中）返回 None，调用方走原有查询逻辑
        """
        if not batch_state.active or self._no_lazy_flag or not keys:
            return None
        refs = [LazyRef(self, k) for k in keys]
        return refs[0] if len(refs) == 1 else refs

    @contextmanager
    def _no_lazy(self):
        """临时关闭延迟语义（LazyRef 物化时回查服务器用）"""
        self._no_lazy_flag = True
        try:
            yield
        finally:
            self._no_lazy_flag = False
