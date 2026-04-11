import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

if getattr(sys, 'frozen', False):
    # noinspection PyUnresolvedReferences, PyProtectedMember
    WEBPAGE_PATH = Path(sys._MEIPASS) / 'static' / 'index.html'
else:
    WEBPAGE_PATH = BASE_DIR / 'static' / 'index.html'

COOKIES_DIR = BASE_DIR / 'data' / 'cookies'
VIDEOS_DIR = BASE_DIR / 'data' / 'videos'
DOWNLOAD_CONFIGS_PATH = BASE_DIR / 'data' / 'config' / 'download_config.json'

if getattr(sys, 'frozen', False):
    # noinspection PyUnresolvedReferences, PyProtectedMember
    FFMPEG_DIR = Path(sys._MEIPASS) / 'assets' / 'ffmpeg'
else:
    FFMPEG_DIR = BASE_DIR / 'assets' / 'ffmpeg'

SITE_CONFIGS = {
    'bilibili.com': {
        'label': 'bilibili',
        'cookiefile': COOKIES_DIR / 'bilibili.com_cookies.txt',
        'outtmpl': VIDEOS_DIR / 'bilibili' / '%(title)s.%(ext)s',
    },
    'youtube.com': {
        'label': 'youtube',
        'cookiefile': COOKIES_DIR / 'youtube.com_cookies.txt',
        'outtmpl': VIDEOS_DIR / 'youtube' / '%(title)s.%(ext)s',
    }
}