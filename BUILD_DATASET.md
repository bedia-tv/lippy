## Usage
 - Install [Python 3].
 - Clone the repository.
 - Run `pip install moviepy youtube_dl`.
 - Install [Docker] on your device.
 - In a separate terminal, run `docker --name gentle --network host -P lowerquality/gentle`.
 - To use, run `python src/build_dataset.py <playlist file>`
 - Add `train` to format the dataset for training
 - Add `val` to format the dataset for validation
 - Add `predict` to format the dataset for prediction
 - If you're receiving an `ImportError: DLL load failed` for `_mklinit`, upgrade numpy with `pip install --upgrade numpy`.

## Dataset structure
 - The playlist file should be a `.txt` file, with each line containing a URL for one YouTube video.
 - The video will be placed into the `videos` folder
 - The audio from the video is placed into the `audio` folder
 - The transcript from YouTube subtitles is placed into the `transcripts` folder
 - The JSON alignment is placed into the `jsons` folder
 - The training words are placed into `dataset/[word]/train/` 
 - The validation words are placed into `dataset/[word]/val/` 
 - The prediction words are placed into `predict/[word]` 
 - A list of videos in the dataset can be found in `src/downloads.txt`

## Dependencies
 - [Python 3]
 - [Moviepy] for video processing
 - [Gentle] for producing JSON alignments
 - [YoutubeDL] for downloading videos and metadata from YouTube
 - [Docker] for accessing the [Gentle] Docker image

[Python 3]: <https://www.python.org/downloads/>
[MoviePy]: <https://zulko.github.io/moviepy/>
[Gentle]: <http://lowerquality.com/gentle/>
[YoutubeDL]: <https://youtube-dl.org/>
[Docker]: <https://www.docker.com/>
