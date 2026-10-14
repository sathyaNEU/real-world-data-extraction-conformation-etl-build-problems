"""task138 assertions: the input gates, every rung of the ladder and its separation, the three-rules block on the clean
truth (R1 to R3c), every semantic fork row (SF1 to SF33), the graded figures' distances to their rounding edges, the four
lateral asks with their stops and devices, the separation line between the call and the asks, the distractors' deletion
test, and the realism and hygiene sweeps. Run by build.py on every build; prints the ladder and the measured figures
the design note quotes."""
from __future__ import annotations

import copy
import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np

import calc as C
import common as K

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def edge(x, step):
    q = x / step + 0.5
    return min(q - math.floor(q), math.ceil(q) - q) * step


def share1(x):
    return math.floor(x * 10 + 0.5) / 10.0


def variant_order(M, start, **kw):
    req, mon = M.thirty(start, **kw)
    return C.order_from(req)


def af(x):
    return "{:,}".format(int(x))


def run(target, golden, W=None, meta_path=None):
    N[0] = 0
    M = C.load(target)
    lad = C.ladder(M)
    g = lad["R4"]
    print("ladder (24th smallest of thirty, order, setting year):")
    for k, v in lad.items():
        print("  %-4s %-86s %12s  %7s  %d  %+.2f%%" % (k, v["label"][:86], "{:,.2f}".format(v["req"]),
                                                   af(v["order"]), v["year"], 100 * (v["req"] / g["req"] - 1)))

    # ------------------------------------------------------------------------------------------ the golden call
    ok(g["order"] == 215000 and g["year"] == 2012, ("golden", g["order"], g["year"]))
    lo = g["req"] - (g["order"] - K.ORDER_STEP)
    ok(400 <= lo <= 600, ("24th smallest mid-bin in its thousand", lo))
    r = g["ranked"]
    ok(r[23][1] - r[22][1] >= 1000 and r[24][1] - r[23][1] >= 1000, ("SF23 neighbours", r[22][1], r[23][1], r[24][1]))
    print("  golden 24th %.2f (%.2f above %s, %.2f under the order), neighbours %d %.0f and %d %.0f" % (
        g["req"], lo, af(g["order"] - K.ORDER_STEP), g["order"] - g["req"], r[22][0], r[22][1], r[24][0], r[24][1]))

    # ------------------------------------------------------------------------------------------ the ladder
    R3, R2d, R4g, O2 = lad["R3"], lad["R2d"], lad["R4g"], lad["O2"]
    ok(R3["order"] == 209000 and R3["year"] == 2012, ("default path", R3["order"], R3["year"]))
    for k, floor in (("R0", 0.07), ("R1", 0.06), ("R2", 0.06), ("R2b", 0.07), ("R3", 0.025), ("R3c", 0.01),
                     ("R4g", 0.02), ("R2d", 0.004)):
        ok(lad[k]["req"] / g["req"] - 1 <= -floor, ("rung under the golden by its floor", k, floor))
        ok(lad[k]["order"] <= g["order"] - K.ORDER_STEP, ("rung a full bin under the order", k))
    for k in ("O1", "O2"):
        ok(lad[k]["order"] >= g["order"] + K.ORDER_STEP, ("over-correction a full bin above", k))
    for k in ("R0", "R1", "R2", "R2b"):
        ok(lad[k]["year"] != g["year"], ("rung names another setting year", k))
    D = M.D_golden
    D3 = M.D_last_set
    meth = np.array([f["method"] for f in M.fields])
    held = meth != "Border"
    print("  31 January 2027: golden acre-weighted %.3f in, %d of %d fields at or past allowable depletion; default path "
          "%.3f in, %d" % (float(D @ M.acres / M.acres.sum()), int((D >= M.raw).sum()), M.n,
                          float(D3 @ M.acres / M.acres.sum()), int((D3 >= M.raw).sum())))

    # ------------------------------------------------------------------------------------------ the record's season
    water = M.set_water()
    lastfull, at_last = _season_path(M, water)
    # every drip, micro-sprinkler and sprinkler field ends its 2026 season short of field capacity; the border fields'
    # last set fills them
    short = at_last[held]
    ok(int(held.sum()) == 501 and float(short.min()) > 0.3, ("held fields short after their last set", int(held.sum()),
                                                           float(short.min())))
    ok(float(at_last[~held].max()) < 1e-9, "every border field full after its last set")
    lf = [dt.date.fromordinal(int(x)) for x in lastfull[held]]
    ok(max(lf) <= dt.date(2026, 6, 15), ("held fields last full in the spring", max(lf)))
    # the season's water against the crop's use: from the day after a held field was last full to the end of its last
    # set's day, its crop water use less rain exceeds its delivered water at its efficiency by at least its depletion
    # there (water beyond field capacity only drains), so a refill at the last set would need water the record never
    # delivered
    shortfall = _season_shortfall(M, water, lastfull)
    ok(np.all(shortfall[held] >= at_last[held] - 1e-6) and float(shortfall[held].min()) > 0.3,
       "the season's water short of the crop's use less rain since the field was last full")
    print("  2026 record: %d held fields short of field capacity after their last set by %.2f to %.2f in (acre-weighted "
          "%.2f); last full between %s and %s; every border field full after its last set" % (
              int(held.sum()), float(short.min()), float(short.max()),
              float((short * M.acres[held]).sum() / M.acres[held].sum()), min(lf), max(lf)))

    # ------------------------------------------------------------------------------------------ the three rules
    files = sorted(os.listdir(target))
    heads = " ".join(open(os.path.join(target, f), encoding="utf-8").readline().lower() for f in files
                     if f.endswith(".csv"))
    ok(not re.search(r"depletion|soil_water|moisture|deficit|requirement", heads),
       "R1: a shipped column holds the deciding quantity")
    orders_head = C.read_csv(os.path.join(target, K.ORDERS))[0]
    ok({"ordered_cfs", "set_start", "set_end", "status", "field_id"} <= set(orders_head),
       "R1: the orders ship at set grain with each set's flow and times")
    ok(len(M.wx) == (K.WEATHER_END - K.WEATHER_START).days + 1, "R1: the daily weather ships whole")
    if W is not None:
        T = _truth(W)
        # R2: the mess on the call's path (two stations spliced, units and missing days; revised and withdrawn requests;
        # former field ids; cancelled sets; turnout ids written three ways), read by the filed rules and the dictionary,
        # gives back the world's own fields, weather and 2026 sets
        ok(sorted(M.ids) == sorted(T["ids"]), "R2: the 2027 fields read from the pack are the world's")
        ok(all(abs(M.acres[i] - T["acres"][fid]) < 0.006 and M.fields[i]["crop"] == T["crop"][fid]
               and M.fields[i]["method"] == T["method"][fid] for i, fid in enumerate(M.ids)),
           "R2: crops, methods and acres read from the requests are the world's")
        ok(max(abs(M.wx[d][0] - W.wx[d][0]) + abs(M.wx[d][1] - W.wx[d][1]) for d in M.wx) < 1e-9,
           "R2: the spliced record read from the pack is the District's record")
        ids = set(M.ids)
        rec_w = {(a, b, round(cfs, 1)) for fid, a, b, cfs, s in M.record if s == "Delivered" and fid in ids}
        ok(rec_w == T["sets26"], "R2: the 2026 delivered sets read from the orders are the world's")
        # R3a: the easy route on the clean truth (the world's own fields, weather and sets), every filed rule applied,
        # files the default path's wrong answer
        t3 = _truth_order(T, M, "last set")
        ok(t3["order"] == R3["order"] and t3["year"] == R3["year"], ("R3a: the default path on the clean truth", t3["order"]))
        # R3b: the same route with only the decisive step changed (the 2026 season run on the water each set put in)
        t4 = _truth_order(T, M, "record")
        ok(t4["order"] == g["order"] and t4["year"] == g["year"] and abs(t4["req"] - g["req"]) < 1e-6,
           ("R3b: the record run on the clean truth", t4["order"]))
        # the fields as they are: the record run reproduces each field's root zone within the yard's rounding
        true31 = np.array([W.true_path[i][K.WEATHER_END] for i in M.ids])
        ok(float(np.abs(true31 - D).max()) < 0.35 and abs(float((true31 - D) @ M.acres) / M.acres.sum()) < 0.03,
           ("R3b: the record run against the fields as they are", float(np.abs(true31 - D).max())))
        print("  three rules on the clean truth: default path %s, the record run %s; the fields as they are within "
              "%.3f in (acre-weighted %+.4f)" % (af(t3["order"]), af(t4["order"]), float(np.abs(true31 - D).max()),
                                                 float((true31 - D) @ M.acres / M.acres.sum())))
    # R3c: nothing planted
    ok(not any(w in f.lower() for f in files for w in ("memo", "draft", "briefing", "estimate")),
       "R3c: a memo, draft, briefing or estimate ships")
    docs_txt = " ".join(_text_of(os.path.join(target, f)) for f in files if f.endswith((".pdf", ".docx", ".txt")))
    stated = sorted(set(re.findall(r"\b(\d{3},\d{3}) acre-feet\b", docs_txt)))
    ok(stated == ["241,000"], ("R3c: a document states a requirement or an order", stated))
    for w in ("field capacity at", "start state", "starting depletion", "initial depletion", "initial condition",
              "initial state", "antecedent", "deficit irrigation", "regulated deficit", "working deficit",
              "soil moisture", "carry-over", "carryover"):
        ok(w not in docs_txt.lower(), ("R3c: a document names the start", w))

    # ------------------------------------------------------------------------------------------ closure
    for c in K.CROPS:
        for su, (awc, lim) in M.T["soils"].items():
            depth = M.T["root"][c] if lim is None else min(M.T["root"][c], lim)
            odd = round(M.T["mad"][c] * 100) * round(awc * 100) * round(depth * 10)
            ok(odd % 2 == 1, ("allowable depletion off the stations' decimals", c, su))
    gap = _min_gap(M, M.start_golden())
    ok(gap > 1e-7, ("closest approach of a day's depletion to an allowable depletion", gap))
    ok(all(d in M.s39 for d in K.daterange(K.WEATHER_START, K.WEATHER_END)), "station 39 has every day")
    wint = {y: sum(M.wx[d][1] for d in K.daterange(dt.date(y, 10, 1), dt.date(y + 1, 1, 31))) for y in range(1995, 2027)}
    ok(min(wint, key=wint.get) == 2026, ("driest October to January", sorted(wint.items(), key=lambda kv: kv[1])[:3]))
    meths = {m: sum(1 for f in M.fields if f["method"] == m) for m in ("Drip", "Micro-sprinkler", "Sprinkler", "Border")}
    ok(meths == {"Drip": 196, "Micro-sprinkler": 255, "Sprinkler": 50, "Border": 130}, ("methods", meths))
    ok(sorted(wint, key=wint.get, reverse=True)[1] == 2025 and abs(wint[2025] - 13.19) < 0.005,
       ("the 2025-26 winter the second wettest", wint[2025]))
    dd = M.D_golden - M.D_last_set
    ok(abs(float(dd[held] @ M.acres[held] / M.acres[held].sum()) - 1.199) < 0.0005 and float(np.abs(dd[~held]).max()) < 1e-9,
       "the record run against the default path: the held fields 1.199 inches deeper, the border fields equal")
    lastm = [M.last_delivery[f["id"]].month for f in M.fields]
    print("  closest approach of a replay day's depletion to an allowable depletion: %.2e in; October 2026 to January "
          "2027 rain %.2f in (next driest %.2f, median of %d winters %.2f); last 2026 sets in September %d, October %d"
          % (gap, wint[2026], sorted(wint.values())[1], len(wint), float(np.median(list(wint.values()))),
             lastm.count(9), lastm.count(10)))

    # ------------------------------------------------------------------------------------------ the fork table
    rows = C.read_csv(os.path.join(target, K.ORDERS))
    head = rows[0]
    ix = {c: head.index(c) for c in head}
    SEEN = {}
    # SF1: no delivered set outside the canal season in any season on file
    for rr in rows[1:]:
        if rr[ix["status"]] == "Delivered":
            a = dt.date.fromisoformat(rr[ix["set_start"]][:10])
            b = dt.date.fromisoformat(rr[ix["set_end"]][:10])
            ok((a.month, a.day) >= (2, 1) and (b.month, b.day) <= (10, 31) and a.year == b.year == int(rr[ix["season"]]),
               ("SF1 delivered set inside the season", rr[ix["order_no"]]))
    # SF2: the interpolated 80th percentile; the 24th rounded to the nearest thousand
    vals = sorted(g["reqs"].values())
    p80 = float(np.percentile(vals, 80))
    ok(K.ceil_to(p80, K.ORDER_STEP) == g["order"], ("SF2 the interpolated 80th percentile converges", p80))
    ok(K.round_to(vals[23], K.ORDER_STEP) != g["order"], "SF2 the 24th rounded to the nearest thousand")
    SEEN["SF2"] = (K.ceil_to(p80, K.ORDER_STEP), K.round_to(vals[23], K.ORDER_STEP))
    # SF3: every request row, or withdrawn requests in
    alt = []
    for q in M.requests:
        gg = M.register[q["Field"]]
        alt.append(dict(id=q["Field"], lateral="L" + gg["lateral"].split()[-1], soil=gg["soil_unit"],
                        crop=q["Crop code"], method=q["Irrigation method"], acres=float(q["Acres"])))
    sf3 = _order_on_fields(M, alt)
    ok(sf3["order"] != g["order"], ("SF3", sf3["order"]))
    SEEN["SF3"] = sf3["order"]
    # SF4: the register's GIS acres in the replays and the record run
    fields4 = [dict(f, acres=float(M.register[f["id"]]["gis_acres"])) for f in M.fields]
    sf4 = _order_on_fields(M, fields4)
    ok(sf4["order"] != g["order"], ("SF4", sf4["order"]))
    SEEN["SF4"] = sf4["order"]
    # SF5: no depth limit
    T5 = copy.deepcopy(M.T)
    T5["soils"] = {k: (v[0], None) for k, v in T5["soils"].items()}
    sf5 = _order_on_tables(M, T5)
    ok(sf5["order"] != g["order"], ("SF5", sf5["order"]))
    SEEN["SF5"] = sf5["order"]
    # SF6: station 39 throughout; the yard from its first day; missing yard days as zero
    wx_a = {d: M.s39[d] for d in M.wx}
    wx_b = {d: (M.yard[d] if (d >= K.DISTRICT_STATION_START and d in M.yard) else M.s39[d]) for d in M.wx}
    wx_c = {d: (M.yard.get(d, (0.0, 0.0)) if d >= K.SPLICE else M.s39[d]) for d in M.wx}
    sf6 = {k: _order_on_weather(M, w) for k, w in (("st39", wx_a), ("yard_from_april", wx_b), ("missing_zero", wx_c))}
    ok(sf6["st39"]["order"] != g["order"], ("SF6 station 39", sf6["st39"]["order"]))
    ok(sf6["yard_from_april"]["order"] == g["order"] and sf6["missing_zero"]["order"] == g["order"],
       "SF6 the yard from its first day and missing yard days as zero converge on the order")
    SEEN["SF6"] = {k: (v["order"], round(v["req"] - g["req"], 1)) for k, v in sf6.items()}
    # SF7: 29 February dropped (WOP 2.4 keeps it)
    sf7 = variant_order(M, M.start_golden(), drop_leap=True)
    ok(sf7["order"] == g["order"] and sf7["year"] == g["year"], "SF7 converges")
    SEEN["SF7"] = (sf7["order"], round(sf7["req"] - g["req"], 1))
    # SF8: a replay day's arithmetic: the irrigation test before rain; the rain taken first
    st = M.start_golden()
    sf8 = _order_test_before_rain(M, st)
    sf8b = _order_rain_first(M, st)
    ok(sf8["order"] != g["order"] and sf8b["order"] == g["order"], ("SF8", sf8["order"], sf8b["order"]))
    SEEN["SF8"] = (sf8["order"], sf8b["order"], round(sf8b["req"] - g["req"], 1))
    # SF9: where each replay starts: every rung files its own order (the ladder above)
    for k in ("R0", "R1", "R2", "R2b", "R3", "R3c"):
        ok(lad[k]["order"] != g["order"], ("SF9 rung files its own order", k))
    # SF10: cancelled sets counted as water (R2d); SF11: no efficiency on the record's sets (R4g); SF20: no cap (O2)
    ok(R2d["order"] != g["order"] and R4g["order"] != g["order"] and O2["order"] != g["order"], "SF10 SF11 SF20")
    # SF12: the record run's start converges: from 1 November 2025 at field capacity or at total available water, and
    # from 1 February 2023 with every season's record (former field ids mapped through the register)
    for D0 in (np.zeros(M.n), M.taw.copy()):
        Dw = M.hindcast({}, start=dt.date(2025, 11, 1), D0=D0, upto=K.WINTER_FULL)
        ok(float(Dw.max()) < 1e-12, "SF12 every root zone at field capacity at the end of 27 January 2026")
    for lab, Dx in (("1 Feb 2026 full", M.hindcast(water, start=dt.date(2026, 2, 1))),
                    ("1 Nov 2025 full", M.hindcast(water, start=dt.date(2025, 11, 1))),
                    ("1 Nov 2025 empty", M.hindcast(water, start=dt.date(2025, 11, 1), D0=M.taw.copy())),
                    ("1 Feb 2023 every season", M.hindcast(_water_all_seasons(M, target), start=dt.date(2023, 2, 1)))):
        ok(float(np.abs(Dx - D).max()) < 1e-9, ("SF12 the record run's start converges", lab))
    # SF13: a set's water by day: all on its first or last day instead of the hours it ran each day
    sf13 = {}
    for split in ("start", "end"):
        Dx = M.hindcast(M.set_water(split=split))
        o = variant_order(M, lambda y, Dx=Dx: Dx)
        ok(o["order"] == g["order"] and o["year"] == g["year"] and abs(o["req"] - g["req"]) < 10.0,
           ("SF13 converges", split, o["req"] - g["req"]))
        sf13[split] = round(o["req"] - g["req"], 1)
    SEEN["SF13"] = sf13
    # SF14: the day's order of the record's water: after the day's floor and cap, or before the day's ET and rain (a
    # border field's last set then leaves that day's crop water use on it): both converge on the order and the year
    Da = M.hindcast(water, order="after")
    oa = variant_order(M, lambda y: Da)
    ok(oa["order"] == g["order"] and oa["year"] == g["year"] and abs(oa["req"] - g["req"]) < 5.0,
       ("SF14 after the floor converges", oa["req"] - g["req"]))
    Db = M.hindcast(water, order="before")
    ob = variant_order(M, lambda y: Db)
    ok(ob["order"] == g["order"] and ob["year"] == g["year"], "SF14 before: the same order and year")
    held_short = lambda Dx: int(held.sum())
    SEEN["SF14"] = (round(oa["req"] - g["req"], 1), round(ob["req"] - g["req"], 1))
    # SF15: the register's GIS acres in the record run (the replays on the request acres)
    gis = np.array([float(M.register[f["id"]]["gis_acres"]) for f in M.fields])
    Dg = M.hindcast(water, acres=gis)
    og = variant_order(M, lambda y: Dg)
    ok(og["order"] == g["order"] and og["year"] == g["year"], "SF15 GIS acres in the record run: the same order and year")
    SEEN["SF15"] = round(og["req"] - g["req"], 1)
    # SF16: each set's water scaled by its turnout meter's season (the meters as the measure of what ran)
    A = C.load_asks(target)
    scale = _meter_scale(M, A, target)
    Dm = M.hindcast({d: v * scale for d, v in water.items()})
    om = variant_order(M, lambda y: Dm)
    ok(om["order"] == g["order"] and om["year"] == g["year"], "SF16 metered: the same order and year")
    SEEN["SF16"] = (round(om["req"] - g["req"], 1), round(float(scale.min()), 3), round(float(scale.max()), 3))
    # SF17: every 2027 field kept its 2026 irrigation method (the record's efficiency is the request's)
    method26 = {rr[0]: rr[5] for rr in C.read_csv(os.path.join(target, K.CROP_REPORT))[1:]}
    ok(all(method26[f["id"]] == f["method"] for f in M.fields), "SF17 every field kept its 2026 method")
    # SF18: every requested field took a delivered set in 2026; SF19: every requested field carries its 2026 crop
    ok(all(f["id"] in M.last_delivery for f in M.fields), "SF18")
    crop26 = {rr[0]: rr[2] for rr in C.read_csv(os.path.join(target, K.CROP_REPORT))[1:]}
    ok(all(crop26[f["id"]] == f["crop"] for f in M.fields), "SF19")
    # SF21: deliveries times one plus each allowance
    sf21 = _order_loss_multiplied(M, st)
    ok(sf21["order"] != g["order"], ("SF21", sf21["order"]))
    SEEN["SF21"] = sf21["order"]
    # SF22: the west spur's fields on Lateral 5 for the call
    rows_o = {rr[ix["field_id"]]: rr[ix["turnout"]] for rr in rows[1:] if rr[ix["season"]] == "2026"}
    fields22 = [dict(f, lateral="L5") if rows_o[f["id"]] in set(K.MOVED) else f for f in M.fields]
    ok(sum(1 for f in fields22 if f["lateral"] == "L5") > sum(1 for f in M.fields if f["lateral"] == "L5"), "SF22 fields")
    sf22 = _order_on_fields(M, fields22)
    ok(sf22["order"] == g["order"] and sf22["year"] == g["year"], "SF22 converges on the order")
    SEEN["SF22"] = (sf22["order"], round(sf22["req"] - g["req"], 1))
    ok(all(M.register[f["id"]]["lateral"] == "Lateral 6" for f in M.fields if rows_o[f["id"]] in set(K.MOVED)),
       "SF22 the spur's fields on Lateral 6 in the register")
    # SF24: ET0 recomputed (Hargreaves on the stations' temperatures)
    sf24 = _order_hargreaves(M, target)
    ok(sf24["order"] != g["order"], ("SF24", sf24["order"]))
    SEEN["SF24"] = sf24["order"]
    # SF25: an effective-rain fraction (75 per cent)
    wx25 = {d: (e, 0.75 * rn) for d, (e, rn) in M.wx.items()}
    sf25 = _order_on_weather(M, wx25)
    ok(sf25["order"] != g["order"], ("SF25", sf25["order"]))
    SEEN["SF25"] = sf25["order"]
    # SF26: acre-feet as inches times acres over 12, a cfs-hour 3,600 cubic feet (the model's own arithmetic)
    ok(abs(M.replay(2012, D) - g["reqs"][2012]) < 1e-6, "SF26")
    # SF27: station 39's millimetres at 25.4 to the inch, carried unrounded
    dic = _text_of(os.path.join(target, K.DICTIONARY))
    ok("25.4 millimetres to the inch" in dic, "SF27 the dictionary's unit line")
    sf27 = {}
    for key, conv in (("hundredths", lambda mm: round(mm / 25.4 + 1e-12, 2)), ("0.0394", lambda mm: mm * 0.0394)):
        wx27 = {d: (M.yard[d] if (d >= K.SPLICE and d in M.yard) else
                    (conv(M.s39[d][0] * 25.4), conv(M.s39[d][1] * 25.4))) for d in M.wx}
        sf27[key] = _order_on_weather(M, wx27)
        ok(sf27[key]["order"] == g["order"], ("SF27 converges on the order", key, sf27[key]["order"]))
    SEEN["SF27"] = {k: round(v["req"] - g["req"], 1) for k, v in sf27.items()}
    print("  forks: %s" % json.dumps(SEEN, default=str))
    # closure axes 14 to 16: the orders' row order changes nothing; order numbers are unique; every 2026 order and every
    # 2027 request names a field in the register as it stands
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        with open(os.path.join(tmp, K.ORDERS), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(rows[0])
            for rr in reversed(rows[1:]):
                w.writerow(rr)
        Mr = C.load(tmp)
        orv = C.order_from(Mr.thirty(Mr.start_golden())[0])
        ok(orv["order"] == g["order"] and abs(orv["req"] - g["req"]) < 1e-6, ("closure 14: the orders reversed",
                                                                            orv["req"] - g["req"]))
    finally:
        shutil.rmtree(tmp)
    nos = [rr[ix["order_no"]] for rr in rows[1:]]
    ok(len(nos) == len(set(nos)), "closure 15: every order number unique")
    reg_ids = set(M.register)
    ok(all(rr[ix["field_id"]] in reg_ids for rr in rows[1:] if rr[ix["season"]] in ("2025", "2026")),
       "closure 16: the 2025 and 2026 orders on the register's field ids")
    ok(all(q["Field"] in reg_ids for q in M.requests), "closure 16: every request on a register field id")

    # ------------------------------------------------------------------------------------------ the asks
    gd, gs, gi = C.ask_a(A)
    sp = C.ask_b(A)
    s1d = C.ask_deliveries(A, mode="turnout")
    s2d = C.ask_deliveries(A, mode="serial")
    s3d = C.ask_deliveries(A, as_of=False)
    i0 = C.ask_inflow(A, estimates=False)
    units = _replacement_units(target)
    s2bd = _ask_a_new_from_zero(A, units)
    b1 = C.ask_b(A, boards=False)
    b2 = C.ask_b(A, fill=False)
    lag = _ask_b_lagged(A)
    for l in K.LATERALS:
        ok(edge(gd[l], 10) >= 2.5 and edge(gi[l], 10) >= 2.5 and edge(sp[l], 10) >= 2.5 and edge(gs[l], 0.1) >= 0.02,
           ("ask edges", l, edge(gd[l], 10), edge(gi[l], 10), edge(sp[l], 10), edge(gs[l], 0.1)))
        # Ask 1: deliveries within each meter (S2), across changes by turnout (S1), new meters from zero (S2b)
        ok(K.round_to(s2d[l], 10) != K.round_to(gd[l], 10), ("deliveries S2", l))
        ok(K.round_to(s1d[l], 10) != K.round_to(gd[l], 10), ("deliveries S1", l))
        ok(K.round_to(s2bd[l], 10) != K.round_to(gd[l], 10), ("deliveries S2b", l))
        # Ask 2: water put in without the Water Master's estimates
        ok(K.round_to(i0[l], 10) != K.round_to(gi[l], 10), ("water put in without the estimates", l))
        # Ask 3: the share off under either device alone
        for dd, ii, lab in ((gd, i0, "chain without the estimates"), (s2d, gi, "estimates without the chain"),
                            (s2d, i0, "neither")):
            ok(share1(100.0 * (ii[l] - dd[l]) / ii[l]) != share1(gs[l]), ("share", lab, l))
        # Ask 4: the bare crest
        ok(K.round_to(b1[l], 10) != K.round_to(sp[l], 10), ("spill bare crest", l))
        ok(sp[l] < gi[l] - gd[l] and b1[l] < gi[l] - gd[l], ("spill under the lateral's loss", l))
    for l in ("L5", "L6"):
        ok(K.round_to(s3d[l], 10) != K.round_to(gd[l], 10), ("SF28 the register's lateral moves the spur's deliveries", l))
        ok(share1(100.0 * (gi[l] - s3d[l]) / gi[l]) != share1(gs[l]), ("SF28 share", l))
    for l in K.LATERALS:
        if l not in ("L5", "L6"):
            ok(abs(s3d[l] - gd[l]) < 1e-6, ("the spur moves only Laterals 5 and 6", l))
    moved_b2 = [l for l in K.LATERALS if K.round_to(b2[l], 10) != K.round_to(sp[l], 10)]
    ok(sorted(moved_b2) == ["L3", "L7", "L8"], ("SF32 alternate-day reading as zero", moved_b2))
    moved_lag = [l for l in K.LATERALS if K.round_to(lag[l], 10) != K.round_to(sp[l], 10)]
    ok(len(moved_lag) >= 1, "SF31 a board change taken from the next day moves a lateral")
    # SF28's convergence: no water ran to the west spur from 13 to 15 June and every spur meter was read on 15 June, so
    # no read interval straddles the change of feed; every spur turnout took water from both laterals
    for rr in rows[1:]:
        if rr[ix["season"]] == "2026" and rr[ix["status"]] == "Delivered" and rr[ix["turnout"]] in set(K.MOVED):
            ok(rr[ix["set_end"]] <= "2026-06-13 06:00" or rr[ix["set_start"]][:10] > "2026-06-15",
               ("SF28 no water to the spur during the tie-in", rr[ix["order_no"]]))
    ok(all(any(t.date() == C.MOVED_FROM for t, _, _, _ in A["reads"][tid]) for tid in K.MOVED), "SF28 spur reads on 15 June")
    ok(all(A["lateral"][tid] == "L6" for tid in K.MOVED) and len(K.MOVED) == 14, "SF28 the spur on Lateral 6")
    for tid in K.MOVED:
        iv = C.turnout_intervals(A, tid, "chain")
        ok(sum(v for t1, v in iv if t1.date() <= C.MOVED_FROM) > 0 and sum(v for t1, v in iv if t1.date() > C.MOVED_FROM) > 0,
           ("SF28 a spur turnout took water from both laterals", tid))
    # SF29: the days without a logger total are exactly the Water Master's estimated days, each a day water ran at the
    # lateral's turnouts
    hd = {}
    for d, l, v in A["headings"]:
        hd.setdefault(l, set()).add(d)
    for l in K.LATERALS:
        missing = set(K.season_days(2026)) - hd[l]
        ok(missing == {d for (ll, d) in A["estimates"] if ll == l} and 2 <= len(missing) <= 5,
           ("SF29 the days without a total are the estimated days", l, len(missing)))
    ran = _days_water_ran(rows, ix)
    for (l, d) in A["estimates"]:
        ok((l, d) in ran, ("SF29 water ran on an estimated day", l, d))
    # SF31: every board note carries the time the rider set or pulled the board, ahead of that sheet's reading
    notes = 0
    for rr in C.read_csv(os.path.join(target, K.WEIRS))[1:]:
        rem = rr[5]
        if "brd" in rem:
            notes += 1
            hhmm = rem.split()[-1]
            ok(re.fullmatch(r"\d{4}", hhmm) and "%s:%s" % (hhmm[:2], hhmm[2:]) < rr[3], ("board note before the reading",
                                                                                     rr[0], rr[1]))
    ok(notes == 24, ("board notes", notes))
    # SF33: the replacements; the shop's registers bracket the book's reads
    ok(set(units.values()) == {"New", "Rebuilt"}, ("new and rebuilt replacements", sorted(set(units.values()))))
    for c in A["changes"]:
        u = units[(c["old"], c["new"])]
        ok((c["installation"] == 0.0) == (u == "New"), ("SF33 installation register", c["new"], u, c["installation"]))
        first = [v for t, s, v, _ in A["reads"][c["turnout"]] if s == c["new"]][0]
        lastv = [v for t, s, v, _ in A["reads"][c["turnout"]] if s == c["old"]][-1]
        ok(0.0 <= first - c["installation"] < 200.0, ("SF33 first read just past the installation register", c["new"]))
        ok((c["removal"] - lastv) % 10000.0 < 200.0, ("SF33 removal register just past the last read", c["old"]))
    ok(len(A["changes"]) >= 18 and len({c["turnout"][:2] for c in A["changes"]}) == 9, "meter changes on every lateral")
    ok(all(v[0][0].date() < dt.date(2026, 2, 1) and v[-1][0].date() > dt.date(2026, 10, 31) for v in A["reads"].values()),
       "SF30 the meter book brackets the season")
    # the counts the design note quotes on the ask paths (H2: each recomputed here)
    hcf = {s_ for s_, u_ in A["units"].items() if u_ == "HCF"}
    rolls = sorted({tid for tid, rd in A["reads"].items()
                    for (t0, s0, v0, _), (t1, s1, v1, _) in zip(rd, rd[1:]) if s0 == s1 and v1 < v0})
    n_new = sum(1 for c_ in A["changes"] if units[(c_["old"], c_["new"])] == "New")
    wo = _work_orders(target)
    remarks = [rr[5] for rr in C.read_csv(os.path.join(target, K.WEIRS))[1:] if rr[5] and "brd" not in rr[5]]
    ok(len(hcf) == 42 and len({t[:2] for t in A["reads"] if any(s_ in hcf for _, s_, _, _ in A["reads"][t])}) == 9,
       ("magnetic meters on every lateral", len(hcf)))
    ok(len(rolls) == 7 and sorted({t[:2] for t in rolls}) == ["01", "02", "05", "07"], ("rollovers", rolls))
    ok(len(A["changes"]) == 31 and n_new == 14 and wo["swaps"] == 31 and wo["other"] == 47,
       ("swaps and work orders", len(A["changes"]), n_new, wo))
    ok(len(A["estimates"]) == 32, ("estimated days", len(A["estimates"])))
    ok(len(remarks) == 91 and len(set(remarks)) == 7, ("other weir remarks", len(remarks), len(set(remarks))))
    print("  ask paths: %d magnetic meters on every lateral; rollovers at %s; %d swaps (%d new, %d rebuilt) among %d "
          "routine work orders; %d logger days without a total; %d board notes among %d other remarks of %d kinds" % (
              len(hcf), ", ".join(rolls), len(A["changes"]), n_new, len(A["changes"]) - n_new, wo["other"],
              len(A["estimates"]), notes, len(remarks), len(set(remarks))))
    print("  Ask 1 deliveries: %s" % ", ".join("%s %s" % (l, af(K.round_to(gd[l], 10))) for l in K.LATERALS))
    print("  Ask 2 water put in: %s" % ", ".join("%s %s" % (l, af(K.round_to(gi[l], 10))) for l in K.LATERALS))
    print("  Ask 3 shares: %s" % ", ".join("%s %.1f" % (l, share1(gs[l])) for l in K.LATERALS))
    print("  Ask 4 spill: %s" % ", ".join("%s %s" % (l, af(K.round_to(sp[l], 10))) for l in K.LATERALS))
    print("  stops: S2 within each meter %s; S1 by turnout %s to %s; S2b new meters from zero %s" % (
        ", ".join("%s %+.0f" % (l, s2d[l] - gd[l]) for l in K.LATERALS),
        af(min(K.round_to(v, 10) for v in s1d.values())), af(max(K.round_to(v, 10) for v in s1d.values())),
        ", ".join("%s %+.0f" % (l, s2bd[l] - gd[l]) for l in K.LATERALS)))
    print("         register's lateral: Lateral 5 %s, Lateral 6 %s; water put in without estimates %s" % (
        af(K.round_to(s3d["L5"], 10)), af(K.round_to(s3d["L6"], 10)),
        ", ".join("%s %+.0f" % (l, i0[l] - gi[l]) for l in K.LATERALS)))
    print("         bare crest %s; alternate days as zero %s; board change from the next day %s" % (
        ", ".join("%s %s" % (l, af(K.round_to(b1[l], 10))) for l in K.LATERALS),
        ", ".join("%s %s" % (l, af(K.round_to(b2[l], 10))) for l in moved_b2),
        ", ".join("%s %s" % (l, af(K.round_to(lag[l], 10))) for l in moved_lag)))
    print("         shares with the chain but not the estimates %s; with the estimates but not the chain %s" % (
        ", ".join("%s %.1f" % (l, share1(100.0 * (i0[l] - gd[l]) / i0[l])) for l in K.LATERALS),
        ", ".join("%s %.1f" % (l, share1(100.0 * (gi[l] - s2d[l]) / gi[l])) for l in K.LATERALS)))

    # ------------------------------------------------------------------------------------------ separation line
    ask_files = [K.METER_BOOK, K.SHOP_LOG, K.HEADINGS, K.WEIRS, K.STRUCTURES, K.OPS_LOG]
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in ask_files + K.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        M2 = C.load(tmp)
        o2 = C.order_from(M2.thirty(M2.start_golden())[0])
        ok(o2["order"] == g["order"] and abs(o2["req"] - g["req"]) < 1e-6, "call unchanged without ask files and distractors")
    finally:
        shutil.rmtree(tmp)
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in K.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        A2 = C.load_asks(tmp)
        d2, s2_, i2 = C.ask_a(A2)
        ok(all(abs(d2[l] - gd[l]) < 1e-9 and abs(i2[l] - gi[l]) < 1e-9 and abs(C.ask_b(A2)[l] - sp[l]) < 1e-9
               for l in K.LATERALS), "asks unchanged without the distractors")
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------------------------------ input gates
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    big = max(len(C.read_csv(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, ("a 25,000-row file", big))
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "distractors")
        ok(all("distractor" not in f.lower() for f in files), "no file named distractor")

    # ------------------------------------------------------------------------------------------ hygiene and realism
    for f in files:
        p = os.path.join(target, f)
        b = open(p, "rb").read()
        for bad in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib", b"Python"):
            if f.endswith((".xlsx", ".docx")):
                with zipfile.ZipFile(p) as z:
                    blob = b"".join(z.read(n) for n in z.namelist())
                ok(bad not in blob, ("container signature", f, bad))
            else:
                ok(bad not in b, ("signature", f, bad))
        txt = _text_of(p)
        ok("\u2014" not in txt and "\u2013" not in txt, ("dash", f))
        for w in ("fictional", "fictitious", "this exercise", "constructed for", "synthetic"):
            ok(w not in txt.lower(), ("fiction tell", f, w))
    for f in os.listdir(golden):
        txt = _text_of(os.path.join(golden, f))
        ok("\u2014" not in txt and "\u2013" not in txt, ("dash in golden", f))
        ok("matplotlib" not in txt.lower() and "openpyxl" not in txt.lower(), ("golden signature", f))
    for rr in rows[1:]:
        ok(rr[ix["set_end"]][:10] <= "2026-10-31" and rr[ix["entered_at"]][:10] <= "2026-10-31", "order dates")
    ok(max(M.wx) == K.WEATHER_END, "weather through 31 January 2027")
    for f in files:
        ds = _dates_in(os.path.join(target, f))
        ok(not ds or max(ds) <= K.EXTRACT, ("a date after the extract", f, max(ds) if ds else None))
    readme = open(os.path.join(target, K.README), encoding="utf-8").read()
    ok(all(f in readme for f in files if f != K.README), "the working-files note lists every file")
    ok(len({round(gi[l], 2) for l in K.LATERALS}) == 9 and len({round(gd[l], 2) for l in K.LATERALS}) == 9,
       "distinct lateral totals")
    ok(all(abs(gd[l] - round(gd[l])) > 1e-6 for l in K.LATERALS), "deliveries not whole numbers before rounding")
    # the request clerk's remarks: a revision's remark says what changed, a withdrawal's reason fits its crop, and no one
    # remark dominates
    versions = {}
    for q in M.requests:
        versions.setdefault(q["Request no."], []).append(q)
    for no, vs in versions.items():
        vs = sorted(vs, key=lambda q: q["Version"])
        lastq = vs[-1]
        rem = (lastq["Remarks"] or "").lower()
        if len(vs) == 2:
            ok(vs[0]["Irrigation method"] == lastq["Irrigation method"] and ("acre" in rem or "revised" in rem),
               ("revision remark", no, rem))
        if lastq["Status"] == "Withdrawn":
            ok(rem != "", ("withdrawal without a reason", no))
        if "orchard" in rem or "trees" in rem:
            ok(lastq["Crop code"] in ("ALM", "PIS", "WAL", "CIT"), ("orchard remark", no, lastq["Crop code"]))
        if "vine" in rem:
            ok(lastq["Crop code"] == "GRW", ("vineyard remark", no, lastq["Crop code"]))
        if "fallowing" in rem or "out of production" in rem:
            ok(lastq["Crop code"] in ("ALF", "PAS"), ("fallowing remark", no, lastq["Crop code"]))
    remarks = [q["Remarks"] for q in M.requests if q["Remarks"]]
    top = max(remarks.count(x) for x in set(remarks))
    ok(len(set(remarks)) >= 10 and top <= 0.35 * len(remarks), ("request remarks", len(set(remarks)), top, len(remarks)))
    # the operations log: entries in time order, each written when it happened; the meter-read entries come after the
    # reads they report
    log = _ops_log(target)
    ok(log == sorted(log, key=lambda e: (e[0], e[1])) and len({e[0] for e in log}) >= 30, "operations log")
    last_read = {}
    for v in A["reads"].values():
        for t_, s_, r_, u_ in v:
            last_read[t_.date()] = max(last_read.get(t_.date(), t_), t_)
    for day, time, text, by in log:
        if "read today" in text or "reads taken" in text:
            hh, mm = (int(x) for x in time.split(":"))
            ok(dt.datetime(day.year, day.month, day.day, hh, mm) > last_read[day], ("log entry before the reads", day))
    print("checks.py: %d assertions passed" % N[0])
    ok(N[0] >= 40, "forty or more assertions")
    return lad


# ---------------------------------------------------------------------------------------------------- the clean truth

def _truth(W):
    """The world before any file is written: the 2027 fields, their crops, methods and acres, and the 2026 delivered
    sets, from the simulation."""
    acc = [f for f in W.fields if f["req_status"] == "accepted"]
    sets26 = {(o["start"], o["end"], round(o["cfs"], 1)) for o in W.orders if o["season"] == 2026
              and o["status"] == "Delivered" and W.field[o["field_id"]]["req_status"] == "accepted"}
    return dict(ids=[f["id"] for f in acc], acres={f["id"]: f["acres"] for f in acc},
                crop={f["id"]: f["crop"] for f in acc}, method={f["id"]: f["method"] for f in acc},
                sets26=sets26, W=W)


def _truth_order(T, M, route):
    """The order on the world's own fields, weather and 2026 sets: route 'last set' (each field's last set taken as a
    refill) or 'record' (the season run on the water its sets put in)."""
    W = T["W"]
    fields = [dict(id=f["id"], lateral=f["lateral"], soil=f["soil"], crop=f["crop"], method=f["method"], acres=f["acres"],
                   turnout=f["turnout"]) for f in W.fields if f["req_status"] == "accepted"]
    fields.sort(key=lambda f: f["id"])
    record, last = [], {}
    for o in W.orders:
        if o["season"] != 2026 or W.field[o["field_id"]]["req_status"] != "accepted":
            continue
        record.append((o["field_id"], o["start"], o["end"], o["cfs"], o["status"]))
        if o["status"] == "Delivered":
            last[o["field_id"]] = max(last.get(o["field_id"], o["end"].date()), o["end"].date())
    Mt = C.Model(fields, W.wx, M.T, last_delivery=last, record=record)
    start = Mt.start_last_set() if route == "last set" else Mt.start_golden()
    return C.order_from(Mt.thirty(start)[0])


# ---------------------------------------------------------------------------------------------------- helpers

def _season_path(M, water):
    """The record run through 2026 to each field's last set: the last day each field was full before its last set,
    and its depletion at the end of its last set's day."""
    Dd = np.zeros(M.n)
    lastfull = np.full(M.n, dt.date(2026, 1, 31).toordinal())
    at_last = np.zeros(M.n)
    lo = np.array([M.last_delivery[i].toordinal() for i in M.ids])
    for d in K.daterange(K.WINTER_FULL + dt.timedelta(days=1), dt.date(2026, 10, 31)):
        e, r = M.wx[d]
        net = water[d] * 12.0 / M.acres * M.ea if d in water else 0.0
        Dd = np.minimum(np.maximum(Dd + M.kc[:, d.month - 1] * e - r - net, 0.0), M.taw)
        lastfull = np.where((Dd < 1e-12) & (d.toordinal() < lo), d.toordinal(), lastfull)
        at_last = np.where(d.toordinal() == lo, Dd, at_last)
    return lastfull, at_last


def _season_shortfall(M, water, lastfull):
    """Each field's crop water use less rain, less its delivered water at its efficiency, from the day after it was
    last full to the end of its last set's day."""
    out = np.zeros(M.n)
    lo = np.array([M.last_delivery[i].toordinal() for i in M.ids])
    for d in K.daterange(K.WINTER_FULL + dt.timedelta(days=1), dt.date(2026, 10, 31)):
        o = d.toordinal()
        inside = (o > lastfull) & (o <= lo)
        e, r = M.wx[d]
        net = water[d] * 12.0 / M.acres * M.ea if d in water else 0.0
        out += np.where(inside, M.kc[:, d.month - 1] * e - r - net, 0.0)
    return out


def _water_all_seasons(M, target):
    """{date: AF on each 2027 field} from every season's delivered sets, a former field id's sets shared between the
    fields the register maps it to."""
    idx = {f: i for i, f in enumerate(M.ids)}
    by_former = {}
    for fid, g_ in M.register.items():
        by_former.setdefault(g_["former_field_id"], []).append(fid)
    out = {}
    rows = C.read_csv(os.path.join(target, K.ORDERS))
    ix = {c: rows[0].index(c) for c in rows[0]}
    for rr in rows[1:]:
        if rr[ix["status"]] != "Delivered":
            continue
        fids = [rr[ix["field_id"]]] if rr[ix["field_id"]] in M.register else by_former.get(rr[ix["field_id"]], [])
        a = dt.datetime.fromisoformat(rr[ix["set_start"]])
        b = dt.datetime.fromisoformat(rr[ix["set_end"]])
        cfs = float(rr[ix["ordered_cfs"]])
        for fid in fids:
            if fid not in idx:
                continue
            t = a
            while t < b:
                seg = min(b, dt.datetime(t.year, t.month, t.day) + dt.timedelta(days=1))
                out.setdefault(t.date(), np.zeros(M.n))[idx[fid]] += \
                    cfs * (seg - t).total_seconds() / K.CUFT_PER_AF / len(fids)
                t = seg
    return out


def _border_last_set_ends(M):
    lasts = {}
    for fid, a, b, cfs, s in M.record:
        if s == "Delivered" and (fid not in lasts or b > lasts[fid][1]):
            lasts[fid] = (a, b)
    return [lasts[f["id"]][1].time() for f in M.fields if f["method"] == "Border"]


def _meter_scale(M, A, target):
    """Each field's 2026 sets scaled by its turnout's metered water over its ordered water (the season)."""
    metered = {tid: sum(v for t1, v in C.turnout_intervals(A, tid, "chain")) for tid in A["reads"]}
    ordered = {}
    rows = C.read_csv(os.path.join(target, K.ORDERS))
    ix = {c: rows[0].index(c) for c in rows[0]}
    for rr in rows[1:]:
        if rr[ix["season"]] == "2026" and rr[ix["status"]] == "Delivered":
            a = dt.datetime.fromisoformat(rr[ix["set_start"]])
            b = dt.datetime.fromisoformat(rr[ix["set_end"]])
            ordered[rr[ix["turnout"]]] = ordered.get(rr[ix["turnout"]], 0.0) + \
                float(rr[ix["ordered_cfs"]]) * (b - a).total_seconds() / K.CUFT_PER_AF
    t_of = {f["id"]: C.tid_from_gis(f["turnout"]) for f in M.fields}
    return np.array([metered[t_of[f["id"]]] / ordered[t_of[f["id"]]] for f in M.fields])


def _days_water_ran(rows, ix):
    """(lateral, date) for every day a delivered 2026 set ran at a turnout fed by that lateral."""
    out = set()
    moved = set(K.MOVED)
    for rr in rows[1:]:
        if rr[ix["season"]] != "2026" or rr[ix["status"]] != "Delivered":
            continue
        tid = rr[ix["turnout"]]
        a = dt.datetime.fromisoformat(rr[ix["set_start"]])
        b = dt.datetime.fromisoformat(rr[ix["set_end"]])
        d = a.date()
        while d <= b.date():
            lat = "L%d" % int(tid[:2])
            if tid in moved and d > C.MOVED_FROM:
                lat = "L6"
            out.add((lat, d))
            d += dt.timedelta(days=1)
    return out


def _text_of(path):
    if path.endswith((".csv", ".txt", ".svg", ".json")):
        return open(path, encoding="utf-8", errors="replace").read()
    if path.endswith((".xlsx", ".docx")):
        with zipfile.ZipFile(path) as z:
            return "".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))
    if path.endswith(".pdf"):
        try:
            import pypdf
            return "".join(p.extract_text() or "" for p in pypdf.PdfReader(path).pages)
        except Exception:
            return ""
    return ""


def _order_rain_first(M, start):
    """SF8's second alternative: each replay day's rain taken off first, its excess drained, then the day's ET added."""
    class RainFirst(C.Model):
        def day(self, D, d, cap=True):
            e, rn = self.wx[d]
            D = np.maximum(D - rn, 0.0) + self.kc[:, d.month - 1] * e
            return np.minimum(D, self.taw) if cap else D
    M2 = RainFirst(M.fields, M.wx, M.T)
    return C.order_from(M2.thirty(start)[0])


def _replacement_units(target):
    """(meter out, meter in) -> New or Rebuilt, from the shop's 2026 work orders."""
    import openpyxl
    rows = list(openpyxl.load_workbook(os.path.join(target, K.SHOP_LOG), data_only=True)["Work orders 2026"]
                .iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "WO no.")
    head = list(rows[hi])
    out = {}
    for r in rows[hi + 1:]:
        if r and r[0] is not None:
            x = dict(zip(head, r))
            if x["Meter out"]:
                out[(x["Meter out"], x["Meter in"])] = x["Unit"]
    return out


def _work_orders(target):
    """The shop's 2026 work orders: swaps (a meter out and a meter in) and other work on meters left in place."""
    import openpyxl
    rows = list(openpyxl.load_workbook(os.path.join(target, K.SHOP_LOG), data_only=True)["Work orders 2026"]
                .iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "WO no.")
    head = list(rows[hi])
    body = [dict(zip(head, r)) for r in rows[hi + 1:] if r and r[0] is not None]
    return {"swaps": sum(1 for x in body if x["Meter out"]), "other": sum(1 for x in body if not x["Meter out"])}


def _lateral_of(A, tid, t1):
    reg_lat, built = A["lateral"][tid], "L%d" % int(tid[:2])
    return built if (built != reg_lat and t1.date() <= C.MOVED_FROM) else reg_lat


def _ask_a_new_from_zero(A, units):
    """Ask 1 deliveries within each meter's own reads, plus each new meter's first read taken from zero."""
    deliv = {l: 0.0 for l in K.LATERALS}
    for tid, rd in A["reads"].items():
        for t1, v in C.turnout_intervals(A, tid, "serial"):
            deliv[_lateral_of(A, tid, t1)] += v
        for c in A["changes"]:
            if c["turnout"] == tid and units[(c["old"], c["new"])] == "New":
                t1, v = next((t, v) for t, s, v, u in rd if s == c["new"])
                deliv[_lateral_of(A, tid, t1)] += v
    return deliv


def _ops_log(target):
    import docx
    t = docx.Document(os.path.join(target, K.OPS_LOG)).tables[0]
    out = []
    for row in t.rows[1:]:
        c = [x.text for x in row.cells]
        out.append((dt.date.fromisoformat(c[0]), c[1], c[2], c[3]))
    return out


def _ask_b_lagged(A):
    """Ask 4 with each board change noted on a sheet taken as in place only from the next day."""
    spill = {}
    for lat in K.LATERALS:
        L, crest, C_ = A["weir"][lat]
        bc = C.board_counts(A, lat)
        prev, p = {}, 0
        for d in sorted(bc):
            prev[d] = p
            p = bc[d]
        rd = {d: g for d, g, _, _ in A["sheets"][lat]}
        tot, cur = 0.0, None
        for d in K.season_days(2026):
            if d in rd:
                cur = (rd[d], prev[d])
            g, nb = cur
            h = g - (crest + 2.0 / 12.0 * nb)
            if h > 0:
                tot += C_ * L * h ** 1.5 * K.AF_PER_CFS_DAY
        spill[lat] = tot
    return spill


def _dates_in(path):
    out = []
    if path.endswith((".csv", ".txt")):
        t = open(path, encoding="utf-8").read()
        out += [dt.date(int(a), int(b), int(c)) for a, b, c in re.findall(r"\b(\d{4})-(\d{2})-(\d{2})\b", t)]
        out += [dt.date(int(c), int(a), int(b)) for a, b, c in re.findall(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", t)]
    elif path.endswith(".xlsx"):
        import openpyxl
        for ws in openpyxl.load_workbook(path, data_only=True).worksheets:
            for row in ws.iter_rows(values_only=True):
                out += [v.date() for v in row if isinstance(v, dt.datetime)]
    return out


def _min_gap(M, start):
    gap = np.inf
    for y in K.REPLAY_YEARS:
        D = start(y).copy()
        for d in K.season_days(y):
            D = M.day(D, d)
            gap = min(gap, float(np.min(np.abs(D - M.raw))))
            D = np.where(D >= M.raw, 0.0, D)
    return gap


def _order_on_fields(M, fields):
    """The golden route on another set of fields: the 2026 record run for each (by field id), then the replays."""
    M2 = C.Model(fields, M.wx, M.T, last_delivery=M.last_delivery, record=M.record)
    M2.ids = [f["id"] for f in fields]
    return C.order_from(M2.thirty(M2.start_golden())[0])


def _order_on_tables(M, T):
    M2 = C.Model(M.fields, M.wx, T, last_delivery=M.last_delivery, record=M.record)
    return C.order_from(M2.thirty(M2.start_golden())[0])


def _order_on_weather(M, wx):
    M2 = C.Model(M.fields, wx, M.T, last_delivery=M.last_delivery, record=M.record)
    return C.order_from(M2.thirty(M2.start_golden())[0])


def _order_test_before_rain(M, start):
    req = {}
    for y in K.REPLAY_YEARS:
        Dd = start(y).copy()
        m9 = np.zeros(M.n)
        for d in K.season_days(y):
            e, rn = M.wx[d]
            Dd = Dd + M.kc[:, d.month - 1] * e
            irr = Dd >= M.raw
            m9 += np.where(irr, np.minimum(Dd, M.taw), 0.0)
            Dd = np.where(irr, 0.0, Dd)
            Dd = np.minimum(np.maximum(Dd - rn, 0.0), M.taw)
        farm = m9 / M.ea * M.acres / 12.0
        req[y] = float((np.bincount(M.lat, weights=farm, minlength=9) / (1 - M.loss)).sum() / (1 - M.main))
    return C.order_from(req)


def _order_loss_multiplied(M, start):
    req = {}
    for y in K.REPLAY_YEARS:
        Dd = start(y).copy()
        tot = np.zeros(M.n)
        for d in K.season_days(y):
            Dd = M.day(Dd, d)
            irr = Dd >= M.raw
            tot += np.where(irr, Dd, 0.0)
            Dd = np.where(irr, 0.0, Dd)
        farm = tot / M.ea * M.acres / 12.0
        req[y] = float((np.bincount(M.lat, weights=farm, minlength=9) * (1 + M.loss)).sum() * (1 + M.main))
    return C.order_from(req)


def _order_hargreaves(M, target):
    """ET0 by Hargreaves-Samani from each station's daily temperatures (station 39 to April 2014, the yard after)."""
    import weather as WX
    rows = C.read_csv(os.path.join(target, K.ST39))
    h = rows[0]
    s39 = {}
    for rr in rows[1:]:
        m, d_, y = (int(x) for x in rr[h.index("Date")].split("/"))
        s39[dt.date(y, m, d_)] = (float(rr[h.index("Max Air Temp (C)")]), float(rr[h.index("Min Air Temp (C)")]))
    yard = {}
    for rr in C.read_csv(os.path.join(target, K.YARD))[1:]:
        if rr[1] == "":
            continue
        yard[dt.date.fromisoformat(rr[0])] = ((float(rr[3]) - 32) * 5 / 9, (float(rr[4]) - 32) * 5 / 9)
    wx = {}
    for d, (e, rn) in M.wx.items():
        tmax, tmin = yard[d] if (d >= K.SPLICE and d in yard) else s39[d]
        ra = WX._ra(d.timetuple().tm_yday) * 0.408
        et = 0.0023 * ra * ((tmax + tmin) / 2 + 17.8) * max(tmax - tmin, 0.0) ** 0.5
        wx[d] = (et / 25.4, rn)
    return _order_on_weather(M, wx)
