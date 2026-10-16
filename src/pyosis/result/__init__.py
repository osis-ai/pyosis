"""结果读取

唯一的取数路径是 PySolver 的 HTTP 路由（见 routes.py）:有头与无头模式服务的是
同一份路由表，因此结果与界面模式无关。公开入口是 ResultManager。

    >>> from pyosis.core.engine import OSISEngine
    >>> engine.result.node_displacement("自重")
    >>> engine.result.element_force(["自重", "二期"])

尚未有 HTTP 路由的只剩规范验算（check()/check_all()），它仍走 /output 命令流，
隔离在 check.py 里，路由就绪后连同该模块一并删除。
"""

from .manager import ResultManager, result_manager

__all__ = ["ResultManager", "result_manager"]
