# --- 截面IO相关功能

from typing import Any, Dict, Literal
from ..core import REGISTRY, get_project_directory
from ..core.command import _tmp

# class SectionManager():
#     def __init__(self):
#         pass

# ExportSecPic,SecNO
@REGISTRY.register("ExportSecPic")
def osis_export_section_pic(nSec: int):
    '''
    生成截面图片，会在 image/section/ 目录下生成一张 {nSec}.jpg
    
    Args:
        nSec (int): 要生成图片的截面编号
    
    Returns:
        tuple (bool, str): 返回一个元组，包含：
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    '''
    path = get_project_directory()[1] + f"Image/section/_{nSec}.jpg\n" # 会默认保存到这里
    _tmp(path, 'image.tmp')                          # 放到临时信息-图片里
    pass