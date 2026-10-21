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
GOLDEN = ["MV03", "MV07", "MV21", "MV25", "MV36", "MV47"]
DEFAULT = ["MV03", "MV25", "MV36"]
CHANGERS = ["MV07", "MV21", "MV32", "MV47"]


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


def truth(x=None):
    if x is None:
        x = W.build()
    if "mid" not in x["members"][0]:
        P.ids(x)
        P.lag_cells(x)
        P.adv_rows(x)
    return x


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    R = Run()
    x = truth(x)
    if "adv_truth" not in x:
        P.adv_rows(x)
    b = B.load(target)
    # -------------------------------------------------------------- the three rules, executed on the clean truth
    te = W.estimates(x)
    easy = sorted(d for d in te if te[d]["default"] > x["rates"][d])
    gold = sorted(d for d in te if te[d]["golden"] > x["rates"][d])
    R.ok(easy == DEFAULT, "R3a the easy route (each district's own 2025) on the clean truth files the default three "
                          "(%s)" % easy)
    R.ok(gold == GOLDEN, "R3b the decisive step alone (the 2026 plan's 2025 factor) files the golden six (%s)" % gold)
    pooled = sorted(d for d in te if te[d]["pooled"] > x["rates"][d])
    R.ok(pooled != GOLDEN, "R3c one cooperative-wide factor files a wrong set (%s)" % pooled)
    # -------------------------------------------------------------- the ladder on the cut pack
    sets = {r: B.raised(b, B.expected(b, r)) for r in B.ROUTES}
    R.ok(sets["golden"] == GOLDEN, "L1 the golden on the pack")
    for r in ("mean_of_ratios", "paid_share"):
        R.ok(sets[r] == GOLDEN, "L1b the golden's form %s: same call" % r)
    R.ok(sets["default"] == DEFAULT, "L2 the default path on the pack (%s)" % sets["default"])
    for r in ("pooled", "annualised"):
        R.ok(sets[r] != GOLDEN, "L3 %s files a wrong set (%s)" % (r, sets[r]))
    est = B.expected(b, "golden")
    R.ok(max(abs(est[d] - te[d]["golden"]) for d in est) < 0.01, "L4 the pack's golden equals the truth's to the cent")
    for d in b["ids"]:
        R.ok(abs(est[d] / b["rates"][d] - 1) >= 0.025, "C2 %s sits at least 2.5 per cent off its claims component "
             "(%.2f)" % (d, 100 * (est[d] / b["rates"][d] - 1)))
    dflt = B.expected(b, "default")
    for d in GOLDEN:
        if d not in DEFAULT:
            R.ok(1 - dflt[d] / b["rates"][d] >= 0.025, "C3 %s under on its own 2025 by 2.5 per cent or more" % d)
    R.ok(sorted(d for d in b["ids"] if b["design"][(d, 2025)] != b["design"][(d, 2026)]) == CHANGERS,
         "C4 the benefit designs PDF parses: four districts changed plan")
    # -------------------------------------------------------------- the fork table
    for d in W.IDS:
        v = {k: int(10 * round(f / 10)) for k, f in te[d]["forms"].items()}
        R.ok(len(set(v.values())) == 1, "SF1 %s every form of the completion rounds to one ten dollars (%s)" % (d, v))
        lo = min(te[d]["forms"].values())
        hi = max(te[d]["forms"].values())
        R.ok(hi - 10 * round(lo / 10) < 5 - 0.5 and 10 * round(hi / 10) - lo < 5 - 0.5,
             "SF1b %s every form half a dollar or more inside its bin" % d)
    R.ok(all(k[2] <= P._after(k[1][0], k[1][1], 3) for k in b["cells"]), "SF2 every cell paid within three months of "
         "service: January to June 2026 complete by September, 2025 by March 2026")
    old = {(r["DistrictID"], B._ym(r["IncurredMonth"]), r["Category"]): r["PaidAmount"]
           for r in _csv(os.path.join(target, P.FILES["lag_old"])) if r["PaidMonth"] == "05/2026"}
    new = {(r["district_code"], B._ym(r["incurred_period"]), "Medical" if r["benefit_type"] == "MED" else "Pharmacy"):
           "%.2f" % (int(r["plan_paid_cents"]) / 100) for r in _csv(os.path.join(target, P.FILES["lag_new"]))
           if r["paid_period"] == "2026-05"}
    R.ok(old == new and len(old) > 0, "SF3 May 2026 sent by both platforms with the same cells")
    pk = B.persons(b)
    for span, months in (("2025", B.Y25), ("January to June 2026", B.H1)):
        ms = {"%d-%02d" % ym for ym in months}
        rows = [r for r in b["enroll"] if r["coverage_month"] in ms]
        R.ok(len(rows) == len({(pk[r["member_id"]], r["coverage_month"]) for r in rows}),
             "SF4 %s member months: rows and persons agree (no reissued ids)" % span)
    memo = _pdf(os.path.join(target, P.FILES["memo"]))
    R.ok("before pharmacy rebates" in memo, "SF5 rebates kept out is filed (memo section 2)")
    R.ok("gross of specific stop-loss reimbursements" in memo, "SF6 gross of stop-loss is filed (memo section 2)")
    R.ok("January to December 2026" in memo, "SF7 the plan year is filed")
    R.ok("paid through 30 September 2026" in memo and "paid through 31 March 2026" in memo, "SF8 both paid-through "
         "dates are filed")
    # -------------------------------------------------------------- ask A
    A = B.ask_a(b, True)
    A0 = B.ask_a(b, False)
    R.ok(sum(A[d] != A0[d] for d in A) >= 12, "A1 rows per member id move twelve or more districts")
    q3 = [(2026, 7), (2026, 8), (2026, 9)]
    tm = {d: W.member_months(x, d, q3) for d in W.IDS}
    R.ok(A == tm, "A2 the golden member months equal the truth")
    keys = {}
    for m in x["members"]:
        k = (m["district"], m["birth"].isoformat(), m["sex"], m["rel"])
        keys[k] = keys.get(k, 0) + 1
    R.ok(max(keys.values()) == 1, "A3 the person key is unique in every district")
    # -------------------------------------------------------------- ask B
    Bb = B.ask_b(b, True, "latest")
    B0 = B.ask_b(b, False, "latest")
    Bm = B.ask_b(b, True, "max")
    Bs = B.ask_b(b, True, "sum")
    R.ok(sum(Bb[d] != B0[d] for d in Bb) >= 12, "B1 claimant numbers alone move twelve or more districts")
    R.ok(sum(int(round(Bb[d][1])) != int(round(Bm[d][1])) for d in Bb) >= 4, "B2 the highest advisory moves some")
    R.ok(sum(int(round(Bb[d][1])) != int(round(Bs[d][1])) for d in Bb) >= 14, "B3 summing advisories moves most")
    tb = {d: (len(v), round(sum(v))) for d, v in x["adv_truth"].items()}
    R.ok(all((Bb[d][0], int(round(Bb[d][1]))) == tb.get(d, (0, 0)) for d in Bb), "B4 the golden equals the truth")
    # -------------------------------------------------------------- separation
    new_ids = {m["mid2"] for m in x["members"] if "mid2" in m}
    R.ok(all(r["coverage_month"] >= "2026-07" for r in b["enroll"] if r["member_id"] in new_ids),
         "X1 every reissued id sits in July 2026 or later: the call reads 2025 and January to June 2026 enrollment, "
         "the lag cells, the designs and the rates; the advisories are read by ask B only")
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
            R.ok("\u2014" not in txt and "\u2013" not in txt, "G6 no dashes in %s" % f)
    adv = _csv(os.path.join(target, P.FILES["adv"]))
    R.ok(max(r["advisory_date"] for r in adv) <= "2026-10-01", "G7 no advisory after the carrier's file date")
    if fig_path and gdir:
        fig = json.load(open(fig_path))
        R.ok(fig["call"]["raised"] == GOLDEN, "F1 figures.json carries the golden six")
        import openpyxl
        ws = openpyxl.load_workbook(os.path.join(gdir, "mvshc_january_2027_contribution_review.xlsx"))[
            "Contribution review"]
        got = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=8).value for r in range(5, 21)}
        R.ok(all(got[d] == fig["expected_pmpm"][d] for d in got), "F2 the workbook matches figures.json")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
