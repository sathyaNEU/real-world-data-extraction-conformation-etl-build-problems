"""task482's assertions on the cut pack and on the generator's clean truth (architecture 13): the input gates, the three
rules (R1 the raw material, R2 every Layer 1 item mishandled, R3a the analyst test, R3b the decisive step alone, R3c no
plant), the ladder, the standing family and its cross product, every semantic fork row (SF1 to SF19), the asks with
their devices, fairness and separation, the documents and the realism sweep.

    python3 task482/generator/checks.py          (after build.py)
"""
import copy
import datetime as dt
import itertools
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import world as W   # noqa: E402

D = dt.date
N, FAILS = [0], []
GOLD = ["Ostrelwood Internal Medicine", "Callowglen Family Practice", "Thornelfield Family Medicine",
        "Raddelview Family Physicians", "Jesselford Family Medicine", "Nerrincreek Family Practice",
        "Torrinridge Family Medicine", "Mallowcrest Pediatrics", "Garrowdale Family Practice"]
DEFAULT = ["Ostrelwood Internal Medicine", "Thornelfield Family Medicine", "Jesselford Family Medicine"]
SEASON = ["Ostrelwood Internal Medicine", "Thornelfield Family Medicine", "Jesselford Family Medicine"]
OUT = ["Haddelcrest Internal Medicine", "Wexelmoor Internal Medicine", "Prestelglen Internal Medicine",
       "Birrelhaven Children's Clinic"]
MARGIN = 0.045


def check(label, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def ent(route):
    return [k for k in route if route[k]["enters"]]


def pos(route):
    return {k: v["projected"] / v["threshold"] - 1 for k, v in route.items()}


def margin(route):
    return min(abs(x) for x in pos(route).values())


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def with_claims(p, fn):
    q = dict(p)
    q["claims"] = fn(p["claims"].copy())
    return q


def truth(w):
    """The clean truth's own figures, on the world before any pack is cut: each practice's interim measure on the
    October run, its 2025 figure and same-cut figure, and its true 2026 figure on the final 2026 attribution."""
    col = w["claims"]
    ppl = {q.pid: q for q in w["people"]}
    df = pd.DataFrame(dict(pid=col["pid"], year=col["year"], payer=col["payer"], svc=pd.to_datetime(col["svc"]),
                           paid=pd.to_datetime(col["paid"]), amt=col["allowed"]))
    cf = W.completion_factors(col)
    df["cf"] = [cf[py][m - 1] if m <= 8 else 1.0 for py, m in zip(df.payer, df.svc.dt.month)]

    def fig(members, y, svc_to, paid_to, upto, complete=False):
        sub = df[(df.year == y) & (df.svc <= pd.Timestamp(svc_to)) & (df.paid <= pd.Timestamp(paid_to)) & df.pid.isin(members)]
        a = sub.amt / sub.cf if complete else sub.amt
        tot = a.groupby(sub.pid).sum().to_dict()
        out = {}
        for pid, prac in members.items():
            o = out.setdefault(prac, [0.0, 0])
            o[0] += min(W.CAP, tot.get(pid, 0.0))
            o[1] += W.enrolled_months(ppl[pid], y, upto)
        return out

    def mem(kind, y):
        return {pid: v[0] for py in W.PAYERS for pid, v in w["att"][(kind, py, y)].items()}

    F = fig(mem("final", 2025), 2025, D(2025, 12, 31), W.FINAL_PAID[2025], 12)
    A = fig(mem("aug", 2025), 2025, D(2025, 8, 31), W.FINAL_PAID[2025], 8)
    S = fig(mem("final", 2025), 2025, D(2025, 8, 31), W.FINAL_PAID[2025], 8)
    I = fig(mem("run", 10), 2026, D(2026, 8, 31), D(2026, 9, 30), 8, complete=True)
    TR = fig(mem("final", 2026), 2026, D(2026, 12, 31), W.FINAL_PAID[2026], 12)
    pm = lambda d, k: d[k][0] / d[k][1]
    Fn = sum(v[0] for v in F.values()) / sum(v[1] for v in F.values())
    An = sum(v[0] for v in A.values()) / sum(v[1] for v in A.values())
    out = {}
    for c in W.CODES:
        th = pm(F, c) * W.TREND * (1 - W.MSR)
        out[W.PRACTICE_NAMES[c]] = dict(threshold=th, default=pm(I, c), golden=pm(I, c) * pm(F, c) / pm(A, c),
                                        season=pm(I, c) * pm(F, c) / pm(S, c), pooled=pm(I, c) * Fn / An, true=pm(TR, c))
    return out


def main():
    p = G.load(T)
    gold = G.golden(p)
    dflt = G.default(p)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    figs_path = os.path.join(HERE, "figures.json")
    figs = json.load(open(figs_path)) if os.path.exists(figs_path) else None
    if figs is not None and "practices" not in figs:
        figs = None                     # an earlier architecture's figures, before build.py has run

    # ------------------------------------------------------------ input gates
    files = sorted(os.listdir(T))
    check("gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, ",".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(T, f), "rb")) for f in files if f.endswith((".csv", ".txt")))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d" % big)
    dis = meta["distractor_files"]
    check("gate: two or more distractors, shipped, named in metadata.json",
          len(dis) >= 2 and all(os.path.basename(d) in files for d in dis), ", ".join(dis))
    check("gate: no file name says distractor", not any("distract" in f for f in files))
    dash = []
    texts = {}
    for f in files:
        if f.endswith(".pdf"):
            texts[f] = pdf_text(os.path.join(T, f))
        elif f.endswith((".csv", ".txt", ".json")):
            texts[f] = open(os.path.join(T, f), encoding="utf-8").read()
        if "—" in texts.get(f, "") or "–" in texts.get(f, ""):
            dash.append(f)
    check("gate: no em or en dash in any text file or PDF", not dash, ",".join(dash))

    # ------------------------------------------------------------ the call
    check("call: the golden enters the nine practices", sorted(ent(gold)) == sorted(GOLD), str(ent(gold)))
    check("call: Haddelcrest, Wexelmoor, Prestelglen and Birrelhaven stay one-sided", all(not gold[k]["enters"] for k in OUT))
    check("call: every practice's golden figure sits 4.5 per cent or more from its threshold", margin(gold) >= MARGIN,
          "%.4f" % margin(gold))
    if figs:
        fc = figs["call"]
        check("call: figures.json carries the golden's set", sorted(fc["enter"]) == sorted(GOLD), str(fc["enter"]))
        check("call: figures.json carries every practice's projected figure, benchmark and threshold to the cent",
              all(abs(figs["practices"][k]["projected"] - round(v["projected"], 2)) < 0.006
                  and abs(figs["practices"][k]["benchmark"] - round(v["benchmark"], 2)) < 0.006
                  and abs(figs["practices"][k]["threshold"] - round(v["threshold"], 2)) < 0.006 for k, v in gold.items()))
    else:
        check("call: figures.json written (build.py)", False, "not built yet")

    # ------------------------------------------------------------ R1: the field's raw material ships
    runs = set(pd.read_csv(os.path.join(T, "mlh_attribution_runs_py2025_py2026.csv"), dtype=str).RUN_ID)
    import openpyxl
    sheets = openpyxl.load_workbook(os.path.join(T, "KBP_ATTRIBUTION_PY2025F_PY2026R10.xlsx"), read_only=True).sheetnames
    pruns = set(pd.read_csv(os.path.join(T, "pmh_attribution_py2025_py2026.csv"), dtype=str).run)
    check("R1: the pack carries each payer's final 2025 run and October 2026 run and no 2025 interim run",
          runs == {"PY2025-F", "PY2026-10"} and sheets == ["PY2025 Final", "PY2026 Run 10"] and pruns == {"FINAL", "INTERIM-10"},
          "%s %s %s" % (sorted(runs), sheets, sorted(pruns)))
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += open(os.path.join(T, f), encoding="utf-8").readline().lower().split(",")
    check("R1: no shipped column holds a projected figure, a run-out or a final 2026 attribution",
          not [h for h in heads if re.search(r"project|run.?out|final.?2026|pmpm|benchmark", h)])
    aug = G.attribute(p, 2025, D(2025, 8, 31), D(2025, 9, 30))
    q25 = p["claims"]
    q25 = q25[(q25.ctype == "P") & (q25.year == 2025) & q25.code.isin(p["qualifying"]) & q25.current]
    check("R1: the golden's decisive computation re-runs the 2025 attribution from the 2025 professional claims "
          "(%d qualifying lines, %d members at the same cut)" % (len(q25), len(aug)), len(q25) > 50000 and len(aug) > 15000)

    # ------------------------------------------------------------ R3 on the clean truth
    w = W.build()
    tr = truth(w)
    t_default = [k for k, v in tr.items() if v["default"] <= v["threshold"]]
    t_golden = [k for k, v in tr.items() if v["golden"] <= v["threshold"]]
    t_season = [k for k, v in tr.items() if v["season"] <= v["threshold"]]
    t_pooled = [k for k, v in tr.items() if v["pooled"] <= v["threshold"]]
    t_true = [k for k, v in tr.items() if v["true"] <= v["threshold"]]
    check("R3a: on the clean truth, the interim measure taken as the 2026 figure enters Ostrelwood, Thornelfield and "
          "Jesselford alone", sorted(t_default) == sorted(DEFAULT), str(t_default))
    check("R3b: on the clean truth, the decisive step alone (each practice's own 2025 run-out) enters the golden nine",
          sorted(t_golden) == sorted(GOLD), str(t_golden))
    check("R3b: on the clean truth, the window's correction alone (the final members' own January to August) stays "
          "wrong", sorted(t_season) != sorted(GOLD), str(t_season))
    check("R3b: on the clean truth, one pooled network run-out stays wrong", sorted(t_pooled) != sorted(GOLD), str(t_pooled))
    agree = sum((k in t_true) == (k in GOLD) for k in tr)
    check("R3b: the world's own final 2026 attribution, paid through March 2027, decides %d of 13 practices as the "
          "projection does (a year's run-out is measured, not known)" % agree, agree >= 11, str(sorted(t_true)))
    gp = pos(gold)
    check("R3b: the pack's golden reproduces the clean truth's construction practice by practice",
          all(abs(gp[k] - (tr[k]["golden"] / tr[k]["threshold"] - 1)) < 0.002 for k in gp),
          "%.4f" % max(abs(gp[k] - (tr[k]["golden"] / tr[k]["threshold"] - 1)) for k in gp))

    # ------------------------------------------------------------ the ladder
    season = G.golden(p, season=True)
    pooled = G.golden(p, pooled=True)
    check("ladder L0: the interim measure as the 2026 figure (default) enters Ostrelwood, Thornelfield and Jesselford",
          sorted(ent(dflt)) == sorted(DEFAULT), str(ent(dflt)))
    check("ladder L0: every practice sits 2.5 per cent or more from its threshold on the default",
          all(abs(x) >= 0.025 for x in pos(dflt).values()), "%.4f" % min(abs(x) for x in pos(dflt).values()))
    for basis, what in (("members", "the run's members over the 2025 final run's"),
                        ("months", "the 2025 same-cut member months over the final run's")):
        dl = G.dilution(p, basis)
        check("ladder L2: the members still to come read as costing nothing (%s) enters Birrelhaven beside the golden "
              "nine" % what, sorted(ent(dl)) == sorted(GOLD + ["Birrelhaven Children's Clinic"]), str(ent(dl)))
    check("ladder L1: the interim measure carried by the final 2025 members' own January to August (seasonality "
          "only) enters Ostrelwood, Thornelfield and Jesselford", sorted(ent(season)) == sorted(SEASON), str(ent(season)))
    check("ladder L3: one pooled network run-out enters Haddelcrest, Wexelmoor and Birrelhaven",
          all(pooled[k]["enters"] for k in OUT if k != "Prestelglen Internal Medicine"), str(ent(pooled)))
    check("ladder: every wrong rung differs from the golden", all(sorted(ent(r)) != sorted(GOLD) for r in (dflt, season, pooled)))
    rng_r = [gold[k]["runout"] for k in gold]
    check("ladder: the practices' own run-outs run 0.82 to 1.00, beside a pooled 0.90",
          0.80 < min(rng_r) < 0.85 and 0.98 < max(rng_r) <= 1.0 and 0.88 < pooled[GOLD[0]]["runout"] < 0.92,
          "%.3f to %.3f, pooled %.3f" % (min(rng_r), max(rng_r), pooled[GOLD[0]]["runout"]))

    # ------------------------------------------------------------ the standing family and the fork rows
    fam = {}
    fam["per payer"] = G.golden(p, per_payer=True)
    fam["re-run paid at the current version"] = G.golden(p, first_paid=False)
    fam["re-run on 2025 claims paid by 31 March 2026"] = G.golden(p, cut_paid=False)
    fam["same-cut figure as reported"] = G.golden(p, a_reported=True)
    fam["same-cut members off the final run's fields"] = G.golden(p, aug=G.proxy_members(p))
    fam["ties to the earliest day"] = G.golden(p, aug=G.attribute(p, 2025, D(2025, 8, 31), D(2025, 9, 30), tie="earliest"))
    for name, r in fam.items():
        check("family: %s enters the golden nine (margin %.3f)" % (name, margin(r)), sorted(ent(r)) == sorted(GOLD), str(ent(r)))
    combos = list(itertools.product(("current", "asof"), (True, False), (True, False), (False, True), (False, True)))
    augs = {(fpaid, cutp): G.attribute(p, 2025, D(2025, 8, 31), D(2025, 9, 30) if cutp else G.FINAL_PAID[2025], first_paid=fpaid)
            for fpaid in (True, False) for cutp in (True, False)}
    bad = []
    worst = 1.0
    for ver, fpaid, cutp, rep, ppay in combos:
        r = G.golden(p, version=ver, aug=augs[(fpaid, cutp)], a_reported=rep, per_payer=ppay)
        worst = min(worst, margin(r))
        if sorted(ent(r)) != sorted(GOLD):
            bad.append((ver, fpaid, cutp, rep, ppay))
    check("family: SF5 x SF8 x SF9 x SF10 cross product (%d constructions) enters the golden nine, worst margin %.3f"
          % (len(combos), worst), not bad, str(bad))

    med = G.golden(with_claims(p, lambda x: x[x.ctype != "R"]))
    check("SF1 total cost of care: medical and pharmacy (section 3.1); medical alone, Kesselcrest's settlement basis, "
          "is ruled out by the standard and enters %s" % ("the same set" if sorted(ent(med)) == sorted(GOLD) else "another set"),
          True, str(sorted(ent(med))))
    nocap = G.golden(p, cap=1e12)
    check("SF2 the member cap: USD 250,000 a member-year; no cap converges", sorted(ent(nocap)) == sorted(GOLD))
    check("SF2 the member cap: Merrinlake's USD 150,000 converges too", sorted(ent(G.golden(p, cap=150000.0))) == sorted(GOLD))
    spans_ok = all(s[8:] == "01" and (e[:4] == "9999" or (dt.date.fromisoformat(e) + dt.timedelta(days=1)).day == 1)
                   for _, _, s, e in p["spans"])
    check("SF3 member month: every coverage span starts on a first and ends on a month end, so any month convention is "
          "the same count", spans_ok)
    c = p["claims"]
    straddle = int(((c.year == 2025) & (c.end.dt.year == 2026) & c.current).sum())
    check("SF4 the year's claims by service start; by service end (%d lines straddle the new year) converges" % straddle,
          sorted(ent(G.golden(with_claims(p, lambda x: x.assign(svc=x.end, year=x.end.dt.year))))) == sorted(GOLD) and straddle > 0)
    check("SF5 a claim's version: the version in force at each cut converges", sorted(ent(G.golden(p, version="asof"))) == sorted(GOLD))
    nocomp = G.golden(p, complete=False)
    check("SF6 completion: the interim measure without the factors converges", sorted(ent(nocomp)) == sorted(GOLD),
          "margin %.3f" % margin(nocomp))
    pc = dict(p)
    means = {py: np.mean([v for (pp, m), v in p["cf"].items() if pp == py]) for py in G.PAYERS}
    pc["cf"] = {(py, m): means[py] for (py, m) in p["cf"]}
    check("SF6 completion: each payer's mean factor on its January to August total converges",
          sorted(ent(G.golden(pc))) == sorted(GOLD))
    check("SF7 the interim cap: year to date uncapped converges", sorted(ent(nocap)) == sorted(GOLD))
    check("SF8 the re-run's cut: a visit counted by its first or its current payment, by 30 September or by 31 March, "
          "converges", all(sorted(ent(fam[k])) == sorted(GOLD) for k in ("re-run paid at the current version",
                                                                         "re-run on 2025 claims paid by 31 March 2026")))
    check("SF9 the same-cut figure: paid by 31 March 2026 or as reported at 30 September 2025 converges",
          sorted(ent(fam["same-cut figure as reported"])) == sorted(GOLD))
    check("SF10 the run-out's grain: by practice or by practice and payer converges", sorted(ent(fam["per payer"])) == sorted(GOLD))
    mpi = pd.read_csv(os.path.join(T, "lpn_master_patient_index.csv"), dtype=str)
    span_df = pd.DataFrame(p["spans"], columns=["payer", "member", "start", "end"])
    span_df = span_df.merge(mpi.rename(columns={"PAYER": "payer", "PAYER_MEMBER_ID": "member"}), on=["payer", "member"])
    two = 0
    for y in (2025, 2026):
        yy = span_df[(span_df.start <= "%d-12-31" % y) & (span_df.end >= "%d-01-01" % y)]
        two += int((yy.groupby("LPN_PATIENT_ID").payer.nunique() > 1).sum())
    check("SF11 members: each payer's own; no patient in the index holds two payers' coverage in one year, so "
          "persons and members are the same count", two == 0, "%d" % two)
    ros = copy.deepcopy(p["roster"])
    last = {}
    for r in sorted(ros, key=lambda r: r["start"]):
        last[r["npi"]] = r
    pr = dict(p)
    pr["roster"] = [dict(r, start=D(2018, 7, 1), end=None) for r in last.values()]
    check("SF12 a qualifying service's practice on the date of service; each clinician at their current practice "
          "converges (R2: the roster's moves mishandled)", sorted(ent(G.golden(pr))) == sorted(GOLD))
    check("SF13 ties to the latest qualifying day; to the earliest converges", sorted(ent(fam["ties to the earliest day"])) == sorted(GOLD))
    st = texts["payer_settlement_statements_py2025.pdf"]
    check("SF14 the benchmark: the 2025 network measure times 1.052; the statements' benchmarks carry each payer's own "
          "Schedule A (caps of USD 150,000, 100,000 and 200,000, Kesselcrest medical only)",
          "150,000" in st and "100,000" in st and "200,000" in st and "1.052" in texts["lpn_performance_standard_2026.pdf"])
    check("SF15 at least 2 per cent below: no practice within 4.5 per cent of its threshold, so strict and inclusive "
          "agree", margin(gold) >= MARGIN)
    fp_feed = G.golden(p, f_paid=D(2026, 10, 12))
    check("SF16 the 2025 figure's paid cut-off: 31 March 2026; every 2025 claim the feeds carry converges (R2)",
          sorted(ent(fp_feed)) == sorted(GOLD))
    check("SF17 the interim window: January to August, the October run's service cut (sections 2.3 and 4.1); the "
          "completion factors stop at August", sorted({m for (_, m) in p["cf"]}) == list(range(1, 9)))
    check("SF18 the projection pools each practice's payers by member months (section 3.3); the per-payer projection "
          "weighted by projected member months converges", sorted(ent(fam["per payer"])) == sorted(GOLD))
    rx = c[(c.ctype == "R") & c.current]
    check("SF19 a fill's incurred date: the fill date (the field guide); every pharmacy line carries one date",
          len(rx) > 0 and (rx.svc.notna()).all())

    # ------------------------------------------------------------ R2: every Layer 1 item mishandled
    def keep_superseded(payer):
        def fn(x):
            m = (x.payer == payer) & x.superseded
            x.loc[m, "current"] = True
            return x
        return fn
    for payer, what in (("MLH", "Merrinlake's voided originals kept beside their replacements"),
                        ("KBP", "Kesselcrest's adjusted lines kept beside their reprocessed claims"),
                        ("PMH", "every Pemberglen version summed")):
        r = G.golden(with_claims(p, keep_superseded(payer)))
        check("R2: %s leaves the call (margin %.3f)" % (what, margin(r)), sorted(ent(r)) == sorted(GOLD))
    r = G.golden(p, version="all")
    check("R2: every row of the three claim feeds summed as it stands leaves the call", sorted(ent(r)) == sorted(GOLD),
          "margin %.3f" % margin(r))
    check("R2: 2025 claims paid after 31 March 2026 counted leaves the call", sorted(ent(fp_feed)) == sorted(GOLD))
    check("R2: the roster read at each clinician's current practice leaves the call", sorted(ent(G.golden(pr))) == sorted(GOLD))
    po = dict(p)
    po["spans"] = [(a, b, s_, "2026-10-12" if e[:4] == "9999" else e) for a, b, s_, e in p["spans"]]
    check("R2: open coverage read as ending at the feed date leaves every member month the measure counts",
          G.member_months(po, 2026, 8) == G.member_months(p, 2026, 8) and G.member_months(po, 2025, 12) == G.member_months(p, 2025, 12))
    check("R2: each payer's mean completion factor in place of its monthly factors leaves the call",
          sorted(ent(G.golden(pc))) == sorted(GOLD))
    tins = {t_ for (_, _, _), t_ in p["att"].items()}
    check("Layer 1: every attribution TIN, hyphenated or not, maps to one roster practice once the hyphen is dropped",
          tins <= set(p["tin2prac"]) and len(set(p["tin2prac"].values())) == 13)

    # ------------------------------------------------------------ separation
    ps = dict(p)
    ps["remit"], ps["fees"] = [], {}
    check("separation: the call reads no remittance and no fee schedule (both emptied, every figure identical)",
          all(abs(G.golden(ps)[k]["projected"] - gold[k]["projected"]) < 1e-9 for k in gold))
    recode = with_claims(p, lambda x: x.assign(code=np.where(x.code.isin(G.EM), "99213", x.code)))
    check("separation: every E&M line re-coded to one level leaves every call figure identical (the call reads the "
          "allowed amount and the qualifying day, never the level)",
          all(abs(G.golden(recode)[k]["projected"] - gold[k]["projected"]) < 1e-9 for k in gold))

    # ------------------------------------------------------------ ask A: level 5 paid share
    A = G.ask_a(p)
    check("ask A: thirteen practices' shares", len(A) == 13 and all(5 < v < 30 for v in A.values()), str(A))
    if figs:
        check("ask A: figures.json carries the golden's 13 shares", all(abs(figs["ask_a"][k] - v) < 1e-9 for k, v in A.items()))
    ac, ar = G.ask_a(p, rule="code"), G.ask_a(p, rule="rate")
    check("ask A device: the code on the claim (Kesselcrest's level review unseen) moves all 13 figures",
          all(abs(ac[k] - A[k]) >= 0.05 for k in A), "%d moved" % sum(abs(ac[k] - A[k]) >= 0.05 for k in A))
    check("ask A device: the full level-5 rate only (Merrinlake's halved E&M with a same-day procedure unseen) moves "
          "all 13 figures", all(abs(ar[k] - A[k]) >= 0.05 for k in A), "%d moved" % sum(abs(ar[k] - A[k]) >= 0.05 for k in A))
    v = c[(c.ctype == "P") & (c.year == 2026) & (c.svc <= pd.Timestamp(D(2026, 8, 31))) & c.code.isin(G.EM) & c.current]
    v = v[[G.npi_practice(p, n, d.date()) is not None for n, d in zip(v.npi, v.svc)]]
    cls = {"rate": 0, "review": 0, "half": 0, "other": 0}
    for r in v.itertuples(index=False):
        fac = r.pos in ("19", "22") or (r.payer == "PMH" and r.pos in ("02", "10"))
        rate = p["fees"][(r.payer, r.code)][1 if fac else 0]
        if abs(r.allowed - rate) < 0.005:
            cls["rate"] += 1
        elif r.payer == "KBP" and r.code == "99215" and abs(r.allowed - p["fees"][(r.payer, "99214")][1 if fac else 0]) < 0.005:
            cls["review"] += 1
        elif r.payer == "MLH" and r.mod == "25" and abs(2 * r.allowed - rate) < 0.01:
            cls["half"] += 1
        else:
            cls["other"] += 1
    check("ask A fairness: every network E&M line's allowed amount is its level's rate for its setting, Kesselcrest's "
          "level-4 rate on a reviewed 99215, or half its rate on a Merrinlake modifier-25 line", cls["other"] == 0
          and cls["review"] > 0 and cls["half"] > 0, str(cls))
    mlh_half = v[(v.payer == "MLH") & (v["mod"] == "25")]
    procs = set(x for x, _ in W.MINOR_PROC)
    pc_ = c[(c.payer == "MLH") & c.code.isin(procs) & c.current][["member", "svc", "npi"]]
    keys = set(zip(pc_.member, pc_.svc, pc_.npi))
    halved = [(m_, s_, n_) in keys for m_, s_, n_, a_, cd in zip(mlh_half.member, mlh_half.svc, mlh_half.npi, mlh_half.allowed,
                                                                  mlh_half.code)
              if abs(2 * a_ - p["fees"][("MLH", cd)][0]) < 0.01 or abs(2 * a_ - p["fees"][("MLH", cd)][1]) < 0.01]
    check("ask A fairness: every halved Merrinlake E&M has a same-day minor procedure by the same clinician, and "
          "modifier-25 lines at the full rate exist beside them (a same-day preventive visit)",
          halved and all(halved) and len(mlh_half) > len(halved), "%d halved, %d modifier-25" % (len(halved), len(mlh_half)))
    nf = dict(p)
    nf["fees"] = {k: (vv[0], vv[0]) for k, vv in p["fees"].items()}
    anf = G.ask_a(nf)
    check("ask A hazard: the non-facility rate everywhere moves the hospital-based practices and the Pemberglen "
          "telehealth visits", sum(abs(anf[k] - A[k]) >= 0.05 for k in A) >= 2)

    # ------------------------------------------------------------ ask B: care coordination fees by coverage quarter
    B = G.ask_b(p)
    check("ask B: 39 figures, thirteen practices by three quarters", len(B) == 39)
    if figs:
        check("ask B: figures.json carries the golden's 39 fees",
              all(abs(figs["ask_b"]["%s|Q%d" % k] - v) < 0.005 for k, v in B.items()))
    bc = G.ask_b(p, pmh_by_period=True, keep_other_programs=True)
    br = G.ask_b(p, keep_other_programs=True)
    bf = G.ask_b(p, pmh_by_period=True)
    check("ask B device: every line as posted, Pemberglen by its period and Kesselcrest's lines all kept (the cracker), "
          "misses all 39", all(abs(bc.get(k, 0) - B[k]) >= 0.005 for k in B))
    check("ask B device: Pemberglen's coverage month read from its reference alone keeps only the two paediatric "
          "practices' 6", sum(abs(br.get(k, 0) - B[k]) < 0.005 for k in B) == 6)
    check("ask B device: the standard's fees alone, Pemberglen by its period, misses all 39",
          all(abs(bf.get(k, 0) - B[k]) >= 0.005 for k in B))
    pm_ = pd.read_csv(os.path.join(T, "pmh_ccf_payments_2026.csv"), dtype=str)
    refm = pm_.paymentRef.str.split("-").str[3].str[4:6].astype(int)
    perm = pm_.period.str[5:7].astype(int)
    check("ask B fairness: every Pemberglen reference month is its period's month or earlier, and earlier on %d lines"
          % int((refm < perm).sum()), bool((refm <= perm).all() and (refm < perm).any()))
    kb = [r for r in p["remit"] if r[0] == "KBP"]
    rates = {round(r[3] / r[5], 2) for r in kb}
    check("ask B fairness: every Kesselcrest line is its members at USD 2.80 or at USD 6.50", rates == {2.80, 6.50}, str(rates))
    ma = pd.DataFrame(W.ma_members())
    ok = True
    for r in kb:
        if abs(r[3] - r[5] * 6.50) < 0.005:
            prac = p["tin2prac"][r[1]]
            code = [k for k, n in W.PRACTICE_NAMES.items() if n == prac][0]
            n = int(((ma.practice == code) & (ma.start.apply(lambda d: d.month) <= r[2])).sum())
            ok &= n == r[5]
    check("ask B fairness: each USD 6.50 line's members are the Medicare Advantage file's members attributed to that "
          "TIN by that month", ok)
    check("ask B: Kesselcrest's January and February remittances carry no commercial line",
          all(abs(r[3] - r[5] * 6.50) < 0.005 for r in kb if r[4][5:7] in ("01", "02")))

    # ------------------------------------------------------------ documents
    sd = texts["lpn_performance_standard_2026.pdf"]
    rs = texts["lpn_board_resolution_2026-07.pdf"]
    check("documents: the standard files the attribution, the measure, the cap, the trend and the interim measure",
          all(x in re.sub(r"\s+", " ", sd) for x in ("most days", "250,000", "1.052", "Appendix C", "final run")))
    check("documents: the resolution files the 2 per cent, the final 2026 attribution and the 30 October deadline",
          all(x in re.sub(r"\s+", " ", rs) for x in ("at least 2 per cent below", "final 2026 attribution", "30 October 2026")))
    stump_words = re.compile(r"run-?out|not yet attributed|attributed later|late visit|added after|immature|still to come",
                             re.I)
    hits = [f for f, tx in texts.items() if stump_words.search(tx)]
    check("documents: no shipped text names the run-out or a late-attributed member", not hits, ",".join(hits))
    import pdfplumber
    import pypdf
    key = {"lpn_performance_standard_2026.pdf": ("most days of qualifying primary care", "first paid by 31 March",
                                                 "rounded to the cent", "USD 250,000", "Merrinlake Health Plan USD 3.25"),
           "lpn_board_resolution_2026-07.pdf": ("at least 2 per cent below", "final 2026 attribution", "30 October 2026"),
           "payer_settlement_statements_py2025.pdf": ("Schedule A", "quality multiplier")}
    readers_ok = []
    for fname in [x for x in files if x.endswith(".pdf")]:
        path = os.path.join(T, fname)
        try:
            strict = " ".join(pg.extract_text() or "" for pg in pypdf.PdfReader(path, strict=True).pages)
            lenient = " ".join(pg.extract_text() or "" for pg in pypdf.PdfReader(path, strict=False).pages)
        except Exception as e:  # noqa: BLE001
            strict, lenient = "ERROR " + str(e), ""
        with pdfplumber.open(path) as d:
            plumb = " ".join(pg.extract_text() or "" for pg in d.pages)
        norm = lambda t_: re.sub(r"[^a-z0-9]", "", t_.lower())
        ok = not strict.startswith("ERROR") and norm(strict) == norm(lenient)
        for k_ in key.get(fname, ()):
            ok &= all(norm(k_) in norm(x) for x in (strict, plumb, texts[fname]))
        readers_ok.append(ok)
    check("H25: every shipped PDF opens strict and lenient alike, and its filed clauses read in pypdf, pdfplumber "
          "and pdftotext", all(readers_ok), str(readers_ok))
    guide = texts["lpn_payer_feed_field_guide.txt"]
    check("documents: the field guide names every payer and network file it describes",
          all(f in guide for f in files if not f.endswith(".pdf") and f not in ("lpn_payer_feed_field_guide.txt",
                                                                                  "kbp_medicare_advantage_attribution_2026.xlsx",
                                                                                  "lpn_quality_composite_2025.csv")))

    # ------------------------------------------------------------ R3c and the realism sweep
    counts25 = [gold[k]["members2025"] for k in gold]
    countsr = [gold[k]["members_run"] for k in gold]
    check("R3c: the practices' 2025 final and October run counts are all distinct and none a round hundred",
          len(set(counts25)) == 13 and len(set(countsr)) == 13 and not any(x % 100 == 0 for x in counts25 + countsr))
    check("R3c: no practice's 2025 figure or interim measure is a round dollar",
          all(abs(v["f2025"] - round(v["f2025"])) > 0.005 and abs(v["interim"] - round(v["interim"])) > 0.005 for v in gold.values()))
    mlh = pd.read_csv(os.path.join(T, "mlh_tcoc_claims_2025-01_2026-09.csv"), dtype=str, keep_default_na=False)
    check("R3c: no exact duplicate row in Merrinlake's claims", not mlh.duplicated().any())
    check("realism: every claim paid on or after its service date, 2026 claims paid by 30 September 2026",
          bool((c.paid >= c.svc).all() and (c[c.year == 2026].paid <= pd.Timestamp(D(2026, 9, 30))).all()))
    check("realism: every claim in the feeds paid by the payer's feed date",
          bool((c.paid <= pd.Timestamp(D(2026, 10, 12))).all()))
    names = set()
    for f, tx in texts.items():
        if f.endswith((".pdf", ".txt")):
            for n in W.PEOPLE.values():
                if n in tx:
                    names.add(n)
    check("R3c: the personas in the documents are the three drawn with guard.py names", names == set(W.PEOPLE.values()),
          str(sorted(names)))
    bad = []
    for f in files:
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(T, f)) as z:
                core = z.read("docProps/core.xml").decode()
                blob = b"".join(z.read(n) for n in z.namelist())
            mod = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
            if b"openpyxl" in blob or mod > "2026-10-16T09:00:00Z":
                bad.append(f)
        if f.endswith(".pdf"):
            raw = open(os.path.join(T, f), "rb").read()
            if b"ReportLab" in raw or b"reportlab" in raw:
                bad.append(f)
    check("realism: containers scrubbed (no writing library, no stamp after the cut)", not bad, ",".join(bad))
    pay_dates = sorted({r[4] for r in p["remit"] if r[0] != "PMH"} | set(pm_.paymentDate))
    check("realism: every remittance paid by 16 October 2026", pay_dates[-1] <= "2026-10-16", pay_dates[-1])

    print("\n%d checks, %d failed" % (N[0], len(FAILS)))
    for f in FAILS:
        print("  FAIL", f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
