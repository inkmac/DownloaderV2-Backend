from fastapi import APIRouter

from src.routers.system.models import OpenUriReq, OpenUriRes, ChoosePathRes, OpenPathRes, OpenPathReq
from src.routers.system.services import handle_open_uri, handle_choose_path, handle_open_path

router = APIRouter(prefix="")

@router.post("/open-uri", response_model=OpenUriRes)
async def open_uri(req: OpenUriReq) -> OpenUriRes:
    uri = req.uri

    try:
        return handle_open_uri(uri)
    except Exception as e:
        return OpenUriRes(
            status="error",
            message=f"[ERROR] Unexpected error: {e}",
        )


@router.post("/open-path", response_model=OpenPathRes)
async def open_path(req: OpenPathReq) -> OpenPathRes:
    path = req.path

    try:
        return handle_open_path(path)
    except Exception as e:
        return OpenPathRes(
            status="error",
            message=f"[ERROR] Unexpected error: {e}",
        )


@router.post("/choose-path", response_model=ChoosePathRes)
async def choose_path() -> ChoosePathRes:
    try:
        return handle_choose_path()
    except Exception as e:
        return ChoosePathRes(
            status="error",
            path="",
            message=f"[ERROR] Unexpected error: {e}",
        )
