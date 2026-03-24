# io/response.py

from typing import Any


class OSISParse:
    """
    封装 C++ 接口返回值，解析 dict 格式：
    {"success": bool, "data": [...]} - GetCoordinate 等
    """

    def __init__(self, raw_result: dict):
        """
        初始化解析器

        Args:
            raw_result: C++ 接口返回的 JSON 对象（dict）
        """
        self._success: bool = False
        self._data: list = []
        self._raw: dict = {}

        self._parse(raw_result)

    def _parse(self, raw_result: dict):
        """
        解析原始返回数据

        Args:
            raw_result: 原始返回数据 dict
        """
        if isinstance(raw_result, dict):
            self._success = raw_result.get("success", False)
            self._raw = raw_result
            self._data = raw_result.get("data", []) if raw_result.get("data") is not None else []

    @property
    def success(self) -> bool:
        """
        是否成功

        Returns:
            True 表示成功，False 表示失败
        """
        return self._success

    @property
    def raw(self) -> dict:
        """
        获取原始 dict 数据

        Returns:
            解析后的完整 JSON 对象
        """
        return self._raw

    @property
    def data(self) -> list:
        """
        获取 data 列表

        Returns:
            JSON 中的 data 字段，通常是元素列表
        """
        return self._data

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取字段值，支持嵌套访问

        Args:
            default:
            key: 字段名，支持点号分隔的嵌套访问
                - 顶级字段: "success", "data"
                - 嵌套访问: "data.0.type" 表示 data[0]["type"]

        Returns:
            字段值；字段不存在返回 default

        Example:
            >>> resp.get("success")
            True
            >>> resp.get("data")
            [...]
            >>> resp.get("data.0.type")
            1
        """
        if "." not in key:
            return self._raw.get(key, default)

        keys = key.split(".")
        current = self._raw

        for k in keys:
            if isinstance(current, dict):
                current = current.get(k)
            elif isinstance(current, list):
                try:
                    current = current[int(k)]
                except (IndexError, ValueError):
                    return default
            else:
                return default

            if current is None:
                return default

        return current

    def __len__(self) -> int:
        """
        获取 data 列表长度

        Returns:
            data 列表的元素数量
        """
        return len(self._data)

    def __iter__(self):
        """
        支持遍历 data 列表

        Returns:
            data 列表的迭代器
        """
        return iter(self._data)

    def __repr__(self):
        """
        字符串表示

        Returns:
            调试用的字符串表示
        """
        return f"OSISParse(success={self._success}, count={len(self._data)})"