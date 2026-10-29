"""
Interfaces of OSIS functions

========

"""


from typing import Literal
from ..core import REGISTRY

# @REGISTRY.register("Boundary")
# def osis_boundary(nBd: int=1, eBoundaryType: Literal["GENERAL", "MSTSLV", "RELEASE", "ELSTCSPT"]="GENERAL", params: Dict[str, Any]={}):
#     '''
#     创建边界
    
#     Args:
#         nBd (int): 边界编号
#         eBoundaryType (str): 边界类型，不区分大小写。GENERAL = 一般边界，MSTSLV = 主从约束，RELEASE = 释放梁端约束，ELSTCSPT = 节点弹性支承
#         params (Dict[str, Any]): 对应边界类型所需要的参数
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     pass

@REGISTRY.register("Boundary")
def osis_boundary_general(nBd: int, eBoundaryType: Literal["GENERAL"]="GENERAL", nCoor: int = "", bX: bool = 1, bY: bool = 1, bZ: bool = 1, bRX: bool = 1, bRY: bool = 1, bRZ: bool = 1, bRW: bool = 1):
    '''
    ## 定义或修改一般边界
    pyosis.boundary.osis_boundary_general
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 GENERAL
        nCoor (int): 局部坐标系编号，"" 代表缺省
        bX (bool): 0 = 释放，1 = 约束
        bY (bool): 0 = 释放，1 = 约束
        bZ (bool): 0 = 释放，1 = 约束
        bRX (bool): 0 = 释放，1 = 约束
        bRY (bool): 0 = 释放，1 = 约束
        bRZ (bool): 0 = 释放，1 = 约束
        bRW (bool): 0 = 释放，1 = 约束
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Boundary")
def osis_boundary_master_slave(nBd: int, eBoundaryType: Literal["MSTSLV"]="MSTSLV", nNode: int = 1, bX: bool = 1, bY: bool = 1, bZ: bool = 1, bRX: bool = 1, bRY: bool = 1, bRZ: bool = 1, bCoincident: Literal[0, 1] | None = 0):
    '''
    ## 定义或修改主从约束
    pyosis.boundary.osis_boundary_master_slave
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 MSTSLV
        nNode (int): 主节点编号
        bDX (bool): 0 = 释放，1 = 约束
        bDY (bool): 0 = 释放，1 = 约束
        bDZ (bool): 0 = 释放，1 = 约束
        bRX (bool): 0 = 释放，1 = 约束
        bRY (bool): 0 = 释放，1 = 约束
        bRZ (bool): 0 = 释放，1 = 约束
        bCoincident: 0 = 同 Midas（缺省 0，可缺省），1 = 仅同位移约束
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Boundary")
def osis_boundary_rigid(nBd: int, eBoundaryType: Literal["RIGID"], nNodeI: int):
    '''
    ## 定义或修改刚性连接
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 RIGID 
        nNodeI (int): 节点1编号

    Notes: 用于形成刚性区域的节点号nodeJ, nodeK, ... , nodeL由osis_assign_boundary定义
        
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Boundary")
def osis_boundary_release(nBd: int, eBoundaryType: Literal["RELEASE"], 
                          Fxi_state: bool, Fyi_state: bool, Fzi_state: bool, Mxi_state: bool, Myi_state: bool, Mzi_state: bool, Mbi_state: bool,
                          Fxi: float,      Fyi: float,      Fzi: float,      Mxi: float,      Myi: float,      Mzi: float,      Mbi: float,
                          Fxj_state: bool, Fyj_state: bool, Fzj_state: bool, Mxj_state: bool, Myj_state: bool, Mzj_state: bool, Mbj_state: bool,
                          Fxj: float,      Fyj: float,      Fzj: float,      Mxj: float,      Myj: float,      Mzj: float,      Mbj: float):
    '''
    ## 定义或修改释放梁端约束
    pyosis.boundary.osis_boundary_release
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 RELEASE
        \\*_state (bool): 
            * 0 = 完全释放
            * 1 = 完全约束
        F\\*i and M\\*i (float): 部分约束的大小，0-1之间，表示释放后残余的约束能力的百分比
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("Boundary")
def osis_boundary_elstcspt(nBd: int, eBoundaryType: Literal["ELSTCSPT"]="ELSTCSPT", nCoor: int = "", bX: bool = 1, DX: int = 1e13, bY: bool = 1, DY: int = 1e13, bZ: bool = 1, DZ: int = 1e13, bRX: bool = 1, RX: int = 1e16, bRY: bool = 1, RY: int = 1e16, bRZ: bool = 1, RZ: int = 1e16):
    '''
    定义或修改弹簧单元弹性支承
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 ELSTCSPT
        nCoor (int): 局部坐标系编号，固定使用""缺省
        bX：UX方向，0 = 弹性，1 = 固定
        DX：坐标系X轴方向的弹性支承刚度
        bY：UY方向，0 = 弹性，1 = 固定
        DY：坐标系Y轴方向的弹性支承刚度
        bZ：UZ方向，0 = 弹性，1 = 固定
        DZ：坐标系Z轴方向的弹性支承刚度
        bRX：RX方向，0 = 弹性，1 = 固定
        RX：绕坐标系X轴方向的转动弹性刚度
        bRY：RY方向，0 = 弹性，1 = 固定
        RY：绕坐标系Y轴方向的转动弹性刚度
        bRZ：RZ方向，0 = 弹性，1 = 固定
        RZ：绕坐标系Z轴方向的转动弹性刚度
        注：弹性支撑与一般边界固定的自由度相同，且弹性支撑其余自由度上约束为零时，二者结果完全相同，不存在数值差异
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Boundary")
def osis_boundary_general_elstcspt(
    nBd: int,
    eBoundaryType: Literal["GES"],
    nCoor: int | str,
    *params: float,
):
    '''
    ## 定义或修改一般弹性支承
    
    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 GES
        nCoor (int | str): 局部坐标系编号，"" 代表缺省
        *params (float): 变长参数序列，按以下顺序排列：
            K11,K12,K13,K14,K15,K16,
            K22,K23,K24,K25,K26,
            K33,K34,K35,K36,
            K44,K45,K46,
            K55,K56,
            K66,
            bM,
            [M11,M12,...,M66（当bM=1时）],
            bC,
            [C11,C12,...,C66（当bC=1时）]
            其中 Kij/Mij/Cij 为上三角矩阵元素，必须全部给出。
            bM/bC: 0=不考虑，1=考虑
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("Boundary")
def osis_boundary_unispt(
    nBd: int,
    eBoundaryType: Literal["UNISPT"],
    sub_type: Literal["T", "N", "ML"],
    val: float | int,
    e_dir: Literal["X", "Y", "Z", "VECTOR"],
    ori: int | None = None,
    vec_x: float | None = None,
    vec_y: float | None = None,
    vec_z: float | None = None,
):
    '''
    ## 定义或修改单向弹性支承
    pyosis.boundary.osis_boundary_unispt

    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 UNISPT
        sub_type (str): T = 仅受拉，N = 仅受压，ML = 多折线
        val (float | int): sub_type 为 T / N 时是刚度值，为 ML 时是 PUCurve 定义的曲线编号
        e_dir (str): X / Y / Z 表示沿坐标轴方向，VECTOR 表示方向由向量分量给出
        ori (int): 方位，0 = 负方向，1 = 正方向；只在 X / Y / Z 分支使用
        vec_x (float): 向量 x 分量；只在 VECTOR 分支使用
        vec_y (float): 向量 y 分量；只在 VECTOR 分支使用
        vec_z (float): 向量 z 分量；只在 VECTOR 分支使用

    Notes:
        文档给两条语法：X/Y/Z 分支在 Dir 之后是 Ori，VECTOR 分支在 Dir 之后是三个向量分量。
        不用的分支传 None，该列不写入命令流，因此两类字段不会互相挤位。
        不适用动力分析。

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("Boundary")
def osis_boundary_lelnk(
    nBd: int,
    eBoundaryType: Literal["LELNK"],
    b_dx: bool,
    k_dx: float,
    b_dy: bool,
    k_dy: float,
    b_dz: bool,
    k_dz: float,
    b_rx: bool,
    k_rx: float,
    b_ry: bool,
    k_ry: float,
    b_rz: bool,
    k_rz: float,
    b_shear: bool,
    s_dy: float | str,
    s_dz: float | str,
    beta: float,
    node_i: int,
    node_j: int,
):
    '''
    ## 定义或修改线弹性连接
    pyosis.boundary.osis_boundary_lelnk

    Args:
        nBd (int): 编号
        eBoundaryType (str): 固定为 LELNK
        b_dx (bool): Dx 自由度，0 = 固定，1 = 弹性
        k_dx (float): Dx 自由度线弹性刚度
        b_dy (bool): Dy 自由度，0 = 固定，1 = 弹性
        k_dy (float): Dy 自由度线弹性刚度
        b_dz (bool): Dz 自由度，0 = 固定，1 = 弹性
        k_dz (float): Dz 自由度线弹性刚度
        b_rx (bool): Rx 自由度，0 = 固定，1 = 弹性
        k_rx (float): Rx 自由度线弹性刚度
        b_ry (bool): Ry 自由度，0 = 固定，1 = 弹性
        k_ry (float): Ry 自由度线弹性刚度
        b_rz (bool): Rz 自由度，0 = 固定，1 = 弹性
        k_rz (float): Rz 自由度线弹性刚度
        b_shear (bool): 0 = 不考虑剪切弹簧位置，1 = 考虑
        s_dy (float | str): y 向剪切弹簧距结束点 I 的距离比；b_shear = 0 时传 "" 占位
        s_dz (float | str): z 向剪切弹簧距结束点 I 的距离比；b_shear = 0 时传 "" 占位
        beta (float): 轴向转角（beta 角）
        node_i (int): 节点 I
        node_j (int): 节点 J

    Notes:
        b_dx、b_dy、b_dz、b_rx、b_ry、b_rz 暂不支持固定，取 1。
        s_dy、s_dz 位于 beta 之前，b_shear = 0 时用 "" 占位而不是 None，
        否则该列消失会把 beta 挤到 s_dy 的位置。

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("Boundary")
def osis_boundary_section_factor(
    nBd: int,
    eBoundaryType: Literal["SECF"],
    Area: float,
    Sy: float,
    Sz: float,
    Ixx: float,
    Iyy: float,
    Izz: float,
    Iww: float,
    W: float,
):
    '''
    ## 修改截面特性
    
    Args:
        nBd (int): 边界编号
        eBoundaryType (str): 固定为 SECF
        Area (float): 面积调整系数
        Sy (float): Y向剪切常数调整系数
        Sz (float): Z向剪切常数调整系数
        Ixx (float): X轴抗扭惯性矩调整系数
        Iyy (float): Y轴抗弯惯性矩调整系数
        Izz (float): Z轴抗弯惯性矩调整系数
        Iww (float): 翘曲惯性矩调整系数
        W (float): 自重调整系数

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("Boundary")
def osis_boundary_soilspring(
    nBd: int,
    e_boundary_type: Literal["SOILSPRING"],
    n_coor: int | str,
    curve_type: int,
    soil_type: Literal["SAND", "CLAY"],
    ground_lv: float,
    d: float,
    gamma: float,
    phi: float | str | None = None,
    k: float | str | None = None,
    su: float | str | None = None,
    e50: float | str | None = None,
    j: float | str | None = None,
):
    '''
    ## 定义或修改土弹簧
    pyosis.boundary.osis_boundary_soilspring

    Args:
        nBd (int): 编号
        e_boundary_type (str): 固定为 SOILSPRING
        n_coor (int | str): 局部坐标系编号，"" 代表缺省（全局坐标系）
        curve_type (int): 土反力曲线类型，1 = API 规范，0 = MIDAS（预留，暂不支持）
        soil_type (str): SAND = 砂土，CLAY = 黏土
        ground_lv (float): 地面标高，埋深 z = ground_lv - 节点标高，仅 z > 0 的节点生成土弹簧
        d (float): 桩直径，必须大于零
        gamma (float): 土的有效重度，必须大于零
        phi (float | str): 内摩擦角（度），仅砂土必填；黏土传 "" 占位
        k (float | str): 初始土模量，仅砂土，可缺省；黏土传 "" 占位
        su (float | str): 不排水抗剪强度，仅黏土必填；砂土留空
        e50 (float | str): 参考应变，仅黏土必填；砂土留空
        j (float | str): 经验系数，仅黏土，可缺省（缺省取 0.5）；砂土留空

    Notes:
        黏土必须保留 phi、k 两个空字段，用 "" 占位；None 会让整列消失，
        后面的 su、e50、j 会错位到前一列。
        尾部 su、e50、j 属缺省参数，可以省略省列。
        砂土的 k 缺省时按 phi 分段线性插值：phi <= 25 度取 5400，30 度取 11000，
        35 度取 22000，phi >= 40 度取 45000，此表固定使用 kN/m³。

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass


@REGISTRY.register("AsgnBd")
def osis_assign_boundary(nBd: int=1, eOP: Literal["a", "s", "r", "aa", "ra"]="a", param: list=[]):
    '''
    ## 分配边界给节点(一般支撑，节点弹性支撑)
    pyosis.boundary.osis_assign_boundary
    
    Args:
        nBd (int): 边界编号
        eOP (str): 操作
            * a = 添加
            * s = 替换
            * r = 移除
            * aa = 添加全部
            * ra = 移除全部
        param (list): 待操作的编号，支持的格式：*，*to*，*by*（仅用于替换）。
            例子：[2,3,5,"8to10"] ["2by3","5by6","8by10"] 重合的编号自动忽略
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("BdGrp")
def osis_boundary_group(strName: str, eOP: Literal["c", "a", "s", "r", "aa", "ra", "m", "d"], *param: str | int):
    '''
    ## 添加或移除边界组
    pyosis.boundary.osis_boundary_group

    Args:
        strName (str): 边界组名
        eOP (str): 操作
            * c = 创建
            * a = 添加
            * s = 替换
            * r = 移除
            * aa = 添加全部
            * ra = 移除全部
            * m = 修改组名
            * d = 删除
        param: 待操作的编号，支持的格式：*, *to*; *by*，仅用于替换。
            例子：[2,3,5,"8to10"] ["2by3","5by6","8by10"] 重合的编号自动忽略

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("BoundaryDel")
def osis_boundary_del(nIndex:int)->tuple[bool, str]:
    """
    删除边界
    Args:
        nIndex: 边界编号

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass