from typing import Any, Dict, Literal, List, Union, Sequence
from ..core import REGISTRY, osis_run
from ..core.client import DEFAULT_SOLVE_TIMEOUT, osis_client

def osis_matrix(matrix_name: str, matrix_data: Union[List, int, float, str]):
    """
    将Python多维列表转换为OSIS DSL格式的矩阵定义和赋值语句。适用于自定义截面函数osis_section_custom、osis_section_steel_custom所需的坐标参数矩阵输入。
    
    Args:
        matrix_name: OSIS中的矩阵变量名
        matrix_data: 任意维度的列表（1维/2维/3维/...）或单个数值（0维）
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    
    Example:
        >>> # 2维矩阵示例
        >>> matrix_2d = [[1, 2, 20], [2, 3, 25], [3, 4, 30], [4, 1, 25]]
        >>> osis_matrix("LineMatrix", matrix_2d)
        >>> # 3维矩阵示例
        >>> matrix_3d = [[[1.5, 2.5], [3.5, 4.5]], [[5.5, 6.5], [7.5, 8.5]]]
        >>> osis_matrix("CubeMatrix", matrix_3d)
        >>> # 1维矩阵示例
        >>> matrix_1d = [10, 20, 30, 40]
        >>> osis_matrix("VectorMatrix", matrix_1d)
        >>> # 0维矩阵示例
        >>> matrix_0d = 10
        >>> osis_matrix("ScalarMatrix", matrix_0d)
    """
    # 存储所有生成的命令
    all_cmds = []
    
    # 验证和获取矩阵维度信息
    def get_dimensions_and_validate(data: Any) -> List[int]:
        """递归获取矩阵维度并验证是否规则"""
        dimensions = []
        current = data
        
        # 递归获取维度
        while isinstance(current, list):
            if not current:
                dimensions.append(0)
                break
            dimensions.append(len(current))
            # 检查当前维度下所有元素的子维度是否一致
            first_sub_dim = get_dimensions_and_validate(current[0]) if isinstance(current[0], list) else []
            for elem in current[1:]:
                elem_sub_dim = get_dimensions_and_validate(elem) if isinstance(elem, list) else []
                if elem_sub_dim != first_sub_dim:
                    raise ValueError(f"矩阵维度不规则：元素维度不一致，第一个元素维度={first_sub_dim}，当前元素维度={elem_sub_dim}")
            current = current[0]
        
        # 处理0维（单个数值）
        if not dimensions:
            return [1]  # 0维视为1x1矩阵
        
        return dimensions
    
    # 获取维度信息
    try:
        dims = get_dimensions_and_validate(matrix_data)
        # matrix_data = [matrix_data]
    except Exception as e:
        raise ValueError(f"矩阵验证失败：{str(e)}") from e
    
    # 处理空矩阵
    if any(d == 0 for d in dims):
        raise ValueError("不支持空矩阵输入")
    # 字符数组用 charn（与 *dim 参数格式不同）；数值数组 OSIS 固定为三维 I,J,K（不足补 1）
    is_charn = (
            (isinstance(matrix_data, list) and len(matrix_data) > 0 and isinstance(matrix_data[0], str))
            or isinstance(matrix_data, str)
    )
    if is_charn:
        dim_str = ",".join(map(str, dims))
        dim_cmd = f"charn,{matrix_name},{dim_str}"
    else:
        if len(dims) > 3:
            raise ValueError(f"OSIS 数值数组最多三维，当前 shape={dims}")
        dims_osi = list(dims)
        while len(dims_osi) < 3:
            dims_osi.append(1)
        dim_str = ",".join(map(str, dims_osi))
        dim_cmd = f"*dim,{matrix_name},{dim_str}"
    all_cmds.append(dim_cmd)
    
    # 递归生成赋值语句
    def generate_assignments(data: Any, indices: List):
        """递归遍历矩阵并生成赋值语句"""
        if isinstance(data, list):
            for idx, elem in enumerate(data):
                new_indices = indices + [idx]
                generate_assignments(elem, new_indices)
        else:
            value = data
            if isinstance(value, (int, float)):
                val_str = str(value)
            else:
                val_str = f"\"{value}\""
            idx_parts = list(indices)
            if not is_charn:
                while len(idx_parts) < 3:
                    idx_parts.append(0)
            idx_str = ",".join(map(str, idx_parts))
            assign_cmd = f"{matrix_name}[{idx_str}] = {val_str}"
            all_cmds.append(assign_cmd)

    generate_assignments(matrix_data, [])

    str_cmds = ";".join(all_cmds)
    return osis_run(str_cmds, "exec")

def output_result_for_calc_book():
    return osis_client("OutputResultForCalcBook", {})


@REGISTRY.register("Replot")
def osis_replot():
    """
    重新绘制窗口
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("Clear")
def osis_clear():
    """
    清空项目
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

@REGISTRY.register("Clc")
def osis_clc():
    """
    清屏
    
    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    pass

def osis_solve(timeout: float | None = None):
    """
    求解工程

    Args:
        timeout: HTTP 超时秒数，默认 600（10 分钟）

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    return osis_run(
        "Solve;",
        "exec",
        timeout=timeout if timeout is not None else DEFAULT_SOLVE_TIMEOUT,
    )
