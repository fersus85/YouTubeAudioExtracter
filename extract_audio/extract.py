from pathlib import Path

from pytube import YouTube

import subprocess


class YouTubeAudioExtracter:
    """ Download mp4 video from YouTube and save it in mp3 file"""

    def __init__(self, link):
        self.link = link
        self.pytube_object = YouTube(self.link)

    def find_tag(self) -> None:
        ''' Print list of tags. By tags you can choose which format
            you can download.
        '''
        print(*[self.pytube_object.streams[tag]
                for tag in range(len(self.pytube_object.streams))], sep='\n')

    def download_youtube_video(self, name: str = 'output.mp4',
                               tag: int = 140) -> None:
        ''' Download video from YouTube by choosen tag, by default 140 '''
        stream = self.pytube_object.streams.get_by_itag(tag)
        stream.download('source', filename=name)
        return name

    def convert_to_mp3(self, file: str) -> None:
        ''' Convert mp4 -> mp3 and save in file '''
        video_file = Path(f'source/{file}')
        match file:
            case 'output.mp4': out_name = 'audio.mp3'
            case _: out_name = f'{file}.mp3'
        command = f"ffmpeg -i {video_file} -b:a 320k {out_name}"
        subprocess.call(command, shell=True)


yt = YouTubeAudioExtracter('https://www.youtube.com/watch?v=hF_hul5k07A')
# yt.find_tag()
from_ = yt.download_youtube_video(name='python_speed_py')
yt.convert_to_mp3(from_)
