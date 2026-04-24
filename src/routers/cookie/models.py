from pydantic import BaseModel

from src.routers.base import BaseResponse


class FetchCookieReq(BaseModel):
    website: str
    browser: str


class FetchCookieRes(BaseResponse):
    savePath: str
