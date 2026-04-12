from typing import TypedDict, Protocol, Any


class YdlLoggerProtocol(Protocol):
    """yt-dlp 要求的日志对象协议"""
    def debug(self, msg: str) -> None: ...
    def warning(self, msg: str) -> None: ...
    def error(self, msg: str) -> None: ...


class YdlProgressHookProtocol(Protocol):
    """yt-dlp 进度回调函数的协议"""
    def __call__(self, status: dict[str, Any]) -> None: ...


class YdlOpts(TypedDict, total=False):
    """
    yt-dlp 常用配置项的类型定义
    total=False 表示所有字段都是可选的
    """
    # 基础下载配置
    format: str
    outtmpl: str

    # 文件与路径
    cookiefile: str
    ffmpeg_location: str

    # 网络与间隔
    sleep_interval: int
    max_sleep_interval: int

    # 日志与控制
    logger: YdlLoggerProtocol
    progress_hooks: list[YdlProgressHookProtocol]
    quiet: bool
    no_warnings: bool
    ignoreerrors: bool
