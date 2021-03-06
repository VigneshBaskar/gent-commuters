import os
import magenta
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
import pretty_midi
import math

from magenta.music.midi_io import sequence_proto_to_midi_file, sequence_proto_to_pretty_midi
import pickle

import pandas as pd

from magenta.music.sequences_lib import *

import magenta.music as mm

import scipy
import subprocess
import IPython

def generate_mp3(total_wave,ext="_bid"):
    scipy.io.wavfile.write('total'+ext+'.wav', rate=44100, data=total_wave)
    subprocess.call(['lame','-h','total'+ext+'.wav','total'+ext+'.mp3'])
    out = IPython.display.Audio('total'+ext+'.mp3')
    return out
    

# Constants.
def produce_drum_generator():
    BUNDLE_DIR = '/home/jovyan/models/'
    MODEL_NAME = 'drum_kit'
    BUNDLE_NAME = 'drum_kit_rnn.mag'
    mm.notebook_utils.download_bundle(BUNDLE_NAME, BUNDLE_DIR)
    bundle = mm.sequence_generator_bundle.read_bundle_file(os.path.join(BUNDLE_DIR, BUNDLE_NAME))
    drum_generator_map = drums_rnn_sequence_generator.get_generator_map()
    drum_generator = drum_generator_map[MODEL_NAME](checkpoint=None, bundle=bundle)
    
    return drum_generator
    
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

def generate_backbone(bpm, beat_per_bar, bar_per_emphasis, n_bars_buildup, progression):
    structure = []

    current_bar = 0
    start_time = 0.0
    for phase in progression:
        print("handling " + str(phase))
        for b in range(phase["duration"]):
            
            bar_properties = phase.copy()
            del bar_properties["tracks"]
            
            end_time = start_time + 60.0 * float(beat_per_bar)/bpm
            
            for t,v in phase["tracks"]:
                if v == "yes":
                    bar_properties[t] = 1.0
                else:
                    bar_properties[t] = 0.0

                buildup = phase["buildup"]
                n_bars_buildup_here = min(n_bars_buildup,phase["duration"])
                bar_properties["buildup_factor"] = buildup*max(0.0, (float(b) - phase["duration"] + float(n_bars_buildup_here) )/float(n_bars_buildup_here))
                bar_properties["current_bar"] = current_bar
                bar_properties["final_bar"] = b+1 == phase["duration"]
                bar_properties["beat_per_bar"] = beat_per_bar
                bar_properties["noise_buildup"] = buildup
                
                bar_properties["start_time"] = start_time
                bar_properties["end_time"]  = end_time

            structure.append(bar_properties)

            current_bar += 1
            start_time=end_time
            
    return structure