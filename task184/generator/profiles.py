"""Arrival profiles and roster plans. A checkpoint's day is an off-peak flow with a morning and an evening bank of
departures whose plateau runs a set number of lanes' worth above the permanent lanes; the roster plan staffs every
lane from 45 minutes before a bank to an hour after the morning bank and an hour and three quarters after the evening
bank, and the off-peak lanes otherwise. The 2027 design days carry the schedule's own unevenness from one 15 minutes to the
next, its draw fixed by airport and period."""
import numpy as np

import world as W
import models as M

R = W.LANE_RATE
HOUR = M.HOUR


def wobble(code, name, s=0):
    """The schedule's own unevenness from one 15 minutes to the next, fixed by airport, period and draw."""
    g = np.random.default_rng([W.SEED, 27, W.CODES.index(code), [n for n, _, _ in W.PERIODS].index(name), s])
    e = g.standard_normal(W.T + 2)
    return 1.0 + 0.032 * (0.25 * e[:-2] + 0.5 * e[1:-1] + 0.25 * e[2:]) / 0.6124


# the off-peak day: a thin first hour, a late-morning wave of leisure departures, an afternoon lull and a thinning
# last hour, as multiples of the off-peak flow; each airport's late-morning wave sits at its own time
LATE_MORNING = {"CUL": 10.75, "ARD": 11.25, "FAR": 10.50, "HAL": 11.50, "ESK": 11.00, "BRN": 12.00, "DRM": 10.75,
                "GLK": 11.75}


def offpeak(code):
    h = HOUR
    m = np.ones(W.T)
    m = np.where(h < 4.5, 0.78, m)
    m = np.where((h >= 4.5) & (h < 5.0), 0.9, m)
    c = LATE_MORNING[code]
    m = m + 0.22 * np.exp(-0.5 * ((h - c) / 0.55) ** 2)
    m = m - 0.08 * np.exp(-0.5 * ((h - 14.25) / 0.6) ** 2)
    m = np.where(h >= 20.5, m * (1 - 0.12 * (h - 20.25)), m)
    return m


def shape(code, demand, ramp=0.75):
    """The unrounded profile of one day: the off-peak day and two banks whose plateau crests a little in its middle."""
    base, xm, xe = demand
    lanes = W.LANES[code]
    _, _, (ms, me), (es, ee) = W.CHECKPOINT[code]
    a = base * offpeak(code)
    for x, s, e in ((xm, ms, me), (xe, es, ee)):
        pk = (lanes + x) * R
        mid, half = (s + e) / 2.0, (e - s) / 2.0
        for i, h in enumerate(HOUR):
            if s - ramp <= h < s:
                v = a[i] + (pk * 0.97 - a[i]) * (h - (s - ramp)) / ramp
            elif s <= h < e:
                v = pk * (1.03 - 0.06 * abs(h + 0.125 - mid) / max(half, 0.25))
            elif e <= h < e + ramp:
                v = pk * 0.97 - (pk * 0.97 - a[i]) * (h - e) / ramp
            else:
                continue
            a[i] = max(a[i], v)
    return a


def plan(code):
    lanes, off, (ms, me), (es, ee) = W.CHECKPOINT[code]
    peak = ((HOUR >= ms - 0.75) & (HOUR < me + 1.0)) | ((HOUR >= es - 0.75) & (HOUR < ee + 1.75))
    return np.where(peak, lanes, off).astype(float)


def margins(code, a, pl):
    """The closest any interval's wait comes to 20 minutes on the golden's two runs (no unit; the unit with the host's
    release by interval) and on every wrong run the ladder names (plan plus three; the release averaged over the
    unit's hours; the release's all-day part only)."""
    r = M.release(code, pl)
    golden = [pl, pl + M.team() - r]
    wrong = [pl + M.team(), pl + M.team() - M.day_average(r), pl + M.team() - M.all_day_part(code, pl)]
    g = min(float(np.min(np.abs(M.queue(a, L)[1] - W.STANDARD_MIN))) for L in golden)
    w = min(float(np.min(np.abs(M.queue(a, L)[1] - W.STANDARD_MIN))) for L in wrong)
    return g, w


def design27(gold_margin=0.3, wrong_margin=0.1):
    """design[code][period] (whole passengers by interval) and plans[code][period]; the unevenness's draw for each
    airport and period is the first that keeps every wait at least gold_margin minutes off 20 on the golden's runs
    and wrong_margin on the ladder's, and whose posting figure neither rounds to a whole thousand nor sits on a half-hundred; August's phase
    also keeps the summer, rounded, equal to the sum of the rounded periods and off a whole thousand."""
    design, plans, phase = {}, {}, {}
    for code in W.CODES:
        design[code], plans[code] = {}, {}
        pl = plan(code)
        figs = {}
        for name, _, _ in W.PERIODS:
            for s in range(400):
                a = np.round(shape(code, W.DEMAND27[code]) * wobble(code, name, s) * W.PERIOD_SCALE[name])
                g, w = margins(code, a, pl)
                fig = M.moved(a, pl, M.release(code, pl)) * W.DAYS[name]
                if g < gold_margin or w < wrong_margin or not round(fig, -2) % 1000 or abs(fig % 100 - 50) < 1:
                    continue
                if name == "August":
                    total = sum(figs.values()) + fig
                    if round(total, -2) != sum(round(v, -2) for v in figs.values()) + round(fig, -2) or \
                            not round(total, -2) % 1000:
                        continue
                break
            else:
                raise RuntimeError("no clean phase for %s %s" % (code, name))
            figs[name] = fig
            design[code][name], plans[code][name], phase[(code, name)] = a, pl.copy(), s
    return design, plans, phase
