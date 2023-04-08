from pytube import Playlist, YouTube
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

print(playlist.title)
for index, video_url in enumerate(playlist.video_urls):
    try:
        yt = YouTube(video_url)
        yt.streams.get_audio_only()
        title = yt.title
        print(title)

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
                if convert == 'y':
                    yt.streams.get_audio_only().download(SAVE_DOWNLOAD)
                else:
                    yt.streams.get_highest_resolution().download(SAVE_DOWNLOAD)
                print("Downloaded Succesfully")
            except Exception as e:
                failedVideos.append(yt.watch_url)
                print("Download Failed, Exception Occured: ")
                print(e)
        else:
            print("Download Skipped")

    except Exception as e:
        print(e)

with open("failedDownloads.txt", "ab") as file:
    for failure in failedVideos:
        file.write(failure + "\n")