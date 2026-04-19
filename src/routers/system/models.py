from typing import Literal

from pydantic import BaseModel


class OpenSystemReq(BaseModel):
    target: str


class OpenSystemRes(BaseModel):
    status: Literal["success", "error"]
    message: str
