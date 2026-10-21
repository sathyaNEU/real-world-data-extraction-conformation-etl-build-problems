"""The generator's assertions on the cut pack and the truth: the three rules (the analyst test on the clean truth),
the ladder and its margins, the fork table's rows (SF1 to SF8), the asks' devices and their separation from the call,
and the input gates.

    python3 task479/generator/checks.py [target]"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
GOLDEN = ["CR113", "CR118", "CR131", "CR149", "CR167", "CR176"]
DEFAULT = ["CR104", "CR109", "CR136", "CR167", "CR176"]


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


def _pdf(path):
    import pypdf
    return " ".join(" ".join(p.extract_text().split()) for p in pypdf.PdfReader(path).pages)


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    R = Run()
    if x is None:
        x = W.build()
        P.ids(x)
        P.lag_cells(x)
        P.hcc_rows(x)
    b = B.load(target)
    # -------------------------------------------------------------- the three rules, executed on the clean truth
    ex = W.experience(x)
    rt = W.routes(ex)
    fm = W.forms(ex)
    easy = sorted(e for e in W.IDS if rt["own_experience"][e] > x["rates"][e])
    gold = sorted(e for e in W.IDS if fm["buhlmann_straub"][e] > x["rates"][e])
    R.ok(easy == DEFAULT, "R3a the easy route (each employer's own experience trended) on the clean truth files the "
                          "default five (%s)" % easy)
    R.ok(gold == GOLDEN, "R3b the decisive step alone (credibility against the trust) files the golden six (%s)" % gold)
    last = sorted(e for e in W.IDS if rt["own_2025"][e] > x["rates"][e])
    R.ok(last != GOLDEN, "R3c the 2025 experience alone files a wrong set (%s)" % last)
    # -------------------------------------------------------------- the ladder on the cut pack
    sets = {r: B.surcharged(b, B.expected(b, r)) for r in B.ROUTES}
    R.ok(sets["golden"] == GOLDEN, "L1 the golden on the pack")
    for r in B.SHRINK[1:]:
        R.ok(sets[r] == GOLDEN, "L1b the credibility form %s: same call" % r)
    R.ok(sets["own_experience"] == DEFAULT, "L2 the default path on the pack (%s)" % sets["own_experience"])
    for r in ("own_2025", "trust_level"):
        R.ok(sets[r] != GOLDEN, "L3 %s files a wrong set (%s)" % (r, sets[r]))
    est = B.expected(b, "golden")
    R.ok(max(abs(est[e] - fm["buhlmann_straub"][e]) for e in est) < 0.02, "L4 the pack's golden equals the truth's "
         "to two cents")
    for e in b["ids"]:
        vals = [B.expected(b, r)[e] for r in B.SHRINK]
        side = {v > b["rates"][e] for v in vals}
        R.ok(len(side) == 1 and min(abs(v / b["rates"][e] - 1) for v in vals) >= 0.024,
             "C2 %s every credibility form on one side, 2.4 per cent or more from its claims component" % e)
    for e in set(GOLDEN) ^ set(DEFAULT):
        d = B.expected(b, "own_experience")[e]
        R.ok(abs(d / b["rates"][e] - 1) >= 0.024, "C3 %s own experience 2.4 per cent or more on the other side" % e)
    # -------------------------------------------------------------- the fork table
    R.ok(all(k[2] <= P._after(k[1][0], k[1][1], 3) for k in b["cells"]), "SF1 every cell paid within three months of "
         "service: each plan year complete by March of the next")
    old = {(r["EmployerNo"], B._ym(r["IncurredMonth"]), r["Category"]): r["PaidAmount"]
           for r in _csv(os.path.join(target, P.FILES["lag_old"])) if r["PaidMonth"] == "05/2026"}
    new = {(r["employer_code"], B._ym(r["incurred_period"]), "Medical" if r["benefit_type"] == "MED" else "Pharmacy"):
           "%.2f" % (int(r["plan_paid_cents"]) / 100) for r in _csv(os.path.join(target, P.FILES["lag_new"]))
           if r["paid_period"] == "2026-05"}
    R.ok(old == new and len(old) > 0, "SF2 May 2026 sent by both platforms with the same cells")
    pk = B.persons(b)
    rows = [r for r in b["enroll"] if r["coverage_month"] < "2026-07"]
    R.ok(len(rows) == len({(pk[r["member_id"]], r["coverage_month"]) for r in rows}),
         "SF3 2023 to June 2026 member months: rows and persons agree (no reissued ids)")
    memo = _pdf(os.path.join(target, P.FILES["memo"]))
    R.ok("before pharmacy rebates" in memo, "SF4 rebates kept out is filed (memo section 2)")
    R.ok("trended at 7 per cent a year to 2027" in memo, "SF5 the trend on each year's retained claims is filed "
         "(memo section 3); the leveraged form gives the same call (L1b)")
    R.ok("paid through 31 March of the next" in memo, "SF6 the paid-through date is filed")
    R.ok("2026 are not yet complete and are not part of the review" in memo, "SF7 2026 claims are out of the evidence")
    re_ = _csv(os.path.join(target, P.FILES["reimb"]))
    R.ok(all(abs(float(r["paid_in_contract_year"]) - 150000 - float(r["reimbursed"])) < 0.01 for r in re_),
         "SF8 every reimbursement is the claims over $150,000 in full")
    # -------------------------------------------------------------- ask A
    A = B.ask_a(b, True)
    A0 = B.ask_a(b, False)
    R.ok(sum(A[e] != A0[e] for e in A) >= 16, "A1 rows per member id move sixteen or more employers")
    q3 = [(2026, 7), (2026, 8), (2026, 9)]
    R.ok(all(A[e] == W.member_months(x, e, q3) for e in W.IDS), "A2 the golden member months equal the truth")
    keys = {}
    for m in x["members"]:
        k = (m["emp"], m["birth"].isoformat(), m["sex"], m["rel"])
        keys[k] = keys.get(k, 0) + 1
    R.ok(max(keys.values()) == 1, "A3 the person key is unique in every employer")
    # -------------------------------------------------------------- ask B
    Bb = B.ask_b(b, True)
    B0 = B.ask_b(b, False)
    R.ok(sum(Bb[e] != B0[e] for e in Bb) >= 16, "B1 member ids alone move sixteen or more employers")
    tb = {e: (len(v), round(sum(v))) for e, v in x["hcc_truth"].items()}
    R.ok(all((Bb[e][0], int(round(Bb[e][1]))) == tb.get(e, (0, 0)) for e in Bb), "B2 the golden equals the truth")
    # -------------------------------------------------------------- separation
    new_ids = {m["mid2"] for m in x["members"]}
    R.ok(all(r["coverage_month"] >= "2026-07" for r in b["enroll"] if r["member_id"] in new_ids),
         "X1 every reissued id sits in July 2026 or later: the call reads 2023 to 2025 eligibility, the lag cells, the "
         "reimbursements and the elections; the high-cost report is read by ask B only")
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
        R.ok(fig["call"]["surcharged"] == GOLDEN, "F1 figures.json carries the golden six")
        import openpyxl
        ws = openpyxl.load_workbook(os.path.join(gdir, "crbht_2027_renewal_surcharges.xlsx"))["Renewal review"]
        got = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=5).value for r in range(5, 23)}
        R.ok(all(got[e] == fig["experience_pmpm"][e] for e in got), "F2 the workbook matches figures.json")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
