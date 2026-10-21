"""The world of task482 (architecture 2): Statistics Ardmuir's business register, fourteen regional registers, the
register's automated risk screen and the summer 2026 quality audit, which drew records the screen flagged at fifteen in
a hundred and the rest at two and a half in a hundred.

A flagged record is in error far more often than an unflagged one, so a region's audited share in error is weighted
toward its flagged records; the register's own rate weighs each audited record by the records of its stratum it
stands for.

    x = build()    the truth: regions, records, flags, errors, the audit draw, the dissolutions"""
import datetime as dt

import numpy as np

SEED = 4822
RATE = {"F": 0.24, "U": 0.04}        # the audit's sampling fractions by the screen's flag
LINE = 0.04

# region code, name, records, share flagged, error rate of flagged, error rate of unflagged (set from
# the side), the side of the line the
# register's rate is drawn to (o over, u under, c clean: under, and under on the audited share too)
REGIONS = [
    ("AR01", "Ardmuir City", 21800, 0.071, 0.214, 0.0335, "o"),
    ("AR02", "Bannock Coast", 9400, 0.118, 0.236, 0.0141, "u"),
    ("AR03", "Carrick Vale", 7600, 0.052, 0.110, 0.0120, "c"),
    ("AR04", "Dunlay", 12300, 0.094, 0.251, 0.0157, "u"),
    ("AR05", "Eskmoor", 5200, 0.137, 0.188, 0.0313, "o"),
    ("AR06", "Fallowmere", 8800, 0.083, 0.229, 0.0182, "u"),
    ("AR07", "Glenquhar", 6100, 0.104, 0.243, 0.0154, "u"),
    ("AR08", "Harlaw", 14700, 0.066, 0.207, 0.0372, "o"),
    ("AR09", "Inverbeck", 4600, 0.048, 0.104, 0.0110, "c"),
    ("AR10", "Kelso Moss", 10200, 0.089, 0.236, 0.0168, "u"),
    ("AR11", "Lenwick", 7100, 0.112, 0.214, 0.0329, "o"),
    ("AR12", "Mossgiel", 9900, 0.059, 0.217, 0.0381, "o"),
    ("AR13", "Northmuir", 11500, 0.097, 0.205, 0.0149, "u"),
    ("AR14", "Strathlorn", 6700, 0.045, 0.098, 0.0125, "c"),
]
IDS = [r[0] for r in REGIONS]
FORMS = ["private limited company", "sole trader", "partnership", "limited liability partnership",
         "public limited company", "community interest company"]


def build():
    rng = np.random.default_rng(SEED)
    recs = []
    k = 0
    for code, name, n, f, ef, eu, side in REGIONS:
        target = {"o": 0.052, "u": 0.030, "c": 0.015}[side] + float(rng.uniform(-0.003, 0.003))
        eu = (target - f * ef) / (1 - f)
        age = rng.integers(0, 9000, n)
        created = np.array([dt.date(2026, 9, 30) - dt.timedelta(days=int(a)) for a in age])
        frame = created <= dt.date(2026, 4, 30)
        fl = (rng.random(n) < f) & frame
        for _ in range(60):
            err = np.where(fl, rng.random(n) < ef, rng.random(n) < eu)
            drawn = np.where(fl, rng.random(n) < RATE["F"], rng.random(n) < RATE["U"]) & frame
            ht, naive, true = _estimates(fl[frame], err[frame], drawn[frame])
            far = min(abs(ht - LINE), abs(true - LINE)) >= 0.005 and abs(naive - LINE) >= 0.005
            ok = (ht > LINE and true > LINE) if side == "o" else (ht < LINE and true < LINE)
            ok = ok and (naive < LINE if side == "c" else naive > LINE)
            if far and ok:
                break
        else:
            raise SystemExit("region %s not placed" % code)
        for i in range(n):
            k += 1
            recs.append({"k": k, "region": code, "flag": bool(fl[i]), "err": bool(err[i]), "drawn": bool(drawn[i]),
                         "created": created[i], "frame": bool(frame[i]), "form": FORMS[int(rng.choice(6, p=[0.52, 0.27, 0.09, 0.05, 0.02,
                                                                                    0.05]))],
                         "employees": int(rng.choice([0, 1, 2, 5, 10, 25, 50, 100], p=[0.3, 0.25, 0.15, 0.12, 0.08,
                                                                                         0.05, 0.03, 0.02]))})
    x = {"recs": recs}
    _q3(x, rng)
    _dissolutions(x, rng)
    return x


def _estimates(fl, err, drawn):
    N = {g: int((fl == g).sum()) for g in (True, False)}
    est = 0.0
    for g in (True, False):
        m = drawn & (fl == g)
        est += N[g] * err[m].sum() / m.sum()
    return est / len(fl), err[drawn].sum() / drawn.sum(), err.mean()


def truth_rates(x):
    out = {}
    for code in IDS:
        rs = [r for r in x["recs"] if r["region"] == code and r["frame"]]
        out[code] = sum(r["err"] for r in rs) / len(rs)
    return out


def _q3(x, rng):
    """Each record's creation time in Ardmuir local time; registrations filed online in the hour after local midnight
    at the quarter's edges, which British Summer Time puts on the previous day in UTC."""
    edge = (dt.date(2026, 7, 1), dt.date(2026, 10, 1))
    for r in x["recs"]:
        c = r["created"]
        r["created_local"] = dt.datetime(c.year, c.month, c.day) + dt.timedelta(seconds=int(rng.integers(7 * 3600,
                                                                                                         19 * 3600)))
    for code in IDS:
        rs = [r for r in x["recs"] if r["region"] == code and edge[0] <= r["created"] < edge[1]]
        for j in rng.permutation(len(rs))[:int(rng.integers(2, 5))]:
            rs[j]["created"] = edge[0]
            rs[j]["created_local"] = dt.datetime(2026, 7, 1) + dt.timedelta(minutes=int(rng.integers(2, 58)))
    x["q3"] = {code: sum(1 for r in x["recs"] if r["region"] == code and
                         dt.datetime(2026, 7, 1) <= r["created_local"] < dt.datetime(2026, 10, 1)) for code in IDS}


def _dissolutions(x, rng):
    """Businesses dissolved in the third quarter of 2026, two to four per cent a region."""
    x["diss"] = {}
    for code in IDS:
        rs = [r for r in x["recs"] if r["region"] == code and r["created"] < dt.date(2026, 1, 1)]
        pick = rng.permutation(len(rs))[:int(len(rs) * float(rng.uniform(0.006, 0.012)))]
        for j in pick:
            rs[j]["dissolved"] = dt.date(2026, 7, 1) + dt.timedelta(days=int(rng.integers(0, 92)))
        x["diss"][code] = len(pick)
