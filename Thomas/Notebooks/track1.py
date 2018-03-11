bpm = 130.0 # beat per minute

beat_per_bar = 8
steps_per_beat=4

bar_per_emphasis = 2

n_bars_buildup = 8

progression = [
    {"part":"intro", "buildup": 1.0, "duration": 4 , "tracks":[("base", "no") , ("chords", "no") , ("drums1", "no") , ("drums2", "no") , ("melody1", "yes"), ("melody2", "no") ]},
    {"part":"verse", "buildup": 1.0, "duration": 12, "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "no") , ("melody1", "yes"), ("melody2", "no") ]},
    {"part":"pause", "buildup": 1.0, "duration": 4,  "tracks":[("base", "yes"), ("chords", "no") , ("drums1", "no") , ("drums2", "no") , ("melody1", "no") , ("melody2", "no") ]},
    {"part":"verse", "buildup": 1.0, "duration": 12, "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "yes"), ("melody1", "yes"), ("melody2", "yes")]},
    {"part":"verse", "buildup": 1.0, "duration": 6,  "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "yes"), ("melody1", "yes"), ("melody2", "yes")]},
    {"part":"verse", "buildup": 0.3, "duration": 6,  "tracks":[("base", "yes"), ("chords", "yes"), ("drums1", "yes"), ("drums2", "no") , ("melody1", "yes"), ("melody2", "no") ]}
]