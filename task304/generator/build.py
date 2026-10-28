"""Write the pack under a target folder: the data files from the world, then the three documents."""
import os
import shutil

import docs
import params as P
import records
import world

PACK = ["lab", "register", "prison", "peer", "arrivals", "pilot", "plan", "evaluation", "pathway", "clinics",
        "nsp_activity", "fibroscan"]
CONTEXT = ["plan", "evaluation", "pathway"]
DISTRACTORS = P.DISTRACTORS
FILE_DATE = "2026-10-12"


def build(target, seed=P.SEED):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = world.build(seed)
    n = records.write_all(W, target)
    docs.plan(os.path.join(target, P.FILES["plan"]))
    docs.evaluation(os.path.join(target, P.FILES["evaluation"]), W.pilot)
    docs.pathway(os.path.join(target, P.FILES["pathway"]))
    stamp(target)
    return W, n


def stamp(target):
    import datetime as dt
    import time
    t = time.mktime(dt.datetime(2026, 10, 12, 11, 40, 0).timetuple())
    for root, _, files in os.walk(target):
        for f in files:
            os.utime(os.path.join(root, f), (t, t))
