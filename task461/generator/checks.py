"""The generator's assertions on the built pack and its clean truth: the three rules (R1 to R3c), the ladder, the
semantic fork table (SF1 to SF16), the hierarchy's evidence and margins, bin edges, the ask devices and their
separation from the main call, the input gates, the realism sweep and the documents read back."""
import csv
import datetime as dt
import json
import os
import re

import numpy as np

import golden as G
import world as W

RESULTS = []
D = dt.timedelta


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    return bool(cond)


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as p:
        return re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in p.pages))


def run(target, golden_dir, x=None, n=None, meta_path=None, fig_path=None):
    RESULTS.clear()
    c = G.compute(target)
    k = c["kpi"]
    fig = json.load(open(fig_path))
    regs = G.bms(target)

    # ------------------------------------------------------------------ R1: the field's raw material ships
    heads = []
    for key in ("hh", "bms", "dips", "dockets", "runs", "fgas"):
        with open(os.path.join(target, W.FILES[key]), encoding="utf-8") as f:
            heads += next(csv.reader(f))
    ok("R1 the import and every meter ship at half-hour grain (settlement periods, cumulative registers)",
       n["hh"] >= 17000 and n["bms"] >= 250000, "%d and %d rows" % (n["hh"], n["bms"]))
    reg = G.register(target)
    ok("R1 no shipped column holds the hierarchy (a parent, a feed, a nesting or a board)",
       not any(re.search(r"parent|fed|feed|nest|board|upstream|downstream|sub", h, re.I) for h in
               heads + list(reg[0].keys())), str(list(reg[0].keys())))

    # ------------------------------------------------------------------ R3a, R3b: the analyst test on the clean truth
    loc = x["loc"]
    in_year = np.array([l.year == 2026 for l in loc])
    supplies = list(W.SUPPLIES)
    rooms = list(W.NESTED)
    imp_t = float((x["imp"] * 0.5)[in_year].sum())
    sup_t = sum(float((x["kw"][t] * 0.5)[in_year].sum()) for t in supplies)
    room_t = sum(float((x["kw"][t] * 0.5)[in_year].sum()) for t in rooms)
    kpi_t = lambda kwh: kwh * W.FACTOR_KG_PER_KWH / W.NLA_M2
    ok("R3a the easy route on the clean truth (every tenancy meter subtracted) is inside the target",
       kpi_t(imp_t - sup_t - room_t) < W.TARGET_KG_M2, "%.2f" % kpi_t(imp_t - sup_t - room_t))
    ok("R3a the clean truth's base building is over the target", kpi_t(imp_t - sup_t) > W.TARGET_KG_M2,
       "%.2f" % kpi_t(imp_t - sup_t))
    ok("R3b the pack's golden reproduces the clean truth's base building within the meters' accuracy",
       abs(k["mwh"] * 1000 - (imp_t - sup_t)) < 0.004 * imp_t and k["missed"],
       "%.1f against %.1f MWh" % (k["mwh"], (imp_t - sup_t) / 1000))
    ok("R3b the decisive step alone (the nested rooms counted once) turns the easy route into the golden",
       c["rungs"]["all"]["kpi"] < W.TARGET_KG_M2 < k["kpi"] and c["nested"] == W.NESTED, str(c["nested"]))
    off = {m: r["kpi"] for m, r in c["rungs"].items()}
    ok("R3b every enumerated reading that does not read the hierarchy from the counters files a KPI other than the "
       "golden's, at least 0.2 away", all(abs(v - k["kpi"]) >= 0.2 for v in off.values()),
       " ".join("%s %.2f" % kv for kv in sorted(off.items())))
    reg_rows = [m for m in reg if m["Recharged to occupier"] == "Yes"]
    occ_of = {m["Meter"]: m["Occupier"] for m in reg_rows}
    loc_of = {m["Meter"]: m["Location"] for m in reg_rows}
    indep_pairs = [(a, b) for a in supplies for b in supplies if a < b and occ_of.get(a) == occ_of.get(b)]
    ok("R3b no register field sorts the meters: one description on every tenancy meter, occupiers with two independent "
       "supplies (%d pairs), an independent pair sharing a location and a nested meter located away from its parent"
       % len(indep_pairs), len({m["Description"] for m in reg_rows}) == 1 and indep_pairs
       and any(loc_of[a] == loc_of[b] for a, b in indep_pairs)
       and any(loc_of[r] != loc_of[p] for r, p in W.NESTED.items()))
    ok("R3b the call's margins: the golden %.2f kg over, the easy route %.2f under" % (k["margin"],
       -c["rungs"]["all"]["margin"]), k["margin"] >= 0.5 and -c["rungs"]["all"]["margin"] >= 0.5)
    ok("R3c no memo, draft, prior report or stakeholder figure ships",
       not any(re.search(r"memo|draft|report_20|prior|email|notes|readme|dictionary|manifest", f, re.I)
               for f in os.listdir(target)))

    # ------------------------------------------------------------------ the hierarchy's evidence, from the pack
    def inc(tag):
        s = regs[tag]
        return {s[i][0]: s[i + 1][1] - s[i][1] for i in range(len(s) - 1) if s[i + 1][0] - s[i][0] == D(minutes=30)}
    for room, parent in W.NESTED.items():
        a, b = inc(room), inc(parent)
        common = [t for t in a if t in b]
        dark = [t for t in common if b[t] < 0.01]
        gap = min(b[t] - a[t] for t in common if b[t] >= 0.01)
        ok("hierarchy: %s inside %s in every common half-hour (smallest headroom %.2f kWh) and at zero in each of the "
           "%d half-hours %s was" % (room, parent, gap, len(dark), parent),
           gap >= 0.5 and dark and all(a[t] < 0.01 for t in dark))
    incs = {t: inc(t) for t in supplies if t != "EM-110"}
    for t in supplies:
        if t == "EM-110":
            continue
        others = [u for u in supplies if u not in (t, "EM-110")]
        live = all(incs[t][k] > 0.05 for u in others for k, v in incs[u].items() if v < 0.01 and k in incs[t])
        ok("hierarchy: %s stayed live through every other tenancy meter's isolation (a supply of its own)" % t, live)

    # ------------------------------------------------------------------ the semantic fork table, each row computed
    hh = list(csv.DictReader(open(os.path.join(target, W.FILES["hh"]), encoding="utf-8")))
    per_day = {}
    for r in hh:
        per_day[r["SETTLEMENT_DATE"]] = per_day.get(r["SETTLEMENT_DATE"], 0) + 1
    ok("SF1 the Measurement Period is the local calendar year (schedule 1.2); a UTC year differs by nothing, both "
       "year ends falling in GMT", "local time of the Building" in pdf_text(os.path.join(target, W.FILES["schedule"]))
       and per_day["29/03/2026"] == 46 and per_day["25/10/2026"] == 50 and len(per_day) == 365)
    sched = pdf_text(os.path.join(target, W.FILES["schedule"]))
    ok("SF2 Tenancy includes the roof licence (schedule 1.3), so EM-114 is a tenancy supply",
       "including any licence of the roof" in sched)
    ten = __import__("openpyxl").load_workbook(os.path.join(target, W.FILES["tenancy"]), read_only=True)
    areas = [r[3] for r in ten["Tenancy schedule"].iter_rows(min_row=2, values_only=True) if isinstance(r[3], int)]
    ok("SF3 the Net Lettable Area is filed (schedule 1.5) and the tenancy schedule's areas sum to it",
       "21,460 square metres" in sched and sum(areas) == W.NLA_M2, str(sum(areas)))
    ok("SF4 the conversion factor and the target are filed (schedule 2.1 and part 3)",
       str(W.FACTOR_KG_PER_KWH) in sched and "%.1f" % W.TARGET_KG_M2 in sched)
    swap = W.REPLACED[2]
    ok("SF5 the replaced meter's two tags join at the swap: EM-110's last register is at the swap, EM-118 starts there "
       "at zero", regs["EM-110"][-1][0] == swap and regs["EM-118"][0] == (swap, 0.0))

    def e118(m):
        a, b = max(G.MONTHS[m - 1], swap), G.MONTHS[m]
        return 0.0 if b <= swap else G.reading_at(regs["EM-118"], b) - (G.reading_at(regs["EM-118"], a) or 0.0)
    drop118 = G.kpi({m: c["monthly"][m] + e118(m) for m in range(1, 13)})
    e103 = [G.meter_energy(regs["EM-103"], G.MONTHS[m - 1], G.MONTHS[m]) for m in range(1, 13)]
    ok("SF6 the watt-hour registers read as kilowatt-hours put every month's base building below zero, an absurd "
       "figure no reading keeps", all(c["monthly"][m] - 999 * e103[m - 1] < 0 for m in range(1, 13)))
    ok("SF7 every month's boundaries are local midnights, none inside the autumn repeat or the spring gap",
       all(G.reading_at(regs["EM-101"], b) is not None for b in G.MONTHS))
    ok("SF8 the KPI is strictly over the target, not at it (schedule 3.1: exceeds)", k["kpi"] - W.TARGET_KG_M2 > 0.3)
    prompt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    ok("SF9 the rounding is the prompt's own closing sentence", prompt.rstrip().endswith(
        "intensity in kilograms per square metre, each to one decimal."))
    recs = G.diesel_records(target)
    dips, dlv, runs = recs
    one_side = True
    for b in G.QUARTERS:
        i = max(j for j, d in enumerate(dips) if d[0] <= b)
        t0, t1 = dips[i][0], dips[i + 1][0]
        inside = [(a, e) for a, e in runs if a < t1 and e > t0]
        sides = {e <= b for a, e in inside} | {a < b for a, e in inside}
        one_side = one_side and len(inside) >= 1 and len({e <= b for a, e in inside}) == 1 and \
            all((e <= b) == (a < b) for a, e in inside)
    ok("SF10 each quarter's local midnight sits in a dip week whose runs all fall on one side of it, so the week's "
       "burn is placed without any split", one_side)
    ok("SF11 a quarter is three calendar months of the local year (schedule 1.2)", "a quarter is three calendar months"
       in sched)
    lin = G.diesel_quarters(target, "linear")
    near = G.diesel_quarters(target, "nearest")
    ok("SF12 the calibration chart lists every millimetre, so each dip converts without interpolation",
       len(G.calibration(target)) == W.TANK_DIAMETER_MM + 1)
    ok("SF13 the gas oil factor and the GWP are filed (schedule 4.2 and 4.3)",
       str(W.DIESEL_KG_PER_L) in sched and "1,430" in sched)
    fg = list(csv.DictReader(open(os.path.join(target, W.FILES["fgas"]), encoding="utf-8")))
    jobs = {r["job_ref"] for r in fg if r["activity"].startswith("Recharge")}
    rjobs = {r["Job"] for r in G.recovery(target)}
    ok("SF14 every recovery in the contractor's record sits on a recharge job in the F-gas log, one per chiller",
       rjobs == jobs and len(jobs) == len(W.CHILLERS))
    ok("SF15 refrigerant released is the charge added less the charge recovered to cylinders (mass balance); every "
       "chiller's figure is positive and under its top-ups plus a tenth of its charge",
       all(0 < c["refrigerant"][ch] < sum(v for _, v in W.CHILLERS[ch]["topups"]) + 0.1 * W.CHILLERS[ch]["charge"]
           for ch in W.CHILLERS))
    ok("SF16 the monthly figures add to the year (each MWh from unrounded kWh)",
       abs(sum(c["monthly"].values()) / 1000 - k["mwh"]) < 1e-6)
    rounded_months = sum(round(v / 1000) for v in c["monthly"].values())
    s_ro = round(k["mwh"]) * W.FACTOR_KG_PER_KWH
    ok("SF17 the twelve rounded months sum to the rounded year (%d against %d)" % (rounded_months, round(k["mwh"])),
       rounded_months == round(k["mwh"]))
    ok("SF18 Scope 2 prints one tenth from the unrounded or the rounded year (%.3f and %.3f t), both clear of the edge"
       % (k["scope2_t"], s_ro), round(k["scope2_t"], 1) == round(s_ro, 1) and edge(k["scope2_t"], 0.1) >= 0.01
       and edge(s_ro, 0.1) >= 0.01)
    ev = list(csv.DictReader(open(os.path.join(target, W.FILES["runs"]), encoding="utf-8")))
    first = dt.datetime.strptime(ev[0]["event_time"], "%d/%m/%Y %H:%M:%S")
    ok("SF19 the controller export opens before the first dip week (%s), so a dip week with no run is on record"
       % first.date(), first < G.diesel_records(target)[0][0][0] - D(days=7))

    # ------------------------------------------------------------------ R2: Layer 1 mishandled keeps the call
    ok("R2 EM-118 left out keeps the call (a supply dropped only raises the base building)", drop118["missed"],
       "%.2f" % drop118["kpi"])
    gap_rows = [t for t, v in regs["EM-101"] if W.BMS_GAP[0] <= t < W.BMS_GAP[1]]
    ok("R2 the BMS server gap (no rows for nine hours) holds no month boundary and the registers carry through it",
       not gap_rows and all(not (W.BMS_GAP[0] <= b < W.BMS_GAP[1]) for b in G.MONTHS))
    ok("R2 every tenancy meter subtracted on the easy route with the replaced tag dropped as well keeps the easy "
       "route inside the target", G.kpi({m: G.base_building(target, "all")[m] + e118(m)
                                         for m in range(1, 13)})["kpi"] < W.TARGET_KG_M2)

    # ------------------------------------------------------------------ bins
    for m, v in c["monthly"].items():
        ok("bin month %d %.3f MWh" % (m, v / 1000), edge(v / 1000, 1.0) >= 0.002, "%.4f" % edge(v / 1000, 1.0))
    ok("bin year %.3f MWh" % k["mwh"], edge(k["mwh"], 1.0) >= 0.002)
    ok("bin scope 2 %.3f t" % k["scope2_t"], edge(k["scope2_t"], 0.1) >= 0.002)
    ok("bin KPI %.3f" % k["kpi"], edge(k["kpi"], 0.1) >= 0.005)
    ok("bin margin %.3f" % k["margin"], edge(k["margin"], 0.1) >= 0.005)
    for q, v in c["diesel"].items():
        ok("bin diesel Q%d %.2f L" % (q, v), edge(v, 1.0) >= 0.02 and edge(v * W.DIESEL_KG_PER_L, 1.0) >= 0.02)
    for ch, v in c["refrigerant"].items():
        ok("bin refrigerant %s %.3f kg" % (ch, v), edge(v, 0.1) >= 0.004 and edge(v * W.GWP_R134A, 1.0) >= 0.02)

    # ------------------------------------------------------------------ the asks' devices and separation
    moved_l = [q for q in range(1, 5) if round(lin[q]) != round(c["diesel"][q])]
    moved_n = [q for q in range(1, 5) if round(near[q]) != round(c["diesel"][q])]
    ok("ask A device: a straight line between dips moves every quarter, and so does the nearer dip",
       len(moved_l) == 4 and len(moved_n) == 4, "%s %s" % ({q: round(v) for q, v in lin.items()},
                                                            {q: round(v) for q, v in near.items()}))
    rf_add = G.refrigerant(target, "added")
    rf_top = G.refrigerant(target, "topups")
    ok("ask B device: every kilogram added, or the top-ups alone, moves every chiller",
       all(round(rf_add[ch], 1) != round(c["refrigerant"][ch], 1) and round(rf_top[ch], 1) != round(
           c["refrigerant"][ch], 1) for ch in W.CHILLERS), "%s %s" % (rf_add, rf_top))
    main_files = {W.FILES[k_] for k_ in ("hh", "bms", "register", "tenancy", "schedule")}
    ask_files = {W.FILES[k_] for k_ in ("dips", "calib", "dockets", "runs", "fgas", "recovery")}
    ok("separation: no ask organ sits in a file the main call reads", not (main_files & ask_files))

    # ------------------------------------------------------------------ input gates, realism, documents
    files = os.listdir(target)
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    ok("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ok("input gate: a file of 25,000 rows or more", max(v for v in n.values()) >= 25000)
    meta = json.load(open(meta_path))
    ok("input gate: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    ok("no file under target/ describes the data", not any(re.search(r"readme|dictionary|notes|manifest|schema|codebook",
                                                                   f, re.I) for f in files))
    months = [round(v / 1000) for v in c["monthly"].values()]
    ok("realism: no two months share a base building figure", len(set(months)) == 12, str(months))
    ok("realism: the year's base building is no round figure", edge(k["mwh"], 100.0) < 45)
    ok("doc: the schedule reads back with its definitions (positive control)", "Base Building Electricity means" in sched)
    ok("doc: no governing sentence names a comms room, a sub-meter, a hierarchy, an isolation, a recovery or a run",
       not re.search(r"comms|sub-?meter|hierarch|nest|isolat|recover|engine run|controller", sched, re.I))
    ok("figures.json carries the call", fig["call"]["missed"] == k["missed"])
    good = all(r[1] for r in RESULTS)
    for name, g, detail in RESULTS:
        if not g:
            print("FAIL", name, detail)
    print("checks: %d of %d passed" % (sum(1 for r in RESULTS if r[1]), len(RESULTS)))
    return good
