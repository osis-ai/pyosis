"""
Interfaces of OSIS functions

========

静力荷载相关

"""


from typing import Literal
from ..core import REGISTRY


# @REGISTRY.register("Load")
# def osis_load(eLoadType: Literal["GRAVITY", "NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"], strLCName: str, params: Dict[str, Any]):
#     '''
#     创建荷载
    
#     Args:
#         eLoadType (str): 荷载类型，不区分大小写。 GRAVITY = 自重荷载，NFORCE = 节点荷载，LINE = 线荷载，DISPLACEMENT = 强迫位移，INITIAL = 初始内力，
#             UTEMP = 均匀温度荷载，GTEMP = 梯度温度荷载， PST = 预应力，CFORCE = 索力
#         strLCName (str): 工况名称
#         params (Dict[str, Any]): 对应荷载类型所需要的参数
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     pass

@REGISTRY.register("Load")
def osis_load_gravity(eType: str="GRAVITY", strLCName: str="自定义工况1", dXCoeff: float=1.0, dYCoeff: float=1.0, dZCoeff: float=1.0):
    '''
    创建或修改自重荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 GRAVITY
        strLCName (str): 荷载工况名称
        nEntity (int): 节点编号
        dXCoeff (float): 全局坐标系x方向的系数，将作用于重力加速度
        dYCoeff (float): 全局坐标系y方向的系数，将作用于重力加速度
        dZCoeff (float): 全局坐标系z方向的系数，将作用于重力加速度
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_nforce(eType: str="NFORCE", strLCName: str="自定义工况1", nEntity: int=1, dFx: float=100, dFy: float=0, dFz: float=0, dMx: float=0, dMy: float=0, dMz: float=0):
    '''
    创建或修改节点荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 NFORCE
        strLCName (str): 荷载工况名称
        nEntity (int): 节点编号
        dFx (float): 全局坐标系x方向的集中力
        dFy (float): 全局坐标系y方向的集中力
        dFz (float): 全局坐标系z方向的集中力
        dMx (float): 全局坐标系x方向的集中弯矩
        dMy (float): 全局坐标系y方向的集中弯矩
        dMz (float): 全局坐标系z方向的集中弯矩
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_line(eType: Literal['LINE'], strLCName: str, nEntity: int, eCoordSystem: Literal[0, 1], eLoadType: Literal[0, 1], 
                   dOffsetXI: float=0, dOffsetYI: float=0, dOffsetZI: float=0, dFXI: float=100, dFYI: float=100, dFZI: float=0, dMXI: float=0, dMYI: float=0, dMZI: float=0,
                   dOffsetXJ: float=0, dOffsetYJ: float=0, dOffsetZJ: float=0, dFXJ: float=100, dFYJ: float=100, dFZJ: float=0, dMXJ: float=0, dMYJ: float=0, dMZJ: float=0):
    '''
    创建或修改任意线荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 LINE
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eCoordSystem (int): 
            * 0-单元坐标系
            * 1-整体坐标系
        eLoadType (int):
            * 0-连续荷载
            * 1-离散荷载
        dOffsetXI (float):  I端偏移量X/L，输入范围[0,1]
        dOffsetYI (float):  I端Y轴偏移量
        dOffsetZI (float):  I端Z轴偏移量
        dFXI (float): I端坐标系x方向的集中力
        dFYI (float): I端坐标系y方向的集中力
        dFZI (float): I端坐标系z方向的集中力
        dMXI (float): I端坐标系x方向的集中弯矩
        dMYI (float): I端坐标系y方向的集中弯矩
        dMZI (float): I端坐标系z方向的集中弯矩
        dOffsetXJ (float):  J端偏移量X/L，输入范围[0,1]
        dOffsetYJ (float):  J端Y轴偏移量
        dOffsetZJ (float):  J端Z轴偏移量
        dFXJ (float): J端坐标系x方向的集中力
        dFYJ (float): J端坐标系y方向的集中力
        dFZJ (float): J端坐标系z方向的集中力
        dMXJ (float): J端坐标系x方向的集中弯矩
        dMYJ (float): J端坐标系y方向的集中弯矩
        dMZJ (float): J端坐标系z方向的集中弯矩
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_concentrated(eType: Literal['PTF', 'PTM'], strLCName: str, nEntity: int,
                           eCoordSystem: Literal[0, 1], nLoadRange: Literal[1, 2, 3, 4, 5],
                           params: list):
    '''
    创建或修改任意节间集中力/力矩

    Args:
        eType (str): 荷载类型，不区分大小写。PTF = 集中力，PTM = 集中力矩
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eCoordSystem (int): 
            * 0-单元坐标系
            * 1-整体坐标系
        nLoadRange (int): 力/力矩组数，1~5
        params (list): 各组力/力矩参数，按顺序填入：
            [offsetX1, offsetY1, offsetZ1, Px1, Py1, Pz1, offsetX2, offsetY2, offsetZ2, Px2, Py2, Pz2, ...]
            每组包含6个参数：偏移量X/L, Y轴偏移量, Z轴偏移量, x方向力/力矩, y方向力/力矩, z方向力/力矩
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_surface_load(eType: str, strLc: str, strEntity: str, strPlanei:str, strDir:str, strGlobalI:Literal["0","1","2"], strP1i:str, strP2i:str,strP3i:str,strP4i:str) -> tuple[bool, str]:
    """
    创建或修改单元面荷载，不考虑边中节点荷载插值

    Args:
        eType (str): 荷载类型，Type = ESRFC
        strLc (str): 荷载工况名称
        strEntity (str): 单元编号
        strPlanei (str): 面位置，板壳单元默认输入1，实体单元输入1,2,3,4,5,6
        strDir (str):方向，X,Y,Z
        strGlobalI (str):
            * 0 = 局部
            * 1 = 整体
            * 2 = 整体 + 投影
        strP1i (str): 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
        strP2i (str): 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
        strP3i (str): 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
        strP4i (str): 对应Plane_i的角节点荷载值，量纲为M L^-1 T^-2
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因
    """
    pass

@REGISTRY.register("Load")
def osis_load_surface_load_vector(eType: str, strLc: str, strEntity: str, strPlanei: str, strDir: str, strXi: str, strYi: str, strZi: str, strP1i: str, strP2i: str, strP3i: str, strP4i: str) -> tuple[bool, str]:
    """
    创建或修改单元面荷载（方向向量定义），不考虑边中节点荷载插值

    Args:
        eType: (str): 荷载类型，默认为 ESRFC
        strLc (str): 荷载工况名称
        strEntity (str): 单元编号
        strPlanei (str): 面位置，板壳单元默认输入1，实体单元输入1,2,3,4,5,6
        strDir (str):方向，默认为 VECTOR
        strXi (str): VECTOR的具体值
        strYi (str): VECTOR的具体值
        strZi (str): VECTOR的具体值
        strP1i (str): 对应Planei的角节点荷载值，量纲为M L^-1 T^-2
        strP2i (str): 对应Planei的角节点荷载值，量纲为M L^-1 T^-2
        strP3i (str): 对应Planei的角节点荷载值，量纲为M L^-1 T^-2
        strP4i (str): 对应Planei的角节点荷载值，量纲为M L^-1 T^-2

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因
    """
    pass

@REGISTRY.register("Load")
def osis_load_displacement(
    eType: str = "DISPLACEMENT",
    strLCName: str = "自定义工况1",
    nEntity: int = 1,
    bX:int = 1,
    Dx: float = 0.0,
    bY: int = 0,
    Dy: float = 0.0,
    bZ: int = 0,
    Dz: float = 0.0,
    bRx: int = 0,
    Rx: float = 0.0,
    bRy: int = 0,
    Ry: float = 0.0,
    bRz: int = 0,
    Rz: float = 0.0,
):
    '''
    创建或修改强迫位移

    Args:
        Type：荷载类型，固定为 DISPLACEMENT
        strLCName (str): 荷载工况名称
        nEntity：节点编号
        bX：UX方向，0 = 自由，1 = 强迫位移
        Dx：强制位移在坐标系x方向的分量
        bY：UY方向，0 = 自由，1 = 强迫位移
        Dy：强制位移在坐标系y方向的分量
        bZ：UZ方向，0 = 自由，1 = 强迫位移
        Dz：强制位移在坐标系z方向的分量
        bRx：RX方向，0 = 自由，1 = 强迫位移
        Rx：绕坐标系x轴的强制旋转角度分量
        bRy：RY方向，0 = 自由，1 = 强迫位移
        Ry：绕坐标系y轴的强制旋转角度分量
        bRz：RZ方向，0 = 自由，1 = 强迫位移
        Rz：绕坐标系z轴的强制旋转角度分量

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass
@REGISTRY.register("Load")
def osis_load_initial(
    eType: str = "INITIAL",
    strLCName: str = "自定义工况1",
    nEntity: int = 1,
    dFXI: float = 100,
    dFYI: float = 100,
    dFZI: float = 0,
    dMXI: float = 0,
    dMYI: float = 0,
    dMZI: float = 0,
    dFXJ: float = 0,
    dFYJ: float = 0,
    dFZJ: float = 0,
    dMXJ: float = 0,
    dMYJ: float = 0,
    dMZJ: float = 0,
):
    '''
    创建或修改初始内力

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 INITIAL
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        dFXI, dFYI, dFZI: I 端局部坐标系 x/y/z 向轴力
        dMXI, dMYI, dMZI: I 端绕 x/y/z 弯矩
        dFXJ, dFYJ, dFZJ: J 端局部坐标系 x/y/z 向轴力
        dMXJ, dMYJ, dMZJ: J 端绕 x/y/z 弯矩
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass
# @REGISTRY.register("Load")
# def osis_load_initial(eType: str="INITIAL", strLCName: str="自定义工况1", nEntity: int=1, dFXI: float=100, dFYI: float=100, dFZI: float=0, dMXI: float=0, dMYI: float=0, dMZI: float=0):
#     '''
#     创建或修改任初始内力
#
#     Args:
#         eType (str): 荷载类型，不区分大小写。固定为 LINE
#         strLCName (str): 荷载工况名称
#         nEntity (int): 单元编号
#         dFXI (float): I端坐标系x方向的集中力
#         dFYI (float): I端坐标系y方向的集中力
#         dFZI (float): I端坐标系z方向的集中力
#         dMXI (float): I端坐标系x方向的集中弯矩
#         dMYI (float): I端坐标系y方向的集中弯矩
#         dMZI (float): I端坐标系z方向的集中弯矩
#     Returns:
#         tuple (bool, str): 是否成功，失败原因
#     '''
#     pass

@REGISTRY.register("Load")
def osis_load_utemp(eType: str="UTEMP", strLCName: str="自定义工况1", nEntity: int=1, eDirect: Literal["X", "Y", "Z"]="X", dTemp: float=1.0, dLength: float=None):
    '''
    创建或修改均匀温度荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 UTEMP
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eDirect (str): 作用方向。单元坐标系X（轴向）/Y/Z方向温差，均匀升降温数值（正为升温）
            * X: 可用来模拟整体升降温荷载
            * Y: 可以用来模拟单元的横向梯度温度荷载
            * Z: 可以用来模拟单元的横向梯度温度荷载
        dTemp (float): 温差值，不影响系统温度
        dLength (float): Y/Z方向的长度，为 "" 则自动通过截面计算
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_gtemp(eType: str="GTEMP", strLCName: str="自定义工况1", nEntity: int=1, eDirect: Literal["Y", "Z"]="Y", eGTempType: Literal["R", "T", "C", "B"]="R", nNum: int=1, param: list=["", 10, 10, 0, 0]):
    '''
    创建或修改梯度温度荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 GTEMP
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eDirect (str): 局部方向
            * Y
            * Z
        eGTempType (str): 定义梁的参考位置
            * R
            * T
            * C
            * B
        nNum (int): 梯度温度荷载段数
        param (list): 每个梯度温度荷载段对应一组参数，多组参数直接全部按顺序填入param中即可
            - B (float): 考虑温度变化的宽度，宽度可设置为空("")
            - H1 (float): 参考位置至定义温度间距离
            - T1 (float): H1处对应温度
            - H2 (float): 参考位置至定义温度间距离
            - T2 (float): H2处对应温度
    Returns:
        tuple (bool, str): 是否成功，失败原因

    Notes:
        R：从梁截面建模位置到温度变化点的距离
        T：从梁顶到温度变化点的距离
        C：从截面中心到温度变化点的距离
        B：从梁底到温度变化点的距离
    '''
    pass

@REGISTRY.register("Load")
def osis_load_pst(eType: str="PST", strLCName: str="自定义工况1", strEntity: str="钢束1", eTensionType: Literal["BOTH", "BEG", "END"]="BOTH", eTensionForceType: Literal["ST", "IF"]="ST", dBeg: float=100, dEnd: float=100):
    '''
    创建或修改预应力荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 PST
        strLCName (str): 荷载工况名称
        strEntity (str): 钢束形状名称，由TdShape定义
        eTensionType (str): 张拉类型
            * BOTH = 两端张拉
            * BEG = 起点张拉
            * END = 终点张拉
        eTensionForceType (str): 张拉力类型
            * ST = 应力
            * IF = 内力
        dBeg (float): 起点应力或内力。eTensionType 为 END 填 None
        dEnd (float): 终点应力或内力。eTensionType 为 BEG 填 None
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_cforce(eType: str="CFORCE", strLCName: str="自定义工况1", nEntity: int=1, eLoadType: Literal["IN", "EX"]="IN", dForce: float=100):
    '''
    创建或修改索力

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 CFORCE
        strLCName (str): 荷载工况名称
        nEntity (int): 单元编号
        eLoadType (str): 施加方式
            * In = 体内力
            * Ex = 体外力
        dForce (float): 索力数值
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("PlanarLoad")
def osis_planar_load_point(strName: str="平面荷载1", strDescription: str="", eType: Literal["Point"]="Point", points: list=None):
    '''
    创建或修改平面荷载（集中荷载）

    Args:
        strName (str): 荷载名称
        strDescription (str): 荷载说明
        eType (str): 荷载类型，不区分大小写。固定为 Point = 集中荷载
        points (list): 集中荷载的坐标与数值，按顺序平铺填入：
            [x1, y1, F1, x2, y2, F2, ...]
            每组包含3个参数：x坐标, y坐标, 荷载数值，组数不限
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("PlanarLoad")
def osis_planar_load_line(strName: str="平面荷载1", strDescription: str="", eType: Literal["Line"]="Line",
                          bUniform: Literal[0, 1]=1, bForceType: Literal[0, 1]=1,
                          dX1: float=0.0, dY1: float=0.0, dF1: float=100,
                          dX2: float=1.0, dY2: float=0.0, dF2: float=100):
    '''
    创建或修改平面荷载（线荷载）

    Args:
        strName (str): 荷载名称
        strDescription (str): 荷载说明
        eType (str): 荷载类型，不区分大小写。固定为 Line = 线荷载
        bUniform (int): 1 = 均布荷载，0 = 非均布荷载
        bForceType (int): 1 = 力，0 = 弯矩
        dX1 (float): 线荷载起点的x坐标
        dY1 (float): 线荷载起点的y坐标
        dF1 (float): 线荷载起点的荷载数值
        dX2 (float): 线荷载终点的x坐标
        dY2 (float): 线荷载终点的y坐标
        dF2 (float): 线荷载终点的荷载数值
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("PlanarLoad")
def osis_planar_load_area(strName: str="平面荷载1", strDescription: str="", eType: Literal["Area"]="Area",
                          bUniform: Literal[0, 1]=1, nPointNum: Literal[3, 4]=3, points: list=None):
    '''
    创建或修改平面荷载（面荷载）

    Args:
        strName (str): 荷载名称
        strDescription (str): 荷载说明
        eType (str): 荷载类型，不区分大小写。固定为 Area = 面荷载
        bUniform (int): 1 = 均布荷载，0 = 非均布荷载
        nPointNum (int): 点数，3 = 3点，4 = 4点，其他输入非法
        points (list): 面荷载各点处的坐标与数值，按顺序平铺填入：
            [x1, y1, F1, x2, y2, F2, x3, y3, F3]（nPointNum = 3）
            [x1, y1, F1, x2, y2, F2, x3, y3, F3, x4, y4, F4]（nPointNum = 4）
            每组包含3个参数：x坐标, y坐标, 荷载数值
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("PlanarLoadCopy")
def osis_planar_load_copy(strName: str="平面荷载1", eDir: Literal["X", "Y"]="X", copies: list=None):
    '''
    复制平面荷载

    Args:
        strName (str): 荷载名称
        eDir (str): 复制方向
            * X
            * Y
        copies (list): 复制的次数与距离，按顺序平铺填入：
            [CopyCount1, CopyDistance1, ..., CopyCountN, CopyDistanceN]
            每组包含2个参数：复制的次数, 复制的距离
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("Load")
def osis_load_plane(eType: Literal["Plane"]="Plane", strLCName: str="自定义工况1", strPlanarLoadName: str="平面荷载1",
                    strElemType: str="",
                    dP1x: float=0.0, dP1y: float=0.0, dP1z: float=0.0,
                    dP2x: float=1.0, dP2y: float=0.0, dP2z: float=0.0,
                    dP3x: float=0.0, dP3y: float=1.0, dP3z: float=0.0,
                    dTolerance: float=0.0,
                    bLoadPosition: Literal[0, 1]=1, strElemGroup: str="", strLoadSurface: str="",
                    eDir: Literal["SurfaceN", "ElementN", "GlobalX", "GlobalY", "GlobalZ"]="SurfaceN",
                    eProjectionOp: Literal["NoProjection", "LoadDir", "LoadPlane"]="NoProjection",
                    bCopyOp: Literal[0, 1]=0, eCopyDir: str="", copies: list=None):
    '''
    布置平面荷载

    Args:
        eType (str): 荷载类型，不区分大小写。固定为 Plane = 平面荷载
        strLCName (str): 荷载工况名称
        strPlanarLoadName (str): 定义的平面荷载名称，由 PlanarLoad 定义
        strElemType (str): 要加载平面荷载的单元类型
        dP1x/dP1y/dP1z (float): 加载平面原点P1在整体坐标系中的坐标
        dP2x/dP2y/dP2z (float): 平面坐标系x轴上的任意点P2在整体坐标系中的坐标
        dP3x/dP3y/dP3z (float): 平面坐标系x-y平面上任意点P3在整体坐标系中的坐标
        dTolerance (float): 决定平面坐标系坐标的容许误差
        bLoadPosition (int): 加载对象
            * 1 = 加载平面上的单元
            * 0 = 单元组
        strElemGroup (str): 单元组名称，bLoadPosition = 0 时有效，无效时填 ""
        strLoadSurface (str): 实体单元加载面（1~6），平面单元无用，填 ""
        eDir (str): 平面荷载加载方向
            * SurfaceN = 法向（加载平面）
            * ElementN = 法向（单元）
            * GlobalX = 整体坐标系X
            * GlobalY = 整体坐标系Y
            * GlobalZ = 整体坐标系Z
        eProjectionOp (str): 投影选项
            * NoProjection = 不投影
            * LoadDir = 荷载方向
            * LoadPlane = 加载平面
        bCopyOp (int): 是否根据输入间距将平面荷载以相同大小复制到其他区域
            * 1 = 复制
            * 0 = 不复制
        eCopyDir (str): 复制方向，X、Y、Z。bCopyOp = 0 时填 ""
        copies (list): 复制的次数与距离，按顺序平铺填入：
            [CopyCount1, CopyDistance1, ..., CopyCountN, CopyDistanceN]
            每组包含2个参数：复制的次数, 复制的距离
    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LoadDel")
def osis_load_del(eType: Literal["GRAVITY", "NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"]="NFORCE", strLCName: str="自定义工况1", entity: int|str=1):
    '''
    删除荷载

    Args:
        eType (str): 荷载类型，不区分大小写
            * GRAVITY = 自重荷载
            * NFORCE = 节点荷载
            * LINE = 线荷载
            * DISPLACEMENT = 强迫位移荷载
            * INITIAL = 初始内力荷载
            * UTEMP = 均匀温度荷载
            * GTEMP = 梯度温度荷载
            * PST = 预应力荷载
            * CFORCE = 索力荷载
        strLCName (str): 荷载工况名称
        entity (int|str): 要删除的荷载所作用的节点/单元/钢束形状。eType 为 GRAVITY 时需要填 None

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

@REGISTRY.register("LoadMod")
def osis_load_mod(eType: Literal["NFORCE", "LINE", "DISPLACEMENT", "INITIAL", "UTEMP", "GTEMP", "PST", "CFORCE"]="NFORCE", strLCName: str="自定义工况1", oldEntity: int|str=1, newEntity: int|str=2):
    '''
    修改工况内荷载作用的单元或节点或钢束形状

    Args:
        eType (str): 荷载类型，不区分大小写
            * NFORCE = 节点荷载
            * LINE = 线荷载
            * DISPLACEMENT = 强迫位移荷载
            * INITIAL = 初始内力荷载
            * UTEMP = 均匀温度荷载
            * GTEMP = 梯度温度荷载
            * PST = 预应力荷载
            * CFORCE = 索力荷载
        strLCName (str): 荷载工况名称
        oldEntity (int|str): 旧编号
        newEntity (int|str): 新编号

    Returns:
        tuple (bool, str): 是否成功，失败原因
    '''
    pass

