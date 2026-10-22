"""The generator's assertions on the cut pack and the truth: the three rules (the analyst test on the clean truth),
the ladder and its margins, the golden family's agreement, the fork table's rows (SF1 to SF8), the ask's device and
its separation from the call, and the input gates.

    python3 task482/generator/checks.py [target]"""
import datetime as dt
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
GOLDEN = ["AC", "AV", "CV", "DM", "GS", "KB", "MR"]
DEFAULT = ["AC", "AV", "DM", "DS", "GS", "IR", "KB"]
TYPED = ["AV", "BM", "CV", "GS", "KB", "MR", "RG"]
FAMILY = ("golden", "golden_built", "stock_count_weights", "per_type_regressions", "golden_second_hand")
WRONG = {"pooled": DEFAULT, "pooled_monthly": DEFAULT, "type_weighted": TYPED, "type_weighted_mean": TYPED,
         "hedonic_no_location": ["AV", "BM", "DS", "GS", "IR", "KB", "RG"],
         "median": ["AV", "BM", "CV", "DS", "GS", "KB", "MR", "RG"],
         "per_m2": ["AV", "BM", "DS", "GS", "IR", "KB", "RG"], "ed_type_cells": DEFAULT}


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
    est = x["est"]
    pick = lambda k: sorted(a for a in est if est[a][k] > W.LINE)
    R.ok(pick("pooled") == DEFAULT, "R3a the easy route (the pooled regression with location, one year effect) on the "
         "clean truth files the default seven (%s)" % pick("pooled"))
    R.ok(pick("hedonic") == GOLDEN, "R3b each type's year effect weighted by the stock's value files the golden seven")
    tv = {}
    for a in x["areas"]:
        ga = a["ga"] if a["ga"] is not None else a["growth"]
        g = [a["growth"]] * 3 + [ga]
        p0 = [W.TFLOOR[t] ** W.ELAST * __import__("math").exp(W.TEFF[t]) for t in W.TYPES]
        tv[a["code"]] = sum(m * v * g_ for m, v, g_ in zip(a["stock"], p0, g)) / sum(m * v for m, v in zip(a["stock"], p0))
    R.ok(sorted(k for k, v in tv.items() if v > W.LINE) == GOLDEN, "R3c the true change in the stock's value (each "
         "type's growth weighted by the stock's value) files the golden seven")
    R.ok(pick("type_weighted") == TYPED and pick("hedonic_no_location") != GOLDEN and pick("median") != GOLDEN,
         "R3d every partial correction on the truth misses the golden")
    # -------------------------------------------------------------- the ladder on the cut pack
    ch = {r: B.change(b, r) for r in FAMILY + tuple(WRONG)}
    sets = {r: sorted(k for k, v in ch[r].items() if round(v, 1) > B.LINE) for r in ch}
    for r in FAMILY:
        R.ok(sets[r] == GOLDEN, "L1 %s files the golden seven (%s)" % (r, sets[r]))
    for r, want in WRONG.items():
        R.ok(sets[r] == want, "L2 %s files its rung (%s)" % (r, sets[r]))
    R.ok(all(abs(ch["golden"][k] - B.LINE) >= 1.5 for k in b["areas"]), "C1 every area 1.5 points or more from the "
         "line on the golden")
    for r in FAMILY:
        R.ok(all(abs(ch[r][k] - B.LINE) >= 1.0 for k in b["areas"]), "C2 every area a point or more from the line "
             "under %s" % r)
    log_family = ("golden", "golden_built", "per_type_regressions", "golden_second_hand")
    spread = max(max(ch[r][k] for r in log_family) - min(ch[r][k] for r in log_family) for k in b["areas"])
    R.ok(spread <= 0.7, "C3 the log hedonic forms agree within 0.7 of a point in every area (%.2f)" % spread)
    for r in WRONG:
        if r not in ("pooled", "type_weighted"):
            continue
        R.ok(sum(abs(ch[r][k] - B.LINE) >= 1.0 for k in b["areas"] if (k in sets[r]) != (k in GOLDEN)) ==
             sum(1 for k in b["areas"] if (k in sets[r]) != (k in GOLDEN)), "C4 every area %s misplaces is a point "
             "or more from the line" % r)
    # -------------------------------------------------------------- forks
    bv = B.load(target, vat=False)
    R.ok(B.designated(bv, "golden") == GOLDEN, "SF1 the old layout's VAT-exclusive new-dwelling prices left as filed: "
         "same call")
    keys = [(s["pn"], s["date"]) for s in b["sales"]]
    R.ok(len(keys) == len(set(keys)), "SF2 one record per sale after the two systems' overlap")
    both = sum(1 for s in x["sales"] if P.OLD_WINDOW[0] <= s["filed"] <= P.OLD_WINDOW[1]
               and P.NEW_WINDOW[0] <= s["filed"] <= P.NEW_WINDOW[1])
    R.ok(both > 100, "SF3 the overlap is real: %d filings in both systems" % both)
    allb = dict(b)
    allb["sales"] = [dict(s, market=True) for s in b["sales"]]
    sf4 = B.designated(allb, "golden")
    R.ok(isinstance(sf4, list), "SF4 every sale counted, not filed (the note keeps sales at full market price): %s" % sf4)
    R.ok(sorted(k for k, v in ch["golden"].items() if round(v, 1) >= B.LINE) == GOLDEN, "SF7 at or over 8 per cent: "
         "same call")
    nf = [s for s in b["sales"] if not s["market"] and Y(s)]
    R.ok(len(nf) > 500, "SF5 sales not at full market price exist and are outside the index (%d)" % len(nf))
    excl = dict(b)
    excl["sales"] = [s for s in b["sales"] if s["market"] or not s["new"]]
    R.ok(B.designated(excl, "golden") == GOLDEN, "SF6 the call does not read a housing body's block")
    R.ok(all(abs(round(ch["golden"][k], 1) - ch["golden"][k]) <= 0.05 for k in b["areas"]) and
         all((round(ch["golden"][k], 1) > B.LINE) == (ch["golden"][k] > B.LINE) for k in b["areas"]),
         "SF8 the call is the same on the printed and the unrounded changes")
    # -------------------------------------------------------------- ask: the device and its separation
    A = B.ask(b)
    A0 = B.ask(b, blocks_once=False)
    R.ok(all(A[k][0] != A0[k][0] and A[k][1] != A0[k][1] for k in b["areas"]), "A1 the block device moves both "
         "figures in every area")
    blocks = [s for s in b["sales"] if Y2(s) and not s["market"]]
    grp = {}
    for s in blocks:
        grp.setdefault((s["building"], s["date"], s["price"]), []).append(s)
    multi = [g for g in grp.values() if len(g) > 1]
    R.ok(all(all(s["new"] and s["type"] == "Apartment" for s in g) for g in multi), "A2 every multi-line purchase is a "
         "block of new apartments")
    R.ok(not any(s["market"] for g in multi for s in g), "X1 no device row in the call's population (every block line "
         "is not at full market price)")
    R.ok(len(multi) >= 16, "A3 at least one block in every area's second year (%d blocks)" % len(multi))
    # -------------------------------------------------------------- golden and figures
    fig = json.load(open(fig_path)) if fig_path else None
    if fig:
        R.ok(fig["call"]["designated"] == GOLDEN, "G1 figures.json carries the golden seven")
        R.ok(all(fig["ask"][k]["purchases"] == A[k][0] and fig["ask"][k]["paid"] == int(round(A[k][1]))
                 for k in b["areas"]), "G2 figures.json carries the ask")
        import openpyxl
        wb = openpyxl.load_workbook(os.path.join(gdir, "bso_area_property_price_change_2026.xlsx"), data_only=True)
        ws = wb["Designation"]
        rows = {r[0]: r for r in ws.iter_rows(min_row=5, max_row=20, values_only=True)}
        R.ok(sorted(k for k, r in rows.items() if r[5] == "yes") == GOLDEN, "G3 the workbook designates the golden seven")
        R.ok(all(abs(rows[k][4] - fig["change"][k]) < 1e-9 for k in b["areas"]), "G4 the workbook's changes match")
        q = {r[0]: r for r in wb["Transactions 2025-26"].iter_rows(min_row=5, max_row=20, values_only=True)}
        R.ok(all(q[k][2] == fig["ask"][k]["purchases"] and q[k][3] == fig["ask"][k]["paid"] for k in b["areas"]),
             "G5 the workbook's transactions match")
        R.ok(len(wb["Designation"]._charts) == 1, "G6 the chart is on the designation sheet")
    # -------------------------------------------------------------- input gates and texture
    files = sorted(os.listdir(target))
    R.ok(len(files) >= 10, "I1 ten or more files (%d)" % len(files))
    R.ok(len(set(f.rsplit(".", 1)[1] for f in files)) >= 3, "I2 three or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="cp1252" if "2024-10-01" in f else "utf-8")) - 1
              for f in files if f.endswith(".csv"))
    R.ok(big >= 25000, "I3 a file of 25,000 or more rows (%d)" % big)
    if meta_path:
        meta = json.load(open(meta_path))
        R.ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
             "I4 two distractors named and shipped")
        R.ok(not any(w in f for f in files for w in ("distract", "decoy", "trap")), "I5 no file name names a role")
    late = [s for s in x["sales"] if P.in_extract(s) and s["filed"] > dt.date(2026, 10, 14)]
    R.ok(not late, "D1 nothing filed after the extract")
    for f in files:
        if f.endswith(".pdf"):
            t = _pdf(os.path.join(target, f)).lower()
            R.ok(not re.search(r"hedonic|regression|electoral division.*(control|adjust)|mix|composition|stratif",
                               t), "D2 %s names no method" % f)
    txt = open(os.path.join(target, P.FILES["dictionary"]), encoding="utf-8").read().lower()
    R.ok(not re.search(r"hedonic|regression|block|total for|each line|once", txt), "D3 the dictionary names no method "
         "and no device")
    allt = "".join(open(os.path.join(TASK, "prompt.txt")).read()) if os.path.exists(os.path.join(TASK, "prompt.txt")) \
        else ""
    R.ok("—" not in allt and "–" not in allt, "T1 no dashes in the prompt")
    print("checks: %d run, %d failed" % (R.n, len(R.bad)))
    return not R.bad


def Y(s):
    return B.Y1[0] <= s["date"] <= B.Y2[1]


def Y2(s):
    return B.Y2[0] <= s["date"] <= B.Y2[1]


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    ok = run(t, os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
             fig_path=os.path.join(HERE, "figures.json"))
    raise SystemExit(0 if ok else 1)
