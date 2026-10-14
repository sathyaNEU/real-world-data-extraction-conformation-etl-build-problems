"""The planning standard's queue computation and the posting scenarios: passengers over the 20-minute standard on a
day, the lanes a checkpoint actually opens (its roster pattern less the posts it carries unfilled), the lanes a host
stands down while the unit is there, the passengers a posting moves within the standard, and every rung of the
ladder. Pure functions on arrays, used by the generator, the goldens and the checks alike."""
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


def bank_windows(code):
    """The intervals the roster pattern staffs for a bank: from 45 minutes before the plateau to an hour after the
    morning one and an hour and three quarters after the evening one."""
    _, _, (ms, me), (es, ee) = W.CHECKPOINT[code]
    m = (HOUR >= ms - 0.75) & (HOUR < me + 1.0)
    e = (HOUR >= es - 0.75) & (HOUR < ee + 1.75)
    return m, e


def quiet_window(code):
    _, _, (_, me), (es, _) = W.CHECKPOINT[code]
    return (HOUR >= me + 1.0) & (HOUR < es - 0.75)


def shortfall(code, plan):
    """The lanes the roster pattern staffs for a bank that the checkpoint's shorter overtime block leaves closed, by
    interval: the same every day of the summer, whether or not the unit is there."""
    n, d = W.SHORT[code]
    _, _, (ms, me), (es, ee) = W.CHECKPOINT[code]
    m = ((HOUR >= ms - 0.75) & (HOUR < ms + d)) | ((HOUR >= me - d) & (HOUR < me + 1.0))
    e = ((HOUR >= es - 0.75) & (HOUR < es + d)) | ((HOUR >= ee - d) & (HOUR < ee + 1.75))
    extra = plan - float(W.CHECKPOINT[code][1])
    return np.minimum(np.where(m | e, float(n), 0.0), extra)


def baseline(code, plan):
    """The lanes the checkpoint opens with no unit posted: its roster pattern less its unfilled posts."""
    return plan - shortfall(code, plan)


def release(code, plan):
    """The host's own lanes stood down while the unit screens there, by interval (never its last lane)."""
    bm, be, q, t = W.RELEASE[code]
    m, e = bank_windows(code)
    r = np.where(quiet_window(code), float(q), 0.0)
    r = np.where(m, float(bm), r)
    r = np.where(e, float(be), r)
    r = np.where(HOUR >= 20.25, float(t), r)
    r = np.where(TEAM_ON, r, 0.0)
    return np.minimum(r, plan - shortfall(code, plan) - 1)


def gap_seen(code, plan):
    """The whole shortfall a posted day shows against the roster pattern: the unfilled posts and the stand-down
    together, which is what the lane feed reports and the pattern cannot separate."""
    return shortfall(code, plan) + release(code, plan)


def day_average(r):
    """A shortfall averaged over the unit's hours (one rung)."""
    return np.where(TEAM_ON, r[TEAM_ON].mean(), 0.0)


def team():
    return np.where(TEAM_ON, float(W.TEAM_LANES), 0.0)


def arms(code, plan, how):
    """The two lane counts a basis compares: the lanes open without the unit, and the lanes open with it.

    gross      the roster pattern, plus the unit's three (the default path)
    average    the pattern, less the posted day's whole shortfall averaged over the unit's hours
    interval   the pattern, less that shortfall interval by interval
    actual     what the checkpoint opens without a unit, against what it opens with one (the golden)
    double     the checkpoint's own lanes on both arms, the whole shortfall taken off again
    standonly  the pattern's shortfall corrected on both arms, the stand-down ignored
    shift      the shortfall averaged over each of the unit's two shifts
    average18  the shortfall averaged over the whole day the checkpoint is open
    uniform    the stand-down of the busiest checkpoint applied at every host
    """
    g = gap_seen(code, plan)
    b = baseline(code, plan)
    if how == "gross":
        return plan, plan + team()
    if how == "average":
        return plan, plan + team() - day_average(g)
    if how == "interval":
        return plan, plan + team() - g
    if how == "actual":
        return b, plan + team() - g
    if how == "double":
        return b, b + team() - g
    if how == "standonly":
        return b, b + team()
    if how == "shift":
        out = np.zeros(W.T)
        for m in (EARLY, LATE):
            out[m] = g[m].mean()
        return plan, plan + team() - out
    if how == "average18":
        return plan, plan + team() - np.full(W.T, g.mean())
    if how == "uniform":
        r = np.where(TEAM_ON, float(W.RELEASE["CUL"][0]), 0.0)
        return plan, plan + team() - np.minimum(r, plan - 1)
    raise ValueError(how)


def moved(arrivals, plan, code, how="actual"):
    """Passengers outside the standard on the lanes open without the unit less those outside it on the lanes open
    with the unit and the host's response, as the standard judges a change."""
    lo, l1 = arms(code, plan, how)
    return queue(arrivals, lo)[0] - queue(arrivals, l1)[0]


def scenario(design, plans, how="actual"):
    """Passengers moved over the posting at each airport and period: the design day's figure times the period's days."""
    out = {}
    for code in W.CODES:
        out[code] = {}
        for name, _, _ in W.PERIODS:
            out[code][name] = moved(design[code][name], plans[code][name], code, how) * W.DAYS[name]
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
        tot += moved(a, plans[code][name], code, "actual") * W.DAYS[name]
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
