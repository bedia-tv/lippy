from unittest import TestCase, mock
from src.model.run_model import run_model, load_options
from src.model.model_tools.predictor import Predictor
from toml import loads
from torch import FloatTensor


class PredictorTest(TestCase):
    with open('options.toml', 'r') as options_file:
        OPTIONS = loads(options_file.read())

    TRAIN_FOLDERS = [('./dataset', ['all', 'friends'], []),
                     ('./dataset/all', ['train'], []
                      ), ('./dataset/all/train', [], ['all.mp4']),
                     ('./dataset/friends', ['train'], []),
                     ('./dataset/friends/train', [], ['friends.mp4'])]
    PREDICT_FILES = [('./dataset-val', [], ['all.mp4', 'friends.mp4'])]
    DATASET_FOLDERS = ['all', 'change', 'friends', 'hope', 'to']
    MAX_INDICES_LIST = [0, 2, 3, 4, 1]
    MAX_INDICES = FloatTensor(MAX_INDICES_LIST)

    @mock.patch('src.model.model_tools.predictor.DataLoader', return_value="")
    @mock.patch('src.model.model_tools.predictor.LipreadingDataset', return_value="")
    @mock.patch('src.model.model_tools.predictor.Predictor._get_files_from_folder', return_value=DATASET_FOLDERS)
    @mock.patch('src.model.model_tools.predictor.Predictor._get_max_indices', return_value=MAX_INDICES)
    def test_returns_correct_prediction(self, mock_max_indices, mock_dataset_folders, mock_dataset, mock_data_loader):
        predictor = Predictor(self.OPTIONS)
        predictor_output = predictor.predict('model')
        self.assertEqual(predictor_output, 'all friends hope to change')

    @mock.patch('src.model.model_tools.predictor.walk', return_value=TRAIN_FOLDERS)
    def test_get_files_from_folder_correct_output_with_parameter_folders(self, mock_walk):
        self.assertEqual(Predictor._get_files_from_folder(
            '', 'folders'), ['all', 'friends'])

    @mock.patch('src.model.model_tools.predictor.walk', return_value=PREDICT_FILES)
    def test_get_files_from_folder_correct_output_with_parameter_files(self, mock_walk):
        self.assertEqual(Predictor._get_files_from_folder(
            './dataset-val', 'files'), ['all.mp4', 'friends.mp4'])

    @mock.patch('src.model.model_tools.predictor.Predictor._get_files_from_folder', return_value=[])
    def test_empty_prediction_folder_returns_empty_string(self, mock_get_files):
        self.assertEqual(Predictor(self.OPTIONS).predict('model'), "")
