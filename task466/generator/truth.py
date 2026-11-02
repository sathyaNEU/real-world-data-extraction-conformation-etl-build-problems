"""Assembles the whole simulated truth for task466 from world.py and records.py."""
import numpy as np

import records as R
import world as W


def flare_event_lines(lit, permissive):
    ev = []
    n = len(lit)
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


def build_truth():
    p = W.build()
    lit, permissive = R.flare_states(p)
    eng_ev = R.engine_events(p)
    flr_ev = flare_event_lines(lit, permissive)
    events = sorted(eng_ev + flr_ev, key=lambda x: (x[0], x[1], x[2]))
    walks = R.surface_walkovers(p)
    checks = R.calibration_log(walks)
    t = dict(plant=p, flare_lit=lit, flare_perm=permissive, flare_lit_h=lit.reshape(W.NH, 60).mean(axis=1),
             events=events, walks=walks, checks=checks, weather=R.weather(p), leachate=R.leachate(p),
             weighbridge=R.weighbridge_archive(), engine_truth=R.engine_truth(p))
    return t
