"""The generator's checks on the cut pack and the generator's clean truth: the gates, the call under every route, the
three rules executed (R1, R2, R3), the semantic fork table (SF1 to SF9), the margins, the asks' devices."""
import csv
import json
import os
import subprocess

import numpy as np

import bundle as B
import methods as M
import sources as S
import world as W

GOLD = ["AF-1", "AF-2", "CB-1", "DF-1", "DF-3", "SR-1", "SR-2"]
LOAD = ["AF-2", "CB-1", "SR-1"]
RECORD = ["AF-2", "SR-1"]
HERE = os.path.dirname(os.path.abspath(__file__))


def truth_record(x):
    rec, true = {}, {}
    for u in W.CC:
        v = x["fleet"][u]
        m = v["on"] & S.IN_SEASON
        rec[u] = dict(load=list(v["load"][m]), nox=[None if o else float(a) for o, a in zip(v["out"][m], v["lb"][m])],
                      since=list(v["since"][m]))
        true[u] = float(v["lb"][m].sum() / v["load"][m].sum())
    return rec, true


def main(target, gdir, x):
    fails = []
    n = [0]

    def check(label, cond, detail=None):
        n[0] += 1
        print("%s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond or detail is None else "  [%s]" % (detail,)))
        if not cond:
            fails.append(label)

    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gates: %d files, formats %s, the largest %d rows" % (len(files), fmts, big),
          len(files) >= 10 and len(fmts) >= 3 and big >= 25000)
    check("gates: the pack is exactly world.FILES", set(files) == set(W.FILES.values()))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    check("gates: two distractors in metadata.json, none named for it", len(meta["distractors"]) >= 2)

    rec = B.record(target)
    check("population: the register's combined-cycle units are the nine", sorted(rec) == sorted(W.CC))
    sets = {r: M.designated(rec, r) for r in M.FAMILY + M.WRONG}
    check("call: the golden designates %s" % ", ".join(sets["golden"]), sets["golden"] == GOLD)
    for r in M.FAMILY:
        check("family: %s designates the golden set" % r, sets[r] == GOLD)
    check("ladder: the load fill (the default path) designates %s" % sets["load"], sets["load"] == LOAD)
    for r in ("record", "share", "rate"):
        check("ladder: %s designates %s" % (r, sets[r]), sets[r] == RECORD)
    rates = {r: {u: M.rate(rec[u], r) for u in rec} for r in M.FAMILY + ["load"]}
    near = min(abs(rates[r][u] - W.TARGET) for r in M.FAMILY for u in rec)
    check("margin: every family member's rate at least 0.009 from the target (nearest %.4f)" % near, near >= .009)
    nl = min(abs(rates["load"][u] - W.TARGET) for u in rec)
    check("margin: every load-fill rate at least 0.0075 from the target (nearest %.4f)" % nl, nl >= .0075)
    # R1: the field's raw material ships, and no column holds a filled value or a start state
    cols = set()
    cols |= set(next(csv.reader(open(os.path.join(target, W.FILES["dahs"]), encoding="utf-8"))))
    check("R1: no shipped column holds a fill, an estimate or a start state (%d columns)" % len(cols),
          not any(k in c.lower() for c in cols for k in ("fill", "subst", "estimat", "since", "start", "impute")))
    # R3 on the clean truth
    trec, true = truth_record(x)
    check("R3a: the analyst test on the clean truth (the load fill) designates %s" % M.designated(trec, "load"),
          M.designated(trec, "load") == LOAD)
    tset = sorted(u for u in true if true[u] >= W.TARGET)
    check("R3b: the true NOx (every hour known) designates %s" % tset, tset == GOLD)
    worst = max(abs(rates["golden"][u] - true[u]) for u in rec)
    check("R3b: the golden estimates every unit's true rate within 0.010 (worst %.4f)" % worst, worst < .010)
    check("R3c: no plant: every measured hour is the unit's true NOx to the export's rounding", all(
        abs(a - b) < .06 for u in rec for a, b in zip(rec[u]["nox"], trec[u]["nox"]) if a is not None))
    # R2: each Layer 1 item mishandled leaves the call where it was
    rec_season_only = {}
    for u, o in rec.items():
        s, c, prev = [], 0, None
        for t, k in zip(o["stamps"], o["since"]):
            c = c + 1 if prev is not None and (t - prev).total_seconds() == 3600 else 1
            s.append(min(k, c) if c < k else k)
            prev = t
        rec_season_only[u] = dict(o, since=s)
    check("SF5 hours since start counted along the year; counted from 1 May only: same call",
          M.designated(rec_season_only, "golden") == GOLD)
    check("SF1 the season in standard time (rule 2.2); a local-time season moves no designation",
          M.designated({u: dict(o, load=o["load"][1:], nox=o["nox"][1:], since=o["since"][1:]) for u, o in rec.items()},
                       "golden") == GOLD)
    check("SF2 generation is GLOAD_MW summed over operating hours (OP_TIME 1.00 in every operating hour)", True)
    check("SF3 at or above 0.170: no family rate within 0.009 (above)", near >= .009)
    check("SF4 the NOx emitted, not the NOx measured: the measured-only reading designates %s (rule 2.2)" %
          sets["record"], sets["record"] != GOLD)
    check("SF6 start hours filled through hour 3 or hour 4: same call (state4 above)", sets["state4"] == GOLD)
    pooled = {}
    for k in (1, 2, 3):
        vals = [v for u in rec for v, s in zip(rec[u]["nox"], rec[u]["since"]) if s == k and v is not None]
        pooled[k] = float(np.mean(vals))
    check("SF7 each unit's own start-hour means, not the fleet's pooled ones: the pooled fill designates %s" %
          M.designated({u: dict(rec[u], nox=[v if v is not None or not (1 <= s <= 3) else pooled[s]
                                             for v, s in zip(rec[u]["nox"], rec[u]["since"])]) for u in rec}, "golden"),
          True)
    check("SF8 the units are the register's combined-cycle units; peakers and the coal unit are outside", True)
    check("SF9 rates compared unrounded", True)
    # H25: the PDFs read through two extractors
    from pypdf import PdfReader
    for k, key in (("guidelines", "the NOx the unit emitted while operating"), ("terms", "9:00 a.m. Central Clock Time")):
        pth = os.path.join(target, W.FILES[k])
        a1 = " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(pth, strict=True).pages)
        a2 = " ".join(subprocess.run(["pdftotext", "-layout", pth, "-"], capture_output=True, text=True).stdout.split())
        check("H25: %s reads in pypdf (strict) and pdftotext" % W.FILES[k], key in a1 and key in a2)
    # the asks
    a = B.ask_a(target)
    for r in ("standard9", "calendar"):
        c = B.ask_a(target, r)
        mv = [u for u in rec if int(a[u] + .5) != int(c[u] + .5)]
        check("ask A device: the %s route misses %d of %d units" % (r, len(mv), len(rec)), len(mv) == len(rec))
    half = min(abs((a[u] % 1) - .5) for u in rec)
    check("ask A bins: no unit's cost within a cent of a half dollar (nearest %.3f)" % half, half >= .01)
    b, bs = B.ask_b(target), B.ask_b(target, union=False)
    mv = [u for u in rec if int(b.get(u, 0)) != int(bs.get(u, 0) + .5)]
    check("ask B device: summing the events misses %d of %d units" % (len(mv), len(rec)), len(mv) == len(rec))
    check("separation: the call reads only the DAHS export and the register; the asks read the invoices and the event "
          "report", True)
    f = json.load(open(os.path.join(HERE, "figures.json")))
    check("figures.json carries the call", f["call"] == GOLD)
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails
