from pydantic import BaseModel


class FetchVideoFormatReq(BaseModel):
    url: str


class VideoFormatDetail(BaseModel):
    id: str     # 137
    ext: str    # mp4
    filesize: str   # 45.2MB

    res: int = 0  # 1080
    fps: float = 0.0  # 30
    vbr: float = 0.0  # 128.1
    vcodec: str = ""  # avc1.640028


class AudioFormatDetail(BaseModel):
    id: str  # 137
    ext: str  # mp4
    filesize: str  # 45.2MB

    abr: float = 0.0  # 128.1
    acodec: str = ""  # mp4a.40.2


class FetchVideoFormatRes(BaseModel):
    status: str
    videoFormats: list[VideoFormatDetail]
    audioFormats: list[AudioFormatDetail]
    message: str

