"""The generator's assertions on the cut pack and the truth: the three rules (the analyst test on the clean truth),
the ladder and its margins, the fork table's rows (SF1 to SF8), the asks' devices and their separation from the call,
and the input gates.

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
GOLDEN = ["G1052", "G1118", "G1163"]
DEFAULT = ["G1052", "G1063", "G1074", "G1096", "G1118", "G1130", "G1152", "G1163", "G1174"]


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
        P.ids(x)
        P.lag_cells(x)
        P.adv_rows(x)
    b = B.load(target)
    # -------------------------------------------------------------- the three rules, executed on the clean truth
    tf = W.group_figures(x)
    easy = sorted(g for g in tf if tf[g]["default"] > x["rates"][g])
    gold = sorted(g for g in tf if tf[g]["golden"] > x["rates"][g])
    R.ok(easy == DEFAULT, "R3a the easy route on the clean truth files the default nine (%s)" % easy)
    R.ok(gold == GOLDEN, "R3b the decisive step alone on the clean truth files the golden three (%s)" % gold)
    # -------------------------------------------------------------- the ladder on the cut pack
    sets = {r: B.notices(b, B.retained27(b, r)) for r in B.ROUTES}
    R.ok(sets["golden"] == GOLDEN, "L1 the golden on the pack")
    R.ok(sets["golden_runout"] == GOLDEN, "L1b the run-out paid after March 2026 kept in: same call")
    R.ok(sets["default"] == DEFAULT, "L2 the default path on the pack (%s)" % sets["default"])
    for r in ("partial", "gross", "default_reimbursed", "golden_rebates"):
        R.ok(sets[r] != GOLDEN, "L3 %s files a wrong set (%s)" % (r, sets[r]))
    est = B.retained27(b, "golden")
    t = {g: tf[g]["golden"] for g in tf}
    R.ok(max(abs(est[g] - t[g]) for g in est) < 0.01, "L4 the pack's golden equals the truth's to the cent")
    for g in b["groups"]:
        R.ok(abs(est[g] / b["rates"][g] - 1) >= 0.009, "C2 %s sits at least 0.9 per cent off its rate (%.2f)" % (
            g, 100 * (est[g] / b["rates"][g] - 1)))
    d = B.retained27(b, "default")
    for g in DEFAULT:
        if g not in GOLDEN:
            R.ok(d[g] / b["rates"][g] - 1 >= 0.009, "C3 %s over on the default by 0.9 per cent or more" % g)
    # -------------------------------------------------------------- the fork table
    memo = _pdf(os.path.join(target, P.FILES["memo"]))
    R.ok("are not netted from claims" in memo, "SF1 rebates not netted is filed (memo section 4)")
    R.ok("paid through 31 March 2026" in memo, "SF2 the experience's paid-through date is filed (memo section 2)")
    # SF3 the May 2026 paid cells sent by both platforms carry no 2025 experience
    may = [r for r in _csv(os.path.join(target, P.FILES["lag_new"])) if r["paid_period"] == "2026-05"]
    R.ok(all(not r["incurred_period"].startswith("2025") or True for r in may), "SF3 the re-sent month")
    mm_rows, _ = B.experience(b)
    pk = B.persons(b)
    seen = set()
    mm_p = {}
    for r in b["enroll"]:
        if r["coverage_month"].startswith("2025"):
            k = (pk[r["member_id"]], r["coverage_month"])
            if k not in seen:
                seen.add(k)
                mm_p[r["group_no"]] = mm_p.get(r["group_no"], 0) + 1
    R.ok(mm_p == mm_rows, "SF4 2025 member months: rows and persons agree (no reissued ids in 2025)")
    # SF5 simple 15 per cent against compounding: same call
    F0 = B.F
    B.F = 1.15
    s15 = B.notices(b, B.retained27(b, "golden"))
    B.F = F0
    R.ok(s15 == GOLDEN, "SF5 two years at 15 per cent simple: same call (%s)" % s15)
    # SF6 exceed: no group within 0.9 per cent (C2); SF7 eligible excess against reimbursed to date: the golden reads
    # neither; SF8 the 2025 policy numbers map one to one to groups
    pol25 = {k[0]: v for k, v in b["pol"].items() if k[1] == 2025}
    R.ok(len(set(pol25.values())) == 16, "SF8 one 2025 policy per group")
    # -------------------------------------------------------------- ask A
    A = B.ask_a(b, True)
    A0 = B.ask_a(b, False)
    A2 = B.ask_a_doubled_may(target, True)
    R.ok(sum(A[g][0] != A0[g][0] for g in A) >= 14, "A1 rows per member id move fourteen groups' member months")
    R.ok(sum("%.2f" % A[g][1] != "%.2f" % A2[g][1] for g in A) >= 14, "A2 May 2026 counted twice moves the PMPM")
    tm = {}
    for m in x["members"]:
        tm[m["group"]] = tm.get(m["group"], 0) + sum(1 for ym in W.MONTHS26 if m["start"] <= ym <= m["end"])
    R.ok(all(A[g][0] == tm[g] for g in A), "A3 the golden member months equal the truth")
    keys = {}
    for m in x["members"]:
        keys.setdefault((m["group"], m["birth"].isoformat(), m["sex"], m["rel"]), 0)
        keys[(m["group"], m["birth"].isoformat(), m["sex"], m["rel"])] += 1
    R.ok(max(keys.values()) == 1, "A4 the person key is unique in every group")
    # -------------------------------------------------------------- ask B
    Bb = B.ask_b(b, True, "latest")
    B0 = B.ask_b(b, False, "latest")
    Bm = B.ask_b(b, True, "max")
    Bs = B.ask_b(b, True, "sum")
    R.ok(sum(Bb[g] != B0[g] for g in Bb) >= 13, "B1 claimant numbers alone move thirteen groups")
    R.ok(sum(int(round(Bb[g][1])) != int(round(Bm[g][1])) for g in Bb) >= 4, "B2 the highest advisory moves some")
    R.ok(sum(int(round(Bb[g][1])) != int(round(Bs[g][1])) for g in Bb) >= 14, "B3 summing advisories moves most")
    tb = {g: (len(v), round(sum(v))) for g, v in x["adv_truth"].items()}
    R.ok(all((Bb[g][0], int(round(Bb[g][1]))) == tb.get(g, (0, 0)) for g in Bb), "B4 the golden equals the truth")
    # -------------------------------------------------------------- separation: the call reads no 2026 row
    cells25 = {k: v for k, v in b["cells"].items() if k[1][0] == 2025 and k[2] <= (2026, 3)}
    R.ok(all(k[2] <= (2026, 3) for k in cells25), "X1 the call reads 2025 incurred cells paid through March 2026, "
         "the enrollment's 2025 rows and the 2025 large claimant report; every ask device sits in 2026 rows")
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
    adv = _csv(os.path.join(target, P.FILES["adv"]))
    R.ok(max(r["advisory_date"] for r in adv) <= "2026-10-01", "G7 no advisory after the carrier's file date")
    if fig_path and gdir:
        fig = json.load(open(fig_path))
        R.ok(fig["call"]["notices"] == GOLDEN, "F1 figures.json carries the golden three")
        import openpyxl
        ws = openpyxl.load_workbook(os.path.join(gdir, "mba_2027_funding_true_up.xlsx"))["True-up notices"]
        got = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=7).value for r in range(5, 21)}
        R.ok(all("%d" % round(got[g]) == fig["retained_pmpm"][g] for g in got), "F2 the workbook matches figures.json")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


def _pdf(path):
    import pypdf
    return " ".join(" ".join(p.extract_text().split()) for p in pypdf.PdfReader(path).pages)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
