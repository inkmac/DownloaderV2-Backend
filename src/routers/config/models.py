from typing import Literal

from pydantic import BaseModel


class GeneralConfig(BaseModel):
    videoSavedPath: str
    cookieSavedPath: str


class GetGeneralConfigRes(BaseModel):
    status: Literal["success", "error"]
    config: GeneralConfig | None
    message: str


class UpdateGeneralConfigReq(BaseModel):
    videoSavedPath: str | None = None
    cookieSavedPath: str | None = None


UpdateGeneralConfigRes = GetGeneralConfigRes