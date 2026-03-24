# io/element_info.py

from ..core.client import osis_client
from .response import OSISParse


class ElementInfo(OSISParse):
    """
    GetAllElementInfo 接口返回封装

    返回格式:
        {
            "success": true,
            "data": [
                {
                    "no": int,
                    "type": int,          # 元素类型: Beam=?, Truss=?, Spring=?, Cable=?, Shell=?
                    "mat": int,
                    "nodeVec": [int, ...],
                    "nodeI": int,
                    "nodeJ": int,
                    "locCoor": {...},
                    "center": [float, float, float],
                    "length": float,
                    "characters": str,
                    # Beam 特有:
                    "isTaper": bool,
                    "secVec": [int, ...],
                    # ... 其他类型特有字段
                },
                ...
            ]
        }
    """

    def __init__(self):
        super().__init__(osis_client("GetAllElementInfo",{}))
        self._elem_map: dict[int, dict] = {elem["no"]: elem for elem in self.data}

    def get_by_no(self, no: int) -> dict | None:
        """
        根据单元编号获取单元信息

        Args:
            no: 单元编号

        Returns:
            单元信息 dict；未找到返回 None
        """
        return self._elem_map.get(no)

    def get_no_list(self) -> list:
        """
        获取所有单元编号列表

        Returns:
            单元编号列表
        """
        return [e.get("no") for e in self.data]

    def get_type(self, no: int) -> int | None:
        """
        根据单元编号获取类型编号

        Args:
            no: 单元编号

        Returns:
            类型编号 (0=Unknown, 1=Beam, 2=Truss, 3=Spring, 4=Cable, 5=Shell)；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("type") if elem else None

    def get_type_name(self, no: int) -> str | None:
        """
        根据单元编号获取类型名称

        Args:
            no: 单元编号

        Returns:
            类型名称 (Unknown, Beam, Truss, Spring, Cable, Shell)；未找到返回 None
        """
        type_map = {
            0: "Unknown",
            1: "Beam",
            2: "Truss",
            3: "Spring",
            4: "Cable",
            5: "Shell",
        }
        t = self.get_type(no)
        return type_map.get(t, "Unknown") if t is not None else None

    def get_material(self, no: int) -> int | None:
        """
        根据单元编号获取材料编号

        Args:
            no: 单元编号

        Returns:
            材料编号；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("mat") if elem else None

    def get_nodes(self, no: int) -> list | None:
        """
        根据单元编号获取节点编号列表

        Args:
            no: 单元编号

        Returns:
            节点编号列表 [nodeI, nodeJ, ...]；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("nodeVec") if elem else None

    def get_length(self, no: int) -> float | None:
        """
        根据单元编号获取单元长度

        Args:
            no: 单元编号

        Returns:
            单元长度值；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("length") if elem else None

    def get_center(self, no: int) -> list | None:
        """
        根据单元编号获取单元中心点坐标

        Args:
            no: 单元编号

        Returns:
            [x, y, z] 列表；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("center") if elem else None

    def get_section_details(self, no: int) -> list | None:
        """
        根据单元编号获取截面详情

        Args:
            no: 单元编号

        Returns:
            截面详情列表；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("sectionDetails") if elem else None

    def filter_by_type(self, elem_type: int) -> list:
        """
        筛选指定类型的单元

        Args:
            elem_type: 单元类型编号 (1=Beam, 2=Truss, 3=Spring, 4=Cable, 5=Shell)

        Returns:
            符合条件的单元列表
        """
        return [e for e in self.data if e.get("type") == elem_type]

    def get_beams(self) -> list:
        """
        获取所有梁单元

        Returns:
            梁单元列表
        """
        return self.filter_by_type(1)

    def get_trusses(self) -> list:
        """
        获取所有桁架单元

        Returns:
            桁架单元列表
        """
        return self.filter_by_type(2)

    def get_springs(self) -> list:
        """
        获取所有弹簧单元

        Returns:
            弹簧单元列表
        """
        return self.filter_by_type(3)

    def get_cables(self) -> list:
        """
        获取所有拉索单元

        Returns:
            拉索单元列表
        """
        return self.filter_by_type(4)

    def get_shells(self) -> list:
        """
        获取所有壳单元

        Returns:
            壳单元列表
        """
        return self.filter_by_type(5)

    # ==================== 通用字段 ====================

    def get_characters(self, no: int) -> list | None:
        """
        根据单元编号获取字符型属性

        Args:
            no: 单元编号

        Returns:
            字符型属性列表；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("characters") if elem else None

    def get_loc_coor(self, no: int) -> dict | None:
        """
        根据单元编号获取局部坐标系

        Args:
            no: 单元编号

        Returns:
            局部坐标系 dict，包含 xDir, yDir, zDir, ox, oy, oz；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("locCoor") if elem else None

    # ==================== Beam 特有 ====================

    def get_taper(self, no: int) -> bool | None:
        """
        根据单元编号判断是否变截面梁

        Args:
            no: 单元编号

        Returns:
            是否变截面；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("isTaper") if elem else None

    def get_sec_vec(self, no: int) -> list | None:
        """
        根据单元编号获取截面编号列表

        Args:
            no: 单元编号

        Returns:
            截面编号列表；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("secVec") if elem else None

    def get_trans_vec(self, no: int) -> list | None:
        """
        根据单元编号获取截面变化次方向量

        Args:
            no: 单元编号

        Returns:
            截面变化次方向量；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("transVec") if elem else None

    def get_strain(self, no: int) -> float | None:
        """
        根据单元编号获取初应变

        Args:
            no: 单元编号

        Returns:
            初应变值；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("strain") if elem else None

    def get_beta(self, no: int) -> float | None:
        """
        根据单元编号获取 beta 角

        Args:
            no: 单元编号

        Returns:
            beta 角值；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("beta") if elem else None

    def get_beta_flag(self, no: int) -> bool | None:
        """
        根据单元编号获取 beta 角定义方式标志

        Args:
            no: 单元编号

        Returns:
            beta 角定义方式标志；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("betaFlag") if elem else None

    def get_key_pt(self, no: int) -> int | None:
        """
        根据单元编号获取关键点编号

        Args:
            no: 单元编号

        Returns:
            关键点编号；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("keyPt") if elem else None

    def get_warp(self, no: int) -> bool | None:
        """
        根据单元编号获取翘曲标志

        Args:
            no: 单元编号

        Returns:
            翘曲标志；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("warp") if elem else None

    def get_comp_thk(self, no: int) -> float | None:
        """
        根据单元编号获取组合截面厚度

        Args:
            no: 单元编号

        Returns:
            组合截面厚度；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("compThk") if elem else None

    # ==================== Spring 特有 ====================

    def is_linear(self, no: int) -> bool | None:
        """
        根据单元编号判断弹簧是否线性

        Args:
            no: 单元编号

        Returns:
            是否线性弹簧；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("isLinear") if elem else None

    def get_dof_prop(self, no: int) -> dict | None:
        """
        根据单元编号获取各自由度弹簧参数

        Args:
            no: 单元编号

        Returns:
            自由度参数 dict，键为 UX, UY, UZ, ROTX, ROTY, ROTZ；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("dofProp") if elem else None

    # ==================== Cable 特有 ====================

    def get_cable_method(self, no: int) -> int | None:
        """
        根据单元编号获取拉索参数定义方法

        Args:
            no: 单元编号

        Returns:
            拉索参数定义方法编号；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("cableMethod") if elem else None

    def get_cable_para(self, no: int) -> float | None:
        """
        根据单元编号获取拉索参数值

        Args:
            no: 单元编号

        Returns:
            拉索参数值；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("cablePara") if elem else None

    def get_cable_section(self, no: int) -> int | None:
        """
        根据单元编号获取拉索截面编号

        Args:
            no: 单元编号

        Returns:
            截面编号；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("sec") if elem else None

    def get_cable_section_detail(self, no: int) -> dict | None:
        """
        根据单元编号获取拉索截面详情

        Args:
            no: 单元编号

        Returns:
            截面详情 dict；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("sectionDetail") if elem else None

    # ==================== Shell 特有 ====================

    def is_thin(self, no: int) -> bool | None:
        """
        根据单元编号判断是否薄壳

        Args:
            no: 单元编号

        Returns:
            是否薄壳；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("isThin") if elem else None

    def get_thickness(self, no: int) -> float | None:
        """
        根据单元编号获取壳单元厚度

        Args:
            no: 单元编号

        Returns:
            壳单元厚度；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("thickness") if elem else None

    def get_node_sum(self, no: int) -> int | None:
        """
        根据单元编号获取壳单元节点数量

        Args:
            no: 单元编号

        Returns:
            节点数量；未找到返回 None
        """
        elem = self.get_by_no(no)
        return elem.get("nodeSum") if elem else None


def get_all_element_info() -> ElementInfo:
    return ElementInfo()