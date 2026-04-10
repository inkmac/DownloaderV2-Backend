from http.cookiejar import MozillaCookieJar

import browser_cookie3
from fastapi import APIRouter, HTTPException

from settings import COOKIES_DIR
from src.routers.cookie.models import FetchCookieReq, FetchCookieRes

router = APIRouter(prefix="")

@router.post("/fetch-cookie")
async def fetch_cookie(req: FetchCookieReq):
    website = req.website
    browser = req.browser

    try:
        cookie_path = COOKIES_DIR / f'{website}_cookies.txt'

        cookie_path.parent.mkdir(parents=True, exist_ok=True)
        cookie_path.touch(exist_ok=True)

        match browser.lower():
            case "chrome":
                cj = browser_cookie3.chrome(domain_name=website)
            case "edge":
                cj = browser_cookie3.edge(domain_name=website)
            case "firefox":
                cj = browser_cookie3.firefox(domain_name=website)
            case "safari":
                cj = browser_cookie3.safari(domain_name=website)
            case _:
                raise ValueError(f"Unsupported browser: {browser}")

        mcj = MozillaCookieJar(cookie_path)

        for cookie in cj:
            mcj.set_cookie(cookie)

        mcj.save(ignore_discard=True, ignore_expires=True)

        return FetchCookieRes(
            status="error",
            savePath=str(cookie_path),
            message=f"[Success] Cookie 已成功保存至\n {str(cookie_path)}\n 请不要移动或修改"
        )

    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")
