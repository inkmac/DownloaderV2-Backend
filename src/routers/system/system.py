from fastapi import APIRouter

from src.routers.system.models import OpenSystemReq, OpenSystemRes
from src.routers.system.services import handle_system_open

router = APIRouter(prefix="")

@router.post("/open-system", response_model=OpenSystemRes)
async def system_open(req: OpenSystemReq) -> OpenSystemRes:
    target = req.target

    try:
        return handle_system_open(target)
    except Exception as e:
        return OpenSystemRes(
            status="error",
            message=f"[ERROR] Unexpected error: {e}",
        )

