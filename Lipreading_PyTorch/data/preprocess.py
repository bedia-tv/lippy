from sys import exit as sys_exit
from imageio import get_reader
from torch import FloatTensor
from torchvision.transforms import (CenterCrop, Compose, Grayscale, Normalize,
                                    ToPILImage, ToTensor)
from torchvision.transforms.functional import to_tensor
from Lipreading_PyTorch.data.statefultransforms import (StatefulRandomCrop,
                                                        StatefulRandomHorizontalFlip)


def load_video(filename):
    '''
    Loads the specified video using ffmpeg.

    Args:
        filename (str): The path to the file to load.
            Should be a format that ffmpeg can handle.

    Returns:
        List[FloatTensor]: the frames of the video as a list of 3D tensors
            (channels, width, height)
    '''
    vid = get_reader(filename, 'ffmpeg')

    return [to_tensor(image) for image in vid]


def bbc(vidframes, augmentation, padding, filename):
    '''
    Preprocesses the specified list of frames by center cropping.
    This will only work correctly on videos that are already centered on the
    mouth region, such as LRITW.

    Args:
        vidframes (List[FloatTensor]):  The frames of the video as a list of
            3D tensors (channels, width, height)

    Returns:
        FloatTensor: The video as a temporal volume, represented as a 5D tensor
            (batch, channel, time, width, height)
    '''
    temporal_volume = FloatTensor(1, padding, 112, 112)
    croptransform = CenterCrop((112, 112))

    if augmentation:
        crop = StatefulRandomCrop((122, 122), (112, 112))
        flip = StatefulRandomHorizontalFlip(0.5)

        crop_transform = Compose([
            crop,
            flip
        ])

    for i in range(padding):
        result = Compose([
            ToPILImage(),
            CenterCrop((122, 122)),
            croptransform,
            Grayscale(num_output_channels=1),
            ToTensor(),
            Normalize([0.4161, ], [0.1688, ]),
        ])(vidframes[i])

        temporal_volume[0][i] = result

    return temporal_volume
