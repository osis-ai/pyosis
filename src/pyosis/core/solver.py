"""pyosis/core/solver.py — OSIS solver 配置与生命周期。

用法:

    from pyosis.core.solver import OSISSolver
    from pyosis.core.engine import OSISEngine

    solver = OSISSolver(osis_install_path=r"D:\\OSIS_Solver")
    engine = OSISEngine.from_solver(solver)
    engine.run("Acel,9.8")
"""

from __future__ import annotations

import ctypes
import os
import time


class OSISSolver:
    """OSIS solver 实例的配置 + 启动入口。

    Args:
        osis_install_path: OSIS 安装根目录,根目录下需有 PySolver.dll。
        port: HTTP server 端口;<0 用 PySolver 默认 18080。端口被占会失败。
        host: 监听地址,默认 127.0.0.1。

    Raises:
        FileNotFoundError: PySolver.dll 不在指定位置。
        RuntimeError: DLL 加载失败、缺少导出、端口被占,或 server 启动超时。
    """

    def __init__(
        self,
        osis_install_path: str,
        port: int = 18080,
        host: str = "127.0.0.1",
    ) -> None:
        self._install_path = osis_install_path
        self._port = port
        self._host = host
        self._lib: ctypes.CDLL | None = None
        self._started = False
        self.start()

    @property
    def port(self) -> int:
        return self._port

    @property
    def host(self) -> str:
        return self._host

    @property
    def url(self) -> str:
        return f"http://{self._host}:{self._port}"

    @property
    def started(self) -> bool:
        return self._started

    @property
    def install_path(self) -> str:
        return self._install_path

    def start(self) -> "OSISSolver":
        """ctypes 加载 PySolver.dll 并启动 HTTP server。幂等。__init__ 已自动调用。

        Raises:
            FileNotFoundError: <install>/PySolver.dll 不存在。
            RuntimeError: DLL 加载/导出/start 失败,或 server 在 15s 内未响应。
        """
        if self._started:
            return self

        path = os.path.join(self._install_path, "PySolver.dll")
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"OSISSolver: 找不到 {path}。"
                f"请确认 PySolver.dll 已编译并放到 {self._install_path}\\ 下。"
            )

        self._add_dll_search_dir(os.path.dirname(path))

        try:
            lib = ctypes.CDLL(path)
        except OSError as e:
            raise RuntimeError(f"OSISSolver: 加载 {path} 失败: {e}")

        if not hasattr(lib, "PySolver_AutoBootstrap"):
            raise RuntimeError(
                f"OSISSolver: {path} 缺少 PySolver_AutoBootstrap 导出。"
                f"请重新编译 PySolver.cpp(已加 ctypes 入口)。"
            )

        fn = lib.PySolver_AutoBootstrap
        fn.restype = ctypes.c_int
        fn.argtypes = [ctypes.c_char_p, ctypes.c_int]
        actual_port = fn(self._host.encode("utf-8"), self._port)
        if actual_port < 0:
            raise RuntimeError("OSISSolver: PySolver_AutoBootstrap 启动失败")

        self._lib = lib
        self._started = True
        self._wait_ready()
        return self

    def stop(self) -> None:
        """best-effort 停止。

        Windows 上 ctypes 加载的 DLL 无法干净 unload,server 实际随 Python
        进程退出才停。本方法只清掉内部状态。
        """
        self._started = False
        self._lib = None

    def _wait_ready(self, timeout: float = 15.0) -> None:
        """轮询 POST /health 直到 server 响应。

        PySolver 的所有路由都用 POST(GET 永远 404);/health 是专用存活探测,
        不依赖工程状态,固定 200 + {"success":true}。
        走 trust_env=False 的独立 session——目标是本机 loopback,不应被
        HTTP_PROXY 等系统代理劫走。
        """
        import requests
        deadline = time.time() + timeout
        last_err: Exception | None = None
        session = requests.Session()
        session.trust_env = False
        while time.time() < deadline:
            try:
                r = session.post(f"{self.url}/health", json={}, timeout=1.0)
                if r.ok:
                    return
            except Exception as e:
                last_err = e
            time.sleep(0.2)
        raise RuntimeError(
            f"OSISSolver: server 在 {timeout}s 内未就绪于 {self.url}"
            + (f" (last error: {last_err})" if last_err else "")
        )

    @staticmethod
    def _add_dll_search_dir(directory: str) -> None:
        """把 directory 加进 DLL 搜索路径(Windows + Linux 兼容)。"""
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(directory)
            except OSError:
                pass
        cur = os.environ.get("PATH", "")
        if directory not in cur.split(os.pathsep):
            os.environ["PATH"] = directory + os.pathsep + cur

    def __enter__(self) -> "OSISSolver":
        return self

    def __exit__(self, *exc) -> None:
        self.stop()

    def __repr__(self) -> str:
        state = "started" if self._started else "not-started"
        return f"OSISSolver({self._install_path!r}, {self.url}, {state})"