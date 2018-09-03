# -*- coding: utf-8 -*-
"""

Alexnet model for FasterRCNN, requiring 3 channels input.

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import warnings

from keras.models import Model
from keras.layers import Flatten, Dense, Input, Conv2D, MaxPooling2D, Dropout
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, TimeDistributed
from keras.engine.topology import get_source_inputs
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras import backend as K
from keras_frcnn.RoiPoolingConv import RoiPoolingConv

from keras.layers.normalization import BatchNormalization



def get_weight_path():
    if K.image_dim_ordering() == 'th':
        print('pretrained weights not available for VGG with theano backend')
        return
    else:
        return 'vgg16_weights_tf_dim_ordering_tf_kernels.h5'


def get_img_output_length(width, height):
    def get_output_length(input_length):
        return input_length//16

    return get_output_length(width), get_output_length(height)    

def nn_base(input_tensor=None, trainable=False):


    # Determine proper input shape
    if K.image_dim_ordering() == 'th':
        input_shape = (3, None, None)
    else:
        #input_shape = (None, None, 1)
        input_shape = (None, None, 3)

    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor

    if K.image_dim_ordering() == 'tf':
        bn_axis = 3
    else:
        bn_axis = 1

	# pretrained alexnet
	# use the same kernel_initializer as sina if you use the same data normalization
    x = Conv2D(96, (11, 11), strides=(4,4), activation='relu', padding='same', name='conv2d_1', kernel_initializer='glorot_normal')(img_input)
    x = MaxPooling2D((2, 2), strides=(2, 2), padding='same', name='max_pooling2d_1')(x)
    x = BatchNormalization()(x)
    x = Conv2D(256, (11, 11), strides = (1,1), activation='relu', padding='same', name='conv2d_2', kernel_initializer='glorot_normal')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='max_pooling2d_2')(x)
    x = BatchNormalization()(x)
    x = Conv2D(384, (3, 3), activation='relu', padding='same', name='conv2d_3', kernel_initializer='glorot_normal')(x)
    x = Conv2D(384, (3, 3), activation='relu', padding='same', name='conv2d_4', kernel_initializer='glorot_normal')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='conv2d_5', kernel_initializer='glorot_normal')(x)

    return x

def rpn(base_layers, num_anchors):

    x = Conv2D(512, (3, 3), padding='same', activation='relu', kernel_initializer='normal', name='rpn_conv1')(base_layers)

    x_class = Conv2D(num_anchors, (1, 1), activation='sigmoid', kernel_initializer='uniform', name='rpn_out_class')(x)
    x_regr = Conv2D(num_anchors * 4, (1, 1), activation='linear', kernel_initializer='zero', name='rpn_out_regress')(x)

    return [x_class, x_regr, base_layers]

# modify here for different initializer
def classifier(base_layers, input_rois, num_rois, nb_classes = 21, trainable=False):

    # compile times on theano tend to be very high, so we use smaller ROI pooling regions to workaround

    if K.backend() == 'tensorflow':
        pooling_regions = 7
        input_shape = (num_rois,7,7,512)
    elif K.backend() == 'theano':
        pooling_regions = 7
        input_shape = (num_rois,512,7,7)

    out_roi_pool = RoiPoolingConv(pooling_regions, num_rois)([base_layers, input_rois])

    out = TimeDistributed(Flatten(name='flatten'))(out_roi_pool)
    #out = TimeDistributed(Dense(4096, activation='relu', name='fc1'))(out)
    out = TimeDistributed(Dense(4096, activation='relu', name='fc1', kernel_initializer='glorot_normal'))(out)
    out = TimeDistributed(Dropout(0.5))(out)
    #out = TimeDistributed(Dense(4096, activation='relu', name='fc2'))(out)
    out = TimeDistributed(Dense(4096, activation='relu', name='fc2', kernel_initializer='glorot_normal'))(out)
    out = TimeDistributed(Dropout(0.5))(out)

    out_class = TimeDistributed(Dense(nb_classes, activation='softmax', kernel_initializer='zero'), name='dense_class_{}'.format(nb_classes))(out)
    # note: no regression target for bg class
    out_regr = TimeDistributed(Dense(4 * (nb_classes-1), activation='linear', kernel_initializer='zero'), name='dense_regress_{}'.format(nb_classes))(out)

    return [out_class, out_regr]



