import os
import yt_dlp

def audio_dl(url: str) -> str:
    download_folder = "downloads"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    try:
        ydl_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "outtmpl": os.path.join(download_folder, "%(id)s.%(ext)s"),
            "extractaudio": True,
            "audioformat": "mp3",
            "audioquality": "192",
            "no_warnings": True,
            "quiet": True,
            "no_playlist": True,
        }

        ydl = yt_dlp.YoutubeDL(ydl_opts)
        info = ydl.extract_info(url, download=True)
        file_path = os.path.join(download_folder, f"{info['id']}.mp3")

        if os.path.exists(file_path):
            return file_path
        else:
            print("[ERROR] İndirilen dosya bulunamadı.")
            return None

    except Exception as e:
        print(f"Download error: {e}")
        return None
