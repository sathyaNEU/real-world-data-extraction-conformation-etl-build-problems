"""task129 generator: tuning knobs, set so every graded figure sits inside its rounding bin.

KEEP_AUG keeps a share of August cached-load views by audience and template, chosen by a hash of
the page-view key (a cached view's removal changes no other view's state, and the windows that
measure the effects close before August); STEP_T is the dated changes' step by title."""
KEEP_AUG = {}
STEP_T = {
    "E": {"ST": 0.46, "LA": 0.46, "KD": 0.46},
    "B": {"ST": 0.68, "LA": 0.68, "KD": 0.68},
    "D": {"ST": 0.72, "LA": 0.72, "KD": 0.72},
}
