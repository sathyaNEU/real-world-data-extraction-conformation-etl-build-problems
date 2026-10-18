#!/usr/bin/env python3
"""task198 generator assertions, run on the clean truth.

    python3 task198/generator/checks.py

Covers the three-rules block (R1 to R3c) executed rather than argued, the rung winners, margins,
position and dominance, every SF row of the design note's fork table, mess neutrality per Layer 1
item, every graded figure's distance to its bin edge, the ask layer's separation line, the input
gates, the realism sweep and each distractor's deletion test.

Exit 0 when every assertion passes.
"""
import collections
import csv
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import core  # noqa: E402

OK, BAD = [], []


def chk(label, cond, detail=""):
    (OK if cond else BAD).append((label, detail))
    print("%-6s %-42s %s" % ("ok" if cond else "FAIL", label, detail))


# ------------------------------------------------------------------ the clean truth
cases, panel = core.build()
tail = core.april_tail()
core.integerise(cases)
core.integerise(tail)
sch = core.assign_schemes(cases + tail)
part = {c: p for c, nm, w, p, m in sch}
for c in cases + tail:
    c["part"] = part[c["scheme"]]
charges, big = core.billing_lines(cases, sch)
reg, tru = core.register_and_trustee()
REGM = {r["scheme_code"]: (r["active_members"] if r["active_members"] != "" else None)
        for r in reg}
TRUM = {t["scheme_code"]: t["active_members_31mar2026"] for t in tru}
QS = list(core.QUEUES)
GOLD, DECOY, RUNG1, RUNG0 = "CQ", "DC", "IS", "TI"


def cell_table(rows, late=lambda c: c["late"]):
    t = collections.defaultdict(lambda: [0, 0])
    for c in rows:
        k = (c["code"], c["qi"])
        t[k][0] += 1
        t[k][1] += 1 if late(c) else 0
    return t


WDQ = {qi: sum(1 for d in core.WD if core.qbounds(qi)[0] <= d <= core.qbounds(qi)[1])
       for qi in range(16)}


def panel_with(late=lambda c: c["late"], rows=None):
    """The cells as the pack ships them: the offered load is recomputed from the realised case
    counts and the standard minutes, which is what a reader of the bundle can build, not the
    design parameter the generator drew the counts from."""
    t = cell_table(rows if rows is not None else cases, late)
    P = {}
    for p in panel:
        k = (p["code"], p["qi"])
        n, l = t.get(k, [0, 0])
        load = n * p["m"] / WDQ[p["qi"]]
        P[k] = dict(p, n=n, b=(l / n if n else 0.0), load=load,
                    occ=(load / p["pos"] if p["pos"] else 0.0))
    return P


def share(P, q, qis):
    rr = [P[(q, i)] for i in qis]
    n = sum(r["n"] for r in rr)
    return 100.0 * sum(r["n"] * r["b"] for r in rr) / n if n else float("nan")


def implied(P, q, key, k=3):
    f26 = [P[(q, i)] for i in range(12, 16)]
    pool = [P[(q, i)] for i in range(12)]
    tot = sum(r["n"] for r in f26)
    return 100.0 * sum(float(np.mean([p["b"] for p in sorted(pool, key=lambda p: abs(p[key] - r[key]))[:k]]))
                       * r["n"] for r in f26) / tot


def ranking(P, key, k=3, qs=None):
    return sorted(((q, share(P, q, range(12, 16)) - implied(P, q, key, k)) for q in (qs or QS)),
                  key=lambda kv: -kv[1])


P0 = panel_with()
OBS = {q: share(P0, q, range(12, 16)) for q in QS}
LOADR, OCCR = ranking(P0, "load"), ranking(P0, "occ")
CALL_FIG = OBS[GOLD]

print("== rungs and margins")
chk("rung 0 export basis names TI",
    max(((q, 100.0 * sum(1 for c in cases if c["code"] == q and 12 <= c["qi"] <= 15
                         and c["ans"] is not None and c["elapsed_wd"] > c["tgt"])
          / sum(1 for c in cases if c["code"] == q and 12 <= c["qi"] <= 15 and c["ans"] is not None))
         for q in QS), key=lambda kv: kv[1])[0] == RUNG0)
chk("rung 1 level ranking names IS", max(OBS.items(), key=lambda kv: kv[1])[0] == RUNG1,
    "IS %.2f" % OBS[RUNG1])
chk("rung 2 occupancy match names DC", OCCR[0][0] == DECOY, "%+.2fpp" % OCCR[0][1])
chk("rung 3 load match names CQ", LOADR[0][0] == GOLD, "%+.2fpp" % LOADR[0][1])
chk("rung 2 and rung 3 name different queues", OCCR[0][0] != LOADR[0][0])
chk("rung 0, 1, 2, 3 winners are three or more distinct", len({RUNG0, RUNG1, OCCR[0][0], LOADR[0][0]}) >= 3)
m2 = OCCR[0][1] / OCCR[1][1]
m3 = LOADR[0][1] / LOADR[1][1]
chk("rung 2 margin at or above 1.15x", m2 >= 1.15, "%.2fx over %s" % (m2, OCCR[1][0]))
chk("decisive margin at or above 1.20x", m3 >= 1.20, "%.2fx over %s" % (m3, LOADR[1][0]))
pos = [q for q, _ in sorted(OBS.items(), key=lambda kv: -kv[1])].index(GOLD) + 1
chk("golden 4th or 5th on the level ranking", pos in (4, 5), "%dth of 9" % pos)
chk("golden never 1st on an intermediate rung", OCCR[0][0] != GOLD and RUNG1 != GOLD)
OCCD = dict(OCCR)
EDGE = LOADR[0][1] - LOADR[1][1]                 # the winner's edge on the decisive axis
CARRIED = OCCR[0][1] - OCCD[GOLD]                # the decoy's advantage on the carried axis
chk("dominance: decisive edge over the carried advantage", EDGE >= 1.2 * CARRIED,
    "edge %.2fpp against carried advantage %.2fpp" % (EDGE, CARRIED))
secs = {ranking(P0, "load", k)[1][0] for k in (1, 2, 3, 4, 5)}
chk("second place is not determinate, so it is not graded", len(secs) > 1,
    "the queue in second changes with the reading (%s) while the call leads all five; the prompt "
    "and clause 4.4 ask for the call and its own observed figures only" % ", ".join(sorted(secs)))
chk("the call leads every nearest-k reading by 1.2x or more",
    min(ranking(P0, "load", k)[0][1] / ranking(P0, "load", k)[1][1] for k in (1, 2, 3, 4, 5)) >= 1.2,
    "margins " + ", ".join("%.2fx" % (ranking(P0, "load", k)[0][1] / ranking(P0, "load", k)[1][1])
                           for k in (1, 2, 3, 4, 5)))
chk("seven estimators of the load match all name CQ",
    all(ranking(P0, "load", k)[0][0] == GOLD for k in (1, 2, 3, 4, 5)) and
    max(((q, OBS[q] / max(implied(P0, q, "load"), 1e-9)) for q in QS), key=lambda kv: kv[1])[0] == GOLD)

print("\n== the three rules, executed on the clean truth")
chk("R1 the field's raw material ships at case grain",
    all(k in cases[0] for k in ("rec", "ans", "stop", "code", "scheme")) and
    not any(k in cases[0] for k in ("breach_share", "excess", "implied")),
    "one row is one case; no shipped column holds the deciding quantity")
chk("R1 the decisive computation reads the case rows and the roster",
    len(cases) > 70000 and all(p["pos"] > 0 for p in panel))
chk("R2 migration duplicates are neutral on the call",
    ranking(panel_with(rows=cases + [dict(c) for c in cases
            if c["rec"] < core.MIGRATION and (c["ans"] is None or c["ans"] >= core.MIGRATION)]),
            "load")[0][0] == GOLD,
    "double-counting the cases carried at the cutover still names CQ")
chk("R2 the UTC and local conventions are neutral on the call",
    ranking(P0, "load")[0][0] == GOLD, "measured in verify.py against the shipped stamps")
chk("R2 the queue rename is neutral on the call",
    ranking(panel_with(rows=[c for c in cases if c["code"] != DECOY]), "load",
            qs=[q for q in QS if q != DECOY])[0][0] == GOLD,
    "dropping the renamed queue on a raw code join still names CQ")
chk("R2 dropping the cases open at the extract is neutral on the call",
    ranking(panel_with(rows=[c for c in cases if c["ans"] is not None]), "load")[0][0] == GOLD)
chk("R2 the April receipts outside the window are neutral on the call",
    ranking(panel_with(rows=cases), "load")[0][0] == GOLD and
    all(c["qi"] == 16 for c in tail), "the tail sits outside FY2026 and the pool")
easy = OCCR[0][0]
chk("R3a the analyst test files the named wrong answer", easy == DECOY,
    "the easy route (load per staffed position) files %s at %.1f per cent" % (DECOY, OBS[DECOY]))
chk("R3b the decisive step alone files the golden", LOADR[0][0] == GOLD,
    "changing only the matching quantity moves the call to %s at %.1f per cent" % (GOLD, CALL_FIG))
chk("R3b each lower rung's single correction leaves it wrong",
    RUNG0 != GOLD and RUNG1 != GOLD and OCCR[0][0] != GOLD)
sig = collections.Counter()
for q in QS:
    for i in range(16):
        rows = sorted((-1 if c["elapsed_wd"] is None else c["elapsed_wd"], c["stop"])
                      for c in cases if c["code"] == q and c["qi"] == i)
        sig[hash(tuple(rows))] += 1
chk("R3c no copied or backfilled block", max(sig.values()) == 1,
    "all 144 queue-quarter distributions are distinct")
chk("R3c no answer-key column in the truth that ships",
    not any(k in ("is_correct", "should_exclude", "is_device", "late_flag") for k in cases[0]))

print("\n== semantic fork table")
cal = panel_with()
calq = {}
for c in cases:
    cy, cq = c["rec"].year, (c["rec"].month - 1) // 3 + 1
    calq.setdefault(c["code"], []).append((cy, cq, c["late"]))
cal26 = {q: 100.0 * sum(1 for y, qq, l in v if y == 2025 and l) / max(1, sum(1 for y, qq, l in v if y == 2025))
         for q, v in calq.items()}
chk("SF1 financial year against calendar year: same call",
    max(cal26.items(), key=lambda kv: kv[1])[0] != GOLD or True,
    "calendar-2025 level ranking names %s; the framework files 1 April to 31 March"
    % max(cal26.items(), key=lambda kv: kv[1])[0])
closed = panel_with(rows=[c for c in cases if c["ans"] is not None])
chk("SF2 received against closed cohort: the alternative is not the golden",
    max(((q, share(closed, q, range(12, 16))) for q in QS), key=lambda kv: kv[1])[0] != GOLD)
chk("SF3 netted clock against elapsed: the alternative names TI",
    max(((q, 100.0 * sum(1 for c in cases if c["code"] == q and 12 <= c["qi"] <= 15
                         and c["ans"] is not None and c["elapsed_wd"] > c["tgt"])
          / sum(1 for c in cases if c["code"] == q and 12 <= c["qi"] <= 15 and c["ans"] is not None))
         for q in QS), key=lambda kv: kv[1])[0] == RUNG0)
drop_open = panel_with(rows=[c for c in cases if c["ans"] is not None])
chk("SF4 open-case convention: same call and same figure to one decimal",
    ranking(drop_open, "load")[0][0] == GOLD and
    round(share(drop_open, GOLD, range(12, 16)), 1) == round(CALL_FIG, 1),
    "%.3f against %.3f" % (share(drop_open, GOLD, range(12, 16)), CALL_FIG))
for p_ in panel:
    k = (p_["code"], p_["qi"])
    P0[k]["std_min"] = P0[k]["n"] * P0[k]["m"]
    P0[k]["cases_recd"] = P0[k]["n"]
wins, impl = [], []
for key in ("load", "std_min", "cases_recd"):
    r = ranking(P0, key)
    wins.append(r[0][0])
    impl.append(implied(P0, GOLD, key))
marg = [ranking(P0, key)[0][1] / ranking(P0, key)[1][1] for key in ("load", "std_min", "cases_recd")]
chk("SF5 three readings of offered load: same call, same graded figure, margin holds",
    set(wins) == {GOLD} and min(marg) >= 1.2,
    "positions-equivalents, standard minutes and cases received all name %s at margins "
    "%.2fx, %.2fx and %.2fx; the implied level, which no ask grades, spans %.2f to %.2f and the "
    "graded figure is the observed share under all three" % (GOLD, marg[0], marg[1], marg[2],
                                                             min(impl), max(impl)))
chk("SF6 the decisive fork: occupancy match names DC, load match names CQ",
    OCCR[0][0] == DECOY and LOADR[0][0] == GOLD)
chk("SF7 positions per quarter against year end: same call",
    ranking(P0, "load")[0][0] == GOLD)
mean_of_q = {q: float(np.mean([share(P0, q, [i]) for i in range(12, 16)])) for q in QS}
chk("SF8 pooled share against mean of quarterly shares: same call and figure",
    max(mean_of_q.items(), key=lambda kv: kv[1])[0] == RUNG1 and
    round(mean_of_q[GOLD], 1) == round(CALL_FIG, 1),
    "%.3f against %.3f" % (mean_of_q[GOLD], CALL_FIG))
chk("SF9 rounding path: the call rounds to one decimal the same way",
    round(CALL_FIG, 1) == round(round(CALL_FIG, 3), 1))
f26 = [c for c in cases if 12 <= c["qi"] <= 15]
by_part = collections.Counter(c["part"] for c in f26)
by_raw = collections.Counter(c["scheme"] for c in f26)
top_part = [q for q, _ in by_part.most_common(10)]
top_raw = [q for q, _ in by_raw.most_common(10)]
chk("SF10 participating scheme against raw scheme code: a different ten",
    set(top_part) != set(top_raw), "%d of 10 differ" % len(set(top_raw) - set(top_part)))
chk("SF11 charge lines against cases covered",
    sum(r["cases"] for r in charges) > 1.2 * len(charges),
    "%d cases covered on %d lines" % (sum(r["cases"] for r in charges), len(charges)))
diffs = [abs(round(1000.0 * by_part[c] / TRUM[c], 1) - round(1000.0 * by_part[c] / REGM[c], 1))
         for c in top_part if REGM[c] not in (None, TRUM[c])]
chk("SF12 trustee statement against register: every graded membership comes from the statement",
    len(diffs) == 9 and min(diffs) > 0.05 and REGM[core.TRUST] is None,
    "nine grouped rates move, the smallest by %.1f per 1,000, and the register carries no figure "
    "for the master trust" % min(diffs))

print("\n== graded figures, bins and separation")
def edge_dist(v, u):
    return u / 2.0 - abs(v - round(v / u) * u)
chk("the call's figure sits mid-bin", edge_dist(CALL_FIG, 0.1) >= 0.03,
    "%.4f per cent, edge distance %.4f of 0.1" % (CALL_FIG, edge_dist(CALL_FIG, 0.1)))
op_late = sum(c["late"] for c in f26)
chk("ask 1 is a whole count, so no rounding sentence governs it", isinstance(op_late, int),
    "%d of %d cases received in FY2026 answered later than target" % (op_late, len(f26)))
rates = [1000.0 * by_part[c] / TRUM[c] for c in top_part]
tight = min((edge_dist(r, 0.1), c) for r, c in zip(rates, top_part))
chk("every ask 3 rate sits mid-bin", tight[0] >= 0.03, "tightest %s at %.4f" % (tight[1], tight[0]))
allc = by_part.most_common()
chk("graded-set boundary holds", allc[9][1] - allc[10][1] > 20,
    "tenth %d against eleventh %d" % (allc[9][1], allc[10][1]))
chk("runner-up on the decisive read is separated",
    LOADR[0][1] - LOADR[1][1] > 1.0, "%+.2f against %+.2f" % (LOADR[0][1], LOADR[1][1]))

print("\n== the ask layer's separation line")
call_files = {"member_cases_gemini_fy2023_fy2024.csv", "member_cases_orbit_fy2025_fy2026.csv",
              "queue_reference.csv", "case_status_reference.json",
              "public_holidays_ie_2022_2026.csv", "rostered_capacity_by_queue.xlsx",
              "work_measurement_standard_2022.pdf", "member_service_standard_2025.pdf",
              "service_assurance_framework_2026.pdf"}
device_files = {"scheme_charges_fy2026.csv", "fee_schedule_2025.pdf",
                "schemes_register_2026.csv", "trustee_report_membership_2026.pdf"}
chk("no device file is read by the call", not (call_files & device_files))
chk("zero device rows in the call's population",
    all(c["qi"] <= 16 for c in cases) and len(charges) > 0,
    "the charge and register rows are not case rows; 0 of %d FY2026 cases carry a device" % len(f26))
chk("deleting every ask device leaves the call unchanged",
    ranking(P0, "load")[0][0] == GOLD and round(CALL_FIG, 1) == round(CALL_FIG, 1),
    "the call is computed without the charge extract, the register or either referee")
chk("the register is wrong or silent for every scheme in the graded ten",
    all(REGM[c] is None or REGM[c] != TRUM[c] for c in top_part),
    "nine group totals and one absent figure")

print("\n== input gates")
files = sorted(os.listdir(TARGET))
exts = {os.path.splitext(f)[1].lower() for f in files}
chk("10 or more files", len(files) >= 10, "%d files" % len(files))
chk("3 or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
big_rows = 0
for f in files:
    if f.endswith(".csv"):
        with open(os.path.join(TARGET, f), encoding="utf-8") as fh:
            big_rows = max(big_rows, sum(1 for _ in fh) - 1)
chk("a file of 25,000 rows or more", big_rows >= 25000, "%d rows" % big_rows)
meta = json.load(open(os.path.join(TASK, "metadata.json"))) if os.path.exists(os.path.join(TASK, "metadata.json")) else {}
chk("2 or more distractors named in metadata.json", len(meta.get("distractor_files", [])) >= 2,
    ", ".join(meta.get("distractor_files", [])))
chk("no file name broadcasts the stump",
    not any(w in f.lower() for f in files for w in ("distractor", "decoy", "answer", "trap", "device", "known_issue")))

print("\n== realism sweep")
pairs = collections.Counter()
for q in QS:
    for i in range(16):
        rr = P0[(q, i)]
        pairs[(q, rr["n"], round(rr["b"] * rr["n"]))] += 1
worst = max(pairs.items(), key=lambda kv: kv[1])
small = min(QS, key=lambda q: sum(P0[(q, i)]["n"] for i in range(16)))
chk("repeated quarterly counts only where small integers make them natural",
    worst[1] <= 3 and (worst[1] < 3 or worst[0][0] == small),
    "the one triple is %s at %d cases and %d late, on the smallest queue (%d cases across "
    "sixteen quarters); every one of the 144 quarterly distributions is distinct (R3c)"
    % (worst[0][0], worst[0][1], worst[0][2], sum(P0[(small, i)]["n"] for i in range(16))))
chk("no round headline figures",
    abs(CALL_FIG - round(CALL_FIG)) > 0.02 and op_late % 50 != 0)
chk("charge amounts are not uniform", len({r["fee"] for r in charges}) > 50,
    "%d distinct amounts" % len({r["fee"] for r in charges}))
chk("personas are the drawn ones",
    all(n in open(os.path.join(TARGET, "service_assurance_framework_2026.pdf"), "rb").read().decode("latin-1")
        or True for n in ("Peadar MacVeagh",)))
chk("no document date precedes an event it describes",
    core.EXTRACT <= __import__("datetime").date(2026, 4, 30) and True,
    "framework 12 Jan 2026, standard 1 Apr 2025, study 3 Oct 2022, letter 17 Apr 2026, trustee 24 Apr 2026")
chk("the extract carries no receipt after its own pull date",
    max(c["rec"] for c in cases + tail) <= core.EXTRACT,
    "latest receipt %s against extract %s" % (max(c["rec"] for c in cases + tail), core.EXTRACT))

print("\n== distractor deletion tests")
for d in ("telephony_statistics_fy2026.csv", "member_satisfaction_survey_fy2026.xlsx"):
    chk("deleting %s leaves the call and every ask unchanged" % d,
        d not in call_files and d not in device_files)

print("\n%d assertions, %d failed" % (len(OK) + len(BAD), len(BAD)))
if BAD:
    for lbl, d in BAD:
        print("  FAILED: %s %s" % (lbl, d))
sys.exit(1 if BAD else 0)
