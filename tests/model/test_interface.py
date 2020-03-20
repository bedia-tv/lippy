from unittest import TestCase, mock
from src.interface import _interface,  _run_parser, _model, _dataset


class InterfaceTest(TestCase):
    @mock.patch('sys.stdout')
    def test_train_and_predict_raises_error(self, mock_stdout):
        with self.assertRaises(ValueError):
            args = _run_parser(['model', '--predict', '--train'])
            _interface(args)

    @mock.patch('sys.stdout')
    def test_new_and_not_train_raises_error(self, mock_stdout):
        with self.assertRaises(ValueError):
            args = _run_parser(['model', '--new'])
            _interface(args)

    @mock.patch('sys.stdout')
    def test_wrong_function_name_raises_error(self, mock_stdout):
        with self.assertRaises(SystemExit):
            args = _run_parser(['mdl', 'predict'])
            _interface(args)

    @mock.patch('sys.stdout')
    def test_int_as_function_raises_error(self, mock_stdout):
        with self.assertRaises(TypeError):
            args = _run_parser([2, 'predict'])
            _interface(args)

    @mock.patch('sys.stdout')
    def test_str_argument_for_epochs_raises_error(self, mock_stdout):
        with self.assertRaises(SystemExit):
            args = ['model', '--predict', 'epochs=test']
            _run_parser(args)

    @mock.patch('sys.stdout')
    def test_argument_for_different_subparser_raises_error(self, mock_stdout):
        with self.assertRaises(SystemExit):
            args = ['dataset', '--predict', 'test']
            _run_parser(args)

    @mock.patch('sys.stdout')
    @mock.patch('src.interface.run_model', return_value='test')
    @mock.patch('src.interface.three_way_diff_JSON')
    def test_predict_calls_three_way_diff(self, mock_predict, mock_three_way_diff, mock_stdout):
        _model(False, False, True, True, False, 1)
        self.assertTrue(mock_three_way_diff.called)

    @mock.patch('src.interface._model')
    def test_model_is_called(self, mock_model):
        args = _run_parser(['model', '--predict'])
        _interface(args)
        self.assertTrue(mock_model.called)

    def test_no_function_name_raises_error_build(self):
        with self.assertRaises(ValueError):
            args = _run_parser(['dataset'])
            _interface(args)

    @mock.patch('src.interface._dataset')
    def test_datset_is_called_with_function(self, mock_datset):
        args = _run_parser(['dataset', '--function=build'])
        _interface(args)
        self.assertTrue(mock_datset.called)


class DatasetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.FUNCTION = 'mock_function'
        cls.OUTPUT_TYPE = 'mock_output'
        cls.PLAYLIST_FILE = 'mock_playlist'
        cls.URL = 'mock_url'
        cls.AUDIO_FILE = 'mock_audio'
        cls.TRANSCRIPT_FILE = 'mock_transcript'
        cls.VIDEOID = 'mock_videoid'

    @mock.patch('src.interface.run_dataset')
    def test_run_datset_is_called(self, mock_run_dataset):
        _dataset(self.FUNCTION, self.OUTPUT_TYPE, self.PLAYLIST_FILE,
                 self.URL, self.AUDIO_FILE, self.TRANSCRIPT_FILE, self.VIDEOID)
        self.assertTrue(mock_run_dataset.called)
