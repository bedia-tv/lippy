'''
This module defines functions to handle arguments from the
command line and use them as parameters for the corresponding
function.
The functions defined are:
 - dataset
 - model
 - interface
 -_run_parser
'''
from argparse import ArgumentParser
from sys import argv
from src.model.run_model import run_model
from src.three_way_diff.three_way_diff import three_way_diff_JSON
from src.dataset_tools.run_dataset import run_dataset
from src.dataset_tools.video_crop import OutputType


def _dataset(function, output_type, playlist_file,
             url, audio_file, transcript_file, videoid):
    '''
    This function is called when the parameter `dataset` is used
    to call the interface. It runs the dataset builder for the
    given function and prints the output.
    '''
    result = run_dataset(function, output_type,
                         playlist_file, url, audio_file,
                         transcript_file, videoid)

    if result is not None:
        print(result)


def _model(train, validate, predict, loadpretrainedmodel,
           check, epochs):
    '''
    This function is called when the parameter `model` is used
    to call the interface. It runs the model and prints a prediction
    to the command line if it is called with 'predict=True'
    '''
    prediction_string = run_model(train, validate, predict,
                                  loadpretrainedmodel, check,
                                  epochs)
    if predict:
        if prediction_string == '':
            print('The prediction folder is empty!')
        else:
            base_string = 'all hope friends to change'
            speech_to_text_string = 'all change hope to friends'
            # Creation of the JSON file results.json comparing
            # the changes between the strings
            three_way_diff_JSON(prediction_string, base_string,
                                speech_to_text_string)
            print(prediction_string)


def _interface(args):
    '''
    Handles the arguments given in the command line
    to call the appropiate function. Also checks for
    incompatible arguments.
    '''

    if args.command == 'model':
        if args.train and args.predict:
            raise ValueError('Training and predicting at the same time.')
        if args.new and not args.train:
            raise ValueError('''The new model is not being trained,
                             use: --train''')

        _model(args.train, args.validate, args.predict,
               not args.new, args.check, args.epochs)
    elif args.command == 'dataset':
        if args.function is None:
            raise ValueError('A function must be specified.')
        _dataset(args.function, args.output, args.playlist, args.url,
                 args.audio_file, args.transcript_file, args.videoid)


def _run_parser(args):
    '''
    Parses the command line arguments and returns them.
    '''
    parser = ArgumentParser(description='''Run the interface
                            to use the model or build a dataset.''')
    subparsers = parser.add_subparsers(help='help for subcommand',
                                       dest='command')
    model_parser = subparsers.add_parser('model')
    model_parser.add_argument('--validate', action='store_true', default=False,
                              help='''Use this to get the
                              accuracy of the model.''')
    model_parser.add_argument('--train', action='store_true', default=False,
                              help='Use to train the model on the dataset.')
    model_parser.add_argument('--predict', action='store_true', default=False,
                              help='''Use to predict the words
                              said in the videos under the prediction
                              folder specified in `options.toml`.''')
    model_parser.add_argument('--new', action='store_true', default=False,
                              help='Use to create new model.')
    model_parser.add_argument('--check', action='store_true',
                              help='''Use to check if any videos
                              in the have a number of frames smaller
                              than the padding.''')
    model_parser.add_argument('--epochs', type=int, default=1,
                              help='Set number of epochs.')

    dataset_parser = subparsers.add_parser('dataset')
    dataset_parser.add_argument('--function', type=str,
                                help='''Which function should
                                be executed, choose from `build`,
                                `download`, `align`, `crop`.''',
                                choices=['build', 'download', 'align', 'crop'])
    dataset_parser.add_argument('--output', type=OutputType,
                                help='''Choose a dataset structure to
                                place cropped videos into. Choose from
                                `train`, `val`, `predict`.''',
                                choices=list(OutputType))
    dataset_parser.add_argument('--playlist', type=str,
                                help='location of playlist file.')
    dataset_parser.add_argument('--url', type=str,
                                help='YouTube video URL to download.')
    dataset_parser.add_argument('--audio_file', type=str,
                                help='file location of audio .mp3 file.')
    dataset_parser.add_argument('--transcript_file', type=str,
                                help='file location of transcript .txt file.')
    dataset_parser.add_argument('--videoid', type=str,
                                help='YouTube videoid.')

    return parser.parse_args(args)


if __name__ == '__main__':
    ARGS = _run_parser(argv[1:])
    _interface(ARGS)
