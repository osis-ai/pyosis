from typing import Literal
from ..core import OSISEngine

def osis_elem_force(strLCName: str, eDataItem: Literal['EF'], eElementType: Literal["BEAM3D", "TRUSS", "SPRING", "CABLE", "SHELL"]):
    '''
    提取内力结果
    
    Args:
        strLCName (str): 工况名称
        eDataItem (str): 数据类型，不区分大小写。EF = 内力
        eElementType (str): 单元类型，不区分大小写。BEAM3D = 梁柱单元，TRUSS = 桁架单元，SPRING = 弹簧单元，CABLE = 拉索单元，SHELL = 壳单元

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    e = OSISEngine.GetInstance()
    eDataItem = eDataItem.upper()
    eElementType = eElementType.upper()
    return e.OSIS_ElemForce(strLCName, eDataItem, eElementType)
