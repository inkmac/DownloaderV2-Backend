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

if getattr(sys, 'frozen', False):
    # noinspection PyUnresolvedReferences, PyProtectedMember
    FFMPEG_DIR = Path(sys._MEIPASS) / 'assets' / 'ffmpeg'
else:
    FFMPEG_DIR = BASE_DIR / 'assets' / 'ffmpeg'
