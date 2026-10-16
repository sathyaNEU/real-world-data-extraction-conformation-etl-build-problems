"""The processes behind the record: what the water did, and what each method could see of it."""
import datetime as dt
import math
import random

import world as W


def _lognorm(rng, s):
    return math.exp(rng.gauss(0.0, s))


def point_calendar(code):
    """the months the programme requires a pesticide sample at this point"""
    out = []
    for (y, m) in W.MONTHS:
        d = dt.date(y, m, 1)
        if code in W.POINT_FROM and d < W.POINT_FROM[code]:
            continue
        if code in W.POINT_TO and d > W.POINT_TO[code]:
            continue
        if (code, y, m) in [(c, yy, mm) for (c, yy, mm) in W.MISSED]:
            continue
        out.append((y, m))
    return out


def mcpa_grid(wb, base):
    """the true MCPA concentration at every point and month, in the generator's own order.

    The draw order is fixed: one fresh stream per water body, points in register order, months in
    calendar order, so the record is reproducible and the calendar's gaps remove rows without
    moving any value that stays.
    """
    name, code, old, catch, area, target, points = wb
    rng = random.Random(W.SEED)
    rows = []
    for (suffix, lab, pf, place) in points:
        pcode = "ARW-" + suffix
        for (y, m) in W.MONTHS:
            true = base * pf * W.SEASON[m] * _lognorm(rng, 0.26)
            rows.append({"point": pcode, "lab": lab, "place": place, "year": y, "month": m,
                         "true": true})
    cal = {}
    for (suffix, lab, pf, place) in points:
        cal["ARW-" + suffix] = set(point_calendar("ARW-" + suffix))
    return [r for r in rows if (r["year"], r["month"]) in cal[r["point"]]]


def solve_base(wb):
    """the water body's pressure, set so its true annual mean over the required samples is the target"""
    target = wb[5]
    lo, hi = 1e-6, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        rows = mcpa_grid(wb, mid)
        mean = sum(r["true"] for r in rows) / len(rows)
        if mean < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def mcpa_rows(wb):
    base = solve_base(wb)
    rows = mcpa_grid(wb, base)
    for r in rows:
        rl = W.METHODS["TAS-LC-PHX-04"]["rl"] if r["lab"] == "TAS" else W.METHODS["KGL-GC-PHX-07"]["rl"]
        r["rl"] = rl
        r["det"] = r["true"] >= rl
        r["base"] = base
    return rows


def tuples(rows):
    return [(r["year"], r["month"], (r["true"] if r["det"] else r["rl"]), r["rl"], r["det"]) for r in rows]


def sample_day(rng, y, m, point):
    """the authority samples each point once a month on a settled round, never on the boundary"""
    start = 6 + (sum(ord(c) for c in point) % 5)
    return dt.date(y, m, start + rng.randrange(0, 4))
