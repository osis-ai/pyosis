"""型钢截面命令。

每种型钢按 UseCatalog 分成两个注册函数：缺省 0 的手动输入分支、缺省 1 的数据库选型分支。
"""

from typing import Literal

from ..core import REGISTRY


# ── 角钢 ──────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_l(
    Index: int,
    Name: str,
    Type: Literal["SteelL"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    tw: float,
    tf: float,
) -> tuple[bool, str]:
    """定义或修改角钢截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelL。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高度。
        B (float): 截面宽度。
        tw (float): 腹板厚度。
        tf (float): 上翼厚度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_l_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelL"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改角钢截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelL。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 槽钢 ──────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_c(
    Index: int,
    Name: str,
    Type: Literal["SteelC"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    tw: float,
    B1: float,
    tf1: float,
    B2: float,
    tf2: float,
    r1: float,
    r2: float,
) -> tuple[bool, str]:
    """定义或修改槽钢截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelC。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高度。
        tw (float): 腹板厚度。
        B1 (float): 上翼宽度。
        tf1 (float): 上翼厚度。
        B2 (float): 下翼宽度。
        tf2 (float): 下翼厚度。
        r1 (float): 上翼圆倒角半径。
        r2 (float): 下翼圆倒角半径。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_c_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelC"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改槽钢截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelC。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 工字型 ────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_i(
    Index: int,
    Name: str,
    Type: Literal["SteelI"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    tw: float,
    B1: float,
    tf1: float,
    B2: float,
    tf2: float,
    r1: float,
    r2: float,
) -> tuple[bool, str]:
    """定义或修改工字型截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelI。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高度。
        tw (float): 腹板厚度。
        B1 (float): 上翼宽度。
        tf1 (float): 上翼厚度。
        B2 (float): 下翼宽度。
        tf2 (float): 下翼厚度。
        r1 (float): 上翼圆倒角半径。
        r2 (float): 下翼圆倒角半径。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_i_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelI"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改工字型截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelI。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── T 型 ──────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_t(
    Index: int,
    Name: str,
    Type: Literal["SteelT"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    tw: float,
    tf: float,
) -> tuple[bool, str]:
    """定义或修改 T 型截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelT。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高度。
        B (float): 翼缘宽度。
        tw (float): 腹板厚度。
        tf (float): 翼缘厚度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_t_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelT"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改 T 型截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelT。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 箱型 ──────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_box(
    Index: int,
    Name: str,
    Type: Literal["SteelBox"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    tw: float,
    tf1: float,
    C: float,
    tf2: float,
) -> tuple[bool, str]:
    """定义或修改箱型截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelBox。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高度。
        B (float): 翼缘宽度。
        tw (float): 腹板厚度。
        tf1 (float): 上翼缘厚度。
        C (float): 腹板间距。
        tf2 (float): 下翼缘厚度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_box_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelBox"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改箱型截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelBox。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 冷轧槽钢 ──────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_cc(
    Index: int,
    Name: str,
    Type: Literal["SteelCC"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    tw: float,
    r: float,
    d: float,
) -> tuple[bool, str]:
    """定义或修改冷轧槽钢截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelCC。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高度。
        B (float): 翼缘宽度。
        tw (float): 腹板厚度。
        r (float): 半径。
        d (float): 卷边高度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_cc_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelCC"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改冷轧槽钢截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelCC。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 管型 ──────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_circular_hollow(
    Index: int,
    Name: str,
    Type: Literal["SteelCircularHollow"],
    UseCatalog: Literal[0] = 0,
    *,
    D: float,
    Tw: float,
) -> tuple[bool, str]:
    """定义或修改管型截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelCircularHollow。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        D (float): 直径。
        Tw (float): 壁厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_circular_hollow_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelCircularHollow"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改管型截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelCircularHollow。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── Z 型 ──────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_z(
    Index: int,
    Name: str,
    Type: Literal["SteelZ"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    Tw: float,
    R: float,
    D: float,
    Th: float,
) -> tuple[bool, str]:
    """定义或修改 Z 型截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelZ。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高度。
        B (float): 顶部宽度。
        Tw (float): 厚度。
        R (float): 内径。
        D (float): 伸出段长度。
        Th (float): 伸出段角度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_z_catalog(
    Index: int,
    Name: str,
    Type: Literal["SteelZ"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改 Z 型截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 SteelZ。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 双角钢 ────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_angle_1(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleAngle1"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    Tf1: float,
    Tf2: float,
    C: float,
) -> tuple[bool, str]:
    """定义或修改双角钢截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleAngle1。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高。
        B (float): 截面宽。
        Tf1 (float): 肢 1 厚度。
        Tf2 (float): 肢 2 厚度。
        C (float): 间隙。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_angle_1_catalog(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleAngle1"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改双角钢截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleAngle1。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Note:
        间隙 C 固定为 0，无需输入。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 交叉角钢 ──────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_angle_2(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleAngle2"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    Tf1: float,
    Tf2: float,
    C: float,
) -> tuple[bool, str]:
    """定义或修改交叉角钢截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleAngle2。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高。
        B (float): 截面宽。
        Tf1 (float): 肢 1 厚度。
        Tf2 (float): 肢 2 厚度。
        C (float): 间隙。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_angle_2_catalog(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleAngle2"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
    C: float,
) -> tuple[bool, str]:
    """定义或修改交叉角钢截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleAngle2。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。
        C (float): 间隙。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 双槽钢 ────────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_c(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleC"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    Tw: float,
    Tf: float,
    C: float,
) -> tuple[bool, str]:
    """定义或修改双槽钢截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleC。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高。
        B (float): 截面宽。
        Tw (float): 腹板厚度。
        Tf (float): 翼缘厚度。
        C (float): 间隙。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_c_catalog(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleC"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
) -> tuple[bool, str]:
    """定义或修改双槽钢截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleC。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。

    Note:
        间隙 C 固定为 0，无需输入。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 双 H 型钢 ─────────────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_h(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleH"],
    UseCatalog: Literal[0] = 0,
    *,
    H1: float,
    B1: float,
    Tw1: float,
    Tf1: float,
    H2: float,
    B2: float,
    Tw2: float,
    Tf2: float,
) -> tuple[bool, str]:
    """定义或修改双 H 型钢截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleH。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H1 (float): 截面 1 高。
        B1 (float): 截面 1 宽。
        Tw1 (float): 腹板 1 厚度。
        Tf1 (float): 翼缘 1 厚度。
        H2 (float): 截面 2 高。
        B2 (float): 截面 2 宽。
        Tw2 (float): 腹板 2 厚度。
        Tf2 (float): 翼缘 2 厚度。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_h_catalog(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleH"],
    UseCatalog: Literal[1] = 1,
    *,
    Code1: str,
    Designation1: str,
    Code2: str,
    Designation2: str,
) -> tuple[bool, str]:
    """定义或修改双 H 型钢截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleH。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code1 (str): 规范 1 名称。
        Designation1 (str): 型钢型号 1。
        Code2 (str): 规范 2 名称。
        Designation2 (str): 型钢型号 2。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 双槽钢+腹板截面1 ──────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_cweb_1(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleCWeb1"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    Tw: float,
    Tf: float,
    Bs: float,
    Ts: float,
) -> tuple[bool, str]:
    """定义或修改双槽钢+腹板截面1（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleCWeb1。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高。
        B (float): 截面宽。
        Tw (float): 腹板厚。
        Tf (float): 翼缘厚。
        Bs (float): 连接板宽。
        Ts (float): 连接板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_cweb_1_catalog(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleCWeb1"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
    Bs: float,
    Ts: float,
) -> tuple[bool, str]:
    """定义或修改双槽钢+腹板截面1（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleCWeb1。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。
        Bs (float): 连接板宽。
        Ts (float): 连接板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── 双槽钢+腹板截面2 ──────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_cweb_2(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleCWeb2"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    Tw: float,
    Tf: float,
    Bs: float,
    Ts: float,
) -> tuple[bool, str]:
    """定义或修改双槽钢+腹板截面2（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleCWeb2。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高。
        B (float): 截面宽。
        Tw (float): 腹板厚。
        Tf (float): 翼缘厚。
        Bs (float): 连接板宽。
        Ts (float): 连接板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_double_cweb_2_catalog(
    Index: int,
    Name: str,
    Type: Literal["BUDoubleCWeb2"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
    Bs: float,
    Ts: float,
) -> tuple[bool, str]:
    """定义或修改双槽钢+腹板截面2（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUDoubleCWeb2。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。
        Bs (float): 连接板宽。
        Ts (float): 连接板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


# ── H 型钢+双板截面 ───────────────────────────────────


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_h_with_plates(
    Index: int,
    Name: str,
    Type: Literal["BUHWithPlates"],
    UseCatalog: Literal[0] = 0,
    *,
    H: float,
    B: float,
    Tw: float,
    Tf: float,
    C: float,
    Ts: float,
) -> tuple[bool, str]:
    """定义或修改 H 型钢+双板截面（手动输入参数）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUHWithPlates。
        UseCatalog (int): 固定为 0，用户手动输入参数。
        H (float): 截面高。
        B (float): 截面宽。
        Tw (float): 腹板厚。
        Tf (float): 翼缘厚。
        C (float): 板中心距。
        Ts (float): 板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass


@REGISTRY.register("Section")
def osis_section_shaped_steel_bu_h_with_plates_catalog(
    Index: int,
    Name: str,
    Type: Literal["BUHWithPlates"],
    UseCatalog: Literal[1] = 1,
    *,
    Code: str,
    Designation: str,
    C: float,
    Ts: float,
) -> tuple[bool, str]:
    """定义或修改 H 型钢+双板截面（数据库选型）。

    Args:
        Index (int): 编号。
        Name (str): 截面名。
        Type (str): 截面类型，固定为 BUHWithPlates。
        UseCatalog (int): 固定为 1，采用数据库选钢。
        Code (str): 规范名称（GB_YB / GB_YB05 / GB50018_02）。
        Designation (str): 型钢型号。
        C (float): 板中心距。
        Ts (float): 板厚。

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass
