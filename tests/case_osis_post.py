# 本文件是后处理导出结果的示例
from pathlib import Path
from pyosis.core.all_func import *

if __name__ == '__main__':

    isok, project_dir = get_project_directory()
    if isok:
        check_path = Path(project_dir) / "Check"
        lcc_files = [f.stem for f in check_path.glob("*.lcc")]
        for filename in lcc_files:
            parts = filename.split("_", 2)  # 最多分割3部分，保留名字中的下划线
            isok, error, check_result = osis_check_result(*parts)
            check_result = check_result.to_string()
            print(filename)
            print(check_result)
            print()

    # isok, error, check_result = osis_check_result("混凝土","PC腹板斜截面抗裂验算","频遇组合包络")
    # print(check_result)
    
    # isok, error, lc_result = osis_loadcase_result("_收缩二次_CS1_主梁预制、张拉预应力","LCEF")
    # print(lc_result)

    # isok, error, env_result = osis_env_result("车道荷载包络","EnvBF")
    # print(env_result)