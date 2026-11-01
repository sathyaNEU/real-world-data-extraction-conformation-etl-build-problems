"""One pack from nothing: the world, the ask records and every file under target/."""
import os
import shutil

import pack as PK
import params as P
import world as W


def build(target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    w = W.World(P.SEED)
    W.make_ask_records(w)
    pref, counts = PK.build_pack(w, target)
    for fn in os.listdir(target):
        t = P.ASSEMBLED.timestamp()
        os.utime(os.path.join(target, fn), (t, t))
    return w, counts
