"""Tuning aid (never ships a figure): each served zone's arrival share as a function of how often a journey makes a
stay in the zone on the way in, from the world's own journeys.  python3 tune_b.py"""
import collections
import datetime as dt

import params as P
import world as W

ZONES = ["KW01", "KW02", "KW03", "KW04", "KW05", "KW09"]


def main():
    keep = dict(P.ARRIVE_P)
    for z in P.ARRIVE_CELLS:
        P.ARRIVE_P[z] = 1.0
    w = W.build()
    P.ARRIVE_P.update(keep)
    days = set(W.ordinary_2027())
    J = collections.defaultdict(list)       # zone -> [(work start minute, arrival-stay start minute, u)]
    import numpy as np
    for idx, dev in enumerate(w["devices"]):
        if dev.kind != "worker" or dev.dest not in ZONES or getattr(dev, "split_from", None):
            continue
        prng = np.random.default_rng([P.SEED, 992, idx])
        acts = [a for a in dev.acts if a[3] != "arrive"]
        arr = {a[2]: a for a in dev.acts if a[3] == "arrive"}
        prev_end = None
        for a in acts:
            if a[3] == "work":
                u, gap, dur = prng.random(), prng.uniform(3, 8), prng.uniform(20, 34)
                end = a[1] - dt.timedelta(minutes=float(gap))
                start = end - dt.timedelta(minutes=float(dur))
                ok = prev_end is None or start > prev_end + dt.timedelta(minutes=40)
                if a[1].date() in days and (a[2] - a[1]).total_seconds() >= 4 * 3600:
                    ws = a[1].replace(second=0, microsecond=0)
                    st = start.replace(second=0, microsecond=0)
                    wm = ws.hour * 60 + ws.minute
                    sm = st.hour * 60 + st.minute if ok else None
                    wm = wm + 1 if wm in (450, 570) else wm
                    if sm is not None and sm in (450, 570):
                        sm += 1
                    J[dev.dest].append((wm, sm, u))
            prev_end = a[2]

    def share(z, q):
        v = J[z]
        hit = sum(1 for wm, sm, u in v if 450 <= ((sm if (sm is not None and u < q) else wm)) <= 570)
        return 100.0 * hit / len(v)

    def longshare(z):
        v = J[z]
        return 100.0 * sum(1 for wm, sm, u in v if 450 <= wm <= 570) / len(v)
    for z in ZONES:
        cands = []
        for k in range(15, 71):
            q = k / 100.0
            s = share(z, q)
            d = abs((s - int(s)) - 0.5)
            if d >= 0.3 and round(s) != round(longshare(z)):
                cands.append((abs(q - P.ARRIVE_P.get(z, 0)), q, round(s, 2)))
        cands.sort()
        print(z, "now q=%.2f share %.2f long %.2f" % (P.ARRIVE_P.get(z, 0), share(z, P.ARRIVE_P.get(z, 0)), longshare(z)),
              "best", cands[:3])


if __name__ == "__main__":
    main()
