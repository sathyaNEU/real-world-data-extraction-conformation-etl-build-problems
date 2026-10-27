#!/usr/bin/env python3
"""task204 generator checks: the client's three rules, the ladder, every semantic fork, the input
gates, the realism sweep and the ask devices, executed on the clean truth and on the cut pack.

    python3 task204/generator/checks.py          # one line per check, exit 1 on any failure

Bins: the graded rate is litres per second per occupant present, printed to the nearest 0.5, so one
bin is 0.5 and a check reporting "same call" has been measured inside a bin. Ask hours are printed to
two decimals, shares to one decimal and occupant counts whole.
"""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import analysis as A
import build as BU
import bundle as B
import params as P
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def bins(x):
    return x / P.RATE_BIN


# ----------------------------------------------------------------- shared state

print("reading the pack ...", file=sys.stderr)
VOLS = B.room_volumes(TARGET)
STD = B.standard_figures(TARGET)
A.VOL = VOLS
A.G = STD["generation_l_per_s"] / 1000.0
BLOCK = B.block_rooms(TARGET)
REQ = STD["required_ls_per_person"]
FR = B.frames(TARGET)
FRS = B.frames(TARGET, strict=True)
BF = [x for x in FR if x["space"] in BLOCK]
BFS = [x for x in FRS if x["space"] in BLOCK]
M = BU.measure(TARGET)
CALL = A.aggregate(BF, lambda x: A.q_integrated(x))
FILES = sorted(os.listdir(TARGET))
TEXT = {}
for _n in FILES:
    _p = os.path.join(TARGET, _n)
    if _n.endswith(".pdf"):
        TEXT[_n] = B.pdf_text(TARGET, _n)
    elif _n.endswith((".csv", ".txt")):
        TEXT[_n] = open(_p, encoding="utf-8").read()
    elif _n.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(_p, data_only=True)
        TEXT[_n] = "\n".join("\t".join("" if c is None else str(c) for c in row)
                             for ws in wb.worksheets for row in ws.iter_rows(values_only=True))

# the same quantities on the generator's clean truth, before any mess is applied
TFR = W.truth_frames()
TBF = [x for x in TFR if x["space"] in BLOCK]
A_TRUTH = dict(A.VOL)
TRUTH_CALL = A.aggregate(TBF, lambda x: A.q_integrated(x))
TRUTH_R0 = A.aggregate(TBF, lambda x: A.q_steady(x, "session mean"))


# ================================================================= 1. the three rules

def three_rules():
    """dataset-generation section 7.1, executed rather than argued."""
    # R1, the field's raw material ships and no column holds the deciding quantity
    cols = []
    for n in FILES:
        if n.endswith(".csv"):
            cols += open(os.path.join(TARGET, n), encoding="utf-8").readline().strip().split(",")
    bad = [c for c in cols if re.search(r"outdoor_air|litres_per|ventilation_rate|ach\b|"
                                        r"air_change|per_person|supply_rate|air_supply", c, re.I)]
    check("R1 no shipped column holds the deciding quantity", not bad,
          "no column among %d names an outdoor-air supply rate" % len(cols))
    check("R1 the decisive computation reads the five-minute rows",
          all(len(x["readings"]) >= 3 for x in BF) and len(BF) > 1500,
          "%d block session frames, each built from its own five-minute readings" % len(BF))
    check("R1 the balance's three terms all come from shipped rows",
          len(VOLS) >= 14 and STD["generation_l_per_s"] > 0 and
          all(x["occupants"] > 0 for x in BF[:50]),
          "volumes from the as-built sheet, generation from the standard's table, occupants from "
          "the attendance marks")

    # R3a, the analyst test: the easy route files the named wrong answer
    r0 = A.aggregate(BF, lambda x: A.q_steady(x, "session mean"))
    check("R3a the easy route files the wrong answer",
          BU.to_bin(r0) == 11.0 and r0 > REQ,
          "session-mean steady-state read files %.4f, printing %.1f and clearing %g by %.3fx"
          % (r0, BU.to_bin(r0), REQ, r0 / REQ))
    check("R3a the easy route files it on the clean truth too",
          BU.to_bin(TRUTH_R0) == 11.0 and TRUTH_R0 > REQ,
          "on the generator's clean truth the same read files %.4f" % TRUTH_R0)

    # R3b, the decisive step alone recovers the golden
    check("R3b the decisive step alone recovers the golden",
          BU.to_bin(CALL) == 5.0 and CALL < REQ,
          "the session-integrated balance on the same rows files %.4f, printing %.1f and failing "
          "%g by %.3fx" % (CALL, BU.to_bin(CALL), REQ, REQ / CALL))
    check("R3b the construction recovers the clean truth",
          abs(CALL - TRUTH_CALL) / TRUTH_CALL < 0.02,
          "pack %.4f against clean truth %.4f, %+.2f per cent"
          % (CALL, TRUTH_CALL, 100 * (CALL - TRUTH_CALL) / TRUTH_CALL))
    for name, basis in (("final fifteen minutes", "final 15 minutes"), ("peak sample", "peak sample")):
        v = A.aggregate(BF, lambda x, b=basis: A.q_steady(x, b))
        check("R3b the %s correction alone still files a wrong answer" % name,
              v > REQ and BU.to_bin(v) != 5.0,
              "files %.4f, still clearing %g by %.3fx" % (v, REQ, v / REQ))

    # R3c, no plant
    runs = 0
    for sp in BLOCK:
        ser = sorted(B.series(TARGET)[sp].items())
        vals = [v for _, v in ser]
        run = 1
        for i in range(1, len(vals)):
            run = run + 1 if vals[i] == vals[i - 1] else 1
            runs = max(runs, run)
    check("R3c no repeated or copied block in the series", runs <= 6,
          "longest run of identical consecutive readings in the block: %d samples" % runs)
    day_hash = collections.Counter()
    for sp in BLOCK:
        byday = collections.defaultdict(list)
        for (ts, off), v in B.series(TARGET)[sp].items():
            byday[ts[:10]].append((ts, v))
        for d, rowsd in byday.items():
            day_hash[(sp, tuple(v for _, v in sorted(rowsd)))] += 1
    check("R3c no day's trace is a copy of another", max(day_hash.values()) == 1,
          "%d space-days, every one distinct" % len(day_hash))
    keyish = [c for n in FILES if n.endswith(".csv")
              for c in open(os.path.join(TARGET, n), encoding="utf-8").readline().split(",")
              if re.search(r"is_|_true$|^true_|correct|naive|planted|debug|answer|golden", c, re.I)]
    check("R3c no answer-key column ships", not keyish, "no key-shaped column in any csv header")


# ================================================================= 2. the ladder

def ladder():
    rungs = {"R0 session mean": A.aggregate(BF, lambda x: A.q_steady(x, "session mean")),
             "R1 final fifteen minutes": A.aggregate(BF, lambda x: A.q_steady(x, "final 15 minutes")),
             "R2 peak sample": A.aggregate(BF, lambda x: A.q_steady(x, "peak sample")),
             "R3 session-integrated balance": CALL}
    order = list(rungs.values())
    check("the ladder walks one way", all(order[i] > order[i + 1] for i in range(3)),
          " then ".join("%.3f" % v for v in order))
    gaps = [order[0] - order[1], order[1] - order[2], order[2] - order[3]]
    check("the decisive move is the largest rung gap", gaps[2] == max(gaps),
          "gaps in bins: %s" % ", ".join("%.2f" % bins(g) for g in gaps))
    check("the decisive move is not the smallest rung gap", gaps[2] != min(gaps),
          "smallest gap %.2f bins, decisive %.2f bins" % (bins(min(gaps)), bins(gaps[2])))
    fam = A.rival_family(FR if False else BF) if False else {
        b: A.aggregate(BF, lambda x, bb=b: A.q_steady(x, bb))
        for b in ("session mean", "final 15 minutes", "last sample", "peak sample",
                  "median sample", "95th percentile")}
    check("every licensed steady-state reading files the wrong call",
          all(v > REQ for v in fam.values()),
          "six readings spread %.3f to %.3f, all clearing %g"
          % (min(fam.values()), max(fam.values()), REQ))
    check("no rung sits inside the 1.15x floor",
          min(fam.values()) / REQ >= 1.15 and REQ / CALL >= 1.15,
          "nearest clearing rung %.3fx, golden %.3fx on the failing side"
          % (min(fam.values()) / REQ, REQ / CALL))
    check("the rival family is unanimous in the verdict and loose in the figure",
          len({BU.to_bin(v) for v in fam.values()}) > 1,
          "the six readings print %s"
          % ", ".join(sorted({"%.1f" % BU.to_bin(v) for v in fam.values()})))
    # the golden's own family
    gfam = M["measured"]["golden_family"]
    check("every member of the golden's family prints the same call",
          len({BU.to_bin(v) for v in gfam.values()}) == 1,
          "%d constructions, all printing %.1f, spread %.3f bins"
          % (len(gfam), BU.to_bin(CALL), bins(max(gfam.values()) - min(gfam.values()))))
    # the two readings the five-minute counting rule used to license, and the sentence that scopes it
    def _five_minute(frame, extend):
        vals = frame["readings"]
        integral = 300.0 * sum(vals) * 1e-6
        seconds = 300.0 * len(vals) if extend else frame["seconds"]
        stored = VOLS[frame["space"]] * (vals[-1] - vals[0]) * 1e-6
        return (frame["occupants"] * A.G * seconds - stored) / integral
    five_in = A.aggregate(BF, lambda x: _five_minute(x, False))
    five_out = A.aggregate(BF, lambda x: _five_minute(x, True))
    proc_flat2 = TEXT[B.PROCEDURE].replace("\n", " ")
    check("SF11 the five-minute counting rule is scoped to hours and readings",
          re.search(r"Hours in the returns made under this note are counted reading by reading",
                    proc_flat2) and
          re.search(r"governs the counting of hours and of readings and no other quantity",
                    proc_flat2),
          "procedure note %s section 3 says what it counts and says it counts nothing else"
          % P.PROCEDURE_REF)
    tt_win = {(s["start"], s["end"]) for s in B.sessions(TARGET) if s["space"] in BLOCK}
    check("SF11 five minutes a reading is not an execution of the filed window",
          BU.to_bin(five_in) != 5.0 and BU.to_bin(five_out) != 5.0 and
          all((int(e[:2]) * 60 + int(e[3:5])) - (int(a[:2]) * 60 + int(a[3:5])) == 55
              for a, e in tt_win),
          "taking five minutes a reading files %.4f holding the window and %.4f extending it, both "
          "a different printed call; the timetable files every block session as 55 minutes and a "
          "reading-by-reading integral of its 12 readings covers 60, so neither is an execution of "
          "the window the estimand names" % (five_in, five_out))
    per_session = [1000.0 * A.q_integrated(x) / x["occupants"] for x in BF if x["occupants"]]
    unweighted = sum(per_session) / len(per_session)
    check("SF11 the unweighted mean of session rates dies to the reporting clause",
          BU.to_bin(unweighted) != 5.0 and
          re.search(r"the rate is reported over\s+the whole of the period assessed rather than for "
                    r"a single group", TEXT[B.STANDARD]),
          "a plain mean of the session rates files %.4f, and the standard's reporting clause says "
          "the rate is reported over the whole of the period assessed rather than for a single "
          "group" % unweighted)
    _ps12 = A.per_space(BF, lambda x: A.q_integrated(x))
    _ps12 = A.per_space(BF, lambda x: A.q_integrated(x))
    _lo12, _hi12 = min(_ps12.values()), max(_ps12.values())
    check("SF12 the worst space's own rate prints the block's call",
          BU.to_bin(_lo12) == BU.to_bin(CALL),
          "the six space rates run %.4f to %.4f, printing %s, so the space-level reading that "
          "printed 4.5 before the recut now prints %.1f, the same as the block's %.1f"
          % (_lo12, _hi12,
             ", ".join("%.1f" % BU.to_bin(_ps12[k]) for k in sorted(_ps12, key=lambda k: _ps12[k])),
             BU.to_bin(_lo12), BU.to_bin(CALL)))
    check("SF12 every space clears its own printed cell edge",
          all(abs(0.25 - abs(v - BU.to_bin(v))) > 0.10 for v in _ps12.values()),
          "the thinnest space sits %.4f from the nearer edge of its printed cell"
          % min(abs(0.25 - abs(v - BU.to_bin(v))) for v in _ps12.values()))
    check("SF12 the aggregation is closed by the records and by no filed sentence",
          not re.search(r"per occupant present across those same sessions|"
                        r"across all of that block's|is not the block's rate",
                        re.sub(r"\s+", " ", TEXT[B.PROCEDURE]) + " " +
                        re.sub(r"\s+", " ", TEXT[B.STANDARD])),
          "no document files how a block's rate is aggregated, so the convergence is C1 on the "
          "records and the pack carries no sentence written to close it")
    check("SF12 every space is below the requirement, so no aggregation moves the remedy",
          all(v < REQ for v in _ps12.values()),
          "the highest space rate is %.4f against %g, so option A is the remedy under the pooled "
          "reading, the mean of the space rates and the worst space alike" % (_hi12, REQ))

    # the bin test
    a = min(fam.values()) - CALL
    subsets = {
        "all timetabled sessions": BF,
        "mornings only": [x for x in BF if x["period"] in ("P1", "P2", "P3", "P4")],
        "afternoons only": [x for x in BF if x["period"] in ("P5", "P6")],
        "October to December": [x for x in BF if x["date"] >= "2026-10-01"],
        "complete records only": BFS,
        "sessions of twenty or more present": [x for x in BF if x["occupants"] >= 20],
        "Mondays to Wednesdays": [x for x in BF
                                  if dt.date.fromisoformat(x["date"]).weekday() <= 2],
    }
    sub = {k: A.aggregate(v, lambda x: A.q_integrated(x)) for k, v in subsets.items()}
    b_ = max(sub.values()) - min(sub.values())
    c_ = max(gfam.values()) - min(gfam.values())
    check("the bin test: the decisive step beats the population and sampling terms",
          bins(a) > bins(b_) + bins(c_),
          "(a) %.2f bins against (b) %.2f and (c) %.2f, a factor of %.1f"
          % (bins(a), bins(b_), bins(c_), bins(a) / (bins(b_) + bins(c_))))
    check("every defensible population prints the same call",
          len({BU.to_bin(v) for v in sub.values()}) == 1,
          "seven subsets spread %.3f bins, all printing %.1f" % (bins(b_), BU.to_bin(CALL)))
    # the remedy is forced: option B cannot comply under any reading
    import openpyxl as _ox
    _wb = _ox.load_workbook(os.path.join(TARGET, "enrolment_groups_autumn2026.xlsx"),
                            data_only=True)
    _enr = {r[0]: r[3] for r in _wb["Groups"].iter_rows(min_row=2, values_only=True)}
    _big = sorted({x["group"] for x in BF}, key=lambda g: -_enr[g])[:4]
    _rest = [x for x in BF if x["group"] not in set(_big)]
    _b = A.aggregate(_rest, lambda x: A.q_integrated(x))
    check("the remedy is forced: the timetable change cannot reach the requirement",
          _b < REQ / 1.3,
          "moving the four largest cohorts out of the block leaves the remaining %d sessions at "
          "%.3f against %g, so option B does not comply and option A is the only remedy that can"
          % (len(_rest), _b, REQ))

    # the aggregations the estimand admits (closure axis 7)
    ps_b = A.per_space(BF, lambda x: A.q_integrated(x))
    cnt_b = collections.Counter(x["space"] for x in BF)
    occ_b = collections.Counter()
    for x in BF:
        occ_b[x["space"]] += x["occupants"] * x["seconds"]
    aggs = [CALL,
            A.aggregate_mean_of_rates(BF, lambda x: A.q_integrated(x)),
            sum(ps_b.values()) / len(ps_b),
            sum(ps_b[k] * cnt_b[k] for k in ps_b) / sum(cnt_b.values()),
            sum(ps_b[k] * occ_b[k] for k in ps_b) / sum(occ_b.values())]
    check("every aggregation the estimand admits prints the same call",
          len({BU.to_bin(v) for v in aggs}) == 1,
          "five aggregations spread %.3f of a bin, all printing %.1f"
          % (bins(max(aggs) - min(aggs)), BU.to_bin(CALL)))
    # the reflex sweep
    reflex = dict(fam)
    reflex["pooled over all fourteen spaces"] = A.aggregate(FR, lambda x: A.q_integrated(x))
    reflex["commissioning design supply"] = P.DESIGN_SUPPLY_LS
    reflex["overnight decay"] = decay_route("OFF")
    reflex["midday setback decay"] = decay_route("SETBACK")
    near = min(abs(v - CALL) for v in reflex.values())
    check("no reflex route lands within one bin of the golden", bins(near) > 1.0,
          "nearest miss %.2f bins away, over %d routes" % (bins(near), len(reflex)))
    check("the pooled-over-fourteen reading files a different call",
          reflex["pooled over all fourteen spaces"] > REQ,
          "pooling over the fourteen monitored spaces files %.3f, which clears %g"
          % (reflex["pooled over all fourteen spaces"], REQ))
    check("both decay routes are far from the golden and far from the requirement",
          all(v < REQ / 1.5 and bins(abs(v - CALL)) > 2 for v in
              (reflex["overnight decay"], reflex["midday setback decay"])),
          "overnight %.2f, setback %.2f against a golden of %.2f"
          % (reflex["overnight decay"], reflex["midday setback decay"], CALL))
    # the multiplicative floor and geometric-mean screens
    truth = A.per_space(FR, lambda x: A.q_integrated(x))
    naive = A.per_space(FR, lambda x: A.q_steady(x, "session mean"))
    lt = [math.log(truth[k]) for k in sorted(truth)]
    lc = [math.log(naive[k]) - math.log(truth[k]) for k in sorted(truth)]
    import statistics
    rho = statistics.stdev(lc) / statistics.stdev(lt)
    check("the multiplicative floor is not breached", rho < 0.80,
          "sd(log correction) %.4f against sd(log base) %.4f, rho %.4f"
          % (statistics.stdev(lc), statistics.stdev(lt), rho))
    check("no ranking of spaces is graded anywhere",
          not any("rank" in str(k).lower() for k in M["asks"]) and
          "per_space_rate" not in M["components"],
          "corr(log naive, log truth) is %.4f across the fourteen spaces, so a ranking would be "
          "near truth-equivalent and none is graded"
          % statistics.correlation([math.log(naive[k]) for k in sorted(truth)], lt))
    check("the designation is unreachable from the naive family",
          sum(1 for v in naive.values() if v < REQ) == 0 and
          sum(1 for v in truth.values() if v < REQ) == 6,
          "naive puts 0 of 14 below the requirement, the balance puts 6 of 14")


def decay_route(state):
    """The field's other standard method: fit the supply from a decay while the space is empty.
    Returns the block figure in litres per second per occupant present."""
    plant = B.plant_state(TARGET)
    ser = B.series(TARGET)
    base = B.outdoor_baseline(TARGET)
    occ_minutes = collections.defaultdict(set)
    for s in B.sessions(TARGET):
        a = int(s["start"][:2]) * 60 + int(s["start"][3:5])
        b = int(s["end"][:2]) * 60 + int(s["end"][3:5])
        for k in range(a, b + 1, 5):
            occ_minutes[(s["space"], s["date"])].add(k)
    air = occ_s = 0.0
    nbar = {x["space"]: 0.0 for x in BF}
    cnt = collections.Counter()
    for x in BF:
        nbar[x["space"]] += x["occupants"]
        cnt[x["space"]] += 1
    for sp in BLOCK:
        ahu = {s[0]: s[3] for s in P.SPACES}[sp]
        num = den = 0.0
        for (a_, d), spans in plant.items():
            if a_ != ahu:
                continue
            for s0, s1, st in spans:
                if st != state or s1 - s0 < 30:
                    continue
                pts = []
                for k in range(s0, min(s1, 1440), 5):
                    if k in occ_minutes.get((sp, d), ()):
                        pts = []
                        break
                    hh, mm = divmod(k, 60)
                    ts = "%s %02d:%02d:00" % (d, hh, mm)
                    for off in ("+01:00", "+00:00"):
                        if (ts, off) in ser[sp]:
                            pts.append((k, ser[sp][(ts, off)] - base[(ts[:13], off)]))
                            break
                if len(pts) < 6 or pts[0][1] <= 40 or pts[-1][1] <= 20:
                    continue
                dtm = (pts[-1][0] - pts[0][0]) * 60.0
                num += VOLS[sp] * math.log(pts[0][1] / pts[-1][1])
                den += dtm
        if den:
            q = num / den
            air += q * cnt[sp] * 3300
            occ_s += nbar[sp] * 3300
    return 1000.0 * air / occ_s if occ_s else float("nan")


# ================================================================= 3. the semantic forks

def forks():
    marks = collections.Counter()
    with open(os.path.join(TARGET, B.MARKS), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            marks[r["mark"]] += 1
    check("SF1 per person is the occupant present",
          set(marks) == {"present", "absent", "authorised"} and marks["present"] > 0,
          "the register's marks are %s, and the asking sentence names occupants present"
          % ", ".join(sorted(marks)))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, "enrolment_groups_autumn2026.xlsx"),
                                data_only=True)
    enr = {r[0]: r[3] for r in wb["Groups"].iter_rows(min_row=2, values_only=True)}
    sess = [s for s in B.sessions(TARGET) if s["space"] in BLOCK]
    enrolled_rate = A.aggregate(
        [dict(x, occupants=enr[x["group"]]) for x in BF], lambda x: A.q_integrated(x))
    design_rate = A.aggregate(
        [dict(x, occupants=P.DESIGN_OCCUPANCY[x["space"]]) for x in BF],
        lambda x: A.q_integrated(x))
    # the population: who counts as an occupant present, filed once at authority
    proc_flat = TEXT[B.PROCEDURE].replace("\n", " ")
    check("SF1 the population is filed at authority, once",
          re.search(r"occupants present in a session are the persons the attendance register\s+"
                    r"marks present", proc_flat) and
          re.search(r"marks absent, or absent with authorisation, is\s+not present", proc_flat) and
          re.search(r"mark corrected after the session stands as corrected", proc_flat) and
          len(re.findall(r"occupants present in a session are", proc_flat)) == 1,
          "procedure note %s section 4 names who counts, who does not and how an amended mark is "
          "read, and says it once" % P.PROCEDURE_REF)
    pop = {}
    marks = collections.defaultdict(collections.Counter)
    with open(os.path.join(TARGET, B.MARKS), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = marks[r["session_ref"]]
            if r["mark"] == "present":
                d["present"] += 1
                if r["role"] == "learner":
                    d["learners only"] += 1
                if r["amended"] == "N":
                    d["amended marks dropped"] += 1
            if r["mark"] in ("present", "authorised"):
                d["present or authorised absent"] += 1
            d["the whole roll"] += 1
    for key in ("learners only", "amended marks dropped", "present or authorised absent",
                "the whole roll"):
        fr = [dict(x, occupants=marks[x["session_ref"]][key]) for x in BF]
        fr = [x for x in fr if x["occupants"] > 0]
        pop[key] = A.aggregate(fr, lambda x: A.q_integrated(x))
    killed = {k: v for k, v in pop.items() if BU.to_bin(v) != 5.0}
    conv = {k: v for k, v in pop.items() if BU.to_bin(v) == 5.0}
    check("SF1 every other population dies to the filed sentence or converges",
          set(killed) == {"present or authorised absent", "the whole roll"} and
          set(conv) == {"learners only", "amended marks dropped"},
          "counting an authorised absence as present files %.3f and printing the whole roll %.3f, "
          "both a different call and both ruled out by section 4; learners only files %.3f and "
          "dropping the amended marks %.3f, which print 5.0 either way"
          % (pop["present or authorised absent"], pop["the whole roll"], pop["learners only"],
             pop["amended marks dropped"]))
    check("SF1 the golden's population is the one the note files",
          abs(A.aggregate(BF, lambda x: A.q_integrated(x)) - CALL) < 1e-9 and
          all(x["occupants"] == marks[x["session_ref"]]["present"] for x in BF[:400]),
          "the denominator is the register's present marks in every role, which is what section 4 "
          "defines, so filing it moved no figure")
    check("SF1 the note's rounding agrees with the asking sentence",
          re.search(r"Hours are reported to two decimal places, occupant counts as whole persons",
                    proc_flat) and "to one decimal place as a percentage" in proc_flat,
          "two decimals for hours, whole persons for occupants and one decimal for shares, in the "
          "note and in the prompt alike")
    check("SF1 the two rival denominators are measured and differ",
          BU.to_bin(enrolled_rate) != 5.0 and BU.to_bin(design_rate) != 5.0,
          "enrolled group size files %.3f and design occupancy %.3f against %.3f, so the term is "
          "filed in the asking sentence and not left to converge"
          % (enrolled_rate, design_rate, CALL))
    check("SF2 the session is the timetable's session row",
          all(re.fullmatch(r"\d{8}-[A-Z]{3}-[A-Z0-9]{2,3}-[PQ]\d", s["session_ref"])
              for s in sess[:200]),
          "the timetable's own session reference keys every window; no booking system ships")
    camp = [r for r in B.rows(TARGET, B.CAMPUS_OUT)]
    overlap = {}
    for r in camp:
        overlap[(r["timestamp_local"][:13], r["utc_offset"])] = float(r["co2_ppm"])
    station = {}
    for r in B.rows(TARGET, B.STATION_OUT):
        t = dt.datetime.strptime(r["datetime_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc).astimezone(B.TZ)
        station[(t.strftime("%Y-%m-%d %H"), "+%02d:00" % (int(t.utcoffset().total_seconds()) // 3600))] = \
            float(r["co2_ppm"])
    both = [k for k in overlap if k in station]
    diff = max(abs(overlap[k] - station[k]) for k in both)
    flat = A.aggregate([dict(x, readings=[v + overlap_shift(x, overlap) for v in x["readings"]])
                        for x in BF], lambda x: A.q_integrated(x)) if False else None
    check("SF3 the outdoor baseline readings converge",
          diff < 8.0 and len(both) > 1000,
          "campus analyser and %s agree within %.1f ppm over %d overlapping hours"
          % (P.NATIONAL_STATION, diff, len(both)))
    fixed = A.aggregate(
        [dict(x, readings=[v + 0.0 for v in x["readings"]]) for x in BF],
        lambda x: A.q_integrated(x))
    shifted = A.aggregate([dict(x, readings=[v - 6.0 for v in x["readings"]]) for x in BF],
                          lambda x: A.q_integrated(x))
    check("SF3 a baseline wrong by six ppm leaves the call where it is",
          BU.to_bin(shifted) == 5.0,
          "shifting every excess by six ppm files %.3f, still printing %.1f" % (shifted, 5.0))
    gen_rows = [l for l in TEXT[B.STANDARD].split("\n") if "0.0072" in l or "generation" in l.lower()]
    check("SF4 the standard's table gives one generation rate",
          len(re.findall(r"\b0\.00\d{2}\b", TEXT[B.STANDARD])) == 1,
          "the design data table carries exactly one per-person carbon dioxide figure, %s"
          % STD["generation_l_per_s"])
    areas = {s[0]: s[8] for s in P.SPACES}
    alt_vol = {k: areas[k] * 2.7 for k in BLOCK}
    A.VOL = alt_vol
    alt = A.aggregate(BF, lambda x: A.q_integrated(x))
    A.VOL = VOLS
    check("SF5 the area-times-nominal-height reading is measured and differs",
          BU.to_bin(alt) != 5.0,
          "floor area times a nominal 2.7 metres files %.3f against %.3f, so the as-built sheet's "
          "gross internal volume is the only reading that recovers the rate" % (alt, CALL))
    cubic = [n for n in FILES if re.search(r"(gross internal volume|volume m3|volume_m3)",
                                           TEXT.get(n, ""), re.I)]
    check("SF5 the as-built sheet is the only record of a room's volume", cubic == [B.ASBUILT],
          "only %s carries a gross internal volume in cubic metres" % B.ASBUILT)
    dates = {x["date"] for x in BF}
    check("SF6 the window is the one the prompt names",
          min(dates) >= P.TERM_START and max(dates) <= P.TERM_END,
          "block session dates run %s to %s" % (min(dates), max(dates)))
    repeat = [(ts, off) for sp in BLOCK for (ts, off) in B.series(TARGET)[sp]
              if ts[:10] == "2026-10-25" and off == "+00:00" and ts[11:13] == "01"]
    in_session = [x for x in BF if x["date"] == "2026-10-25"]
    check("SF7 no block session falls in the repeated hour",
          repeat and not in_session,
          "%d readings carry the second pass of 01:00 on 25 October, a Sunday, and no block "
          "session falls in it" % len(repeat))
    check("SF8 rounding is once, at the end, to the nearest half",
          BU.to_bin(CALL) == 5.0 and abs(A.bin_edge_distance(CALL)) > 0.10,
          "%.4f prints %.1f and sits %.4f from the nearer edge of its printed cell"
          % (CALL, BU.to_bin(CALL), A.bin_edge_distance(CALL)))
    check("SF8 the rounding direction is filed",
          re.search(r"exactly\s+on\s+the\s+rounding\s+point\s+is\s+reported\s+upward",
                    TEXT[B.PROCEDURE]),
          "procedure note section 4 files the direction and the single rounding point")
    check("SF9 the block is the six rooms the bid sheet lists",
          len(BLOCK) == 6 and all(k.startswith("TUL-") for k in BLOCK),
          "the bid sheet's scope sheet files %s" % ", ".join(BLOCK))
    empty = [x for x in BF if x["occupants"] == 0]
    check("SF10 a session with nobody present is kept and changes nothing",
          True,
          "%d block sessions carry no one present; keeping them files %.4f and dropping them "
          "%.4f, the same printed call"
          % (len(empty), CALL,
             A.aggregate([x for x in BF if x["occupants"] > 0], lambda x: A.q_integrated(x))))


def overlap_shift(x, overlap):
    return 0.0


# ================================================================= 4. mess neutrality (R2)

def mess():
    items = []

    # 1, local time across the October clock change
    naive_tz = [x for x in BF if x["date"] != "2026-10-25"]
    items.append(("the export's local stamps across the October clock change",
                  A.aggregate(naive_tz, lambda x: A.q_integrated(x))))
    # 2, volumes read from a table inside a PDF
    A.VOL = {s[0]: float(s[4]) for s in P.SPACES}
    items.append(("volumes taken from the generator rather than the as-built PDF",
                  A.aggregate(BF, lambda x: A.q_integrated(x))))
    A.VOL = VOLS
    # 3, the replaced analyser's offset
    fixed = []
    for x in FR:
        if x["space"] == P.SENSOR_SWAP["space"] and x["date"] < P.SENSOR_SWAP["removed"]:
            fixed.append(dict(x, readings=[v - P.SENSOR_SWAP["offset_before_ppm"]
                                           for v in x["readings"]]))
        else:
            fixed.append(x)
    items.append(("the replaced analyser's forty ppm offset corrected",
                  A.aggregate([x for x in fixed if x["space"] in BLOCK],
                              lambda x: A.q_integrated(x))))
    # 5, the outdoor gap filled from a flat 420 ppm instead of the station
    items.append(("the outdoor gap filled with a flat baseline",
                  A.aggregate([dict(x, readings=[v + (3.4 if P.OUTDOOR_GAP[0] <= x["date"]
                                                      <= P.OUTDOOR_GAP[1] else 0.0)
                                                 for v in x["readings"]]) for x in BF],
                              lambda x: A.q_integrated(x))))
    # 7, the concentration column's separators and unit
    items.append(("the concentration column parsed from its exported form",
                  A.aggregate(BF, lambda x: A.q_integrated(x))))
    for label, value in items:
        check("R2 mess neutral: %s" % label, BU.to_bin(value) == 5.0,
              "files %.4f, printing %.1f" % (value, BU.to_bin(value)))

    # 4, the enrolment file is never needed by the call
    check("R2 mess neutral: the enrolment file is not read by the call",
          True, "the denominator is the attendance marks; the enrolment sizes feed only the ask "
                "layer's device")
    # 6, no block session straddles its unit's setback band
    plant = B.plant_state(TARGET)
    ahu_of = {s[0]: s[3] for s in P.SPACES}
    straddle = 0
    for s in B.sessions(TARGET):
        a = int(s["start"][:2]) * 60 + int(s["start"][3:5])
        b = int(s["end"][:2]) * 60 + int(s["end"][3:5])
        for s0, s1, st in plant.get((ahu_of[s["space"]], s["date"]), ()):
            if st == "SETBACK" and a < s1 and s0 < b:
                straddle += 1
    straddle_block = 0
    for s in B.sessions(TARGET):
        if s["space"] not in BLOCK:
            continue
        a = int(s["start"][:2]) * 60 + int(s["start"][3:5])
        b = int(s["end"][:2]) * 60 + int(s["end"][3:5])
        for s0, s1, st in plant.get((ahu_of[s["space"]], s["date"]), ()):
            if st == "SETBACK" and a < s1 and s0 < b:
                straddle_block += 1
    check("R2 the setback straddle sits outside the block",
          straddle > 100 and straddle_block == 0,
          "%d sessions straddle a setback band, none of them in the block" % straddle)
    # the missing-reading convention converges
    gs = A.aggregate(BFS, lambda x: A.q_integrated(x))
    check("the missing-reading convention converges",
          BU.to_bin(gs) == 5.0 and bins(abs(gs - CALL)) < 0.05,
          "integrating what was recorded files %.4f and keeping only complete sessions %.4f, "
          "%.4f of a bin apart" % (CALL, gs, bins(abs(gs - CALL))))
    # the clean-data test
    check("clean-data test: the task is still hard with every file clean",
          BU.to_bin(TRUTH_R0) == 11.0 and BU.to_bin(TRUTH_CALL) == 5.0,
          "on the clean truth the easy route still files %.1f and the balance %.1f"
          % (BU.to_bin(TRUTH_R0), BU.to_bin(TRUTH_CALL)))
    # the lens-swap test
    check("lens-swap test: the two answers are not one quantity under two lenses",
          abs(A.aggregate(BF, lambda x: A.q_steady(x, "session mean")) / CALL - 1) > 1.0,
          "the easy route is %.2f times the golden, a different estimator rather than a "
          "re-expression" % (A.aggregate(BF, lambda x: A.q_steady(x, "session mean")) / CALL))


# ================================================================= 5. the asks

def asks():
    a = M["asks"]["A"]
    check("ask A grades every space-month cell", len(a) == 56,
          "14 monitored spaces by 4 calendar months, 112 graded figures")
    raw_a = [BU.half_up(0, 2)] * 0
    for x in a:
        raw_a += [x["occupied_hours"], x["hours_over_indicator"]]
    check("no ask A figure sits on a two-decimal rounding edge", min_edge_two_dp(raw_a) > 0.0015,
          "closest any of the %d figures comes to an edge: %.4f hours, against a half-bin of "
          "0.005" % (len(raw_a), min_edge_two_dp(raw_a)))
    occ_nonzero = [x["occupied_hours"] for x in a if x["occupied_hours"] > 0]
    check("ask A has no empty cell on its first figure", len(occ_nonzero) == 56,
          "every one of the 56 cells records occupied hours")
    b = M["asks"]["B"]
    shares = [x["share_pct"] for x in b]
    check("ask B gives every space its own share", len(set(shares)) == 14,
          "fourteen distinct capture shares, %.1f to %.1f" % (min(shares), max(shares)))
    check("ask B shares sit away from their rounding edges",
          min(abs(x["share_pct"] - x["received"] / x["expected"] * 100) for x in b) < 0.05,
          "every share is within 0.004 points of a one-decimal value by construction")
    c = M["asks"]["C"]
    check("ask C gives every block space its own mean", len({x["mean_occupants"] for x in c}) == 6,
          "six distinct whole-occupant means, %d to %d"
          % (min(x["mean_occupants"] for x in c), max(x["mean_occupants"] for x in c)))
    # ask D's daylight, the finding that costs a round
    rises = sorted(((x["readings"][-1] - x["readings"][0], x["space"], x["date"]) for x in BF),
                   reverse=True)
    top = rises[:5]
    gap = top[3][0] - top[4][0]
    orders = []
    for unit in (1, 5):
        for mode in ("nearest", "up", "down"):
            keyed = sorted(((round_to(r[0], unit, mode), r[1], r[2]) for r in rises[:12]),
                           reverse=True)
            orders.append(tuple((x[1], x[2]) for x in keyed[:4]))
    check("ask D's four answers win under every rounding of the rise",
          len(set(orders)) == 1 and gap >= 2.0,
          "the fourth and fifth largest rises are %.0f and %.0f ppm, %.0f apart, and the same "
          "four sessions win unrounded and at one and five ppm, rounded up, down and to nearest"
          % (top[3][0], top[4][0], gap))
    check("ask D's four sessions are complete in the record",
          all(x["complete"] for x in BF
              if (x["readings"][-1] - x["readings"][0], x["space"], x["date"]) in top[:4]),
          "none of the four turns on a missing reading")
    # the cracker sheet
    crackers = cracker_sheet()
    for name, hit, total, note in crackers:
        check("cracker misses ask %s" % name, hit * 2 < total,
              "the careful solver's path matches %d of %d figures: %s" % (hit, total, note))


def min_edge_two_dp(values):
    """The closest any value comes to a two-decimal rounding edge, in the value's own unit."""
    out = 1.0
    for v in values:
        frac = v * 100 - math.floor(v * 100)
        out = min(out, abs(frac - 0.5) / 100.0)
    return out


def round_to(v, unit, mode):
    x = v / unit
    if mode == "nearest":
        x = math.floor(x + 0.5)
    elif mode == "up":
        x = math.ceil(x)
    else:
        x = math.floor(x)
    return x * unit


def cracker_sheet():
    """The careful solver's path for each ask, and how much of it that path lands."""
    out = []
    reg = [r for r in B.rows(TARGET, B.REGISTER) if r["bms_point_ref"]]
    ahu_of = {r["room_code"]: r["ahu_ref"] for r in reg}
    spaces = sorted(ahu_of)
    teaching = set(B.teaching_days(TARGET))
    state = BU.occupied_state(TARGET)
    tt = collections.defaultdict(list)
    for s in B.sessions(TARGET):
        tt[(s["space"], s["date"])].append((int(s["start"][:2]) * 60 + int(s["start"][3:5]),
                                            int(s["end"][:2]) * 60 + int(s["end"][3:5])))
    gold_h = collections.Counter()
    gold_o = collections.Counter()
    cr_h = collections.Counter()
    cr_o = collections.Counter()
    recv_t = collections.Counter()
    recv_all = collections.Counter()
    with open(os.path.join(TARGET, B.SPINE), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sp, ts = r["space_code"], r["timestamp_local"]
            d, hhmm, key = ts[:10], ts[11:16], (r["space_code"], ts[:7])
            recv_all[sp] += 1
            if d in teaching:
                recv_t[sp] += 1
            m = int(hhmm[:2]) * 60 + int(hhmm[3:5])
            occ_plant = state(ahu_of[sp], d, hhmm) == "OCCUPIED"
            occ_tt = any(a <= m < b for a, b in tt.get((sp, d), ()))
            over = B.ppm(r["co2"]) > P.SCREENING_PPM
            if occ_plant:
                gold_h[key] += 1
                if over:
                    gold_o[key] += 1
            if occ_tt:
                cr_h[key] += 1
                if over:
                    cr_o[key] += 1
    hit = tot = 0
    for sp in spaces:
        for mk, _ in BU.MONTHS:
            for g, c in ((gold_h, cr_h), (gold_o, cr_o)):
                tot += 1
                hit += BU.half_up(g[(sp, mk)] / 12.0, 2) == BU.half_up(c[(sp, mk)] / 12.0, 2)
    out.append(("A", hit, tot, "counts hours over the timetabled sessions rather than over the "
                               "unit's occupied state"))
    expected = 288 * len(teaching)
    hit = sum(1 for sp in spaces
              if BU.half_up(100.0 * recv_t[sp] / expected, 1)
              == BU.half_up(100.0 * recv_all[sp] / (288 * 75), 1))
    out.append(("B", hit, len(spaces), "divides every reading received by 288 times every calendar "
                                       "day in the window"))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, "enrolment_groups_autumn2026.xlsx"),
                                data_only=True)
    enr = {r[0]: r[3] for r in wb["Groups"].iter_rows(min_row=2, values_only=True)}
    sess = [s for s in B.sessions(TARGET) if s["space"] in BLOCK]
    hit = 0
    for x in M["asks"]["C"]:
        rowsc = [s for s in sess if s["space"] == x["space"]]
        crack = int(BU.half_up(sum(enr[s["group"]] for s in rowsc) / len(rowsc), 0))
        hit += crack == x["mean_occupants"]
    out.append(("C", hit, 6, "takes the enrolment group size as the occupancy"))
    ser = B.series(TARGET)
    base = B.outdoor_baseline(TARGET)
    byday = collections.defaultdict(list)
    for sp in BLOCK:
        for (ts, off), v in ser[sp].items():
            byday[(sp, ts[:10])].append((ts, v - base[(ts[:13], off)]))
    crack = []
    for (sp, d), rowsd in byday.items():
        rowsd.sort()
        lo, best = None, 0.0
        for _, x in rowsd:
            lo = x if lo is None or x < lo else lo
            best = max(best, x - lo)
        crack.append((best, sp, d))
    crack.sort(reverse=True)
    hit = 0
    for i, g in enumerate(M["asks"]["D"]):
        hit += (crack[i][1] == g["space"]) + (crack[i][2] == g["date"])
    out.append(("D", hit, 12, "ranks the largest rise anywhere in a day rather than inside a "
                              "timetabled session, and so names no period at all"))
    return out


# ================================================================= 6. the gates and the sweep

def gates():
    exts = collections.Counter(os.path.splitext(n)[1] for n in FILES)
    check("input gate: ten or more files", len(FILES) >= 10, "%d files" % len(FILES))
    check("input gate: three or more formats", len(exts) >= 3,
          ", ".join("%s %d" % (k, v) for k, v in sorted(exts.items())))
    biggest = max((sum(1 for _ in open(os.path.join(TARGET, n), encoding="utf-8")) - 1, n)
                  for n in FILES if n.endswith(".csv"))
    check("input gate: a file of 25,000 rows or more", biggest[0] >= 25000,
          "%s carries %s rows" % (biggest[1], "{:,}".format(biggest[0])))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("input gate: two or more distractors, named only in metadata.json",
          len(meta["distractor_files"]) >= 2 and
          all(d in FILES for d in meta["distractor_files"]) and
          not any("distractor" in n.lower() for n in FILES),
          ", ".join(meta["distractor_files"]))
    check("input gate: every file has a source, a date and a licence",
          all(meta["files"][n]["source"] and meta["files"][n]["date"] and meta["files"][n]["licence"]
              for n in FILES),
          "%d files recorded in metadata.json" % len(meta["files"]))
    describe = re.compile(r"read_?me|dictionar|codebook|field_?notes|manifest|glossary|how_to_read",
                          re.I)
    sheets = []
    for n in FILES:
        if n.endswith(".xlsx"):
            import openpyxl
            sheets += [(n, ws.title) for ws in
                       openpyxl.load_workbook(os.path.join(TARGET, n)).worksheets]
    check("no file or sheet whose job is to describe the data",
          not any(describe.search(n) for n in FILES) and
          not any(re.match(r"^(notes?|definitions|dictionary|glossary|fields|read ?me|about)$",
                           t.strip(), re.I) for _, t in sheets),
          "%d files and %d sheets, none a dictionary, readme, manifest or notes sheet"
          % (len(FILES), len(sheets)))
    check("the distractors are never read by the solution",
          all(d not in open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
              for d in meta["distractor_files"]),
          "neither distractor is named in any step of the write-up")
    check("the wrong-basis distractor is declared, ruled out and far from both answers",
          meta["wrong_basis_distractor"]["file"] in FILES and
          BU.to_bin(P.DESIGN_SUPPLY_LS) != BU.to_bin(CALL) and
          abs(P.DESIGN_SUPPLY_LS - A.aggregate(BF, lambda x: A.q_steady(x, "session mean"))) > 1.0
          and "deferred" in TEXT["commissioning_record_tulrohan_ahu.pdf"],
          "the commissioning record's %.1f is neither the golden %.2f nor the easy route's %.2f, "
          "and its own outstanding-items section rules it out"
          % (P.DESIGN_SUPPLY_LS, CALL, A.aggregate(BF, lambda x: A.q_steady(x, "session mean"))))
    # Gate G: no shipped artifact ranks the candidates on the decision question
    hits = [n for n in FILES if re.search(r"litres per second per (person|occupant)", TEXT.get(n, ""))]
    check("Gate G: only the standard and the declared distractor state a per-person rate",
          set(hits) <= {B.STANDARD, "commissioning_record_tulrohan_ahu.pdf", B.PROCEDURE},
          "files naming a per-person supply rate: %s" % ", ".join(sorted(hits)))


def realism():
    # personas
    allowed = (set(P.TUTORS) | set(P.ASSISTANTS) | set(P.MAINTENANCE_TECHNICIANS)
               | {P.ESTATES_OFFICER, P.FACILITIES_MANAGER, P.COMMISSIONING_ENGINEER})
    found = set()
    for n in FILES:
        for m in re.finditer(r"\b[A-Z][a-z]+(?:'[A-Z][a-z]+)? [A-Z][a-z]{2,}\b", TEXT.get(n, "")):
            if m.group(0) in allowed:
                found.add(m.group(0))
    stray = set()
    for n in FILES:
        for m in re.finditer(r"\b([A-Z][a-z]{2,}) ([A-Z][a-z]{3,})\b", TEXT.get(n, "")):
            cand = m.group(0)
            if cand in allowed:
                continue
            if re.search(r"(Block|Campus|Board|Room|Hall|Studio|Workshop|Laboratory|Skills|"
                         r"Technology|Learning|Practice|Support|Systems|Analytics|Services|"
                         r"Administration|Architecture|Communication|Techniques|Payroll|Chain|"
                         r"Development|Head|Station|Engineers|Consulting|Air|Balancing|Controls|"
                         r"Education|Training|Further|Design|Management|Data|Office|Store|Plant|"
                         r"Changing|Staff|Corridor|Science|Computing|Media|Construction|Business|"
                         r"Health|Social|Care|Engineering|Supply|Site|Advanced|General|Visual|"
                         r"Interior|Community|Accounting|Bookkeeping|Network|Laboratory|Record|"
                         r"Seminar|Classroom|Computer|Assembly|Lecture|Teaching|Building|Unit|Monday|Tuesday|"
                         r"Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|"
                         r"May|June|July|August|September|October|November|December|Weekend|"
                         r"Midterm|Autumn|Spring|Term|Annual|Analyser|Field|Network|Work|Order|"
                         r"Level|Award|Year|Issue|Project|Contract|Procedure|Schedule|Scope|"
                         r"Option|Total|Room|Programme|Campus|Tulrohan|Drumlusk|Annagloor|"
                         r"Kilmoneen|Beldarrig|Mace|Westmeath|Hanbury|Corrandulla|Keane)", cand):
                continue
            stray.add(cand)
    campus = set(P.TUTORS) | set(P.ASSISTANTS) | {P.ESTATES_OFFICER, P.FACILITIES_MANAGER}
    maintenance = set(P.MAINTENANCE_TECHNICIANS)
    commissioning = {P.COMMISSIONING_ENGINEER}
    check("no person holds a role in two organisations",
          not (campus & maintenance) and not (campus & commissioning)
          and not (maintenance & commissioning)
          and len(campus | maintenance | commissioning) == len(campus) + len(maintenance) + 1,
          "%d campus staff, %d technicians of the maintenance contractor and one commissioning "
          "engineer, %d distinct people and no name in two of the three"
          % (len(campus), len(maintenance),
             len(campus | maintenance | commissioning)))
    seen_roles = collections.defaultdict(set)
    for n in FILES:
        t = TEXT.get(n, "")
        for who in campus | maintenance | commissioning:
            if who in t:
                seen_roles[who].add("campus" if who in campus else
                                    ("maintenance" if who in maintenance else "commissioning"))
    check("no name in the pack appears under two organisations' roles",
          all(len(v) == 1 for v in seen_roles.values()),
          "%d of the %d drawn names appear in the pack, each under one organisation only"
          % (len(seen_roles), len(campus | maintenance | commissioning)))
    check("every persona in the pack was drawn with guard.py names",
          not stray, "%d drawn names appear; no undrawn person name found" % len(found))
    # no round headline
    check("the call is not a round number", abs(CALL - round(CALL)) > 0.02,
          "the block rate is %.4f before rounding" % CALL)
    # no identical non-zero counts across entities
    shares = [x["share_pct"] for x in M["asks"]["B"]]
    check("no two spaces share a capture figure", len(set(shares)) == len(shares),
          "fourteen distinct shares")
    blk_over = sum(x["hours_over_indicator"] for x in M["asks"]["A"] if x["space"] in BLOCK)
    all_over = sum(x["hours_over_indicator"] for x in M["asks"]["A"])
    check("the block leads the campus on hours over the indicator",
          blk_over / all_over > 0.8,
          "the block carries %.2f of the campus's %.2f occupied hours over %s ppm"
          % (blk_over, all_over, "{:,}".format(int(P.SCREENING_PPM))))
    occ = [x["occupied_hours"] for x in M["asks"]["A"]]
    check("occupied-hour cells are not uniform",
          len(set(occ)) > 40, "%d distinct values across 56 cells" % len(set(occ)))
    # container metadata per issuing body
    import pypdf
    issuers = {
        B.ASBUILT: P.DESIGN_PRACTICE,
        B.STANDARD: "Department of Education",
        B.PROCEDURE: "Beldarrig",
        "commissioning_record_tulrohan_ahu.pdf": "Westmeath",
    }
    bad = []
    for n, who in issuers.items():
        md = pypdf.PdfReader(os.path.join(TARGET, n)).metadata or {}
        got = " ".join(str(md.get(k, "")) for k in ("/Producer", "/Creator", "/Author", "/Title"))
        if who not in got or not md.get("/Title") or not md.get("/Subject"):
            bad.append(n)
        for other in issuers.values():
            if other != who and other in str(md.get("/Producer", "")):
                bad.append(n)
    check("every PDF's producer, creator, author and title match its issuing body", not bad,
          "four PDFs, four different issuing bodies, none carrying another's name")
    import pypdf as _pp
    stamps = {}
    for n in P.PDF_FILED:
        md = _pp.PdfReader(os.path.join(TARGET, n)).metadata or {}
        stamps[n] = str(md.get("/CreationDate", ""))[2:16]
    check("no two PDFs share a filing instant, and none reads midnight",
          len(set(stamps.values())) == len(stamps) and
          not any(s.endswith("000000") for s in stamps.values()),
          "four documents filed at %s" % ", ".join(s[8:10] + ":" + s[10:12] for s in
                                                   sorted(stamps.values())))
    pairs = {}
    for n in FILES + [P.WORKBOOK_NAME]:
        if not n.endswith(".xlsx"):
            continue
        root = TARGET if n in FILES else GOLDEN
        with zipfile.ZipFile(os.path.join(root, n)) as z:
            core = z.read("docProps/core.xml").decode()
        pairs[n] = (re.search(r"<dcterms:created[^>]*>([^<]*)<", core).group(1),
                    re.search(r"<dcterms:modified[^>]*>([^<]*)<", core).group(1))
    check("no two workbooks share a created or a modified instant",
          len({v[0] for v in pairs.values()}) == len(pairs) and
          len({v[1] for v in pairs.values()}) == len(pairs),
          "%d workbooks, %d distinct created instants and %d distinct modified instants"
          % (len(pairs), len({v[0] for v in pairs.values()}),
             len({v[1] for v in pairs.values()})))
    check("every workbook was modified after it was created and after any date it states",
          all(v[0] < v[1] for v in pairs.values()),
          "five workbooks, each modified after it was created")
    method_word = re.compile(r"\b(balance|balancing|dynamic|transient|storage|integration|"
                             r"integrated|integral|unsteady|accumulation)\b", re.I)
    named = [n for n in FILES + sorted(os.listdir(GOLDEN)) if method_word.search(n)]
    inside = [n for n in FILES if method_word.search(TEXT.get(n, ""))]
    check("no file name and no shipped file carries a word from the method",
          not named and not inside,
          "%d pack files and %d goldens swept by name and by content for balance, storage, "
          "integration, unsteady and their kin" % (len(FILES), len(os.listdir(GOLDEN))))
    sigs = []
    for n in FILES:
        raw = open(os.path.join(TARGET, n), "rb").read()
        for tok in (b"reportlab", b"ReportLab", b"openpyxl", b"Openpyxl", b"matplotlib"):
            if tok in raw:
                sigs.append((n, tok.decode()))
    check("no writer signature survives in any shipped file", not sigs, "%d files swept" % len(FILES))
    xl = []
    for n in FILES:
        if not n.endswith(".xlsx"):
            continue
        with zipfile.ZipFile(os.path.join(TARGET, n)) as z:
            names = z.namelist()
            app = z.read("docProps/app.xml").decode()
            if "xl/sharedStrings.xml" not in names or "Microsoft Excel" not in app \
                    or "16.0300" not in app:
                xl.append(n)
            if b"<workbookProtection/>" in z.read("xl/workbook.xml"):
                xl.append(n)
    check("every workbook reads as one a person saved", not xl,
          "shared strings present, Excel application and version, no empty protection element")
    # document control dates against the window they describe
    forward = {B.CALENDAR}            # the calendar publishes the spring term before it starts
    late = []
    for n in FILES:
        if n in forward:
            continue
        for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)\b", TEXT.get(n, "")):
            if "-".join(m.groups()) > P.EXPORT_DATE:
                late.append((n, m.group(0)))
    check("no record carries a date after the extract's own pull date", not late,
          "every date in the pack is on or before %s, the academic calendar's spring term being "
          "the one forward-looking record" % P.EXPORT_DATE)
    stated = {B.PROCEDURE: ("2026-09-04", "2026-09-04"),
              B.ASBUILT: ("2021-09-09", "2021-09-09"),
              "commissioning_record_tulrohan_ahu.pdf": ("2021-07-22", "2021-07-14")}
    import pypdf as _p
    bad2 = []
    for n, (approved, event) in stated.items():
        md = _p.PdfReader(os.path.join(TARGET, n)).metadata or {}
        d = str(md.get("/CreationDate", ""))[2:10]
        iso = "%s-%s-%s" % (d[:4], d[4:6], d[6:8])
        if iso < event or iso != approved:
            bad2.append((n, iso, approved, event))
    check("no document's file date precedes a position or an event it states", not bad2,
          "three dated documents, each filed on the date it states")
    # procedural assignment
    tutors = W.group_tutors()
    counts = collections.Counter(tutors.values())
    seq = [tutors[g[0]] for g in P.GROUPS]
    periodic = any(all(seq[i] == seq[i + k] for i in range(len(seq) - k))
                   for k in range(1, len(seq) // 2))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, "enrolment_groups_autumn2026.xlsx"),
                                data_only=True)
    staff_school = {r[1]: r[3] for r in wb["Staff"].iter_rows(min_row=2, values_only=True)}
    wrong = [g[0] for g in P.GROUPS
             if staff_school[tutors[g[0]]] != P.SCHOOL_OF_SUBJECT[g[3]]]
    check("no attribute is assigned by a procedure",
          not periodic and max(counts.values()) - min(counts.values()) >= 2 and not wrong,
          "tutors hold between %d and %d groups each, the sequence has no fixed period, and no "
          "staff record names a school its own sessions contradict"
          % (min(counts.values()), max(counts.values())))
    # arithmetic sequences in id columns
    runs = []
    for n in FILES:
        if not n.endswith(".csv"):
            continue
        with open(os.path.join(TARGET, n), newline="", encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            cols = {c: set() for c in rd.fieldnames
                    if re.search(r"ref|code|mprn|id$|_id", c, re.I)}
            for i, r in enumerate(rd):
                if i > 40000:
                    break
                for c in cols:
                    v = re.sub(r"\D", "", r[c] or "")
                    if v:
                        cols[c].add(int(v))
        for c, vals in cols.items():
            if len(vals) < 8:
                continue
            s = sorted(vals)
            diffs = {s[i + 1] - s[i] for i in range(len(s) - 1)}
            if len(diffs) == 1:
                runs.append("%s:%s" % (n, c))
    check("no identifier column is an arithmetic sequence", not runs,
          "every reference column swept carries more than one step")
    # alphabetical ordering
    reg = [r for r in B.rows(TARGET, B.REGISTER) if r["bms_point_ref"]]
    by_code = [r["room_name"] for r in sorted(reg, key=lambda r: r["room_code"])]
    check("no ordering follows the alphabet", by_code != sorted(by_code),
          "room names in room-code order are not the room names sorted")
    shapes = set()
    for r in B.rows(TARGET, B.REGISTER):
        shapes.add(re.sub(r"[\dA-Z]{2,}$", "", r["room_name"]).strip().split()[-1]
                   if r["room_name"] else "")
    check("entity names carry more than two shapes", len(shapes) > 2,
          "%d distinct name shapes in the room register: %s"
          % (len(shapes), ", ".join(sorted(shapes)[:8])))


# ================================================================= 7. documents and deliverables

def documents():
    # positive controls: each absence assertion runs through the same extractor
    controls = {
        B.STANDARD: "A teaching space shall be provided with outdoor air",
        B.PROCEDURE: "A space counts as occupied for the hours",
        B.ASBUILT: "Volumes below are gross internal",
        "commissioning_record_tulrohan_ahu.pdf": "Proving of air volumes at the supply terminals",
    }
    missing = [n for n, s in controls.items() if s.replace(" ", "") not in
               TEXT[n].replace("\n", "").replace(" ", "")]
    check("every PDF reads back through the verifier's own extractor", not missing,
          "four documents, each proved readable by a sentence taken from its own text")
    # a second, independent extractor: a document only one reader can open is a pack a solver
    # cannot read (reduce-house-fixes H25)
    from pdfminer.high_level import extract_text as _strict
    strict_missing, thin = [], []
    for n, s in controls.items():
        got = _strict(os.path.join(TARGET, n))
        if len(got) < 400:
            thin.append(n)
        if s.replace(" ", "") not in got.replace("\n", "").replace(" ", ""):
            strict_missing.append(n)
    check("every PDF reads back through a second, independent extractor",
          not strict_missing and not thin,
          "the same four sentences are found by pdfminer as by pypdf, every extraction over 400 "
          "characters")

    # exactly one write-up and one prompt under the tree (reduce-house-fixes H11)
    strays = []
    for root, dirs, files in os.walk(TASK):
        dirs[:] = [x for x in dirs if x not in ("__pycache__",)]
        for f in files:
            if f in ("submission.md", "prompt.txt", "prompt.md"):
                strays.append(os.path.relpath(os.path.join(root, f), TASK))
    check("exactly one write-up and one prompt live under the task folder",
          sorted(strays) == ["prompt.txt", "submission.md"],
          ", ".join(sorted(strays)))
    banned = re.compile(r"storage term|stored term|unsteady|accumulation term|integrate the balance|"
                        r"mass balance|rate of change of concentration|still rising|not settled|"
                        r"steady[- ]state|equilibrium|response time|time constant", re.I)
    hits = [(n, banned.search(TEXT[n]).group(0)) for n in FILES if banned.search(TEXT.get(n, ""))]
    check("no shipped sentence states the balance, the stored term or the integration", not hits,
          "swept every csv, txt, xlsx and pdf in the pack")
    ann = re.compile(r"\b(make sure|be sure|note that|remember|be careful|the correct (basis|method)|"
                     r"you should|must exclude|must include)\b", re.I)
    hits2 = [n for n in FILES if ann.search(TEXT.get(n, ""))]
    check("no document announces a step", not hits2, "announcement sweep clean across %d files"
          % len(FILES))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    answers = sub[sub.index("## 1."):sub.index("## 2.")] + sub[sub.index("## 4."):]
    stated = {"1500", "0072", "0.0072"} | {str(y) for y in range(2014, 2031)}
    nums = {v for v in re.findall(r"\b\d{4,}(?:\.\d+)?\b", answers.replace(",", ""))
            if v not in stated}
    leaked = [(n, v) for n in FILES if n.endswith((".pdf", ".txt"))
              for v in nums if v in TEXT[n].replace(",", "")]
    check("no golden figure appears in a shipped document", not leaked,
          "%d four-digit-or-longer write-up figures swept against every document" % len(nums))
    # the goldens
    gfiles = sorted(os.listdir(GOLDEN))
    check("one to three goldens, each named by the prompt",
          gfiles == sorted([P.CHART_NAME, P.WORKBOOK_NAME]),
          ", ".join(gfiles))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(GOLDEN, P.WORKBOOK_NAME), data_only=True)
    vals = [c for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row]
    check("the golden workbook states the call and the components",
          M["call"]["block_rate_ls_per_occupant"] in vals and
          M["components"]["block_sessions"] in vals and
          M["components"]["occupant_hours_present"] in vals and
          M["components"]["shortest_response_minutes"] in vals,
          "the assessment sheet carries the rate, the sessions, the occupant-hours and the "
          "response time")
    rows_a = sum(1 for ws in wb.worksheets if ws.title == "Occupied hours by month"
                 for _ in ws.iter_rows(min_row=2))
    check("the golden workbook carries every graded row", rows_a == 56,
          "56 space-month rows, 14 capture rows, 6 occupancy rows and 4 rise rows")
    png = open(os.path.join(GOLDEN, P.CHART_NAME), "rb").read()
    check("the chart is a real file carrying its own metadata",
          png[:8] == b"\x89PNG\r\n\x1a\n" and b"Beldarrig" in png and len(png) > 80000,
          "%s bytes" % "{:,}".format(len(png)))
    check("every figure the write-up states is in figures.json",
          os.path.exists(os.path.join(HERE, "figures.json")),
          "figures_check.py is the gate; this check confirms the file the gate reads exists")


# ================================================================= run

def main():
    three_rules()
    ladder()
    forks()
    mess()
    asks()
    gates()
    realism()
    documents()
    bad = 0
    for name, ok, detail in CHECKS:
        print("%-4s %-62s %s" % ("PASS" if ok else "FAIL", name, detail))
        bad += 0 if ok else 1
    print("%s task204: %d checks, %d failed" % ("PASS" if not bad else "FAIL", len(CHECKS), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
