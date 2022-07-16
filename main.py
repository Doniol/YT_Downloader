from pytube import Playlist
import os
from pathlib import Path
import re


# Where to save the vids
PATH = Path.cwd()
SAVE_DOWNLOAD = str(PATH.joinpath("Downloaded"))

# Enter playlist
url = str(input("Enter link to YT-playlist: "))
convert = str(input("Download only audio instead of entire video? y/n "))
playlist = Playlist(url)
existing = os.listdir(SAVE_DOWNLOAD)

# Download playlist
for video in playlist.videos:
    name = re.sub(r'[<>:\"/\\|?*\'.,$#@!%€&^]', '', video.title) + ".mp4"
    if name not in existing:
        try:
            print(name)
            if convert == 'y':
                video.streams.get_audio_only().download(SAVE_DOWNLOAD)
            else:
                video.streams.get_highest_resolution().download(SAVE_DOWNLOAD)
        except:
            print("failed")
    else:
        print("SKIPPEDDDDDDDDDDDDD: " + name)