bpm = 130.0 # beat per minute

beat_per_bar = 8
steps_per_beat=4

bar_per_emphasis = 2

n_bars_buildup = 8

progression = [
    {"part":"verse", "buildup": 1.0, "duration": 4, "tracks":[("drums1", "yes"), ("drums2", "no")]},
    {"part":"verse", "buildup": 0.0, "duration": 4, "tracks":[("drums1", "yes"), ("drums2", "yes")]},
]

def track_primer(drum, bar):
    clonk = 49 if bar["final_bar"] else 42

    if drum == "drum1":
        primer = [(35,),(),(42,),(),(35,),(),(clonk,),()]
    elif drum == "drum2":
        primer = [(46,),(42,),(46,42,),(42,),(46,),(42,),(46,clonk,),(42,)]
        
    return primer