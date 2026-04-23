from pyosis.core.engine import OSISEngine

def build_sections(engine: OSISEngine) -> list[int]:
    """创建截面，返回截面编号列表 [sec1, sec2, sec3, sec4, sec5]"""
    section = engine.section
    
    sec1 = section.create_hollowslab("标准截面", "MIDDLE", 0.9500,1.0000,0.5700,0.0500,0.1200,0.1200,0.1600,0.1200,0.2400,0.3800,0.1500,0.0800,0.1200,0.0800,0.0500,0.0500,0.0800,0.0800,0.1200)
    sec1.set_offset("Middle",0.0000,"Top",0.0000)
    sec1.set_mesh(0, 0.1000)
    
    sec2 = section.create_hollowslab("墩顶截面", "MIDDLE", 0.9500,1.0000,0.6200,0.0000,0.1200,0.2500,0.3200,0.1200,0.2400,0.3800,0.1500,0.0800,0.1200,0.0800,0.0000,0.0500,0.0000,0.0800,0.1200)
    sec2.set_offset("Middle",0.0000,"Top",0.0000)
    sec2.set_mesh(0, 0.1000)
    
    sec3 = section.create_hollowslab("加厚截面", "MIDDLE", 0.9500,1.0000,0.5700,0.0500,0.1200,0.2500,0.2400,0.1200,0.2400,0.3800,0.1500,0.0800,0.1200,0.0800,0.0500,0.0500,0.0800,0.0800,0.1200)
    sec3.set_offset("Middle",0.0000,"Top",0.0000)
    sec3.set_mesh(0, 0.1000)
    
    sec4 = section.create_hollowslab("墩顶截面", "MIDDLE", 0.9500,1.0000,0.6200,0.0000,0.1200,0.2500,0.3200,0.1200,0.2400,0.3800,0.1500,0.0800,0.1200,0.0800,0.0000,0.0500,0.0000,0.0800,0.1200)
    sec4.set_offset("Middle",0.0000,"Top",0.0000)
    sec4.set_mesh(0, 0.1000)
    
    sec5 = section.create_hollowslab("加厚截面", "MIDDLE", 0.9500,1.0000,0.5700,0.0500,0.1200,0.2500,0.2400,0.1200,0.2400,0.3800,0.1500,0.0800,0.1200,0.0800,0.0500,0.0500,0.0800,0.0800,0.1200)
    sec5.set_offset("Middle",0.0000,"Top",0.0000)
    sec5.set_mesh(0, 0.1000)
    
    sec_nos = [sec1.no, sec2.no, sec3.no, sec4.no, sec5.no]
    return sec_nos

if __name__ == "__main__":
    from _0_engine import engine
    sec_nos = build_sections(engine)
    print(sec_nos)
    print(engine.section.all())
