"""The honest careful-solver cracker, as code on the cut pack, and the pair arithmetic.

Main call routes (each on the shipped files): statistical inventory reconciliation, the field's own method
(daily, weekly and cumulative forms); the quarter's total shortfall per hour; a drift law in months since
calibration; the golden's drift law in litres since calibration.

Ask routes: the cracker lands the call, reads every field for its plain meaning, executes every filed rule and
runs the hygiene battery (one row per delivery report across the monthly pulls, UTC to CST, latest export);
it takes a drop's received litres as the gauge's increase and a bill with no report as unmeasured. The
partial includers handle one device each; the full includer must reproduce figures.json or this exits 1.

Scoring: a call-landing response banks 38 + 7 + 55 L, a response off the call 5 + 7 + 55 L, L the share of
ask figures hit (the same figure to the nearest 10 litres).
"""
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A        # noqa: E402

TD = dt.timedelta
TARGET = os.path.join(os.path.dirname(HERE), "target")


def sir_routes(pk):
    out = {"SIR daily": {}, "SIR weekly": {}, "SIR cumulative": {}}
    q0, q1 = pk.didx[A.Q4[0]], pk.didx[A.Q4[1]] + 1
    for key in sorted(pk.hoses):
        sales, recv, close = pk.book(key)
        v = close[q0:q1] + recv[q0:q1] - sales[q0:q1] - close[q0 + 1:q1 + 1]
        s = sales[q0:q1]
        ok = ~np.isnan(v)
        X = np.c_[np.ones(ok.sum()), s[ok]]
        b = np.linalg.lstsq(X, v[ok], rcond=None)[0]
        out["SIR daily"][key] = b[0] / 24.0
        n = (q1 - q0) // 7
        vw = np.array([np.nansum(v[7 * i:7 * i + 7]) for i in range(n)])
        sw = np.array([s[7 * i:7 * i + 7].sum() for i in range(n)])
        bw = np.linalg.lstsq(np.c_[np.ones(n), sw], vw, rcond=None)[0]
        out["SIR weekly"][key] = bw[0] / (24.0 * 7)
        cv = np.cumsum(np.nan_to_num(v))
        cs = np.cumsum(s)
        t = np.arange(1, len(v) + 1, dtype=float)
        bc = np.linalg.lstsq(np.c_[t, cs], cv, rcond=None)[0]
        out["SIR cumulative"][key] = bc[0] / 24.0
    return out


def months_route(pk):
    """drift in months since calibration: quarter shortfall on sales x mean months since the hoses' resets"""
    rows = []
    q4 = {}
    for key in sorted(pk.hoses):
        site, prod = key
        sales, recv, close = pk.book(key)
        mon = np.zeros(len(pk.days))
        okm = np.ones(len(pk.days), bool)
        fps = sorted(pk.hoses[key])
        for i, d in enumerate(pk.days):
            ms = []
            for fp in fps:
                rs = [r for r in pk.resets[(site, fp, prod)] if r <= d]
                if not rs:
                    okm[i] = False
                    break
                ms.append((d - max(rs)).days / 30.4375)
            if okm[i]:
                mon[i] = np.mean(ms)
        for r in pk.tq:
            if r["key"] != key:
                continue
            i0, i1 = r["i0"], r["i1"]
            if not okm[i0:i1].all():
                continue
            M = (sales[i0:i1] * mon[i0:i1]).sum()
            if r["q"] == (2026, 4):
                q4[key] = (r["short"], M, r["hrs"])
            elif r["q"] <= (2026, 3):
                rows.append((r["short"], M))
    y = np.array([a for a, b in rows])
    x = np.array([b for a, b in rows])
    c = float(x @ y / (x @ x))
    return {k: (s - c * M) / h for k, (s, M, h) in q4.items()}


def main_routes(pk):
    routes = sir_routes(pk)
    routes["total shortfall"] = {k: v["total_lph"] for k, v in pk.q4.items()}
    routes["months law"] = months_route(pk)
    routes["litres law (golden)"] = {k: v["loss_lph"] for k, v in pk.q4.items()}
    return {name: (sorted(k for k, v in r.items() if v > A.THRESHOLD), r) for name, r in routes.items()}


# ----------------------------------------------------------------- the ask

def ask_route(pk, add_drawn=True, rebuild=True, widen=0, both_products=False, russell_local=False, months_by_bill=False):
    tx_all = pk.tx_series()
    if russell_local:
        # reading the host's UTC through Manitoba's wall clock for Russell (daylight time in October)
        for key in list(tx_all):
            if key[0] == "CL-412":
                tx_all[key] = [(s + TD(hours=1) if s < dt.datetime(2026, 11, 1, 1) else s,
                                e + TD(hours=1) if e < dt.datetime(2026, 11, 1, 1) else e, l) for s, e, l in tx_all[key]]
    by_c = defaultdict(float)
    by_s = defaultdict(float)
    for d in pk.drops:
        if d["how"] == "hourly" and not rebuild:
            continue
        a, b = d["window"]
        a, b = a - TD(minutes=widen), b + TD(minutes=widen)
        if d["how"] == "report":
            inc = d["received"] - d["drawn"]
            got = inc
            if add_drawn:
                keys = [(d["site"], "D"), (d["site"], "R")] if both_products else [(d["site"], d["prod"])]
                got += sum(pk.drawn(tx_all, k, a, b) for k in keys)
        else:
            got = d["received"]
        short = d["net"] - got
        m = d["loaded"].month if months_by_bill else d["when"].month
        by_c[(d["carrier"], m)] += short
        by_s[(d["site"], m)] += short
    return by_c, by_s


def loaded_date_route(pk):
    """the rival dating: every drop whose bill was loaded in the quarter, in the month its bill was loaded"""
    by_c = defaultdict(float)
    by_s = defaultdict(float)
    for d in pk.all_drops:
        if "2026-10-01" <= d["loaded_day"] <= "2026-12-31":
            m = int(d["loaded_day"][5:7])
            by_c[(d["carrier"], m)] += d["short"]
            by_s[(d["site"], m)] += d["short"]
    return by_c, by_s


def moved_cells(route, figs):
    by_c, by_s = route
    out = {}
    for k, v in figs["cardlock_short_by_carrier"].items():
        c, m = k.split("|")
        alt = A.r10(by_c.get((c, int(m)), 0.0))
        if alt != v:
            out[k] = (alt, v)
    for k, v in figs["cardlock_short_by_site"].items():
        s, m = k.split("|")
        alt = A.r10(by_s.get((s, int(m)), 0.0))
        if alt != v:
            out[k] = (alt, v)
    return out


def score(route, figs):
    by_c, by_s = route
    hits = 0
    total = 0
    for k, v in figs["cardlock_short_by_carrier"].items():
        c, m = k.split("|")
        total += 1
        hits += A.r10(by_c.get((c, int(m)), 0.0)) == v
    for k, v in figs["cardlock_short_by_site"].items():
        s, m = k.split("|")
        total += 1
        hits += A.r10(by_s.get((s, int(m)), 0.0)) == v
    return hits, total


def main():
    pk = A.run(TARGET)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    golden = sorted(pk.designated)
    print("MAIN CALL ROUTES (set of systems over 0.75 L/h)")
    mains = main_routes(pk)
    for name, (st, r) in mains.items():
        print("  %-22s %-44s lands=%s" % (name, ", ".join("%s %s" % k for k in st) or "none", st == golden))
    cheap = [n for n, (st, r) in mains.items() if st == golden and "golden" not in n]
    print("  cheap routes landing the call:", cheap or "none")
    routes = {
        "cracker (plain meaning, hygiene, unreported bill unmeasured)": dict(add_drawn=False, rebuild=False),
        "cracker, months by bill": dict(add_drawn=False, rebuild=False, months_by_bill=True),
        "fills during the drop only": dict(add_drawn=True, rebuild=False),
        "rebuild from hourly only": dict(add_drawn=False, rebuild=True),
        "both, fills of both products": dict(add_drawn=True, rebuild=True, both_products=True),
        "both, window widened 15 min": dict(add_drawn=True, rebuild=True, widen=15),
        "both, Russell read on wall clock": dict(add_drawn=True, rebuild=True, russell_local=True),
        "full includer": dict(add_drawn=True, rebuild=True),
    }
    print("ASK ROUTES (figures hit of the cardlock table)")
    res = {}
    for name, kw in routes.items():
        h, t = score(ask_route(pk, **kw), figs)
        res[name] = (h, t)
        print("  %-62s %2d / %d" % (name, h, t))
    ld = loaded_date_route(pk)
    h, t = score(ld, figs)
    res["full includer, drops dated by the bill's loaded date"] = (h, t)
    print("  %-62s %2d / %d   (the prompt dates each drop by the day it arrived)" %
          ("full includer, drops dated by the bill's loaded date", h, t))
    h_full, t = res["full includer"]
    L_cr = res["cracker (plain meaning, hygiene, unreported bill unmeasured)"][0] / t
    L_best_partial = max(v[0] for k, v in res.items() if k != "full includer") / t
    on_call = 38 + 7 + 55 * L_cr
    off_call = 5 + 7 + 55 * L_cr
    pair = (on_call + off_call) / 2
    print("SCORING")
    print("  careful response on the call: %.1f; off the call: %.1f; pair %.1f" % (on_call, off_call, pair))
    print("  two careful on-call responses: %.1f and %.1f" % (on_call, on_call))
    print("  best partial includer on the call: %.1f" % (45 + 55 * L_best_partial))
    fail = []
    if res["cracker (plain meaning, hygiene, unreported bill unmeasured)"][0] != 0:
        fail.append("the cracker hits an ask figure")
    if pair > 60:
        fail.append("pair over 60")
    if on_call >= 70:
        fail.append("careful on-call response at or over 70")
    if h_full != t:
        fail.append("the full includer does not reproduce figures.json")
    if cheap:
        fail.append("a cheap route lands the call")
    json.dump(dict(main={k: [list(x) for x in v[0]] for k, v in mains.items()}, ask={k: list(v) for k, v in res.items()},
                   on_call=on_call, off_call=off_call, pair=pair), open(os.path.join(HERE, "ceiling.json"), "w"),
              indent=1, sort_keys=True)
    print("RESULT:", "FAIL " + "; ".join(fail) if fail else "PASS")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
