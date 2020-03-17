# Lipreading With Machine Learning In PyTorch
A PyTorch implementation of the models described in [Combining Residual Networks with LSTMs for Lipreading]  by T. Stafylakis and G. Tzimiropoulos. Adapted from the [Torch7 code].

## Usage
 - Install [Python 3].
 - Clone the repository.
 - Run `pip3 install -r requirements.txt` to install all dependencies
 - To use, run  `python3 main.py`.

## Options
 - options.toml can be used to change settings
 - Add the path to your dataset under "dataset:" for validation and training

## Dataset structure
 - Folders under the dataset directory are used as lables.
 - Each folder under that directory should have a folder called train containing examples of that word.
 - For validation files need to be under the folder for the corresponding word, in a folder called val.
## Dependencies
 - [Python 3] to run the program
 - [PyTorch] for tensors, network definition and backprop
 - [ImageIO] to load video clips
 - [NumPy] to visualize individual layers
 - [TOML] to parse TOML-formatted data

   [Combining Residual Networks with LSTMs for Lipreading]: <https://arxiv.org/pdf/1703.04105.pdf>
   [Torch7 code]: <https://github.com/tstafylakis/Lipreading-ResNet>
   [Python 3]: <https://www.python.org/downloads/>
   [PyTorch]: <http://pytorch.org/>
   [ImageIO]: <https://imageio.github.io/>
   [NumPy]: <http://www.numpy.org/>
   [TOML]: <https://github.com/uiri/toml>
