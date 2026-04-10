import time
from multiprocessing import Process

import uvicorn
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings import WEBPAGE_PATH
from src.routers.cookie import cookie
from src.routers.download import download
from src.utils.port import is_api_ready

fastapi_app = FastAPI(title="Downloader API")

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
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()

        # 加载页面
        self.browser.setUrl(QUrl.fromLocalFile(WEBPAGE_PATH))
        self.setCentralWidget(self.browser)


def run_fastapi(port: int):
    uvicorn.run(fastapi_app, host="127.0.0.1", port=port)


def main():
    port = 56000
    fastapi_process = Process(target=run_fastapi, args=(port,))
    fastapi_process.start()

    for _ in range(100):
        if is_api_ready(port):
            time.sleep(2)
            break
        time.sleep(0.1)

    pyside_app = QApplication([])
    window = MainWindow()
    settings = window.browser.settings()
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
    window.showMaximized()
    pyside_app.exec()

    # uvicorn.run(
    #     "main:fastapi_app",
    #     host="127.0.0.1",
    #     port=56000,
    # )

if __name__ == '__main__':
    main()