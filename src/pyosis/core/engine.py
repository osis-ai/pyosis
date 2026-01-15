import os
import sys

# 查找dll路径
current_dir =os.path.dirname(os.path.abspath(__file__))
# dll_dir= os.path.abspath(os.path.join(current_dir, "../../../../bin64"))

if os.path.exists(os.path.join(current_dir, "PyInterface.pyi")):
    from PyInterface import PyInterface as OSISEngine       # 如果有pyi，认为pyd已经被找到了，直接导入就行
else:
    from .PyInterface import PyInterface as OSISEngine      # 如果没有pyi，认为只是简单实验下能不能跑，不用打开pyd


