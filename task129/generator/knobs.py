"""task129 generator: tuning knobs, set so every graded figure sits inside its rounding bin.

KEEP_AUG keeps a share of August cached-load views by audience and template, chosen by a hash of
the page-view key (a cached view's removal changes no other view's state, and the windows that
measure the effects close before August); STEP_T is the dated changes' step by title."""
KEEP_AUG = {'base|artikel': 0.92,
 'base|forside': 1.0,
 'base|galleri': 0.94,
 'base|liveblog': 0.8275,
 'base|sektion': 0.8725,
 'base|sport': 0.8,
 'puz|spil': 0.905,
 'sub|artikel': 0.85,
 'sub|forside': 1.0,
 'sub|galleri': 0.94,
 'sub|liveblog': 0.8,
 'sub|sektion': 1.0,
 'sub|sport': 0.8}
STEP_T = {'E': {'ST': 0.46, 'LA': 0.4191, 'KD': 0.4693},
 'B': {'ST': 0.6644, 'LA': 0.6775, 'KD': 0.6472},
 'D': {'ST': 0.7369, 'LA': 0.7466, 'KD': 0.6744}}
