from PySide6.QtWidgets import QApplication

from src.downloader import Downloader


def main():
    app = QApplication([])
    window = Downloader()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()