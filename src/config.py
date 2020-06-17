# Configuration for training and testing

import os.path

class_names = ['BG','bluewhiting','herring','lanternfish','mackerel']

initial_weights = None
epochs = 10
input_size = (256,256,3)
batch_size = 2

# Settings for the output of imagesim-docker
subdirs = ['2017', '2018']
train_dirs = [os.path.join('/data','sim-'+y) for y in subdirs]
validation_dirs = [os.path.join('/data/validation','sim-'+y) for y in subdirs]
test_dirs = [os.path.join('/data','test-'+y) for y in subdirs]
