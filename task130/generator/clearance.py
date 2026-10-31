"""C1 by construction for the complaint response ask: each 2026 district's median hours from first notice to the
inspector's arrival sits at least 0.03 hours from a one-decimal rounding edge. Where one does not, the arrival at the
investigation holding the median moves later by a minute or two (the same working day)."""
import datetime as dt
from collections import defaultdict

import world as W

MARGIN = 0.03


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def b_rows(R):
    """Each 2026 complaint investigation (new system) with its district, hours from first notice and visit index."""
    prem = {p["pid"]: p for p in R["premises"]}
    out = defaultdict(list)
    for i, v in enumerate(R["visits"]):
        if v["kind"] != "complaint" or v["day"].year != 2026:
            continue
        inc = R["incidents"][v["incident"]]
        start = dt.datetime.combine(v["day"], v["time"])
        shown = [t for t in inc["times"] if t <= start - dt.timedelta(minutes=20)]
        if not shown:
            continue
        d = prem[R["permits"][v["permit"]]["prem"]]["d26"]
        out[d].append(((start - shown[0]).total_seconds() / 3600.0, i))
    return out


def median_of(lst):
    s = sorted(lst)
    n = len(s)
    if n % 2:
        return s[n // 2][0], [s[n // 2][1]]
    return (s[n // 2 - 1][0] + s[n // 2][0]) / 2, [s[n // 2][1]]


def run(R):
    moved = []
    for _ in range(40):
        rows = b_rows(R)
        bad = []
        for d, lst in rows.items():
            m, who = median_of(lst)
            if edge(m, 0.1) < MARGIN:
                bad.append((d, who[0]))
        if not bad:
            return moved
        for d, i in bad:
            v = R["visits"][i]
            t = dt.datetime.combine(v["day"], v["time"]) + dt.timedelta(seconds=150)
            if t.date() != v["day"] or t.hour >= 17:
                t = dt.datetime.combine(v["day"], v["time"]) - dt.timedelta(seconds=150)
            v["time"] = t.time()
            moved.append((d, i))
    raise AssertionError("complaint response medians could not be cleared")
