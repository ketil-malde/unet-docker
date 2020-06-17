# Train a Unet

import config as C
from model import unet

import skimage.io as io
import skimage.transform as trans

import os
import re
import random
import csv
import numpy as np 
import skimage.transform as T

# todo: check if we are continuing from previous training or starting afresh
model = unet(C.initial_weights) # does it scale images to input size automatically?

from tensorflow.keras.callbacks import CSVLogger
logger = CSVLogger("train.log", append=True, separator='\t')

# Output arrays of images and masks
def my_generator(batch_size, images_dirs):
    width, height, depth = C.input_size
    num_classes = len(C.class_names)

    for images_dir in images_dirs:
        filenames = [os.path.join(images_dir,f) for f in os.listdir(images_dir) if re.match(r'sim-201[78]_[0-9]+\.png', f)]

    while True:
        # specifications for this?
        imgs = np.empty(shape = (batch_size,width,height,3)) # dtype='uint8' anywhere?
        masks = np.zeros(shape = (batch_size, width, height, num_classes))
        #print('imgs.shape:',imgs.shape)
        for i in range(batch_size):
            f = random.choice(filenames)
            #print('f=',f)

            # load the image
            img = io.imread(f)/255 # np.array(Image.open(f))/255
            #print('img max:', np.max(img), 'shape:', img.shape)

            # load annotations
            ann = f[:-4]+'.txt'
            #print('ann=', ann)
            h, w, c = img.shape
            mask = np.zeros([h, w, num_classes])
            with open(ann) as af:
                nr = 0
                for p,xmin,ymin,xmax,ymax,classname in csv.reader(af):
                    class_id = C.class_names.index(classname)
                    m = io.imread(os.path.join(os.path.dirname(f),'mask_'+os.path.basename(f)[:-4]+'_'+str(nr)+'.png'), as_gray = True)
                    #print('m max:', np.max(m), 'shape:', m.shape)
                    mask[:,:,class_id] += m
                    nr += 1
            # todo: augment using the same ops on img and mask, (scipy.ndimage?)
            # resize, and then...
            imgs[i] = T.resize(img, (width,height), anti_aliasing=True)
            masks[i] = T.resize(mask, (width, height), anti_aliasing=False)  # does this work at all?
        yield (imgs, masks)

g = my_generator(C.batch_size, C.train_dirs)

# (i,m) = next(g)
# print('images=',i.shape, i)
# print('masks=', m.shape, m)
        
model = unet()
# model_checkpoint = ModelCheckpoint('unet_membrane.hdf5', monitor='loss',verbose=1, save_best_only=True)
model.fit_generator(g, steps_per_epoch=300, epochs=10, callbacks=[logger]) # callbacks=[model_checkpoint,logger])
model.save_weights('unet_weights.h5')
