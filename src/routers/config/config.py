from fastapi import APIRouter

from src.routers.config.models import GetGeneralConfigRes, UpdateGeneralConfigRes, UpdateGeneralConfigReq
from src.routers.config.services import handle_get_general_config, handle_update_general_config

router = APIRouter(prefix="/config")

@router.get("/general", response_model=GetGeneralConfigRes)
def get_general_config() -> GetGeneralConfigRes:
    try:
        return handle_get_general_config()
    except Exception as e:
        return GetGeneralConfigRes(
            status="error",
            config=None,
            message=f"[ERROR] Unexpected error: {e}",
        )


@router.put("/general", response_model=UpdateGeneralConfigRes)
async def update_general_config(req: UpdateGeneralConfigReq) -> UpdateGeneralConfigRes:
    video_saved_path = req.videoSavedPath
    cookie_saved_path = req.cookieSavedPath

    try:
        return handle_update_general_config(
            video_saved_path=video_saved_path,
            cookie_saved_path=cookie_saved_path
        )
    except Exception as e:
        return UpdateGeneralConfigRes(
            status="error",
            config=None,
            message=f"[ERROR] Unexpected error during update: {e}",
        )
