"""命令批量执行（batch）核心

设计要点：
- 任何经 REGISTRY 注册的命令函数在 batch 激活时都只进本地缓冲，退出 with 时
  拼成一条命令流、一次 /OSIS_Run 发送（服务端 SplitOsisCommands + 单次 Execution）
- 查询类调用（osis_client 的所有接口，含用户直接调用的 OSIS_Run）会先自动冲刷
  缓冲，保证查询永远看到"已执行完毕"的状态
- manager 通过影子工厂表（BasicManager._shadow_factories）在命令入缓冲时登记
  影子对象，使 create 尾部的回查 get() 命中本地影子而不触发冲刷
- 错误策略：冲刷失败抛 BatchError（附 OSIS 原文）；不重试、不退避、默认不二分
  （isolate=True 可选二分定位坏命令，仅供调试，无 sleep）

用法:
    >>> import pyosis
    >>> with pyosis.batch():
    ...     for i in range(1000):
    ...         engine.element.create_beam3d(None, i, i + 1, 1, 1, 1)
    ...  # 退出 with 时 1000 条命令一次发送
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Callable, Iterator

from .client import osis_client


class BatchError(RuntimeError):
    """批量冲刷失败

    Attributes:
        error: OSIS 返回的错误原文
        failed: 定位到的失败命令列表（isolate 模式下逐条列出，否则为空）
        executed: 冲刷前缓冲中的命令总数
    """

    def __init__(self, error: str, failed: list[str] | None = None, executed: int = 0):
        self.error = error
        self.failed = failed or []
        self.executed = executed
        msg = f"批量冲刷失败（共 {executed} 条命令）: {error}"
        if self.failed:
            lines = "\n".join(f"  [FAIL] {c}" for c in self.failed)
            msg += f"\n失败命令（{len(self.failed)} 条）:\n{lines}"
        super().__init__(msg)


class _BatchState:
    """batch 全局状态（模块级单例 batch_state）"""

    def __init__(self) -> None:
        self.buffer: list[str] = []       # 已入队的命令流（每条自带分号终止符）
        self.depth: int = 0               # batch 嵌套深度，>0 表示激活
        self.flushing: bool = False       # 冲刷进行中（防止拦截器递归冲刷）

    @property
    def active(self) -> bool:
        """batch 模式是否激活"""
        return self.depth > 0


batch_state = _BatchState()


# ──────────────────────────────────────────────
# 冲刷
# ──────────────────────────────────────────────

def flush(
    isolate: bool = False,
    timeout: float | None = None,
    max_size: int | None = None,
) -> int:
    '''冲刷缓冲：把已入队的全部命令拼成一条流，一次 /OSIS_Run 发送

    一般无需手动调用——退出 batch 上下文或任何查询调用都会自动冲刷。

    Args:
        isolate (bool): 冲刷失败时是否二分定位失败命令（仅供调试，
            无重试无退避；二分重放假设失败命令本身无副作用残留）
        timeout (float): HTTP 超时秒数，默认 600（大批量 Execution 耗时较长）
        max_size (int): 单次请求最大命令条数，默认不限（一次全发）。
            超大模型可设 5000 之类的安全阀，将分多次请求发送

    Returns:
        int: 本次冲刷发送的命令条数

    Raises:
        BatchError: OSIS 返回失败时抛出（isolate=True 时附失败命令清单）
    '''
    if batch_state.flushing or not batch_state.buffer:
        return 0
    cmds = batch_state.buffer[:]
    batch_state.buffer.clear()
    batch_state.flushing = True
    try:
        chunks = (
            [cmds[i:i + max_size] for i in range(0, len(cmds), max_size)]
            if max_size else [cmds]
        )
        failed: list[str] = []
        for chunk in chunks:
            failed += _send(chunk, isolate=isolate, timeout=timeout)
        if failed:
            raise BatchError(
                failed_error(failed),
                failed=[c.split("||", 1)[1] for c in failed],
                executed=len(cmds),
            )
        return len(cmds)
    finally:
        batch_state.flushing = False


def failed_error(failed: list[str]) -> str:
    """汇总失败命令对应的 OSIS 错误信息（_send 记录在命令前缀）"""
    errs = {c.split("||", 1)[0] for c in failed if "||" in c}
    return "; ".join(errs) or "未知错误"


def _send(cmds: list[str], isolate: bool = False, timeout: float | None = None) -> list[str]:
    """发送一组命令，返回失败命令列表（"错误||命令" 格式；成功返回空表）"""
    stream = "".join(cmds)
    resp = osis_client(
        "OSIS_Run",
        {"strCmd": stream, "mode": "exec"},
        timeout=timeout if timeout is not None else 600,
    )
    if resp.get("success"):
        return []
    err = resp.get("error", "")
    if not isolate or len(cmds) == 1:
        return [f"{err}||{cmds[0]}"] if len(cmds) == 1 else [f"{err}||(共{len(cmds)}条)"]
    # 二分定位：无重试无退避，把坏命令找出来
    mid = len(cmds) // 2
    return _send(cmds[:mid], True, timeout) + _send(cmds[mid:], True, timeout)


# ──────────────────────────────────────────────
# batch 上下文
# ──────────────────────────────────────────────

@contextmanager
def batch() -> Iterator[None]:
    '''batch 模式上下文：内部所有命令只进缓冲，退出时一次性发送

    >>> with pyosis.batch():
    ...     engine.node.create(None, 0, 0, 0)
    ...     engine.node.create(None, 1, 0, 0)
    ...     element_manager.create_beam3d(None, 1, 2, 1, 1, 1)
    ... # 退出时 3 条命令拼成一条流，一次 HTTP 请求

    规则:
        * 正常退出：自动 flush()，缓冲内全部命令一次执行
        * 异常退出：丢弃本次进入后新增的缓冲命令并抛出原异常
          （半截模型不落盘；需要保留请自行 try/finally + flush()）
        * 支持嵌套：内层退出不冲刷，最外层退出才统一冲刷
        * 期间任何查询（get/all/solve/用户直接 osis_run 等）会先自动
          冲刷缓冲再执行，保证查询结果实时
    '''
    batch_state.depth += 1
    added = len(batch_state.buffer)
    try:
        yield
    except BaseException:
        del batch_state.buffer[added:]
        batch_state.depth -= 1
        raise
    else:
        batch_state.depth -= 1
        if batch_state.depth == 0:
            flush()
