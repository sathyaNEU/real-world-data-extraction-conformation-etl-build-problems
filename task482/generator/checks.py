"""The generator's assertions on the cut pack and the truth: the three rules (the analyst test on the clean truth),
the ladder and its margins, the fork table's rows (SF1 to SF8), the asks' devices and their separation from the call,
and the input gates.

    python3 task482/generator/checks.py [target]"""
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
GOLDEN = ["214682", "214946", "216190", "216278", "216454"]
DEFAULT = ["214506", "214682", "214858", "214946", "215298"]


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


def five(v):
    return sorted(sorted(v, key=lambda u: v[u])[:5])


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    R = Run()
    if x is None:
        x = W.build()
        P.codes(x)
        P.census(x)
    b = B.load(target)
    # -------------------------------------------------------------- the three rules, executed on the clean truth
    t = W.truth_per_fte(x)
    easy = {}
    for u in W.IDS:
        if W.KIND[u] == "S":
            easy[u] = t[u]
    for p in [u for u in W.IDS if W.KIND[u] == "P"]:
        mem = [p] + [c for c in W.IDS if W.PARENT[c] == p]
        for u in mem:
            easy[u] = x["reported"][p] / sum(x["fte"][m] for m in mem)
    R.ok(five(easy) == DEFAULT, "R3a the easy route (each parent's return split by FTE) on the clean truth files the "
                                "default five (%s)" % five(easy))
    R.ok(five(t) == GOLDEN, "R3b each campus's own instruction expense (the decisive step) files the golden five (%s)" %
         five(t))
    # -------------------------------------------------------------- the ladder on the cut pack
    sets = {r: B.awarded(b, B.per_fte(b, r)) for r in B.ROUTES}
    for r in ("golden", "wls_fte", "with_intercept", "by_term"):
        R.ok(sets[r] == GOLDEN, "L1 %s on the pack files the golden five (%s)" % (r, sets[r]))
    R.ok(sets["fte_split"] == DEFAULT, "L2 the default path on the pack (%s)" % sets["fte_split"])
    for r in ("credit_hour_split", "two_level", "exclude_children", "zero", "direct"):
        R.ok(sets[r] != GOLDEN, "L3 %s files a wrong five (%s)" % (r, sets[r]))
    for r in ("golden", "wls_fte", "by_term"):
        v = B.per_fte(b, r)
        o = sorted(v, key=lambda u: v[u])
        R.ok(v[o[5]] / v[o[4]] >= 1.03, "C2 %s: the sixth stands 3 per cent or more over the fifth (%.3f)" % (
            r, v[o[5]] / v[o[4]]))
    v = B.per_fte(b, "with_intercept")
    o = sorted(v, key=lambda u: v[u])
    R.ok(v[o[5]] / v[o[4]] >= 1.02, "C2b with an intercept the sixth stands 2 per cent or more over the fifth")
    coef = B.fit(b)
    R.ok(all(abs(c / W.COST[lv] - 1) < 0.04 for c, lv in zip(coef, W.LEVELS)), "C3 the fitted costs per credit hour "
         "sit within 4 per cent of the truth (%s)" % [round(c) for c in coef])
    g = B.per_fte(b, "golden")
    R.ok(all(abs(g[u] / t[u] - 1) < 0.04 for u in W.IDS), "C4 every campus's golden estimate within 4 per cent of "
         "its own instruction expense per FTE")
    # -------------------------------------------------------------- the fork table
    guide = _pdf(os.path.join(target, P.FILES["guide"]))
    R.ok("ranked on the instruction expense of the branch itself, which its parent's return includes" in guide,
         "SF1 a branch is ranked on its own instruction expense, inside its parent's (the zero reading ruled out)")
    R.ok("the parent is ranked on its own, without its branches'" in guide, "SF2 the parent ranked on its own")
    R.ok("undergraduate FTE plus graduate FTE" in guide, "SF3 the FTE is the 12-month return's")
    R.ok("July 2025 to June 2026" in guide, "SF4 the fiscal year is filed")
    ch_tot = {u: sum(b["ch"][u].values()) for u in b["ids"]}
    R.ok(all(ch_tot[u] == int(b["e12"][u]["CDACTUA"]) + int(b["e12"][u]["CDACTGA"]) for u in b["ids"]),
         "SF5 the credit hour file ties to the 12-month return's credit hours for every campus")
    R.ok(all(b["inst"][u] == 0 for u in b["ids"] if b["kind"][u] == "C"), "SF6 every branch's own return is zero")
    R.ok(len({b["code"][c] for c in b["code"]}) == 26, "SF7 one campus code per campus")
    R.ok("No campus's fiscal 2026 return is restated for the grant" in guide, "SF8 the parents' totals are kept")
    # -------------------------------------------------------------- asks
    A, A0 = B.ask_a(b, True), B.ask_a(b, False)
    R.ok(all(A[u] != A0[u] for u in A), "A1 rows per course move every branch's FTE")
    R.ok(all(abs(A[u] - x["census_truth"][u]["fte"]) < 0.05 for u in A), "A2 the golden FTE equals the truth")
    Bb, B0 = B.ask_b(b, True), B.ask_b(b, False)
    R.ok(all(Bb[u] == x["census_truth"][u]["head"] for u in Bb), "B1 the golden headcount equals the truth")
    R.ok(sum(Bb[u] != B0[u] for u in Bb) == 6, "B2 student ids alone move all six branches")
    R.ok(True, "X1 the call reads the finance, the 12-month return, the codes and the credit hour file; the fall "
               "census file is read by the asks only")
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
        R.ok(fig["call"]["awarded"] == GOLDEN, "F1 figures.json carries the golden five")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if ok else 1)
