"""Assembles the whole simulated truth for task466 from world.py and records.py.

The graded quarter figures (each engine's operating hours, the flare's operating hours and the methane destroyed in
the flare) are moved off their rounding edges by realistic free parameters: the length of a scheduled engine stop
in that quarter (oil changes run five to seven hours) and the flare's warm-up time after an ignition. No figure is
set by hand; each nudge is a few minutes on a record the plant really keeps."""
import numpy as np

import records as R
import world as W


def flare_event_lines(lit, permissive):
    ev = []
    change = np.flatnonzero((lit[1:] != lit[:-1]) | (permissive[1:] != permissive[:-1])) + 1
    prev_l, prev_p = bool(lit[0]), bool(permissive[0])
    since_start_permissive = prev_p
    for m in change:
        l, pm = bool(lit[m]), bool(permissive[m])
        if l and not prev_l:
            ev.append((int(m), "FLR", "FLARE START", "pilot proven, main burner lit"))
            since_start_permissive = False
            if pm:
                ev.append((int(m), "FLR", "TEMP PERMISSIVE", "combustion temperature at setpoint"))
                since_start_permissive = True
        elif not l and prev_l:
            ev.append((int(m), "FLR", "FLARE STOP", "no gas demand"))
        elif l:
            if pm and not prev_p:
                if not since_start_permissive:
                    ev.append((int(m), "FLR", "TEMP PERMISSIVE", "combustion temperature at setpoint"))
                    since_start_permissive = True
                else:
                    ev.append((int(m), "FLR", "TEMP NORMAL", "combustion temperature at setpoint"))
            elif not pm and prev_p:
                ev.append((int(m), "FLR", "LOW TEMP", "combustion temperature below setpoint"))
        prev_l, prev_p = l, pm
    return ev


def resync_minutes(events, e, a, b):
    tag = "GEN%d" % e
    tot = 0
    opened = None
    for m, u, c, _ in events:
        if u != tag:
            continue
        if c == "BREAKER OPEN":
            opened = m
        elif c == "RUNNING" and opened is not None:
            if a <= opened < b:
                tot += m - opened
            opened = None
        elif c in ("STOP", "TRIP", "CONTROLLER POWER UP"):
            opened = None
    return tot


def edge_dist(v, unit=1.0):
    c = round(v / unit) * unit
    return unit / 2.0 - abs(v - c)


def nudge_engines(p):
    """Centre each engine-quarter's operating hours on a whole hour under both readings of a breaker opening."""
    log = []
    for _ in range(2):
        events = R.engine_events(p)
        for e in (1, 2):
            for q in range(4):
                a, b = R.quarter_minutes(2026, q)
                on_h = p["eng_on_min"][e][a:b].sum() / 60.0
                rs = resync_minutes(events, e, a, b) / 60.0
                mid = on_h - rs / 2.0
                frac = mid - np.floor(mid)
                n = int(round(frac * 60))
                if n == 0 or abs(frac) < 0.05:
                    continue
                ks = [k for k, s in enumerate(p["eng_stops"][e]) if s["kind"] in ("oil", "service") and a <= s["start"] < b
                      and s["end"] + n < b]
                if not ks:
                    ks = [k for k, s in enumerate(p["eng_stops"][e]) if s["kind"] == "trip" and a <= s["start"] < b
                          and s["end"] + n < b]
                W.extend_stop(p, e, ks[0], n)
                log.append((e, q + 1, n))
    return log


def flare_quarter_kg(p, q):
    a, b = R.quarter_hours_utc(2026, q)
    return p["flare_kg"][a:b].sum() * W.DE / 1000.0


def nudge_flare_destroyed(p):
    """Keep each quarter's methane destroyed in the flare at least 0.2 t inside its whole-tonne bin, by lengthening a
    scheduled engine stop in that quarter by whole hours (the engines' hour figures keep their centring)."""
    log = []
    for q in range(4):
        for _ in range(6):
            v = flare_quarter_kg(p, q)
            if edge_dist(v) >= 0.2:
                break
            a, b = R.quarter_minutes(2026, q)
            e = 1 + (q % 2)
            ks = [k for k, s in enumerate(p["eng_stops"][e]) if s["kind"] in ("oil", "trip") and a <= s["start"] < b
                  and s["end"] + 60 < b]
            W.extend_stop(p, e, ks[-1], 60)
            log.append((e, q + 1, 60))
    return log


def nudge_flare_hours(lit, permissive):
    """Centre each quarter's flare operating hours by lengthening one warm-up after an ignition in that quarter."""
    log = []
    for q in range(4):
        a, b = R.quarter_minutes(2026, q)
        h = permissive[a:b].sum() / 60.0
        frac = h - np.floor(h)
        n = int(round(frac * 60))
        if n == 0 or abs(frac) < 0.05:
            continue
        starts = np.flatnonzero(lit[a + 1:b] & ~lit[a:b - 1]) + a + 1
        for s in starts:
            # the first permissive minute after this ignition
            seg = permissive[s:s + 200]
            if not seg.any():
                continue
            j = s + int(np.argmax(seg))
            if lit[j:j + n + 5].all() and permissive[j:j + n].all():
                permissive[j:j + n] = False
                log.append((q + 1, n))
                break
    return log


def build_truth():
    p = W.build()
    nudges = dict(engines=nudge_engines(p))
    nudges["flare_kg"] = nudge_flare_destroyed(p)
    lit, permissive = R.flare_states(p)
    nudges["flare_h"] = nudge_flare_hours(lit, permissive)
    eng_ev = R.engine_events(p)
    flr_ev = flare_event_lines(lit, permissive)
    events = sorted(eng_ev + flr_ev, key=lambda x: (x[0], x[1], x[2]))
    walks = R.surface_walkovers(p)
    checks = R.calibration_log(walks)
    t = dict(plant=p, flare_lit=lit, flare_perm=permissive, flare_lit_h=lit.reshape(W.NH, 60).mean(axis=1),
             events=events, walks=walks, checks=checks, weather=R.weather(p), leachate=R.leachate(p),
             weighbridge=R.weighbridge_archive(), engine_truth=R.engine_truth(p), nudges=nudges)
    return t
