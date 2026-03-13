from pyosis.core.all_func import *
from pyosis.post import osis_check_result, osis_loadcase_result
from pyosis.post.env import osis_env_result

if __name__ == '__main__':
    # osis_check_result("混凝土","PC腹板斜截面抗裂验算","频遇组合包络")
    # osis_loadcase_result("_钢束二次_CS1_主梁预制、张拉预应力", "lcef")
    print(osis_env_result("车道荷载包络_车道荷载工况1","EnvBF"))
