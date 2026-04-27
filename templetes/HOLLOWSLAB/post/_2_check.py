from pathlib import Path

from pyosis.core.engine import OSISEngine


def export_check_results(
    engine: OSISEngine,
    output_dir: str | None = None,
    save_format: str = "csv",
    verbose: bool = True
) -> dict[str, Path]:
    """导出项目下所有验算结果

    自动扫描 OSIS 项目 Check 目录中的 .lcc 文件，
    逐个导出为表格文件（CSV 或 Excel）。

    Args:
        engine: OSISEngine 实例
        output_dir: 输出目录，默认使用项目目录下的 "Check"
        save_format: 保存格式，"csv" 或 "excel"
        verbose: 直接打印所有结果

    Returns:
        字典，键为验算名称，值为导出的文件路径
    """
    # 获取项目目录
    project_dir = engine.project.get_directory()
    if not project_dir:
        raise RuntimeError("无法获取项目目录，请确认 OSIS 已登录并打开项目")

    if output_dir is None:
        output_dir = Path(project_dir) / "Check"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print("开始导出验算结果...")
    results = engine.result.check_all()

    exported: dict[str, Path] = {}
    for name, df in results.items():
        safe_name = name.replace("/", "_").replace("\\", "_")
        if verbose:
            print(safe_name)
            print(df)

        if save_format.lower() in ["excel", "xlsx"]:
            file_path = output_dir / f"{safe_name}.xlsx"
            df.to_excel(file_path, index=False, engine="openpyxl")
        else:
            file_path = output_dir / f"{safe_name}.csv"
            df.to_csv(file_path, index=False, encoding="utf-8-sig")

        exported[name] = file_path
        print(f"  已导出: {name} ({len(df)} 行)")

    print(f"\n共导出 {len(exported)} 个验算结果，保存至: {output_dir}")
    return exported


if __name__ == "__main__":
    from ._0_engine import engine

    # 导出所有验算结果为 CSV
    export_check_results(engine, save_format="csv")

    # 如需导出为 Excel，取消下面一行的注释：
    # export_check_results(engine, save_format="excel")
