from ..core import REGISTRY

@REGISTRY.register("Replot")
def osis_replot():
    """
    重新绘制窗口
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("Clear")
def osis_clear():
    """
    清空项目
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("Solve")
def osis_solve():
    """
    求解工程
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass
