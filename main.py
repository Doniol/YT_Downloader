from pytube import Playlist
import os


# Where to save the vids
SAVE_DOWNLOAD = os.path.join(os.path.dirname(__file__), "Downloaded")

# Enter playlist
url = str(input("Enter link to YT-playlist: "))
convert = str(input("Download only audio instead of entire video? y/n "))
playlist = Playlist(url)

# Download playlist
for video in playlist.videos:
    if convert == 'y':
        video.streams.get_audio_only().download(SAVE_DOWNLOAD)
    else:
        video.streams.get_highest_resolution().download(SAVE_DOWNLOAD)