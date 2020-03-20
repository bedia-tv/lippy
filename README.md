# Lippy

Lippy is a lipreading system developed in Python using PyTorch, based on models described in [Combining Residual Networks with LSTMs for Lipreading] by T. Stafylakis and G. Tzimiropoulos.

Lippy is created by Denica Nedjalkova, Lewis Dyer, Lucas Prieto, Oscar Palafox Verna and Rory Young.

## Key Features

Lippy includes:

* A word-level model to predict the word being spoken, given a video of a speaker's lips, without the use of audio.
* A set of dataset tools to automatically process YouTube videos into separate videos for each word.
* A tool to compare the results of lipreading with a perfect transcript.

## Quick Start Guide

To set up Lippy:

- Install [Python 3], [Cmake] and [FFmpeg].
- Clone the repository.
- Run `pip3 install -r requirements.txt` to install all dependencies.

Lippy provides a command line interface to automatically process many YouTube videos at once. In order to build a training dataset:

1. Add a list of YouTube video URLs to `playlist.txt`, with one URL per line.
2. Run the command ```python -m src.interface dataset --function build --output train --playlist playlist.txt```.

In order to train our model on this dataset:

1. Create a new model and train it using `python -m src.interface.py model --train --new`.
2. If a model already exists in the path specified in `options.toml` use `python -m src.interface.py model --train` to keep training it.
3. Use `--epochs=` to set the number of times to train over the dataset (default = 1).
4. Use `--validate` to check the accuracy of the model. By default this checks the accuracy on the training dataset, you can change that in the `folder` field under `[validation]` in the `options.toml` file. The output is recorded in `accuracy.txt` file.

In order to perform predictions using this model:

1. Place one URL in `playlist.txt` of the YouTube video you wish to perform lipreading on.
2. Run the command ```python -m src.interface dataset --function build --output predict --playlist playlist.txt```.
3. Run `python -m src.interface.py model --predict` to get the model's prediction for each word in the `/predict` folder

## Further Information

Further information about the various components of Lippy is provided in the `docs` folder, giving additional details on how to run and set up each component.

## Bugs 

The current implementation uses code from an external source for `three-way-diff` which seems to fail in some cases. This is not part of the main functionality of Lippy but should be improved uppon moving forward.

## Licenses

Our model is based on an existing [PyTorch implementation] of the models described in [Combining Residual Networks with LSTMs for Lipreading]. This model is covered under the BSD 3-Clause License, which allows redistribution with modification, provided this license is retained.

Our software as a whole is covered under the MIT License.

[Combining Residual Networks with LSTMs for Lipreading]: <https://arxiv.org/pdf/1703.04105.pdf>
[Python 3]: <https://www.python.org/downloads/>
[PyTorch implementation]: <https://github.com/psyec1/Lipreading-PyTorch>
[Cmake]: <https://cmake.org/>
[FFmpeg]: <https://www.ffmpeg.org/>
