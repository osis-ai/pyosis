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
        func_name: C++ 接口名（如 "OSIS_Run"）
        payload: 请求参数字典（自动序列化为 JSON）
    Returns:
        异常时返回 (False, 错误信息)
    """
    url = f"http://localhost:8080/{func_name}"

    try:
        response = session.post(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=30,
        )

        data = None
        if response.content:
            try:
                data = response.json()
            except ValueError:
                pass

        # 接口不存在
        if response.status_code == 404:
            return {"success": False, "error": f"接口不存在: {func_name}"}
        # 200
        # if response.ok:
        return data if data is not None else {"success": False }

        # 500
        # # 500：[false, "命令流中……"]
        # if isinstance(data, list) and len(data) >= 2 and data[0] is False:
        #     return False, str(data[1])

        # 无结构化 body 时退回文本 / 状态码
        # detail = response.text.strip() if response.text else ""
        # return {"success": False, "error": detail if detail else f"HTTP {response.status_code}"}# False, detail if detail else f"HTTP {response.status_code}"

    except requests.RequestException as e:
        return {"success": False, "error": f"调用失败: {str(e)}"}