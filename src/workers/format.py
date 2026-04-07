import traceback
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from src.utils.cookiefile import check_cookie_file_valid
from src.utils.custom_yt import SignalYoutubeDL
from src.utils.logger import YtLogger


class FetchFormatWorker(QThread):
    console_output = Signal(str)
    video_formats_ready = Signal(list)
    audio_formats_ready = Signal(list)

    def __init__(
            self,
            url: str,
            cookiefile: Path,
    ):
        super().__init__()
        self.url = url
        self.cookiefile = cookiefile


    def run(self):
        try:
            self.fetch_format()
        except Exception as e:
            self.console_output.emit(f"[Exception] 获取格式失败: {str(e)}")
            traceback.print_exc()


    def fetch_format(self):
        is_valid, msg = check_cookie_file_valid(self.cookiefile)
        self.console_output.emit(msg)

        if is_valid:
            ydl_opts = {
                'cookiefile': str(self.cookiefile),
                'logger': YtLogger(self.console_output),
            }
        else:
            ydl_opts = {
                'logger': YtLogger(self.console_output),
            }


        with SignalYoutubeDL(ydl_opts, console_signal=self.console_output) as ydl:
            info = ydl.extract_info(self.url, download=False)
            ydl.list_formats(info)


        formats = info.get('formats', [])
        if not formats:
            self.console_output.emit("未能获取到可用格式信息。")
            return

        video_format_ids: list[tuple[str, str]] = []
        audio_format_ids: list[tuple[str, str]] = []

        for f in formats:
            if f.get('ext') == 'mhtml':
                continue

            fmt_id = f['format_id']
            ext = f['ext']

            height = f.get('height')
            if height:
                resolution = f"{height}p"
            else:
                resolution = f.get('resolution') or 'audio only'

            abr = f.get('abr')

            if f.get('vcodec', 'none') != 'none':
                video_format_ids.append((f'{fmt_id}（{resolution} {ext}格式）', fmt_id))
            elif f.get('acodec', 'none') != 'none':
                audio_format_ids.append((f'{fmt_id}（{round(abr)}kbps {ext}格式）', fmt_id))

        # send format table
        self.console_output.emit("可用格式已更新，可以在『视频格式』下拉框中选择想要下载的格式 ID")

        # send format id signal
        self.video_formats_ready.emit(video_format_ids)
        self.audio_formats_ready.emit(audio_format_ids)
