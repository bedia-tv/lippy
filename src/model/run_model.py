'''
This module defines the function to run the model.
The function defined is:
- run_model
'''

from os import remove
from os.path import exists
from toml import loads
from torch import load
from torch.backends import cudnn
from Lipreading_PyTorch.model_tools.trainer import Trainer
from Lipreading_PyTorch.model_tools.validator import Validator
from Lipreading_PyTorch.models.lip_read import LipRead
from src.model.model_tools.predictor import Predictor


def run_model(train, validate, predict, loadpretrainedmodel, epochs):
    '''Function to run the model in order to train, validate or predict a
    set of words.

    Args:
        train `(bool)`: Holds if the model has to train
        validate `(bool)`: Holds if the model has to validate while training
        predict `(bool)`: Holds if the model has to validate the sentence in
        the validation dataset
        loadpretrainedmodel `(bool)`: Holds if the pretrainedmodel will be
        loaded
        epochs `(int)`: Number of epochs to train or validate the model

    Returns:
        The predicted `string` if `predict` is `true`, `None` otherwise.
    '''
    with open('options.toml', 'r') as options_file:
        options = loads(options_file.read())

    if (options['general']['usecudnnbenchmark'] and
            options['general']['usecudnn']):
        cudnn.benchmark = True

    model = LipRead(options)
    pretrainedmododel_path = options['general']['pretrainedmodelpath']

    if loadpretrainedmodel:
        model.load_state_dict(load(pretrainedmododel_path))
    elif train and exists(pretrainedmododel_path):
        remove(pretrainedmododel_path)

    if options['general']['usecudnn']:
        model = model.cuda(options['general']['gpuid'])

    if predict:
        return Predictor(options).predict(model)
    else:
        print('Starting training...\n')
        if train:
            trainer = Trainer(options)

        if validate:
            validator = Validator(options)

        for epoch in range(epochs):
            if train:
                trainer.epoch(model, epoch)

            if validate:
                validator.epoch(model)
        return None
