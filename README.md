
MUST INSTALL:

- Gentle force aligner 
https://github.com/lowerquality/gentle

Gentle must be launched at localhost port 8765 to synchronise files using a curl command.


- jq (read from JSON)
https://shapeshed.com/jq-json/

- ffmpeg (video clearing/extraction)
https://github.com/FFmpeg/FFmpeg



SHOULD INSTALL:

- youtube-dl
https://github.com/ytdl-org



The script’s functionality are as follows; 

__MAIN.sh

- if we’re downloading an online media file or its subtitles, take in URL as first argument 
`__MAIN.sh https://www.youtube.com/watch?v=ye9OeMAc9oE`

- prompts variables to be entered (integer for YES, ENTER for NO - uses ‘if greater than’ logic
- uses extract_text.py to strip the subtitle formatting and leave us with the raw text
- feeds in the Gentle JSON view

We don’t need to download subtitles from Youtube if we have the corresponding Gentle JSON/text already; however, Gentle does need a local media file to sync the transcript with, so it’s good to have the first two prompts handy to download an online file and its subtitles. It also sets up the clipping file nicely.


___clip.sh
- reads in a variety of variables from a Gentle JSON using `JQ` and extracts the corresponding frames from a video file using `ffmpeg`
- the video/JSON names have to be identical, which is why running MAIN and answering ENTER for all the variables is a good idea.

Currently this just does the bare minimum of taking the start/end time of each word and extracting a GIF from the video accordingly; the refinements to be applied to such as a script are listed below, but this will mainly take shape as we draw from more data over time.


TO-DOs:
- refine the GIF extraction
	- take a certain number of frames for each GIF, as specified by existing data libraries
	- recognise if speaker / speaker’s lips aren’t onscreen during the time specified and prevent extraction of these GIFs
	- are GIFs for short words like ‘and’ etc too short to make use of? should they be extracted along with other leading words to better inform the data? how complex might this get?
- create standardised process for organising/accessing the data
	- moving these scripts online to allow for Scriptate to run it with each new completed transcript and increase the size of their dataset.
		- AWS S3 with Lambda functions that are run upon submitting a new transcript/video seems like a natural home; there’s a lot of existing examples about this and a basic visual interface for searching through the files can easily be connected.
	- bare-bones submission form page which takes into account the arguments within the bash script in a checkbock format runs the process after completion of a transcript