"""Quick ladder readings from the simulation for a few settings (no files written)."""
import sys
from collections import defaultdict

import numpy as np

import book
import world


def peaks(rows, work):
    by = defaultdict(list)
    for d, s, e in rows:
        by[d] += [(s, 1), (e, -1)]
    out = {}
    for d in work:
        c = m = 0
        for _, v in sorted(by.get(d, [])):
            c += v
            m = max(m, c)
        out[d] = m
    return out


def p13(pk):
    return sorted(pk.values(), reverse=True)[12]


def run(rate, seed=114):
    world.ADHOC_RATE = rate
    W = world.World()
    rng = np.random.default_rng(seed)
    W.rooms = world.rooms()
    world.build_people(W, rng); world.build_presence(W, rng); world.build_meetings(W, rng)
    world.build_client_and_events(W, rng); book.build(W, rng)
    di = {d: i for i, d in enumerate(W.work)}
    ans, acc, allr, bk = [], [], [], []
    for m in W.meetings:
        if m["cancelled"]:
            continue
        i = di[m["day"]]
        n = sum(1 for q, t, r in m["att"] if r != "declined" and W.pres[q, i] > 0)
        na = sum(1 for q, t, r in m["att"] if r in ("accepted", "organizer") and W.pres[q, i] > 0)
        nall = sum(1 for q, t, r in m["att"] if W.pres[q, i] > 0)
        iv = (m["day"], m["start"], m["start"] + m["dur"])
        if n >= 2: ans.append(iv)
        if na >= 2: acc.append(iv)
        if nall >= 2: allr.append(iv)
    for b in W.bookings:
        if b["kind"] in ("meeting",):
            bk.append((b["day"], b["s"], b["e"]))
        if b["kind"] == "noshow":
            bk.append((b["day"], b["s"], b["s"] + 15))
    pa = peaks(ans, W.work)
    R = p13(pa)
    vals = sorted(pa.values(), reverse=True)
    return dict(rate=rate, R=R, top=vals[10:15], natural=p13(peaks(bk, W.work)), acc=p13(peaks(acc, W.work)),
                declined=p13(peaks(allr, W.work)), fails=len(W.book_fails))


if __name__ == "__main__":
    for r in [float(x) for x in sys.argv[1:]]:
        print(run(r))
