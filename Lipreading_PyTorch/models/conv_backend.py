from torch import max as t_max
from torch.nn import (
    BatchNorm1d, Conv1d, CrossEntropyLoss, Linear, MaxPool1d, Module)
from torch.nn.functional import relu


def _validate(model_output, labels):
    _maxvalues, maxindices = t_max(model_output.data, 1)
    count = 0

    for i in range(labels.squeeze(1).size(0)):
        if maxindices[i] == labels.squeeze(1)[i]:
            count += 1

    return count


class ConvBackend(Module):
    def __init__(self):
        super(ConvBackend, self).__init__()

        bn_size = 256
        self.conv1 = Conv1d(bn_size, 2 * bn_size, 2, 2)
        self.norm1 = BatchNorm1d(bn_size * 2)
        self.pool1 = MaxPool1d(2, 2)
        self.conv2 = Conv1d(2 * bn_size, 4 * bn_size, 2, 2)
        self.norm2 = BatchNorm1d(bn_size * 4)
        self.linear = Linear(4 * bn_size, bn_size)
        self.norm3 = BatchNorm1d(bn_size)
        self.linear2 = Linear(bn_size, 500)
        self.loss = CrossEntropyLoss()
        self.validator = _validate

    def forward(self, forward_input):
        transposed = forward_input.transpose(1, 2).contiguous()

        output = self.conv1(transposed)
        output = self.norm1(output)
        output = relu(output)
        output = self.pool1(output)
        output = self.conv2(output)
        output = self.norm2(output)
        output = relu(output)
        output = output.mean(2)
        output = self.linear(output)
        output = self.norm3(output)
        output = relu(output)
        output = self.linear2(output)

        return output
