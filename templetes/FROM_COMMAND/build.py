#!/usr/bin/env python3
"""从 OSIS 命令流文件构建 Python 建模项目骨架

增强版特性：
1. 命令路由：自动识别多态命令（如 Boundary/GENERAL vs Boundary/MSTSLV）
2. 结构化注释：利用 pyosis REGISTRY 中的参数定义生成带语义的注释
3. 自动代码生成：简单命令（Node, Material, Beam3D 等）直接生成 pyosis 代码
4. 编号索引追踪：建立跨模块编号引用表，降低 AI 理解难度

用法:
    python build.py <command_file> [output_dir]
    
示例:
    python build.py C:/Temp/OSIS.out ./prep
"""

import re
import sys
import inspect
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# ──────────────────────────────────────────────
# 配置区
# ──────────────────────────────────────────────

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

# 创建命令时会生成对象的模块（用于编号追踪）
OBJECT_CREATING_MODULES = {
    "MATERIAL": "material",
    "SECTION": "section",
    "NODE": "node",
    "ELEMENT": "element",
    "BOUNDARY": "boundary",
}


# ──────────────────────────────────────────────
# 命令路由配置
# ──────────────────────────────────────────────

# 多态命令路由表：命令名 → {识别字段索引, 子类型路由}
CMD_ROUTER = {
    "Boundary": {
        "dispatcher_field": 2,
        "routes": {
            "GENERAL": {
                "engine_method": "engine.boundary.create_general",
                "param_map": ["no", "nCoor", "bX", "bY", "bZ", "bRX", "bRY", "bRZ", "bRW"],
                "skip_params": [1],  # 跳过 eBoundaryType
                "description": "一般支撑",
            },
            "MSTSLV": {
                "engine_method": "engine.boundary.create_master_slave",
                "param_map": ["no", "nNode", "bX", "bY", "bZ", "bRX", "bRY", "bRZ"],
                "skip_params": [1],
                "description": "主从约束",
            },
            "RELEASE": {
                "engine_method": "engine.boundary.create_release",
                "param_map": ["no", "Fxi_state", "Fyi_state", "Fzi_state", "Mxi_state", "Myi_state", "Mzi_state", "Mbi_state",
                             "Fxi", "Fyi", "Fzi", "Mxi", "Myi", "Mzi", "Mbi",
                             "Fxj_state", "Fyj_state", "Fzj_state", "Mxj_state", "Myj_state", "Mzj_state", "Mbj_state",
                             "Fxj", "Fyj", "Fzj", "Mxj", "Myj", "Mzj", "Mbj"],
                "skip_params": [1],
                "description": "释放梁端约束",
            },
            "ELSTCSPT": {
                "engine_method": "engine.boundary.create_elstcspt",
                "param_map": ["no", "nCoor", "bX", "DX", "bY", "DY", "bZ", "DZ", "bRX", "RX", "bRY", "RY", "bRZ", "RZ"],
                "skip_params": [1],
                "description": "弹性支承",
            },
            "RIGID": {
                "engine_method": "engine.boundary.create_rigid",
                "param_map": ["no", "nNodeI"],
                "skip_params": [1],
                "description": "刚性连接",
            },
            "GES": {
                "engine_method": "engine.boundary.create_general_elstcspt",
                "param_map": ["no", "nCoor"],
                "varargs": True,
                "skip_params": [1],
                "description": "一般弹性支承",
            },
            "SECF": {
                "engine_method": "engine.boundary.create_section_factor",
                "param_map": ["no", "Area", "Sy", "Sz", "Ixx", "Iyy", "Izz", "Iww", "W"],
                "skip_params": [1],
                "description": "截面系数",
            },
        }
    },
    "Element": {
        "dispatcher_field": 2,
        "routes": {
            "BEAM3D": {
                "engine_method": "engine.element.create_beam3d",
                "param_map": ["no", "node1", "node2", "nMat", "nSec1", "nSec2", "nYTrans", "nZTrans", "dStrain", "bFlag", "dTheta", "bWarping"],
                "skip_params": [1],
                "description": "梁单元",
            },
            "TRUSS": {
                "engine_method": "engine.element.create_truss",
                "param_map": ["no", "node1", "node2", "nMat", "nSec1", "nSec2", "dStrain"],
                "skip_params": [1],
                "description": "桁架单元",
            },
            "SPRING": {
                "engine_method": "engine.element.create_spring",
                "param_map": ["no", "node1", "node2", "bLinear", "dx", "dy", "dz", "rx", "ry", "rz", "dBeta"],
                "skip_params": [1],
                "description": "弹簧单元",
            },
            "CABLE": {
                "engine_method": "engine.element.create_cable",
                "param_map": ["no", "node1", "node2", "nMat", "nSec", "eMethod", "dPara"],
                "skip_params": [1],
                "description": "拉索单元",
            },
            "SHELL": {
                "engine_method": "engine.element.create_shell",
                "param_map": ["no", "bIsThin", "nMat", "nThk", "node1", "node2", "node3", "node4"],
                "skip_params": [1],
                "description": "壳单元",
            },
        }
    },
    "Material": {
        "dispatcher_field": 3,
        "routes": {
            "CONC": {
                "engine_method": "engine.material.create_conc",
                "param_map": ["no", "strName", "eCode", "eGrade", "nCrepShrk", "dDmp"],
                "skip_params": [2],  # 跳过 eMaterialType
                "description": "混凝土",
            },
            "STEEL": {
                "engine_method": "engine.material.create_steel",
                "param_map": ["no", "strName", "eCode", "eGrade", "dDmp"],
                "skip_params": [2],
                "description": "钢材",
            },
            "PRESTRESSED": {
                "engine_method": "engine.material.create_prestressed",
                "param_map": ["no", "strName", "eCode", "eGrade", "dDmp"],
                "skip_params": [2],
                "description": "预应力",
            },
            "REBAR": {
                "engine_method": "engine.material.create_rebar",
                "param_map": ["no", "strName", "eCode", "eGrade", "dDmp"],
                "skip_params": [2],
                "description": "钢筋",
            },
            "CUSTOM": {
                "engine_method": "engine.material.create_custom",
                "param_map": ["no", "strName", "dE", "dG", "dMu", "dExpCoeff", "dUnitWeight", "dDensity", "dDmp"],
                "skip_params": [2],
                "description": "自定义材料",
            },
        }
    },
}

# 单态命令直接映射：命令名 → Engine API
SIMPLE_CMD_MAP = {
    "Node": {
        "engine_method": "engine.node.create",
        "param_map": ["no", "x", "y", "z"],
        "creates_object": True,
        "object_type": "node",
    },
    "NodeDel": {
        "engine_method": "engine.node.delete",
        "param_map": ["no"],
    },
    "NodeMod": {
        "engine_method": "engine.node.renumber",
        "param_map": ["old_no", "new_no"],
    },
    "MaterialDel": {
        "engine_method": "engine.material.delete",
        "param_map": ["no"],
    },
    "MaterialMod": {
        "engine_method": "engine.material.renumber",
        "param_map": ["old_no", "new_no"],
    },
    "ElementDel": {
        "engine_method": "engine.element.delete",
        "param_map": ["no"],
    },
    "ElementMod": {
        "engine_method": "engine.element.renumber",
        "param_map": ["old_no", "new_no"],
    },
    "SecDel": {
        "engine_method": "engine.section.delete",
        "param_map": ["no"],
    },
    "SecMod": {
        "engine_method": "engine.section.renumber",
        "param_map": ["old_no", "new_no"],
    },
    # 控制参数
    "Acel": {
        "engine_method": "engine.control.set_gravity_acceleration",
        "param_map": ["dG"],
    },
    "CalcTendon": {
        "engine_method": "engine.control.set_calc_tendon",
        "param_map": ["bFlag"],
    },
    "CalcConForce": {
        "engine_method": "engine.control.set_calc_concurrent_force",
        "param_map": ["bFlag"],
    },
    "CalcShrink": {
        "engine_method": "engine.control.set_calc_shrink",
        "param_map": ["bFlag"],
    },
    "CalcCreep": {
        "engine_method": "engine.control.set_calc_creep",
        "param_map": ["bFlag"],
    },
    "CalcShear": {
        "engine_method": "engine.control.set_calc_shear",
        "param_map": ["bFlag"],
    },
    "CalcRlx": {
        "engine_method": "engine.control.set_calc_relaxation",
        "param_map": ["bFlag"],
    },
    "ModLocCoor": {
        "engine_method": "engine.control.set_mod_loc_coor",
        "param_map": ["bFlag"],
    },
    "IncTendon": {
        "engine_method": "engine.control.set_inc_tendon",
        "param_map": ["bFlag"],
    },
    # 荷载工况
    "LoadCase": {
        "engine_method": "engine.load.create",
        "param_map": ["strName", "eLoadCaseType", "dScalar", "strPrompt"],
        "creates_object": True,
        "object_type": "loadcase",
    },
    "LoadCaseDel": {
        "engine_method": "engine.load.delete",
        "param_map": ["strName"],
    },
    "LCMod": {
        "engine_method": "engine.load.rename",
        "param_map": ["strOldName", "strNewName"],
    },
    # 单元组
    "EleGrp": {
        "engine_method": "engine.element.group",
        "param_map": ["strName", "eOP", "param"],
        "is_group_op": True,
    },
    # 边界组
    "BdGrp": {
        "engine_method": "engine.boundary.group",
        "param_map": ["strName", "eOP", "param"],
        "is_group_op": True,
    },
    # 分配边界
    "AsgnBd": {
        "engine_method": "engine.boundary.assign",
        "param_map": ["nBd", "eOP", "param"],
    },
}


# ──────────────────────────────────────────────
# 解析器
# ──────────────────────────────────────────────

def parse_command_file(file_path: str) -> Dict[str, List[str]]:
    """解析命令流文件，按模块分割"""
    file_path = Path(file_path)
    
    content = None
    for encoding in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
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
    
    for line in lines:
        stripped = line.strip()
        match = module_pattern.match(stripped)
        if match:
            module_name = match.group(1).upper()
            if module_name in MODULE_FILES:
                current_module = module_name
                modules[current_module] = []
            continue
        
        if stripped.startswith("//") or not stripped:
            continue
            
        if current_module:
            modules[current_module].append(stripped.rstrip(";"))
    
    return modules


# ──────────────────────────────────────────────
# 命令路由与解析
# ──────────────────────────────────────────────

def route_command(parts: List[str]) -> Tuple[Optional[str], Optional[Dict], str]:
    """路由命令到对应的 Engine API
    
    Returns:
        (engine_method, route_info, description)
        engine_method: 对应的 Engine API 方法名，None 表示无法路由
        route_info: 路由配置字典
        description: 描述信息
    """
    if not parts:
        return None, None, "空命令"
    
    cmd_name = parts[0]
    
    # 尝试多态路由
    if cmd_name in CMD_ROUTER:
        router = CMD_ROUTER[cmd_name]
        field_idx = router["dispatcher_field"]
        
        if field_idx < len(parts):
            sub_type = parts[field_idx].upper()
            if sub_type in router["routes"]:
                route_info = router["routes"][sub_type]
                return route_info["engine_method"], route_info, route_info["description"]
            else:
                return None, None, f"未知子类型: {sub_type}"
        else:
            return None, None, f"参数不足，无法识别子类型"
    
    # 尝试单态映射
    if cmd_name in SIMPLE_CMD_MAP:
        route_info = SIMPLE_CMD_MAP[cmd_name]
        return route_info["engine_method"], route_info, route_info.get("description", cmd_name)
    
    return None, None, f"未映射命令"


def parse_params(parts: List[str], route_info: Dict) -> Dict[str, Any]:
    """根据路由配置解析参数
    
    返回参数字典 {参数名: 值}
    """
    params = {}
    param_map = route_info.get("param_map", [])
    skip_params = route_info.get("skip_params", [])
    varargs = route_info.get("varargs", False)
    
    # 命令名占 parts[0]，所以参数从 parts[1:] 开始
    # 但要跳过被标记为 skip 的参数（如类型标记）
    param_idx = 0
    for i, part in enumerate(parts[1:], start=1):
        if i in skip_params:
            continue
        
        if param_idx < len(param_map):
            param_name = param_map[param_idx]
            params[param_name] = part
            param_idx += 1
        elif varargs:
            # 变长参数，用索引存储
            params[f"param_{param_idx}"] = part
            param_idx += 1
        else:
            # 多余参数，忽略或标记
            params[f"extra_{i}"] = part
    
    return params


def format_param_value(value: str, param_name: str = "") -> str:
    """格式化参数值为 Python 代码中的字符串"""
    if value == "" or value is None:
        return '""'
    
    # 尝试判断是否为数字
    try:
        float_val = float(value)
        # 如果是整数形式
        if float_val == int(float_val):
            return str(int(float_val))
        return str(float_val)
    except (ValueError, TypeError):
        pass
    
    # 字符串值，需要转义
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def generate_pyosis_call(engine_method: str, params: Dict[str, Any], 
                         cmd_line: str, description: str) -> List[str]:
    """生成 pyosis API 调用代码和注释
    
    Returns:
        代码行列表（包含注释和代码）
    """
    lines = []
    
    # 生成注释
    lines.append(f"    # [{cmd_line.split(',')[0]}] {description}")
    lines.append(f"    # 原始命令: {cmd_line}")
    
    # 生成参数注释
    param_comments = []
    for name, value in params.items():
        if name.startswith("extra_"):
            param_comments.append(f"    #   [额外参数] {value}")
        else:
            param_comments.append(f"    #   {name}={value}")
    
    if param_comments:
        lines.append("    # 参数:")
        lines.extend(param_comments)
    
    # 生成代码调用
    if not params:
        lines.append(f"    {engine_method}()")
    else:
        # 构建关键字参数
        kwargs = []
        for name, value in params.items():
            if name.startswith("extra_"):
                continue
            formatted = format_param_value(value, name)
            kwargs.append(f"{name}={formatted}")
        
        kwargs_str = ", ".join(kwargs)
        lines.append(f"    {engine_method}({kwargs_str})")
    
    return lines


# ──────────────────────────────────────────────
# 编号索引追踪
# ──────────────────────────────────────────────

class IndexTracker:
    """跨模块编号索引追踪器"""
    
    def __init__(self):
        # object_type → {原始编号 → 列表索引}
        self.indices: Dict[str, Dict[str, int]] = {}
        # object_type → 当前列表长度
        self.counters: Dict[str, int] = {}
    
    def add(self, obj_type: str, original_id: str):
        """添加一个对象到索引"""
        if obj_type not in self.indices:
            self.indices[obj_type] = {}
            self.counters[obj_type] = 0
        
        if original_id not in self.indices[obj_type]:
            self.indices[obj_type][original_id] = self.counters[obj_type]
            self.counters[obj_type] += 1
    
    def get_ref(self, obj_type: str, original_id: str) -> Optional[str]:
        """获取对象引用表达式，如 node_nos[0]"""
        if obj_type in self.indices and original_id in self.indices[obj_type]:
            idx = self.indices[obj_type][original_id]
            return f"{obj_type}_nos[{idx}]"
        return None
    
    def get_list_name(self, obj_type: str) -> str:
        """获取对象列表变量名，如 node_nos"""
        return f"{obj_type}_nos"
    
    def generate_index_comment(self) -> List[str]:
        """生成编号索引注释"""
        lines = []
        lines.append("    # ========== 跨模块编号索引 ==========")
        
        for obj_type, id_map in self.indices.items():
            list_name = self.get_list_name(obj_type)
            lines.append(f"    # {list_name} 索引:")
            for orig_id, idx in sorted(id_map.items(), key=lambda x: x[1]):
                lines.append(f"    #   [{idx}] = {obj_type} {orig_id}")
        
        return lines


def build_index_from_commands(modules: Dict[str, List[str]]) -> IndexTracker:
    """从所有模块的命令中构建编号索引"""
    tracker = IndexTracker()
    
    # 第一遍扫描：收集创建命令的对象编号
    for module_name, commands in modules.items():
        obj_type = OBJECT_CREATING_MODULES.get(module_name)
        if not obj_type:
            continue
        
        for cmd in commands:
            parts = cmd.split(',')
            if not parts:
                continue
            
            cmd_name = parts[0]
            
            # 根据命令名判断是否为创建命令
            if cmd_name in CMD_ROUTER:
                # 多态命令
                router = CMD_ROUTER[cmd_name]
                field_idx = router["dispatcher_field"]
                if field_idx < len(parts):
                    sub_type = parts[field_idx].upper()
                    if sub_type in router["routes"]:
                        # 编号通常是第一个参数（parts[1]）
                        if len(parts) > 1:
                            tracker.add(obj_type, parts[1])
            elif cmd_name in SIMPLE_CMD_MAP:
                route_info = SIMPLE_CMD_MAP[cmd_name]
                if route_info.get("creates_object"):
                    if len(parts) > 1:
                        tracker.add(obj_type, parts[1])
            
            # 特殊处理：Node 命令
            if cmd_name == "Node" and len(parts) > 1:
                tracker.add("node", parts[1])
            # 特殊处理：LoadCase 命令
            if cmd_name == "LoadCase" and len(parts) > 1:
                tracker.add("loadcase", parts[1])
    
    return tracker


# ──────────────────────────────────────────────
# 模块文件生成
# ──────────────────────────────────────────────

def generate_module(module_name: str, commands: List[str], tracker: IndexTracker) -> str:
    """生成模块 Python 文件（增强版）
    
    特性：
    1. 对简单命令直接生成 pyosis 代码
    2. 对多态命令生成带路由注释的结构化代码
    3. 对未知命令保留原始命令流注释
    """
    title = MODULE_NAMES.get(module_name, module_name)
    func_name = module_name.lower()
    
    # 根据模块确定函数签名
    signatures = {
        "CONTROL": ("def setup_control(engine: OSISEngine) -> None:", "    return\n"),
        "PROPERTY": ("def build_property(engine: OSISEngine) -> list[str]:", "    return []\n"),
        "MATERIAL": ("def build_materials(engine: OSISEngine) -> list[int]:", "    return []\n"),
        "SECTION": ("def build_sections(engine: OSISEngine) -> list[int]:", "    return []\n"),
        "NODE": ("def build_nodes(engine: OSISEngine) -> list[int]:", "    return []\n"),
        "ELEMENT": ("def build_elements(engine: OSISEngine, mat_nos: list[int], sec_nos: list[int], node_nos: list[int]) -> tuple[list[int], list[str]]:", "    return [], []\n"),
        "BOUNDARY": ("def build_boundaries(engine: OSISEngine, node_nos: list[int]) -> tuple[list[int], list[str]]:", "    return [], []\n"),
        "LOADCASE": ("def build_loadcases(engine: OSISEngine, geo_names: list[str], mat_nos: list[int], elem_nos: list[int], elem_group_names) -> list[str]:", "    return []\n"),
        "ANALYSIS": ("def build_live_analysis(engine: OSISEngine, elem_group_names) -> list[str]:", "    return []\n"),
        "STAGE": ("def build_stages(engine: OSISEngine, elem_group_names, bd_group_names, lc_names, settle_names, live_names) -> None:", ""),
    }
    
    signature, return_type = signatures.get(module_name, (f"def build_{func_name}(engine: OSISEngine):", ""))
    
    lines = [
        f'"""{title}"""',
        "",
        "from pyosis.core.engine import OSISEngine",
        "",
        signature,
        f'    """{title}"""',
        "",
    ]
    
    # 如果是创建对象的模块，生成收集列表的代码
    obj_type = OBJECT_CREATING_MODULES.get(module_name)
    created_objects = []
    
    if obj_type:
        list_name = tracker.get_list_name(obj_type)
        lines.append(f"    {list_name} = []")
        lines.append("")
    
    # 逐条处理命令
    for cmd in commands:
        parts = cmd.split(',')
        engine_method, route_info, description = route_command(parts)
        
        if engine_method and route_info:
            # 可以路由的命令
            params = parse_params(parts, route_info)
            
            # 检查是否需要替换编号为索引引用
            # 对于创建命令，将 no 参数记录
            if route_info.get("creates_object"):
                if "no" in params:
                    created_objects.append(params["no"])
            
            call_lines = generate_pyosis_call(engine_method, params, cmd, description)
            lines.extend(call_lines)
            lines.append("")
        else:
            # 无法路由的命令，保留原始注释
            lines.append(f"    # [TODO] 未识别命令: {cmd}")
            lines.append(f"    # 提示: {description}")
            lines.append("")
    
    # 返回对象列表
    if obj_type and created_objects:
        list_name = tracker.get_list_name(obj_type)
        lines.append(f"    return {list_name}")
    elif return_type:
        lines.append(return_type.rstrip())
    
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    from ._0_engine import engine")
    
    # 根据模块生成对应的测试代码
    test_codes = {
        "CONTROL": "    setup_control(engine)",
        "PROPERTY": "    geo_names = build_property(engine)\n    print(geo_names)\n    print(engine.geometry.all())",
        "MATERIAL": "    mat_nos = build_materials(engine)\n    print(mat_nos)\n    print(engine.material.all())",
        "SECTION": "    sec_nos = build_sections(engine)\n    print(sec_nos)\n    print(engine.section.all())",
        "NODE": "    node_nos = build_nodes(engine)\n    print(node_nos)\n    print(engine.node.all())",
        "ELEMENT": (
            "    mats = engine.material.all()\n"
            "    mat_nos = [m.no for m in mats]\n"
            "    secs = engine.section.all()\n"
            "    sec_nos = [s.no for s in secs]\n"
            "    nodes = engine.node.all()\n"
            "    node_nos = [n.no for n in nodes]\n"
            "    elem_nos, elem_group_names = build_elements(engine, mat_nos, sec_nos, node_nos)\n"
            "    print(elem_nos)\n"
            "    print(elem_group_names)\n"
            "    print(engine.element.all())\n"
            "    print(engine.element.group.all())"
        ),
        "BOUNDARY": (
            "    nodes = engine.node.all()\n"
            "    node_nos = [n.no for n in nodes]\n"
            "    bd_nos, bd_groups = build_boundaries(engine, node_nos)\n"
            "    print(bd_nos)\n"
            "    print(bd_groups)\n"
            "    print(engine.boundary.all())\n"
            "    print(engine.boundary.group.all())"
        ),
        "LOADCASE": (
            "    mats = engine.material.all()\n"
            "    mat_nos = [m.no for m in mats]\n"
            "    elems = engine.element.all()\n"
            "    elem_nos = [e.no for e in elems]\n"
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    geos = engine.geometry.all()\n"
            "    geo_names = [s.name for s in geos]\n"
            "    lc_names = build_loadcases(engine, geo_names, mat_nos, elem_nos, elem_group_names)\n"
            "    print(lc_names)\n"
            "    print(engine.load.all())"
        ),
        "ANALYSIS": (
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    live_names = build_live_analysis(engine, elem_group_names)\n"
            "    print(live_names)"
        ),
        "STAGE": (
            "    elem_groups = engine.element.group.all()\n"
            "    elem_group_names = [eg.name for eg in elem_groups]\n"
            "    bd_groups = engine.boundary.group.all()\n"
            "    bd_group_names = [bg.name for bg in bd_groups]\n"
            "    lcs = engine.load.all()\n"
            "    lc_names = [lc.name for lc in lcs]\n"
            "    live_names = []\n"
            "    settle_names = []\n"
            "    build_stages(engine, elem_group_names, bd_group_names, lc_names, settle_names, live_names)"
        ),
    }
    
    lines.append(test_codes.get(module_name, f"    build_{func_name}(engine)"))
    
    return "\n".join(lines)


# ──────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────

def build_project(command_file: str, output_dir: str = "./prep") -> None:
    """从命令流文件构建 Python 项目骨架"""
    print(f"解析命令流文件: {command_file}")
    modules = parse_command_file(command_file)
    
    print("构建跨模块编号索引...")
    tracker = build_index_from_commands(modules)
    
    # 打印索引信息
    print(f"  发现对象:")
    for obj_type, id_map in tracker.indices.items():
        print(f"    {obj_type}: {len(id_map)} 个")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 创建 _0_engine.py
    engine_file = output_path / "_0_engine.py"
    if not engine_file.exists():
        engine_file.write_text(
            "from pyosis.core.engine import OSISEngine\n\n"
            "engine = OSISEngine()\n\n"
            "# 自动打开OSIS等操作暂未实现\n"
            "# 目前需要手动打开OSIS并创建项目\n",
            encoding="utf-8"
        )
        print(f"创建: _0_engine.py")
    
    print(f"生成 Python 文件到: {output_path}")
    
    for module_name, commands in modules.items():
        if module_name in MODULE_FILES:
            file_name = MODULE_FILES[module_name]
            file_path = output_path / file_name
            
            python_code = generate_module(module_name, commands, tracker)
            file_path.write_text(python_code, encoding="utf-8")
            
            # 统计转换情况
            total = len(commands)
            routed = sum(1 for cmd in commands if route_command(cmd.split(','))[0] is not None)
            print(f"  创建: {file_name} ({total} 条命令, {routed} 条已路由, {total-routed} 条待处理)")
    
    # 创建 main.py
    main_file = output_path.parent / "main.py"
    if not main_file.exists():
        main_content = '''"""
从命令流构建的桥梁建模项目

使用方式:
    python main.py              # 完整建模（默认清空重建）
    python main.py --increment  # 增量模式：不清空，幂等执行
    
也可以直接执行单个模块:
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
from prep._9_analysis import build_live_analysis
from prep._10_stage import build_stages


def build_model(incremental: bool = False, run_analysis: bool = False):
    """完整的桥梁建模流程
    
    Args:
        incremental: 是否增量模式（不清空），默认 False（清空重建）
        run_analysis: 是否自动运行分析，默认 False（只建模）
    """

    if not incremental:
        print("清空项目...")
        engine.clear()
        engine.clc()

    print("=" * 50)
    print("开始建模" + ("（增量模式）" if incremental else "（清空重建）"))
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
    
    # 9. 分析设置（依赖单元组）
    print("[9/10] 创建分析设置...")
    live_names = build_live_analysis(engine, elem_group_names)
    
    # 10. 施工阶段（依赖所有组）
    print("[10/10] 创建施工阶段...")
    build_stages(engine, elem_group_names, bd_group_names, lc_names, [], live_names)
    
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
    parser.add_argument('--increment', action='store_true', 
                        help='增量模式：不清空（默认清空重建）')
    parser.add_argument('--solve', action='store_true',
                        help='建模后自动运行分析')
    
    args = parser.parse_args()
    
    # 执行建模（默认清空重建）
    build_model(incremental=args.increment, run_analysis=args.solve)


if __name__ == "__main__":
    main()
'''
        main_file.write_text(main_content, encoding="utf-8")
        print(f"创建: main.py")
    
    print(f"\n完成！共生成 {len(modules)} 个模块文件")
    print("提示:")
    print("  - 已路由的命令已生成带注释的 pyosis 代码骨架")
    print("  - 标记为 [TODO] 的命令需要手动转换")
    print("  - 请检查参数中的编号引用是否需要替换为索引（如 node_nos[0]）")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python build.py <command_file> [output_dir]")
        print("示例: python build.py C:/Temp/OSIS.out ./prep")
        sys.exit(1)
    
    command_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./prep"
    
    build_project(command_file, output_dir)
