"""The generator's assertions on the cut pack: the ladder, the margins, the forks, the separation, the asks' stops
and the input gates.

    python3 task125/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs as F    # noqa: E402
import pack as P    # noqa: E402
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLD = ["KH1", "MZ4", "NT1", "NY2"]
DEFAULT = ["KH1", "MZ2", "NT1", "NY3"]
ALLOC = {r[0]: r[5] for r in W.RU}
N = [0, 0]


def ok(label, cond, detail=""):
    N[0] += 1
    if cond:
        print("PASS  " + label)
    else:
        N[1] += 1
        print("FAIL  " + label + ("  " + str(detail) if detail != "" else ""))


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in PdfReader(path).pages))


def main(target=TARGET):
    D = F.load(target)
    g = F.season_loads(D, "golden")
    p = F.season_loads(D, "point")
    runs = F.dry_runs(D)
    ok("the dry season holds the routine runs from 1 May to 30 September 2026", len(runs) == 11 and
       runs[0] >= W.DRY0 and runs[-1] <= W.DRY1, len(runs))
    ok("R3 the conserved loads file the golden set", F.over_set(g) == GOLD, F.over_set(g))
    ok("R0 the boundary sample times the boundary flow files the default set", F.over_set(p) == DEFAULT, F.over_set(p))
    ok("R2 the flow-weighted ratio estimator on the boundary samples files the default set",
       F.over_set(F.ratio_loads(D)) == DEFAULT)
    # every golden verdict at least 8 per cent from its allocation; the default's flipped units 8 per cent the other way
    marg = {c: g[c] / ALLOC[c] - 1 for c in g}
    ok("margins: every unit's conserved load at least 8 per cent from its allocation",
       min(abs(v) for v in marg.values()) >= 0.08, {c: round(v, 3) for c, v in marg.items()})
    ok("margins: the four flipped units' boundary loads at least 8 per cent across the allocation the other way",
       all(abs(p[c] / ALLOC[c] - 1) >= 0.08 and (p[c] > ALLOC[c]) != (g[c] > ALLOC[c]) for c in
           ("MZ2", "MZ4", "NY2", "NY3")))
    # the alternatives inside the standing family converge: the section's blend times the boundary flow, and the next
    # mixed weir below read for the unit
    alt = {}
    for code, weir, inflows in D["ru"]:
        vals = []
        for d in runs:
            q = D["flow"][(D["station"][weir], d.isoformat())]
            if inflows:
                qin = sum(D["flow"][(D["station"][[u for u in D["ru"] if u[0] == i][0][1]], d.isoformat())]
                          for i in inflows)
                vals.append(F.conserved_load(D, code, d) / qin * q)
            else:
                vals.append(F.point_load(D, code, d))
        alt[code] = float(np.mean(vals))
    ok("SF1 the blend's concentration times the boundary flow gives the same set and whole tonnes",
       F.over_set(alt) == GOLD and all(round(alt[c]) == round(g[c]) for c in g),
       {c: (round(alt[c], 2), round(g[c], 2)) for c in g if round(alt[c]) != round(g[c])})
    down = {"MZ2": ("MZ3", []), "MZ4": ("MZ5", ["GB1"]), "NY3": ("NY4", []), "NY2": ("NY4", ["MP1"])}
    for code, (below, joins) in down.items():
        v = np.mean([F.point_load(D, below, d) - sum(F.point_load(D, j, d) for j in joins) for d in runs])
        ok("SF2 %s read at the mixed weir below (%s, less what joins between) lands the same verdict" % (code, below),
           (v > ALLOC[code]) == (g[code] > ALLOC[code]) and abs(v / g[code] - 1) < 0.01, round(v, 2))
    for code in ("MZ3", "MZ5", "NY4"):
        ok("the mixed boundary %s agrees with what its inflows carry in within one per cent" % code,
           abs(p[code] / g[code] - 1) < 0.01, round(p[code] / g[code], 4))
    # the default's inconsistency is there on every run, at the four weirs only
    bad = {}
    for code, weir, inflows in D["ru"]:
        if not inflows:
            continue
        r = [F.point_load(D, code, d) / sum(F.conserved_load(D, i, d) for i in inflows) for d in runs]
        bad[code] = (min(r), max(r))
    ok("the four boundary loads break the balance on every run by more than 12 per cent, the others within 3",
       all(not (0.88 < bad[c][0] and bad[c][1] < 1.12) for c in ("MZ2", "MZ4", "NY2", "NY3")) and
       all(0.97 < bad[c][0] and bad[c][1] < 1.03 for c in ("MZ3", "MZ5", "NY4")), bad)
    # mess-neutral: the first laboratory result instead of the re-run, and the UTC day for the gauges, leave the call
    so4_first = {}
    for r in F._rows(target, "lab"):
        if r["analyte"] == "SO4" and not r["lab_sample_id"].endswith("-R"):
            so4_first[(r["site_code"], r["sample_date"])] = float(r["result"])
    D2 = dict(D)
    D2["so4"] = so4_first
    ok("SF3 a re-run's first result instead of the re-run leaves both sets", F.over_set(F.season_loads(D2, "golden"))
       == GOLD and F.over_set(F.season_loads(D2, "point")) == DEFAULT)
    ok("SF4 above the allocation and at or above it agree (no unit within 0.5 t/d of its allocation)",
       min(abs(g[c] - ALLOC[c]) for c in g) > 0.5)
    ok("SF5 sulfate as SO4 throughout the laboratory's results (no as-S unit on the call's path)",
       all(r["unit"] == "mg/L" for r in F._rows(target, "lab") if r["analyte"] == "SO4"))
    # the shock: the golden set is no interval of any shipped statistic's sort
    stats = {"boundary load": p, "allocation": ALLOC,
             "boundary sulfate": {c: np.mean([D["so4"][(D["boundary"][c], d.isoformat())] for d in runs]) for c in g},
             "boundary flow": {c: np.mean([D["flow"][(D["station"][[u for u in D["ru"] if u[0] == c][0][1]],
                                                      d.isoformat())] for d in runs]) for c in g}}
    for name, s in stats.items():
        order = sorted(s, key=lambda c: -s[c])
        k = len(GOLD)
        ok("shock: the golden set is not the top or bottom four by %s" % name,
           set(order[:k]) != set(GOLD) and set(order[-k:]) != set(GOLD))
    # pins: the schedule files the WHAT and names no mixing, plume, bank or balance
    text = pdf_text(os.path.join(target, P.FILES["schedule"]))
    ok("the schedule reads (positive control)", "carries past its lower boundary" in text and "Table 2" in text)
    ok("pins: no filed sentence names mixing, a plume, a bank, a balance or conservation",
       not re.search(r"mix|plume|bank|balanc|conserv|cross-section|representative", text, re.I))
    # ask A stops
    a = F.ask_a(target)
    raw = F.ask_a(target, as_s="raw")
    rst = F.ask_a(target, meter="restart")
    first = F.ask_a(target, resub="first")
    mv = sum(round(a[k], -1) != round(raw[k], -1) for k in a)
    ok("ask A the laboratory's as-S reporting left as it stands misses at least fifteen figures", mv >= 15, mv)
    ok("ask A the restarted totaliser read without the inspection's final reading misses Silwane's Q2",
       round(a[("SAM-DP1", "Q2")], -1) != round(rst[("SAM-DP1", "Q2")], -1))
    ok("ask A the first of a resubmitted month misses Ntsheketshe DP2's Q2",
       round(a[("NCH-DP2", "Q2")], -1) != round(first[("NCH-DP2", "Q2")], -1))
    ok("bins: every ask A figure at least 2 t from its ten-tonne rounding edge", min(
        5 - abs(v - round(v, -1)) for v in a.values()) >= 2.0, round(min(5 - abs(v - round(v, -1)) for v in a.values()), 2))
    a3 = {}
    for k, v in a.items():
        a3[k] = v
    ok("SF6 the S-to-SO4 factor 3.0 for 2.996 leaves every ask A figure in its bin", all(
        round(v * 1.0013, -1) == round(v, -1) for v in a.values()))
    ok("bins: every unit's whole-tonne load at least 0.15 t from its rounding edge",
       min(0.5 - abs(g[c] - round(g[c])) for c in g) >= 0.15, {c: round(g[c], 2) for c in g})
    # ask B stops
    b = F.ask_b(target)
    nod = F.ask_b(target, drift="none")
    nom = F.ask_b(target, memory=False)
    utc = F.ask_b(target, clock="utc")
    ok("ask B the loggers' readings taken as they stand (no drift taken off) miss every figure by two hours or more",
       all(abs(b[k] - nod[k]) >= 2 for k in b), sum(abs(b[k] - nod[k]) >= 2 for k in b))
    ok("ask B the telemetry alone (no memory downloads) misses at least ten figures",
       sum(b[k] != nom[k] for k in b) >= 10, sum(b[k] != nom[k] for k in b))
    ok("ask B the UTC clock read as SAST moves at least one figure", sum(b[k] != utc[k] for k in b) >= 1)
    cr = F.ask_b(target, drift="none", memory=False)
    ok("ask B the cracker (SAST, no drift, no memory) keeps no figure", sum(b[k] == cr[k] for k in b) == 0)
    # separation: the asks' device rows are outside the call's rows
    ok("separation: no mine return, logger reading, service visit or memory download is read by the call",
       all(k not in ("returns", "ec", "service", "memory", "inspections") for k in ("lab", "gauges", "register")))
    # input gates
    names = sorted(os.listdir(target))
    fmts = {os.path.splitext(n)[1] for n in names}
    big = max(sum(1 for _ in open(os.path.join(target, n), encoding="utf-8")) for n in names if n.endswith(".csv"))
    ok("gates: 10 or more files in 3 or more formats, one file of 25,000 rows or more",
       len(names) >= 10 and len(fmts) >= 3 and big >= 25000, (len(names), fmts, big))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("gates: two or more distractors named in metadata.json, none in a file name",
       len(meta["distractors"]) >= 2 and not any("distract" in n for n in names))
    print("%d checks, %d failed" % (N[0], N[1]))
    return N[1]


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
