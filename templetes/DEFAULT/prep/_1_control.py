"""全局控制参数"""

from pyosis.core.engine import OSISEngine

def setup_control(engine: OSISEngine) -> None:
    """全局控制参数"""

    # ========== 原始命令流 ==========
    # Acel,9.8066; //定义加速度
    # CalcTendon,1;//打开计算预应力开关
    # CalcConForce,1;//打开计算并发反力开关
    # CalcShrink,1;//打开计算收缩开关
    # CalcCreep,1;//打开计算徐变开关
    # CalcShear,1;//打开计算剪切变形开关
    # CalcRlx,1;//打开计算钢束松弛开关
    # ModLocCoor,0;//打开修改变截面局部坐标系开关
    # IncTendon,1;//打开考虑钢束自重开关
    # NL,0,0;//设置非线性参数，打开几何非线性
    # LnSrch,0;//设置非线性参数，打开非线性连接单元
    # AutoTs,0;//设置非线性参数，线形检索
    # ModOpt,0;//设置模态阶数
    return


if __name__ == "__main__":
    from ._0_engine import engine
    setup_control(engine)