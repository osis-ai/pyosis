from ..core import REGISTRY

@REGISTRY.register('Node')
def osis_node(nNO: int=1, x: float=0.0, y: float=0.0, z: float=0.0):
    """创建一个节点

    Args:
        nNO (int): 节点编号，从 1 开始编号。
        x (float): 节点X坐标
        y (float): 节点Y坐标
        z (float): 节点Z坐标
        
    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('NodeDel')
def osis_node_del(nNO: int=1):
    """删除一个节点

    Args:
        nNO (int): 节点编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

@REGISTRY.register('NodeMod')
def osis_node_mod(nOld: int=1, nNew: int=2):
    """修改一个节点的编号。节点编号存在时，交换

    Args:
        nOld (int): 旧编号
        nNew (int): 新编号

    Returns:
        tuple (bool, str):
            - bool: 操作是否成功
            - str: 失败原因（如果操作失败）
    """
    pass

# @REGISTRY.register('test')
# def test(a: int=1, b: bool=1, c:str=None):
#     pass
