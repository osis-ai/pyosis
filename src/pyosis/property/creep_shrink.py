'''
pyosis.property.creep_shrink 的 Docstring

时间依存性材料属性
'''
from ..core import REGISTRY

@REGISTRY.register("CrpShrk")
def osis_creep_shrink(
    nNO: int = 1,
    strName: str = "收缩徐变1",
    strCode: str = "JTG3362_2018",
    dFcuk: float = 5.0e7,
    dAvgHumidity: float = 70.0,
    dComponentApproximateSize: float = 1.0,
    dTypeCoeff: float = 5.0,
    nBirthByShrinking: int = 3,
    dFlyAshRatio: float = 0.0,
):
    """
    创建或修改收缩徐变特性

    命令流：CrpShrk, Index, Name, Code, Fcuk, AVG.Humidity,
            ComponentApproximateSize, Type.Coeff, BirthByShrinking, FlyAshRatio
    参数按此顺序组装，共 9 个，缺一不可（软件侧会校验参数个数）。

    Args:
        nNO (int): 收缩徐变特性编号（Index）
        strName (str): 名称（Name）
        strCode (str): 规范（Code），目前只支持 JTG3362_2018
        dFcuk (float): 28天龄期的混凝土强度（Fcuk），按工程当前压力单位填写，
            默认单位 Pa 下 5.0e7 即 50MPa，合法区间 1MPa~200MPa
        dAvgHumidity (float): 周围环境的相对湿度，百分比，取值 40~99
        dComponentApproximateSize (float): 构件大致尺寸（m），必须大于 0
        dTypeCoeff (float): 水泥种类系数（Type.Coeff）
        nBirthByShrinking (int): 收缩开始时的混凝土龄期，天数（BirthByShrinking）
        dFlyAshRatio (float): 粉煤灰添加量，百分比，取值 0~50

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register('CrpShrkDel')
def osis_creep_shrink_del(nNO: int):
    """删除收缩徐变特性

    Args:
        nNO (int): 收缩徐变特性编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('CrpShrkMod')
def osis_creep_shrink_mod(nOld: int, nNew: int):
    """修改一个收缩徐变特性的编号。收缩徐变特性编号存在时，交换

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
