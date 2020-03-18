## Usage
 - Install [Python 3].
 - Clone the repository.
 - Install Docker on your device.
 - In a separate terminal, run `docker --network host -P lowerquality/gentle`
 - To use, run `python src/get_align.py <audio file> <transcript file>`.

## Dataset structure
 - The program assumes that a Gentle session is currently running, and makes no attempt to create one on its own (this is so, when building a dataset, we can use the same Gentle session for every video).
 - The transcript the program creates is placed into the `jsons` folder, into a file with the same name as the audio file (which, if created using `download.py`, should be named after the YouTube video ID)

## Dependencies
 - [Python 3]
 - [Gentle] for generating JSON alignments

[Python 3]: <https://www.python.org/downloads/>
[Gentle]: <http://lowerquality.com/gentle/>