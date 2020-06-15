# Configuration for training and testing

import os.path

class_names = ['BG','bluewhiting','herring','lanternfish','mackerel']

initial_weights = None
epochs = 10

# Settings for the output of imagesim-docker
# subdirs = ['sim-2017', 'sim-2018']
# multiple dires doesn't play well with ImageDataGenerators
train_dir = "/data/train/sim-2018"
validation_dir = "/data/validation/sim-2018"
test_dir = "/data/test"
