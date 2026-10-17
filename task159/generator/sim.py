"""The morning, train by train: every line in both directions, each train taking at most the room it has left, the
riders it cannot take waiting for the next one. Used three ways: expected-value runs (the clean truth the checks
hold the golden to), and seeded runs for the census days and the count days (what the records were drawn from)."""
from __future__ import annotations

import math

import numpy as np

import world as W

T0, T1 = 5 * 60, 11 * 60          # the simulated morning, minutes after local midnight
GRID = np.arange(T0, T1 + 1, dtype=float)


def _tprof(minute, mu=488.0, sd=32.0):
    return W.profile(minute, mu, sd)


def rates(factor_of, plan="autumn2026"):
    """Per-minute arrival and alighting rates for every (station, line, direction) on a day.

    factor_of(station) gives the day's riding factor at a station (the network's weekday, month and year level times
    the station's own jitter). Returns (arrive, alight) dicts keyed by (station, line, dir), each an array over GRID
    of people per minute, and a dict of transfer flows {(station, from, to): array}."""
    arrive, alight = {}, {}
    mins = GRID
    for (s, l, d), f in W.FLOWS.items():
        prof = np.array([W.profile(m, f["mu"], f["sd"]) for m in mins])
        k = factor_of(s)
        arrive[(s, l, d)] = f["board"] * prof * k
        alight[(s, l, d)] = f["exit"] * np.array([W.profile(m, f["mu"] + 8, f["sd"]) for m in mins]) * k
    trans = {}
    for s, a, b, r in W.TRANSFERS:
        la, da = a[0], a[1:]
        lb, db = b[0], b[1:]
        prof = np.array([_tprof(m) for m in mins]) * r * factor_of(s)
        trans[(s, a, b)] = prof
        alight[(s, la, da)] = alight.get((s, la, da), np.zeros_like(mins)) + prof
        arrive[(s, lb, db)] = arrive.get((s, lb, db), np.zeros_like(mins)) + prof
    return arrive, alight, trans


def _cum(arr):
    """Cumulative people from GRID[0]; arr is a per-minute rate sampled at GRID points (left Riemann)."""
    c = np.concatenate([[0.0], np.cumsum(arr[:-1])])
    return c


def _integral(cum, a, b):
    """People arriving between minute a and minute b (fractional), from the cumulative series."""
    def at(x):
        x = min(max(x, GRID[0]), GRID[-1])
        i = int(x - GRID[0])
        if i >= len(cum) - 1:
            return cum[-1]
        frac = x - GRID[0] - i
        return cum[i] + (cum[i + 1] - cum[i]) * frac
    return max(0.0, at(b) - at(a))


def run_line(line, direction, arrive, alight, plan="autumn2026", rng=None, cars=None, car_max=None,
             delays=None):
    """Simulate one line-direction. Returns {station: [events]} with each event a dict: t (arrival minute), crowd
    (waiting before the doors open), board, left (behind), alight, load_in, load_out, room."""
    stations, offs = W.arrival_offsets(line, direction)
    ncars = cars if cars is not None else W.CARS[plan][line]
    cap = ncars * (car_max if car_max is not None else W.CAR_MAX)
    deps = W.departures(line, plan)
    cums_a = {s: _cum(arrive.get((s, line, direction), np.zeros_like(GRID))) for s in stations}
    cums_x = {s: _cum(alight.get((s, line, direction), np.zeros_like(GRID))) for s in stations}
    carry = {s: 0.0 for s in stations}
    last_t = {s: None for s in stations}
    events = {s: [] for s in stations}
    for k, dep in enumerate(deps):
        load = 0.0
        late = 0.0 if delays is None else delays[k]
        for s in stations:
            t = dep + offs[s] + late
            t_prev = last_t[s] if last_t[s] is not None else t - W.headway(line, dep, plan)
            n_exp = _integral(cums_a[s], t_prev, t)
            x_exp = _integral(cums_x[s], t_prev, t)
            if rng is not None:
                n = float(rng.poisson(n_exp))
                x = float(rng.poisson(x_exp))
            else:
                n, x = n_exp, x_exp
            a = min(load, x)
            crowd = carry[s] + n
            room = cap - (load - a)
            b = min(crowd, room)
            carry[s] = crowd - b
            load_in = load
            load = load - a + b
            events[s].append(dict(t=t, sched=dep + offs[s], crowd=crowd, board=b, left=carry[s], alight=a,
                                  load_in=load_in, load_out=load, room=room, arrivals=n))
            last_t[s] = t
    return events


def run_all(factor_of, plan="autumn2026", rng=None, cars=None, car_max=None, delay_rng=None):
    """Every line-direction on one morning. delay_rng, when given, draws each train's running delay (minutes,
    applied from its origin): most trains on time, a few a minute or two late."""
    arrive, alight, trans = rates(factor_of, plan)
    out = {}
    for l, L in W.LINES.items():
        for d in L["dirs"]:
            c = None if cars is None else cars.get(l)
            dl = None
            if delay_rng is not None:
                nd = len(W.departures(l, plan))
                base = delay_rng.exponential(0.25, nd)
                big = delay_rng.random(nd) < 0.08
                dl = list(np.round(base + big * delay_rng.uniform(0.8, 2.6, nd), 2))
            out[(l, d)] = run_line(l, d, arrive, alight, plan, rng=rng, cars=c, car_max=car_max, delays=dl)
    return out, arrive, alight, trans


def platform_series(out, key):
    """At-arrival counts on a platform: [(t, crowd, line, dir)], for an island the whole platform's crowd (both
    directions' waiting riders) at each train's arrival."""
    station, rest = key.split("|")
    line = rest[0]
    if len(rest) == 1:      # island
        d1, d2 = W.LINES[line]["dirs"]
        e1, e2 = out[(line, d1)][station], out[(line, d2)][station]
        res = []
        for mine, other, dd in ((e1, e2, d1), (e2, e1, d2)):
            for ev in mine:
                res.append((ev["t"], ev["crowd"] + _waiting_at(other, ev["t"]), line, dd, ev["sched"]))
        res.sort()
        return res
    d = rest[1:]
    return [(ev["t"], ev["crowd"], line, d, ev["sched"]) for ev in out[(line, d)][station]]


def _waiting_at(events, t):
    """The other direction's waiting crowd at time t: what its last train left behind plus arrivals since, taken
    linearly between that train and its next one."""
    prev, nxt = None, None
    for ev in events:
        if ev["t"] <= t:
            prev = ev
        else:
            nxt = ev
            break
    if prev is None:
        return 0.0
    if nxt is None:
        return prev["left"]
    span = nxt["t"] - prev["t"]
    grown = (nxt["crowd"] - prev["left"]) * (t - prev["t"]) / span if span > 0 else 0.0
    return prev["left"] + max(0.0, grown)


def peak_quarter(series, start=7 * 60, end=9 * 60 + 45):
    """Highest quarter-hour mean of at-arrival counts, quarter-hours 07:00-07:15 ... 09:30-09:45."""
    best, bq = 0.0, None
    q = start
    while q < end:
        xs = [c for (t, c, *_rest) in series if q <= t < q + 15]
        if xs:
            m = sum(xs) / len(xs)
            if m > best:
                best, bq = m, q
        q += 15
    return best, bq
