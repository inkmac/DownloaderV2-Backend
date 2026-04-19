import webbrowser

from src.routers.system.models import OpenSystemRes


def handle_system_open(target: str) -> OpenSystemRes:
    success = webbrowser.open(target, new=2, autoraise=True)

    if success:
        return OpenSystemRes(
            status="success",
            message=f"已成功打开：{target}"
        )
    else:
        return OpenSystemRes(
            status="error",
            message="系统未能启动默认浏览器，请检查默认程序设置"
        )

