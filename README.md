# YouTube Segment Downloader

A Python utility to download and extract specific segments from YouTube videos. This tool allows you to specify a start time and duration to download just the portion of the video you need.

## Features

- Download specific segments of YouTube videos
- Simple command-line interface
- Support for timestamp format (MM:SS)
- Automatic cleanup of temporary files
- High-quality video download

## Requirements

- Python 3.6 or higher
- FFmpeg (required for video processing)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository or download the source code

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg:
   - **MacOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

Run the script using the following command format:

```bash
python download_youtube_segment.py \
  --url <youtube_url> \
  --start_time MM:SS \
  --length <seconds> \
  --output <output_path>
```

### Arguments

- `--url`: YouTube video URL (required)
- `--start_time`: Start time in MM:SS format (required)
- `--length`: Duration of the segment in seconds (required)
- `--output`: Output path for the MP4 file (required)

### Example

```bash
python download_youtube_segment.py \
  --url https://www.youtube.com/watch?v=NSOkOXa-Ar8 \
  --start_time 1:42 \
  --length 10 \
  --output ~/Downloads/ten_second_segment.mp4
```

This will download a 10-second segment starting at 1 minute and 42 seconds from the specified YouTube video.

## Error Handling

The script includes error handling for common issues:
- FFmpeg not installed
- Invalid YouTube URLs
- Invalid timestamp format
- Network connectivity issues
- File system permissions

## How It Works

1. The script first verifies that FFmpeg is installed on your system
2. It downloads the complete video in the best available quality using yt-dlp
3. FFmpeg is then used to extract the specified segment from the downloaded video
4. The original full video is automatically deleted after extraction
5. The final segment is saved to your specified output location

## Troubleshooting

### Common Issues

1. **FFmpeg Not Found**
   - Make sure FFmpeg is installed and accessible from your command line
   - Try running `ffmpeg -version` to verify the installation

2. **Permission Errors**
   - Ensure you have write permissions in the output directory
   - Try running with sudo/administrator privileges if needed

3. **Download Fails**
   - Check your internet connection
   - Verify the YouTube URL is valid and the video is available
   - Some videos may be region-restricted or private

### Debug Mode

If you encounter issues, you can modify the script to enable debug output:
- Set `'quiet': False` in the yt-dlp options
- The script will then show detailed download progress and error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is intended for personal use only. Please respect YouTube's terms of service and copyright laws when downloading content. The developers are not responsible for any misuse of this tool.

## Acknowledgments

This project uses the following open-source libraries:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) for video processing
