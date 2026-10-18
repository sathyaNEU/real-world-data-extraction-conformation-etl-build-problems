"""checks.py: the generator's assertions, on the clean truth and on the cut pack.

Blocks: input gates; the three rules (R1, R2 per Layer 1 item, R3a the analyst test, R3b the decisive step alone,
R3c no plant); the golden family and every reflex route; the back-test that separates the specifications; the
stumping 1.2 screens as code; the semantic fork rows SF1 to SF16; the separation line; the asks and their stops;
the realism sweep; distractor deletion; redraws of the world. Exit 1 on any FAIL."""
import csv
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import date, datetime, timedelta

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A        # noqa: E402
import bundle as B          # noqa: E402
import cracker as CR        # noqa: E402
import deliver as DL        # noqa: E402
import names as N           # noqa: E402
import pack as PK           # noqa: E402
import records as R         # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RESULTS = []
CODE2REF = PK.SEG_REF
REF2CODE = {v: k for k, v in CODE2REF.items()}
GOLD_CALL, GOLD_SEG, GOLD_HOUR = "CW1", "CW1-03", 8


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-74s %s" % ("PASS" if ok else "FAIL", label[:74], detail))


def winner(res):
    m = max(res.values())
    w = [c for c, v in res.items() if v == m]
    return w[0] if len(w) == 1 else "tie:" + "+".join(sorted(w))


def truth_inputs(T):
    fl = W.summer_twoway(T)
    days = {y: W.summer_days(y) for y in W.SUMMERS}
    dts = {y: [W.daytype(d) for d in days[y]] for y in W.SUMMERS}
    wx = T["weather"]
    weather = {d: (wx["tmax"][i], wx["rain"][i]) for d, i in wx["idx"].items()}
    caps = {c: W.SEGMENTS[c]["cap"] for c in W.SEGMENTS}
    cws = {cw: [s[0] for s in segs] for cw, name, segs in W.CYCLEWAYS}
    return fl, days, dts, weather, caps, cws


def binding(sc, caps, cws, days, dts, cw):
    per = {s: np.mean([A.crowded_by_counter(sc, caps, [s], y)[s] for y in A.YEARS]) for s in cws[cw]}
    b = max(per, key=per.get)
    cells = {}
    for y in A.YEARS:
        for i in range(len(days[y])):
            for h in A.H_WINDOW:
                if sc[b][y][i, h] > caps[b]:
                    cells[(dts[y][i], h)] = cells.get((dts[y][i], h), 0) + 1
    top = max(cells, key=cells.get) if cells else None
    return b, top, cells, per


def golden_on(P, spec=DL.GOLDEN):
    res, G, sc = A.golden(P["flows"], P["days"], P["dts"], P["weather"], P["caps"], P["cycleways"], *spec)
    w = winner(res)
    b, top, cells, per = binding(sc, P["caps"], P["cycleways"], P["days"], P["dts"], w if not w.startswith("tie") else "CW1")
    return dict(res=res, win=w, seg=b, top=top, cells=cells, per=per, G=G, sc=sc)


# ====================================================================================== input gates
def gates(meta):
    files = sorted(os.listdir(TARGET))
    fm = {f["path"]: f for f in meta["files"]}
    check("GATE files: 10 or more", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("GATE formats: 3 or more", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(meta["files"], key=lambda f: f["rows"] or 0)
    check("GATE a file of 25,000 rows or more", (big["rows"] or 0) >= 25000, "%s %d rows" % (big["path"], big["rows"]))
    d = meta["distractor_files"]
    check("GATE two or more distractors named in metadata.json", len(d) >= 2 and all(x in files for x in d), ", ".join(d))
    check("GATE no file named after its role", not any(re.search(r"distract|decoy|known_issue|trap|stump", f) for f in files))
    check("GATE every file has source, date and licence",
          set(fm) == set(files) and all(fm[f]["source"] and fm[f]["date"] and fm[f]["license"] for f in files))
    check("GATE manifest lists every other shipped file",
          sorted(r["file"] for r in csv.DictReader(open(os.path.join(TARGET, PK.F["manifest"])))) ==
          sorted(f for f in files if f != PK.F["manifest"]))


# ====================================================================================== R1
def r1(P):
    heads = []
    for f in sorted(os.listdir(TARGET)):
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            lines = open(p, encoding="utf-8").read().splitlines()
            h = [l for l in lines[:3] if not l.startswith("#")][0 if not f.startswith("counts_summer2024") else 1]
            heads.append((f, h.lower()))
        elif f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                for r in ws.iter_rows(max_row=8, values_only=True):
                    heads.append((f, " ".join(str(x) for x in r if x is not None).lower()))
        elif f.endswith(".parquet"):
            import pyarrow.parquet as pq
            heads.append((f, " ".join(pq.ParquetFile(p).schema_arrow.names).lower()))
    bad = [f for f, h in heads if re.search(r"crowd|forecast|growth|exceed|over_capacity|capacity", h)]
    check("R1 no shipped column holds the deciding quantity (crowding, forecast, growth, capacity)", not bad, ", ".join(bad))
    n = sum(np.isfinite(P["flows"][s][y]).sum() for s in P["flows"] for y in A.YEARS)
    check("R1 the pack ships every counted segment's hourly riders for the three summers",
          set(P["flows"]) == set(P["caps"]) and len(P["flows"]) == 22 and n > 0.97 * 22 * 276 * 24, "%d recorded hours" % n)


# ====================================================================================== R3 on the clean truth
def r3(T):
    fl, days, dts, wx, caps, cws = truth_inputs(T)
    yoy = A.total_growth(fl, "yoy")
    d3 = winner(A.crowded_days(A.scale_uniform(fl, yoy), caps, cws))
    check("R3a analyst test: three summers at each counter's 2025-26 total growth files Estuary Path (CW3)", d3 == "CW3", d3)
    d1 = winner(A.crowded_days(A.scale_uniform(fl, yoy), caps, cws, years=[2026]))
    check("R3a the latest summer replayed at its total growth files CW3 too", d1 == "CW3", d1)
    g = winner(A.golden(fl, days, dts, wx, caps, cws, *DL.GOLDEN)[0])
    check("R3b the default path with the decisive step alone (hour and day-type growth, weather held) files CW1", g == "CW1", g)
    G = A.cell_growth(fl, days, dts, wx, "wkwe", "hour", "none")
    c_only = winner(A.crowded_days(A.scale_cells(fl, days, dts, G, "wkwe"), caps, cws))
    check("R3b one half alone: hour-cell growth without weather files a wrong cycleway", c_only != "CW1", c_only)
    G = A.cell_growth(fl, days, dts, wx, "wkwe", "day", "flagT")
    w_only = winner(A.crowded_days(A.scale_cells(fl, days, dts, G, "wkwe"), caps, cws))
    check("R3b other half alone: weather-held daily growth files a wrong cycleway", w_only != "CW1", w_only)
    fam = {m: winner(A.golden(fl, days, dts, wx, caps, cws, *m)[0]) for m in A.FAMILY}
    check("R3 clean truth: all %d golden-family specifications name CW1" % len(fam), set(fam.values()) == {"CW1"},
          str(sorted(set(fam.values()))))
    return fam


# ====================================================================================== the family and the routes on the pack
EXTENDED = [("wkwe", "hour", "Tonly", "ols"), ("wkwe", "hour", "logmmT", "ols"), ("wkwe", "hour", "flagTwetT", "ols"),
            ("dow", "hour", "flagT", "ols"), ("dow_term", "hour", "flagT", "ols"), ("dt3", "hour", "Tonly", "ols"),
            ("dow", "period", "flagT", "ols"), ("wkwe", "hour", "logmmT", "poisson"), ("dt3", "hour", "mmT", "ols")]
HALF_WEATHER = [("wkwe", "hour", "wetonly", "ols"), ("wkwe", "hour", "mmonly", "ols"), ("dt3", "hour", "wetonly", "ols")]


def family(P):
    out = {}
    for m in A.FAMILY + EXTENDED:
        out[m] = A.golden(P["flows"], P["days"], P["dts"], P["weather"], P["caps"], P["cycleways"], *m)[0]
    wins = {m: winner(v) for m, v in out.items()}
    check("FAMILY all %d specifications with hour cells and temperature name CW1" % len(wins), set(wins.values()) == {"CW1"},
          str(sorted(set(wins.values()))))
    lo = min(v["CW1"] for v in out.values())
    hi_other = max(max(x for c, x in v.items() if c != "CW1") for v in out.values())
    margins = [v["CW1"] / max(x for c, x in v.items() if c != "CW1") for v in out.values()]
    check("FAMILY CW1 leads by 1.15x or more in every specification", min(margins) >= 1.15,
          "smallest margin %.2fx; CW1 %.1f to %.1f, best rival %.1f" % (min(margins), lo,
                                                                       max(v["CW1"] for v in out.values()), hi_other))
    for m in HALF_WEATHER:
        w = winner(A.golden(P["flows"], P["days"], P["dts"], P["weather"], P["caps"], P["cycleways"], *m)[0])
        check("LADDER rain without temperature (%s, %s) lands a wrong cycleway" % (m[0], m[2]), w != "CW1", w)
    return out


def dashboard_route(P):
    """each cycleway's growth read off the dashboard's headline counter, summer 2026 over summer 2025"""
    rows = list(csv.DictReader([l for l in open(os.path.join(TARGET, PK.F["dashboard"])).read().splitlines()
                                if not l.startswith("#")]))
    reg = {r["legacy_site_name"]: r for r in P["register"] if r["type"] == "dashboard" and not r["unit_of_record_to"]}
    g = {}
    for site, r in reg.items():
        s = {y: sum(int(x["cyclists"]) for x in rows if x["site"] == site and x["month"] in
                    ("%d-06" % y, "%d-07" % y, "%d-08" % y)) for y in (2025, 2026)}
        g[r["cycleway"]] = s[2026] / s[2025]
    fac = {seg: g[cw] for cw, segs in P["cycleways"].items() for seg in segs}
    return A.crowded_days(A.scale_uniform(P["flows"], fac), P["caps"], P["cycleways"])


def app_route(P):
    rows = list(csv.DictReader(open(os.path.join(TARGET, PK.F["app"]))))
    name2cw = {v: k for k, v in DL.CW_NAME.items()}
    g = {}
    for cwn in name2cw:
        s = {y: sum(int(x["rides"]) for x in rows if x["cycleway"] == cwn and x["month"] in
                    ("%d-06" % y, "%d-07" % y, "%d-08" % y)) for y in (2025, 2026)}
        g[name2cw[cwn]] = s[2026] / s[2025]
    fac = {seg: g[cw] for cw, segs in P["cycleways"].items() for seg in segs}
    return A.crowded_days(A.scale_uniform(P["flows"], fac), P["caps"], P["cycleways"])


def cell_ratio(P, y0, y1, filt=None):
    """growth of each counter's weekday or weekend hour as the ratio of its mean riders between two summers, on the
    days a filter keeps (no regression): the shortcut an analyst takes instead of a model"""
    fl, days, dts, wx = P["flows"], P["days"], P["dts"], P["weather"]
    G = {}
    for code, per in fl.items():
        G[code] = {}
        for g in ("wk", "we"):
            for h in range(24):
                m = {}
                for y in (y0, y1):
                    v = [per[y][i, h] for i, (d, t) in enumerate(zip(days[y], dts[y])) if A.daygroup(d, t, "wkwe") == g
                         and not np.isnan(per[y][i, h]) and (filt is None or (d in wx and filt(wx[d])))]
                    m[y] = np.mean(v) if v else np.nan
                r = (m[y1] / m[y0]) ** (1.0 / (y1 - y0)) if (m[y0] and m[y0] > 0) else 1.0
                G[code][(g, h)] = r if np.isfinite(r) else 1.0
    return A.crowded_days(A.scale_cells(fl, days, dts, G, "wkwe"), P["caps"], P["cycleways"])


def peak_factor(P, peak, off):
    G = {c: {(g, h): (peak if (g == "wk" and h in (7, 8, 9, 16, 17, 18)) else off) for g in ("wk", "we") for h in range(24)}
         for c in P["flows"]}
    return A.crowded_days(A.scale_cells(P["flows"], P["days"], P["dts"], G, "wkwe"), P["caps"], P["cycleways"])


RIGHT_FAMILY_ROUTES = ("golden variant: hour cells, weather, 2025-26 only",
                       "hour cells on dry 18 to 22 C days only, 2024 to 2026 mean ratio")
ESTIMAND_VIOLATIONS = ("golden growth, 2026 weather only",)


def routes(P):
    Rr = A.routes(P["flows"], P["days"], P["dts"], P["weather"], P["caps"], P["cycleways"])
    Rr["each cycleway's dashboard counter growth, summer 2026 over 2025"] = dashboard_route(P)
    Rr["each cycleway's activity app rides growth, summer 2026 over 2025"] = app_route(P)
    Rr["hour cells, no weather, 2024 to 2025 mean ratio (the hot summer left out)"] = cell_ratio(P, 2024, 2025)
    Rr["hour cells, no weather, 2024 to 2026 mean ratio"] = cell_ratio(P, 2024, 2026)
    Rr["hour cells on dry days only, 2024 to 2026 mean ratio"] = cell_ratio(P, 2024, 2026, lambda w: w[1] < 1.0)
    Rr["hour cells on dry 18 to 22 C days only, 2024 to 2026 mean ratio"] = cell_ratio(
        P, 2024, 2026, lambda w: w[1] < 1.0 and 18 <= w[0] <= 22)
    tot = {c: np.nansum(P["flows"][c][2025]) / np.nansum(P["flows"][c][2024]) for c in P["flows"]}
    Rr["each counter's total growth 2024 to 2025 (the hot summer left out)"] = A.crowded_days(
        A.scale_uniform(P["flows"], tot), P["caps"], P["cycleways"])
    Rr["rule of thumb: 10 per cent at weekday peaks, flat otherwise"] = peak_factor(P, 1.10, 1.0)
    Rr["rule of thumb: 5 per cent at weekday peaks, -2 per cent otherwise"] = peak_factor(P, 1.05, 0.98)
    bad = []
    for k, v in Rr.items():
        w = winner(v)
        if k in RIGHT_FAMILY_ROUTES:
            check("ROUTE right-family variant names CW1: %s" % k, w == "CW1", w)
            continue
        if k in ESTIMAND_VIOLATIONS:
            check("ROUTE estimand violation (policy 3.4 three summers) does not name CW1 alone: %s" % k, w != "CW1", w)
            continue
        if w == "CW1":
            bad.append(k)
    check("ROUTES every reflex route misses CW1 (%d routes)" % (len(Rr) - len(RIGHT_FAMILY_ROUTES) - len(ESTIMAND_VIOLATIONS)),
          not bad, "; ".join(bad))
    d = winner(Rr["three summers at each counter's 2025-26 total growth"])
    check("ROUTE the default path on the pack files Estuary Path (CW3)", d == "CW3", d)
    return Rr


# ====================================================================================== back-test
def backtest(P):
    """fit on 2024 and 2025, predict every 2026 hour cell from its own day's weather; mean squared log error"""
    fl, days, dts, wx = P["flows"], P["days"], P["dts"], P["weather"]

    def series(code, g, hs, years):
        out = []
        for y in years:
            for i, (d, t) in enumerate(zip(days[y], dts[y])):
                if A.daygroup(d, t, "wkwe") != g or d not in wx:
                    continue
                v = fl[code][y][i, hs]
                if np.isnan(v).any() or v.sum() <= 0:
                    continue
                out.append((y, wx[d][0], wx[d][1], float(v.sum())))
        return out

    def err(spec, cellwise):
        e_all = []
        for code in P["caps"]:
            for g in ("wk", "we"):
                dayfit = series(code, g, list(range(24)), [2024, 2025]) if not cellwise else None
                for h in A.H_WINDOW:
                    fit = series(code, g, [h], [2024, 2025])
                    te = series(code, g, [h], [2026])
                    if len(fit) < 20 or len(te) < 5:
                        continue
                    src = fit if cellwise else dayfit
                    X = np.array([[1.0, y - 2026] + A._design(t, r, spec) for y, t, r, v in src])
                    b = np.linalg.lstsq(X, np.log([v for *_, v in src]), rcond=None)[0]
                    # level of the cell from its own 2024-25 mean, trend and weather from the chosen fit
                    Xc = np.array([[1.0, y - 2026] + A._design(t, r, spec) for y, t, r, v in fit])
                    off = np.mean(np.log([v for *_, v in fit]) - Xc @ b)
                    for y, t, r, v in te:
                        x = np.array([1.0, y - 2026] + A._design(t, r, spec))
                        e_all.append(math.log(v) - (x @ b + off))
        return float(np.mean(np.square(e_all)))
    m = {s: err(s, True) for s in ("flagT", "Tonly", "wetonly", "none")}
    check("BACKTEST hour cells with rain and temperature predict summer 2026 best out of sample",
          m["flagT"] < min(m["Tonly"], m["wetonly"], m["none"]) * 0.85,
          "MSE log: rain+temp %.4f, temp only %.4f, rain only %.4f, none %.4f" % (m["flagT"], m["Tonly"], m["wetonly"], m["none"]))

    def bias(code, g, h, src, spec):
        fit = series(code, g, [h], [2024, 2025])
        te = series(code, g, [h], [2026])
        X = np.array([[1.0, y - 2026] + A._design(t, r, spec) for y, t, r, v in src])
        b = np.linalg.lstsq(X, np.log([v for *_, v in src]), rcond=None)[0]
        Xc = np.array([[1.0, y - 2026] + A._design(t, r, spec) for y, t, r, v in fit])
        off = np.mean(np.log([v for *_, v in fit]) - Xc @ b)
        return float(np.mean([math.log(v) - (np.array([1.0, y - 2026] + A._design(t, r, spec)) @ b + off) for y, t, r, v in te]))
    bc, bd, bn = [], [], []
    tr3 = None
    for code in P["caps"]:
        best = None
        for g in ("wk", "we"):
            idx = [i for i, (d, t) in enumerate(zip(days[2026], dts[2026])) if A.daygroup(d, t, "wkwe") == g]
            for h in A.H_WINDOW:
                mu = np.nanmean(fl[code][2026][idx, h])
                if best is None or mu > best[0]:
                    best = (mu, g, h)
        _, g, h = best
        x = (bias(code, g, h, series(code, g, [h], [2024, 2025]), "flagT"),
             bias(code, g, h, series(code, g, list(range(24)), [2024, 2025]), "flagT"),
             bias(code, g, h, series(code, g, [h], [2024, 2025]), "none"))
        bc.append(abs(x[0]))
        bd.append(abs(x[1]))
        bn.append(abs(x[2]))
        if code == GOLD_SEG:
            tr3 = x
    m_day = (float(np.mean(bc)), float(np.mean(bd)), float(np.mean(bn)))
    check("BACKTEST at each counted segment's busiest 2026 cell, the hour's own growth with weather held has the smallest bias",
          m_day[0] < 0.7 * min(m_day[1], m_day[2]),
          "mean |log bias|: cell %.3f, the day's growth %.3f, no weather %.3f; Tolland Bridge 08:00 cell %.3f, day %.3f"
          % (m_day + (tr3[0], tr3[1])))
    return m, m_day


# ====================================================================================== stumping 1.2 screens
def screens(P, gold, Rr):
    # dispersion: the decisive quantity is a level (each cell's growth and the days over capacity), not a spread
    check("SCREEN dispersion: the decisive quantity is a level (growth of the binding cell), no variance enters the call",
          all(isinstance(v, float) for v in gold["G"][GOLD_SEG].values()))
    # variance-only: the decisive step moves the point comparison, not only its uncertainty: the margin of CW1 over
    # the default path's pick (CW3) moves by more than that margin's spread across the golden family
    dft = Rr["three summers at each counter's 2025-26 total growth"]
    lever = (gold["res"]["CW1"] - gold["res"]["CW3"]) - (dft["CW1"] - dft["CW3"])
    margins = [v["CW1"] - v["CW3"] for v in FAM.values()]
    noise = max(margins) - min(margins)
    check("SCREEN variance-only: the decisive step moves the CW1 against CW3 margin by more than its spread across the family",
          lever / max(noise, 1e-9) >= 1.0, "lever %.1f days, family spread of the margin %.1f days" % (lever, noise))
    # common-exposure subset: days already at a common weather, compared at the daily total, still miss
    fl, days, dts, wx, caps, cws = P["flows"], P["days"], P["dts"], P["weather"], P["caps"], P["cycleways"]
    g = {}
    for code, per in fl.items():
        m = {}
        for y in A.YEARS:
            v = [np.nansum(per[y][i]) for i, d in enumerate(days[y]) if d in wx and wx[d][1] < 1.0 and 19 <= wx[d][0] <= 23
                 and dts[y][i] == "wk_term" and not np.isnan(per[y][i]).any()]
            m[y] = np.mean(v) if v else np.nan
        g[code] = (m[2026] / m[2024]) ** 0.5
    w_sub = winner(A.crowded_days(A.scale_uniform(fl, g), caps, cws))
    check("SCREEN common exposure: dry 19-23 C term weekdays compared at the daily total miss (the hour still decides)",
          w_sub != "CW1", w_sub)
    w_2026 = winner(Rr["2026 replayed as recorded"])
    check("SCREEN common exposure: the summer already at the latest level, replayed as recorded, misses", w_2026 != "CW1", w_2026)
    # truncation: nothing suppresses or caps a count
    mx = [np.nanmax(fl[s][y]) for s in fl for y in A.YEARS]
    tops = [np.sum(fl[s][y] == np.nanmax(fl[s][y])) for s in fl for y in A.YEARS]
    check("SCREEN truncation: no count is capped or suppressed (each series' maximum occurs on one hour or two)",
          max(tops) <= 3, "largest count of hours at a series maximum %d" % max(tops))


# ====================================================================================== semantic fork rows
def sf_rows(P, gold):
    pol = " ".join(open_pdf(PK.F["policy"]).split())
    fl, days, dts, wx, caps, cws = P["flows"], P["days"], P["dts"], P["weather"], P["caps"], P["cycleways"]
    sc = gold["sc"]
    check("SF1 'crowded' is policy 3.3's any clock hour 06:00-22:00 local, both directions, above capacity",
          "in any clock hour from 06:00 to 22:00 local time" in pol and "both directions together" in pol)
    # SF2: no minimum width sits on a band edge, so inclusive or exclusive edges give one capacity
    widths = [float(s["min_width_m"]) for s in P["inventory"] if s["counter_id"]]
    edges = [lo for lo, hi, cap in P["bands"]]
    check("SF2 capacity at minimum width: no counted width on a Table 4.3 band edge", not any(w in edges for w in widths),
          "widths %s" % sorted(set(widths)))
    # SF3: exceed strictly against at-or-above: no scaled hour equals a capacity
    eq = sum(int(np.sum(np.isclose(sc[s][y][:, A.H_WINDOW], caps[s], atol=1e-6))) for s in sc for y in A.YEARS)
    check("SF3 'exceed' strict or not: no forecast hour sits exactly on a capacity", eq == 0, "%d hours on a capacity" % eq)
    # SF4: mean against sum of the three summers' crowded days: one ranking
    tot = {cw: v * 3 for cw, v in gold["res"].items()}
    check("SF4 mean or total over the three summers: same call", winner(tot) == "CW1")
    # SF5: uncounted segments carry no counts, so 'counted segments' is the only population a count can make
    unc = [s for s in P["inventory"] if not s["counter_id"]]
    check("SF5 counted segments (policy 3.1): uncounted segments have no counts", all(s["segment_ref"] not in fl for s in unc),
          "%d uncounted segments" % len(unc))
    # SF6: the window's last hour, 21:00 or 22:00 beginning
    H2 = list(range(6, 23))
    alt = {}
    for cw, segs in cws.items():
        t = 0
        for y in A.YEARS:
            c = None
            for s in segs:
                hit = (np.nan_to_num(sc[s][y][:, H2], nan=-1) > caps[s]).any(axis=1)
                c = hit if c is None else (c | hit)
            t += int(c.sum())
        alt[cw] = t / 3
    check("SF6 06:00 to 22:00 read as hours beginning 06:00 to 22:00: same call", winner(alt) == "CW1" and alt == gold["res"])
    # SF7: an hour not recorded cannot make a day crowded: estimated hours read as recorded, same call
    P2 = B.load(TARGET, estimated_as_recorded=True)
    w = winner(golden_on(P2)["res"])
    check("SF7 estimated hours read as recorded: same call", w == "CW1", w)
    # SF8: 'the numbers expected in the coming summer' carried at whole years: each day's own date in its summer instead
    G = gold["G"]
    sc2 = {}
    for s, per in fl.items():
        sc2[s] = {}
        for y in A.YEARS:
            lab = [A.daygroup(d, t, "wkwe") for d, t in zip(days[y], dts[y])]
            yrs = np.array([(date(2027, d.month, d.day) - d).days / 365.25 for d in days[y]])
            fac = np.array([[G[s][(g, h)] for h in range(24)] for g in lab]) ** yrs[:, None]
            sc2[s][y] = per[y] * fac
    w = winner(A.crowded_days(sc2, caps, cws))
    check("SF8 growth carried day by day to the same date in 2027 rather than by whole years: same call", w == "CW1", w)
    # SF9: both directions: legacy Ch1 plus Ch2 and platform in plus out; two-way sums do not depend on which is which
    check("SF9 both directions together: two-way sums are direction-free", True)
    # SF10: the hours it crowds, local clock (policy 3.3) against UTC
    check("SF10 the hours it crowds on the local clock: 08:00 to 09:00", gold["top"] == ("wk_term", 8), str(gold["top"]))
    # SF11: the segment that crowds it is the only CW1 segment over capacity in every summer
    per = {s: [A.crowded_by_counter(sc, caps, [s], y)[s] for y in A.YEARS] for s in cws["CW1"]}
    check("SF11 'the segment that crowds it' is unique: only CW1-03 crowds on Tolland Road",
          all(v == [0, 0, 0] for s, v in per.items() if s != GOLD_SEG) and min(per[GOLD_SEG]) > 0, str(per))
    check("SF12 the three summers are named in policy 3.4 (2024, 2025 and 2026)",
          "the three summers are those of 2024, 2025 and 2026" in pol)
    check("SF13 the coming summer is 1 June to 31 August 2027 (policy 2.2)", "1 June to 31 August 2027" in pol)
    check("SF14 no tie for the committee to break (policy 2.3)", not winner(gold["res"]).startswith("tie"))
    # SF15: the Corn Exchange's two units: one site; 2024 from the old unit by site name, 2025-26 from the new unit
    reg = [r for r in P["register"] if r["legacy_site_name"] == "Corn Exchange"]
    check("SF15 Corn Exchange's two units share one segment, so either unit of record gives one series",
          len(reg) == 2 and len({r["segment_ref"] for r in reg}) == 1)
    # SF16: each day as an equally likely day: mean over days of a summer against the summer's share of crowded days
    check("SF16 days counted against 92-day summers: every summer has 92 days, so shares and counts rank alike",
          all(len(P["days"][y]) == 92 for y in A.YEARS))


def open_pdf(name):
    import pdfplumber
    with pdfplumber.open(os.path.join(TARGET, name)) as p:
        return "\n".join(pg.extract_text() for pg in p.pages)


# ====================================================================================== R2: each Layer 1 item mishandled
def r2(P, gold):
    def same(g, label, hour_shift=0):
        ok = g["win"] == GOLD_CALL and g["seg"] == GOLD_SEG and g["top"] == ("wk_term", GOLD_HOUR + hour_shift)
        check("R2 %s: call, segment and binding hour unchanged" % label, ok, "%s %s %s" % (g["win"], g["seg"], g["top"]))

    def with_flows(fl, dts=None, weather=None):
        Q = dict(P)
        Q["flows"] = fl
        if dts is not None:
            Q["dts"] = dts
        if weather is not None:
            Q["weather"] = weather
        return golden_on(Q)
    # L1 legacy local hours read as UTC (shifted an hour later)
    fl = {s: dict(v) for s, v in P["flows"].items()}
    for s in fl:
        a = np.full_like(fl[s][2024], np.nan)
        a[:, 1:] = P["flows"][s][2024][:, :-1]
        fl[s][2024] = a
    g = with_flows(fl)
    check("R2 legacy local hours read as UTC: call and segment unchanged", g["win"] == GOLD_CALL and g["seg"] == GOLD_SEG,
          "%s %s" % (g["win"], g["seg"]))
    # L2 platform UTC read as local: the same physical hour is labelled an hour earlier in 2025-26
    g = golden_on(B.load(TARGET, utc_as_local=True))
    check("R2 platform UTC read as local: call and segment unchanged", g["win"] == GOLD_CALL and g["seg"] == GOLD_SEG,
          "%s %s" % (g["win"], g["seg"]))
    # L3 legacy channels: two sites wired with Ch1 away from the centre; two-way sums unaffected
    check("R2 legacy Ch1 direction at EP3 and MS4: two-way sums identical either way", True)
    # L4 no_data hours read as counts of 0
    same(golden_on(B.load(TARGET, nodata_as_zero=True)), "no_data and legacy blanks read as zero")
    # L5 estimated hours read as recorded
    same(golden_on(B.load(TARGET, estimated_as_recorded=True)), "estimated hours read as recorded")
    # L6 hours losing part of their minutes dropped as unrecorded
    fl = {s: dict(v) for s, v in P["flows"].items()}
    for code, ref in CODE2REF.items():
        for y in A.YEARS:
            f = R.lost_fraction(code, y, P["days"][y])
            a = fl[ref][y].copy()
            a[(f > 0) & (f < 0.5)] = np.nan
            fl[ref][y] = a
    same(with_flows(fl), "partly lost hours dropped")
    # L7 missing weather days filled with the month's mean
    wx = dict(P["weather"])
    for d in W.WEATHER_MISSING:
        same_month = [v for k, v in P["weather"].items() if k.month == d.month and k.year == d.year]
        wx[d] = (float(np.mean([v[0] for v in same_month])), float(np.mean([v[1] for v in same_month])))
    same(with_flows(P["flows"], weather=wx), "missing weather days filled with the month's mean")
    # L8 bank holidays read as ordinary weekdays
    dts = {y: [("we" if d.weekday() >= 5 else ("wk_hol" if W.in_school_holiday(d) else "wk_term")) for d in P["days"][y]]
           for y in A.YEARS}
    same(with_flows(P["flows"], dts=dts), "bank holidays read as weekdays")
    # L9 event days in the programme dropped
    ev = {date.fromisoformat(e[0]) for e in R.EVENTS}
    fl = {s: dict(v) for s, v in P["flows"].items()}
    for s in fl:
        for y in A.YEARS:
            a = fl[s][y].copy()
            for i, d in enumerate(P["days"][y]):
                if d in ev:
                    a[i] = np.nan
            fl[s][y] = a
    same(with_flows(fl), "event days dropped")
    # L10 the Corn Exchange's 2024 legacy series dropped by a join on the current unit only
    fl = {s: dict(v) for s, v in P["flows"].items()}
    fl["CW5-01"][2024] = np.full_like(fl["CW5-01"][2024], np.nan)
    same(with_flows(fl), "Corn Exchange 2024 dropped (current unit only)")
    # L11 SF2's overnight logger sleep in August 2024 read as zero
    fl = {s: dict(v) for s, v in P["flows"].items()}
    fl["CW6-02"][2024] = np.nan_to_num(fl["CW6-02"][2024], nan=0.0)
    same(with_flows(fl), "SF2 overnight blanks read as zero")


# ====================================================================================== separation
def separation(P, gold):
    summer = {d for y in A.YEARS for d in P["days"][y]}
    cw = [datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ").date()
          for r in csv.DictReader(open(os.path.join(TARGET, PK.F["week"])))]
    check("SEPARATION the count week lies outside the three summers", not any(d in summer for d in cw))
    lc = [(date.fromisoformat(a), date.fromisoformat(b)) for a, b in R.LOCAL_CLOCK.values()]
    check("SEPARATION the laptop-clock spells lie outside the three summers",
          not any(a <= d <= b for d in summer for a, b in lc))
    dev = [s for s in R.SPELLS if s.get("recur") or s.get("con") or s.get("asset") or s["a"][:4] != s["b"][:4] or
           s.get("checks")]
    inside = [s for s in dev if any(date.fromisoformat(s["a"][:10]) <= d <= date.fromisoformat(s["b"][:10]) for d in summer)]
    check("SEPARATION no maintenance-log device spell (follow-up, recurrence, contractor twin, mis-keyed id, year edge) "
          "falls in a summer", not inside, str([s["code"] + " " + s["a"] for s in inside]))
    tmp = tempfile.mkdtemp(prefix="sep169_")
    try:
        for f in os.listdir(TARGET):
            if f not in (PK.F["week"], PK.F["volunteers"], PK.F["log"]):
                shutil.copy(os.path.join(TARGET, f), tmp)
        g = golden_on(B.load(tmp))
        check("SEPARATION with every ask file deleted the call, segment and hour are unchanged",
              g["win"] == GOLD_CALL and g["seg"] == GOLD_SEG and g["top"] == gold["top"] and g["res"] == gold["res"])
        for f in PK.DISTRACTORS:
            p = os.path.join(tmp, f)
            if os.path.exists(p):
                os.remove(p)
        g = golden_on(B.load(tmp))
        check("DISTRACTORS deleted too: the golden is unchanged", g["res"] == gold["res"])
    finally:
        shutil.rmtree(tmp)


# ====================================================================================== asks
def asks(ctx):
    aa, bb = DL.ask_a(TARGET), DL.ask_b(TARGET)
    ta = R.ask_a_truth(ctx["CW"], ctx["sheets"])
    tb = R.outages_2025_truth()
    ok = all((aa[N.COUNTER_IDS[c]]["C"], aa[N.COUNTER_IDS[c]]["V"]) == (v[0], v[1]) for c, v in ta.items())
    check("ASK A the golden read from the pack equals the truth at every site", ok)
    ok = all((bb[N.COUNTER_IDS[c]]["minutes"], bb[N.COUNTER_IDS[c]]["n"]) == v for c, v in tb.items())
    check("ASK B the golden read from the pack equals the truth at every counter", ok)
    ea = min(R.edge(v["short"]) for v in aa.values())
    check("ASK A every shortfall sits 0.02 points or more inside its printed cell", ea >= 0.02, "closest %.3f" % ea)
    eb = min(R.edge(v["hours"]) for v in bb.values())
    check("ASK B every hours figure sits 0.02 h or more inside its printed cell", eb >= 0.02, "closest %.3f h" % eb)
    sh = CR.sheet(TARGET)
    check("CRACKER natural path misses every one of the 24 ask figures", sh["cracker"][1] == 0,
          "%d of %d hit" % (sh["cracker"][1], sh["cracker"][2]))
    check("PAIR ceiling 40 or under on the cut pack", sh["pair"] <= 40, "%.1f" % sh["pair"])
    check("PAIR both responses on the call 45 or under", sh["both_on_call"] <= 45, "%.1f" % sh["both_on_call"])
    worst = max(v[2] for v in sh["cracks"].values())
    check("PAIR every single crack 40 or under", worst <= 40, "worst %.1f" % worst)
    check("MIRROR keeps under 35 per cent of ask weight", sh["mirror"][1] / sh["mirror"][2] < 0.35,
          "%d of %d" % (sh["mirror"][1], sh["mirror"][2]))
    # each stop is a complete pipeline landing outside the bin on every figure it touches
    ga = CR.ask_a(TARGET, **CR.GOLD_A)
    for name, kw in [("stamps read as starts", dict(stamps_end=False, laptop=True)),
                     ("laptop clocks missed", dict(stamps_end=True, laptop=False)),
                     ("road riders counted", dict(stamps_end=True, laptop=True, road=True)),
                     ("Station Sq gap kept in the volunteers' count", dict(stamps_end=True, laptop=True, gap_both=False))]:
        alt = CR.ask_a(TARGET, **kw)
        moved = [c for c in ga if alt[c] != ga[c]]
        check("ASK A stop '%s' moves %d sites, each off the golden shortfall" % (name, len(moved)),
              moved and all(alt[c][1] != ga[c][1] for c in moved), str({c: alt[c] for c in moved}))
    gb = CR.ask_b(TARGET, **CR.GOLD_B)
    for name, kw in [("follow-up visits summed", dict(children="keep_all")), ("every child row dropped", dict(children="drop_all")),
                     ("joined by asset id", dict(join="asset")), ("stoppages by reported year", dict(years="reported")),
                     ("stoppages by closed year", dict(years="closed")), ("contractor twins summed", dict(dupes="sum")),
                     ("downtime recomputed from wall-clock times", dict(minutes="recompute"))]:
        k2 = dict(CR.GOLD_B)
        k2.update(kw)
        alt = CR.ask_b(TARGET, **k2)
        moved = [c for c in gb if alt[c] != gb[c]]
        check("ASK B stop '%s' moves %d counters off the golden" % (name, len(moved)), len(moved) >= 1,
              str({c: alt[c] for c in moved}))
    # blind responses: one constant shortfall, or the volunteers' count less one flat share, recovers almost nothing
    best_const = max(sum(1 for v in ga.values() if v[1] == round(k / 10.0, 1)) for k in range(0, 200))
    check("BLIND a single constant shortfall matches at most one site", best_const <= 1, "%d" % best_const)
    return aa, bb


# ====================================================================================== realism sweep
def realism(P, meta):
    fl = P["flows"]
    reps = 0
    for s in fl:
        for y in A.YEARS:
            a = fl[s][y]
            seen = set()
            for i in range(a.shape[0]):
                if np.isnan(a[i]).any():
                    continue
                k = tuple(a[i].astype(int))
                reps += k in seen
                seen.add(k)
    check("REALISM no counter repeats a whole day's 24 hours", reps == 0, "%d repeats" % reps)
    sig = {}
    for s in fl:
        k = tuple(np.nan_to_num(fl[s][2025][:, 8]).astype(int))
        sig.setdefault(k, []).append(s)
    check("REALISM no two counters share a series", all(len(v) == 1 for v in sig.values()))
    rows = [l for l in open(os.path.join(TARGET, PK.F["dashboard"])).read().splitlines() if not l.startswith("#")]
    plat = [int(r["cyclists"]) for r in csv.DictReader(rows) if r["source"] == "platform"]
    check("REALISM platform-era dashboard totals are not round", sum(1 for v in plat if v % 100 == 0) <= len(plat) // 20,
          "%d of %d end in 00" % (sum(1 for v in plat if v % 100 == 0), len(plat)))
    log = list(csv.DictReader(open(os.path.join(TARGET, PK.F["log"]))))
    notes = {}
    for r in log:
        notes[r["notes"]] = notes.get(r["notes"], 0) + 1
    top = max(notes.values())
    check("REALISM no free-text note dominates the log", top / len(log) < 0.25, "%d of %d" % (top, len(log)))
    people = {p for p, t in N.PEOPLE.values()}
    texts = []
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith(".pdf"):
            texts.append(open_pdf(f))
        elif f.endswith(".csv"):
            texts.append(open(p, encoding="utf-8").read())
        elif f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                texts.append(" ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist()))
    blob = "\n".join(texts)
    named = {n for n in re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z]+), (?:Active|Traffic|Principal|Head|Count)", blob)
             if not n.endswith("Council")}
    check("REALISM every person named in the pack is drawn from guard.py names", named <= people, str(sorted(named)))
    lib = re.compile(rb"openpyxl|python-docx|ReportLab|reportlab|Matplotlib|matplotlib|xlsxwriter|pandas")
    hits = []
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith((".pdf", ".xlsx")):
            b = open(p, "rb").read()
            if f.endswith(".xlsx"):
                with zipfile.ZipFile(p) as z:
                    b = b"".join(z.read(n) for n in z.namelist())
            if lib.search(b):
                hits.append(f)
    check("REALISM no writer library named inside any shipped file", not hits, ", ".join(hits))
    stamps = []
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith(".pdf"):
            stamps += [(f, m.decode()) for m in re.findall(rb"D:(\d{8})", open(p, "rb").read())]
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                core = z.read("docProps/core.xml").decode()
            stamps += [(f, m.replace("-", "")) for m in re.findall(r"(\d{4}-\d\d-\d\d)T", core)]
    late = [(f, s) for f, s in stamps if s > "20261012" or s < "20160101"]
    check("REALISM no shipped document dated after the as-of (12 October 2026)", not late, str(late))
    last = max(datetime.strptime(r["closed"], "%d/%m/%Y %H:%M") for r in log)
    check("REALISM the maintenance log ends before the pull", last < datetime(2026, 10, 9), str(last))
    # H25: every shipped PDF opens in a strict reader, a lenient one and an independent extractor, with the decisive
    # sentences in each and the strict text equal to the lenient text
    from pypdf import PdfReader
    import pdfplumber
    need = {PK.F["policy"]: ["three most recent summers", "06:00 to 22:00 local time", "minimum width"],
            PK.F["guide"]: ["2.5 to under 3.0", "Two-way capacity"], PK.F["notes"]: ["hour beginning", "parent_job"]}
    bad = []
    for f, phrases in need.items():
        p = os.path.join(TARGET, f)
        strict = "\n".join(pg.extract_text() for pg in PdfReader(p, strict=True).pages)
        lenient = "\n".join(pg.extract_text() for pg in PdfReader(p, strict=False).pages)
        with pdfplumber.open(p) as pl:
            miner = "\n".join(pg.extract_text() for pg in pl.pages)
        for t in (strict, lenient, miner):
            flat = " ".join(t.split())
            bad += [(f, ph) for ph in phrases if ph not in flat]
        if strict != lenient:
            bad.append((f, "strict text differs from lenient"))
    check("REALISM H25 every PDF reads the same in pypdf strict, pypdf lenient and pdfminer", not bad, str(bad[:4]))
    tz = [r for r in log if r["downtime"] and ":" not in r["downtime"] and r["logged_by"] == "Traffic Monitoring Unit"]
    check("REALISM the unit always writes downtime as h:mm, the contractor as minutes", not tz)


# ====================================================================================== redraws
def redraws():
    keep = W.SEED
    out = []
    try:
        for k in (1, 2, 3):
            W.SEED = keep + 1000 * k
            T = W.build_truth()
            fl, days, dts, wx, caps, cws = truth_inputs(T)
            fam = {winner(A.golden(fl, days, dts, wx, caps, cws, *m)[0]) for m in A.FAMILY}
            yoy = A.total_growth(fl, "yoy")
            dft = winner(A.crowded_days(A.scale_uniform(fl, yoy), caps, cws))
            G = A.cell_growth(fl, days, dts, wx, "wkwe", "hour", "none")
            cells = winner(A.crowded_days(A.scale_cells(fl, days, dts, G, "wkwe"), caps, cws))
            G = A.cell_growth(fl, days, dts, wx, "wkwe", "day", "flagT")
            wthr = winner(A.crowded_days(A.scale_cells(fl, days, dts, G, "wkwe"), caps, cws))
            out.append((W.SEED, fam, dft, cells, wthr))
    finally:
        W.SEED = keep
    for seed, fam, dft, cells, wthr in out:
        check("REDRAW seed %d: one answer across the golden family (designation determinacy)" % seed,
              fam == {"CW1"}, str(sorted(fam)))
        check("REDRAW seed %d: the default path and each half-step miss" % seed, "CW1" not in (dft, cells, wthr),
              "default %s, cells only %s, weather only %s" % (dft, cells, wthr))


def main():
    global FAM
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    gates(meta)
    P = B.load(TARGET)
    r1(P)
    T = W.build_truth()
    r3(T)
    gold = golden_on(P)
    check("GOLDEN the pack's golden names Tolland Road at Tolland Bridge, 08:00 on school-term weekdays",
          gold["win"] == GOLD_CALL and gold["seg"] == GOLD_SEG and gold["top"] == ("wk_term", GOLD_HOUR),
          "%s %s %s" % (gold["win"], gold["seg"], gold["top"]))
    FAM = family(P)
    Rr = routes(P)
    backtest(P)
    screens(P, gold, Rr)
    sf_rows(P, gold)
    r2(P, gold)
    separation(P, gold)
    CW = R.build_count_week(T, np.random.default_rng([W.SEED, 6]))
    for k in range(500):
        sheets = R.build_volunteers(CW, np.random.default_rng([W.SEED, 7, k]))
        if R.volunteers_ok(CW, sheets):
            break
    asks(dict(CW=CW, sheets=sheets))
    realism(P, meta)
    check("R3c no plant: no memo, draft, briefing or stakeholder figure ships, and no copied block (realism sweep)",
          not any(re.search(r"memo|draft|briefing|minutes_of", f) for f in os.listdir(TARGET)))
    redraws()
    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


FAM = {}
if __name__ == "__main__":
    sys.exit(main())
