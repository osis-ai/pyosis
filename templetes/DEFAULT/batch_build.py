#!/usr/bin/env python3
r"""批量将 .sml 模型文件转换为 Python 项目

用法:
    python batch_build.py

说明:
    自动遍历 C:\Users\99340\Desktop\工程项目\模型 下的所有 .sml 文件，
    逐个导入 OSIS，导出命令流，然后使用 build.py 生成 Python 项目。
"""

import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

# 添加 build.py 所在目录到路径
BUILD_PY_DIR = Path(r"C:\Users\99340\.config\opencode\skills\project-builder\assets\templates\DEFAULT")
sys.path.insert(0, str(BUILD_PY_DIR))

from build import build_project

# 源目录和目标目录
SOURCE_DIR = Path(r"C:\Users\99340\Desktop\工程项目\模型")
OUTPUT_BASE_DIR = Path(r"C:\Users\99340\Desktop\工程项目\python_projects")


def get_bridge_type(rel_path: Path) -> str:
    """从相对路径推断桥梁类型"""
    parts = rel_path.parts
    if not parts:
        return "未分类"
    
    # 第一层目录通常是桥梁体系分类
    type_map = {
        "现浇等截面体系": "现浇等截面连续梁/刚构桥",
        "变截面大跨体系": "变截面大跨连续梁/刚构桥",
        "预制简支体系": "预制简支梁桥",
        "钢混组合体系": "钢-混凝土组合梁桥",
        "纯钢结构体系": "纯钢桥",
        "拱桥体系": "拱桥",
        "缆索体系": "斜拉桥/悬索桥",
        "专题模型": "专题研究模型",
    }
    
    first_dir = parts[0]
    return type_map.get(first_dir, first_dir)


def get_cross_section_type(rel_path: Path) -> str:
    """从相对路径推断截面类型"""
    path_str = str(rel_path).lower()
    
    if "单箱单室" in path_str:
        return "单箱单室截面"
    elif "单箱多室" in path_str:
        # 进一步判断几室
        if "2室" in path_str or "两室" in path_str:
            return "单箱双室截面"
        elif "3室" in path_str or "三室" in path_str:
            return "单箱三室截面"
        elif "4室" in path_str or "四室" in path_str:
            return "单箱四室截面"
        return "单箱多室截面"
    elif "小箱梁" in path_str:
        return "预制小箱梁截面"
    elif "异形截面" in path_str or "人行桥" in path_str:
        return "异形截面"
    elif "钢箱" in path_str or "钢混" in path_str:
        return "钢箱梁截面"
    elif "t梁" in path_str or "t型" in path_str:
        return "T梁截面"
    elif "空心板" in path_str:
        return "空心板截面"
    else:
        return "常规截面"


def get_span_info(filename: str) -> str:
    """从文件名推断跨径信息"""
    import re
    # 匹配跨径模式如 30+40+30, 20+20+20 等
    spans = re.findall(r'(\d+)[\+](\d+)(?:[\+](\d+))?', filename)
    if spans:
        # 取第一组匹配
        span_group = spans[0]
        span_list = [s for s in span_group if s]
        if span_list:
            total = sum(int(s) for s in span_list)
            return f"跨径布置: {'+'.join(span_list)}m (总长{total}m)"
    
    # 匹配单一跨径如 40m
    single_span = re.search(r'(\d+)m', filename)
    if single_span:
        return f"跨径: {single_span.group(1)}m"
    
    return "跨径信息: 详见模型"


def generate_readme(output_dir: Path, sml_path: Path, summary: Dict[str, Any], rel_path: Path) -> None:
    """生成项目 README.md"""
    
    bridge_type = get_bridge_type(rel_path)
    section_type = get_cross_section_type(rel_path)
    span_info = get_span_info(sml_path.stem)
    
    # 从文件名提取更多特征
    filename_features = []
    name_lower = sml_path.stem.lower()
    if "变宽" in name_lower:
        filename_features.append("变宽桥梁")
    if "匝道" in name_lower:
        filename_features.append("互通匝道")
    if "枢纽" in name_lower:
        filename_features.append("枢纽互通")
    if "人行" in name_lower:
        filename_features.append("人行天桥")
    if "分离" in name_lower:
        filename_features.append("分离式路基")
    if "无支座" in name_lower:
        filename_features.append("无支座模拟")
    if "二次渐变" in name_lower or "2次" in name_lower:
        filename_features.append("二次渐变截面")
    
    features_str = "、".join(filename_features) if filename_features else "标准设计"
    
    # 统计信息
    materials = summary.get("materials", 0)
    sections = summary.get("sections", 0)
    nodes = summary.get("nodes", 0)
    elements = summary.get("elements", 0)
    boundaries = summary.get("boundaries", 0)
    load_cases = summary.get("load_cases", 0)
    stages = summary.get("stages", 0)
    geometries = summary.get("geometry", 0)
    live_loads = summary.get("live_loads", 0)
    settlements = summary.get("settlements", 0)
    tendon_props = summary.get("tendon_props", 0)
    tendon_shapes = summary.get("tendon_shapes", 0)
    
    # 复杂度评估
    complexity = "简单"
    if elements > 1000 or stages > 10:
        complexity = "复杂"
    elif elements > 500 or stages > 5:
        complexity = "中等"
    
    # 是否有预应力
    has_prestress = tendon_props > 0 or tendon_shapes > 0
    prestress_str = "有预应力钢束" if has_prestress else "无预应力"
    
    # 是否有施工阶段
    has_stages = stages > 0
    stage_str = f"含{stages}个施工阶段" if has_stages else "无施工阶段模拟"
    
    # 是否有活载
    has_live = live_loads > 0
    live_str = "含移动活载分析" if has_live else "无移动活载"
    
    # 是否有沉降
    has_settlement = settlements > 0
    settlement_str = "含支座沉降分析" if has_settlement else "无沉降分析"
    
    readme_content = f"""# {sml_path.stem}

## 项目画像

### 基本信息
- **桥梁体系**: {bridge_type}
- **截面类型**: {section_type}
- **{span_info}**
- **特征**: {features_str}
- **模型复杂度**: {complexity}

### 模型规模
- **节点数量**: {nodes}
- **单元数量**: {elements}
- **截面数量**: {sections}
- **材料数量**: {materials}
- **边界条件**: {boundaries}

### 分析特征
- **{prestress_str}**
- **{stage_str}**
- **荷载工况**: {load_cases}个
- **{live_str}**
- **{settlement_str}**
- **几何线型**: {geometries}条

### 文件信息
- **原始模型**: `{sml_path.name}`
- **模型路径**: `{rel_path}`
- **生成时间**: 自动生成

### 使用说明

本项目由 `build.py` 从 OSIS `.sml` 模型文件自动生成。

```bash
# 完整建模（清空重建）
python main.py

# 增量模式
python main.py --increment

# 建模并运行分析
python main.py --solve
```

### 项目结构
```
{sml_path.stem}/
├── main.py          # 主入口
├── build.py         # 构建脚本
├── prep/            # 建模模块
│   ├── _0_engine.py
│   ├── _1_control.py
│   ├── _2_property.py
│   ├── _3_material.py
│   ├── _4_section.py
│   ├── _5_node.py
│   ├── _6_element.py
│   ├── _7_boundary.py
│   ├── _8_loadcase.py
│   ├── _9_analysis.py
│   └── _10_stage.py
└── post/            # 后处理目录
```

---
*注意: 生成的代码中标记为 `# TODO` 的部分需要手动检查和完善。*
"""

    readme_path = output_dir / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"  生成: README.md")


def process_sml_file(sml_path: Path, output_base_dir: Path, source_dir: Path) -> bool:
    """处理单个 .sml 文件

    Returns:
        是否成功
    """
    # 计算相对路径，用于保持目录结构
    try:
        rel_path = sml_path.relative_to(source_dir)
    except ValueError:
        rel_path = sml_path.name

    # 创建输出目录
    output_dir = output_base_dir / rel_path.parent / sml_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"处理: {rel_path}")
    print(f"输出: {output_dir}")
    print(f"{'='*60}")

    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix="osis_build_")
    temp_out = Path(temp_dir) / "OSIS.out"

    try:
        # 导入到 OSIS
        print(f"\n[1/4] 导入 .sml 到 OSIS...")
        try:
            from pyosis.core.engine import OSISEngine
            engine = OSISEngine()
            print("  清空项目...")
            engine.clear()
            engine.clc()
            print(f"  导入: {sml_path}")
            engine.import_apdl(str(sml_path))
            print("  导入成功")
        except Exception as e:
            print(f"  导入失败: {e}")
            print("  建议: 请确保 OSIS 软件已打开")
            return False

        # 获取模型统计信息
        print(f"\n[2/4] 获取模型信息...")
        try:
            summary = engine.model_summary()
            print(f"  节点: {summary.get('nodes', 0)}")
            print(f"  单元: {summary.get('elements', 0)}")
            print(f"  材料: {summary.get('materials', 0)}")
            print(f"  截面: {summary.get('sections', 0)}")
            print(f"  荷载: {summary.get('load_cases', 0)}")
            print(f"  阶段: {summary.get('stages', 0)}")
        except Exception as e:
            print(f"  获取统计信息失败: {e}")
            summary = {}

        # 导出 OSIS.out
        print(f"\n[3/4] 导出命令流...")
        try:
            engine.export_apdl(str(temp_out))
            if temp_out.exists() and temp_out.stat().st_size > 0:
                print(f"  导出成功: {temp_out} ({temp_out.stat().st_size} bytes)")
            else:
                print("  导出失败: 文件未生成或为空")
                return False
        except Exception as e:
            print(f"  导出失败: {e}")
            return False

        # 构建 Python 项目
        print(f"\n[4/4] 生成 Python 项目...")
        try:
            build_project(str(temp_out), str(output_dir))
        except Exception as e:
            print(f"  生成失败: {e}")
            import traceback
            traceback.print_exc()
            return False

        # README.md 稍后手动根据项目文件内容编写
        print(f"\n跳过自动生成 README.md（将手动编写）")

        print(f"\n✓ 成功: {output_dir}")
        return True

    finally:
        # 清理临时文件
        if Path(temp_dir).exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """主函数"""
    print("="*60)
    print("批量 .sml -> Python 项目转换工具")
    print("="*60)
    print(f"源目录: {SOURCE_DIR}")
    print(f"输出目录: {OUTPUT_BASE_DIR}")
    
    if not SOURCE_DIR.exists():
        print(f"\n错误: 源目录不存在: {SOURCE_DIR}")
        sys.exit(1)

    # 创建输出根目录
    OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)

    # 查找所有 .sml 文件
    sml_files = sorted(SOURCE_DIR.rglob("*.sml"))
    total = len(sml_files)
    
    print(f"\n找到 {total} 个 .sml 文件")
    print("-"*60)

    if total == 0:
        print("没有找到 .sml 文件，退出")
        sys.exit(0)

    # 确认处理
    print(f"\n即将处理以下 {total} 个模型文件:")
    for i, sml_path in enumerate(sml_files, 1):
        rel = sml_path.relative_to(SOURCE_DIR)
        print(f"  {i}. {rel}")
    
    print(f"\n输出位置: {OUTPUT_BASE_DIR}")
    print("-"*60)

    # 处理每个文件
    success_count = 0
    failed_count = 0
    failed_files = []

    for i, sml_path in enumerate(sml_files, 1):
        print(f"\n\n[{i}/{total}] ")
        success = process_sml_file(sml_path, OUTPUT_BASE_DIR, SOURCE_DIR)
        if success:
            success_count += 1
        else:
            failed_count += 1
            failed_files.append(str(sml_path.relative_to(SOURCE_DIR)))

    # 统计结果
    print(f"\n\n{'='*60}")
    print("处理完成")
    print(f"{'='*60}")
    print(f"总计: {total}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    
    if failed_files:
        print(f"\n失败的文件:")
        for f in failed_files:
            print(f"  - {f}")
    
    print(f"\n输出目录: {OUTPUT_BASE_DIR}")
    print("="*60)


if __name__ == "__main__":
    main()
