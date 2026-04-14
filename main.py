import os
from moviepy import VideoFileClip
from moviepy.video.fx import MultiplySpeed
from dotenv import load_dotenv
load_dotenv()

# --- SETTINGS ---
source_folder = os.getenv("SOURCE_FOLDER")
output_folder = os.getenv("OUTPUT_FOLDER")
freq = float(os.getenv("FREQ", 1.0))
width = int(os.getenv("WIDTH", 480))
duration = 10  # Length in seconds

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# --- PROCESSING ---
for filename in os.listdir(source_folder):
    if filename.endswith(".mp4"):
        video_path = os.path.join(source_folder, filename)

        # Create output filename (change .mp4 to .gif)
        gif_path = os.path.join(output_folder, filename.replace(".mp4", ".gif"))

        print(f"Processing: {filename}...")

        try:
            # Load video and subclip to 10 seconds
            with VideoFileClip(video_path).subclipped(0, duration) as clip:
                if freq != 1.0:
                    clip = clip.with_effects([MultiplySpeed(freq)])
                
                # Shrink video resolution to reduce GIF size
                if width > 0:
                    clip = clip.resized(width=width)
                    
                # 'fps' keeps the gif smooth but small
                clip.write_gif(gif_path, fps=10)
        except Exception as e:
            print(f"Could not convert {filename}: {e}")

print("Done! All videos converted.")