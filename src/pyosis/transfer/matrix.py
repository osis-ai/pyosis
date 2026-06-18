"""矩阵命令收集，合并为 engine.matrix(...) 调用。"""

from __future__ import annotations

from typing import Any


def _parse_number(raw: str) -> int | float:
    s = raw.strip()
    f = float(s)
    if f == int(f) and "e" not in s.lower() and "." not in s and "E" not in s:
        return int(f)
    return f


def _format_literal(value: Any) -> str:
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, list):
        inner = ", ".join(_format_literal(v) for v in value)
        return f"[{inner}]"
    return repr(value)


class MatrixAccumulator:
    """收集 *dim 与 Name[i,j,k]=value，flush 为 engine.matrix 调用。"""

    def __init__(self) -> None:
        self.name: str | None = None
        self.dims: tuple[int, ...] = ()
        self.data: dict[tuple[int, ...], int | float | str] = {}

    def on_dim(self, fields: list[str]) -> None:
        if not fields:
            return
        head = fields[0].lower()
        if head.startswith("*dim"):
            self.name = fields[1]
            self.dims = tuple(int(x) for x in fields[2:])
        elif head == "charn":
            self.name = fields[1]
            self.dims = tuple(int(x) for x in fields[2:])
        else:
            return
        self.data = {}

    def on_assign(self, name: str, indices: tuple[int, ...], value: str) -> None:
        if self.name is None:
            self.name = name
        if self.name != name:
            return
        self.data[indices] = _parse_number(value) if value.strip() else value

    def flush(self) -> str | None:
        if self.name is None or not self.data:
            self._reset()
            return None
        nested = self._build_nested_list()
        line = f"engine.matrix({_format_literal(self.name)}, {_format_literal(nested)})"
        self._reset()
        return line

    def _reset(self) -> None:
        self.name = None
        self.dims = ()
        self.data = {}

    def _build_nested_list(self) -> list[Any]:
        if not self.data:
            return []

        max_indices = [max(idx[i] for idx in self.data) for i in range(len(next(iter(self.data))))]

        if self.dims:
            sizes = list(self.dims)
            while len(sizes) < len(max_indices):
                sizes.append(max_indices[len(sizes)] + 1)
            shape = tuple(sizes[: len(max_indices)])
        else:
            shape = tuple(m + 1 for m in max_indices)

        if len(shape) == 1:
            result: list[Any] = [0] * shape[0]
            for idx, val in self.data.items():
                result[idx[0]] = val
            return result

        if len(shape) == 2:
            rows, cols = shape
            result = [[0] * cols for _ in range(rows)]
            for idx, val in self.data.items():
                result[idx[0]][idx[1]] = val
            return result

        depth, height, width = shape[0], shape[1], shape[2]
        result = [[[0] * width for _ in range(height)] for _ in range(depth)]
        for idx, val in self.data.items():
            i = idx[0]
            j = idx[1] if len(idx) > 1 else 0
            k = idx[2] if len(idx) > 2 else 0
            result[i][j][k] = val
        return result
