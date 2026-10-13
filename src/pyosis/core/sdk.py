"""SDK 元信息与服务端实例查询

对应 HTTP 端点 /health、/sdk/version、/sdk/commands、GET /instance。
这些端点同时支持 GET/POST（/instance 仅 GET），不依赖工程状态。

用法:
    from pyosis.core.sdk import sdk_version, list_commands, instance_info
    sdk_version()      # {"success": True, "sdk": "5.1.x", "osis": ..., "abi": ..., "port": ...}
    list_commands()    # 运行时可用的命令名列表
    instance_info()    # {"pid": ..., "port": ..., "project": ..., "version": ..., "state": ...}
"""
from __future__ import annotations

from .client import osis_client, osis_get


def health(base_url=None) -> bool:
    """存活探测（POST /health）。

    只证明 HTTP server 在跑,不碰工程/command 状态。

    Returns:
        bool: server 存活返回 True
    """
    resp = osis_client("health", {}, base_url=base_url)
    return bool(resp.get("success"))


def sdk_version(base_url=None) -> dict:
    """查询 SDK/OSIS 版本与 ABI（POST/GET /sdk/version）。

    Returns:
        {"success": True, "sdk": 版本串, "osis": 版本串, "abi": ABI, "port": 端口}

    Raises:
        RuntimeError: 查询失败时抛出
    """
    resp = osis_client("sdk/version", {}, base_url=base_url)
    if not resp.get("success"):
        raise RuntimeError(f"查询 SDK 版本失败: {resp.get('error')}")
    return resp


def list_commands(base_url=None) -> list[str]:
    """查询运行时可用命令名（POST/GET /sdk/commands）。

    返回当前工程命令流可识别的命令名（GUI 书册命令不列出）。

    Returns:
        list[str]: 命令名列表

    Raises:
        RuntimeError: 查询失败时抛出
    """
    resp = osis_client("sdk/commands", {}, base_url=base_url)
    if not resp.get("success"):
        raise RuntimeError(f"查询命令列表失败: {resp.get('error')}")
    return list(resp.get("commands") or [])


def instance_info(base_url=None) -> dict:
    """查询 OSIS 实例信息（GET /instance）。

    broker 登记实例时用它确认端口实际归属。

    Returns:
        {"pid": 进程号, "port": HTTP 端口, "project": 工程路径,
         "version": 版本, "state": 实例状态}

    Raises:
        RuntimeError: 查询失败时抛出
    """
    resp = osis_get("instance", base_url=base_url)
    if not isinstance(resp, dict) or resp.get("error"):
        raise RuntimeError(f"查询实例信息失败: {resp.get('error', resp)}")
    return resp
