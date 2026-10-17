"""The clean truth for task265: every primary total hip done at Brennick Valley Health's three hospitals from 2005 to
2026, its patient, its first revision, the patient's death or move out of Wisconsin, which earlier hips the registry
enrolled at its 2018 to 2021 clinics and which later operations it captured. The registry's view, the rungs of the
ladder and the 2026 operating-room record are all computed from this, never the other way round."""
import datetime as dt

import numpy as np

import common as K

SEED = 6543
P = {
    "attend": 0.55,          # share of earlier hips' patients who came to a registry clinic from 2018 to 2021
    "capture": 0.975,        # share of operations from 2018 the registry captured
    "second": 0.11,          # patients who have the other hip replaced later
    "same_day": 0.12,        # of those, both hips in one operation
    "move": 0.006,           # moves out of Wisconsin a year
    "mort_a": 0.0065, "mort_b": 0.088,
}
# annual revision hazard by years since the operation: [0,1), [1,3), [3,8), [8, on)
HAZ = {
    "TA": (0.0240, 0.0080, 0.0033, 0.0046),
    "TS": (0.0220, 0.0074, 0.0031, 0.0042),
    "MF": (0.0110, 0.0030, 0.0024, 0.0030),
    "VS": (0.0125, 0.0038, 0.0025, 0.0031),
    "MS": (0.0128, 0.0040, 0.0027, 0.0034),
    "BP": (0.0225, 0.0078, 0.0052, 0.0061),
    "MC": (0.0120, 0.0040, 0.0035, 0.0045),
    "TI": (0.0180, 0.0060, 0.0040, 0.0050),
}
EDGES = (0.0, 1.0, 3.0, 8.0)


def volume(c, y):
    """First hips a year for each construct (second hips come on top)."""
    if c == "TA":
        return 150 if y < 2015 else (112 if y < 2018 else 62)
    if c == "TS":
        return 0 if y < 2008 else (122 if y < 2018 else 66)
    if c == "MF":
        return 150 if y < 2018 else 140
    if c == "VS":
        return 55 if y < 2012 else (135 if y < 2018 else 290)
    if c == "MS":
        return 0 if y < 2011 else (82 if y < 2018 else 205)
    if c == "BP":
        return 0 if y < 2010 else (72 if y < 2018 else 132)
    if c == "MC":
        return 60 if y < 2012 else 0
    if c == "TI":
        return 45 if y < 2010 else 0
    raise KeyError(c)


# share of each construct's hips at each hospital
MIX = {"TA": (0.30, 0.58, 0.12), "TS": (0.18, 0.07, 0.75), "MF": (0.50, 0.30, 0.20), "VS": (0.35, 0.15, 0.50),
       "MS": (0.40, 0.20, 0.40), "BP": (0.35, 0.20, 0.45), "MC": (0.55, 0.30, 0.15), "TI": (0.25, 0.60, 0.15)}


def revision_time(rng, c):
    h = HAZ[c]
    u = -np.log(rng.random())
    cum = 0.0
    for i, a in enumerate(EDGES):
        b = EDGES[i + 1] if i + 1 < len(EDGES) else None
        span = (b - a) if b is not None else None
        if span is None or u < cum + h[i] * span:
            return a + (u - cum) / h[i]
        cum += h[i] * span


def death_time(rng, age):
    a, b = P["mort_a"], P["mort_b"]
    e = -np.log(rng.random())
    return np.log(1 + e * b / (a * np.exp(b * (age - 60)))) / b


def construct_at(rng, d):
    y = d.year
    w = np.array([volume(c, y) for c in K.CODES + ["MC", "TI"]], float)
    return (K.CODES + ["MC", "TI"])[rng.choice(len(w), p=w / w.sum())]


def clinic_day(rng, hosp):
    a, b = K.CLINIC[hosp]
    while True:
        d = a + dt.timedelta(days=int(rng.integers(0, (b - a).days + 1)))
        if d.weekday() < 5 and not (K.PAUSE[0] <= d <= K.PAUSE[1]):
            return d


def world(seed=SEED):
    rng = np.random.default_rng(seed)
    patients, hips = [], []
    pid = 0

    def add_hip(p, c, hosp, op, side):
        t_rev = revision_time(rng, c)
        h = dict(hip=len(hips), patient=p["patient"], construct=c, hospital=hosp, op=op, side=side,
                 rev=op + dt.timedelta(days=int(round(t_rev * K.YEAR))), rerev=None,
                 rev_where="system" if rng.random() < 0.86 else "other", age=p["age0"] + (op - p["op0"]).days / K.YEAR)
        if rng.random() < 0.14:
            h["rerev"] = h["rev"] + dt.timedelta(days=int(rng.integers(60, 1500)))
        hips.append(h)
        p["hips"].append(h["hip"])
        return h

    for c in K.CODES + ["MC", "TI"]:
        for y in range(2005, 2027):
            n = rng.poisson(volume(c, y))
            for _ in range(n):
                op = dt.date(y, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
                while op.weekday() >= 5:
                    op -= dt.timedelta(days=1)
                if op.year != y:
                    op = dt.date(y, 1, 2)
                hosp = K.HOSP[rng.choice(3, p=MIX[c])]
                age = float(np.clip(rng.normal(67.0, 9.5), 38, 92))
                p = dict(patient=pid, age0=age, op0=op, sex="F" if rng.random() < 0.58 else "M", hips=[])
                pid += 1
                p["death"] = op + dt.timedelta(days=int(round(death_time(rng, age) * K.YEAR)))
                p["moved"] = op + dt.timedelta(days=int(round(rng.exponential(1 / P["move"]) * K.YEAR)))
                patients.append(p)
                side = "R" if rng.random() < 0.55 else "L"
                add_hip(p, c, hosp, op, side)
                if rng.random() < P["second"]:
                    other = "L" if side == "R" else "R"
                    if rng.random() < P["same_day"]:
                        op2 = op
                    else:
                        op2 = op + dt.timedelta(days=int(rng.integers(90, 2900)))
                        while op2.weekday() >= 5:
                            op2 += dt.timedelta(days=1)
                    if op2 <= K.EXTRACT and op2 < p["death"] and op2 < p["moved"] and \
                            op2 < hips[p["hips"][0]]["rev"] + dt.timedelta(days=36500):
                        c2 = c if (rng.random() < 0.72 and volume(c, op2.year) > 0) else construct_at(rng, op2)
                        add_hip(p, c2, hosp if rng.random() < 0.85 else K.HOSP[rng.integers(0, 3)], op2, other)
    # which earlier hips the registry enrolled, which later operations it captured
    for p in patients:
        legacy = [hips[i] for i in p["hips"] if hips[i]["op"] < K.REG_START]
        p["visit"] = None
        if legacy and rng.random() < P["attend"]:
            v = clinic_day(rng, legacy[0]["hospital"])
            if v < p["death"] and v < p["moved"]:
                p["visit"] = v
        for i in p["hips"]:
            h = hips[i]
            if h["op"] < K.REG_START:
                h["entry"] = p["visit"] if (p["visit"] and h["rev"] > p["visit"]) else None
            else:
                h["entry"] = h["op"] if rng.random() < P["capture"] else None
    return dict(patients=patients, hips=hips, rng=rng)


# ------------------------------------------------------------------------------------------------- the curves
def follow(T, h, death_rule="exact"):
    """(start, stop, event) in days since the operation for a hip on the registry."""
    p = T["patients"][h["patient"]]
    end = min(p["death"], p["moved"], K.EXTRACT)
    ev = h["rev"] <= end
    stop = h["rev"] if ev else end
    return (h["entry"] - h["op"]).days, (stop - h["op"]).days, ev


def km(rows, horizon=K.TEN, inclusive_entry=False):
    """Kaplan-Meier with delayed entry: rows of (entry, stop, event) in days; a hip is at risk at t when
    entry < t <= stop (entry <= t <= stop with inclusive_entry). Returns per cent revised by horizon."""
    a = np.array(rows, float)
    if len(a) == 0:
        return float("nan")
    e, s, d = a[:, 0], a[:, 1], a[:, 2].astype(bool)
    times = np.unique(s[d & (s <= horizon)])
    S = 1.0
    for t in times:
        at = ((e <= t) if inclusive_entry else (e < t)) & (s >= t)
        n = at.sum()
        k = (d & (s == t) & at).sum()
        if n:
            S *= 1 - k / n
    return 100 * (1 - S)


def rung_rows(T, c, rung, horizon=K.TEN):
    out = []
    for h in T["hips"]:
        if h["construct"] != c or h["entry"] is None:
            continue
        e, s, ev = follow(T, h)
        if rung == "op":
            e = 0
        elif rung == "reg" and h["op"] < K.REG_START:
            e = (K.REG_START - h["op"]).days
        elif rung == "prosp" and h["op"] < K.REG_START:
            continue
        out.append((e, s, ev))
    return out


def rungs(T):
    R = {}
    for c in K.CODES:
        R[c] = {}
        for r in ("golden", "op", "reg"):
            R[c][r] = km(rung_rows(T, c, r))
        rows = rung_rows(T, c, "golden")
        R[c]["crude"] = 100 * sum(1 for x in rows if x[2]) / len(rows)
        R[c]["n"] = len(rows)
        R[c]["legacy"] = sum(1 for h in T["hips"] if h["construct"] == c and h["entry"] is not None and
                             h["op"] < K.REG_START)
    return R


if __name__ == "__main__":
    import sys
    s = int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    T = world(s)
    R = rungs(T)
    for c in K.CODES:
        r = R[c]
        print("%-16s n=%5d legacy=%5d crude=%5.2f op=%5.2f reg=%5.2f golden=%5.2f" % (
            K.CNAME[c], r["n"], r["legacy"], r["crude"], r["op"], r["reg"], r["golden"]))
