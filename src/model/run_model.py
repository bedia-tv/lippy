'''
This module defines the function to run the model.
The function defined is:
- run_model
'''
from os import remove
from os.path import exists, isfile
from toml import loads
from torch import load
from torch.backends import cudnn
from Lipreading_PyTorch.models.lip_read import LipRead
from Lipreading_PyTorch.model_tools.trainer import Trainer
from Lipreading_PyTorch.model_tools.validator import Validator
from src.model.model_tools.predictor import Predictor
from src.model.model_tools.checker import check_vidframes


def load_options(train, valdiate, predict, load_pretrained_model, check):
    '''
    This function loads the options from options.toml
    into a dictionary, creates a model with those options
    and returns both.
    '''
    if not isfile('options.toml'):
        raise FileNotFoundError('''The `options.toml`file\
                                doesn\'t exist''')
    with open('options.toml', 'r') as options_file:
        options = loads(options_file.read())

    if train and not exists(options['training']['dataset']):
        raise FileNotFoundError('''The training dataset directory specified\
                                in `options.toml` doesn\'t exist''')
    if predict and not exists(options['prediction']['dataset']):
        raise FileNotFoundError('''The predict file specified\
                                in options.toml doesn\'t exist''')
    pretrained_model_path = options['general']['pretrainedmodelpath']
    if load_pretrained_model and not exists(
            pretrained_model_path):
        raise FileNotFoundError('''The pretrained model file specified\
                                in options.toml doesn\'t exist''')
    if check:
        if not check_vidframes(options['training']['dataset'],
                               options['prediction']['dataset'],
                               options['general']['padding']):
            raise ValueError('''The videos mentioned above don\'t have
                            enough frames.''')

    if (options['general']['usecudnnbenchmark'] and
            options['general']['usecudnn']):
        cudnn.benchmark = True

    model = LipRead(options)

    if load_pretrained_model:
        model.load_state_dict(load(pretrained_model_path))
    elif train and exists(pretrained_model_path):
        remove(pretrained_model_path)

    if options['general']['usecudnn']:
        model = model.cuda(options['general']['gpuid'])
    return options, model


def run_model(train, validate, predict, load_pretrained_model, check, epochs):
    '''
    Function to run the model in order to train, validate or predict a
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
    options, model = load_options(
        train, validate, predict, load_pretrained_model, check)

    if predict:
        return Predictor(options).predict(model)

    if train:
        print('Starting training...\n')
        trainer = Trainer(options)

    if validate:
        validator = Validator(options)

    for epoch in range(epochs):
        if train:
            trainer.epoch(model, epoch)

        if validate:
            validator.epoch(model)

    return None
