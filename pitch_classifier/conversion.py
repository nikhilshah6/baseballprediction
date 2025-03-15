import os
import pandas as pd
import shutil

# Load CSV
df = pd.read_csv("scherzer_scraper_aid.csv")

# Assume your CSV has at least the columns "Date" and "Pitch".
# Create a pitch number column for each date (starting at 1)
df['pitch_number'] = df.groupby('Date').cumcount() + 1

# Build a dictionary mapping folder names (e.g. "3_30_2018_4") to the pitch type.
folder_to_pitch = {}
for _, row in df.iterrows():
    date_str = str(row['Date'])         # e.g., "3/30/2018"
    formatted_date = date_str.replace('/', '_')  # becomes "3_30_2018"
    pitch_num = row['pitch_number']       # e.g., 4
    folder_name = f"{formatted_date}_{pitch_num}"
    folder_to_pitch[folder_name] = row['Pitch']

# Define source and destination directories
source_dir = "scraper_vids_processed"   # contains subdirectories with .avi files
target_dir = "avi_files_for_loader"       # new folder to hold all .avi files
os.makedirs(target_dir, exist_ok=True)

# Iterate over each subdirectory in source_dir
for folder in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder)
    if os.path.isdir(folder_path):
        # Check if we have a pitch mapping for this folder name.
        pitch_type = folder_to_pitch.get(folder)
        if pitch_type is None:
            print(f"Folder '{folder}' not found in CSV mapping. Skipping.")
            continue

        # Find the .avi file(s) in this subdirectory.
        avi_files = [f for f in os.listdir(folder_path) if f.endswith('.avi')]
        if not avi_files:
            print(f"No .avi file found in folder '{folder}'. Skipping.")
            continue
        
        # If multiple .avi files exist, you can choose one (here, the first one).
        avi_file = avi_files[0]
        src_file = os.path.join(folder_path, avi_file)
        
        # Create a new filename that encodes the folder name and pitch type.
        # For example: "3_30_2018_4_slider.avi" if pitch type is "slider"
        new_filename = f"{folder}_{pitch_type}.avi"
        dst_file = os.path.join(target_dir, new_filename)
        
        # Copy the file to the target directory.
        shutil.copy(src_file, dst_file)
        print(f"Copied {src_file} to {dst_file}")
