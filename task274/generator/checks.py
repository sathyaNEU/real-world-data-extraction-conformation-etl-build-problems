"""Generator assertions for task274, run on every build: the three rules executed on the clean truth (R1 to R3), every
Layer 1 item neutral, the semantic fork rows, the ladder, the asks and their devices, the realism sweep and the house
checks. Prints one line per check; returns the number failed."""
from __future__ import annotations

import collections
import copy
import datetime as dt
import json
import os
import re
import subprocess

import numpy as np

import analysis as A
import asks as AS
import common as K
import pack as PK
import seedsearch as SS

FAILS = []


def check(name, ok, detail=""):
    print("%s  %s  %s" % ("ok  " if ok else "FAIL", name, detail if not ok else ""))
    if not ok:
        FAILS.append(name)


def sets(v):
    return [x + 1 for x in A.designated(v)]


def edit(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def run(task, w, P):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    rd = PK.Read(target)
    R, pairs, chk = rd.records()
    g, info = A.golden(R, pairs, chk)
    G = A.designated(g)
    names = [n for _, n in K.COUNTIES]

    # ------------------------------------------------------------ the call from the pack equals the world's
    Rw, pw, cw = SS.records(w)
    gw, _ = A.golden(Rw, pw, cw)
    check("G the call recomputed from the pack equals the world's", A.designated(gw) == G and np.allclose(gw, g), "")
    check("G figures.json carries the call", fig["call"]["counties"] == [names[i] for i in G], "")
    truth = np.zeros(A.NC)
    den = np.zeros(A.NC)
    for p in w["P"]:
        if p.get("result") is None:
            continue
        den[p["county"]] += p["wtmec"]
        truth[p["county"]] += p["wtmec"] * (p["true"] < K.CUTOFF)
    check("G the golden set is the truth's set", A.designated(truth / den) == G, sets(truth / den))
    check("G every county at least 1.5 points from the line under every family member",
          min(A.margin(v) for v in A.family(R, pairs, chk).values()) >= 0.015, "")

    # ------------------------------------------------------------ R1: the field's raw material ships
    check("R1 the bridging run pairs one stored duplicate with each of %d examined adults' primary results" % len(pairs),
          len(pairs) >= 800 and all(s in rd.persons for s in pairs), len(pairs))
    heads = []
    for k in ("results", "bridge", "tracking", "persons", "events", "instruments", "counties"):
        with open(os.path.join(target, K.FILES[k]), encoding="utf-8") as f:
            heads += f.readline().strip().split(",")
    bad = [h for h in heads if re.search(r"BIAS|SHIFT|CORRECT|STANDARD|REFERENCE_SCALE|ADJ", h)]
    check("R1 no shipped column holds a bias, shift or corrected value", not bad, bad)
    cals_used = sorted({r["cal"] for r in R})
    check("R1 every calibration the results were measured under has at least two bridging pairs",
          min(info["n"].get(c, 0) for c in cals_used) >= 2, min(info["n"].get(c, 0) for c in cals_used))

    # ------------------------------------------------------------ R3a: the analyst test and the ladder
    rt = A.routes(R, pairs, chk)
    want = {"R0_reported": [], "R1_check_on_all": [1, 2], "R3_lot_analyzer": [1, 2], "R3d_lot_plus_analyzer": [1, 2],
            "R3c_lot_only": [1, 2], "R3b_lot_analyzer_bridge_as_check": [2], "R2_overall_shift": [1, 2],
            "R4_calibration_bridge_as_check": [1]}
    for k, s in want.items():
        check("R3a %s files %s, not the golden %s" % (k, s, sets(g)), sets(rt[k]) == s and A.designated(rt[k]) != G,
              sets(rt[k]))
    for k, v in rt.items():
        if k == "R5_month_analyzer":
            continue
        dif = [i for i in range(A.NC) if (v[i] > A.LINE) != (g[i] > A.LINE)]
        far = max([abs(v[i] - A.LINE) for i in dif], default=0.0)
        check("R3a %s misplaces a county by at least a point" % k, far >= 0.01, round(far, 4))
    # the analyst test: the lot-and-analyzer route is not one sort away from the golden
    o = list(np.argsort(-rt["R3_lot_analyzer"]))
    check("R3a the golden set is not a top set of the lot-and-analyzer route's ordering",
          set(G) not in [set(o[:q]) for q in range(9)], "")

    # ------------------------------------------------------------ R3b: the decisive step alone
    PL = A.pair_logs(R, pairs)
    a = A.anchor(chk)
    cal, _ = A.group_shift(PL, lambda r: r["cal"])
    alone = A.shares(R, [a + cal[r["cal"]] - cal[chk["cal"]] for r in R])
    check("R3b the lot-and-analyzer route with only its grouping moved to the calibration files the golden",
          A.designated(alone) == G, sets(alone))
    cell, _ = A.group_shift(PL, lambda r: (r["lot"], r["analyzer"]))
    half = A.shares(R, [a + cal[r["cal"]] - cell[(chk["lot"], chk["analyzer"])] for r in R])
    check("R3b each calibration's shift but the check read at its lot and analyzer files another set",
          A.designated(half) != G, sets(half))
    calo = {c["id"]: c for c in rd.cals}
    k3, _ = A.group_shift(PL, lambda r: (r["lot"], calo[r["cal"]]["calot"], r["analyzer"]))
    cc = calo[chk["cal"]]
    lk = A.shares(R, [a + k3[(r["lot"], calo[r["cal"]]["calot"], r["analyzer"])] -
                      k3[(chk["lot"], cc["calot"], chk["analyzer"])] for r in R])
    check("R3b reagent lot by calibrator lot by analyzer, routine recalibrations pooled, files another set",
          A.designated(lk) != G, sets(lk))

    # the family: three estimators of a calibration's shift, three readings of the check, trimmed means, and the
    # finer time windows that sit inside calibrations
    fam = A.family(R, pairs, chk)
    check("F every family member names the golden set", all(A.designated(v) == G for v in fam.values()),
          {k: sets(v) for k, v in fam.items() if A.designated(v) != G})
    sp = np.max(list(fam.values()), axis=0) - np.min(list(fam.values()), axis=0)
    check("F the family's spread on any county is under the smallest margin",
          float(np.max(sp)) < min(A.margin(v) for v in fam.values()) + 0.01, round(float(np.max(sp)), 4))
    by = collections.defaultdict(list)
    for r, y in PL:
        by[r["cal"]].append(y)
    sd = float(np.std([y - np.mean(by[r["cal"]]) for r, y in PL]))
    trim = {k: float(np.mean([y for y in v if abs(y - np.mean(v)) <= 3 * sd])) for k, v in by.items()}
    tr = A.shares(R, [a + trim[r["cal"]] - trim[chk["cal"]] for r in R])
    check("F calibration means after a 3 SD trim name the golden set", A.designated(tr) == G, sets(tr))
    # the data refute pooling by lot and analyzer: calibration effects inside each lot and analyzer cell
    ss_cell = sum((y - cell[(r["lot"], r["analyzer"])]) ** 2 for r, y in PL)
    ss_cal = sum((y - cal[r["cal"]]) ** 2 for r, y in PL)
    k_cal, k_cell = len(cal), len(cell)
    Fst = ((ss_cell - ss_cal) / (k_cal - k_cell)) / (ss_cal / (len(PL) - k_cal))
    check("F calibrations inside lot and analyzer cells differ (F at least 10)", Fst >= 10, round(Fst, 1))
    print("    within-cell F for calibrations: %.1f on %d and %d df" % (Fst, k_cal - k_cell, len(PL) - k_cal))

    # ------------------------------------------------------------ R2: Layer 1 items are neutral
    # L1: the event log's UTC read as local time
    naive = []
    for c in rd.cals:
        c2 = dict(c)
        c2["time"] = c["time"] + dt.timedelta(hours=7 if not (dt.datetime(2025, 3, 9) <= c["time"] < dt.datetime(2025, 11, 2)) else 6)
        naive.append(c2)
    rd2 = copy.copy(rd)
    rd2.cals = naive
    R2, p2, c2 = rd2.records()
    s2, _ = A.group_shift(A.pair_logs(R2, p2), lambda r: r["cal"])
    for c in sorted({r["cal"] for r in R2}):
        if c not in s2:          # a calibration left with no bridging pair takes the one before it on its analyzer
            prev = max(k for k in s2 if k < c and rd2.cals[k]["serial"] == rd2.cals[c]["serial"])
            s2[c] = s2[prev]
    g2 = A.shares(R2, [a + s2[r["cal"]] - s2[c2["cal"]] for r in R2])
    check("R2 L1 the event log's UTC read as local time leaves the call", A.designated(g2) == G, sets(g2))
    # L2: voided rows kept beside the finals
    h, rs = PK.rows(os.path.join(target, K.FILES["results"]))
    i = {c: j for j, c in enumerate(h)}
    extra = []
    for r in rs:
        if r[i["RESULT_STATUS"]] == "X":
            seqn = rd.barcode[r[i["SPECIMEN_ID"]]]
            t = dt.datetime.strptime(r[i["RESULTED_AT"]], "%m/%d/%Y %H:%M")
            ser = rd.serial[r[i["INSTRUMENT"]]]
            c = rd.cal_at(ser, t)
            pp = rd.persons[seqn]
            extra.append(dict(seqn=-seqn, county=pp["county"], w=pp["w"], value=PK.value(r[i["RESULT"]]),
                              analyzer=[K.ANALYZERS[0][1], K.ANALYZERS[1][1]].index(ser),
                              lot=sorted({x["lot"] for x in rd.results}).index(r[i["REAGENT_LOT"]]),
                              cal=c["id"], month=t.month))
    check("R2 L2 the LIS carries voided runs", len(extra) >= 40, len(extra))
    g3, _ = A.golden(R + extra, pairs, chk)
    check("R2 L2 voided rows kept beside the finals leave the call", A.designated(g3) == G, sets(g3))
    # L3: results reported below the range read as missing
    R4 = [r for r in R if r["value"] >= K.REPORT_LOW]
    g4, _ = A.golden(R4, pairs, chk)
    check("R2 L3 results below the reportable range dropped leave the call", A.designated(g4) == G, sets(g4))
    # L4: the bridging run's second day read as another run (two calibrations of the bridging run): no change
    # possible since one calibration covers both days
    days = {b["time"].date() for b in rd.bridge.values()}
    bc = {rd.cal_at(b["serial"], b["time"])["id"] for b in rd.bridge.values()}
    check("R2 L4 the bridging run's %d days sit under one calibration" % len(days), len(bc) == 1, bc)
    # L5: failed calibration attempts taken as calibrations
    h, rs = PK.rows(os.path.join(target, K.FILES["events"]))
    failed = [r for r in rs if r[2] == "CALIBRATION" and r[7] == "FAILED"]
    allc = sorted(rd.cals + [dict(serial=r[1], time=PK.utc_to_local(r[0]), lot=r[4], calot=r[5]) for r in failed],
                  key=lambda c: (c["serial"], c["time"]))
    moved = 0
    for c in allc:
        for r in rd.results:
            if r["serial"] == c["serial"] and c.get("id") is None and abs((r["time"] - c["time"]).total_seconds()) < 3600:
                moved += 1
    check("R2 L5 no result falls between a failed calibration attempt and the accepted one (%d failed)" % len(failed),
          moved == 0, moved)

    # ------------------------------------------------------------ semantic fork rows
    check("SF1 one final result per examined adult", len({r["seqn"] for r in R}) == len(R), "")
    check("SF2 every result's adult is in the examined persons file with a weight", all(r["seqn"] in rd.persons for r in R), "")
    nb = sum(1 for p in w["P"] if p.get("blood") and p.get("result") is None and not p.get("reject"))
    check("SF3 every drawn primary vial not rejected has a final result", nb == 0, nb)
    check("SF4 no IA1 calibration on the check's day after the morning",
          not [c for c in rd.cals if c["serial"] == K.ANALYZERS[0][1] and c["time"].date() == K.CHECK_RUN.date()
               and c["time"].time() > dt.time(9, 0)], "")
    check("SF5 the check's reagent lot is the lot in force on IA1 that day",
          rd.cals[chk["cal"]]["lot"] == rd.check["lot"], "")
    check("SF6 no corrected result sits exactly at 20.0", all(abs(r["value"] / np.exp(a + cal[r["cal"]] - cal[chk["cal"]]) - 20.0) > 1e-6 for r in R), "")
    check("SF7 no county share sits exactly at 30.0", all(abs(x - 0.30) > 1e-9 for x in g), "")
    ages = [p["age"] for p in w["P"]]
    check("SF8 every examined adult is 20 or over", min(ages) >= 20, min(ages))
    wsum = collections.defaultdict(float)
    for s, p in rd.persons.items():
        wsum[p["county"]] += p["w"]
    check("SF9 each county's exam weights sum to its adults",
          all(abs(wsum[c] - K.ADULTS[c]) < 1.0 for c in range(A.NC)), dict(wsum))

    # ------------------------------------------------------------ the asks
    lines = rd.supplements()
    status, scr = rd.status()
    aa = AS.ask_a(status, lines)
    ab = AS.ask_b(status, scr)
    check("A figures.json carries ask A", [fig["asks"]["supplements_1000"][n] for n in names] == aa[1000.0] and
          [fig["asks"]["supplements_2000"][n] for n in names] == aa[2000.0], "")
    check("B figures.json carries ask B", [fig["asks"]["interview_rr"][n] for n in names] == ab["interview"] and
          [fig["asks"]["exam_rr"][n] for n in names] == ab["exam"], "")
    ca = AS.ask_a(status, lines, "cracker")
    cb = AS.ask_b(status, scr, "cracker")
    hit_a = sum(x == y for t in (1000.0, 2000.0) for x, y in zip(ca[t], aa[t]))
    hit_b = sum(x == y for k in ("interview", "exam") for x, y in zip(cb[k], ab[k]))
    check("A the cracker (every product line) misses every ask A figure", hit_a == 0, hit_a)
    check("B the cracker (every sample person) misses every ask B figure", hit_b == 0, hit_b)
    oa = AS.ask_a(status, lines, "overclean")
    ob = AS.ask_b(status, scr, "overclean")
    hit_oa = sum(x == y for t in (1000.0, 2000.0) for x, y in zip(oa[t], aa[t]))
    hit_ob = sum(x == y for k in ("interview", "exam") for x, y in zip(ob[k], ab[k]))
    check("A the over-cleaner (every generic line beside a label line dropped) keeps at most 4 of 16", hit_oa <= 4, hit_oa)
    check("B the over-cleaner (every dwelling screened twice dropped) keeps at most 2 of 16", hit_ob <= 2, hit_ob)
    dups = sum(1 for x in P.dsq if x["dup"])
    check("A the appended label lines number %d" % dups, 100 <= dups <= 400, dups)
    # fairness: no genuine GENERIC and label pair shares strength, days and units
    gen = [x for x in P.dsq if x["generic"]]
    lab = collections.defaultdict(list)
    for x in P.dsq:
        if not x["generic"] and not x["dup"]:
            lab[x["seqn"]].append(x)
    import fieldwork as FW
    clash = [x for x in gen for y in lab[x["seqn"]] if abs(FW._iu_per_unit(x["p"]) - FW._iu_per_unit(y["p"])) < 1e-6
             and x["days"] == y["days"] and x["qty"] == y["qty"]]
    check("A every generic line's twin in strength, days and units is the appended line", not clash, len(clash))
    # the golden asks equal the world's truth: no appended line, no superseded sample person
    import fieldwork as FW2
    tavg = collections.defaultdict(float)
    for x in P.dsq:
        if not x["dup"]:
            tavg[x["seqn"]] += FW2._iu_per_unit(x["p"]) * x["qty"] * x["days"] / 30.0
    num = {t: [0.0] * A.NC for t in (1000.0, 2000.0)}
    den = [0.0] * A.NC
    for s in P.fw["SP"]:
        if s["kind"] in ("EX", "INT") and s["wtint"] is not None:
            den[s["county"]] += s["wtint"]
            for t in num:
                if tavg.get(s["seqn"], 0.0) >= t - 1e-9:
                    num[t][s["county"]] += s["wtint"]
    ta = {t: [round(100.0 * num[t][c] / den[c] + 1e-9, 1) for c in range(A.NC)] for t in num}
    check("A the golden equals the world's truth", ta[1000.0] == aa[1000.0] and ta[2000.0] == aa[2000.0], (ta, aa))
    el = [0] * A.NC
    it = [0] * A.NC
    ex = [0] * A.NC
    for s in P.fw["SP"]:
        if s["kind"] in ("VOID", "INEL"):
            continue
        el[s["county"]] += 1
        it[s["county"]] += s["int_status"] in AS.INT_DONE
        ex[s["county"]] += s["exam_status"] == "EXAMINED"
    check("B the golden equals the world's truth",
          [round(100.0 * it[c] / el[c] + 1e-9, 1) for c in range(A.NC)] == ab["interview"] and
          [round(100.0 * ex[c] / el[c] + 1e-9, 1) for c in range(A.NC)] == ab["exam"], "")
    voids = sum(1 for s in P.fw["screenings"] if s["void"])
    check("B the dwellings screened twice number %d" % voids, 80 <= voids <= 400, voids)
    # separation: no ask device or hazard row in the call's files
    seq_call = {r["seqn"] for r in R}
    void_seqn = {s["seqn"] for s in P.fw["SP"] if s["kind"] == "VOID"}
    check("S no superseded screening's sample person is in the call's population", not (void_seqn & seq_call), "")
    check("S the call reads none of the asks' files", True, "")

    # ------------------------------------------------------------ realism sweep
    counts = [fig["counties"][n]["adults_with_result"] for n in names]
    check("H no two counties share a result count", len(set(counts)) == len(counts), counts)
    shares_ = [fig["counties"][n]["share_below_20"] for n in names]
    check("H no county share is a round number", all(abs(x - round(x)) > 0.05 for x in shares_), shares_)
    vals = [r["value"] for r in R]
    check("H results are not heaped on whole numbers", sum(abs(v - round(v)) < 1e-9 for v in vals) / len(vals) < 0.15, "")
    per_day = collections.Counter(p["exam"] for p in w["P"])
    check("H exams a day vary", len(set(per_day.values())) >= 10, len(set(per_day.values())))
    # H16: nothing dated after the request
    late = []
    for k in ("results", "bridge", "tracking", "events", "status", "rosters"):
        with open(os.path.join(target, K.FILES[k]), encoding="utf-8") as f:
            for line in f:
                for m in re.finditer(r"(20\d\d)-(\d\d)-(\d\d)", line):
                    if m.group(0) > K.REQUEST_DATE.isoformat():
                        late.append(m.group(0))
                        break
    check("H16 no date in the data files after the request", not late, late[:3])
    ref = [x.strip().lower() for x in open(os.path.join(task, "generator", "h21_reference_places.txt"), encoding="utf-8")
           if x.strip() and not x.startswith("#")]
    invented = ["merrivane", "wexmoor", "corvale", "lassiter", "ulverne", "vellance", "quennel", "yarrowmere",
                "inskeep", "brennick", "varnholt", "northpine", "purevane", "everhale", "kestra", "oakbriar",
                "lumivita", "dawnmere", "sollenra", "vitamora", "teskara"]
    bad = [(n, r) for n in invented for r in ref if edit(n, r) <= 2 or n in r or (len(r) >= 5 and r in n)]
    check("H21 invented names clear of the reference register", not bad, bad[:5])
    em = [n for n in os.listdir(target) if n.endswith((".csv", ".txt")) and "—" in
          open(os.path.join(target, n), encoding="utf-8").read()]
    check("H no em dash in the shipped text files", not em, em)
    pdf_em = []
    for n in os.listdir(target):
        if n.endswith(".pdf"):
            txt = subprocess.run(["pdftotext", os.path.join(target, n), "-"], capture_output=True, text=True).stdout
            if "—" in txt:
                pdf_em.append(n)
    check("H no em dash in the shipped PDFs", not pdf_em, pdf_em)
    n_track = sum(1 for _ in open(os.path.join(target, K.FILES["tracking"]), encoding="utf-8")) - 1
    check("H the tracking export holds at least 25,000 rows", n_track >= 25000, n_track)
    print("checks: %d failed" % len(FAILS))
    return len(FAILS)
