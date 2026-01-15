"""
Interfaces of OSIS functions

========

"""
from typing import Literal
from ..core import REGISTRY

# 后续会重写这部分接口

# @REGISTRY.register('Material')
# def osis_material(nMat: int, strName: str, eMaterialType: Literal["CONC", "STEEL", "PRESTRESSED", "REBAR", "CUSTOM"], eCode: str, eGrade: str, nCrepShrk: int, dDmp: float, params: dict[str, Any]={}):
#     """创建或修改材料。

#     Args:
#         nMat (int): 材料编号
#         strName (str): 材料名称
#         eMaterialType (str): 材料类型，不区分大小写。可选值：
#             * CONC: 混凝土
#             * STEEL: 钢材
#             * PRESTRESSED: 预应力材料
#             * REBAR: 普通钢筋
#             * CUSTOM: 自定义材料
#         eCode (str): 材料标准代码，可选值：
#             * 钢材: JTGD64_2015
#             * 其他材料: JTG3362_2018, JTGD62_2004
#         eGrade (str): 材料等级牌号，根据材料类型可选：
#             * 混凝土: C15, C20, C25, C30, C35, C40, C45, C50, C55, C60, C65, C70, C75, C80
#             * 钢材: Q235, Q345, Q390, Q420
#             * 预应力材料:
#                 ** JTG3362_2018: Strand1720, Strand1860, Strand1960, Wire1470, Wire1570, 
#                   Wire1770, Wire1860, Rebar785, Rebar930, Rebar1080
#                 ** JTGD62_2004: Strand1860, Wire1670, Wire1770, Rebar785, Rebar930
#             * 普通钢筋:
#                 ** JTG3362_2018: HPB300, HRB400, HRBF400, RRB400, HRB500
#                 ** JTGD62_2004: R235, HRB335, HRB400, KL400
#         nCrepShrk (int): 收缩徐变特性编号（混凝土材料需要，其他材料设置为-1）
#         dDmp (float): 材料阻尼比
#         params (dict): 自定义材料的参数 (E, G, Mu, ExpCoeff, UnitWeight, Density, Dmp)，创建其他材料不填。创建自定义材料 eCode eGrade nCrepShrk dDmp 会被忽略

#     Returns:
#         tuple (bool, str):
#             - bool: 操作是否成功
#             - str: 失败原因（如果操作失败）

#     Examples:
#         >>> result = osis_material(1, "C30", "CONC", "JTG3362_2018", "C30", 1, 0.05)
#         >>> print(result)
#         (True, "")
#     """
#     e = OSISEngine.GetInstance()
#     eMaterialType = eMaterialType.upper()
#     return e.OSIS_Material(nMat, strName, eMaterialType, eCode, eGrade, nCrepShrk, dDmp, params)

@REGISTRY.register('Material')
def osis_material_conc(nMat: int, strName: str, eMaterialType: Literal["CONC"],
                       eCode: Literal["JTG3362_2018", "JTGD62_2004"], 
                       eGrade: Literal["C15", "C20", "C25", "C30", "C35", "C40", "C45", "C50", "C55", "C60", "C65", "C70", "C75", "C80"], 
                       nCrepShrk: int, dDmp: float):
    """创建或修改混凝土材料

    Args:
        nMat (int): 材料编号
        strName (str): 材料名称
        eMaterialType (str): 材料类型，不区分大小写。固定为 CONC
        eCode (str): 材料标准代码，不区分大小写。可选值：
            * JTG3362_2018
            * JTGD62_2004
        eGrade (str): 材料等级牌号，不区分大小写。根据材料类型可选：
            * C15, C20, C25, C30, C35, C40, C45, C50, C55, C60, C65, C70, C75, C80
        nCrepShrk (int): 收缩徐变特性编号
        dDmp (float): 材料阻尼比

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Material')
def osis_material_steel(nMat: int, strName: str, eMaterialType: Literal["STEEL"], eCode: Literal["JTGD64_2015"], eGrade: Literal["Q235", "Q345", "Q390", "Q420"], dDmp: float):
    """创建或修改钢材

    Args:
        nMat (int): 材料编号
        strName (str): 材料名称
        eMaterialType (str): 材料类型，不区分大小写。固定为 STEEL
        eCode (str): 材料标准代码，可选值：
            * JTGD64_2015
        eGrade (str): 材料等级牌号，根据材料类型可选：
            * Q235
            * Q345
            * Q390
            * Q420
        dDmp (float): 材料阻尼比

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Material')
def osis_material_prestressed(nMat: int, strName: str, eMaterialType: Literal["PRESTRESSED"], eCode: Literal["JTG3362_2018", "JTGD62_2004"], eGrade: str, dDmp: float):
    """创建或修改材料。

    Args:
        nMat (int): 材料编号
        strName (str): 材料名称
        eMaterialType (str): 材料类型，不区分大小写。固定为 PRESTRESSED
        eCode (str): 材料标准代码，可选值：
            * JTG3362_2018
            * JTGD62_2004
        eGrade (str): 材料等级牌号，根据材料类型可选：
            * JTG3362_2018: Strand1720, Strand1860, Strand1960, Wire1470, Wire1570, 
                  Wire1770, Wire1860, Rebar785, Rebar930, Rebar1080
            * JTGD62_2004: Strand1860, Wire1670, Wire1770, Rebar785, Rebar930
        nCrepShrk (int): 收缩徐变特性编号（混凝土材料需要，其他材料设置为-1）
        dDmp (float): 材料阻尼比
        params (dict): 自定义材料的参数 (E, G, Mu, ExpCoeff, UnitWeight, Density, Dmp)

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Material')
def osis_material_reber(nMat: int, strName: str, eMaterialType: Literal["REBAR"], eCode: Literal["JTG3362_2018", "JTGD62_2004"], 
                        eGrade: Literal["HPB300", "HRB400", "HRBF400", "RRB400", "HRB500"] | Literal["R235", "HRB335", "HRB400", "KL400"], dDmp: float):
    """创建或修改钢材

    Args:
        nMat (int): 材料编号
        strName (str): 材料名称
        eMaterialType (str): 材料类型，不区分大小写。固定为 REBAR
        eCode (str): 材料标准代码，可选值：
            * JTG3362_2018
            * JTGD62_2004
        eGrade (str): 材料等级牌号，根据材料类型可选（不按照规定填写可能会有错误）：
            * JTG3362_2018: HPB300, HRB400, HRBF400, RRB400, HRB500
            * JTGD62_2004: R235, HRB335, HRB400, KL400
        dDmp (float): 材料阻尼比

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('Material')
def osis_material_custom(nMat: int, strName: str, eMaterialType: Literal["CUSTOM"], dE: float=0, dG: float=0, dMu: float=0, dExpCoeff: float=0, dUnitWeight: float=0, dDensity: float=0, dDmp: float=0):
    """创建或修改材料。

    Args:
        nMat (int): 材料编号
        strName (str): 材料名称
        eMaterialType (str): 材料类型，不区分大小写。固定为 CUSTOM
        dE (float): 弹性模量(Pa)
        dG (float): 剪切模量(Pa)
        dMu (float): 泊松比
        dExpCoeff (float): 线膨胀系数(1/摄氏度)
        dUnitWeight (float): 容重(N/m^3)
        dDensity (float): 质量密度(kg/m^3)
        dDmp (float): 材料阻尼比

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('MaterialDel')
def osis_material_del(nMat: int):
    """删除一个材料

    Args:
        nMat (int): 单元编号，从 1 开始计数

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('MaterialMod')
def osis_material_mod(nOld: int, nNew: int):
    """修改一个材料的编号。材料编号存在时，交换

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

