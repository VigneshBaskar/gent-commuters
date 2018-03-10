import os
import magenta
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

import pandas as pd

from magenta.music.sequences_lib import *

import magenta.music as mm

# Constants.
BUNDLE_DIR = '/home/jovyan/models/'
MODEL_NAME = 'drum_kit'
BUNDLE_NAME = 'drum_kit_rnn.mag'

def compute_time(qpm=120, nsteps=16, steps_per_quarter=4):
    seconds_per_step = 60.0 / qpm / steps_per_quarter
    total_seconds = nsteps * seconds_per_step
    return total_seconds

def generate_one_bar_sequence(generator, qpm=120.0,temp=1.0,number_of_steps=16,beam_size=4, steps_per_quarter=4, primer=[]):
    generator_options = generator_pb2.GeneratorOptions()

    generator_options.args['temperature'].float_value = temp  # Higher is more random; 1.0 is default.
    generator_options.args['beam_size'].int_value = beam_size

    if len(primer) != 0:
        print("Using primer" + str(primer))
        primer_drums = magenta.music.DrumTrack([frozenset(pitches) for pitches in primer])
        primer_sequence = primer_drums.to_sequence(qpm=qpm)
    else:
        print("no primer")
        primer_sequence = music_pb2.NoteSequence()
        
    total_seconds = compute_time(qpm, number_of_steps, steps_per_quarter)
    last_end_time = compute_time(qpm, len(primer), steps_per_quarter)

    generate_section = generator_options.generate_sections.add(
        start_time=last_end_time,
        end_time=total_seconds)

    return generator.generate(primer_sequence, generator_options)

def adjust_sequence_times_and_merge(seq1, seq2, delta_time):
    """Adjusts note and total NoteSequence times by 'delta_time'."""
    retimed_seq2 = music_pb2.NoteSequence()
    retimed_seq2.CopyFrom(seq2)

    for note in retimed_seq2.notes:
        note.start_time += delta_time
        note.end_time += delta_time
        retimed_seq2.total_time += delta_time
    
    seq1.MergeFrom(retimed_seq2)
    
    return seq1 