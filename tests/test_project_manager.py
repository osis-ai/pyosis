"""
测试 ProjectManager（create / open / save / save_as / get_directory）

前置条件: OSIS 已打开。

使用方式:
    python tests/test_project_manager.py

说明:
    create / open / save_as 传入完整 .sis 路径；
    create 只创建项目目录，不会生成 .sis 文件；
    save / save_as 后才会在磁盘上生成 .sis 工程文件；
    close 关闭 OSIS 软件（测试最后一步，执行后需重新打开 OSIS）。
"""

from __future__ import annotations

import os
import time

from pyosis.core.engine import OSISEngine


def _expect_eq(actual, expected, label: str) -> None:
    if actual != expected:
        raise ValueError(f"{label} 不符: 期望 {expected!r}, 实际 {actual!r}")


def _expect_true(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def _norm_path(path: str) -> str:
    """规范化路径，去掉末尾分隔符便于比较。"""
    return os.path.normcase(os.path.normpath(path.rstrip("\\/")))


def _expected_project_dir(filepath: str) -> str:
    """由 .sis 完整路径推导项目目录（去掉扩展名）。"""
    return os.path.splitext(filepath)[0]


def _sibling_names(filepath: str) -> list[str]:
    parent = os.path.dirname(filepath) or "."
    if not os.path.isdir(parent):
        return []
    return sorted(os.listdir(parent))


def _wait_isfile(filepath: str, timeout: float = 3.0, interval: float = 0.2) -> bool:
    """等待文件出现（兼顾落盘延迟）。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if os.path.isfile(filepath):
            return True
        time.sleep(interval)
    return os.path.isfile(filepath)


def _expect_sis_file(filepath: str, label: str) -> None:
    """断言工程文件为 .sis，失败时打印同级目录内容。"""
    _expect_true(filepath.lower().endswith(".sis"), f"{label} 路径应为 .sis: {filepath}")
    if _wait_isfile(filepath):
        return
    siblings = _sibling_names(filepath)
    raise ValueError(
        f"{label} 后应存在文件: {filepath}\n"
        f"  同级目录内容: {siblings}"
    )


def test_project(engine: OSISEngine, filepath: str) -> None:
    """依次验证 create / get_directory / save / save_as / open。

    Args:
        filepath: 项目文件完整路径，例如 "D:\Temp\demo.sis"
    """
    project = engine.project
    expected_dir = _expected_project_dir(filepath)
    path2 = os.path.splitext(filepath)[0] + "_v2.sis"

    # ── create：只建目录，不生成 .sis ──
    project.create(type=101, filepath=filepath)
    print(f"  create -> {filepath}")
    _expect_true(
        not os.path.isfile(filepath),
        f"create 后不应生成 .sis 文件: {filepath}",
    )

    # ── get_directory ──
    directory = project.get_directory()
    print(f"  get_directory -> {directory}")
    _expect_true(isinstance(directory, str) and len(directory) > 0, "get_directory 应返回非空路径")
    _expect_eq(_norm_path(directory), _norm_path(expected_dir), "项目目录")
    _expect_true(os.path.isdir(expected_dir), f"项目目录应存在: {expected_dir}")

    # ── save：路径为空时使用当前项目路径，此时才生成 .sis ──
    project.save()
    print("  save() -> 当前项目路径")
    _expect_sis_file(filepath, "save")

    # ── save：显式传入路径 ──
    project.save(filepath)
    print(f"  save({filepath})")
    _expect_sis_file(filepath, "save(显式路径)")

    # ── save_as ──
    project.save_as(path2)
    print(f"  save_as -> {path2}")
    _expect_sis_file(path2, "save_as")

    # ── open ──
    project.open(path2)
    print(f"  open -> {path2}")
    directory2 = project.get_directory()
    print(f"  get_directory -> {directory2}")
    _expect_eq(
        _norm_path(directory2),
        _norm_path(_expected_project_dir(path2)),
        "另存为后打开的项目目录",
    )

    # ── close：关闭软件 ──
    project.close()
    print("  close ok（OSIS 已退出）")


if __name__ == "__main__":
    engine = OSISEngine()
    filepath = r"D:\Temp\demo5555555.sis"
    print(f"项目文件: {filepath}")
    print("开始测试 ProjectManager ...")
    test_project(engine, filepath)
    print("全部通过")
