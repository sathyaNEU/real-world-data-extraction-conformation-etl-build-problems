"""The generator's assertions for task466: the three rules executed on the clean truth (R1 to R3c), every row of the
semantic fork table (SF1 to SF15), the ladder and its margins, the graded figures' distance to their rounding edges,
the Layer 1 items' neutrality, the ask's devices and stops, the separation of the call from the ask, the distractors,
the goldens against figures.json, the input gates and the realism sweep.

    python3 task466/generator/checks.py      (after build.py has written target/ and golden/)
"""
import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np                # noqa: E402
from scipy import special, stats  # noqa: E402

import bundle as B                # noqa: E402
import golden as GO               # noqa: E402
import methods as M               # noqa: E402
import pack as P                  # noqa: E402
import sim as S                   # noqa: E402
import world as W                 # noqa: E402

TASK = os.path.dirname(HERE)
PERSONAS = {"Jaime Galloway", "Phyllis Mitchell", "Darryl Powell"}      # guard.py names --geo "United States" --seed 466
MAIN_FILES = ("gauge", "reports", "guidance", "permit", "plan", "station", "offer")
ASK_FILES = ("notices", "scada", "elmhollow", "welllog", "meters")


def edge(v, step=0.01):
    """Distance from v to the nearest rounding edge of its bin."""
    return abs(((v / step) % 1.0) - 0.5) * step


def logs(rec):
    lg = np.log10([v for y, (k, v) in sorted(rec.items()) if k == "gauged"])
    lm = np.log10([v for y, (k, v) in sorted(rec.items()) if k == "measured"])
    silent = sum(1 for k, _ in rec.values() if k == "none")
    return lg, lm, silent


def censored(lg, lm, silent, extra=0):
    return M.decision(*M.fit(np.concatenate([lg, lm]), above=silent + extra))


def minima_by(target, start_month):
    """{year: 7-day low flow} for the complete years of approved record that begin on the first of start_month."""
    rows = B.gauge(target)
    days = [d for d, _, _ in rows]
    q = np.array([v for _, v, _ in rows])
    qual = [c for _, _, c in rows]
    m7 = np.convolve(q, np.ones(7) / 7, mode="full")[:len(q)]
    by = {}
    for i, d in enumerate(days):
        by.setdefault(d.year if d.month >= start_month else d.year - 1, []).append(i)
    out = {}
    for y, idx in by.items():
        if days[idx[0]] != dt.date(y, start_month, 1) or days[idx[-1]] != dt.date(y + 1, start_month, 1) - dt.timedelta(1):
            continue
        if any(not qual[i].startswith("A") for i in idx):
            continue
        out[y] = float(min(m7[i] for i in idx if i >= 6))
    return out


def with_skew(g, fn):
    """Run fn with the methods module's skew set to g (the station-skew reading of SF8)."""
    saved = M.G, M.A, M.LGA
    M.G, M.A = g, 4.0 / g ** 2
    M.LGA = special.gammaln(M.A)
    try:
        return fn()
    finally:
        M.G, M.A, M.LGA = saved


def doc_texts(target):
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = B.pdf_text(p)
        elif f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p)
            out[f] = " ".join(str(c) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for c in r
                              if c is not None)
    return out


def ask_figures(target, supply):
    out = []
    for a, b in B.stage2_periods(target):
        v = [supply[d] for d in B.daterange(a, b)]
        out.append((a, b, float(np.mean(v)), float(np.max(v))))
    return out


def supply_variant(target, elm=True, wells="golden"):
    """The town's own supply under a handling: elm=False keeps Elm Hollow's water in; wells is "golden" (the historian
    until the telemetry failed, the operator's log after), "scada" (the telemetered total throughout) or "none"."""
    sc, eh, wl = B.scada(target), B.elm_hollow(target), B.well_log(target)
    out = {}
    for (d, tag), v in sc.items():
        if tag != "WTP_FIN_TOTAL" or d not in eh:
            continue
        if wells == "golden":
            w = wl.get(d) if d >= W.RADIO_FAILED else sc.get((d, "HR_WELLS_TOTAL"))
        elif wells == "scada":
            w = sc.get((d, "HR_WELLS_TOTAL"))
        else:
            w = 0.0
        if w is None:
            continue
        out[d] = v - (eh[d] if elm else 0.0) + w
    return out


def copy_without(target, keys):
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".chk")
    drop = {W.FILES[k] for k in keys}
    for f in os.listdir(target):
        if f not in drop:
            shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
    return tmp


def run(target, golden, x=None, meta_path=None, fig_path=None):
    bad = []

    def check(label, cond, detail=""):
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))
        if not cond:
            bad.append(label)

    x = x or S.everything()
    F = json.load(open(fig_path or os.path.join(HERE, "figures.json"), encoding="utf-8"))
    meta = json.load(open(meta_path or os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    fx = GO.compute(target)
    g, R = fx["golden"], fx["rungs"]
    rec = fx["record"]
    lg, lm, silent = logs(rec)
    D = W.STAGE2_DEMAND[2027]
    docs = doc_texts(target)
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------ the call
    check("the call: reserve %.1f MGD (%d blocks); the 50-year 7-day low flow %.4f cfs, the withdrawal %.4f MGD, the "
          "shortfall %.4f MGD against %.2f MGD" % (g["block"], fx["blocks"], g["flows"][50], g["withdrawals"][50],
                                                    g["shortfalls"][50], D),
          g["block"] == 0.3 and fx["blocks"] == 3 and F["call"]["block_mgd"] == "0.3")
    check("the record fitted: %d gauged climatic years 1951 to 2024, %d measured report years, %d report years without a "
          "stoppage, %d reports not found" % (fx["gauged"], fx["measured"], fx["silent"], fx["missing"]),
          fx["gauged"] == 74 and fx["measured"] + fx["silent"] + fx["missing"] == 57 and fx["missing"] == 3
          and sorted(y for y, (k, _) in rec.items() if k == "gauged") == list(range(1951, 2025)))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    n_days = (W.EXPORT_DAY - W.GAUGE_START).days + 1
    gauge_rows = B.gauge(target)
    check("R1 the pack ships the river's raw record: %d daily values at the gauge (1951-04-01 to 2026-10-15) and one "
          "report row for each year 1894 to 1950" % len(gauge_rows),
          len(gauge_rows) == n_days and sorted(B.reports(target)) == list(range(1894, 1951)))
    stat_hits = {f: m for f, t in docs.items()
                 for m in re.findall(r"(?:7Q10|7Q2|\d+-year 7-day low flow|design drought flow)[^.]{0,60}?\d\.\d+ ?"
                                     r"(?:cfs|cubic feet)", t)}
    flows = {GO.r2(g["flows"][t]) for t in W.SCENARIOS} | {GO.r2(R[k]["flows"][50]) for k in R}
    num_hits = {f: sorted(v for v in flows if re.search(r"(?<![\d.])%s(?!\d)" % re.escape(v), t)) for f, t in docs.items()}
    check("R1 no shipped document states a low-flow statistic, a design flow or a fitted figure for the river (no rung's "
          "50-year flow and no golden scenario flow in any document)", not stat_hits and not any(num_hits.values()),
          (stat_hits, {f: v for f, v in num_hits.items() if v}))
    check("R1 no shipped column holds an annual 7-day low flow: the gauge exports daily means, the reports a season's "
          "measured flow or a status", open(os.path.join(target, W.FILES["gauge"]), encoding="utf-8").read().count(
              "agency\tstation\tdate\tdischarge_cfs\tqual") == 1)
    check("R1 the decisive computation reads the reports' silent years: %d years enter the likelihood above %.4f cfs"
          % (silent, W.SUSPEND_CFS), silent == fx["silent"] and silent >= 35)

    # ------------------------------------------------------------------ R3: the analyst test on the clean truth
    clean_g = np.log10([v for y, v in sorted(x["gauge_targets"].items()) if W.FIT_YEARS[0] <= y <= W.FIT_YEARS[1]])
    clean_m = np.log10([s["flow"] for y, s in sorted(x["seasons"].items()) if s["suspended"]])
    clean_s = sum(1 for s in x["seasons"].values() if not s["suspended"])
    both_c = np.concatenate([clean_g, clean_m])
    c_r1 = M.decision(*M.fit(both_c))
    c_r2 = M.decision(*M.fit(both_c, above=clean_s))
    c_r1b = M.decision(*M.fit(np.concatenate([both_c, np.full(clean_s, M.LT)])))
    c_r1c = M.decision(*M.fit(clean_g, below=len(clean_m)))
    c_r0 = M.decision(*M.fit(clean_g))
    check("R3a the analyst test on the clean truth: every field read right and every filed rule applied (climatic years, "
          "approved record, units, regional skew, maximum likelihood, passby, Stage 2 demand, smallest block), the fit "
          "to the years that carry a flow reserves %.1f MGD (50-year flow %.4f cfs)" % (c_r1["block"], c_r1["flows"][50]),
          c_r1["block"] == 0.4 and R["R1"]["block"] == 0.4)
    check("R3b the decisive step alone (the silent years as 7-day low flows above the suspension flow) reserves the "
          "golden %.1f MGD on the clean truth (%.4f cfs)" % (c_r2["block"], c_r2["flows"][50]), c_r2["block"] == 0.3)
    check("R3b each lower rung's single correction stays wrong on the clean truth: the silent years at the suspension flow "
          "%.1f, the measured years censored below it %.1f, the gauge alone %.1f" % (
              c_r1b["block"], c_r1c["block"], c_r0["block"]),
          c_r1b["block"] == 0.5 and c_r1c["block"] == 0.4 and c_r0["block"] <= 0.2)
    words = re.compile(r"censor|perception|threshold|survival|truncat|expected moments|historical information|"
                       r"lower bound|upper bound|lower limit|upper limit", re.I)
    named = {f: sorted(set(m.lower() for m in words.findall(t))) for f, t in docs.items()}
    check("R3c no document names the decisive step (censoring, a threshold, a bound, a survival term, historical "
          "information)", not any(named.values()), {f: v for f, v in named.items() if v})
    vals = [v for _, v, _ in gauge_rows]
    run_max, cur = 1, 1
    for a, b in zip(vals, vals[1:]):
        cur = cur + 1 if a == b else 1
        run_max = max(run_max, cur)
    check("R3c no copied or held block in the river's record: the longest run of one daily value is %d days" % run_max,
          run_max <= 12)
    years = {}
    for d, v, _ in gauge_rows:
        years.setdefault(W.climatic_year(d), []).append(v)
    sig = [tuple(v[:300]) for v in years.values() if len(v) >= 300]
    check("R3c no swapped or repeated year in the river's record", len(sig) == len(set(sig)))
    check("R3c no memo, draft or briefing argues a method or a figure: no document mentions 2027 except the plan's "
          "demand table and Castlewick's offer",
          all("2027" not in t for f, t in docs.items() if f not in (W.FILES["plan"], W.FILES["offer"])))

    # ------------------------------------------------------------------ the semantic fork table
    check("SF1 the guidance defines the design drought flow as a climatic year's 7-day low flow with a 0.02 chance of "
          "being undercut", "falls with a probability of 0.02" in docs[W.FILES["guidance"]])
    q98 = float(np.percentile([v for d, v, c in gauge_rows if c.startswith("A") and d < dt.date(2025, 4, 1)], 2))
    check("SF1 the flow-duration reading (the daily flow exceeded on 98 per cent of days, %.2f cfs) gives another block "
          "(%.1f)" % (q98, M.block(M.shortfall(q98))), M.block(M.shortfall(q98)) != 0.3)
    years_conv = {}
    for label, sm in (("water year (October to September)", 10), ("calendar year", 1)):
        mm = minima_by(target, sm)
        d2 = censored(np.log10(list(mm.values())), lm, silent)
        years_conv[sm] = d2
        check("SF2 the %s reading (%d complete approved years) reserves the same %.1f MGD (50-year flow %.4f cfs)" % (
            label, len(mm), d2["block"], d2["flows"][50]), d2["block"] == 0.3)
    months = sorted({d.month for y, (v, d) in x["minima"].items()})
    spans = [a.month for s in x["seasons"].values() if s["suspended"] for a, b in s["spans"]] + \
            [b.month for s in x["seasons"].values() if s["suspended"] for a, b in s["spans"]]
    check("SF2 C1 every gauged year's lowest window ends in %s and every stoppage falls between June and November" % months,
          set(months) <= {7, 8, 9} and set(spans) <= {6, 7, 8, 9, 10, 11})
    rec25 = dict(rec)
    rec25[2025] = ("gauged", B.gauge_minima(target, approved_only=False)[2025])
    d25 = censored(*logs(rec25))
    check("SF3 climatic year 2025 added (its winter provisional) reserves the same %.1f MGD (%.4f cfs)" % (
        d25["block"], d25["flows"][50]), d25["block"] == 0.3)
    check("SF3 the station description dates the approval (September 30, 2025)",
          "approved through September 30, 2025" in docs[W.FILES["station"]])
    near_april = [y for y, (v, d) in x["minima"].items() if d.month == 4 and d.day <= 7]
    check("SF4 C1 no year's lowest window ends in the first week of April, so windows held inside the year or centred "
          "give the same minima", not near_april, near_april)
    rep = B.reports(target)
    alt = [np.log10(v / W.MGD_PER_CFS) if y >= W.UNITS_CHANGE else np.log10(v)
           for y, (k, v) in sorted(rep.items()) if k == "measured"]
    d5 = censored(lg, np.array(alt), silent)
    check("SF5 second-feet read as million gallons a day gives another block (%.1f); the transcription names the unit"
          % d5["block"], d5["block"] != 0.3 and "second-feet (cubic feet per second)" in docs[W.FILES["reports"]])
    meas = [v for y, (k, v) in rep.items() if k == "measured"]
    lt_save = M.LT
    th = {}
    for lvl in (3.09, 3.094, W.SUSPEND_CFS):
        M.LT = math.log10(lvl)
        th[lvl] = censored(lg, lm, silent)
    M.LT = lt_save
    check("SF6 every measured season's flow lies below the agreement's 3.0944 cfs (highest %.3f), and the level taken "
          "as 3.09, 3.094 or 3.0944 cfs gives the same figures" % max(meas),
          max(meas) < W.SUSPEND_CFS and len({(GO.r2(d["flows"][50]), d["block"], round(d["flip_years"])) for d in th.values()}) == 1)
    d7 = censored(lg, lm, silent, extra=3)
    check("SF7 the three missing reports read as years without a stoppage reserve the same %.1f MGD (%.4f cfs)" % (
        d7["block"], d7["flows"][50]), d7["block"] == 0.3)
    check("SF7 the transcription says the three reports were not found",
          "The reports for 1909, 1918 and 1944 have not been found" in docs[W.FILES["reports"]])
    for label, arr in (("the gauge's", lg), ("every measured year's", np.concatenate([lg, lm]))):
        gs = float(stats.skew(arr, bias=False))
        d8 = with_skew(gs, lambda: censored(lg, lm, silent))
        check("SF8 %s station skew (%.3f) in place of the regional -0.30 reserves the same %.1f MGD" % (label, gs, d8["block"]),
              d8["block"] == 0.3)
    d9 = M.decision(*M.ema(np.concatenate([lg, lm]), silent))
    check("SF9 the expected moments algorithm (each silent year's expectation above 3.0944 cfs) reserves the same %.1f "
          "MGD (%.4f cfs)" % (d9["block"], d9["flows"][50]), d9["block"] == 0.3)
    check("SF9 the guidance files maximum likelihood", "estimated by maximum likelihood" in docs[W.FILES["guidance"]])
    whole = M.block(max(0.0, D - min(W.PERMIT_MAX_MGD, g["flows"][50] * W.MGD_PER_CFS)))
    check("SF10 the whole flow without the passby gives another block (%.1f); the permit files the passby" % whole,
          whole != 0.3 and "pass at least 0.50 cubic feet per second" in docs[W.FILES["permit"]])
    d11 = M.block(M.shortfall(g["flows"][50], W.STAGE2_DEMAND[2026]))
    check("SF11 the plan's 2026 Stage 2 demand (%.2f MGD) in place of 2027's reserves the same %.1f MGD" % (
        W.STAGE2_DEMAND[2026], d11), d11 == 0.3)
    nearest = round(g["shortfalls"][50] / W.BLOCK_MGD) * W.BLOCK_MGD
    check("SF12 the nearest block (%.1f MGD) differs from the smallest covering one; the plan files the smallest" % nearest,
          round(nearest, 1) != 0.3 and "smallest block offered that covers" in docs[W.FILES["plan"]])
    check("SF13 at the flip flow (%.4f cfs) the shortfall equals the block, and the flip lies beyond the 50-year flow "
          "(%.2f years)" % (g["flip_flow"], g["flip_years"]),
          abs(M.shortfall(g["flip_flow"]) - g["block"]) < 1e-9 and 50 < g["flip_years"] < 100)
    est_years = {W.climatic_year(d) for d, v, c in gauge_rows if c.endswith(":e")}
    rec16 = {y: kv for y, kv in rec.items() if not (kv[0] == "gauged" and y in est_years)}
    d16 = censored(*logs(rec16))
    head = open(os.path.join(target, W.FILES["gauge"]), encoding="utf-8").read()
    check("SF16 the approved record read as only the days coded A without an estimate (%d climatic years with an "
          "ice-estimated winter day dropped, %d gauged years left) reserves the same %.1f MGD (%.4f cfs); the export's "
          "header codes such a day A:e" % (len(est_years & set(y for y, (k, _) in rec.items() if k == "gauged")),
                                           sum(1 for k, _ in rec16.values() if k == "gauged"), d16["block"],
                                           d16["flows"][50]),
          d16["block"] == 0.3 and "e   value estimated (combined with A or P, e.g. A:e)" in head)
    # ------------------------------------------------------------------ R2: every Layer 1 item real and neutral
    clim = minima_by(target, 4)
    check("R2 the Survey's export (comment lines, a field-width row, qualifier codes): read as a table skipping both, the "
          "%d climatic-year minima equal the golden's" % len(clim),
          {y: round(v, 9) for y, v in clim.items() if W.FIT_YEARS[0] <= y <= W.FIT_YEARS[1]}
          == {y: round(v, 9) for y, (k, v) in rec.items() if k == "gauged"})
    check("R2 the provisional months overlapping the approved record: climatic year 2025 taken in leaves the call (%.1f "
          "MGD)" % d25["block"], d25["block"] == 0.3)
    est_days = {d for d, v, c in gauge_rows if c.endswith(":e")}
    low_windows = {d - dt.timedelta(days=k) for y, (v, d) in x["minima"].items() for k in range(7)}
    check("R2 the ice-estimated winter days (A:e): no year's lowest seven days holds one, so dropping the days moves no "
          "minimum, and dropping their whole years leaves the call (%.1f MGD)" % d16["block"],
          not (est_days & low_windows) and d16["block"] == 0.3)
    check("R2 the climatic year against the water year and the calendar year: each leaves the call (%.1f and %.1f MGD)" % (
        years_conv[10]["block"], years_conv[1]["block"]), years_conv[10]["block"] == years_conv[1]["block"] == 0.3)
    k2 = 0.6463
    alt_units = [np.log10(v * W.MGD_PER_CFS / k2) if y < W.UNITS_CHANGE else np.log10(v)
                 for y, (k, v) in sorted(rep.items()) if k == "measured"]
    du = censored(lg, np.array(alt_units), silent)
    check("R2 the reports' units (gallons a day to 1920, second-feet from 1921) converted at the rounded 0.6463 MGD per "
          "cfs give the same figures (%.4f cfs)" % du["flows"][50],
          GO.r2(du["flows"][50]) == GO.r2(g["flows"][50]) and du["block"] == 0.3)
    check("R2 the three missing reports: read as years without a stoppage they leave the call (%.1f MGD)" % d7["block"],
          d7["block"] == 0.3)
    multi = [y for y, s in x["seasons"].items() if s.get("suspended") and len(s["spans"]) > 1]
    check("R2 the seasons stopped twice (%d years) carry one lowest seven-day flow each, so each report year enters once"
          % len(multi), len(multi) >= 2 and len(rep) == 57)
    gold_sup = B.own_supply(target)
    gold_ask = ask_figures(target, gold_sup)
    shift_ask = ask_figures(target, B.own_supply(target, log_shift=1))
    days_all = [d for d, _, _ in gauge_rows]
    m7 = np.convolve([v for _, v, _ in gauge_rows], np.ones(7) / 7, mode="full")[:len(gauge_rows)]
    trig = [d for d, v in zip(days_all, m7) if d.year >= 2012 and 6 <= d.month <= 11 and v < W.TRIGGER_STAGE2_CFS]
    trig_ask = {}
    for d in trig:
        if d in gold_sup:
            trig_ask.setdefault(d.year, []).append(gold_sup[d])
    moved = sum(1 for a, b, av, hi in gold_ask if a.year in trig_ask and
                (GO.r2(np.mean(trig_ask[a.year])) != GO.r2(av)) + (GO.r2(max(trig_ask[a.year])) != GO.r2(hi)) > 0)
    check("SF14 the days the gauge met the trigger in place of the board's declared periods move %d of %d periods' "
          "figures" % (moved, len(gold_ask)), moved >= len(gold_ask) // 2)

    # ------------------------------------------------------------------ the ladder
    lad = {k: R[k]["block"] for k in ("R0", "R1", "R1b", "R1c", "R1d", "R2")}
    check("ladder: R0 %.1f, R1 %.1f (the default path), R1b %.1f, R1c %.1f, R1d %.1f, R2 %.1f (golden)" % tuple(lad.values()),
          lad == {"R0": 0.1, "R1": 0.4, "R1b": 0.5, "R1c": 0.4, "R1d": 0.3, "R2": 0.3}, lad)
    check("ladder margins: the golden shortfall %.4f sits %.4f inside its block, the default path's %.4f %.4f inside its "
          "own" % (g["shortfalls"][50], min(g["shortfalls"][50] - 0.2, 0.3 - g["shortfalls"][50]), R["R1"]["shortfalls"][50],
                   min(R["R1"]["shortfalls"][50] - 0.3, 0.4 - R["R1"]["shortfalls"][50])),
          0.225 <= g["shortfalls"][50] <= 0.275 and 0.315 <= R["R1"]["shortfalls"][50] <= 0.385)
    check("ladder position: the golden 50-year flow (%.4f) lies between the default path's (%.4f) and the gauge alone "
          "(%.4f)" % (g["flows"][50], R["R1"]["flows"][50], R["R0"]["flows"][50]),
          R["R1"]["flows"][50] < g["flows"][50] < R["R0"]["flows"][50])
    check("ladder: the moments of the values on file (R1m) land with the default path (%.1f)" % R["R1m"]["block"],
          R["R1m"]["block"] == 0.4)

    # ------------------------------------------------------------------ graded figures off their rounding edges
    figs = {"%d-year flow" % t: g["flows"][t] for t in W.SCENARIOS}
    figs.update({"%d-year withdrawal" % t: g["withdrawals"][t] for t in W.SCENARIOS})
    figs.update({"%d-year shortfall" % t: g["shortfalls"][t] for t in W.SCENARIOS if g["shortfalls"][t] > 0})
    figs.update({"default path's 50-year flow": R["R1"]["flows"][50], "gauge-alone 50-year flow": R["R0"]["flows"][50]})
    near = {k: round(edge(v), 5) for k, v in figs.items() if edge(v) < 0.001}
    check("mid-bin: every main figure at least 0.001 from its rounding edge (closest %s %.4f)" % min(
        ((k, edge(v)) for k, v in figs.items()), key=lambda kv: kv[1]), not near, near)
    check("mid-bin: the flip interval %.2f years sits %.2f from its rounding edge" % (
        g["flip_years"], abs((g["flip_years"] % 1) - 0.5)), abs((g["flip_years"] % 1) - 0.5) >= 0.15)
    check("mid-bin: no scenario shortfall between 0 and 0.01 MGD, and none at 10 years (withdrawal %.4f)" % g["withdrawals"][10],
          all(s == 0 or s >= 0.01 for s in g["shortfalls"].values()) and g["shortfalls"][10] == 0
          and g["withdrawals"][10] >= D + 0.02)
    ask_all = [(str(a), v) for a, b, av, hi in gold_ask + shift_ask for v in (av, hi)]
    ask_near = [(a, round(v, 5)) for a, v in ask_all if edge(v) < 0.0008]
    check("mid-bin: every Stage 2 average and highest day, under either log-day convention, at least 0.0008 from its "
          "rounding edge (closest %.4f)" % min(edge(v) for a, v in ask_all), not ask_near, ask_near)
    check("SF15 hazard: the operator log's morning readings assigned to the following day give the same %d figures" % (
        2 * len(gold_ask)), [(GO.r2(av), GO.r2(hi)) for a, b, av, hi in gold_ask]
          == [(GO.r2(av), GO.r2(hi)) for a, b, av, hi in shift_ask])

    # ------------------------------------------------------------------ the ask's devices and stops
    def missed(var):
        return sum((GO.r2(a[2]) != GO.r2(b[2])) + (GO.r2(a[3]) != GO.r2(b[3])) for a, b in zip(gold_ask, var))
    n_ask = 2 * len(gold_ask)
    cracker = ask_figures(target, supply_variant(target, elm=False, wells="scada"))
    plant = ask_figures(target, supply_variant(target, elm=False, wells="none"))
    d4 = ask_figures(target, supply_variant(target, elm=True, wells="scada"))
    d5 = ask_figures(target, supply_variant(target, elm=False, wells="golden"))
    late = [i for i, (a, b, av, hi) in enumerate(gold_ask) if a >= W.RADIO_FAILED]
    check("Ask A: %d declared Stage 2 periods since 2012, in %s" % (len(gold_ask), [a.year for a, b, av, hi in gold_ask]),
          len(gold_ask) >= 5 and all(a.year >= 2012 for a, b, av, hi in gold_ask))
    check("Ask A cracker (finished water plus the telemetered wells, Elm Hollow kept): misses %d of %d" % (
        missed(cracker), n_ask), missed(cracker) == n_ask)
    check("Ask A stop, the plant's finished water alone: misses %d of %d" % (missed(plant), n_ask), missed(plant) == n_ask)
    check("Ask A device D5 (Elm Hollow's water inside the finished water) moves %d of %d figures, by %.3f to %.3f MGD" % (
        missed(d5), n_ask, min(b[2] - a[2] for a, b in zip(gold_ask, d5)), max(b[3] - a[3] for a, b in zip(gold_ask, d5))),
        missed(d5) == n_ask)
    d4_late = sum((GO.r2(gold_ask[i][2]) != GO.r2(d4[i][2])) + (GO.r2(gold_ask[i][3]) != GO.r2(d4[i][3])) for i in late)
    d4_early = sum((GO.r2(gold_ask[i][2]) != GO.r2(d4[i][2])) + (GO.r2(gold_ask[i][3]) != GO.r2(d4[i][3]))
                   for i in range(len(gold_ask)) if i not in late)
    check("Ask A device D4 (the wellfield's telemetry held since 2023-06-14) moves %d of the %d figures after it and none "
          "before" % (d4_late, 2 * len(late)), d4_late == 2 * len(late) and d4_early == 0 and len(late) >= 2)
    held = [v for (d, t), v in B.scada(target).items() if t == "HR_WELLS_TOTAL" and d >= W.RADIO_FAILED]
    check("Ask A device D4 is the historian's own behaviour: one value (%s MG) repeated on every day since the failure, and "
          "the operator log opens with the failure" % held[0], len(set(held)) == 1 and "Telemetry down" in open(
              os.path.join(target, W.FILES["welllog"]), encoding="utf-8").read().split("\n")[1])
    sc_rows = list(csv.DictReader(open(os.path.join(target, W.FILES["scada"]), encoding="utf-8")))
    dup = {}
    for r in sc_rows:
        dup.setdefault((r["Date"], r["Tag"]), []).append(r["DailyTotal"])
    resent = {k: v for k, v in dup.items() if len(v) > 1}
    summed = {}
    for (d, t), v in dup.items():
        if t == "WTP_FIN_TOTAL":
            summed[dt.date.fromisoformat(d)] = sum(float(z) for z in v)
    eh, wl = B.elm_hollow(target), B.well_log(target)
    sc = B.scada(target)
    sum_sup = {d: v - eh[d] + (wl.get(d) if d >= W.RADIO_FAILED else sc[(d, "HR_WELLS_TOTAL")]) for d, v in summed.items()
               if d in eh and (d < W.RADIO_FAILED or d in wl)}
    moved_r = missed(ask_figures(target, sum_sup))
    check("Ask A hazard: the historian restore re-sent %d day-tag rows with identical totals under new record numbers; "
          "summing them moves %d figures" % (len(resent), moved_r),
          len(resent) >= 40 and all(len(set(v)) == 1 for v in resent.values()) and moved_r >= 1)

    # ------------------------------------------------------------------ separation and the distractors
    tmp = copy_without(target, ASK_FILES)
    try:
        rec_s = B.annual_record(tmp)
        same_main = rec_s == rec and censored(*logs(rec_s))["flows"][50] == g["flows"][50]
    finally:
        shutil.rmtree(tmp)
    check("separation: the call and every rung read no notice, historian, master-meter, operator-log or meter-register row "
          "(identical with those files deleted)", same_main)
    tmp = copy_without(target, ("gauge", "reports", "guidance", "permit", "station", "plan", "offer"))
    try:
        same_ask = ask_figures(tmp, B.own_supply(tmp)) == gold_ask
    finally:
        shutil.rmtree(tmp)
    check("separation: the ask reads no gauge, report, guidance, permit, station, plan or offer row (identical with those "
          "files deleted)", same_ask)
    for k in W.DISTRACTORS:
        tmp = copy_without(target, (k,))
        try:
            f2 = GO.compute(tmp)
            same = f2["golden"]["flows"][50] == g["flows"][50] and f2["ask"] == fx["ask"]
        finally:
            shutil.rmtree(tmp)
        check("distractor %s: the call, every scenario and every ask figure unchanged with it deleted" % W.FILES[k], same)
    check("distractors: two named in metadata.json by bundle path",
          sorted(meta["distractor_files"]) == sorted(W.FILES[k] for k in W.DISTRACTORS))

    # ------------------------------------------------------------------ the goldens against figures.json
    memo = B.pdf_text(os.path.join(golden, W.GOLDEN["memo"]))
    want = ["Reserve %s million gallons a day" % F["call"]["block_mgd"],
            "50-year 7-day low flow of %s cubic feet per second" % F["components"]["design_flow_cfs"],
            "%s-year 7-day low flow (%s cfs)" % (F["flip"]["years"], F["flip"]["flow_cfs"])]
    for t in ("10", "25", "50", "100"):
        s = F["scenarios"][t]
        want.append("%s years %s %s %s" % (t, s["flow_cfs"], s["withdrawal_mgd"],
                                           s["shortfall_mgd"] if float(s["shortfall_mgd"]) > 0 else "none"))
    for a in F["ask"]:
        want.append("%s to %s %d %s %s" % (a["start"], a["end"], a["days"], a["average_mgd"], a["highest_mgd"]))
    miss = [w for w in want if w not in memo]
    check("golden memo: the call, the scenario rows, the flip and every Stage 2 row equal figures.json", not miss, miss)
    with open(os.path.join(golden, W.GOLDEN["table"]), encoding="utf-8") as fh:
        crow = list(csv.DictReader(fh))
    kinds = {}
    for r in crow:
        kinds[r["record"]] = kinds.get(r["record"], 0) + 1
    check("golden conformed record: %d rows 1894 to 2024, %d with a flow" % (len(crow), sum(1 for r in crow if r[
        "seven_day_low_flow_cfs"])), len(crow) == F["conformed_rows"] == 131
          and sum(1 for r in crow if r["seven_day_low_flow_cfs"]) == fx["gauged"] + fx["measured"])
    check("golden memo carries its chart", b"/Subtype /Image" in open(os.path.join(golden, W.GOLDEN["memo"]), "rb").read())

    # ------------------------------------------------------------------ the input gates
    rows = {}
    for f in files:
        if f.endswith((".csv", ".txt")):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                rows[f] = sum(1 for line in fh if not line.startswith("#")) - (2 if f.endswith(".txt") else 1)
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("input gates: %d files, %d formats %s, the largest %s with %d rows" % (
        len(files), len(fmts), sorted(fmts), max(rows, key=rows.get), max(rows.values())),
          len(files) >= 10 and len(fmts) >= 3 and max(rows.values()) >= 25000)
    check("every shipped file is in the folder's contents list and the data dictionary covers every data file's columns",
          {r["file"] for r in csv.DictReader(open(os.path.join(target, W.FILES["index"]), encoding="utf-8"))}
          == set(files) - {W.FILES["index"]}
          and all(any(r["file_name"] == f for r in csv.DictReader(open(os.path.join(target, W.FILES["dict"]),
                                                                          encoding="utf-8")))
                  for f in files if f.endswith((".csv", ".txt")) and f not in (W.FILES["dict"], W.FILES["index"])))

    # ------------------------------------------------------------------ the realism sweep
    dash = [f for f in files if not f.endswith((".xlsx", ".pdf"))
            and re.search("[\u2013\u2014]", open(os.path.join(target, f), encoding="utf-8").read())]
    dash += [f for f, t in docs.items() if re.search("[\u2013\u2014]", t)]
    dash += [f for f in os.listdir(golden) if f.endswith(".csv")
             and re.search("[\u2013\u2014]", open(os.path.join(golden, f), encoding="utf-8").read())]
    if re.search("[\u2013\u2014]", memo):
        dash.append("memo")
    check("realism: no em or en dash in any file", not dash, dash)
    late_d = []
    for f in files:
        if f.endswith((".csv", ".txt")):
            t = open(os.path.join(target, f), encoding="utf-8").read()
            late_d += [(f, d) for d in set(re.findall(r"20\d\d-\d\d-\d\d", t)) if d > W.AS_OF]
    check("realism: no date after the folder's as-of date (%s)" % W.AS_OF, not late_d, late_d[:5])
    nulls = [f for f in files if f.endswith((".csv", ".txt"))
             and re.search(r"(^|[,\t])(None|nan|NaN|True|False)([,\t]|\r?$)",
                           open(os.path.join(target, f), encoding="utf-8").read(), re.M)]
    check("realism: no Python null or boolean in any file", not nulls, nulls)
    tool = []
    for folder in (target, golden):
        for f in os.listdir(folder):
            blob = open(os.path.join(folder, f), "rb").read()
            if f.endswith(".xlsx"):
                with zipfile.ZipFile(os.path.join(folder, f)) as z:
                    blob = b"".join(z.read(n) for n in z.namelist())
            if re.search(rb"openpyxl|reportlab|ReportLab|matplotlib|Matplotlib|python", blob):
                tool.append(f)
    check("realism: no writing library named in any file's container, pack or golden", not tool, tool)
    dups = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                body = fh.read().splitlines()[1:]
            dups[f] = len(body) - len(set(body))
    check("R3c realism: no repeated record in any file (the historian's re-sent rows carry new record numbers)",
          not any(dups.values()), {f: v for f, v in dups.items() if v})
    big = {f: n for f, n in rows.items() if n >= 1000}
    check("realism: no large file with a round number of records", all(n % 100 for n in big.values()), big)
    names = set(re.findall(r"\b(?:Jaime|Phyllis|Darryl|Mr\.|Ms\.) [A-Z][a-z]+", " ".join(docs.values()) + memo))
    check("realism: every person named comes from guard.py names (%s)" % sorted(names),
          {n for n in names if not n.startswith(("Mr.", "Ms."))} <= PERSONAS and set(W.PEOPLE.values()) == PERSONAS)
    basis = [r["basis"] for r in csv.DictReader(open(os.path.join(target, W.FILES["notices"]), encoding="utf-8"))
             if r["action"] == "Declared"]
    check("realism: every declared notice quotes its own real-time reading", len(basis) == len(set(basis)))
    below = []
    for r in csv.DictReader(open(os.path.join(target, W.FILES["notices"]), encoding="utf-8")):
        if r["action"] == "Declared":
            level = W.TRIGGER_STAGE2_CFS if r["stage"] == "Stage 2" else W.TRIGGER_STAGE1_CFS
            below.append(float(re.search(r"(\d+\.\d\d) cfs", r["basis"]).group(1)) < level)
    check("realism: every declaration quotes a reading below the level that triggers its stage", all(below) and below)
    import openpyxl
    reg = {r[0]: r[5] for r in openpyxl.load_workbook(os.path.join(target, W.FILES["meters"]))["Meters"].iter_rows(
        min_row=5, values_only=True) if r[0]}
    first = {"WTP-RAW": min(d for d, t in B.scada(target) if t == "WTP_RAW_TOTAL"),
             "WTP-FIN": min(d for d, t in B.scada(target) if t == "WTP_FIN_TOTAL"),
             "HR-WF": min(d for d, t in B.scada(target) if t == "HR_WELLS_TOTAL"),
             "EH-01": min(B.elm_hollow(target))}
    check("realism: every meter in the register went into service before the first value its tag or file carries",
          all(dt.date.fromisoformat(str(reg[m])[:10]) < d for m, d in first.items()), {m: reg.get(m) for m in first})
    mins = [round(v, 3) for v in fx["record"].values() if v[1] is not None for v in [v[1]]]
    check("realism: no two record years share a 7-day low flow to the thousandth",
          len(mins) - len(set(mins)) <= 1, len(mins) - len(set(mins)))
    print("%d checks failed" % len(bad) if bad else "all checks passed")
    return not bad


if __name__ == "__main__":
    ok = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    sys.exit(0 if ok else 1)
