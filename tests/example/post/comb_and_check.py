import os
from pyosis import OSISEngine

engine = OSISEngine()
post_apdl_dir = os.path.abspath("../OSISPost.out")
engine.import_apdl(post_apdl_dir)               # 导入之前的后处理组合和验算的步骤
if os.path.exists(post_apdl_dir):
    engine.post.select_elements("All")          # 全选单元
    engine.post.solve_checks()                  # 进行验算
    print("OK")
else:
    print("首次进行后处理荷载组合与验算请在软件内进行操作，后续重复进行荷载组合与验算将自动复用您的操作步骤！")
