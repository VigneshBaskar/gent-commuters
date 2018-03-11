import os

bpm = 130.0 # beat per minute

beat_per_bar = 8
steps_per_beat=4

bar_per_emphasis = 2

root_name = 'funk_30'

bar_offset = 1

n_bars_buildup = 8

progression = [
    {"part":"intro", "buildup": 1.0, "duration": 4 , "tracks":[("base", "no") , ("chords", "no") , ("drums1", "no") , ("drums2", "no") , ("melody1", "yes"), ("melody2", "no") ]},
    {"part":"verse", "buildup": 1.0, "duration": 12, "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "no") , ("melody1", "yes"), ("melody2", "no") ]},
    {"part":"pause", "buildup": 1.0, "duration": 4,  "tracks":[("base", "yes"), ("chords", "no") , ("drums1", "no") , ("drums2", "no") , ("melody1", "no") , ("melody2", "no") ]},
    {"part":"verse", "buildup": 1.0, "duration": 12, "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "yes"), ("melody1", "yes"), ("melody2", "yes")]},
    {"part":"verse", "buildup": 0.5, "duration": 6,  "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "yes"), ("melody1", "yes"), ("melody2", "yes")]},
    {"part":"verse", "buildup": 0.0, "duration": 6,  "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "no") , ("melody1", "yes"), ("melody2", "no") ]}
]

def track_primer(drum, bar):
    clonk = 49 if bar["final_bar"] else 42

    if drum == "drum1":
        primer = [(35,),(),(42,),(),(35,),(),(clonk,),()]
    elif drum == "drum2":
        primer = [(46,),(42,),(46,),(42,),(46,),(42,),(46,),(42,)]
        
    return primer