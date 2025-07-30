import asyncio
import yt_dlp
import os

async def audio_dl(url: str, file_name: str = "audio") -> str | None:
    """
    YouTube'dan mp3 formatında ses dosyası indirir.
    İndirilen dosyayı /tmp klasörüne kaydeder (Heroku uyumlu).
    cookie dosyası aynı klasörde www.youtube.com_cookies.txt olarak beklenir.
    """
    try:
        temp_dir = "/tmp"  # Heroku'da yazılabilir temp dizini
        output_path = os.path.join(temp_dir, f"{file_name}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': os.path.join(os.path.dirname(__file__), "www.youtube.com_cookies.txt"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, ydl.download, [url])

        final_path = output_path.replace("%(ext)s", "mp3")
        if os.path.exists(final_path):
            print(f"✅ Download başarılı: {final_path}")
            return final_path
        else:
            print("❌ İndirilen dosya bulunamadı.")
            return None

    except Exception as e:
        print(f"🔴 İndirme hatası: {e}")
        return None
