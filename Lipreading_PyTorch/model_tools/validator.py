from os import walk
from torch import max as t_max
from torch import sum as t_sum
from torch.autograd import Variable
from torch.utils.data import DataLoader
from data.lipreading_dataset import LipreadingDataset


class Validator():
    def __init__(self, options):
        self.validation_dataset = LipreadingDataset(
            options['training']['dataset'], options['validation']['folder'], True,
            options['general']['padding'])
        self.validation_data_loader = DataLoader(
            self.validation_dataset,
            batch_size=options['input']['batchsize'],
            shuffle=options['input']['shuffle'],
            num_workers=options['input']['numworkers'],
            drop_last=True
        )
        self.usecudnn = options['general']['usecudnn']
        self.batchsize = options['input']['batchsize']
        self.gpuid = options['general']['gpuid']
        self.accuracy_file_location = options['validation']['accuracyfilelocation']

    def epoch(self, model):
        print('Validating...')
        validator_function = model.validator_function()
        count = 0

        for _i_batch, sample_batched in enumerate(self.validation_data_loader):
            input_var = Variable(sample_batched['temporalvolume'])
            labels = sample_batched['label']

            if self.usecudnn:
                input_var = input_var.cuda(self.gpuid)
                labels = labels.cuda(self.gpuid)

            outputs = model(input_var)
            count += validator_function(outputs, labels)

        accuracy = count / len(self.validation_dataset)

        with open(self.accuracy_file_location, 'a') as accuracyfile:
            accuracyfile.write(
                f'correct count: {count}, total count: {len(self.validation_dataset)} accuracy: {accuracy}\n')
