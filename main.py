import os
import sys
import argparse
from moviepy import VideoFileClip
from moviepy.video.fx import MultiplySpeed
from dotenv import load_dotenv

def process_video(video_path, gif_path, freq, width, duration=10):
    """Processes a single video file and converts it to GIF."""
    print(f"Processing: {video_path} -> {gif_path} (Freq: {freq}, Width: {width})")
    try:
        with VideoFileClip(video_path).subclipped(0, duration) as clip:
            if freq != 1.0:
                clip = clip.with_effects([MultiplySpeed(freq)])
            
            if width > 0:
                clip = clip.resized(width=width)
                
            clip.write_gif(gif_path, fps=10)
    except Exception as e:
        print(f"Could not convert {video_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="MPEG to GIF converter. Supports batch processing via .env or single file via arguments.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Modes:
  Mode 1 (Batch): Run without arguments. Uses SOURCE_FOLDER, OUTPUT_FOLDER, FREQ, WIDTH from .env.
  Mode 2 (Single): Run with <input> [output]. FREQ and WIDTH can be passed via --freq and --width.
        """
    )
    parser.add_argument("input", nargs="?", help="Input MP4 file path")
    parser.add_argument("output", nargs="?", help="Output GIF file path (optional)")
    parser.add_argument("--freq", type=float, help="Speed multiplier (default: 1.0 or from .env)")
    parser.add_argument("--width", type=int, help="Output width in pixels (default: 480 or from .env)")
    
    # Check if we should use .env or arguments
    # If no arguments are passed at all, we look for .env
    if len(sys.argv) == 1:
        # Mode 1: .env based
        load_dotenv()
        source_folder = os.getenv("SOURCE_FOLDER")
        output_folder = os.getenv("OUTPUT_FOLDER")
        
        if not source_folder or not output_folder:
            parser.print_help()
            print("\nError: SOURCE_FOLDER and OUTPUT_FOLDER must be set in .env for batch mode.")
            sys.exit(1)
            
        freq = float(os.getenv("FREQ", 1.0))
        width = int(os.getenv("WIDTH", 480))
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        print(f"Mode 1: Batch processing from {source_folder} to {output_folder}")
        
        files = [f for f in os.listdir(source_folder) if f.lower().endswith(".mp4")]
        if not files:
            print(f"No .mp4 files found in {source_folder}")
            return

        for filename in files:
            video_path = os.path.join(source_folder, filename)
            gif_filename = os.path.splitext(filename)[0] + ".gif"
            gif_path = os.path.join(output_folder, gif_filename)
            process_video(video_path, gif_path, freq, width)
            
        print("Batch processing complete.")
    else:
        # Mode 2: Argument based
        args = parser.parse_args()
        
        if not args.input:
            parser.print_help()
            sys.exit(1)
            
        video_path = args.input
        if not os.path.exists(video_path):
            print(f"Error: Input file '{video_path}' not found.")
            sys.exit(1)
            
        # Defaults for Mode 2 if not provided in args
        # We don't load .env here by default to keep modes distinct, 
        # but user might want .env as fallback. Let's stick to explicit args or defaults.
        freq = args.freq if args.freq is not None else 1.0
        width = args.width if args.width is not None else 480
        
        if args.output:
            gif_path = args.output
        else:
            gif_path = os.path.splitext(video_path)[0] + ".gif"
            
        print(f"Mode 2: Single file processing")
        process_video(video_path, gif_path, freq, width)
        print("Done.")

import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
