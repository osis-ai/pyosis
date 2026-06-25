# from pyosis.core.engine import OSISEngine
#
# def sync_from_osis() -> None:
#     engine = OSISEngine()
#     result = engine.sync_apdl()
#
#     if result is None:
#         print("跳过：未获取到项目路径")
#         return
#
#     session = engine._apdl_session
#     print(f".out: {session.last_path}")
#     print(f"MD5: {session.last_hash}")
#     print(result.summary())
#
# if __name__ == "__main__":
#     sync_from_osis()

"""执行 prep 模块，测试生成的 Python 能否在 OSIS 里跑通。"""
from __future__ import annotations

import sys

from pyosis.core.engine import OSISEngine
from pyosis.transfer.sync_exec import (
    execute_prep_modules,
    get_project_dir_optional,
    resolve_project_paths,
)


def run_prep_test(engine: OSISEngine | None = None) -> int:
    if engine is None:
        engine = OSISEngine()

    if get_project_dir_optional(engine) is None:
        print("跳过：未获取到项目路径")
        return 0

    _, prep_dir = resolve_project_paths(engine)
    print(f"prep 目录: {prep_dir}")

    # 传入 engine，与当前 OSIS 会话一致（推荐）
    results = execute_prep_modules(prep_dir, engine=engine)

    failed = [r for r in results if not r.ok]
    print(f"\n完成: 成功 {len(results) - len(failed)}/{len(results)}, 失败 {len(failed)}")
    for r in failed:
        print(f"  [FAIL] {r.line}: {r.error}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run_prep_test())