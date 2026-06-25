"""通过 APDL 导出实现 OSIS → pyosis 主动同步。

流程:
    1. export .out
    2. 对比 MD5 与 {项目}/py/.apdl_sync.json
    3. 未变化 → 跳过 parse / 写 prep
    4. 有变化 → parse → 写 prep → 存本次 hash

用法:
    result = engine.sync_apdl()
    if result and result.changed:
        print(result.summary())
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import OSISEngine

SYNC_STATE_FILE = ".apdl_sync.json"

# 忽略 TIME: 行，避免时间戳导致 MD5 每次不同
_TIME_LINE_PATTERN = re.compile(
    r"^//-+ TIME:.*//\s*$",
    re.MULTILINE | re.IGNORECASE,
)

@dataclass
class ApdlSyncResult:
    """APDL 同步结果。"""

    changed: bool = False

    def summary(self) -> str:
        return "命令流已变化，已写 prep" if self.changed else "命令流未变化"


@dataclass
class ApdlSessionStore:
    """记录最近一次同步的 .out 路径与 hash（供调试/展示，不由 ApdlSyncResult 重复携带）。"""

    last_path: str = ""
    last_hash: str = ""

    def update_file(self, path: str, file_hash: str) -> None:
        self.last_path = path
        self.last_hash = file_hash


# 读取 .out 文件内容
def _read_out_text(path: Path) -> str:
    for encoding in ("gbk", "utf-8", "gb2312", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"无法解码 .out 文件: {path}")


# 忽略 TIME: 行，避免时间戳导致 MD5 每次不同
def _normalize_out_for_hash(text: str) -> str:
    return _TIME_LINE_PATTERN.sub("", text)


# 计算 .out 文件内容的 MD5
def _text_hash(text: str) -> str:
    return hashlib.md5(_normalize_out_for_hash(text).encode("utf-8")).hexdigest()


# 获取同步状态文件路径
def _sync_state_path(prep_dir: Path) -> Path:
    return prep_dir.parent / SYNC_STATE_FILE


# 加载持久化存储的 hash
def _load_persisted_hash(state_path: Path, out_path: Path) -> str:
    if not state_path.is_file():
        return ""
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        saved_out = Path(data.get("out_path", ""))
        if saved_out.resolve() == out_path.resolve():
            return str(data.get("file_hash", ""))
    except (OSError, json.JSONDecodeError, TypeError):
        pass
    return ""


# 保存持久化存储的 hash
def _save_persisted_hash(state_path: Path, out_path: Path, file_hash: str) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {"out_path": str(out_path), "file_hash": file_hash},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


# 执行 APDL 同步
def perform_apdl_sync(
    engine: "OSISEngine",
    path: str | None = None,
    *,
    force_export: bool = True,
) -> ApdlSyncResult | None:
    """执行 APDL 同步：export → 比 hash → 有变化则写 prep（不执行 prep）。

    无项目路径时返回 None。
    """
    from ..transfer import parse_text
    from ..transfer.sync_exec import (
        get_project_dir_optional,
        resolve_out_file,
        resolve_project_paths,
        write_prep_outputs,
    )

    if get_project_dir_optional(engine) is None:
        return None

    session: ApdlSessionStore = engine._apdl_session

    default_out, prep_dir = resolve_project_paths(engine)
    out_path = Path(path) if path is not None else default_out
    out_path = resolve_out_file(engine, out_path, force_export=force_export)

    text = _read_out_text(out_path)
    file_hash = _text_hash(text)

    state_path = _sync_state_path(prep_dir)
    last_hash = _load_persisted_hash(state_path, out_path)

    session.update_file(str(out_path), file_hash)

    if file_hash == last_hash:
        return ApdlSyncResult(changed=False)

    parsed = parse_text(text)
    write_prep_outputs(parsed, prep_dir)

    # 未执行 prep，OSIS 未变
    _save_persisted_hash(state_path, out_path, file_hash)

    return ApdlSyncResult(changed=True)