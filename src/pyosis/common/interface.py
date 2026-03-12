from typing import Any, Dict, Literal, List, Union, Sequence
from ..core import REGISTRY, osis_run
from ..core.command import _log

def osis_matrix(matrix_name: str, matrix_data: Union[List, int, float, str]):
    """
    将Python多维列表转换为OSIS DSL格式的矩阵定义和赋值语句。适用于自定义截面函数osis_section_custom、osis_section_steel_custom所需的坐标参数矩阵输入。
    
    Args:
        matrix_name: OSIS中的矩阵变量名
        matrix_data: 任意维度的列表（1维/2维/3维/...）或单个数值（0维）
    
    Returns:
        OSIS DSL格式的字符串（拼接后的完整命令）
    
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
        matrix_data = [matrix_data]
    except Exception as e:
        raise ValueError(f"矩阵验证失败：{str(e)}") from e
    
    # 处理空矩阵
    if any(d == 0 for d in dims):
        raise ValueError("不支持空矩阵输入")
    
    # 生成 *DIM 定义语句
    # 如果数组元素为字符串，用charn定义
    dim_type = "charn" if (isinstance(matrix_data, list) and isinstance(matrix_data[0], str)) or isinstance(matrix_data, str) else "*dim"
    
    dim_str = ",".join(map(str, dims))
    dim_cmd = f"{dim_type},{matrix_name},{dim_str}"

    all_cmds.append(dim_cmd)
    
    # 递归生成赋值语句
    def generate_assignments(data: Any, indices: List):
        """递归遍历矩阵并生成赋值语句"""
        if isinstance(data, list):
            for idx, elem in enumerate(data):
                new_indices = indices + [idx]
                generate_assignments(elem, new_indices)
        else:
            # 处理数值赋值
            value = data
            
            # 格式化数值
            if isinstance(value, int) or isinstance(value, float):
                val_str = str(value)
            else:
                # 其他类型尝试转为string
                val_str = f"\"{value}\""
            
            # 生成OSIS赋值命令
            idx_str = ",".join(map(str, indices))
            assign_cmd = f"{matrix_name}[{idx_str}] = {val_str}"
            # _log(assign_cmd)
            # osis_run(assign_cmd, "stash")
            all_cmds.append(assign_cmd)
    
    # 开始递归生成赋值语句（OSIS索引从0开始）
    generate_assignments(matrix_data, [])
    # osis_run()
    # 返回拼接后的完整命令字符串
    str_cmds = "\n".join(all_cmds)
    _log(str_cmds)
    return osis_run(str_cmds, "exec")