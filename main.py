from pytube import Playlist
import os
from pathlib import Path
import re
import pickle


# Where to save the vids
PATH = Path.cwd()
SAVE_DOWNLOAD = str(PATH.joinpath("Downloaded"))

# Enter playlist
presence = str(input("Do you want to skip previously downloaded files as mentioned in /previous.txt? y/n "))
url = str(input("Enter link to YT-playlist: "))
convert = str(input("Download only audio instead of entire video? y/n "))
playlist = Playlist(url)
existing = os.listdir(SAVE_DOWNLOAD)

failedVideos = []
alreadyDownloaded = []
if presence == 'y' and os.path.isfile("previous.pkl"):
    with open("previous.pkl", "rb") as file:
        alreadyDownloaded = pickle.load(file)

# Download playlist
for video in playlist.videos:
    try:
        title = video.title
    except Exception as e:
        failedVideos.append(video.watch_url)
        print("failed")
        print(e)

    # For backwards compatibility with versions directly compared names without these characters
    name = re.sub(r'[<>:\"/\\|?*\'.,$#@!%€&^]', '', title) + ".mp4"
    # Add the original title to pickle
    if name in existing:
        alreadyDownloaded.append(title)
        with open("previous.pkl", "wb") as file:
            pickle.dump(alreadyDownloaded, file)

    # Depending on if user wants to redownload files, download the file
    if presence != 'y' or title not in alreadyDownloaded:
        alreadyDownloaded.append(title)
        with open("previous.pkl", "wb") as file:
            pickle.dump(alreadyDownloaded, file)

        try:
            print(title)
            if convert == 'y':
                video.streams.get_audio_only().download(SAVE_DOWNLOAD)
            else:
                video.streams.get_highest_resolution().download(SAVE_DOWNLOAD)
        except Exception as e:
            failedVideos.append(video.watch_url)
            print("failed")
            print(e)
    else:
        print("SKIPPEDDDDDDDDDDDDD: " + title)
    
with open("failed.txt", "w") as file:
    for entry in failedVideos:
        file.write(entry + "\n")