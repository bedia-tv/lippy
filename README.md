# Lipreading With Machine Learning In PyTorch
A PyTorch implementation of the models described in [Combining Residual Networks with LSTMs for Lipreading]  by T. Stafylakis and G. Tzimiropoulos. Adapted from the [Torch7 code].

## Usage
 - Install [Python 3].
 - Clone the repository.
 - Run `pip3 install -r requirements.txt` to install all dependencies
 
## Training a model
 - Create a new model and train it using `python -m src.interface.py model --train --new`.
 - If a model already exists in the path specified in `options.toml` use `python -m src.interface.py model --train` to keep training it.
 - Use `--epochs=` to set the number of times to train over the dataset (default = 1).
 - Use `--validate` to check the accuracy of the model. By default this checks the accuracy on the training dataset, you can change that in the `folder` field under `[validation]` in the `options.toml` file.
 - A usual command when training a model would look like: `python -m src.interface.py model --train --validate --epochs=30`

## Lipreading on a YouTube Video
 - Once a model is trained we can use it to process the lip movements.
 - We can use a command from the dataset builder to get clips from the video and save them under the predict folder.
 - Once the contents of the YouTube video are saved under predict use `python -m src.interface.py model --predict` to get the model's prediction for each word in the `/predict` folder. 

## Options
 - The `options.toml` file can be used to change the behaviour of the program
 - Add the path to your dataset under `dataset:` for validation and training.
 - When validating the accuracy score is saved in the file specified under `[validation]` at `accuracyfilelocation` in the options.toml file.
 - When predicting the model goes over the dataset specified under `prediction` to make a word prediction for each video in it.  
 - Under `[training]` you can specify the `folder` to use as dataset, and `printfrequency` to specify the frequency in epochs with which to print information about the training progress.
 - The pretrained model is saved to, and loaded from the path under `[general]` and `pretrainedmodelpath` in the options.toml file.
 - The `[validation]`, `folder` option can be used to specify a folder under each word folder to be used as validation examples for that word. If this option is set to `train` the model uses the training dataset for validation.
 
## Dataset structure
 - Every video in the training dataset is stored in a folder with the name of the word being said in the video.
 - The structure is `dataset/{word}/train/video.mp4`.
 - The model is trained to predict what word folder better fits a new video. For a video in which someone is saying `Hello` the model should predict the index of the `Hello` folder inside the dataset directory. This index is mapped to the word `Hello` which is returned to the interface as a string and printed to the command line.

## Main principles of the model
 - The main functionality is managed by the files under `Lipreading_PyTorch/model_tools` and `src/model/model_tools` which are called from run_model.py depending on the parameters passed to the interface.
 - The `Lipreading_PyTorch/data` folder contains code related to processing the videos.
 - The `src/model/models` folder contains the code for the different networks that the system can use.
 - `src/model/checker.py` is used to check that every video has enough frames to be processed. Note that the value of the allowed padding can be changed in the options.toml file.

## Testing
 - To run the tests use `python -m pytest tests/`.
 
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
