"""pyosis/core/solver.py — OSIS solver 配置与生命周期。

用法:

    from pyosis.core.solver import OSISSolver
    from pyosis.core.engine import OSISEngine

    solver = OSISSolver(osis_install_path=r"D:\\OSIS_SDK\\runtime")
    engine = OSISEngine.from_solver(solver)
    engine.run("Acel,9.8")

无头宿主是 ``osis-headless.exe``（子进程），不是 ``ctypes`` 加载
``PySolver_AutoBootstrap``。客户包不暴露后者。
"""

from __future__ import annotations

import os
import subprocess
import time


class OSISSolver:
    """OSIS solver 实例的配置 + 启动入口。

    Args:
        osis_install_path: 含 ``osis-headless.exe`` 与 ``config/`` 的运行时根
            （SDK zip 里的 ``runtime/``）。
        port: HTTP server 端口;<0 用默认 18080。被占用时宿主失败并退出。
        host: 监听地址,默认 127.0.0.1。

    Raises:
        FileNotFoundError: osis-headless.exe 不在指定位置。
        RuntimeError: 进程启动失败,或在超时内没打出 ``PORT=``。
    """

    def __init__(
        self,
        osis_install_path: str,
        port: int = 18080,
        host: str = "127.0.0.1",
    ) -> None:
        self._install_path = osis_install_path
        self._port = port if port > 0 else 18080
        self._host = host
        self._proc: subprocess.Popen | None = None
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
        """拉起 ``osis-headless.exe --runtime <dir>``。幂等。__init__ 已自动调用。

        Raises:
            FileNotFoundError: <install>/osis-headless.exe 不存在。
            RuntimeError: 进程退出,或 30s 内 stdout 没有 ``PORT=<n>``。
        """
        if self._started:
            return self

        exe = os.path.join(self._install_path, "osis-headless.exe")
        if not os.path.isfile(exe):
            raise FileNotFoundError(
                f"OSISSolver: 找不到 {exe}。"
                f"请把 osis_install_path 指到 SDK 的 runtime/（含 osis-headless.exe 与 config/）。"
            )

        env = os.environ.copy()
        # 许可文件可由调用方事先设好；这里不注入 OSIS_INTERNAL_LICENSE。
        cmd = [
            exe,
            "--runtime",
            self._install_path,
            "--host",
            self._host,
            "--port",
            str(self._port),
        ]
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=self._install_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                env=env,
            )
        except OSError as e:
            raise RuntimeError(f"OSISSolver: 启动 {exe} 失败: {e}") from e

        self._proc = proc
        self._port = self._wait_port(proc)
        self._started = True
        return self

    def stop(self) -> None:
        """结束宿主进程。进程退出后 HTTP 不再监听。"""
        proc = self._proc
        self._started = False
        self._proc = None
        if proc is None or proc.poll() is not None:
            return
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=4)

    def _wait_port(self, proc: subprocess.Popen, timeout: float = 30.0) -> int:
        """读 stdout 直到 ``PORT=<n>``。宿主在许可失败时会立刻退出。"""
        deadline = time.time() + timeout
        buf = ""
        while time.time() < deadline:
            if proc.poll() is not None:
                err = ""
                if proc.stderr is not None:
                    try:
                        err = proc.stderr.read() or ""
                    except Exception:
                        err = ""
                raise RuntimeError(
                    f"OSISSolver: osis-headless 退出 {proc.returncode}\n{buf}{err}"
                )
            line = proc.stdout.readline() if proc.stdout else ""
            if not line:
                time.sleep(0.05)
                continue
            buf += line
            if line.startswith("PORT="):
                return int(line.strip().split("=", 1)[1])
        self.stop()
        raise RuntimeError(f"OSISSolver: {timeout}s 内未收到 PORT=\n{buf}")

    def __enter__(self) -> "OSISSolver":
        return self

    def __exit__(self, *exc) -> None:
        self.stop()

    def __repr__(self) -> str:
        state = "started" if self._started else "not-started"
        return f"OSISSolver({self._install_path!r}, {self.url}, {state})"
