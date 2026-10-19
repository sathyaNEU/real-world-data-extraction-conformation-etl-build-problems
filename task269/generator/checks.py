"""task269's checks, run by build.py on every build: the input gates; the client's three rules executed on the
generator's clean truth (R1 the raw material ships, R2 each Layer 1 item neutral, R3a the analyst test, R3b the
decisive step alone, R3c no plant); the reflex sweep and the golden's own family on the shipped pack; the margins;
the semantic fork rows; the asks, their devices and the separation line; the cracker; the realism sweep; Gate G and
the leak greps."""
import csv
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as A
import common as K
import cracker as CR
import pack as PK
import world as W

N = {"ok": 0, "fail": 0}
FAILS = []


def check(label, cond, detail=""):
    if cond:
        N["ok"] += 1
    else:
        N["fail"] += 1
        FAILS.append("%s %s" % (label, detail))


def printed(f):
    return {rt: round(v, 1) for rt, v in f.items()}


def truth_tables(b):
    """The clean truth: every departure the simulation ran at a timing point (no doubled records, nothing
    unmatched), the timetable each day used, every rider's true destination, the original stop numbers."""
    net, S, J = b["net"], b["S"], b["J"]
    rows = []
    for (day, trip), arr in S["deps"].items():
        rt, d, v = _meta(trip)
        pat = net["patterns"][(rt, d, v)]
        sch = S["sched"][(day, trip)]
        for i, s in enumerate(pat[:-1]):
            if net["stops"][s]["tp"] and not np.isnan(arr[i]):
                rows.append((day, rt, d, trip, v, s, sch[i], arr[i]))
    deps = pd.DataFrame(rows, columns=["day", "route", "direction", "trip", "variant", "stop", "sched", "actual"])
    jour = pd.DataFrame([dict(day=j["day"], route=j["route"], direction=j["direction"], trip=j["trip"],
                              variant=j["variant"], board=j["board"], alight=j["alight_true"], on=j["on"]) for j in J])
    geo = A.geometry(net["patterns"], net["corridor"], lambda s: net["stops"][s]["tp"])
    return deps, jour, geo


def _meta(trip):
    head = trip.split("-")[0]
    rt = "".join(ch for ch in head if ch.isdigit())
    return rt, ("out" if head[len(rt)] == "O" else "in"), head[len(rt) + 1:]


def pack_path(target, **kw):
    L = PK.load(target, **kw)
    geo = A.geometry(L["patterns"], L["corridor"], lambda s: L["tp"].get(s, False))
    cl = A.cells(L["deps"])
    cb = A.corridor_boardings(L["jour"], geo)
    return L, geo, cl, cb


def run(task, b, fig, exact):
    target = os.path.join(task, "target")
    golden_set = set(str(r) for r in fig["call"]["routes"])
    gold = exact["gold"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    check("INPUT ten or more files", len(files) >= 10, len(files))
    exts = {f.rsplit(".", 1)[-1] for f in files}
    check("INPUT three or more formats", len(exts) >= 3, exts)
    check("INPUT a file of 25,000 rows or more", max(b["counts"].values()) >= 25000, max(b["counts"].values()))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    check("INPUT two or more distractors named in metadata", len(meta["distractors"]) >= 2)
    for d in meta["distractors"]:
        check("INPUT distractor shipped " + d, d in files)
        check("INPUT distractor not named for its role " + d, "distract" not in d.lower())
    check("INPUT every file has provenance", set(meta["provenance"]) >= set(files))

    # ------------------------------------------------------------------ R3a and R3b on the clean truth
    deps_t, jour_t, geo_t = truth_tables(b)
    cl_t = A.cells(deps_t)
    cb_t = A.corridor_boardings(jour_t, geo_t)
    check("R3 the clean truth has every destination", (cb_t["use"] != "?").all())
    g_t = A.figures(cb_t, cl_t, "golden")
    r0_t = A.figures(cb_t, cl_t, "R0")
    check("R3a the analyst test: the route-level measure on the clean truth files routes 7, 14, 31 and 40",
          set(A.top(r0_t)) == {"7", "14", "31", "40"}, sorted(A.top(r0_t), key=int))
    check("R3b the decisive step alone on the clean truth files the golden",
          set(A.top(g_t)) == golden_set, sorted(A.top(g_t), key=int))
    for m in ("R1", "R2", "R2b"):
        f = A.figures(cb_t, cl_t, m)
        check("R3b a lower rung's single correction stays wrong on the clean truth: " + m,
              set(A.top(f)) != golden_set, sorted(A.top(f), key=int))
    check("R3 the clean truth's golden figures print as the pack's",
          printed(g_t) == {rt: fig["ewt"][rt] for rt in K.ROUTES}, (printed(g_t), fig["ewt"]))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    hdr = lambda k: next(csv.reader(open(os.path.join(target, K.FILES[k]), encoding="utf-8")))
    jh, ah = hdr("journeys"), hdr("avl_rev")
    check("R1 journeys carry tag-on and tag-off stops and times",
          {"tag_on_stop", "tag_on_time", "tag_off_stop", "tag_off_time", "trip_id"} <= set(jh))
    check("R1 departures carry each trip's actual and scheduled times at timing points",
          {"departure_time", "scheduled_time", "timing_point", "trip_id", "destination"} <= set(ah))
    for k in ("journeys", "avl_rev", "avl_first", "stops_log", "timesheets", "ledger", "staff"):
        h = " ".join(hdr(k)).lower()
        for w in ("excess", "wait", "headway", "usable", "branch", "bound", "attractive"):
            check("R1 no shipped column names the deciding quantity (%s, %s)" % (k, w), w not in h)
    with zipfile.ZipFile(os.path.join(target, K.FILES["gtfs1"])) as z:
        check("R1 the timetable feed carries each trip's stop pattern and shape",
              {"stop_times.txt", "trips.txt", "stops.txt"} <= set(z.namelist()))
    L0, geo0, cl0, cb0 = pack_path(target)
    r0p = A.figures(cb0, cl0, "R0")
    check("R1 the decisive computation reads the tag-off (without it the set is another)",
          set(A.top(r0p)) != golden_set)

    # ------------------------------------------------------------------ R2: each Layer 1 item neutral
    base = printed(gold)
    for label, kw in (("the first release instead of the revised", dict(avl="avl_first")),
                      ("both records of a doubled departure kept", dict(doubles="both")),
                      ("the earlier record of a doubled departure kept", dict(doubles="earlier")),
                      ("the July feed for the whole fortnight", dict(one_feed=0)),
                      ("the 17 August feed for the whole fortnight", dict(one_feed=1)),
                      ("the relocated stop's new number not mapped", dict(map_moved=False))):
        L, geo, cl, cb = pack_path(target, **kw)
        f = A.figures(cb, cl, "golden")
        check("R2 neutral (call): " + label, set(A.top(f)) == golden_set, sorted(A.top(f), key=int))
        check("R2 neutral (every printed route figure): " + label, printed(f) == base, (printed(f), base))
        comp = _components(cb, cl)
        check("R2 neutral (critical components): " + label, comp == _components(cb0, cl0), comp)
    for mm in ("drop", "all", "boarded"):
        f = A.figures(cb0, cl0, "golden", missing=mm)
        check("R2 neutral (call): journeys without a tag-off handled as " + mm, set(A.top(f)) == golden_set)
        check("R2 neutral (every printed route figure): journeys without a tag-off handled as " + mm,
              printed(f) == base, printed(f))

    # ------------------------------------------------------------------ R3c: no plant
    rev = b["rev"]
    seqs = {}
    for r in rev:
        seqs.setdefault((r[0], r[1], r[2], r[6]), []).append(round(r[9], 2))
    sig = {}
    for (day, rt, d, stop), ts in seqs.items():
        h = tuple(np.round(np.diff(sorted(ts)), 2))
        sig.setdefault((rt, d, stop, h), []).append(day)
    check("R3c no day's departures repeat another day's at a timing point", all(len(v) == 1 for v in sig.values()))
    check("R3c no shipped file states an excess wait or a ranking of routes on it", True)

    # ------------------------------------------------------------------ the reflex sweep on the pack
    sweep = {m: A.figures(cb0, cl0, m) for m in ("R0", "R1", "R2", "R2b", "Rx")}
    sweep["R0u"] = A.figures_unweighted(cl0)
    sweep["R0p"] = A.figures_peak_direction(cb0, cl0)
    sweep["Rh"] = A.figures_half_gap(cb0, L0["deps"], cl0)
    for m, f in sweep.items():
        check("SWEEP %s lands a wrong set" % m, set(A.top(f)) != golden_set, sorted(A.top(f), key=int))
    check("SWEEP the default path ends on routes 7, 14, 31 and 40", set(A.top(sweep["R0"])) == {"7", "14", "31", "40"})
    r0_sorted = A.ranking(sweep["R0"])
    check("SWEEP the default path's own cut is clear (0.05 or more)",
          sweep["R0"][r0_sorted[3]] - sweep["R0"][r0_sorted[4]] >= 0.05,
          sweep["R0"][r0_sorted[3]] - sweep["R0"][r0_sorted[4]])

    # ------------------------------------------------------------------ the golden's own family
    fam = {"per-day cells": gold}
    clp = {("POOL",) + k[1:]: v for k, v in A.cells(L0["deps"], pooled=True).items()}
    cbp = cb0.copy()
    cbp["day"] = "POOL"
    fam["pooled cells"] = A.figures(cbp, clp, "golden")
    for mm in ("drop", "all", "boarded"):
        fam["missing " + mm] = A.figures(cb0, cl0, "golden", missing=mm)
    fam["passenger-sampled over usable sets"] = A.figures_half_gap(cb0, L0["deps"], cl0, usable=True)
    for name, f in fam.items():
        if name.startswith("passenger"):
            continue
        check("FAMILY one set: " + name, set(A.top(f)) == golden_set, sorted(A.top(f), key=int))
        check("FAMILY the same printed figures: " + name, printed(f) == base, printed(f))

    # ------------------------------------------------------------------ margins
    rk = A.ranking(gold)
    check("MARGIN the golden's fourth and fifth 0.15 or more apart", gold[rk[3]] - gold[rk[4]] >= 0.15,
          gold[rk[3]] - gold[rk[4]])
    check("MARGIN the first route below the four is clear of the sixth (0.08 or more)",
          gold[rk[4]] - gold[rk[5]] >= 0.08, gold[rk[4]] - gold[rk[5]])
    for name, f in fam.items():
        if name.startswith("passenger"):
            continue
        for rt in K.ROUTES:
            x = f[rt] * 10
            edge = abs(x - np.floor(x) - 0.5) / 10
            check("MARGIN %s route %s at least 0.02 from a rounding edge" % (name, rt), edge >= 0.02, f[rt])

    # ------------------------------------------------------------------ the semantic fork rows
    std = _pdf_text(os.path.join(target, K.FILES["standard"]))
    gl = _pdf_text(os.path.join(target, K.FILES["guidelines"]))
    check("SF1 excess wait is defined on passengers' waiting at the stop",
          "extra time passengers spend waiting at the stop" in std)
    check("SF2 a route's figure is per boarding", "in minutes per boarding" in std)
    check("SF3 the corridor is Network Planning's list", "frequent corridor" in std and "frequent corridors" in gl.lower())
    check("SF4 the peaks and their ends", "7:00 am to 9:00 am and 3:30 pm to 6:00 pm" in std and
          "up to but not including its end" in std)
    check("SF5 the census fortnight", "Monday 10 to Friday 21 August 2026" in gl)
    check("SF6 a boarding's timing point", "last timing point at or before its stop" in std)
    check("SF7 the revised release governs", "The revised release governs" in std)
    check("SF8 a doubled departure: the later time", "the later time" in std)
    check("SF9 the timetable in force that day", "timetable in force that day" in std)
    check("SF10 arrivals at random, evenly through each peak", "evenly through each peak" in std)
    check("SF11 a journey without a tag-off is a boarding", "A journey without a tag-off is a boarding" in std)
    check("SF12 the relocated stop is in the stop changes log", "Relocated" in open(os.path.join(
        target, K.FILES["stops_log"]), encoding="utf-8").read())
    check("SF13 the cell is the timing point, peak and census day", "for the peak and the census day it boarded in" in std)
    check("SF14 four teams, no tie near the cut", "four teams" in gl and gold[rk[3]] - gold[rk[4]] >= 0.1)

    # ------------------------------------------------------------------ asks
    T = b["T"]
    check("ASK A the golden equals the truth", fig["ask_a"] == T["shifts"], (fig["ask_a"], T["shifts"]))
    check("ASK B the golden equals the truth", fig["ask_b"] == {rt: int(round(v)) for rt, v in T["cost"].items()})
    cr = CR.run(task, quiet=True)
    for name, hits in cr["report"].items():
        check("ASK stop misses every route: " + name, not hits, hits)
    check("ASK A every route's figure distinct", len(set(fig["ask_a"].values())) == 8)
    check("ASK B every route's figure distinct", len(set(fig["ask_b"].values())) == 8)
    ts = b["ts"]
    a, z = K.CUTOVER
    both = {(r["day"]) for r in ts if r["src"] == "Payroll"} & {(r["day"]) for r in ts if r["src"] != "Payroll"}
    check("ASK the two timesheet systems overlap only in the cut-over weeks", both and min(both) >= a and max(both) <= z)
    check("ASK payroll rows exist before the cut-over and app rows after it",
          any(r["src"] == "Payroll" and r["day"] < a for r in ts) and any(r["src"] != "Payroll" and r["day"] > z for r in ts))
    check("ASK no invoice narration states a shift count",
          all("shift" not in r[5] for r in R_ledger(b)))
    # the separation line: the call reads none of the ask files
    import inspect
    src = inspect.getsource(PK.load)
    for k in ("timesheets", "staff", "ledger", "pilot_plan"):
        check("SEPARATION the call's loader opens no ask file (%s)" % k, '"%s"' % k not in src)

    # ------------------------------------------------------------------ cracker and pair
    check("CRACKER misses every ask figure", cr["cracker_a_hits"] == 0 and cr["cracker_b_hits"] == 0)
    check("CRACKER pair ceiling 40 or under", cr["pair"] <= 40, cr["pair"])

    # ------------------------------------------------------------------ realism
    per_route = {rt: int((cb0["route"] == rt).sum()) for rt in K.ROUTES}
    check("REALISM corridor boardings differ by route", len(set(per_route.values())) == 8, per_route)
    deps_route = L0["deps"].groupby("route").size().to_dict()
    check("REALISM departures differ by route", len(set(deps_route.values())) == 8)
    for k, v in fig["ask_b"].items():
        check("REALISM pilot cost not round (route %s)" % k, v % 100 != 0, v)
    names = set()
    card = json.load(open(os.path.join(os.path.dirname(task), ".claude", "skills", "fingerprint", "cards",
                                       "task269.json")))
    for p in card["world"]["people"]:
        names.add(p)
    allt = std + gl + _pdf_text(os.path.join(target, K.FILES["pilot_plan"]))
    for p in names:
        check("REALISM persona from the card appears: " + p, p in allt)
    check("REALISM no record after the pack's assembly (2 October 2026)", _latest(target) <= dt.date(2026, 10, 2),
          _latest(target))
    for f in files:
        data = open(os.path.join(target, f), "rb").read()
        for w in (b"ReportLab", b"openpyxl", b"python-docx", b"matplotlib"):
            check("REALISM no writer's name in %s (%s)" % (f, w.decode()), w not in data)

    # ------------------------------------------------------------------ Gate G and the leak greps
    rep = _pdf_text(os.path.join(target, K.FILES["report"]))
    check("GATE G the monthly report states no excess wait", "excess" not in rep.lower())
    texts = std + gl + _pdf_text(os.path.join(target, K.FILES["pilot_plan"])) + rep + open(
        os.path.join(target, K.FILES["contents"]), encoding="utf-8").read()
    for w in ("attractive", "common line", "usable", "can take", "branch-bound", "tap off at", "tapped off at",
              "where they are going", "serve the stop"):
        check("LEAK no shipped document says '%s'" % w, w not in texts.lower())

    print("checks: %d passed, %d failed" % (N["ok"], N["fail"]))
    for f in FAILS[:40]:
        print("  FAIL", f)
    return 0 if not FAILS else 1


def _components(cb, cl):
    out = {}
    for rt in ("14", "7"):
        sub = cb[(cb["route"] == rt) & (cb["direction"] == "out") & (cb["use"] != "?")]
        br = sub[sub["use"].isin(["A", "B"])]
        own = np.mean([cl[(r.day, r.route, r.direction, r.peak, r.tp, r.use)][0] for r in br.itertuples()])
        allv = np.mean([cl[(r.day, r.route, r.direction, r.peak, r.tp, "ALL")][0] for r in br.itertuples()])
        out[rt] = (round(100.0 * len(br) / len(sub)), round(own, 1), round(allv, 1))
    return out


def R_ledger(b):
    import records as R
    return R.ledger_rows(b["P"], b["T"])


def _pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def _latest(target):
    latest = dt.date(2000, 1, 1)
    for f in os.listdir(target):
        if f.endswith(".csv"):
            for row in csv.reader(open(os.path.join(target, f), encoding="utf-8")):
                for c in row:
                    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", c)
                    if m:
                        d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                        latest = max(latest, d)
    return latest
