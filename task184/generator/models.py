"""The planning standard's queue computation and the posting scenarios: passengers over the 20-minute standard on a
day, the passengers a posting moves within it, the lanes a host stands down while the unit is there, and every rung
of the ladder. Pure functions on arrays, used by the generator, the goldens and the checks alike."""
import numpy as np

import world as W

HOUR = np.array([W.hour_of(i) for i in range(W.T)])
TEAM_ON = (HOUR >= W.TEAM_FROM) & (HOUR < W.TEAM_TO)
EARLY = (HOUR >= 5) & (HOUR < 13)
LATE = (HOUR >= 13) & (HOUR < 21)


def queue(arrivals, lanes, rate=W.LANE_RATE):
    """The standard: the wait of an interval's arrivals is the queue at its start and half its arrivals over what the
    open lanes screen in 15 minutes, in minutes; the queue carries forward; passengers waiting over 20 minutes are
    outside the standard. Returns (passengers outside the standard, waits by interval)."""
    a = np.asarray(arrivals, float)
    c = np.asarray(lanes, float) * rate
    q, waits, over = 0.0, np.zeros(W.T), 0.0
    for i in range(W.T):
        w = 15.0 * (q + a[i] / 2.0) / c[i]
        waits[i] = w
        if w > W.STANDARD_MIN:
            over += a[i]
        q = max(0.0, q + a[i] - c[i])
    return over, waits


def windows(code):
    m = np.zeros(W.T, bool)
    for s, e in W.RELEASE[code][2]:
        m |= (HOUR >= s) & (HOUR < e)
    return m


def release(code, plan):
    """The host's own lanes stood down while the unit screens there, by interval (never its last lane)."""
    r_all, r_win, _ = W.RELEASE[code]
    r = np.where(TEAM_ON, float(r_all), 0.0) + np.where(windows(code) & TEAM_ON, float(r_win), 0.0)
    return np.minimum(r, plan - 1)


def all_day_part(code, plan):
    return np.minimum(np.where(TEAM_ON, float(W.RELEASE[code][0]), 0.0), plan - 1)


def day_average(r):
    """A release averaged over the unit's hours (the second rung)."""
    return np.where(TEAM_ON, r[TEAM_ON].mean(), 0.0)


def team():
    return np.where(TEAM_ON, float(W.TEAM_LANES), 0.0)


def moved(arrivals, plan, released):
    """Passengers outside the standard without the unit less those outside it with the unit and the host's release."""
    o0, _ = queue(arrivals, plan)
    o1, _ = queue(arrivals, plan + team() - released)
    return o0 - o1


def released_for(how, code, plan):
    if how == "gross":
        return np.zeros(W.T)
    r = release(code, plan)
    if how == "average":
        return day_average(r)
    if how == "average18":
        return np.full(W.T, r.mean())
    if how == "shift":
        out = np.zeros(W.T)
        for m in (EARLY, LATE):
            out[m] = r[m].mean()
        return out
    if how == "allday":
        return all_day_part(code, plan)
    if how == "uniform2":
        return np.where(TEAM_ON, 2.0, 0.0)
    return r


def scenario(design, plans, how="interval"):
    """Passengers moved over the posting at each airport and period: the design day's figure times the period's days.
    how: 'gross' (planned lanes plus three, rung 0), 'average' (the host's release averaged over the unit's hours,
    rung 2), 'interval' (the release by interval, the golden), and the variants the checks sweep."""
    out = {}
    for code in W.CODES:
        out[code] = {}
        for name, _, _ in W.PERIODS:
            a, p = design[code][name], plans[code][name]
            out[code][name] = moved(a, p, released_for(how, code, p)) * W.DAYS[name]
    return out


def totals(sc):
    return {c: sum(v.values()) for c, v in sc.items()}


def ranking(sc):
    t = totals(sc)
    return sorted(t, key=lambda c: -t[c])


def summer(design, plans, code, factor=1.0, mode="none"):
    """One airport's posting over the summer with its design-day arrivals scaled by factor (the flip)."""
    tot = 0.0
    for name, _, _ in W.PERIODS:
        a = design[code][name] * factor
        if mode == "round":
            a = np.round(a)
        elif mode == "floor":
            a = np.floor(a)
        p = plans[code][name]
        tot += moved(a, p, release(code, p)) * W.DAYS[name]
    return tot


def flip(design, plans, pick, mode="none"):
    """The smallest whole per cent by which the pick's design-day arrivals can fall short, uniformly, before another
    airport's posting moves more passengers."""
    base = totals(scenario(design, plans))
    best_other = max(v for c, v in base.items() if c != pick)
    for k in range(1, 100):
        if summer(design, plans, pick, 1 - k / 100.0, mode) < best_other:
            return k
    return None
