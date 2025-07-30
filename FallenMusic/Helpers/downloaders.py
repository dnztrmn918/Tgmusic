import asyncio
import os
import yt_dlp
import tempfile

from FallenMusic.Helpers.channel_storage import upload_to_channel, download_from_channel
from FallenMusic.Helpers.analytics import track_play


async def audio_dl(url: str, title: str = "Unknown", video_id: str = None):
    """
    YouTube'dan müzik indirir, varsa cache kullanır, yoksa indirip kaydeder.
    """
    try:
        print(f"[DEBUG] Starting download: {url}")

        # 1. Daha önce indirildiyse kanaldan çek
        if video_id:
            cached_file = await download_from_channel(video_id)
            if cached_file:
                print(f"[DEBUG] ✅ Found in channel cache: {cached_file}")
                await track_play(video_id, title, "channel_cache")
                return cached_file

        # 2. Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_path = temp_file.name

        # 3. yt-dlp ayarları
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

        # 4. İndirme işlemi
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"[DEBUG] Downloading with yt-dlp...")
            await asyncio.get_event_loop().run_in_executor(None, ydl.download, [url])

        # 5. Başarı kontrolü
        if os.path.exists(temp_path):
            print(f"[DEBUG] ✅ Downloaded: {temp_path}")

            # 6. Kanal önbelleğine yükle (arka planda)
            if video_id:
                asyncio.create_task(
                    upload_to_channel(temp_path, video_id, title, "3:30")
                )
                await track_play(video_id, title, "youtube_download")

            return temp_path
        else:
            print(f"[DEBUG] ❌ File not found after download")
            return None

    except Exception as e:
        print(f"[DEBUG] ❌ Download error: {e}")
        return None
