from unittest import TestCase, mock
from os import makedirs
from io import StringIO
from imageio import get_reader
from torchvision.transforms.functional import to_tensor
from src.model.model_tools.checker import check_video, check_vidframes
from shutil import rmtree


class TestChecker(TestCase):
    @classmethod
    def setUpClass(cls):
        makedirs('./dataset_test/')
        cls.DIR = './dataset_test/'
        cls.EMPTY_FILE = cls.DIR+'empty.mp4'
        cls.PADDING = 11

    VALUE = [1]*11

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.DIR)

    @mock.patch('src.model.model_tools.checker.to_tensor', return_value=VALUE[1])
    @mock.patch('src.model.model_tools.checker.get_reader', return_value=VALUE)
    def test_check(self, mock_get_reader, mock_to_tensor):
        self.assertTrue(check_video(self.EMPTY_FILE, 11))
        self.assertFalse(check_video(self.EMPTY_FILE, 12))

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('src.model.model_tools.checker.to_tensor', return_value=VALUE[1])
    @mock.patch('src.model.model_tools.checker.get_reader', return_value=VALUE)
    def test_output_false(self, mock_get_reader, mock_to_tensor, mock_stdout):
        check_video(self.EMPTY_FILE, 12)
        expected_output_false = f'{self.EMPTY_FILE} is too short to be processed\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output_false)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('src.model.model_tools.checker.to_tensor', return_value=VALUE[1])
    @mock.patch('src.model.model_tools.checker.get_reader', return_value=VALUE)
    def test_output_true(self, mock_get_reader, mock_to_tensor, mock_stdout):
        check_vidframes(self.DIR, self.DIR, self.PADDING)
        expected_output_true = f'All videos can be processed\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output_true)
