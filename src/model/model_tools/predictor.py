'''
This module defines the Predictor class used to predict sentences given
a set of videos.
'''

from os import walk
from torch import max as t_max
from torch import sum as t_sum
from torch.autograd import Variable
from torch.utils.data import DataLoader
from Lipreading_PyTorch.data.lipreading_dataset import LipreadingDataset


class Predictor():
    '''Class to predict the words being said in the given folder.'''

    def __init__(self, options):
        self.dataset_folder = options['training']['dataset']
        self.prediction_dataset_folder = options['prediction']['dataset']
        self.prediction_dataset = LipreadingDataset(
            self.prediction_dataset_folder, None, True,
            options['general']['padding'])
        self.prediction_data_loader = DataLoader(
            self.prediction_dataset,
            batch_size=options['input']['batchsize'],
            shuffle=options['input']['shuffle'],
            num_workers=options['input']['numworkers'],
            drop_last=True
        )
        self.usecudnn = options['general']['usecudnn']
        self.batchsize = options['input']['batchsize']
        self.gpuid = options['general']['gpuid']

    @staticmethod
    def _get_files_from_folder(folder, file_type):
        type_to_index = {
            'folders': 1,
            'files': 2
        }

        return list(walk(folder))[0][type_to_index[file_type]]

    def _get_max_indices(self, model):
        sample_batched = list(self.prediction_data_loader)[0]
        input_var = Variable(sample_batched['temporalvolume'])
        outputs = model(input_var)

        average_energies = t_sum(outputs.data, 1)
        _max_values, max_indices = t_max(average_energies, 1)

        return max_indices

    def predict(self, model):
        ''''This function predicts the words said in the videos
        that are in the prediction folder.'''
        print('Predicting...')

        dataset_folders = Predictor._get_files_from_folder(
            self.dataset_folder, 'folders')
        index_to_word = dict(enumerate(dataset_folders))

        prediction_videos_num = len(Predictor._get_files_from_folder(
            self.prediction_dataset_folder, 'files'))
        max_indices = self._get_max_indices(model)
        prediction_list = [index_to_word.get(max_indices[video_index].item(),
                                             '<unk>')
                           for video_index in range(prediction_videos_num)]
        prediction = ' '.join(prediction_list)

        return prediction
