"""The generator's assertions for task468 (architecture 3): the three rules executed on the clean truth (R1 to R3c),
every row of the semantic fork table (SF1 to SF12) with the readings' convergence and each figure's distance to its
bin edge, the Layer 1 items' effect on the call, the rebate ask's device and stops, the separation of the call from
the ask, the distractors, the goldens against figures.json, the input gates and the realism sweep.

    python3 task468/generator/checks.py      (after build.py has written target/ and golden/)
"""
import datetime as dt
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


def readings(f, raw):
    """The golden and every reading the fork table names (SF6 to SF8)."""
    out = {"golden": M.golden(f), "durations capped at 12": M.golden(f, cap=12),
           "capped at 24": M.golden(f, cap=24), "capped at 48": M.golden(f, cap=48),
           "three-month bands": M.golden(f, band=3), "six-month bands": M.golden(f, band=6),
           "month-to-month chain": M.chain(f)}
    for gp in (30, 90, 180):
        out["a new episode after a %d-day lapse" % gp] = M.golden(M.prepare(raw, gap=gp))
    return out


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
    words = (r"months? on therapy|persisten|continuation|development|cohort|discontinu|duration|survival|retention|"
             r"episode|restart|re-?start|lapse|resum|return")
    hits = {fn: sorted(set(m.group(0).lower() for m in re.finditer(words, t, re.I))) for fn, t in docs.items()}
    check("R1 no shipped document names the projection: no months on therapy, persistence, continuation, development, "
          "cohort, discontinuation, duration, survival, retention, episode, restart, lapse or return", not any(hits.values()),
          {k: v for k, v in hits.items() if v})
    check("R1 no shipped document gives a staffing, a class's managed spend or a pharmacist count",
          not any(re.search(r"\bpharmacists?\b[^.]{0,40}\b\d+\b", t) and fn != W.FILES["charter"]
                  for fn, t in docs.items()) and not re.search(r"\d+ (?:clinical )?pharmacists", docs[W.FILES["charter"]]))
    cols = {fn: open(os.path.join(target, fn), encoding="utf-8").readline().strip().split(",") for fn in files
            if fn.endswith(".csv")}
    flagged = {fn: [k for k in v if re.search(r"start|first|tenure|month|persist|new|status_since|episode|gap|lapse", k, re.I)]
               for fn, v in cols.items()}
    check("R1 no claim column carries a therapy start, a first fill or a months-on-therapy count",
          not any(flagged.values()), {k: v for k, v in flagged.items() if v})

    # ------------------------------------------------------------------ R3: the three rules on the clean truth
    rungs = {k: ph(getattr(M, k)(clean)) for k in ("first_fill", "trailing", "run_rate", "analog", "from_start")}
    check("R3a the analyst test on the clean truth (every field read right, every charter rule applied): the "
          "development by months since each member's first fill in the class files %s, against the golden %s" % (
              rungs["first_fill"], ph(c_gold)),
          sum(rungs["first_fill"][c] != ph(c_gold)[c] for c in W.CANDIDATES) >= 3)
    check("R3a the lower rungs on the clean truth: last year's caseload %s, the trailing year %s, the June run-rate "
          "%s, the curve from first fill %s" % (rungs["analog"], rungs["trailing"], rungs["run_rate"],
                                                rungs["from_start"]),
          all(rungs[k] != ph(c_gold) for k in ("analog", "trailing", "run_rate", "from_start")))
    check("R3b only the decisive step changes: the same development with each member's months counted from the start "
          "of the episode of therapy they are in files the golden on the clean truth", ph(c_gold) == gold)
    # the record separates the clocks: members back on a drug after a lapse, early in the new episode, spend like new
    # starters at the same episode month, not like continuing members at the same months since first fill
    obs = []
    for i in range(0, W.N_MONTHS - W.HORIZON):
        co = M.on_therapy(f, M.month_end(i))
        sp = M.spend_after(f, co[["member", "cls"]], i)
        co = co.set_index(["member", "cls"])
        co["next"] = sp.reindex(co.index, fill_value=0.0)
        co = co.reset_index()
        co["Te"], co["Tf"] = i - co["emi"], i - co["fmi"]
        co["back"] = co["eseen"] & (co["emi"] != co["fmi"])
        obs.append(co[co["seen_start"]])
    ob = pd.concat(obs)
    sep = {}
    for c in ("ONC", "AST", "CGR"):
        oc = ob[ob["cls"] == c]
        back = oc[oc["back"] & (oc["Te"] < 6) & (oc["Tf"] >= 12)]
        cont = oc[~oc["back"]].groupby("Tf")["next"].mean()
        new = oc[~oc["back"] & (oc["Tf"] < 6)].groupby("Tf")["next"].mean()
        sep[c] = (len(back), round(float(back["next"].mean() / cont.reindex(back["Tf"]).mean()), 2),
                  round(float(back["next"].mean() / new.reindex(back["Te"]).mean()), 2))
    check("Separation: in the record to June 2025, members back on therapy after a lapse, in their first six months of "
          "the new episode, spend %s of what continuing members at the same months since first fill spend over the next "
          "twelve months and %s of what new starters at the same episode month spend (oral oncology, severe asthma, "
          "CGRP)" % ({c: v[1] for c, v in sep.items()}, {c: v[2] for c, v in sep.items()}),
          all(v[0] >= 30 and v[1] < 0.7 and 0.8 < v[2] < 1.2 for v in sep.values()), sep)
    raw = B.fills(target)
    rd = readings(f, raw)
    alloc = {k: ph(v) for k, v in rd.items()}
    e = {k: min(edge(v).values()) for k, v in rd.items()}
    check("SF6, SF7 and SF13 every reading files the golden staffing (%s); the nearest any class comes to a bin edge is %.2f "
          "of a pharmacist" % (", ".join(alloc), min(e.values())),
          all(a == gold for a in alloc.values()) and min(e.values()) >= 0.15, {k: round(v, 3) for k, v in e.items()})
    spend_m = {k: {c: int(np.floor(v[c] / 1e6 + 0.5)) for c in W.CANDIDATES} for k, v in rd.items()}
    se = min(0.5 - abs(v[c] / 1e6 - np.floor(v[c] / 1e6 + 0.5)) for v in rd.values() for c in W.CANDIDATES)
    check("SF9 every reading gives the same managed spend to the nearest million in every class (nearest edge %.2f "
          "million)" % se, all(s == F["spend_m"] for s in spend_m.values()) and se >= 0.05,
          {k: v for k, v in spend_m.items() if v != F["spend_m"]})
    f2 = f.copy()
    f2["seen_start"] = True
    f2["eseen"] = True
    fs = ph(M.golden(f2))
    check("SF8 a member filling in early 2019 is not read as starting then (the transition notes: \"may have been on "
          "the drug for years before that\"); read as a start, the staffing would be %s" % fs,
          "may have been on the drug for years before that" in docs[W.FILES["transition"]])
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
    op = ph(M.golden(M.prepare(o_paid.drop(columns=["mi", "first", "fmi", "seen_start", "eps", "emi", "eseen"]))))
    check("SF2 Orrin's own paid amounts for the 2019 to 2025 fills instead of the 2026 schedule give %s, another "
          "staffing that charter 2.2 rules out (\"priced at the Tallis 2026 specialty price schedule\")" % op,
          op != gold and "priced at the Tallis 2026 specialty price schedule" in docs[W.FILES["charter"]])

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
    # the statement's contract quarters against the claims' units: only a February-to-January contract year ties
    once = reb.drop_duplicates(["product", "cq"])
    q_units = reb.groupby(["product", "cq"])["units"].sum()
    dl = B.drugs(target)
    cf = B.fills(target)
    cf = cf[cf["source"] == "Orrin"]
    cf["product"] = cf["ndc11"].map(dl["product_name"])

    def tie(start_month):
        bad = 0
        for (prod, cq), u in q_units.items():
            cy, q = int(cq[:4]), int(cq[-1])
            m0 = start_month - 1 + 3 * (q - 1)
            lo = dt.date(cy + m0 // 12, m0 % 12 + 1, 1)
            m1 = m0 + 3
            hi = dt.date(cy + m1 // 12, m1 % 12 + 1, 1)
            got = cf[(cf["product"] == prod) & (cf["date"] >= lo) & (cf["date"] < hi)]["units"].sum()
            bad += abs(got - u) > 0.01
        return bad
    check("SF10 the statement's contract quarters are February to April, May to July, August to October and November "
          "to January: every product-quarter's units tie to the claims on that calendar (%d misses) and none on calendar "
          "quarters (%d of %d miss)" % (tie(2), tie(1), len(q_units)), tie(2) == 0 and tie(1) > 0.8 * len(q_units))
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
    check("Ask the golden rebates equal the rebates the manufacturers paid on the fills dispensed in 2025: %s" %
          F["rebates_k"], all(abs(rb[c] - truth_rb[c]) < 5 for c in W.CANDIDATES) and
          all(F["rebates_k"][c] == int(np.floor(rb[c] / 1000 + 0.5)) for c in W.CANDIDATES),
          {c: round(rb[c] - truth_rb[c], 2) for c in W.CANDIDATES})
    paths = {"contract year 2025 read as calendar 2025, each product-quarter once (the cracker)":
             B.rebates_2025(target, "calendar"),
             "every contract-year 2025 line summed": B.rebates_2025(target, "lines"),
             "the 2025 invoices, each product-quarter once": B.rebates_2025(target, "invoiced")}
    rk = lambda d: {c: int(np.floor(d[c] / 1000 + 0.5)) for c in W.CANDIDATES}
    miss = {k: sum(rk(v)[c] != F["rebates_k"][c] for c in W.CANDIDATES) for k, v in paths.items()}
    check("Ask stops: %s" % "; ".join("%s misses %d of 9" % (k, v) for k, v in miss.items()),
          min(miss.values()) >= 8 and list(miss.values())[0] == 9, {k: rk(v) for k, v in paths.items()})
    lines_per = reb.groupby(["product", "cq"]).size()
    same_amt = reb.groupby(["product", "cq"])["amount"].nunique().max() == 1
    per_unit = (once.set_index(["product", "cq"])["amount"] / q_units).round(4)
    cy_const = per_unit.groupby([per_unit.index.get_level_values(0),
                                 per_unit.index.get_level_values(1).str[:4]]).nunique().max() == 1
    check("Ask the device: no line names a month or a date; each product's rebate per unit is constant within a "
          "contract year (so January 2025's share of 2024-Q4 is that quarter's rate times January's units); every "
          "product-quarter's rebate stands on %d to %d channel lines, the same amount on each; every key is unique" % (
              lines_per.min(), lines_per.max()),
          cy_const and lines_per.min() >= 2 and same_amt and
          not reb.duplicated(["cq", "product", "channel"]).any() and
          not re.search(r"february|january|20\d\d-\d\d-\d\d", docs[W.FILES["rebates"]], re.I))
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
