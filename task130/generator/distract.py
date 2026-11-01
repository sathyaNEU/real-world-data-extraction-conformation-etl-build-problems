"""Two files the solution never reads that look worth weighing: the crews' good-catch (near-miss) reports and the
subcontractors' monthly safety returns. The good catches are the field leadership programme's raw material; the
subcontractors fall outside CS-4's measures (section 2)."""
import csv
import datetime as dt
import hashlib
import os

import numpy as np

import pack as P
import world as W

CATS = ["Hazard observed", "Equipment defect", "Traffic control", "Public contact", "Near miss", "Housekeeping",
        "Energised equipment", "Wildlife"]
SUBS = [("Tallow Creek Tree Service", 61000), ("Harbison Boring Inc", 38500), ("Ridgeway Traffic Control", 22800),
        ("Briarwood Excavating", 30500), ("Delmar Pole Testing", 12400), ("Sweetgum Hydro-Vac", 9800)]


def _rng(*keys):
    h = hashlib.blake2b(("|".join(str(k) for k in (W.SEED, "distract") + keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "little"))


def write_good_catch(S, target):
    rng = _rng("gc")
    rows = []
    start = dt.date(2025, 1, 6)
    for c in S["crews"]:
        rate = 0.018 * (1.3 if c["type"] in ("OH", "VEG") else 1.0)
        d = start
        while d <= W.HIST1:
            if d.weekday() < 5 and rng.random() < rate:
                code = P.sim.crew_code(c, d)
                rows.append([d.isoformat(), code, P.sim.crew_district(c, d), CATS[int(rng.integers(len(CATS)))],
                             "Closed" if rng.random() < 0.9 else "Open"])
            d += dt.timedelta(days=1)
    rows.sort()
    for n, r in enumerate(rows, 1):
        r.insert(0, "GC-%05d" % (n * 3 + 1000))
    with open(os.path.join(target, P.FILES["nearmiss"]), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["report_no", "report_date", "crew_code", "district", "category", "status"])
        w.writerows(rows)
    return len(rows)


def write_subs(target):
    rng = _rng("subs")
    rows = []
    for name, base in SUBS:
        for m in range(1, 10):
            h = int(base * float(rng.normal(1.0, 0.08)) / 12)
            rec = int(rng.poisson(h * 3.1 / 200000))
            rows.append([name, "2026-%02d" % m, h, rec, int(rng.poisson(rec * 0.3))])
    with open(os.path.join(target, P.FILES["subs"]), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["subcontractor", "month", "hours_reported", "recordable_cases", "days_away_cases"])
        w.writerows(rows)
    return len(rows)
