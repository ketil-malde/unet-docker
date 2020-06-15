# Train a Unet

import config as C
from model import unet

import skimage.io as io
import skimage.transform as trans
from keras.preprocessing.image import ImageDataGenerator
import numpy as np 

# todo: check if we are continuing from previous training or starting afresh
model = unet(C.initial_weights) # does it scale images to input size automatically?

from tensorflow.keras.callbacks import CSVLogger
logger = CSVLogger("train.log", append=True, separator='\t')

data_gen_args = dict(rotation_range = 0.2,
                    width_shift_range = 0.05,
                    height_shift_range = 0.05,
                    shear_range = 0.05,
                    zoom_range = 0.05,
                    horizontal_flip = True,
                    fill_mode = 'nearest')

# What is this about?
def adjustData(img, mask, flag_multi_class, num_class):
    if(flag_multi_class):
        img = img / 255
        mask = mask[:,:,:,0] if(len(mask.shape) == 4) else mask[:,:,0]
        new_mask = np.zeros(mask.shape + (num_class,))
        for i in range(num_class):
            #for one pixel in the image, find the class in mask and convert it into one-hot vector
            #index = np.where(mask == i)
            #index_mask = (index[0],index[1],index[2],np.zeros(len(index[0]),dtype = np.int64) + i) if (len(mask.shape) == 4) else (index[0],index[1],np.zeros(len(index[0]),dtype = np.int64) + i)
            #new_mask[index_mask] = 1
            new_mask[mask == i,i] = 1
        new_mask = np.reshape(new_mask,(new_mask.shape[0],new_mask.shape[1]*new_mask.shape[2],new_mask.shape[3])) if flag_multi_class else np.reshape(new_mask,(new_mask.shape[0]*new_mask.shape[1],new_mask.shape[2]))
        mask = new_mask
    elif(np.max(img) > 1):
        img = img / 255
        mask = mask /255
        mask[mask > 0.5] = 1
        mask[mask <= 0.5] = 0
    return (img,mask)

def train_generator(batch_size, train_path, image_folders, mask_folders, aug_dict, image_color_mode = "grayscale",
                    mask_color_mode = "grayscale", image_save_prefix  = "image", mask_save_prefix  = "mask",
                    flag_multi_class = False, num_class = 2, save_to_dir = None, target_size = (256,256), seed = 1):
    '''
    can generate image and mask at the same time
    use the same seed for image_datagen and mask_datagen to ensure the transformation for image and mask is the same
    if you want to visualize the results of generator, set save_to_dir = "your path"
    '''
    image_datagen = ImageDataGenerator(**aug_dict)
    mask_datagen = ImageDataGenerator(**aug_dict)
    image_generator = image_datagen.flow_from_directory(
        train_path,
        classes = image_folders,
        class_mode = None,
        color_mode = image_color_mode,
        target_size = target_size,
        batch_size = batch_size,
        save_to_dir = save_to_dir,
        save_prefix  = image_save_prefix,
        seed = seed)

    mask_generator = mask_datagen.flow_from_directory(
        train_path,
        classes = mask_folders,
        class_mode = None,
        color_mode = mask_color_mode,
        target_size = target_size,
        batch_size = batch_size,
        save_to_dir = save_to_dir,
        save_prefix  = mask_save_prefix,
        seed = seed)

    train_generator = zip(image_generator, mask_generator)

    # generator for data
    for (img,mask) in train_generator:
        img,mask = adjustData(img, mask, flag_multi_class, num_class)
        yield (img,mask)

def test_generator(test_path, num_image = 30, target_size = (256,256), flag_multi_class = False, as_gray = True):
    for i in range(num_image):
        img = io.imread(os.path.join(test_path,"%d.png"%i),as_gray = as_gray)
        img = img / 255
        img = trans.resize(img,target_size)
        img = np.reshape(img,img.shape+(1,)) if (not flag_multi_class) else img
        img = np.reshape(img,(1,)+img.shape)
        yield img
        
myGen = train_generator(2, C.train_dirs, 'image', 'label', data_gen_args, save_to_dir = None)

model = unet()
# model_checkpoint = ModelCheckpoint('unet_membrane.hdf5', monitor='loss',verbose=1, save_best_only=True)
model.fit_generator(myGen, steps_per_epoch=300, epochs=1, callbacks=[logger]) # callbacks=[model_checkpoint,logger])
