"""The pair ceiling for task466, measured as code on the cut pack (supplemental-stumping Part 0 and 1.1).

    python3 task466/generator/ceiling.py

Weights: the call 20 and the three critical components 6 each (38), instruction-following 7, the asks 55 spread
evenly over their 32 graded cells. The cracker lands the call and takes the careful solver's route through every ask:
it executes every filed rule (rule 1.8's starts from standstill, the 1400 F threshold the log states, plan 7.3's void
rule, the 500 ppm above background), and it meets each silent device the way that route meets it: the run before a
power failure is closed at the CONTROLLER POWER UP line (no stop is written; the stop minute sits only in the blower
outage log), the event log's site time is subtracted as written (no offset is printed beside it), the flare's methane is
read from the flare's own meter at the rule's normal density, and re-checks are matched to a walkover by the plan's ten
days. The mirror stops at the running-share rung of the call (Tier 3) and keeps the captured methane; its asks are the
cracker's asks (the conservative case, since the asks do not depend on the call). Sensitivity rows print what the
cracker keeps when it also handles the clock, and the clock and the power failures.
"""
import datetime as dt
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as C     # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
W_CALL, W_COMP, W_IF, W_ASK = 20.0, 6.0, 7.0, 55.0


def naive_clock(fn, *args, **kw):
    """Run fn with the event log's site time read as written (no zone) and the quarters taken on that clock."""
    orig = (A.read_events, A.quarter_bounds, A.year_bounds)
    try:
        A.read_events = lambda target: [dict(x, t=dt.datetime.strptime(x["local"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=C.UTC))
                                        for x in orig[0](target)]
        A.quarter_bounds = lambda y, q: (dt.datetime(y, (1, 4, 7, 10)[q - 1], 1, tzinfo=C.UTC),
                                         dt.datetime(y, (1, 4, 7, 10)[q - 1] + 3, 1, tzinfo=C.UTC) if q < 4
                                         else dt.datetime(y + 1, 1, 1, tzinfo=C.UTC))
        A.year_bounds = lambda y: (dt.datetime(y, 1, 1, tzinfo=C.UTC), dt.datetime(y + 1, 1, 1, tzinfo=C.UTC))
        return fn(*args, **kw)
    finally:
        A.read_events, A.quarter_bounds, A.year_bounds = orig


def local_as_utc(outs):
    return [dict(o, start=o["start"].astimezone(C.TZ).replace(tzinfo=C.UTC), end=o["end"].astimezone(C.TZ).replace(tzinfo=C.UTC))
            for o in outs]


def ask_cells(handle_clock, handle_power, d, outs):
    if handle_clock:
        eng = A.engine_answers(T, outs, use_outage_log=handle_power)
        flh = A.flare_answers(T, d, outs)
    else:
        eng = naive_clock(A.engine_answers, T, local_as_utc(outs), use_outage_log=handle_power)
        flh = naive_clock(A.flare_answers, T, d, local_as_utc(outs))
    fld = A.flare_answers(T, d, outs)
    sem = A.sem_answers(T, void_rule=True, match="window")
    cells = {}
    for q in (1, 2, 3, 4):
        for e in (1, 2):
            cells["engine%d_hours_q%d" % (e, q)] = int(round(eng[(e, q)]["hours"]))
            cells["engine%d_starts_q%d" % (e, q)] = eng[(e, q)]["starts"]
        cells["flare_hours_q%d" % q] = int(round(flh[q]["hours"]))
        cells["flare_destroyed_t_q%d" % q] = int(round(fld[q]["destroyed_meter_normal"]))
        cells["sem_exceed_q%d" % q] = sem[q]["exceed"]
        cells["sem_still_q%d" % q] = sem[q]["still"]
    return cells


ASKS = {
    "engines: hours and starts by quarter": [k for k in F if k.startswith("engine")],
    "flare: hours and methane destroyed by quarter": [k for k in F if k.startswith("flare_")],
    "walkovers: exceedance locations and still over at first re-monitoring": [k for k in F if k.startswith("sem_") and k[-2] == "q"],
}
ALL = [k for v in ASKS.values() for k in v]


def kept(cells):
    return {k: cells[k] == F[k] for k in ALL}


def score(on_call, comps_kept, k):
    ask = W_ASK * sum(k.values()) / len(k)
    return (W_CALL if on_call else 0.0) + W_COMP * comps_kept + W_IF + ask, ask


def main():
    d = A.read_scada(T)
    outs = A.read_outages(T)
    digest = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:8]
    crack = kept(ask_cells(False, False, d, outs))
    c_score, c_ask = score(True, 3, crack)
    m_score, m_ask = score(False, 1, crack)
    pair = (c_score + m_score) / 2.0
    print("pack target.zip %s; %d graded ask cells over %d asks" % (digest, len(ALL), len(ASKS)))
    print("%-72s %s" % ("ask (cracker)", "cells kept / verdict"))
    for name, keys in ASKS.items():
        n = sum(crack[k] for k in keys)
        print("%-72s %d of %d  %s" % (name, n, len(keys), "miss" if n < len(keys) else "KEPT WHOLE"))
    print("cracker: on the call, %.1f of 55 ask points (%.1f per cent), total %.1f" % (c_ask, 100 * c_ask / W_ASK, c_score))
    print("mirror: off the call at Tier 3, captured kept, the cracker's asks: total %.1f" % m_score)
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * m_ask / W_ASK))
    for label, hc, hp in (("cracker also handles the daylight-saving clock", True, False),
                          ("cracker handles the clock and the power-failure stops", True, True)):
        kk = kept(ask_cells(hc, hp, d, outs))
        cs, ca = score(True, 3, kk)
        ms, ma = score(False, 1, kk)
        print("sensitivity, %s: keeps %.1f per cent of the asks, pair %.1f" % (label, 100 * ca / W_ASK, (cs + ms) / 2.0))
    return pair


if __name__ == "__main__":
    p = main()
    sys.exit(0 if p <= 60.0 else 1)
