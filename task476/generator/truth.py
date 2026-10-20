"""The truth every shipped file is cut from: the main segments, each segment's yearly survey dates, and every leak on
a cast-iron or bare-steel main from 2015 to 2026 with its true start, how it was found (an odor report within days of
the start, or the segment's next survey), its grade and its repair."""
import calendar
import datetime as dt

import numpy as np

import world as W


def rng_for(*key):
    s = "|".join(str(k) for k in (W.SEED,) + key)
    h = 0
    for ch in s:
        h = (h * 1000003 + ord(ch)) % (2 ** 63)
    return np.random.default_rng(h)


class Segment:
    __slots__ = ("sid", "district", "material", "miles", "day", "surveys", "street", "abandoned")


class Leak:
    __slots__ = ("lid", "seg", "start", "found", "how", "grade", "repaired", "visits", "addr", "report_time")


MATS = (("CI", 1), ("BS", 2), ("CS", 3), ("PL", 4))


def segments():
    out = []
    n = 0
    for d, k in W.DISTRICTS.items():
        rng = rng_for("seg", d)
        month = k[0]
        for mat, idx in MATS:
            total = k[idx]
            left = total
            while left > 0.02:
                L = min(left, round(float(rng.uniform(0.06, 0.42)), 3))
                left -= L
                n += 1
                s = Segment()
                s.sid = "M%06d" % (100000 + n * 3 + int(rng.integers(0, 3)))
                s.district, s.material, s.miles = d, mat, round(L, 3)
                s.day = int(rng.integers(2, 27))
                s.street = int(rng.integers(0, 60))
                s.abandoned = None
                s.surveys = {}
                for y in range(2015, W.YEAR + 1):
                    last = calendar.monthrange(y, month)[1]
                    day = min(last, max(1, s.day + int(rng.integers(-2, 3))))
                    s.surveys[y] = dt.date(y, month, day)
                out.append(s)
    return out


def _day_weights(start, stop, season):
    """Daily start density over [start, stop): each day the month's share over the month's days."""
    days = (stop - start).days
    w = np.empty(days)
    for i in range(days):
        t = start + dt.timedelta(days=i)
        w[i] = season[t.month - 1] / calendar.monthrange(t.year, t.month)[1]
    return w


LAM_MAX = 2.6
WDAY = None


def leaks(segs):
    global WDAY
    if WDAY is None:
        w = _day_weights(dt.date(2015, 1, 1), dt.date(W.YEAR + 1, 1, 1), W.SEASON)
        WDAY = w / w.sum()
    out = []
    n = 0
    t0, t1 = dt.date(2015, 1, 1), dt.date(W.YEAR, 12, 31)
    for s in segs:
        if s.material not in ("CI", "BS"):
            continue
        k = W.DISTRICTS[s.district]
        rng = rng_for("leaks", s.sid)
        lam = k[5] * s.miles * (1.12 if s.material == "CI" else 0.85)
        lam_max = LAM_MAX * s.miles * (1.12 if s.material == "CI" else 0.85)
        years = (t1 - t0).days / 365.25
        count = int(rng.poisson(lam_max * years))
        if not count:
            continue
        days = rng.choice(len(WDAY), size=count, p=WDAY)
        keep = rng.random(count) < lam / lam_max       # thinning: a rate change adds or drops leaks, never redraws
        for dd in sorted(int(x) for x, k_ in zip(days, keep) if k_):
            rng = rng_for("leak", s.sid, dd)
            n += 1
            L = Leak()
            L.lid = None
            L.seg = s
            L.start = dt.datetime.combine(t0 + dt.timedelta(days=int(dd)), dt.time(int(rng.integers(0, 24)),
                                                                                    int(rng.integers(0, 60))))
            if rng.random() < k[6]:
                lag = float(rng.exponential(1.6)) + 0.1
                L.found = L.start + dt.timedelta(days=lag)
                L.how = "ODOR"
                L.grade = int(rng.choice([1, 2, 3], p=[0.36, 0.46, 0.18]))
            else:
                d0 = L.start.date()
                y = d0.year
                sv = s.surveys.get(y)
                if sv is None or sv <= d0:
                    sv = s.surveys.get(y + 1)
                if sv is None:
                    continue
                L.found = dt.datetime.combine(sv, dt.time(int(rng.integers(8, 16)), int(rng.integers(0, 60))))
                L.how = "SURVEY"
                L.grade = int(rng.choice([1, 2, 3], p=W.GRADE_P))
            if L.found.date() > W.END:
                continue
            fd = L.found
            if L.grade == 1:
                L.repaired = fd + dt.timedelta(hours=float(rng.uniform(2, 20)))
            elif L.grade == 2:
                L.repaired = fd + dt.timedelta(days=float(rng.exponential(k[7])) + 3)
            else:
                if rng.random() < k[8]:
                    L.repaired = fd + dt.timedelta(days=float(rng.uniform(20, 365)))
                else:
                    L.repaired = fd + dt.timedelta(days=float(rng.uniform(380, 1500)))
            L.repaired = L.repaired.replace(second=0, microsecond=0)
            out.append(L)
    out.sort(key=lambda L: (L.found, L.seg.sid))
    for i, L in enumerate(out):
        L.lid = "L%02d-%05d" % (L.found.year % 100, i + 1)
    return out
