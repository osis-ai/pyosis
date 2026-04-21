from typing import Dict, Any, Literal
from ..core import REGISTRY

@REGISTRY.register("InflAlgo")
def osis_lane_ve(strName: str, eType: Literal["VE"], dLength: float, wheel: int, eOriention: Literal[-1, 0, 1], eRef: Literal[0, 1], param: list):
    # Name, type, length, vehOri, ref, par1,par2, par3
    '''
    定义活载影响线计算方法：车道单元法（Vehicle Element Method）

    Args:
        strName (str): 车道名称，如"行车道-左幅"
        eType (str): 算法类型，不区分大小写。固定为 'VE'（Vehicle Element）
        dLength (float): 车道对应的桥梁跨度（m），决定影响线计算范围
        wheel: 轮距(默认为0，占位)
        eOriention (int): 车辆移动方向
            - -1: 向后（车辆沿坐标轴负向行驶）
            - 0: 往返（影响线对称，用于最不利加载）
            - 1: 向前（车辆沿坐标轴正向行驶）
        eRef (int): 车道参照方式
            - 0: 参照单元组定义车道
            - 1: 参照样条曲线定义车道
        param (list): 可变参数列表，长度和内容取决于 eRef：
            - **当 eRef=0 时**: param = [ESel, OffsetY, OffsetZ]
                - ESel (str): 参照纵梁单元组名称（纵梁）
                - OffsetY (float): 局部坐标系下Y方向偏移量（m），车道路径相对于单元组的横向偏移
                - OffsetZ (float): 局部坐标系下Z方向偏移量（m），车道路径相对于单元组的竖向偏移
            - **当 eRef=1 时**: param = [SplineName]
                - SplineName (str): 样条曲线名称（需在命令流中预先用数组定义）

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    工程说明:
        - 适用于主梁为梁单元（Beam/Truss）的桥梁结构
        - 车辆荷载沿定义的纵向路径移动，自动计算各主梁内力影响线
        - 多车道时需定义多个车道线，考虑横向折减系数
        - 偏移量用于模拟实际车轮轨迹与主梁轴线不重合的情况（如悬臂行车道）

    示例:
        # 基于纵梁单元定义车道，横向偏移2.5m（右侧行车道）
        osis_lane_ve("行车道-右", "VE", 30.0, 1, 0, ["主梁单元组", 2.5, 0.0])
        
        # 基于样条曲线定义曲线桥车道
        osis_lane_ve("弯桥车道", "VE", 120.0, 1, 1, ["spline_curve_1"])
    '''
    pass

@REGISTRY.register("InflAlgo")
def osis_lane_tcb(strName: str, eType: Literal["TCB"], ESel: str, dLength: float, wheel: int,eOriention: Literal[-1, 0, 1], eRef: Literal[0, 1], param: list):
    '''
    定义活载影响线计算方法：横向联系梁法（Transverse Connection Beam Method）

    Args:
        strName (str): 车道名称，如"重车道-TCB"
        eType (str): 算法类型，不区分大小写。固定为 'TCB'（Transverse Connection Beam）
        ESel (str): 横梁单元组名称（如横隔板、横梁框架）
        dLength (float): 车道对应的桥梁跨度（m）
        wheel: 轮距(默认为0，占位)
        eOriention (int): 车辆移动方向
            - -1: 向后
            - 0: 往返
            - 1: 向前
        eRef (int): 车道参照方式
            - 0: 参照单元组定义车道
            - 1: 参照样条曲线定义车道
        param (list): 可变参数列表，长度和内容取决于 eRef：
            - **当 eRef=0 时**: param = [RefESel, OffsetY, OffsetZ]
                - RefESel (str): 参照纵梁单元组名称（主梁）
                - OffsetY (float): 局部坐标系下Y方向偏移量（m）
                - OffsetZ (float): 局部坐标系下Z方向偏移量（m）
            - **当 eRef=1 时**: param = [SplineName]
                - SplineName (str): 样条曲线名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    工程说明:
        - 适用于由主梁+横梁组成的格子梁桥、刚架桥等空间传力结构
        - 车辆荷载先分配给最近的横梁，再经横梁传递至主梁，更符合实际传力路径
        - 能准确模拟"荷载横向分布系数"的物理本质
        - 横梁刚度越大，计算精度越高（建议横梁单元刚度不小于主梁的0.1倍）

    示例:
        # 混凝土T梁桥的横隔板体系
        osis_lane_tcb(
            "重车道-TCB", "TCB", 
            "横隔板单元组",  # 横梁
            40.0, 1, 0, 
            ["T梁单元组", 0.0, 0.0]  # 纵梁，无偏移
        )
    '''
    pass

@REGISTRY.register("InflAlgoDel")
def osis_lane_del(strName: str):
    '''
    删除车道线
    
    Args:
        strName (str): 名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

@REGISTRY.register("InflAlgoMod")
def osis_lane_mod(strOldName: str, strNewName: str):
    '''
    修改车道线名称
    
    Args:
        strOldName (str): 旧名称
        strOldName (str): 新名称

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass
