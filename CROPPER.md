## Usage
 - Install [Python 3].
 - Clone the repository.
 - Run `pip install moviepy`.
 - To use, run `python src/video_crop.py <YouTube video ID>`.
 - Add `train` to format the dataset for training
 - Add `val` to format the dataset for validation
 - Add `predict` to format the dataset for prediction
 - If you're receiving an `ImportError: DLL load failed` for `_mklinit`, upgrade numpy with `pip install --upgrade numpy`.

## Dataset structure
 - The program assumes that your video and your JSON alignment are both named after your YouTube video ID (e.g for ID `r7x-RGfd0Yk`, the video is called `r7x-RGfd0Yk.mp4` and the
 align is called `r7x-RGfd0Yk.json`).
 - The video should be in a directory named `videos`, and the align should be in a directory named `outputs`.
 - The training words are placed into `dataset/[word]/train/` 
 - The validation words are placed into `dataset/[word]/val/` 
 - The prediction words are placed into `predict/[word]` 
 - Each clip has the filename `<video ID>_<start time>.mp4`.

## Dependencies
 - [Python 3]
 - [MoviePy] for video processing

 [Python 3]: <https://www.python.org/downloads/>
 [MoviePy]: <https://zulko.github.io/moviepy/>