import time
from threading import Thread

import uvicorn
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineScript
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings import WEBPAGE_PATH
from src.routers.cookie import cookie
from src.routers.download import download
from src.utils.port import is_api_ready, get_available_port

fastapi_app = FastAPI(title="Downloader API")

# noinspection PyTypeChecker
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（开发环境）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 Header
)

fastapi_app.include_router(download.router)
fastapi_app.include_router(cookie.router)


class MainWindow(QMainWindow):
    def __init__(self, port: int):
        super().__init__()
        self.view = QWebEngineView()
        self.setup_backend_port(port)

        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)

        # 加载页面
        self.view.setUrl(QUrl.fromLocalFile(WEBPAGE_PATH))
        self.setCentralWidget(self.view)


    def setup_backend_port(self, port: int):
        # 1. 定义注入的 JS 代码
        js_code = f"window.BACKEND_PORT = {port};"

        # 2. 创建脚本对象
        script = QWebEngineScript()
        script.setName("InjectedConfig")
        script.setSourceCode(js_code)

        # 3. 关键设置：在文档创建后、其他脚本执行前注入
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(True)

        # 4. 将脚本添加到页面的配置文件中
        self.view.page().profile().scripts().insert(script)


def run_fastapi(port: int):
    import sys
    import os
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

    uvicorn.run(
        fastapi_app,
        host="127.0.0.1",
        port=port,
        log_config=None,
        access_log=False,
        use_colors=False,
    )


def main():
    port = get_available_port()
    fastapi_thread = Thread(target=run_fastapi, args=(port,), daemon=True)
    fastapi_thread.start()

    for _ in range(100):
        if is_api_ready(port):
            time.sleep(0.1)
            break
        time.sleep(0.1)

    pyside_app = QApplication([])
    window = MainWindow(port)
    window.showMaximized()
    pyside_app.exec()

    # uvicorn.run(
    #     "main:fastapi_app",
    #     host="127.0.0.1",
    #     port=56000,
    # )

if __name__ == '__main__':
    main()