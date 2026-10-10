"""task129 generator: tuning knobs, set so every graded figure sits inside its rounding bin.

KEEP_AUG keeps a share of August cached-load views by audience and template, chosen by a hash of
the page-view key (a cached view's removal changes no other view's state, and the windows that
measure the effects close before August); STEP_T is the dated changes' step by title."""
KEEP_AUG = {}
STEP_T = {'E': {'ST': 0.46, 'LA': 0.4375, 'KD': 0.4906},
 'B': {'ST': 0.6824, 'LA': 0.652, 'KD': 0.6472},
 'D': {'ST': 0.7369, 'LA': 0.7377, 'KD': 0.6744}}
