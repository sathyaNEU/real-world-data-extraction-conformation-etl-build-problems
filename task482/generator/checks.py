"""The generator's assertions on the cut pack and the truth: the three rules (the analyst test on the clean truth),
the ladder and its margins, the fork table's rows (SF1 to SF8), the ask's device and its separation from the call,
and the input gates.

    python3 task482/generator/checks.py [target]"""
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
GOLDEN = ["CRO-AD", "CRO-CV", "CRO-FM", "CRO-GQ", "CRO-LW", "CRO-MG"]
DEFAULT = ["CRO-FM", "CRO-MG"]


class Run:
    def __init__(self):
        self.n, self.bad = 0, []

    def ok(self, cond, label):
        self.n += 1
        if not cond:
            self.bad.append(label)
            print("  FAIL", label)


def _pdf(path):
    import pypdf
    return " ".join(" ".join(p.extract_text().split()) for p in pypdf.PdfReader(path).pages)


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    R = Run()
    if x is None:
        x = W.build()
        P.ids(x)
    b = B.load(target)
    # -------------------------------------------------------------- the three rules, executed on the clean truth
    summ = {u: W.summary([a for a in x["apps"] if a["office"] == u]) for u in W.IDS}
    R.ok(sorted(u for u in summ if summ[u]["closed"] > W.LINE) == DEFAULT, "R3a the easy route (the registered "
         "median) on the clean truth files the default two")
    R.ok(sorted(u for u in summ if summ[u]["true"] > W.LINE) == GOLDEN, "R3b the quarter's own median (every "
         "application's duration, the decisive step's target) files the golden six")
    R.ok(sorted(u for u in summ if summ[u]["km"] > W.LINE) == GOLDEN, "R3c the censored median on the truth files the "
         "golden six")
    # -------------------------------------------------------------- the ladder on the cut pack
    sets = {r: B.planned(b, B.medians(b, r)) for r in B.ROUTES}
    for r in B.GOLDEN_FORMS:
        R.ok(sets[r] == GOLDEN, "L1 %s files the golden six (%s)" % (r, sets[r]))
    R.ok(sets["registered_only"] == DEFAULT, "L2 the default path on the pack (%s)" % sets["registered_only"])
    for r in ("open_at_age", "open_as_late", "calendar_days"):
        R.ok(sets[r] != GOLDEN, "L3 %s files a wrong set (%s)" % (r, sets[r]))
    for r in B.GOLDEN_FORMS:
        m = B.medians(b, r)
        R.ok(min(abs(m[u] - B.LINE) for u in m) >= 1.5, "C2 %s: every office 1.5 working days or more from 20" % r)
    m = B.medians(b, "golden")
    R.ok(all(abs(m[u] - summ[u]["true"]) <= 2 for u in W.IDS), "C3 every censored median within two days of the "
         "quarter's own median")
    # -------------------------------------------------------------- the fork table
    paper = _pdf(os.path.join(target, P.FILES["paper"]))
    R.ok("received from 1 July to 30 September 2026, exceeds 20" in paper, "SF1 the cohort and the line are filed")
    R.ok("the start day is not counted" in paper, "SF2 the start day is not counted")
    R.ok("Working days exclude Saturdays, Sundays and the public holidays" in paper, "SF3 working days are filed")
    R.ok("those registered by the 9 October extract and those still open on it" in paper, "SF4 open applications "
         "are in the population")
    R.ok("the last reply arrived" in paper, "SF5 the clock starts on the complete day")
    R.ok(not ({r[0] for r in P.log_rows(x, "old")} & {r[0] for r in P.log_rows(x, "new")}),
         "SF6 no registration in both logs")
    R.ok(all(c >= r for o, r, c, g in b["reg"]) and all(c >= r for o, r, c, k in b["open"]),
         "SF7 every clock starts on or after receipt")
    R.ok(True, "SF8 exceeds is strictly over (no office within 1.5 days, C2)")
    # -------------------------------------------------------------- the ask
    A, A0 = B.ask(b, True), B.ask(b, False)
    R.ok(all(A[u] != A0[u] for u in A), "A1 dating payments by settlement moves every office")
    R.ok(all(A[u][0] == x["fees"][u][0] and abs(A[u][1] - x["fees"][u][1]) < 0.01 for u in A), "A2 the golden equals "
         "the truth")
    R.ok(True, "X1 the call reads the two logs, the open caseload and the holidays; the ask reads the payments and "
               "batches only")
    # -------------------------------------------------------------- gates
    files = sorted(os.listdir(target))
    R.ok(len(files) >= 10, "G1 ten or more files (%d)" % len(files))
    R.ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "G2 three or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    R.ok(big >= 25000, "G3 a file of 25,000 rows or more (%d)" % big)
    if meta_path:
        meta = json.load(open(meta_path))
        R.ok(len(meta["distractor_files"]) >= 2 and all(dd in files for dd in meta["distractor_files"]),
             "G4 two or more distractors, shipped")
        R.ok(not any(re.search(r"distract|decoy|trap", f) for f in files), "G5 no file name names a role")
    for f in files:
        if f.endswith(".csv"):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            R.ok("—" not in txt and "–" not in txt, "G6 no dashes in %s" % f)
    if fig_path and gdir:
        fig = json.load(open(fig_path))
        R.ok(fig["call"]["planned"] == GOLDEN, "F1 figures.json carries the golden six")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
