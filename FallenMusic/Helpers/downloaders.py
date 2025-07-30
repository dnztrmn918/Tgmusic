import os
from yt_dlp import YoutubeDL

def audio_dl(url: str) -> str:
    cookie_path = os.path.join(os.path.dirname(__file__), "..", "cookies.txt")
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
        "prefer_ffmpeg": True,
        "cookiefile": cookie_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    }
    
    ydl = YoutubeDL(ydl_opts)
    
    sin = ydl.extract_info(url, False)
    x_file = os.path.join("downloads", f"{sin['id']}.mp3")
    if os.path.exists(x_file):
        return x_file
    ydl.download([url])
    return x_file
