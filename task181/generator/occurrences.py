"""The occurrence record, January 2025 to September 2026: losses of separation (separation minima infringements),
ACAS resolution advisory reports, and the unit's other reportable occurrences.

Every loss of separation is a pair of aircraft in one sector at once whose levels changed order (one climbed or
descended through the other's level): the expected count in a sector and local month is a constant rate per such
pair times the pairs, and the realised count follows the expectation by error diffusion (the offsets chosen once
so that each window's count stays near its expectation). ACAS encounters come from pairs that changed order and
from close pairs where one aircraft levelled off near the other; a crew that got an advisory files its own report,
so an encounter in which both crews reported is two occurrences."""
import datetime as dt

import numpy as np
import pandas as pd

import exposure as X
import traffic as T
import world as W

SEED = 18121


def local_month(sec):
    """Local (year, month) index for UTC seconds since the traffic epoch: months since January 2025."""
    ts = pd.to_datetime(np.asarray(sec, dtype="int64") + int(T.EPOCH.timestamp()), unit="s", utc=True)
    loc = ts.tz_convert(W.LOCAL)
    return (loc.year.values - 2025) * 12 + loc.month.values - 1


def season_mask(sec, year):
    a, b = W.season(year)
    sec = np.asarray(sec)
    return (sec >= T.secs(a)) & (sec < T.secs(b))


def pairs_of(t):
    """Per sector: the sorted traversal indices and the pair table of the record."""
    out = {}
    for s, order, pt in X.by_sector(t):
        out[s] = (order, pt)
    return out


def untie(f, t, rounds=12):
    """Move a flight by one second where a pair's level difference is all but zero at the start or end of its shared
    time and one of the two levels there is interpolated (not a recorded entry or exit level, nor a level flight),
    so that whether two profiles change order never rests on rounding. A difference of exactly zero between two
    recorded levels (an aircraft reaching or leaving the level of another at its own entry or exit) is exact under
    any arithmetic and stays. Returns the number of flights moved."""
    moved = 0
    for _ in range(rounds):
        bad = set()
        for s, order, pt in X.by_sector(t):
            t0, t1 = t["t0"][order], t["t1"][order]
            lvl = t["a"][order] == t["b"][order]
            i, j = pt["i"], pt["j"]

            def exact(at):
                return ((lvl[i] | (at == t0[i]) | (at == t1[i])) & (lvl[j] | (at == t0[j]) | (at == t1[j])))
            tiny = ((~exact(pt["lo"]) & (np.abs(pt["dlo"]) < 1e-3)) | (~exact(pt["hi"]) & (np.abs(pt["dhi"]) < 1e-3)))
            for jj in pt["j"][tiny]:
                bad.add(int(t["fi"][order[jj]]))
        if not bad:
            return moved
        mask = np.isin(t["fi"], np.array(sorted(bad)))
        t["t0"][mask] += 1
        t["t1"][mask] += 1
        f["eobt"][np.array(sorted(bad))] += 1
        moved += len(bad)
    raise SystemExit("untie did not converge")


def _diffuse(expected, offset, dither):
    """Integer counts by error diffusion with a moving threshold: each month takes the expectation plus the error
    carried from the months before, rounds at a threshold near one half, and carries what it did not take, so the
    running total never strays a whole event from the running expectation."""
    err = offset - 0.5
    out = []
    for e, d in zip(expected, dither):
        x = err + e
        n = max(int(np.floor(x + 0.5 + d)), 0)
        out.append(n)
        err = x - n
    return np.array(out, dtype=int)


def schedule_losses(t, pairs, lam, rng, constraints=None, tries=4000):
    """Per sector and local month, how many of the pairs that changed order become losses of separation, by error
    diffusion with offsets searched until the constraints hold. Returns {sector: counts by month index}."""
    months = 21
    cross_by = {}
    for s, (order, pt) in pairs.items():
        mi = local_month(pt["tx"][pt["cross"]].astype(np.int64))
        cross_by[s] = np.bincount(mi[(mi >= 0) & (mi < months)], minlength=months)
    for k in range(tries):
        offs = rng.random(8)
        dith = rng.uniform(-0.35, 0.35, size=(8, months))
        counts = {s: _diffuse(lam * cross_by[s], offs[s], dith[s]) for s in range(8)}
        if constraints is None or constraints(counts, cross_by):
            return counts, cross_by, k
    raise SystemExit("no loss schedule met the constraints")


def pick_events(t, pairs, counts, rng, exclude=None):
    """Choose the pairs that became events: for each sector and local month, that many pairs that changed order,
    uniformly. Returns rows (sector, traversal i, traversal j, tx, lx)."""
    out = []
    for s, (order, pt) in pairs.items():
        cr = np.nonzero(pt["cross"])[0]
        mi = local_month(pt["tx"][cr].astype(np.int64))
        for m, n in enumerate(counts[s]):
            if n == 0:
                continue
            pool = cr[mi == m]
            if exclude is not None:
                pool = np.array([p for p in pool if (s, int(p)) not in exclude], dtype=int)
            pick = rng.choice(pool, size=n, replace=False)
            for p in sorted(pick, key=lambda q: pt["tx"][q]):
                out.append((s, int(order[pt["i"][p]]), int(order[pt["j"][p]]), float(pt["tx"][p]), float(pt["lx"][p]),
                            int(p)))
    return out


def phase(a, b):
    return "CLB" if b > a else ("DES" if b < a else "CRZ")


def loss_rows(f, t, events, atm, rng):
    rows = []
    for s, i, j, tx, lx, _ in events:
        # the two aircraft named with the one that was changing level first where only one was
        ai, bi, aj, bj = t["a"][i], t["b"][i], t["a"][j], t["b"][j]
        if ai == bi and aj != bj:
            i, j = j, i
        vs = int(rng.integers(1, 9)) * 100
        lvl = 100 * lx
        l1 = int(round((lvl + vs / 2) / 100.0)) * 100 if rng.random() < 0.5 else int(round((lvl - vs / 2) / 100.0)) * 100
        l2 = l1 - vs if l1 > lvl else l1 + vs
        hor = round(float(rng.uniform(1.6, 4.9)), 1)
        if atm:
            sev = "B" if rng.random() < 0.16 else "C"
            contrib = "D" if rng.random() < 0.68 else "I"
            rep = "ATC" if rng.random() < 0.8 else "STCA"
        else:
            sev = "C" if rng.random() < 0.8 else "B"
            contrib = "N"
            rep = "ATC"
        rows.append(dict(sec=s, tx=tx, type="SMI", cs1=f["callsign"][t["fi"][i]], cs2=f["callsign"][t["fi"][j]],
                         lv1=l1, lv2=l2, ph1=phase(t["a"][i], t["b"][i]), ph2=phase(t["a"][j], t["b"][j]),
                         hor=hor, ver=abs(l1 - l2), sev=sev, contrib=contrib, rep=rep))
    return rows


def ra_rows(f, t, pairs, rng, used):
    """ACAS resolution advisory encounters and their reports. Encounters arise at pairs that changed order and at
    close pairs (within 900 ft at the nearest) where one aircraft was changing level; one or both crews report. The
    record also holds an encounter in the two hours either side of each summer's local edges (the night of 31 May and
    of 31 August, UTC), as any season's night traffic can."""
    def when(s, p):
        order, pt = pairs[s]
        if pt["cross"][p]:
            return float(pt["tx"][p])
        return float(pt["lo"][p] if abs(pt["dlo"][p]) < abs(pt["dhi"][p]) else pt["hi"][p])

    def level_at(s, p, tx):
        order, pt = pairs[s]
        i = order[pt["i"][p]]
        if pt["cross"][p]:
            return float(pt["lx"][p])
        return float(X.level(t["a"][i], t["b"][i], t["t0"][i], t["t1"][i], tx))

    enc = []
    cands = {}
    for s, (order, pt) in pairs.items():
        cand = np.nonzero(pt["moving"] & ((pt["cross"]) | (pt["gap"] < 9)))[0]
        cand = np.array([c for c in cand if (s, int(c)) not in used], dtype=int)
        cands[s] = cand
        n = rng.poisson(W.LAMBDA_RA * len(cand))
        for p in rng.choice(cand, size=n, replace=False):
            enc.append((s, int(p)))
    for y in (2025, 2026):
        taken = set()
        for edge in W.season(y):
            lo, hi = T.secs(edge), T.secs(edge) + 2 * 3600
            have = [s for s, p in enc if lo <= when(s, p) < hi]
            if have:
                taken.update(have)
                continue
            pool = [(s, int(p)) for s in range(8) if s not in taken for p in cands[s] if lo <= when(s, int(p)) < hi]
            pool = [x for x in pool if x not in set(enc)]
            if pool:
                pick = pool[int(rng.integers(len(pool)))]
                enc.append(pick)
                taken.add(pick[0])
    full = []
    for s, p in enc:
        order, pt = pairs[s]
        tx = when(s, p)
        full.append((s, int(order[pt["i"][p]]), int(order[pt["j"][p]]), tx, level_at(s, p, tx)))
    full.sort(key=lambda e: (e[3], e[0]))
    rows = []
    for e_no, (s, i, j, tx, lx) in enumerate(full):
        both = rng.random() < 0.46
        who = [i, j] if both else ([i] if rng.random() < 0.5 else [j])
        for k, me in enumerate(who):
            other = j if me == i else i
            jitter = int(rng.integers(-2, 3)) * 60 if k else 0
            vs = int(rng.integers(3, 10)) * 100
            hor = round(float(rng.uniform(0.6, 3.8)), 1)
            l1 = int(round(lx)) * 100 + int(rng.integers(-3, 4)) * 100
            rows.append(dict(sec=s, tx=tx + jitter, type="ACAS RA", cs1=f["callsign"][t["fi"][me]],
                             cs2=f["callsign"][t["fi"][other]], lv1=l1, lv2=l1 + (vs if rng.random() < 0.5 else -vs),
                             ph1=phase(t["a"][me], t["b"][me]), ph2=phase(t["a"][other], t["b"][other]), hor=hor,
                             ver=vs, sev="E" if rng.random() < 0.7 else "C", contrib="N" if rng.random() < 0.75 else "I",
                             rep="Flight crew", enc=e_no))
    return rows, full


OTHER = [("LB", 4.0), ("PLOC", 6.0), ("DEV", 3.0), ("ATMT", 1.6), ("AI", 0.6), ("WTE", 0.8)]


def other_rows(f, t, rng):
    rows = []
    lo, hi = T.secs(W.ACTUAL_START), T.secs(W.ACTUAL_END)
    n_months = 21
    for typ, per_month in OTHER:
        n = rng.poisson(per_month * n_months)
        for _ in range(n):
            k = int(rng.integers(len(t["t0"])))
            if typ == "LB":
                while t["a"][k] == t["b"][k]:
                    k = int(rng.integers(len(t["t0"])))
            tx = float(rng.uniform(t["t0"][k], t["t1"][k]))
            if not lo <= tx < hi:
                continue
            lv = 100 * int(round(X.level(t["a"][k], t["b"][k], t["t0"][k], t["t1"][k], tx)))
            row = dict(sec=int(t["sec"][k]), tx=tx, type=typ, cs1=f["callsign"][t["fi"][k]], cs2="", lv1=lv, lv2=None,
                       ph1=phase(t["a"][k], t["b"][k]), ph2="", hor=None, ver=None,
                       sev="E" if rng.random() < 0.6 else ("C" if rng.random() < 0.85 else "D"),
                       contrib="N" if rng.random() < 0.7 else ("I" if rng.random() < 0.6 else "D"),
                       rep="ATC" if typ != "WTE" else "Flight crew")
            if typ == "ATMT":
                row.update(cs1="", lv1=None, ph1="", contrib="D" if rng.random() < 0.5 else "I", rep="Engineering")
            rows.append(row)
    return rows
