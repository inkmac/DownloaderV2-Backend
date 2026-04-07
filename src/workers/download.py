import traceback
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL

from settings import FFMPEG_DIR
from src.utils.cookiefile import check_cookie_file_valid
from src.utils.logger import YtLogger


class DownloadWorker(QThread):
    console_output = Signal(str)

    def __init__(
            self,
            url: str,
            fmt: str,
            outtmpl: Path,
            cookiefile: Path,
    ):
        super().__init__()
        self.url = url
        self.fmt = fmt
        self.outtmpl = outtmpl
        self.cookiefile = cookiefile


    def run(self):
        try:
            self.download()
        except Exception as e:
            self.console_output.emit(f'[Exception] {str(e)}')
            traceback.print_exc()

    def download(self):
        self.outtmpl.parent.mkdir(parents=True, exist_ok=True)

        is_valid, msg = check_cookie_file_valid(self.cookiefile)
        self.console_output.emit(msg)

        if is_valid:
            ydl_opts = {
                'format': self.fmt,
                'cookiefile': str(self.cookiefile),
                'outtmpl': str(self.outtmpl),
                'logger': YtLogger(self.console_output),
                "ffmpeg_location": str(FFMPEG_DIR),
            }
        else:
            ydl_opts = {
                'format': self.fmt,
                'outtmpl': str(self.outtmpl),
                'logger': YtLogger(self.console_output),
                "ffmpeg_location": str(FFMPEG_DIR),
            }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        self.console_output.emit("[Success] Download Complete")
