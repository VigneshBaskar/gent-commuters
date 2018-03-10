# -*- coding: utf-8 -*-
# <nbformat>4</nbformat>

# <codecell>

import warnings
warnings.filterwarnings('ignore')
from scripts.TrainingDataPreparation import get_notes, prepare_sequences, create_network, train
import glob
import numpy as np
from music21 import converter, instrument, note, chord
import tensorflow as tf

# <codecell>

midi_directory = 'test_midi_songs'
notes = get_notes(midi_directory)
n_vocab = len(set(notes))
sequence_length = 100
network_input, network_output = prepare_sequences(notes, n_vocab, sequence_length)

# <codecell>

model = create_network(network_input, n_vocab, device_name='/gpu:0', dropout_rate=0.3)
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
train(model, network_input, network_output, n_epochs=10, batch_size=512, filename='mehdi_songs')
