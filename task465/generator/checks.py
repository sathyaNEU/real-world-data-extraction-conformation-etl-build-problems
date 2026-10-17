"""The generator's assertions for task465: the three rules executed on the clean truth (R1 to R3c), the convergence of
the fusions that keep both surveys' shares (C1), every row of the semantic fork table (SF1 to SF15), the ladder and its
margins, the Layer 1 items' neutrality, the asks' devices and stops, the separation of the call from the asks, the
distractors, the input gates and the realism sweep.

    python3 task465/generator/checks.py      (after build.py has written target/ and golden/)
"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B     # noqa: E402
import methods as M    # noqa: E402
import sim as S        # noqa: E402
import world as W      # noqa: E402

TASK = os.path.dirname(HERE)
FAMILY = M.FAMILY
CALL = 38
RUNGS = {"independence": 26, "pilot_shares": 42, "energy_x_pilot": 51, "health_x_pilot": 33, "lift": 41}
POOLED_BANDS = 25


def r100(v):
    return int((v / 100.0) + 0.5) * 100 if v >= 0 else -r100(-v)


def staffing(cells):
    tot = M.division_totals(cells)
    return {d: M.caseworkers(tot[d]) for d in W.DIV_NAMES}


def run(target, golden, x=None, meta_path=None, fig_path=None):
    bad = []

    def check(label, cond, detail=""):
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))
        if not cond:
            bad.append(label)

    x = x or S.everything()
    F = json.load(open(fig_path or os.path.join(HERE, "figures.json")))
    meta = json.load(open(meta_path or os.path.join(TASK, "metadata.json")))

    # ------------------------------------------------------------------ the call from the pack
    N, p, q, tabs, tabs_div = B.conformed(target)
    R, info = M.routes(N, p, q, tabs, tabs_div)
    g = R["golden"]
    gd = M.division_totals(g)
    gst = staffing(g)
    check("the call: %d caseworkers (%s)" % (sum(gst.values()), ", ".join("%s %d" % (d, gst[d]) for d in W.DIV_NAMES)),
          gst == F["call"]["by_division"] and sum(gst.values()) == F["call"]["total"] == CALL)

    # ------------------------------------------------------------------ R1, the field's raw material ships
    heads = {}
    for f in sorted(os.listdir(target)):
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads[f] = next(csv.reader(fh))
    check("R1 the surveys ship household microdata with their weights and the pilot its screen answers",
          "WT_FINAL" in heads[W.FILES["heas"]] and "HH_WT" in heads[W.FILES["shs"]]
          and {"HH_INCOME", "ELEC_12M", "OTHER_FUELS_12M", "MED_EQUIPMENT"} <= set(heads[W.FILES["pilot"]]))
    joint_cols = [c for h in heads.values() for c in h if re.search(r"ELIGIB|JOINT|REFERR|BURDEN|ODDS|BOTH", c)]
    check("R1 no shipped column holds the deciding quantity (an eligible count, a joint share, a referral or a burden "
          "flag)", not joint_cols, joint_cols)
    check("R1 the golden's decisive computation reads the microdata (the pilot's tables come from its screen rows)",
          sum(sum(t) for t in tabs.values()) > 3000 and len(tabs_div) == 4)

    # ------------------------------------------------------------------ R3, the three rules on the clean truth
    pc, qc = S.conformed(x, x["pub"])
    tc, tdc = S.pilot_tables(x["P"])
    Nc = S.eligible_cells(x["cells"], x["pub"])
    Rc, _ = M.routes(Nc, pc, qc, tc, tdc)
    check("R3a the analyst test: every field read right and every filed rule applied, the two surveys' shares multiplied "
          "on the clean truth staff 26", sum(staffing(Rc["independence"]).values()) == 26,
          staffing(Rc["independence"]))
    check("R3a the independence table keeps every filed sentence: households and both surveys' shares in every cell",
          all(abs(Rc["independence"][k] - Nc[k] * pc[k] * qc[k]) < 1e-6 for k in Nc))
    check("R3b the decisive step alone (the pilot's within-band association, both shares kept) staffs %d on the clean "
          "truth" % CALL, staffing(Rc["golden"]) == gst)
    for m, want in RUNGS.items():
        got = sum(staffing(Rc[m]).values())
        check("R3b the lower rung %s staffs %d, not the golden" % (m, want), got == want and got != CALL, got)
    check("R3b the independence product with each division's bands pooled staffs %d" % POOLED_BANDS,
          sum(M.caseworkers(v) for v in M.independence_by_division(N, p, q).values()) == POOLED_BANDS)
    check("R3 the clean truth and the pack agree cell by cell (the pack's mess handled as the golden handles it)",
          all(abs(Rc["golden"][k] - g[k]) < 0.5 for k in g), round(max(abs(Rc["golden"][k] - g[k]) for k in g), 3))
    docs = {}
    from pypdf import PdfReader
    for f in os.listdir(target):
        if f.endswith(".pdf"):
            docs[f] = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, f)).pages))
    banned = r"independen|odds|\brak(e|ing)\b|iterative proportional|associat|\bjoint\b|correlat|\bfus(e|ion)\b|" \
             r"statistical match|both traits|go together"
    hits = {f: re.findall(banned, t, re.I) for f, t in docs.items()}
    check("R3c no document names the decisive step (independence, an odds ratio, raking, association, fusion)",
          not any(hits.values()), {f: v for f, v in hits.items() if v})
    figs = {v for v in list(F["eligible"].values()) + list(F["cells"].values()) + list(F["baseline"].values())
            + list(F["battery"].values()) if v >= 1000}
    seen = {f: sorted(v for v in figs if re.search(r"(?<![\d,])%s(?![\d,])" % "{:,}".format(v), t))
            for f, t in docs.items()}
    check("R3c no graded figure of four digits or more appears in a document (a count that only coincides included)",
          not any(seen.values()), {f: v for f, v in seen.items() if v})
    check("R3c the pilot report counts screens only: no share with the equipment or with high costs",
          not re.search(r"\d+(\.\d+)? per cent", docs[W.FILES["pilot_report"]]))
    rowsets = {}
    for f in (W.FILES["heas"], W.FILES["shs"]):
        with open(os.path.join(target, f), encoding="utf-8") as fh:
            body = [tuple(r[1:]) for r in csv.reader(fh)][1:]
        rowsets[f] = len(body) - len(set(body))
    check("R3c no copied block: no repeated record in either survey file", not any(rowsets.values()), rowsets)

    # ------------------------------------------------------------------ C1, the family that keeps both shares
    for m in FAMILY:
        st = staffing(R[m])
        same_cells = all(r100(R[m][k]) == r100(g[k]) for k in g)
        same_div = all(r100(M.division_totals(R[m])[d]) == r100(gd[d]) for d in W.DIV_NAMES)
        check("C1 %s: the same staffing, all 18 cells and nine division totals on the golden's hundred" % m,
              st == gst and same_cells and same_div, round(max(abs(R[m][k] - g[k]) for k in g), 1))
    closed = {k: M.joint(p[k], q[k], info["psi_band"][k[1]]) * N[k] for k in N}
    check("C1 the raked band tables and the closed-form fusion give the same cells",
          all(abs(closed[k] - g[k]) < 0.01 for k in g))
    check("C1 the eligible households in each cell never exceed the households with the equipment or with high costs",
          all(g[k] <= N[k] * min(p[k], q[k]) + 1e-9 for k in g))

    # ------------------------------------------------------------------ the ladder and its margins
    step = {d: round(min(gd[d] % W.CASELOAD, W.CASELOAD - gd[d] % W.CASELOAD)) for d in W.DIV_NAMES}
    check("ladder: every division's eligible households 90 or more from a caseworker step", min(step.values()) >= 90, step)
    edge = min(50 - abs(g[k] - r100(g[k])) for k in g)
    check("ladder: every cell 40 or more from its hundred's edge", edge >= 40, round(edge, 1))
    dedge = min(50 - abs(gd[d] - r100(gd[d])) for d in W.DIV_NAMES)
    check("ladder: every division total 30 or more from its hundred's edge", dedge >= 30, round(dedge, 1))
    ind = M.division_totals(R["independence"])
    istep = min(min(ind[d] % W.CASELOAD, W.CASELOAD - ind[d] % W.CASELOAD) for d in W.DIV_NAMES)
    check("ladder: the default path's division totals 40 or more from a step", istep >= 40, round(istep))
    moved = sum(1 for d in W.DIV_NAMES if staffing(R["independence"])[d] != gst[d])
    check("ladder: the default path moves eight of nine divisions' staffing and all 18 cells",
          moved == 8 and all(r100(R["independence"][k]) != r100(g[k]) for k in g), moved)
    cap = {k: N[k] * min(p[k], q[k]) for k in g}
    over = {m: sum(1 for k in g if R[m][k] > cap[k]) for m in ("pilot_shares", "energy_x_pilot", "lift")}
    check("ladder: the pilot's own shares, the energy survey times the pilot and the dependence ratio each give a cell "
          "more eligible households than households with the equipment", all(v >= 2 for v in over.values()), over)
    t0 = tabs[0]
    gapb = {d: p[(d, 0)] - (q[(d, 0)] * t0[0] / (t0[0] + t0[2]) + (1 - q[(d, 0)]) * t0[1] / (t0[1] + t0[3]))
            for d in W.DIV_NAMES if d not in W.PILOT_DIVISIONS}
    check("ladder: the health survey times the pilot holds burden shares under $25,000 five or more points below the "
          "energy survey's in every division outside the pilot", min(gapb.values()) >= 0.05,
          round(min(gapb.values()), 3))
    for b in W.ELIGIBLE_BANDS:
        t = tabs[b]
        hi, lo = 100 * t[0] / (t[0] + t[1]), 100 * t[2] / (t[2] + t[3])
        check("data-native: band %d, the equipment in %.1f per cent of high-burden screens against %.1f per cent of the "
              "rest" % (b, hi, lo), round(hi, 1) == F["pilot_rates"][str(b)]["equip_high"]
              and round(lo, 1) == F["pilot_rates"][str(b)]["equip_rest"] and hi > 2.5 * lo)
    ors = {k: M.odds(t) for k, t in tabs_div.items()}
    check("data-native: the association holds in both pilot divisions and both bands (odds ratios 2.5 to 4)",
          all(2.5 < v < 4.0 for v in ors.values()), {"%s %d" % k: round(v, 2) for k, v in ors.items()})

    # ------------------------------------------------------------------ the semantic fork table
    import openpyxl
    heas = B.rows(target, "heas")
    reg = B.register(target)
    ratios = []
    for r in heas:
        elec = float(r["ELEC_AMT"]) * (12 if r["ELEC_BASIS"] == "M" else 1)
        ratios.append((elec + float(r["GAS_AMT"]) + float(r["OTHER_AMT"])) / float(r["HHINC"]))
    pilot_rows = B.rows(target, "pilot")
    pil = [r for r in pilot_rows if r["STATUS"] != "Ended - income"]
    pratios = [(float(r["ELEC_12M"]) + float(r["OTHER_FUELS_12M"])) / float(r["HH_INCOME"]) for r in pil]
    check("SF1 eligible household: no household at an income of exactly $50,000 and none within 0.12 points of 6 per "
          "cent, so the edges' inclusivity files the same call",
          all(float(r["HHINC"]) != 50000 for r in heas) and all(float(r["HH_INCOME"]) != 50000 for r in pilot_rows)
          and all(abs(v - 0.06) >= 0.0012 for v in ratios + pratios))
    num, den = {}, {}
    for r in heas:
        d, b = reg.get(r["COUNTY"]), B.band_of_income(r["HHINC"])
        if d is None or b > 1:
            continue
        elec = float(r["ELEC_AMT"]) * (12 if r["ELEC_BASIS"] == "M" else 1)
        w = float(r["WT_FINAL"])
        den[(d, b)] = den.get((d, b), 0) + w
        num[(d, b)] = num.get((d, b), 0) + w * (elec / float(r["HHINC"]) > W.BURDEN)
    p_elec = {k: num[k] / den[k] for k in den}
    Re, _ = M.routes(N, p_elec, q, tabs)
    check("SF2 annual home energy costs: electricity alone files a different call (the plan's eligibility names gas "
          "and other fuels); the monthly bill taken as the year's files the same call (R2 below)",
          staffing(Re["golden"]) != gst and "natural gas and other home heating fuels" in docs[W.FILES["plan"]])
    check("SF3 2025 eligible households: the surveys and estimates are 2025's and no projection ships",
          "2025" in W.FILES["estimates"] and not any("projection" in h.lower() for h in heads)
          and "2025, the latest survey year" in docs[W.FILES["plan"]])
    ws = openpyxl.load_workbook(B.path(target, "estimates"), data_only=True)["Households by income"]
    kv = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[1] == W.FIPS["Kestrelmere"]:
            kv = {b: int(row[3 + b]) for b in W.ELIGIBLE_BANDS}
    alt_n = dict(N)
    for b in W.ELIGIBLE_BANDS:
        alt_n[("Southwest", b)] -= kv[b]
        alt_n[("Central", b)] += kv[b]
    Ra, _ = M.routes(alt_n, p, q, tabs)
    check("SF4 service division: Kestrelmere's households under Central move Central and Southwest; the register "
          "holds one division per county and the plan staffs the register's divisions",
          staffing(Ra["golden"]) != gst and "division register" in docs[W.FILES["plan"]])
    check("SF5 household: no person or adult weight ships beside the household weights",
          not any("ADULT_WT" in c or "PERSON" in c for h in heads.values() for c in h))
    check("SF6 the equipment item: don't know and refused left out (counted as no is in R2 below)",
          "Estimates of percentages exclude don't know (7) and refused (9) responses" in _codebook_notes(target))
    nest = {k: b for k, _, b in W.INCCAT}
    check("SF7 income band: the health survey's categories nest exactly in the demographer's bands",
          [k for k in nest if nest[k] == 0] == [1, 2, 3] and [k for k in nest if nest[k] == 1] == [4, 5])
    check("SF8 weights: WT_FINAL and HH_WT name the published estimates (the base weight is in R2 below)",
          "The office's published estimates use WT_FINAL" in docs[W.FILES["heas_methods"]]
          and "Use HH_WT for estimates of households" in _codebook_notes(target))
    tot_w = {}
    for r in heas:
        tot_w[r["COUNTY"]] = tot_w.get(r["COUNTY"], 0) + float(r["WT_FINAL"])
    est_c = {row[1]: int(row[2]) for row in ws.iter_rows(min_row=5, values_only=True) if row[1] and row[1] != "000"}
    check("SF9 households: the final weights reproduce every county's published households (within a household)",
          all(abs(tot_w[c] - est_c[c]) < 1.0 for c in est_c), round(max(abs(tot_w[c] - est_c[c]) for c in est_c), 4))
    nearest = {d: int(round(gd[d] / W.CASELOAD)) for d in W.DIV_NAMES}
    check("SF10 caseload standard: rounding to the nearest caseworker files a different call (the plan's 'or part of "
          "that number' rounds up)", nearest != gst and "or part of that number" in docs[W.FILES["plan"]])
    check("SF11 rounding path: caseworkers from the rounded counts file the same call",
          {d: M.caseworkers(r100(gd[d])) for d in W.DIV_NAMES} == gst)
    check("SF12 an address screened twice: the latest complete screen (both kept is in R2 below)",
          "latest complete screen" in docs[W.FILES["pilot_report"]])
    check("SF13 partial screens and don't-know answers: left out (counted as no is in R2 below)",
          "stopped before Q4" in docs[W.FILES["pilot_report"]])
    Nk, pk, qk = B.households(target, by="county"), B.burden_shares(target, by="county"), \
        B.equipment_shares(target, by="county")
    reg_ = B.register(target)
    kc = {}
    for (c_, b_), n_ in Nk.items():
        kc[(reg_[c_], b_)] = kc.get((reg_[c_], b_), 0) + n_ * M.joint(pk[(c_, b_)], qk[(c_, b_)], info["psi_band"][b_])
    check("SF15 the estimation domain: each division and band as a whole (the annex); a county-by-band fusion summed to "
          "the divisions keeps every division's staffing",
          staffing(kc) == gst and "estimated for the division and band as a whole" in docs[W.FILES["plan"]],
          {d: int(round(v)) for d, v in M.division_totals(kc).items() if r100(v) != r100(gd[d])})
    check("SF14 the conformed table agrees with each survey: every golden cell keeps both shares",
          all(abs(g[k] - closed[k]) < 0.01 for k in g) and "the table reproduces" in docs[W.FILES["plan"]])

    # ------------------------------------------------------------------ R2, each Layer 1 item neutral on the call
    for label, kw in (("electricity's monthly bill taken as the year's", dict(monthly_as_annual=True)),
                      ("the energy survey's base weight", dict(weight="WT_BASE")),
                      ("don't know and refused counted as no", dict(dk_as_no=True)),
                      ("both screens of a twice-screened address kept", dict(keep_dups=True)),
                      ("partial screens counted as no", dict(partial_as_no=True)),
                      ("the pilot's don't-know answers counted as no", dict(pilot_dk_as_no=True))):
        N2, p2, q2, t2, td2 = B.conformed(target, **kw)
        R2, _ = M.routes(N2, p2, q2, t2, td2)
        check("R2 %s leaves the call where it is" % label, staffing(R2["golden"]) == gst)
    raw = {r["COUNTY"] for r in heas}
    check("R2 county codes: three-digit text in one survey and integers in the other, every territory county joins",
          all(("%03d" % int(r["CNTYFIPS"])) in raw for r in B.rows(target, "shs")) and set(reg) <= raw)
    check("R2 the estimates' region and state rows carry no county code the register knows",
          not any((row[1] or "") in reg for row in ws.iter_rows(min_row=5, values_only=True)
                  if str(row[0]).startswith(("State", "Planning"))))

    # ------------------------------------------------------------------ the asks
    names = B.county_names(target)
    A = B.baseline_households(target)
    check("Ask A golden: households on the medical baseline rate on 31 October 2026 by division", A == F["baseline"], A)
    for label, kw in (("open accounts by the register's division (the cracker)", dict(unit="account")),
                      ("open accounts by the extract's own division column", dict(unit="account", division="stored"))):
        v = B.baseline_households(target, **kw)
        check("Ask A stop, %s, misses every division" % label, all(v[d] != A[d] for d in W.DIV_NAMES),
              [v[d] - A[d] for d in W.DIV_NAMES])
    v = B.baseline_households(target, division="stored")
    check("Ask A hazard H1: households by the stored division move Central and Southwest only",
          [d for d in W.DIV_NAMES if v[d] != A[d]] == ["Central", "Southwest"])
    openx = {d: 0 for d in W.DIV_NAMES}
    for r in B.rows(target, "baseline"):
        if not r["END_DATE"]:
            openx[names[r["SERVICE_COUNTY"]]] += 1
    check("Ask A stop, spells open at the extract (3 November), misses every division",
          all(openx[d] != A[d] for d in W.DIV_NAMES), [openx[d] - A[d] for d in W.DIV_NAMES])
    on_edge = [r for r in B.rows(target, "baseline") if "2026-10-31" in (r["START_DATE"], r["END_DATE"])]
    check("Ask A: no spell starts or ends on 31 October itself (inclusive and exclusive readings agree)", not on_edge)
    Bb = B.battery_households(target)
    check("Ask B golden: households given a backup battery from January to October 2026 by division",
          Bb == F["battery"], Bb)
    for label, kw in (("distinct accounts on Central Time (the cracker)", dict(unit="account")),
                      ("distinct unit serials", dict(unit="serial")),
                      ("completed orders on UTC dates", dict(unit="order", clock="utc"))):
        v = B.battery_households(target, **kw)
        check("Ask B stop, %s, misses every division" % label, all(v[d] != Bb[d] for d in W.DIV_NAMES),
              [v[d] - Bb[d] for d in W.DIV_NAMES])
    v = B.battery_households(target, clock="utc")
    check("Ask B hazard H2: UTC dates move seven or more divisions", sum(v[d] != Bb[d] for d in W.DIV_NAMES) >= 7,
          [v[d] - Bb[d] for d in W.DIV_NAMES])
    ch = B.Chains(target)
    seen = {}
    for r in B.rows(target, "batteries"):
        if r["STATUS"] == "Completed" and "2026-01-01" <= r["SCHEDULED"] <= "2026-10-31":
            seen[ch.find(r["ACCOUNT_NO"])] = names[r["SERVICE_COUNTY"]]
    sched = {d: 0 for d in W.DIV_NAMES}
    for dd in seen.values():
        sched[dd] += 1
    check("Ask B: the booked date in place of the completion moves some divisions",
          any(sched[d] != Bb[d] for d in W.DIV_NAMES), [sched[d] - Bb[d] for d in W.DIV_NAMES])
    check("Ask B: no household placed in December 2025 has a later order inside the window",
          _no_carryover(target, ch))
    check("asks: every ask figure distinct across divisions (no repeated count)",
          len(set(A.values())) == 9 and len(set(Bb.values())) == 9)

    # ------------------------------------------------------------------ separation and distractors
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        main_files = [W.FILES[k] for k in ("heas", "shs", "pilot", "estimates", "divisions")]
        ask_files = [W.FILES[k] for k in ("baseline", "batteries", "divisions")]
        for keep, label in ((main_files, "the call with the asks' and distractors' files deleted"),
                            (ask_files, "the asks with the surveys, pilot, estimates and distractors deleted")):
            d0 = os.path.join(tmp, "x")
            if os.path.exists(d0):
                shutil.rmtree(d0)
            os.makedirs(d0)
            for f in keep:
                shutil.copy(os.path.join(target, f), d0)
            if keep is main_files:
                N3, p3, q3, t3, td3 = B.conformed(d0)
                R3, _ = M.routes(N3, p3, q3, t3, td3)
                check("separation: %s is unchanged" % label, staffing(R3["golden"]) == gst
                      and all(abs(R3[m][k] - R[m][k]) < 1e-9 for m in R for k in g))
            else:
                check("separation: %s are unchanged" % label, B.baseline_households(d0) == A
                      and B.battery_households(d0) == Bb)
    finally:
        shutil.rmtree(tmp)
    src = open(os.path.join(HERE, "bundle.py")).read()
    check("distractors: the call and the asks read neither distractor (no reader in bundle.py opens them)",
          '"hvi"' not in src and '"liheap"' not in src and len(meta["distractor_files"]) >= 2)

    # ------------------------------------------------------------------ goldens and figures
    import openpyxl as ox
    wb = ox.load_workbook(os.path.join(golden, W.GOLDEN["workbook"]))
    ws1 = wb["Caseworkers 2027"]
    rows_ = {ws1.cell(row=i, column=1).value: [ws1.cell(row=i, column=j).value for j in range(2, 6)] for i in range(5, 15)}
    check("golden workbook: each division's eligible households, caseworkers and the two asks' figures",
          all(rows_[d] == [F["eligible"][d], gst[d], A[d], Bb[d]] for d in W.DIV_NAMES)
          and rows_["Total"] == [F["eligible_sum"], CALL, sum(A.values()), sum(Bb.values())])
    import zipfile
    media = [m for m in zipfile.ZipFile(os.path.join(golden, W.GOLDEN["workbook"])).namelist() if m.startswith("xl/media/")]
    png = zipfile.ZipFile(os.path.join(golden, W.GOLDEN["workbook"])).read("xl/media/image1.png") if media else b""
    check("golden workbook: the chart is embedded as a valid PNG", media == ["xl/media/image1.png"]
          and png.startswith(b"\x89PNG"), media)
    with open(os.path.join(golden, W.GOLDEN["table"]), encoding="utf-8") as fh:
        tab = list(csv.DictReader(fh))
    check("golden table: 18 cells, each on the golden's hundred, households the demographer's",
          len(tab) == 18 and all(int(r["ELIGIBLE_HOUSEHOLDS_2025"]) == r100(g[(r["SERVICE_DIVISION"],
                                                                                W.BANDS.index(r["INCOME_BAND"]))])
                                 and int(r["HOUSEHOLDS_2025"]) == N[(r["SERVICE_DIVISION"],
                                                                     W.BANDS.index(r["INCOME_BAND"]))] for r in tab))
    check("golden: each division's rounded total is the sum of its rounded cells, the divisions' sum the rounded total",
          all(sum(F["cells"]["%s|%d" % (d, b)] for b in W.ELIGIBLE_BANDS) == F["eligible"][d] for d in W.DIV_NAMES)
          and r100(sum(gd.values())) == F["eligible_sum"])

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    big = meta["input_gates"]["largest_file_rows"]
    check("gates: %d files, %d formats, the largest file %d rows, %d distractors" % (
        len(files), len(fmts), big, len(meta["distractor_files"])),
        len(files) >= 10 and len(fmts) >= 3 and big >= 25000 and len(meta["distractor_files"]) >= 2)
    check("gates: the register lists every shipped file but itself",
          {r["FILE_NAME"] for r in B.rows(target, "register")} == set(files) - {W.FILES["register"]})
    text = ""
    for f in files:
        if f.endswith((".csv", ".txt")):
            text += open(os.path.join(target, f), encoding="utf-8").read()
    text += " ".join(docs.values())
    check("realism: no em or en dash anywhere in the pack", "\u2014" not in text and "\u2013" not in text)
    people = set(re.findall(r"(Stacy Williams|Shawn Taylor)", text))
    check("realism: the personas are the drawn ones", people == {"Stacy Williams", "Shawn Taylor"}, people)
    late = []
    for f in files:
        if f == W.FILES["plan"] or not f.endswith(".csv"):
            continue
        body = open(os.path.join(target, f), encoding="utf-8").read()
        if re.search(r"2026-11-(1[7-9]|2\d|30)|2026-12-|2027-", body):
            late.append(f)
    check("realism: no dated record after the folder's as-of date", not late, late)
    check("realism: the divisions' eligible households are not round thousands",
          sum(v % 1000 == 0 for v in F["eligible"].values()) == 0)
    return not bad


def _codebook_notes(target):
    import openpyxl
    ws = openpyxl.load_workbook(B.path(target, "shs_codebook"))["Notes"]
    return " ".join(str(c.value) for row in ws.iter_rows() for c in row if c.value)


def _no_carryover(target, ch):
    days = {}
    for r in B.rows(target, "batteries"):
        if r["STATUS"] == "Completed":
            days.setdefault(ch.find(r["ACCOUNT_NO"]), []).append(B.central_date(r["COMPLETED_UTC"]))
    for ds in days.values():
        if min(ds) < dt.date(2026, 1, 1) and any(dt.date(2026, 1, 1) <= d <= dt.date(2026, 10, 31) for d in ds):
            return False
    return True


if __name__ == "__main__":
    ok = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    raise SystemExit(0 if ok else 1)
