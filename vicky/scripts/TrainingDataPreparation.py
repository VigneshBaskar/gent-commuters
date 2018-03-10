# -*- coding: utf-8 -*-
# <nbformat>4</nbformat>

# <codecell>

import glob
import pickle
import numpy as np
from music21 import converter, instrument, note, chord
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import os

# <codecell>

# def train_network():
#     """ Train a Neural Network to generate music """
#     notes = get_notes()

#     # get amount of pitch names
#     n_vocab = len(set(notes))

#     network_input, network_output = prepare_sequences(notes, n_vocab)

#     model = create_network(network_input, n_vocab)

#     train(model, network_input, network_output)

# <codecell>

def get_notes(directory):
    """ Get all the notes and chords from the midi files in the directory """
    notes = []

    for file in glob.glob(directory+"/*.mid"):
        midi = converter.parse(file)

        notes_to_parse = None

        parts = instrument.partitionByInstrument(midi)

        if parts: # file has instrument parts
            notes_to_parse = parts.parts[0].recurse()
        else: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes

# <codecell>

def prepare_sequences(notes, n_vocab, sequence_length):
    """ Prepare the sequences used by the Neural Network """

    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

     # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    network_input = network_input / float(n_vocab)

    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)

# <codecell>

def create_network(network_input, n_vocab, device_name, dropout_rate=0.3):
    """ create the structure of the neural network """
    with tf.device(device_name):

        model = Sequential()
        model.add(LSTM(
            512,
            input_shape=(network_input.shape[1], network_input.shape[2]),
            return_sequences=True
        ))
        model.add(Dropout(dropout_rate))
        model.add(LSTM(512, return_sequences=True))
        model.add(Dropout(dropout_rate))
        model.add(LSTM(512))
        model.add(Dense(256))
        model.add(Dropout(dropout_rate))
        model.add(Dense(n_vocab))
        model.add(Activation('softmax'))
        return model

# <codecell>

def train(model, network_input, network_output, n_epochs, batch_size, filename):
    """ train the neural network """
    filepath = os.path.join('Models',filename+"-{epoch:02d}-{loss:.4f}-bigger.hdf5")
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]
    model.fit(network_input, network_output, epochs=n_epochs, batch_size=batch_size,
              callbacks=callbacks_list)

# <codecell>

if __name__ == '__main__':
    print('Training from Scripts')
    train_network()
