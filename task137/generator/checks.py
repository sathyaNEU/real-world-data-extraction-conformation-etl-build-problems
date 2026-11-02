"""Every assertion the build stands on, run on the cut pack and the generator's clean truth. Labels: R (the three
rules), M (the main call), L (light labels and the back-test), A7 (lesson 7: assumptions the data could contradict),
SF (semantic forks), K (clocks), D (ask devices), G (input gates, realism, leaks). Returns the number of failures."""
import collections
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd
from scipy import stats

import analysis as AN
import astro as A
import pack as PK
import params as P
import seeds as SD
import solve as S

FAILS = []


def ok(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ((": " + str(detail)) if detail != "" else ""))
    if not cond:
        FAILS.append(label)


def b50(x):
    return int(50 * round(x / 50 + 1e-9))


def b25(x):
    return int(25 * round(x / 25 + 1e-9))


def margin(x, k):
    """distance from x to the nearer edge of its rounding bin of width k"""
    lo = (round(x / k + 1e-9) - 0.5) * k
    return min(x - lo, lo + k - x)


def routes(E, C, F):
    out = {}
    for name, cols in list(AN.MODELS_EASY.items()) + list(AN.MODELS_LIGHT.items()):
        if "year" in cols:
            continue
        q, y, _ = AN.forecast(E, C, F, cols)
        out[name] = (y, [float(q.get(i, 0)) for i in (1, 2, 3, 4)])
    q, y = AN.cell_forecast(E, C, F, ["month", "band"], ["band"])
    out["month by band cells"] = (y, [float(q.get(i, 0)) for i in (1, 2, 3, 4)])
    q, y = AN.cell_forecast(E, C, F, ["band", "dark"], ["band"])
    out["band by light cells (light)"] = (y, [float(q.get(i, 0)) for i in (1, 2, 3, 4)])
    return out


def text_of(target):
    """Every shipped file's text, for the leak and wording sweeps."""
    import pdfplumber
    from openpyxl import load_workbook
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            with pdfplumber.open(p) as pdf:
                out[f] = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
        elif f.endswith(".xlsx"):
            wb = load_workbook(p, read_only=True)
            out[f] = "\n".join(" ".join(str(v) for v in r if v is not None) for ws in wb.worksheets
                               for r in ws.iter_rows(values_only=True)) + "\n" + " ".join(wb.sheetnames)
        else:
            out[f] = open(p, encoding="utf-8").read()
    return out


def main(target, W, F, X):
    FAILS.clear()
    E, C, Fx = X["E"], X["C"], X["F"]
    M = X["M"]
    # ------------------------------------------------------------------ M: the call and the ladder on the pack
    R = routes(E, C, Fx)
    easy = {k: v for k, v in R.items() if "light" not in k}
    fam = {k: v for k, v in R.items() if "light" in k}
    g = R["clock band and light (golden)"]
    ok("M1 golden year 350 (unrounded %.1f)" % g[0], b50(g[0]) == 350 == F["claims_2027"])
    sw = lambda q: (q[1] + q[2], q[0] + q[3])      # April to September; the other six months
    ok("M1 golden April to September 150 and the other six months 200 (%.1f, %.1f)" % sw(g[1]),
       (b50(sw(g[1])[0]), b50(sw(g[1])[1])) == (150, 200) ==
       (F["claims_2027_apr_sep"], F["claims_2027_other_months"]))
    for k, (y, q) in easy.items():
        ok("M2 easy route '%s' files a wrong year (%s)" % (k, b50(y)), b50(y) != 350, round(y, 1))
    ok("M2 Gate F: cheap routes reaching 350 on the pack = 0", sum(b50(y) == 350 for y, _ in easy.values()) == 0)
    for k, (y, q) in fam.items():
        ok("M3 standing member '%s' year in 350 with margin >= 10" % k, b50(y) == 350 and margin(y, 50) >= 10, round(y, 1))
        ok("M3 standing member '%s' April to September and the other months in the golden's bins, margin >= 7" % k,
           (b50(sw(q)[0]), b50(sw(q)[1])) == (150, 200) and min(margin(x, 50) for x in sw(q)) >= 7,
           [round(x, 1) for x in sw(q)])
    ok("M4 easy routes all on 300 (the default path's figure)", all(b50(y) == 300 for y, _ in easy.values()),
       sorted(round(y, 1) for y, _ in easy.values()))
    ok("M4 easy routes file the other six months at 150, not 200", all(b50(sw(q)[1]) == 150 for _, q in easy.values()),
       sorted(round(sw(q)[1], 1) for _, q in easy.values()))
    # SF20: the measured family, three constructions of light by nine models, on the year and the two seasons
    runs_l, T_l, row_l = X["X"]["runs"], X["X"]["T"], X["X"]["row_of"]
    plan_l = [(d, dep, a, a + dur, km) for d in X["X"]["days"] for dep, a, dur, km in X["X"]["routes"]]
    claims_l = [(cc["date"], cc["depot"], cc["h"]) for cc in X["X"]["TC"] if cc["date"] <= S.REC_END]
    Eh = AN.exposure_hourmid(runs_l, T_l, row_l, S.bst)
    Fh = AN.exposure_hourmid(plan_l, T_l, row_l, S.bst)
    Ch = AN.claim_frame_hourmid(claims_l, T_l, row_l, S.bst)
    cut2 = dt.date(2024, 10, 1)
    cons = {"exact split": (AN.with_am(E), AN.with_am(C), AN.with_am(Fx)),
            "hour-midpoint light": (Eh, Ch, Fh),
            "last two years": (AN.with_am(E[E.date >= cut2]), AN.with_am(C[C.date >= cut2]), AN.with_am(Fx))}
    table, q4s = [], []
    for cn, (e, cc_, f) in cons.items():
        for mn, cols in AN.FAMILY.items():
            q, y, _ = AN.forecast(e, cc_, f, cols)
            qq = [float(q.get(i, 0)) for i in (1, 2, 3, 4)]
            table.append((cn, mn, y, qq))
        q, y = AN.cell_forecast(e, cc_, f, ["band", "dark"], ["band"])
        table.append((cn, "band by light cells", y, [float(q.get(i, 0)) for i in (1, 2, 3, 4)]))
    print("     SF20 family table: construction | model | year | Q1 Q2 Q3 Q4 | Apr-Sep | other months")
    for cn, mn, y, qq in table:
        print("     %s | %s | %.1f | %s | %.1f | %.1f" % (cn, mn, y, " ".join("%.1f" % v for v in qq), qq[1] + qq[2],
                                                      qq[0] + qq[3]))
    ok("SF20 every member of the measured family (%d) files 350 for the year, 150 for April to September and 200 for the "
       "other six months" % len(table), all(b50(y) == 350 and b50(qq[1] + qq[2]) == 150 and b50(qq[0] + qq[3]) == 200
                                            for _, _, y, qq in table))
    ok("SF20 the family's nearest edges: year %.1f, April to September %.1f, other months %.1f" % (
        min(margin(y, 50) for _, _, y, _ in table), min(margin(qq[1] + qq[2], 50) for _, _, _, qq in table),
        min(margin(qq[0] + qq[3], 50) for _, _, _, qq in table)),
       min(margin(y, 50) for _, _, y, _ in table) >= 5 and min(margin(qq[0] + qq[3], 50) for *_, qq in table) >= 5)
    crossing = [(cn, mn, round(qq[3], 1)) for cn, mn, y, qq in table if b25(qq[3]) != 100 or b25(qq[0]) != 100]
    ok("SF20 quarters at the nearest 25 would not hold: %d members cross a quarter's edge %s" % (len(crossing),
       crossing[:3]), len(crossing) >= 1)
    # clean truth: the same ladder on the generator's world (exact times and durations)
    Et, Ct, Ft = SD.frames(W)
    Rt = routes(Et, Ct, Ft)
    ok("R2 analyst test on the clean truth: clock-band route files 300, golden 350",
       b50(Rt["by clock band"][0]) == 300 and b50(Rt["clock band and light (golden)"][0]) == 350,
       (round(Rt["by clock band"][0], 1), round(Rt["clock band and light (golden)"][0], 1)))
    ok("R2 clean truth: every easy route off 350, every light member on 350",
       all(b50(y) != 350 for k, (y, _) in Rt.items() if "light" not in k) and
       all(b50(y) == 350 for k, (y, _) in Rt.items() if "light" in k))
    # ------------------------------------------------------------------ L: light from shipped records alone
    T, rows = S.sun_table(target)
    ok("L1 handbook Appendix C parses to the world's table exactly (%d cells)" % len(T), T == A.TABLE)
    ok("L1 table rows are the world's rows", [(a, b) for a, b in rows] ==
       [((a.month, a.day), (b.month, b.day)) for _, a, b in A.ROWS])
    ok("L1 the handbook's clock rule equals the world's on every day 2023 to 2027",
       all(S.bst(d) == A.bst_offset(d) for d in (dt.date(2023, 1, 1) + dt.timedelta(days=i) for i in range(1826))
           if d.weekday() < 6))
    routes27, days27 = X["X"]["routes"], X["X"]["days"]
    plan = [(d, dep, a, a + dur, km) for d in days27 for dep, a, dur, km in routes27]
    Ftruth = AN.exposure(plan, A.TABLE, A.row_of, A.bst_offset)
    Fship = AN.exposure(plan, T, S.row_finder(rows), S.bst)
    same = (len(Ftruth) == len(Fship) and (Ftruth.dark.values == Fship.dark.values).all() and
            np.allclose(Ftruth.km.values, Fship.km.values))
    ok("L2 every 2027 route-hour's dark or light label is recovered from shipped data alone (%d route-hour pieces, "
       "%d route-days)" % (len(Fship), len(plan)), same)
    ok("L2 the 2027 delivery days are the calendar's Yes days and the world's plan days",
       sorted(days27) == sorted(__import__("world").plan_2027()), len(days27))
    dark27 = float(Fx[Fx.dark == 1].km.sum() / Fx.km.sum())
    darkrec = float(E[E.dark == 1].km.sum() / E.km.sum())
    ok("L3 the 2027 schedule drives more of its km in the dark than the record (%.3f against %.3f)" % (dark27, darkrec),
       dark27 > 1.5 * darkrec)
    bt = X["BT"]
    p_light = 2 * min(stats.poisson.cdf(bt["obs"], bt["light"]), stats.poisson.sf(bt["obs"] - 1, bt["light"]))
    ok("L4 back-test: the record's 04:00-07:00 dark km sit in the summer schedule's months", set(bt["months"]) <= {5, 6, 7, 8},
       bt["months"])
    ok("L4 back-test: the light model fitted without them predicts their claims (obs %d, expected %.1f, two-sided p %.3f)"
       % (bt["obs"], bt["light"], p_light), p_light > 0.05)
    ok("L4 back-test: the 04:00-07:00 clock rate does not (expected %.1f, P(X>=obs) %.2e)" % (bt["band"],
       stats.poisson.sf(bt["obs"] - 1, bt["band"])), stats.poisson.sf(bt["obs"] - 1, bt["band"]) < 0.001)
    ok("L4 back-test: each clock hour's rate does not (expected %.1f, P(X>=obs) %.2e)" % (bt["hour"],
       stats.poisson.sf(bt["obs"] - 1, bt["hour"])), stats.poisson.sf(bt["obs"] - 1, bt["hour"]) < 0.01)
    ok("L4 back-test figures are the ones the golden prints", F["backtest"]["claims"] == bt["obs"])
    cut = dt.date(2025, 10, 1)
    qh, yh, _ = AN.forecast(E[E.date < cut], C[C.date < cut], E[E.date >= cut], ["band"])
    nh = int((C.date >= cut).sum())
    ph = 2 * min(stats.poisson.cdf(nh, yh), stats.poisson.sf(nh - 1, yh))
    ok("L5 the textbook check passes the easy route: the clock-band rate fitted to September 2025 predicts the next "
       "twelve months (%.1f against %d, p %.2f)" % (yh, nh, ph), ph > 0.2)
    # ------------------------------------------------------------------ A7: assumptions the golden makes
    for big, lab in ((["band", "dark", "month"], "no month or season effect beyond darkness"),
                     (["band", "dark", "year"], "no year-on-year trend"),
                     (["hour", "dark"], "clock band carries the time of day (no hour effect within bands)"),
                     (["band", "dark", "dark_am"], "the same darkness multiplier morning and evening")):
        lr, df, p = AN.lr_test(E, C, ["band", "dark"], big)
        ok("A7 %s (LR %.2f on %d df, p %.3f)" % (lab, lr, df, p), p > 0.05)
    lr, df, p = AN.lr_test(E, C, ["band"], ["band", "dark"])
    ok("A7 darkness is needed over the clock band (LR %.1f, p %.1e)" % (lr, p), p < 1e-6)
    lr, df, p = AN.lr_test(E, C, ["month", "band"], ["month", "band", "dark"])
    ok("A7 darkness is needed over month and clock band (LR %.1f, p %.1e)" % (lr, p), p < 1e-6)
    lr, df, p = AN.lr_test(E, C, ["band", "dark"], ["band", "dark", "depot"])
    ok("A7 a depot term, whatever its test (LR %.2f, p %.3f), leaves the call: same call" % (lr, p),
       b50(R["depot, clock band and light"][0]) == 350)
    G = AN.cells(E, C, AN.FINEST)
    G = G[G.km > 0]
    mfit = AN.fit_on(G, ["band", "dark"])
    disp = mfit.pearson_chi2 / mfit.df_resid
    ok("A7 Poisson dispersion near 1 at the finest grain (%.3f)" % disp, 0.8 < disp < 1.25)
    rk = collections.defaultdict(list)
    for r in W["runs"]:
        if r["date"] <= P.REC_END:
            rk[r["route"]].append(r["journeys"][0][2])
    ratio = [np.mean(v) / rr["km"] for rr in W["routes"] for k, v in rk.items() if k == rr["route"]]
    ok("A7 each route's recorded km average its planned km (ratio %.3f to %.3f)" % (min(ratio), max(ratio)),
       0.97 < min(ratio) and max(ratio) < 1.03)
    # ------------------------------------------------------------------ SF: semantic forks, each closed or same call
    L, REG = X["X"]["L"], X["X"]["REG"]
    TC = X["X"]["TC"]

    def refit(claims):
        Cc = AN.claim_frame([(c[0], c[1], c[2]) for c in claims], T, S.row_finder(rows), S.bst)
        q, y, _ = AN.forecast(E, Cc, Fx, ["band", "dark"])
        return y
    base_claims = [(c["date"], c["depot"], c["h"]) for c in TC if c["date"] <= S.REC_END]
    cars = [x for x in L if x["Vehicle"] == "Car" and x["Incident date"] <= S.REC_END]
    dups = [x for x in L if (str(x["Status"]).startswith("Closed") or x["Status"] == "Withdrawn")
            and x["Incident date"] <= S.REC_END]
    ok("SF1 company cars excluded by the fund terms; counting them is the same call (%d car claims)" % len(cars),
       b50(F["claims_2027_unrounded"] * (len(base_claims) + len(cars)) / len(base_claims)) == 350)
    extra = [(x["Incident date"], REG[S.norm_reg(x["Registration"])]["depot"],
              int(str(x["Incident time (UK)"])[:2]) + int(str(x["Incident time (UK)"])[3:]) / 60) for x in dups]
    ok("SF2 duplicates and withdrawn notifications excluded by the terms; counting them is the same call (%d rows)" %
       len(dups), b50(refit(base_claims + extra)) == 350)
    octo = [(c["date"], c["depot"], c["h"]) for c in TC]
    ok("SF3 claims to 31 Oct 2026 against km to 30 Sep: same call (%d October claims)" % (len(octo) - len(base_claims)),
       b50(refit(octo)) == 350)
    E2 = pd.concat([E, E[(E.date >= PK.TELE_B_START) & (E.date <= PK.TELE_A_END)]])
    q, y, _ = AN.forecast(E2, C, Fx, ["band", "dark"])
    ok("SF4 the two telematics exports' overlap week counted twice: same call", b50(y) == 350, round(y, 1))
    bh = {dt.date.fromisoformat(e["date"]) for e in PK.bank_holidays()}
    Fnb = Fx[~Fx.date.isin(bh)]
    q, y, _ = AN.forecast(E, C, Fnb, ["band", "dark"])
    ok("SF5 2027 bank holidays dropped from the delivery days: same call", b50(y) == 350, round(y, 1))
    ok("SF6 the terms count spares' collisions with the route trucks' (one fleet, one exposure)",
       "route truck or a depot spare" in text_of(target)[PK.FILES["terms"]].replace("\n", " "))
    # K: clocks
    runs_local_wrong = [(d, dep, a - S.bst(d), b - S.bst(d), km) for d, dep, a, b, km in X["X"]["runs"]]
    Ew = AN.exposure(runs_local_wrong, T, S.row_finder(rows), S.bst)
    q, yw, _ = AN.forecast(Ew, C, Fx, ["band", "dark"])
    heads2 = [open(os.path.join(target, PK.FILES[k]), encoding="utf-8").readline() for k in ("tele_a", "tele_b")]
    ok("SF7 telematics clocks are labelled UTC in both exports' headers (rival: read as UK clock time files %.1f, %d)" %
       (yw, b50(yw)), "(UTC)" in heads2[0] and "_utc" in heads2[1] and b50(yw) != 350)
    # incident against notification for the 2027 quarters: shift each month's expectation by the notification lags
    mon = F["claims_2027_months_unrounded"]
    qn = collections.Counter()
    for m in range(1, 13):
        ndays = (dt.date(2027 + (m == 12), m % 12 + 1, 1) - dt.date(2027, m, 1)).days
        for lag, pr in P.NOTIFY_LAG:
            late = min(1.0, lag / ndays)          # share of the month's collisions notified in the next month
            qn[(m - 1) // 3 + 1] += mon["%02d" % m] * pr * (1 - late)
            if m < 12:
                qn[m // 3 + 1] += mon["%02d" % m] * pr * late
    ok("SF8 the seasons by notification date rather than incident date: same call",
       (b50(qn[2] + qn[3]), b50(qn[1] + qn[4])) == (150, 200), (round(qn[2] + qn[3], 1), round(qn[1] + qn[4], 1)))
    ok("SF8 the terms file the quarter by incident date in UK clock time",
       "by its incident date in UK clock time" in text_of(target)[PK.FILES["terms"]].replace("\n", " "))
    ok("SF9 the listing's time column names its clock", "Incident time (UK)" in [str(x) for x in L[0].keys()])
    TXT = text_of(target)
    hb = TXT[PK.FILES["handbook"]].replace("\n", " ")
    ok("SF10 the handbook's lighting rule runs from sunset to sunrise and Appendix C gives both at each depot",
       "from sunset to sunrise" in hb and "Appendix C" in hb)
    from openpyxl import load_workbook
    cal = {(r[0].date() if hasattr(r[0], "date") else r[0]): r[3] for r in
           load_workbook(os.path.join(target, PK.FILES["schedule"]), read_only=True)["Calendar 2027"].iter_rows(
               min_row=2, values_only=True)}
    ok("SF11 the 2027 calendar: no deliveries on 1 January, the new schedule's first day 2 January",
       cal[dt.date(2027, 1, 1)] == "No" and cal[dt.date(2027, 1, 2)] == "Yes")
    qq = [F["claims_2027_apr_sep"], F["claims_2027_other_months"]]
    ok("SF12 the rounded seasons sum to the rounded year (%s)" % qq, sum(qq) == F["claims_2027"])
    # ------------------------------------------------------------------ D: the ask devices
    K = X["K"]
    ok("D0 the asks' figures equal the generator's truth (B1)", all(
        abs(F["repair_cost_unrounded"]["%s %s" % k] - v) < 0.01 for k, v in truth_b1(W).items()))
    ok("D0 the asks' figures equal the generator's truth (A1)", all(
        abs(F["recoveries_unrounded"][k] - v) < 0.01 for k, v in truth_a1(W).items()))
    ok("D1 every receipt without our claim number matches exactly one claim (payer, share, net outlay): %d of %d" %
       (K["n_matched"], K["n_receipts"]), not K["unmatched"] and K["n_matched"] > 40)
    cop = [x for x in W["invoices"] if x["copy"]]
    ok("D2 resent copies only inside the bodyshop feed's three spells (%d copies)" % len(cop),
       all(any(a <= x["sent"] - dt.timedelta(days=7) <= b for a, b in P.DOUBLE_SEND) for x in cop))
    fit = {v["reg"]: v["adas"] for v in W["vehicles"]}
    pairs = collections.Counter((x["job"]) for x in W["invoices"] if x["desc"] == "ADAS calibration" and not x["copy"])
    ok("D2 two genuine calibrations only on camera-and-radar trucks",
       all(fit[W["claims"][j_claim(W, j)]["reg"]] == "Camera and radar" for j, n in pairs.items() if n == 2))
    ok("D2 never two calibrations on a camera-only truck's job outside the spells",
       all(n == 1 for j, n in pairs.items() if fit[W["claims"][j_claim(W, j)]["reg"]] == "Camera"))
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    for f in os.listdir(target):
        if f not in (PK.FILES["ap"], PK.FILES["jobs"], PK.FILES["bank"]):
            shutil.copy(os.path.join(target, f), tmp)
    E3, C3, F3, _ = S.frames(tmp)
    y3 = S.main_call(E3, C3, F3)["year"]
    shutil.rmtree(tmp)
    ok("D3 the main call reads no ask-only file: with the AP ledger, the jobs and the recovery account deleted it files "
       "the same figure (%.1f)" % y3, abs(y3 - F["claims_2027_unrounded"]) < 0.05)
    # ask-side conventions
    REG2 = X["X"]["REG"]
    CI = S.claim_index(L, REG2)
    J = S.jobs(target)
    AP = S.ap(target)
    lines = S.genuine_lines(AP, J, CI, REG2)
    OUT = S.outlays(lines, J, CI)
    res, _ = S.recoveries(S.bank(target), L, CI, OUT)
    own = {x["Claim no."]: x for x in L}
    byrec = collections.Counter()
    for d, amt, no, how in res:
        byrec[S.quarter(d)] += amt
    diff = sum(int(100 * round(byrec[q] / 100)) != F["recoveries_by_collision_quarter"][q] for q in S.QS)
    terms = TXT[PK.FILES["terms"]].replace("\n", " ")
    ok("SF13 recoveries by the collision's quarter (terms); the receipt's own quarter moves %d of 6 figures" % diff,
       "credited to the quarter of that collision" in terms and diff >= 4)
    salv = [x for x in S.bank(target) if x["Description"].startswith(PK.SALVAGE)]
    ok("SF14 the salvage agent's credits (%d) are not another insurer's and stay out" % len(salv),
       len(salv) > 0 and PK.SALVAGE.split()[0] not in S.insurer_crosswalk(L) and "another party's insurer" in terms)
    gross = collections.Counter()
    for x in lines:
        c = CI[J[x["Supplier Ref"]]["Claim Ref"]]
        per = S.period(c["Incident date"])
        if per:
            gross["%s %s" % (REG2[S.norm_reg(c["Registration"])]["depot"], per)] += float(x["Gross"])
    ok("SF15 repair cost net of VAT (terms); gross moves every figure", "net of VAT" in terms and
       all(int(100 * round(gross[k] / 100)) != v for k, v in F["repair_cost_by_depot"].items()))
    sites = collections.defaultdict(set)
    for j in J.values():
        c = CI[j["Claim Ref"]]
        sites[j["Site"]].add(REG2[S.norm_reg(c["Registration"])]["depot"])
    ok("SF16 the depot is the truck's (register), not the bodyshop site: Washington repairs both %s" %
       sorted(sites["Washington"]), sites["Washington"] == {"CRA", "GAT"})
    tl = collections.Counter()
    for x in lines:
        if x["Description"] == "Inspection and storage":
            c = CI[J[x["Supplier Ref"]]["Claim Ref"]]
            per = S.period(c["Incident date"])
            if per:
                tl["%s %s" % (REG2[S.norm_reg(c["Registration"])]["depot"], per)] += float(x["Net"])
    ok("SF17 a total loss's inspection and storage is repair cost (terms); leaving it out moves %d figures" %
       sum(1 for k in tl if int(100 * round((F["repair_cost_unrounded"][k] - tl[k]) / 100)) != F["repair_cost_by_depot"][k]),
       "inspecting and storing it when it is a total loss" in terms and len(tl) >= 2)
    byinv = collections.Counter()
    for x in lines:
        c = CI[J[x["Supplier Ref"]]["Claim Ref"]]
        d = dt.datetime.strptime(x["Invoice Date"], "%d/%m/%Y").date()
        per = S.period(d)
        if per:
            byinv["%s %s" % (REG2[S.norm_reg(c["Registration"])]["depot"], per)] += float(x["Net"])
    nd = sum(int(100 * round(byinv[k] / 100)) != v for k, v in F["repair_cost_by_depot"].items())
    ok("SF18 the period is the collision's incident date (terms, the collision's repair); the invoice date moves %d of 8"
       % nd, nd >= 4)
    carregs = {S.norm_reg(c["reg"]) for c in W["cars"]}
    ok("SF19 no Brantwick job or recovery receipt belongs to a company car", all(
        S.norm_reg(CI[j["Claim Ref"]]["Registration"]) not in carregs for j in J.values()) and all(
        S.norm_reg(own[no]["Registration"]) not in carregs for _, _, no, _ in res))
    # ------------------------------------------------------------------ G: input gates, realism, leaks
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("G1 10 or more files (%d)" % len(files), len(files) >= 10)
    ok("G1 3 or more formats (%s)" % sorted(fmts), len(fmts) >= 3)
    nrows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("G1 a file of 25,000 rows or more (%s)" % max(nrows.values()), max(nrows.values()) >= 25000)
    meta = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "metadata.json")))
    ok("G1 two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]))
    ok("G1 metadata.json gives source, date and licence for every file", sorted(x["path"] for x in meta["files"]) == files
       and all(x.get("source") and x.get("date") and x.get("license") for x in meta["files"]))
    TX = TXT
    bad_names = [f for f in files if re.search(r"readme|dictionary|codebook|manifest|notes|definitions|schema", f, re.I)]
    ok("G2 no file describing the data, by name", not bad_names, bad_names)
    allx = "\n".join(TX.values())
    ok("G2 no sheet describing the data", not re.search(r"\b(Notes|README|Data dictionary|Definitions|Field guide)\b",
                                                         " ".join(TX[f] for f in files if f.endswith(".xlsx"))))
    for f in (PK.FILES["handbook"], PK.FILES["terms"]):
        t = TX[f].lower()
        ok("G3 %s names no darkness risk, rate or method" % f,
           not re.search(r"dark|night|collision rate|per km|per kilomet|risk of|more likely|safer|danger", t))
    ok("G3 no shipped document states or proposes a 2027 claims figure",
       not re.search(r"\b\d{2,3} (collision )?claims\b", TX[PK.FILES["terms"]] + TX[PK.FILES["handbook"]]))
    from openpyxl import load_workbook
    xh = []
    for f in files:
        if f.endswith(".xlsx"):
            for ws in load_workbook(os.path.join(target, f), read_only=True).worksheets:
                for r in ws.iter_rows(max_row=6, values_only=True):
                    xh += [str(v).lower() for v in r if v is not None]
    ok("G3 no workbook header names light, dark or sun", not any(re.search(r"\b(dark|daylight|light|sunrise|sunset|sunlight)\b", h)
                                                                   for h in xh if len(h) < 40))
    heads = [open(os.path.join(target, f), encoding="utf-8").readline().lower() for f in files if f.endswith(".csv")]
    ok("G3 no CSV header names light, dark or sun", not any(re.search(r"dark|light|sun", h) for h in heads))
    mc = list(F["record_claims_by_month"].values())
    ok("G4 realism: monthly claims vary (no repeated block, %d distinct of %d)" % (len(set(mc)), len(mc)),
       len(set(mc)) >= 12 and max(mc) > min(mc) + 8)
    ok("G4 realism: no round headline totals", F["claims_2027_unrounded"] % 10 != 0 and
       all(v % 100 != 0 for v in F["recoveries_unrounded"].values()))
    for f in files:
        b = open(os.path.join(target, f), "rb").read()
        ok("G5 %s carries no toolchain signature" % f, not re.search(rb"ReportLab|openpyxl|python-docx|matplotlib", b, re.I))
    people = set(P.PEOPLE.values())
    names_in = set(re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", TX[PK.FILES["terms"]] + TX[PK.FILES["handbook"]]))
    ok("G6 personas are the card's people", {n for n in names_in if n in people} <= people)
    ok("G7 no em or en dash in any shipped text", chr(0x2014) not in allx and chr(0x2013) not in allx)
    ok("G8 no date after the pack's as-of in any record (2027 schedule, calendar and holidays apart)",
       max(x["Notified"] for x in L) <= P.AS_OF)
    print("checks: %d failures" % len(FAILS))
    return len(FAILS)


def j_claim(W, job):
    for j in W["jobs"]:
        if j["job"] == job:
            return j["claim"]


def truth_b1(W):
    t = collections.defaultdict(float)
    for x in W["invoices"]:
        c = W["claims"][x["claim"]]
        if x["copy"] or not (P.ASK_FROM <= c["date"] <= P.ASK_TO):
            continue
        t[(c["depot"], S.period(c["date"]))] += x["net"]
    return t


def truth_a1(W):
    t = collections.defaultdict(float)
    for r in W["receipts"]:
        c = W["claims"][r["claim"]]
        if P.ASK_FROM <= c["date"] <= P.ASK_TO:
            t["%dQ%d" % (c["date"].year, (c["date"].month - 1) // 3 + 1)] += r["amount"]
    return t
