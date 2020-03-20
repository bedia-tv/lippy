from random import randint, random
from torchvision.transforms.functional import crop, hflip


class StatefulRandomCrop():
    def __init__(self, insize, outsize):
        self.size = outsize
        self.crop_params = self.get_params(insize, self.size)

    def __call__(self, img):
        '''
        Args:
            img (PIL Image): Image to be cropped.
        Returns:
            PIL Image: Cropped image.
        '''
        i, j, h, w = self.crop_params

        return crop(img, i, j, h, w)

    def __repr__(self):
        return f'{self.__class__.__name__}(size={self.size})'

    @staticmethod
    def get_params(insize, outsize):
        '''
        Get parameters for ``crop`` for a random crop.
        Args:
            insize (PIL Image): Image to be cropped.
            outsize (tuple): Expected output size of the crop.
        Returns:
            tuple: params (i, j, h, w) to be passed to ``crop``
            for random crop.
        '''
        w, h = insize
        th, tw = outsize

        if w == tw and h == th:
            i = 0
            j = 0

        else:
            i = randint(0, h - th)
            j = randint(0, w - tw)

        return i, j, th, tw


class StatefulRandomHorizontalFlip():
    def __init__(self, p=0.5):
        self.p = p
        self.rand = random()

    def __call__(self, image):
        '''
        Args:
            img (PIL Image): Image to be flipped.
        Returns:
            PIL Image: Randomly flipped image.
        '''
        if self.rand < self.p:
            return hflip(image)
        else:
            return image

    def __repr__(self):
        return f'{self.__class__.__name__}(p={self.p})'
