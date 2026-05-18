"""
简支空心板桥梁建模示例

使用方式:
    python main.py              # 完整建模（默认清空重建）
    python main.py --increment  # 增量模式：不清空，幂等执行
    
也可以直接执行单个模块:
    python modules/_5_node.py   # 只执行节点创建
    python modules/_6_element.py # 只执行单元创建（会从engine读取已有节点）
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
from prep._9_analysis import build_settle_analysis, build_live_analysis, build_buckling_analysis, build_damping
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
    print("开始建模：简支空心板桥梁" + ("（增量模式）" if incremental else "（清空重建）"))
    print("=" * 50)
    
    # 1. 全局设置（无依赖）
    print("\n[1/10] 设置全局控制参数...")
    setup_control(engine)
    
    # 2. 几何属性（无依赖）
    print("[2/10] 设置几何属性（钢束线型）...")
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
    
    # 6. 单元（获取node/section/material）
    print("[6/10] 创建单元...")
    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)
    
    # 7. 边界（获取node）
    print("[7/10] 创建边界条件...")
    bd_nos, bd_group_names = build_boundaries(engine, node_nos)
    
    # 8. 荷载工况（获取geo/mat/elem）
    print("[8/10] 创建荷载工况和钢束...")
    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)
    
    # 9. 活载分析（获取elem）
    print("[9/10] 创建分析...")
    settle_names = build_settle_analysis(engine, node_nos)
    live_names = build_live_analysis(engine, elem_group_names)
    buckling_names = build_buckling_analysis(engine, lc_names)
    damping_names = build_damping(engine)
    
    # 10. 施工阶段（获取所有组）
    print("[10/10] 创建施工阶段...")
    build_stages(
        engine,
        elem_group_names,
        bd_group_names,
        lc_names,
        settle_names,
        live_names,
        buckling_names,
        damping_names,
    )    
    print("\n" + "=" * 50)
    print("建模完成！")
    print("=" * 50)
    
    if run_analysis:
        print("\n开始运行分析...")
        engine.solve()
        print("分析完成！")
    else:
        print("\n提示: 调用 engine.solve() 运行分析")
    
    return engine


def main():
    parser = argparse.ArgumentParser(description='简支空心板桥梁建模')
    parser.add_argument('--increment', action='store_true', 
                        help='增量模式：不清空（默认清空重建）')
    parser.add_argument('--solve', action='store_true',
                        help='建模后自动运行分析')
    parser.add_argument('--save', type=str, default='',
                        help='保存项目到指定路径')
    
    args = parser.parse_args()
    
    # 执行建模（默认清空重建）
    build_model(incremental=args.increment, run_analysis=args.solve)
    
    # 保存项目
    if args.save:
        print(f"\n保存项目到: {args.save}")
        engine.save_project()


if __name__ == "__main__":
    main()
