"""task162 calibration (run by hand, never by build.py): the per-district multipliers on background leakage that
put every graded figure mid-bin. Two runs measure each figure's slope against its multiplier; the multipliers that
centre each figure in its printed cell are then printed for world.LEAK_TUNE. Phase 3 shares one multiplier, chosen so
the reduction, the two years and the shortfall all clear their rounding edges by a quarter of a step or more.

    python3 task162/generator/tune.py <scratch dir>            the leakage multipliers (Ask A and the call)
    python3 task162/generator/tune.py balance <scratch dir>    the zone balance's knobs (Ask B)"""
from __future__ import annotations

import importlib
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402


def run(out, tune):
    import world as W
    import records as R
    import calc as C
    W.LEAK_TUNE.clear()
    W.LEAK_TUNE.update(tune)
    T = W.simulate()
    F, inl, zon = R.logger_series(T)
    os.makedirs(out, exist_ok=True)
    K.write_csv(os.path.join(out, R.F_INLET), R.INLET_COLS, inl)
    K.write_csv(os.path.join(out, R.F_ZONE), R.ZONE_COLS, zon)
    K.write_csv(os.path.join(out, R.F_LOGGERS), R.LOGGER_COLS, R.logger_register_rows(F))
    K.write_csv(os.path.join(out, R.F_DISTRICTS), R.DISTRICT_COLS, R.district_rows(T))
    K.write_csv(os.path.join(out, R.F_CODES), R.CODE_COLS, R.CODE_HISTORY)
    props = R.properties(T)
    K.write_csv(os.path.join(out, R.F_PROPS), R.PROP_COLS, R.property_rows(props))
    N1 = {p["code"]: p["n1"] for p in T["P"]}
    S = {p["code"]: p["setting"] for p in T["P"] if p["phase"] == 3}
    P = C.Pack(out, N1, S)
    a = C.ask_a(P, W.NEAR)
    c = C.call(P, W.PHASE3)
    return a, c


def clear(x, step):
    return K.bin_clearance(x, step)


def main(out):
    a0, c0 = run(out, {})
    up = {code: 1.03 for code in a0}
    up.update({code: 1.03 for code in __import__("world").PHASE3})
    a1, c1 = run(out, up)
    tune = {}
    for code in a0:
        slope = (a1[code] - a0[code]) / 0.03
        target = round(a0[code], 3)
        tune[code] = round(1.0 + (target - a0[code]) / slope, 4)
    # Phase 3: one multiplier on a grid, linear in the slopes
    best = None
    for f in np.arange(0.90, 1.10001, 0.0025):
        d = f - 1.0
        vals = {k: c0[k] + (c1[k] - c0[k]) / 0.03 * d for k in ("base", "fc", "reduction")}
        vals["shortfall"] = K.TARGET - vals["reduction"]
        m = min(clear(vals["base"], 0.01), clear(vals["fc"], 0.01), clear(vals["reduction"], 0.01),
                clear(vals["shortfall"], 0.01), K.ceil_clearance(vals["shortfall"], K.GANG_YIELD))
        if best is None or m > best[0] + 1e-9 or (abs(m - best[0]) < 1e-9 and abs(d) < abs(best[1] - 1)):
            best = (m, f, vals)
    for code in __import__("world").PHASE3:
        tune[code] = round(best[1], 4)
    print("LEAK_TUNE = %r" % tune)
    print("phase 3 multiplier %.4f, min clearance %.2f, predicted %s" % (best[1], best[0], best[2]))
    a2, c2 = run(out, tune)
    for code in a2:
        print(code, "%.5f" % a2[code], "clearance %.2f" % clear(a2[code], 0.001))
    print("call", {k: round(c2[k], 5) for k in ("base", "fc", "reduction", "shortfall", "gangs")},
          "clearances", [round(clear(c2[k], 0.01), 2) for k in ("base", "fc", "reduction", "shortfall")])


def balance_run(out):
    import world as W
    import records as R
    import calc as C
    T = W.simulate()
    os.makedirs(out, exist_ok=True)
    K.write_csv(os.path.join(out, R.F_DISTRICTS), R.DISTRICT_COLS, R.district_rows(T))
    K.write_csv(os.path.join(out, R.F_CODES), R.CODE_COLS, R.CODE_HISTORY)
    props = R.properties(T)
    K.write_csv(os.path.join(out, R.F_PROPS), R.PROP_COLS, R.property_rows(props))
    b = R.bills(T, props)
    K.write_csv(os.path.join(out, R.F_BILLS), R.BILL_COLS, b)
    K.write_csv(os.path.join(out, R.F_OUTLET), R.OUTLET_COLS, R.outlet_daily(T, b))
    g = C.ask_b(out)
    lo = C.ask_b(out, "multiply")
    lo2 = C.ask_b(out, "exclusive")
    # the corridor's low ends: each target sits half the corridor above its cell's centre
    g["siv_off"] = (g["siv"] - lo["siv"]) / 2.0
    g["real_off"] = (g["real"] - min(lo["real"], lo2["real"], g["real"] + (lo["real"] - g["real"]) + (lo2["real"] - g["real"]))) / 2.0
    n_unm = 0.9 * sum(1 for x in props if x["basis"] == "unmeasured" and not x["flat"] and x["code"][:2] == "NZ")
    return g, float(np.mean(T["ind"])), n_unm


def balance(out):
    """The zone balance's three knobs (the mill's draw, the trunk main's losses, the unmeasured households' band mix)
    solved so system input, billed unmetered and real losses each sit mid-bin at two decimals. By section 8, real
    losses are 0.993 system input less 1.025 billed metered less billed unmetered, so the mill moves system input and
    real losses a little, the trunk main system input and real losses, and the band mix billed unmetered and real
    losses."""
    import world as W
    for it in range(4):
        g, ind, n_unm = balance_run(out)
        s, m, b, r = g["siv"], g["metered"], g["unmeasured"], g["real"]
        print("run %d: system input %.4f, billed unmetered %.4f, real losses %.4f (clearances %.2f %.2f %.2f); "
              "billed metered %.4f" % (it, s, b, r, clear(s, 0.01), clear(b, 0.01), clear(r, 0.01), m))
        so, ro = g["siv_off"], g["real_off"]
        s_t, r_t = round(s - so, 2) + so, round(r - ro, 2) + ro
        # billed unmetered has no corridor; billed metered, shown in the balance though not asked, is fixed by the
        # identity 1.025 m + u = 0.993 s - r once the others are placed, and its own corridor runs 0.0011 up (bills read
        # to the next read's date): place u where the worse of u's and m's edge distances is largest
        ident = 0.993 * s_t - r_t
        def edge(x):
            return 0.005 - abs(x - round(x, 2))
        b_t = max((round(b, 2) + k * 0.0001 for k in range(-45, 46)),
                  key=lambda u: min(edge(u), edge((ident - u) / 1.025), edge((ident - u) / 1.025 + 0.0011)))
        want = np.array([s_t - s, b_t - b, r_t - r])
        print("   corridor: system input %.4f to %.4f, real losses %.4f to %.4f"
              % (s - 2 * so, s, r - 2 * ro, r))
        if it == 3 or (max(abs(want)) < 0.0003):
            break
        A = np.array([[1.0, 1.0, 0.0], [0.0, 0.0, 1.0], [-0.032, 0.993, -1.0]])
        x, y, u = np.linalg.solve(A, want)
        W.MILL_LPS = round(float(W.MILL_LPS + x / (ind * 0.0864)), 3)
        W.TRUNK_LOSS = round(float(W.TRUNK_LOSS + y), 4)
        W.BAND_SHIFT = round(float(W.BAND_SHIFT + u / (n_unm * 29.0 / 365.0 / 1000.0)), 5)
    print("MILL_LPS = %r, TRUNK_LOSS = %r, BAND_SHIFT = %r" % (W.MILL_LPS, W.TRUNK_LOSS, W.BAND_SHIFT))


if __name__ == "__main__":
    if sys.argv[1] == "balance":
        balance(sys.argv[2])
    else:
        main(sys.argv[1])
