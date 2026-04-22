"""
简支空心板桥梁建模示例

使用方式:
    python main.py          # 完整建模并运行分析
    
也可以在交互式环境使用:
    from main import build_model
    engine = build_model()  # 只建模不分析
"""

from modules._0_engine import engine
from modules._1_control import setup_control
from modules._2_property import setup_property
from modules._3_material import build_materials
from modules._4_section import build_sections
from modules._5_node import build_nodes
from modules._6_element import build_elements
from modules._7_boundary import build_boundaries
from modules._8_loadcase import build_loadcases
from modules._9_analysis import build_settle_analysis, build_live_analysis
from modules._10_stage import build_stages


def build_model(run_analysis: bool = False):
    """完整的桥梁建模流程
    
    Args:
        run_analysis: 是否自动运行分析，默认False（只建模）
    """

    print("清空项目...")
    engine.clear()
    engine.clc()

    print("=" * 50)
    print("开始建模：简支空心板桥梁")
    print("=" * 50)
    
    # 1. 全局设置
    print("\n[1/10] 设置全局控制参数...")
    setup_control(engine)
    
    # 2. 几何属性
    print("[2/10] 设置几何属性（钢束线型）...")
    setup_property(engine)
    
    # 3. 材料（无依赖）
    print("[3/10] 创建材料...")
    mat_nos = build_materials(engine)
    
    # 4. 截面（无依赖）
    print("[4/10] 创建截面...")
    sec_nos = build_sections(engine)
    
    # 5. 节点（无依赖）
    print("[5/10] 创建节点...")
    node_nos = build_nodes(engine)
    
    # 6. 单元（依赖 mat, sec, node）
    print("[6/10] 创建单元...")
    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)
    
    # 7. 边界（依赖 node）
    print("[7/10] 创建边界条件...")
    boundary_nos, boundary_group_name = build_boundaries(engine, node_nos)
    
    # 8. 荷载工况（依赖 mat, elem）
    print("[8/10] 创建荷载工况和钢束...")
    loadcase_names = build_loadcases(engine, mat_nos, elem_nos)
    
    # 9. 活载分析
    print("[9/10] 创建分析...")
    settle_analysis_names = build_settle_analysis(engine, node_nos)
    live_analysis_names = build_live_analysis(engine, elem_group_names)
    
    # 10. 施工阶段（依赖单元组、边界组、荷载工况、沉降分析、移动荷载分析）
    print("[10/10] 创建施工阶段...")
    build_stages(engine, elem_group_names, boundary_group_name, loadcase_names, settle_analysis_names, live_analysis_names)
    
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


if __name__ == "__main__":
    build_model(run_analysis=True)
