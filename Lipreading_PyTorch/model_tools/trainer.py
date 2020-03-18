from math import floor
from torch.optim import SGD
from torch import save
from torch.autograd import Variable
from torch.utils.data import DataLoader
from data.lipreading_dataset import LipreadingDataset


class Trainer():
    def __init__(self, options):
        self.training_dataset = LipreadingDataset(
            options['training']['dataset'], 'train', True,
            options['general']['padding'])
        self.trainingdataloader = DataLoader(
            self.training_dataset,
            batch_size=options['input']['batchsize'],
            shuffle=options['input']['shuffle'],
            num_workers=options['input']['numworkers'],
            drop_last=True
        )
        self.usecudnn = options['general']['usecudnn']
        self.batchsize = options['input']['batchsize']
        self.printfrequency = options['training']['printfrequency']
        self.gpuid = options['general']['gpuid']
        self.learningrate = options['training']['learningrate']
        self.model_type = options['training']['learningrate']
        self.weightdecay = options['training']['weightdecay']
        self.momentum = options['training']['momentum']
        self.pretrainedmodelpath = options['general']['pretrainedmodelpath']

    def learning_rate(self, epoch):
        decay = floor((epoch - 1) / 5)

        return self.learningrate * pow(0.5, decay)

    def epoch(self, model, epoch):
        # Set up the loss function.
        criterion = model.loss()
        optimizer = SGD(
            model.parameters(),
            lr=self.learning_rate(epoch),
            momentum=self.learningrate,
            weight_decay=self.weightdecay)

        if self.usecudnn:
            criterion = criterion.cuda(self.gpuid)

        for _i_batch, sample_batched in enumerate(self.trainingdataloader):
            optimizer.zero_grad()
            input_variable = Variable(sample_batched['temporalvolume'])
            labels = Variable(sample_batched['label'])

            if self.usecudnn:
                input_variable = input_variable.cuda(self.gpuid)
                labels = labels.cuda(self.gpuid)

            outputs = model(input_variable)
            loss = criterion(outputs, labels.squeeze(1))

            loss.backward()
            optimizer.step()

        if not epoch % self.printfrequency:
            print(f'Iteration: {epoch}')

        print('Epoch completed, saving state...')
        save(model.state_dict(), self.pretrainedmodelpath)
