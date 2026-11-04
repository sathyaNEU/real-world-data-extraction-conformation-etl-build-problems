"""The ask figures under the golden handling and under each other handling a careful reader might take, all from the
cut pack: the monthly station atrazine (four sampled stations, April to September) and the monthly carbon fed (May
to August). Used by checks.py (device masses, converging conventions) and ceiling.py (the pair ceiling)."""
import bisect
import csv
import datetime as dt
import os
from collections import defaultdict

import numpy as np
import openpyxl

import golden as G

LOAD_MONTHS = (4, 5, 6, 7)
PAC_MONTHS = (5, 6, 7, 8)


def visits(target):
    wb = openpyxl.load_workbook(os.path.join(target, "hydro/DC-04_LB-05_ratings_and_field_visits.xlsx"), read_only=True)
    out = defaultdict(list)
    for row in wb["Field visits"].iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        k = {"DC-04": "DUN", "LB-05": "LAD"}[row[0]]
        out[k].append((dt.datetime.strptime(row[1] + " " + row[2], "%Y-%m-%d %H:%M"), float(row[3]) - float(row[4])))
    for k in out:
        out[k].sort()
    return out


def offsets(target, how):
    """The loggers' offsets under each handling: `golden` (periods split where the level steps), `mean` (one offset,
    the mean of every visit), `visit` (each visit's offset until the next visit), `prorate` (interpolated between
    visits), `none` (the level read as gage height), `median` (the golden periods, the median of their visits)."""
    if how == "golden":
        return G.logger_offset(target)
    V = visits(target)
    if how == "mean":
        return {k: [(None, float(np.mean([o for _, o in v])))] for k, v in V.items()}
    if how == "none":
        return {k: [(None, 0.0)] for k in V}
    if how == "median":
        segs = G.logger_offset(target)
        out = {}
        for k, sg in segs.items():
            bounds = [t for t, _ in sg] + [None]
            new = []
            for n, (t0, _) in enumerate(sg):
                t1 = bounds[n + 1]
                inside = [o for t, o in V[k] if (t0 is None or t >= t0) and (t1 is None or t < t1)]
                new.append((t0, float(np.median(inside))))
            out[k] = new
        return out
    if how == "visit":
        return {k: [(None, v[0][1])] + [(t, o) for t, o in v[1:]] for k, v in V.items()}
    if how == "visit in hang":
        # each visit's own offset until the next visit, the hang's first visit taken back to the step
        segs = G.logger_offset(target)
        out = {}
        for k, sg in segs.items():
            cuts = [t for t, _ in sg[1:]]
            new = [(None, V[k][0][1])]
            for t, o in V[k][1:]:
                new.append((t, o))
            for c in cuts:
                first_after = [o for t, o in V[k] if t >= c][0]
                new.append((c, first_after))
            new.sort(key=lambda x: (x[0] is not None, x[0] or dt.datetime(2026, 1, 1)))
            out[k] = new
        return out
    if how == "prorate in hang":
        segs = G.logger_offset(target)
        out = {}
        for k, sg in segs.items():
            cuts = [t for t, _ in sg[1:]]

            def f(loc, k=k, cuts=cuts):
                hang = sum(1 for c in cuts if loc >= c)
                lo = cuts[hang - 1] if hang else None
                hi = cuts[hang] if hang < len(cuts) else None
                vs = [(t, o) for t, o in V[k] if (lo is None or t >= lo) and (hi is None or t < hi)]
                xs = np.array([(t - dt.datetime(2026, 1, 1)).total_seconds() for t, _ in vs])
                return float(np.interp((loc - dt.datetime(2026, 1, 1)).total_seconds(), xs, [o for _, o in vs]))
            out[k] = f
        return out
    if how == "prorate":
        out = {}
        for k, v in V.items():
            xs = np.array([(t - dt.datetime(2026, 1, 1)).total_seconds() for t, _ in v])
            ys = np.array([o for _, o in v])
            out[k] = (lambda xs, ys: (lambda loc: float(np.interp((loc - dt.datetime(2026, 1, 1)).total_seconds(),
                                                                   xs, ys))))(xs, ys)
        return out
    raise ValueError(how)


def monthly(target, bottles="golden", offs="golden", utc_window=False, within_month=False):
    """{(k, month): kg} for the sampled stations."""
    L, S, series = G.loads(target, mode=bottles, offsets=offsets(target, offs))
    out = {}
    for k, (ts, q) in series.items():
        for m in LOAD_MONTHS:
            w = (dt.datetime(2026, m, 1), dt.datetime(2026, m + 1, 1))
            if utc_window and k in ("DUN", "LAD"):
                w = (G.utc_to_local(w[0]), G.utc_to_local(w[1]))
            samples = S[k]
            if within_month:
                samples = [(t, v) for t, v in S[k] if w[0] <= t < w[1]]
            out[(k, m)] = G.load_kg(ts, q, samples, window=w)
    return out


def pac(target, how="golden"):
    """{month: lb} under each handling of the feeder's record: `golden`, `nodown` (setpoints only), `runonly` (run
    status, no hopper alarm), `alarmspan` (a trip until its return-to-normal, the low-low alarm until its return),
    `utc` (setpoints and events left on UTC), `lowalarm` (the hopper from its LOW alarm to that alarm's return)."""
    sp, ev = G.feeder_record(target)
    run = G.spans(ev, ("RUN STATUS ON", "EVT"), ("RUN STATUS OFF", "EVT"))
    empty = G.spans(ev, ("HOPPER LEVEL LOW-LOW NO FEED", "ALM"), ("HOPPER LEVEL LOW-LOW NO FEED", "RTN"))
    allday = [(dt.datetime(2026, 1, 1), dt.datetime(2026, 11, 1))]
    if how == "golden":
        r = G.carbon(target)
    elif how == "nodown":
        r = G.carbon(target, run_spans=allday, empty_spans=[])
    elif how == "runonly":
        r = G.carbon(target, run_spans=run, empty_spans=[])
    elif how == "alarmspan":
        trips = G.spans(ev, ("MOTOR OVERLOAD TRIP", "ALM"), ("MOTOR OVERLOAD TRIP", "RTN"))
        r = G.carbon(target, run_spans=complement(trips), empty_spans=empty)
    elif how == "lowalarm":
        lows = G.spans(ev, ("HOPPER LEVEL LOW", "ALM"), ("HOPPER LEVEL LOW", "RTN"))
        r = G.carbon(target, run_spans=run, empty_spans=lows)
    elif how == "utc":
        back = lambda t: t + dt.timedelta(hours=5 if dt.datetime(2026, 3, 8, 2) <= t < dt.datetime(2026, 11, 1, 2) else 6)
        sp_u = [(back(t), v) for t, v in sp]
        run_u = [(back(a), back(b)) for a, b in run]
        empty_u = [(back(a), back(b)) for a, b in empty]
        r = G.carbon(target, run_spans=run_u, empty_spans=empty_u, sp=sp_u)
    else:
        raise ValueError(how)
    return {m: r[0].get(m, 0.0) for m in PAC_MONTHS}


def complement(sp):
    out, t = [], dt.datetime(2026, 1, 1)
    for a, b in sorted(sp):
        out.append((t, a))
        t = b
    out.append((t, dt.datetime(2026, 11, 1)))
    return out


LOAD_ROUTES = {
    "golden": dict(bottles="golden", offs="golden"),
    "logged": dict(bottles="logged", offs="golden"),
    "position": dict(bottles="position", offs="golden"),
    "mean offset": dict(bottles="golden", offs="mean"),
    "visit offset": dict(bottles="golden", offs="visit"),
    "prorated offset": dict(bottles="golden", offs="prorate"),
    "no offset": dict(bottles="golden", offs="none"),
    "cracker": dict(bottles="logged", offs="mean"),
    "joined, mean offset": dict(bottles="golden", offs="mean"),
    "joined, visit offset": dict(bottles="golden", offs="visit"),
    "joined by position, visit offset": dict(bottles="position", offs="visit"),
}
LOAD_CONVENTIONS = {
    "median offset within each period": dict(bottles="golden", offs="median"),
    "each visit's offset until the next, within each hang": dict(bottles="golden", offs="visit in hang"),
    "offsets prorated between the visits of each hang": dict(bottles="golden", offs="prorate in hang"),
    "logger months read on UTC": dict(bottles="golden", offs="golden", utc_window=True),
}
PAC_ROUTES = ("golden", "nodown", "runonly", "alarmspan", "utc", "lowalarm")
