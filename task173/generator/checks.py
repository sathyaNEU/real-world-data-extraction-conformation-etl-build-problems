"""Generator assertions: the analyst test on the clean truth, every semantic fork (SFn), the golden family's convergence,
the default path's back-test, the ask goldens against the simulation's truth, and the separation line.

    python3 generator/checks.py        (exit 1 on any failure)"""
from __future__ import annotations

import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C     # noqa: E402
import world as W    # noqa: E402

FAIL = []


def check(name, ok, detail=""):
    print("%-4s %s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAIL.append(name)


def bin50(x):
    return int(round(x / 50.0) * 50)


def main():
    P = C.Pack()
    S = W.simulate()
    g = C.golden(P)
    L = C.line(P)
    L, pm = C.link(L, P)
    call = bin50(g["total"])

    # ---- the record against the simulation (Layer 1 handled: spells, the number map, codes, methods)
    sim = pd.Series([s["admit"] for s in S["spells"] if s["kind"] == "EM_GS" and s["admit"] <= W.RECORD_END])
    sim_fy = pd.Series(np.where(pd.to_datetime(sim).dt.month >= 4, pd.to_datetime(sim).dt.year, pd.to_datetime(sim).dt.year - 1)).value_counts().sort_index()
    check("line spells by year equal the simulation", L.groupby("fy").size().to_dict() == sim_fy.to_dict(), str(L.groupby("fy").size().to_dict()))

    # ---- the plan year's truth: expected first presentations plus the hazard on the planned list
    exp_first = 0.0
    for m in range(72, 84):
        yr = W.month_date(m).year
        for d in W.DISTRICTS:
            for s, rates in (("F", W.RATE_F), ("M", W.RATE_M)):
                exp_first += (S["pop"].at(d, s, yr) * np.array(rates) * W.RATE_SCALE / 1e5 / 12 * W.season(m)).sum()
        exp_first += 1.9 * W.SCALE * W.season(m)
    tr = C.plan_traj(P.t)
    keys = list(tr.keys())[5:]
    exp_list = sum(W.HAZ * W.season(72 + i) * tr[k] for i, k in enumerate(keys))
    truth = exp_first + exp_list
    check("analyst test: the truth sits in the golden's bin", bin50(truth) == call, "truth %.1f (first %.1f, listed %.1f), golden %.1f" % (truth, exp_first, exp_list, g["total"]))
    check("analyst test: the default path files another bin", bin50(g["default"]) != call and g["default"] / truth > 1.3,
          "default %.1f, %.2f times the truth" % (g["default"], g["default"] / truth))

    # ---- the default path's back-tests (the textbook route validates)
    for base, tgt in (((2023,), 2024), ((2024,), 2025)):
        f = C.rate_forecast(L, P, base, tgt) * (1.0)
        act = (L.fy == tgt).sum()
        check("back-test FY%d rates on FY%d" % (base[0], tgt), abs(f / act - 1) < 0.05, "%.1f against %d (%+.1f%%)" % (f, act, 100 * (f / act - 1)))

    # ---- SF1 emergency methods: codes 21 to 2D and the EPR's Emergency methods, SDEC and other included (definitions 2)
    first = C.spells(P)
    em_codes = first[first.gall].admission_method.unique()
    check("SF1 every emergency method read", set(L.admission_method) <= set(m for m in em_codes if str(m).startswith(("2", "Emergency"))) and L.admission_method.str.contains("SDEC|2A").any(),
          "methods %s" % sorted(set(L.admission_method)))
    # ---- SF2 first finished consultant episode, not any episode
    ep = P.ep
    anyep = ep[ep.primary_diagnosis.str.replace(".", "", regex=False).str.replace(r"[^A-Z0-9]", "", regex=True).str[:4].str.match(C.GALL)]
    check("SF2 first episode's diagnosis, as the definition reads", len(L) <= anyep.provider_spell_no.nunique(), "%d against %d spells with any episode coded" % (len(L), anyep.provider_spell_no.nunique()))
    # ---- SF3 the code list read through the coding systems' formats
    raw = first[first.emergency & first.primary_diagnosis.str.match(r"^(K80|K81|K83\.?0|K85\.?1)")]
    check("SF3 suffix and dot forms normalised", len(raw) == len(L), "%d strict-prefix against %d normalised" % (len(raw), len(L)))
    # ---- SF4 window by admission date, SF12 nearest 50 of the central expectation
    check("SF4 financial year by admission date", set(L.fy) <= set(range(2021, 2027)))
    check("SF12 nearest 50 of the central expectation", call == 400, "call %d" % call)
    # ---- SF5 any residence: rates on residents with the out-of-area share added give the same call
    res = L[L.la_of_residence != "Out of area"]
    share = len(L[L.fy >= 2024]) / len(res[res.fy >= 2024])
    alt = C.rate_forecast(res[~res.listed], P) * share + g["listed_part"]
    check("SF5 residence: same call", bin50(alt) == call, "%.1f" % alt)
    # ---- SF6 central expectation (definitions 1); SF7 the plan's list, not the record's (definitions 1, capacity plan 3)
    donothing = g["first"] + g["hazard"] * pm.loc[[m for m in pm.index if m >= 55]].mean() * 12
    check("SF7 a list held at its record size files the default's bin, ruled out by the plan basis", bin50(donothing) != call, "%.1f" % donothing)
    check("SF6 central expectation, no prudence margin", abs(g["total"] - 407.7) < 0.1, "%.1f" % g["total"])
    # ---- SF8 2026 population from the projection or estimates, SF9 patient-month convention, SF10 hazard window,
    #      SF11 rate years and mid-year, SF13 on-list test, SF14 the number map (every licensed reading prints the call)
    fam = []
    for hy in [(2022, 2023, 2024, 2025, 2026), (2023, 2024, 2025, 2026), (2024, 2025, 2026), (2025, 2026)]:
        months = [m for m in pm.index if m // 12 + 2021 in hy]
        hz = L[L.listed & L.fy.isin(hy)].shape[0] / pm.loc[months].sum()
        for fy in [(2024, 2025, 2026), (2025, 2026), (2023, 2024, 2025, 2026), (2024, 2025)]:
            for tgt in (2027, 2028):
                f1 = C.rate_forecast(L[~L.listed], P, fy, 2027)
                f = f1 if tgt == 2027 else 0.5 * (f1 + C.rate_forecast(L[~L.listed], P, fy, 2028))
                for pmf in (g["pm_plan"], sum((a + b) / 2 for a, b in zip([tr["Mar 2027"]] + [tr[k] for k in keys][:-1], [tr[k] for k in keys]))):
                    fam.append(f + hz * pmf)
    nl = L[~L.listed]
    mc = nl.groupby("mi").size().reindex(range(0, 67), fill_value=0)
    for start in (12, 24, 36):
        b = np.polyfit(np.arange(start, 67), mc.values[start:], 1)
        months = [m for m in pm.index if m >= start]
        fam.append(np.polyval(b, np.arange(72, 84)).sum() + L[L.listed & (L.mi >= start)].shape[0] / pm.loc[months].sum() * g["pm_plan"])
    # share-scaling route: the rate method's figure split by the listed share and the list scaled to the plan
    hist_list = pm.loc[[m for m in pm.index if m >= 12]].mean()
    fam.append(C.rate_forecast(L[~L.listed], P) + g["default"] * 0 + L[L.listed & (L.mi >= 12)].shape[0] / pm.loc[[m for m in pm.index if m >= 12]].sum() * hist_list * 12 * (g["pm_plan"] / 12 / hist_list))
    check("SF8 SF9 SF10 SF11 the standing family prints the call", all(bin50(x) == call for x in fam), "%d routes, %.1f to %.1f" % (len(fam), min(fam), max(fam)))
    # SF13: exact intervals (pathway life from date added to its last month end) against the month-end test
    c = C.chole_list(P)
    life = c.groupby(["patient", "added"]).snap.max().reset_index()
    gl = {k: v for k, v in life.groupby("patient")}
    exact = []
    for pat, adm in zip(L.patient, L.admit):
        v = gl.get(pat)
        exact.append(bool(v is not None and ((v.added < adm) & (v.snap + pd.Timedelta(days=31) >= adm)).any()))
    L2 = L.copy()
    L2["listed"] = exact
    hz2 = L2[L2.listed & (L2.fy >= 2022)].shape[0] / pm.loc[[m for m in pm.index if m >= 12]].sum()
    alt13 = C.rate_forecast(L2[~L2.listed], P) + hz2 * g["pm_plan"]
    check("SF13 on-list test by interval: same call", bin50(alt13) == call, "%.1f" % alt13)
    # SF14: without the Fennick number map the listed share falls; the map is shipped, and the call holds either way
    P2 = C.Pack()
    P2.ep["patient"] = P2.ep.hospital_number
    P2.ptl["patient"] = P2.ptl.hospital_number
    alt14 = C.golden(P2)["total"]
    check("SF14 Fennick numbers through the map: same call", bin50(alt14) == call, "%.1f without the map" % alt14)

    # ---- the asks against the simulation's truth (one handling reproduces truth exactly)
    asks = C.ask_tables(P, "golden")
    pws = S["pathways"]
    ers = {r["ubrn"]: r["received"] for r in S["referrals"]}

    def true_clock(pw):
        if pw["prev"] is not None:     # a re-listing or a move: the wait began with the first pathway's referral
            return true_clock(pws[pw["prev"]])
        return ers[pw["ubrn"]] if pw["ubrn"] else pw["clock"]
    ok = True
    for d in C.QDATES:
        D = dt.date.fromisoformat(d)
        for site in W.SITES:
            open_ = [pw for pw in pws if pw["site"] == site and pw["added"] <= D and (pw["removed"] is None or pw["removed"] > D)]
            a = sum(1 for pw in open_ if (D - true_clock(pw)).days >= 364)
            b = sum(1 for pw in open_ if pw["group"] == "hernia")
            ok &= (a == asks[("A", d, site)]) and (b == asks[("B", d, site)])
            if not ((a == asks[("A", d, site)]) and (b == asks[("B", d, site)])):
                print("   ", d, site, a, asks[("A", d, site)], b, asks[("B", d, site)])
    check("SF15 SF16 SF17 SF18 ask goldens reproduce the simulation's truth", ok)
    # ---- separation line: the asks' devices leave the call's rows unchanged
    naive = C.ask_tables(P, "naive")
    check("asks: every Fennick cell and every 52-week cell moves under the PTL as shipped",
          all(asks[k] != naive[k] for k in asks if k[2] == "FEN" or k[0] == "A"))
    relist = [pw for pw in pws if pw["reason"] == "cancelled_relisted" and pw["group"] == "chole" and pw["removed"] <= W.RECORD_END]
    gap = sum(1 for pw in relist if not any(q["prev"] == pw["id"] and q["added"] == pw["removed"] for q in pws))
    check("separation: every re-listed cholecystectomy pathway reopens the day it closes (list presence unbroken)", gap == 0, "%d re-listings" % len(relist))
    check("separation: the moved pathways are hernia repairs only", all(pw["group"] == "hernia" for pw in pws if pw.get("moved_from") is not None))
    print("FAIL" if FAIL else "PASS", "%d failures" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
