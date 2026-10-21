"""The Harbourgate quarter's recorded offences, 2025 and 2026 seasons.

One row is one recorded offence. The classes the patrol contract covers are offences against something that
sits in the quarter all season (a shop front, a business premises, a flat above it, a vehicle in a long-stay
bay, a cycle in a store) and whose keeper looks at it on a routine. The force records the occurrence as the
gap in that routine the offence fell in, which is how a victim can vouch for it: the premises closed and
opened again, the vehicle left and returned to, the cycle locked and found gone. Victims give those times in
round clock hours, so both ends of a window sit on the hour. An offence that falls in a watched hour is seen
at the time, so it carries a time to the minute and no window. The four witnessed classes are reported as
they happen and carry a time throughout.

The keeper's routine belongs to the target, not to the offence, so which gap a recorded offence carries does
not depend on where inside that gap the offence fell.
"""
import datetime as dt
import functools

import numpy as np

import world as W

POINT_KINDS = ("point_night", "point_day")
HW = W.HOURS_WEEK


def rng(k):
    return np.random.default_rng([W.SEED, 2, k, W.NUDGE])


@functools.lru_cache(maxsize=1)
def intensity():
    """The quarter's property-crime clock: the share of the covered offences that happen in each of the 168
    hours of the week, Monday 00:00 first.

    One night mode per night of the week, cresting before midnight on the nights the quarter's licences end
    at 23:00 and after it on the nights they run late, plus a daytime shoulder from the hours the premises
    and the bays stand empty. Nothing in the pack states it; it is what the record is of.
    """
    v = np.zeros(HW + 72)
    for d in range(7):
        crest = d * 24 + W.NIGHT_CREST[d]
        for t in range(d * 24 + 10, d * 24 + 46):
            v[t] += W.NIGHT_AMP[d] * np.exp(-0.5 * ((t - crest) / W.NIGHT_WID) ** 2)
        for t in range(d * 24 + 4, d * 24 + 24):
            v[t] += W.DAY_AMP * W.DAY_DOW[d] * np.exp(-0.5 * ((t - (d * 24 + W.DAY_CREST)) / W.DAY_WID) ** 2)
    q = v[:HW].copy()
    q[:72] += v[HW:HW + 72]                      # the week wraps: Sunday night runs into Monday
    q = q + W.FLOOR * q.max()
    return q / q.sum()


# How far either side of its family's hours one keeper's own routine sits. "edges" moves the two ends of a
# trading day independently (a shop opens an hour early, shuts two hours late); "shift" moves a one-hour
# look at a vehicle or a cycle whole. The kiosk and the bars are fixed: a timetable and a licence fix them.
JITTER = {
    "ferry": ("fixed", [(0, 1.0)], [(0, 1.0)]),
    "bar": ("fixed", [(0, 1.0)], [(0, 1.0)]),
    "shop": ("edges", [(-1, 0.22), (0, 0.50), (1, 0.28)], [(-1, 0.26), (0, 0.44), (2, 0.30)]),
    "market": ("edges", [(-1, 0.30), (0, 0.46), (1, 0.24)], [(0, 0.52), (1, 0.28), (3, 0.20)]),
    "kiosk": ("edges", [(-1, 0.24), (0, 0.48), (2, 0.28)], [(-1, 0.30), (0, 0.42), (2, 0.28)]),
    "office": ("edges", [(-1, 0.26), (0, 0.50), (1, 0.24)], [(0, 0.44), (1, 0.32), (3, 0.24)]),
    "depot": ("edges", [(-2, 0.26), (0, 0.46), (1, 0.28)], [(0, 0.46), (2, 0.30), (4, 0.24)]),
    "store": ("edges", [(-1, 0.28), (0, 0.44), (2, 0.28)], [(-1, 0.28), (0, 0.44), (3, 0.28)]),
    "chandler": ("edges", [(-1, 0.24), (0, 0.50), (1, 0.26)], [(-1, 0.26), (0, 0.46), (2, 0.28)]),
    "home_eve": ("edges", [(-2, 0.28), (0, 0.44), (1, 0.28)], [(-1, 0.30), (0, 0.42), (2, 0.28)]),
    "home_shift": ("edges", [(-1, 0.30), (0, 0.44), (1, 0.26)], [(-1, 0.26), (0, 0.46), (2, 0.28)]),
    "home_part": ("edges", [(-1, 0.26), (0, 0.48), (1, 0.26)], [(-1, 0.28), (0, 0.44), (2, 0.28)]),
    "home_away": ("edges", [(-2, 0.30), (0, 0.42), (2, 0.28)], [(-1, 0.28), (0, 0.44), (3, 0.28)]),
    "bay_two": ("fixed", [(0, 1.0)], [(0, 1.0)]),
    "bay_one": ("shift", [(-2, 0.26), (0, 0.46), (1, 0.28)], [(0, 1.0)]),
    "bay_commute": ("shift", [(-1, 0.30), (0, 0.44), (1, 0.26)], [(0, 1.0)]),
    "bay_week": ("shift", [(-2, 0.28), (0, 0.44), (2, 0.28)], [(0, 1.0)]),
    "rack_day": ("shift", [(-1, 0.28), (0, 0.46), (1, 0.26)], [(0, 1.0)]),
    "rack_eve": ("shift", [(-2, 0.26), (0, 0.44), (2, 0.30)], [(0, 1.0)]),
    "rack_store": ("shift", [(-1, 0.30), (0, 0.42), (1, 0.28)], [(0, 1.0)]),
}


@functools.lru_cache(maxsize=None)
def variants(name):
    """[(share, start offset, end offset)] for one keeper family: the hours its own premises keep."""
    mode, starts, ends = JITTER[name]
    if mode == "shift":
        return [(ws, ds, ds) for ds, ws in starts]
    out = [(ws * we, ds, de) for ds, ws in starts for de, we in ends]
    tot = sum(x for x, _, _ in out)
    return [(x / tot, ds, de) for x, ds, de in out]


@functools.lru_cache(maxsize=None)
def routine(name, ds=0, de=0):
    """(gap holder, watched mask) for one keeper's routine, as that keeper actually keeps it.

    The holder maps each unwatched hour of the week to the gap that holds it, as (start hour of the week,
    length in hours). Any set of watched intervals tiles the week into gaps, so the gap a recorded offence
    carries is independent of where inside it the offence fell whatever the keeper's hours are.
    """
    mark = np.zeros(HW, bool)
    for a, b in W.WATCHED[name]:
        a, b = a + ds, b + de
        if b <= a:
            b = a + 1
        for t in range(a, b):
            mark[t % HW] = True
    watched_hours = np.where(mark)[0]
    if len(watched_hours) == 0:
        raise ValueError("a routine with no watched hour: %s" % name)
    origin = int(watched_hours[0])
    holder, t = {}, origin
    while t < origin + HW:
        if not mark[t % HW]:
            s = t
            while not mark[t % HW]:
                t += 1
            for u in range(s, t):
                holder[u % HW] = (s % HW, t - s)
        else:
            t += 1
    return holder, mark


@functools.lru_cache(maxsize=None)
def routine_mix(cls):
    """The keepers of one class's targets, family by family and then premises by premises."""
    out = []
    for share, name in W.ROUTINE_MIX[cls]:
        for v, ds, de in variants(name):
            out.append((share * v, name, ds, de))
    w = np.array([x for x, _, _, _ in out], float)
    return w / w.sum(), [(n, ds, de) for _, n, ds, de in out]


def window(kind, g, n):
    """(start hour from midnight of the first day, length in hours) for n offences of a witnessed class."""
    if kind == "point_night":
        s = 19.5 + 10.0 * g.beta(2.0, 2.4, n)                 # 19:30 to 05:30, the taxi rank clearing last
        return s, np.zeros(n)
    if kind == "point_day":
        u = g.random(n)
        market = u < 0.34                                     # the fish market trades from 04:00
        s = np.where(market, 4.0 + 4.0 * g.random(n), 8.5 + 12.5 * g.beta(2.0, 2.0, n))
        return s, np.zeros(n)
    raise ValueError(kind)


def on_the_hour(t, up):
    t = t.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1 if up else 0)
    return t


def date_for(days_by_dow, dow, g):
    ds = days_by_dow[dow]
    return ds[int(g.integers(0, len(ds)))]


def covered_record(cls, g, days_by_dow, season):
    """One recorded offence of a covered class: the hour it happened, and the gap the record carries.

    The hour comes from the quarter's clock, the routine from the target, and the two meet: if the hour is a
    watched one the keeper sees it and the record carries a time, otherwise the record carries the gap.
    """
    q = intensity()
    h = int(g.choice(HW, p=q))
    weights, names = routine_mix(cls)
    holder, mark = routine(*names[int(g.choice(len(names), p=weights))])
    d0, d1 = season
    minute = int(g.integers(0, 60))
    day = date_for(days_by_dow, h // 24, g)
    true_at = dt.datetime.combine(day, dt.time()) + dt.timedelta(hours=h % 24, minutes=minute)
    if mark[h]:
        start = end = true_at.replace(second=0, microsecond=0)
    else:
        a, ln = holder[h]
        back = (h - a) % HW
        start = (true_at - dt.timedelta(hours=back)).replace(minute=0, second=0, microsecond=0)
        end = start + dt.timedelta(hours=ln)
    while end.date() > d1:
        start -= dt.timedelta(days=7)
        end -= dt.timedelta(days=7)
        true_at -= dt.timedelta(days=7)
    while start.date() < d0:
        start += dt.timedelta(days=7)
        end += dt.timedelta(days=7)
        true_at += dt.timedelta(days=7)
    return start, end, true_at


def simulate():
    """Every recorded offence of the two seasons, with the force's own fields and the unobserved true time."""
    rows = []
    for k, (cls, (per_season, kind, dow_w)) in enumerate(W.CLASSES.items()):
        g = rng(k + 1)
        for si, (d0, d1) in enumerate(W.SEASONS):
            n = int(round(per_season * (1.0 + 0.03 * (si * 2 - 1))))
            days = W.season_days(si)
            loc = g.choice(len(W.LOCATIONS), size=n, p=location_mix(cls))
            rep_lag = g.gamma(1.6, 5.0, n)                    # hours from discovery to the report
            if kind == "routine":
                by_dow = {d: [x for x in days if x.weekday() == d] for d in range(7)}
                for j in range(n):
                    start, end, true_at = covered_record(cls, g, by_dow, (d0, d1))
                    rows.append({
                        "cls": cls, "season": si, "from": start, "to": end, "true": true_at,
                        "reported": (end + dt.timedelta(hours=float(rep_lag[j]))).replace(
                            second=0, microsecond=0),
                        "loc": W.LOCATIONS[int(loc[j])],
                    })
                continue
            w = np.array(dow_w, float)
            dows = np.array([d.weekday() for d in days])
            p = w[dows] / w[dows].sum()
            di = g.choice(len(days), size=n, p=p)
            s, _ln = window(kind, g, n)
            for j in range(n):
                base = dt.datetime.combine(days[int(di[j])], dt.time())
                at = (base + dt.timedelta(hours=float(s[j]))).replace(second=0, microsecond=0)
                while at.date() > d1:
                    at -= dt.timedelta(days=7)
                rows.append({
                    "cls": cls, "season": si, "from": at, "to": at, "true": at,
                    "reported": (at + dt.timedelta(hours=float(rep_lag[j]))).replace(second=0, microsecond=0),
                    "loc": W.LOCATIONS[int(loc[j])],
                })
    rows.sort(key=lambda r: (r["reported"], r["cls"], r["from"]))
    return rows


def location_mix(cls):
    """Where in the quarter each class sits: the car parks take the vehicle crime, the street the rest."""
    mix = {
        "Theft from a motor vehicle": [0.12, 0.44, 0.08, 0.06, 0.30],
        "Theft of a pedal cycle":     [0.34, 0.14, 0.22, 0.20, 0.10],
        "Criminal damage":            [0.38, 0.14, 0.24, 0.14, 0.10],
        "Burglary business":          [0.46, 0.04, 0.18, 0.28, 0.04],
        "Burglary residential":       [0.30, 0.04, 0.46, 0.14, 0.06],
        "Theft from the person":      [0.44, 0.06, 0.14, 0.30, 0.06],
        "Assault without injury":     [0.48, 0.08, 0.16, 0.22, 0.06],
        "Public order":               [0.46, 0.08, 0.18, 0.22, 0.06],
        "Shoplifting":                [0.40, 0.04, 0.12, 0.42, 0.02],
    }[cls]
    m = np.array(mix, float)
    m[0] *= W.LOC_SHIFT                       # fixed at design so the location shares sit mid-bin
    return m / m.sum()


def season_of(d):
    """The season an occurrence date falls in, or None. A witnessed offence at one in the morning of 1 October
    happened after the season closed, whatever the night it belongs to in the telling."""
    for i, (a, b) in enumerate(W.SEASONS):
        if a <= d <= b:
            return i
    return None


def contracted(rows):
    return [r for r in rows if r["cls"] in W.CONTRACTED]


def slot_of(ts):
    return (ts.weekday(), (ts.hour // W.SLOT_H) * W.SLOT_H)


def hour_of_week(ts):
    return ts.weekday() * 24 + ts.hour
