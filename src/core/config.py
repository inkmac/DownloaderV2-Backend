from pathlib import Path
from PySide6.QtCore import QSettings

from settings import BASE_DIR


class AppConfig:
    _config = QSettings("Inkmac", "DownloaderV2")

    @classmethod
    def get_videos_dir(cls):
        default_path = BASE_DIR / 'data' / 'videos'
        path = str(cls._config.value("paths/videos_dir", str(default_path)))
        return Path(path)

    @classmethod
    def set_videos_dir(cls, path: Path | str):
        cls._config.setValue("paths/videos_dir", str(path))


    @classmethod
    def get_cookies_dir(cls):
        default_path = BASE_DIR / 'data' / 'cookies'
        path = str(cls._config.value("paths/cookies_dir", str(default_path)))
        return Path(path)

    @classmethod
    def set_cookies_dir(cls, path: Path | str):
        cls._config.setValue("paths/cookies_dir", str(path))


    @classmethod
    def get_site_configs(cls):
        videos_dir = cls.get_videos_dir()
        cookies_dir = cls.get_cookies_dir()

        return {
            'bilibili.com': {
                'label': 'bilibili',
                'cookiefile': cookies_dir / 'bilibili.com_cookies.txt',
                'outtmpl': videos_dir / 'bilibili' / '%(title)s.%(ext)s',
            },
            'youtube.com': {
                'label': 'youtube',
                'cookiefile': cookies_dir / 'youtube.com_cookies.txt',
                'outtmpl': videos_dir / 'youtube' / '%(title)s.%(ext)s',
            }
        }
