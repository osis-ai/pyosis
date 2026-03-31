
"""
io 模块接口测试 - 预应力
"""

from pyosis.io import *

def test_prestressed_info():
    """测试获取预应力材料信息"""
    print("\n=== PrestressedMaterialInfo ===")
    pm = PrestressedMaterialInfo()
    print("success:", pm.success, "count:", len(pm.data))
    for row in pm.data[:5]:
        print(row)

    print("\n=== PrestressedLoadInfo ===")
    pl = PrestressedLoadInfo()
    print("success:", pl.success, "count:", len(pl.data))
    for row in pl.data[:5]:
        print(row)
    if pl.success:
        print("load case list:", pl.get_load_case_list())
        print("name list:", pl.get_name_list())


def test_tendon_info():
    """测试获取钢束信息"""
    print("\n=== TendonShapeInfo ===")
    ts = TendonShapeInfo()
    print("success:", ts.success, "count:", len(ts.data))
    for row in ts.data[:5]:
        print(row)
    if ts.success:
        print("name list:", ts.get_name_list())

    print("\n=== TendonPropInfo ===")
    tp = TendonPropInfo()
    print("success:", tp.success, "count:", len(tp.data))
    for row in tp.data[:5]:
        print(row)
    if tp.success:
        print("name list:", tp.get_name_list())

if __name__ == '__main__':
    test_prestressed_info()
    test_tendon_info()
