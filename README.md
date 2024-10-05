This Python script allows you to input Reddit post URLs and generates videos that combine the post's content with text-to-speech audio and subtitles.

## Features

- **Reddit Content Extraction:** Retrieves the title and body text from specified Reddit posts.
- **Text-to-Speech Conversion:** Converts the extracted text into audio using Microsoft's Edge TTS service.
- **Subtitle Generation:** Creates subtitle files corresponding to the audio.
- **Video Rendering:** Merges the audio and subtitles with a base video of your choice using `ffmpeg`.

## Requirements

- **Python Libraries:**
  - `subprocess`
  - `beautifulsoup4`
  - `lxml`
  - `requests`
  - `edge_tts`
  - You can install them using `pip install -r requirements.txt`
- **External Tools:**
  - `ffmpeg` (Ensure it's installed and accessible in your system's PATH.)
- **A base video**
  - you can choose any video you want you don't need to worry about the duration or anything [(example using minecraft parkour )](https://youtu.be/pQWCY6EoyOM?si=DFdgwLZNwcWEG7ur)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/BugAlpha/RedditShortCreator
   cd RedditShortCreator
   python3 main.py
### Example Execution

```bash
Do you want to remove audio and subs after the script ends? (Y/N): Y
How many posts would like to generate?: 3
Please input the 1# link: https://www.reddit.com/r/example1
Please input the 2# link: https://www.reddit.com/r/example2
Please input the 3# link: https://www.reddit.com/r/example3
```

The script will process the Reddit posts, generate the corresponding videos with TTS and subtitles, and save them as `result1.mp4`, `result2.mp4`, and `result3.mp4`.

## Output Files

- **Resulting videos**: `result1.mp4`, `result2.mp4`, ...
- **Generated audio files**: `audio1.mp3`, `audio2.mp3`, ...
- **Subtitles**: `subs1.srt`, `subs2.srt`, ...
 

## Notes

- Make sure to have a valid Reddit post URL, and the post should be accessible (not restricted, private, or deleted).
- FFmpeg must be installed and accessible from your system's PATH.
## Contributing
Contributions are welcome! If you have suggestions for improvements or encounter issues, feel free to open an issue or submit a pull request.
## Acknowledgments
- Thanks to the developers of edge_tts for the text-to-speech functionality.
- Credit to the creators of ffmpeg for the video processing capabilities.

## License
This project is licensed under the GPLv3.0 License. See the [LICENSE](LICENSE) file for details.

