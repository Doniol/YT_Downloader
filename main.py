from pytubefix import Playlist, YouTube
import os
from pathlib import Path
import re
import pickle
import mutagen


# Where to save the vids
PATH = Path.cwd()
SAVE_DOWNLOAD = str(PATH.joinpath("Downloaded"))
failedVideos = []

playlists = []
with open(str(PATH.joinpath("playlist-urls.txt")), "r") as file:
    for line in file:
        tempUrls = line.strip("\n").split(",")
        for url in tempUrls:
            playlists.append(Playlist(url))

for playlist in playlists:
    print(playlist.title)
    for index, video_url in enumerate(playlist.video_urls):
        yt = YouTube(video_url)
        try:
            yt.streams.get_audio_only()
            # Get the name under which the video will be saved
            title = os.path.splitext(yt.streams[0].default_filename)[0]
            title = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", title)
            print(title)

            # Download the file
            if title + ".m4a" not in os.listdir(SAVE_DOWNLOAD):
                try:
                    yt.streams.get_audio_only().download(SAVE_DOWNLOAD, title + ".m4a")
                    print("Downloaded Succesfully")

                    # Update file metadata 
                    print(str(PATH.joinpath("Downloaded", "{}.m4a".format(title))))
                    with open(str(PATH.joinpath("Downloaded", "{}.m4a".format(title))), "r+b") as file:
                        media_file = mutagen.File(file, easy=True)
                        media_file['artist'] = yt.author
                        media_file['genre'] = playlist.title
                        media_file.save(file)

                except Exception as e:
                    failedVideos.append(yt.watch_url)
                    print("Download Failed, Exception Occured: ")
                    print(e)
            
            elif title + ".m4a" in os.listdir(SAVE_DOWNLOAD):
                # Update file metadata 
                with open(str(PATH.joinpath("Downloaded", "{}.m4a".format(title))), "r+b") as file:
                    media_file = mutagen.File(file, easy=True)
                    # If genre not already mentioned, add it
                    genres = media_file.pprint().split("genre=")[1]
                    if playlist.title not in genres.split(";"):
                        media_file['genre'] = "{};{}".format(media_file.pprint().split("genre=")[1], playlist.title)
                    media_file.save(file)

            else:
                print("Download Skipped")
                
        except Exception as e:
            failedVideos.append(yt.watch_url)
            print("Download Failed, Exception Occured: ")
            print(e)


with open("failedDownloads.txt", "a") as file:
    for failure in failedVideos:
        file.write(failure + "\n")
