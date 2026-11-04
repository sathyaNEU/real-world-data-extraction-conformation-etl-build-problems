"""The Merrin Water Treatment Plant's own records, built from the world's truth.

- The daily raw-water sample (07:30 at the raw-water tap): an ELISA screen every day from 15 April, otherwise
  weekly; a GC/MS confirmation at the State Hygienic Laboratory on routine weeks and whenever the screen reaches
  2.5 ug/L. The day's result is the confirmation where one was run, otherwise the screen (SOP-WQ-07 2.3).
- Boundary days are closed in the record: no reported result in (3.00, 3.05], so a source that put a few
  hundredths into the raw water cannot carry a day across the trigger.
- The carbon feed: the operators start powdered activated carbon when the day's result exceeds 3.0 ug/L, set the
  dose from the result, and stop after two results in a row at or below 2.5 ug/L. The feeder's setpoint changes
  are logged; it stops on a motor overload until an operator restarts it, and feeds nothing while its hopper is
  empty until the hopper is refilled.
- The raw-water pumping rate is set once a day at 06:00 and held, so a day's flow is one rate."""
import datetime as dt
import math

import numpy as np

import world as W

LB_PER_MG_PER_MGL = 8.34


def results(rng, rec):
    """Per day: truth, ELISA screen (or None), GC/MS confirmation (or None), reported result, sample time."""
    out = []
    for r in rec:
        d = r["date"]
        i = r["i"]
        truth = r["intake"]
        daily = d >= dt.date(2026, 4, 15)
        weekly = d.weekday() == 1          # Tuesdays outside the daily season
        screen = conf = None
        hh, mm = 7, int(rng.integers(18, 44))
        if daily or weekly:
            for _ in range(200):
                e = truth * 1.075 * math.exp(rng.normal(0, 0.055))
                screen = max(0.05, round(e, 2))
                routine_conf = (d.weekday() == 1 and d.isocalendar()[1] % 2 == 0)
                want_conf = screen >= 2.5 or routine_conf
                conf = None
                if want_conf:
                    conf = max(0.05, round(truth * math.exp(rng.normal(0, 0.035)), 2))
                rep = conf if conf is not None else screen
                if not (3.00 < rep <= 3.05):
                    break
            else:
                raise SystemExit("no clear draw for %s (truth %.3f)" % (d, truth))
        rep = conf if conf is not None else screen
        out.append(dict(i=i, date=d, truth=truth, screen=screen, conf=conf, rep=rep, t=dt.time(hh, mm),
                        raw_temp=r["intake_t"] + float(rng.normal(0, 0.12))))
    return out


def dose_for(result):
    if result > 5.5:
        return 25.0
    if result > 4.0:
        return 18.0
    return 12.0


def flows(rng, rec):
    """The day's raw-water pumping rate (MGD), held from 06:00 to 06:00 the next morning."""
    return [round(r["city_m3s"] / W.MGD, 2) for r in rec]


def carbon(rng, res, mgd):
    """The operators' setpoint log and the feeder's events, in local time. Returns the setpoint changes, the
    feeder events, and the true pounds fed by local calendar day."""
    setpoints = []          # (datetime, mg/L)  0 means feed off
    feeding = False
    below = 0
    cur = 0.0
    for k, r in enumerate(res):
        if r["rep"] is None:
            continue
        d = r["date"]
        t_set = dt.datetime.combine(d, dt.time(10, int(rng.integers(5, 55))))
        if r["rep"] > W.TRIGGER:
            below = 0
            new = dose_for(r["rep"])
            if not feeding or new != cur:
                setpoints.append((t_set, new))
                feeding, cur = True, new
        elif feeding:
            if r["rep"] <= 2.5:
                below += 1
            else:
                below = 0
            if below >= 2:
                setpoints.append((t_set, 0.0))
                feeding, cur, below = False, 0.0, 0
    # feeder faults while feeding, one or two in every month the feed ran: motor overloads (stopped until an
    # operator presses RUN) and an empty hopper (feeding nothing until it is refilled, the feeder still running)
    feeds = []
    for a, b in zip(setpoints, setpoints[1:] + [(dt.datetime(2026, 11, 1), 0.0)]):
        if a[1] > 0:
            feeds.append((a[0], b[0], a[1]))
    events = []
    downtime = []
    picks = []
    kind_cycle = ["overload", "empty"]
    nk = 0
    for month in range(5, 11):
        spans = []
        for s0, e0, dose in feeds:
            a = max(s0, dt.datetime(2026, month, 1))
            b = min(e0, dt.datetime(2026, month + 1, 1) if month < 12 else e0)
            if (b - a).total_seconds() > 14 * 3600:
                spans.append((a, b))
        if not spans:
            continue
        hours = sum((b - a).total_seconds() for a, b in spans) / 3600.0
        nf = 2 if hours > 240 else 1
        chosen = sorted(set(int(x) for x in rng.integers(0, len(spans), nf)))
        for j in chosen:
            a, b = spans[j]
            span_h = (b - a).total_seconds() / 3600.0
            t0 = a + dt.timedelta(hours=float(rng.uniform(0.2, 0.6)) * span_h)
            t0 = t0.replace(second=0, microsecond=0)
            kind = kind_cycle[nk % 2]
            nk += 1
            if kind == "overload":
                rtn = t0 + dt.timedelta(minutes=int(rng.integers(6, 25)))
                run = rtn + dt.timedelta(minutes=int(rng.integers(150, 520)))
                run = min(run, b - dt.timedelta(minutes=30))
                picks.append((kind, t0, rtn, run))
                downtime.append((t0, run))
            else:
                low = t0 - dt.timedelta(minutes=int(rng.integers(40, 160)))
                refill = t0 + dt.timedelta(minutes=int(rng.integers(180, 600)))
                refill = min(refill, b - dt.timedelta(minutes=30))
                picks.append((kind, low, t0, refill))
                downtime.append((t0, refill))
    for p in picks:
        if p[0] == "overload":
            _, t0, rtn, run = p
            events += [(t0, "PAC-FDR-1", "MOTOR OVERLOAD TRIP", "ALM"),
                       (t0 + dt.timedelta(seconds=2), "PAC-FDR-1", "RUN STATUS OFF", "EVT"),
                       (rtn, "PAC-FDR-1", "MOTOR OVERLOAD TRIP", "RTN"),
                       (run, "PAC-FDR-1", "RUN STATUS ON", "EVT")]
        else:
            _, low, t0, refill = p
            events += [(low, "PAC-FDR-1", "HOPPER LEVEL LOW", "ALM"),
                       (t0, "PAC-FDR-1", "HOPPER LEVEL LOW-LOW NO FEED", "ALM"),
                       (refill, "PAC-FDR-1", "HOPPER LEVEL LOW-LOW NO FEED", "RTN"),
                       (refill + dt.timedelta(seconds=20), "PAC-FDR-1", "HOPPER LEVEL LOW", "RTN")]
    # the feeder is started and stopped at the panel when the shift lead enters the setpoint
    prev = 0.0
    for t_, v in sorted(setpoints):
        if v > 0 and prev == 0:
            events.append((t_ + dt.timedelta(seconds=30), "PAC-FDR-1", "RUN STATUS ON", "EVT"))
        elif v == 0 and prev > 0:
            events.append((t_ + dt.timedelta(seconds=30), "PAC-FDR-1", "RUN STATUS OFF", "EVT"))
        prev = v
    # the hopper running low and topped up in time, on feeding days away from the faults
    for s0, e0, dose in feeds:
        day = s0.date()
        while dt.datetime.combine(day, dt.time(0)) < e0:
            if rng.random() < 0.3:
                t1 = dt.datetime.combine(day, dt.time(int(rng.integers(0, 24)), int(rng.integers(0, 60))))
                t2 = t1 + dt.timedelta(minutes=int(rng.integers(25, 110)))
                clear = all(abs((t1 - q[1]).total_seconds()) > 86400 and abs((t1 - q[2]).total_seconds()) > 86400
                            for q in picks)
                if s0 + dt.timedelta(hours=2) <= t1 and t2 <= e0 - dt.timedelta(hours=2) and clear:
                    events += [(t1, "PAC-FDR-1", "HOPPER LEVEL LOW", "ALM"), (t2, "PAC-FDR-1", "HOPPER LEVEL LOW", "RTN")]
            day += dt.timedelta(days=1)
    # true pounds fed by local calendar day: dose (mg/L) x the day's rate (MGD, held 06:00 to 06:00) x 8.34,
    # integrated over the minutes the feeder ran with carbon in the hopper
    lb = {}
    t = dt.datetime(2026, 1, 1, 0, 0)
    step = dt.timedelta(minutes=1)
    sp = sorted(setpoints)
    k = 0
    cur = 0.0
    down = sorted(downtime)
    di_ = 0
    end = dt.datetime(2026, 11, 1, 0, 0)
    mgd_by_day = {W.day(i): mgd[i] for i in range(len(mgd))}
    while t < end:
        while k < len(sp) and sp[k][0] <= t:
            cur = sp[k][1]
            k += 1
        if cur > 0:
            off = any(a <= t < b for a, b in down)
            if not off:
                pump_day = (t - dt.timedelta(hours=6)).date()
                rate = mgd_by_day.get(pump_day, mgd[0])
                lb[t.date()] = lb.get(t.date(), 0.0) + cur * rate * LB_PER_MG_PER_MGL / 1440.0
        t += step
    return sp, sorted(events), lb, downtime


def alarm_history(rng, events, res, setpoints):
    """The plant's SCADA alarm and event history: the carbon feeder's events among everything else the plant
    alarms on, in local time (written out in UTC as the historian stores them)."""
    tags = [("FLT-03", "FILTER 3 HEADLOSS HIGH"), ("FLT-01", "FILTER 1 TURBIDITY HIGH"), ("FLT-05", "FILTER 5 BACKWASH COMPLETE"),
            ("FLT-02", "FILTER 2 BACKWASH COMPLETE"), ("FLT-04", "FILTER 4 BACKWASH COMPLETE"), ("FLT-06", "FILTER 6 BACKWASH COMPLETE"),
            ("RWP-2", "RAW WATER PUMP 2 RUN STATUS ON"), ("RWP-2", "RAW WATER PUMP 2 RUN STATUS OFF"),
            ("RWP-3", "RAW WATER PUMP 3 RUN STATUS ON"), ("RWP-3", "RAW WATER PUMP 3 RUN STATUS OFF"),
            ("CL2-1", "CHLORINE RESIDUAL LOW"), ("CL2-1", "CHLORINE CYLINDER SWITCHOVER"),
            ("LIME-1", "LIME SLAKER TEMPERATURE HIGH"), ("LIME-2", "LIME FEEDER 2 HOPPER LEVEL LOW"),
            ("CW-1", "CLEARWELL LEVEL LOW"), ("HSP-1", "HIGH SERVICE PUMP 1 RUN STATUS ON"),
            ("HSP-1", "HIGH SERVICE PUMP 1 RUN STATUS OFF"), ("HSP-4", "HIGH SERVICE PUMP 4 RUN STATUS ON"),
            ("HSP-4", "HIGH SERVICE PUMP 4 RUN STATUS OFF"), ("SCADA", "PLC-2 COMMUNICATION FAIL"),
            ("BLDG", "CHEMICAL ROOM DOOR OPEN"), ("FLU-1", "FLUORIDE FEED RATE DEVIATION"),
            ("ALUM-1", "ALUM DAY TANK LEVEL LOW"), ("SED-2", "BASIN 2 SLUDGE BLANKET HIGH")]
    weights = np.array([1.0, 0.8, 1.3, 1.3, 1.3, 1.3, 1.6, 1.6, 1.4, 1.4, 0.7, 0.5, 0.4, 0.6, 0.3, 1.9, 1.9, 1.2, 1.2,
                        0.35, 0.8, 0.6, 0.5, 0.45])
    weights = weights / weights.sum()
    rows = []
    t = dt.datetime(2026, 1, 1, 0, 0)
    end = dt.datetime(2026, 11, 1, 0, 0)
    while t < end:
        busy = 1.6 if 6 <= t.hour < 22 else 0.6
        t += dt.timedelta(minutes=float(rng.exponential(14.0 / busy)))
        tag, desc = tags[int(rng.choice(len(tags), p=weights))]
        kind = "EVT" if ("STATUS" in desc or "COMPLETE" in desc or "SWITCHOVER" in desc) else "ALM"
        rows.append((t.replace(microsecond=0), tag, desc, kind))
        if kind == "ALM" and rng.random() < 0.93:
            rows.append(((t + dt.timedelta(minutes=float(rng.exponential(18.0)) + 0.3)).replace(microsecond=0),
                         tag, desc, "ACK"))
            rows.append(((t + dt.timedelta(minutes=float(rng.exponential(55.0)) + 1.0)).replace(microsecond=0),
                         tag, desc, "RTN"))
    # the carbon system's dust collector trips on its pressure switch while bags are emptied into the hopper,
    # on feeding days and now and then on the days carbon is delivered and loaded
    sp = sorted(setpoints)
    feeding = [(t0, nxt[0]) for (t0, v), nxt in zip(sp, sp[1:] + [(end, 0.0)]) if v > 0]
    day = dt.date(2026, 1, 1)
    while day < end.date():
        on = any(a.date() <= day <= b.date() for a, b in feeding)
        n = int(rng.poisson(1.4 if on else 0.04))
        for _ in range(n):
            t1 = dt.datetime.combine(day, dt.time(int(rng.integers(6, 20)), int(rng.integers(0, 60)), int(rng.integers(0, 60))))
            rows.append((t1, "PAC-FDR-1", "DUST COLLECTOR DIFFERENTIAL PRESSURE HIGH", "ALM"))
            rows.append(((t1 + dt.timedelta(minutes=float(rng.exponential(9.0)) + 0.4)).replace(microsecond=0), "PAC-FDR-1",
                         "DUST COLLECTOR DIFFERENTIAL PRESSURE HIGH", "ACK"))
            rows.append(((t1 + dt.timedelta(minutes=float(rng.exponential(25.0)) + 2.0)).replace(microsecond=0), "PAC-FDR-1",
                         "DUST COLLECTOR DIFFERENTIAL PRESSURE HIGH", "RTN"))
        day += dt.timedelta(days=1)
    for e in events:
        rows.append(e)
        if e[3] == "ALM":
            rows.append(((e[0] + dt.timedelta(minutes=float(rng.uniform(1.5, 22.0)))).replace(microsecond=0), e[1], e[2], "ACK"))
    rank = {"ALM": 0, "EVT": 1, "ACK": 2, "RTN": 3}
    rows.sort(key=lambda x: (x[0], rank[x[3]], x[1], x[2]))
    return rows
