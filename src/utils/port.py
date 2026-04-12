import http.client

import http.client
import socket


def is_api_ready(port: int):
    conn = None
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=0.2)
        conn.request("GET", "/")
        response = conn.getresponse()
        # 只要能拿到响应对象（哪怕是 404），说明 FastAPI 已经接客了
        return response.status > 0
    except (http.client.HTTPException, socket.error, Exception):
        # 捕捉所有异常，因为启动瞬间可能会有各种网络握手错误
        return False
    finally:
        if conn:
            conn.close()


def get_available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        return port