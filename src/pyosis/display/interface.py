"""显示控制命令接口

控制边界、荷载、钢束显隐，以及视图方向、显示开关等。
"""

from typing import Literal, Sequence, Union

from ..core import REGISTRY


@REGISTRY.register("DispCtrl")
def osis_disp_ctrl(
    eObject: Literal["bc", "boundary", "lg", "load", "td", "tendon"],
    eType: str,
    ids: Union[str, int, Sequence[Union[str, int]]],
    bShow: Literal[0, 1] = 1,
):
    """控制边界 / 荷载 / 钢束的显示与隐藏。

    格式: ``dispctrl,<Object>,<Type>,<Number/Name...>,<0|1>``

    Args:
        eObject (str): 对象类型
            * ``bc`` / ``boundary`` = 边界
            * ``lg`` / ``load`` = 荷载
            * ``td`` / ``tendon`` = 钢束
        eType (str): 子类型
            * 边界: ``all``, ``general``, ``mstslv``, ``release``, ``elstcspt``,
              ``generalelstcspt``, ``rigid``, ``secfactor``
            * 荷载: ``all``, ``gravity``, ``nforce``, ``line``, ``pointforce``,
              ``pointmoment``, ``displacement``, ``initial``, ``utemp``, ``gtemp``,
              ``pst``, ``cforce``, ``elementsurface``
            * 钢束: 通常为 ``all``
        ids: 编号或名称
            * ``all`` = 全部
            * 单个编号 / 名称，或多个组成的序列（如 ``[1, 2, "3to10"]``、``["T1", "T2"]``）
        bShow (int): ``0`` = 隐藏，``1`` = 显示

    Returns:
        tuple (bool, str): 是否成功，失败原因

    Examples:
        >>> # 显示全部边界
        >>> osis_disp_ctrl("bc", "all", "all", 1)
        >>> # 显示一般边界 1、2、3to10
        >>> osis_disp_ctrl("bc", "general", [1, 2, "3to10"], 1)
        >>> # 显示全部节点力荷载
        >>> osis_disp_ctrl("lg", "nforce", "all", 1)
        >>> # 显示名为 DeadLoad 的荷载
        >>> osis_disp_ctrl("lg", "all", "DeadLoad", 1)
        >>> # 隐藏钢束 1、2、3to10
        >>> osis_disp_ctrl("td", "all", [1, 2, "3to10"], 0)
        >>> # 显示钢束 T1、T2
        >>> osis_disp_ctrl("td", "all", ["T1", "T2"], 1)
    """
    pass


@REGISTRY.register("/control")
def osis_control(
    eAction: str,
    eArg: str | None = None,
    *dValues = None
):
    """视图 / 界面控制命令。

    格式: ``/control,<Action>[,<Arg>]``

    Args:
        eAction (str): 子命令
            * ``view`` = 切换视图方向（配合 eArg）
            * 其他如 ``quickCreateModel`` 等
        eArg (str | None): 子命令参数
            * 当 eAction 为 ``view`` 时: ``standard`` / ``top`` / ``right`` / ``front`` / ``zoom`` / ``move``
        dValues (unknown): 附加参数

    Returns:
        tuple (bool, str): 是否成功，失败原因

    Examples:
        >>> osis_control("view", "standard")
        >>> osis_control("view", "top")
        >>> osis_control("view", "right")
        >>> osis_control("view", "front")
        >>> osis_control("view", "zoom", 0.8)
    """
    pass


@REGISTRY.register("Plsm")
def osis_plsm(bFlag: Literal[0, 1] = 1):
    """显示开关（Plsm）。

    格式: ``plsm,<0|1>``

    Args:
        bFlag (int): ``0`` = 关，``1`` = 开

    Returns:
        tuple (bool, str): 是否成功，失败原因

    Examples:
        >>> osis_plsm(1)
        >>> osis_plsm(0)
    """
    pass

@REGISTRY.register("jpeg")
def osis_jpeg(path: str = "image"):
    """截图工具。

    格式: ``jpeg,path``

    Args:
        path (str): 图片保存名字，将保存到 `{path}.jpg`

    Returns:
        tuple (bool, str): 是否成功，失败原因

    Examples:
        >>> osis_jepg("IMG_盖梁裂缝宽度计算结果图")
    """
    pass
