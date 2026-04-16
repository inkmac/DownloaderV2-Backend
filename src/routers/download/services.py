from yt_dlp import YoutubeDL

from settings import FFMPEG_DIR, SITE_CONFIGS
from src.routers.download.models import AudioFormatDetail, VideoFormatDetail, FetchVideoFormatRes, DownloadVideoRes, \
    GetSupportedWebsiteRes, GetDownloadOutputsRes
from src.utils.cookiefile import check_cookie_file_valid
from src.utils.logger import YdlLogger
from src.utils.site import get_site_config, is_url_supported
from src.utils.ydl_types import YdlOpts


def handle_download_video(url: str, fmt_id: str, outputs: list[str]) -> DownloadVideoRes:
    if not is_url_supported(url):
        return DownloadVideoRes(
            status="error",
            message="[ERROR] 当前网址不支持\n"
        )

    config = get_site_config(url)

    cookiefile = config['cookiefile']
    outtmpl = config['outtmpl']

    outtmpl.parent.mkdir(parents=True, exist_ok=True)

    is_valid, msg = check_cookie_file_valid(cookiefile)

    if is_valid:
        ydl_opts: YdlOpts = {
            'format': fmt_id,
            'cookiefile': str(cookiefile),
            'outtmpl': str(outtmpl),
            "sleep_interval": 3,
            "ffmpeg_location": str(FFMPEG_DIR),
            "logger": YdlLogger(outputs)
        }
    else:
        ydl_opts: YdlOpts = {
            'format': fmt_id,
            'outtmpl': str(outtmpl),
            "sleep_interval": 3,
            "ffmpeg_location": str(FFMPEG_DIR),
            "logger": YdlLogger(outputs)
        }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return DownloadVideoRes(
        status="success",
        message=(
            "[SUCCESS] Successfully downloaded\n"
            f"[SUCCESS] Saved to : {str(outtmpl.parent)}\n"
        )
    )


def handle_get_download_outputs(download_outputs: list[str]) -> GetDownloadOutputsRes:
    current_outputs = download_outputs.copy()
    download_outputs.clear()
    return GetDownloadOutputsRes(
        status="success",
        outputs=current_outputs,
        message="[SUCCESS] Successfully get download outputs\n"
    )


def format_size(size_bytes):
    """将字节大小转换为更易读的格式 (MB/GB)"""
    if not size_bytes:
        return "未知大小"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"


def handle_get_available_formats(url: str) -> FetchVideoFormatRes:
    if not is_url_supported(url):
        return FetchVideoFormatRes(
            status="error",
            videoFormats=[],
            audioFormats=[],
            message="[ERROR] 当前网址不支持！\n"
        )

    config = get_site_config(url)

    cookiefile = config['cookiefile']

    is_valid, msg = check_cookie_file_valid(cookiefile)

    if is_valid:
        ydl_opts: YdlOpts = {
            "sleep_interval": 3,
            'cookiefile': str(cookiefile),
        }
    else:
        ydl_opts: YdlOpts = {
            "sleep_interval": 3,
        }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.list_formats(info)

    formats = info.get('formats', [])
    if not formats:
        return FetchVideoFormatRes(
            status="error",
            videoFormats=[],
            audioFormats=[],
            message="[ERROR] 未能获取到可用格式信息\n"
        )

    video_formats: list[VideoFormatDetail] = []
    audio_formats: list[AudioFormatDetail] = []

    for f in formats:
        if f.get('ext') == 'mhtml':
            continue

        fmt_id = f['format_id']
        ext = f['ext']
        filesize_raw = f.get('filesize') or f.get('filesize_approx')
        filesize = format_size(filesize_raw)

        # 视频分支
        if f.get('vcodec', 'none') != 'none':
            height = f.get('height')
            fps = f.get('fps')
            vbr = f.get('vbr')
            vcodec = f.get('vcodec')

            video_formats.append(VideoFormatDetail(
                id=fmt_id,
                ext=ext,
                filesize=filesize,

                res=height,
                fps=fps,
                vbr=vbr,
                vcodec=vcodec,
            ))

        # 音频分支
        elif f.get('acodec', 'none') != 'none':
            abr = f.get('abr')
            acodec = f.get('acodec', 'unknown acodec')

            audio_formats.append(AudioFormatDetail(
                id=fmt_id,
                ext=ext,
                filesize=filesize,

                abr=abr,
                acodec=acodec
            ))


    return FetchVideoFormatRes(
        status="success",
        videoFormats=video_formats,
        audioFormats=audio_formats,
        message="[SUCCESS] 可用格式已更新，可以在『视频格式』下拉框中选择想要下载的格式 ID\n"
    )


def handle_get_supported_sites() -> GetSupportedWebsiteRes:
    supported_websites = [config['label'] for config in SITE_CONFIGS.values()]

    return GetSupportedWebsiteRes(
        status="success",
        websites=supported_websites,
        message="[Success] Get supported websites\n"
    )