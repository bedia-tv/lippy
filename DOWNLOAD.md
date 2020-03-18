## Usage
 - Install [Python 3].
 - Clone the repository.
 - Run `pip install youtube_dl`.
 - To use, run `python src/download.py <youtube url>`.

## Dataset structure
 - The video should be in a directory named `videos` with the filename `<video ID>.mp4`
 - The audio should be in a directory named `audio` with the filename `<video ID>.mp3`
 - The auto generated transcript should be in a directory named `transcript` with the filename `<video ID>.txt`

## Dependencies
 - [Python 3]
 - [YoutubeDL] for video processing

[Python 3]: <https://www.python.org/downloads/>
[YoutubeDL]: <https://youtube-dl.org/>