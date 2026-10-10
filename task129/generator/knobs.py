"""task129 generator: tuning knobs, set so every graded figure sits inside its rounding bin.

KEEP thins whole sessions by audience and landing template (on its own random stream, so a knob
moves volume without reshuffling anything else); STEP_T is the dated changes' step by title."""
KEEP = {'base': {'sektion': 0.88124,
          'galleri': 0.93822,
          'liveblog': 0.80302,
          'artikel': 0.84474,
          'sport': 0.82327,
          'forside': 0.85283},
 'sub': {'sektion': 0.30944,
         'galleri': -0.04453,
         'liveblog': 0.91692,
         'artikel': 0.86505,
         'sport': 1.0,
         'forside': 0.85255},
 'puz': {'spil': 0.83321}}
STEP_T = {'E': {'ST': 0.4737, 'LA': 0.4295, 'KD': 0.4675},
 'B': {'ST': 0.669, 'LA': 0.6928, 'KD': 0.6352},
 'D': {'ST': 0.7138, 'LA': 0.6979, 'KD': 0.7476}}
