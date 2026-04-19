from fastapi import APIRouter

from src.routers.system.models import OpenUriReq, OpenUriRes
from src.routers.system.services import handle_open_uri

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

