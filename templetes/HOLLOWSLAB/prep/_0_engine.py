from pyosis.core.engine import OSISEngine

engine = OSISEngine()

# 自动打开OSIS等操作暂未实现
# 目前需要手动打开OSIS并创建项目

def build_py_project(path: str | None = None):
    '''
    从OSIS .out / .sml 文件中构建OSIS python项目
    
    Args:
        path (str): 命令流文件路径
    '''
    with open(path, "r", encoding="gbk") as fp:
        ...

if __name__ == '__main__':
    engine.export_apdl()    # 在项目目录导出OSIS文件
    ...