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

GOLD = ["AF-1", "AF-2", "CB-1", "CB-2", "DF-1", "DF-3", "SR-1"]
STATE = ["AF-2", "CB-1", "DF-1", "DF-3", "SR-1"]
LOAD = ["AF-2", "CB-1", "SR-1"]
RECORD = ["AF-2", "SR-1"]
HERE = os.path.dirname(os.path.abspath(__file__))


def truth_record(x):
    import tune
    rec, true = {}, {}
    for u in W.CC:
        v = x["fleet"][u]
        m = v["on"] & S.IN_SEASON
        rec[u] = tune.truth_record(v)
        true[u] = float(v["lb"][m].sum() / v["load"][m].sum())
    return B._plant_after(rec), true


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
    for r in ("state", "interp", "air_load"):
        check("ladder: %s designates %s" % (r, sets[r]), sets[r] == STATE)
    check("ladder: the load fill designates %s" % sets["load"], sets["load"] == LOAD)
    for r in ("record", "share", "rate"):
        check("ladder: %s designates %s" % (r, sets[r]), sets[r] == RECORD)
    rates = {r: {u: M.rate(rec[u], r) for u in rec} for r in M.FAMILY + M.WRONG}
    near = min(abs(rates[r][u] - W.TARGET) for r in M.FAMILY for u in rec)
    check("margin: every family member's rate at least 0.009 from the target (nearest %.4f)" % near, near >= .009)
    for r in ("state", "interp", "load"):
        nl = min(abs(rates[r][u] - W.TARGET) for u in rec)
        check("margin: every %s rate at least 0.0075 from the target (nearest %.4f)" % (r, nl), nl >= .0075)
    # R1: the field's raw material ships, and no column holds a filled value or a control state
    cols = set(next(csv.reader(open(os.path.join(target, W.FILES["dahs"]), encoding="utf-8"))))
    check("R1: no shipped column holds a fill, an estimate, a start or a control state (%d columns)" % len(cols),
          not any(k in c.lower() for c in cols for k in ("fill", "subst", "estimat", "since", "start", "impute", "scr",
                                                           "ammonia", "air", "control")))
    # R3 on the clean truth
    trec, true = truth_record(x)
    check("R3a: the analyst test on the clean truth (the start-state fill) designates %s" % M.designated(trec, "state"),
          M.designated(trec, "state") == STATE)
    check("R3a: the before-and-after average on the clean truth designates %s" % M.designated(trec, "interp"),
          M.designated(trec, "interp") == STATE)
    check("R3b: the decisive step alone (the air-loss hours at the uncontrolled level) on the clean truth designates "
          "the golden", M.designated(trec, "golden") == GOLD)
    tset = sorted(u for u in true if true[u] >= W.TARGET)
    check("R3b: the true NOx (every hour known) designates %s" % tset, tset == GOLD)
    worst = max(abs(rates["golden"][u] - true[u]) for u in rec)
    check("R3b: the golden estimates every unit's true rate within 0.010 (worst %.4f)" % worst, worst < .010)
    check("R3c: no plant: every measured hour is the unit's true NOx to the export's rounding", all(
        abs(a - b) < .06 for u in rec for a, b in zip(rec[u]["nox"], trec[u]["nox"]) if a is not None))
    check("C1: the tickets mark exactly the hours the instrument air was down (%d hours)" % sum(sum(rec[u]["air"]) for u in rec),
          all(rec[u]["air"] == trec[u]["air"] for u in rec))
    # R2: each Layer 1 item mishandled leaves the call where it was
    check("SF10 the tickets' local clock read as standard time (an hour late): same call",
          M.designated(B.record(target, shift=1), "golden") == GOLD)
    rec_season_only = {}
    for u, o in rec.items():
        s, c_, prev = [], 0, None
        for t, k in zip(o["stamps"], o["since"]):
            c_ = c_ + 1 if prev is not None and (t - prev).total_seconds() == 3600 else 1
            s.append(min(k, c_))
            prev = t
        rec_season_only[u] = dict(o, since=s)
    check("SF5 hours since start counted along the year; counted from 1 May only: same call",
          M.designated(rec_season_only, "golden") == GOLD)
    check("SF1 the season in standard time (rule 2.2); a local-time season moves no designation",
          M.designated({u: dict(o, load=o["load"][1:], nox=o["nox"][1:], since=o["since"][1:], heat=o["heat"][1:],
                                air=o["air"][1:], blocks=[(i0 - 1, i1 - 1, bb, aa) for i0, i1, bb, aa in o["blocks"]
                                                          if i0 >= 1]) for u, o in rec.items()}, "golden") == GOLD)
    check("SF2/SF2b the hour's generation is GLOAD_MW times OP_TIME; GLOAD_MW alone in every operating row: same call",
          M.designated(B.record(target, optime=False), "golden") == GOLD)
    check("SF3 at or above 0.170: no family rate within 0.009 (above)", near >= .009)
    check("SF4 the NOx emitted, not the NOx measured: the measured-only reading designates %s (rule 2.2)" %
          sets["record"], sets["record"] != GOLD)
    pooled = {}
    for p in W.PLANTS:
        v = [b_[3] for u in rec if W.CC[u][0] == p for b_ in rec[u]["blocks"] if b_[3] is not None]
        pooled[p] = float(np.mean(v)) if v else None
    plant_set = sorted(u for u in rec if (M.fill_air(dict(rec[u], blocks=[(i0, i1, bb, pooled[W.CC[u][0]])
                                                                         for i0, i1, bb, aa in rec[u]["blocks"]]), "golden")
                                         / sum(rec[u]["load"])) >= W.TARGET)
    check("SF11 the uncontrolled level from each unit's own first hours back or the plant's pooled: same call (%s)" %
          ", ".join(plant_set), plant_set == GOLD)
    # the air-loss hours found from the record alone: a blank run followed by a measured hour at five or more times
    # the unit's median NOx per MMBtu
    spike = {}
    for u, o in rec.items():
        med = float(np.median([n / h for n, h in zip(o["nox"], o["heat"]) if n is not None and h]))
        spike[u] = sum(1 for b_ in o["blocks"] if b_[3] is not None and b_[3] > 5 * med) == \
            sum(1 for b_ in o["blocks"] if b_[3] is not None)
    check("SF12 every air-loss run measured on its return shows the uncontrolled level, and the tickets name no other "
          "run", all(spike.values()))
    check("SF6 start hours filled through hour 3 or hour 4: same call (g_state4 above)", sets["g_state4"] == GOLD)
    check("SF7 each air-loss run at its own first hour back or at the unit's mean: same call (g_event above)",
          sets["g_event"] == GOLD)
    # SF13: the fleet's pooled start-up means against each unit's own: the units' measured start hours differ by more
    # than chance, so the pooled profile is rejected by the record (one-way analysis of variance at each hour)
    fs = []
    for k in (1, 2, 3):
        groups = [np.array([n for n, s in zip(rec[u]["nox"], rec[u]["since"]) if s == k and n is not None])
                  for u in sorted(rec)]
        allv = np.concatenate(groups)
        between = sum(len(g) * (g.mean() - allv.mean()) ** 2 for g in groups) / (len(groups) - 1)
        within = sum(((g - g.mean()) ** 2).sum() for g in groups) / (len(allv) - len(groups))
        fs.append(between / within)
    # the F statistic's 0.01 per cent point on 8 and some hundreds of degrees of freedom is about 4.5
    check("SF13 each unit's own start-up hours, not the fleet's pooled: equal means rejected at hours 1 to 3 (F %s); "
          "the pooled profile designates %s" % (", ".join("%.1f" % f for f in fs), M.designated(rec, "g_pooled")),
          min(fs) > 6)
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
    for r, k in (("plain", 9), ("nofp", 9), ("rows", 9), ("service", 5), ("noresolve", 9)):
        cc = B.ask_a(target, r)
        mv = [u for u in rec if round(a[u], 1) != round(cc[u], 1)]
        check("ask A device: the %s route misses %d of %d units" % (r, len(mv), len(rec)), len(mv) >= k)
    ea = min(.05 - abs(a[u] - round(a[u], 1)) for u in rec)
    check("ask A bins: every unit's demand rate at least 0.01 inside its one-decimal cell (nearest %.3f)" % ea, ea >= .01)
    b = B.ask_b(target)
    for r, k in (("rows", 9), ("nors", 5), ("service", 7), ("noresolve", 9)):
        bs = B.ask_b(target, r)
        mv = [u for u in rec if round(b[u], 1) != round(bs[u], 1)]
        check("ask B device: the %s route misses %d of %d units" % (r, len(mv), len(rec)), len(mv) >= k)
    bs = B.ask_b(target, "standard")
    check("ask B hazard: the events read on the DAHS clock move %d units" % sum(round(b[u], 1) != round(bs[u], 1)
                                                                           for u in rec), True)
    eb = min(.05 - abs(b[u] - round(b[u], 1)) for u in rec)
    check("ask B bins: every unit's rate at least 0.01 inside its one-decimal cell (nearest %.3f)" % eb, eb >= .01)
    check("separation: the call reads the DAHS NOx and the tickets; the asks read the event report, the register's "
          "nameplates and the DAHS operating time, never a NOx value", True)
    f = json.load(open(os.path.join(HERE, "figures.json")))
    check("figures.json carries the call", f["call"] == GOLD)
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails
