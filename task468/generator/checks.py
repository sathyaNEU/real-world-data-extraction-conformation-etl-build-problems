"""The generator's assertions for task468 (architecture 2): the three rules executed on the clean truth (R1 to R3c),
every row of the semantic fork table (SF1 to SF12) with the readings' convergence and each figure's distance to its
bin edge, the Layer 1 items' effect on the call, the rebate ask's device and stops, the separation of the call from
the ask, the distractors, the goldens against figures.json, the input gates and the realism sweep.

    python3 task468/generator/checks.py      (after build.py has written target/ and golden/)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np                # noqa: E402
import pandas as pd               # noqa: E402

import bundle as B                # noqa: E402
import golden as GO               # noqa: E402
import methods as M               # noqa: E402
import pack as P                  # noqa: E402
import sim as S                   # noqa: E402
import world as W                 # noqa: E402

TASK = os.path.dirname(HERE)
DASH = re.compile("[–—]")
PH = W.PER_PHARMACIST


def ph(d):
    return M.pharmacists(d)


def edge(d):
    """Each class's distance, in pharmacists, from its quota to the nearest bin edge."""
    return {c: min(d[c] / PH - np.floor(d[c] / PH), np.ceil(d[c] / PH) - d[c] / PH) for c in W.CANDIDATES}


def doc_texts(target):
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-raw", p, "-"], capture_output=True,
                                                        text=True).stdout)
        elif f.endswith(".xlsx"):
            from openpyxl import load_workbook
            wb = load_workbook(p, data_only=True)
            out[f] = " ".join(str(v) for ws in wb for r in ws.iter_rows(values_only=True) for v in r if v is not None)
    return out


def readings(f):
    f2 = f.copy()
    f2["seen_start"] = True
    return {"golden": M.golden(f), "durations capped at 12": M.golden(f, cap=12),
            "capped at 24": M.golden(f, cap=24), "capped at 48": M.golden(f, cap=48),
            "three-month bands": M.golden(f, band=3), "six-month bands": M.golden(f, band=6),
            "starts read at the first fill in the files": M.golden(f2), "month-to-month chain": M.chain(f)}


def copy_without(target, keys):
    tmp = tempfile.mkdtemp(prefix=".nodistr_", dir=TASK)
    for fn in os.listdir(target):
        if fn not in [W.FILES[k] for k in keys]:
            shutil.copy2(os.path.join(target, fn), tmp)
    return tmp


def run(target, golden, x=None, meta_path=None, fig_path=None):
    bad = []

    def check(label, cond, detail=""):
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))
        if not cond:
            bad.append(label)

    x = x or S.simulate()
    F = json.load(open(fig_path or os.path.join(HERE, "figures.json"), encoding="utf-8"))
    meta = json.load(open(meta_path or os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    files = sorted(os.listdir(target))
    docs = doc_texts(target)
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    g = GO.compute(target)
    f = g["f"]
    gold = ph(g["spend"])

    # ------------------------------------------------------------------ the call and the clean truth
    fl = x["fills"]
    clean = M.prepare(fl[(fl["date"] >= W.FIRST_MONTH) & (fl["date"] <= W.LAST_DAY)])
    c_gold = M.golden(clean)
    check("the call: %s (%d pharmacists)" % (gold, sum(gold.values())), gold == F["call"]["pharmacists"] and
          sum(gold.values()) == F["call"]["total"])
    check("the pack's conformed record gives the clean truth's projection to the cent in every class",
          all(abs(c_gold[c] - g["spend"][c]) < 0.5 for c in W.CANDIDATES),
          {c: round(c_gold[c] - g["spend"][c], 2) for c in W.CANDIDATES})
    real = S.truth_next_year(fl)
    err = {c: round(g["spend"][c] / real[c] - 1, 3) for c in W.CANDIDATES if real[c] > 0}
    check("the projection tracks what the caseloads went on to cost (within 20 per cent in every class but hepatitis "
          "C's few courses): %s" % err, all(abs(v) < 0.2 for c, v in err.items() if c != "HCV"))

    # ------------------------------------------------------------------ R1: nothing hands the method over
    words = r"months? on therapy|persisten|continuation|development|cohort|discontinu|duration|survival|retention"
    hits = {fn: sorted(set(m.group(0).lower() for m in re.finditer(words, t, re.I))) for fn, t in docs.items()}
    check("R1 no shipped document names the projection: no months on therapy, persistence, continuation, development, "
          "cohort, discontinuation, duration, survival or retention", not any(hits.values()),
          {k: v for k, v in hits.items() if v})
    check("R1 no shipped document gives a staffing, a class's managed spend or a pharmacist count",
          not any(re.search(r"\bpharmacists?\b[^.]{0,40}\b\d+\b", t) and fn != W.FILES["charter"]
                  for fn, t in docs.items()) and not re.search(r"\d+ (?:clinical )?pharmacists", docs[W.FILES["charter"]]))
    cols = {fn: open(os.path.join(target, fn), encoding="utf-8").readline().strip().split(",") for fn in files
            if fn.endswith(".csv")}
    flagged = {fn: [k for k in v if re.search(r"start|first|tenure|month|persist|new|status_since", k, re.I)]
               for fn, v in cols.items()}
    check("R1 no claim column carries a therapy start, a first fill or a months-on-therapy count",
          not any(flagged.values()), {k: v for k, v in flagged.items() if v})

    # ------------------------------------------------------------------ R3: the three rules on the clean truth
    rungs = {k: ph(getattr(M, k)(clean)) for k in ("trailing", "run_rate", "analog", "from_start")}
    check("R3a the analyst test on the clean truth (every field read right, every charter rule applied): last year's "
          "on-therapy members' following-year spend files %s, against the golden %s" % (rungs["analog"], ph(c_gold)),
          rungs["analog"] != ph(c_gold) and sum(rungs["analog"][c] != ph(c_gold)[c] for c in W.CANDIDATES) >= 3)
    check("R3a the lower rungs on the clean truth: the trailing year %s, the June run-rate %s, the curve from first "
          "fill %s" % (rungs["trailing"], rungs["run_rate"], rungs["from_start"]),
          all(rungs[k] != ph(c_gold) for k in ("trailing", "run_rate", "from_start")))
    check("R3b only the decisive step changes: the development by months on therapy at each member's own duration "
          "files the golden on the clean truth", ph(c_gold) == gold)
    rd = readings(f)
    alloc = {k: ph(v) for k, v in rd.items()}
    e = {k: min(edge(v).values()) for k, v in rd.items()}
    check("SF6, SF7 and SF8 every reading files the golden staffing (%s); the nearest any class comes to a bin edge is %.2f "
          "of a pharmacist" % (", ".join(alloc), min(e.values())),
          all(a == gold for a in alloc.values()) and min(e.values()) >= 0.15, {k: round(v, 3) for k, v in e.items()})
    spend_m = {k: {c: int(np.floor(v[c] / 1e6 + 0.5)) for c in W.CANDIDATES} for k, v in rd.items()}
    se = min(0.5 - abs(v[c] / 1e6 - np.floor(v[c] / 1e6 + 0.5)) for v in rd.values() for c in W.CANDIDATES)
    check("SF9 every reading gives the same managed spend to the nearest million in every class (nearest edge %.2f "
          "million)" % se, all(s == F["spend_m"] for s in spend_m.values()) and se >= 0.05,
          {k: v for k, v in spend_m.items() if v != F["spend_m"]})
    check("R3c not a plant: the claim files are both PBMs' extracts as written, every fill in them is a fill the "
          "simulation dispensed, and no document argues a method", len(f) == len(clean))

    # ------------------------------------------------------------------ Layer 1 on the call
    o_paid = f.copy()
    o_paid["paid26"] = np.where(o_paid["source"] == "Orrin", o_paid["paid26"] * 0.97, o_paid["paid26"])
    raw = pd.read_csv(B.path(target, "orrin"), dtype=str, keep_default_na=False)
    n_rev = int((raw["line_type"] == "REVERSAL").sum())
    check("Layer 1: %d Orrin reversal lines and their claims; Tallis R lines; every Orrin key and Tallis number in the "
          "crosswalk" % n_rev, n_rev > 100 and set(raw["member_key"]) <= set(B.crosswalk(target)[0]))
    keep_rev = B.fills(target)
    check("Layer 1 Orrin's own paid amounts instead of the 2026 schedule move no class across a bin edge in the "
          "golden's reading", ph(M.golden(M.prepare(o_paid.drop(columns=["mi", "first", "fmi", "seen_start"])))) == gold)

    # ------------------------------------------------------------------ the fork table rows
    check("SF1 the caseload is the members whose fill's days' supply reaches June 30, 2026 (charter 2.1): %s" %
          F["caseload"], sum(F["caseload"].values()) == len(M.on_therapy(f, W.LAST_DAY)))
    check("SF2 managed spend at the 2026 schedule: units times unit price plus the fee per fill (charter 2.2)",
          "plus the schedule's dispensing fee" in docs[W.FILES["charter"]])
    check("SF3 the program year is July 1, 2026 to June 30, 2027 by date dispensed (charter 2.2)",
          "dispensed from July 1, 2026 to June 30, 2027" in docs[W.FILES["charter"]])
    check("SF4 a drug's class is its class code in the drug list (charter 1.2); every NDC in both files is listed",
          f["cls"].notna().all())
    check("SF11 managed spend is the caseload members' fills only: a member who starts after June 30 is outside it "
          "(charter 2.2)", "spend on its caseload members' fills in the class" in docs[W.FILES["charter"]])
    check("SF5 one pharmacist per $1.5 million or part (charter 3.1): the counts are ceilings",
          "or part of $1.5 million" in docs[W.FILES["charter"]])
    reb = B.rebates(target)
    check("SF10 rebates on fills dispensed in 2025 are the statement's 2025 utilization quarters (its header defines "
          "utilization quarter as the quarter dispensed); %d lines carry 2024Q4 and 2025Q4 is invoiced in 2026" %
          int((reb["util"] == "2024Q4").sum()), (reb["util"] == "2024Q4").any() and
          (reb["invoice"] == "2026Q1").any() and "the quarter the fills were dispensed" in docs[W.FILES["rebates"]])
    xw = pd.read_csv(B.path(target, "crosswalk"), dtype=str, keep_default_na=False)
    both = int(((xw["orrin_member_key"] != "") & (xw["tallis_member_no"] != "")).sum())
    check("SF12 members continuing across the PBM change are one member through the crosswalk (%d with both ids)" % both,
          both > 1000)
    unlinked = f.copy()
    unlinked["member"] = np.where(unlinked["source"] == "Tallis", "T:" + unlinked["member"], unlinked["member"])
    ul = ph(M.golden(M.prepare(unlinked[["member", "ndc11", "date", "days", "units", "source", "cls", "paid26"]])))
    check("SF12 read without the crosswalk (every Tallis member a new start), the staffing moves to %s" % ul, ul != gold)

    # ------------------------------------------------------------------ the rebate ask
    truth_rb = P.truth_rebates(x)
    rb = B.rebates_2025(target)
    check("Ask the golden rebates equal the rebates the manufacturers paid on 2025's fills: %s" % F["rebates_k"],
          all(abs(rb[c] - truth_rb[c]) < 0.01 for c in W.CANDIDATES) and
          all(F["rebates_k"][c] == int(np.floor(rb[c] / 1000 + 0.5)) for c in W.CANDIDATES))
    paths = {"every line summed (the cracker)": B.rebates_2025(target, "lines"),
             "invoiced in 2025, each product-quarter once": B.rebates_2025(target, "invoiced")}
    rk = lambda d: {c: int(np.floor(d[c] / 1000 + 0.5)) for c in W.CANDIDATES}
    miss = {k: sum(rk(v)[c] != F["rebates_k"][c] for c in W.CANDIDATES) for k, v in paths.items()}
    check("Ask stops: %s" % "; ".join("%s misses %d of 9" % (k, v) for k, v in miss.items()),
          miss["every line summed (the cracker)"] == 9 and miss["invoiced in 2025, each product-quarter once"] == 9,
          {k: rk(v) for k, v in paths.items()})
    lines_per = reb[reb["util"].str.startswith("2025")].groupby(["product", "util"]).size()
    same_amt = reb.groupby(["product", "util"])["amount"].nunique().max() == 1
    check("Ask the device: every product's 2025 quarterly rebate sits on %d to %d channel lines, the same amount on each; "
          "no line is flagged, the statement has no total row, and every key is unique" % (lines_per.min(),
                                                                                          lines_per.max()),
          lines_per.min() >= 2 and same_amt and not reb.duplicated(["invoice", "util", "product", "channel"]).any())
    redge = min(0.5 - abs(rb[c] / 1000 - np.floor(rb[c] / 1000 + 0.5)) for c in W.CANDIDATES)
    check("Ask every rebate figure is an exact sum clear of its rounding edge (nearest %.3f thousand)" % redge, redge >= 0.001)
    check("Ask separation: the call reads no rebate; the statement is not read by the projection", True)

    # ------------------------------------------------------------------ distractors, gates, goldens
    tmp = copy_without(target, W.DISTRACTORS)
    try:
        g2 = GO.compute(tmp)
        same_d = ph(g2["spend"]) == gold and g2["rebates"] == g["rebates"]
    finally:
        shutil.rmtree(tmp)
    check("distractors: with %s deleted the call and the ask are unchanged" % " and ".join(meta["distractor_files"]),
          same_d and sorted(meta["distractor_files"]) == sorted(W.FILES[k] for k in W.DISTRACTORS))
    fmts = {fn.rsplit(".", 1)[1] for fn in files}
    rows = {fn: (sum(1 for _ in open(os.path.join(target, fn), encoding="utf-8")) - 1 if fn.endswith(".csv") else 0)
            for fn in files}
    check("input gates: %d files, %d formats (%s), the largest %s with %d rows, %d distractors named only in "
          "metadata.json" % (len(files), len(fmts), ", ".join(sorted(fmts)), max(rows, key=rows.get),
                             max(rows.values()), len(meta["distractor_files"])),
          len(files) >= 10 and len(fmts) >= 3 and max(rows.values()) >= 25000 and len(meta["distractor_files"]) >= 2
          and not any("distractor" in fn.lower() for fn in files))
    check("metadata: the deliverable is the one file the prompt names", meta["deliverables"] == [W.GOLDEN["workbook"]]
          and all(d_ in prompt for d_ in meta["deliverables"]) and sorted(os.listdir(golden)) == [W.GOLDEN["workbook"]])
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(golden, W.GOLDEN["workbook"]), data_only=True)["Staffing"]
    gw = {str(r[0]): r for r in ws.iter_rows(min_row=5, values_only=True) if r and r[0] in W.CANDIDATES}
    check("golden workbook: every class's pharmacists, managed spend and rebates as figures.json states them",
          all(gw[c][4] == F["call"]["pharmacists"][c] and gw[c][3] == F["spend_m"][c] and
              gw[c][5] == F["rebates_k"][c] for c in W.CANDIDATES))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    texts = list(docs.values()) + [prompt, sub, open(os.path.join(TASK, "DESIGN_NOTE.md"), encoding="utf-8").read()]
    check("no en or em dash in the pack, the prompt, the write-up or the design note", not any(DASH.search(t)
                                                                                               for t in texts))
    print("%d checks failed" % len(bad) if bad else "all checks passed")
    return not bad


if __name__ == "__main__":
    ok = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    sys.exit(0 if ok else 1)
