from http.cookiejar import MozillaCookieJar

import browser_cookie3
from PySide6.QtCore import QThread, Signal

from settings import COOKIES_DIR


class CookieWorker(QThread):
    result_ready = Signal(str)

    def __init__(self, website: str, browser: str):
        super().__init__()
        self.website = website
        self.browser = browser

    def run(self):
        self.result_ready.emit('开始获取cookie...')
        try:
            cookie_path = COOKIES_DIR / f'{self.website}_cookies.txt'

            cookie_path.parent.mkdir(parents=True, exist_ok=True)
            cookie_path.touch(exist_ok=True)

            match self.browser:
                case "Google Chrome":
                    cj = browser_cookie3.chrome(domain_name=self.website)
                case "Edge":
                    cj = browser_cookie3.edge(domain_name=self.website)
                case "Firefox":
                    cj = browser_cookie3.firefox(domain_name=self.website)
                case _:
                    raise ValueError(f"Unsupported browser: {self.browser}")

            mcj = MozillaCookieJar(cookie_path)

            for cookie in cj:
                mcj.set_cookie(cookie)

            mcj.save(ignore_discard=True, ignore_expires=True)

            self.result_ready.emit(f'cookie已保存到: {cookie_path}，请不要移动或者修改')
        except Exception as e:
            self.result_ready.emit(f'获取Cookie失败，{e}')
