import os
import subprocess
import sys
import webbrowser
import tkinter as tk
from multiprocessing import Queue, Process
from tkinter import filedialog

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


def _askdirectory(queue: Queue):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.focus_force()
    path = filedialog.askdirectory(title="选择视频文件夹")
    root.destroy()
    queue.put(path)

def _get_askdirectory() -> str:
    q = Queue()
    p = Process(target=_askdirectory, args=(q,))
    p.start()
    p.join()

    path = q.get() if not q.empty() else ""

    q.close()
    q.join_thread()
    p.close()
    return path

def handle_choose_path() -> ChoosePathRes:
    path = _get_askdirectory()

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