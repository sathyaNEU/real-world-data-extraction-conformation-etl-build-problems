"""The Harbourgate quarter's recorded offences, 2025 and 2026 seasons.

One row is one recorded offence. The classes the patrol contract covers are discovered rather than witnessed, so
their occurrence time is recorded as the window the victim can vouch for: the premises closed and opened again, the
vehicle left and returned to, the cycle locked and found gone. Victims give those times in round clock hours, so
both ends of a window sit on the hour. The four witnessed classes carry a time to the minute and no window.
"""
import datetime as dt

import numpy as np

import world as W

POINT_KINDS = ("point_night", "point_day")


def rng(k):
    return np.random.default_rng([W.SEED, 2, k, W.NUDGE])


def window(kind, g, n):
    """(start hour from midnight of the first day, length in hours) for n offences of one class.

    Each kind is a mixture, because the circumstances are: a shop is shut overnight, or over a bank holiday
    weekend, or the damage is found before closing; a car is left for a morning, a working day or a whole night.
    """
    if kind == "point_night":
        s = 19.5 + 10.0 * g.beta(2.0, 2.4, n)                 # 19:30 to 05:30, the taxi rank clearing last
        return s, np.zeros(n)
    if kind == "point_day":
        u = g.random(n)
        market = u < 0.34                                     # the fish market trades from 04:00
        s = np.where(market, 4.0 + 4.0 * g.random(n), 8.5 + 12.5 * g.beta(2.0, 2.0, n))
        return s, np.zeros(n)
    if kind == "mixed_park":                                  # a vehicle left at an evening or a commuter park
        u = g.random(n)
        s = np.where(u < 0.44, 17.5 + 4.5 * g.random(n),
                     np.where(u < 0.82, 6.5 + 3.5 * g.random(n), 10.0 + 6.0 * g.random(n)))
        ln = np.where(u < 0.44, 2.0 + 6.5 * g.random(n),
                      np.where(u < 0.82, 5.5 + 5.5 * g.random(n), 2.0 + 4.0 * g.random(n)))
        return s, ln
    if kind == "lockup":                                      # a cycle locked up and found gone
        u = g.random(n)
        s = np.where(u < 0.38, 16.0 + 4.0 * g.random(n),
                     np.where(u < 0.88, 7.5 + 5.0 * g.random(n), 12.0 + 6.0 * g.random(n)))
        ln = np.where(u < 0.38, 2.0 + 8.0 * g.random(n),
                      np.where(u < 0.88, 2.0 + 7.0 * g.random(n), 20.0 + 28.0 * g.random(n)))
        return s, ln
    if kind == "closed_hours":                                # closed or last seen, found at opening
        u = g.random(n)
        s = np.where(u < 0.10, 13.0 + 7.0 * g.random(n), 18.5 + 4.0 * g.random(n))
        end = np.where(u < 0.10, 20.0 + 4.0 * g.random(n),
                       np.where(u < 0.86, 29.5 + 5.5 * g.random(n), 48.0 + 26.0 * g.random(n)))
        ln = np.maximum(end - s, 2.0)
        return s, ln
    if kind == "absence":                                     # a dwelling empty for a working day or a trip
        u = g.random(n)
        s = np.where(u < 0.18, 6.5 + 4.5 * g.random(n),
                     np.where(u < 0.74, 7.0 + 2.5 * g.random(n), 16.0 + 5.0 * g.random(n)))
        ln = np.where(u < 0.18, 22.0 + 50.0 * g.random(n),
                      np.where(u < 0.74, 7.5 + 4.5 * g.random(n), 11.0 + 6.0 * g.random(n)))
        return s, ln
    raise ValueError(kind)


def on_the_hour(t, up):
    t = t.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1 if up else 0)
    return t


def simulate():
    """Every recorded offence of the two seasons, with the force's own fields and the unobserved true time."""
    rows = []
    for k, (cls, (per_season, kind, dow_w)) in enumerate(W.CLASSES.items()):
        g = rng(k + 1)
        w = np.array(dow_w, float)
        for si, (d0, d1) in enumerate(W.SEASONS):
            n = int(round(per_season * (1.0 + 0.03 * (si * 2 - 1))))
            days = W.season_days(si)
            dows = np.array([d.weekday() for d in days])
            p = w[dows] / w[dows].sum()
            di = g.choice(len(days), size=n, p=p)
            s, ln = window(kind, g, n)
            loc = g.choice(len(W.LOCATIONS), size=n, p=location_mix(cls))
            rep_lag = g.gamma(1.6, 5.0, n)                    # hours from discovery to the report
            for j in range(n):
                base = dt.datetime.combine(days[int(di[j])], dt.time())
                start = base + dt.timedelta(hours=float(s[j]))
                length = float(ln[j])
                if length > 0:
                    end = start + dt.timedelta(hours=length)
                    start = on_the_hour(start, start.minute >= 30)
                    end = on_the_hour(end, end.minute >= 30)
                    if end <= start:
                        end = start + dt.timedelta(hours=1)
                    while end.date() > d1:
                        # the quarter's own season: an occurrence the force records against it lies inside it,
                        # so a window that would run past the close belongs to the same weekday a week earlier
                        start -= dt.timedelta(days=7)
                        end -= dt.timedelta(days=7)
                    true_at = start + (end - start) * float(g.random())
                else:
                    start = start.replace(second=0, microsecond=0)
                    while start.date() > d1:
                        start -= dt.timedelta(days=7)
                    end = start
                    true_at = start
                rows.append({
                    "cls": cls, "season": si, "from": start, "to": end, "true": true_at,
                    "reported": (end + dt.timedelta(hours=float(rep_lag[j]))).replace(second=0, microsecond=0),
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
