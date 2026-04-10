from typing import Literal

from pydantic import BaseModel


class FetchCookieReq(BaseModel):
    website: str
    browser: str


class FetchCookieRes(BaseModel):
    status: Literal["success", "error"]
    savePath: str
    message: str
