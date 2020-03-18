"""This modules handles downloading the audio,
 video and transcripts from a youtube video"""
from os import remove
from os.path import exists
import re
import argparse
import youtube_dl

class MyLogger():
    """Redefine logger for downloading so fewer lines are printed"""
    def debug(self, msg):
        """Don't print any debug issues"""

    def warning(self, msg):
        """Don't print any warning messages"""


def get_options():
    """Return the download options for ydl"""
    ydl_video_opts = {
        "outtmpl": "videos/%(id)s",
        "logger": MyLogger(),
        "postprocessors": [{"key": "FFmpegVideoConvertor",
                            "preferedformat": "mp4"}],
    }

    ydl_audio_opts = {
        "outtmpl": "audio/%(id)s",
        "logger": MyLogger(),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
        ]
    }

    ydl_subs_opts = {
        "outtmpl": "transcripts/%(id)s",
        "logger": MyLogger(),
        "writeautomaticsub": True,
        "skip_download": True,
        "subtitlesformat": "ttml"
    }

    subs = youtube_dl.YoutubeDL(ydl_subs_opts)
    audio = youtube_dl.YoutubeDL(ydl_audio_opts)
    video = youtube_dl.YoutubeDL(ydl_video_opts)

    return [subs, audio, video]


def get_transcript(videoid):
    """Given a video file save return the context of the given ttml file."""
    with open(f"transcripts/{videoid}.en.ttml") as ttml_file:
        cleantext = ttml_file.read()

    return cleantext


def extract_transcript(cleantext):
    """Given a ttml transcript remove tags and return clean text."""
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", cleantext)
    cleantext = re.sub(r"\n\s*\n", "\n", cleantext)

    cleantext = re.sub("&#39;", "'", cleantext)

    return cleantext


def save_transcript(cleantext, videoid):
    """Given a transcript save as text file and remvoe TTML."""
    with open(f"transcripts/{videoid}.txt", "w+") as txt_file:
        txt_file.write(cleantext)

    if exists(f"transcripts/{videoid}.en.ttml"):
        remove(f"transcripts/{videoid}.en.ttml")


def handle_subtitles(url, ydl_subs):
    """Download subtitles for the given youtube url."""
    print("Downloading subtitles...")
    subs_info = ydl_subs.extract_info(url, download=True)
    text = get_transcript(subs_info["id"])
    transcript_info = extract_transcript(text)
    save_transcript(transcript_info, subs_info["id"])

    return subs_info


def file_locations(videoid):
    """Return the location of audio, video and transcript files."""
    video_file = f"videos/{videoid}.mp4"
    audio_file = f"audio/{videoid}.mp3"
    subs_file = f"transcripts/{videoid}.txt"

    return [video_file, audio_file, subs_file, videoid]

def download(url):
    """Given a youtube url download the audio, video and transcript"""
    ydl_subs, ydl_audio, ydl_video = get_options()

    try:
        subs_info = handle_subtitles(url, ydl_subs)

    except Exception as exception:
        print(exception)
        raise Exception("Error downloading subtitles")

    try:
        print("Downloading audio...")
        ydl_audio.download([url])
    except:
        raise Exception("Error downloading audio")

    try:
        print("Downloading video...")
        ydl_video.download([url])
    except:
        raise Exception("Error downloading video\n")

    print(f'Downloaded {subs_info["title"]}\n')

    return file_locations(subs_info["id"])