from fastapi import APIRouter
from yt_dlp import YoutubeDL

from settings import FFMPEG_DIR, SITE_CONFIGS
from src.routers.download.models import (FetchVideoFormatReq, FetchVideoFormatRes, VideoFormatDetail, AudioFormatDetail,
    DownloadVideoReq, DownloadVideoRes, GetSupportedWebsiteRes)
from src.utils.cookiefile import check_cookie_file_valid
from src.utils.site import get_site_config

router = APIRouter(prefix="")

@router.post("/download-video")
async def download_video(req: DownloadVideoReq):
    url = req.url
    fmt_id = req.formatId

    config = get_site_config(url)
    if config is None:
        return DownloadVideoRes(
            status="error",
            message="[ERROR] 当前网址不支持"
        )

    cookiefile = config['cookiefile']
    outtmpl = config['outtmpl']

    outtmpl.parent.mkdir(parents=True, exist_ok=True)

    is_valid, msg = check_cookie_file_valid(cookiefile)

    if is_valid:
        ydl_opts = {
            'format': fmt_id,
            'cookiefile': str(cookiefile),
            'outtmpl': str(outtmpl),
            "sleep_interval": 3,
            "ffmpeg_location": str(FFMPEG_DIR),
        }
    else:
        ydl_opts = {
            'format': fmt_id,
            'outtmpl': str(outtmpl),
            "sleep_interval": 3,
            "ffmpeg_location": str(FFMPEG_DIR),
        }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return DownloadVideoRes(
        status="success",
        message="[SUCCESS] Successfully downloaded"
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

@router.post("/get-available-formats")
async def get_available_formats(req: FetchVideoFormatReq):
    url = req.url
    config = get_site_config(url)
    if config is None:
        return '当前网址不支持！'

    cookiefile = config['cookiefile']

    is_valid, msg = check_cookie_file_valid(cookiefile)

    if is_valid:
        ydl_opts = {
            "sleep_interval": 3,
            'cookiefile': str(cookiefile),
        }
    else:
        ydl_opts = {
            "sleep_interval": 3,
        }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.list_formats(info)

    formats = info.get('formats', [])
    if not formats:
        return {
            "status": "error",
            "message": "未能获取到可用格式信息"
        }

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
        message="可用格式已更新，可以在『视频格式』下拉框中选择想要下载的格式 ID"
    )


@router.get("/get-supported-websites")
async def get_supported_sites():
    supported_websites = [config['label'] for config in SITE_CONFIGS.values()]

    return GetSupportedWebsiteRes(
        status="success",
        websites=supported_websites,
        message="[Success] Get supported websites"
    )
