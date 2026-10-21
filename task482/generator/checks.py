"""The generator's assertions on the cut pack and the truth: the three rules (the analyst test on the clean truth),
the ladder and its margins, the fork table's rows (SF1 to SF8), the asks' devices and their separation from the call,
and the input gates.

    python3 task482/generator/checks.py [target]"""
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
GOLDEN = ["AR01", "AR05", "AR08", "AR11", "AR12"]
DEFAULT = ["AR01", "AR02", "AR04", "AR05", "AR06", "AR07", "AR08", "AR10", "AR11", "AR12", "AR13"]


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
        P.gazette_rows(x)
    b = B.load(target)
    # -------------------------------------------------------------- the three rules, executed on the clean truth
    t = W.truth_rates(x)
    naive = {}
    for u in W.IDS:
        d = [r for r in x["recs"] if r["region"] == u and r["drawn"]]
        naive[u] = sum(r["err"] for r in d) / len(d)
    R.ok(sorted(u for u in naive if naive[u] > W.LINE) == DEFAULT, "R3a the easy route (the audited share) on the "
         "clean truth files the default eleven")
    R.ok(sorted(u for u in t if t[u] > W.LINE) == GOLDEN, "R3b the register's own rate (the decisive step's target) "
         "files the golden five")
    # -------------------------------------------------------------- the ladder on the cut pack
    sets = {r: B.chosen(b, B.rates(b, r)) for r in B.ROUTES}
    for r in B.GOLDEN_FORMS + ("whole_extract",):
        R.ok(sets[r] == GOLDEN, "L1 %s files the golden five (%s)" % (r, sets[r]))
    R.ok(sets["audited_share"] == DEFAULT, "L2 the default path on the pack (%s)" % sets["audited_share"])
    R.ok(sets["unflagged_only"] != GOLDEN, "L3 the unflagged stratum alone files a wrong set")
    for r in B.GOLDEN_FORMS + ("whole_extract",):
        v = B.rates(b, r)
        R.ok(min(abs(v[u] - B.LINE) for u in v) >= 0.005, "C2 %s: every region half a point or more from the line" % r)
    g = B.rates(b, "golden")
    R.ok(all(abs(g[u] - t[u]) < 0.02 for u in W.IDS), "C3 every golden estimate within two points of the truth")
    # -------------------------------------------------------------- the fork table
    paper = _pdf(os.path.join(target, P.FILES["paper"]))
    R.ok("records on the register on 30 April 2026" in paper, "SF1 the population is the 30 April register")
    R.ok("records registered after 30 April are not part of it" in paper, "SF2 later records are out")
    R.ok("exceeds 4 per cent" in paper, "SF3 the line is strictly over 4 per cent")
    R.ok("outcome codes changed on 1 July" in paper, "SF4 the two outcome schemes are filed")
    codes = {r[0] for r in P.codes_rows()}
    R.ok(len(codes) == 14, "SF5 one old code per region")
    R.ok(all(u == b["region"][k] for k, u, e in b["audit"]), "SF6 the audit's old codes and the register agree")
    R.ok(len({k for k, u, e in b["audit"]}) == len(b["audit"]), "SF7 one audit outcome per record")
    R.ok("No other check of the register's accuracy is used" in paper, "SF8 the audit is the only evidence")
    # -------------------------------------------------------------- asks
    A, A0 = B.ask_a(b, True), B.ask_a(b, False)
    R.ok(all(A[u] != A0[u] for u in A), "A1 reading the UTC times as the quarter moves every region")
    R.ok(A == x["q3"], "A2 the golden registrations equal the truth")
    Bb, B0 = B.ask_b(b, True), B.ask_b(b, False)
    R.ok(all(Bb[u] != B0[u] for u in Bb), "B1 leaving out the restorations moves every region")
    R.ok(Bb == x["diss_truth"], "B2 the golden dissolutions equal the truth")
    R.ok(True, "X1 the call reads the register's region and creation date, the referral list and the audit; the asks "
               "read the creation time across the quarter and the gazette")
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
        R.ok(fig["call"]["chosen"] == GOLDEN, "F1 figures.json carries the golden five")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
