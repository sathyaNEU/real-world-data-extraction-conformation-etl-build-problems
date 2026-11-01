"""task145 architecture 2: the generator's assertions on the cut pack. The three rules executed (R1 to R3c), the call
and its margins, the ladder's rungs, the decisive route's family of defensible variants and the routes the data
refute, every semantic fork (SF1 to SF12) closed, the asks' devices and the separation from the call, the input gates
and the realism sweep.

    python3 task145/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import ceiling as CE  # noqa: E402
import params as P  # noqa: E402
import world as WD  # noqa: E402

FAILS = []
N = [0]


def check(label, ok, detail=""):
    N[0] += 1
    print(("PASS  " if ok else "FAIL  ") + label + (("  [" + str(detail) + "]") if detail and not ok else ""))
    if not ok:
        FAILS.append(label)


def rows(name):
    with open(os.path.join(TARGET, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdf_text(name):
    return subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, name), "-"], capture_output=True,
                          text=True).stdout


def main():
    t = TARGET
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(t))
    S = A.solve(t)
    R = A.rungs(t, S)
    V, X, L = A.family(t, S)
    g = S["expected"]
    T1, T2 = P.TIERS[0][1], P.TIERS[1][1]

    # ---- input gates
    check("gate: ten or more files", len(files) >= 10, len(files))
    check("gate: three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(t, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gate: a file of 25,000 or more rows", big >= 25000, big)
    check("gate: two or more distractors named in metadata.json", len(meta["distractors"]) >= 2 and
          all(d in files for d in meta["distractors"]))
    check("gate: no distractor's file name says it is one", not any(re.search("distract|decoy|unused", f) for f in files))
    check("gate: every file carries source, date and licence", all(
        set(meta["files"][f]) >= {"source", "date", "license"} for f in files) and set(meta["files"]) == set(files))
    src = open(os.path.join(HERE, "analysis.py")).read()
    check("gate: the golden never reads a distractor", not any(d in src for d in meta["distractors"]))

    # ---- the three rules, executed
    ab_cols = rows("attendance_absences_2024-25_to_2026-27.csv")[0].keys()
    check("R1 the field's raw material ships: one row per student, school and day absent, no run or rate column",
          set(ab_cols) == {"local_id", "school_number", "absence_date", "portion", "code", "recorded_utc"})
    check("R1 the decisive computation reads the absence rows against the calendars",
          S["with_run"] > 0 and A.solve(t, run_min=50)["with_run"] == 0)
    check("R2 legacy minutes layout (2023-24): read on the half-day rule, the call holds without it",
          A.tier_for(L["no half-day rule"]) == S["tier"])
    check("R2 exits entered after the next school's entry: the call's figure is unmoved",
          abs(L["no overlap rule"] - g) < 1e-9, L["no overlap rule"])
    check("R2 records opened without a state id: the call holds unlinked", A.tier_for(
        L["records without a state id left unlinked"]) == S["tier"])
    check("R2 exit codes renamed in July 2024: every legacy and current exit code is in the code reference",
          {r["exit_code"] for r in rows("enrollment_records_2023-24_to_2026-27.csv") if r["exit_code"]} <=
          {r["code"] for r in rows("sis_code_reference.csv") if r["code_table"] == "exit"})
    check("R2 transfers checked against the records requests: the call holds on every reading",
          all(A.tier_for(L[k]) == S["tier"] for k in ("only unconfirmed transfers checked",
                                                      "no transfer counted as leaving",
                                                      "every unconfirmed transfer counted as leaving")))
    check("R2 suspension days posted only in part: the call holds with them added or dropped",
          A.tier_for(V["suspension days from the behaviour file added"]) == S["tier"] and
          A.tier_for(V["suspension rows dropped"]) == S["tier"])
    check("R2 amended suspensions in the behaviour log: the call never reads them",
          abs(L["amended suspensions not collapsed"] - g) < 1e-9)
    ew = {k: v for k, v in R.items() if k[:2] in ("R0", "R1", "R2")}
    check("R3a the analyst test: every early-warning route on the share of days missed files Tier 1",
          all(A.tier_for(v) == "Tier 1" for v in ew.values()), {k[:3]: round(v, 1) for k, v in ew.items()})
    check("R3a with margin: the highest early-warning route sits 15 per cent or more under Tier 1's seats",
          max(ew.values()) * 1.15 <= T1, round(max(ew.values()), 1))
    r1b = R["R1b early-warning cells (chronic absence, F grades)"]
    check("R3b the decisive step alone: the same cells on runs instead of chronic absence file Tier 2",
          A.tier_for(r1b) == "Tier 1" and S["tier"] == "Tier 2")
    check("R3b each lower rung's single correction stays on Tier 1 (severity bins, the logistic, one closed year)",
          all(A.tier_for(R[k]) == "Tier 1" for k in R if k.startswith(("R1c", "R2", "R2b", "R2c"))))
    eml = open(os.path.join(t, "bridge_seats_for_spring.eml"), encoding="utf-8").read().split("\n\n", 1)[1]
    check("R3c no plant: the request carries no figure and no belief about the answer",
          not re.search(r"\d{2,}", eml.split("--")[0].replace("29th", "").replace("31st", "")) and
          "tier" in eml and "expect" not in eml)
    docs = "".join(pdf_text(f) for f in files if f.endswith(".pdf"))
    check("R3c no plant: no shipped document carries a forecast of leavers or a recommended tier",
          not re.search(r"expect\w*\s+(about\s+)?\d+", docs) and "recommend" not in docs.lower())
    ab = A.absences(t)
    seqs = Counter(tuple(sorted(v)) for k, v in ab.items() if k[0] == P.CUR and len(v) >= 8)
    check("R3c no plant: no copied block of absence days across students", max(seqs.values()) <= 2, seqs.most_common(1))

    # ---- the call and its margins
    check("call: %s" % S["tier"], S["tier"] == "Tier 2" == fig["call"]["tier"])
    check("call: no cell of the decisive model is empty for a student on roll", S["missing"] == 0)
    check("call: expected leavers 15 per cent or more above Tier 1's seats", g >= 1.15 * T1, round(g, 1))
    check("call: expected leavers 15 per cent or more under Tier 2's seats", g * 1.15 <= T2, round(g, 1))
    check("call: the expected number is not near a whole-student half", abs(g - int(g) - 0.5) > 0.05, g)
    sd = sum(p * (1 - p) for p in [
        S["num"].get(A.golden_key(S["feat"][(P.CUR, k)]), 0) / S["den"][A.golden_key(S["feat"][(P.CUR, k)])]
        for k in S["cur"]]) ** 0.5
    check("call: a 90th-percentile reading of the leavers lands the same tier", A.tier_for(g + 1.2816 * sd) ==
          S["tier"], round(g + 1.2816 * sd, 1))
    check("call: the logistic on runs lands the golden's tier", A.tier_for(
        R["R3b logistic on runs, F grades and incidents"]) == S["tier"])

    # ---- the family of defensible variants, and what the data refute
    for k, v in V.items():
        check("family: %s files %s" % (k, S["tier"]), A.tier_for(v) == S["tier"], round(v, 1))
    check("family: no variant within 8 per cent of a tier edge", all(v >= 1.08 * T1 and v * 1.08 <= T2
                                                                    for v in V.values()),
          (round(min(V.values()), 1), round(max(V.values()), 1)))
    lb = A.leave_by_longest(S)
    rate = lambda ks: 100.0 * sum(lb[k][0] for k in ks) / sum(lb[k][1] for k in ks)
    short, long5 = rate(["3", "4"]), rate(["5-9"])
    base = rate(["0", "1", "2"])
    check("refuted: a longest absence of three or four days carries under twice the scattered rate",
          short < 2 * base, (round(short, 2), round(base, 2)))
    check("refuted: a longest absence of five to nine days carries ten times the scattered rate or more",
          long5 >= 10 * base, (round(long5, 2), round(base, 2)))
    check("refuted: ten days or more carries no lower rate than five to nine",
          rate(["10+"]) >= 0.85 * long5, (round(rate(["10+"]), 1), round(long5, 1)))
    for k, v in X.items():
        check("refuted route priced: %s" % k.split(" (")[0], v > 0, round(v, 1))

    # ---- the semantic forks
    recs = S["recs"]
    jan = [r for r in recs if r["entry"].month in (1, 2, 3, 4, 5) and r["entry_code"] in ("E1", "E2")]
    check("SF1 the roll: no closed spring had a student entering after the fall, so the roll at the extract is the "
          "semester's", not jan, len(jan))
    check("SF1 the roll: every student on roll has a fall record", all((P.CUR, k) in S["feat"] for k in S["cur"]))
    check("SF2 leaving per JF-7 section 3: checking only the unconfirmed transfers gives the same leavers",
          abs(L["only unconfirmed transfers checked"] - g) < 1e-9)
    req = A.requests(t)
    gaps = []
    for r in recs:
        if r["exit_code"] in A.TRANSFER and r["exit"]:
            for gd in req.get((r["last_name"].lower(), r["first_name"].lower(), r["birth_date"]), []):
                gaps.append((gd - r["exit"]).days)
    check("SF10 the 45-day records test: no request lands within three days of the line", not any(
        42 <= x <= 48 for x in gaps), sorted(x for x in gaps if 40 <= x <= 50))
    check("SF3 legacy codes: W3, W5, W9 and WT appear only in 2023-24", all(
        r["school_year"] == "2023-24" for r in recs if r["exit_code"].startswith("W")))
    check("SF4 a day absent per JH-R section 1: the call is the same with or without the half-day rule",
          abs(L["no half-day rule"] - g) < 1e-9)
    check("SF5 suspension days as days absent: same tier added from the behaviour log or dropped",
          A.tier_for(V["suspension days from the behaviour file added"]) == A.tier_for(V["suspension rows dropped"])
          == S["tier"])
    check("SF6 'expected to leave': the expectation and its 90th percentile give one tier (see the call block)",
          A.tier_for(g) == A.tier_for(g + 1.2816 * sd))
    ends = [r["exit"] for r in recs if r["exit"] and r["school_year"] in P.HIST and r["exit"] > A.YEARS[
        r["school_year"]][4]]
    check("SF7 the window to 30 June: no closed-year exit falls after the last instructional day", not ends,
          len(ends))
    moves = [r for r in recs if r["exit_code"] in ("TN", "W1")]
    check("SF8 a move between the network's schools: every TN exit is followed by a record at another network school",
          all(any(x["key"] == r["key"] and x["school_year"] == r["school_year"] and x["school"] != r["school"] and
                  x["entry"] >= r["entry"] for x in recs) for r in moves if r["exit_code"] == "TN"))
    check("SF9 a student read on the school they attended each day: the call is the same on the records as filed",
          abs(L["no overlap rule"] - g) < 1e-9)
    check("SF11 the tier rule on the unrounded and the rounded number agree", A.tier_for(g) == A.tier_for(round(g)))
    check("SF12 graduates are completers: no GR or W0 exit is counted as leaving", not any(
        A.is_leaver(r, req) for r in recs if r["exit_code"] in ("GR", "W0")))

    # ---- the asks: devices, fairness and separation
    a, b = A.ask_a(t, S), A.ask_b(t, S)
    check("ask A: sixteen cells, none on an exact half at one decimal", len(a) == 16 and all(
        abs(v[0] * 10 - int(v[0] * 10) - 0.5) > 1e-6 for v in a.values()))
    check("ask A: every cell from 100 or more students", all(v[2] >= 100 for v in a.values()), min(
        v[2] for v in a.values()))
    check("ask B: twenty cells, no two schools' months identical", len(b) == 20 and len(
        {tuple(b[(s, m)] for m in A.MONTHS) for s in P.SCHOOLS}) == 4)
    C = CE.main(t)
    check("asks: the cracker misses ask A (records as filed)", C["ca"] <= 5, C["ca"])
    check("asks: the cracker misses ask B (an amendment under a re-coded behaviour kept)", C["cb"] <= 4, C["cb"])
    check("asks: pair ceiling at or under 60", C["pair"] <= 60, round(C["pair"], 1))
    over = A.ask_a(t, S, overlap=False)
    moved = sum(1 for k in a if round(over[k][0], 1) != round(a[k][0], 1))
    check("ask A device: the records as filed move ten or more cells", moved >= 10, moved)
    nod = A.ask_b(t, S, dedupe=False)
    check("ask B device: every incident row kept moves eighteen or more cells", sum(
        1 for k in b if nod[k] != b[k]) >= 18)
    bat = A.ask_b(t, S, dedupe="battery")
    check("ask B device: the battery's same-behaviour dedupe still moves fifteen or more cells", sum(
        1 for k in b if bat[k] != b[k]) >= 15)
    inc = rows("behavior_incidents_2023-24_to_2026-27.csv")
    pairs = defaultdict(list)
    for r in inc:
        if r["action"] == "OSS":
            pairs[(r["local_id"], r["action_start"])].append(r)
    amended = [v for v in pairs.values() if len(v) > 1]
    check("ask B fair: an amended suspension's two rows share the student and start, the later carrying fewer days",
          amended and all(len(v) == 2 and int(max(v, key=lambda x: x["entered_utc"])["action_days"]) <
                          int(min(v, key=lambda x: x["entered_utc"])["action_days"]) for v in amended))
    recoded = sum(1 for v in amended if v[0]["behavior_code"] != v[1]["behavior_code"])
    check("ask B no marker: amendments under a re-coded behaviour and under the same one both ship",
          0.5 * len(amended) <= recoded < len(amended), (recoded, len(amended)))
    sus = sum(1 for r in rows("attendance_absences_2024-25_to_2026-27.csv") if r["code"] == "SUS")
    served = sum(len(v) for k, v in A.oss_days(t, S["cal"], recs).items() if k[0] != "2023-24")
    check("ask A hazard: the attendance office posted only part of the suspension days", 0.4 * served < sus <
          0.8 * served, (sus, served))
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        t2 = os.path.join(tmp, "target")
        shutil.copytree(t, t2)
        bf = os.path.join(t2, "behavior_incidents_2023-24_to_2026-27.csv")
        head = open(bf, encoding="utf-8").readline()
        open(bf, "w", encoding="utf-8").write(head)
        g2 = A.solve(t2)["expected"]
    check("separation: the call is the same with the behaviour log emptied", abs(g2 - g) < 1e-9, g2)
    check("separation: the decisive model's cells use no incident or suspension field",
          A.golden_key({"runs": 1, "fails": 1, "inc": 99}) == A.golden_key({"runs": 1, "fails": 1, "inc": 0}))

    # ---- figures, realism, the world
    check("figures.json carries the call", fig["call"]["expected"] == round(g) and fig["call"]["seats"] == T2)
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("submission: the call and the expected number", "Fund %s" % fig["call"]["tier"] in sub and
          "**%d**" % fig["call"]["expected"] in sub)
    check("submission: every ask figure", all(("%.1f" % v) in sub for v in fig["ask_a"].values()) and
          all(("%s: %d" % (m, v)) in sub for (k, v) in fig["ask_b"].items() for m in [k.split(" ")[1]]))
    hl = list(fig["hist_leavers"].values())
    check("realism: the closed springs' leavers are not round or uniform", len(set(hl)) == 3 and not all(
        x % 5 == 0 for x in hl), hl)
    check("realism: no em dash in any shipped text", not any("—" in open(os.path.join(t, f), encoding="utf-8",
                                                                              errors="ignore").read()
                                                             for f in files if f.endswith((".csv", ".eml"))))
    W = WD.build()
    disp = sum(1 for r in W["years"][P.CUR].values() if r.get("disp"))
    check("world: the displaced families are a minority of the roll", 0.05 < disp / len(W["years"][P.CUR]) < 0.2,
          disp)
    print("checks: %d assertions, %d failure(s)" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
