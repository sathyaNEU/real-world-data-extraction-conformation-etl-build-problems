"""The world before any record is written: births by attendance area, every pupil's October count history, and the
fall 2026 schedule and preschool rolls the asks read. Nothing here ships; records.py and asks.py write the exports.

The truth (seed-searched, see the design note's Ladder): between one October count and the next a pupil in grades K to
4 leaves the district at a rate set by the school it leaves, moves to another attendance area at a rate set by the
school it leaves, repeats the grade, or promotes; pupils arrive from outside the district into grades 1 to 5 at a
steady count per school and grade (year effects for the housing market); kindergartners enter at a stable share of
the area's births five years earlier. The random streams are the seed search's own, so the realised history is the
one the search measured."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

Z = K.ZONES
NZ = len(Z)
IX = {z: i for i, z in enumerate(Z)}
G = 6
BIRTH_Y0 = 1999


class World:
    pass


def simulate():
    W = World()
    par = K.PAR
    seed = K.SEED
    # births by area (the seed search's stream)
    rb = np.random.default_rng([seed, 1])
    W.births = {z: {y: int(rb.poisson(K.lin(par["births"][z], y))) for y in range(BIRTH_Y0, 2026)} for z in Z}
    M = np.zeros((NZ, NZ))
    for k, v in par["moves"].items():
        a, b = k.split(">")
        M[IX[a], IX[b]] = v
    W.M = M
    out, ext, kr, ret = par["out"], par["ext"], par["kratio"], par["retain"]
    yr = par["yr_eff"]
    ns = float(par["noise"])
    W.snap = {}
    nid = [100000]

    def new_id():
        nid[0] += 1
        return nid[0]

    cur = []
    for y in range(2004, 2027):
        r = np.random.default_rng([seed, 2, y])
        nxt = []
        if cur:
            groups = {}
            for (pid, s, g) in cur:
                if g == G - 1:
                    continue
                groups.setdefault((s, g), []).append(pid)
            for (s, g) in sorted(groups):
                pids = groups[(s, g)]
                n = len(pids)
                probs = [out[Z[s]]] + [M[s, j] for j in range(NZ)] + [ret[g]]
                probs[1 + s] = 0.0
                probs.append(1.0 - sum(probs))
                probs = np.array(probs)
                d0 = r.multinomial(n, probs)
                d = np.floor(n * probs + ns * (d0 - n * probs) + r.random(len(probs))).astype(int)
                d = np.maximum(d, 0)
                d[-1] += n - d.sum()
                if d[-1] < 0:
                    d[0] += d[-1]
                    d[-1] = 0
                perm = r.permutation(n)
                k = 0
                for c, cnt in enumerate(d):
                    for _ in range(int(cnt)):
                        pid = pids[perm[k]]
                        k += 1
                        if c == 0:
                            pass
                        elif 1 <= c <= NZ:
                            nxt.append([pid, c - 1, g + 1])
                        elif c == NZ + 1:
                            nxt.append([pid, s, g])
                        else:
                            nxt.append([pid, s, g + 1])
        for i, z in enumerate(Z):
            b = W.births[z][y - 5]
            kk = kr[z]
            n = r.binomial(b, kk) if kk <= 1 else b + r.binomial(b, kk - 1)
            for _ in range(int(n)):
                nxt.append([new_id(), i, 0])
        if cur:
            f = yr.get(y, 1.0)
            for i, z in enumerate(Z):
                for g in range(1, G):
                    lam = ext[z] * f
                    c = max(0, int(np.floor(lam + ns * (r.poisson(lam) - lam) + r.random())))
                    for _ in range(int(c)):
                        nxt.append([new_id(), i, g])
        cur = nxt
        W.snap[y] = [tuple(x) for x in cur]
    W.counts = {y: counts(W.snap[y]) for y in W.snap}
    attributes(W)
    return W


def counts(rows):
    E = np.zeros((NZ, G))
    for (_, s, g) in rows:
        E[s, g] += 1
    return E


# ---------------------------------------------------------------------------------------------------- pupil attributes
def _uniform_date(r, lo, hi):
    span = (hi - lo).days
    return lo + dt.timedelta(days=int(r.integers(0, span + 1)))


def _school_day_between(r, lo, hi):
    """A weekday between lo and hi inclusive."""
    for _ in range(50):
        d = _uniform_date(r, lo, hi)
        if d.weekday() < 5:
            return d
    return lo


def attributes(W):
    """Birth dates, sexes, state IDs, legacy numbers, entry dates and codes, program flags. Each from its own stream
    keyed by the pupil, so nothing here touches the flows."""
    first_seen = {}
    years = sorted(W.snap)
    prev = {}
    W.spell = {}          # (pid, year) -> (entry_date, new_code, old_code)
    W.info = {}           # pid -> dict
    ids = set()
    rid = K.rng("state_ids")
    for y in years:
        now = {pid: (s, g) for (pid, s, g) in W.snap[y]}
        for pid, (s, g) in now.items():
            if pid not in W.info:
                r = K.rng("pupil", pid)
                if g == 0:
                    lo, hi = dt.date(y - 6, 10, 2), dt.date(y - 5, 10, 1)
                else:
                    lo, hi = dt.date(y - 6 - g, 10, 2), dt.date(y - 5 - g, 10, 1)
                    if r.random() < 0.02:
                        lo, hi = dt.date(y - 7 - g, 10, 2), dt.date(y - 6 - g, 10, 1)
                bd = _uniform_date(r, lo, hi)
                u = r.random()
                sex = "F" if u < 0.488 else "M"
                if y >= 2021 and r.random() < 0.0015:
                    sex = "X"
                while True:
                    sid = "%010d" % int(rid.integers(1300000000, 1899999999))
                    if sid not in ids:
                        ids.add(sid)
                        break
                z = Z[s]
                ell_p = {"A": 0.20, "B": 0.07, "P": 0.27, "C": 0.08, "D": 0.09, "E": 0.10, "F": 0.05}[z]
                W.info[pid] = dict(birth=bd, sex=sex, sid=sid, first_year=y, first_grade=g, first_school=s,
                                   ell0=r.random() < ell_p, ell_exit=int(r.integers(2, 7)),
                                   iep=r.random() < (0.085 + 0.012 * g), iep_from=y + int(r.integers(0, 3)),
                                   newcode=None)
            info = W.info[pid]
            r = K.rng("spell", pid, y)
            if pid not in prev:
                # a new enrollment: kindergarten entry or an arrival from outside the district
                if g == 0 and y == info["first_year"]:
                    ed = K.FIRST_DAY[y] if r.random() < 0.86 else _school_day_between(
                        r, K.FIRST_DAY[y] + dt.timedelta(days=1), K.count_day(y) - dt.timedelta(days=3))
                    code, old = "01", "E1"
                else:
                    u = r.random()
                    if u < 0.55:
                        ed = K.FIRST_DAY[y]
                    elif u < 0.80:
                        ed = _school_day_between(r, K.FIRST_DAY[y] + dt.timedelta(days=1), K.count_day(y) - dt.timedelta(days=3))
                    else:
                        ed = _school_day_between(r, K.count_day(y - 1) + dt.timedelta(days=3),
                                                 dt.date(y, 5, 20))
                    v = r.random()
                    code = "02" if v < 0.46 else ("03" if v < 0.76 else ("04" if v < 0.89 else "05"))
                    old = "E1"
                W.spell[(pid, y)] = (ed, code, old)
            else:
                ps, pg = prev[pid]
                if ps != s:
                    u = r.random()
                    if u < 0.56:
                        ed = K.FIRST_DAY[y]
                    else:
                        ed = _school_day_between(r, K.count_day(y - 1) + dt.timedelta(days=3),
                                                 dt.date(y, 5, 20))
                    W.spell[(pid, y)] = (ed, "06", "E2")
                else:
                    W.spell[(pid, y)] = W.spell[(pid, y - 1)]
        prev = now
    # legacy local numbers: every pupil on a legacy October roll, numbered in order of first legacy appearance
    rl = K.rng("local_numbers")
    nums = sorted(rl.choice(np.arange(200000, 699999), size=40000, replace=False).tolist())
    W.local = {}
    k = 0
    for y in years:
        if y > 2018:
            break
        for (pid, s, g) in sorted(W.snap[y], key=lambda t: (W.info[t[0]]["first_year"], t[0])):
            if pid not in W.local:
                W.local[pid] = str(nums[k])
                k += 1
    # legacy rows whose state ID had not come back from the state's ID system by the count day (new pupils only)
    W.sid_blank = set()
    rb = K.rng("sid_blank")
    for y in K.OLD_YEARS:
        for (pid, s, g) in W.snap[y]:
            if W.info[pid]["first_year"] == y and rb.random() < 0.035:
                W.sid_blank.add((pid, y))


def ell_on(W, pid, y):
    i = W.info[pid]
    return bool(i["ell0"]) and (y - i["first_year"]) < i["ell_exit"]


def iep_on(W, pid, y):
    i = W.info[pid]
    return bool(i["iep"]) and y >= i["iep_from"]
