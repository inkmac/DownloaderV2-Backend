from threading import Thread

import uvicorn
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from fastapi import FastAPI

from settings import WEBPAGE_PATH

fastapi_app = FastAPI(title="Downloader API")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()

        # 加载页面
        self.browser.setUrl(QUrl.fromLocalFile(WEBPAGE_PATH))
        self.setCentralWidget(self.browser)


def run_fastapi():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)


def main():
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    pyside_app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    pyside_app.exec()


if __name__ == '__main__':
    main()