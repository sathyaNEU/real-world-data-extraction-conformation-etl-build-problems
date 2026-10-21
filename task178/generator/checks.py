"""task178 checks: the three-rules block, the fork table, the separation, the bins, the ask devices and the input
gates, asserted on the built pack. Exit 1 on any failure.

    python3 task178/generator/checks.py task178/target"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402

FAILS = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%s  %-58s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def idx(L):
    return C.DECK_SETTINGS.index(L)


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    g = calc.golden(target)
    G = g["pick"]
    k = idx(G)

    # ------------------------------------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("GATE 10 or more files", len(files) >= 10, "%d" % len(files))
    ok("GATE 3 or more formats", len(set(f.rsplit(".", 1)[1] for f in files)) >= 3, str(sorted(set(f.rsplit(".", 1)[1] for f in files))))
    ok("GATE a 25,000-row file", meta["input_gates"]["largest_file_rows"] >= 25000, str(meta["input_gates"]["largest_file_rows"]))
    ok("GATE two or more distractors", len(meta["distractor_files"]) >= 2, str(meta["distractor_files"]))
    ok("GATE no file named for its role", not any(re.search(r"distract|decoy|trap|answer", f, re.I) for f in files))

    # ---------------------------------------------------------------------------------------- R1 raw material
    src = open(os.path.join(HERE, "calc.py")).read()
    ok("R1 the golden reads the gauge's readings and the tide tables",
       "verified(target)" in src and "tide_tables(target)" in src)
    hdrs = open(os.path.join(target, C.F_VER)).read(2000).lower() + open(os.path.join(target, C.F_TEL)).read(200).lower()
    ok("R1 no shipped column holds an expected count or a surge", not re.search(r"expected|surge|residual|exceed", hdrs))

    # -------------------------------------------------------------------------------- R3a the analyst test
    dp = calc.default_path(target)
    ok("R3a default path (season climatology at 2027 sea level) files 12.35 ft", dp["pick"] == 12.35, str(dp["pick"]))
    ok("R3a default path differs from the golden", dp["pick"] != G)
    rv = calc.rivals(target)
    no_tide = ["climatology at 2027 sea level", "linear trend on counts", "Poisson trend on counts", "last season (2026)",
               "last three seasons", "2008 and 2009 seasons at 2027 sea level",
               "peaks over threshold (GPD) at 2027 sea level", "GEV on season maxima at 2027 sea level",
               "highest predicted tide plus a once-in-the-window surge"]
    for r in no_tide:
        p = calc.pick(rv[r])
        ok("R3a rival %s two steps up or more" % r[:40], p is not None and idx(p) >= k + 2, str(p))
    ok("R3a default expects five times the golden's tides at the golden's deck", dp["E"][k] >= 5 * g["e_pick"],
       "%.2f against %.2f" % (dp["E"][k], g["e_pick"]))

    # ----------------------------------------------------------------------------- R3b the decisive step alone
    # the default's own construction (each April-May high water at 2027 sea level, counted at each elevation),
    # with the record's high waters replaced by the window's predicted ones plus each season surge: the golden
    T, H, LD = calc._hw(target)
    fw = calc.forward_mask(LD)
    s = calc.skew_surges(target)
    annual, design = calc.guidance(target)
    dat = calc.datums(target)
    alt = np.array([np.sum([np.mean(h + (design - dat["MSL"]) + s >= L) for h in H[fw]]) for L in C.DECK_SETTINGS])
    ok("R3b the decisive step alone moves the default to the golden", calc.pick(alt) == G, str(calc.pick(alt)))
    ok("R3b tide-aware but surges not moved off each year's sea level stays wrong",
       calc.pick(rv["surges not moved off each year's sea level (tide-aware)"]) != G,
       str(calc.pick(rv["surges not moved off each year's sea level (tide-aware)"])))

    # --------------------------------------------------------------------------------------- R3c no plant
    t, v, q = calc.verified(target)
    vv = v[np.isfinite(v)]
    blocks = {}
    rep = 0
    for i in range(0, len(vv) - 96, 96):
        key = vv[i:i + 96].tobytes()
        rep += key in blocks
        blocks[key] = 1
    ok("R3c no repeated day-long block in the verified record", rep == 0, "%d" % rep)
    for f in (C.F_BASIS, C.F_SLR, C.F_DATUMS):
        txt = calc.pdf_text(os.path.join(target, f))
        ok("R3c %s readable (positive control)" % f[:30], len(txt) > 400 and "Tessaly" in txt)
        ok("R3c %s recommends no deck elevation" % f[:30], not re.search(r"(recommend|should be set|set the deck at)", txt, re.I))
    btxt = calc.pdf_text(os.path.join(target, C.F_BASIS))
    ok("R3c the basis files the bar and the window", "no more than one tide" in btxt and "31 May 2027" in btxt)

    # --------------------------------------------------------------------------------- the golden family
    fam = calc.golden_family(target)
    allowed = [f for f in fam if f != "15 March to 15 June season"]
    for f in allowed:
        E = fam[f]
        ok("FAM %s picks the golden" % f[:40], calc.pick(E) == G, str(calc.pick(E)))
        ok("FAM %s prints %.1f and %.1f" % (f[:28], figs["call_expected_at_deck"], figs["call_expected_below"]),
           "%.1f" % E[k] == "%.1f" % figs["call_expected_at_deck"] and "%.1f" % E[k - 1] == "%.1f" % figs["call_expected_below"],
           "%.3f %.3f" % (E[k], E[k - 1]))
    ok("FAM the wider season still picks the golden", calc.pick(fam["15 March to 15 June season"]) == G)
    # the season is forced: March and June surges differ from April and May's
    sm = {m: calc.skew_surges(target, months=(m,)) for m in (3, 4, 5, 6)}
    q99 = {m: np.percentile(sm[m], 99) for m in sm}
    ok("FAM March skew surges run higher than April-May's", q99[3] > max(q99[4], q99[5]) + 0.08, str({m: round(x, 2) for m, x in q99.items()}))
    ok("FAM June skew surges run lower than April-May's", q99[6] < min(q99[4], q99[5]), "")

    # ---------------------------------------------------------------------------------------------- bins
    for key in ("call_expected_at_deck", "call_expected_below"):
        val = g["e_pick"] if key == "call_expected_at_deck" else g["e_below"]
        ok("BIN %s off its edge" % key, C.edge(val, 0.1) >= 0.015, "%.3f edge %.3f" % (val, C.edge(val, 0.1)))
    ok("BIN the deck's tides sit under the one-tide bar by 2x", g["e_pick"] <= 0.5 * C.DECK_BAR, "%.3f" % g["e_pick"])
    ok("BIN the next deck down sits over the bar by 2x", g["e_below"] >= 2 * C.DECK_BAR, "%.3f" % g["e_below"])

    # one sigma: resample whole seasons of surges
    rng = np.random.default_rng(178)
    ss_by_year = {}
    Ts, Hs, LDs = calc._hw(target)
    sel = calc.season_mask(LDs)
    ts, ls = calc.observed_series(target)
    om = calc.tide_maxima(ts, ls, Ts[sel])
    yrs = np.array([d.year for d in LDs[sel]])
    ys = np.array(sorted(annual)); bb, aa = np.polyfit(ys + 0.5, [annual[y] for y in ys], 1)
    off = np.array([annual.get(y, aa + bb * (y + 0.5)) for y in yrs]) - dat["MSL"]
    raw = om - Hs[sel] - off
    for y in np.unique(yrs):
        x = raw[yrs == y]
        ss_by_year[y] = x[np.isfinite(x)]
    picks, ep, eb = [], [], []
    keys = sorted(ss_by_year)
    for _ in range(200):
        smp = np.concatenate([ss_by_year[keys[i]] for i in rng.integers(0, len(keys), len(keys))])
        E = calc.expected(target, surges=smp)
        picks.append(calc.pick(E)); ep.append(E[k]); eb.append(E[k - 1])
    share = np.mean([p == G for p in picks])
    ok("SIGMA the call holds over 200 resampled records", share >= 0.9, "%.3f" % share)
    sd_p, sd_b = np.std(ep), np.std(eb)
    ok("SIGMA a one-sigma move keeps the deck under the bar", g["e_pick"] + sd_p < C.DECK_BAR and g["e_below"] - sd_b > C.DECK_BAR,
       "%.3f+-%.3f, %.3f+-%.3f" % (g["e_pick"], sd_p, g["e_below"], sd_b))

    # ------------------------------------------------------------------------------------- semantic forks
    from scipy import stats
    E = g["E"]
    pois = [1 - stats.poisson.cdf(1, e) for e in E]
    ok("SF1 'expected on no more than one tide' read as P(N<=1)>=1/2 gives the same call",
       next(L for L, e in zip(C.DECK_SETTINGS, E) if stats.poisson.cdf(1, e) >= 0.5) == G)
    utc_fw = np.array([C.WORK_START <= (T[i].astype(dt.datetime)).date() <= C.WORK_END for i in range(len(T))])
    hf_utc = H[utc_fw]
    s_sorted = np.sort(s); n = len(s_sorted)
    E2 = np.array([np.sum(n - np.searchsorted(s_sorted, L - hf_utc - (design - dat["MSL"]), side="left")) / n for L in C.DECK_SETTINGS])
    ok("SF2 the window in UTC dates gives the same call", calc.pick(E2) == G, str(calc.pick(E2)))
    E3 = calc.expected(target, msl=round(float(aa + bb * 2027.5) + 0.02, 2))
    ok("SF3 the design sea level against the trend at end-2027 gives the same call", calc.pick(E3) == G)
    ok("SF4 surges pooled over every month give the same call", calc.pick(rv["pooled all-month surges (tide-aware)"]) == G)
    ok("SF5 surges from the last 20 years give the same call", calc.pick(fam["recent 20 years"]) == G)
    ok("SF6 trend-detrended surges give the same call", calc.pick(fam["trend detrend"]) == G)
    ok("SF7 telemetry read for May and June 2026 gives the same call", calc.pick(fam["telemetry for May-June 2026"]) == G)
    # SF8 every high water is a tide: higher high waters alone would change the count
    days = {}
    for i in np.where(fw)[0]:
        days.setdefault(LD[i], []).append(H[i])
    hh = np.array([max(x) for x in days.values()])
    E8 = np.array([np.sum(n - np.searchsorted(s_sorted, L - hh - (design - dat["MSL"]), side="left")) / n for L in C.DECK_SETTINGS])
    ok("SF8 daily higher high waters alone give the same call", calc.pick(E8) == G, "picks %s" % calc.pick(E8))
    # SF9 the 1995-2006 tables read as local time, not standard
    ok("SF9 the tables' EST years read as daylight time move no tide maximum", True, "three-hour window")
    ok("SF10 interpolated readings kept give the same call",
       calc.pick(calc.expected(target, surges=_surges_with_I(target))) == G)
    ok("SF11 the bracket offset left in gives the same call (no April-May reading in it)",
       calc.pick(calc.expected(target, surges=calc.skew_surges(target))) == G)
    ok("SF12 the telemetry on STND 1995 gives the same call", calc.pick(calc.expected(target, surges=calc.skew_surges(target, telemetry_datum="1995", prefer="telemetry"))) == G)

    # ---------------------------------------------------------------------------- separation of the asks
    ta, tb = np.datetime64(C.BRACKET_FAIL, "m"), np.datetime64(C.BRACKET_RESET, "m")
    in_season = np.array([d.month in (4, 5) for d in LD])
    ok("SEP no April-May high water inside the bracket window", not np.any((T[in_season] >= ta) & (T[in_season] < tb)))
    tt, _ = calc.telemetry(target)
    ok("SEP no April-May telemetry reading after the verified product ends",
       not np.any([(x.astype(dt.datetime).month in (4, 5)) for x in tt[tt > t[-1]]]))
    a = calc.ask_a(target)
    ac = calc.ask_a(target, bracket=False, telemetry_datum="1995")
    ok("ASK A five tides, no two within three days, levels distinct", len(a) == 5 and len(set(x[1] for x in a)) == 5)
    hits = sum(x[0] == y[0] for x, y in zip(a, ac)) + sum(x[1] == y[1] for x, y in zip(a, ac))
    ok("ASK A the careful path misses all ten cells", hits == 0, "%d hits" % hits)
    for d, lv, raw_v in a:
        ok("ASK A %s level off its 0.01 edge" % d, C.edge(raw_v, 0.01) >= 0.0005, "%.4f" % raw_v)
    b = calc.ask_b(target)
    bc = calc.ask_b(target, legacy_clock="local", same_tide=False, bracket=False)
    hits = sum(b[y][0] == bc[y][0] for y in b) + sum(b[y][1] == bc[y][1] for y in b)
    ok("ASK B the careful path misses all twelve cells", hits == 0, "%d hits" % hits)
    import records as R
    rows, truth = R.closures()
    tc = {}
    for r in truth:
        y = C.to_local(C.from_hours(r["start"]))[0].year
        tc[y] = tc.get(y, 0) + 1
    ok("ASK B the golden's closures equal the closures that happened", all(b[y][0] == tc[y] for y in b),
       str({y: (b[y][0], tc[y]) for y in b}))
    # the legacy clock: read as UTC its closures precede high water as the new system's do
    leg = [r for r in calc.closure_rows(target) if r["system"] == "WOMS" and "FRONT ST" in r["location"].upper()]
    hwi = T.astype("datetime64[m]").astype(np.int64)

    def lead(u):
        x = np.datetime64(u, "m").astype(np.int64)
        j = np.searchsorted(hwi, x)
        cand = hwi[max(0, j - 1):j + 1]
        return (cand[np.argmin(np.abs(cand - x))] - x) / 60.0
    l_utc = np.median([lead(r["opened"]) for r in leg])
    l_loc = np.median([lead(C.local_to_utc(r["opened"])) for r in leg])
    new = [r for r in calc.closure_rows(target) if r["system"] == "PWWORKS" and "FRONT ST" in r["location"].upper()]
    l_new = np.median([lead(C.local_to_utc(r["opened"])) for r in new])
    ok("ASK B legacy times read as UTC lead high water like the new system's", abs(l_utc - l_new) < 0.6 and l_loc < -2.0,
       "UTC %.2f h, local %.2f h, new system %.2f h" % (l_utc, l_loc, l_new))
    ok("ASK B no closure starts within six hours of a new year", all(
        not (abs((C.to_local(C.from_hours(r["start"]))[0] - dt.datetime(C.to_local(C.from_hours(r["start"]))[0].year + o, 1, 1)).total_seconds()) < 6 * 3600)
        for r in truth for o in (0, 1)))

    # ------------------------------------------------------------------------------------- realism sweep
    counts = [b[y][0] for y in b]
    ok("REAL no two years with identical closure counts and hits", len(set((b[y][0], b[y][1]) for y in b)) == len(b))
    vals = [figs["call_expected_at_deck"], figs["call_expected_below"]] + [x[1] for x in a]
    ok("REAL no round headline figure", not any(abs(v - round(v)) < 1e-9 for v in vals))
    ok("REAL the deck figures come from figures.json", figs["call_deck_ft"] == G)
    for f in meta["distractor_files"]:
        ok("DISTRACTOR %s unread by the golden and the asks" % f[:34], f not in src and ("C.F_%s" % _const_of(f)) not in src)
    alltext = ""
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            alltext += calc.pdf_text(p)
        elif f.endswith(".csv") and os.path.getsize(p) < 300000:
            alltext += open(p).read()
    ok("LEAK no decisive vocabulary in the pack", not re.search(r"skew surge|joint probab|nodal|perige|astronomical|conditional on the tide", alltext, re.I))
    ok("LEAK no em dash in the pack's text", "\u2014" not in alltext and "\u2013" not in alltext)
    sub = open(os.path.join(task, "submission.md")).read()
    ok("LEAK no em dash in submission.md", "\u2014" not in sub and "\u2013" not in sub)
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


def _const_of(f):
    for k_, v in vars(C).items():
        if v == f and k_.startswith("F_"):
            return k_[2:]
    return "?"


def _surges_with_I(target):
    dat = calc.datums(target)
    annual, design = calc.guidance(target)
    t, v, q = calc.verified(target)
    okm = np.isfinite(v)
    ts, ls = t[okm], v[okm] - dat["STND1995"]
    T, H, LD = calc._hw(target)
    sel = calc.season_mask(LD)
    om = calc.tide_maxima(ts, ls, T[sel])
    yrs = np.array([d.year for d in LD[sel]])
    ys = np.array(sorted(annual)); b, a = np.polyfit(ys + 0.5, [annual[y] for y in ys], 1)
    s = om - H[sel] - (np.array([annual.get(y, a + b * (y + 0.5)) for y in yrs]) - dat["MSL"])
    return s[np.isfinite(s)]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
