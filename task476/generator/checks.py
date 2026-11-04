"""checks.py: the generator's assertions on the cut pack and the clean truth. Labels: I input gates, R the three rules
(R1 raw material, R2 per mess item, R3a analyst test, R3b decisive step alone, R3c no plant, R3d no defect anywhere),
L the measurement analysis, G the ladder, B the licensed correction forms and the grading bands, SF the semantic fork
table, A the asks and their devices, X the realism sweep."""
import datetime as dt
import json
import os
import re
import shutil
import tempfile

import pdfplumber
from openpyxl import load_workbook

import bundle as B
import docs as D
import golden as G
import sim as S
import world as W

FAILS = []
FORMS = [("shift", "mean"), ("shift", "median"), ("shift", "ls"), ("shift", "each"), ("shift", "stage"),
         ("ratio", "mean"), ("ratio", "median"), ("ratio", "ls"), ("ratio", "each")]
ONSETS = ("day27", "day28", "day29", "visit", "ramp")
MET_ONLY = G.MET_ONLY_DAYS


def chk(label, ok, detail=""):
    print("%s  %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)


def text_of(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


def licensed(d):
    """Every correction the monitoring plan's standard methods leave open, run through the golden's own code: the
    post-storm correction's form and level, the earlier measurements' small corrections or none, the staff readings as
    gauge-height corrections or not, and the correction's onset."""
    out = {}
    for form, level in FORMS:
        for pre in ("none", "each", "each0"):
            for gc in (False, True):
                out[(form, level, "peak", pre, gc)] = G.compute(d, form=form, level=level, pre=pre, ghcorr=gc)
    for onset in ONSETS:
        for form, level in FORMS:
            for pre in ("none", "each"):
                out[(form, level, onset, pre, False)] = G.compute(d, form=form, level=level, onset=onset, pre=pre)
    return out


def main(target, gdir, x):
    del FAILS[:]
    d = B.load(target)
    g = G.compute(d)
    gold = [[dt.date(2026, 7, 29), dt.date(2026, 9, 13)], [dt.date(2026, 9, 21), dt.date(2026, 10, 31)]]
    files = []
    for root, _, fs in os.walk(target):
        files += [os.path.relpath(os.path.join(root, f), target) for f in fs]
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))

    # ---- I: input gates
    chk("I1 ten or more files", len(files) >= 10, "%d" % len(files))
    chk("I2 three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, str(sorted({f.rsplit(".", 1)[1] for f in files})))
    chk("I3 a file of 25,000 or more rows", len(d["stage"]) >= 25000, "stage record %d rows" % len(d["stage"]))
    chk("I4 two or more distractors in metadata.json", len(meta["distractor_files"]) >= 2)
    wb = load_workbook(os.path.join(target, W.FILES["register"]), read_only=True)
    bad = [f for f in files if re.search(r"readme|dictionar|notes|manifest|codebook|schema", f, re.I)]
    bad += [s for s in wb.sheetnames if re.search(r"readme|dictionar|notes|about", s, re.I)]
    chk("I5 no file or sheet describing the data", not bad, str(bad))
    tmp = tempfile.mkdtemp()
    shutil.copytree(target, os.path.join(tmp, "t"))
    for f in meta["distractor_files"]:
        os.remove(os.path.join(tmp, "t", f))
    g2 = G.compute(B.load(os.path.join(tmp, "t")))
    shutil.rmtree(tmp)
    chk("I6 golden unchanged with every distractor deleted", g2["periods"] == g["periods"] and g2["vol"] == g["vol"])

    # ---- R: the three rules
    truth = S.daily_truth(x)
    dev_truth = sorted(k for k, v in truth.items() if v["true"] < W.requirement(k))
    dev_rated = sorted(k for k, v in truth.items() if v["rated"] < W.requirement(k))
    chk("R3a analyst test on the clean truth: Rating 7 on the stage record files no deviation", not dev_rated,
        "%d days" % len(dev_rated))
    chk("R3a the clean truth's deviations are the golden's", dev_truth == g["dev"], "%d days" % len(dev_truth))
    rows = x["rows"]
    st_ok = len(rows) == len(d["stage"]) and all(t == r["t"] and abs(h - r["h"]) <= 0.0005 + 1e-9
                                                  for (t, h), r in zip(d["stage"], rows))
    chk("R3d no defect: every shipped stage reading is the logger's stage at its 0.001 ft resolution, on the clock the "
        "header names", st_ok)
    chk("R3d no defect: the register's table is Rating 7 at every 0.01 ft", all(abs(q - D.table_q(h)) < 1e-9
                                                                              for h, q in d["table"].items()))
    gauged = [(v, sv) for v, sv in zip(sorted(d["visits"], key=lambda v: v["mid"]), x["visits"])]
    honest = all(abs(v["q"] / sv["q_true"] - 1) < 0.025 and abs(v["gh"] - sv["gh"]) <= 0.005 + 1e-9 for v, sv in gauged)
    chk("R3d no defect: every measurement is the reach's flow while it ran within 2.5 per cent, at the logger's mean "
        "gauge height", honest, "largest error %.2f%%" % max(100 * abs(v["q"] / sv["q_true"] - 1) for v, sv in gauged))
    chk("R3d no defect: the shift is a change in the channel the truth carries (the flow the reach passed at each stage), "
        "not in any record", all(abs(r["bypass"] - W.q_true(r["h"], r["t"])) < 0.05 for r in rows[::37]))
    easy = G.compute(d, route="rating")
    chk("R3b the easy route on the pack files no deviation", not easy["dev"])
    chk("R3b only the decisive step changed (the post-storm relation) files the golden", g["periods"] == gold,
        str([(a.isoformat(), b.isoformat()) for a, b in g["periods"]]))
    chk("R1a the decisive step reads the stage record and the measurements, not a computed flow",
        not re.search(r"discharge|flow_cfs|cfs", open(os.path.join(target, W.FILES["stage"])).read(2000), re.I))
    cols = []
    for f in files:
        if f.endswith(".csv"):
            lines = open(os.path.join(target, f), encoding="utf-8").read().splitlines()
            hdr = next(l for l in lines if "," in l and not l.startswith(("Site", "Parameter", "Instrument", "Time", "Exported")))
            cols += hdr.split(",")
    hit = [c for c in cols if re.search(r"shift|rated|rating|true|correct|deviation|bypass_flow", c, re.I)]
    chk("R1b no shipped column holds a flow on any relation, a shift or a deviation", not hit, str(hit))
    pst = G.compute(d, days="pst")
    chk("R2 the logger's standard-time days used as local days: same deviations", pst["periods"] == g["periods"])
    for hw in ("power", "linear", "cap"):
        v = G.compute(d, hiwater=hw)
        chk("R2 the table extended above 4.00 ft (%s) instead of the memo's segment: same deviations" % hw,
            v["periods"] == g["periods"])
    blocks = [tuple(round(h, 3) for _, h in d["stage"][i:i + 144]) for i in range(0, len(d["stage"]) - 144, 144)]
    chk("R3c no copied block of stage readings", len(set(blocks)) == len(blocks))

    # ---- L: the measurements against Rating 7
    on, post = g["on"], g["post"]
    chk("L1 every measurement before the storm sits within 3 per cent of Rating 7, either side",
        max(abs(v["pct"]) for v in on) <= 3.0 and min(v["pct"] for v in on) < 0 < max(v["pct"] for v in on),
        "%.1f to %+.1f%%" % (min(v["pct"] for v in on), max(v["pct"] for v in on)))
    chk("L1 every measurement after it sits 10 per cent or more below Rating 7",
        max(v["pct"] for v in post) <= -10.0, "%.1f to %.1f%%" % (min(v["pct"] for v in post), max(v["pct"] for v in post)))
    sep = abs(max(v["pct"] for v in post)) / max(abs(v["pct"]) for v in on)
    chk("L1 separation: the nearest post-storm measurement sits five times further off than the furthest earlier one, "
        "and more than twice the 5 per cent the memo's measurements stay within", sep >= 5.0 and
        abs(max(v["pct"] for v in post)) > 10.0, "%.1f times" % sep)
    spread = max(v["shift"] for v in post) - min(v["shift"] for v in post)
    chk("L2 the post-storm stage shifts agree within 0.01 ft across their gauge heights", spread < 0.01,
        "spread %.4f ft at %.2f to %.2f ft, mean %.4f ft" % (spread, min(v["gh"] for v in post), max(v["gh"] for v in post),
                                                           g["s_mean"]))
    chk("L3 the storm's peak is the highest stage between the last measurement on Rating 7 and the first off it, on 27 July",
        g["peak"].date() == dt.date(2026, 7, 27))
    chk("L4 the measured shift recovers the channel's change within 0.005 ft", abs(abs(g["s_mean"]) - W.SHIFT_FT) < 0.005,
        "%.4f against %.2f" % (abs(g["s_mean"]), W.SHIFT_FT))

    # ---- G: the ladder
    spot = sorted(v["date"] for v in g["shifts"] if v["q"] < d["minimum"](v["date"]))
    chk("G1 golden periods: 29 July to 13 September, 21 September to 31 October", g["periods"] == gold)
    chk("G2 rung 0, Rating 7 throughout: no deviation", not easy["dev"])
    chk("G3 rung 1, only the days a measurement fell below the minimum: three days", len(spot) == 3, str(spot))
    near = min(abs(v - d["minimum"](k)) / d["minimum"](k) for k, v in g["daily"].items())
    chk("G4 every day's mean sits 6 per cent or more from its minimum on the golden", near >= 0.06, "closest %.1f%%" % (100 * near))
    near_e = min((v - d["minimum"](k)) / d["minimum"](k) for k, v in easy["daily"].items())
    chk("G5 on Rating 7 every day sits above its minimum by 6 per cent or more", near_e >= 0.06, "closest %.1f%%" % (100 * near_e))

    # ---- B: every licensed correction form against the golden, and the grading bands
    lic = licensed(d)
    rec = [k for k in g["daily"] if k.month >= 7]
    graded = [k for k in rec if k not in MET_ONLY]
    met = lambda r, k: r["daily"][k] >= d["minimum"](k)
    chk("B1 every licensed form files the golden's periods and the same met flag on every record day",
        all(v["periods"] == g["periods"] and all(met(v, k) == met(g, k) for k in rec) for v in lic.values()),
        "%d forms" % len(lic))
    du = max(abs(v["daily"][k] - g["daily"][k]) for v in lic.values() for k in graded)
    dr = max(abs(G.r0(v["daily"][k]) - G.r0(g["daily"][k])) for v in lic.values() for k in graded)
    chk("B2 every licensed form's whole-cfs daily mean sits within the %d cfs band of the golden's on every record day "
        "but 27, 28 and 29 July (unrounded within 1.5)" % G.BAND_CFS, dr <= G.BAND_CFS and du < 1.5,
        "largest %d cfs whole, %.2f unrounded" % (dr, du))
    gap = min(abs(v["daily"][k] - d["minimum"](k)) for v in list(lic.values()) + [g] for k in MET_ONLY)
    chk("B3 27, 28 and 29 July carry the golden's verdict under every form and onset (27 and 28 met, 29 below; graded on "
        "met only), 0.25 cfs or more from the minimum", all(met(v, k) == met(g, k) for v in lic.values() for k in MET_ONLY)
        and met(g, MET_ONLY[0]) and met(g, MET_ONLY[1]) and not met(g, MET_ONLY[2]) and gap >= 0.25,
        "closest %.2f cfs (29 July with the correction from the first measurement after the storm: %.1f cfs)"
        % (gap, lic[("shift", "mean", "visit", "none", False)]["daily"][MET_ONLY[2]]))
    sf = sorted(v["shortfall"] for v in lic.values())
    chk("B4 the shortfall rounds to the golden's 100 acre-feet under every licensed form",
        all(G.r100(s) == G.r100(g["shortfall"]) for s in sf), "%.1f to %.1f" % (sf[0], sf[-1]))
    edge = min(G.SHORT_BAND_AF - abs(s - G.r100(g["shortfall"])) for s in sf)
    chk("B4 every licensed form's shortfall sits 40 acre-feet or more inside the %d acre-foot grading band"
        % G.SHORT_BAND_AF, edge >= 40, "closest %.1f AF" % edge)
    spring_same = all(G.r100(v["vol"][5]) == G.r100(g["vol"][5]) and G.r100(v["vol"][6]) == G.r100(g["vol"][6]) and
                      G.r0(v["spring_peak"][1]) == G.r0(g["spring_peak"][1]) and v["spring_peak"][0] == g["spring_peak"][0]
                      for v in list(lic.values()) + [pst, G.compute(d, days="pst", pre="each")])
    chk("B5 the May and June volumes and the spring peak (flow and time) are the golden's under every licensed form and on "
        "the logger's standard-time months", spring_same,
        "May %.0f to %.0f, June %.0f to %.0f" % (min(v["vol"][5] for v in lic.values()), max(v["vol"][5] for v in lic.values()),
                                                 min(v["vol"][6] for v in lic.values()), max(v["vol"][6] for v in lic.values())))
    post_days = [k for k in graded if k >= dt.date(2026, 7, 29)]
    chk("B6 the band separates: Rating 7 throughout falls outside it on every graded day after the storm",
        all(abs(G.r0(easy["daily"][k]) - G.r0(g["daily"][k])) > G.BAND_CFS for k in post_days),
        "closest %d cfs" % min(abs(G.r0(easy["daily"][k]) - G.r0(g["daily"][k])) for k in post_days))

    stated = G.compute(d, fixed=float("%.4f" % g["s_mean"]))
    chk("B7 the solution's stated shift (%.4f ft) recomputes every graded figure: each whole-cfs daily mean, the "
        "periods, the shortfall and the spring figures" % g["s_mean"],
        all(G.r0(stated["daily"][k]) == G.r0(g["daily"][k]) for k in rec) and stated["periods"] == g["periods"] and
        G.r100(stated["shortfall"]) == G.r100(g["shortfall"]) and stated["vol"] == g["vol"])
    tenth = G.compute(d, fixed=-0.10)
    chk("B7 the shift rounded to 0.10 ft lands inside every band (cells within %d cfs, every met flag the golden's, the shortfall "
        "to the same 100)" % G.BAND_CFS, all(abs(G.r0(tenth["daily"][k]) - G.r0(g["daily"][k])) <= G.BAND_CFS for k in graded)
        and all(met(tenth, k) == met(g, k) for k in rec) and G.r100(tenth["shortfall"]) == G.r100(g["shortfall"]),
        "%d cells differ by 1 cfs" % sum(1 for k in rec if G.r0(tenth["daily"][k]) != G.r0(g["daily"][k])))

    # ---- SF: semantic fork table
    chk("SF1 local days against the logger's standard-time days: same call", pst["periods"] == g["periods"])
    bounds = [k for k in g["daily"] if k in (dt.date(2026, 6, 30), dt.date(2026, 7, 1), dt.date(2026, 9, 30), dt.date(2026, 10, 1))]
    chk("SF2 the minimum's change days sit clear of it", all(abs(g["daily"][k] - d["minimum"](k)) / d["minimum"](k) > 0.06
                                                           for k in bounds))
    chk("SF3 below against at-or-below the minimum: same call", sorted(k for k, v in g["daily"].items()
                                                                       if v <= d["minimum"](k)) == g["dev"])
    sub = lambda f: [v for k, v in lic.items() if f(k)]
    same = lambda vs: all(v["periods"] == g["periods"] for v in vs)
    chk("SF5 the correction's onset (the storm's peak, local midnight on 27, 28 or 29 July, the first measurement off "
        "the rating, ramped from the last measurement on it): same call", same(sub(lambda k: k[2] != "peak")))
    chk("SF6 the correction's form, a stage shift or a flow ratio: same call", same(sub(lambda k: k[0] == "ratio")))
    chk("SF7 the correction's level (mean, median, least squares, each measurement's own prorated, varying with stage): "
        "same call", same(sub(lambda k: k[0] == "shift")))
    chk("SF8 the earlier measurements' small departures carried as corrections: same call", same(sub(lambda k: k[3] != "none")))
    chk("SF13 the staff readings' differences from the logger applied as gauge-height corrections: same call",
        same(sub(lambda k: k[4])))
    chk("SF9 above 4.00 ft, the memo's segment against the table extended: same call",
        all(G.compute(d, hiwater=hw)["periods"] == g["periods"] for hw in ("power", "linear", "cap")))
    chk("SF10 the daily mean of 10-minute flows against the flow at the day's mean stage: same call",
        sorted(k for k, v in _mean_stage_daily(d, g).items() if v < d["minimum"](k)) == g["dev"])
    chk("SF11 the bypassed reach's flow is BP-1's: the plan puts it upstream of any tributary inflow",
        "upstream of any tributary inflow" in re.sub(r"\s+", " ", text_of(os.path.join(target, W.FILES["plan"]))))
    chk("SF12 a deviation period is a run of consecutive deviation days", all(
        (b - a).days + 1 == sum(1 for k in g["dev"] if a <= k <= b) for a, b in g["periods"]))

    # ---- A: the asks
    for hw in ("power", "linear", "cap"):
        v = G.compute(d, hiwater=hw)
        chk("A1 the table extended above 4.00 ft (%s) moves both spring volumes" % hw,
            G.r100(v["vol"][5]) != G.r100(g["vol"][5]) and G.r100(v["vol"][6]) != G.r100(g["vol"][6]),
            "May %d against %d, June %d against %d" % (G.r100(v["vol"][5]), G.r100(g["vol"][5]), G.r100(v["vol"][6]),
                                                       G.r100(g["vol"][6])))

    def edge_of(v, u):
        return u / 2 - abs(v - round(v / u) * u)
    e = min(edge_of(v, 100) for r in list(lic.values()) + [g] for v in (r["vol"][5], r["vol"][6]))
    chk("A3 the spring volumes sit 10 acre-feet or more inside their bins under every licensed form", e >= 10,
        "closest %.1f AF" % e)
    for hw in ("power", "linear", "cap"):
        v = G.compute(d, hiwater=hw)
        chk("A7 the table extended above 4.00 ft (%s) moves the spring peak" % hw,
            G.r0(v["spring_peak"][1]) != G.r0(g["spring_peak"][1]), "%d against %d" % (G.r0(v["spring_peak"][1]),
                                                                                   G.r0(g["spring_peak"][1])))
    pk = [r["spring_peak"][1] for r in list(lic.values()) + [g]]
    chk("A8 the spring peak sits 0.2 cfs or more inside its whole-cfs bin under every licensed form",
        min(edge_of(v, 1) for v in pk) >= 0.2, "%.2f to %.2f cfs" % (min(pk), max(pk)))
    hi_days = sorted({t.astimezone(B.PDT).date() for t, h in d["stage"] if h > 4.0 and t.astimezone(B.PDT).month in (5, 6)})
    chk("A5 the high-water segment decides the daily means of the freshet days", len(hi_days) >= 20, "%d days" % len(hi_days))
    chk("A6 separation: the asks' high-water rows never touch a deviation day", not set(hi_days) & set(g["dev"]))

    # ---- X: realism sweep and documents
    pdfs = [f for f in files if f.endswith(".pdf")]
    texts = {f: text_of(os.path.join(target, f)) for f in pdfs}
    ctl = "50 cubic feet" in texts[W.FILES["license"]] and "Rating 7" in texts[W.FILES["rating_report"]]
    chk("X1 positive control: the PDF reader finds known sentences", ctl and all(len(t) > 300 for t in texts.values()))
    stump = re.compile(r"\bshift|aggrad|gravel bar|overstat|rating (?:is|was) (?:wrong|out)|re-?rat|\bfill\b|scour|"
                       r"rework|reshap", re.I)
    hits = {f: stump.findall(t) for f, t in texts.items() if stump.findall(t)}
    for f in files:
        if f.endswith(".csv"):
            h = stump.findall(open(os.path.join(target, f), encoding="utf-8").read())
            if h:
                hits[f] = h
    chk("X2 no shipped document or table names a shift, a changed control or the rating's error", not hits, str(hits)[:200])
    mtxt = json.dumps(meta).lower()
    chk("X3 metadata.json names no mechanism", not stump.search(mtxt) and "storm" not in mtxt)
    named = set(re.findall(r"\b(?:Marissa Harmon|Melinda Walter|Krista Soto|[A-Z][a-z]+ [A-Z][a-z]+son)\b", " ".join(texts.values())))
    chk("X4 every person named in the documents is a drawn persona", named <= {W.MANAGER, W.HYDROGRAPHER, W.SUPER}, str(named))
    chk("X5 the 2023 memo states nothing after its date and the 2025 report nothing after January 2026",
        not re.search(r"202[4-9]", texts[W.FILES["rating_report"]]) and not re.search(r"2026-(0[2-9]|1)", texts[W.FILES["prior"]]))
    steps = {round(b - a, 3) for (_, a), (_, b) in zip(d["stage"], d["stage"][1:])}
    chk("X6 the stage record is not a constant step or a repeating pattern", len(steps) > 50)
    vis = sorted(d["visits"], key=lambda v: v["mid"])
    durs = {int((v["end"] - v["start"]).total_seconds() // 60) for v in vis}
    setups = {int((v["start"] - v["arrival"]).total_seconds() // 60) for v in vis}
    diffs = {round(v["staff"] - v["logger"], 2) for v in vis}
    rem = [v["remarks"] for v in vis]
    chk("X7 the visit log varies as a hydrographer's does: measurement lengths, set-up times, staff against logger, "
        "remarks", len(durs) >= 6 and len(setups) >= 6 and len(diffs) >= 3 and max(abs(c) for c in diffs) <= 0.02 and
        len(set(rem)) == len(rem), "%d lengths, %d set-ups, differences %s" % (len(durs), len(setups), sorted(diffs)))
    mm = [(dd, e_) for dd, _, e_ in D.R7_MEAS]
    chk("X8 the memo's 17 measurements scatter as gaugings do: within 5 per cent, signs in runs, sizes from under 1 to "
        "over 4 per cent", max(abs(e_) for _, e_ in mm) < 0.05 and max(abs(e_) for _, e_ in mm) > 0.04 and
        min(abs(e_) for _, e_ in mm) < 0.01 and any((a > 0) == (b > 0) for (_, a), (_, b) in zip(sorted(mm), sorted(mm)[1:])))
    print("checks: %d failures" % len(FAILS))
    return not FAILS


def _mean_stage_daily(d, g):
    qf = G.rating(d)
    acc = {}
    for t, h in d["stage"]:
        day = t.astimezone(B.PDT).date()
        if not (dt.date(2026, 5, 1) <= day <= dt.date(2026, 10, 31)):
            continue
        a = acc.setdefault(day, [0.0, 0, t])
        a[0] += h
        a[1] += 1
    out = {}
    for k, (s, n, t) in acc.items():
        sh = g["s_mean"] if k > g["peak"].date() else 0.0
        out[k] = qf(s / n + sh)
    return out
