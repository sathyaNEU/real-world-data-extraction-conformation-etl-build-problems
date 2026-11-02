"""The generator's assertions: the three rules on the clean truth (R1 to R3), the ladder and the cheap routes, every
semantic fork row (SF1 to SF22), the ask devices and their separation from the call, the rounding clearances, the
input gates and the realism sweep.  Run by build.py on every build; exit status follows the count of failures."""
import csv
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np
import openpyxl

import golden as G
import world as W

RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def edge(x, unit):
    f = (x / unit) % 1.0
    return abs(f - 0.5) * unit


def r0(x):
    return int(np.floor(x + 0.5))


def season_days(y):
    d = dt.date(y, 6, 1)
    while d <= dt.date(y, 9, 30):
        yield d
        d += dt.timedelta(1)


def read(T, fn):
    with open(os.path.join(T, fn), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run(TASK, T, S, F):
    RESULTS.clear()
    lk, rv, wk, sd = S["lake"], S["river"], S["works"], S["sondes"]
    idx = {d: i for i, d in enumerate(W.DAYS)}
    surf_true = lk["prof"][:, :6].mean(axis=1)
    rday_true = rv["temp"].reshape(-1, 24).mean(axis=1)
    rmax_true = rv["temp"].reshape(-1, 24).max(axis=1)

    # ------------------------------------------------------------------ R1: the field's raw material ships
    st = G.station_hourly(T)
    hrs = [u for u in st if 6 <= u.month <= 9 and u.year in W.SEASONS]
    ok("R1a station hourly temperature for every season hour", len(hrs) == 3 * 122 * 24, len(hrs))
    prof = G.buoy_profiles(T)
    full = all(len(prof[d]) == len(W.DEPTHS) for y in W.SEASONS for d in season_days(y))
    ok("R1b buoy profile at every depth on every season day", full)
    ret = G.returns(T)
    ok("R1c Hollinsby's effluent temperature and load in every season month",
       all(ret[("Hollinsby", y, m)]["temp"] is not None for y in W.SEASONS for m in (6, 7, 8, 9)))
    heads = []
    for fn in os.listdir(T):
        if fn.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(T, fn), encoding="utf-8")))
        elif fn.endswith(".xlsx"):
            for ws in openpyxl.load_workbook(os.path.join(T, fn), read_only=True).worksheets:
                for row in ws.iter_rows(max_row=3, values_only=True):
                    heads += [str(c) for c in row if c is not None]
    bad = [h for h in heads if re.search(r"insert|plung|interflow|entry depth|layer|thermocline|epilimn|density", h, re.I)]
    ok("R1d no column holds where an inflow enters the lake", not bad, bad)

    # ------------------------------------------------------------------ R2: Layer 1 present, never decisive
    val = read(T, "lenning_foot_hourly_validated.csv")
    stamps = [r["Timestamp (UK)"] for r in val]
    ok("R2a the station's clock repeats the October hour", stamps.count("29/10/2023 01:00") == 2)
    ok("R2a the station's clock skips the March hour", "31/03/2024 01:00" not in stamps)
    prov = {r["Timestamp (UK)"]: r for r in read(T, "lenning_foot_hourly_provisional.csv")}
    diff = sum(1 for r in val if r["Timestamp (UK)"] in prov and r["Flow (m3/s)"] != prov[r["Timestamp (UK)"]]["Flow (m3/s)"])
    ok("R2b the provisional release differs from the validated where they overlap", diff > 50, diff)
    wb = openpyxl.load_workbook(os.path.join(T, "fellmoor_wwtw_monthly_returns.xlsx"), read_only=True)
    h24 = [c for c in next(wb["2024-25"].iter_rows(min_row=3, max_row=3, values_only=True))]
    h25 = [c for c in next(wb["2025-26"].iter_rows(min_row=3, max_row=3, values_only=True))]
    ok("R2c the returns' layout changes with the 2025-26 reporting year", h24 != h25)
    sites = {r["site"] for r in read(T, "fellside_lake_lab_results.csv")}
    ok("R2d the laboratory's site codes change in 2025", sites == {"NB", "SWL01"}, sites)
    # the call is the same with the river's day read on the station's clock rather than UTC
    acc = {}
    for r in val + list(prov.values()):
        d = G.parse_uk(r["Timestamp (UK)"]).date()
        acc.setdefault(d, []).append(float(r["Water temp (C)"]))
    surf = G.buoy_surface(T)
    loc = all(W.density(np.mean(acc[d])) > W.density(surf[d]) for y in W.SEASONS for d in season_days(y))
    ok("R2e the river is denser on every season day with its day on the station's clock", loc)

    # ------------------------------------------------------------------ R3: the analyst test on the clean truth
    colder = all(rday_true[idx[d]] < surf_true[idx[d]] for y in W.SEASONS for d in season_days(y))
    ok("R3a clean truth: the Lenning is colder than the 0-5 m water on every season day", colder)
    dens = all(W.density(rday_true[idx[d]]) > W.density(surf_true[idx[d]]) for y in W.SEASONS for d in season_days(y))
    ok("R3b clean truth: the Lenning is denser than the 0-5 m water on every season day", dens)
    strat = all(lk["strat"][idx[d]] for y in W.SEASONS for d in season_days(y))
    ok("R3c clean truth: the lake is stratified on every season day", strat)
    clean_rung1 = {}
    for k, nm in (("B", "Brathwick"), ("C", "Hollinsby")):
        clean_rung1[k] = np.mean([W.CREDIT[k] * sum(wk[nm]["load"][idx[d]] for d in season_days(y)) for y in W.SEASONS])
    ok("R3d clean truth: the easy route (every input to the surface water) files Brathwick",
       clean_rung1["B"] > 1.15 * clean_rung1["C"], {k: round(v, 1) for k, v in clean_rung1.items()})
    c10 = [sd["cond"][idx[d], 2] for y in W.SEASONS for d in (dt.date(y, 6, 1), dt.date(y, 9, 30))]
    c1 = [sd["cond"][idx[d], 0] for y in W.SEASONS for d in (dt.date(y, 6, 1), dt.date(y, 9, 30))]
    rise10 = all(c10[2 * j + 1] - c10[2 * j] > 20 for j in range(3))
    flat1 = all(abs(c1[2 * j + 1] - c1[2 * j]) < 8 for j in range(3))
    ok("R3e clean truth: the river's water collects at 10 m and not at 1 m", rise10 and flat1, (c10, c1))

    # ------------------------------------------------------------------ the ladder and the cheap routes
    seas, ap, ins = G.season_figures(T)
    dp, an = G.default_path(T), G.annual_path(T)
    m1 = {k: float(np.mean([dp[y][k] for y in W.SEASONS])) for k in "ABCD"}
    m0 = {k: float(np.mean([an[y][k] for y in W.SEASONS])) for k in "ABCD"}
    gold = {"A": 0.0, "B": F["B_mean"], "C": F["C_mean"], "D": F["D_mean"]}

    def top(m):
        s = sorted(m, key=lambda k: -m[k])
        return s[0], m[s[0]] / max(m[s[1]], 1e-9), s
    t0, g0, s0 = top(m0)
    t1, g1, s1 = top(m1)
    t2, g2, s2 = top(gold)
    ok("L1 rung 0, the annual inventory, files the farms", t0 == "A" and g0 >= 1.15, (s0, round(g0, 3)))
    ok("L2 rung 1, the season's load budget, files Brathwick", t1 == "B" and g1 >= 1.15, (s1, round(g1, 3)))
    ok("L3 the decisive rung files Hollinsby", t2 == "C" and g2 >= 1.2, (s2, round(g2, 2)))
    ok("L4 Hollinsby is first on no rung below the decisive one", t0 != "C" and t1 != "C")
    ok("L5 Hollinsby is no better than second on rung 1 and third on rung 0", s1.index("C") == 1 and s0.index("C") == 2)
    cost = {"A": 1248000, "B": 1176000, "C": 1337000, "D": 612000}
    ce = {k: m1[k] / cost[k] for k in "ABCD"}
    ok("L6 kilograms per pound on the season's loads files Brathwick, not Hollinsby", top(ce)[0] == "B", ce)
    routes = {"annual inventory": t0, "season load budget": t1, "cost per kilogram": top(ce)[0],
              "insertion by density": t2}
    landing = [k for k, v in routes.items() if v == "C"]
    ok("L7 one cheap route reaches the call", landing == ["insertion by density"], routes)
    # the textbook route validates: the river's summer phosphorus falls with flow (dilution of a point source)
    bot = [b for b in G.sampler(T) if b["kind"] == "DAY" and 6 <= b["first"].month <= 9]
    fl = {}
    for u, v in st.items():
        fl.setdefault(u.date(), []).append(v["flow"])
    xs = [np.log(np.mean(fl[b["first"].date()])) for b in bot]
    ys = [np.log(b["tp"]) for b in bot]
    slope = float(np.polyfit(xs, ys, 1)[0])
    share = np.mean([seas[y]["bra"] / dp[y]["river"] for y in W.SEASONS])
    ok("L8 the back-test passes: summer concentration dilutes with flow and Brathwick is most of the river's load",
       slope < -0.2 and share > 0.6, (round(slope, 3), round(float(share), 3)))

    # ------------------------------------------------------------------ the semantic fork table
    ins_rows = ins
    # SF1 surface water: 0 to 5 m (fund rules 2.1); read as the mixed layer, the river still enters below it
    below_mixed = True
    for y in W.SEASONS:
        for d in season_days(y):
            p = prof[d]
            zs = sorted(p)
            tr = float(np.mean(acc[d]))
            mixed = [z for z in zs if p[z] >= p[zs[0]] - 0.5]
            below_mixed &= tr < min(p[z] for z in mixed)
    ok("SF1 the Lenning is colder than every sensor in the mixed layer on every season day", below_mixed)
    # SF2 the season's days in UTC or on the UK clock: the same days compared, every one dense
    ok("SF2 every season day dense on either clock", all(ins_rows[y]["dense"] == ins_rows[y]["n"] == 122 for y in W.SEASONS) and loc)
    # SF3 Hollinsby's effluent is warmer than the surface water in every season month (it spreads at the top)
    eb = G.effluent_buoyancy(T)
    ok("SF3 Hollinsby's effluent warmer than the 0-5 m water in every season month", all(a > b + 1.0 for a, b in eb.values()))
    # SF4 the credit applied to the source's season input: C and D by their credits
    ok("SF4 programme C is 71 per cent and D 50 per cent of their sources' season input",
       all(abs(seas[y]["C"] - 0.71 * seas[y]["hol"]) < 1e-9 and abs(seas[y]["D"] - 0.5 * seas[y]["out"]) < 1e-9 for y in W.SEASONS))
    # SF5 the mean of the seasons, or the mean of the rounded seasons: the same printed figures
    for k in "CD":
        a = r0(F["%s_mean" % k])
        b = r0(np.mean([r0(F["%s_%d" % (k, y)]) for y in W.SEASONS]))
        ok("SF5 %s's average prints the same from the rounded seasons" % k, a == b, (a, b))
    # SF6 the returns' load column or volume times concentration: the same printed figures
    raw = {}
    for y in W.SEASONS:
        raw[y] = 0.71 * sum(ret[("Hollinsby", y, m)]["vol"] * ret[("Hollinsby", y, m)]["tp"] / 1000.0 for m in (6, 7, 8, 9))
    ok("SF6 Hollinsby's figures print the same from volume times concentration",
       all(r0(raw[y]) == r0(F["C_%d" % y]) for y in W.SEASONS) and r0(np.mean(list(raw.values()))) == r0(F["C_mean"]))
    # SF7 the reporting-year tabs: every season month held once
    ok("SF7 every season month appears once across the reporting-year tabs",
       all(("Hollinsby", y, m) in ret and ("Brathwick", y, m) in ret for y in W.SEASONS for m in (6, 7, 8, 9)))
    # SF8 the river's day as its mean, or its warmest hour: colder than the surface water either way
    sf8 = all(max(st[u]["temp"] for u in st if u.date() == d) < surf[d] for y in W.SEASONS for d in season_days(y))
    ok("SF8 the river's warmest hour is colder than the 0-5 m water on every season day", sf8)
    # SF9 the surface water's temperature as the 0-5 m mean, the 1 m sensor or the 0.5 m sensor
    sf9 = all(min(prof[d][0.5], prof[d][1.0], surf[d]) > float(np.mean(acc[d])) + 1.0 for y in W.SEASONS for d in season_days(y))
    ok("SF9 the river colder than the 0.5 m, 1 m and 0-5 m water on every season day", sf9)
    # SF10 density with the river's dissolved salts (its conductivity is above the lake's): denser still
    rc = np.mean([float(r["Conductivity (mS/m)"]) * 10 for r in val[:2000]])
    lc = np.mean([float(r["Specific conductance (uS/cm)"]) for r in read(T, "fellside_buoy_sondes_daily.csv")[:500] if r["Depth (m)"] == "1"])
    ok("SF10 the river carries more dissolved salts than the surface water", rc > lc, (round(rc), round(lc)))
    # SF11 Brathwick's effluent: enters the Lenning; even its own temperature is below the surface water's
    sf11 = all(ret[("Brathwick", y, m)]["temp"] < eb[(y, m)][1] for y in W.SEASONS for m in (6, 7, 8, 9))
    ok("SF11 Brathwick's effluent colder than the 0-5 m water in every season month", sf11)
    # SF12 the Mill Beck outfall warmer than the surface water on every season day
    wbm = openpyxl.load_workbook(os.path.join(T, "mill_beck_outfall_monitoring.xlsx"), data_only=True)
    otemp = {}
    for row in list(wbm["Daily"].iter_rows(min_row=3, values_only=True)):
        otemp[row[0].date() if hasattr(row[0], "date") else row[0]] = row[2]
    ok("SF12 the Mill Beck outfall warmer than the 0-5 m water on every season day",
       all(otemp[d] > surf[d] for y in W.SEASONS for d in season_days(y)))
    # SF13 the farm programme acts on the Lenning's catchment (the Brankell Beck's farms included): zero either way
    ok("SF13 programmes A and B keep nothing out of the surface water", F["A_mean"] == 0 and F["B_mean"] == 0)
    # SF14 the 2027 season is judged on 2024 to 2026: no forecast enters
    ok("SF14 the figures use the 2024, 2025 and 2026 seasons only", sorted(seas) == [2024, 2025, 2026])
    # SF15 the runner-up: D clear of A and B at zero
    ok("SF15 the runner-up is D with a figure above zero", s2[1] == "D" and F["D_mean"] > 10, s2)
    # SF16 phosphorus as total phosphorus; on soluble reactive phosphorus the river still enters below
    ok("SF16 the returns give total phosphorus for both works", all(ret[("Hollinsby", y, m)]["tp"] > 0 for y in W.SEASONS for m in (6, 7, 8, 9)))

    # ------------------------------------------------------------------ asks: devices, stops and separation
    wa = G.winter_ask(T)[(2023, 2024)]
    reg = G.regulator(T)
    bridge = reg["LENNING BRIDGE"]
    brankell = reg["BRANKELL BECK AT HOWE"]
    pre = [u for u in st if u.date() < W.GAUGE_SWITCH and u in bridge]
    post = [u for u in st if W.GAUGE_SWITCH <= u.date() < dt.date(2026, 1, 1) and u in bridge]
    ok("SF17 the station's flow is the Lenning Bridge gauge before 1 June 2024",
       all(abs(st[u]["flow"] - bridge[u]) < 0.0011 for u in pre), len(pre))
    ok("SF17 the station's flow is both gauges from 1 June 2024",
       all(abs(st[u]["flow"] - bridge[u] - brankell[u]) < 0.0021 for u in post), len(post))
    conc = G.hourly_conc(T)
    a = dt.datetime(2023, 9, 30, 23)
    z = dt.datetime(2024, 4, 30, 23)

    def winter(add_brankell=True, storm=True, shift=0, start=a, stop=z):
        cm = conc if storm else {}
        if not storm:
            for b in G.sampler(T):
                if b["kind"] == "DAY":
                    u0 = b["first"] - dt.timedelta(hours=W.uk_offset(b["first"]))
                    u1 = b["last"] - dt.timedelta(hours=W.uk_offset(b["last"]))
                    t = u0
                    while t <= u1:
                        cm[t] = b["tp"]
                        t += dt.timedelta(hours=1)
        vol = load = 0.0
        t = start
        while t < stop:
            q = st[t]["flow"] + (brankell[t] if add_brankell and t.date() < W.GAUGE_SWITCH else 0.0)
            c = cm.get(t + dt.timedelta(hours=shift))
            if c is None:
                c = conc[t]
            vol += q * 3600
            load += q * 3600 * c / 1e6
            t += dt.timedelta(hours=1)
        return vol / 1e6, load
    g_in, g_ld = round(wa["vol"], 1), int(np.floor(wa["load"] / 100 + 0.5)) * 100
    ok("SF18 the winter window on UTC days prints the same", tuple(np.round(winter(start=a + dt.timedelta(hours=1), stop=z + dt.timedelta(hours=1)), 1))[0] == g_in
       and int(np.floor(winter(start=a + dt.timedelta(hours=1), stop=z + dt.timedelta(hours=1))[1] / 100 + 0.5)) * 100 == g_ld)
    sh = [int(np.floor(winter(shift=s)[1] / 100 + 0.5)) * 100 for s in (-1, 1)]
    ok("SF19 pairing each flow with the sub-sample an hour either side prints the same load", sh == [g_ld, g_ld], sh)
    ns_in, ns_ld = winter(add_brankell=False)
    ok("K1 the station's flow alone misses the inflow and the load",
       round(ns_in, 1) != g_in and int(np.floor(ns_ld / 100 + 0.5)) * 100 != g_ld, (round(ns_in, 1), round(ns_ld)))
    db_in, db_ld = winter(storm=False)
    ok("K1 the day bottle for every hour misses the load", int(np.floor(db_ld / 100 + 0.5)) * 100 != g_ld, round(db_ld))
    # survey
    regs = {r["UPRN"]: r for r in read(T, "hollinsby_address_register_extract.csv")}
    vis = read(T, "connect_right_visits_export.csv")
    mis_u = {v["UPRN"] for v in vis if v["Outcome"] == "MISCONNECTED"}
    fix_u = {v["UPRN"] for v in vis if v["Outcome"] == "FIX CONFIRMED"}
    up = {v["UPRN"] for v in vis if v["Outcome"] == "FIX CONFIRMED" and dt.datetime.strptime(v["Uploaded"], "%d/%m/%Y").date() <= dt.date(2026, 9, 30)}
    ok("K2 counting addresses misses all three dwelling figures",
       len(mis_u) != F["dw_found"] and len(fix_u & mis_u) != F["dw_fixed"] and len(mis_u - fix_u) != F["dw_open"],
       (len(mis_u), len(fix_u & mis_u), len(mis_u - fix_u)))
    flats = {}
    for u, r in regs.items():
        if r["PARENT_UPRN"]:
            flats.setdefault(r["PARENT_UPRN"], []).append(u)

    def dw(us):
        s = set()
        for u in us:
            s.update(flats.get(u) or [u])
        return s
    nodate = len(dw(fix_u) & dw(mis_u))
    byup = len(dw(up) & dw(mis_u))
    ok("K2 every flat counted but the visits dated by upload misses fixed and not fixed",
       byup != F["dw_fixed"] and len(dw(mis_u)) - byup != F["dw_open"], byup)
    ok("K2 every flat counted but no date cut misses fixed and not fixed", nodate != F["dw_fixed"], nodate)
    ok("SF20 the golden equals the clean truth's dwellings",
       F["dw_found"] == len(S["survey"]["truth"]["mis_dwell"]) and F["dw_fixed"] == len(S["survey"]["truth"]["fixed_dwell"]))
    refd = [dt.datetime.strptime(v["Visit ref"].split("-")[1], "%y%m%d").date() for v in vis]
    upd = [dt.datetime.strptime(v["Uploaded"], "%d/%m/%Y").date() for v in vis]
    ok("SF21 every upload on or after the date its visit reference carries", all(u >= r for u, r in zip(upd, refd)))
    ok("SF21 no visit reference dated on a weekend", all(r.weekday() < 5 for r in refd))
    # laboratory
    lab = read(T, "fellside_lake_lab_results.csv")
    nb_after = [r for r in lab if r["site"] == "NB" and dt.datetime.strptime(r["sampled"], "%d-%b-%Y").date() >= dt.date(2025, 4, 1)]
    ok("SF22 NB carries no 20 m bottle from April 2025", all(r["depth_m"] == "0-5" for r in nb_after) and nb_after)
    sw = [r for r in lab if r["site"] == "SWL01"]
    ok("SF22 SWL01 carries the tube and the 20 m bottle", {r["depth_m"] for r in sw} == {"0-5", "20"})
    for y in (2025, 2026):
        acc_nb = {"Total phosphorus": [], "Chlorophyll a": []}
        for r in lab:
            d = dt.datetime.strptime(r["sampled"], "%d-%b-%Y").date()
            if r["site"] == "NB" and d.year == y and 6 <= d.month <= 9 and r["depth_m"] == "0-5":
                acc_nb[r["determinand"]].append(float(r["result"]))
        ok("K3 the site code the plan files misses %d's phosphorus and chlorophyll" % y,
           round(np.mean(acc_nb["Total phosphorus"]), 1) != round(F["tp_%d" % y], 1)
           and round(np.mean(acc_nb["Chlorophyll a"]), 1) != round(F["chl_%d" % y], 1))
    q_in = [r for r in lab if r["qualifier"] and r["site"] == "SWL01" and dt.datetime.strptime(r["sampled"], "%d-%b-%Y").month in (6, 7, 8, 9)]
    ok("SF22 no below-detection result in the north basin's season samples", not q_in)
    # separation: no device row in the main call's population
    ok("K4 every season day the call reads is after the gauge switch", all(dt.date(y, 6, 1) >= W.GAUGE_SWITCH for y in W.SEASONS))
    storm_season = [b for b in G.sampler(T) if b["kind"] == "STORM" and 5 <= b["first"].month <= 9]
    ok("K4 no storm bottle in May to September", not storm_season)

    # ------------------------------------------------------------------ rounding clearances
    for k in ("C_2024", "C_2025", "C_2026", "C_mean", "D_2024", "D_2025", "D_2026", "D_mean", "gap"):
        ok("E %s clear of its rounding edge" % k, edge(F[k], 1) >= 0.15, round(F[k], 3))
    ok("E the gap prints the same from the printed averages", r0(F["C_mean"]) - r0(F["D_mean"]) == r0(F["gap"]))
    ok("E the winter inflow clear of its rounding edge", edge(F["inflow_2023_24"], 0.1) >= 0.015, F["inflow_2023_24"])
    ok("E the winter load clear of its rounding edge", edge(F["load_2023_24"], 100) >= 15, F["load_2023_24"])
    for k in ("tp_2025", "tp_2026", "chl_2025", "chl_2026"):
        ok("E %s clear of its rounding edge" % k, edge(F[k], 0.1) >= 0.02, F[k])

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(T))
    ok("G1 ten or more files", len(files) >= 10, len(files))
    ok("G2 three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(T, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok("G3 a file of 25,000 rows or more", big >= 25000, big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("G4 two or more distractors, each shipped", len(meta["distractor_files"]) >= 2
       and all(os.path.exists(os.path.join(TASK, d)) for d in meta["distractor_files"]))
    ok("G5 every file has provenance", all("target/" + f in meta["files"] for f in files))
    ok("G6 no describing file", not [f for f in files if re.search(r"readme|dictionary|manifest|codebook|notes|schema", f, re.I)])
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += openpyxl.load_workbook(os.path.join(T, f), read_only=True).sheetnames
    ok("G6 no describing sheet", not [s for s in sheets if re.search(r"readme|notes|dictionary|about|key|legend", s, re.I)], sheets)
    m = S["monthly"]
    hl = [m[k]["load"] for k in sorted(m) if k[0] == "Hollinsby"]
    ok("G7 no monthly load repeated three times or three months running",
       max(hl.count(v) for v in hl) < 3 and all(not (a == b == c) for a, b, c in zip(hl, hl[1:], hl[2:])))
    ok("G7 no round headline figure", all(r0(F[k]) % 10 != 0 for k in ("C_mean", "D_mean", "gap")))
    people = {"Debra Rose", "Dominic Davies", "Oliver Thomas"}
    named = set()
    for f in files:
        if f.endswith(".xlsx"):
            core = zipfile.ZipFile(os.path.join(T, f)).read("docProps/core.xml").decode()
            named.update(re.findall(r"<dc:creator>([^<]*)</dc:creator>", core))
            named.update(re.findall(r"<cp:lastModifiedBy>([^<]*)</cp:lastModifiedBy>", core))
    ok("G8 every person in a container is one of the build's personas", named <= people, named)
    stamp = dt.datetime(2026, 11, 9, 16, 42).timestamp()
    ok("G9 every file stamped when the folder was assembled", all(abs(os.path.getmtime(os.path.join(T, f)) - stamp) < 1 for f in files))
    pdfs = [open(os.path.join(T, f), "rb").read() for f in files if f.endswith(".pdf")]
    ok("G9 no PDF names its toolchain", all(b"ReportLab" not in p and b"reportlab" not in p for p in pdfs))
    emitted = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    ok("G10 figures.json carries the call and the runner-up", emitted["call"] == "C" and emitted["runner_up"] == "D")

    # the measured values the design note quotes, printed so each has a script behind it
    print("ladder rung 0 (annual inventory): " + ", ".join("%s %.1f" % (k, m0[k]) for k in "ABCD"))
    print("ladder rung 1 (season load budget): " + ", ".join("%s %.1f" % (k, m1[k]) for k in "ABCD"))
    print("ladder decisive: " + ", ".join("%s %.1f" % (k, gold[k]) for k in "ABCD")
          + "; entrainment share at which B passes C %.2f" % (gold["C"] / m1["B"]))
    print("back-test: log slope %.3f, Brathwick's share of the river's season load %.3f" % (slope, share))
    print("10 m conductivity rise by season %s; 1 m change %s" % ([round(c10[2 * j + 1] - c10[2 * j], 1) for j in range(3)],
                                                                  [round(c1[2 * j + 1] - c1[2 * j], 1) for j in range(3)]))
    print("winter stops: station alone %.1f / %d kg; day bottle for every hour %d kg; dwellings by address %d / %d / %d;"
          " flats by upload %d fixed; flats no date cut %d fixed" % (ns_in, ns_ld, db_ld, len(mis_u), len(fix_u & mis_u),
                                                                    len(mis_u - fix_u), byup, nodate))
    fails = [r for r in RESULTS if not r[1]]
    for label, good, detail in RESULTS:
        if not good:
            print("FAIL", label, detail)
    print("checks: %d assertions, %d failed" % (len(RESULTS), len(fails)))
    return not fails
