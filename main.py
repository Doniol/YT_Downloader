from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from pytube import YouTube
import os
from moviepy.editor import *


# Where to save the vids
SAVE_DOWNLOAD = os.path.join(os.path.dirname(__file__), "Downloaded")
SAVE_CONVERT = os.path.join(os.path.dirname(__file__), "Converted")

# Enter playlist and it's length
url = str(input("Enter link to YT-playlist: "))
list_len = int(input("Enter playlist length: "))
convert = str(input("Download only audio instead of entire video? y/n "))
fix_failures = str(input("Do you want to try and redownload eventual failed downloads? y/n "))


# Start driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

# YT on Chrome loads only 100 vids at a time, needing to scroll down to the 100th to load the next 100
# For each 100 vids in the playlist, scroll to the end and wait 5 seconds for the vids to load
for i in range(0, list_len, 100):
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(5)

# Scrape all the data from the inspect element data from the site
soup = BeautifulSoup(driver.page_source)
# Select all desired data, filtering by classname
a_tags = soup.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})
playlist = set()
# For each data-entry, save the link to the video
for a in a_tags:
    link = a.get("href")
    link = "https://www.youtube.com" + link[0 : link.find("&")]
    print(link)
    playlist.add(link)


# # Write the video links to file (for testing purposes)
# output = open("data.txt", "w", encoding="utf-8")
# output.write(str(playlist))

driver.close()

# Counters for the amount of successes and failures
correct_count = 0
failed_count = 0
# Save the failed downloads
failures = []

# Loop through all YT-links in the playlist
print("\n", "\n", "Downloads: ")
for video in playlist:
    print(correct_count + failed_count, " - ", video)
    try:
        # Create a new data-object containing the video, change its' settings and download
        yt = YouTube(video)
        print("Fetched!")

        if convert == "y":
            stream = yt.streams.get_audio_only()
        else:
            stream = yt.streams.get_highest_resolution()

        print("Downloading ", yt.title, "...")
        stream.download(SAVE_DOWNLOAD)

        print("Downloaded")

        correct_count += 1
    except:
        # If an error occured, skip the current video
        print("Failed!")

        failed_count += 1
        failures.append(video)
    print()
print("Finished first download!")
print(failed_count, " Temporary Failures")
print(correct_count, " Temporary Successes")


# Try to redownload the failed downloads
if fix_failures == "y":
    print("\n", "\n", "Trying to fix the failures: ")
    temp = failed_count
    # Try to fix the failures i times, with i depending on the amount of failures
    for i in range(0, temp):
        if len(failures) > 0:
            # If there's no more failures left to fix, stop
            for failure in failures:
                print(failure)
                try:
                    # Create a new data-object containing the video, change its' settings and download
                    yt = YouTube(failure)
                    print("Fetched!")

                    if convert == "y":
                        stream = yt.streams.get_audio_only()
                    else:
                        stream = yt.streams.get_highest_resolution()

                    print("Downloading ", yt.title, "...")
                    stream.download(SAVE_DOWNLOAD)
                    print("Downloaded")

                    correct_count += 1
                    failed_count -= 1
                    failures.remove(failure)
                except:
                    # If an error occured, skip the current video
                    print("Failed again!")
                print()
        else:
            break
print("Finished downloading!")
print(failed_count, " Failures")
print(correct_count, " Successes")