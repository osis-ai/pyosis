# APDL, path
# 简介：输出前处理的当前状态，文件格式为.out
# path: 路径，可缺省。格式：C:\\Temp\\OSIS.out

from ..core import REGISTRY

from typing import Literal, List, Tuple, Optional

@REGISTRY.register("APDL", timeout=3600)
def osis_apdl(path=None):
    '''
    输出前处理的当前状态，文件格式为.out

    Args:
        path: 路径，可缺省。格式：C:\\Temp\\OSIS.out

    Note:
        大模型导出耗时较长，HTTP 超时缺省给到 3600（60 分钟）；
        可用 set_timeout() 全局调整，或调用时传 timeout= 单独指定

    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    pass

