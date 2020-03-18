"""This module contains the logic for producing alignments,
given audio and a related transcript file."""

from argparse import ArgumentParser
from os import path

from requests import post

def set_file_locations(audio_file: str, transcript_file: str) -> dict:
    """Set up the options parameters to pass to the Gentle session."""
    params = (("async", "false"),)

    audio_contents = open(audio_file, 'rb')
    transcript_contents = open(transcript_file, 'rb')
    files = {
        "audio": (audio_file, audio_contents),
        "transcript": (transcript_file, transcript_contents),
    }

    base = path.basename(audio_file)

    align_name = f"jsons/{path.splitext(base)[0]}.json"

    return {"params": params, "files": files, "align_name": align_name}


def gentle_align_get(params, files):
    """Make a POST request to the Gentle session."""
    try:
        return post(
            "http://localhost:8765/transcriptions", params=params, files=files
        )
    except ConnectionError:
        return None

def get_align(audio_file: str, transcript_file: str):
    """Given an audio file, a transcript, and assuming
    a running Gentle session, gets the JSON alignment
    and adds it to the aligns folder."""

    options = set_file_locations(audio_file, transcript_file)

    response = gentle_align_get(options["params"], options["files"])
    if response is None:
        print(
            """A connection to the Gentle session could not be established.
            This is probably due to Gentle not running on your machine."""
        )
        return None

    with open(options["align_name"], "w+") as align:
        align.write(response.text)

    return options["align_name"]
