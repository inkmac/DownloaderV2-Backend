from pydantic import BaseModel

from src.routers.base import BaseResponse


class GeneralConfig(BaseModel):
    videoSavedPath: str
    cookieSavedPath: str


class GetGeneralConfigRes(BaseResponse):
    config: GeneralConfig | None


class UpdateGeneralConfigReq(BaseModel):
    videoSavedPath: str | None = None
    cookieSavedPath: str | None = None


UpdateGeneralConfigRes = GetGeneralConfigRes