'''
Functions below ensure that all videos in training and prediction
datasets can be successfully processed.
'''
from os import walk, listdir, path
from imageio import get_reader
from torchvision.transforms.functional import to_tensor


def check_video(filename, padding):
    '''
    The function compares the number of videoframes
    to padding in order to decide if the video
    can be processed.
    '''
    vid = get_reader(filename, 'ffmpeg')
    vidframes = [to_tensor(image) for image in vid]

    if len(vidframes) < padding:
        print(f'{filename} is too short to be processed')
        return False

    return True


def check_vidframes(trainingdataset, predictiondataset, padding):
    '''
    The function iterates through all videos
    in training and prediction datasets.
    '''
    allowed = True

    for maindir, subdirs, files in walk(trainingdataset, topdown=False):
        if not subdirs:
            for file in files:
                filepath = path.join(maindir, file)
                check = check_video(filepath, padding)
                if not check:
                    allowed = False

    for file in listdir(predictiondataset):
        filepath = path.join(predictiondataset, file)
        check = check_video(filepath, padding)
        if not check:
            allowed = False

    if allowed:
        print('All videos can be processed')

    return allowed
