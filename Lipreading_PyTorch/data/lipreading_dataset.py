from os import listdir
from torch import LongTensor
from torch.utils.data import Dataset
from Lipreading_PyTorch.data.preprocess import bbc, load_video


def build_file_list(directory, type_set):
    labels = listdir(directory)
    complete_list = []
    predict = type_set is None

    if predict:
        dirpath = f'{directory}/'
        files = listdir(dirpath)

        for file in files:
            if file.endswith('mp4'):
                filepath = f'{dirpath}/{file}'
                entry = (0, filepath)
                complete_list.append(entry)
    else:
        for index, label in enumerate(labels):
            dirpath = f'{directory}/{label}/{type_set}'
            files = listdir(dirpath)

            for file in files:
                if file.endswith('mp4'):
                    filepath = f'{dirpath}/{file}'
                    entry = (index, filepath)
                    complete_list.append(entry)

    return labels, complete_list


class LipreadingDataset(Dataset):
    '''BBC Lip Reading dataset.'''

    def __init__(self, directory, type_set, augment, padding):
        self.label_list, self.file_list = build_file_list(
            directory, type_set)
        self.augment = augment
        self.padding = padding

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        # Load video into a tensor
        label, filename = self.file_list[idx]
        vidframes = load_video(filename)
        temporalvolume = bbc(vidframes, self.augment,
                             self.padding, filename)

        sample = {'temporalvolume': temporalvolume,
                  'label': LongTensor([label])}

        return sample
