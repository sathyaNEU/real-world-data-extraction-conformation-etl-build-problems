"""checks.py: the build's assertions, run on every build and every repair.

    python3 task168/generator/checks.py <target dir>

Blocks: R1 to R3c (the client's three rules, executed on the generator's clean truth and on the pack), SF (the
semantic fork table), the ladder (rung winners, separation, the construction family, bins), the holdouts, the
ask (golden, devices, ladder stops, fairness, separation), input gates, realism sweep, distractors and dates.
"""
import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)

import calc as C  # noqa: E402
import rivals as R  # noqa: E402
import world as W  # noqa: E402

UNIT = 25000
RESULTS = []
FIRST_NAMES = {"Ugo", "Concetta", "Piero", "Vincenza", "Lucrezia", "Nino", "Franco", "Ubaldo", "Damiano", "Matteo",
               "Marco", "Giulia", "Luca", "Paolo", "Anna", "Maria", "Giuseppe", "Francesca", "Alessandro", "Laura"}


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


def rnd(v, u=UNIT):
    return int(math.floor(v / u + 0.5) * u)


def edge(v, u=UNIT):
    return u / 2 - abs(v - round(v / u) * u)


def main(target):
    g = C.golden(target)
    gain = g["gain"]
    call = rnd(gain)
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    fam = R.family(target, g)
    rg = R.rungs(target, g)
    bt = R.backtest(target, g)
    pc = R.pseudo_censor(target, g)
    th = R.transfer_holdout(target, g)[0]
    sd, _ = R.bootstrap(target, g, n=80)
    ta = C.turnaways(target, rows, "golden")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))

    # ------------------------------------------------------------ the generator's clean truth
    from records import Seasons
    import pack as PK
    S = Seasons()
    tmp = tempfile.mkdtemp()
    try:
        _, truth, ev = PK.refusals_log(S, os.path.join(tmp, "r.csv"))
    finally:
        shutil.rmtree(tmp)

    # ============================================================ R1: the field's raw material ships
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    nref = {m: n for m, n in g["n_curve"].items()}
    check("R1a golden completes from departure-level booking builds", min(v for m, v in nref.items() if m != 3) >= 1000,
          "never-sold-out departures off the nine routes per month: %s" % nref)
    heads = {}
    for f in os.listdir(target):
        if f.endswith(".csv"):
            heads[f] = next(csv.reader(open(os.path.join(target, f), encoding="utf-8")))
    con = sqlite3.connect(os.path.join(target, "ym3_leg_history_s24.sqlite"))
    for (t,) in con.execute("select name from sqlite_master where type='table'"):
        heads["ym3." + t] = [r[1] for r in con.execute("pragma table_info(%s)" % t)]
    con.close()
    bad = [(f, h) for f, hs in heads.items() for h in hs
           if re.search(r"demand|unconstrain|spill|uplift|forecast|denied|turn", h, re.I)]
    check("R1b no shipped column holds the deciding quantity", not bad, str(bad) if bad else "headers clean")
    check("R1c the decisive build varies by departure month in the shipped rows",
          C.interp(g["curves"][8], dcps, 60) - C.interp(g["curves"][4], dcps, 60) > 0.25,
          "share on hand 60 days out: April %.3f, August %.3f" % (C.interp(g["curves"][4], dcps, 60),
                                                                  C.interp(g["curves"][8], dcps, 60)))

    # ============================================================ R2: every Layer 1 item real and neutral
    check("R2a lap infants counted as carried leaves the call", rnd(rg["side_infants_counted"]) == call,
          "%.0f -> %d" % (rg["side_infants_counted"], rnd(rg["side_infants_counted"])))

    def shift_so(hours):
        rr = []
        for r in rows:
            r2 = dict(r)
            if r["so"]:
                t = dt.datetime.strptime(r["so"], "%Y-%m-%dT%H:%M:%SZ") - dt.timedelta(hours=hours)
                r2["so"] = t.strftime("%Y-%m-%dT%H:%M:%SZ")
            rr.append(r2)
        return C.forecast(rr, dcs, dcps, lambda r: g["curves"][r["dep"].month])[0]
    v_local = shift_so(-2)
    check("R2b sell-out stamp read as local time leaves the call", rnd(v_local) == call, "%.0f" % v_local)
    check("R2c capacity plan v3 switch dates leave the call when read from v2", rnd(rg["side_switch_ignored"]) == call,
          "%.0f" % rg["side_switch_ignored"])
    # files the call never reads: the YM3 archive (old layout, old numbering), the refusals log, the close-out,
    # the fleet register; deleting each leaves the golden
    tmpd = tempfile.mkdtemp()
    try:
        for f in ("rm_booking_build_s25.csv", "dcs_flight_close_s25.csv"):
            shutil.copy(os.path.join(target, f), tmpd)
        g2 = C.golden(tmpd)
        check("R2d the call reads only the RM build and the DCS close-out", abs(g2["gain"] - gain) < 1e-6,
              "golden recomputed with the other twelve files absent")
    finally:
        shutil.rmtree(tmpd)
    days_nine = Counter((r["orig"], r["dest"]) for r in rows if C.is_nine(r["orig"], r["dest"]))
    check("R2e every nine-route departure has its DCS close-out row",
          all((r["flt"], r["dep"].isoformat()) in dcs for r in rows), "%d departures" % len(rows))

    # ============================================================ R3a: the analyst test on the clean truth
    def truth_per_seat():
        past = {(b, s) for b, s, *_ in W.PAST}
        pax = defaultdict(int)
        seats = defaultdict(int)
        for season in ("S24", "S25"):
            for L in S.legs(season, "past"):
                pax[season] += int(L.flown.sum())
                seats[season] += int(L.seats.sum())
        return (pax["S25"] - pax["S24"]) / (seats["S25"] - seats["S24"])
    ps_truth = truth_per_seat()
    r0_truth = ps_truth * rg["added_seats"]
    check("R3a easy route on the clean truth files the named wrong answer", rnd(r0_truth) != call and rnd(r0_truth) == rnd(rg["rung0_per_seat"]),
          "per seat %.4f x %d = %.0f -> %d (golden %d)" % (ps_truth, rg["added_seats"], r0_truth, rnd(r0_truth), call))
    check("R3a' the easy route on the pack files the same", rnd(rg["rung0_per_seat"]) == 500000,
          "%.0f" % rg["rung0_per_seat"])
    # R3b: the completion pooled over the summer with only the reference changed to the departure's month is the golden
    cp, _ = C.curves(rows, lambda r: 0, keep=nn)
    pooled = C.forecast(rows, dcs, dcps, lambda r: cp[0])[0]
    check("R3b the pooled completion with only the season matched files the golden",
          rnd(pooled) != call and rnd(C.forecast(rows, dcs, dcps, lambda r: g["curves"][r["dep"].month])[0]) == call,
          "pooled %.0f -> month %.0f" % (pooled, gain))
    check("R3b' each lower rung's single correction leaves it wrong",
          rnd(rg["rung1_carried_plus_turned_away"]) != call and rnd(rg["rung2b_pooled_nine_own_open"]) != call,
          "carried plus turned away %.0f, own open builds %.0f" % (rg["rung1_carried_plus_turned_away"],
                                                                  rg["rung2b_pooled_nine_own_open"]))
    # R3c: no plant
    texts = pdf_texts(target)
    basis = texts["planning_basis_NP-PB-26S_issue2.pdf"]
    check("R3c no filed basis for demand (carried plus refused, booking curve, per seat)",
          not re.search(r"refus|turned away|denied|booking curve|per seat|load factor|unconstrain", basis, re.I),
          "planning basis sections: %s" % ", ".join(re.findall(r"\d\. [A-Z][a-z]+", basis)))
    blocks = Counter()
    with open(os.path.join(target, "rm_booking_build_s25.csv"), encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        for row in rd:
            if row[9]:
                blocks[tuple(row[10:])] += 1
    check("R3c' no copied block of booking builds among sold-out departures", max(blocks.values()) <= 3,
          "largest repeat of a full 58-snapshot build: %d" % max(blocks.values()))

    # ============================================================ SF: semantic fork table
    base = sum(int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"]) for r in rows if C.is_nine(r["orig"], r["dest"]))
    booked = sum(int(dcs[(r["flt"], r["dep"].isoformat())]["pax_booked"]) for r in rows if C.is_nine(r["orig"], r["dest"]))
    check("SF1 passengers carried = pax_flown (infants and no-shows out); the bookings reading moves the call",
          base == g["base"] and rnd(rg["side_noshows_ignored"]) != call and rnd(rg["side_infants_counted"]) == call,
          "flown %d, booked %d; no-shows left in %.0f" % (base, booked, rg["side_noshows_ignored"]))
    deps = sorted({r["dep"] for r in rows})
    check("SF2 summer 2025 is the IATA season 30/03-25/10/2025 in every file", deps[0] == dt.date(2025, 3, 30)
          and deps[-1] == dt.date(2025, 10, 25) and len(deps) == 210, "%s to %s" % (deps[0], deps[-1]))
    nine_od = {(r["orig"], r["dest"]) for r in rows if C.is_nine(r["orig"], r["dest"])}
    check("SF3 the nine routes counted both ways: 18 route directions", len(nine_od) == 18, str(len(nine_od)))
    d26 = [d + dt.timedelta(days=364) for d in deps]
    check("SF4 summer 2026 repeats summer 2025's departures 364 days on, same weekday, inside IATA S26",
          d26[0] == W.SEASONS["S26"][0] and d26[-1] == W.SEASONS["S26"][1]
          and all(a.weekday() == b.weekday() for a, b in zip(deps, d26)), "%s to %s" % (d26[0], d26[-1]))
    caps = Counter(r["cap"] for r in rows if C.is_nine(r["orig"], r["dest"]))
    check("SF5 seats are physical seats (no overbooking): every nine-route departure sold at most its seats",
          set(caps) == {144} and all(r["bkd"][-1] <= r["cap"] for r in rows), str(dict(caps)))
    check("SF6 'demand' is wanting to fly (section 6); the carried reading would add nothing",
          "wanted to fly" in basis.replace("\n", " "), "section 6 wording present")
    check("SF7 capacity plan version 3 is the latest and adds the seats the prompt names",
          rg["added_seats"] == 620224 and "Version 3" in cap_cover(target), "%d" % rg["added_seats"])
    check("SF8 the call's rounding path: once, on the network total", rnd(gain) == call and edge(gain) >= UNIT / 4,
          "%.0f, %.0f from the nearest edge" % (gain, edge(gain)))
    s26_switch = sum(1 for r in rows if C.is_nine(r["orig"], r["dest"]) and C.station(r["orig"], r["dest"]) in ("BDS", "SUF")
                     and C.seats_s26(r) == 144)
    early = sum(1 for d in deps if d + dt.timedelta(days=364) < dt.date(2026, 6, 1))
    check("SF9 Brindisi and Lamezia Terme on 144 seats to 31/05/2026 (capacity plan v3)", s26_switch == 8 * early,
          "%d departures at 144 (%d days)" % (s26_switch, early))

    # ============================================================ the ladder
    lad = {"rung0 per seat": rg["rung0_per_seat"], "rung1 carried + turned away": rg["rung1_carried_plus_turned_away"],
           "rung2 pooled build": rg["rung2_pooled_network"], "rung2b own open build": rg["rung2b_pooled_nine_own_open"],
           "rung3 golden": gain}
    check("L1 each rung files its own figure", len({rnd(v) for v in lad.values()}) == 5,
          ", ".join("%s %d" % (k, rnd(v)) for k, v in lad.items()))
    check("L2 every rung misses the golden by at least one full bin",
          all(abs(rnd(v) - call) >= UNIT for k, v in lad.items() if k != "rung3 golden"),
          "nearest %d" % min(abs(rnd(v) - call) for k, v in lad.items() if k != "rung3 golden"))
    check("L3 the default path is rung 0", rnd(rg["rung0_per_seat"]) == 500000, "%.0f" % rg["rung0_per_seat"])
    check("L4 side errors on the golden construction: no-shows left in miss by a bin",
          abs(rnd(rg["side_noshows_ignored"]) - call) >= UNIT, "%.0f" % rg["side_noshows_ignored"])
    check("L5 added seats at the summer 2025 load factor misses", abs(rnd(rg["side_added_seats_at_s25_load"]) - call) >= UNIT,
          "%.0f" % rg["side_added_seats_at_s25_load"])
    loc = R.local_members(target, g)
    members = {k: v for k, v in fam.items() if not k.startswith("_")}
    members.update({k: v for k, v in loc.items() if not re.match(r"same flight within (28|35) days", k)})
    check("L6 every month-matched construction files the golden's figure",
          all(rnd(v) == call for v in members.values()),
          "%.0f to %.0f over %d constructions" % (min(members.values()), max(members.values()), len(members)))
    check("L7 every construction stays inside the bin under one bootstrap sigma",
          all(rnd(v - sd) == call and rnd(v + sd) == call for v in members.values()),
          "sigma %.0f; nearest edge %.0f" % (sd, min(edge(v) for v in members.values())))
    check("L8 the golden is at least a quarter bin from either edge", edge(gain) >= UNIT / 4, "%.0f" % edge(gain))
    check("L9 the deciding quantity rests on enough departures: golden +- sigma keeps the figure",
          rnd(gain - sd) == call and rnd(gain + sd) == call, "sigma %.0f" % sd)
    meth = R.methods(target, g)
    check("L10 additive pickup and normal EM, every grouping, land outside the bin",
          all(not (call - UNIT / 2 <= v < call + UNIT / 2) for v in meth.values()),
          "; ".join("%s %.0f" % (n, v) for n, v in meth.items()))
    near_ = min(min(abs(v - (call - UNIT / 2)), abs(v - (call + UNIT / 2))) for v in meth.values())
    check("L10' each of them at least 1,500 off the bin's edge", near_ >= 1500, "nearest %.0f" % near_)
    check("L11 per-seat responses of the 2025 gauge changes differ by depth (LOO error over a fifth)",
          rg["loo_mae"] > 0.2, "LOO mean abs error %.3f" % rg["loo_mae"])
    peak = [r for r in rows if C.is_nine(r["orig"], r["dest"]) and r["so"] and r["dep"].month in (7, 8)]
    xs = np.array([C.x_sellout(r) for r in peak])
    left = np.array([1 - C.interp(g["curves"][r["dep"].month], dcps, C.x_sellout(r)) for r in peak])
    check("L12 July and August departures sold out a median 23 days out, about a fifth of bookings still to come",
          22.5 <= float(np.median(xs)) < 23.5 and 0.18 < float(left.mean()) < 0.23,
          "median %.1f days, mean share to come %.3f" % (float(np.median(xs)), float(left.mean())))
    resp = R.per_seat_response(target, rows, dcs)
    lo_, hi_ = min(resp["routes"].values()), max(resp["routes"].values())
    over = sum(1 for r in rows if C.is_nine(r["orig"], r["dest"]) and C.demand(r, g["curves"][r["dep"].month], dcps) > 232)
    check("L13 the design note's rung 0 facts: per-seat 0.48 to 0.95 by route, completed demand over 232 on 118",
          round(lo_, 2) == 0.48 and round(hi_, 2) == 0.95 and over == figs["nine_departures_demand_over_232"] == 118,
          "%.3f to %.3f; %d departures" % (lo_, hi_, over))

    past_ = R.gauge_changes_s25(target)
    _, legs24_ = R.read_ym3(target)
    b24 = sum(L["bkd"][-1] for L in legs24_ if R.route_of(L["orig"], L["dest"]) in past_)
    c24 = sum(L["cap"] for L in legs24_ if R.route_of(L["orig"], L["dest"]) in past_)
    b25 = sum(int(dcs[(r["flt"], r["dep"].isoformat())]["pax_booked"]) for r in rows
              if R.route_of(r["orig"], r["dest"]) in past_)
    c25 = sum(r["cap"] for r in rows if R.route_of(r["orig"], r["dest"]) in past_)
    sold_ps = (b25 - b24) / (c25 - c24)
    check("L14 rung 0's 0.80 is passengers carried per extra seat, lap infants out of both summers; summer 2024 with "
          "its lap infants (the close-out's basis) gives 0.74 and seats sold 0.82",
          round(resp["per_seat"], 2) == 0.80 and round(resp["per_seat_infants_left_in"], 2) == 0.74
          and round(sold_ps, 2) == 0.82,
          "%.4f; %.4f; %.4f" % (resp["per_seat"], resp["per_seat_infants_left_in"], sold_ps))

    # ============================================================ coarse groupings of months, EM, own-route windows
    bk = R.buckets(target, g)
    mh = R.month_holdout(target, g)
    worst_month = max(abs(v) for v in mh.values())
    check("B1 the month build recovers the censored open departures within 1 per cent in every month",
          worst_month < 0.01, "worst %.2f per cent" % (100 * worst_month))
    for name, (v, h) in bk.items():
        w = max(abs(x) for x in h.values())
        inside = call - UNIT / 2 + UNIT / 4 <= v < call + UNIT / 2 - UNIT / 4
        check("B2 %s: rejected by the holdout or well inside the bin" % name,
              w >= 0.03 or inside, "%.0f (%d), worst month %.2f per cent" % (v, rnd(v), 100 * w))
        if not (call - UNIT / 2 <= v < call + UNIT / 2):
            check("B3 %s lands outside the bin and misses the holdout by over a tenth" % name, w > 0.10,
                  "worst month %.2f per cent" % (100 * w))
    eh = R.em_holdout(target, g)
    peak = [eh[m]["em"] for m in (6, 7, 8, 9)]
    check("E1 at the nine routes' censoring, EM falls short of the demand above the cap in each of June to September",
          max(peak) < -0.10, "June to September %s" % ", ".join("%.1f" % (100 * x) for x in peak))
    check("E2 over the summer EM falls about a fifth short, the month build under a tenth over in every month",
          -0.25 < eh["summer"]["em"] < -0.18 and max(eh[m]["month"] for m in range(3, 11)) < 0.10
          and min(eh[m]["month"] for m in range(3, 11)) > -0.10,
          "EM %.1f, month build %.1f to %.1f per cent" % (100 * eh["summer"]["em"],
                                                          100 * min(eh[m]["month"] for m in range(3, 11)),
                                                          100 * max(eh[m]["month"] for m in range(3, 11))))
    check("E3 EM falls short by about half in August", -0.65 < eh[8]["em"] < -0.45, "%.1f" % (100 * eh[8]["em"]))
    check("E4 the censoring the holdout copies is the nine routes' own: 98 per cent of August departures",
          round(100 * eh[8]["censored_share"]) == 98, "%.3f" % eh[8]["censored_share"])
    # EM and Tobit: the peak cells the fits would rest on, the call under each, and their month profile on both
    # depth-matched holdouts (per cell, and one cap per route direction), against the month build's
    pk = R.peak_cells(rows)
    op7 = sorted(a for a, b in pk[7].values())
    op8 = sorted(a for a, b in pk[8].values())
    n8 = sum(b for a, b in pk[8].values())
    check("E5 the nine routes' August route-direction months hold 0 to 4 departures that never sold out (none in six), "
          "July's 0 to 8: there a censored-distribution fit rests on its assumed shape",
          op8[0] == 0 and op8[-1] == 4 and op8.count(0) == 6 and op7[0] == 0 and op7[-1] == 8,
          "August %s (%d of %d open); July %s" % (op8, sum(op8), n8, op7))
    cfit = R.censored_fits(target, g)
    want = {"normal EM, route direction and month": 125000, "normal EM, route direction": 150000,
            "normal Tobit, route direction and month effects": 150000,
            "lognormal EM, route direction and month": 150000, "lognormal EM, route direction": call,
            "lognormal Tobit, route direction and month effects": 200000}
    check("E6 EM and Tobit on the nine routes' final bookings: each files its own figure; lognormal EM by route "
          "direction lands in the bin by accident", all(rnd(cfit[k]) == v for k, v in want.items()),
          "; ".join("%s %.0f (%d)" % (k, v, rnd(v)) for k, v in cfit.items()))
    fh = R.fit_holdouts(target, g)
    pcell = fh["per cell"]
    check("E7 the per-cell holdout of the fits reproduces em_holdout's EM and month build month by month",
          all(abs(pcell["normal EM, route direction and month"]["months"][m] - eh[m]["em"]) < 1e-6
              and abs(pcell["month build"]["months"][m] - eh[m]["month"]) < 1e-9 for m in range(3, 11)), "")
    for lab in ("per cell", "constant cap"):
        h = fh[lab]
        mb = h["month build"]
        fits = {k: v for k, v in h.items() if not k.startswith("_") and k != "month build"}
        check("E8 %s holdout: every EM and Tobit fit misses the nine routes' months by more than the month build "
              "(weighted RMS 1.3 times, worst month 1.5 times)" % lab,
              all(v["rms_w"] >= 1.3 * mb["rms_w"] and v["worst"] >= 1.5 * mb["worst"] for v in fits.values()),
              "month build summer %+.1f, worst %.1f, RMS %.1f; " % (100 * mb["summer"], 100 * mb["worst"], 100 * mb["rms_w"])
              + "; ".join("%s summer %+.1f, worst %.1f, RMS %.1f" % (k, 100 * v["summer"], 100 * v["worst"],
                                                                     100 * v["rms_w"]) for k, v in fits.items()))
    lk = fh["constant cap"]["_EM, route direction and month, empty cells at the truth"]
    hon = fh["constant cap"]["normal EM, route direction and month"]
    check("E11 at one cap per direction, EM by route direction and month reads near the month build only if its cells "
          "with none below the cap are handed their true final bookings, and its months still miss",
          fh["per cell"]["_empty_cell_departures"] == 0 and abs(lk["summer"]) < abs(hon["summer"])
          and lk["rms_w"] >= 1.3 * fh["constant cap"]["month build"]["rms_w"],
          "%+.1f (RMS %.1f) against %+.1f at the cap; %d departures in cells with none below the cap (none per cell)"
          % (100 * lk["summer"], 100 * lk["rms_w"], 100 * hon["summer"], fh["constant cap"]["_empty_cell_departures"]))
    tob = [fh[lab]["normal Tobit, route direction and month effects"]["rms_w"] / fh[lab]["month build"]["rms_w"]
           for lab in ("per cell", "constant cap")]
    check("E9 the fixed-effects Tobit's margin is the thinnest, 1.4 to 1.5 times the month build's RMS on both "
          "holdouts: its rejection is structural (the sell-out timing it discards)", all(1.3 <= t <= 1.6 for t in tob),
          "per cell %.2f, constant cap %.2f; constant cap summer %+.1f against %+.1f"
          % (tob[0], tob[1], 100 * fh["constant cap"]["normal Tobit, route direction and month effects"]["summer"],
             100 * fh["constant cap"]["month build"]["summer"]))
    lg = [fh[lab]["lognormal EM, route direction"] for lab in ("per cell", "constant cap")]
    check("E10 lognormal EM by route direction, the wrong method that lands, fails both holdouts month by month",
          all(v["rms_w"] >= 3 * fh[lab]["month build"]["rms_w"] for v, lab in zip(lg, ("per cell", "constant cap"))),
          "summer %+.1f and %+.1f; RMS %.1f and %.1f" % (100 * lg[0]["summer"], 100 * lg[1]["summer"],
                                                         100 * lg[0]["rms_w"], 100 * lg[1]["rms_w"]))
    sh = R.selection_holdout(target, g)
    ws = [sh["same flight within %d days" % d] for d in (7, 14, 21, 28, 35)]
    check("W1 the same-flight reference drifts up with its window in the holdout",
          all(b >= a - 0.005 for a, b in zip(ws, ws[1:])) and ws[-1] > 3 * sh["month"],
          "month %.1f; windows %s" % (100 * sh["month"], ", ".join("%.1f" % (100 * x) for x in ws)))
    su = R.selection_holdout_uniform(target, g)
    wu = [su["same flight within %d days" % d] for d in (7, 14, 21, 28, 35)]
    check("W3 the uniform 85 per cent holdout does not separate the same-flight windows (each within 1.5 points of "
          "the month build); only the depth holdout does", max(abs(x - su["month"]) for x in wu) < 0.015,
          "uniform: month %.1f; windows %s" % (100 * su["month"], ", ".join("%.1f" % (100 * x) for x in wu)))
    check("W4 the 21-day window lands while missing the depth holdout at nearly twice the month build's error",
          rnd(loc["same flight within 21 days"]) == call and sh["same flight within 21 days"] >= 1.8 * sh["month"],
          "%.0f; holdout %.1f against %.1f" % (loc["same flight within 21 days"], 100 * sh["same flight within 21 days"],
                                               100 * sh["month"]))
    for d in (28, 35):
        v = loc["same flight within %d days" % d]
        if not (call - UNIT / 2 <= v < call + UNIT / 2):
            check("W2 same flight within %d days lands outside the bin and misses the holdout by 2.5 times the month build" % d,
                  sh["same flight within %d days" % d] >= 2.5 * sh["month"],
                  "%.0f; holdout %.1f against %.1f" % (v, 100 * sh["same flight within %d days" % d], 100 * sh["month"]))

    # ============================================================ holdouts on the shipped rows
    check("H1 month builds recover censored open departures within 1 per cent in every month",
          max(abs(v["month"]) for v in pc.values()) < 0.01, str({m: round(v["month"], 4) for m, v in pc.items()}))
    check("H2 the pooled build misses them by over a tenth in July and August",
          pc[7]["pooled"] > 0.1 and pc[8]["pooled"] > 0.1, "Jul %.3f Aug %.3f" % (pc[7]["pooled"], pc[8]["pooled"]))
    size = size_holdout(rows, g, dcps)
    check("H3 additive pickup errs with departure size, multiplicative does not",
          size["add_small"] > 0.04 and size["add_large"] < -0.02 and max(abs(size["mult_small"]), abs(size["mult_large"])) < 0.015,
          str({k: round(v, 4) for k, v in size.items()}))
    check("H4 the completion forecasts the 2025 gauge changes from summer 2024 within 2 per cent",
          abs(bt["month_lastopen_err"]) < 0.02, "%.4f" % bt["month_lastopen_err"])
    check("H5 the transfer to the nine routes' own open departures holds (multiplicative within 1 per cent)",
          abs(th["multiplicative"]) < 0.01, str({k: round(v, 4) for k, v in th.items()}))

    # ============================================================ the ask: passengers turned away because full
    # the unit is filed in the prompt: each website or app session, call or booking reference once per departure
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    check("SF10 A0 the prompt files the ask's unit: each website or app session, call or booking reference once per "
          "departure", "counting each website or app session, call or booking reference once per departure" in prompt, "")
    tr = defaultdict(int)
    parties = {}
    for (eid, after, pid, size_, lo, ld), e in zip(truth, ev):
        parties[pid] = (lo, ld, size_, after)
    for pid, (o, d, kk, after) in parties.items():
        if after and C.is_nine(o, d):
            tr[(o, d)] += kk
    check("A1 the filed unit's literal execution reproduces the generator's truth exactly", dict(tr) == ta,
          "total %d, LIN-CTA %d" % (sum(ta.values()), ta[("LIN", "CTA")]))
    for mode in ("cracker", "departure", "nolight", "nodedup", "naive"):
        alt = C.turnaways(target, rows, mode)
        miss = sum(1 for kk in ta if alt.get(kk, 0) != ta[kk])
        check("A2 ladder stop %-9s misses every route direction" % mode, miss == 18,
              "%d of 18 differ; total %d against %d" % (miss, sum(alt.values()), sum(ta.values())))
    ref = C.read_refusals(target)
    so = {(r["flt"], r["dep"].isoformat()): r["so"] for r in rows}
    pre = Counter()
    journey = Counter()
    keys = defaultdict(list)
    for e in ref:
        od = route_of_flight(rows, e["flight_no"], e["dep_date"])
        if not C.is_nine(*od):
            continue
        s = so[(int(e["flight_no"]), e["dep_date"])]
        if s and e["logged_utc"] < s:
            pre[od] += 1
        if (e["orig"], e["dest"]) != od and s and e["logged_utc"] >= s:
            journey[od] += 1
        keys[(e["session_ref"], e["flight_no"], e["dep_date"])].append(e)
    names = defaultdict(int)
    seen_n = set()
    for e in ref:
        od = route_of_flight(rows, e["flight_no"], e["dep_date"])
        s = so[(int(e["flight_no"]), e["dep_date"])]
        if not (C.is_nine(*od) and s and e["logged_utc"] >= s):
            continue
        if e["channel"] == "GDS":
            names[od] += 1
            continue
        kk = (e["session_ref"], e["flight_no"], e["dep_date"])
        if kk not in seen_n:
            seen_n.add(kk)
            names[od] += int(e["pax"])
    gpax = defaultdict(list)
    for e in ref:
        if e["channel"] == "GDS":
            gpax[(e["session_ref"], e["flight_no"], e["dep_date"])].append(int(e["pax"]))
    check("SF10' reading each agency name record as one passenger gives the filed unit's counts (a booking writes one "
          "record per name, each at its party's pax)", dict(names) == ta and all(len(v) == v[0] for v in gpax.values()),
          "total %d against %d; %d agency bookings" % (sum(names.values()), sum(ta.values()), len(gpax)))
    check("A3 device P1 (fare-family refusals logged before the sell-out) on every route direction",
          len(pre) == 18 and min(pre.values()) > 20, "min %d" % min(pre.values()))
    check("A4 device P4 (agency records naming a connecting journey's airports) on every route direction",
          len(journey) == 18 and min(journey.values()) > 20, "min %d" % min(journey.values()))
    same_pax = all(len({x["pax"] for x in v}) == 1 for v in keys.values())
    check("A5 every record of one reference and departure carries the same pax (the unit has one weight)", same_pax,
          "%d references" % len(keys))
    straddle = sum(1 for (sref, f_, d_), v in keys.items() if so[(int(f_), d_)] and
                   min(x["logged_utc"] for x in v) < so[(int(f_), d_)] <= max(x["logged_utc"] for x in v))
    check("A6 no reference straddles its departure's sell-out", straddle == 0, str(straddle))
    gap = min(abs(dt.datetime.strptime(e["logged_utc"], "%Y-%m-%dT%H:%M:%SZ") -
                  dt.datetime.strptime(so[(int(e["flight_no"]), e["dep_date"])], "%Y-%m-%dT%H:%M:%SZ")).total_seconds()
              for e in ref if so[(int(e["flight_no"]), e["dep_date"])])
    check("A7 no request within 30 seconds of its departure's sell-out (the boundary converges)", gap >= 30, "%.0f s" % gap)
    cc = Counter(e["session_ref"] for e in ref if e["channel"] == "CC")
    check("A8 contact-centre call references are unique per record", max(cc.values()) == 1, "%d calls" % len(cc))
    gref = defaultdict(set)
    for e in ref:
        if e["channel"] == "GDS":
            gref[e["session_ref"]].add((e["flight_no"], e["dep_date"]))
    check("A8' every booking reference is one departure's", max(len(v) for v in gref.values()) == 1, "%d bookings" % len(gref))
    check("A9 no device row in the main call's population (the call reads no refusal record)", True,
          "R2d: the golden recomputes from the RM build and the DCS close-out alone")
    fams = Counter(e["fare_family"] for e in ref if C.is_nine(*route_of_flight(rows, e["flight_no"], e["dep_date"])))
    check("A10 fare family is no marker: LIGHT on both sides of the sell-out", fams["LIGHT"] > sum(pre.values()),
          str(dict(fams)))
    ch_j = Counter(e["channel"] for e in ref if (e["orig"], e["dest"]) != route_of_flight(rows, e["flight_no"], e["dep_date"]))
    gds_n = sum(1 for e in ref if e["channel"] == "GDS")
    check("A10' the journey airports are no marker: most agency records name the departure's own airports",
          set(ch_j) == {"GDS"} and ch_j["GDS"] < 0.3 * gds_n, "%s of %d agency records" % (dict(ch_j), gds_n))
    jr = [(e, route_of_flight(rows, e["flight_no"], e["dep_date"])) for e in ref
          if (e["orig"], e["dest"]) != route_of_flight(rows, e["flight_no"], e["dep_date"])]
    jr9 = [(e, od) for e, od in jr if C.is_nine(*od)]
    ok_j = all(e["channel"] == "GDS" and ((e["dest"] == od[1] and e["orig"] not in C.NINE + ["LIN"])
                                          or (e["orig"] == od[0] and e["dest"] not in C.NINE + ["LIN"]))
               for e, od in jr9)
    check("A12 the departure attributes the request: a record naming other airports is an agency booking's connecting "
          "journey, the departure's southern end and a hub abroad, never another route direction of the nine",
          ok_j and not any(C.is_nine(e["orig"], e["dest"]) for e, od in jr),
          "%d such records on the nine routes' departures" % len(jr9))
    check("A11 ask figures are distinct across route directions", len(set(ta.values())) == 18,
          "%d distinct" % len(set(ta.values())))

    # ============================================================ input gates and provenance
    files = sorted(os.listdir(target))
    fmts = {os.path.splitext(f)[1] for f in files}
    check("G1 ten or more files", len(files) >= 10, str(len(files)))
    check("G2 three or more formats", len(fmts) >= 3, str(sorted(fmts)))
    nrows = sum(1 for _ in open(os.path.join(target, "booking_engine_refusals_s25.csv"))) - 1
    check("G3 a file of 25,000 rows or more", nrows >= 25000 and len(rows) >= 25000,
          "refusals %d, RM build %d" % (nrows, len(rows)))
    dis = meta.get("distractor_files", [])
    check("G4 two or more distractors named in metadata.json", len(dis) >= 2 and all(d in files for d in dis), str(dis))
    check("G5 no distractor word in any file name", not any("distract" in f.lower() for f in files), "")
    tmpd = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in dis:
                shutil.copy(os.path.join(target, f), tmpd)
        g3 = C.golden(tmpd)
        ta3 = C.turnaways(tmpd, g3["rows"], "golden")
        check("G6 golden and ask unchanged with the distractors deleted", abs(g3["gain"] - gain) < 1e-6 and ta3 == ta, "")
    finally:
        shutil.rmtree(tmpd)
    mani = list(csv.DictReader(open(os.path.join(target, "export_manifest.csv"), encoding="utf-8")))
    check("G7 the manifest lists every other shipped file and not itself",
          {m["file"] for m in mani} == set(files) - {"export_manifest.csv"}, "%d rows" % len(mani))
    fleet = list(csv.DictReader(open(os.path.join(target, "fleet_register.csv"), encoding="utf-8")))
    regs_ = [x["registration"] for x in fleet]
    check("G8 every registration is listed once in the fleet register", len(regs_) == len(set(regs_)), "%d" % len(regs_))
    dcs_tails = {(d["tail"], d["equip"]) for d in dcs.values()}
    reg_model = {x["registration"]: x["seats"] for x in fleet}
    seats_of = {"319": "144", "320": "180", "32N": "186", "321": "220", "32Q": "232"}
    check("G9 every DCS tail is in the register with its type's seats",
          all(reg_model.get(t) == seats_of[e] for t, e in dcs_tails), "%d tails" % len(dcs_tails))
    first = min(e["logged_utc"] for e in ref)
    last = max(e["logged_utc"] for e in ref)
    f_loc = dt.datetime.strptime(first, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=C.UTC).astimezone(C.ROME).date()
    l_loc = dt.datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=C.UTC).astimezone(C.ROME).date()
    span = "%d %s %d to %d %s %d" % (f_loc.day, f_loc.strftime("%B"), f_loc.year, l_loc.day, l_loc.strftime("%B"), l_loc.year)
    man_ref = [m for m in mani if m["file"] == "booking_engine_refusals_s25.csv"][0]
    check("G10 the dictionary and the manifest give the refusal log's own first and last dates",
          span in " ".join(texts["data_dictionary_rev5.pdf"].split()) and span in man_ref["covers"], span)

    # ============================================================ realism sweep
    by_route = Counter()
    for r in rows:
        if C.is_nine(r["orig"], r["dest"]):
            by_route[C.station(r["orig"], r["dest"])] += int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"])
    check("S1 no identical passenger totals across routes", len(set(by_route.values())) == 9, str(dict(by_route)))
    check("S2 no round headline figure in the pack's own totals", g["base"] % 100 != 0 and sum(ta.values()) % 100 != 0,
          "%d, %d" % (g["base"], sum(ta.values())))
    people = set(json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task168.json")))["world"]["people"])
    alltext = " ".join(texts.values()) + " " + cap_cover(target)
    caps_names = set(re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]{3,}\b", alltext))
    strangers = {n for n in caps_names if n.split()[0] in FIRST_NAMES and n not in people}
    used = {p for p in people if p in alltext}
    check("S3 every persona in the pack is one the card drew from guard.py names", used and not strangers,
          "%s; others %s" % (sorted(used), sorted(strangers)))
    # dates after the pack's export date sit only in the files that carry plans (house fix H16, a file allow-list)
    allow = {"planning_basis_NP-PB-26S_issue2.pdf", "summer2026_capacity_plan_v3.xlsx", "schedule_change_log.xlsx",
             "fleet_register.csv"}
    late_files = set()
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            t = texts[f]
        elif f.endswith(".xlsx"):
            from openpyxl import load_workbook
            wb = load_workbook(p, read_only=True)
            t = " ".join(str(c) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row if c)
        elif f.endswith(".csv"):
            t = open(p, encoding="utf-8").read()
        else:
            continue
        ds = [dt.date(int(y), int(m), int(d)) for d, m, y in re.findall(r"\b(\d{1,2})/(\d{1,2})/(20\d\d)\b", t)]
        ds += [dt.date(int(y), int(m), int(d)) for y, m, d in re.findall(r"\b(20\d\d)-(\d\d)-(\d\d)\b", t)]
        if any(d0 > W.ASOF for d0 in ds):
            late_files.add(f)
    check("S4 dates past the export date only in the files that carry plans", late_files <= allow,
          "late dates in %s" % sorted(late_files))
    stamps = {"rm_booking_build_s25.csv": max(r["so"] for r in rows if r["so"])[:10],
              "booking_engine_refusals_s25.csv": max(e["logged_utc"] for e in ref)[:10]}
    check("S4' each extract's latest record precedes its extract date", stamps["rm_booking_build_s25.csv"] <= "2025-12-01"
          and stamps["booking_engine_refusals_s25.csv"] <= "2025-12-03", str(stamps))
    late = [e for e in ref if e["logged_utc"] > "2025-10-26"]
    check("S5 every refusal logged before its departure's sales close",
          not late and all(e["logged_utc"][:10] <= e["dep_date"] for e in ref), "")
    so_bad = [r for r in rows if r["so"] and r["so"][:10] > r["dep"].isoformat()]
    check("S6 every sell-out before its departure", not so_bad, str(len(so_bad)))
    check("S7 the ask's chart labels and the workbook carry the same figures", figs["turned_away"] == {"%s-%s" % k: v for k, v in sorted(ta.items())}, "")

    fails = [r for r in RESULTS if not r[1]]
    print("\n%d assertions, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


# ------------------------------------------------------------------ helpers
def pdf_texts(target):
    from pypdf import PdfReader
    out = {}
    for f in os.listdir(target):
        if f.endswith(".pdf"):
            out[f] = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, f)).pages)
    return out


def cap_cover(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "summer2026_capacity_plan_v3.xlsx"))
    return " ".join(str(c.value) for row in wb["Cover"].iter_rows() for c in row if c.value)


def route_of_flight(rows, f_, d_, _cache={}):
    if not _cache:
        for r in rows:
            _cache[(str(r["flt"]), r["dep"].isoformat())] = (r["orig"], r["dest"])
    return _cache[(str(f_), d_)]


def gds_line_gaps(ref):
    by = defaultdict(list)
    for e in ref:
        by[(e["channel"], e["session_ref"], e["flight_no"], e["dep_date"])].append(
            dt.datetime.strptime(e["logged_utc"], "%Y-%m-%dT%H:%M:%SZ"))
    gds_max, web_min = 0, 10 ** 9
    for (ch, *_), ts in by.items():
        if len(ts) < 2:
            continue
        ts.sort()
        gaps = [(b - a).total_seconds() for a, b in zip(ts, ts[1:])]
        if ch == "GDS":
            gds_max = max(gds_max, max(gaps))
        elif ch in ("WEB", "APP"):
            web_min = min(web_min, min(gaps))
    return {"gds_max": gds_max, "web_min": web_min}


def size_holdout(rows, g, dcps, share=0.85):
    arr = np.array(dcps, float)
    refs = [r for r in rows if r["so"] == "" and not C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] >= 40]
    pick = defaultdict(list)
    for r in refs:
        pick[r["dep"].month].append(r["bkd"][-1] - r["bkd"])
    pm = {m: np.mean(v, axis=0) for m, v in pick.items()}
    fin = np.array([r["bkd"][-1] for r in refs])
    q = np.quantile(fin, [1 / 3, 2 / 3])
    acc = defaultdict(float)
    for r in refs:
        cap = share * r["bkd"][-1]
        j = int(np.nonzero(r["bkd"] >= cap)[0][0])
        if j == 0:
            continue
        b0, b1 = r["bkd"][j - 1], r["bkd"][j]
        x = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap - b0) / (b1 - b0) if b1 > b0 else 1.0)
        t = "small" if r["bkd"][-1] < q[0] else ("large" if r["bkd"][-1] >= q[1] else "mid")
        acc["mult_" + t] += cap / C.interp(g["curves"][r["dep"].month], dcps, x)
        acc["add_" + t] += cap + float(np.interp(x, arr[::-1], pm[r["dep"].month][::-1]))
        acc["act_" + t] += r["bkd"][-1]
    return {k: acc[k] / acc["act_" + k.split("_")[1]] - 1 for k in ("mult_small", "mult_large", "add_small", "add_large")}


def guard_names():
    import subprocess
    out = subprocess.run([sys.executable, os.path.join(REPO, ".claude", "skills", "fingerprint", "guard.py"), "names",
                          "--geo", "Italy", "--seed", "168", "--n", "30"], capture_output=True, text=True).stdout
    return {m for m in re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", out)}


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
