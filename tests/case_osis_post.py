from pyosis.core.all_func import *

if __name__ == '__main__':
    isok, error, check_result = osis_check_result("混凝土","PC腹板斜截面抗裂验算","频遇组合包络")
    print(check_result)
    
    isok, error, lc_result = osis_loadcase_result("_收缩二次_CS1_主梁预制、张拉预应力","LCEF")
    print(lc_result)