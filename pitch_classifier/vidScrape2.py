import os
import requests
from bs4 import BeautifulSoup
import re
import yt_dlp
import pandas as pd

def download_video(url: str, output_filename: str):
    # Step 1: Fetch the webpage HTML
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {url}")
        return

    # Step 2: Parse the HTML to find the video URL
    soup = BeautifulSoup(response.text, 'html.parser')
    video_tag = soup.find("video")
    if video_tag:
        source_tag = video_tag.find("source")
        video_url = source_tag["src"] if source_tag and "src" in source_tag.attrs else None
    else:
        match = re.search(r'"contentUrl":"(https://.*?)"', response.text)
        video_url = match.group(1) if match else None

    if not video_url:
        print("Could not find video URL for:", url)
        return

    print(f"Found video URL: {video_url}")

    # Step 3: Download the video using yt_dlp
    ydl_opts = {"outtmpl": output_filename}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Downloaded: {output_filename}")

if __name__ == "__main__":
    # Load the CSV into a DataFrame
    scherzer_df = pd.read_csv("scherzer_scraper_aid.csv")
    
    # Store the original video URL column name (assumed to be the last column)
    video_url_col = scherzer_df.columns[-1]
    
    # Reverse the DataFrame to get chronological order
    scherzer_df = scherzer_df.iloc[::-1].reset_index(drop=True)
    
    # Create a new column 'pitch_number' that numbers each pitch from 1 for each date.
    scherzer_df['pitch_number'] = scherzer_df.groupby('Date').cumcount() + 1

    # Iterate over each row to download videos.
    for idx, row in scherzer_df.head(1000).iterrows():
        video_link = row[video_url_col]
        date_str = str(row['Date'])  # e.g., "3/30/2018"
        pitch_num = row['pitch_number']  # e.g., 4

        # Format the date string for filename (replace '/' with '_')
        formatted_date = date_str.replace('/', '_')
        
        # Folder name is the same as the desired output file name (without extension)
        folder_name = f"{formatted_date}_{pitch_num}"
        folder_path = os.path.join("scraper_vids", folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Output filename inside that folder (folder name + ".mp4")
        output_filename = os.path.join(folder_path, f"{folder_name}.mp4")
        
        print(f"\nDownloading video from: {video_link}")
        download_video(video_link, output_filename)
