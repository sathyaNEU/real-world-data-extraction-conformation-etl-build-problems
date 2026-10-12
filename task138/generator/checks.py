"""task138 assertions: the input gates, every rung of the ladder and its separation, every semantic fork row (SF1 to
SF29, the asks' readings among them), the graded figures' distances to their rounding edges, the asks' stops and
devices, the separation line between the call and the asks, the distractors' deletion test, and the realism and
hygiene sweeps. Run by build.py on every build; prints the ladder and the measured figures the design note quotes."""
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
    o = C.order_from(req)
    o["months"] = C.schedule(o["order"], mon)[0]
    return o


def run(target, golden, W=None, meta_path=None):
    N[0] = 0
    M = C.load(target)
    lad = C.ladder(M)
    g = lad["R3"]
    print("ladder (24th smallest of thirty, order, setting year):")
    for k, v in lad.items():
        print("  %-4s %-92s %12s  %7s  %d  %+.2f%%" % (k, v["label"][:92], "{:,.2f}".format(v["req"]),
                                                   "{:,}".format(v["order"]), v["year"], 100 * (v["req"] / g["req"] - 1)))

    # ------------------------------------------------------------------------------------------ the golden call
    ok(g["order"] == 202700 and g["year"] == 2012, ("golden", g["order"], g["year"]))
    ok(K.round_to(g["req"], 10) == 202660, g["req"])
    ok(g["months"] == [13520, 970, 10290, 27190, 37470, 42010, 37270, 24010, 9970], g["months"])
    ok(sum(g["months"]) == g["order"], "schedule adds to the order")
    lo = g["req"] - (g["order"] - 100)
    ok(25 <= lo <= 75, ("24th smallest inside its hundred", lo))
    ok(edge(g["req"], 10) >= 1.5, ("setting requirement edge", edge(g["req"], 10)))
    for x in g["raw_months"][:8]:
        ok(edge(x, 10) >= 1.5, ("month edge", x))
    r = g["ranked"]
    ok(r[23][1] - r[22][1] >= 300 and r[24][1] - r[23][1] >= 300, ("SF23 neighbours", r[22][1], r[23][1], r[24][1]))
    print("  golden 24th %.2f (%.2f above %s), neighbours %s %.0f and %s %.0f; month edges min %.2f AF" % (
        g["req"], lo, "{:,}".format(g["order"] - 100), r[22][0], r[22][1], r[24][0], r[24][1],
        min(edge(x, 10) for x in g["raw_months"][:8])))

    # ------------------------------------------------------------------------------------------ the ladder
    R0, R1, R2, R2b, R2c, R2d, O1, O2 = (lad[k] for k in ("R0", "R1", "R2", "R2b", "R2c", "R2d", "O1", "O2"))
    ok(R0["order"] == 189800 and R0["year"] == 2003, ("default path", R0["order"], R0["year"]))
    ok(R0["req"] / g["req"] - 1 <= -0.05, "R0 at least 5 per cent under")
    ok(R1["req"] / g["req"] - 1 <= -0.045, "R1 at least 4.5 per cent under")
    ok(R2["req"] / g["req"] - 1 <= -0.03, "R2 at least 3 per cent under")
    ok(R2b["req"] / g["req"] - 1 <= -0.05, "R2b at least 5 per cent under")
    ok(R2c["req"] / g["req"] - 1 <= -0.01, "R2c at least 1 per cent under")
    ok(R2d["req"] / g["req"] - 1 <= -0.006, "R2d at least 0.6 per cent under")
    ok(O1["req"] > g["req"] and O2["req"] > g["req"], "over-corrections above")
    # SF9: where each replay starts; every start the ladder prices files its own order
    for k in ("R0", "R1", "R2", "R2b", "R2c", "R2d", "O1", "O2"):
        ok(lad[k]["order"] != g["order"], ("SF9 rung files its own order", k))
    for k in ("R0", "R1", "R2", "R2b"):
        ok(lad[k]["year"] != g["year"], ("rung names another setting year", k))
        ok(lad[k]["months"] != g["months"] and lad[k]["months"][0] != g["months"][0], ("rung's February", k))
    ok(R0["months"][0] < 100 and g["months"][0] > 10000, "February under the default path and the golden")
    D = M.D_golden
    print("  31 January 2027: acre-weighted depletion %.2f in; %d of %d fields at or past allowable depletion" % (
        float((D * M.acres).sum() / M.acres.sum()), int((D >= M.raw).sum()), M.n))

    # ------------------------------------------------------------------------------------------ closure
    # axis 9: every allowable depletion is an odd number of hundred-thousandths of an inch, off every lattice a day's
    # depletion can sit on (station 39's tenths of a millimetre, the yard's hundredths of an inch, two-decimal
    # coefficients), so no replay day lands on one; the closest approach is measured
    for c in K.CROPS:
        for su, (awc, lim) in M.T["soils"].items():
            depth = M.T["root"][c] if lim is None else min(M.T["root"][c], lim)
            odd = round(M.T["mad"][c] * 100) * round(awc * 100) * round(depth * 10)
            ok(odd % 2 == 1, ("allowable depletion off the stations' decimals", c, su))
    gap = _min_gap(M, M.start_golden())
    ok(gap > 1e-7, ("closest approach of a day's depletion to an allowable depletion", gap))
    # axis 12: the weather record has every day from October 1995 to 31 January 2027
    ok(all(d in M.s39 for d in K.daterange(K.WEATHER_START, K.WEATHER_END)), "station 39 has every day")
    print("  closest approach of a replay day's depletion to an allowable depletion: %.2e in" % gap)
    # the data-native sentence: the October to January before the order is the driest in the record
    wint = {y: sum(M.wx[d][1] for d in K.daterange(dt.date(y, 10, 1), dt.date(y + 1, 1, 31))) for y in range(1995, 2027)}
    ok(min(wint, key=wint.get) == 2026, ("driest October to January", sorted(wint.items(), key=lambda kv: kv[1])[:3]))
    lastm = [M.last_delivery[f["id"]].month for f in M.fields]
    print("  October 2026 to January 2027 rain %.2f in (the next driest %.2f in, median of %d winters %.2f in); last "
          "2026 sets in September %d, October %d" % (wint[2026], sorted(wint.values())[1], len(wint),
                                                    float(np.median(list(wint.values()))), lastm.count(9),
                                                    lastm.count(10)))

    # ------------------------------------------------------------------------------------------ the fork table
    st = M.start_golden()
    # SF1: no delivered set outside the canal season in any season on file
    rows = C.read_csv(os.path.join(target, K.ORDERS))
    head = rows[0]
    ix = {c: head.index(c) for c in head}
    for rr in rows[1:]:
        if rr[ix["status"]] == "Delivered":
            a = dt.date.fromisoformat(rr[ix["set_start"]][:10])
            b = dt.date.fromisoformat(rr[ix["set_end"]][:10])
            ok((a.month, a.day) >= (2, 1) and (b.month, b.day) <= (10, 31) and a.year == b.year == int(rr[ix["season"]]),
               ("SF1 delivered set inside the season", rr[ix["order_no"]]))
    # SF2: the interpolated 80th percentile files another order
    vals = sorted(g["reqs"].values())
    p80 = float(np.percentile(vals, 80))
    ok(K.ceil_hundred(p80) != g["order"], ("SF2 interpolated 80th percentile", p80))
    ok(K.round_to(vals[23], 100) == g["order"], "SF2 the 24th rounded to the nearest hundred converges")
    # SF3: every request row, or withdrawn requests in
    M3 = copy.copy(M)
    alt = []
    for q in M.requests:
        if q["Status"] == "Superseded" or q["Status"] == "Accepted" or q["Status"] == "Withdrawn":
            gg = M.register[q["Field"]]
            alt.append(dict(id=q["Field"], lateral="L" + gg["lateral"].split()[-1], soil=gg["soil_unit"],
                            crop=q["Crop code"], method=q["Irrigation method"], acres=float(q["Acres"])))
    sf3 = _order_on_fields(M, alt, allow_dupes=True)
    ok(sf3["order"] != g["order"], ("SF3", sf3["order"]))
    # SF4: the register's GIS acres
    fields4 = [dict(f, acres=float(M.register[f["id"]]["gis_acres"])) for f in M.fields]
    sf4 = _order_on_fields(M, fields4)
    ok(sf4["order"] != g["order"], ("SF4", sf4["order"]))
    # SF5: no depth limit
    T5 = copy.deepcopy(M.T)
    T5["soils"] = {k: (v[0], None) for k, v in T5["soils"].items()}
    sf5 = _order_on_tables(M, T5)
    ok(sf5["order"] != g["order"], ("SF5", sf5["order"]))
    # SF6: station 39 throughout; the yard from its first day; missing yard days dropped
    wx_a = {d: M.s39[d] for d in M.wx}
    wx_b = {d: (M.yard[d] if (d >= K.DISTRICT_STATION_START and d in M.yard) else M.s39[d]) for d in M.wx}
    wx_c = {d: (M.yard.get(d, (0.0, 0.0)) if d >= K.SPLICE else M.s39[d]) for d in M.wx}
    sf6 = {k: _order_on_weather(M, w) for k, w in (("st39", wx_a), ("yard_from_april", wx_b), ("missing_zero", wx_c))}
    ok(sf6["st39"]["order"] != g["order"], ("SF6 station 39", sf6["st39"]["order"]))
    ok(sf6["missing_zero"]["order"] != g["order"] or sf6["missing_zero"]["months"] != g["months"], "SF6 missing")
    ok(sf6["yard_from_april"]["order"] == g["order"] and sf6["yard_from_april"]["months"] != g["months"],
       "SF6 the yard from April 2014: the same order, other months")
    print("  SF6 station 39 throughout %s; yard from April 2014 %s; missing yard days as zero %s" % (
        "{:,}".format(sf6["st39"]["order"]), "{:,}".format(sf6["yard_from_april"]["order"]),
        "{:,}".format(sf6["missing_zero"]["order"])))
    # the grid: every start of the ladder on both weather records (WOP 6.1's splice, station 39 throughout)
    M39 = C.Model(M.fields, wx_a, M.T, last_delivery=M.last_delivery, turnout_last=M.turnout_last,
                  cancelled_last=M.cancelled_last)
    lad39 = C.ladder(M39)
    cells = {(k, "splice"): v["order"] for k, v in lad.items()}
    cells.update({(k, "station 39"): v["order"] for k, v in lad39.items()})
    ok(len(cells) == 18 and [kv for kv, v in cells.items() if v == g["order"]] == [("R3", "splice")],
       ("grid: the golden cell alone files the golden order", cells))
    print("  grid on station 39 throughout: %s" % ", ".join("%s %s" % (k, "{:,}".format(v["order"]))
                                                          for k, v in lad39.items()))
    # SF7: 29 February dropped (WOP 2.4 keeps it)
    sf7 = variant_order(M, st, drop_leap=True)
    ok(sf7["order"] != g["order"] or sf7["months"] != g["months"], ("SF7", sf7["order"]))
    print("  SF7 29 February dropped: %s set by %d" % ("{:,}".format(sf7["order"]), sf7["year"]))
    # SF8: the irrigation test before rain
    sf8 = _order_test_before_rain(M, st)
    ok(sf8["order"] != g["order"], ("SF8", sf8["order"]))
    # SF8, second alternative: the day's rain taken first, its excess over the depletion drained, then the day's ET
    # (WOP 3.1 nets the day: the previous depletion plus the day's ET less its rain, then the floor at zero)
    sf8b = _order_rain_first(M)
    ok(sf8b["order"] != g["order"], ("SF8 rain first", sf8b["order"]))
    # SF10: cancelled orders as irrigations (R2d), SF14 no cap (O2): in the ladder
    ok(R2d["order"] != g["order"] and O2["order"] != g["order"], "SF10 SF14")
    # SF11: every requested field's last 2026 delivered set starts and ends on one day
    lastset = {}
    for rr in rows[1:]:
        if rr[ix["season"]] == "2026" and rr[ix["status"]] == "Delivered":
            a, b = rr[ix["set_start"]], rr[ix["set_end"]]
            fid = rr[ix["field_id"]]
            if fid not in lastset or b > lastset[fid][1]:
                lastset[fid] = (a, b)
    for f in M.fields:
        a, b = lastset[f["id"]]
        ok(a[:10] == b[:10], ("SF11 last set on one day", f["id"]))
    # SF12: every requested field took a delivered set in 2026
    ok(all(f["id"] in M.last_delivery for f in M.fields), "SF12")
    # SF13: every requested field carries its 2026 crop
    crop26 = {rr[0]: rr[2] for rr in C.read_csv(os.path.join(target, K.CROP_REPORT))[1:]}
    ok(all(crop26[f["id"]] == f["crop"] for f in M.fields), "SF13")
    # axes 15 and 16: order numbers unique; the requests and the 2026 orders on the register's current field ids
    ok(len({rr[ix["order_no"]] for rr in rows[1:]}) == len(rows) - 1, "order numbers unique")
    ok(all(f["id"] in M.register for f in M.fields), "requests on register field ids")
    ok({rr[ix["field_id"]] for rr in rows[1:] if rr[ix["season"]] == "2026"} <= set(M.register),
       "2026 orders on register field ids")
    # axis 14: row order changes nothing (the orders shuffled, the requests reversed)
    o14 = _order_shuffled(target)
    ok(o14["order"] == g["order"] and o14["months"] == g["months"] and abs(o14["req"] - g["req"]) < 1e-6, "row order")
    # SF15: deliveries times one plus each allowance
    sf15 = _order_loss_multiplied(M, st)
    ok(sf15["order"] != g["order"], ("SF15", sf15["order"]))
    # SF16: the Lateral 5 tail fields on Lateral 5
    moved = set(K.MOVED)
    rows_o = {rr[ix["field_id"]]: rr[ix["turnout"]] for rr in rows[1:] if rr[ix["season"]] == "2026"}
    fields16 = [dict(f, lateral="L5") if rows_o[f["id"]] in moved else f for f in M.fields]
    ok(sum(1 for f in fields16 if f["lateral"] == "L5") > sum(1 for f in M.fields if f["lateral"] == "L5"), "SF16 fields")
    sf16 = _order_on_fields(M, fields16)
    ok(sf16["order"] != g["order"] or K.round_to(sf16["req"], 10) != K.round_to(g["req"], 10), ("SF16", sf16["order"]))
    # SF17, SF18
    ok(r[24][0] != g["year"] and K.round_to(g["req"], 10) != g["order"], "SF17 SF18")
    # SF19: the setting replay's own months; the mean of the thirty years' monthly shares
    own = g["mon"][g["year"]]
    alt19a = [K.round_to(g["order"] * x / own.sum(), 10) for x in own[:8]]
    shares = np.mean([g["mon"][y] / g["mon"][y].sum() for y in K.REPLAY_YEARS], axis=0)
    alt19b = [K.round_to(g["order"] * x, 10) for x in shares[:8]]
    ok(alt19a != g["months"][:8] and alt19b != g["months"][:8], "SF19")
    # SF20: ET0 recomputed (Hargreaves on the stations' temperatures)
    sf20 = _order_hargreaves(M, target)
    ok(sf20["order"] != g["order"], ("SF20", sf20["order"]))
    # SF21: an effective-rain fraction (75 per cent)
    wx21 = {d: (e, 0.75 * rn) for d, (e, rn) in M.wx.items()}
    sf21 = _order_on_weather(M, wx21)
    ok(sf21["order"] != g["order"], ("SF21", sf21["order"]))
    # SF24: the 2026 season run through the balance with each delivered set's volume as the water it put in, not as
    # an irrigation that returns the root zone to field capacity (WOP 3.4)
    sf24 = _order_applied_depth(M, target)
    ok(sf24["order"] != g["order"], ("SF24", sf24["order"]))
    print("  SF24 each 2026 set's delivered volume as its applied depth: %s set by %d" % ("{:,}".format(sf24["order"]),
                                                                                         sf24["year"]))
    # SF22: acre-feet as inches times acres over 12 (the model's own arithmetic)
    ok(abs(M.replay(2012, D) - g["reqs"][2012]) < 1e-6, "SF22")
    # SF25: the day of a field's last 2026 set ends at zero depletion (WOP 3.4) and the balance resumes the next day;
    # counting that day's ET and rain after the set moves the order
    D25 = _carry_from_set_day(M)
    sf25 = variant_order(M, lambda y: D25)
    ok(sf25["order"] != g["order"], ("SF25", sf25["order"]))
    # SF29: station 39's millimetres in inches at 25.4 to the inch (the dictionary's unit line), carried unrounded
    # (closure axis 10); each converted value rounded to the yard's hundredths, or converted at 0.0394 in per mm, moves
    # the order: neither is a reading of WOP 6.1 or 3.2
    dic = _text_of(os.path.join(target, K.DICTIONARY))
    ok("25.4 millimetres to the inch" in dic, "SF29 the dictionary's unit line")
    sf29 = {}
    for key, conv in (("hundredths", lambda mm: round(mm / 25.4 + 1e-12, 2)), ("0.0394", lambda mm: mm * 0.0394)):
        wx29 = {d: (M.yard[d] if (d >= K.SPLICE and d in M.yard) else
                    (conv(M.s39[d][0] * 25.4), conv(M.s39[d][1] * 25.4))) for d in M.wx}
        sf29[key] = _order_on_weather(M, wx29)
        ok(sf29[key]["order"] != g["order"], ("SF29", key, sf29[key]["order"]))
    print("  SF2 %s, SF3 %s, SF4 %s, SF5 %s, SF8 %s and rain first %s, SF15 %s, SF16 %s, SF20 %s, SF21 %s, SF25 %s, "
          "SF29 hundredths %s and 0.0394 %s" % tuple(
              "{:,}".format(x) for x in (K.ceil_hundred(p80), sf3["order"], sf4["order"], sf5["order"], sf8["order"],
                                         sf8b["order"], sf15["order"], sf16["order"], sf20["order"], sf21["order"],
                                         sf25["order"], sf29["hundredths"]["order"], sf29["0.0394"]["order"])))

    # ------------------------------------------------------------------------------------------ the asks
    A = C.load_asks(target)
    gd, gs, inflow = C.ask_a(A)
    s1d, s1s, _ = C.ask_a(A, mode="turnout")
    s2d, s2s, _ = C.ask_a(A, mode="serial")
    s3d, s3s, _ = C.ask_a(A, as_of=False)
    s4d, s4s, _ = C.ask_a(A, drop_estimated=True)
    sp = C.ask_b(A)
    b1 = C.ask_b(A, boards=False)
    b2 = C.ask_b(A, fill=False)
    for l in K.LATERALS:
        ok(edge(gd[l], 10) >= 1.0 and edge(sp[l], 10) >= 1.0 and edge(gs[l], 0.1) >= 0.01, ("ask edges", l))
        ok(K.round_to(s1d[l], 10) != K.round_to(gd[l], 10) and share1(s1s[l]) != share1(gs[l]), ("Ask A S1", l))
        ok(K.round_to(s2d[l], 10) != K.round_to(gd[l], 10) and share1(s2s[l]) != share1(gs[l]), ("Ask A S2", l))
        ok(K.round_to(b1[l], 10) != K.round_to(sp[l], 10), ("Ask B S1", l))
        ok(b1[l] < inflow[l] - gd[l], ("bare-crest spill stays under the lateral's loss", l))
        ok(sp[l] < inflow[l] - gd[l], ("spill under the loss", l))
    for l in ("L5", "L6"):
        ok(K.round_to(s3d[l], 10) != K.round_to(gd[l], 10) and share1(s3s[l]) != share1(gs[l]), ("Ask A S3", l))
    for l in K.LATERALS:
        if l not in ("L5", "L6"):
            ok(abs(s3d[l] - gd[l]) < 1e-6, ("realignment moves only Laterals 5 and 6", l))
    for l in ("L2", "L4", "L6", "L9"):
        ok(share1(s4s[l]) != share1(gs[l]), ("Ask A S4", l))
    for l in ("L3", "L7", "L8"):
        ok(K.round_to(b2[l], 10) != K.round_to(sp[l], 10), ("Ask B S2", l))
    ok(len(A["changes"]) >= 18 and len({c["turnout"][:2] for c in A["changes"]}) == 9, "meter changes on every lateral")
    # S2b: within each meter's own reads, with a new meter's first read counted from zero (a rebuilt meter's carried
    # register cannot be): every figure still off
    units = _replacement_units(target)
    s2bd = _ask_a_new_from_zero(A, units)
    for l in K.LATERALS:
        s2bs = 100.0 * (inflow[l] - s2bd[l]) / inflow[l]
        ok(K.round_to(s2bd[l], 10) != K.round_to(gd[l], 10) and share1(s2bs) != share1(gs[l]), ("Ask A S2b", l))
    # realism of the replacements: a new meter goes in at zero, a rebuilt one with the register it carried out of its
    # last service; the book starts each replacement at or above the register the shop recorded, and the shop's
    # removal register sits just past the old meter's last weekly read
    ok(set(units.values()) == {"New", "Rebuilt"}, ("new and rebuilt replacements", sorted(set(units.values()))))
    for c in A["changes"]:
        u = units[(c["old"], c["new"])]
        ok((c["installation"] == 0.0) == (u == "New"), ("installation register", c["new"], u, c["installation"]))
        first = [v for t, s, v in A["reads"][c["turnout"]] if s == c["new"]][0]
        last = [v for t, s, v in A["reads"][c["turnout"]] if s == c["old"]][-1]
        ok(0.0 <= first - c["installation"] < 200.0, ("first read just past the installation register", c["new"]))
        ok((c["removal"] - last) % 10000.0 < 200.0, ("removal register just past the last read", c["old"]))
    # SF26: a Lateral 5 tail turnout's lateral on a read interval is the lateral that fed it: Lateral 5 through its 15
    # June 2026 read, Lateral 6 after (the operations log's 13 and 15 June entries; the register as it stands carries
    # Lateral 6). The register's lateral all season moves four figures (S3 above); the turnout number's lateral all
    # season leaves Lateral 5 delivering more than its heading put in
    db, reach_after = _ask_a_built(A)
    ok(inflow["L5"] - db["L5"] < 0, "SF26 the turnout number's lateral all season: Lateral 5 delivers more than it took")
    # SF26's convergence: no water ran to the reach while the connector was tied in (13 to 15 June), so the interval
    # ending at each tail meter's 15 June read and the one after it each hold one lateral's water
    for rr in rows[1:]:
        if rr[ix["season"]] == "2026" and rr[ix["status"]] == "Delivered" and rr[ix["turnout"]] in set(K.MOVED):
            ok(rr[ix["set_end"]][:10] < "2026-06-13" or rr[ix["set_start"]][:10] > "2026-06-15",
               ("SF26 no water to the reach during the tie-in", rr[ix["order_no"]]))
    # SF27: each heading's volumes as recorded (the water that passed that heading); the reach's metered water after
    # 15 June moved from Lateral 6's heading to Lateral 5's, with the reach on Lateral 5 all season, moves four figures
    inf27 = dict(inflow)
    inf27["L5"] += reach_after
    inf27["L6"] -= reach_after
    for l in ("L5", "L6"):
        s27 = 100.0 * (inf27[l] - db[l]) / inf27[l]
        ok(K.round_to(db[l], 10) != K.round_to(gd[l], 10) and share1(s27) != share1(gs[l]), ("SF27", l))
    # SF28: the head over a tail weir with flashboards in is the gauge less the crest raised 2 inches a board (the
    # bare crest files every lateral high: Ask B S1 above); the notes' times converge below
    ok(all(K.round_to(b1[l], 10) > K.round_to(sp[l], 10) for l in K.LATERALS), "SF28 the bare crest files high")
    # converging readings on Ask A: the book brackets the season at every turnout (opening reads before 1 February,
    # closing reads after 31 October), and every Lateral 5 tail meter was read on the realignment day, so no read
    # interval straddles it
    ok(all(v[0][0].date() < dt.date(2026, 2, 1) and v[-1][0].date() > dt.date(2026, 10, 31) for v in A["reads"].values()),
       "the meter book brackets the season")
    ok(all(any(t.date() == C.MOVED_FROM for t, _, _ in A["reads"][tid]) for tid in K.MOVED), "realignment reads")
    ok(all(A["lateral"][tid] == "L6" for tid in K.MOVED) and len(K.MOVED) == 14, "the tail reach on Lateral 6")
    # converging readings on Ask B: every flashboard note carries the time the rider set or pulled the board, ahead of
    # that sheet's reading, so the board change is in place at the reading (a change taken from the next day instead
    # moves three laterals)
    notes = 0
    for rr in C.read_csv(os.path.join(target, K.WEIRS))[1:]:
        rem = rr[5]
        if "board" in rem and rem[:2].isdigit():
            notes += 1
            ok(rem[2] == ":" and rem[:5] < rr[3], ("board note before the reading", rr[0], rr[1], rem, rr[3]))
        ok(not ("board" in rem and "inch" in rem and not rem[:2].isdigit()), ("untimed board note", rr[0], rr[1]))
    ok(notes == 24, ("board notes", notes))
    lag = _ask_b_lagged(A)
    moved = [l for l in K.LATERALS if K.round_to(lag[l], 10) != K.round_to(sp[l], 10)]
    ok(len(moved) >= 1, "the next-day reading of a board change is a real fork, closed by the notes' times")
    print("  Ask B with each board change taken from the next day: %s" % ", ".join(
        "%s %s" % (l, "{:,}".format(K.round_to(lag[l], 10))) for l in moved))
    print("  Ask A: deliveries %s" % ", ".join("%s %s" % (l, "{:,}".format(K.round_to(gd[l], 10))) for l in K.LATERALS))
    print("         shares %s" % ", ".join("%s %.1f" % (l, share1(gs[l])) for l in K.LATERALS))
    print("         within-serial lost %s AF" % ", ".join("%s %.0f" % (l, gd[l] - s2d[l]) for l in K.LATERALS))
    print("         S1 by turnout across changes: deliveries %s to %s AF, shares %.0f to %.0f per cent" % (
        "{:,}".format(min(K.round_to(v, 10) for v in s1d.values())),
        "{:,}".format(max(K.round_to(v, 10) for v in s1d.values())), min(s1s.values()), max(s1s.values())))
    print("         S2b new meters counted from zero (%d new, %d rebuilt): %s AF low" % (
        sum(1 for u in units.values() if u == "New"), sum(1 for u in units.values() if u == "Rebuilt"),
        ", ".join("%s %.0f" % (l, gd[l] - s2bd[l]) for l in K.LATERALS)))
    print("         S2b filed: %s" % ", ".join("%s %s and %.1f" % (l, "{:,}".format(K.round_to(s2bd[l], 10)),
                                                               share1(100.0 * (inflow[l] - s2bd[l]) / inflow[l]))
                                              for l in K.LATERALS))
    print("         S3 register's lateral: %s; SF26 turnout number's lateral: Lateral 5 %s against %s put in; SF27 "
          "headings moved with the reach: %s" % (
              ", ".join("%s %s and %.1f" % (l, "{:,}".format(K.round_to(s3d[l], 10)), share1(s3s[l]))
                        for l in ("L5", "L6")),
              "{:,}".format(K.round_to(db["L5"], 10)), "{:,}".format(K.round_to(inflow["L5"], 10)),
              ", ".join("%s %s and %.1f" % (l, "{:,}".format(K.round_to(db[l], 10)),
                                           share1(100.0 * (inf27[l] - db[l]) / inf27[l])) for l in ("L5", "L6"))))
    print("  Ask B: spill %s" % ", ".join("%s %s" % (l, "{:,}".format(K.round_to(sp[l], 10))) for l in K.LATERALS))
    print("         bare crest %s" % ", ".join("%s %s" % (l, "{:,}".format(K.round_to(b1[l], 10))) for l in K.LATERALS))

    # ------------------------------------------------------------------------------------------ separation line
    ask_files = [K.METER_BOOK, K.SHOP_LOG, K.HEADINGS, K.WEIRS, K.STRUCTURES]
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
        d2, s2_, _ = C.ask_a(A2)
        ok(all(abs(d2[l] - gd[l]) < 1e-9 and abs(C.ask_b(A2)[l] - sp[l]) < 1e-9 for l in K.LATERALS),
           "asks unchanged without the distractors")
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    big = max(len(C.read_csv(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, ("a 25,000-row file", big))
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "distractors")
        ok(all("distractor" not in f.lower() for f in files), "no file named distractor")

    # ------------------------------------------------------------------------------------------ hygiene and realism
    text_ext = (".csv", ".txt")
    names_ok = set(K.PEOPLE.values())
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
        for w in ("antecedent", "field capacity on 1 February", "dry winter", "soil moisture", "carry-over",
                  "starting depletion", "initial depletion"):
            ok(w.lower() not in txt.lower(), ("stump word", f, w))
    for f in os.listdir(golden):
        txt = _text_of(os.path.join(golden, f))
        ok("\u2014" not in txt and "\u2013" not in txt, ("dash in golden", f))
        ok("matplotlib" not in txt.lower() and "openpyxl" not in txt.lower(), ("golden signature", f))
    # dates: nothing on record after the extract
    for rr in C.read_csv(os.path.join(target, K.ORDERS))[1:]:
        ok(rr[ix["set_end"]][:10] <= "2026-10-31" and rr[ix["entered_at"]][:10] <= "2026-10-31", "order dates")
    ok(max(M.wx) == K.WEATHER_END, "weather through 31 January 2027")
    for f in files:
        ds = _dates_in(os.path.join(target, f))
        ok(not ds or max(ds) <= K.EXTRACT, ("a date after the extract", f, max(ds) if ds else None))
    # the working-files note names every other file in the folder
    readme = open(os.path.join(target, K.README), encoding="utf-8").read()
    ok(all(f in readme for f in files if f != K.README), "the working-files note lists every file")
    # no identical heading totals, no round asks
    ok(len({round(inflow[l], 2) for l in K.LATERALS}) == 9, "distinct heading totals")
    ok(all(abs(gd[l] - round(gd[l])) > 1e-6 for l in K.LATERALS), "deliveries not whole numbers before rounding")
    # the request clerk's remarks: a revision's remark says what the grower revised, an irrigation system remark only
    # where the method differs from 2026, a withdrawal's reason fits the crop, and no one remark dominates
    method26 = {rr[0]: rr[5] for rr in C.read_csv(os.path.join(target, K.CROP_REPORT))[1:]}
    versions = {}
    for q in M.requests:
        versions.setdefault(q["Request no."], []).append(q)
    sys_words = ("method", "changed to", "converted to", "system", "border", "sprinklers pulled")
    for no, vs in versions.items():
        vs = sorted(vs, key=lambda q: q["Version"])
        last = vs[-1]
        rem = (last["Remarks"] or "").lower()
        if len(vs) == 2:
            changed = vs[0]["Irrigation method"] != last["Irrigation method"]
            ok(any(w in rem for w in sys_words) == changed, ("revision remark", no, rem))
        elif last["Status"] == "Accepted" and any(w in rem for w in sys_words):
            ok(method26[last["Field"]] != last["Irrigation method"], ("system remark", no, rem))
        if last["Status"] == "Withdrawn":
            ok(rem != "", ("withdrawal without a reason", no))
        if "orchard" in rem or "trees" in rem:
            ok(last["Crop code"] in ("ALM", "PIS", "WAL", "CIT"), ("orchard remark", no, last["Crop code"]))
        if "vine" in rem:
            ok(last["Crop code"] == "GRW", ("vineyard remark", no, last["Crop code"]))
        if "fallowing" in rem or "out of production" in rem:
            ok(last["Crop code"] in ("ALF", "PAS"), ("fallowing remark", no, last["Crop code"]))
    remarks = [q["Remarks"] for q in M.requests if q["Remarks"]]
    top = max(remarks.count(x) for x in set(remarks))
    ok(len(set(remarks)) >= 12 and top <= 0.35 * len(remarks), ("request remarks", len(set(remarks)), top, len(remarks)))
    # the operations log: entries in time order, each written when it happened (every heading outage it logs ends on
    # the last of the headings' estimated days, the logger's totals resuming the next day)
    log = _ops_log(target)
    ok(log == sorted(log, key=lambda e: (e[0], e[1])) and len({e[0] for e in log}) >= 30, "operations log")
    # an entry reporting the day's meter reads is logged after the last of them
    last_read = {}
    for v in A["reads"].values():
        for t_, s_, r_ in v:
            last_read[t_.date()] = max(last_read.get(t_.date(), t_), t_)
    for day, time, text, by in log:
        if "read today" in text or "reads taken" in text:
            hh, mm = (int(x) for x in time.split(":"))
            ok(dt.datetime(day.year, day.month, day.day, hh, mm) > last_read[day], ("log entry before the reads", day))
    e_days = {}
    for d_, l_, v_, q_ in A["headings"]:
        if q_ == "E":
            e_days.setdefault(l_, []).append(d_)
    resumed = {}
    for day, time, text, by in log:
        m = re.search(r"Lateral (\d) .*totals (?:again from (\d{1,2}) (\w+)|good from midnight)", text)
        if m:
            when = (dt.datetime.strptime("%s %s 2026" % (m.group(2), m.group(3)), "%d %B %Y").date() if m.group(2)
                    else day + dt.timedelta(days=1))
            resumed["L" + m.group(1)] = when
    ok(sorted(resumed) == sorted(e_days) and all(resumed[l] == max(e_days[l]) + dt.timedelta(days=1) for l in e_days),
       ("heading outages in the log", resumed))
    print("checks.py: %d assertions passed" % N[0])
    ok(N[0] >= 40, "forty or more assertions")
    return lad


# ---------------------------------------------------------------------------------------------------- helpers

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


def _order_rain_first(M):
    """SF8's second alternative: each day's rain taken off first, its excess drained, then the day's ET added."""
    class RainFirst(C.Model):
        def day(self, D, d, cap=True):
            e, rn = self.wx[d]
            D = np.maximum(D - rn, 0.0) + self.kc[:, d.month - 1] * e
            return np.minimum(D, self.taw) if cap else D
    M2 = RainFirst(M.fields, M.wx, M.T, last_delivery=M.last_delivery, turnout_last=M.turnout_last,
                   cancelled_last=M.cancelled_last)
    return variant_order(M2, M2.start_golden())


def _carry_from_set_day(M, upto=K.WEATHER_END):
    """SF25's alternative: each field's 31 January depletion with the day of its last 2026 set counted after the set."""
    anchors = [M.last_delivery[i] for i in M.ids]
    D = np.zeros(M.n)
    a_ord = np.array([a.toordinal() for a in anchors])
    for d in K.daterange(min(anchors), upto):
        nd = M.day(D, d)
        D = np.where(d.toordinal() >= a_ord, nd, D)
    return D


def _replacement_units(target):
    """(meter removed, meter installed) -> New or Rebuilt, from the shop log's 2026 changes."""
    import openpyxl
    rows = list(openpyxl.load_workbook(os.path.join(target, K.SHOP_LOG), data_only=True)["2026 changes"]
                .iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
    col = list(rows[hi]).index("New or rebuilt")
    return {(r[3], r[5]): r[col] for r in rows[hi + 1:] if r and r[0] is not None}


def _lateral_of(A, tid, t1):
    reg_lat, built = A["lateral"][tid], "L%d" % int(tid[:2])
    return built if (built != reg_lat and t1.date() <= C.MOVED_FROM) else reg_lat


def _ask_a_new_from_zero(A, units):
    """Ask A deliveries within each meter's own reads, plus each new meter's first read taken from zero."""
    deliv = {l: 0.0 for l in K.LATERALS}
    for tid, rd in A["reads"].items():
        for t1, v in C.turnout_intervals(A, tid, "serial"):
            deliv[_lateral_of(A, tid, t1)] += v
        for c in A["changes"]:
            if c["turnout"] == tid and units[(c["old"], c["new"])] == "New":
                t1, v = next((t, v) for t, s, v in rd if s == c["new"])
                deliv[_lateral_of(A, tid, t1)] += v
    return deliv


def _ask_a_built(A):
    """Ask A deliveries chained, every turnout on the lateral its number names all season; and the Lateral 5 tail
    reach's metered water after its 15 June read."""
    deliv = {l: 0.0 for l in K.LATERALS}
    after = 0.0
    for tid in A["reads"]:
        for t1, v in C.turnout_intervals(A, tid, "chain"):
            deliv["L%d" % int(tid[:2])] += v
            if tid in K.MOVED and t1.date() > C.MOVED_FROM:
                after += v
    return deliv, after


def _ops_log(target):
    """The operations log's rows as (date, time, entry, initials)."""
    import docx
    t = docx.Document(os.path.join(target, K.OPS_LOG)).tables[0]
    out = []
    for row in t.rows[1:]:
        c = [x.text for x in row.cells]
        out.append((dt.date.fromisoformat(c[0]), c[1], c[2], c[3]))
    return out


def _ask_b_lagged(A):
    """Ask B with each board change noted on a sheet taken as in place only from the next day."""
    spill = {}
    for lat in K.LATERALS:
        L, crest, C_ = A["weir"][lat]
        bc = C.board_counts(A, lat)
        prev, p = {}, 0
        for d in sorted(bc):
            prev[d] = p
            p = bc[d]
        rd = {d: g for d, g, _ in A["sheets"][lat]}
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
    """Every calendar date written in a CSV or text file (ISO or month/day/year) or held in a workbook cell."""
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


def _order_shuffled(target):
    import openpyxl
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        rows = C.read_csv(os.path.join(tmp, K.ORDERS))
        perm = np.random.default_rng(138).permutation(len(rows) - 1)
        with open(os.path.join(tmp, K.ORDERS), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(rows[0])
            w.writerows(rows[1 + i] for i in perm)
        wb = openpyxl.load_workbook(os.path.join(tmp, K.REQUESTS))
        ws = wb["Requests"]
        vals = [list(r) for r in ws.iter_rows(values_only=True)]
        hi = next(i for i, r in enumerate(vals) if r and r[0] == "Request no.")
        n = 0
        while hi + 1 + n < len(vals) and vals[hi + 1 + n][0] is not None:
            n += 1
        data = vals[hi + 1:hi + 1 + n][::-1]
        for k, r in enumerate(data):
            for j, v in enumerate(r):
                ws.cell(row=hi + 2 + k, column=j + 1, value=v)
        wb.save(os.path.join(tmp, K.REQUESTS))
        M2 = C.load(tmp)
        return variant_order(M2, M2.start_golden())
    finally:
        shutil.rmtree(tmp)


def _order_applied_depth(M, target):
    """The 2026 season from a full root zone on 1 February, each delivered set's volume at the turnout times the
    application efficiency taken off the depletion on the set's last day, then the winter to 31 January 2027."""
    rows = C.read_csv(os.path.join(target, K.ORDERS))
    ix = {c: rows[0].index(c) for c in rows[0]}
    idx = {f: i for i, f in enumerate(M.ids)}
    applied = {}
    for rr in rows[1:]:
        if rr[ix["season"]] != "2026" or rr[ix["status"]] != "Delivered" or rr[ix["field_id"]] not in idx:
            continue
        i = idx[rr[ix["field_id"]]]
        a = dt.datetime.fromisoformat(rr[ix["set_start"]])
        b = dt.datetime.fromisoformat(rr[ix["set_end"]])
        af = float(rr[ix["ordered_cfs"]]) * (b - a).total_seconds() / K.CUFT_PER_AF
        applied.setdefault(b.date(), np.zeros(M.n))[i] += af * 12.0 / M.acres[i] * M.ea[i]
    D = np.zeros(M.n)
    for d in K.daterange(dt.date(2026, 2, 1), K.WEATHER_END):
        D = M.day(D, d)
        if d in applied:
            D = np.maximum(D - applied[d], 0.0)
    return variant_order(M, lambda y: D)


def _order_on_fields(M, fields, allow_dupes=False):
    M2 = C.Model(fields, M.wx, M.T, last_delivery=M.last_delivery, turnout_last=M.turnout_last,
                 cancelled_last=M.cancelled_last)
    if allow_dupes:
        M2.ids = [f["id"] for f in fields]
    return variant_order(M2, M2.start_golden())


def _order_on_tables(M, T):
    M2 = C.Model(M.fields, M.wx, T, last_delivery=M.last_delivery, turnout_last=M.turnout_last,
                 cancelled_last=M.cancelled_last)
    return variant_order(M2, M2.start_golden())


def _order_on_weather(M, wx):
    M2 = C.Model(M.fields, wx, M.T, last_delivery=M.last_delivery, turnout_last=M.turnout_last,
                 cancelled_last=M.cancelled_last)
    return variant_order(M2, M2.start_golden())


def _order_test_before_rain(M, start):
    req, mon = {}, {}
    for y in K.REPLAY_YEARS:
        Dd = start(y).copy()
        m9 = np.zeros((9, M.n))
        for d in K.season_days(y):
            e, rn = M.wx[d]
            Dd = Dd + M.kc[:, d.month - 1] * e
            irr = Dd >= M.raw
            m9[d.month - 2] += np.where(irr, np.minimum(Dd, M.taw), 0.0)
            Dd = np.where(irr, 0.0, Dd)
            Dd = np.minimum(np.maximum(Dd - rn, 0.0), M.taw)
        farm = m9 / M.ea * M.acres / 12.0
        tot = 0.0
        for k in range(9):
            tot += (np.bincount(M.lat, weights=farm[k], minlength=9) / (1 - M.loss)).sum() / (1 - M.main)
        req[y] = tot
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
