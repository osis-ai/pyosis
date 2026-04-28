"""pyosis 命令流转换模块

提供 OSIS 命令流与 pyosis Engine API 之间的双向转换能力。

主要组件:
    - command_map: 命令映射表
    - parser: 命令流解析器
    - generator: pyosis 代码生成器

用法:
    from pyosis.transfer import CommandParser, PyosisGenerator
    
    # 解析命令流
    parser = CommandParser()
    modules = parser.parse_file("path/to/OSIS.out")
    
    # 生成 pyosis 代码
    generator = PyosisGenerator()
    code = generator.generate_module("MATERIAL", modules["MATERIAL"])
"""

from .command_map import (
    CMD_MAP,
    DISPATCHER_CONFIG,
    CommandMapping,
    lookup_command,
    list_all_commands,
)

from .parser import (
    CommandParser,
    ParsedCommand,
)

from .generator import (
    PyosisGenerator,
    IndexTracker,
)

__all__ = [
    "CMD_MAP",
    "DISPATCHER_CONFIG",
    "CommandMapping",
    "lookup_command",
    "list_all_commands",
    "CommandParser",
    "ParsedCommand",
    "PyosisGenerator",
    "IndexTracker",
]
