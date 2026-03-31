
"""
io 模块接口测试 - node
"""
from pyosis.io import *


def test_coordinate():
    """测试获取节点坐标"""
    coord = Coordinate()
    print(f"\n=== Coordinate ===")
    print(f"success: {coord.success}")
    print(f"count: {len(coord)}")

    if coord.success and len(coord) > 0:
        first_id = coord.get_id_list()[0]
        print(f"first node id: {first_id}")
        print(f"get_by_id({first_id}): {coord.get_by_id(first_id)}")
        print(f"get_x({first_id}): {coord.get_x(first_id)}")
        print(f"get_y({first_id}): {coord.get_y(first_id)}")
        print(f"get_z({first_id}): {coord.get_z(first_id)}")
        print(f"get_xyz({first_id}): {coord.get_xyz(first_id)}")
        print(f"get_id_list(): {coord.get_id_list()}")

if __name__ == "__main__":
    test_coordinate()