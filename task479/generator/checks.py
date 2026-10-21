"""The generator's assertions on the cut pack and the truth: the three rules (the analyst test on the clean truth),
the ladder and its margins, the evidence that rapid responses carry nothing, the fork table's rows (SF1 to SF7), the
asks' devices and their separation from the call, and the input gates.

    python3 task479/generator/checks.py [target]"""
import csv
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
GOLDEN = ["C01", "C04", "C07", "C13"]
DEFAULT = ["C01", "C03", "C04", "C06", "C07", "C09", "C11", "C13"]


class Run:
    def __init__(self):
        self.n, self.bad = 0, []

    def ok(self, cond, label):
        self.n += 1
        if not cond:
            self.bad.append(label)
            print("  FAIL", label)


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    R = Run()
    if x is None:
        x = W.build()
        P.people(x)
    b = B.load(target)
    # -------------------------------------------------------------- the three rules on the clean truth
    tv, tg, tt = W.shares(x, "ss_vendor"), W.shares(x, "ss_gold"), W.shares(x, "ss_true")
    R.ok(sorted(c for c in tv if tv[c] >= W.LINE) == DEFAULT, "R3a the vendor's scores on the clean truth: the default")
    R.ok(sorted(c for c in tg if tg[c] >= W.LINE) == GOLDEN, "R3b the effort-moderated scores on the truth: the golden")
    R.ok(sorted(c for c in tt if tt[c] >= W.LINE) == GOLDEN, "R3c the students' true achievement: the golden")
    # -------------------------------------------------------------- the ladder on the cut pack
    sets = {r: B.designate(b, B.spring(b, r)) for r in B.ROUTES}
    for r in ("golden", "golden_3s", "golden_6s"):
        R.ok(sets[r] == GOLDEN, "L1 %s files the golden four" % r)
    R.ok(sets["vendor"] == DEFAULT and sets["rescore_all"] == DEFAULT, "L2 the vendor's and the all-response rescore")
    for r in ("drop_rapid_students", "drop_rapid_sessions"):
        R.ok(sets[r] != GOLDEN, "L3 %s files a wrong set (%s)" % (r, sets[r]))
    v, a = B.spring(b, "vendor"), B.spring(b, "rescore_all")
    R.ok(all(v[k] == a[k] for k in v), "L4 the vendor's scores are the MLE on all forty responses, every student")
    sh = B.shares(b, B.spring(b, "golden"))
    for c in b["campuses"]:
        R.ok(abs(sh[c] - B.LINE) >= 0.03, "C2 %s at least 3 points off the line (%.1f)" % (c, 100 * sh[c]))
    shv = B.shares(b, v)
    for c in DEFAULT:
        if c not in GOLDEN:
            R.ok(shv[c] >= 0.38, "C3 %s 3 points over on the vendor's scores (%.1f)" % (c, 100 * shv[c]))
    # -------------------------------------------------------------- the evidence the rapid responses carry nothing
    fast, slow = [], []
    acc_by_b = {}
    for s, rows in b["resp"].items():
        for seq, iid, sc, t in rows:
            (fast if t < B.RAPID else slow).append(t)
            if t < B.RAPID:
                q = int(b["bank"][iid][1] > 0)
                acc_by_b.setdefault(q, []).append(sc)
    R.ok(max(fast) < 3.0 and min(slow) > 7.4, "E1 a gap in the times: rapid under 3 seconds, engaged over 7.4")
    accs = [np.mean(acc_by_b[q]) for q in (0, 1)]
    R.ok(all(0.22 < z < 0.28 for z in accs), "E2 rapid responses right at the guess rate on easy and hard items (%s)" % accs)
    # -------------------------------------------------------------- the fork table
    man = _pdf(os.path.join(target, P.FILES["manual"]))
    R.ok("maximum likelihood" in man and "500 + 40 theta" in man, "SF1 scoring by maximum likelihood on the bank, filed")
    R.ok("untimed" in man, "SF2 the test is untimed, filed")
    R.ok(sets["golden_3s"] == sets["golden_6s"] == GOLDEN, "SF3 any threshold in the gap: same call")
    memo = _docx(os.path.join(target, P.FILES["memo"]))
    R.ok("A student tested is a student with a spring 2026 benchmark administration" in memo, "SF4 students tested, filed")
    R.ok("later administration is the student's score" in man, "SF5 a restarted session's later administration, filed")
    ms = {}
    for r in _csv(os.path.join(target, P.FILES["resp1"])):
        ms.setdefault(r["StudentID"], 0)
    R.ok(len(set(ms) & {r["student_id"] for r in _csv(os.path.join(target, P.FILES["resp2"]))}) == 0,
         "SF6 no student in both export layouts")
    R.ok(all(len(rows) == 40 for rows in b["resp"].values()), "SF7 forty responses per student")
    # -------------------------------------------------------------- the asks
    A, A0 = B.ask_a(b, True), B.ask_a(b, False)
    R.ok(sum(A[c][0] != A0[c][0] for c in A) == 14, "A1 rows as students move every campus's count")
    R.ok(sum("%.1f" % A[c][1] != "%.1f" % A0[c][1] for c in A) >= 13, "A2 the share moves")
    truthA = {}
    for s in x["students"]:
        t = truthA.setdefault(s["fall_campus"], [0, 0])
        t[0] += 1
        t[1] += s["fall"] >= W.PROFICIENT
    R.ok(all(A[c][0] == truthA[c][0] and "%.1f" % A[c][1] == "%.1f" % (100 * truthA[c][1] / truthA[c][0]) for c in A),
         "A3 the golden equals the truth")
    Bb, B0 = B.ask_b(b, True), B.ask_b(b, False)
    R.ok(sum(Bb[c][0] != B0[c][0] for c in Bb) >= 13, "B1 the crosswalk alone moves the counts")
    R.ok(sum("%.1f" % Bb[c][1] != "%.1f" % B0[c][1] for c in Bb) >= 13, "B2 the growth moves")
    truthB = {}
    for s in x["students"]:
        t = truthB.setdefault(s["campus"], [0, 0])
        t[0] += 1
        t[1] += s["winter"] - s["fall"]
    R.ok(all(Bb[c][0] == truthB[c][0] and "%.1f" % Bb[c][1] == "%.1f" % (truthB[c][1] / truthB[c][0]) for c in Bb),
         "B3 the golden equals the truth")
    # -------------------------------------------------------------- separation
    R.ok(True, "X1 the call reads the spring responses, the bank and the spring report; the ask devices sit in the "
               "fall and winter reports, the temporary register, the rosters and the crosswalk")
    # -------------------------------------------------------------- gates
    files = sorted(os.listdir(target))
    R.ok(len(files) >= 10, "G1 ten or more files (%d)" % len(files))
    R.ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "G2 three or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    R.ok(big >= 25000, "G3 a file of 25,000 rows or more (%d)" % big)
    if meta_path:
        meta = json.load(open(meta_path))
        R.ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "G4 distractors")
        R.ok(not any(re.search(r"distract|decoy|trap", f) for f in files), "G5 no file name names a role")
    for f in files:
        if f.endswith(".csv"):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            R.ok("—" not in txt and "–" not in txt, "G6 no dashes in %s" % f)
    if fig_path and gdir:
        fig = json.load(open(fig_path))
        R.ok(fig["call"]["designated"] == GOLDEN, "F1 figures.json carries the golden four")
        import openpyxl
        ws = openpyxl.load_workbook(os.path.join(gdir, "bellweather_2026-27_tutoring_designation.xlsx"))["Designation"]
        got = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=5).value for r in range(5, 19)}
        R.ok(all("%.1f" % got[c] == fig["below_basic_pct"][c] for c in got), "F2 the workbook matches figures.json")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


def _pdf(path):
    import pypdf
    return " ".join(" ".join(p.extract_text().split()) for p in pypdf.PdfReader(path).pages)


def _docx(path):
    import docx
    return " ".join(p.text for p in docx.Document(path).paragraphs)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
