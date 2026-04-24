from pydantic import BaseModel

from src.routers.base import BaseResponse


class OpenUriReq(BaseModel):
    uri: str


class OpenUriRes(BaseResponse):
    pass


class OpenPathReq(BaseModel):
    path: str


class OpenPathRes(BaseResponse):
    pass


class ChoosePathRes(BaseResponse):
    path: str
