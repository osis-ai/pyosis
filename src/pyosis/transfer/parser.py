"""命令流解析器

提供命令流文件的解析、分割和结构化功能。

用法:
    from pyosis.transfer.parser import CommandParser
    
    parser = CommandParser()
    modules = parser.parse_file("path/to/OSIS.out")
    
    for module_name, commands in modules.items():
        for cmd in commands:
            print(cmd.raw)      # 原始命令字符串
            print(cmd.name)     # 命令名
            print(cmd.parts)    # 参数列表
            print(cmd.mapping)  # 映射信息
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, NamedTuple
from .command_map import CommandMapping, lookup_command


class ParsedCommand(NamedTuple):
    """解析后的命令"""
    raw: str                # 原始命令字符串（不含分号）
    name: str               # 命令名
    parts: List[str]        # 分割后的参数列表
    mapping: Optional[CommandMapping]   # 映射信息
    module: str             # 所属模块


class CommandParser:
    """命令流解析器"""
    
    # 模块标记正则：//----- MODULE_NAME -----
    MODULE_PATTERN = re.compile(r"//-+\s*(\w+)\s*-*")
    
    # 模块名映射
    MODULE_MAP = {
        "CONTROL": "CONTROL",
        "PROPERTY": "PROPERTY",
        "MATERIAL": "MATERIAL",
        "SECTION": "SECTION",
        "NODE": "NODE",
        "ELEMENT": "ELEMENT",
        "BOUNDARY": "BOUNDARY",
        "LOADCASE": "LOADCASE",
        "ANALYSIS": "ANALYSIS",
        "STAGE": "STAGE",
    }
    
    def __init__(self):
        self.modules: Dict[str, List[ParsedCommand]] = {}
    
    def parse_file(self, file_path: str | Path) -> Dict[str, List[ParsedCommand]]:
        """解析命令流文件
        
        Args:
            file_path: 命令流文件路径
            
        Returns:
            {模块名: [ParsedCommand, ...]}
        """
        file_path = Path(file_path)
        
        # 尝试多种编码读取
        content = None
        for encoding in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
            try:
                content = file_path.read_text(encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise ValueError(f"无法读取文件: {file_path}")
        
        return self.parse_text(content)
    
    def parse_text(self, text: str) -> Dict[str, List[ParsedCommand]]:
        """解析命令流文本
        
        Args:
            text: 命令流文本内容
            
        Returns:
            {模块名: [ParsedCommand, ...]}
        """
        self.modules = {}
        current_module = None
        
        for line in text.splitlines():
            stripped = line.strip()
            
            # 检查模块标记
            match = self.MODULE_PATTERN.match(stripped)
            if match:
                module_name = match.group(1).upper()
                if module_name in self.MODULE_MAP:
                    current_module = module_name
                    self.modules[current_module] = []
                continue
            
            # 跳过注释和空行
            if stripped.startswith("//") or not stripped:
                continue
            
            # 解析命令
            if current_module:
                cmd_raw = stripped.rstrip(";")
                parts = cmd_raw.split(",")
                cmd_name = parts[0] if parts else ""
                
                # 查询映射
                mapping = lookup_command(cmd_name, parts)
                
                cmd = ParsedCommand(
                    raw=cmd_raw,
                    name=cmd_name,
                    parts=parts,
                    mapping=mapping,
                    module=current_module,
                )
                
                self.modules[current_module].append(cmd)
        
        return self.modules
    
    def get_statistics(self) -> Dict[str, int]:
        """获取解析统计信息
        
        Returns:
            {模块名: 命令数量}
        """
        return {name: len(cmds) for name, cmds in self.modules.items()}
    
    def get_unmapped_commands(self) -> List[ParsedCommand]:
        """获取未映射的命令列表
        
        Returns:
            [ParsedCommand, ...]
        """
        result = []
        for cmds in self.modules.values():
            for cmd in cmds:
                if cmd.mapping is None:
                    result.append(cmd)
        return result
