# This file trains the network.

import argparse
import sys

import params.Imagenet as p

from model.cnn_net import get_model, compile
from data.data_generator import Data
from data.preprocess_data import mapped_batch

if __name__ == "__main__":

    """ PARAMETERS"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="Params", default=None, type=str)
    arg = parser.parse_args(sys.argv[1:])

    print('Getting parameters to train the model...')
    params_string = arg.p
    params = p.PARAMS_DICT[params_string].get_params()
    output_path = params[p.OUTPUT_PATH]

    print('PARAMETERS')
    print(params)

    """ ARCHITECTURE DEFINITION """
    print(" Defining architecture ... ")
    # get model
    model = get_model(params[p.INPUT_SHAPE])
    # compile model
    model = compile(model)
    model.summary()

    """ DATA LOADING """
    print("Loading data ...")
    dataset_path = './data/dataset'
    d = Data(dataset_path)
    d.generate_data_from_url_file(dataset_file_path='./data/dataset.txt', h=256, w=256)

    listdir_train, listdir_val = d.split_train_val(num_images_train= params[p.N_IMAGES_TRAIN_VAL],train_size= params[p.TRAIN_SIZE])
    generator_train = d.data_generator(listdir=listdir_train,purpose='train', batch=params[p.BATCH_SIZE])
    generator_val = d.data_generator(listdir=listdir_val,purpose='val', batch=10)

    steps_per_epoch = len(listdir_train)
    steps_per_val = len(listdir_val)

    """ TENSORBOARD """
    # Define callbacks

    """ MODEL TRAINING """
    model.fit_generator(generator=generator_train,
                        steps_per_epoch=steps_per_epoch,
                        epochs=params[p.N_EPOCHS],
                        validation_data=generator_val,
                        validation_steps=steps_per_val)
    print("Training finished")