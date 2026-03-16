from typing import Literal
from pyosis.core import REGISTRY


@REGISTRY.register("AsgnCompThk")
def osis_property_asgncompthk(dThickness: float, strOp: str, strElem: str) -> tuple[bool, str]:
    """
    分配或重置单个单元的理论厚度，用于定义收缩徐变特性

    Args:
        dThickness (float): 构件理论厚度
        strOp (str): 操作；
        strElem (str): 待分配单元的编号

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

