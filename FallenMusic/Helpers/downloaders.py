import asyncio
import os
import yt_dlp
import tempfile

async def audio_dl(url: str, title: str = "Unknown", video_id: str = None):
    """
    Youtube'dan hızlı audio indirme (herkese açık videolar için).
    """
    try:
        print(f"DEBUG: Starting audio download for URL: {url}")

        # Temp dosya oluştur
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_path = temp_file.name

        # yt-dlp seçenekleri (cookies.txt yok!)
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': temp_path,
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192',
            'no_warnings': True,
            'quiet': True,
            'no_playlist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"DEBUG: yt-dlp processing...")
            await asyncio.get_event_loop().run_in_executor(
                None, ydl.download, [url]
            )

        if os.path.exists(temp_path):
            print(f"DEBUG: ✅ Download successful: {temp_path}")
            return temp_path
        else:
            print(f"DEBUG: ❌ Download failed - file not found")
            return None

    except Exception as e:
        print(f"DEBUG: Download error: {e}")
        return None
