'''
pyosis.core.command 的 Docstring

===
# OSIS命令流兼容
'''
import os
import datetime
import inspect
import functools
from typing import Dict, Any, Tuple, Literal, Optional
# from .engine import OSISEngine
from .client import osis_client
from .batch import batch_state, batch, flush, BatchError

# def _log(text, filename="pyosis.log"):
#     """简单的日志函数"""
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open(filename, 'a', encoding='utf-8') as f:
#         f.write(f"[{timestamp}] {text}\n")
#         f.close()

def osis_run(
    strCmd: str = "",
    mode: Literal["stash", "exec"] = "exec",
    timeout: float | None = None,
) -> tuple[bool, str]:
    """
    http 模拟 C++ 原生 OSIS_Run 函数
    Args:
        strCmd: 完整的命令流
        mode: 运行模式，此参数为了同时执行多条命令提高效率
            * 使用 stash 仅会将命令流存到OSIS中，不会执行
            * 收到 exec 信号才会执行暂存包括当前的所有命令流。
        timeout: HTTP 超时秒数；不传则用 set_timeout() 的全局设置，
            未设置时用 osis_client 的 DEFAULT_TIMEOUT

    Returns:
        tuple (bool, str): 是否成功，失败原因
    """
    if timeout is None:
        timeout = REGISTRY.timeout
    response = osis_client(
        "OSIS_Run",
        {"strCmd": strCmd, "mode": mode},
        timeout=timeout,
    )
    return response['success'], response['error']
    
def _log(text, log_dir="pyosis_logs"):
    ...
# def _log(text, log_dir="pyosis_logs"):
#     """
#     同一轮执行（<1秒间隔）的代码追加到同一文件，
#     超过1秒则创建新文件
    
#     Args:
#         text: 要记录的代码行
#         log_dir: 日志文件夹路径
#     Returns:
#         目标文件路径
#     """
#     # 创建日志目录
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#         files = []
#     else:
#         # 获取所有文件（排除子目录）
#         files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) 
#                 if os.path.isfile(os.path.join(log_dir, f))]
    
#     current_time = datetime.datetime.now()
#     target_file = None
#     is_new_file = True
    
#     # 查找最近修改的文件
#     if files:
#         latest_file = max(files, key=os.path.getmtime)
#         mtime = datetime.datetime.fromtimestamp(os.path.getmtime(latest_file))
        
#         # 如果小于1秒，追加到该文件
#         if (current_time - mtime).total_seconds() < 1.0:
#             target_file = latest_file
#             is_new_file = False
    
#     # 需要创建新文件
#     if is_new_file:
#         timestamp = current_time.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 毫秒级
#         target_file = os.path.join(log_dir, f"session_{timestamp}.txt")
    
#     with open(target_file, 'a', encoding='utf-8') as f:
#         f.write(f"{text}\n")
    
#     return target_file

# def _tmp(text, tmp_file="tmp.tmp", clear=False):        # 运行时临时信息
#     if clear:
#         os.remove(tmp_file)
#     with open(tmp_file, "a+", encoding="utf-8") as f:
#         f.write(text)

class OSISFunctionRegistry:
    """
    OSIS函数注册表.通过装饰器注册函数，可指定命令流名称

    ---
    Attributes:
        commands (dict): 存储所有注册的命令，键为函数名称，值为对应的函数信息
    
    Example:
        >>> REGISTRY = OSISFunctionRegistry()
        >>> 
        >>> @REGISTRY.register("BdGrp")
        ... def boundary_group(name, op, params=None):      # 函数名写全名便于人和**AI**理解
        ...     '''边界组操作'''
        ...     pass
        >>> 
        >>> # 调用函数会自动转换为命令字符串
        >>> result = boundary_group(2, "a", [2, 3, 5, "8to10"]) # 会自动组装成 “ BdGrp,2,a,2,3,5,8to10; ” 并发给OSIS执行
        >>> print(result)
        (True, "")
        >>>  
        >>> @REGISTRY.register("test")
        ... def test_func(a: str, b: bool, c: float, d: int=None):
        ...     '''示例'''
        ...     pass
        >>> test_func("name", True, 1.0, None)  # 组装成 test,name,1,1.0;   # 参数值为None会被忽略
        >>> test_func("name", True, "", 1)      # 组装成 test,name,1,,1;    # 需要空参数忽略参数类型填一个空字符串： ""
        >>>
        >>> # timeout 是命令流的保留参数，不写进命令流。任何命令都可以在调用时传，
        >>> # 覆盖本次 HTTP 超时：
        >>> osis_combine_solve(timeout=7200)    # 只发 CombineSolve;
        >>> # 耗时命令在注册时给出自己的缺省值（普通命令用 osis_client 的 300）：
        >>> @REGISTRY.register("CombineSolve", timeout=3600)
        ... def osis_combine_solve():
        ...     '''计算组合和包络'''
        ...     pass


    """

    def __init__(self):
        self.commands = {}      # func_name -> info
        self.run_mode = "exec"     # 命令处理模式，默认执行
        self.timeout = None     # set_timeout 设的全局超时，None 时用各命令注册的缺省值

    def register(self, cmd_name=None, timeout: float | None = None):
        """
        注册函数装饰器

        Args:
            cmd_name: 命令名，不提供则使用函数名
            timeout: 该命令的 HTTP 超时秒数缺省值，None 时用 osis_client 的
                DEFAULT_TIMEOUT。耗时命令（求解、导出等）应显式给出
        """
        def decorator(func):
            name = cmd_name or func.__name__
            register_timeout = timeout

            # 保存函数信息
            self.commands[func.__name__] = {
                'func': func,
                'name': func.__name__,
                'cmd_name': name,
                'doc': func.__doc__ or '',
                'module': func.__module__,
                'timeout': timeout
            }

            # 创建包装函数
            @functools.wraps(func)
            def wrapper(*args, **kwargs):   # 函数执行时，都会走这个路径
                # timeout 是命令流的保留参数，不进命令流
                call_timeout = kwargs.pop("timeout", None)
                # 包装参数
                cmd, _bound_args = self._process_arguments(func, cmd_name, *args, **kwargs)
                timeout = self._resolve_timeout(call_timeout, register_timeout)
                # batch 模式：进缓冲，退出上下文时统一发送
                if batch_state.active:
                    batch_state.buffer.append(cmd)
                    return (True, "queued")
                # 发送到软件
                return self._execute_command(cmd, timeout=timeout)

            return wrapper

        return decorator

    def _resolve_timeout(self, call_timeout: float | None, register_timeout: float | None):
        """确定本次 HTTP 超时：调用时传入 > set_timeout 全局设置 > 注册时声明的缺省值"""
        if call_timeout is not None:
            return call_timeout
        return self.timeout if self.timeout is not None else register_timeout

    def _process_arguments(self, func, cmd_name, *args, **kwargs):
        """处理参数并生成命令字符串，同时返回绑定参数（供 batch 影子登记）"""

        # 获取函数签名
        sig = inspect.signature(func)

        # 绑定用户参数
        try:
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
        except TypeError as e:
            raise ValueError(f"参数错误: {e}")

        # 收集参数值
        param_values = []

        for param_name, param in sig.parameters.items():    # 参数值为空字符串时会加一个空的参数
            value = bound.arguments[param_name]

            # 自动展开list/tuple
            if isinstance(value, (list, tuple)):
                for item in value:
                    param_values.append(str(item))
            # 自动展开dict，只取值
            elif isinstance(value, dict):
                for val in value.values():
                    param_values.append(str(val))
            elif isinstance(value, bool):
                param_values.append(str(int(value)))
            elif value is None:
                # 参数值为空字符串时会加一个空的参数
                # 如果希望生成 cmd,a,b,,d;的命令格式，c参数需要忽略参数类型填写空字符串：""
                # param_values.append("")     # 加一个空字符串
                continue        # 如果为None则跳过解析
            else:
                # 普通值
                param_values.append(str(value))

        # 生成命令字符
        cmd = f"{cmd_name},{','.join(param_values)};" if len(param_values) != 0 else f"{cmd_name};"
        return cmd, dict(bound.arguments)
    
    def _execute_command(self, cmd, timeout: float | None = None) -> Tuple[bool, str, Any]:
        """执行命令（发送到软件）"""
        # _log(cmd)
        result = osis_run(cmd, "exec", timeout=timeout)
        isok, error, *rest = result
        return result
    
    def list_commands(self):
        """列出所有命令"""
        for cmd_name, info in self.commands.items():
            print(f"{cmd_name}: {info['doc'].split(chr(10))[0] if info['doc'] else '无描述'}")
    
    def get_command(self, cmd_name):
        """获取函数信息"""
        return self.commands.get(cmd_name)
    
    def count_command(self):
        """计算总共多少个函数"""
        return len(self.commands)
    
    def set_run_mode(self, mode: Literal["stash", "exec"]="exec"):
        '''设置命令运行模式，默认是暂存，可以提高性能'''
        self.run_mode = mode

    def set_timeout(self, timeout: float | None = None):
        '''设置所有命令流的默认 HTTP 超时秒数

        Args:
            timeout: 超时秒数；None 恢复为各命令注册时声明的缺省值

        Note:
            优先级：调用时传入的 timeout > 本设置 > 注册时声明的缺省值。
            batch 冲刷同样受本设置影响（未设置时用 600）
        '''
        self.timeout = timeout
        batch_state.timeout = timeout

# 全局函数注册表实例
REGISTRY = OSISFunctionRegistry()       # 作用为提供python函数和命令流的映射关系，保证参数个数与顺序正常，python函数一定要注册一下

def set_run_mode(mode: Literal["stash", "exec"]="exec"):
    '''
    设置全局命令运行模式，默认是暂存，可以提高性能

    Args:
        mode: 运行模式，此参数为了同时执行多条命令提高效率
            * 使用 stash 仅会将命令流存到OSIS中，不会执行
            * 收到 exec 信号才会执行暂存包括当前的所有命令流。
    '''
    REGISTRY.set_run_mode(mode)

def set_timeout(timeout: float | None = None):
    '''
    设置所有命令流的默认 HTTP 超时秒数

    Args:
        timeout: 超时秒数；None 恢复为各命令注册时声明的缺省值

    Note:
        优先级：调用时传入的 timeout > 本设置 > 注册时声明的缺省值。
        batch 冲刷同样受本设置影响（未设置时用 600）
    '''
    REGISTRY.set_timeout(timeout)
