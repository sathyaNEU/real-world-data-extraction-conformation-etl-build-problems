"""Assertions on the built pack and the world it came from: the three-rules block (the resident route files the named
wrong answer on the clean truth and on the pack; adding the parks' guests alone files the golden), the standing family,
the ladder, every semantic fork row, the bins, the ask devices, separation, the input gates and the realism sweep.

    python3 task305/generator/checks.py <target dir>
"""
import collections
import csv
import re
import datetime as dt
import io
import math
import os
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ops as O
import params as P
import records as R
import solve as S
import world as Wd

GOLD_SITE, EASY_SITE = "S3", "S1"
N = 0


def ok(cond, msg):
    global N
    N += 1
    if not cond:
        raise AssertionError(msg)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def walk(folder):
    out = []
    for root, dirs, fs in os.walk(folder):
        out += [os.path.relpath(os.path.join(root, f), folder) for f in fs]
    return sorted(out)


def tenth(v):
    return round(v / 1e5) / 10.0


def main(target):
    F = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    pk = S.Pack(target)
    c = pk.call()
    g, r0, V = c["golden"], c["resident"], c["V"]
    T = Wd.truth()
    # ---- R1: the field's raw material ships at its own grain; no shipped column holds a site's trade --------------
    ok(len(pk.oas) >= 300 and len(pk.voa) >= 4000, "R1 output areas and the rating list ship at their grains")
    heads = []
    for k, f in P.FILES.items():
        if f.endswith(".csv"):
            heads += next(csv.reader(open(F[k], encoding="utf-8")))
    ok(not [h for h in heads if any(w in h.lower() for w in ("guest", "visitor", "addition", "contribution", "forecast"))],
       "R1 no shipped column names a site's trade, the guests or an addition")
    ok(len(pk.cards) > 7000 and len({r["cardholder_home_sector"] for r in pk.cards}) > 300,
       "R1 the card feed ships by store, month and home sector")
    # ---- R3a: the resident route, every filed rule applied over the census alone, files S1 ---------------------------
    tr = T["resident"]
    win = max(tr, key=lambda k: tr[k]["add"])
    ok(win == EASY_SITE and tenth(tr[win]["add"]) == 0.4, "R3a clean truth: the resident route files S1 at 0.4 million")
    ok(c["resident_site"] == EASY_SITE and tenth(r0[EASY_SITE]["add"]) == 0.4, "R3a pack: the resident route files S1 at 0.4")
    order0 = sorted(r0, key=lambda k: -r0[k]["add"])
    ok(order0.index(GOLD_SITE) >= 1 and r0[EASY_SITE]["add"] >= 2 * r0[GOLD_SITE]["add"],
       "R3a Wrentoft trails S1 by a factor of two or more on the resident route (%s)" % order0)
    # ---- the default path: the parks carried (the model sheet files anyone's spend where they stay), a pitch priced
    # straight off our park-side stores' take, when that take is only our modelled share of each park's spend -------
    guests = pk.guests()
    named = {r[9]: pk.smv[r[6]][0] for r in pk.voa if r[6] in pk.smv and pk.smv[r[6]][1] == "pitches"}
    side = {"107": "RADDLEFORD WATER HOLIDAY PARK", "105": "WITHYBECK LAKES CARAVAN PARK"}
    v_direct = {"both": sum(guests[s] for s in side) / sum(named[p] for p in side.values())}
    for s_, p_ in list(side.items()) + [("104", "SALLOWMERE MILL CARAVAN PARK")]:
        v_direct[s_] = guests[s_] / named[p_]
    v_direct["every pitch"] = sum(guests.values()) / sum(p["n"] for p in pk.parks)
    for lab, v in v_direct.items():
        a = pk.appraise(v)
        o = sorted(a, key=lambda k: -a[k]["add"])
        ok(o[0] == EASY_SITE and a[o[0]]["add"] >= 1.15 * a[o[1]]["add"] and tenth(a[o[0]]["add"]) == 0.4,
           "default path (%s, GBP %.0f a pitch) files S1 at 0.4, clear by %.2f" % (lab, v, a[o[0]]["add"] / a[o[1]]["add"]))
    st_ = T["stores"]
    idx_ = {x["id"]: k for k, x in enumerate(st_)}
    v_true_direct = (T["vis"][idx_["107"]] + T["vis"][idx_["105"]]) / sum(p[3] for p in P.PARKS if p[0] in
                                                                         ("Raddleford Water Holiday Park", "Withybeck Lakes Caravan Park"))
    old_v = P.V_PITCH
    P.V_PITCH = v_true_direct
    tdir = Wd.appraise(T["oas"], True, st_)
    P.V_PITCH = old_v
    ok(max(tdir, key=lambda k: tdir[k]["add"]) == EASY_SITE and tenth(tdir[EASY_SITE]["add"]) == 0.4,
       "analyst test, clean truth: the parks carried at our park-side stores' take over their pitches file S1 at 0.4")
    sh_side = {s_: sum(pk.shares(next(p["xy"] for p in pk.parks_2025 if p["pc"] == pc_), pk.stores_2025)[k]
                       for k, x in enumerate(pk.stores_2025) if x["own"])
               for s_, pc_ in (("107", next(r[14] for r in pk.voa if r[9] == side["107"])),
                               ("105", next(r[14] for r in pk.voa if r[9] == side["105"])))}
    ok(all(0.05 <= v <= 0.35 for v in sh_side.values()), "the decisive quantity: in the card feed's year our stores took "
       "%s of the two parks' spend, the competitor beside each the most of the rest" % {k: round(v, 3) for k, v in
                                                                                         sh_side.items()})
    ok(V >= 3 * v_direct["both"], "the decisive step's worth: recovered through our share a pitch is %.2f times the "
       "direct reading" % (V / v_direct["both"]))
    # ---- R3b: the decisive step alone files the golden ------------------------------------------------------------
    tg = T["golden"]
    ok(max(tg, key=lambda k: tg[k]["add"]) == GOLD_SITE and tenth(tg[GOLD_SITE]["add"]) == 0.8,
       "R3b clean truth: the parks' spend recovered through our modelled share files S3 at 0.8")
    ok(c["site"] == GOLD_SITE and tenth(c["add"]) == 0.8, "R3b pack: the parks' spend per pitch recovered from our share")
    ok(edge(c["add"] / 1e6, 0.1) >= 0.02, "golden %.4f clears its cell's edges" % (c["add"] / 1e6))
    ok(g[GOLD_SITE]["add"] >= 1.5 * g[EASY_SITE]["add"], "golden margin %.2f" % (g[GOLD_SITE]["add"] / g[EASY_SITE]["add"]))
    # the lower rungs stay on S1, each clearing its runner-up
    act = {str(r["store_no"]): float(r["sales_fy2025_26_gbp"]) for r in pk.estate}
    pct = guests["107"] / act["107"]
    rung2a = {k: v["add"] + (P.MARGIN * v["new"] * pct / (1 - pct) if k == GOLD_SITE else 0.0) for k, v in r0.items()}
    rung2b = {k: v["add"] + (P.MARGIN * guests["107"] if k == GOLD_SITE else 0.0) for k, v in r0.items()}
    big = max(named.values())
    rung2c = {k: v["add"] + (P.MARGIN * guests["107"] * big / named[side["107"]] if k == GOLD_SITE else 0.0)
              for k, v in r0.items()}
    base = pk.sales(pk.stores, pk.oas)
    ratio = np.mean([act[s["id"]] / base[k] for k, s in enumerate(pk.stores) if s["own"]])
    rung1 = {k: P.MARGIN * (v["new"] - v["took"]) * ratio - v["cost"] for k, v in r0.items()}
    rungs2c = {}
    for sid_, park_ in (("107", side["107"]), ("105", side["105"]), ("104", "SALLOWMERE MILL CARAVAN PARK")):
        rungs2c["rung 2c at %s (the park-side store's take scaled by pitches)" % sid_] = {
            k: v["add"] + (P.MARGIN * guests[sid_] * big / named[park_] if k == GOLD_SITE else 0.0) for k, v in r0.items()}
    for lab, rr in [("rung 0", {k: v["add"] for k, v in r0.items()}), ("rung 1", rung1), ("rung 2a", rung2a),
                    ("rung 2b", rung2b)] + list(rungs2c.items()):
        o = sorted(rr, key=lambda k: -rr[k])
        ok(o[0] == EASY_SITE and rr[o[0]] >= 1.15 * rr[o[1]], "%s stays on S1 by %.2f" % (lab, rr[o[0]] / rr[o[1]]))
        ok(o.index(GOLD_SITE) >= 1, "%s Wrentoft %d" % (lab, o.index(GOLD_SITE) + 1))
    # ---- the standing family: every construction recovering the parks' spend through our share files S3 at 0.8 ----
    fam = {"pooled": V}
    for s_ in ("104", "105", "107"):
        fam["store %s" % s_] = pk.v_per_pitch(only={s_})
    fam["105 and 107"] = pk.v_per_pitch(only={"105", "107"})
    fam["off Dec-Feb"] = pk.v_per_pitch(guests=pk.guests(off=("2025-12", "2026-01", "2026-02")))
    fam["off Jan-Feb"] = pk.v_per_pitch(guests=pk.guests(off=("2026-01", "2026-02")))
    fam["no gross-up"] = pk.v_per_pitch(guests=pk.guests(gross=False))
    vals = {}
    for lab, v in fam.items():
        a = pk.appraise(v)
        w = max(a, key=lambda k: a[k]["add"])
        vals[lab] = a[w]["add"] / 1e6
        ok(w == GOLD_SITE and tenth(a[w]["add"]) == 0.8, "family %s files %s %.3f" % (lab, w, a[w]["add"] / 1e6))
    ok(max(vals.values()) - min(vals.values()) <= 0.07, "standing family spread %.3f" % (max(vals.values()) - min(vals.values())))
    ok(min(edge(v, 0.1) for v in vals.values()) >= 0.01, "every standing member clears its cell's edges (%s)" %
       {k: round(v, 4) for k, v in vals.items()})
    # SF27: a park scaled by its rateable value instead of its pitches recovers the same spend per unit (caravan parks
    # are valued at one rate a pitch)
    rv = {r[9]: float(r[17]) for r in pk.voa if r[6] in pk.smv and pk.smv[r[6]][1] == "pitches"}
    rv_per = {k: rv[k] / named[k] for k in named if "CARAVAN PARK" in next(r[5] for r in pk.voa if r[9] == k)}
    ok(max(rv_per.values()) / min(rv_per.values()) < 1.02, "SF27 caravan parks carry one rateable value a pitch (%s)" %
       {k[:12]: round(v) for k, v in rv_per.items()})
    # C1 on the boundaries the call and ask A read
    ms = [pk.smv[r[6]][0] for r in pk.voa if r[5] in P.GROCERY and r[6] in pk.smv and pk.smv[r[6]][1] == "m2"]
    ok(not [m for m in ms if 270 <= m <= 290], "C1 no grocery entry within 10 m2 of the 280 m2 line")
    lo = dt.datetime.combine(P.TMS_FROM, dt.time(0, 0))
    hi = dt.datetime.combine(P.TMS_TO + dt.timedelta(days=1), dt.time(0, 0))
    ok(not [r for r in S.rd(F["tms"]) if r["stop_type"] == "DEL" and
            min(abs((S.to_local(r["arrive_utc"]) - lo).total_seconds()), abs((S.to_local(r["arrive_utc"]) - hi).total_seconds())) < 7200],
       "C1 no delivery arrives within two hours of the 25 weeks' edges")
    ok({str(r["postcode"]) for r in pk.estate} <= {r[14] for r in pk.voa if r[5] in P.GROCERY} and
       {r["store_no"] for r in pk.cards} == {str(r["store_no"]) for r in pk.estate}, "joins: the estate, the list and the feed resolve")
    # ---- semantic fork rows ---------------------------------------------------------------------------------------
    from pypdf import PdfReader
    model_src = " ".join(" ".join(pg.extract_text() for pg in PdfReader(F["model"]).pages).split())
    ok("26 per cent of its own sales" in model_src and "less its running costs" in model_src, "SF1 the appraisal is filed")
    ok("Spend starts where people are: a household's at its output area, and anyone else's at the place where they are "
       "staying." in model_src, "SF26 the population is filed: a household's spend at its output area, anyone else's where "
       "they stay, no kind of place, count or rate named")
    dc_src = " ".join(" ".join(pg.extract_text() for pg in PdfReader(F["dc_proc"]).pages).split())
    ok("the driver still closes the stop as delivered, and the planners send the same load again the next day on a trip "
       "of its own" in dc_src and "keeps every time in UTC" in dc_src, "SF28 ask A: a load turned away at the door is filed "
       "in the DC's procedure TP-04 (closed as delivered, sent again the next day on its own trip); which stops they are "
       "is left to the records")
    wfm_head = open(F["wfm"], encoding="utf-8").read().split("\n")[:5]
    ok(any("A shift is shown against each calendar date it covers, with its paid hours on each line" in ln for ln in wfm_head),
       "SF29 ask B: the report's own header files its grain (a shift on every date it covers); which lines are one shift "
       "is left to the punches")
    joint = {}
    for key in ("gtfs_lb", "gtfs_pdc"):
        with zipfile.ZipFile(F[key]) as z:
            for r in csv.DictReader(io.TextIOWrapper(z.open("routes.txt"), encoding="utf-8")):
                if r["route_desc"]:
                    joint.setdefault(key, set()).add(r["route_short_name"])
    ok(joint == {"gtfs_lb": {"4", "41"}, "gtfs_pdc": {"4", "41"}}, "SF30 ask C: both feeds mark routes 4 and 41 as a joint "
       "service with the other operator; a block is one vehicle's working as GTFS defines block_id; the Friday-late "
       "repeats, the school-day duplicates and the clock past 24:00 are left to the feeds (%s)" % joint)
    allf = walk(target)
    bad = [f for f in allf if f.lower().endswith((".md", ".txt")) and f not in (P.FILES["voa_list"], P.FILES["voa_hist"])]
    ok(not bad and not [f for f in allf if re.search(r"(?i)read_?me|dictionar|field_?notes|manifest|data_?notes", f)],
       "dataset-generation 3: no readme, dictionary, notes or manifest file ships (%s)" % bad)
    ok("a year of trading at 2026 prices" in model_src, "SF2 a year at 2026 prices")
    ok(len({r["date"] for r in S.rd(F["households"])}) == 1, "SF3 one census count of households, 2021")
    a = pk.appraise(V)
    ok(True, "SF4 the guests' spend is measured in store, so 88 per cent applies to households only")
    a88 = pk.appraise(V * P.INSTORE)
    ok(tenth(a88[GOLD_SITE]["add"]) != 0.8, "SF4 multiplying the measured spend by 0.88 files another figure")
    small = [r for r in pk.voa if r[5] in P.GROCERY and r[6] in pk.smv and pk.smv[r[6]][0] < P.MIN_AREA]
    ok(len(small) >= 10, "SF5 small food stores sit under the 280 m2 line (%d)" % len(small))
    ok("280 m2 or more" in model_src, "SF5 the share's stores are filed")
    ok("1.25 x straight-line" in model_src and "population-weighted centroid" in model_src, "SF6 distances filed")
    ok(all(r["postcode"] in pk.pc for r in pk.sites), "SF7 every site's postcode is in the ONSPD extract")
    # SF8: what the new store takes from ours includes the guests it takes; residents only gives the same call
    a_res_took = {}
    for k, v in a.items():
        a_res_took[k] = v["add"] + P.MARGIN * (v["took"] - r0[k]["took"])
    ok(max(a_res_took, key=lambda k: a_res_took[k]) == GOLD_SITE and tenth(a_res_took[GOLD_SITE]) == 0.8, "SF8 same call")
    # SF9: a park at its postcode (filed) or at its output area's centroid: same call
    oa_of = {r["pcds"]: r["oa21"] for r in S.rd(F["onspd"])}
    pwc = {r["OA21CD"]: (float(r["x"]), float(r["y"])) for r in S.rd(F["pwc"])}
    parks2 = [dict(p, xy=pwc[oa_of[p["pc"]]]) for p in pk.parks]
    parks25 = [dict(p, xy=pwc[oa_of[p["pc"]]]) for p in pk.parks_2025]
    a9 = pk.appraise(pk.v_per_pitch(parks=parks25), parks=parks2)
    w9 = max(a9, key=lambda k: a9[k]["add"])
    print("SF9 a park at its output area's centroid files %s %.3f (the filed reading files %s %.3f)" % (
        w9, a9[w9]["add"] / 1e6, GOLD_SITE, c["add"] / 1e6))
    ok("any other address at its postcode" in model_src and (w9, tenth(a9[w9]["add"])) != (GOLD_SITE, 0.8) or
       (w9 == GOLD_SITE and tenth(a9[GOLD_SITE]["add"]) == 0.8),
       "SF9 a park is an address, at its postcode's grid reference as the model sheet files it; the centroid reading "
       "is ruled out by that sentence")
    ok("any other address at its postcode" in model_src, "SF9 the postcode is filed")
    # SF10: the guests' spend: with or without the gross-up, same call; without the year-round subtraction, another
    # figure, ruled out because the year-round out-of-region spend runs at the stores no park reaches
    a10 = pk.appraise(pk.v_per_pitch(guests=pk.guests(gross=False)))
    ok(max(a10, key=lambda k: a10[k]["add"]) == GOLD_SITE and tenth(a10[GOLD_SITE]["add"]) == 0.8, "SF10 no gross-up, same call")
    a10b = pk.appraise(pk.v_per_pitch(guests=pk.guests(off=())))
    ok(tenth(a10b[GOLD_SITE]["add"]) != 0.8, "SF10 counting every out-of-region pound as guests files another figure")
    far = [s["id"] for k, s in enumerate(pk.stores) if s["own"] and
           max(pk.shares(p["xy"], pk.stores)[k] for p in pk.parks) < 0.006]
    nl = {}
    for r in pk.cards:
        if not r["cardholder_home_sector"].startswith(P.AREA):
            nl.setdefault(r["store_no"], {}).setdefault(r["month"], 0.0)
            nl[r["store_no"]][r["month"]] += float(r["spend_gbp"])
    ok(len(far) >= 2, "SF10 stores no park reaches: %s" % far)
    ok(all(np.mean([nl[s][m] for m in S.OFF]) > 300 for s in nl), "SF10 every store has out-of-region cardholders all year")
    for s in far:
        offm = np.mean([nl[s][m] for m in S.OFF])
        seas = np.mean([nl[s][m] for m in P.MONTHS if int(m[5:]) in P.SEASON])
        ok(offm > 300 and seas / offm < 1.4, "SF10 store %s carries much the same out-of-region spend all year" % s)
    for s in ("105", "107"):
        offm = np.mean([nl[s][m] for m in S.OFF])
        seas = np.mean([nl[s][m] for m in P.MONTHS if int(m[5:]) in P.SEASON])
        ok(seas / offm > 5, "SF10 store %s: the season runs %.0f times its year-round level" % (s, seas / offm))
    # SF11: every pitch-measured site, or caravan parks only: same call
    car = [p for p in pk.parks if "CARAVAN PARK" in p["desc"]]
    car25 = [p for p in pk.parks_2025 if "CARAVAN PARK" in p["desc"]]
    a11 = pk.appraise(pk.v_per_pitch(parks=car25), parks=car)
    ok(max(a11, key=lambda k: a11[k]["add"]) == GOLD_SITE and tenth(a11[GOLD_SITE]["add"]) == 0.8, "SF11 same call")
    # SF12: the season's months: the excess runs March to October; April to September only files another figure
    off = np.mean([sum(nl["107"].get(m, 0) for m in S.OFF) / 4.0])
    ok(nl["107"]["2026-03"] > 1.5 * off and nl["107"]["2025-10"] > 1.5 * off and nl["107"]["2025-11"] < 1.3 * off,
       "SF12 the excess at Raddleford runs March to October")
    # SF13: rounding once, at the end
    ok(tenth(sum([v["add"] for v in [a[GOLD_SITE]]])) == 0.8, "SF13 the addition rounded once")
    ok(abs(tenth(a[GOLD_SITE]["new"] * P.MARGIN) - tenth(a[GOLD_SITE]["took"] * P.MARGIN) - tenth(a[GOLD_SITE]["cost"]) - 0.8) < 0.11,
       "SF13 rounding the parts first stays within a tenth")
    # SF31: the year-round out-of-region cardholders are people staying with residents (or living here on an address
    # outside the area); carried at the output areas, their spend files the same call and figure
    yr = sum(np.mean([nl[s_][m] for m in S.OFF]) * 12 for s_ in nl)
    card_tot = sum(float(r["spend_gbp"]) for r in pk.cards)
    oas_keep = pk.oas
    pk.oas = [(xy, dd * (1 + yr / card_tot)) for xy, dd in oas_keep]
    a31 = pk.appraise(V)
    pk.oas = oas_keep
    ok(max(a31, key=lambda k: a31[k]["add"]) == GOLD_SITE and tenth(a31[GOLD_SITE]["add"]) == 0.8,
       "SF31 the year-round out-of-region spend (%.2f per cent of card spend) carried at the output areas files the same "
       "call and figure" % (100 * yr / card_tot))
    ok("as Census 2021 counted them, not rolled forward" in model_src, "SF17 the households are the census count")
    oas0 = pk.oas
    pk.oas = [(xy, dd * 1.05) for xy, dd in oas0]
    a17 = pk.appraise(pk.v_per_pitch())
    pk.oas = oas0
    ok(tenth(a17[GOLD_SITE]["add"]) != 0.8, "SF17 households rolled forward five per cent file another figure")
    prompt = open(os.path.join(os.path.dirname(target.rstrip("/")), "prompt.txt"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(os.path.dirname(target.rstrip("/")), "prompt.txt")) else ""
    ok("once it is trading" in prompt and "a year of trading" in model_src, "SF14 no ramp: a year of trading")
    # SF15 the small parks near other sites carried alike
    ok(g["S6"]["add"] > r0["S6"]["add"], "SF15 the Sallowmere Mill park reaches S6 too")
    ok(g[GOLD_SITE]["add"] - g["S1"]["add"] > 0.2e6, "SF16 no tie")
    ok(all(0.30 <= g[k]["took"] / g[k]["new"] <= 0.37 for k in ("S2",)), "block 1: about a third of S2's sales come from "
       "ours (%.3f)" % (g["S2"]["took"] / g["S2"]["new"]))
    pdist = {r["site"]: math.dist(pk.pc[r["postcode"]], max(pk.parks, key=lambda p: p["n"])["xy"]) for r in pk.sites}
    ok(min(pdist, key=pdist.get) == GOLD_SITE, "component 1: the largest park is nearer S3 than any other site (%s)" % pdist)
    # ---- the stores and parks as they stood when the take was made (the 2023 list to its close) ---------------------
    ok("The grocery stores trading when the spend is made, each at its floor area then" in model_src,
       "SF33 the model sheet files the stores in a share: those trading when the spend is made, at their floor area then")
    hist = [ln.rstrip("\r\n").split("*") for ln in open(F["voa_hist"], encoding="utf-8", newline="") if ln.strip()]
    cur_eff = {r[6]: dt.datetime.strptime(r[15], "%d-%b-%Y").date() for r in pk.voa}
    moved = sorted({r[6] for r in pk.voa if r[6] in pk.smv and cur_eff[r[6]] > P.LIST_2026 and
                    (r[5] in P.GROCERY or pk.smv[r[6]][1] == "pitches")})
    ok(all(cur_eff[u] > P.FY[1] for u in moved), "SF34 every alteration since the card feed's year takes effect after 31 "
       "March 2026, so the year traded on one state")
    by_u = collections.defaultdict(list)
    for r in hist:
        by_u[r[6]].append((dt.datetime.strptime(r[26], "%d-%b-%Y").date(),
                           dt.datetime.strptime(r[27], "%d-%b-%Y").date() if r[27] else dt.date(9999, 1, 1)))
    ok(all(any(a <= P.FY[0] and b >= P.FY[1] for a, b in by_u[r[6]]) for r in pk.voa
           if r[5] in P.GROCERY or (r[6] in pk.smv and pk.smv[r[6]][1] == "pitches")),
       "SF34 every grocery store and park has one historic version spanning the whole card feed's year")
    for day in (dt.date(2025, 4, 1), dt.date(2025, 10, 31), dt.date(2026, 3, 31)):
        hsmv = {r["assessment_reference"]: (float(r["main_measure"]), r["unit_of_measurement"]) for r in S.rd(F["voa_hist_smv"])}
        own_pc = {r["postcode"]: str(r["store_no"]) for r in pk.estate}
        st_d, pk_d = pk.state_on(hist, hsmv, own_pc, day)
        ok(abs(pk.v_per_pitch(stores=st_d, parks=pk_d) - V) < 1e-6, "SF34 the state on %s gives the same spend per pitch" % day)
    est = {str(r["store_no"]): r for r in pk.estate}
    prev = [dict(x, a=float(est[x["id"]]["previous_floor_area_m2"])) if x["own"] and
            est[x["id"]]["previous_floor_area_m2"] and str(est[x["id"]]["floor_area_changed"])[:4] == "2026" else x
            for x in pk.stores]
    asof = {"the take inverted on today's stores and parks (the list as shipped)": pk.v_per_pitch(stores=pk.stores, parks=pk.parks),
            "the estate's previous floor areas, today's pitches": pk.v_per_pitch(stores=prev, parks=pk.parks),
            "the estate's previous floor areas, the 2025 pitches": pk.v_per_pitch(stores=prev, parks=pk.parks_2025),
            "the 2025 floor areas, today's pitches": pk.v_per_pitch(stores=pk.stores_2025, parks=pk.parks),
            "today's floor areas, the 2025 pitches": pk.v_per_pitch(stores=pk.stores, parks=pk.parks_2025)}
    for lab, v in asof.items():
        a_ = pk.appraise(v)
        w_ = max(a_, key=lambda k: a_[k]["add"])
        ok(w_ == GOLD_SITE and a_[w_]["add"] / 1e6 <= 0.69,
           "SF35 rung: %s files %s %.3f (GBP %.0f a pitch), not 0.8" % (lab, w_, a_[w_]["add"] / 1e6, v))
    a_o = pk.appraise(V, parks=pk.parks_2025)
    ok(tenth(a_o[GOLD_SITE]["add"]) <= 0.7, "SF36 the 2027 trade on the 2025 parks (Wrentoft Lakes at %d pitches, not %d) "
       "files %.3f: 2027's spend is shared among 2027's stores and parks" % (
           min(p["n"] for p in pk.parks_2025 if p["n"] > 1000), max(p["n"] for p in pk.parks), a_o[GOLD_SITE]["add"] / 1e6))
    ok(len(hist) > len(pk.voa), "SF34 the historic entries hold the 2023 list and every superseded version (%d lines)" % len(hist))
    # ---- R2: each Layer 1 item mishandled leaves the call where it is ---------------------------------------------
    term = {r["pcds"] for r in S.rd(F["onspd"]) if r["doterm"]}
    used = {r["postcode"] for r in pk.sites} | {r[14] for r in pk.voa if r[5] in P.GROCERY} | {p["pc"] for p in pk.parks}
    ok(not (term & used), "R2 no store, site or park sits on a terminated postcode")
    ok(len(term) >= 40, "R2 the extract carries terminated postcodes")
    pfs = [r for r in pk.voa if r[5].startswith("PETROL FILLING")]
    ok(len(pfs) > 3 and all(r[5] not in P.GROCERY for r in pfs), "R2 our filling stations are separate hereditaments")
    ok(all(len(r) == 28 for r in pk.voa), "R2 the list parses to 28 fields on every line")
    # ---- R3c: no plant ---------------------------------------------------------------------------------------------
    sales = [round(v) for v in act.values()]
    ok(len(set(sales)) == 10 and all(v % 1000 for v in sales), "R3c the estate's sales distinct and not round")
    ok(len({r["card_share_of_sales"] for r in pk.estate}) >= 7, "R3c card shares vary")
    pv = {s: pk.v_per_pitch(only={s}) for s in ("104", "105", "107")}
    ok(len({round(v) for v in pv.values()}) == 3, "R3c the stores' spend per pitch differs a little (%s)" % pv)
    # ---- ask A ----------------------------------------------------------------------------------------------------
    A = S.ask_a(target)
    rows, recs, at = O.tms(T, R.geography())
    weeks = 25.0
    for s in A:
        ok(round(A[s]) == round(at["cases"][s] / weeks), "ask A %s %.2f against the world" % (s, A[s]))
        ok(edge(A[s], 1.0) >= 0.015, "ask A %s clears its edge (%.2f, an exact total over exactly 25 weeks)" % (s, A[s]))
    tms = S.rd(F["tms"])
    dels = [r for r in tms if r["stop_type"] == "DEL"]
    ta = S.turned_away(dels)
    ok(len(ta) == at["refused"], "ask A the stops closed too soon for their cases are the world's turned-away loads (%d)" % len(ta))
    dwell = lambda r: (S._utc(r["depart_utc"]) - S._utc(r["arrive_utc"])).total_seconds() / 60.0
    for cut in (8.5, 9.0, 10.0):
        flat = {(r["trip_id"], r["stop_seq"]) for r in dels if dwell(r) < cut and int(r["cases"]) >= 200}
        ok(flat == ta, "SF32 ask A a flat %.1f-minute cut on loads of 200 cases or more picks the same turned-away stops" % cut)
    ok(max(dwell(r) for r in dels if (r["trip_id"], r["stop_seq"]) in ta) < min(
        dwell(r) for r in dels if (r["trip_id"], r["stop_seq"]) not in ta and int(r["cases"]) >= 200),
       "SF32 ask A every turned-away stop closes sooner than any delivered load of 200 cases or more")
    by_trip = {}
    for r in tms:
        by_trip.setdefault(r["trip_id"], []).append(r)
    single = [r for r in dels if len(by_trip[r["trip_id"]]) == 1]
    day = lambda r: S.to_local(r["arrive_utc"]).date()
    per, lone = {}, []
    for r in dels:
        if (r["trip_id"], r["stop_seq"]) in ta:
            again = [q for q in single if q["store_no"] == r["store_no"] and q["cases"] == r["cases"] and
                     (day(q) - day(r)).days == 1]
            if len(again) != 1:
                lone.append((r["store_no"], str(day(r))))
            per[r["store_no"]] = per.get(r["store_no"], 0) + 1
    ok(not lone, "ask A every turned-away load goes again the next day on a trip of its own (%s)" % lone)
    ok(sorted(per) == sorted(A) and min(per.values()) >= 1, "ask A every store turned a load away (%s)" % per)
    # law 5, the interior: the genuine next-day pairs a blanket dedup destroys, at every store
    pairs = {}
    seen = {}
    for r in sorted(dels, key=lambda r: r["arrive_utc"]):
        k = (r["store_no"], r["cases"])
        if k in seen and (day(r) - day(seen[k])).days == 1 and (seen[k]["trip_id"], seen[k]["stop_seq"]) not in ta \
                and P.TMS_FROM <= day(r) <= P.TMS_TO:
            pairs[r["store_no"]] = pairs.get(r["store_no"], 0) + 1
        seen[k] = r
    ok(sorted(pairs) == sorted(A) and min(pairs.values()) >= 2, "ask A every store has genuine same-cases next-day deliveries (%s)" % pairs)
    ok({r["status"] for r in tms} == {"COMPLETE"}, "ask A no status marks a turned-away stop")
    ok(all(int(r["cages"]) == -(-int(r["cases"]) // 55) for r in dels), "ask A cages follow cases on every stop")
    # the receipts tie under both handlings: none of the turned-away loads falls where the handhelds count
    rec = S.rd(F["receipts"])
    first_rec = {}
    for r in rec:
        d = r["received_local"][:10]
        first_rec[r["store_no"]] = min(first_rec.get(r["store_no"], d), d)
    late = [r["store_no"] for r in dels if (r["trip_id"], r["stop_seq"]) in ta and r["store_no"] in first_rec and
            str(day(r)) >= first_rec[r["store_no"]]]
    ok(not late, "ask A no turned-away load falls where the handhelds count (%s)" % late)
    for s, d0 in first_rec.items():
        n_tms = sum(1 for r in dels if r["store_no"] == s and str(day(r)) >= d0 and day(r) <= P.TMS_TO)
        n_rec = sum(1 for r in rec if r["store_no"] == s)
        ok(abs(n_tms - n_rec) <= 1, "ask A store %s: %d receipts against %d stops once the handhelds start" % (s, n_rec, n_tms))
    rc = {}
    for r in rec:
        rc[r["store_no"]] = rc.get(r["store_no"], 0) + int(r["cases"])
    ok(sum(round(rc.get(s, 0) / weeks) == round(A[s]) for s in A) == 0, "ask A the receipts alone keep no store")
    for mode in ("naive", "drop_short", "dedup_equal"):
        Am = S.ask_a(target, mode)
        ok(all(round(Am[s]) != round(A[s]) for s in A), "ask A the %s path misses all ten" % mode)
    Au = S.ask_a(target, "utc")
    ok(all(round(Au[s]) == round(A[s]) for s in A), "SF18 ask A by UK or by UTC arrival date: the same ten figures")
    # ---- ask B ----------------------------------------------------------------------------------------------------
    B = S.ask_b(target)
    shifts, punches, register, st = O.staffing(T)
    for s in B:
        ok(round(B[s]) == round(st["hours"][s] / weeks), "ask B %s %.2f against the world" % (s, B[s]))
        ok(edge(B[s], 1.0) >= 0.015, "ask B %s clears its edge (%.2f)" % (s, B[s]))
    for mode in ("location", "terminal_all", "dedup_exact", "dedup_day", "dedup_day_max", "in_days", "exact_in_days",
                 "punch_hours"):
        Bm = S.ask_b(target, mode)
        ok(all(abs(Bm.get(s, 0) - B[s]) >= 1.0 for s in B), "ask B the %s path misses all ten by an hour or more" % mode)
    lines = S.wfm_lines(target)
    pun = S.punches_by_employee(target)
    starts = S.punch_shifts(pun)
    days = S._by_day(lines)
    n_shift = sum(len(v) for v in starts.values())
    ok(n_shift == len(shifts) - st["night_lines"], "ask B the terminals' shifts are the report's lines less one a night "
       "(%d shifts, %d lines, %d nights)" % (n_shift, len(shifts), st["night_lines"]))
    extra, uneven, short = {}, [], []
    for key, g in days.items():
        k = len(starts.get(key, []))
        if len(g) < k:
            short.append(key)
        if len(g) > k:
            extra[g[0]["location"]] = extra.get(g[0]["location"], 0) + len(g) - k
            if len({r["paid_hours"] for r in g}) > 1:
                uneven.append(key)
    ok(not short, "ask B no date has more shifts than lines (%s)" % short[:2])
    ok(not uneven, "SF23 ask B a date with a night's second line carries one paid figure, so which line goes is "
       "immaterial (%s)" % uneven[:2])
    ok(sorted(extra) == sorted(B) and min(extra.values()) >= 50, "ask B every store has nights listed on the morning they "
       "end (%s)" % extra)
    ends = {}
    for key, g in days.items():
        k = len(starts.get(key, []))
        if len(g) > k and k == 0:
            ends[g[0]["location"]] = ends.get(g[0]["location"], 0) + 1
    ok(sorted(ends) == sorted(B), "ask B every store has a night's second line on a date no shift starts, the line an exact "
       "duplicate check keeps (%s)" % ends)
    eq = {}
    for key, g in days.items():
        if len(g) == 2 and len(starts.get(key, [])) == 2 and g[0]["paid_hours"] == g[1]["paid_hours"]:
            eq[g[0]["location"]] = eq.get(g[0]["location"], 0) + 1
    ok(len(eq) >= 8 and sum(eq.values()) >= 60, "ask B genuine second shifts of the same length as the first, the lines an "
       "exact duplicate check deletes (%s)" % eq)
    n_in = sum(1 for ps in pun.values() for p in ps if p[1] == "IN")
    n_out = sum(1 for ps in pun.values() for p in ps if p[1] == "OUT")
    ok(n_in < n_shift and n_out < n_shift and n_shift - n_in < 0.02 * n_shift and n_shift - n_out < 0.02 * n_shift,
       "ask B a few clock-ins and clock-outs are missing (%d and %d of %d shifts)" % (n_shift - n_in, n_shift - n_out, n_shift))
    lone_in = {}
    for e, ps in pun.items():
        opened = None
        for t, kind, store in ps:
            if kind == "OUT" and opened is None:
                lone_in[store] = lone_in.get(store, 0) + 1
            opened = (t, store) if kind == "IN" else None
    ok(sorted(lone_in) == sorted(B), "ask B every store has shifts with no clock-in, which a date with no clock-in drops "
       "(%s)" % lone_in)
    split_store = []
    for e, ps in pun.items():
        for (t0, k0, s0), (t1, k1, s1) in zip(ps, ps[1:]):
            if k0 == "IN" and k1 == "OUT" and s0 != s1:
                split_store.append(e)
    ok(not split_store, "ask B no shift is clocked in at one store and out at another (%s)" % split_store[:2])
    ok(all(P.TMS_FROM.isoformat() <= r["date"] <= P.TMS_TO.isoformat() for r in lines) and
       all(P.TMS_FROM <= p[0].date() <= P.TMS_TO for ps in pun.values() for p in ps),
       "SF19 ask B every line and punch falls inside the 25 weeks, so no shift straddles their edges")
    away, total = {}, 0
    for key, stores in starts.items():
        loc = days[key][0]["location"]
        for s_ in stores:
            total += 1
            if s_ != loc:
                away[loc] = away.get(loc, 0) + 1
    share_home = 1 - sum(away.values()) / total
    ok(0.9 <= share_home < 0.99, "ask B most shifts are worked at the colleague's location (%.3f)" % share_home)
    ok(sorted(away) == sorted(B), "ask B every location has shifts worked elsewhere (%s)" % away)
    whead = next(r for r in csv.reader(open(F["wfm"], encoding="utf-8")) if r and r[0] == "employee_no")
    ok(not [h for h in whead if any(w in h for w in ("store", "site", "worked", "version", "extract", "amend", "status",
                                                     "shift", "night", "start", "end", "seq"))],
       "ask B no column marks a worked store, a shift or a line's place in it (%s)" % whead)
    # ---- ask C ----------------------------------------------------------------------------------------------------
    C = S.ask_c(target)
    feeds, stops, bt, near, dups, seam = O.buses(T)
    ok(C == bt, "ask C %s against the world %s" % (C, bt))
    for mode in ("maxfeed", "set", "naive", "half", "nodedup"):
        Cm = S.ask_c(target, mode)
        ok(all(Cm[k] != C[k] for k in C), "ask C the %s path misses all six (%s)" % (mode, Cm))
    ok(min(dups.values()) >= 2, "ask C every site has school-day duplicate buses (%s)" % dups)
    ok(min(seam.values()) >= 2, "ask C every site has weekday journeys the Friday-late timetable lists again (%s)" % seam)
    Cs = S.ask_c(target, "set")
    ok(all(C[k] - Cs[k] == dups[k] for k in C), "SF25 ask C the duplicates are the whole gap to every same-time call once")
    Cx = S.ask_c(target, "maxfeed")
    ok(all(Cx[k] - C[k] == seam[k] for k in C), "SF24 ask C the Friday-late repeats are the whole gap to the larger feed's "
       "count of each call")
    ok(P.BUS_DAY.weekday() == 4, "ask C the day is a Friday")
    # a block is one bus: no block has two journeys at once, unless one is the other listed again (the same calls)
    for key in ("gtfs_lb", "gtfs_pdc"):
        with zipfile.ZipFile(F[key]) as z:
            R_ = lambda n: list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8")))
            trs = R_("trips.txt")
            cal_ = {r["service_id"]: r for r in R_("calendar.txt")}
            st_ = R_("stop_times.txt")
        span = {}
        pat = {}
        for r in st_:
            m = S._mins(r["departure_time"])
            a, b = span.get(r["trip_id"], (m, m))
            span[r["trip_id"]] = (min(a, m), max(b, m))
            pat.setdefault(r["trip_id"], []).append((r["stop_id"], m))
        clash = []
        for dow in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            onb = {}
            for r in trs:
                c_ = cal_.get(r["service_id"])
                if c_ is None or c_[dow] != "1":
                    continue
                onb.setdefault(r["block_id"], []).append(r["trip_id"])
            for blk, tids in onb.items():
                for i, x in enumerate(tids):
                    for y in tids[i + 1:]:
                        (a0, a1), (b0, b1) = span[x], span[y]
                        if a0 < b1 and b0 < a1 and pat[x] != pat[y]:
                            clash.append((key, dow, blk))
        ok(not clash, "ask C no bus is in two places at once (%s)" % clash[:3])
        tid_vj = [r["vehicle_journey_code"] for r in trs]
        ok(len(set(tid_vj)) == len(tid_vj), "ask C no journey code repeats inside %s, so only the block tells a repeat" % key)
    import geo
    names = {}
    for key in ("gtfs_lb", "gtfs_pdc"):
        with zipfile.ZipFile(F[key]) as z:
            R_ = lambda n: list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8")))
            st_ = R_("stop_times.txt")
            stp = {r["stop_id"]: r for r in R_("stops.txt")}
            cd = R_("calendar_dates.txt")
            fi = R_("feed_info.txt")[0]
        ok(fi["feed_start_date"] <= P.BUS_DAY.strftime("%Y%m%d") <= fi["feed_end_date"], "ask C the day is inside %s" % key)
        ok(not [r for r in cd if r["date"] in ("20270114", "20270115") and r["exception_type"] == "2"],
           "ask C no service is removed on the Thursday or the Friday (%s)" % key)
        differ = [k for k, r in stp.items() if k in names and names[k] != (r["stop_name"], r["stop_lat"], r["stop_lon"])]
        ok(not differ, "ask C both feeds give a shared stop alike (%s)" % differ[:3])
        shared = len([k for k in stp if k in names])
        for k, r in stp.items():
            names[k] = (r["stop_name"], r["stop_lat"], r["stop_lon"])
        ok(key == "gtfs_lb" or shared >= 50, "ask C the two feeds share the NaPTAN stops of the joint routes (%d)" % shared)
        last, calls = {}, {}
        for r in st_:
            if r["trip_id"] not in last or int(r["stop_sequence"]) > int(last[r["trip_id"]]["stop_sequence"]):
                last[r["trip_id"]] = r
        ok(all(r["pickup_type"] == "1" for r in last.values()), "SF20 every trip's final stop is set down only (%s)" % key)
        for r in pk.sites:
            ll = geo.bng_to_wgs84(*pk.pc[r["postcode"]])
            dd = {k: geo.haversine_m(float(v["stop_lat"]), float(v["stop_lon"]), *ll) for k, v in stp.items()}
            ok(not [x for x in dd.values() if 360 <= x <= 440], "SF21 no stop within 360 to 440 m of %s (%s)" % (r["site"], key))
            for q in st_:
                if q["pickup_type"] != "1" and dd[q["stop_id"]] <= P.BUS_RADIUS:
                    calls[(q["trip_id"], r["site"])] = calls.get((q["trip_id"], r["site"]), 0) + 1
        ok(max(calls.values()) == 1, "SF22 ask C no trip departs twice within 400 m of a site, so departures and journeys "
                                     "agree (%s)" % key)
    # ---- separation and the input gates -----------------------------------------------------------------------------
    src = open(os.path.join(HERE, "solve.py"), encoding="utf-8").read()
    call_src = src.split("# ----------------------------------------------------------------- ask A")[0]
    for k in ("tms", "receipts", "wfm", "punches", "terminals", "gtfs_lb", "gtfs_pdc"):
        ok('F["%s"]' % k not in call_src, "separation: the call reads no %s" % k)
    for k in DISTRACTORS:
        ok('"%s"' % k not in src, "distractor %s unread" % k)
    files = walk(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8", errors="ignore")) for f in files if f.endswith((".csv", ".txt")))
    ok(big >= 25000, "input gates: a file of %d rows" % big)
    print("checks: %d passed (call %s %.3f at %.1f a pitch; resident route %s)" % (N, c["site"], c["add"] / 1e6, V, c["resident_site"]))
    return 0


DISTRACTORS = ("aadf", "survey")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
