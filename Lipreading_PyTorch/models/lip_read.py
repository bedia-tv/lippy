from re import search
from torch.nn import Module
from Lipreading_PyTorch.models.conv_backend import ConvBackend
from Lipreading_PyTorch.models.conv_frontend import ConvFrontend
from Lipreading_PyTorch.models.LSTMBackend import LSTMBackend
from Lipreading_PyTorch.models.ResNetBBC import ResNetBBC


class LipRead(Module):
    def __init__(self, options):
        super(LipRead, self).__init__()
        self.frontend = ConvFrontend()
        self.resnet = ResNetBBC(options)
        self.backend = ConvBackend()
        self.lstm = LSTMBackend(options)
        self.type = options['model']['type']

        def weights_init(m):
            '''Function to initialize the weights and biases of each
            module. Matches the classname with a regular expression to
            determine the type of the module, then initializes the weights
            for it.'''
            classname = m.__class__.__name__

            if search('Conv[123]d', classname):
                m.weight.data.normal_(0.0, 0.02)
            elif search('BatchNorm[123]d', classname):
                m.weight.data.fill_(1.0)
                m.bias.data.fill_(0)
            elif search('Linear', classname):
                m.bias.data.fill_(0)

        # Apply weight initialization to every module in the model.
        self.apply(weights_init)

    def forward(self, forward_input):
        if self.type == 'temp-conv':
            output = self.backend(self.resnet(self.frontend(forward_input)))

        if self.type == 'LSTM' or self.type == 'LSTM-init':
            output = self.lstm(self.resnet(self.frontend(forward_input)))

        return output

    def loss(self):
        if self.type == 'temp-conv':
            return self.backend.loss
        elif self.type == 'LSTM' or self.type == 'LSTM-init':
            return self.lstm.loss
        else:
            return None

    def validator_function(self):
        if self.type == 'temp-conv':
            return self.backend.validator
        elif self.type == 'LSTM' or self.type == 'LSTM-init':
            return self.lstm.validator
        else:
            return None
