from typing import Literal

from pydantic import BaseModel


class OpenUriReq(BaseModel):
    uri: str


class OpenUriRes(BaseModel):
    status: Literal["success", "error"]
    message: str


class OpenPathReq(BaseModel):
    path: str


class OpenPathRes(BaseModel):
    status: Literal["success", "error"]
    message: str


class ChoosePathRes(BaseModel):
    status: Literal["success", "error"]
    path: str
    message: str
