import os
import yt_dlp
import tempfile

def audio_dl(url: str) -> str:
    try:
        # Geçici mp3 dosyası oluştur
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_path = temp_file.name

        ydl_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "outtmpl": temp_path,
            "extractaudio": True,
            "audioformat": "mp3",
            "audioquality": "192",
            "no_warnings": True,
            "quiet": True,
            "no_playlist": True,
        }

        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.download([url])

        if os.path.exists(temp_path):
            return temp_path
        else:
            return None

    except Exception as e:
        print(f"Download error: {e}")
        return None
