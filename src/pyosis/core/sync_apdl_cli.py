"""OSIS 界面操作后触发 pyosis APDL 同步的 CLI 入口。

仅负责触发 perform_apdl_sync；prep 模块的执行不在本模块职责范围内。

用法:
    python -m pyosis.core.sync_apdl_cli
退出码:
    0 - 成功，或无可同步项目（静默跳过）
    1 - sync_apdl 执行失败
"""

from __future__ import annotations

import sys

from .apdl_sync import perform_apdl_sync
from .engine import OSISEngine


def main() -> int:
    engine = OSISEngine()
    try:
        result = perform_apdl_sync(engine)
    except Exception as exc:
        print(f"sync_apdl 失败: {exc}", file=sys.stderr)
        return 1

    if result is None:
        print("跳过：未获取到项目路径")
        return 0

    print(result.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())