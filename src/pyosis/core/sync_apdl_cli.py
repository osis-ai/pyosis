"""OSIS 界面操作后触发 pyosis APDL 同步的 CLI 入口。
用法:
    python -m pyosis.core.sync_apdl_cli
退出码:
    0 - 成功，或无可同步项目（静默跳过）
    1 - sync_apdl 执行失败
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from .engine import OSISEngine

if TYPE_CHECKING:
    from .apdl_sync import ApdlSyncResult


def _print_result(result: ApdlSyncResult) -> None:

    if result.changed:
        print("命令流有变化，已重新生成并执行 prep")
    else:
        print("命令流未变化，已 export，未重新执行 prep")

    summary = result.summary()
    if summary:
        print(f"摘要: {summary}")



def main() -> int:
    try:
        result = OSISEngine().sync_apdl()
    except Exception as exc:
        print(f"sync_apdl 失败: {exc}", file=sys.stderr)
        return 1

    if result is None:
        print("跳过：未获取到项目路径")
        return 0

    # _print_result(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())