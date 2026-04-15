from fastapi import APIRouter

from src.routers.cookie.models import FetchCookieReq, FetchCookieRes
from src.routers.cookie.services import handle_fetch_cookie

router = APIRouter(prefix="")

@router.post("/fetch-cookie", response_model=FetchCookieRes)
def fetch_cookie(req: FetchCookieReq)-> FetchCookieRes:
    website = req.website
    browser = req.browser

    try:
        return handle_fetch_cookie(website, browser)
    except Exception as e:
        return FetchCookieRes(
            status="error",
            savePath="",
            message=f"[ERROR] {e}\n"
        )
