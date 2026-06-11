#!/usr/bin/env python3
"""从 OSIS 命令流文件直接生成可执行的 pyosis Python 代码

用法:
    python build.py [command_file]

示例:
    python build.py              # 自动从当前 OSIS 项目导出命令流并生成代码
    python build.py C:/Temp/OSIS.out  # 从指定的 .out 文件生成代码

说明:
    直接解析 OSIS.out 命令流，转换为 pyosis API 调用代码。
    对于无法自动转换的命令，保留为注释供手动修改。
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 模块映射
MODULE_FILES = {
    "CONTROL": "_1_control.py",
    "PROPERTY": "_2_property.py",
    "MATERIAL": "_3_material.py",
    "SECTION": "_4_section.py",
    "NODE": "_5_node.py",
    "ELEMENT": "_6_element.py",
    "BOUNDARY": "_7_boundary.py",
    "LOADCASE": "_8_loadcase.py",
    "ANALYSIS": "_9_analysis.py",
    "STAGE": "_10_stage.py",
}

MODULE_NAMES = {
    "CONTROL": "全局控制参数",
    "PROPERTY": "几何属性",
    "MATERIAL": "材料",
    "SECTION": "截面",
    "NODE": "节点",
    "ELEMENT": "单元",
    "BOUNDARY": "边界条件",
    "LOADCASE": "荷载工况",
    "ANALYSIS": "分析设置",
    "STAGE": "施工阶段",
}


# ========== 辅助函数 ==========


def _val(v: str) -> str:
    """将字符串值转为 Python 字面量"""
    v = v.strip()
    if not v:
        return '""'
    # 尝试转为数字
    try:
        f = float(v)
        if f == int(f):
            return str(int(f))
        return str(f)
    except ValueError:
        pass
    # 布尔值
    if v.lower() == "true":
        return "True"
    if v.lower() == "false":
        return "False"
    # 字符串
    return repr(v)


def _bool(v: str) -> str:
    """将 0/1 转为 False/True"""
    return "True" if v.strip() == "1" else "False"


def _item_val(v: str) -> str:
    """将列表项转为 Python 字面量

    与 _val 的区别：
    - 纯数字：保持数字（如 17）
    - 范围格式（含 'to'）：加引号（如 '14to19'）
    - 其他字符串：加引号
    """
    v = v.strip()
    if not v:
        return '""'
    # 纯数字
    try:
        f = float(v)
        if f == int(f):
            return str(int(f))
        return str(f)
    except ValueError:
        pass
    # 范围格式或其他字符串，加引号
    return repr(v)


def _indent(lines: List[str], level: int = 1) -> List[str]:
    """缩进代码行"""
    prefix = "    " * level
    return [prefix + line for line in lines if line.strip()]


def parse_command_file(file_path: str) -> Dict[str, List[str]]:
    """解析命令流文件，按模块分割

    解析逻辑：
    1. 读取整个文件
    2. 移除每行中 // 后面的注释
    3. 按 ; 分割命令（支持多行命令自动合并）
    4. 去掉空白字符/制表符/换行符
    5. 再按逗号分成多个参数
    """
    file_path = Path(file_path)

    content = None
    for encoding in ["gbk", "utf-8", "gb2312", "gb18030", "latin-1"]:
        try:
            content = file_path.read_text(encoding=encoding)
            print(f"使用编码: {encoding}")
            break
        except UnicodeDecodeError:
            continue

    if content is None:
        raise ValueError(f"无法读取文件: {file_path}")

    lines = content.splitlines()
    module_pattern = re.compile(r"//-+\s*(\w+)\s*-*")

    modules: Dict[str, List[str]] = {}
    current_module = None

    # 先移除所有注释，然后拼接成文本
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # 模块标记
        match = module_pattern.match(stripped)
        if match:
            # 保存之前的模块内容
            if current_module and cleaned_lines:
                text = "\n".join(cleaned_lines)
                commands = _split_commands(text)
                modules[current_module].extend(commands)
                cleaned_lines = []

            module_name = match.group(1).upper()
            if module_name in MODULE_FILES:
                current_module = module_name
                modules[current_module] = []
            else:
                current_module = None
            continue

        # 跳过纯注释行和空行
        if stripped.startswith("//") or not stripped:
            continue

        # 移除行内注释（// 后面的内容）
        if "//" in stripped:
            stripped = stripped[: stripped.index("//")].strip()

        if stripped and current_module:
            cleaned_lines.append(stripped)

    # 处理最后一个模块
    if current_module and cleaned_lines:
        text = "\n".join(cleaned_lines)
        commands = _split_commands(text)
        modules[current_module].extend(commands)

    return modules


def _split_commands(text: str) -> List[str]:
    """按 ; 分割命令，去除空白后返回干净的命令列表

    Args:
        text: 已移除注释的文本（可能包含多行）

    Returns:
        命令列表，每个命令是去除所有空白后的字符串
    """
    # 按 ; 分割
    raw_cmds = text.split(";")

    commands = []
    for cmd in raw_cmds:
        # 去掉所有空白字符（空格、制表符、换行等）
        # 只保留参数之间的逗号
        cleaned = cmd.strip()
        if not cleaned:
            continue

        # 将内部的多余空白（包括换行、制表符）压缩为单个空格，然后去掉
        # 但保留逗号两侧的空格用于后续分割
        cleaned = " ".join(cleaned.split())
        # 去掉逗号前后的空格
        cleaned = cleaned.replace(" ,", ",").replace(", ", ",")

        commands.append(cleaned)

    return commands


def _split_cmd(cmd: str) -> List[str]:
    """分割命令参数

    命令已经过 _split_commands 处理，去除了注释和多余空白。
    只需按逗号分割，保留空值。
    方括号 [] 内的逗号不分割（支持矩阵下标如 Matrix[0,0]）。
    """
    if not cmd:
        return []

    parts = []
    current = ""
    in_quotes = False
    bracket_depth = 0
    for char in cmd:
        if char == '"':
            in_quotes = not in_quotes
            current += char
        elif char == "[" and not in_quotes:
            bracket_depth += 1
            current += char
        elif char == "]" and not in_quotes:
            bracket_depth -= 1
            current += char
        elif char == "," and not in_quotes and bracket_depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    # 总是添加最后一部分（即使为空）
    parts.append(current.strip())
    return parts


# ========== 文件头尾生成 ==========


def _module_header(module_name: str, imports: List[str] = None) -> List[str]:
    """生成模块文件头"""
    title = MODULE_NAMES.get(module_name, module_name)
    lines = [f'"""{title}"""', ""]
    if imports:
        for imp in imports:
            lines.append(imp)
        lines.append("")
    return lines


def _module_footer(module_name: str, test_code: str = None) -> List[str]:
    """生成模块文件尾（测试代码）"""
    lines = ["", 'if __name__ == "__main__":', "    from _0_engine import engine"]
    if test_code:
        lines.append("    " + test_code)
    else:
        func_name = module_name.lower()
        lines.append(f"    build_{func_name}(engine)")
    return lines


# ========== 各模块专门的代码生成函数 ==========


def generate_control(commands: List[str]) -> str:
    """生成 _1_control.py：全局控制参数"""

    # 命令到 pyosis API 的映射：(方法名, 参数位置列表, 是否布尔)
    # 参数位置列表中的整数表示 args 中的索引（从0开始）
    CONTROL_MAP = {
        "Acel": ("set_gravity_acceleration", [0]),
        "CalcTendon": ("set_calc_tendon", [0], True),
        "CalcConForce": ("set_calc_concurrent_force", [0], True),
        "CalcShrink": ("set_calc_shrink", [0], True),
        "CalcCreep": ("set_calc_creep", [0], True),
        "CalcShear": ("set_calc_shear", [0], True),
        "CalcRlx": ("set_calc_relaxation", [0], True),
        "ModLocCoor": ("set_mod_loc_coor", [0], True),
        "IncTendon": ("set_inc_tendon", [0], True),
        "LnSrch": ("set_line_search", [0], True),
        "AutoTs": ("set_auto_time_step", [0], True),
        "ModOpt": ("set_modal_opt", [0]),
    }

    lines = _module_header("CONTROL", ["from pyosis.core.engine import OSISEngine"])
    lines.append("def setup_control(engine: OSISEngine) -> None:")
    lines.append('    """设置全局控制参数"""')
    lines.append("")

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue
        cmd_name = args[0]

        if cmd_name == "NL":
            geom = _bool(args[1])
            link = _bool(args[2])
            lines.append(
                f"    engine.control.set_nonlinear(geom={geom}, link={link})"
            )
            continue

        if cmd_name == "NSUBST":
            lines.append(
                f"    engine.control.set_substitution_steps({args[1]}, {args[2]})"
            )
            continue

        if cmd_name in CONTROL_MAP:
            info = CONTROL_MAP[cmd_name]
            method = info[0]
            param_indices = info[1]
            is_bool = len(info) > 2 and info[2]

            params = []
            for idx in param_indices:
                v = args[idx + 1]
                params.append(_bool(v) if is_bool else _val(v))

            if params:
                lines.append(f"    engine.control.{method}({', '.join(params)})")
        else:
            lines.append(f"    # TODO: {cmd}")

    lines.append("")
    lines.extend(_module_footer("CONTROL", "setup_control(engine)"))
    return "\n".join(lines)


def generate_property(commands: List[str]) -> str:
    """生成 _2_property.py：几何属性（样条曲线）"""

    lines = _module_header("PROPERTY", ["from pyosis.core.engine import OSISEngine"])
    lines.append("def build_property(engine: OSISEngine) -> list[str]:")
    lines.append('    """设置几何属性（钢束线型、车道线等）"""')
    lines.append("")
    lines.append("    geo_names = []")
    lines.append("")

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        if args[0] == "Spline3D":
            name = args[1]
            stype = args[2]
            owner = args[3]
            points = args[4:]
            points_str = ", ".join(_val(p) for p in points)

            if stype == "ARC3D":
                lines.append(
                    f"    spline = engine.geometry.create_arc3d({_val(name)}, {_val(owner)}, [{points_str}])"
                )
            elif stype == "ARC2D":
                lines.append(
                    f"    spline = engine.geometry.create_arc2d({_val(name)}, {_val(owner)}, [{points_str}])"
                )
            elif stype == "GENERAL":
                lines.append(
                    f"    spline = engine.geometry.create_general({_val(name)}, {_val(owner)}, [{points_str}])"
                )
            elif stype == "NATURAL":
                lines.append(
                    f"    spline = engine.geometry.create_natural({_val(name)}, {_val(owner)}, [{points_str}])"
                )
            else:
                lines.append(f"    # TODO: Spline3D {stype} not supported")
                continue

            lines.append("    geo_names.append(spline.name)")
            lines.append("")

        elif args[0] == "CoorSys":
            coor_type = args[2].upper() if len(args) > 2 else "TRIPT"
            no = args[1]
            if coor_type == "TRIPT":
                p1x, p1y, p1z = args[3], args[4], args[5]
                p2x, p2y, p2z = args[6], args[7], args[8]
                p3x, p3y, p3z = args[9], args[10], args[11]
                lines.append(f"    engine.prop.coord.create_three_point(")
                lines.append(f"        no={no}, p1x={p1x}, p1y={p1y}, p1z={p1z},")
                lines.append(f"        p2x={p2x}, p2y={p2y}, p2z={p2z},")
                lines.append(f"        p3x={p3x}, p3y={p3y}, p3z={p3z}")
                lines.append("    )")
                lines.append("")
            elif coor_type == "DBPT":
                p1x, p1y, p1z = args[3], args[4], args[5]
                p2x, p2y, p2z = args[6], args[7], args[8]
                angle = args[9]
                lines.append(f"    engine.prop.coord.create_two_point_rotation(")
                lines.append(f"        no={no}, p1x={p1x}, p1y={p1y}, p1z={p1z},")
                lines.append(f"        p2x={p2x}, p2y={p2y}, p2z={p2z}, angle={angle}")
                lines.append("    )")
                lines.append("")
            else:
                lines.append(
                    f"    # TODO: CoorSys {coor_type} not supported"
                )
                lines.append("")
        else:
            lines.append(f"    # TODO: {cmd}")

    lines.append("    return geo_names")
    lines.append("")
    lines.extend(
        _module_footer(
            "PROPERTY",
            "geo_names = build_property(engine)\n    print(geo_names)\n    print(engine.geometry.all())",
        )
    )
    return "\n".join(lines)


def generate_material(commands: List[str]) -> str:
    """生成 _3_material.py：材料定义"""

    lines = _module_header("MATERIAL", ["from pyosis.core.engine import OSISEngine"])
    lines.append("def build_materials(engine: OSISEngine) -> list[int]:")
    lines.append('    """创建材料，返回材料编号列表"""')
    lines.append("")
    lines.append("    mat_nos = []")
    lines.append("")

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        if args[0] == "CrpShrk":
            lines.append(f"    engine.prop.creep_shrink.create(")
            lines.append(
                f"        no={args[1]}, name={_val(args[2])}, avg_humidity={args[3]},"
            )
            lines.append(
                f"        birth_time={args[4]}, type_coeff={args[5]}, shrink_birth={args[6]}"
            )
            lines.append("    )")
            lines.append("")
            continue

        if args[0] == "Material":
            no = args[1]
            name = _val(args[2])
            mat_type = args[3].upper()
            code = _val(args[4])
            grade = _val(args[5])

            if mat_type == "CONC":
                # Material,no,name,CONC,code,grade,nCrepShrk,dDmp
                if len(args) > 7:
                    nCrepShrk = _val(args[6])
                    dDmp = args[7]
                    lines.append(f"    mat = engine.material.create_conc(")
                    lines.append(f"        {name}, eCode={code}, eGrade={grade},")
                    lines.append(f"        nCrepShrk={nCrepShrk}, dDmp={dDmp}, no={no}")
                    lines.append("    )")
                else:
                    dDmp = args[6] if len(args) > 6 else "0.0"
                    lines.append(f"    mat = engine.material.create_conc(")
                    lines.append(
                        f"        {name}, eCode={code}, eGrade={grade}, dDmp={dDmp}, no={no}"
                    )
                    lines.append("    )")

            elif mat_type == "STEEL":
                dDmp = args[6] if len(args) > 6 else "0.0"
                lines.append(f"    mat = engine.material.create_steel(")
                lines.append(
                    f"        {name}, eCode={code}, eGrade={grade}, dDmp={dDmp}, no={no}"
                )
                lines.append("    )")

            elif mat_type == "REBAR":
                dDmp = args[6] if len(args) > 6 else "0.0"
                lines.append(f"    mat = engine.material.create_rebar(")
                lines.append(
                    f"        {name}, eCode={code}, eGrade={grade}, dDmp={dDmp}, no={no}"
                )
                lines.append("    )")

            elif mat_type == "PRESTRESSED":
                dDmp = args[6] if len(args) > 6 else "0.0"
                lines.append(f"    mat = engine.material.create_prestressed(")
                lines.append(
                    f"        {name}, eCode={code}, eGrade={grade}, dDmp={dDmp}, no={no}"
                )
                lines.append("    )")

            else:
                lines.append(f"    # TODO: Material type {mat_type}")
                continue

            lines.append("    mat_nos.append(mat.no)")
            lines.append("")
            continue

        lines.append(f"    # TODO: {cmd}")

    lines.append("    return mat_nos")
    lines.append("")
    lines.extend(
        _module_footer(
            "MATERIAL",
            "mat_nos = build_materials(engine)\n    print(mat_nos)\n    print(engine.material.all())",
        )
    )
    return "\n".join(lines)


# SECTION 类型到 pyosis 方法名的映射
SECTION_TYPE_MAP = {
    "CONVENTIONALBOX": "create_conventionalbox",
    "FLATBOX": "create_flat_box",
    "DOUBLESIDEBOX": "create_double_side_box",
    "RIBBEDSLAB": "create_ribbed_slab",
    "HOLLOWSLAB": "create_hollowslab",
    "SMALLBOX": "create_smallbox",
    "TGIRDER": "create_TGirder",
    "RECT": "create_rect",
    "CIRCLE": "create_circle",
    "ISHAPE": "create_Ishape",
    "LSHAPE": "create_Lshape",
    "TSHAPE": "create_Tshape",
    "ROUNDEDEND": "create_rounded_end",
    "STEELI": "create_steel_i",
    "STEELBOX": "create_steel_box",
    "STEELBOXTHREECELL": "create_steel_box_three_cell",
    "STEELBOXITF": "create_steel_box_itf",
    "STEELCANTIBOX": "create_steel_canti_box",
    "STEELCANTIBOXIBF": "create_steel_canti_box_ibf",
    "STEELCUSTOM": "create_steel_custom",
    "STEELCUSTOMPLATE": "create_steel_custom_plate",
    "CUSTOM": "create_custom",
}


def generate_section(commands: List[str]) -> str:
    """生成 _4_section.py：截面定义

    OSIS 命令格式：Section,no,name,TYPE,p1,p2,p3,...
    pyosis 格式：engine.section.create_xxx(name, p1, p2, ..., no=no)

    注意：从 TYPE 后面的参数开始，按顺序对应 pyosis 函数的参数（name 之后，no 之前）
    """

    # 矩阵赋值正则：MatrixName[row,col] = value
    matrix_assign_re = re.compile(r"^(\w+)\[(\d+),(\d+)\]\s*=\s*(.+)$")

    lines = _module_header("SECTION", ["from pyosis.core.engine import OSISEngine"])
    lines.append("def build_sections(engine: OSISEngine) -> list[int]:")
    lines.append('    """创建截面，返回截面编号列表"""')
    lines.append("")
    lines.append("    sec_nos = []")
    lines.append("")

    # 矩阵数据收集状态
    current_matrix_name: Optional[str] = None
    current_matrix_rows: int = 0
    current_matrix_cols: int = 0
    current_matrix_data: Dict[tuple[int, int], str] = {}

    def _flush_matrix():
        """将收集的矩阵数据输出为 engine.matrix() 调用"""
        nonlocal current_matrix_name, current_matrix_rows, current_matrix_cols, current_matrix_data
        if current_matrix_name is None or not current_matrix_data:
            return
        # 构建二维列表
        matrix_lines = ["    contour_matrix = ["]
        for r in range(current_matrix_rows):
            row_vals = []
            for c in range(current_matrix_cols):
                val = current_matrix_data.get((r, c), "0")
                row_vals.append(val)
            matrix_lines.append(f"        [{', '.join(row_vals)}],")
        matrix_lines.append("    ]")
        matrix_lines.append(f'    engine.matrix("{current_matrix_name}", contour_matrix)')
        lines.extend(matrix_lines)
        lines.append("")
        # 重置状态
        current_matrix_name = None
        current_matrix_rows = 0
        current_matrix_cols = 0
        current_matrix_data = {}

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        # 处理 *dim 命令: *dim,MatrixName,rows,cols
        if args[0].startswith("*dim"):
            _flush_matrix()
            current_matrix_name = args[1]
            current_matrix_rows = int(args[2])
            current_matrix_cols = int(args[3])
            current_matrix_data = {}
            continue

        # 处理矩阵赋值: MatrixName[row,col] = value
        if len(args) == 1:
            m = matrix_assign_re.match(args[0])
            if m:
                mat_name = m.group(1)
                row = int(m.group(2))
                col = int(m.group(3))
                val = m.group(4).strip()
                # 如果矩阵名匹配当前收集的矩阵
                if current_matrix_name == mat_name:
                    current_matrix_data[(row, col)] = val
                else:
                    # 不匹配，作为 TODO
                    lines.append(f"    # TODO: {cmd}")
                continue

        if args[0] == "Section":
            no = args[1]
            name = args[2]
            sec_type = args[3]
            params = args[4:]

            method = SECTION_TYPE_MAP.get(sec_type)
            if method is None:
                lines.append(f"    # TODO: Section type {sec_type} not supported")
                continue

            # CUSTOM 截面使用矩阵，先 flush 矩阵定义
            if method == "create_custom":
                _flush_matrix()

            # 构建参数列表：name 是第一个参数，然后是其他参数，最后是 no
            param_strs = [_val(name)]
            for p in params:
                param_strs.append(_val(p))
            param_strs.append(f"no={no}")

            # 格式化输出，每行最多 4 个参数
            lines.append(f"    sec = engine.section.{method}(")
            for i in range(0, len(param_strs), 4):
                chunk = param_strs[i : i + 4]
                lines.append("        " + ", ".join(chunk) + ",")
            lines.append("    )")
            lines.append("    sec_nos.append(sec.no)")
            lines.append("")

        elif args[0] == "SectionOffset":
            lines.append(f"    sec.set_offset(")
            lines.append(
                f"        offset_type_y={_val(args[2])}, offset_value_y={args[3]},"
            )
            lines.append(
                f"        offset_type_z={_val(args[4])}, offset_value_z={args[5]}"
            )
            lines.append("    )")
            lines.append("")

        elif args[0] == "SectionMesh":
            lines.append(f"    sec.set_mesh(")
            lines.append(f"        mesh_method={args[2]}, mesh_size={args[3]}")
            lines.append("    )")
            lines.append("")

        elif args[0] == "StressPoint":
            lines.append(
                f"    sec.set_stress_point({args[2]}, {args[3]}, {args[4]})"
            )

        # ── 钢筋──
        elif args[0] == "RebarL":
            sec_no = args[1]
            rebar_no = args[2]
            rebar_type = args[3].upper()
            mat_no = args[4]

            if rebar_type == "POINT":
                y, z = args[5], args[6]
                dia = _val(args[7])
                lines.append(
                    f"    engine.section.get({sec_no}).add_rebar_point({rebar_no}, {mat_no}, {y}, {z}, {dia})"
                )
            elif rebar_type == "LINEA":
                y_ref = _val(args[5])
                y_ref_val = args[6]
                z_ref = _val(args[7])
                z_ref_val = args[8]
                num = args[9]
                interval = args[10]
                dia = _val(args[11])
                lines.append(
                    f"    engine.section.get({sec_no}).add_rebar_line_a({rebar_no}, {mat_no}, {y_ref}, {y_ref_val}, {z_ref}, {z_ref_val}, {num}, {interval}, {dia})"
                )
            elif rebar_type == "LINEB":
                start_y, start_z = args[5], args[6]
                end_y, end_z = args[7], args[8]
                method = args[9]
                num = args[10]
                interval = args[11]
                layout_ref = _val(args[12])
                has_end = args[13]
                dia = _val(args[14])
                lines.append(
                    f"    engine.section.get({sec_no}).add_rebar_line_b({rebar_no}, {mat_no}, {start_y}, {start_z}, {end_y}, {end_z}, {method}, {num}, {interval}, {layout_ref}, {has_end}, {dia})"
                )
            elif rebar_type == "CIRCLE":
                center_y,center_z = args[5], args[6]
                radius = args[7]
                method = args[8]
                num = args[9]
                interval = args[10]
                diameter = args[11]
                lines.append(
                    f"    engine.section.get({sec_no}).add_rebar_circle({rebar_no},{mat_no},{center_y},{center_z},{radius},{method},{num}, {interval}, {diameter})"
                )
            else:
                lines.append(f"    # TODO: RebarL type {rebar_type}")

        elif args[0] == "RebarS":
            sec_no = args[1]
            rebar_type = args[2].upper()
            mat_no = args[3]

            if rebar_type == "SHEARSTIRRUP":
                interval = args[4]
                area = args[5]
                lines.append(
                    f"    engine.section.get({sec_no}).add_rebar_s_shear_stirrup({mat_no}, {interval}, {area})"
                )
            elif rebar_type == "BENTUPREBAR":
                interval = args[4]
                area = args[5]
                angle = args[6] if len(args) > 6 else "45"
                lines.append(
                    f"    engine.section.get({sec_no}).add_rebar_s_bent_up({mat_no}, {interval}, {area}, {angle})"
                )
            else:
                lines.append(f"    # TODO: RebarS type {rebar_type}")

        else:
            lines.append(f"    # TODO: {cmd}")

    #  Flush 剩余矩阵定义
    _flush_matrix()

    lines.append("    return sec_nos")
    lines.append("")
    lines.extend(
        _module_footer(
            "SECTION",
            "sec_nos = build_sections(engine)\n    print(sec_nos)\n    print(engine.section.all())",
        )
    )
    return "\n".join(lines)


def generate_node(commands: List[str]) -> str:
    """生成 _5_node.py：节点创建"""

    lines = _module_header("NODE", ["from pyosis.core.engine import OSISEngine"])
    lines.append("def build_nodes(engine: OSISEngine) -> list[int]:")
    lines.append('    """创建节点，返回节点编号列表"""')
    lines.append("")
    lines.append("    node_nos = []")
    lines.append("")

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args or args[0] != "Node":
            lines.append(f"    # TODO: {cmd}")
            continue

        no = args[1]
        x, y, z = args[2], args[3], args[4]
        lines.append(f"    n = engine.node.create({x}, {y}, {z}, no={no})")
        lines.append("    node_nos.append(n.no)")
        lines.append("")

    lines.append("    return node_nos")
    lines.append("")
    lines.extend(
        _module_footer(
            "NODE",
            "node_nos = build_nodes(engine)\n    print(node_nos)\n    print(engine.node.all())",
        )
    )
    return "\n".join(lines)


def generate_element(commands: List[str]) -> str:
    """生成 _6_element.py：单元创建

    OSIS 命令格式：Element,no,TYPE,p1,p2,p3,...;
    pyosis 格式：engine.element.create_xxx(p1, p2, p3, ..., no=no)

    注意：从 TYPE 后面的参数开始，顺序与 pyosis 函数完全一致，直接按顺序传入即可
    """

    lines = _module_header("ELEMENT", ["from pyosis.core.engine import OSISEngine"])
    lines.append(
        "def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:"
    )
    lines.append('    """创建单元，返回单元编号列表和单元组名称列表"""')
    lines.append("")
    lines.append("    elem_nos = []")
    lines.append("    elem_group_names = []")
    lines.append("")

    # 跟踪当前单元组，用于连续 c->a 操作优化
    current_elem_group = None

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        if args[0] == "Element":
            no = args[1]
            elem_type = args[2].upper()
            # 从 TYPE 后面的参数开始，按顺序传入
            params = [_val(p) for p in args[3:]]
            params.append(f"no={no}")

            method_map = {
                "BEAM3D": "create_beam3d",
                "TRUSS": "create_truss",
                "SPRING": "create_spring",
            }

            method = method_map.get(elem_type)
            if method:
                lines.append(f"    e = engine.element.{method}({', '.join(params)})")
                lines.append("    elem_nos.append(e.no)")
                lines.append("")
            else:
                lines.append(f"    # TODO: Element type {elem_type}")

        elif args[0] == "AsgnCompThk":
            thickness = args[1]
            op = _val(args[2])
            items = ", ".join(_item_val(item) for item in args[3:])
            lines.append(
                f"    engine.prop.assign_component_thickness({thickness}, op={op}, elems=[{items}])"
            )
            lines.append("")

        elif args[0] == "EleGrp":
            op = args[2]
            raw_name = args[1]
            name = _val(raw_name)
            if op == "c":
                lines.append(f"    eg = engine.element.group.create({name})")
                lines.append("    elem_group_names.append(eg.name)")
                lines.append("")
                current_elem_group = raw_name
            elif op == "a":
                items = ", ".join(_item_val(item) for item in args[3:])
                # 如果紧接着同名组，直接用 eg 变量
                if raw_name == current_elem_group:
                    lines.append(f"    eg.add([{items}])")
                else:
                    lines.append(
                        f"    engine.element.group.get({name}).add([{items}])"
                    )
                lines.append("")

        else:
            lines.append(f"    # TODO: {cmd}")

    lines.append("    return elem_nos, elem_group_names")
    lines.append("")
    lines.extend(
        _module_footer(
            "ELEMENT",
            "mats = engine.material.all()\n"
            "    mat_nos = [m.no for m in mats]\n"
            "    secs = engine.section.all()\n"
            "    sec_nos = [s.no for s in secs]\n"
            "    nodes = engine.node.all()\n"
            "    node_nos = [n.no for n in nodes]\n"
            "    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)\n"
            "    print(elem_nos)\n"
            "    print(elem_group_names)\n"
            "    print(engine.element.all())\n"
            "    print(engine.element.group.all())",
        )
    )
    return "\n".join(lines)


def generate_boundary(commands: List[str]) -> str:
    """生成 _7_boundary.py：边界条件"""

    lines = _module_header("BOUNDARY", ["from pyosis.core.engine import OSISEngine"])
    lines.append(
        "def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:"
    )
    lines.append('    """创建边界条件，返回边界编号列表和边界组名称列表"""')
    lines.append("")
    lines.append("    bd_nos = []")
    lines.append("    bd_group_names = []")
    lines.append("")

    # 跟踪已创建的边界和边界组
    bd_created = {}  # no -> type
    current_bd_no = None  # 上一个创建的边界编号
    current_bd_group = None

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        if args[0] == "Boundary":
            no = args[1]
            bd_type = args[2].upper()
            bd_created[no] = bd_type

            if bd_type == "GENERAL":
                nCoor = _val(args[3]) if args[3] else '""'
                bX, bY, bZ = args[4], args[5], args[6]
                bRX, bRY, bRZ, bRW = args[7], args[8], args[9], args[10]

                params = [f"nCoor={nCoor}"]
                if bX != "1":
                    params.append(f"bX={bX}")
                if bY != "1":
                    params.append(f"bY={bY}")
                if bZ != "1":
                    params.append(f"bZ={bZ}")
                if bRX != "1":
                    params.append(f"bRX={bRX}")
                if bRY != "1":
                    params.append(f"bRY={bRY}")
                if bRZ != "1":
                    params.append(f"bRZ={bRZ}")
                if bRW != "1":
                    params.append(f"bRW={bRW}")
                params.append(f"no={no}")

                lines.append(
                    f"    bd = engine.boundary.create_general({', '.join(params)})"
                )
                lines.append("    bd_nos.append(bd.no)")
                lines.append("")
                current_bd_no = no

            elif bd_type == "MSTSLV":
                master = args[3]
                bX, bY, bZ = args[4], args[5], args[6]
                bRX, bRY, bRZ = args[7], args[8], args[9]

                params = [f"nNode={master}"]
                if bX != "1":
                    params.append(f"bX={bX}")
                if bY != "1":
                    params.append(f"bY={bY}")
                if bZ != "1":
                    params.append(f"bZ={bZ}")
                if bRX != "1":
                    params.append(f"bRX={bRX}")
                if bRY != "1":
                    params.append(f"bRY={bRY}")
                if bRZ != "1":
                    params.append(f"bRZ={bRZ}")
                params.append(f"no={no}")

                lines.append(
                    f"    bd = engine.boundary.create_master_slave({', '.join(params)})"
                )
                lines.append("    bd_nos.append(bd.no)")
                lines.append("")
                current_bd_no = no

            elif bd_type == "ELSTCSPT":
                nCoor = _val(args[3]) if args[3] else '""'
                params = [f"nCoor={nCoor}"]

                # 成对参数: (flag, stiffness) -- 仅当 flag!=1 或 stiffness!=默认值时传入
                pair_defaults = {
                    "bX": ("1", "1e13"),
                    "bY": ("1", "1e13"),
                    "bZ": ("1", "1e13"),
                    "bRX": ("1", "1e16"),
                    "bRY": ("1", "1e16"),
                    "bRZ": ("1", "1e16"),
                }
                pair_names = [
                    ("bX", "DX"),
                    ("bY", "DY"),
                    ("bZ", "DZ"),
                    ("bRX", "RX"),
                    ("bRY", "RY"),
                    ("bRZ", "RZ"),
                ]
                idx = 4
                for bname, dname in pair_names:
                    bval = args[idx] if idx < len(args) else None
                    idx += 1
                    dval = args[idx] if idx < len(args) else None
                    idx += 1

                    bdef, ddef = pair_defaults[bname]
                    if bval is not None and (
                        bval != bdef or (dval is not None and dval != ddef)
                    ):
                        params.append(f"{bname}={bval}")
                        if dval is not None:
                            params.append(f"{dname}={dval}")

                params.append(f"no={no}")

                lines.append(
                    f"    bd = engine.boundary.create_elstcspt({', '.join(params)})"
                )
                lines.append("    bd_nos.append(bd.no)")
                lines.append("")
                current_bd_no = no

            else:
                lines.append(f"    # TODO: Boundary type {bd_type}")

        elif args[0] == "AsgnBd":
            no = args[1]
            op = args[2]
            nodes = ", ".join(_item_val(item) for item in args[3:])
            # 如果紧接着同名边界，直接用 bd 变量
            if no == current_bd_no:
                lines.append(f"    bd.assign('{op}', [{nodes}])")
            else:
                lines.append(
                    f"    engine.boundary.get({no}).assign('{op}', [{nodes}])"
                )
            lines.append("")

        elif args[0] == "BdGrp":
            raw_name = args[1]
            name = _val(raw_name)
            op = args[2]
            if op == "c":
                lines.append(f"    bg = engine.boundary.group.create({name})")
                lines.append("    bd_group_names.append(bg.name)")
                lines.append("")
                current_bd_group = raw_name
            elif op == "a":
                items = ", ".join(_item_val(item) for item in args[3:])
                # 如果紧接着同名组，直接用 bg 变量
                if raw_name == current_bd_group:
                    lines.append(f"    bg.add([{items}])")
                else:
                    lines.append(
                        f"    engine.boundary.group.get({name}).add([{items}])"
                    )
                lines.append("")

        else:
            lines.append(f"    # TODO: {cmd}")

    lines.append("    return bd_nos, bd_group_names")
    lines.append("")
    lines.extend(
        _module_footer(
            "BOUNDARY",
            "nodes = engine.node.all()\n"
            "    node_nos = [n.no for n in nodes]\n"
            "    bd_nos, bd_groups = build_boundaries(engine, node_nos)\n"
            "    print(bd_nos)\n"
            "    print(bd_groups)\n"
            "    print(engine.boundary.all())\n"
            "    print(engine.boundary.group.all())",
        )
    )
    return "\n".join(lines)


def generate_loadcase(commands: List[str]) -> str:
    """生成 _8_loadcase.py：荷载工况

    包含：荷载工况创建、钢束、各种荷载施加
    """

    lines = _module_header("LOADCASE", ["from pyosis.core.engine import OSISEngine"])
    lines.append(
        "def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:"
    )
    lines.append('    """创建荷载工况和钢束，返回荷载工况名称列表"""')
    lines.append("")
    lines.append("    lc_names = []")
    lines.append("")

    # 跟踪已创建的荷载工况和钢束形状
    lc_created = set()
    current_lc_name = None  # 上一个创建的荷载工况名
    current_shape_name = None

    def _get_lc_prefix(lc_name_raw: str) -> str:
        """返回荷载工况调用前缀：如果是当前工况用 lc.，否则用 engine.load.get(name)."""
        if lc_name_raw == current_lc_name:
            return "lc."
        return f"engine.load.get({_val(lc_name_raw)})."

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        if args[0] == "LoadCase":
            raw_name = args[1]
            name = _val(raw_name)
            lc_type = _val(args[2])
            scalar = args[3] if len(args) > 3 else "1.0"
            lines.append(
                f"    lc = engine.load.create({name}, load_case_type={lc_type}, scalar={scalar})"
            )
            lines.append("    lc_names.append(lc.name)")
            lines.append("")
            lc_created.add(raw_name)
            current_lc_name = raw_name

        elif args[0] == "Load":
            load_type = args[1].upper()
            lc_name_raw = args[2]
            prefix = _get_lc_prefix(lc_name_raw)

            if load_type == "GRAVITY":
                dX, dY, dZ = args[3], args[4], args[5]
                lines.append(f"    {prefix}create_gravity({dX}, {dY}, {dZ})")
                lines.append("")

            elif load_type == "NFORCE":
                node = args[3]
                Fx, Fy, Fz = args[4], args[5], args[6]
                Mx, My, Mz = args[7], args[8], args[9]
                lines.append(
                    f"    {prefix}create_nforce({node}, {Fx}, {Fy}, {Fz}, {Mx}, {My}, {Mz})"
                )
                lines.append("")

            elif load_type == "LINE":
                elem = args[3]
                eCoord = args[4]
                eType = args[5]
                i_params = args[6:15]  # dOffsetXI ~ dMZI
                j_params = args[15:24]  # dOffsetXJ ~ dMZJ

                i_names = [
                    "dOffsetXI",
                    "dOffsetYI",
                    "dOffsetZI",
                    "dFXI",
                    "dFYI",
                    "dFZI",
                    "dMXI",
                    "dMYI",
                    "dMZI",
                ]
                j_names = [
                    "dOffsetXJ",
                    "dOffsetYJ",
                    "dOffsetZJ",
                    "dFXJ",
                    "dFYJ",
                    "dFZJ",
                    "dMXJ",
                    "dMYJ",
                    "dMZJ",
                ]

                params = [
                    f"nEntity={elem}",
                    f"eCoordSystem={eCoord}",
                    f"eLoadType={eType}",
                ]
                for name, val in zip(i_names, i_params):
                    params.append(f"{name}={val}")
                for name, val in zip(j_names, j_params):
                    params.append(f"{name}={val}")

                lines.append(f"    {prefix}create_line_load({', '.join(params)})")
                lines.append("")

            elif load_type == "UTEMP":
                elem = args[3]
                direct = _val(args[4])
                temp = args[5]
                lines.append(
                    f"    {prefix}create_uniform_temperature({elem}, eDirect={direct}, dTemp={temp})"
                )
                lines.append("")

            elif load_type == "GTEMP":
                elem = args[3]
                direct = _val(args[4])
                gtype = _val(args[5])
                num = args[6]
                params = ", ".join(_val(p) for p in args[7:])
                lines.append(
                    f"    {prefix}create_gradient_temperature({elem}, eDirect={direct}, eGTempType={gtype}, nNum={num}, param=[{params}])"
                )
                lines.append("")

            elif load_type == "PST":
                shape = _val(args[3])
                tension_type = _val(args[4])
                force_type = _val(args[5])
                beg = args[6]
                if len(args) > 7:
                    end = args[7]
                    lines.append(
                        f"    {prefix}create_prestress({shape}, eTensionType={tension_type}, eTensionForceType={force_type}, dBeg={beg}, dEnd={end})"
                    )
                else:
                    # OSIS 导出时可能省略末尾的 0 值
                    if args[4].upper() == "BEG":
                        lines.append(
                            f"    {prefix}create_prestress({shape}, eTensionType={tension_type}, eTensionForceType={force_type}, dBeg={beg}, dEnd=None)"
                        )
                    elif args[4].upper() == "END":
                        lines.append(
                            f"    {prefix}create_prestress({shape}, eTensionType={tension_type}, eTensionForceType={force_type}, dBeg=None, dEnd={beg})"
                        )
                    else:
                        lines.append(
                            f"    {prefix}create_prestress({shape}, eTensionType={tension_type}, eTensionForceType={force_type}, dBeg={beg}, dEnd={beg})"
                        )
                lines.append("")

            elif load_type in ("PTF", "PTM"):
                elem = args[3]
                eCoord = args[4]
                is_moment = "True" if load_type == "PTM" else "False"
                offset_x = args[6]
                offset_y = args[7]
                offset_z = args[8]
                fx = args[9]
                fy = args[10]
                fz = args[11]
                lines.append(
                    f"    {prefix}create_concentrated_force({elem}, eCoordSystem={eCoord}, is_moment={is_moment}, forces=[[{offset_x}, {offset_y}, {offset_z}, {fx}, {fy}, {fz}]])"
                )
                lines.append("")

            else:
                lines.append(f"    # TODO: Load {load_type}")
                lines.append(f"    # {cmd}")
                lines.append("")

        elif args[0] == "TdProp":
            name = _val(args[1])
            t_type = args[2].upper()
            mat = args[3]
            bArea = args[4]

            # 从 args[5] 开始取剩余参数
            rem = args[5:]

            def _fmt_param(idx: int, pname: str) -> str:
                if idx < len(rem):
                    return f"{pname}={rem[idx]}"
                return ""

            if t_type == "IN":
                if bArea == "1":
                    # IN 按规范: eCode, diameter, nNum, dPipe, [friction, deviation, startDef, endDef, tension, relax]
                    params = [
                        f"n_mat={mat}",
                        f"e_code={_val(rem[0])}",
                        f"diameter={rem[1]}",
                        f"n_num={rem[2]}",
                        f"d_pipe={rem[3]}",
                    ]
                    # 可选参数
                    opts = [
                        (4, "d_friction_coeff"),
                        (5, "d_deviation_coeff"),
                        (6, "d_starting_deform"),
                        (7, "d_end_deform"),
                        (8, "d_tensioning_coeff"),
                        (9, "d_relaxation_coeff"),
                    ]
                    for idx, pname in opts:
                        s = _fmt_param(idx, pname)
                        if s:
                            params.append(s)
                    lines.append(f"    engine.tendon.prop.create_in({name}, {', '.join(params)})")
                else:
                    # IN 用户输入: dVal, dPipe, [friction, deviation, startDef, endDef, tension, relax]
                    params = [
                        f"n_mat={mat}",
                        f"d_val={rem[0]}",
                        f"d_pipe={rem[1]}",
                    ]
                    opts = [
                        (2, "d_friction_coeff"),
                        (3, "d_deviation_coeff"),
                        (4, "d_starting_deform"),
                        (5, "d_end_deform"),
                        (6, "d_tensioning_coeff"),
                        (7, "d_relaxation_coeff"),
                    ]
                    for idx, pname in opts:
                        s = _fmt_param(idx, pname)
                        if s:
                            params.append(s)
                    lines.append(f"    engine.tendon.prop.create_in_custom({name}, {', '.join(params)})")
                lines.append("")

            elif t_type == "EX":
                if bArea == "1":
                    # EX 按规范: eCode, diameter, nNum, dPipe, [friction, startDef, endDef, tension, relax]
                    params = [
                        f"n_mat={mat}",
                        f"e_code={_val(rem[0])}",
                        f"diameter={rem[1]}",
                        f"n_num={rem[2]}",
                        f"d_pipe={rem[3]}",
                    ]
                    opts = [
                        (4, "d_friction_coeff"),
                        (5, "d_starting_deform"),
                        (6, "d_end_deform"),
                        (7, "d_tensioning_coeff"),
                        (8, "d_relaxation_coeff"),
                    ]
                    for idx, pname in opts:
                        s = _fmt_param(idx, pname)
                        if s:
                            params.append(s)
                    lines.append(f"    engine.tendon.prop.create_ex({name}, {', '.join(params)})")
                else:
                    # EX 用户输入: dVal, dPipe, [friction, startDef, endDef, tension, relax]
                    params = [
                        f"n_mat={mat}",
                        f"d_val={rem[0]}",
                        f"d_pipe={rem[1]}",
                    ]
                    opts = [
                        (2, "d_friction_coeff"),
                        (3, "d_starting_deform"),
                        (4, "d_end_deform"),
                        (5, "d_tensioning_coeff"),
                        (6, "d_relaxation_coeff"),
                    ]
                    for idx, pname in opts:
                        s = _fmt_param(idx, pname)
                        if s:
                            params.append(s)
                    lines.append(f"    engine.tendon.prop.create_ex_custom({name}, {', '.join(params)})")
                lines.append("")

            elif t_type == "PRE":
                if bArea == "1":
                    # PRE 按规范: eCode, diameter, nNum, dDeltaT, [tension, relax]
                    params = [
                        f"n_mat={mat}",
                        f"e_code={_val(rem[0])}",
                        f"diameter={rem[1]}",
                        f"n_num={rem[2]}",
                        f"d_delta_t={rem[3]}",
                    ]
                    opts = [
                        (4, "d_tensioning_coeff"),
                        (5, "d_relaxation_coeff"),
                    ]
                    for idx, pname in opts:
                        s = _fmt_param(idx, pname)
                        if s:
                            params.append(s)
                    lines.append(f"    engine.tendon.prop.create_pre({name}, {', '.join(params)})")
                else:
                    # PRE 用户输入: dVal, dDeltaT, [tension, relax]
                    params = [
                        f"n_mat={mat}",
                        f"d_val={rem[0]}",
                        f"d_delta_t={rem[1]}",
                    ]
                    opts = [
                        (2, "d_tensioning_coeff"),
                        (3, "d_relaxation_coeff"),
                    ]
                    for idx, pname in opts:
                        s = _fmt_param(idx, pname)
                        if s:
                            params.append(s)
                    lines.append(f"    engine.tendon.prop.create_pre_custom({name}, {', '.join(params)})")
                lines.append("")

            else:
                lines.append(f"    # TODO: TdProp type {t_type}")
                lines.append("")

        elif args[0] == "TdShape":
            raw_name = args[1]
            name = _val(raw_name)
            num = args[2]
            prop = _val(args[3])
            elem_group = _val(args[4])
            shape_type = args[5].upper()

            if shape_type == "ARC3D":
                curve = _val(args[6])
                lines.append(
                    f"    shape = engine.tendon.shape.create_arc3d({name}, n_num={num}, prop={prop}, element_group={elem_group}, curve_name={curve})"
                )
                lines.append("")
                current_shape_name = raw_name
            elif shape_type == "SPL3D":
                curve = _val(args[6])
                lines.append(
                    f"    shape = engine.tendon.shape.create_spl3d({name}, n_num={num}, prop={prop}, element_group={elem_group}, curve_name={curve})"
                )
                lines.append("")
                current_shape_name = raw_name
            elif shape_type == "ARC2D":
                e_type = args[6]
                curve1 = _val(args[7])
                curve2 = _val(args[8])
                lines.append(
                    f"    shape = engine.tendon.shape.create_arc2d({name}, n_num={num}, prop={prop}, element_group={elem_group}, e_type={e_type}, param=[{curve1}, {curve2}])"
                )
                lines.append("")
                current_shape_name = raw_name
            else:
                lines.append(f"    # TODO: TdShape type {shape_type}")
                lines.append("")

        elif args[0] == "LayoutTS":
            name = args[1]
            layout_type = args[2]
            if layout_type.upper() == "ELEMENT":
                layout_type = _val(layout_type)
                n_ele = args[3]
                n_beg = args[4]
                n_dir = args[5]
                d_offset_x = args[6]
                d_offset_y = args[7]
                d_offset_z = args[8] if len(args) > 8 else "0.0"
                # 如果紧接着同名 shape，直接用 shape 变量
                if name == current_shape_name:
                    lines.append(f"    shape.layout({layout_type}, {n_ele}, {n_beg}, {n_dir}, {d_offset_x}, {d_offset_y}, {d_offset_z})")
                else:
                    lines.append(
                        f"    engine.tendon.shape.get({name}).layout({layout_type}, {n_ele}, {n_beg}, {n_dir}, {d_offset_x}, {d_offset_y}, {d_offset_z})"
                    )
                lines.append("")
            elif layout_type.upper() == "GLOBAL":
                layout_type = _val(layout_type)
                if name == current_shape_name:
                    lines.append(f"    shape.layout({layout_type})")
                else:
                    lines.append(
                        f"    engine.tendon.shape.get({name}).layout({layout_type})"
                    )
                lines.append("")
            else:
                lines.append(f"    # TODO: LayoutTS type {layout_type}")
                lines.append("")

        else:
            lines.append(f"    # TODO: {cmd}")

    lines.append("    return lc_names")
    lines.append("")
    lines.extend(
        _module_footer(
            "LOADCASE",
            "mats = engine.material.all()\n"
            "    mat_nos = [m.no for m in mats]\n"
            "    elems = engine.element.all()\n"
            "    elem_nos = [e.no for e in elems]\n"
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    geos = engine.geometry.all()\n"
            "    geo_names = [s.name for s in geos]\n"
            "    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)\n"
            "    print(lc_names)\n"
            "    print(engine.load.all())",
        )
    )
    return "\n".join(lines)


def generate_analysis(commands: List[str]) -> str:
    """生成 _9_analysis.py：分析设置（沉降+活载）"""

    lines = _module_header("ANALYSIS", ["from pyosis.core.engine import OSISEngine"])
    lines.append(
        "def build_analysis(engine: OSISEngine, node_nos: list[int], elem_group_names: list[str]) -> tuple[list[str], list[str]]:"
    )
    lines.append(
        '    """创建沉降分析和活载分析，返回(沉降工况名列表, 活载工况名列表)"""'
    )
    lines.append("")
    lines.append("    settle_names = []")
    lines.append("    live_names = []")
    lines.append("")

    # 生成器内部状态跟踪
    _current_settlement = None
    _current_live_case = None

    def _get_live_prefix(live_name_raw: str) -> str:
        """返回活载工况调用前缀：如果是当前工况用 lc.，否则用 engine.live.case.get(name)."""
        if live_name_raw == _current_live_case:
            return "lc."
        return f"engine.live.case.get({_val(live_name_raw)})."

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        if args[0] == "SetlGrp":
            name = repr(args[1])
            val = args[2]
            node = args[3]
            lines.append(
                f"    engine.settlement.group.create({name}, {val}, [{node}])"
            )
            lines.append("")

        elif args[0] == "SetlAnal":
            raw_name = args[1]
            name = repr(raw_name)
            lines.append(f"    st = engine.settlement.create({name})")
            lines.append("    settle_names.append(st.name)")
            lines.append("")
            _current_settlement = raw_name

        elif args[0] == "SetlAnalInc":
            raw_name = args[1]
            grps = ", ".join(repr(g) for g in args[3:])
            if raw_name == _current_settlement:
                lines.append(f"    st.include({grps})")
            else:
                lines.append(
                    f"    engine.settlement.get({repr(raw_name)}).include({grps})"
                )
            lines.append("")

        elif args[0] == "LiveGrade":
            name = _val(args[1])
            code = _val(args[2])
            grade = _val(args[3])
            lines.append(
                f"    engine.live.grade.create_highway({name}, eCode={code}, eLiveLoadType={grade})"
            )
            lines.append("")

        elif args[0] == "InflAlgo":
            name = _val(args[1])
            algo_type = args[2].upper()

            if algo_type == "VE":
                length = args[3]
                wheel = args[4]
                ori = args[5]
                ref = args[6]
                esel = _val(args[7])
                if ref == "0":
                    offset_y = args[8] if len(args) > 8 else "0.0"
                    offset_z = args[9] if len(args) > 9 else "0.0"
                    lines.append(
                        f"    engine.live.lane.create_ve({name}, dLength={length}, wheel={wheel}, eOriention={ori}, eRef=0, ref_elems={esel}, offsetY={offset_y}, offsetZ={offset_z})"
                    )
                else:
                    spline = _val(args[8]) if len(args) > 8 else '""'
                    lines.append(
                        f"    engine.live.lane.create_ve({name}, dLength={length}, wheel={wheel}, eOriention={ori}, eRef=1, spline_name={spline})"
                    )

            elif algo_type == "TCB":
                crossbeam = _val(args[3])
                length = args[4]
                wheel = args[5]
                ori = args[6]
                ref = args[7]
                if ref == "0":
                    ref_elems = _val(args[8]) if len(args) > 8 else '""'
                    offset_y = args[9] if len(args) > 9 else "0.0"
                    offset_z = args[10] if len(args) > 10 else "0.0"
                    lines.append(
                        f"    engine.live.lane.create_tcb({name}, crossbeam_elems={crossbeam}, dLength={length}, wheel={wheel}, eOriention={ori}, eRef=0, ref_elems={ref_elems}, offsetY={offset_y}, offsetZ={offset_z})"
                    )
                else:
                    spline = _val(args[8]) if len(args) > 8 else '""'
                    lines.append(
                        f"    engine.live.lane.create_tcb({name}, crossbeam_elems={crossbeam}, dLength={length}, wheel={wheel}, eOriention={ori}, eRef=1, spline_name={spline})"
                    )

            else:
                lines.append(f"    # TODO: InflAlgo type {algo_type}")

            lines.append("")

        elif args[0] == "LiveAnal":
            raw_name = args[1]
            name = _val(raw_name)
            code = _val(args[2])
            sub_cmb = args[3]
            lines.append(
                f"    lc = engine.live.case.create({name}, code={code}, sub_cmb_type={sub_cmb})"
            )
            lines.append("    live_names.append(lc.name)")
            lines.append("")
            _current_live_case = raw_name

        elif args[0] == "LiveAnalFactor":
            raw_name = args[1]
            prefix = _get_live_prefix(raw_name)
            factors = ", ".join(args[2:])
            lines.append(f"    {prefix}set_trans_reduction_factors([{factors}])")
            lines.append("")

        elif args[0] == "LiveAnalOpt":
            raw_name = args[1]
            prefix = _get_live_prefix(raw_name)
            sub_name = _val(args[2])
            min_lanes = args[3]
            max_lanes = args[4]
            lines.append(
                f"    {prefix}set_lane_count({sub_name}, {min_lanes}, {max_lanes})"
            )
            lines.append("")

        elif args[0] == "LiveAnalInc":
            raw_name = args[1]
            op = args[2]                     # 'a' 或 'm'
            if op in ['a', 'm']:
                sub_name = _val(args[3])
                grade_name = _val(args[4])
                scalar = args[5]
                calc_mu = (args[6] == "1")       # muFlag
                extra = args[8:]                 # bridgeType 之后的所有参数

                # 根据 OP 选择函数名
                func_name = "create_sub" if op == "a" else "modify_sub"
                prefix = _get_live_prefix(raw_name)

                # 构建基础参数
                params = f"{sub_name}, {grade_name}, scalar={scalar}, calc_mu={calc_mu}"

                if calc_mu:
                    bridge_type = _val(args[7])
                    # 各桥型需要的 para_i 数量
                    mu_param_counts = {
                        "SIMPLE": 4,
                        "CONTINUOUS": 5,
                        "ARCH": 5,
                        "CABLE_STAYED": 2,
                        "CABLE_STAYED_AUX": 2,
                        "SUSPENSION": 5,
                        "BRIDGE_TYPE_CUSTOM": 1,
                        "CUSTOM": 1,
                    }
                    n_mu = mu_param_counts.get(args[7], 0)
                    mu_params = extra[:n_mu] if n_mu else []
                    lane_names = extra[n_mu:]   # 剩余部分为车道名列表
                    params += f", bridge_type={bridge_type}"
                    if mu_params:
                        # mu_params 通常是数值，直接拼接
                        mu_str = ", ".join(str(p) for p in mu_params)
                        params += f", mu_params=[{mu_str}]"
                else:
                    # 不考虑冲击系数时，bridgeType 和 para_i 被忽略，所有 extra 均为车道名
                    lane_names = extra

                if lane_names:
                    lane_str = ", ".join(_val(l) for l in lane_names)
                    params += f", lane_names=[{lane_str}]"

                lines.append(f"    {prefix}{func_name}({params})")
                lines.append("")
            else:
                lines.append(f"    # TODO: {cmd}")

        else:
            lines.append(f"    # TODO: {cmd}")

    lines.append("    return settle_names, live_names")
    lines.append("")
    lines.extend(
        _module_footer(
            "ANALYSIS",
            "nodes = engine.node.all()\n"
            "    node_nos = [n.no for n in nodes]\n"
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    settle_names, live_names = build_analysis(engine, node_nos, elem_group_names)\n"
            "    print(settle_names)\n"
            "    print(live_names)",
        )
    )
    return "\n".join(lines)


def generate_stage(commands: List[str]) -> str:
    """生成 _10_stage.py：施工阶段"""

    lines = _module_header("STAGE", ["from pyosis.core.engine import OSISEngine"])
    lines.append(
        "def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:"
    )
    lines.append('    """创建施工阶段"""')
    lines.append("")

    # 跟踪当前 stage
    _current_stage = None

    for cmd in commands:
        args = _split_cmd(cmd)
        if not args:
            continue

        if args[0] == "Stage":
            no = args[1]
            name = _val(args[2])
            duration = args[3]
            lines.append(f"    stg = engine.stage.create({no}, {name}, {duration})")
            lines.append("")
            _current_stage = no

        elif args[0] == "StgEle":
            stage_no = args[1]
            eOP = args[2]
            eType = args[3]
            group_name = _val(args[4])
            birth = args[5]
            part = args[6] if len(args) > 6 else "None"
            if stage_no == _current_stage:
                lines.append(
                    f"    stg.define_element({eOP}, {eType}, {group_name}, nBirth={birth}, ePart={part})"
                )
            else:
                lines.append(
                    f"    engine.stage.get({stage_no}).define_element({eOP}, {eType}, {group_name}, nBirth={birth}, ePart={part})"
                )
            lines.append("")

        elif args[0] == "StgBd":
            stage_no = args[1]
            eOP = args[2]
            eType = args[3]
            group_name = _val(args[4])
            if stage_no == _current_stage:
                lines.append(
                    f"    stg.define_boundary({eOP}, {eType}, {group_name})"
                )
            else:
                lines.append(
                    f"    engine.stage.get({stage_no}).define_boundary({eOP}, {eType}, {group_name})"
                )
            lines.append("")

        elif args[0] == "StgLc":
            stage_no = args[1]
            eOP = args[2]
            eType = args[3]
            ref_name = _val(args[4]) if args[4] else '""'
            lc_name = _val(args[5])
            if stage_no == _current_stage:
                lines.append(
                    f"    stg.define_loadcase({eOP}, {eType}, {ref_name}, {lc_name})"
                )
            else:
                lines.append(
                    f"    engine.stage.get({stage_no}).define_loadcase({eOP}, {eType}, {ref_name}, {lc_name})"
                )
            lines.append("")

        elif args[0] == "StgAnal":
            stage_no = args[1]
            eOP = args[2]
            eType = _val(args[3])
            lc_name = _val(args[4])
            if stage_no == _current_stage:
                lines.append(f"    stg.define_analysis({eOP}, {eType}, {lc_name})")
            else:
                lines.append(
                    f"    engine.stage.get({stage_no}).define_analysis({eOP}, {eType}, {lc_name})"
                )
            lines.append("")

        else:
            lines.append(f"    # TODO: {cmd}")

    lines.append("")
    lines.extend(
        _module_footer(
            "STAGE",
            "elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    bd_groups = engine.boundary.group.all()\n"
            "    bd_group_names = [bg.name for bg in bd_groups]\n"
            "    lcs = engine.load.all()\n"
            "    lc_names = [lc.name for lc in lcs]\n"
            "    build_stages(engine, elem_group_names, bd_group_names, lc_names, [], [])",
        )
    )
    return "\n".join(lines)


# ========== 主流程 ==========


def export_command_file() -> Optional[str]:
    """从当前 OSIS 项目导出命令流文件"""
    print("未提供命令流文件，尝试从当前 OSIS 项目导出...")

    try:
        from pyosis.core.engine import OSISEngine

        engine = OSISEngine()
        project_dir = engine.project.get_directory()
        if not project_dir:
            print("导出失败: 未检测到已打开的 OSIS 项目")
            print("\n建议: 请确保 OSIS 软件已打开并加载了项目")
            print("      或手动提供 .out 文件路径: python build.py <文件路径>")
            return None

        export_path = Path(project_dir) / "OSIS.out"
        print(f"正在导出命令流到: {export_path}")
        engine.export_apdl(str(export_path))

        if export_path.exists() and export_path.stat().st_size > 0:
            print(f"导出成功: {export_path}")
            return str(export_path)
        else:
            print("导出失败: 文件未生成或为空")
            return None

    except Exception as e:
        print(f"导出失败: {e}")
        return None


# 模块名到生成函数的映射
MODULE_GENERATORS = {
    "CONTROL": generate_control,
    "PROPERTY": generate_property,
    "MATERIAL": generate_material,
    "SECTION": generate_section,
    "NODE": generate_node,
    "ELEMENT": generate_element,
    "BOUNDARY": generate_boundary,
    "LOADCASE": generate_loadcase,
    "ANALYSIS": generate_analysis,
    "STAGE": generate_stage,
}


def build_project(command_file: Optional[str] = None, output_dir: Optional[str] = None) -> None:
    """从命令流文件构建 Python 项目

    在当前目录自动创建:
    - post/     后处理目录
    - prep/     建模模块目录
    - main.py   主入口文件

    Args:
        command_file: 命令流文件路径 (.out 或 .sml)，为 None 时自动从当前 OSIS 项目导出
        output_dir: 输出目录，为 None 时使用 build.py 所在目录
    """
    # 如果未提供命令流文件，尝试从项目导出
    if command_file is None:
        command_file = export_command_file()
        if command_file is None:
            print("\n错误: 无法获取命令流文件，构建终止")
            sys.exit(1)

    print(f"解析命令流文件: {command_file}")
    modules = parse_command_file(command_file)

    # 获取输出目录
    if output_dir:
        base_dir = Path(output_dir).resolve()
        base_dir.mkdir(parents=True, exist_ok=True)
    else:
        base_dir = Path(__file__).parent.resolve()

    # 创建目录结构
    prep_dir = base_dir / "prep"
    post_dir = base_dir / "post"
    prep_dir.mkdir(exist_ok=True)
    post_dir.mkdir(exist_ok=True)

    # 创建 .gitignore
    gitignore_file = base_dir / ".gitignore"
    gitignore_file.write_text(
        "# Ignore log files\n"
        "*.log\n"
        "\n"
        "# Ignore Python cache\n"
        "__pycache__/\n"
        "*.pyc\n"
        "*.pyo\n",
        encoding="utf-8",
    )
    print("写入: .gitignore")

    # 创建 post/__init__.py
    post_init = post_dir / "__init__.py"
    post_init.write_text('"""后处理模块"""\n', encoding="utf-8")
    print("写入: post/__init__.py")

    # 创建 _0_engine.py
    engine_file = prep_dir / "_0_engine.py"
    engine_file.write_text(
        "from pyosis.core.engine import OSISEngine\n\n"
        "engine = OSISEngine()\n\n"
        "# 自动打开OSIS等操作暂未实现\n"
        "# 目前需要手动打开OSIS并创建项目\n",
        encoding="utf-8",
    )
    print(f"写入: prep/_0_engine.py")

    print(f"生成 Python 文件到: {prep_dir}")

    # 统计 TODO 数量
    total_todos = 0

    for module_name, commands in modules.items():
        if module_name in MODULE_FILES:
            file_name = MODULE_FILES[module_name]
            file_path = prep_dir / file_name

            # 使用专门的生成函数
            generator = MODULE_GENERATORS[module_name]
            python_code = generator(commands)
            file_path.write_text(python_code, encoding="utf-8")

            # 统计 TODO 数量
            todo_count = python_code.count("# TODO")
            total_todos += todo_count

            if todo_count > 0:
                print(f"  创建: prep/{file_name} ({len(commands)} 条命令, {todo_count} 条未转换)")
            else:
                print(f"  创建: prep/{file_name} ({len(commands)} 条命令)")

    if total_todos > 0:
        print(f"\n警告: 共 {total_todos} 条命令未转换 (# TODO)，请手动检查")

    # 创建 main.py（在当前目录）
    main_file = base_dir / "main.py"
    main_content = '''"""
从命令流构建的桥梁建模项目

使用方式:
    python main.py              # 完整建模（自动清空重建）
    python main.py --solve      # 建模后自动运行分析

也可以直接执行单个模块（注意：单独跑某个模块时，OSIS 中应已有对应节点/材料等数据）:
    python prep/_5_node.py   # 只执行节点创建
    python prep/_6_element.py # 只执行单元创建（会从engine读取已有节点）
"""

import argparse

from prep._0_engine import engine
from prep._1_control import setup_control
from prep._2_property import build_property
from prep._3_material import build_materials
from prep._4_section import build_sections
from prep._5_node import build_nodes
from prep._6_element import build_elements
from prep._7_boundary import build_boundaries
from prep._8_loadcase import build_loadcases
from prep._9_analysis import build_analysis
from prep._10_stage import build_stages


def build_model(run_analysis: bool = False):
    """完整的桥梁建模流程（先清空 OSIS 数据，再依次重建所有组件）

    Args:
        run_analysis: 是否自动运行分析，默认 False（只建模）
    """

    print("清空项目...")
    engine.clear()
    engine.clc()

    print("=" * 50)
    print("开始建模")
    print("=" * 50)

    # 1. 全局设置（无依赖）
    print("\\n[1/10] 设置全局控制参数...")
    setup_control(engine)

    # 2. 几何属性（无依赖）
    print("[2/10] 设置几何属性...")
    geo_names = build_property(engine)

    # 3. 材料（无依赖）
    print("[3/10] 创建材料...")
    mat_nos = build_materials(engine)

    # 4. 截面（无依赖）
    print("[4/10] 创建截面...")
    sec_nos = build_sections(engine)

    # 5. 节点（无依赖）
    print("[5/10] 创建节点...")
    node_nos = build_nodes(engine)

    # 6. 单元（依赖节点、截面、材料）
    print("[6/10] 创建单元...")
    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)

    # 7. 边界（依赖节点）
    print("[7/10] 创建边界条件...")
    bd_nos, bd_group_names = build_boundaries(engine, node_nos)

    # 8. 荷载工况（依赖单元、材料、几何）
    print("[8/10] 创建荷载工况...")
    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)

    # 9. 分析设置（依赖节点编号和单元组名称）
    print("[9/10] 创建分析设置...")
    settle_names, live_names = build_analysis(engine, node_nos, elem_group_names)

    # 10. 施工阶段（依赖所有组）
    print("[10/10] 创建施工阶段...")
    build_stages(engine, elem_group_names, bd_group_names, lc_names, settle_names, live_names)

    print("\\n" + "=" * 50)
    print("建模完成！")
    print("=" * 50)

    if run_analysis:
        print("\\n开始运行分析...")
        engine.solve()
        print("分析完成！")
    else:
        print("\\n提示: 调用 engine.solve() 运行分析")

    return engine


def main():
    parser = argparse.ArgumentParser(description='桥梁建模')
    parser.add_argument('--solve', action='store_true',
                        help='建模后自动运行分析')

    args = parser.parse_args()

    # 执行建模（先清空 OSIS 数据，再重建）
    build_model(run_analysis=args.solve)


if __name__ == "__main__":
    main()
'''
    main_file.write_text(main_content, encoding="utf-8")
    print(f"写入: main.py")

    # 创建 post/README.md
    post_readme = post_dir / "README.md"
    post_readme.write_text(
        "# 后处理目录\n\n"
        "此目录用于存放后处理脚本和结果文件。\n\n"
        "例如:\n"
        "- 结果提取脚本\n"
        "- 数据可视化脚本\n"
        "- 报告生成脚本\n",
        encoding="utf-8",
    )

    # 创建 项目画像.md（空架子，由AI后续填写）
    profile_file = base_dir / "项目画像.md"
    profile_content = """# 项目画像

> **说明**：本文件由AI维护。每次构建或修改模型后，AI应自动更新此文件，记录桥梁工程师最关心的设计特征。

## 基本信息
- **桥梁名称**：
- **桥梁体系**：
- **结构形式**：
- **设计规范**：

## 几何参数
- **跨径布置**：
- **桥梁宽度**：
- **梁高**：
- **桥面横坡**：
- **平面线型**：

## 截面特征
- **截面类型**：
- **室数**：
- **顶板厚度**：
- **底板厚度**：
- **腹板厚度**：
- **悬臂长度**：

## 材料
- **混凝土等级**：
- **钢筋等级**：
- **预应力钢束等级**：

## 预应力
- **预应力体系**：
- **钢束类型**：
- **张拉控制应力**：
- **张拉方式**：

## 施工方法
- **施工方式**：
- **节段划分**：
- **挂篮/支架形式**：

## 边界条件
- **支座类型**：
- **支座布置**：
- **特殊约束**：

## 荷载
- **设计荷载等级**：
- **活载类型**：
- **温度荷载**：
- **风荷载**：
- **地震荷载**：

## 分析设置
- **分析方法**：
- **施工阶段数**：
- **成桥状态**：

## 关键控制指标
- **最大挠度**：
- **最大应力**：
- **预应力损失**：
- **收缩徐变**：

---
*最后更新：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    profile_file.write_text(profile_content, encoding="utf-8")
    print(f"创建: 项目画像.md（AI维护的项目画像）")

    print(f"\n完成！共生成 {len(modules)} 个模块文件")
    print("项目结构:")
    print(f"  {base_dir.name}/")
    print(f"  ├── build.py")
    print(f"  ├── main.py")
    print(f"  ├── post/")
    print(f"  └── prep/")
    print("\n提示:")
    print("  1. 生成的代码可直接运行，但部分复杂命令标记为 # TODO 需要手动检查")
    print("  2. 建议先运行单个模块测试：python prep/_5_node.py")
    print("  3. 完整建模：python main.py")


def build_from_sml(sml_file: str, output_dir: Optional[str] = None) -> None:
    """从 .sml 模型文件构建 Python 项目

    流程:
        1. 导入 .sml 到 OSIS
        2. 导出 OSIS.out 命令流
        3. 使用 build_project 生成 Python 项目

    Args:
        sml_file: .sml 文件路径
        output_dir: 输出目录，为 None 时在 .sml 同级目录创建项目
    """
    sml_path = Path(sml_file).resolve()
    if not sml_path.exists():
        print(f"错误: 文件不存在: {sml_path}")
        sys.exit(1)

    if not sml_path.suffix.lower() == ".sml":
        print(f"错误: 不是 .sml 文件: {sml_path}")
        sys.exit(1)

    # 确定输出目录
    if output_dir is None:
        output_dir = sml_path.parent / sml_path.stem
    else:
        output_dir = Path(output_dir).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)

    # 临时目录用于存放导出的 OSIS.out
    import tempfile
    temp_dir = tempfile.mkdtemp(prefix="osis_build_")
    temp_out = Path(temp_dir) / "OSIS.out"

    try:
        print(f"\n{'='*50}")
        print(f"处理: {sml_path.name}")
        print(f"{'='*50}")

        # 导入 .sml 到 OSIS
        print(f"\n[1/3] 导入 .sml 到 OSIS...")
        try:
            from pyosis.core.engine import OSISEngine
            engine = OSISEngine()
            print("  清空当前项目...")
            engine.clear()
            engine.clc()
            print(f"  导入: {sml_path}")
            engine.import_apdl(str(sml_path))
            print("  导入成功")
        except Exception as e:
            print(f"导入失败: {e}")
            print("\n建议: 请确保 OSIS 软件已打开")
            sys.exit(1)

        # 导出 OSIS.out
        print(f"\n[2/3] 导出命令流...")
        try:
            engine.export_apdl(str(temp_out))
            if temp_out.exists() and temp_out.stat().st_size > 0:
                print(f"  导出成功: {temp_out}")
            else:
                print("  导出失败: 文件未生成或为空")
                sys.exit(1)
        except Exception as e:
            print(f"导出失败: {e}")
            sys.exit(1)

        # 构建 Python 项目
        print(f"\n[3/3] 生成 Python 项目...")
        build_project(str(temp_out), str(output_dir))

        print(f"\n{'='*50}")
        print(f"完成: {output_dir}")
        print(f"{'='*50}")

    finally:
        # 清理临时文件
        import shutil
        if Path(temp_dir).exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    command_file = sys.argv[1] if len(sys.argv) > 1 else None

    if command_file is None:
        print("用法: python build.py [command_file]")
        print("示例:")
        print("  python build.py                    # 自动从当前 OSIS 项目导出")
        print("  python build.py C:/Temp/OSIS.out   # 从 .out 文件生成")
        print("  python build.py C:/Temp/model.sml  # 从 .sml 文件导入并生成")
        print("")
        build_project(None)
    elif command_file.lower().endswith(".sml"):
        # 从 .sml 文件构建
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        build_from_sml(command_file, output_dir)
    else:
        # 从 .out 文件构建
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        build_project(command_file, output_dir)
