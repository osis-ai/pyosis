"""
pyosis.core 的 Docstring
--------

OSISEngine中的函数，将会分发到各个模块，被再次封装，意图为：
- 避免麻烦的OSISEngine::GetInstance().OSIS_XXX调用方式
- 将各个模块分类开以实现逻辑清晰
- 将函数命名格式转换成python的常用格式，便于人与AI的理解
"""

from .engine import OSISEngine
from .command import REGISTRY, osis_run, set_run_mode
