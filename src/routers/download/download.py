from fastapi import APIRouter

from src.routers.download.models import (FetchVideoFormatReq, FetchVideoFormatRes, DownloadVideoReq, DownloadVideoRes,
                                         GetSupportedWebsiteRes)
from src.routers.download.services import handle_download_video, handle_get_available_formats, \
    handle_get_supported_sites

router = APIRouter(prefix="")

@router.post("/download-video", response_model=DownloadVideoRes)
def download_video(req: DownloadVideoReq) -> DownloadVideoRes:
    url = req.url
    fmt_id = req.formatId

    try:
        return handle_download_video(url, fmt_id)
    except Exception as e:
        return DownloadVideoRes(
            status="error",
            message=f"[ERROR] Unexpected error: {e}",
        )


@router.post("/get-available-formats", response_model=FetchVideoFormatRes)
def get_available_formats(req: FetchVideoFormatReq) -> FetchVideoFormatRes:
    url = req.url
    try:
        return handle_get_available_formats(url)
    except Exception as e:
        return FetchVideoFormatRes(
            status="error",
            videoFormats=[],
            audioFormats=[],
            message=f"[ERROR] Unexpected error: {e}",
        )


@router.get("/get-supported-websites", response_model=GetSupportedWebsiteRes)
async def get_supported_sites() -> GetSupportedWebsiteRes:
    try:
        return handle_get_supported_sites()
    except Exception as e:
        return GetSupportedWebsiteRes(
            status="error",
            websites=[],
            message=f"[ERROR] Unexpected error: {e}",
        )
