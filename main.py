from pytube import Playlist, YouTube
import os
from pathlib import Path
import re
import pickle
import mutagen


# Where to save the vids
PATH = Path.cwd()
SAVE_DOWNLOAD = str(PATH.joinpath("Downloaded"))

# Enter playlist
playlists = []
url = str(input("Enter link to YT-playlist: "))
while url != "c":
    playlists.append(Playlist(url))
    url = str(input("Enter link to next YT-playlist (enter c to cancel): "))

failedVideos = []

for playlist in playlists:
    print(playlist.title)
    for index, video_url in enumerate(playlist.video_urls):
        yt = YouTube(video_url)
        yt.streams.get_audio_only()
        # Get the name under which the video will be saved
        title = os.path.splitext(yt.streams[0].default_filename)[0]
        print(title)

        # Download the file
        if title + ".mp4" not in os.listdir(SAVE_DOWNLOAD):
            try:
                yt.streams.get_audio_only().download(SAVE_DOWNLOAD)
                print("Downloaded Succesfully")

                # Update file metadata 
                with open(str(PATH.joinpath("Downloaded", "{}.mp4".format(title))), "r+b") as file:
                    media_file = mutagen.File(file, easy=True)
                    media_file['artist'] = yt.author
                    media_file['genre'] = playlist.title
                    media_file.save(file)

            except Exception as e:
                failedVideos.append(yt.watch_url)
                print("Download Failed, Exception Occured: ")
                print(e)
        
        elif title + ".mp4" in os.listdir(SAVE_DOWNLOAD):
            # Update file metadata 
            with open(str(PATH.joinpath("Downloaded", "{}.mp4".format(title))), "r+b") as file:
                media_file = mutagen.File(file, easy=True)
                # If genre not already mentioned, add it
                genres = media_file.pprint().split("genre=")[1]
                if playlist.title not in genres.split(";"):
                    media_file['genre'] = "{};{}".format(media_file.pprint().split("genre=")[1], playlist.title)
                media_file.save(file)

        else:
            print("Download Skipped")

with open("failedDownloads.txt", "ab") as file:
    for failure in failedVideos:
        file.write(failure + "\n")