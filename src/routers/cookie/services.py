from http.cookiejar import MozillaCookieJar

import browser_cookie3

from settings import COOKIES_DIR
from src.routers.cookie.models import FetchCookieRes


def handle_fetch_cookie(website: str, browser: str) -> FetchCookieRes:
    cookie_path = COOKIES_DIR / f'{website}_cookies.txt'

    cookie_path.parent.mkdir(parents=True, exist_ok=True)
    cookie_path.touch(exist_ok=True)

    browser_name = browser.lower()
    if browser_name == "chrome":
        cj = browser_cookie3.chrome(domain_name=website)
    elif browser_name == "edge":
        cj = browser_cookie3.edge(domain_name=website)
    elif browser_name == "firefox":
        cj = browser_cookie3.firefox(domain_name=website)
    elif browser_name == "safari":
        cj = browser_cookie3.safari(domain_name=website)
    else:
        return FetchCookieRes(
            status="error",
            savePath='',
            message=f"Unsupported browser: {browser}"
        )

    mcj = MozillaCookieJar(cookie_path)

    for cookie in cj:
        mcj.set_cookie(cookie)

    mcj.save(ignore_discard=True, ignore_expires=True)

    return FetchCookieRes(
        status="error",
        savePath=str(cookie_path),
        message=f"[Success] Cookie 已成功保存至\n {str(cookie_path)}\n 请不要移动或修改\n"
    )