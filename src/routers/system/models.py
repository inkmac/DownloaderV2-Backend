from typing import Literal

from pydantic import BaseModel


class OpenUriReq(BaseModel):
    uri: str


class OpenUriRes(BaseModel):
    status: Literal["success", "error"]
    message: str
