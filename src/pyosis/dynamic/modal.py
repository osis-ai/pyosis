"""
pyosis.dynamic.modal 的 Docstring

自振模态分析底层命令接口
"""

from ..core import REGISTRY


@REGISTRY.register("ModOpt")
def osis_mod_opt(nNum: int = 1):
    """定义模态分析所需的特征值最大数目。

    Args:
        nNum (int): 需要计算的特征值最大数目，缺省值：1

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Examples:
        >>> # 设置计算前 5 阶模态
        >>> result = osis_mod_opt(5)
        >>> print(result)
        (True, "")
    """
    pass
