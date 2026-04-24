from pyosis.core.engine import OSISEngine

def build_sections(engine: OSISEngine) -> list[int]:
    """创建截面，返回截面编号列表 [1, 2, 3, 4, 5]
    
    截面编号（显式定义，幂等执行）：
    - 1: 标准截面（MIDDLE）
    - 2: 墩顶截面（MIDDLE）
    - 3: 加厚截面（MIDDLE）
    - 4: 墩顶截面（MIDDLE）
    - 5: 加厚截面（MIDDLE）
    """
    section = engine.section
    
    # 截面 1: 标准截面
    sec1 = section.create_hollowslab(
        "标准截面", "MIDDLE",
        0.9500, 1.0000, 0.5700, 0.0500,
        0.1200, 0.1200, 0.1600, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0500, 0.0500, 0.0800, 0.0800, 0.1200,
        no=1
    )
    sec1.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec1.set_mesh(0, 0.1000)
    
    # 截面 2: 墩顶截面
    sec2 = section.create_hollowslab(
        "墩顶截面", "MIDDLE",
        0.9500, 1.0000, 0.6200, 0.0000,
        0.1200, 0.2500, 0.3200, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0000, 0.0500, 0.0000, 0.0800, 0.1200,
        no=2
    )
    sec2.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec2.set_mesh(0, 0.1000)
    
    # 截面 3: 加厚截面
    sec3 = section.create_hollowslab(
        "加厚截面", "MIDDLE",
        0.9500, 1.0000, 0.5700, 0.0500,
        0.1200, 0.2500, 0.2400, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0500, 0.0500, 0.0800, 0.0800, 0.1200,
        no=3
    )
    sec3.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec3.set_mesh(0, 0.1000)
    
    # 截面 4: 墩顶截面（复制）
    sec4 = section.create_hollowslab(
        "墩顶截面", "MIDDLE",
        0.9500, 1.0000, 0.6200, 0.0000,
        0.1200, 0.2500, 0.3200, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0000, 0.0500, 0.0000, 0.0800, 0.1200,
        no=4
    )
    sec4.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec4.set_mesh(0, 0.1000)
    
    # 截面 5: 加厚截面（复制）
    sec5 = section.create_hollowslab(
        "加厚截面", "MIDDLE",
        0.9500, 1.0000, 0.5700, 0.0500,
        0.1200, 0.2500, 0.2400, 0.1200, 0.2400,
        0.3800, 0.1500, 0.0800, 0.1200, 0.0800,
        0.0500, 0.0500, 0.0800, 0.0800, 0.1200,
        no=5
    )
    sec5.set_offset("Middle", 0.0000, "Top", 0.0000)
    sec5.set_mesh(0, 0.1000)
    
    return [sec1.no, sec2.no, sec3.no, sec4.no, sec5.no]

if __name__ == "__main__":
    from ._0_engine import engine
    sec_nos = build_sections(engine)
    print(sec_nos)
    print(engine.section.all())
