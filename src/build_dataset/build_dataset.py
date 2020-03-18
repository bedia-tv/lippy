"""A driver program that combines each step
in the dataset building pipeline."""

from argparse import ArgumentParser
from os import path, remove, mkdir
from build_dataset.download import download
from build_dataset.get_align import get_align
from build_dataset.video_crop import crop_video, OutputType


def get_playlist_videos(playlist_path: str) -> list:
    """Opens the playlist file, and returns a list of each video in the file.
    if the playlist file doesn't exist, create it and return a blank list."""

    videos = []

    try:
        with open(playlist_path, "r") as playlist_file:
            for video in playlist_file:
                videos.append(video)

    except FileNotFoundError:
        open(playlist_path, "w+").close()
        print(f"created {playlist_path}")

    return videos


def get_processed_videos(processed_path: str) -> set:
    """Opens the file of processed videos, and returns a dictionary
    of each video in the file. if the file doesn't exist, create it
    and return a blank dictionary."""
    try:
        with open(processed_path, "r") as processed_file:
            videos = list(processed_file)
            downloaded_videos = {video.rstrip("\n") for video in videos}
            return downloaded_videos
    except FileNotFoundError:
        open(processed_path, "w+").close()  # create downloaded.txt
        return set()

def clear_dirs(video_id: str):
    """Remove the auxiliary folders, including their contents, to
    avoid storing many unneeded files."""

    aux_files = [f'audio/{video_id}.mp3', f'jsons/{video_id}.json', f'transcripts/{video_id}.txt',
                 f'videos/{video_id}.mp4']
    
    for file in aux_files:
        if path.exists(file):
            remove(file)

def add_to_dataset(video: str, output_type: OutputType):
    """Given a Youtube video URL, adds it to the dataset."""
    videoid = '<DEFAULT>' # make sure this variable exist even if the video isn't downloaded
    try:
        # STEP 1: YouTube-DL
        print(f"Downloading {video}...")
        _v_loc, a_loc, t_loc, videoid = download(video)

        # STEP 2: Gentle
        print("Getting alignment file...")
        _align_loc = get_align(a_loc, t_loc)
        print(f"Gentle alignment for {video} added")

        # STEP 3: Cropper
        print("Cropping video...")
        crop_video(videoid, output_type)
    except Exception as _excepted: # pylint: disable=broad-except
        print("Unable to crop video")
    finally:
        with open("src/downloaded.txt", "a+") as downloaded:
            downloaded.writelines(video + "\n")

        print("Removing files...")
        clear_dirs(videoid)

def setup_dirs():
    """Create the various directories we'll need."""
    directories = ["dataset", "audio", "videos", "transcripts", "jsons", "predict" ]
    for dir in directories:
        if not path.exists(dir):
            mkdir(dir)

def build(playlist: str, output_type: OutputType = OutputType.TRAIN) -> None:
    """Take in a playlist and a list of already downloaded videos, and
    add each video to the dataset that hasn't been added already."""

    setup_dirs()

    download_file = "src/downloaded.txt"
    downloaded_videos = get_processed_videos(download_file)
    playlist_videos = get_playlist_videos(playlist)

    for video in playlist_videos:
        if video.rstrip("\n") not in downloaded_videos:
            print(video)
            add_to_dataset(video, output_type)
            downloaded_videos.add(video.rstrip("\n"))
        else:
            print(video.rstrip("\n") + " has already been downloaded")
