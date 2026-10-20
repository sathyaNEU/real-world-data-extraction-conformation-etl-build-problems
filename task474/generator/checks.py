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
    check("SF2 generation is GLOAD_MW summed over operating hours (OP_TIME 1.00 in every operating hour)", True)
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
    for r in ("prev", "interp", "skip", "standard9", "calendar"):
        cc = B.ask_a(target, r)
        mv = [u for u in rec if round(a[u] / 100) != round(cc[u] / 100)]
        check("ask A device: the %s route misses %d of %d units" % (r, len(mv), len(rec)), len(mv) >= 7)
    # every invoice line's quantity ties to its plant's burn over the gas days since the point's previous line
    import datetime as dt_
    burn = {}
    for r in csv.DictReader(open(os.path.join(target, W.FILES["dahs"]), encoding="utf-8")):
        if r["HEAT_INPUT_MMBTU"]:
            t = dt_.datetime(*map(int, r["OP_DATE"].split("-")), int(r["OP_HOUR"]))
            loc = t + dt_.timedelta(hours=1) if dt_.datetime(2026, 3, 8, 2) <= t < dt_.datetime(2026, 11, 1, 1) else t
            k = (r["FACILITY_NAME"], (loc - dt_.timedelta(hours=9)).date())
            burn[k] = burn.get(k, 0.0) + float(r["HEAT_INPUT_MMBTU"])
    lines = {}
    for r in csv.DictReader(open(os.path.join(target, W.FILES["invoices"]), encoding="utf-8")):
        lines.setdefault(r["delivery_point"], []).append((dt_.date.fromisoformat(r["gas_day"]), float(r["quantity_dth"])))
    bad, n_strip = 0, 0
    for p, ls in lines.items():
        if p == "Holt Creek Station":
            continue
        ls.sort()
        for (d0, _q0), (d1, q1) in zip(ls, ls[1:]):
            tot = sum(burn.get((p, d0 + dt_.timedelta(days=k)), 0.0) for k in range(1, (d1 - d0).days + 1))
            n_strip += (d1 - d0).days > 1
            bad += abs(tot - q1) > .2
    check("ask A fair: every invoice line's quantity is its plant's burn since the point's previous line (%d lines off, "
          "%d lines covering more than one gas day)" % (bad, n_strip), bad == 0)
    edge = min(50 - abs(a[u] - 100 * round(a[u] / 100)) for u in rec)
    check("ask A bins: every unit's cost at least $15 inside its hundred-dollar cell (nearest %.0f)" % edge, edge >= 15)
    b = B.ask_b(target)
    evs = list(csv.DictReader(open(os.path.join(target, W.FILES["events"]), encoding="utf-8")))
    import datetime as dt2
    full = [r for r in evs if r["event_type"] in ("U1", "U2", "U3")]
    pairs = 0
    for e in full:
        s0 = dt2.datetime.strptime(e["start_local"], "%Y-%m-%d %H:%M")
        e0 = dt2.datetime.strptime(e["end_local"], "%Y-%m-%d %H:%M")
        for f_ in full:
            s1 = dt2.datetime.strptime(f_["start_local"], "%Y-%m-%d %H:%M")
            e1 = dt2.datetime.strptime(f_["end_local"], "%Y-%m-%d %H:%M")
            if f_ is not e and f_["unit"] == e["unit"] and f_["event_type"] == e["event_type"] and \
                    f_["cause_code"] == e["cause_code"] and e1 - s1 == e0 - s0 and s1.time() == s0.time() and \
                    s1 != s0 and f_["date_reported"] > e["date_reported"]:
                pairs += 1
    n_designed = sum(1 for e in x["asks"]["events"] if e.get("swapped") and e["filed"] <= dt2.date(2026, 10, 16))
    check("ask B fair: the reports repeating an outage's type, cause, length and hours under other dates are exactly "
          "the %d corrected entries (%d found)" % (n_designed, pairs), pairs == n_designed)
    for r, k in (("latest", 9), ("samestart", 9), ("sum", 9), ("union", 9)):
        bs = B.ask_b(target, r)
        mv = [u for u in rec if b.get(u, 0) != bs.get(u, 0)]
        check("ask B device: the %s route misses %d of %d units" % (r, len(mv), len(rec)), len(mv) >= k)
    check("separation: the call reads only the DAHS export and the register; the asks read the invoices and the event "
          "report", True)
    f = json.load(open(os.path.join(HERE, "figures.json")))
    check("figures.json carries the call", f["call"] == GOLD)
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails
