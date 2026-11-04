"""checks.py: the generator's assertions on the cut pack and the clean truth. Labels: I input gates, R the three rules
(R1 raw material, R2 per mess item, R3a analyst test, R3b decisive step alone, R3c no plant), L the shift analysis, G the
ladder, SF the semantic fork table, A the asks and their devices, X the realism sweep."""
import datetime as dt
import json
import os
import re
import shutil
import tempfile

import pdfplumber
from openpyxl import load_workbook

import bundle as B
import golden as G
import sim as S
import world as W

FAILS = []


def chk(label, ok, detail=""):
    print("%s  %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)


def text_of(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


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
    easy = G.compute(d, route="rating")
    chk("R3b the easy route on the pack files no deviation", not easy["dev"])
    chk("R3b only the decisive step changed (the post-storm relation) files the golden", g["periods"] == gold,
        str([(a.isoformat(), b.isoformat()) for a, b in g["periods"]]))
    chk("R1a the decisive step reads the stage record and the measurements, not a computed flow",
        not any(re.search(r"discharge|flow_cfs|cfs", open(os.path.join(target, W.FILES["stage"])).read(2000), re.I) for _ in [0]))
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

    # ---- L: the shift analysis
    sh = sorted(g["shifts"], key=lambda v: v["mid"])
    pre = [v for v in sh if v["mid"] < g["peak"]]
    post = [v for v in sh if v["mid"] > g["peak"]]
    chk("L1 every measurement before the storm sits within 1 per cent of Rating 7",
        max(abs(v["pct"]) for v in pre) < 1.0, "largest %.2f%%" % max(abs(v["pct"]) for v in pre))
    chk("L1 every measurement after it sits 10 per cent or more below Rating 7",
        max(v["pct"] for v in post) <= -10.0, "%.1f to %.1f%%" % (min(v["pct"] for v in post), max(v["pct"] for v in post)))
    spread = max(v["shift"] for v in post) - min(v["shift"] for v in post)
    chk("L2 the post-storm shifts agree within 0.02 ft at four stages from 1.99 to 2.68 ft", spread < 0.02,
        "spread %.3f ft, mean %.3f ft" % (spread, g["s_mean"]))
    chk("L3 the storm's peak is the only rise above 5 ft between the last pre-storm and first post-storm measurements",
        g["peak"].date() == dt.date(2026, 7, 27))
    sim_shift = W.SHIFT_FT
    chk("L4 the measured shift recovers the channel's change within 0.01 ft", abs(abs(g["s_mean"]) - sim_shift) < 0.01,
        "%.4f against %.2f" % (abs(g["s_mean"]), sim_shift))

    # ---- G: the ladder
    spot = sorted(v["date"] for v in sh if v["q"] < d["minimum"](v["date"]))
    chk("G1 golden periods: 29 July to 13 September, 21 September to 31 October", g["periods"] == gold)
    chk("G2 rung 0, Rating 7 throughout: no deviation", not easy["dev"])
    chk("G3 rung 1, only the days a measurement fell below the minimum: three days", len(spot) == 3, str(spot))
    near = min(abs(v - d["minimum"](k)) / d["minimum"](k) for k, v in g["daily"].items())
    chk("G4 every day's mean sits 6 per cent or more from its minimum on the golden", near >= 0.06, "closest %.1f%%" % (100 * near))
    near_e = min((v - d["minimum"](k)) / d["minimum"](k) for k, v in easy["daily"].items())
    chk("G5 on Rating 7 every day sits above its minimum by 6 per cent or more", near_e >= 0.06, "closest %.1f%%" % (100 * near_e))

    # ---- SF: semantic fork table
    chk("SF1 local days against the logger's standard-time days: same call", pst["periods"] == g["periods"])
    bounds = [k for k in g["daily"] if k in (dt.date(2026, 6, 30), dt.date(2026, 7, 1), dt.date(2026, 9, 30), dt.date(2026, 10, 1))]
    chk("SF2 the minimum's change days sit clear of it", all(abs(g["daily"][k] - d["minimum"](k)) / d["minimum"](k) > 0.06
                                                           for k in bounds))
    chk("SF3 below against at-or-below the minimum: same call", sorted(k for k, v in g["daily"].items()
                                                                       if v <= d["minimum"](k)) == g["dev"])
    pr = G.compute(d, route="prorate")
    chk("SF5 the shift prorated from measurement to measurement: same call", pr["periods"] == g["periods"])
    ra = G.compute(d, route="ratio")
    chk("SF6 the shift taken as a flow ratio: same call", ra["periods"] == g["periods"])
    chk("SF7 the shift's level, each measurement's own against their mean: same call", pr["periods"] == g["periods"])
    chk("SF8 pre-storm measurements carry no shift (prorated small shifts give the same call)", pr["periods"] == g["periods"])
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
    chk("A2 the spring volumes and the shortfall hold under the prorated and the per-stage shift", G.r100(pr["vol"][5]) ==
        G.r100(g["vol"][5]) and G.r100(pr["vol"][6]) == G.r100(g["vol"][6]) and G.r100(pr["shortfall"]) == G.r100(g["shortfall"]))
    def edge(v, u):
        return u / 2 - abs(v - round(v / u) * u)
    e = min(edge(g["vol"][5], 100), edge(g["vol"][6], 100), edge(g["shortfall"], 100))
    chk("A3 the volumes and the shortfall sit 10 acre-feet or more inside their bins", e >= 10, "closest %.1f AF" % e)
    rec = [k for k in g["daily"] if k.month >= 7]
    same = sum(1 for k in rec if G.r0(pr["daily"][k]) == G.r0(g["daily"][k]))
    chk("A4 the prorated shift gives the same whole-cfs daily mean on every record day but the storm's two",
        same >= len(rec) - 2, "%d of %d" % (same, len(rec)))
    for hw in ("power", "linear", "cap"):
        v = G.compute(d, hiwater=hw)
        chk("A7 the table extended above 4.00 ft (%s) moves the spring peak" % hw,
            G.r0(v["spring_peak"][1]) != G.r0(g["spring_peak"][1]), "%d against %d" % (G.r0(v["spring_peak"][1]),
                                                                                   G.r0(g["spring_peak"][1])))
    chk("A8 the spring peak holds under the prorated shift and sits 0.2 cfs or more inside its whole-cfs bin",
        G.r0(pr["spring_peak"][1]) == G.r0(g["spring_peak"][1]) and edge(g["spring_peak"][1], 1) >= 0.2,
        "%.2f cfs, edge %.2f" % (g["spring_peak"][1], edge(g["spring_peak"][1], 1)))
    hi_days = sorted({t.astimezone(B.PDT).date() for t, h in d["stage"] if h > 4.0 and t.astimezone(B.PDT).month in (5, 6)})
    chk("A5 the high-water segment decides the daily means of the freshet days", len(hi_days) >= 20, "%d days" % len(hi_days))
    chk("A6 separation: the asks' high-water rows never touch a deviation day",
        not set(hi_days) & set(g["dev"]))

    # ---- X: realism sweep and documents
    pdfs = [f for f in files if f.endswith(".pdf")]
    texts = {f: text_of(os.path.join(target, f)) for f in pdfs}
    ctl = "50 cubic feet" in texts[W.FILES["license"]] and "Rating 7" in texts[W.FILES["rating_report"]]
    chk("X1 positive control: the PDF reader finds known sentences", ctl and all(len(t) > 300 for t in texts.values()))
    stump = re.compile(r"\bshift|aggrad|gravel bar|overstat|rating (?:is|was) (?:wrong|out)|re-?rat", re.I)
    hits = {f: stump.findall(t) for f, t in texts.items() if stump.findall(t)}
    for f in files:
        if f.endswith(".csv"):
            h = stump.findall(open(os.path.join(target, f), encoding="utf-8").read())
            if h:
                hits[f] = h
    chk("X2 no shipped document or table names a shift or the rating's error", not hits, str(hits)[:200])
    mtxt = json.dumps(meta).lower()
    chk("X3 metadata.json names no mechanism", not stump.search(mtxt) and "storm" not in mtxt)
    named = set(re.findall(r"\b(?:Marissa Harmon|Melinda Walter|Krista Soto|[A-Z][a-z]+ [A-Z][a-z]+son)\b", " ".join(texts.values())))
    chk("X4 every person named in the documents is a drawn persona", named <= {W.MANAGER, W.HYDROGRAPHER, W.SUPER}, str(named))
    chk("X5 the 2023 memo states nothing after its date and the 2025 report nothing after January 2026",
        not re.search(r"202[4-9]", texts[W.FILES["rating_report"]]) and not re.search(r"2026-(0[2-9]|1)", texts[W.FILES["prior"]]))
    steps = {round(b - a, 3) for (_, a), (_, b) in zip(d["stage"], d["stage"][1:])}
    chk("X6 the stage record is not a constant step or a repeating pattern", len(steps) > 50)
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
