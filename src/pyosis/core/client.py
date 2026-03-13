import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ========== 全局初始化：连接池 Session（只创建一次） ==========
# 配置重试策略
retry_strategy = Retry(
    total=3,                # 最多重试3次
    backoff_factor=0.1,      # 重试间隔：0.1, 0.2, 0.4... 秒
    status_forcelist=[429, 500, 502, 503, 504]  # 遇到这些状态码自动重试
)

# 配置连接池适配器
adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=10,    # 最大连接池数
    pool_maxsize=100         # 每个池最大连接数
)

# 创建全局 Session
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)  # 如果你后续用HTTPS

# ========== 通用客户端函数（复用连接池） ==========
def osis_client(func_name: str, payload: dict) -> dict | tuple[bool, str]:
    """
    通用 OSIS 接口客户端（复用连接池，高效批量调用）
    Args:
        func_name: C++ 接口名（如 "OSIS_Run", "OSIS_Run_Batch"）
        payload: 请求参数字典（自动序列化为 JSON）
    Returns: 
        异常时返回 (False, 错误信息)
    """
    url = f"http://localhost:8080/{func_name}"
    
    try:
        # 复用连接池发送 POST 请求
        response = session.post(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=30  # 批量调用适当延长超时
        )
        response.raise_for_status()  # 抛出 HTTP 状态码错误
        return tuple(response.json())
        
    except Exception as e:
        # 异常时保持和 C++ 一致的返回格式
        return False, f"调用失败: {str(e)}"