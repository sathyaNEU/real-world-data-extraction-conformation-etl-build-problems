"""task482's assertions on the cut pack and on the generator's clean truth (architecture 14): the input gates, the three
rules (R1 the raw material, R2 every Layer 1 item mishandled, R3a the analyst test, R3b the decisive step alone, R3c no
plant), the ladder, the standing family and its cross product, every semantic fork row (SF1 to SF26), the asks with
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
        "Birrelhaven Children's Clinic", "Raddelview Family Physicians", "Jesselford Family Medicine",
        "Nerrincreek Family Practice", "Torrinridge Family Medicine"]
DEFAULT = ["Ostrelwood Internal Medicine", "Thornelfield Family Medicine", "Jesselford Family Medicine"]
HELD = {"Mallowcrest Pediatrics": 3, "Garrowdale Family Practice": 4}
RUNOUT = GOLD + list(HELD)
OUT = ["Haddelcrest Internal Medicine", "Wexelmoor Internal Medicine", "Prestelglen Internal Medicine"] + list(HELD)
MARGIN = 0.045


def check(label, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def ent(route):
    return sorted(k for k in route if route[k]["enters"])


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
    October run, its own 2025 run-out at the same cut, the members whose long stay is running at the 2026 cut carried at
    the cap, and its true 2026 figure on the final 2026 attribution paid through March 2027."""
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

    def running(y):
        cut = D(y, 8, 31)
        return {q.pid for q in w["people"] if q.stays.get(y) and q.stays[y]["long"] and q.stays[y]["start"] <= cut
                < q.stays[y]["start"] + dt.timedelta(days=q.stays[y]["los"])}

    h26, h25 = running(2026), running(2025)
    drop = lambda m, h: {k: v for k, v in m.items() if k not in h}
    F, A = fig(drop(mem("final", 2025), h25), 2025, D(2025, 12, 31), W.FINAL_PAID[2025], 12), \
        fig(drop(mem("aug", 2025), h25), 2025, D(2025, 8, 31), W.FINAL_PAID[2025], 8)
    F0 = fig(mem("final", 2025), 2025, D(2025, 12, 31), W.FINAL_PAID[2025], 12)
    I = fig(mem("run", 10), 2026, D(2026, 8, 31), D(2026, 9, 30), 8, complete=True)
    Ir = fig(drop(mem("run", 10), h26), 2026, D(2026, 8, 31), D(2026, 9, 30), 8, complete=True)
    TR = fig(mem("final", 2026), 2026, D(2026, 12, 31), W.FINAL_PAID[2026], 12)
    pm = lambda d, k: d[k][0] / d[k][1]
    run10 = mem("run", 10)
    out = {}
    for c in W.CODES:
        th = round(round(pm(F0, c), 2) * W.TREND, 2) * (1 - W.MSR)
        R = pm(F, c) / pm(A, c)
        held = [pid for pid in h26 if run10.get(pid) == c]
        months = Ir[c][1] * F[c][1] / A[c][1]
        add_m = sum(W.enrolled_months(ppl[pid], 2026) for pid in held)
        gold = (pm(Ir, c) * R * months + W.CAP * len(held)) / (months + add_m)
        out[W.PRACTICE_NAMES[c]] = dict(threshold=th, default=pm(I, c), runout=pm(I, c) * R, golden=gold, true=pm(TR, c),
                                        held=len(held))
    return out, h26, h25


def main():
    p = G.load(T)
    gold = G.golden(p)
    dflt = G.default(p)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    figs_path = os.path.join(HERE, "figures.json")
    figs = json.load(open(figs_path)) if os.path.exists(figs_path) else None
    if figs is not None and "parameters" not in figs:
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
    check("call: the golden enters the eight practices", ent(gold) == sorted(GOLD), str(ent(gold)))
    check("call: Haddelcrest, Wexelmoor, Prestelglen, Mallowcrest and Garrowdale stay one-sided",
          all(not gold[k]["enters"] for k in OUT))
    check("call: every practice's golden figure sits 4.5 per cent or more from its threshold", margin(gold) >= MARGIN,
          "%.4f" % margin(gold))
    held26 = G.open_stays(p, 2026)
    r26 = G.run_members(p, "run2026")
    hc = {}
    for mk in held26:
        hc[r26[mk]] = hc.get(r26[mk], 0) + 1
    check("call: seven members in a stay running at the 2026 cut are past the cap, three at Mallowcrest and four at "
          "Garrowdale", hc == HELD, str(hc))
    check("call: no stay of the kind runs at the 2025 cut", not G.open_stays(p, 2025), str(G.open_stays(p, 2025)))
    if figs:
        fc = figs["call"]
        check("call: figures.json carries the golden's set and the five staying", sorted(fc["enter"]) == sorted(GOLD)
              and sorted(fc["stay"]) == sorted(OUT), str(fc["enter"]))
        check("call: figures.json carries every practice's benchmark and threshold to the cent",
              all(abs(figs["parameters"]["benchmark"][k] - round(v["benchmark"], 2)) < 0.006
                  and abs(figs["parameters"]["threshold"][k] - round(v["threshold"], 2)) < 0.006 for k, v in gold.items()))
        check("call: figures.json carries the held members by practice", dict(figs["parameters"]["steps"]["held"]) == HELD)
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
    heads += open(os.path.join(T, "KBP_CLAIMS_LPN_20261009.txt"), encoding="utf-8").readline().lower().split("|")
    check("R1: no shipped column holds a projected figure, a run-out, a final 2026 attribution, a stay's status or a "
          "discharge flag", not [h for h in heads if re.search(r"project|run.?out|final.?2026|pmpm|benchmark|status_?cd|"
                                                                  r"discharg|admit|stay|census|reserve", h)])
    c = p["claims"]
    stay_prof = c[(c.ctype == "P") & c.current & (c.pos == "21") & c.code.isin(list(G.STAY_CODES))]
    fac = c[(c.ctype == "I") & c.current]
    check("R1: the golden's decisive computation reads the attending physicians' daily inpatient visits (%d lines) and "
          "the facility claims of closed stays (%d)" % (len(stay_prof), len(fac)), len(stay_prof) > 5000 and len(fac) > 2000)
    rates = G.stay_rates(p)
    check("R1: the lowest per-day allowed of the closed stays of 30 days or more is USD 4,580 in neonatal care and USD "
          "6,380 in intensive care", rates == {"NICU": 4580.0, "ICU": 6380.0}, str(rates))

    # ------------------------------------------------------------ R3 on the clean truth
    w = W.build()
    tr, h26, h25 = truth(w)
    t_default = sorted(k for k, v in tr.items() if v["default"] <= v["threshold"])
    t_runout = sorted(k for k, v in tr.items() if v["runout"] <= v["threshold"])
    t_golden = sorted(k for k, v in tr.items() if v["golden"] <= v["threshold"])
    t_true = sorted(k for k, v in tr.items() if v["true"] <= v["threshold"])
    check("R3a: on the clean truth, the easy route with every filed rule applied (each practice's interim measure "
          "carried by its own 2025 run-out) enters ten practices, Mallowcrest and Garrowdale among them",
          t_runout == sorted(RUNOUT), str(t_runout))
    check("R3a: on the clean truth, the interim measure as it stands enters Ostrelwood, Thornelfield and Jesselford",
          t_default == sorted(DEFAULT), str(t_default))
    check("R3b: on the clean truth, the decisive step alone (the members in a long stay running at the cut carried at "
          "the cap) enters the golden eight", t_golden == sorted(GOLD), str(t_golden))
    check("R3b: on the clean truth, seven members are in a long stay running at the 2026 cut and none at the 2025 cut",
          len(h26) == 7 and not h25 and {k: v["held"] for k, v in tr.items() if v["held"]} == HELD)
    agree = sum((k in t_true) == (k in GOLD) for k in tr)
    check("R3b: the world's own final 2026 attribution, paid through March 2027, decides %d of 13 practices as the "
          "golden does (a year's run-out is measured, not known)" % agree, agree >= 12, str(t_true))
    col = w["claims"]
    yr_tot = {}
    for i in range(len(col["pid"])):
        if col["pid"][i] in h26 and col["year"][i] == 2026 and col["paid"][i] <= W.FINAL_PAID[2026]:
            yr_tot[col["pid"][i]] = yr_tot.get(col["pid"][i], 0.0) + col["allowed"][i]
    check("R3b: each member held at the cap is past it on the world's own 2026 claims paid through March 2027 (the "
          "lowest at USD %s)" % "{:,.0f}".format(min(yr_tot.values())), len(yr_tot) == 7 and min(yr_tot.values()) > W.CAP)
    check("R3b: the world's own final 2026 measure is reported for the two practices the step moves, not graded (a "
          "year's run-out is measured, not known)", True,
          str({k: round(tr[k]["true"] / tr[k]["threshold"] - 1, 3) for k in HELD}))
    gp = pos(gold)
    check("R3b: the pack's golden reproduces the clean truth's construction practice by practice",
          all(abs(gp[k] - (tr[k]["golden"] / tr[k]["threshold"] - 1)) < 0.002 for k in gp),
          "%.4f" % max(abs(gp[k] - (tr[k]["golden"] / tr[k]["threshold"] - 1)) for k in gp))

    # ------------------------------------------------------------ the ladder
    runout = G.golden(p, stays=False)
    pooled = G.golden(p, pooled=True, stays=False)
    pooled_s = G.golden(p, pooled=True)
    season = G.golden(p, season=True, stays=False)
    check("ladder L0: the interim measure as the 2026 figure enters Ostrelwood, Thornelfield and Jesselford",
          ent(dflt) == sorted(DEFAULT), str(ent(dflt)))
    check("ladder L0: every practice sits 2.5 per cent or more from its threshold on the interim measure",
          all(abs(x) >= 0.025 for x in pos(dflt).values()), "%.4f" % min(abs(x) for x in pos(dflt).values()))
    check("ladder L1 (default path): each practice's own run-out enters ten, Mallowcrest and Garrowdale among them",
          ent(runout) == sorted(RUNOUT), str(ent(runout)))
    check("ladder L1: Mallowcrest and Garrowdale sit 3 per cent or more under their thresholds on the run-out alone",
          all(pos(runout)[k] <= -0.03 for k in HELD), str({k: round(pos(runout)[k], 4) for k in HELD}))
    for basis, what in (("members", "the run's members over the 2025 final run's"),
                        ("months", "the 2025 same-cut member months over the final run's")):
        dl = G.dilution(p, basis)
        check("ladder L1b: the members still to come read as costing nothing (%s) enters the run-out's ten" % what,
              ent(dl) == sorted(RUNOUT), str(ent(dl)))
    check("ladder L1c: one pooled network run-out enters eleven", len(ent(pooled)) == 11 and ent(pooled) != sorted(GOLD),
          str(ent(pooled)))
    check("ladder L1c: one pooled run-out with the held members at the cap still misses the golden (Haddelcrest and "
          "Wexelmoor in, Callowglen out)", ent(pooled_s) != sorted(GOLD), str(ent(pooled_s)))
    check("ladder: the final 2025 members' own January to August (seasonality only) enters the interim's three",
          ent(season) == sorted(DEFAULT), str(ent(season)))
    rng_r = [gold[k]["runout"] for k in gold]
    check("ladder: the practices' own run-outs run 0.82 to 0.99, beside a pooled 0.88",
          0.80 < min(rng_r) < 0.85 and 0.97 < max(rng_r) <= 1.0 and 0.87 < pooled_s[GOLD[0]]["runout"] < 0.92,
          "%.3f to %.3f, pooled %.3f" % (min(rng_r), max(rng_r), pooled_s[GOLD[0]]["runout"]))

    # ------------------------------------------------------------ the standing family and its cross product
    augs = {(fpaid, cutp): G.attribute(p, 2025, D(2025, 8, 31), D(2025, 9, 30) if cutp else G.FINAL_PAID[2025], first_paid=fpaid)
            for fpaid in (True, False) for cutp in (True, False)}
    combos = list(itertools.product(("current", "asof"), list(augs), (False, True), (False, True), ("cap", "all"),
                                    (True, False)))
    bad = []
    worst = 1.0
    for ver, ak, rep, ppay, rule, s25 in combos:
        r = G.golden(p, version=ver, aug=augs[ak], a_reported=rep, per_payer=ppay, stay_rule=rule, stays25=s25)
        worst = min(worst, margin(r))
        if ent(r) != sorted(GOLD):
            bad.append((ver, ak, rep, ppay, rule, s25))
    check("family: SF5 x SF8 x SF9 x SF10 x SF22 x SF24 cross product (%d constructions) enters the golden eight, worst "
          "margin %.3f" % (len(combos), worst), not bad, str(bad[:4]))
    fam = {}
    fam["per payer"] = G.golden(p, per_payer=True)
    fam["re-run paid at the current version"] = G.golden(p, first_paid=False)
    fam["re-run on 2025 claims paid by 31 March 2026"] = G.golden(p, cut_paid=False)
    fam["same-cut figure as reported"] = G.golden(p, a_reported=True)
    fam["same-cut members off the final run's fields"] = G.golden(p, aug=G.proxy_members(p))
    fam["ties to the earliest day"] = G.golden(p, aug=G.attribute(p, 2025, D(2025, 8, 31), D(2025, 9, 30), tie="earliest"))
    fam["every open stay at its amount so far plus its days"] = G.golden(p, stay_rule="all")
    for name, r in fam.items():
        check("family: %s enters the golden eight (margin %.3f)" % (name, margin(r)), ent(r) == sorted(GOLD), str(ent(r)))

    # ------------------------------------------------------------ the semantic fork rows
    med = G.golden(with_claims(p, lambda x: x[x.ctype != "R"]))
    check("SF1 total cost of care: medical and pharmacy (section 3.1); medical alone, Kesselcrest's settlement basis, "
          "is ruled out by the standard and enters %s" % ("the same set" if ent(med) == sorted(GOLD) else "another set"),
          True, str(ent(med)))
    c150 = G.golden(p, cap=150000.0)
    check("SF2 the member cap: USD 250,000 a member-year (section 3.1); Merrinlake's own Schedule A cap of USD 150,000 "
          "files another call, so the standard's filed figure decides it", ent(c150) != sorted(GOLD) and
          "USD 250,000" in re.sub(r"\s+", " ", texts["lpn_performance_standard_2026.pdf"]), str(ent(c150)))
    spans_ok = all(s[8:] == "01" and (e[:4] == "9999" or (dt.date.fromisoformat(e) + dt.timedelta(days=1)).day == 1)
                   for _, _, s, e in p["spans"])
    check("SF3 member month: every coverage span starts on a first and ends on a month end, so any month convention is "
          "the same count", spans_ok)
    straddle = int(((c.year == 2025) & (c.end.dt.year == 2026) & c.current).sum())
    def by_end(x):
        m = x.end.dt.year != x.svc.dt.year
        x.loc[m, "svc"] = x.loc[m, "end"]
        x["year"] = x.svc.dt.year
        return x
    check("SF4 the year's claims by service start; by service end (%d lines straddle the new year) converges" % straddle,
          ent(G.golden(with_claims(p, by_end))) == sorted(GOLD) and straddle > 0)
    check("SF5 a claim's version: the version in force at each cut converges", ent(G.golden(p, version="asof")) == sorted(GOLD))
    nocomp = G.golden(p, complete=False)
    check("SF6 completion: the interim measure without the factors converges", ent(nocomp) == sorted(GOLD),
          "margin %.3f" % margin(nocomp))
    pc = dict(p)
    means = {py: np.mean([v for (pp, m), v in p["cf"].items() if pp == py]) for py in G.PAYERS}
    pc["cf"] = {(py, m): means[py] for (py, m) in p["cf"]}
    check("SF6 completion: each payer's mean factor on its January to August total converges", ent(G.golden(pc)) == sorted(GOLD))
    nocap = G.golden(p, cap=1e12)
    check("SF7 the interim cap: each member's year to date capped (section 4.1); uncapped converges", ent(nocap) == sorted(GOLD),
          str(ent(nocap)))
    check("SF8 the re-run's cut: a visit counted by its first or its current payment, by 30 September or by 31 March, "
          "converges", all(ent(fam[k]) == sorted(GOLD) for k in ("re-run paid at the current version",
                                                                 "re-run on 2025 claims paid by 31 March 2026")))
    check("SF9 the same-cut figure: paid by 31 March 2026 or as reported at 30 September 2025 converges",
          ent(fam["same-cut figure as reported"]) == sorted(GOLD))
    check("SF10 the run-out's grain: by practice or by practice and payer converges", ent(fam["per payer"]) == sorted(GOLD))
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
          "converges (R2: the roster's moves mishandled)", ent(G.golden(pr)) == sorted(GOLD))
    check("SF13 ties to the latest qualifying day; to the earliest converges", ent(fam["ties to the earliest day"]) == sorted(GOLD))
    st = texts["payer_settlement_statements_py2025.pdf"]
    check("SF14 the benchmark: the 2025 network measure times 1.052; the statements' benchmarks carry each payer's own "
          "Schedule A (caps of USD 150,000, 100,000 and 200,000, Kesselcrest medical only)",
          "150,000" in st and "100,000" in st and "200,000" in st and "1.052" in texts["lpn_performance_standard_2026.pdf"])
    check("SF15 at least 2 per cent below: no practice within 4.5 per cent of its threshold, so strict and inclusive "
          "agree", margin(gold) >= MARGIN)
    fp_feed = G.golden(p, f_paid=D(2026, 10, 12))
    check("SF16 the 2025 figure's paid cut-off: 31 March 2026; every 2025 claim the feeds carry converges (R2)",
          ent(fp_feed) == sorted(GOLD))
    check("SF17 the interim window: January to August, the October run's service cut (sections 2.3 and 4.1); the "
          "completion factors stop at August", sorted({m for (_, m) in p["cf"]}) == list(range(1, 9)))
    check("SF18 the projection pools each practice's payers by member months (section 3.3); the per-payer projection "
          "weighted by projected member months converges", ent(fam["per payer"]) == sorted(GOLD))
    rx = c[(c.ctype == "R") & c.current]
    check("SF19 a fill's incurred date: the fill date (the field guide); every pharmacy line carries one date",
          len(rx) > 0 and bool(rx.svc.notna().all()))
    # SF20: a stay running at the cut, read from the daily visits
    o_all = G.open_stays(p, 2026, rule="all")
    ends = []
    for mk, (kind, first, days) in held26.items():
        g_ = stay_prof[(stay_prof.payer == mk[0]) & (stay_prof.member == mk[1]) & (stay_prof.svc <= pd.Timestamp(D(2026, 8, 31)))
                       & (stay_prof.first_paid <= pd.Timestamp(D(2026, 9, 30)))]
        last = g_.svc.max()
        f_ = fac[(fac.payer == mk[0]) & (fac.member == mk[1]) & (fac.first_paid <= pd.Timestamp(D(2026, 9, 30)))
                 & (fac.svc <= pd.Timestamp(first) + pd.Timedelta(days=1)) & (fac.end >= last)]
        ends.append(((D(2026, 8, 31) - last.date()).days, len(f_)))
    check("SF20 a stay running at the cut: the attending physicians' daily visits run to within days of 31 August and no "
          "facility claim covers them; each of the seven's visits runs to within %d days of the cut with no facility "
          "claim covering the stay in the feeds" % max(e[0] for e in ends), all(e[0] <= 6 and e[1] == 0 for e in ends),
          str(ends))
    alt_rates = G.stay_day_amounts(p)
    alt = [mk for mk, (kind, first, days) in held26.items() if days * alt_rates[kind] < G.CAP]
    check("SF21 the per-day amount the running stays are priced at: the lowest of the closed stays of 30 days or more "
          "of the same kind; the median of every closed stay of the kind (USD %s and %s) puts the same seven past the cap"
          % ("{:,.0f}".format(alt_rates["NICU"]), "{:,.0f}".format(alt_rates["ICU"])), not alt)
    days_min = min(v[2] for v in held26.values())
    check("SF21 the seven are past the cap with room: the fewest days to the cut is %d, and the cap at the lowest "
          "per-day amount is reached in %d neonatal or %d intensive care days" % (
              days_min, int(np.ceil(G.CAP / rates["NICU"])), int(np.ceil(G.CAP / rates["ICU"]))),
          all(v[2] * rates[v[0]] >= 1.25 * G.CAP for v in held26.values()))
    check("SF22 which running stays are carried: those past the cap at the cap; every running stay (%d) at the lesser "
          "of the cap and its amount so far plus its days at the median per-day amount converges" % len(o_all),
          ent(fam["every open stay at its amount so far plus its days"]) == sorted(GOLD))
    nom = G.golden(p, stay_months=False)
    check("SF23 the held members' months: each one's 2026 months of coverage counted (section 3.3); left out converges",
          ent(nom) == sorted(GOLD))
    check("SF24 the 2025 run-out without the members in a stay running at the 2025 cut: no stay of the kind runs at the "
          "2025 cut, so the reading is identical", not G.open_stays(p, 2025) and ent(G.golden(p, stays25=False)) == sorted(GOLD))
    k = pd.read_csv(os.path.join(T, "KBP_CLAIMS_LPN_20261009.txt"), sep="|", dtype=str, keep_default_na=False)
    ub = k[k.CLAIM_FORM == "UB04"]
    rb = ub.REVENUE.str.match(r"^01\d\d$|^02[01]\d$")
    check("SF25 Kesselcrest's inpatient claims: bill type 011x; the room-and-board revenue codes read the same claims",
          bool((ub.BILL_TYPE.str.startswith("011") == rb).all()), "%d disagree" % int((ub.BILL_TYPE.str.startswith("011") != rb).sum()))
    nb = [q for q in w["people"] if q.born is not None and q.born.year == 2026]
    ids = W.member_ids(w["people"])
    span_start = {(py, m): s for py, m, s, e in p["spans"]}
    ok = all(span_start.get((dict(B="MLH", M="KBP", T="PMH")[q.payer[2026]], ids[(q.pid, q.payer[2026])]), "2026-%02d-01" % q.born.month)
             == "2026-%02d-01" % q.born.month for q in nb)
    check("SF26 a newborn's coverage: from the month of birth in every payer's coverage file (the spans), %d newborns" % len(nb),
          ok and len(nb) > 20)

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
        check("R2: %s leaves the call (margin %.3f)" % (what, margin(r)), ent(r) == sorted(GOLD))
    r = G.golden(p, version="all")
    check("R2: every row of the three claim feeds summed as it stands leaves the call", ent(r) == sorted(GOLD),
          "margin %.3f" % margin(r))
    check("R2: 2025 claims paid after 31 March 2026 counted leaves the call", ent(fp_feed) == sorted(GOLD))
    check("R2: the roster read at each clinician's current practice leaves the call", ent(G.golden(pr)) == sorted(GOLD))
    po = dict(p)
    po["spans"] = [(a, b, s_, "2026-10-12" if e[:4] == "9999" else e) for a, b, s_, e in p["spans"]]
    check("R2: open coverage read as ending at the feed date leaves every member month the measure counts",
          G.member_months(po, 2026, 8) == G.member_months(p, 2026, 8) and G.member_months(po, 2025, 12) == G.member_months(p, 2025, 12))
    check("R2: each payer's mean completion factor in place of its monthly factors leaves the call", ent(G.golden(pc)) == sorted(GOLD))
    tins = {t_ for (_, _, _), t_ in p["att"].items()}
    check("Layer 1: every attribution TIN, hyphenated or not, maps to one roster practice once the hyphen is dropped",
          tins <= set(p["tin2prac"]) and len(set(p["tin2prac"].values())) == 13)

    # ------------------------------------------------------------ separation
    ps = dict(p)
    ps["fees"] = {}
    check("separation: the call reads no fee schedule (emptied, every figure identical)",
          all(abs(G.golden(ps)[k]["projected"] - gold[k]["projected"]) < 1e-9 for k in gold))
    recode = with_claims(p, lambda x: x.assign(code=np.where(x.code.isin(G.EM), "99213", x.code)))
    check("separation: every E&M line re-coded to one level leaves every call figure identical (the call reads the "
          "allowed amount and the qualifying day, never the level)",
          all(abs(G.golden(recode)[k]["projected"] - gold[k]["projected"]) < 1e-9 for k in gold))
    nomod = with_claims(p, lambda x: x.assign(mod=""))
    check("separation: every modifier blanked leaves every call figure identical",
          all(abs(G.golden(nomod)[k]["projected"] - gold[k]["projected"]) < 1e-9 for k in gold))

    def fold(x):
        """Each Kesselcrest claim's adjustment line folded into its service line, the claim's allowed unchanged."""
        isadj = (x.payer == "KBP") & (x.code == "") & (x.rev == "") & (x.ctype != "R")
        tot = x.groupby("clm").allowed.transform("sum")
        y = x[~isadj].copy()
        y.loc[y.clm.isin(set(x.clm[isadj])), "allowed"] = tot[~isadj][y.clm.isin(set(x.clm[isadj]))]
        return y
    folded = with_claims(p, fold)
    check("separation: Kesselcrest's claim adjustment lines folded into their service lines leave every call figure "
          "identical", all(abs(G.golden(folded)[k]["projected"] - gold[k]["projected"]) < 1e-6 for k in gold))

    # ------------------------------------------------------------ ask A: level 5 paid share
    A = G.ask_a(p)
    check("ask A: thirteen practices' shares", len(A) == 13 and all(5 < v < 30 for v in A.values()), str(A))
    if figs:
        check("ask A: figures.json carries the golden's 13 shares", all(abs(figs["ask_a"][k] - v) < 1e-9 for k, v in A.items()))
    for rule, what in (("code", "the code on the claim (the mirror)"),
                       ("line", "each visit at the level whose rate its own line's allowed amount equals (Kesselcrest's "
                                "review unseen, Merrinlake's halved level 5 read at its level 3 rate)"),
                       ("line_mlh", "the line's allowed with Merrinlake's halved visits found (round 1's cracker; "
                                    "Kesselcrest's review unseen)"),
                       ("halve_all", "every Merrinlake modifier 25 visit read at twice its line's allowed amount"),
                       ("claim_only", "the claim's allowed with Merrinlake's halved visits read at the level they match")):
        x = G.ask_a(p, rule=rule)
        moved = sum(abs(x[k_] - A[k_]) >= 0.05 for k_ in A)
        check("ask A device: %s moves all 13 figures" % what, moved == 13, "%d moved" % moved)
    v = c[(c.ctype == "P") & (c.year == 2026) & (c.svc <= pd.Timestamp(D(2026, 8, 31))) & c.code.isin(G.EM) & c.current]
    v = v[[G.npi_practice(p, n, d.date()) is not None for n, d in zip(v.npi, v.svc)]]
    cur = c[(c.ctype == "P") & (c.year == 2026) & (c.svc <= pd.Timestamp(D(2026, 8, 31))) & c.current]
    ctot = cur.groupby("clm").allowed.sum().to_dict()
    nlines = cur.groupby("clm").size().to_dict()
    other = cur[~cur.code.isin(G.EM) & ~cur.code.isin(list(p["qualifying"])) & (cur.code != "")]
    proc = set(zip(other.payer, other.member, other.npi, other.svc))
    prevc = cur[cur.code.str.match(r"^993[89]\d$")]
    prevs = set(zip(prevc.payer, prevc.member, prevc.npi, prevc.svc))
    cls = {"rate": 0, "review": 0, "half beside a procedure": 0, "other": 0}
    m25 = {"half beside a procedure": 0, "full beside a preventive visit": 0, "full beside neither": 0, "other": 0}
    kline = {"at its code's rate": 0, "other": 0}
    for r in v.itertuples(index=False):
        fac_ = r.pos in ("19", "22") or (r.payer == "PMH" and r.pos in ("02", "10"))
        rate = p["fees"][(r.payer, r.code)][1 if fac_ else 0]
        key = (r.payer, r.member, r.npi, r.svc)
        amt = ctot[r.clm]
        half = abs(2 * amt - rate) < 0.01
        if r.payer == "KBP":
            kline["at its code's rate" if abs(r.allowed - rate) < 0.005 else "other"] += 1
        if r.payer == "MLH" and r.mod == "25":
            if half and key in proc:
                m25["half beside a procedure"] += 1
            elif abs(amt - rate) < 0.005 and key in prevs and key not in proc:
                m25["full beside a preventive visit"] += 1
            elif abs(amt - rate) < 0.005 and key not in proc:
                m25["full beside neither"] += 1
            else:
                m25["other"] += 1
        if abs(amt - rate) < 0.005 and nlines[r.clm] == 1:
            cls["rate"] += 1
        elif (r.payer == "KBP" and r.code == "99215" and nlines[r.clm] == 2 and
              abs(amt - p["fees"][(r.payer, "99214")][1 if fac_ else 0]) < 0.005):
            cls["review"] += 1
        elif r.payer == "MLH" and r.mod == "25" and half and key in proc:
            cls["half beside a procedure"] += 1
        else:
            cls["other"] += 1
    check("ask A fairness: every network E&M claim's allowed amount is its level's rate for its setting, Kesselcrest's "
          "level 4 rate on a reviewed 99215 (the line at the 99215 rate, the claim's second line the difference), or half "
          "its rate on a Merrinlake modifier 25 visit beside a same-day minor procedure by the same clinician",
          cls["other"] == 0 and cls["review"] > 300 and cls["half beside a procedure"] > 0, str(cls))
    check("ask A silence: every Kesselcrest E&M line's own allowed amount is its code's rate for its setting, so a check "
          "at the line finds no level review", kline["other"] == 0 and kline["at its code's rate"] > 5000, str(kline))
    kc = c[(c.payer == "KBP") & c.current]
    adj = kc[(kc.code == "") & (kc.rev == "") & (kc.ctype != "R")]
    on_em = adj.clm.isin(set(kc.clm[kc.code.isin(G.EM)]))
    check("ask A twin: Kesselcrest's lines with no procedure, revenue or drug code are adjustments on outpatient facility "
          "claims as well as on reviewed visits (%d facility, %d visits), each the claim's second line" % (
              int((~on_em).sum()), int(on_em.sum())),
          (~on_em).sum() > 500 and on_em.sum() > 300 and bool((adj.allowed < 0).all()) and
          all(nl == 2 for nl in kc[kc.clm.isin(set(adj.clm))].groupby("clm").size()))
    dup_md = int(v.groupby(["payer", "member", "svc"]).size().gt(1).sum())
    check("ask A unit: no member has two established-patient visits with the practice's clinicians on one day, so a line, "
          "a member-day-clinician and a member-day count the same visits", dup_md == 0, "%d member-days" % dup_md)
    gold_raw = {}
    for prac, payer, code, lvl in G.paid_levels(p, "golden"):
        o_ = gold_raw.setdefault(prac, [0, 0])
        o_[0] += int(lvl == 5)
        o_[1] += 1
    dist = {k_: abs((100.0 * a_ / b_ * 10) % 1 - 0.5) / 10 for k_, (a_, b_) in gold_raw.items()}
    check("ask A rounding: every share sits at least 0.005 points from its rounding boundary (closest %s at %.4f)" % (
        min(dist, key=dist.get), min(dist.values())), min(dist.values()) >= 0.005)
    check("ask A fairness: every Merrinlake modifier 25 visit beside a same-day minor procedure by the same clinician is "
          "at half its rate, and every other is at its full rate", m25["other"] == 0 and m25["half beside a procedure"] > 1000
          and m25["full beside a preventive visit"] > 500, str(m25))
    mlh = {code: p["fees"][("MLH", code)] for code in G.EM}
    check("ask A device: Merrinlake's 2026 level 5 rate is twice its level 3 rate in both settings, so a halved level 5 "
          "equals a full level 3", all(abs(mlh["99215"][i] - 2 * mlh["99213"][i]) < 0.005 for i in (0, 1)), str(mlh))
    nf = dict(p)
    nf["fees"] = {k_: (vv[0], vv[0]) for k_, vv in p["fees"].items()}
    anf = G.ask_a(nf)
    check("ask A hazard: the non-facility rate everywhere moves the hospital-based practices", sum(abs(anf[k_] - A[k_]) >= 0.05
                                                                                                for k_ in A) >= 2)

    # ------------------------------------------------------------ distractors: the care coordination remittances
    remit = ("mlh_care_coordination_remittance_2026.csv", "KBP_CCF_REMIT_2026.xlsx", "pmh_ccf_payments_2026.csv")
    gsrc = open(os.path.join(HERE, "golden.py")).read()
    check("distractors: the golden opens none of the three remittances", not any(
        x.split("_2026")[0].split("_REMIT")[0] in gsrc for x in remit))
    mr = pd.read_csv(os.path.join(T, remit[0]), dtype=str)
    pm_ = pd.read_csv(os.path.join(T, remit[2]), dtype=str)
    import openpyxl
    kr = [r for r in openpyxl.load_workbook(os.path.join(T, remit[1]), read_only=True).active.iter_rows(values_only=True)][1:]
    check("distractors: every remittance line's amount is its member count times the standard's fee for its payer",
          all(abs(float(x.PMT_AMT) - int(x.MBR_CNT) * W.CCF_RATE["B"]) < 0.005 for x in mr.itertuples()) and
          all(abs(float(x.amount) - int(x.memberCount) * W.CCF_RATE["T"]) < 0.005 for x in pm_.itertuples()) and
          all(abs(float(r[5]) - int(r[4]) * W.CCF_RATE["M"]) < 0.005 for r in kr if r[0] is not None))
    late = [x for x in mr.itertuples() if x.LINE_TYP == "RETRO" and int(x.PMT_RUN[-2:]) >= 7]
    check("distractors: every Merrinlake retro line from its July run carries a member count that is a multiple of the "
          "months from its coverage month through the month before the run (%d lines)" % len(late),
          all(int(x.MBR_CNT) % (int(x.PMT_RUN[-2:]) - int(x.COV_MO[4:6])) == 0 for x in late) and len(late) > 100)

    # ------------------------------------------------------------ documents
    sd = texts["lpn_performance_standard_2026.pdf"]
    rs = texts["lpn_board_resolution_2026-07.pdf"]
    sdn = re.sub(r"\s+", " ", sd)
    check("documents: the standard files the attribution, the measure, the cap, the trend, the interim measure and the "
          "factors' large-claim rule", all(x in sdn for x in ("most days", "250,000", "1.052", "Appendix C", "final run",
                                                              "over USD 100,000 are left out")))
    check("documents: the resolution files the 2 per cent, the final 2026 attribution and the 30 October deadline",
          all(x in re.sub(r"\s+", " ", rs) for x in ("at least 2 per cent below", "final 2026 attribution", "30 October 2026")))
    stump_words = re.compile(r"run-?out|not yet attributed|attributed later|late visit|added after|immature|still to come|"
                             r"still in (the )?hospital|open stay|stays? (still )?(open|running)|not yet billed|billed at "
                             r"discharge|at discharge|known (large )?claim|case reserve|catastroph|stop-?loss|in hospital",
                             re.I)
    hits = [f for f, tx in texts.items() if stump_words.search(tx)]
    check("documents: no shipped text names the run-out, a stay running at the cut or its billing", not hits, ",".join(hits))
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
    check("documents: the field guide says nothing of how Merrinlake's retro lines group months or of a halved E&M",
          not re.search(r"half|halv|consolidat|group|cohort|first month|several months", guide, re.I))

    # ------------------------------------------------------------ R3c and the realism sweep
    counts25 = [gold[k_]["members2025"] for k_ in gold]
    countsr = [gold[k_]["members_run"] for k_ in gold]
    check("R3c: the practices' 2025 final and October run counts are all distinct and none a round hundred",
          len(set(counts25)) == 13 and len(set(countsr)) == 13 and not any(x % 100 == 0 for x in counts25 + countsr))
    check("R3c: no practice's 2025 figure or interim measure is a round dollar",
          all(abs(v_["f2025"] - round(v_["f2025"])) > 0.005 and abs(v_["interim"] - round(v_["interim"])) > 0.005
              for v_ in gold.values()))
    mlhc = pd.read_csv(os.path.join(T, "mlh_tcoc_claims_2025-01_2026-09.csv"), dtype=str, keep_default_na=False)
    check("R3c: no exact duplicate row in Merrinlake's claims", not mlhc.duplicated().any())
    check("realism: every claim paid on or after its service date, 2026 claims paid by 30 September 2026",
          bool((c.paid >= c.svc).all() and (c[c.year == 2026].paid <= pd.Timestamp(D(2026, 9, 30))).all()))
    check("realism: every facility claim of a stay paid after its last day", bool((fac.paid >= fac.end).all()))
    check("realism: every claim in the feeds paid by the payer's feed date", bool((c.paid <= pd.Timestamp(D(2026, 10, 12))).all()))
    fam_ids = {}
    for mk in held26:
        fam_ids.setdefault(r26[mk], set()).add(mk[1][:9])
    check("realism: the members of each long stay share one Pemberglen contract number", all(len(s_) == 1 for s_ in fam_ids.values())
          and len(fam_ids) == 2, str(fam_ids))
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
    pay_dates = sorted(set(pm_.paymentDate) | set(mr.PMT_DT))
    check("realism: every remittance paid by 16 October 2026", pay_dates[-1] <= "2026-10-16", pay_dates[-1])
    npis = {}
    for r in p["roster"]:
        npis.setdefault(r["practice"], []).append(int(r["npi"]))
    spans = [(min(v_), max(v_)) for v_ in npis.values()]
    overlap = sum(1 for a_, b_ in itertools.combinations(spans, 2) if a_[0] < b_[1] and b_[0] < a_[1])
    check("realism: the roster's NPIs are drawn at random, the practices' ranges overlapping (%d of 78 pairs)" % overlap,
          overlap > 60 and len({r["npi"] for r in p["roster"]}) == len({(r["npi"], r["practice"]) for r in p["roster"]}) - 1)
    icn_day = pd.to_datetime("20" + mlhc.CLM_ID.str[1:3], format="%Y") + pd.to_timedelta(mlhc.CLM_ID.str[3:6].astype(int) - 1, unit="D")
    check("realism: every Merrinlake control number dated on or after its last day of service and on or before its payment",
          bool(((icn_day >= pd.to_datetime(mlhc.SVC_THRU_DT)) & (icn_day <= pd.to_datetime(mlhc.PD_DT))).all()))
    kb_ = pd.read_csv(os.path.join(T, "KBP_CLAIMS_LPN_20261009.txt"), sep="|", dtype=str, keep_default_na=False)
    pmj = json.load(open(os.path.join(T, "pmh_partner_claims_2026-10-12.json")))["records"]
    check("realism: each payer numbers its claims in its own scheme (Merrinlake's 13-digit control numbers, Kesselcrest's "
          "E and ten digits, Pemberglen's C and eight hexadecimal)",
          mlhc.CLM_ID.str.fullmatch(r"4\d{12}").all() and kb_.CLAIM_NO.str.fullmatch(r"E\d{10}(-01)?").all() and
          all(re.fullmatch(r"C[0-9A-F]{8}", r_["claimId"]) for r_ in pmj) and mlhc.CLM_ID.is_unique)

    print("\n%d checks, %d failed" % (N[0], len(FAILS)))
    for f in FAILS:
        print("  FAIL", f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
