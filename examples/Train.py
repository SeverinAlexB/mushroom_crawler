from __future__ import absolute_import
from __future__ import print_function
from src.Dataset import Dataset, CategorieInfo

import numpy as np


from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.regularizers import l2
from keras import callbacks

def load_dataset():
    #load dataset
    cat_infos = []

    echte_pfifferling = CategorieInfo.from_default("Echter Pfifferling/", [1,0,0])
    falscher_pfifferling = CategorieInfo.from_default("Falscher Pfifferling/", [0,1,0])
    fliegenpilz = CategorieInfo.from_default("fliegenpilz/", [0,0,1])

    cat_infos.append(echte_pfifferling)
    cat_infos.append(falscher_pfifferling)
    cat_infos.append(fliegenpilz)

    dataset = Dataset.from_sourcefolder("dataset1/")
    dataset.categorie_infos = cat_infos
    dataset.read_samples()
    return dataset



def VGG_16(input_shape=(224,224), nb_output=2):
    model = Sequential()
    model.add(ZeroPadding2D((1, 1),input_shape=(3, input_shape[0], input_shape[1])))
    model.add(Convolution2D(64, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(MaxPooling2D((2, 2), stride=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(MaxPooling2D((2, 2), stride=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(MaxPooling2D((2, 2), stride=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(MaxPooling2D((2,2), stride=(2,2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, init="glorot_normal"))
    model.add(PReLU())
    model.add(MaxPooling2D((2, 2), stride=(2, 2)))

    model.add(Flatten())
    model.add(Dense(4096, init="glorot_normal"))
    model.add(PReLU())

    model.add(Dropout(0.5))
    model.add(Dense(4096, init="glorot_normal"))
    model.add(PReLU())

    model.add(Dropout(0.5))
    model.add(Dense(nb_output, activation='softmax', init="glorot_normal"))
    return model

nb_classes = 3

# input image dimensions
input_shape = (224, 224)

print("make model")
model = VGG_16(input_shape, nb_classes)

print("start compiling")
model.compile(loss='categorical_crossentropy', optimizer='adadelta')

print("load dataset")
dataset = load_dataset()
train_data, test_data = dataset.split_train_test(0.9)
train_x, train_y = train_data.to_input_response()
test_x, test_y = test_data.to_input_response()
print("trainset len " + str(len(train_data.samples_shuffled)))
print("testset len " + str(len(test_data.samples_shuffled)))
print("input shape " + str(train_x.shape))
print("output shape " + str(train_y.shape))

print("start training")
filepath = "kerasSerialization/vgg_mushrooms1{epoch:02d},loss{val_loss:.3f},acc{val_acc:.4f}.hdf5"
save_callback = ModelCheckpoint(filepath, verbose=1, save_best_only=True)

batch_size = 16
nb_epoch = 500
model.fit(train_x, train_y, batch_size=batch_size, nb_epoch=nb_epoch, show_accuracy=True, verbose=1, validation_data=(test_x,test_y), callbacks=[save_callback])

