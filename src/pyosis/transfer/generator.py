"""pyosis 代码生成器

将解析后的命令流转换为 pyosis Engine API 代码。

用法:
    from pyosis.transfer.generator import PyosisGenerator
    from pyosis.transfer.parser import CommandParser
    
    parser = CommandParser()
    modules = parser.parse_file("path/to/OSIS.out")
    
    generator = PyosisGenerator()
    code = generator.generate_module("MATERIAL", modules["MATERIAL"])
    print(code)
"""

from typing import Dict, List, Optional, NamedTuple
from .parser import ParsedCommand
from .command_map import CommandMapping


class ObjectIndex(NamedTuple):
    """对象索引信息"""
    original_id: str        # 原始编号（命令流中的编号）
    list_index: int         # 在列表中的索引
    obj_type: str           # 对象类型


class IndexTracker:
    """跨模块对象编号索引追踪器"""
    
    def __init__(self):
        # {对象类型: {原始编号: 索引}}
        self._indices: Dict[str, Dict[str, int]] = {}
        self._counters: Dict[str, int] = {}
    
    def register(self, obj_type: str, original_id: str) -> int:
        """注册一个对象编号
        
        Returns:
            分配的列表索引
        """
        if obj_type not in self._indices:
            self._indices[obj_type] = {}
            self._counters[obj_type] = 0
        
        if original_id not in self._indices[obj_type]:
            self._indices[obj_type][original_id] = self._counters[obj_type]
            self._counters[obj_type] += 1
        
        return self._indices[obj_type][original_id]
    
    def get_ref(self, obj_type: str, original_id: str) -> Optional[str]:
        """获取对象引用表达式
        
        Returns:
            如 "node_nos[0]"，如果未注册则返回 None
        """
        if obj_type in self._indices and original_id in self._indices[obj_type]:
            idx = self._indices[obj_type][original_id]
            return f"{obj_type}_nos[{idx}]"
        return None
    
    def get_list_name(self, obj_type: str) -> str:
        """获取对象列表变量名"""
        return f"{obj_type}_nos"
    
    def build_from_commands(self, modules: Dict[str, List[ParsedCommand]]) -> "IndexTracker":
        """从所有模块命令中构建索引"""
        # 对象类型到模块的映射
        MODULE_TO_TYPE = {
            "MATERIAL": "material",
            "NODE": "node",
            "ELEMENT": "element",
            "BOUNDARY": "boundary",
            "SECTION": "section",
            "LOADCASE": "loadcase",
        }
        
        for module_name, commands in modules.items():
            obj_type = MODULE_TO_TYPE.get(module_name)
            if not obj_type:
                continue
            
            for cmd in commands:
                if cmd.mapping and cmd.mapping.creates_object:
                    # 创建命令的编号通常是 parts[1]
                    if len(cmd.parts) > 1:
                        self.register(obj_type, cmd.parts[1])
        
        return self
    
    def generate_index_comment(self) -> List[str]:
        """生成编号索引注释"""
        lines = ["    # 跨模块编号索引:"]
        for obj_type, id_map in sorted(self._indices.items()):
            list_name = self.get_list_name(obj_type)
            lines.append(f"    #   {list_name}: {len(id_map)} 个对象")
            for orig_id, idx in sorted(id_map.items(), key=lambda x: x[1]):
                lines.append(f"    #     [{idx}] = {orig_id}")
        return lines


class PyosisGenerator:
    """pyosis 代码生成器"""
    
    def __init__(self, tracker: Optional[IndexTracker] = None):
        self.tracker = tracker or IndexTracker()
    
    def format_value(self, value: str) -> str:
        """格式化参数值为 Python 代码字符串"""
        if value == "" or value is None:
            return '""'
        
        # 尝试判断是否为数字
        try:
            float_val = float(value)
            if float_val == int(float_val):
                return str(int(float_val))
            return str(float_val)
        except (ValueError, TypeError):
            pass
        
        # 字符串值，需要转义
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    
    def generate_param_comment(self, param_name: str, value: str) -> str:
        """生成参数注释行"""
        return f"    #   {param_name}={value}"
    
    def generate_pyosis_call(self, cmd: ParsedCommand) -> List[str]:
        """生成单条命令的 pyosis 调用代码
        
        Returns:
            代码行列表（包含注释和代码）
        """
        lines = []
        mapping = cmd.mapping
        
        if mapping is None:
            # 未映射的命令
            lines.append(f"    # [TODO] 未映射命令: {cmd.raw}")
            return lines
        
        # 生成注释头
        sub_type = cmd.parts[mapping.params.index("no") + 1] if "no" in mapping.params and len(cmd.parts) > 2 else ""
        type_info = f"/{sub_type}" if sub_type and mapping.object_type else ""
        lines.append(f"    # [{cmd.name}{type_info}] {mapping.description}")
        lines.append(f"    # 原始命令: {cmd.raw}")
        
        # 解析参数
        kwargs = []
        param_comments = []
        
        # 命令名占 parts[0]，参数从 parts[1:] 开始
        # 但需要根据映射跳过某些字段
        param_idx = 0
        
        # 获取 dispatcher 字段索引（用于跳过类型标记）
        from .command_map import DISPATCHER_CONFIG
        dispatcher_idx = DISPATCHER_CONFIG.get(cmd.name, -1)
        
        for i, part in enumerate(cmd.parts[1:], start=1):
            # 跳过 dispatcher 字段（类型标记）
            if i == dispatcher_idx:
                continue
            
            if param_idx < len(mapping.params):
                param_name = mapping.params[param_idx]
                param_comments.append(self.generate_param_comment(param_name, part))
                
                # 格式化参数值
                formatted = self.format_value(part)
                kwargs.append(f"{param_name}={formatted}")
                param_idx += 1
            else:
                # 多余参数
                param_comments.append(f"    #   [额外参数] {part}")
        
        # 添加参数注释
        if param_comments:
            lines.append("    # 参数:")
            lines.extend(param_comments)
        
        # 生成代码调用
        kwargs_str = ", ".join(kwargs)
        lines.append(f"    {mapping.engine_method}({kwargs_str})")
        
        return lines
    
    def generate_module(self, module_name: str, commands: List[ParsedCommand]) -> str:
        """生成模块 Python 文件
        
        Args:
            module_name: 模块名（如 "MATERIAL", "NODE"）
            commands: 该模块的命令列表
            
        Returns:
            Python 代码字符串
        """
        # 模块标题映射
        MODULE_TITLES = {
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
        
        # 函数签名映射
        MODULE_SIGNATURES = {
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
        
        title = MODULE_TITLES.get(module_name, module_name)
        signature, return_stmt = MODULE_SIGNATURES.get(module_name, (f"def build_{module_name.lower()}(engine: OSISEngine):", ""))
        
        lines = [
            f'"""{title}"""',
            "",
            "from pyosis.core.engine import OSISEngine",
            "",
            signature,
            f'    """{title}"""',
            "",
        ]
        
        # 确定该模块是否创建对象
        MODULE_TO_TYPE = {
            "MATERIAL": "material",
            "NODE": "node",
            "ELEMENT": "element",
            "BOUNDARY": "boundary",
            "SECTION": "section",
            "LOADCASE": "loadcase",
        }
        obj_type = MODULE_TO_TYPE.get(module_name)
        created_objects = []
        
        if obj_type:
            list_name = self.tracker.get_list_name(obj_type)
            lines.append(f"    {list_name} = []")
            lines.append("")
        
        # 生成每条命令的代码
        for cmd in commands:
            call_lines = self.generate_pyosis_call(cmd)
            lines.extend(call_lines)
            lines.append("")
            
            # 如果命令创建对象，记录编号
            if cmd.mapping and cmd.mapping.creates_object and len(cmd.parts) > 1:
                created_objects.append(cmd.parts[1])
        
        # 返回对象列表
        if obj_type and created_objects:
            list_name = self.tracker.get_list_name(obj_type)
            lines.append(f"    return {list_name}")
        elif return_stmt:
            lines.append(return_stmt.rstrip())
        
        # 添加测试代码
        lines.extend([
            "",
            'if __name__ == "__main__":',
            "    from ._0_engine import engine",
        ])
        
        # 模块测试代码
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
        
        lines.append(test_codes.get(module_name, f"    # TODO: 添加测试代码"))
        
        return "\n".join(lines)
    
    def generate_project(self, modules: Dict[str, List[ParsedCommand]], output_dir: str = "./prep") -> Dict[str, str]:
        """生成完整项目代码
        
        Returns:
            {文件路径: 代码内容}
        """
        files = {}
        
        # 先构建索引
        self.tracker.build_from_commands(modules)
        
        # 生成各模块文件
        for module_name, commands in modules.items():
            file_name = f"_{list(modules.keys()).index(module_name) + 1}_{module_name.lower()}.py"
            code = self.generate_module(module_name, commands)
            files[file_name] = code
        
        return files
