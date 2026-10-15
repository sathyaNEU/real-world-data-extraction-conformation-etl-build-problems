"""task138 assertions: the input gates, every rung of the ladder and its separation, the soil moisture stations (the
efficiency they show, their misfit under every rival, their blind 31 January readings, the golden method's variants and
one standard error), the three-rules block on the clean truth (R1 to R3c), every semantic fork row (SF1 to SF47), the
graded figures' distances to their rounding edges, the four lateral asks with their stops and devices (each figure as
shipped at round 2), the separation line between the call and the asks, the distractors' deletion test, and the realism
and hygiene sweeps. Run by build.py on every build; prints the ladder and the measured figures the design note
quotes."""
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
K_READ_VAR = 0.05 ** 2      # a station's reading noise (world.READ_NOISE_IN), squared


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
    g = lad["G"]
    print("ladder (24th smallest of thirty, order, setting year):")
    for k, v in sorted(lad.items(), key=lambda kv: kv[1]["req"]):
        print("  %-4s %-86s %12s  %7s  %d  %+.2f%%" % (k, v["label"][:86], "{:,.2f}".format(v["req"]),
                                                   af(v["order"]), v["year"], 100 * (v["req"] / g["req"] - 1)))

    # ------------------------------------------------------------------------------------------ the golden call
    ok(g["order"] == 212000 and g["year"] == 2012, ("golden", g["order"], g["year"]))
    lo = g["req"] - (g["order"] - K.ORDER_STEP)
    ok(400 <= lo <= 600, ("24th smallest mid-bin in its thousand", lo))
    r = g["ranked"]
    ok(r[23][1] - r[22][1] >= 1000 and r[24][1] - r[23][1] >= 1000, ("SF23 neighbours", r[22][1], r[23][1], r[24][1]))
    print("  golden 24th %.2f (%.2f above %s, %.2f under the order), neighbours %d %.0f and %d %.0f" % (
        g["req"], lo, af(g["order"] - K.ORDER_STEP), g["order"] - g["req"], r[22][0], r[22][1], r[24][0], r[24][1]))

    # ------------------------------------------------------------------------------------------ the ladder
    T4 = lad["T4"]
    ok(T4["order"] == 215000 and T4["year"] == 2012, ("default path", T4["order"], T4["year"]))
    expect = {"R0": 196000, "R2b": 197000, "R1": 199000, "R2": 199000, "O3": 206000, "R3": 209000, "R4g": 210000,
              "R3c": 211000, "R2d": 211000, "KC": 211000, "O2": 213000, "O1": 214000, "PT": 214000, "AB": 215000,
              "P1": 215000, "T4": 215000, "RG": 216000, "MI": 218000, "HT": 218000}
    for k, v in expect.items():
        ok(lad[k]["order"] == v, ("rung order", k, lad[k]["order"], v))
        ok(abs(lad[k]["order"] - g["order"]) >= K.ORDER_STEP, ("rung a full bin from the order", k))
    for k, floor in (("R0", 0.07), ("R2b", 0.065), ("R1", 0.06), ("R2", 0.06), ("O3", 0.025), ("R3", 0.014),
                     ("R4g", 0.010), ("R3c", 0.005), ("R2d", 0.005), ("KC", 0.002)):
        ok(lad[k]["req"] / g["req"] - 1 <= -floor, ("rung under the golden by its floor", k, floor))
    for k, floor in (("O2", 0.003), ("O1", 0.010), ("PT", 0.010), ("AB", 0.011), ("P1", 0.013), ("T4", 0.013),
                     ("RG", 0.018), ("MI", 0.025), ("HT", 0.025)):
        ok(lad[k]["req"] / g["req"] - 1 >= floor, ("rung over the golden by its floor", k, floor))
    for k in ("R0", "R1", "R2", "R2b"):
        ok(lad[k]["year"] != g["year"], ("rung names another setting year", k))
    D, D4 = M.D_golden, M.D_t4
    D3 = M.start_last_set()(0)
    meth = np.array([f["method"] for f in M.fields])
    crop = np.array([f["crop"] for f in M.fields])
    held = meth != "Border"
    aw = lambda X: float(X @ M.acres / M.acres.sum())
    print("  31 January 2027: golden acre-weighted %.3f in, %d of %d fields at or past allowable depletion; default path "
          "(Table 4) %.3f in, %d; last set as a refill %.3f in" % (aw(D), int((D >= M.raw).sum()), M.n, aw(D4),
                                                                  int((D4 >= M.raw).sum()), aw(D3)))

    # ------------------------------------------------------------------------------------------ the stations
    S = M.stations
    hs = [st for st in S if st["method"] != "Border"]
    ok(len(S) == 11 and len(hs) == 9 and [sum(1 for st in S if st["method"] == m) for m in K.METHODS] == [4, 3, 2, 2],
       ("SF36 the network's stations by method", len(S)))
    ok(len({st["field"] for st in S}) == 11 and all(st["field"] in M.index for st in S), "SF36 one 2027 field each")
    apns = [g_["apn"].replace("-", "") for g_ in M.register.values()]
    ok(len(apns) == len(set(apns)), "SF36 every APN in the register names one field")
    per, by = M.ea_station, M.ea_by
    ok(all(per[st["station"]] > M.T["ea"][st["method"]] + 0.02 for st in hs), ("every station above Table 4", per))
    sse_e = sum(M.station_sse(st, per[st["station"]]) for st in hs)
    sse_4 = sum(M.station_sse(st, M.T["ea"][st["method"]]) for st in hs)
    sse_1 = sum(M.station_sse(st, 1.0) for st in hs)
    kf, sse_k = M.kc_factor()
    nread = sum(len(st["reads"]) for st in hs)
    ok(sse_4 >= 40 * sse_e and sse_1 >= 10 * sse_e, ("the season rejects Table 4 and all-of-it", sse_e, sse_4, sse_1))
    ok(sse_k >= 2 * sse_e and kf < 0.99, ("SF44 a crop coefficient factor fits worse", kf, sse_k, sse_e))
    ok(abs(sse_e / nread - K_READ_VAR) < 0.0008, ("the misfit at the stations' efficiency is reading noise",
                                                 sse_e / nread))
    # January: every station's 31 January state is the same at Table 4 and at every efficiency up to its own (the dry
    # autumn and winter took each to the bottom of its root zone), and its reading sits on both runs
    jan = M.station_jan()
    for st in S:
        t4 = M.T["ea"][st["method"]]
        top = per.get(st["station"], t4) + 0.02
        v = [M.station_path(st, e)[K.WEATHER_END] for e in np.linspace(t4, top, 7)]
        ok(max(v) - min(v) < 1e-9, ("SF46 the station's 31 January state is blind to the efficiency", st["station"]))
        i = M.index[st["field"]]
        ok(abs(D4[i] - jan[i]) < 0.15 and abs(D[i] - jan[i]) < 0.15, ("SF46 January reading on both runs", st["station"]))
    off = [round(float(D4[M.index[st["field"]]] - jan[M.index[st["field"]]]), 3) for st in S]
    # why: each held station's two runs meet at the bottom of its root zone after its last set (the almond and vine
    # blocks, last watered in September, in October; the shallow pastures, watered to late October, by early January);
    # a border station's last set runs past field capacity at Table 4's efficiency or any above it, so its runs meet the
    # day after that set
    meet = {}
    for st in S:
        i = M.index[st["field"]]
        p4 = M.station_path(st, M.T["ea"][st["method"]])
        po = M.station_path(st, per[st["station"]] if st["method"] != "Border" else 0.90)
        last = M.last_delivery[st["field"]]
        d0 = next(d for d in sorted(po) if d > last and abs(po[d] - p4[d]) < 1e-9)
        ok(all(abs(po[d] - p4[d]) < 1e-9 for d in po if d >= d0), ("the runs stay together", st["station"]))
        if st["method"] == "Border":
            ok(d0 == last + dt.timedelta(days=1), ("a border station's runs meet the day after its last set", st["station"]))
        else:
            ok(abs(po[d0] - M.taw[i]) < 1e-9, ("a held station's runs meet at the bottom of its root zone", st["station"]))
        meet[st["station"]] = (st["crop"], st["method"], last, d0)
    tree = [v[3] for v in meet.values() if v[0] in ("ALM", "GRW")]
    past = [v[3] for v in meet.values() if v[0] == "PAS" and v[1] != "Border"]
    ok(all(v[2].month == 9 for v in meet.values() if v[0] in ("ALM", "GRW")) and
       all(v[2].month == 10 for v in meet.values() if v[0] == "PAS" and v[1] != "Border"), "the stations' last sets")
    ok(max(tree) <= dt.date(2026, 10, 31) and min(past) >= dt.date(2026, 12, 1) and max(past) <= K.WEATHER_END,
       ("when the held stations' runs meet", min(tree), max(tree), min(past), max(past)))
    lastat = [(M.last_delivery.get(f["id"]) or dt.date(1900, 1, 1)) for f in M.fields if f["crop"] in ("ALM", "GRW")]
    ok(all(d.year == 2026 and d.month == 9 for d in lastat), "every almond and vine field's last 2026 set in September")
    print("  held stations' runs meet at the bottom of the root zone: almonds and vines %s to %s, sprinkler pastures %s "
          "and %s; border stations the day after their last set" % (min(tree), max(tree), min(past), max(past)))
    share = {}
    for c in ("PIS", "CIT", "WAL", "ALM", "GRW", "PAS", "ALF"):
        m = crop == c
        share[c] = (round(float((D4[m] / M.taw[m]).mean()), 2), round(float((D[m] / M.taw[m]).mean()), 2))
    ok(all(share[c][0] - share[c][1] >= 0.10 for c in ("PIS", "CIT", "WAL")) and
       all(share[c][0] - share[c][1] <= 0.05 for c in ("ALM", "GRW", "PAS", "ALF")),
       ("the late crops' 31 January share of total available water moves, the stations' crops' barely", share))
    print("  31 January mean share of total available water, Table 4 run and golden: %s" % ", ".join(
        "%s %.2f %.2f" % (c, a, b) for c, (a, b) in share.items()))
    # the write-up's rival clauses: every drip, micro-sprinkler and sprinkler station reads short of its full point after
    # its last set (no refill), and every station is deep in its root zone on 31 January (no full start)
    for st in S:
        i = M.index[st["field"]]
        after = st["full"] - st["reads"][M.last_delivery[st["field"]]]
        ok(st["method"] == "Border" or after >= 0.2, ("a held station short of full after its last set", st["station"], after))
        ok(jan[i] >= 0.5 * M.taw[i], ("a station deep in its root zone on 31 January", st["station"], jan[i]))
    # the drip stations in two crops agree (the efficiency is the method's)
    alm = [per[st["station"]] for st in hs if st["method"] == "Drip" and st["crop"] == "ALM"]
    grw = [per[st["station"]] for st in hs if st["method"] == "Drip" and st["crop"] == "GRW"]
    ok(len(alm) == 2 and len(grw) == 2 and abs(np.mean(alm) - np.mean(grw)) < 0.01, ("SF41 drip almonds and vines",
                                                                                   alm, grw))
    print("  stations: efficiency %s; by method %s; misfit at their efficiency %.1f, at Table 4 %.1f, all of it %.1f, "
          "crop coefficient factor %.3f %.1f (%d readings); January offset from the Table 4 run %s" % (
              {k: round(v, 4) for k, v in per.items()}, {k: round(v, 4) for k, v in by.items()}, sse_e, sse_4, sse_1, kf,
              sse_k, nread, off))
    # the golden method's variants: every defensible way of fitting the stations files the same order, mid-bin
    VAR = {}
    _, b_med = M.station_efficiency(how="median")
    VAR["median"] = b_med
    fac = float(np.mean([per[st["station"]] / M.T["ea"][st["method"]] for st in hs]))
    VAR["one factor"] = {m: M.T["ea"][m] * fac for m in by}
    VAR["pooled least squares"] = _pooled(M)
    for lab, kw in (("February to October", dict(days=(dt.date(2026, 1, 28), dt.date(2026, 10, 31)))),
                    ("May to October", dict(days=(dt.date(2026, 5, 1), dt.date(2026, 10, 31)))),
                    ("UTC date as the day", dict(shift=1)), ("a day early", dict(shift=-1))):
        VAR[lab] = M.station_efficiency(**kw)[1]
    w_ac = {st["station"]: M.acres[M.index[st["field"]]] for st in hs}
    VAR["acre-weighted"] = {m: float(sum(per[st["station"]] * w_ac[st["station"]] for st in hs if st["method"] == m) /
                                     sum(w_ac[st["station"]] for st in hs if st["method"] == m)) for m in by}
    out = {}
    for lab, b in VAR.items():
        Dv = M.hindcast(M.water26(), ea=M.ea_from(b))
        out[lab] = variant_order(M, lambda y, Dv=Dv: Dv)
    Db = M.hindcast(M.water26(), ea=M.ea_from({m: M.T["ea"][m] * fac for m in by}, border=0.70 * fac))
    out["one factor, border too"] = variant_order(M, lambda y: Db)
    Ds = D.copy()
    for i, v in jan.items():
        Ds[i] = v
    out["stations' fields at their readings"] = variant_order(M, lambda y: Ds)
    for lab, o in out.items():
        ok(o["order"] == g["order"] and o["year"] == g["year"] and 250 <= o["req"] - (g["order"] - K.ORDER_STEP) <= 750,
           ("SF40 the golden method's variants file the order mid-bin", lab, o["req"]))
    SEEN = {"SF40": {k: round(v["req"] - g["req"], 1) for k, v in out.items()}}
    # one standard error of each method's efficiency (the stations' spread) moves no order
    for sgn in (-1, 1):
        b_ = {}
        for m in by:
            v = [per[st["station"]] for st in hs if st["method"] == m]
            b_[m] = by[m] + sgn * float(np.std(v, ddof=1)) / len(v) ** 0.5
        Dv = M.hindcast(M.water26(), ea=M.ea_from(b_))
        o = variant_order(M, lambda y, Dv=Dv: Dv)
        ok(o["order"] == g["order"], ("one standard error of the stations' efficiency", sgn, o["req"]))
        SEEN.setdefault("one standard error", []).append(round(o["req"] - g["req"], 1))
    # SF43: a border set runs past field capacity, so any efficiency from Table 4's up leaves every border field's 31
    # January state where it is; the border stations' own fit (about Table 4's) files the same order
    bord = ~held
    for eb in (0.70, 0.80, 0.90, 1.00):
        Dx = M.hindcast(M.water26(), ea=M.ea_from(by, border=eb))
        ok(float(np.abs(Dx[bord] - D[bord]).max()) < 1e-9, ("SF43 border efficiency", eb))
    e_b = [M.calibrate_station(st) for st in S if st["method"] == "Border"]
    ok(all(abs(x - 0.70) < 0.01 for x in e_b), ("SF43 the border stations fit about Table 4", e_b))
    Dx = M.hindcast(M.water26(), ea=M.ea_from(by, border=float(np.mean(e_b))))
    o = variant_order(M, lambda y: Dx)
    ok(o["order"] == g["order"] and abs(o["req"] - g["req"]) < 200, ("SF43 border at its stations' fit", o["req"]))
    SEEN["SF43"] = (round(float(np.mean(e_b)), 4), round(o["req"] - g["req"], 1))

    # ------------------------------------------------------------------------------------------ the record's season
    water = M.water26()
    lastfull, at_last = _season_path(M, water, M.ea_record)
    short = at_last[held]
    ok(int(held.sum()) == 501 and int((short < 1e-9).sum()) <= 3, ("held fields short after their last set",
                                                                     int(held.sum()), int((short < 1e-9).sum())))
    ok(float(at_last[~held].max()) < 1e-9, "every border field full after its last set")
    late = np.array([lastfull[i] > dt.date(2026, 6, 30).toordinal() for i in range(M.n)])
    print("  2026 record at the stations' efficiency: %d of %d held fields short of field capacity after their last set "
          "(acre-weighted %.2f in); %d held fields full at some point after June; every border field full after its "
          "last set" % (int((short > 1e-9).sum()), int(held.sum()), float((short * M.acres[held]).sum() /
                                                                          M.acres[held].sum()), int((late & held).sum())))
    # the late-season crops carry the difference between Table 4 and the stations' efficiency on 31 January; the
    # stations' crops, near the bottom of their root zones by then, barely
    diff = D4 - D
    lates = np.isin(crop, ["PIS", "CIT", "WAL"]) | ((crop == "ALF") & held)
    ok(float((diff * M.acres)[lates].sum()) > 3 * float((diff * M.acres)[~lates].sum()),
       "the late crops carry the Table 4 run's excess depletion")
    print("  Table 4 run less golden on 31 January: pistachios, citrus, walnuts and sprinkler alfalfa %.0f acre-inches, "
          "the rest %.0f, of %.0f; acre-weighted %.3f in, %.3f on the held fields" % (
              float((diff * M.acres)[lates].sum()), float((diff * M.acres)[~lates].sum()), float(diff @ M.acres),
              aw(diff), float(diff[held] @ M.acres[held] / M.acres[held].sum())))

    # ------------------------------------------------------------------------------------------ the three rules
    files = sorted(os.listdir(target))
    heads = " ".join(open(os.path.join(target, f), encoding="utf-8").readline().lower() for f in files
                     if f.endswith(".csv"))
    ok(not re.search(r"depletion|soil_water|moisture|deficit|requirement|efficiency", heads),
       "R1: a shipped column holds the deciding quantity")
    orders_head = C.read_csv(os.path.join(target, K.ORDERS))[0]
    ok({"ordered_cfs", "set_start", "set_end", "status", "field_id"} <= set(orders_head),
       "R1: the orders ship at set grain with each set's flow and times")
    ok(len(M.wx) == (K.WEATHER_END - K.WEATHER_START).days + 1, "R1: the daily weather ships whole")
    ok(len(S) == 11 and min(len(st["reads"]) for st in S) >= 380, "R1: the stations ship their daily readings")
    if W is not None:
        T = _truth(W)
        # R2: the mess on the call's path (two stations spliced, units and missing days; revised and withdrawn requests;
        # former field ids; cancelled sets; turnout ids written three ways; the stations keyed by APN, stamped in UTC,
        # with logger gaps), read by the filed rules and the dictionary, gives back the world's own fields, weather,
        # 2026 sets and station readings
        ok(sorted(M.ids) == sorted(T["ids"]), "R2: the 2027 fields read from the pack are the world's")
        ok(all(abs(M.acres[i] - T["acres"][fid]) < 0.006 and M.fields[i]["crop"] == T["crop"][fid]
               and M.fields[i]["method"] == T["method"][fid] for i, fid in enumerate(M.ids)),
           "R2: crops, methods and acres read from the requests are the world's")
        ok(max(abs(M.wx[d][0] - W.wx[d][0]) + abs(M.wx[d][1] - W.wx[d][1]) for d in M.wx) < 1e-9,
           "R2: the spliced record read from the pack is the District's record")
        ids = set(M.ids)
        rec_w = {(a, b, round(cfs, 1)) for fid, a, b, cfs, s in M.record if s == "Delivered" and fid in ids}
        ok(rec_w == T["sets26"], "R2: the 2026 delivered sets read from the orders are the world's")
        wst = {x["station"]: x for x in W.stations}
        for st in S:
            x = wst[st["station"]]
            ok(st["field"] == x["field"] and abs(st["full"] - x["full"]) < 1e-9, ("R2: a station's field and full point",
                                                                                 st["station"]))
            wr = {q["day"]: q["profile"] for q in W.station_reads if q["station"] == st["station"]}
            ok(wr == st["reads"], ("R2: a station's readings by the day each ends", st["station"]))
        # R3a: the easy route on the clean truth (the world's own fields, weather, sets and stations' true state), every
        # filed rule applied, files the default path's wrong answer
        t3 = _truth_order(T, M, "table 4")
        ok(t3["order"] == T4["order"] and t3["year"] == T4["year"], ("R3a: the default path on the clean truth",
                                                                    t3["order"]))
        # R3b: the same route with only the decisive step changed (the record's efficiency fitted on the stations'
        # season, here on the stations' readings without their reading noise)
        t4, eb = _truth_order(T, M, "stations")
        ok(t4["order"] == g["order"] and t4["year"] == g["year"], ("R3b: the stations' efficiency on the clean truth",
                                                                  t4["order"], t4["req"]))
        # the fields as they are: the golden start sits on them, the Table 4 run and the last set as a refill do not
        true31 = np.array([W.state_path[i][K.WEATHER_END] for i in M.ids])
        aws = lambda X: float(np.abs(X - true31) @ M.acres) / M.acres.sum()
        e_g, e_4, e_3, e_0 = aws(D), aws(D4), aws(D3), aws(np.zeros(M.n))
        ok(e_g < 0.10 and e_4 > 5 * e_g and e_3 > 5 * e_g and e_0 > 3.0, ("SF34 the fields as they are", e_g, e_4, e_3,
                                                                          e_0))
        # SF35: the estimators of the filed state separate on the clean truth by a full order and more
        ok(t3["order"] - t4["order"] >= 2 * K.ORDER_STEP, ("SF35 the two estimators on the clean truth", t3["order"],
                                                           t4["order"]))
        print("  three rules on the clean truth: default path (Table 4) %s, the stations' efficiency %s (%s); acre-weighted "
              "miss of the fields as they are: golden %.3f in, Table 4 %.3f, last set %.3f, full %.3f" % (
                  af(t3["order"]), af(t4["order"]), {k: round(v, 4) for k, v in eb.items()}, e_g, e_4, e_3, e_0))
    # R3c: nothing planted
    ok(not any(w in f.lower() for f in files for w in ("memo", "draft", "briefing", "estimate")),
       "R3c: a memo, draft, briefing or estimate ships")
    docs_txt = " ".join(_text_of(os.path.join(target, f)) for f in files if f.endswith((".pdf", ".docx", ".txt")))
    stated = sorted(set(re.findall(r"\b(\d{3},\d{3}) acre-feet\b", docs_txt)))
    ok(stated == ["241,000"], ("R3c: a document states a requirement or an order", stated))
    for w in ("field capacity at", "start state", "starting depletion", "initial depletion", "initial condition",
              "initial state", "antecedent", "deficit irrigation", "regulated deficit", "working deficit", "carry-over",
              "carryover", "calibrat"):
        ok(w not in docs_txt.lower(), ("R3c: a document names the start or the method", w))
    st_txt = _text_of(os.path.join(target, K.STATIONS)).lower()
    for w in (r"efficien", r"calibrat", r"table 4", r"\border\b", r"requirement", r"deficit", r"depletion"):
        ok(not re.search(w, st_txt), ("R3c: the stations' export names the method", w))

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
    lastm = [M.last_delivery[f["id"]].month for f in M.fields]
    print("  closest approach of a replay day's depletion to an allowable depletion: %.2e in; October 2026 to January "
          "2027 rain %.2f in (next driest %.2f, median of %d winters %.2f); last 2026 sets in September %d, October %d"
          % (gap, wint[2026], sorted(wint.values())[1], len(wint), float(np.median(list(wint.values()))),
             lastm.count(9), lastm.count(10)))

    # ------------------------------------------------------------------------------------------ the fork table
    rows = C.read_csv(os.path.join(target, K.ORDERS))
    head = rows[0]
    ix = {c: head.index(c) for c in head}
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
    # the 24th rounded to the nearest thousand happens to give the same thousand (the 24th sits above its half-thousand),
    # and WOP 2.3's smallest thousand that would have covered it is the order
    ok(K.round_to(vals[23], K.ORDER_STEP) == g["order"] and K.ceil_to(vals[23], K.ORDER_STEP) == g["order"],
       "SF2 the 24th rounded to the nearest thousand")
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
    # SF6: station 39 throughout; the yard from its first day; missing yard days as zero (the stations fitted on each)
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
    st0 = M.start_golden()
    sf8 = _order_test_before_rain(M, st0)
    sf8b = _order_rain_first(M, st0)
    ok(sf8["order"] != g["order"] and sf8b["order"] == g["order"], ("SF8", sf8["order"], sf8b["order"]))
    SEEN["SF8"] = (sf8["order"], sf8b["order"], round(sf8b["req"] - g["req"], 1))
    # SF9: where each replay starts: every rung files its own order (the ladder above)
    for k in ("R0", "R1", "R2", "R2b", "R3", "T4"):
        ok(lad[k]["order"] != g["order"], ("SF9 rung files its own order", k))
    # SF10: cancelled sets counted as water (R2d); SF11: the record's water at Table 4 (T4) or all of it (R4g); SF20:
    # no cap (O2)
    ok(lad["R2d"]["order"] != g["order"] and lad["R4g"]["order"] != g["order"] and lad["T4"]["order"] != g["order"]
       and lad["O2"]["order"] != g["order"], "SF10 SF11 SF20")
    # SF12: the record run's start converges: from 1 November 2025 at field capacity or at total available water, and
    # from 1 February 2023 with every season's record (former field ids mapped through the register); the stations
    # fitted from 1 February 2026 give the same efficiency
    for D0 in (np.zeros(M.n), M.taw.copy()):
        Dw = M.hindcast({}, start=dt.date(2025, 11, 1), D0=D0, upto=K.WINTER_FULL)
        ok(float(Dw.max()) < 1e-12, "SF12 every root zone at field capacity at the end of 27 January 2026")
    ea_r = M.ea_record
    for lab, Dx in (("1 Feb 2026 full", M.hindcast(water, start=dt.date(2026, 2, 1), ea=ea_r)),
                    ("1 Nov 2025 full", M.hindcast(water, start=dt.date(2025, 11, 1), ea=ea_r)),
                    ("1 Nov 2025 empty", M.hindcast(water, start=dt.date(2025, 11, 1), D0=M.taw.copy(), ea=ea_r)),
                    ("1 Feb 2023 every season", M.hindcast(_water_all_seasons(M, target), start=dt.date(2023, 2, 1),
                                                           ea=ea_r))):
        ok(float(np.abs(Dx - D).max()) < 1e-9, ("SF12 the record run's start converges", lab))
    for st in hs:
        e1 = M.calibrate_station(st, days=(dt.date(2026, 2, 1), K.WEATHER_END))
        ok(abs(e1 - per[st["station"]]) < 0.002, ("SF12 a station fitted from 1 February", st["station"], e1))
    # SF13: a set's water by day: all on its first or last day instead of the hours it ran each day (the stations fitted
    # the same way)
    sf13 = {}
    for split in ("start", "end"):
        o = _calibrated_variant(M, water=M.set_water(split=split))
        ok(o["order"] == g["order"] and o["year"] == g["year"] and abs(o["req"] - g["req"]) < 420.0,
           ("SF13 converges", split, o["req"] - g["req"]))
        sf13[split] = round(o["req"] - g["req"], 1)
        # and the stations' daily readings follow the hours each set ran, not a set's water on one day
        ok(o["sse"] >= 5 * sse_e, ("SF13 the stations reject a set's water on one day", split, o["sse"], sse_e))
    SEEN["SF13"] = sf13
    # SF14: the day's order of the record's water: after the day's floor and cap, or before the day's ET and rain
    sf14 = {}
    for ordr in ("after", "before"):
        o = _calibrated_variant(M, order=ordr)
        ok(o["order"] == g["order"] and o["year"] == g["year"] and abs(o["req"] - g["req"]) < 420.0,
           ("SF14 converges", ordr, o["req"] - g["req"]))
        sf14[ordr] = (round(o["req"] - g["req"], 1), round(o["sse"] / sse_e, 2))
    SEEN["SF14"] = sf14
    # SF15: the register's GIS acres in the record run (the replays on the request acres)
    gis = np.array([float(M.register[f["id"]]["gis_acres"]) for f in M.fields])
    og = _calibrated_variant(M, acres=gis)
    ok(og["order"] == g["order"] and og["year"] == g["year"], "SF15 GIS acres in the record run: the same order and year")
    SEEN["SF15"] = round(og["req"] - g["req"], 1)
    # SF16: each set's water scaled by its turnout meter's season (the meters as the measure of what ran)
    A = C.load_asks(target)
    scale = _meter_scale(M, A, target)
    om = _calibrated_variant(M, water={d: v * scale for d, v in water.items()})
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
    sf21 = _order_loss_multiplied(M, st0)
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
    # SF37: a reading's day: local midnight ends the day before (the UTC date taken as the day files the same order,
    # SF40); SF38: a station's depletion is its full point less its profile water, and the full point is the profile
    # water at the end of January 2026 (every station within 0.15 in of it at the end of 27 January 2026)
    for st in S:
        ok(abs(st["full"] - st["reads"][K.WINTER_FULL]) < 0.15, ("SF38 the full point is the wet winter's profile",
                                                                  st["station"]))
    ok("UTC date as the day" in out and "a day early" in out, "SF37 the reading's day")
    # SF39: the period fitted (whole series, February to October, May to October) converges (SF40); SF42: the stations'
    # own fields at their readings converge (SF40); SF47: the logger gaps leave no reading on those days (nothing filled)
    gaps = {st["station"]: (K.WEATHER_END - dt.date(2025, 12, 31)).days + 1 - len(st["reads"]) for st in S}
    ok(sorted(v for v in gaps.values() if v) == [6, 8], ("SF47 two stations with logger gaps", gaps))
    ok("February to October" in out and "May to October" in out and "stations' fields at their readings" in out,
       "SF39 SF42")
    # SF41: the stations' efficiency kept to the stations' crops (PT) files another order; SF44: the crop coefficient
    # fit (KC) another; SF45: the stations' efficiency in the replays' deliveries (O3) another (WOP 3.5 files Table 4's)
    ok(lad["PT"]["order"] != g["order"] and lad["KC"]["order"] != g["order"] and lad["O3"]["order"] != g["order"],
       "SF41 SF44 SF45")
    # SF46: the stations' 31 January readings used directly, as an offset, as a share or through a fitted model on the
    # obvious covariates file other orders
    ok(all(lad[k]["order"] != g["order"] for k in ("P1", "AB", "MI", "RG")), "SF46")
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
    # the asks' files and the 2026 record are as shipped at round 2 (the operations log reworded, its estimates the same),
    # so every lateral figure is round 2's
    R2_ASKS = {"deliveries": [17870, 17530, 15400, 17890, 18160, 18210, 15310, 11490, 15080],
               "water in": [19680, 19410, 16880, 21020, 19760, 21060, 16710, 13110, 17370],
               "share": [9.2, 9.7, 8.8, 14.9, 8.1, 13.5, 8.4, 12.4, 13.2],
               "spill": [580, 630, 440, 270, 550, 650, 510, 420, 360]}
    for k, l in enumerate(K.LATERALS):
        ok(K.round_to(gd[l], 10) == R2_ASKS["deliveries"][k] and K.round_to(gi[l], 10) == R2_ASKS["water in"][k]
           and abs(share1(gs[l]) - R2_ASKS["share"][k]) < 1e-9 and K.round_to(sp[l], 10) == R2_ASKS["spill"][k],
           ("the lateral figures as shipped at round 2", l))
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
    """The world before any file is written: the 2027 fields, their crops, methods and acres, the 2026 delivered sets,
    and each soil moisture station's root zone as it is (its full point less the field's depletion at the end of each
    day, with no reading noise, no logger gaps and no time stamps), from the simulation."""
    acc = [f for f in W.fields if f["req_status"] == "accepted"]
    sets26 = {(o["start"], o["end"], round(o["cfs"], 1)) for o in W.orders if o["season"] == 2026
              and o["status"] == "Delivered" and W.field[o["field_id"]]["req_status"] == "accepted"}
    stations = []
    for x in W.stations:
        path = W.state_path[x["field"]]
        stations.append(dict(station=x["station"], field=x["field"], method=x["method"], crop=x["crop"], full=x["full"],
                             reads={d: x["full"] - path[d] for d in K.daterange(dt.date(2025, 12, 31), K.WEATHER_END)}))
    return dict(ids=[f["id"] for f in acc], acres={f["id"]: f["acres"] for f in acc},
                crop={f["id"]: f["crop"] for f in acc}, method={f["id"]: f["method"] for f in acc},
                sets26=sets26, stations=stations, W=W)


def _truth_order(T, M, route):
    """The order on the world's own fields, weather and 2026 sets: route 'table 4' (the record run at the Table 4
    efficiency, the default path) or 'stations' (the record run at the efficiency the stations' clean readings show,
    returned with that efficiency)."""
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
    if route == "table 4":
        return C.order_from(Mt.thirty(Mt.start_t4())[0])
    Mt.stations = T["stations"]
    o = C.order_from(Mt.thirty(Mt.start_golden())[0])
    return o, Mt.ea_by


# ---------------------------------------------------------------------------------------------------- helpers

def _season_path(M, water, ea):
    """The record run through 2026 to each field's last set at efficiency ea: the last day each field was full before
    its last set, and its depletion at the end of its last set's day."""
    Dd = np.zeros(M.n)
    lastfull = np.full(M.n, dt.date(2026, 1, 31).toordinal())
    at_last = np.zeros(M.n)
    lo = np.array([M.last_delivery[i].toordinal() for i in M.ids])
    for d in K.daterange(K.WINTER_FULL + dt.timedelta(days=1), dt.date(2026, 10, 31)):
        e, r = M.wx[d]
        net = water[d] * 12.0 / M.acres * ea if d in water else 0.0
        Dd = np.minimum(np.maximum(Dd + M.kc[:, d.month - 1] * e - r - net, 0.0), M.taw)
        lastfull = np.where((Dd < 1e-12) & (d.toordinal() < lo), d.toordinal(), lastfull)
        at_last = np.where(d.toordinal() == lo, Dd, at_last)
    return lastfull, at_last


def _golden_section(f, lo=0.55, hi=1.0, tol=1e-6):
    g = (5 ** 0.5 - 1) / 2
    a, b = lo, hi
    c, d_ = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d_)
    while b - a > tol:
        if fc <= fd:
            b, d_, fd = d_, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d_, fd
            d_ = a + g * (b - a)
            fd = f(d_)
    return (a + b) / 2


def _pooled(M):
    """One efficiency per method fitted on all the method's stations' readings together (least squares)."""
    out = {}
    for m in ("Drip", "Micro-sprinkler", "Sprinkler"):
        sts = [st for st in M.stations if st["method"] == m]
        out[m] = _golden_section(lambda e: sum(M.station_sse(st, e) for st in sts))
    return out


def _calibrated_variant(M, water=None, acres=None, order="net"):
    """The golden route under another construction of the record run (a set's water by day, the day's order of
    operations, the acres): the stations fitted with that construction, then every field run with it."""
    water = water if water is not None else M.water26()
    ac = M.acres if acres is None else acres
    days = list(K.daterange(K.WINTER_FULL + dt.timedelta(days=1), K.WEATHER_END))

    def path(i, e):
        D, out = 0.0, {}
        taw, kc = M.taw[i], M.kc[i]
        for d in days:
            ee, r = M.wx[d]
            net = water[d][i] * 12.0 / ac[i] * e if d in water else 0.0
            et = kc[d.month - 1] * ee
            if order == "net":
                D = min(taw, max(D + et - r - net, 0.0))
            elif order == "after":
                D = max(min(taw, max(D + et - r, 0.0)) - net, 0.0)
            else:
                D = min(taw, max(max(D - net, 0.0) + et - r, 0.0))
            out[d] = D
        return out

    def sse(st, e):
        p = path(M.index[st["field"]], e)
        return sum((st["full"] - v - p[d]) ** 2 for d, v in st["reads"].items() if d in p)

    per = {st["station"]: _golden_section(lambda e, st=st: sse(st, e)) for st in M.stations if st["method"] != "Border"}
    by = {m: float(np.mean([per[st["station"]] for st in M.stations if st["method"] == m]))
          for m in ("Drip", "Micro-sprinkler", "Sprinkler")}
    D = M.hindcast(water, acres=ac, order=order, ea=M.ea_from(by))
    o = variant_order(M, lambda y: D)
    o["sse"] = sum(sse(st, per[st["station"]]) for st in M.stations if st["method"] != "Border")
    o["by"] = by
    return o


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
    M2.stations = M.stations
    return C.order_from(M2.thirty(M2.start_golden())[0])


def _order_on_tables(M, T):
    M2 = C.Model(M.fields, M.wx, T, last_delivery=M.last_delivery, record=M.record)
    M2.stations = M.stations
    return C.order_from(M2.thirty(M2.start_golden())[0])


def _order_on_weather(M, wx):
    M2 = C.Model(M.fields, wx, M.T, last_delivery=M.last_delivery, record=M.record)
    M2.stations = M.stations
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
