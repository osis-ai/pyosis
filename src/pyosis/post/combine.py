"""

荷载组合

"""
from typing import Literal
from ..core import REGISTRY


@REGISTRY.register('Combine')
def osis_combine_create(
    strName: str,
    eLCOrEnv: Literal["LC", "Env"],
    eSheetType: Literal["General", "Concrete", "Steel", "Composite"],
    eActivateType: Literal[
        "Activate", "Inactivate", "Basic", "Accidental", "Seismic",
        "Frequent", "Quasipermanent", "Standard",
        "Concreted1", "Concreted2", "ConcretePre1", "ConcretePre2",
        "SteelD", "SteelPre", "CompositeD", "CompositePre"
    ],
    eOperationType: Literal["ADD", "OR", "ABS", "SRSS", "AND"],
    strPrompt: str = None,
):
    """创建荷载组合（声明荷载组合）。

    命令列顺序：Combine,Name,LC/Env,SheetType,ActivateType,OperationType,Prompt

    Args:
        strName (str): 包络名称
        eLCOrEnv (str): 工况或包络，不区分大小写。可选值：
            * LC — 工况
            * Env — 包络
        eSheetType (str): 表单类型，可选值：
            * General — 一般
            * Concrete — 混凝土
            * Steel — 钢结构
            * Composite — 组合结构
        eActivateType (str): 激活类型，如 Activate、Inactivate、Basic、Accidental、Seismic、
            Frequent、Quasipermanent、Standard、Concreted1/2、ConcretePre1/2、SteelD、SteelPre、
            CompositeD、CompositePre 等（与软件表单一致）
        eOperationType (str): 操作类型，可选值：
            * ADD — 相加
            * OR — 包络
            * ABS — 绝对值
            * SRSS — 平方之和开方
            * AND — 相加（最不利），仅允许包络
        strPrompt (str): 说明，可缺省；为 None 时不输出该列

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('Post')
def osis_combine_post(combine: Literal["Combine"], strCombineName: str, strAddCombineName: str,
                      dFactor: float = 1.0):
    """定义荷载组合的内容。


    Args:
        combine (str): 固定为 Combine， 以后会删掉
        strCombineName (str): 定义的荷载组合名称
        strAddCombineName (str): 往该荷载组合中加入的工况或包络名称
        dFactor (float): 系数，缺省为 1.0

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CombineSolve')
def osis_combine_solve():
    """计算组合和包络。

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CombineDel')
def osis_combine_del(
    strPara: Literal["All", "General", "Concrete", "Steel", "Composite"] | str,
):
    """删除荷载组合。

    命令列顺序：Combine,Para

    Args:
        strPara (str): 删除范围或目标名称，可选值：
            * All — 删除全部荷载组合
            * General — 删除一般表单下的荷载组合
            * Concrete — 删除混凝土表单下的荷载组合
            * Steel — 删除钢结构表单下的荷载组合
            * Composite — 删除组合结构表单下的荷载组合
            亦可填指定荷载组合名称

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# @REGISTRY.register('Combine')
# def osis_combine_mod(
#     eRowType: Literal["CombineMod"],
#     strOldName: str,
#     strNewName: str = None,
#     eActivateType: Literal[
#         "Activate", "Inactivate", "Basic", "Accidental", "Seismic",
#         "Frequent", "Quasipermanent", "Standard",
#         "Concreted1", "Concreted2", "ConcretePre1", "ConcretePre2",
#         "SteelD", "SteelPre", "CompositeD", "CompositePre"
#     ] = None,
# ):
#     """修改荷载组合（子类型 CombineMod）。

#     命令列顺序：Combine,CombineMod,…（与后端 CombineMod 一致）

#     Args:
#         eRowType (str): 固定为 CombineMod，不区分大小写
#         strOldName (str): 旧名称
#         strNewName (str): 新名称
#         eActivateType (str): 激活类型

#     Returns:
#         tuple (bool, str):
#             - bool: 操作是否成功
#             - str: 失败原因（如果操作失败）
#     """
#     pass


# # 兼容旧函数名
# osis_post = osis_combine_post
