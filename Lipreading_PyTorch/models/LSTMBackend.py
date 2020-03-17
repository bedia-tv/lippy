from os import walk
from torch import max as t_max, sum as t_sum
from torch.nn import LSTM, Linear, LogSoftmax, Module, NLLLoss

MAXCOUNT = 0


class NLLSequenceLoss(Module):
    '''Custom loss function.
    Returns a loss that is the sum of all losses at each time step.'''

    def __init__(self):
        super(NLLSequenceLoss, self).__init__()
        self.criterion = NLLLoss()

    def forward(self, forward_input, target):
        loss = 0.0
        transposed = forward_input.transpose(0, 1).contiguous()

        for i in range(transposed.size(0)):
            loss += self.criterion(transposed[i], target)

        return loss


def get_folders_dic():
    '''This function gets the name of the folders from the dataset folder
    and creates a dictionary assigning the index of each folders to its
    name.'''
    dict_folder_index = {}

    for index, value_folder in enumerate(list(walk('./dataset-val'))[0][1]):
        dict_folder_index[index] = value_folder

    return dict_folder_index


class LSTMBackend(Module):
    def __init__(self, options):
        super(LSTMBackend, self).__init__()
        self.module = LSTM(input_size=options['model']['inputdim'],
                           hidden_size=options['model']['hiddendim'],
                           num_layers=options['model']['numlstms'],
                           batch_first=True,
                           bidirectional=True)

        self.fc = Linear(options['model']['hiddendim'] * 2,
                         options['model']['numclasses'])

        self.softmax = LogSoftmax(dim=2)

        self.loss = NLLSequenceLoss()

        self.validator = _validate

    def forward(self, forward_input):
        lstm_output, _ = self.module(forward_input)

        output = self.fc(lstm_output)
        output = self.softmax(output)

        return output
