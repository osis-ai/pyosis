# cpp/boundary_info.py

from ..core.client import osis_client
from .response import OSISParse


class BoundaryInfo(OSISParse):
    """
    GetAllBoundaryInfo 接口返回封装

    返回格式:
        {
            "success": true,
            "data": [
                {
                    "no": int,
                    "name": str,
                    "type": int,  # 1=General, 2=MstSlv, 4=Release, 5=ElstcSpt, 6=GeneralElstcSpt
                    "entityVec": [int, ...],
                    "isOccupied": bool,
                    "isSelected": bool,
                    "isPloted": bool,
                    # type=1 (General) 特有:
                    "coorNO": int,
                    "constraints": [int, ...],  # 7个约束值
                    # type=2 (MstSlv) 特有:
                    "masterNO": int,
                    "constraints": [int, ...],
                    # type=4 (Release) 特有:
                    "endIState": [int, ...],
                    "endJState": [int, ...],
                    "endI": [float, ...],
                    "endJ": [float, ...],
                    # type=5 (ElstcSpt) 特有:
                    "coorNO": int,
                    "k": [float, ...],
                    "elasticK": [{"isFixed": bool, "value": float}, ...],
                    # type=6 (GeneralElstcSpt) 特有:
                    "coorNO": int,
                    "flagM": bool,
                    "flagC": bool,
                    "stiffnessMatrix": [[float, ...], ...],
                    "massMatrix": [[float, ...], ...],  # 仅当flagM=True时
                    "dampingMatrix": [[float, ...], ...],  # 仅当flagC=True时
                },
                ...
            ]
        }
    """

    # 边界类型枚举映射
    BOUNDARY_TYPE_NAMES = {
        1: "General",
        2: "MstSlv",
        3: "Rigid",
        4: "Release",
        5: "ElstcSpt",
        6: "GeneralElstcSpt",
    }

    def __init__(self):
        super().__init__(osis_client("GetAllBoundaryInfo", {}))
        self._bd_map: dict[int, dict] = {bd["no"]: bd for bd in self.data}

    def get_by_no(self, no: int) -> dict | None:
        """
        根据边界编号获取边界信息

        Args:
            no: 边界编号

        Returns:
            边界信息 dict；未找到返回 None
        """
        return self._bd_map.get(no)

    def get_no_list(self) -> list:
        """
        获取所有边界编号列表

        Returns:
            边界编号列表
        """
        return [bd.get("no") for bd in self.data]

    def get_type(self, no: int) -> int | None:
        """
        根据边界编号获取边界类型编号

        Args:
            no: 边界编号

        Returns:
            边界类型编号（1=General, 2=MstSlv, 4=Release, 5=ElstcSpt, 6=GeneralElstcSpt）；未找到返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("type") if bd else None

    def get_type_name(self, no: int) -> str | None:
        """
        根据边界编号获取边界类型名称

        Args:
            no: 边界编号

        Returns:
            边界类型名称字符串；未找到返回 None
        """
        bd = self.get_by_no(no)
        if bd:
            return self.BOUNDARY_TYPE_NAMES.get(bd.get("type"), "Unknown")
        return None

    def get_entity_vec(self, no: int) -> list | None:
        """
        根据边界编号获取关联的节点/单元列表

        Args:
            no: 边界编号

        Returns:
            关联的节点/单元编号列表；未找到返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("entityVec") if bd else None

    def get_master_no(self, no: int) -> int | None:
        """
        根据边界编号获取主从边界的主节点编号

        Args:
            no: 边界编号

        Returns:
            主节点编号；未找到或非主从边界返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("masterNO") if bd else None

    def get_constraints(self, no: int) -> list | None:
        """
        根据边界编号获取边界约束值

        Args:
            no: 边界编号

        Returns:
            约束值列表（7个）；未找到返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("constraints") if bd else None

    def get_coor_no(self, no: int) -> int | None:
        """
        根据边界编号获取局部坐标系编号

        Args:
            no: 边界编号

        Returns:
            局部坐标系编号；未找到返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("coorNO") if bd else None

    def is_occupied(self, no: int) -> bool | None:
        """
        根据边界编号判断边界是否被节点/单元占用

        Args:
            no: 边界编号

        Returns:
            是否被占用；未找到返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("isOccupied") if bd else None

    def is_selected(self, no: int) -> bool | None:
        """
        根据边界编号判断边界是否被选中

        Args:
            no: 边界编号

        Returns:
            是否选中；未找到返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("isSelected") if bd else None

    def get_stiffness_matrix(self, no: int) -> list | None:
        """
        根据边界编号获取GeneralElstcSpt边界的刚度矩阵

        Args:
            no: 边界编号

        Returns:
            6x6刚度矩阵；未找到或非GeneralElstcSpt类型返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("stiffnessMatrix") if bd else None

    def get_mass_matrix(self, no: int) -> list | None:
        """
        根据边界编号获取GeneralElstcSpt边界的质量矩阵

        Args:
            no: 边界编号

        Returns:
            6x6质量矩阵；未找到、非GeneralElstcSpt类型或flagM=False时返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("massMatrix") if bd else None

    def get_damping_matrix(self, no: int) -> list | None:
        """
        根据边界编号获取GeneralElstcSpt边界的阻尼矩阵

        Args:
            no: 边界编号

        Returns:
            6x6阻尼矩阵；未找到、非GeneralElstcSpt类型或flagC=False时返回 None
        """
        bd = self.get_by_no(no)
        return bd.get("dampingMatrix") if bd else None


def get_all_boundary_info() -> BoundaryInfo:
    """
    获取所有边界信息

    Returns:
        BoundaryInfo 对象
    """
    return BoundaryInfo()