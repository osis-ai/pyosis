#!/usr/bin/env python3
"""从 OSIS 命令流文件构建 Python 建模项目骨架

用法:
    python build.py [command_file]
    
示例:
    python build.py              # 自动从当前 OSIS 项目导出命令流并生成骨架
    python build.py C:/Temp/OSIS.out  # 从指定的 .out 文件生成骨架

说明:
    生成骨架文件，函数体为 pass，原始命令流作为注释放在函数内。
    开发者可根据注释中的命令流手动转换为 pyosis API 调用。
"""

import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from pyosis.core.engine import OSISEngine

# 模块映射
MODULE_FILES = {
    "CONTROL": "_1_control.py",
    "PROPERTY": "_2_property.py",
    "MATERIAL": "_3_material.py",
    "SECTION": "_4_section.py",
    "NODE": "_5_node.py",
    "ELEMENT": "_6_element.py",
    "BOUNDARY": "_7_boundary.py",
    "LOADCASE": "_8_loadcase.py",
    "ANALYSIS": "_9_analysis.py",
    "STAGE": "_10_stage.py",
}

MODULE_NAMES = {
    "CONTROL": "全局控制参数",
    "PROPERTY": "几何属性",
    "MATERIAL": "材料",
    "SECTION": "截面",
    "NODE": "节点",
    "ELEMENT": "单元",
    "BOUNDARY": "边界条件",
    "LOADCASE": "荷载工况",
    "ANALYSIS": "分析设置",
    "STAGE": "施工阶段",
}


def parse_command_file(file_path: str) -> Dict[str, List[str]]:
    """解析命令流文件，按模块分割"""
    file_path = Path(file_path)
    
    content = None
    for encoding in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
        try:
            content = file_path.read_text(encoding=encoding)
            print(f"使用编码: {encoding}")
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise ValueError(f"无法读取文件: {file_path}")
    
    lines = content.splitlines()
    module_pattern = re.compile(r"//-+\s*(\w+)\s*-*")
    
    modules: Dict[str, List[str]] = {}
    current_module = None
    
    for line in lines:
        stripped = line.strip()
        match = module_pattern.match(stripped)
        if match:
            module_name = match.group(1).upper()
            if module_name in MODULE_FILES:
                current_module = module_name
                modules[current_module] = []
            continue
        
        if stripped.startswith("//") or not stripped:
            continue
            
        if current_module:
            modules[current_module].append(stripped.rstrip(";"))
    
    return modules


def generate_module(module_name: str, commands: List[str]) -> str:
    """生成模块 Python 文件（骨架版）
    
    函数体为 pass，原始命令流作为注释放在函数内
    """
    title = MODULE_NAMES.get(module_name, module_name)
    func_name = module_name.lower()
    
    # 根据模块确定函数签名
    signatures = {
        "CONTROL": ("def setup_control(engine: OSISEngine) -> None:", "    return\n"),
        "PROPERTY": ("def build_property(engine: OSISEngine) -> list[str]:", "    return []\n"),
        "MATERIAL": ("def build_materials(engine: OSISEngine) -> list[int]:", "    return []\n"),
        "SECTION": ("def build_sections(engine: OSISEngine) -> list[int]:", "    return []\n"),
        "NODE": ("def build_nodes(engine: OSISEngine) -> list[int]:", "    return []\n"),
        "ELEMENT": ("def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:", "    return [], []\n"),
        "BOUNDARY": ("def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:", "    return [], []\n"),
        "LOADCASE": ("def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:", "    return []\n"),
        "ANALYSIS": ("def build_live_analysis(engine: OSISEngine, elem_group_names) -> list[str]:", "    return []\n"),
        "STAGE": ("def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:", ""),
    }
    
    signature, return_type = signatures.get(module_name, (f"def build_{func_name}(engine: OSISEngine):", ""))
    
    lines = [
        f'"""{title}"""',
        "",
        "from pyosis.core.engine import OSISEngine",
        "",
        signature,
        f'    """{title}"""',
        "",
        "    # ========== 原始命令流 ==========",
    ]
    
    for cmd in commands:
        lines.append(f"    # {cmd}")
    
    if return_type:
        lines.append(return_type)
    
    lines.extend([
        "",
        'if __name__ == "__main__":',
        "    from ._0_engine import engine",
    ])
    
    # 根据模块生成对应的测试代码（和空心板模板一致）
    test_codes = {
        "CONTROL": "    setup_control(engine)",
        "PROPERTY": "    geo_names = build_property(engine)\n    print(geo_names)\n    print(engine.geometry.all())",
        "MATERIAL": "    mat_nos = build_materials(engine)\n    print(mat_nos)\n    print(engine.material.all())",
        "SECTION": "    sec_nos = build_sections(engine)\n    print(sec_nos)\n    print(engine.section.all())",
        "NODE": "    node_nos = build_nodes(engine)\n    print(node_nos)\n    print(engine.node.all())",
        "ELEMENT": (
            "    mats = engine.material.all()\n"
            "    mat_nos = [m.no for m in mats]\n"
            "    secs = engine.section.all()\n"
            "    sec_nos = [s.no for s in secs]\n"
            "    nodes = engine.node.all()\n"
            "    node_nos = [n.no for n in nodes]\n"
            "    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)\n"
            "    print(elem_nos)\n"
            "    print(elem_group_names)\n"
            "    print(engine.element.all())\n"
            "    print(engine.element.group.all())"
        ),
        "BOUNDARY": (
            "    nodes = engine.node.all()\n"
            "    node_nos = [n.no for n in nodes]\n"
            "    bd_nos, bd_groups = build_boundaries(engine, node_nos)\n"
            "    print(bd_nos)\n"
            "    print(bd_groups)\n"
            "    print(engine.boundary.all())\n"
            "    print(engine.boundary.group.all())"
        ),
        "LOADCASE": (
            "    mats = engine.material.all()\n"
            "    mat_nos = [m.no for m in mats]\n"
            "    elems = engine.element.all()\n"
            "    elem_nos = [e.no for e in elems]\n"
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    geos = engine.geometry.all()\n"
            "    geo_names = [s.name for s in geos]\n"
            "    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)\n"
            "    print(lc_names)\n"
            "    print(engine.load.all())"
        ),
        "ANALYSIS": (
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    live_names = build_live_analysis(engine, elem_group_names)\n"
            "    print(live_names)"
        ),
        "STAGE": (
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    bd_groups = engine.boundary.group.all()\n"
            "    bd_group_names = [bg.name for bg in bd_groups]\n"
            "    lcs = engine.load.all()\n"
            "    lc_names = [lc.name for lc in lcs]\n"
            "    live_names = []\n"
            "    settle_names = []\n"
            "    build_stages(engine, elem_group_names, bd_group_names, lc_names, settle_names, live_names)"
        ),
    }
    
    lines.append(test_codes.get(module_name, f"    build_{func_name}(engine)"))
    
    return "\n".join(lines)


def export_command_file() -> Optional[str]:
    """从当前 OSIS 项目导出命令流文件
    
    Returns:
        导出的 .out 文件路径，如果失败则返回 None
    """
    print("未提供命令流文件，尝试从当前 OSIS 项目导出...")
    
    try:
        engine = OSISEngine()
        
        # 获取项目目录，用于确定导出位置
        project_dir = engine.project.get_directory()
        if not project_dir:
            print("导出失败: 未检测到已打开的 OSIS 项目")
            print("\n可能的原因:")
            print("  1. OSIS 软件未打开")
            print("  2. OSIS 软件未加载项目")
            print("  3. pyosis 与 OSIS 连接异常")
            print("\n建议:")
            print("  - 请确保 OSIS 软件已打开并加载了项目")
            print("  - 或手动提供 .out 文件路径: python build.py <文件路径>")
            return None
        
        export_path = Path(project_dir) / "exported_model.out"
        
        # 导出命令流
        print(f"正在导出命令流到: {export_path}")
        engine.export_apdl(str(export_path))
        
        # 验证文件是否生成
        if export_path.exists() and export_path.stat().st_size > 0:
            print(f"导出成功: {export_path}")
            return str(export_path)
        else:
            print("导出失败: 文件未生成或为空")
            return None
            
    except Exception as e:
        print(f"导出失败: {e}")
        print("\n可能的原因:")
        print("  1. OSIS 软件未打开或未加载项目")
        print("  2. OSIS 软件与 pyosis 连接异常")
        print("  3. 当前项目为空或未保存")
        print("\n建议:")
        print("  - 请确保 OSIS 软件已打开并加载了项目")
        print("  - 或手动提供 .out 文件路径: python build.py <文件路径>")
        return None


def build_project(command_file: Optional[str] = None) -> None:
    """从命令流文件构建 Python 项目骨架
    
    在当前目录自动创建:
    - post/     后处理目录
    - prep/     建模模块目录
    - main.py   主入口文件
    
    Args:
        command_file: 命令流文件路径，如果为 None 则自动从项目导出
    """
    # 如果未提供命令流文件，尝试从项目导出
    if command_file is None:
        command_file = export_command_file()
        if command_file is None:
            print("\n错误: 无法获取命令流文件，构建终止")
            sys.exit(1)
    
    print(f"解析命令流文件: {command_file}")
    modules = parse_command_file(command_file)
    
    # 获取当前目录（build.py 所在目录）
    base_dir = Path(__file__).parent.resolve()
    
    # 创建目录结构
    prep_dir = base_dir / "prep"
    post_dir = base_dir / "post"
    prep_dir.mkdir(exist_ok=True)
    post_dir.mkdir(exist_ok=True)
    
    # 创建 post/__init__.py
    post_init = post_dir / "__init__.py"
    if not post_init.exists():
        post_init.write_text('"""后处理模块"""\n', encoding="utf-8")
        print("创建: post/__init__.py")
    
    # 创建 _0_engine.py
    engine_file = prep_dir / "_0_engine.py"
    if not engine_file.exists():
        engine_file.write_text(
            "from pyosis.core.engine import OSISEngine\n\n"
            "engine = OSISEngine()\n\n"
            "# 自动打开OSIS等操作暂未实现\n"
            "# 目前需要手动打开OSIS并创建项目\n",
            encoding="utf-8"
        )
        print(f"创建: prep/_0_engine.py")
    
    print(f"生成 Python 文件到: {prep_dir}")
    
    for module_name, commands in modules.items():
        if module_name in MODULE_FILES:
            file_name = MODULE_FILES[module_name]
            file_path = prep_dir / file_name
            
            python_code = generate_module(module_name, commands)
            file_path.write_text(python_code, encoding="utf-8")
            
            print(f"  创建: prep/{file_name} ({len(commands)} 条命令)")
    
    # 创建 main.py（在当前目录）
    main_file = base_dir / "main.py"
    if not main_file.exists():
        main_content = '''"""
从命令流构建的桥梁建模项目

使用方式:
    python main.py              # 完整建模（默认清空重建）
    python main.py --increment  # 增量模式：不清空，幂等执行
    
也可以直接执行单个模块:
    python prep/_5_node.py   # 只执行节点创建
    python prep/_6_element.py # 只执行单元创建（会从engine读取已有节点）
"""

import argparse

from prep._0_engine import engine
from prep._1_control import setup_control
from prep._2_property import build_property
from prep._3_material import build_materials
from prep._4_section import build_sections
from prep._5_node import build_nodes
from prep._6_element import build_elements
from prep._7_boundary import build_boundaries
from prep._8_loadcase import build_loadcases
from prep._9_analysis import build_live_analysis
from prep._10_stage import build_stages


def build_model(incremental: bool = False, run_analysis: bool = False):
    """完整的桥梁建模流程
    
    Args:
        incremental: 是否增量模式（不清空），默认 False（清空重建）
        run_analysis: 是否自动运行分析，默认 False（只建模）
    """

    if not incremental:
        print("清空项目...")
        engine.clear()
        engine.clc()

    print("=" * 50)
    print("开始建模" + ("（增量模式）" if incremental else "（清空重建）"))
    print("=" * 50)
    
    # 1. 全局设置（无依赖）
    print("\\n[1/10] 设置全局控制参数...")
    setup_control(engine)
    
    # 2. 几何属性（无依赖）
    print("[2/10] 设置几何属性...")
    geo_names = build_property(engine)
    
    # 3. 材料（无依赖）
    print("[3/10] 创建材料...")
    mat_nos = build_materials(engine)
    
    # 4. 截面（无依赖）
    print("[4/10] 创建截面...")
    sec_nos = build_sections(engine)
    
    # 5. 节点（无依赖）
    print("[5/10] 创建节点...")
    node_nos = build_nodes(engine)
    
    # 6. 单元（依赖节点、截面、材料）
    print("[6/10] 创建单元...")
    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)
    
    # 7. 边界（依赖节点）
    print("[7/10] 创建边界条件...")
    bd_nos, bd_group_names = build_boundaries(engine, node_nos)
    
    # 8. 荷载工况（依赖单元、材料、几何）
    print("[8/10] 创建荷载工况...")
    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)
    
    # 9. 分析设置（依赖单元组）
    print("[9/10] 创建分析设置...")
    live_names = build_live_analysis(engine, elem_group_names)
    
    # 10. 施工阶段（依赖所有组）
    print("[10/10] 创建施工阶段...")
    build_stages(engine, elem_group_names, bd_group_names, lc_names, [], live_names)
    
    print("\\n" + "=" * 50)
    print("建模完成！")
    print("=" * 50)
    
    if run_analysis:
        print("\\n开始运行分析...")
        engine.solve()
        print("分析完成！")
    else:
        print("\\n提示: 调用 engine.solve() 运行分析")
    
    return engine


def main():
    parser = argparse.ArgumentParser(description='桥梁建模')
    parser.add_argument('--increment', action='store_true', 
                        help='增量模式：不清空（默认清空重建）')
    parser.add_argument('--solve', action='store_true',
                        help='建模后自动运行分析')
    
    args = parser.parse_args()
    
    # 执行建模（默认清空重建）
    build_model(incremental=args.increment, run_analysis=args.solve)


if __name__ == "__main__":
    main()
'''
        main_file.write_text(main_content, encoding="utf-8")
        print(f"创建: main.py")
    
    # 创建 post/README.md
    post_readme = post_dir / "README.md"
    if not post_readme.exists():
        post_readme.write_text(
            "# 后处理目录\n\n"
            "此目录用于存放后处理脚本和结果文件。\n\n"
            "例如:\n"
            "- 结果提取脚本\n"
            "- 数据可视化脚本\n"
            "- 报告生成脚本\n",
            encoding="utf-8"
        )
        print("创建: post/README.md")
    
    print(f"\n完成！共生成 {len(modules)} 个模块文件")
    print("项目结构:")
    print(f"  {base_dir.name}/")
    print(f"  ├── build.py")
    print(f"  ├── main.py")
    print(f"  ├── post/")
    print(f"  └── prep/")
    print("\n提示: 请根据函数内注释的命令流，手动转换为 pyosis API 调用")


if __name__ == "__main__":
    command_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if command_file is None:
        print("用法: python build.py [command_file]")
        print("示例:")
        print("  python build.py              # 自动从当前 OSIS 项目导出")
        print("  python build.py C:/Temp/OSIS.out  # 从指定文件生成")
        print("")
    
    build_project(command_file)
