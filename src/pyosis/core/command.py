'''
pyosis.core.command 的 Docstring

===
# OSIS命令流兼容
'''

import datetime
import inspect
import functools
from typing import Dict, Any, Tuple, Literal
from .engine import OSISEngine

def osis_run(strCmd: str="", mode: Literal["stash", "exec"]="exec") -> Tuple[bool, str, Any]:
    '''
    直接以命令流的形式运行OSIS功能
    
    Args:
        strCmd: 完整的命令流
        mode: 运行模式，此参数为了同时执行多条命令提高效率
            * 使用 stash 仅会将命令流存到OSIS中，不会执行
            * 收到 exec 信号才会执行暂存包括当前的所有命令流。

    Returns:
        tuple (bool, str, Any): 是否成功，失败原因，其他结果数据
    '''
    e = OSISEngine.GetInstance()
    return e.OSIS_Run(strCmd, mode)

def _log(text, filename="pyosis.log"):
    """简单的日志函数"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {text}\n")
        f.close()


class OSISFunctionRegistry:
    """
    OSIS函数注册表.通过装饰器注册函数，可指定命令流名称

    ---
    Attributes:
        commands (dict): 存储所有注册的命令，键为命令流名称，值为对应的函数
    
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

    
    """
    
    def __init__(self):
        self.commands = {}      # func_name -> info
        self.run_mode = "stash"     # 命令处理模式，默认暂存
    
    def register(self, cmd_name=None):
        """
        注册函数装饰器
        
        Args:
            cmd_name: 命令别名，不提供则使用函数名
        """
        def decorator(func):
            name = cmd_name or func.__name__
            
            # 保存函数信息
            self.commands[func.__name__] = {
                'func': func,
                'name': func.__name__,
                'cmd_name': name,
                'doc': func.__doc__ or '',
                'module': func.__module__
            }
            
            # 创建包装函数
            @functools.wraps(func)
            def wrapper(*args, **kwargs):   # 函数执行时，都会走这个路径
                # 包装参数
                cmd = self._process_arguments(func, cmd_name, *args, **kwargs)
                # 发送到软件
                return self._execute_command(cmd)
            
            return wrapper
        
        return decorator

    def _process_arguments(self, func, cmd_name, *args, **kwargs):
        """处理参数并生成命令字符串"""
        
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
        return f"{cmd_name},{','.join(param_values)};" if len(param_values) != 0 else f"{cmd_name};"
    
    def _execute_command(self, cmd) -> Tuple[bool, str, Any]:
        """执行命令（发送到软件）"""
        _log(cmd)
        return osis_run(cmd, self.run_mode)
    
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
        self.mode = mode

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
