'''This module handles the logic regarding taking a video, and cropping it into
smaller videos of individual words.'''

from enum import Enum
from json import load
from pathlib import Path
from typing import Tuple
from cv2 import COLOR_BGR2GRAY, cvtColor
from moviepy.video.fx.all import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from dlib import get_frontal_face_detector


class OutputType(Enum):
    '''An enum describing the three ways to structure our dataset.'''
    TRAIN = 'train'
    VAL = 'val'
    PREDICT = 'predict'


def load_align(videoid: str) -> dict:
    '''Read in an alignment .json file.'''
    return load(open(f'jsons/{videoid}.json'))


def apply_padding(start, end, pad, duration):
    '''Applies padding to start and end, but only if
    full padding can be applied on both sides.'''
    if start > end:
        start, end = end, start
    if start > pad:
        start = start - pad
    if end < duration - pad:
        end = end + pad
    return start, end


def crop_word(found_word: str, start: float, end: float,
              videoid: str, save_loc: Tuple[str]):
    # pylint: disable=too-many-arguments, too-many-locals
    '''crops a video into a small segment, including padding, face detection
    and face bounding.'''
    # get full video
    full_video = VideoFileClip(f'videos/{videoid}.mp4')

    # pad video
    pad = 0.25
    start, end = apply_padding(start, end, pad, full_video.duration)

    # get subclip
    word_subclip = full_video.subclip(start, end)

    # get frame
    start_frame = word_subclip.get_frame(t=0)
    end_frame = word_subclip.get_frame(t=end - start)

    # detect faces
    start_faces = get_faces(start_frame)
    end_faces = get_faces(end_frame)

    if len(start_faces) == 1 and len(end_faces) == 1:
        bound_face = get_face_bounds(start_faces[0], end_faces[0])

        final_word = crop(
            word_subclip,
            x1=bound_face['left'],
            x2=bound_face['right'],
            y1=bound_face['top'],
            y2=bound_face['bottom'],
        )

        filename = f'{videoid}_{start:.2f}'
        save_to_file(final_word, found_word, filename,
                     save_loc)

    elif len(start_faces) == 0 or len(end_faces) == 0:
        print('No faces found in either the start or end frame.')
    else:
        print('Multiple faces found')


def get_face_bounds(start_face, end_face):
    '''Creates a bounding box around the face in the start and end frame
    to save space. This assumes that the face moves linearly
    within the span of a single word.'''
    bound_face = {}
    bound_face['left'] = min(start_face.left(), end_face.left())
    bound_face['right'] = max(start_face.right(), end_face.right())
    bound_face['top'] = min(start_face.top(), end_face.top())
    bound_face['bottom'] = max(start_face.bottom(), end_face.bottom())

    return bound_face


def save_to_file(final_word, found_word: str,
                 filename: str,
                 save_loc: Tuple[str]) -> None:
    '''Saves the final cropped word to the correct location based on
    the desired output type (train/val/predict)'''

    folder_output_path = Path(save_loc[0])
    folder_output_path.mkdir(exist_ok=True)

    if save_loc[1] is not None:
        word_path = Path(f'{save_loc[0]}/{found_word}')
        word_path.mkdir(exist_ok=True)

        folder_output_path = Path(f'{save_loc[0]}/{found_word}/{save_loc[1]}')
        folder_output_path.mkdir(exist_ok=True)

    final_word.write_videofile(
        filename=f'{str(folder_output_path)}/{filename}.mp4', audio_codec='aac'
    )


def get_faces(frame):
    '''Detect faces in a given frame of a video.'''
    detector = get_frontal_face_detector()
    gray = cvtColor(frame, COLOR_BGR2GRAY)
    # convert faces to grayscale to speed up face detection
    return detector(gray, 1)


def crop_video(videoid: str, output_type: OutputType,
               save_loc: Tuple[str]) -> None:
    '''Load an alignment and crop a video using that alignment.'''
    align = load_align(videoid)
    crop_words(align, videoid, save_loc)


def crop_words(align: dict, videoid: str,
               save_loc: Tuple[str]) -> None:
    '''Crop an entire video, filtering out failed alignments and OOV terms.'''
    for word in align['words']:
        if word['case'] == 'success':
            found_word = word['alignedWord']
            # <unk> represents a word not in the phonetic dictionary
            if found_word != '<unk>':
                crop_word(
                    found_word, word['start'], word['end'],
                    videoid, save_loc
                )
