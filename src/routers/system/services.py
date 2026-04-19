import webbrowser

from src.routers.system.models import OpenUriRes


def handle_open_uri(uri: str) -> OpenUriRes:
    success = webbrowser.open(uri, new=2, autoraise=True)

    if success:
        return OpenUriRes(
            status="success",
            message=f"已成功打开：{uri}"
        )
    else:
        return OpenUriRes(
            status="error",
            message="系统未能启动默认浏览器，请检查默认程序设置"
        )

