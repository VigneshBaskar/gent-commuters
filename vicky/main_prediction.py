# -*- coding: utf-8 -*-
# <nbformat>4</nbformat>

# <codecell>

import warnings
import os
warnings.filterwarnings('ignore')
import pickle
import numpy as np
from scripts.TrainingDataPreparation import prepare_sequences, create_network
from scripts.Prediction import generate_notes, create_midi

# <codecell>

with open('data/notes', 'rb') as filepath:
    notes = pickle.load(filepath)

pitchnames = sorted(set(item for item in notes))
n_vocab = len(set(notes))


# <codecell>

sequence_length = 100
network_input, network_output = prepare_sequences(notes, n_vocab, sequence_length)

# <codecell>

model = create_network(network_input, n_vocab, device_name='/gpu:1', dropout_rate=0.3)
model.load_weights(os.path.join('Models','mehdi_songs-07-4.1176-bigger.hdf5'))


# <codecell>

prediction_output = generate_notes(model, network_input, pitchnames, n_vocab)
output_midi_fname = 'test_out_midi'
create_midi(prediction_output, output_midi_fname)
