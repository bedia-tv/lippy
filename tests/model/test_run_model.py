from unittest import TestCase, mock
from src.model.run_model import run_model, load_options


class RunModelTest(TestCase):
    OPTIONS = {
        'general': {
            'usecudnnbenchmark': False,
            'usecudnn': False,
            'pretrainedmodelpath': 'trainedmodel.pt',
            'gpuid': 0,
            'padding': 11

        },
        'model': {
            'type': 'LSTM',
            'inputdim': 256,
            'hiddendim': 256,
            'numclasses': 500,
            'numlstms': 2
        },
        'input': {
            'numworkers': 18,
            'batchsize': 5,
            'shuffle': True
        },
        'training': {
            'dataset': './datset'
        },
        'validation': {
            'folder': 'train'
        },
        'prediction': {
            'dataset': './predict'
        }
    }
    OPTIONS_CUDA = {**OPTIONS, 'general': {**OPTIONS['general'],
                                           'usecudnnbenchmark': True,
                                           'usecudnn': True
                                           }
                    }

    @mock.patch('src.model.run_model.isfile', return_value=True)
    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.loads', return_value=OPTIONS_CUDA)
    @mock.patch('src.model.run_model.LipRead.cuda', return_value='Cuda model')
    def test_usecudnn_calls_cuda(self, mock_options, mock_cuda, mock_load_model,
                                 mock_load, mock_is_file, mock_exists):
        self.assertEqual(load_options(True, False, False, True, False),
                         (self.OPTIONS_CUDA, 'Cuda model'))

    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('src.model.run_model.loads', return_value=OPTIONS)
    @mock.patch('src.model.model_tools.predictor.DataLoader', return_value="")
    @mock.patch('src.model.model_tools.predictor.LipreadingDataset', return_value="")
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.Predictor.predict',
                return_value='Predictor output')
    def test_returns_predictor_output(self, mock_predict, mock_load_model, mock_load, mock_dataset,
                                      moc_data_loader, mock_options, mock_exists):
        predictor_output = run_model(False, False, True, True, False, 1)
        self.assertEqual(predictor_output, 'Predictor output')

    @mock.patch('Lipreading_PyTorch.model_tools.trainer.Trainer.__init__', return_value=None)
    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('sys.stdout')
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.Trainer.epoch')
    def test_train_runs_for_every_epoch(self, mock_train, mock_load_model,
                                        mock_load, mock_stdout, mock_exists,
                                        mock_init):
        run_model(True, False, False, True, False, 5)
        self.assertEqual(mock_train.call_count, 5)

    @mock.patch('Lipreading_PyTorch.model_tools.validator.Validator.__init__', return_value=None)
    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.Validator.epoch')
    def test_validate_runs_for_every_epoch(self, mock_validate, mock_load_model,
                                           mock_load, mock_exists, mock_init):
        run_model(False, True, False, True, False, 6)
        self.assertEqual(mock_validate.call_count, 6)

    @mock.patch('src.model.run_model.remove')
    @mock.patch('src.model.run_model.exists', return_value=True)
    def test_using_new_replaces_model(self, mock_remove, mock_exists):
        load_options(True, False, False, False, False)
        self.assertTrue(mock_remove.called)

    @mock.patch('Lipreading_PyTorch.model_tools.trainer.Trainer.__init__', return_value=None)
    @mock.patch('Lipreading_PyTorch.model_tools.validator.Validator.__init__', return_value=None)
    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('sys.stdout')
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.Trainer.epoch')
    @mock.patch('src.model.run_model.Validator.epoch')
    def test_validate_run_whith_train_and_validate(self, mock_validate, mock_train,
                                                   mock_load_model, mock_load,
                                                   mock_stdout, mock_exists,
                                                   mock_init_v, mock_init_t):
        run_model(True, True, False, True, False, 6)
        self.assertEqual(mock_validate.call_count, 6)

    @mock.patch('Lipreading_PyTorch.model_tools.trainer.Trainer.__init__', return_value=None)
    @mock.patch('Lipreading_PyTorch.model_tools.validator.Validator.__init__', return_value=None)
    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('sys.stdout')
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.Validator.epoch')
    @mock.patch('src.model.run_model.Trainer.epoch')
    def test_train_run_whith_train_and_validate(self, mock_train, mock_validate,
                                                mock_load_model, mock_load,
                                                mock_stdout, mock_exists,
                                                mock_init, mock_init_t):
        run_model(True, True, False, True, False, 6)
        self.assertEqual(mock_train.call_count, 6)

    @mock.patch('Lipreading_PyTorch.model_tools.trainer.Trainer.__init__', return_value=None)
    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('sys.stdout')
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.Trainer.epoch')
    @mock.patch('src.model.run_model.Validator.epoch')
    def test_validate_not_run_whith_train(self, mock_validate, mock_train,
                                          mock_load_model, mock_load,
                                          mock_stdout, mock_exists,
                                          mock_init):
        run_model(True, False, False, True, False, 1)
        self.assertEqual(mock_validate.call_count, 0)

    @mock.patch('Lipreading_PyTorch.model_tools.validator.Validator.__init__', return_value=None)
    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('sys.stdout')
    @mock.patch('src.model.run_model.load')
    @mock.patch('src.model.run_model.LipRead.load_state_dict')
    @mock.patch('src.model.run_model.Validator.epoch')
    @mock.patch('src.model.run_model.Trainer.epoch')
    def test_train_not_run_whith_validate(self, mock_train, mock_validate,
                                          mock_load_model, mock_load,
                                          mock_stdout, mock_exists,
                                          mock_init):
        run_model(False, True, False, True, False, 1)
        self.assertEqual(mock_train.call_count, 0)

    @mock.patch('src.model.run_model.loads', return_value=OPTIONS)
    @mock.patch('src.model.run_model.exists', return_value=False)
    def test_missing_train_dataset_raises_error(self, mock_exists, mock_loadss):
        with self.assertRaises(FileNotFoundError):
            load_options(True, False, False, True, False)

    @mock.patch('src.model.run_model.loads', return_value=OPTIONS)
    @mock.patch('src.model.run_model.exists', return_value=False)
    def test_missing_prediction_folder_raises_error(self, mock_exists, mock_loads):
        with self.assertRaises(FileNotFoundError):
            load_options(False, False, True, True, False)

    @mock.patch('src.model.run_model.loads', return_value=OPTIONS)
    @mock.patch('src.model.run_model.exists', return_value=False)
    def test_missing_pretrained_model_raises_error(self, mock_exists, mock_loads):
        with self.assertRaises(FileNotFoundError):
            load_options(False, False, False, True, False)

    @mock.patch('src.model.run_model.loads', return_value=OPTIONS)
    @mock.patch('src.model.run_model.isfile', return_value=False)
    def test_missing_options_file_raises_error(self, mock_exists, mock_loads):
        with self.assertRaises(FileNotFoundError):
            load_options(False, False, False, True, False)

    @mock.patch('src.model.run_model.exists', return_value=True)
    @mock.patch('src.model.run_model.check_vidframes', return_value=False)
    def test_raises_error_if_check_fails(self, mock_check_vidframes,
                                         mock_exists):
        with self.assertRaises(ValueError):
            run_model(False, False, True, True, True, 1)
