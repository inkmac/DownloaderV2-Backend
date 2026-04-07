from PySide6.QtWidgets import QMainWindow

from settings import SITE_CONFIGS
from src.ui.download_mainwindow import Ui_MainWindow
from src.utils.site import get_site_config
from src.workers.cookie import CookieWorker
from src.workers.download import DownloadWorker
from src.workers.format import FetchFormatWorker

STATIC_VIDEO_ITEMS = (
    ("bestvideo（自动选择最好视频格式）", "bestvideo"),
    ("None（不下载视频）", None),
)

STATIC_AUDIO_ITEMS = (
    ("bestaudio（自动选择最好音频格式）", "bestaudio"),
    ("None（不下载音频）", None),
)

class Downloader(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # init
        self.init_state()
        self.connect_signals()


    def init_state(self):
        # set combobox choices
        self.init_website_combobox()
        self.init_video_combobox()
        self.init_audio_combobox()

    def init_website_combobox(self):
        self.website_combobox.clear()
        for domain, config in SITE_CONFIGS.items():
            self.website_combobox.addItem(config['label'], domain)

    def init_video_combobox(self):
        self.video_format_id_combobox.clear()
        for item in STATIC_VIDEO_ITEMS:
            self.video_format_id_combobox.addItem(*item)

    def init_audio_combobox(self):
        self.audio_format_id_combobox.clear()
        for item in STATIC_AUDIO_ITEMS:
            self.audio_format_id_combobox.addItem(*item)

    def connect_signals(self):
        self.video_url_lineedit.textChanged.connect(self.on_video_url_changed)

        self.get_cookies_button.clicked.connect(self.get_cookies)
        self.video_download_button.clicked.connect(self.download_video)
        self.video_format_fetch_button.clicked.connect(self.fetch_video_format)

    # ------------------------------------- slot functions -------------------------------
    # cookie get functions
    def get_cookies(self):
        browser = self.browser_combobox.currentText()
        website = self.website_combobox.currentData()

        self.cookie_worker = CookieWorker(website, browser)
        self.cookie_worker.result_ready.connect(self.on_cookie_get_done)
        self.cookie_worker.start()

    def on_cookie_get_done(self, result: str):
        self.get_cookie_result_plaintextedit.setPlainText(result)

    # video download functions
    def download_video(self):
        self.clear_cmd_output()

        # get params
        url = self.video_url_lineedit.text()

        video_fmt = self.video_format_id_combobox.currentData()
        audio_fmt = self.audio_format_id_combobox.currentData()

        if video_fmt is None and audio_fmt is None:
            self.cmd_output_plaintextedit.appendPlainText('未选择下载内容')
            return
        if video_fmt is None:
            fmt = f'{audio_fmt}'
        elif audio_fmt is None:
            fmt = f'{video_fmt}'
        else:
            fmt = f'{video_fmt}+{audio_fmt}'

        config = get_site_config(url)

        if config is None:
            self.cmd_output_plaintextedit.appendPlainText('当前网址不支持！')
            return

        cookiefile = config['cookiefile']
        outtmpl = config['outtmpl']

        # start worker
        self.download_worker = DownloadWorker(url=url, fmt=fmt, outtmpl=outtmpl, cookiefile=cookiefile)
        self.download_worker.console_output.connect(self.append_console_output)
        self.download_worker.start()

    # video format fetch functions
    def fetch_video_format(self):
        self.clear_cmd_output()

        url = self.video_url_lineedit.text()

        config = get_site_config(url)
        if config is None:
            self.cmd_output_plaintextedit.appendPlainText('当前网址不支持！')
            return

        cookiefile = config['cookiefile']

        self.video_fetch_format_worker = FetchFormatWorker(url, cookiefile)
        self.video_fetch_format_worker.console_output.connect(self.append_console_output)
        self.video_fetch_format_worker.video_formats_ready.connect(self.video_fetch_format_ready)
        self.video_fetch_format_worker.audio_formats_ready.connect(self.audio_fetch_format_ready)
        self.video_fetch_format_worker.start()

    def video_fetch_format_ready(self, video_format_ids: list[tuple[str, str]]):
        self.init_video_combobox()

        for display_text, video_format_id in video_format_ids:
            self.video_format_id_combobox.addItem(display_text, userData=video_format_id)

    def audio_fetch_format_ready(self, audio_format_ids: list[tuple[str, str]]):
        self.init_audio_combobox()

        for display_text, audio_format_id in audio_format_ids:
            self.audio_format_id_combobox.addItem(display_text, userData=audio_format_id)

    def on_video_url_changed(self):
        self.init_video_combobox()
        self.init_audio_combobox()

    def append_console_output(self, message: str):
        self.cmd_output_plaintextedit.appendPlainText(message)

    # util functions
    def clear_cmd_output(self):
        self.cmd_output_plaintextedit.clear()
