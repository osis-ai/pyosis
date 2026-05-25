"""

规范验算（后处理）

"""
from typing import Literal
from ..core import REGISTRY


@REGISTRY.register('Code')
def osis_code(eCode: Literal["JTG", "JTG18", "JTGD64"]):
    """设置验算规范（仅能设置一个；软件侧若未下发本命令则默认为 JTG18）。

    Args:
        eCode (str): 规范代号，不区分大小写。可选值：
            * JTG — JTG 3362-2018
            * JTG18 — JTG 3362-2018
            * JTGD64 — JTG D64-2015

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CdEleSel')
def osis_cd_ele_sel(
    eOP: Literal["All", "None", "Inve", "S", "A", "U", "R"],
    *paras: str | int,
):
    """后处理选择单元。


    Args:
        eOP (str): 操作，不区分大小写。可选值：
            * All — 全选
            * None — 全不选
            * Inve — 反选
            * S — 替换
            * A — 添加
            * U — 删除
            * R — 再选择
        *paras: 待操作的单元编号，支持 8to10 等形式；All、None、Inve 时可缺省

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CdEleAct')
def osis_cd_ele_act(
    eOP: Literal["All", "Inve", "S", "A", "U", "R"],
    *paras: str | int,
):
    """后处理激活单元

    Args:
        eRowType (str): 固定为 CdEleAct
        eOP (str): 操作，不区分大小写。可选值：
            * All — 全激活
            * Inve — 反选
            * S — 替换
            * A — 添加
            * U — 删除
            * R — 再激活
        *paras: 待操作的单元编号，支持 8to10 等形式；All、Inve 时可缺省

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CdDL')
def osis_cd_dl( nLevel: Literal[1, 2, 3] = 1):
    """设置设计安全等级（需先选中单元；软件侧若未设置则默认为一级）。

    Args:
        nLevel (int): 等级，可选值 1、2、3，分别对应一级、二级、三级

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CdPC')
def osis_cd_pc(
    eMemberType: Literal["EPC", "APC", "BPC", "RC", "PierCap"] | None = None,
    eConstructType: Literal["Pre", "Cast"] | None = None,
    ePCTensioningType: Literal["Pre", "Post"] | None = None,
):
    """设置构件类型、PC 构件施工方式及张拉方式（需先选中单元）。

    Args:
        eMemberType (str): 构件类型；为 None 时不输出本列及后续列（不修改相关设置）。可选值：
            * EPC — 全预应力
            * APC — A 类预应力
            * BPC — B 类预应力
            * RC — 钢筋混凝土
            * PierCap — 盖梁
        eConstructType (str): 施工方式，Pre=预制，Cast=现浇；为 None 时不修改。RC、PierCap 无需填写
        ePCTensioningType (str): 张拉方式，Pre=先张，Post=后张；为 None 时不修改。RC、PierCap 无需填写

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Note:
        eMemberType 为 None 时，请勿单独传入 eConstructType / ePCTensioningType，以免命令列与后端约定不一致。
    """
    pass


@REGISTRY.register('CdPRSRatio')
def osis_cd_prs_ratio(dRatio: float = 1.0):
    """设置基于截面底缘起算多少倍 h 范围内预应力弯起钢筋参与抗剪验算（需先选中单元）。

    Args:
        dRatio (float): 倍数，取值范围 [0.0, 1.0]；软件侧默认 1.0

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CdCSCRatio')
def osis_cd_csc_ratio(dRatio: float = 0.8):
    """设置施工阶段混凝土强度折减系数（需先选中单元）。

    Args:
        eRowType (str): 固定为 CdCSCRatio
        dRatio (float): 折减系数，取值范围 [0.8, 1.0]；软件侧默认 0.8

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CdE')
def osis_cd_e(
    nType: Literal[1, 2, 3, 4, 5, 6, 7] | None = None,
    strGrade: Literal["A", "B", "C", "D", "E", "E/F", "D/E/F"] | None = None,
):
    """设置环境类别和环境等级（需先选中单元；软件侧默认一般环境、等级 A）。

    Args:
        nType (int): 环境类别，可选值 1～7：
            * 1 — 一般环境
            * 2 — 冻融环境
            * 3 — 海洋氯化物环境
            * 4 — 其他氯化物环境
            * 5 — 盐结晶环境
            * 6 — 化学腐蚀环境
            * 7 — 磨蚀环境
        strGrade (str): 环境等级，需与类别匹配，如 A、B、C、D、E、E/F、D/E/F 等（详见规范表）

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Note:
        为 None 的项在命令流中省略。若后端按固定列解析且需“只改等级不改类别”等，请对不修改列传空字符串 \"\" 占位。
    """
    pass


@REGISTRY.register('CdCrack')
def osis_cd_crack(
    dC1: float | str | None = None,
    dC2: float | str | None = None,
    dC3: float | str | None = None,
    dCover: float | str | None = None,
):
    """设置裂缝计算参数（需先选中单元）。

    Args:
        dC1 (float): 参数 C1，须大于 0；软件侧默认 1.0
        dC2 (float): 参数 C2，须大于 0；软件侧默认 1.5
        dC3 (float): 参数 C3，须大于 0；软件侧默认 1.0
        dCover (float): 混凝土保护层厚度，须 ≥ 0；软件侧默认 0.0

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Note:
        为 None 的项在命令流中省略。若需保持列位置而表示“不修改”，对该列传入空字符串 \"\"（参见 pyosis 命令组装规则）。
    """
    pass


@REGISTRY.register('CdAutoC2')
def osis_cd_auto_c2(strPara: Literal["My", "Mz", "Nx"]):
    """自动计算裂缝参数 C2（长期效应影响系数）（需先选中单元）。

    Args:
        eRowType (str): 固定为 CdAutoC2
        strPara (str): 只能为 My、Mz、Nx。对准永久与频遇组合循环，子工况一致时按 C2=1+0.5Ml/Ms，
            各单元取最大 C2

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CdCrackWeld')
def osis_cd_crack_weld(
    nPara: Literal[0, 1],
    dFactor: float = 1.3,
):
    """设置焊接钢筋骨架系数（需先选中单元）。

    Args:
        nPara (int): 0 — 无焊接钢筋骨架（默认）；1 — 有焊接钢筋骨架
        dFactor (float): 焊接钢筋骨架系数，须大于 0；软件侧默认 1.3，仅在 nPara 为 1 时生效

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Note:
        nPara 为 None 时两项均省略（不修改）。nPara 为 0 时通常无需传 dFactor。
    """
    pass


@REGISTRY.register('CdGeoLCo')
def osis_cd_geo_lco(
    dLy: float,
    dKy: float,
    dLz: float,
    dKz: float,
):
    """设置构件几何长度及计算长度系数（需先选中单元）。

    命令列顺序：Cd,CdGeoLCo,Ly,Ky,Lz,Kz

    Args:
        eRowType (str): 固定为 CdGeoLCo
        dLy (float): 方向 y 几何长度，须大于 0；软件侧默认取单元长度
        dKy (float): 方向 y 计算长度系数，须大于 0；软件侧默认 1.0
        dLz (float): 方向 z 几何长度，须大于 0；软件侧默认取单元长度
        dKz (float): 方向 z 计算长度系数，须大于 0；软件侧默认 1.0

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Note:
        为 None 的项在命令流中省略。若需保持列位置而表示“不修改”，对该列传入空字符串 \"\"。
    """
    pass


@REGISTRY.register('CdCheck')
def osis_cd_check(strPara: Literal["All", "None"] | str):
    """设置验算项开关（需先选中单元）。

    Args:
        eRowType (str): 固定为 CdCheck
        strPara (str): All / all — 全部打开；None / none — 全部关闭；
            亦可为 JSON 字符串，例如 '[{"UltM":1,"Shear":1}]'，其中 0 表示关闭该项、1 表示打开。
            因命令组装对 dict 仅输出取值，字典形式请使用 json.dumps 等转为字符串后传入。

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('Check')
def osis_check_add(
    eItem: Literal[
        "UltM", "UltN", "Shear", "CrackS", "CrackL", "CrackWeb", "CrackWidth",
        "SSNC", "SSPC", "CSNC", "CSNT",
    ],
    strCombineName: str,
):
    """添加验算作用。

    Args:
        eItem (str): 验算项代号，如 UltM、UltN、Shear、CrackS、CrackL、CrackWeb、CrackWidth、
            SSNC、SSPC、CSNC、CSNT（与荷载组合类型匹配关系见规范说明）
        strCombineName (str): 荷载组合名称（可为工况或包络）

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CheckSolve')
def osis_check_solve():
    """计算验算作用。

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register('CheckDel')
def osis_check_del(
    strItem: (
        Literal[
            "UltM", "UltN", "Shear", "CrackS", "CrackL", "CrackWeb", "CrackWidth",
            "SSNC", "SSPC", "CSNC", "CSNT",
        ]
        | Literal["All", "all"]
        | str
    ),
    strCombineName: str | None = None,
):
    """删除验算作用。

    Args:
        strItem (str): All / all — 删除所有验算；具体验算项代号同 Check；
            传空字符串 \"\" 表示 Item 缺省 — 删除该荷载组合名称下的全部验算作用
        strCombineName (str): 荷载组合名称；在 strItem 为 All / all 时通常可省略（为 None 时不输出该列）

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）

    Note:
        删除某一组合下全部验算时：strItem 传 \"\"，strCombineName 传目标组合名，生成 Cd,CheckDel,,CombineName。
    """
    pass
