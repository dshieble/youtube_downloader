#!/usr/bin/env python3

import argparse
import yt_dlp
import ffmpeg
import os
import re
import shutil

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    if not shutil.which('ffmpeg'):
        raise RuntimeError(
            "ffmpeg not found. Please install it first:\n"
            "  On MacOS: brew install ffmpeg\n"
            "  On Ubuntu/Debian: sudo apt-get install ffmpeg\n"
            "  On Windows: download from https://ffmpeg.org/download.html"
        )

def parse_timestamp(timestamp):
    """Convert timestamp in format MM:SS to seconds"""
    match = re.match(r'(\d+):(\d{2})', timestamp)
    if not match:
        raise ValueError("Time must be in format MM:SS")
    minutes, seconds = map(int, match.groups())
    return minutes * 60 + seconds

def sanitize_filename(filename):
    """Remove special characters from filename"""
    # Replace special characters with underscore
    sanitized = re.sub(r'[^\w\-_\. ]', '_', filename)
    # Replace spaces with underscore
    sanitized = sanitized.replace(' ', '_')
    return sanitized

def download_video_segment(url, start_time, length, output_path):
    """Download a segment of a YouTube video"""
    # Check for ffmpeg first
    check_ffmpeg()
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(os.path.expanduser(output_path))
    os.makedirs(output_dir, exist_ok=True)

    # Convert start_time to seconds
    start_seconds = parse_timestamp(start_time)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'best',  # Best quality
        'quiet': True,
        'nocheckcertificate': True,
    }

    try:
        # Get video information
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = sanitize_filename(info['title'])
            temp_video_path = os.path.join(output_dir, f"{video_title}.{info['ext']}")
            
            # Set the output template for yt-dlp
            ydl_opts['outtmpl'] = temp_video_path
            
            # Download the video
            print(f"Downloading video: {info['title']}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Use ffmpeg to trim the video
            print(f"Trimming video from {start_time} for {length} seconds...")
            try:
                (
                    ffmpeg
                    .input(temp_video_path, ss=start_seconds, t=length)
                    .output(os.path.expanduser(output_path), acodec='copy', vcodec='copy')
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
            except ffmpeg._run.Error as e:
                print(f"FFmpeg error occurred:\nOutput: {e.stdout.decode()}\nError: {e.stderr.decode()}")
                raise

            # Remove the original full video
            os.remove(temp_video_path)
            
            print(f"\nSuccess! Video segment saved to: {output_path}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Download a segment of a YouTube video')
    parser.add_argument('--url', required=True, help='YouTube video URL')
    parser.add_argument('--start_time', required=True, help='Start time in format MM:SS')
    parser.add_argument('--length', required=True, type=int, help='Length of segment in seconds')
    parser.add_argument('--output', required=True, help='Output path for the mp4 file')
    
    args = parser.parse_args()
    
    # Set default output path if not provided
    if not args.output:
        args.output = "output.mp4"
    
    download_video_segment(args.url, args.start_time, args.length, args.output)

if __name__ == "__main__":
    
    """
    python download_youtube_segment.py \
      --url https://www.youtube.com/watch?v=NSOkOXa-Ar8 \
      --start_time 1:42 \
      --length 10 \
      --output ~/Downloads/ten_second_segment.mp4
    """
    main()