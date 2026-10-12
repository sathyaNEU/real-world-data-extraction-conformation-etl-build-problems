"""Last summer at the eight checkpoints, 15 June to 31 August 2026: each day's arrivals, the host's lanes (the summer
roster plan less lane faults, or less the lanes its duty managers stood down while the mobile unit screened there),
the unit's three lanes, the two staff and aircrew lanes at the shift changes, the queue, each lane's passengers
screened by 15 minutes and the queue-time sensor. One random stream per airport and purpose, so the build is
byte-identical run to run."""
import datetime as dt

import numpy as np

import models as M
import profiles as PR
import world as W

MONTH = {6: 0.95, 7: 1.0, 8: 1.02}
DOW = [1.02, 0.97, 0.97, 1.01, 1.04, 0.98, 1.01]        # Monday first
STAFF_PEAK = {"CUL": 30, "ARD": 26, "FAR": 25, "HAL": 17, "ESK": 21, "BRN": 18, "DRM": 18, "GLK": 15}
FAULTS = [("XR-GEN", "X-ray generator fault"), ("XR-BELT", "Conveyor belt stopped"),
          ("ETD", "Trace detection unit out of calibration"), ("TRAY", "Tray return jammed"),
          ("WTMD", "Walk-through detector alarm fault"), ("PWR", "Lane power trip")]
# each checkpoint opens its lanes in its own order of preference
ORDER = {
    "CUL": [3, 4, 2, 5, 6, 1, 7, 8, 9], "ARD": [2, 3, 4, 1, 5, 6, 7, 8], "FAR": [4, 5, 3, 6, 2, 7, 1, 8],
    "HAL": [2, 3, 1, 4, 5], "ESK": [3, 2, 4, 1, 5, 6, 7], "BRN": [1, 2, 3, 4, 5, 6], "DRM": [2, 1, 3, 4, 5, 6],
    "GLK": [1, 2, 3, 4, 5],
}
TEAM_IDS = ["M1", "M2", "M3"]


def lane_id(n):
    return "L%02d" % n


def staff_ids(code):
    n = W.LANES[code]
    return [lane_id(n + 1), lane_id(n + 2)]


def rng_for(code, purpose):
    return np.random.default_rng([W.SEED, W.CODES.index(code), purpose])


def faults_for(code, days):
    """Lane faults on the days the unit was elsewhere: (date, lane number, first interval, last interval, code)."""
    g = rng_for(code, 1)
    out = []
    for d in days:
        if W.host_on(d) == code:
            continue
        if g.random() < 0.22:
            n_open = int(W.CHECKPOINT[code][1])
            lane = ORDER[code][int(g.integers(0, n_open))]
            start = int(g.integers(4, 46))
            length = int(g.integers(3, 14))
            kind = FAULTS[int(g.integers(0, len(FAULTS)))]
            out.append((d, lane, start, min(W.T - 1, start + length - 1), kind))
    return out


def simulate_airport(code, days):
    plan = PR.plan(code)
    shape = PR.shape(code, W.DEMAND26[code])
    g = rng_for(code, 2)
    gs = rng_for(code, 3)
    faults = faults_for(code, days)
    fault_on = {}
    for d, lane, s, e, kind in faults:
        fault_on.setdefault(d, []).append((lane, s, e))
    lane_rows, wait_rows, daily = [], [], []
    for d in days:
        posted = W.host_on(d) == code
        f = MONTH[d.month] * DOW[d.weekday()] * (1 + 0.02 * g.standard_normal())
        arr = np.maximum(0, np.round(shape * f * (1 + 0.04 * g.standard_normal(W.T)))).astype(int)
        host = plan - (M.release(code, plan) if posted else 0)
        open_lanes = []                                   # per interval: list of lane ids
        for i in range(W.T):
            k = int(host[i])
            down = {ln for ln, s, e in fault_on.get(d, []) if s <= i <= e}
            ids = [lane_id(n) for n in ORDER[code][:k] if n not in down]
            if posted and M.TEAM_ON[i]:
                ids += TEAM_IDS
            open_lanes.append(ids)
        q, over, wait = 0.0, 0, np.zeros(W.T)
        screened = np.zeros(W.T, int)
        caps = []
        for i in range(W.T):
            cap_i = 37.5 * (0.93 + 0.14 * g.random(len(open_lanes[i])))
            c = float(cap_i.sum())
            caps.append(cap_i)
            wait[i] = 15.0 * (q + arr[i] / 2.0) / c
            if wait[i] > W.STANDARD_MIN:
                over += arr[i]
            s_i = min(c, q + arr[i])
            q = q + arr[i] - s_i
            screened[i] = int(round(s_i))
        if q > 0.5:
            raise RuntimeError("queue left at close: %s %s %.0f" % (code, d, q))
        # passengers screened by lane: shared in proportion to each lane's pace, whole passengers
        for i in range(W.T):
            ids = open_lanes[i]
            share = caps[i] / caps[i].sum()
            raw = screened[i] * share
            base = np.floor(raw).astype(int)
            rem = screened[i] - base.sum()
            if rem:
                frac = raw - base + 1e-9 * g.random(len(ids))
                base[np.argsort(-frac)[:rem]] += 1
            for lid, n in zip(ids, base):
                lane_rows.append((code, lid, d, i, int(n)))
        # staff and aircrew search at the shift changes
        for j, lid in enumerate(staff_ids(code)):
            for i in list(range(0, 4)) + list(range(68, 72)):
                lvl = STAFF_PEAK[code] * (1.0 if i in (1, 2, 69, 70) else 0.55) * (0.9 + 0.1 * j)
                n = int(max(1, round(lvl * (1 + 0.18 * gs.standard_normal()))))
                lane_rows.append((code, lid, d, i, n))
        measured = np.maximum(0.3, wait * (1 + 0.05 * gs.standard_normal(W.T)) + 0.3 * gs.standard_normal(W.T))
        for i in range(W.T):
            wait_rows.append((code, d, i, round(float(measured[i]), 1)))
        daily.append({"date": d, "posted": posted, "arrivals": int(arr.sum()), "screened": int(screened.sum()),
                      "over": int(over), "host_lanes": host.copy(), "open": [len(x) for x in open_lanes]})
    return {"lanes": lane_rows, "waits": wait_rows, "daily": daily, "faults": faults}


def sensor_gaps(wait_rows):
    """The queue-time sensors drop out now and then for a few intervals (camera resets); those rows are absent."""
    g = np.random.default_rng([W.SEED, 99])
    keep, i, n = [], 0, len(wait_rows)
    while i < n:
        if g.random() < 0.0012:
            i += int(g.integers(1, 7))
            continue
        keep.append(wait_rows[i])
        i += 1
    return keep


def simulate_all():
    days = W.summer26_days()
    out = {c: simulate_airport(c, days) for c in W.CODES}
    waits = sensor_gaps([r for c in W.CODES for r in out[c]["waits"]])
    return {"days": days, "airports": out, "waits": waits}
