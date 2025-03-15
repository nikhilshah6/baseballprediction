import tensorflow as tf
import os
import sys
import warnings
import logging
from tensorflow.python.saved_model import tag_constants
from optparse import OptionParser
from src.get_pitch_frames import get_pitch_frames
from src.generate_overlay import generate_overlay

# Ignore warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
tf.get_logger().setLevel(logging.ERROR)

# Allow GPU memory growth
physical_devices = tf.config.experimental.list_physical_devices("GPU")
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option(
        "-f",
        "--parent_folder",
        dest="parentDir",
        help="Parent directory that contains subdirectories of pitching videos",
        default=os.path.join("videos")
    )
    (options, args) = optparser.parse_args()

    # Initialize variables
    size = 416
    iou = 0.45
    score = 0.5
    weights = os.path.join("model", "yolov4-tiny-baseball-416")

    # Load pretrained model
    saved_model_loaded = tf.saved_model.load(weights, tags=[tag_constants.SERVING])
    infer = saved_model_loaded.signatures["serving_default"]

    parentDir = options.parentDir

    # Iterate through each subdirectory in the parent folder
    for subfolder in os.listdir(parentDir):
        subfolder_path = os.path.join(parentDir, subfolder)
        if os.path.isdir(subfolder_path):
            print(f"Processing subdirectory: {subfolder_path}")
            pitch_frames = []
            width = height = fps = None  # initialize variables for overlay video
            
            # Iterate over all files in the subdirectory
            for idx, file in enumerate(os.listdir(subfolder_path)):
                video_path = os.path.join(subfolder_path, file)
                # Optional: filter files by video extensions
                if os.path.isfile(video_path) and video_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    print(f"  Processing video {idx + 1}: {video_path}")
                    try:
                        ball_frames, width, height, fps = get_pitch_frames(video_path, infer, size, iou, score)
                        pitch_frames.append(ball_frames)
                    except Exception as e:
                        print(f"  Error processing video {file} in {subfolder_path}: {e}")
            
            # If any valid pitch frames were found, generate the overlay video
            if pitch_frames and width and height and fps:
                output_filename = f"{subfolder}_overlay.avi"
                outputPath = os.path.join(subfolder_path, output_filename)
                generate_overlay(pitch_frames, width, height, fps, outputPath)
                print(f"  Overlay video saved to {outputPath}")
            else:
                print(f"  No valid pitch frames found in {subfolder_path}. Skipping overlay generation.")
