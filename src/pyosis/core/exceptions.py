"""
pyosis 自定义异常
"""

class DependencyError(RuntimeError):
    """删除实体时存在依赖项

    Attributes:
        entity_type: 实体类型字符串，如 "Material"
        id_value: 实体编号（int）或名称（str）
        no: 按编号寻址时的编号，否则为 None
        name: 按名称寻址时的名称，否则为 None
        dependencies: 依赖关系字典
    """
    def __init__(self, entity_type: str, id_value: int | str, dependencies: dict[str, list]):
        self.entity_type = entity_type
        self.id_value = id_value
        self.dependencies = dependencies
        if isinstance(id_value, int):
            self.no = id_value
            self.name = None
            label = f"#{id_value}"
        else:
            self.no = None
            self.name = id_value
            label = id_value

        lines = [f"无法删除 {entity_type} {label}，存在以下依赖:"]
        for kind, refs in dependencies.items():
            if refs:
                lines.append(f"  - {kind}: {refs}")
        super().__init__("\n".join(lines))
