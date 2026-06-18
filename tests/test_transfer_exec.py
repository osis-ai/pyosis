"""从 .out 生成 pyosis 调用并逐条执行（可选检查 transfer 路由覆盖率）。

直接运行本文件或在代码中调用 run_transfer_exec()，不依赖命令行参数。
是否检查覆盖率：改 CHECK_COVERAGE，或调用时传 check_coverage=...
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from pyosis.core.engine import OSISEngine
from pyosis.transfer import parse_text
from pyosis.transfer.generator import generate_lines
from pyosis.transfer.parser import ParsedCommand

OUT_FILE = Path(os.environ.get("PYOSIS_TRANSFER_OUT", r"D:\temp\Temp1\_pyosis_sync.out"))
DEFAULT_GENERATED = Path(__file__).resolve().parent / "output" / "generated_from_out.py"
DEFAULT_REPORT = Path(__file__).resolve().parent / "output" / "exec_report.txt"
DEFAULT_EXPORT_NAME = "_pyosis_sync.out"

# 是否检查路由覆盖率
CHECK_COVERAGE = True

@dataclass
class CoverageStats:
    total: int
    mapped: int
    fallback: int
    by_name: dict[str, tuple[int, int, int]]

    @property
    def rate(self) -> float:
        return self.mapped / self.total if self.total else 0.0


@dataclass
class ExecResult:
    index: int
    line: str
    ok: bool
    error: str


def read_out_file(path: Path) -> str:
    for encoding in ("gbk", "utf-8", "gb2312", "gb18030", "latin-1"):
        try:
            text = path.read_text(encoding=encoding)
            print(f"使用编码: {encoding}")
            return text
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"无法解码 .out 文件: {path}")

# 计算覆盖率
def compute_coverage(cmds: list[ParsedCommand]) -> CoverageStats:
    if not cmds:
        return CoverageStats(0, 0, 0, {})

    lines = generate_lines(cmds)
    name_total: Counter[str] = Counter()
    name_mapped: Counter[str] = Counter()
    name_fallback: Counter[str] = Counter()

    for cmd, line in zip(cmds, lines):
        name_total[cmd.name] += 1
        if line.startswith("engine.run("):
            name_fallback[cmd.name] += 1
        else:
            name_mapped[cmd.name] += 1
    # 按命令名统计覆盖率
    by_name = {
        name: (name_total[name], name_mapped[name], name_fallback[name])
        for name in sorted(name_total)
    }
    total = len(cmds)
    # 计算fallback数量
    fallback = sum(name_fallback.values())
    return CoverageStats(total, total - fallback, fallback, by_name)


def print_coverage_table(stats: CoverageStats, title: str) -> None:
    print(f"\n{'=' * 60}")
    print(title)
    print(f"覆盖率: {stats.mapped}/{stats.total} = {stats.rate:.1%}")
    print(f"{'=' * 60}")

    if not stats.by_name:
        print("(无命令)")
        return

    width = max(len("命令名"), max(len(n) for n in stats.by_name))
    header = f"{'命令名':<{width}}  {'总数':>6}  {'已映射':>6}  {'fallback':>8}  {'覆盖率':>6}"
    print(header)
    print("-" * len(header))

    for name, (total, mapped, fb) in stats.by_name.items():
        rate = mapped / total if total else 0.0
        print(f"{name:<{width}}  {total:>6}  {mapped:>6}  {fb:>8}  {rate:>5.1%}")


def print_fallback_details(cmds: list[ParsedCommand]) -> None:
    lines = generate_lines(cmds)
    for cmd, line in zip(cmds, lines):
        if line.startswith("engine.run("):
            print(f"  {cmd.source}")
            print(f"    → {line}")


def run_coverage(out_file: Path, parsed: list[ParsedCommand]) -> CoverageStats:
    """打印解析摘要，并对命令统计路由覆盖率。"""
    buckets: dict[str, list[ParsedCommand]] = {}
    for cmd in parsed:
        if cmd.kind in ("matrix_dim", "matrix_assign"):
            kind = cmd.kind
        else:
            kind = "normal"

        buckets.setdefault(kind, []).append(cmd)

    normal_cmds = buckets.get("normal", [])

    print(f"文件: {out_file}")
    print(f"解析总行数: {len(parsed)}")
    print(f"  矩阵赋值: {len(buckets.get('matrix_assign', []))}（合并为 engine.matrix）")
    print(f"  *dim 定义: {len(buckets.get('matrix_dim', []))}")
    print(f"  普通命令: {len(normal_cmds)}")
    print(f"  生成代码行数: {len(generate_lines(parsed))}")

    stats = compute_coverage(normal_cmds)
    print_coverage_table(stats, "路由覆盖率（按命令名，普通命令）")

    if stats.fallback:
        print(f"\n── fallback 明细（共 {stats.fallback} 条）──")
        print_fallback_details(normal_cmds)

    return stats


def resolve_out_file(
    engine: OSISEngine,
    out_file: Path,
    force_export: bool = False,
) -> Path:
    """解析 .out 路径；文件不存在时从当前 OSIS 项目 apdl 导出。"""
    if out_file.is_file() and not force_export:
        return out_file

    proj_dir = engine.project.get_directory()
    if not proj_dir:
        raise RuntimeError(
            f"找不到 .out 文件: {out_file}\n"
            "且无法获取 OSIS 项目目录。请先打开 OSIS 并加载项目，"
            "或用 --out-file 指定已存在的 .out 路径。"
        )

    if not out_file.is_file() and out_file == OUT_FILE:
        export_path = Path(proj_dir) / DEFAULT_EXPORT_NAME
    else:
        export_path = out_file

    if force_export or not export_path.is_file() or export_path.stat().st_size == 0:
        export_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"执行 export_apdl → {export_path}")
        engine.export_apdl(str(export_path))

    if not export_path.is_file() or export_path.stat().st_size == 0:
        raise FileNotFoundError(f"导出失败或未生成有效 .out 文件: {export_path}")

    return export_path


def build_script_body(lines: list[str]) -> str:
    header = (
        '"""由 test_transfer_exec 从 .out 自动生成，请勿手工编辑。"""\n'
        "from pyosis.core.engine import OSISEngine\n\n"
        "engine = OSISEngine()\n\n"
    )
    return header + "\n".join(lines) + "\n"

# 执行代码行
def execute_lines(engine: OSISEngine, lines: list[str]) -> list[ExecResult]:
    namespace = {"engine": engine}
    results: list[ExecResult] = []

    for i, line in enumerate(lines, start=1):
        try:
            exec(line, namespace)
            results.append(ExecResult(i, line, True, ""))
            print(f"[OK] {i}: {line}")
        except Exception as exc:
            msg = str(exc)
            results.append(ExecResult(i, line, False, msg))
            print(f"[FAIL] {i}: {line}")
            print(f"       {msg}")

    return results

# 写入报告
def write_report(path: Path, results: list[ExecResult], out_file: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok_count = sum(1 for r in results if r.ok)
    lines = [
        f"out_file: {out_file}",
        f"total: {len(results)}",
        f"ok: {ok_count}",
        f"fail: {len(results) - ok_count}",
        "",
    ]
    for r in results:
        status = "OK" if r.ok else "FAIL"
        lines.append(f"{status}\t#{r.index}\t{r.line}")
        if not r.ok:
            lines.append(f"\terror: {r.error}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 .out 检查 transfer 覆盖率、生成并执行 pyosis 代码",
    )
    parser.add_argument("--out-file", type=Path, default=OUT_FILE)
    parser.add_argument(
        "--generated",
        type=Path,
        default=Path(os.environ.get("PYOSIS_TRANSFER_GENERATED", str(DEFAULT_GENERATED))),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(os.environ.get("PYOSIS_TRANSFER_REPORT", str(DEFAULT_REPORT))),
    )
    parser.add_argument("--save-only", action="store_true")
    parser.add_argument(
        "--force-export",
        action="store_true",
        help="强制 export_apdl 重新导出 .out（即使文件已存在）",
    )
    return parser.parse_args()


def run_transfer_exec(
    out_file: Path | None = None,
    generated: Path | None = None,
    report: Path | None = None,
    check_coverage: bool = CHECK_COVERAGE,
    save_only: bool = False,
    force_export: bool = False,
    engine: OSISEngine | None = None,
) -> int:
    """从 .out 生成并执行 transfer 代码。

    Args:
        out_file: .out 路径，默认 OUT_FILE
        generated: 生成脚本路径
        report: 执行报告路径
        check_coverage: 是否打印路由覆盖率，默认 CHECK_COVERAGE
        save_only: 只生成脚本，不执行
        force_export: 强制 export_apdl 重新导出
        engine: 可传入已有 OSISEngine，否则自动创建

    Returns:
        0 成功，1 失败
    """
    out_file = out_file or OUT_FILE
    generated = generated or DEFAULT_GENERATED
    report = report or DEFAULT_REPORT
    if engine is None:
        engine = OSISEngine()

    try:
        # 从 .out 文件中解析命令
        resolved = resolve_out_file(
            engine,
            out_file,
            force_export=force_export,
        )
    except (RuntimeError, FileNotFoundError) as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"使用 .out: {resolved}")
    # 解析命令
    parsed = parse_text(read_out_file(resolved))

    if check_coverage:
        run_coverage(resolved, parsed)

    # 生成代码
    code_lines = generate_lines(parsed)

    script_text = build_script_body(code_lines)
    # 生成脚本
    generated.parent.mkdir(parents=True, exist_ok=True)
    generated.write_text(script_text, encoding="utf-8")
    print(f"\n已生成: {generated}")
    print(f"  输入命令: {len(parsed)} 条, 生成代码: {len(code_lines)} 行")

    if save_only:
        print("save_only：跳过执行")
        return 0

    print("engine.clear() ...")
    engine.clear()

    print(f"开始执行 (共 {len(code_lines)} 行) ...")
    results = execute_lines(engine, code_lines)

    # 写入报告
    write_report(report, results, resolved)
    failed = [r for r in results if not r.ok]
    print(f"\n完成: 成功 {len(results) - len(failed)}/{len(results)}, 失败 {len(failed)}")
    print(f"报告: {report}")

    return 1 if failed else 0


def main() -> int:
    """命令行入口（可选）；覆盖率由 CHECK_COVERAGE / run_transfer_exec 参数控制。"""
    args = parse_args()
    return run_transfer_exec(
        out_file=args.out_file,
        generated=args.generated,
        report=args.report,
        save_only=args.save_only,
        force_export=args.force_export,
    )


if __name__ == "__main__":
    sys.exit(run_transfer_exec())
