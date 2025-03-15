import requests
from bs4 import BeautifulSoup
import re
import yt_dlp
import pandas as pd


def download_video(url: str, title: str):

    # Step 1: Fetch the webpage HTML
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the page")
        exit()

    # Step 2: Parse the HTML to find the video URL
    soup = BeautifulSoup(response.text, 'html.parser')
    video_tag = soup.find("video")  # Direct <video> tag (if available)
    if video_tag:
        video_url = video_tag.find("source")["src"]
    else:
        # Fallback: Extract video URL from JavaScript or meta tags
        match = re.search(r'"contentUrl":"(https://.*?)"', response.text)
        video_url = match.group(1) if match else None

    if not video_url:
        print("Could not find video URL")
        exit()

    print(f"Video URL: {video_url}")

    # Step 3: Download the video
    output_filename = title + ".mp4"

    ydl_opts = {
        "outtmpl": output_filename
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"Downloaded: {output_filename}")
    
if __name__ == "__main__":
    scherzer_df = pd.read_csv("scherzer_scraper_aid.csv")
    video_links = scherzer_df.iloc[:, -1]

    count = 10
    for link in video_links:
        print("\nLink to Download: " + link + "\n")
        download_video(link, str(count))
        count -= 1
        if count == 0:
            print("Video downloading complete")
            break   
        