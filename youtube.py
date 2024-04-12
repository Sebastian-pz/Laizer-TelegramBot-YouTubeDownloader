from pytube import YouTube

DOWNLOAD_PATH = "./downloads"


def filter_formats(video_format):
    if video_format.mime_type == "video/mp4":
        return True
    else:
        return False


class VideoDownloader:
    def __init__(self):
        self.video = None
        self.formats = []
        self.current_format = None

    def set_video(self, url):
        self.video = YouTube(url)
        self.formats = self.video.streams.filter(progressive=True)
        return self

    def get_video_info(self):
        return {
            "title": self.video.title,
            "length": self.video.length,
            "thumbnail_url": self.video.thumbnail_url
        }

    def set_format(self, format_index):
        self.current_format = self.formats[format_index]
        return self

    def download_video(self):
        self.current_format.download(output_path=DOWNLOAD_PATH)
