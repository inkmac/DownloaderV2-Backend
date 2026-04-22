from src.core.config import AppConfig
from src.routers.config.models import GetGeneralConfigRes, GeneralConfig, UpdateGeneralConfigRes


def handle_get_general_config() -> GetGeneralConfigRes:
    v_dir = AppConfig.get_videos_dir()
    c_dir = AppConfig.get_cookies_dir()

    return GetGeneralConfigRes(
        status="success",
        config=GeneralConfig(
            videoSavedPath=str(v_dir),
            cookieSavedPath=str(c_dir)
        ),
        message="Successfully fetched general config",
    )


def handle_update_general_config(
    *,
    video_saved_path: str | None = None,
    cookie_saved_path: str | None = None
) -> UpdateGeneralConfigRes:
    if video_saved_path is not None:
        AppConfig.set_videos_dir(video_saved_path)

    if cookie_saved_path is not None:
        AppConfig.set_cookies_dir(cookie_saved_path)

    updated_v_dir = AppConfig.get_videos_dir()
    updated_c_dir = AppConfig.get_cookies_dir()

    return UpdateGeneralConfigRes(
        status="success",
        config=GeneralConfig(
            videoSavedPath=str(updated_v_dir),
            cookieSavedPath=str(updated_c_dir)
        ),
        message="Configuration updated successfully"
    )

#         return UpdateGeneralConfigRes(
#             status="error",
#             config=None,
#             message=f"Failed to update config: {str(e)}"
#         )