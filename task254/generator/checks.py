"""Every assertion the design note owes: the semantic fork rows SF1 to SF13, the ladder's stage 3 acceptance
criteria and the grid, the closures, the hazard ledger and the separation line, the ask stops and every subset of
mishandlings, the chart, the bin distances, the input gates, the counter-pin sweep and the realism sweep."""
import glob
import json
import math
import os
import re
import zipfile

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import analysis as AN
import asks as A
import core
import golden as GD
import pack as P
import world as WD

RESULTS = []
VARIANTS = AN.VARIANTS


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def clear(x, unit=1.0):
    return abs(((x / unit) % 1.0) - 0.5)          # distance from the rounding boundary, in steps


def route_rows(target):
    """The route's rows of the twelve exports: (working-weekday index, epoch, segment) arrays of the passenger
    time, the passenger speed and the all-vehicle time, and every route row's density flag with its day and minute."""
    days = [d for d in core.days() if core.working(d)]
    di = {d.isoformat(): i for i, d in enumerate(days)}
    codes = [r[0] for r in core.ROUTE]
    ci = {c: k for k, c in enumerate(codes)}
    shape = (len(days), core.NE, len(codes))
    tp, sp = np.full(shape, np.nan), np.full(shape, np.nan)
    dens, dup, months = [], 0, {}
    for f in sorted(glob.glob(os.path.join(target, "trelvane_tmc_export_*.csv"))):
        df = pd.read_csv(f, dtype={"tmc_code": str, "measurement_tstamp": str, "data_density": str})
        dup += int(df.duplicated(["tmc_code", "measurement_tstamp"]).sum())
        months[os.path.basename(f)] = sorted(set(df.measurement_tstamp.str[:7]))
        df = df[df.tmc_code.isin(ci)]
        mins = df.measurement_tstamp.str[11:13].astype(int) * 60 + df.measurement_tstamp.str[14:16].astype(int)
        dens.append(pd.DataFrame({"day": df.measurement_tstamp.str[:10], "min": mins, "d": df.data_density}))
        w = df.measurement_tstamp.str[:10].isin(di)
        df, mins = df[w], mins[w]
        i = df.measurement_tstamp.str[:10].map(di).to_numpy()
        e = ((mins - core.E0) // 5).to_numpy()
        k = df.tmc_code.map(ci).to_numpy()
        tp[i, e, k] = df.travel_time_passenger.to_numpy(float)
        sp[i, e, k] = df.speed_passenger.to_numpy(float)
    return days, tp, sp, pd.concat(dens), dup, months


def run(W, S, F, G, target, golden_dir, task_dir, docs_text):
    del RESULTS[:]
    work = W["work"]
    tt = W["route"][work]
    N, need, call = F["N"], F["need"], F["call"]
    nxt = call + 5
    gc = F["golden_counts"]
    deps = core.DEPARTURES
    std, readme = docs_text["standard"], docs_text["readme"]
    prompt = open(os.path.join(task_dir, "prompt.txt")).read()
    grid = F["grid"]

    # ---------------------------------------------------------------- the call
    ok("call is 7:05", call == 7 * 60 + 5, call)
    ok("252 working weekdays, bar 227", N == 252 and need == 227, (N, need))
    ok("at least 8 days above the bar at the call", gc[call] - need >= 8, gc[call])
    ok("at least 15 days below the bar at the next departure", need - gc[nxt] >= 15, gc[nxt])
    ok("on-time counts fall with the departure", all(gc[a] >= gc[b] for a, b in zip(deps, deps[1:])))

    # ---------------------------------------------------------------- semantic fork rows
    ok("SF1 the prompt asks for the latest five-minute departure", "the latest five-minute departure" in prompt)
    ok("SF1 no later departure meets the bar", all(gc[d] < need for d in deps if d > call))
    ok("SF2 no arrival within a second of 8:00 at any departure, any convention",
       min(F["nearest_seconds"].values()) >= 1.0, min(F["nearest_seconds"].values()))
    ok("SF2 strictly before 8:00 gives the same counts", all(grid["strict"][d] == gc[d] for d in deps))
    ok("SF3 working weekday filed", "A working weekday is a Monday to Friday that is not a hospital holiday in the "
                                    "HR holiday calendar." in std)
    ok("SF3 holidays kept: same call", grid["holidays_kept"] == call and grid["weekdays_all"] == 261,
       (grid["holidays_kept"], grid["weekdays_all"]))
    ok("SF4 the bar 226.8 gives 227 under at least and more than", math.ceil(0.9 * N) == 227 and gc[call] > 0.9 * N
       and gc[nxt] < 0.9 * N)
    ok("SF5 passenger class filed", "Trip times use the passenger-vehicle travel times in the vendor's export." in std)
    ok("SF5 all vehicles: same call", grid["class_all"] == call, grid["class_all"])
    ok("SF5 freight: another call, ruled out by the standard", grid["class_freight"] != call, grid["class_freight"])
    ok("SF6 trip filed with the route file's fixed legs", "along the route in the route file, with the route file's "
                                                          "fixed legs" in std)
    ok("SF6 no legs: another call, ruled out by the standard", grid["no_legs"] != call, grid["no_legs"])
    for v in VARIANTS:
        ok("SF7 %s convention: the same counts at every departure" % v,
           all(F["walked"][v][d] == gc[d] for d in deps), F["walked"][v])
    herd_ok = True
    for i in range(len(tt)):
        for dep in WD.HERD_DEPS:
            arr = np.array([core.walk(tt[i][None], dep, v)[0] for v in VARIANTS])
            if not ((arr <= core.BAR_TIME - WD.MARGIN).all() or (arr > core.BAR_TIME + WD.MARGIN).all()):
                herd_ok = False
    ok("SF7 every working weekday 15 seconds clear of 8:00 under every convention, 6:50 to 7:20", herd_ok)
    lam = np.array(list(W["herded"].values()))
    ok("SF7 herding factors within 25 per cent of 1", len(lam) == 0 or (np.abs(lam - 1) <= 0.25).all(),
       (len(lam), lam.min() if len(lam) else None, lam.max() if len(lam) else None))
    ok("SF8 every working weekday counts, filed", "Every working weekday counts, whatever happened on the road that "
                                                  "day." in std)
    ok("SF8 incident days dropped: same call", grid["incidents_dropped_walk"] == call, grid["incidents_dropped_walk"])
    ok("SF9 the 90th percentile of each departure's trips: same call", grid["p90_rule"] == call, grid["p90_rule"])
    ok("SF10 local time filed", "start of the five-minute epoch, local time (Eastern)" in readme)
    last = max(float(core.walk(tt, d, v).max()) for d in deps for v in VARIANTS)
    ok("SF10 every trip ends inside the export's epochs", last < core.E0 + 5 * core.NE, last)

    days, tp, sp, dens, dup, months = route_rows(target)
    ok("SF12 every route segment carries a passenger time in every morning epoch of every working weekday",
       not np.isnan(tp).any())
    wk = {d.isoformat() for d in days}
    dm = dens[dens.day.isin(wk) & (dens["min"] >= 6 * 60 + 30)]
    ok("SF12 densities A and B only on the route's working-weekday rows from 6:30",
       set(dm.d.unique()) <= {"A", "B"} and len(dm) > 0, sorted(dm.d.unique()))
    walked = {d: int((core.walk(tp, d) <= core.BAR_TIME).sum()) for d in deps}
    ok("shipped passenger times walk to the golden counts", walked == gc, walked)
    miles = np.array([r[4] for r in core.ROUTE])
    tsp = miles[None, None, :] / sp * 3600
    by_speed = {d: int((core.walk(tsp, d) <= core.BAR_TIME).sum()) for d in deps}
    ok("SF13 length over the rounded speed: the same counts at every departure", by_speed == gc, by_speed)

    # SF11: the route file's codes, the releases and the road order
    rf = load_workbook(os.path.join(target, P.FILES["route"]), read_only=True)["Route"]
    rrows = [r for r in rf.iter_rows(values_only=True) if r and isinstance(r[0], int)]
    ok("SF11 the route file lists the sixteen codes in order between the two legs",
       [r[3] for r in rrows if r[1] == "TMC"] == [r[0] for r in core.ROUTE] and rrows[0][1] == "Leg"
       and rrows[-1][1] == "Leg" and rrows[0][4] == core.LOT_LEG and rrows[-1][4] == core.STOP_LEG)
    tmc = pd.read_csv(os.path.join(target, P.FILES["tmc"]), dtype={"tmc": str, "network_release": str})
    r25 = tmc[tmc.network_release == P.RELEASE_2025].set_index("tmc")
    r26 = tmc[tmc.network_release == P.RELEASE_2026].set_index("tmc")
    rc = [r[0] for r in core.ROUTE]
    cols = ["road", "direction", "intersection", "miles", "road_order"]
    ok("SF11 no route code differs between the releases", all((r25.loc[c, cols] == r26.loc[c, cols]).all() for c in rc))
    ok("SF11 the route runs I-65 northbound 1 to 13 then S Brook St 1 to 3",
       list(r26.loc[rc, "road_order"]) == list(range(1, 14)) + [1, 2, 3])

    # ---------------------------------------------------------------- the ladder and the grid
    ok("R0 (default path) at 7:15", F["R0"] == 7 * 60 + 15, F["R0"])
    ok("R0 clears its bar at 7:15 by at least 8 days", F["R0_counts"][7 * 60 + 15] - need >= 8,
       F["R0_counts"][7 * 60 + 15])
    ok("R1 at 7:10", F["R1"] == 7 * 60 + 10, F["R1"])
    ok("R2 at 7:10", F["R2"] == 7 * 60 + 10, F["R2"])
    ok("R3 at 7:00", F["R3"] == 7 * 60, F["R3"])
    ok("the median profile walked is not the call", F["P50"] != call, F["P50"])
    ok("grid: departure period with incident days dropped is not the call", grid["incidents_dropped_R0"] != call)
    ok("grid: midpoint with incident days dropped is not the call", grid["incidents_dropped_R2"] != call)
    ok("walked trips at the default path's 7:15 far below the bar", F["walked_715"] <= need - 60, F["walked_715"])
    kinds = W["kind"][work]
    brk = kinds == "break"
    ok("break days on time through the call under the walked and the departure-period constructions",
       all((core.walk(tt[brk], d) <= core.BAR_TIME).all() and (core.at_departure(tt[brk], d) <= core.BAR_TIME).all()
           for d in deps if d <= call))
    ok("no observed trip in the pack: no file carries an arrival, a run or a GPS column",
       not any(re.search(r"arriv|gps|run_id|trip_id|odometer", open(f, errors="ignore").readline().lower())
               for f in glob.glob(os.path.join(target, "*.csv"))))

    # ---------------------------------------------------------------- closures
    ok("C1 no duplicate segment-epoch rows in any export", dup == 0, dup)
    ok("C1 each monthly export holds its own month only",
       all(v == [k.split("_")[-1][:7]] for k, v in months.items()), months)
    ok("C1 twelve monthly exports", len(months) == 12)

    # ---------------------------------------------------------------- the separation line and the devices
    main_files = {P.FILES[k] for k in P.FILES if k.startswith("probe_")} | {P.FILES[k] for k in
                                                                            ("route", "standard", "holidays", "readme")}
    dev_files = {P.FILES[k] for k in ("reassign", "hr", "charges", "budget", "deadhead", "notice")}
    ok("separation: the ask files are not the main call's", not main_files & dev_files)
    dh = load_workbook(os.path.join(target, P.FILES["deadhead"]), read_only=True)["Deadhead"]
    drows = [r for r in dh.iter_rows(values_only=True) if r and isinstance(r[0], int)]
    dcodes = [r[3] for r in drows if r[1] == "TMC"]
    ok("separation: no deadhead or ramp code on the route",
       not set(dcodes + [core.RAMP_2025, core.RAMP_2026] + [r[0] for r in core.T1_NEW]) & set(rc))
    ok("T1 the deadhead file lists the reissued code", core.T1_OLD in dcodes and dcodes == [r[0] for r in core.DEADHEAD])
    ok("T1 the code is on I-65 southbound in 2025.2 and the I-264 ramp in 2026.1",
       r25.loc[core.T1_OLD, "road"] == "I-65" and r26.loc[core.T1_OLD, "road"] == "I-264"
       and float(r25.loc[core.T1_OLD, "miles"]) == 1.21 and float(r26.loc[core.T1_OLD, "miles"]) == 0.52)
    ok("T1 every other deadhead code is the same in both releases",
       all((r25.loc[c, cols[:4]] == r26.loc[c, cols[:4]]).all() for c in dcodes if c != core.T1_OLD))
    ok("T1 the replacing codes add to the old code's length",
       abs(sum(float(r26.loc[r[0], "miles"]) for r in core.T1_NEW) - 1.21) < 1e-9)
    ok("T1 release 2025.2 was in force when the deadhead route was set up",
       r25.effective_date.iloc[0] <= "2025-10-14" < r26.effective_date.iloc[0])
    ok("T1 the reissued code has rows in every month (no gap)", all(
        int((pd.read_csv(f, usecols=["tmc_code"], dtype=str).tmc_code == core.T1_OLD).sum()) > 0
        for f in sorted(glob.glob(os.path.join(target, "trelvane_tmc_export_*.csv")))))
    ok("T1 miles: release in force 10.96, current release 10.27, code dropped 9.75",
       [round(G["miles"][k], 2) for k in ("golden", "current", "drop")] == [10.96, 10.27, 9.75], G["miles"])
    ok("H5 deadhead legs 0.8 and 2.1 miles", drows[0][4] == A.LEG_MILES_IN and drows[-1][4] == A.LEG_MILES_OUT)
    ok("H4 2027 service days 252", core.working_days_2027() == 252)

    ra = load_workbook(os.path.join(target, P.FILES["reassign"]), read_only=True)
    sheets = {ws.title: [r for r in ws.iter_rows(values_only=True)] for ws in ra.worksheets}
    roll = [r for r in sheets["Permit roll"] if r and isinstance(r[0], str) and r[0].startswith("CG-")]
    req = [r for r in sheets["Late requests"] if r and isinstance(r[0], str) and r[0].startswith("LR-")]
    opt = [r for r in sheets["Opt-outs"] if r and isinstance(r[0], int)]
    hr = pd.read_csv(os.path.join(target, P.FILES["hr"]), dtype={"payroll_id": str})
    ok("R1 34 people on both sheets", len(S["dup"]) == 34 and G["both_sheets"] == 34)
    dd = {h["department"] for h in S["hr"] if h["employee_no"] in S["dup"]}
    ok("R1 spread over all seven departments", dd == set(A.DEPTS), dd)
    ok("R1 no key repeats inside a sheet", len({r[1] for r in roll}) == len(roll) and len({r[1] for r in req}) == len(req)
       and len({r[0] for r in opt}) == len(opt))
    ok("R1 no exact duplicate row inside a sheet", len(set(roll)) == len(roll) and len(set(req)) == len(req))
    ok("R1 nothing joins the sheets without HR (identifier sets disjoint)",
       not {str(r[1]) for r in roll} & {str(r[1]) for r in req})
    ok("R1 HR carries both identifiers for everyone on the sheets",
       {r[1] for r in roll} <= set(hr.employee_no) and {r[1] for r in req} <= set(hr.payroll_id))
    ok("H1 three start forms", {r[3] for r in roll} >= {"08:00"} and {r[3] for r in req} >= {"8:00 AM"} and
       800 in set(hr.sched_start_hhmm))
    ok("H2 opt-outs: 13 among 8:00 starters, 12 among others",
       sum(1 for o in S["optout"] if any(p["employee_no"] == o["employee_no"] and p["start"] == 800
                                         for p in S["permit"])) == 13 and len(S["optout"]) == 25)
    ok("H3 other starts on both sheets", {r[3] for r in roll} - {"08:00"} and {r[3] for r in req} - {"8:00 AM"})

    # ---------------------------------------------------------------- the asks
    gold = G["gold"]
    ok("Ask A golden 410 riders, 15 vehicles, 10 seats left empty",
       (gold["riders"], gold["vehicles"], gold["seats_empty"]) == (410, 15, 10))
    stops_a = {"R1": (444, 16, 4), "H2": (423, 16, 25), "H3": (531, 19, 1)}
    for k, v in stops_a.items():
        n = G["riders"][k]
        ok("Ask A stop %s %s" % (k, v), (n, A.vehicles(n), A.vehicles(n) * A.SEATS - n) == v,
           (n, A.vehicles(n), A.vehicles(n) * A.SEATS - n))
    late_g = [F["late"]["walk"][d] for d in A.ASK_DEPS]
    ok("Ask B late weekdays 1, 1, 3, 14, 62, 116, 163", late_g == [1, 1, 3, 14, 62, 116, 163], late_g)
    ok("Ask B default path late weekdays 0, 0, 0, 1, 2, 11, 71",
       [F["late"]["R0"][d] for d in A.ASK_DEPS] == [0, 0, 0, 1, 2, 11, 71])
    ok("Ask B midpoint late weekdays 0, 0, 1, 1, 10, 59, 125",
       [F["late"]["R2"][d] for d in A.ASK_DEPS] == [0, 0, 1, 1, 10, 59, 125])
    for d in A.ASK_DEPS:
        ok("Ask B cost %s clears its rounding boundary by 0.2" % core.clock(d), clear(gold["cost"][d]) >= 0.2,
           gold["cost"][d])
    ok("Ask B every late-arrival cost a whole number of dollars",
       all(float(A.HOLDOVER * gold["late_arrivals"][d]).is_integer() for d in A.ASK_DEPS))
    cents = A.vehicles(410) * core.working_days_2027() * (A.DAY_RATE + A.MILE_RATE * G["miles"]["golden"]) * 100
    ok("Ask B operator charges exact in cents (no rounding path moves them)", abs(cents - round(cents)) < 1e-6, cents)
    # every subset of mishandlings: each figure a subset touches leaves its bin
    cells, near = 0, []
    for (rk, lk, mk), s1 in G["stops"].items():
        if (rk, lk, mk) == ("golden", "walk", "golden"):
            continue
        if rk != "golden":
            for f in ("riders", "vehicles", "seats_empty"):
                ok("subset %s %s out of bin" % ((rk, lk, mk), f), s1[f] != gold[f], (s1[f], gold[f]))
                cells += 1
        for d in A.ASK_DEPS:
            if rk != "golden" or lk != "walk":
                same = s1["late_arrivals"][d] == gold["late_arrivals"][d]
                ok("subset %s late arrivals %s out of bin" % ((rk, lk, mk), core.clock(d)), not same)
                near.append(abs(s1["late_arrivals"][d] - gold["late_arrivals"][d]))
                cells += 1
            dlt = abs(round(s1["cost"][d]) - round(gold["cost"][d]))
            ok("subset %s cost %s out of bin" % ((rk, lk, mk), core.clock(d)), dlt >= 1, dlt)
            near.append(dlt)
            cells += 1
    ok("the nearest composed figure sits at least 9 units from the golden", min(near) >= 9, min(near))
    ok("the nearest composition as figures.json states it", min(near) == AN.nearest_composition(G)[0])
    # the cracker lands the call, executes every filed rule and misses every ask figure
    crk = G["stops"][("R1", "walk", "current")]
    ok("cracker misses every Ask A figure", all(crk[f] != gold[f] for f in ("riders", "vehicles", "seats_empty")))
    ok("cracker misses every Ask B figure", all(crk["late_arrivals"][d] != gold["late_arrivals"][d] and
                                                round(crk["cost"][d]) != round(gold["cost"][d]) for d in A.ASK_DEPS))

    # ---------------------------------------------------------------- the goldens
    page = open(os.path.join(golden_dir, GD.HTML), encoding="utf-8").read()
    svg = page[page.index("<svg"):page.index("</svg>")]
    labels = re.findall(r'text-anchor="middle" fill="#1d2733">(\$[\d,]+)</text>', svg)
    ticks = re.findall(r'font-size="12.5" text-anchor="middle" fill="#1d2733">(\d:\d\d)</text>', svg)
    ok("chart: one bar per departure from 6:50 to 7:20, in time order",
       ticks == [core.clock(d) for d in A.ASK_DEPS], ticks)
    ok("chart: each bar labelled with its cost in whole dollars",
       labels == ["${:,}".format(int(round(gold["cost"][d]))) for d in A.ASK_DEPS], labels)
    ok("chart: the dollar axis and the departure axis are titled",
       "2027 cost (US dollars)" in svg and "Departure from Cedar Grove (a.m.)" in svg)
    fills = re.findall(r'<rect [^>]*fill="(#[0-9a-f]{6})"', svg)
    ok("chart: no bar marked apart from the others (two segment colours, the legend's)",
       set(fills) == {"#8ea9db", "#1f3864"})
    h1 = page[page.index("<h1>"):page.index("</h1>")].lower()
    ok("chart page title says nothing of the on-time test or the call",
       not any(w in h1 for w in ("on time", "on-time", "7:05", "90 per cent", "latest")))
    trs = re.findall(r"<tr><td>(\d:\d\d a\.m\.)</td><td>([\d,]+)</td><td>(\$[\d,]+)</td><td>(\$[\d,]+)</td>"
                     r"<td>(\$[\d,]+)</td></tr>", page)
    ok("cost table: every departure's late arrivals and cost", [(t[0], t[1], t[4]) for t in trs] ==
       [(GD.ampm(d), "{:,}".format(gold["late_arrivals"][d]), "${:,}".format(int(round(gold["cost"][d]))))
        for d in A.ASK_DEPS], trs)
    ok("cost table: charges plus late-arrival cost add to the cost in whole dollars",
       all(int(t[2][1:].replace(",", "")) + int(t[3][1:].replace(",", "")) == int(t[4][1:].replace(",", ""))
           for t in trs))
    ok("golden page: no script, no external resource", "<script" not in page and "http://" not in
       page.replace('xmlns="http://www.w3.org/2000/svg"', "") and "https://" not in page)
    gw = load_workbook(os.path.join(golden_dir, GD.XLSX))
    dep = [r for r in gw["Departure"].iter_rows(values_only=True)]
    ok("workbook: the departure and its two counts", dep[3][1] == GD.ampm(call) and dep[7][:3] ==
       (GD.ampm(call), gc[call], N) and dep[8][:3] == (GD.ampm(nxt), gc[nxt], N), (dep[3], dep[7], dep[8]))
    rid = [r for r in gw["Riders"].iter_rows(values_only=True)]
    ok("workbook: riders, vehicles, seats left empty", [rid[i][1] for i in (3, 4, 5)] == [410, 15, 10])
    ok("workbook: riders by department add to the riders",
       sum(r[1] for r in rid[8:15]) == 410 and rid[15][1] == 410)
    dps = [r for r in gw["Departures"].iter_rows(values_only=True)][1:]
    ok("workbook: every departure's counts", [(r[1], r[2]) for r in dps] == [(gc[d], N - gc[d]) for d in deps])
    ok("workbook and page agree on the late weekdays",
       all(dict((GD.ampm(d), N - gc[d]) for d in deps)[GD.ampm(d)] * 410 == gold["late_arrivals"][d]
           for d in A.ASK_DEPS))

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv"))
    ok("gate: a file of 25,000 rows", big >= 25000, big)
    meta = json.load(open(os.path.join(task_dir, "metadata.json")))
    ok("gate: two distractors named in metadata", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]))
    ok("gate: no file named as a distractor", not any("distract" in f.lower() for f in files))
    ok("gate: every file has source, date and licence", all(x.get("source") and x.get("date") and x.get("license")
                                                            for x in meta["files"]))

    # ---------------------------------------------------------------- counter-pin sweep
    allt = "\n".join(docs_text.values()).lower()
    for wd in ("experienced", "instantaneous", "trajector", "time-dependent", "enter the segment", "entering",
               "reaches each", "reach each", "simulat", "walk", "midpoint", "percentile of the", "percentile profile",
               "planning time",
               "travel time index"):
        ok("counter-pin: no '%s' in the filed text" % wd, wd not in allt, wd)
    prose = "\n".join(docs_text[k] for k in ("standard", "budget", "notice", "readme")).lower()
    for wd in ("duplicate", "both sheets", "both lists", "twice", "reissue", "ramp"):
        ok("counter-pin: no device narrated ('%s') in the documents" % wd, wd not in prose, wd)
    ok("counter-pin: no route travel time by departure in any file",
       not any(re.search(r"route_?travel|travel_time_route|departure", open(f, errors="ignore").readline().lower())
               for f in glob.glob(os.path.join(target, "*.csv"))))
    ok("counter-pin: the readme names no entry rule for an epoch",
       "vehicles entering" not in readme.lower() and "entered" not in readme.lower())

    # ---------------------------------------------------------------- realism sweep
    for name, lo, hi in (("Late requests", dt_(2026, 9, 28), dt_(2026, 10, 14)),
                         ("Opt-outs", dt_(2026, 9, 28), dt_(2026, 10, 16))):
        ds = [r[4] if name == "Late requests" else r[1] for r in
              (req if name == "Late requests" else opt)]
        ok("realism: %s dated inside the sheet's own range" % name, all(lo <= x.date() <= hi for x in ds),
           (min(ds), max(ds)))
    ok("realism: the HR extract holds about 1,900 staff", 1800 <= len(hr) <= 2000, len(hr))
    for f in files:
        b = open(os.path.join(target, f), "rb").read()
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                b = b"".join(z.read(x) for x in z.namelist())
                if f.endswith(".docx"):
                    nl = z.namelist()
                    ok("realism: %s carries no template parts" % f,
                       not any(x.startswith("customXml/") or x in ("word/stylesWithEffects.xml",
                                                                   "docProps/thumbnail.jpeg") for x in nl))
        for tag in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib", b"\xe2\x80\x94",
                    b"\xe2\x80\x93"):
            ok("container scrubbed: %s in %s" % (tag[:12], f), tag not in b)
    for f in os.listdir(golden_dir):
        b = open(os.path.join(golden_dir, f), "rb").read()
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(golden_dir, f)) as z:
                b = b"".join(z.read(x) for x in z.namelist())
        for tag in (b"openpyxl", b"\xe2\x80\x94", b"\xe2\x80\x93"):
            ok("golden scrubbed: %s in %s" % (tag[:12], f), tag not in b)

    bad = [(a, c) for a, b, c in RESULTS if not b]
    if bad:
        raise AssertionError("%d failed:\n" % len(bad) + "\n".join("%s: %s" % x for x in bad))
    return len(RESULTS), cells


def dt_(y, m, d):
    import datetime
    return datetime.date(y, m, d)
