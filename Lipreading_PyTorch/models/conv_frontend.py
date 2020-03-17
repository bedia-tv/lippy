from torch.nn import BatchNorm3d, Conv3d, MaxPool3d, Module
from torch.nn.functional import relu


class ConvFrontend(Module):
    def __init__(self):
        super(ConvFrontend, self).__init__()

        self.conv = Conv3d(
            1, 64, (5, 7, 7), stride=(1, 2, 2), padding=(2, 3, 3))
        self.norm = BatchNorm3d(64)
        self.pool = MaxPool3d(
            (1, 3, 3), stride=(1, 2, 2), padding=(0, 1, 1))

    def forward(self, forward_input):
        output = self.pool(relu(self.norm(self.conv(forward_input))))

        return output
