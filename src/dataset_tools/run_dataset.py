'''
This module handles the arguments from the interface to
call the appropriate functions in producing a dataset.
'''
from os.path import isfile

from src.dataset_tools.build_dataset import build
from src.dataset_tools.download import download
from src.dataset_tools.get_align import get_align
from src.dataset_tools.video_crop import crop_video
from src.dataset_tools.video_crop import OutputType


def run_dataset(function, output_type, playlist_file, url,
                audio_file, transcript_file, videoid):
    '''Handles the arguments given from the interface in order to
    run one of the dataset functions.

    Args:
        function(str): determines which function to run.
        Either 'build', 'download', 'align' or 'crop'.

        output_type(str): determines format to save dataset (build/crop only)
        Possible options: 'train', 'val' or 'predict'.
        playlist_file(str): playlist file location (build/download only)
        url(str): the YouTube video URL (download only)
        audio_file(str): the location of the audio file (align only)
        transcript_file(str): the location of the transcript file (align only)
        videoid(str): The videoid of the video you wish to crop. (crop only)

        Returns:

        If function is 'build', returns None.

        If function is 'download', returns a list of 4 elements,
        giving the location of the video file, audio file,
        transcript file and the videoid respectively.

        If function is 'align', returns a string containing the align location.

        If function is 'crop', returns None.
    '''
    if function == 'build':
        if output_type is None:
            raise ValueError('An output type must be defined.')
        else:
            output = OutputType(output_type)

        if playlist_file is None:
            raise ValueError('A playlist file must be specified.')
        if not isfile(playlist_file):
            raise ValueError(f'{playlist_file} is not a valid playlist file.')

        build(playlist_file, output)

        return None

    elif function == 'download':
        if url is None:
            raise ValueError('A url must be specified.')
        return download(url)

    elif function == 'align':
        if audio_file is None:
            raise ValueError('An audio file must be specified.')
        if not isfile(audio_file):
            raise ValueError(f'{audio_file} is not a valid audio file.')
        if transcript_file is None:
            raise ValueError('A transcript file must be specified.')
        if not isfile(transcript_file):
            raise ValueError(
                f'{transcript_file} is not a valid transcript file.')

        return get_align(audio_file, transcript_file)

    elif function == 'crop':
        if output_type is None:
            raise ValueError('An output type must be defined.')
        else:
            output = OutputType(output_type)

        if videoid is None:
            raise ValueError('A video id must be specified.')
        return crop_video(videoid, output_type)
