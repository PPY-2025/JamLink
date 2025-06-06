import os
from yt_dlp import YoutubeDL
import imageio_ffmpeg

class AudioLoader:
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = output_dir
        self.ffmpeg_location = imageio_ffmpeg.get_ffmpeg_exe()
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def _url_to_filename(url: str) -> str:
        safe = url.replace("://", "_").replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
        return safe + ".mp3"

    def get_title(self, url: str) -> str:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['title']

    def download(self, url: str):
        output_path = os.path.join(self.output_dir, self._url_to_filename(url))
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path.replace(".mp3", ".%(ext)s"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
        if self.ffmpeg_location:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_location

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
