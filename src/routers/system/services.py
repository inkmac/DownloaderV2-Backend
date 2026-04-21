import os
import subprocess
import sys
import webbrowser

from src.routers.system.models import OpenUriRes, ChoosePathRes, OpenPathRes


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


def handle_open_path(path: str) -> OpenPathRes:
    if sys.platform == "darwin":
        subprocess.run(["open", path], check=True)

    elif sys.platform == "win32":
        os.startfile(os.path.normpath(path))

    else:
        return OpenPathRes(status="error", message="Platform not supported")

    return OpenPathRes(status="success", message="文件夹已打开")


def handle_choose_path() -> ChoosePathRes:
    # macOS
    if sys.platform == "darwin":
        res = subprocess.run(
            [
                "osascript",
                "-e",
                'POSIX path of (choose folder with prompt "选择视频文件夹")'
            ],
            capture_output=True,
            text=True,
        )
        path = res.stdout.strip()

    # Windows
    elif sys.platform == "win32":
        res = subprocess.run(
            [
                "powershell",
                "-Command",
                ("$app = New-Object -ComObject Shell.Application; "
                 "$folder = $app.BrowseForFolder(0, '选择文件夹', 0, 0); "
                 "if ($folder) { $folder.Self.Path }")
            ],
            capture_output=True,
            text=True,
            creationflags=0x08000000
        )
        path = res.stdout.strip()

    else:
        return ChoosePathRes(
            status="error",
            path="",
            message="Platform not supported"
        )

    if path:
        return ChoosePathRes(
            status="success",
            path=path,
            message="Success"
        )
    else:
        return ChoosePathRes(
            status="error",
            path="",
            message="User did not select a path"
        )