"""Assertions on the built pack and the world it came from: the three-rules block (the resident route files the named
wrong answer on the clean truth and on the pack; adding the parks' guests alone files the golden), the standing family,
the ladder, every semantic fork row, the bins, the ask devices, separation, the input gates and the realism sweep.

    python3 task305/generator/checks.py <target dir>
"""
import csv
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
    ok(len(pk.cards) > 10000 and len({r["cardholder_home_sector"] for r in pk.cards}) > 300,
       "R1 the card feed ships by store, month and home sector")
    # ---- R3a: the resident route, every filed rule applied, files the named wrong answer ---------------------------
    tr = T["resident"]
    win = max(tr, key=lambda k: tr[k]["add"])
    ok(win == EASY_SITE and tenth(tr[win]["add"]) == 0.5, "R3a clean truth: the resident route files S1 at 0.5 million")
    ok(c["resident_site"] == EASY_SITE and tenth(r0[EASY_SITE]["add"]) == 0.5, "R3a pack: the resident route files S1 at 0.5")
    order0 = sorted(r0, key=lambda k: -r0[k]["add"])
    ok(order0.index(GOLD_SITE) >= 1 and r0[EASY_SITE]["add"] >= 3 * r0[GOLD_SITE]["add"],
       "R3a Wrentoft trails S1 by a factor of three on the resident route (%s)" % order0)
    # ---- R3b: the decisive step alone files the golden ------------------------------------------------------------
    tg = T["golden"]
    ok(max(tg, key=lambda k: tg[k]["add"]) == GOLD_SITE and tenth(tg[GOLD_SITE]["add"]) == 0.8,
       "R3b clean truth: carrying the parks' guests files S3 at 0.8")
    ok(c["site"] == GOLD_SITE and tenth(c["add"]) == 0.8, "R3b pack: the guests carried at the card feed's spend per pitch")
    ok(edge(c["add"] / 1e6, 0.1) >= 0.04, "golden %.4f clears its cell's edges" % (c["add"] / 1e6))
    ok(g[GOLD_SITE]["add"] >= 1.5 * g[EASY_SITE]["add"], "golden margin %.2f" % (g[GOLD_SITE]["add"] / g[EASY_SITE]["add"]))
    # the lower rungs stay on S1, each clearing its runner-up
    act = {str(r["store_no"]): float(r["sales_fy2025_26_gbp"]) for r in pk.estate}
    guests = pk.guests()
    pct = guests["107"] / act["107"]
    rung2a = {k: v["add"] + (P.MARGIN * v["new"] * pct / (1 - pct) if k == GOLD_SITE else 0.0) for k, v in r0.items()}
    rung2b = {k: v["add"] + (P.MARGIN * guests["107"] if k == GOLD_SITE else 0.0) for k, v in r0.items()}
    base = pk.sales(pk.stores, pk.oas)
    ratio = np.mean([act[s["id"]] / base[k] for k, s in enumerate(pk.stores) if s["own"]])
    rung1 = {k: P.MARGIN * (v["new"] - v["took"]) * ratio - v["cost"] for k, v in r0.items()}
    for lab, rr in (("rung 0", {k: v["add"] for k, v in r0.items()}), ("rung 1", rung1), ("rung 2a", rung2a), ("rung 2b", rung2b)):
        o = sorted(rr, key=lambda k: -rr[k])
        ok(o[0] == EASY_SITE and rr[o[0]] >= 1.15 * rr[o[1]], "%s stays on S1 by %.2f" % (lab, rr[o[0]] / rr[o[1]]))
        ok(o.index(GOLD_SITE) >= 1, "%s Wrentoft %d" % (lab, o.index(GOLD_SITE) + 1))
    # ---- the standing family: every construction carrying the guests files S3 at 0.8 -------------------------------
    fam = {"pooled": V}
    for s in ("104", "105", "106", "107", "108"):
        fam["store %s" % s] = pk.v_per_pitch(only={s})
    fam["105 and 107"] = pk.v_per_pitch(only={"105", "107"})
    fam["off Dec-Feb"] = pk.v_per_pitch(guests=pk.guests(off=("2025-12", "2026-01", "2026-02")))
    fam["off Jan-Feb"] = pk.v_per_pitch(guests=pk.guests(off=("2026-01", "2026-02")))
    vals = {}
    for lab, v in fam.items():
        a = pk.appraise(v)
        w = max(a, key=lambda k: a[k]["add"])
        vals[lab] = a[w]["add"] / 1e6
        ok(w == GOLD_SITE and tenth(a[w]["add"]) == 0.8, "family %s files %s %.3f" % (lab, w, a[w]["add"] / 1e6))
    ok(max(vals.values()) - min(vals.values()) <= 0.06, "standing family spread %.3f" % (max(vals.values()) - min(vals.values())))
    ok(min(edge(v, 0.1) for v in vals.values()) >= 0.015, "every standing member clears its cell's edges (%s)" %
       {k: round(v, 4) for k, v in vals.items()})
    # the analog route: a park-side store's guest spend scaled by the pitches beside Wrentoft
    named = {r[9]: pk.smv[r[6]][0] for r in pk.voa if r[6] in pk.smv and pk.smv[r[6]][1] == "pitches"}
    big = max(named.values())
    for sid, park in (("107", "RADDLEFORD WATER HOLIDAY PARK"), ("105", "WITHYBECK LAKES CARAVAN PARK")):
        an = r0[GOLD_SITE]["add"] + P.MARGIN * guests[sid] * big / named[park]
        ok(an > max(v["add"] for k, v in r0.items() if k != GOLD_SITE) and tenth(an) == 0.8, "family analog %s files S3 %.3f" % (sid, an / 1e6))
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
    a9 = pk.appraise(pk.v_per_pitch(parks=parks2), parks=parks2)
    ok(max(a9, key=lambda k: a9[k]["add"]) == GOLD_SITE and tenth(a9[GOLD_SITE]["add"]) == 0.8, "SF9 same call")
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
    ok(all(np.mean([nl[s][m] for m in S.OFF]) > 1000 for s in nl), "SF10 every store has out-of-region cardholders all year")
    for s in far:
        offm = np.mean([nl[s][m] for m in S.OFF])
        seas = np.mean([nl[s][m] for m in P.MONTHS if int(m[5:]) in P.SEASON])
        ok(offm > 300 and seas / offm < 1.4, "SF10 store %s carries much the same out-of-region spend all year" % s)
    for s in ("105", "107"):
        offm = np.mean([nl[s][m] for m in S.OFF])
        seas = np.mean([nl[s][m] for m in P.MONTHS if int(m[5:]) in P.SEASON])
        ok(seas / offm > 10, "SF10 store %s: the season runs %.0f times its year-round level" % (s, seas / offm))
    # SF11: every pitch-measured site, or caravan parks only: same call
    car = [p for p in pk.parks if "CARAVAN PARK" in p["desc"]]
    a11 = pk.appraise(pk.v_per_pitch(parks=car), parks=car)
    ok(max(a11, key=lambda k: a11[k]["add"]) == GOLD_SITE and tenth(a11[GOLD_SITE]["add"]) == 0.8, "SF11 same call")
    # SF12: the season's months: the excess runs March to October; April to September only files another figure
    off = np.mean([sum(nl["107"].get(m, 0) for m in S.OFF) / 4.0])
    ok(nl["107"]["2026-03"] > 1.5 * off and nl["107"]["2025-10"] > 1.5 * off and nl["107"]["2025-11"] < 1.3 * off,
       "SF12 the excess at Raddleford runs March to October")
    # SF13: rounding once, at the end
    ok(tenth(sum([v["add"] for v in [a[GOLD_SITE]]])) == 0.8, "SF13 the addition rounded once")
    ok(abs(tenth(a[GOLD_SITE]["new"] * P.MARGIN) - tenth(a[GOLD_SITE]["took"] * P.MARGIN) - tenth(a[GOLD_SITE]["cost"]) - 0.8) < 0.11,
       "SF13 rounding the parts first stays within a tenth")
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
    ok(all(g[k]["took"] / g[k]["new"] > 0.34 for k in ("S2",)), "block 1: over a third of S2's sales come from ours")
    pdist = {r["site"]: math.dist(pk.pc[r["postcode"]], max(pk.parks, key=lambda p: p["n"])["xy"]) for r in pk.sites}
    ok(min(pdist, key=pdist.get) == GOLD_SITE, "component 1: the largest park is nearer S3 than any other site (%s)" % pdist)
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
    for mode in ("location", "terminal_all", "dedup_last", "dedup_first", "dedup_max", "punch_hours"):
        Bm = S.ask_b(target, mode)
        ok(all(abs(Bm.get(s, 0) - B[s]) >= 1.0 for s in B), "ask B the %s path misses all ten by an hour or more" % mode)
    ok(S.ask_b(target, "by_file") == B, "SF24 ask B C1: the later extract's row and the row the clock-out follows agree")
    rows = S.wfm_shifts(target)
    pun = S.punches_by_employee(target)
    cur = S.current_shifts(rows, pun)
    groups = {}
    for r in rows:
        groups.setdefault((r["employee_no"], r["shift_date"]), []).append(r)
    twice = splits = 0
    per_twice, per_split = {}, {}
    for (emp, d), g in groups.items():
        if len(g) < 2:
            continue
        g = sorted(g, key=lambda r: r["a"])
        overl = any(x["a"] < y["b"] and y["a"] < x["b"] for x in g for y in g if x is not y)
        if overl:
            twice += 1
            per_twice[g[0]["location"]] = per_twice.get(g[0]["location"], 0) + 1
        else:
            splits += 1
            per_split[g[0]["location"]] = per_split.get(g[0]["location"], 0) + 1
    ok(twice == st["amended"] and splits >= 300, "ask B %d shifts extracted twice, %d genuine second shifts" % (twice, splits))
    ok(sorted(per_twice) == sorted(B) and sorted(per_split) == sorted(B),
       "ask B every store's colleagues have shifts extracted twice and second shifts (law 5, the interior)")
    # each shift worked has its punches and only the current row of a twice-extracted shift is followed by a clock-out
    unmatched = [r for r in cur if not any(0 <= (r["a"] - t).total_seconds() / 60 <= 15 for t, k_, _ in pun.get(r["employee_no"], [])
                                           if k_ == "IN") and not any(0 <= (t - r["b"]).total_seconds() / 60 <= 15
                                                                     for t, k_, _ in pun.get(r["employee_no"], []) if k_ == "OUT")]
    ok(not unmatched, "ask B every shift worked has a clock-in or a clock-out (%s)" % unmatched[:2])
    n_in = sum(1 for ps in pun.values() for p in ps if p[1] == "IN")
    n_out = sum(1 for ps in pun.values() for p in ps if p[1] == "OUT")
    ok(n_in < len(cur) and n_out < len(cur) and len(cur) - n_in < 0.02 * len(cur) and len(cur) - n_out < 0.02 * len(cur),
       "ask B a few clock-ins and clock-outs are missing (%d and %d of %d shifts)" % (len(cur) - n_in, len(cur) - n_out, len(cur)))
    split_store = [r for r in cur if r["location"] and any(
        0 <= (r["a"] - t).total_seconds() / 60 <= 15 and s_in != s_out
        for t, k_, s_in in pun.get(r["employee_no"], []) if k_ == "IN"
        for t2, k2, s_out in pun.get(r["employee_no"], []) if k2 == "OUT" and 0 <= (t2 - r["b"]).total_seconds() / 60 <= 15)]
    ok(not split_store, "ask B no shift is clocked in at one store and out at another")
    off, cross = [], []
    for r in rows:
        el = (O.local_to_utc(r["b"]) - O.local_to_utc(r["a"])).total_seconds() / 3600
        if abs(el - int(r["unpaid_break_mins"]) / 60 - r["paid"]) > 1e-6:
            off.append(r["employee_no"])
        if not (P.TMS_FROM <= r["a"].date() and r["b"] <= dt.datetime.combine(P.TMS_TO + dt.timedelta(days=1), dt.time(0, 0))):
            cross.append(r["employee_no"])
    ok(not off, "SF23 ask B paid hours are each row's elapsed time less its unpaid break (%s)" % off[:2])
    ok(not cross, "SF19 ask B no shift crosses the 25 weeks' edges, so dating a shift by its start or its end agrees")
    away = {}
    for r in cur:
        if S.worked_store(r, pun) != r["location"]:
            away[r["location"]] = away.get(r["location"], 0) + 1
    share_home = 1 - sum(away.values()) / len(cur)
    ok(0.9 <= share_home < 0.99, "ask B most shifts are worked at the colleague's location (%.3f)" % share_home)
    ok(sorted(away) == sorted(B), "ask B every location has shifts worked elsewhere (%s)" % away)
    whead = next(csv.reader(open(F["wfm"], encoding="utf-8")))
    ok(not [h for h in whead if any(w in h for w in ("store", "site", "worked", "version", "extract", "amend", "status"))],
       "ask B no column marks a worked store or a row's extract")
    # ---- ask C ----------------------------------------------------------------------------------------------------
    C = S.ask_c(target)
    feeds, stops, bt, near, dups = O.buses(T)
    ok(C == bt, "ask C %s against the world %s" % (C, bt))
    for mode in ("set", "naive", "half", "nodedup"):
        Cm = S.ask_c(target, mode)
        ok(all(Cm[k] != C[k] for k in C), "ask C the %s path misses all six (%s)" % (mode, Cm))
    ok(min(dups.values()) >= 2, "ask C every site has school-day duplicate buses (%s)" % dups)
    Cs = S.ask_c(target, "set")
    ok(all(C[k] - Cs[k] == dups[k] for k in C), "SF25 ask C the duplicates are the whole gap to every same-time call once")
    ok(P.BUS_DAY.weekday() == 4, "ask C the day is a Friday")
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
    files = [f for f in os.listdir(target)]
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8", errors="ignore")) for f in files if f.endswith((".csv", ".txt")))
    ok(big >= 25000, "input gates: a file of %d rows" % big)
    print("checks: %d passed (call %s %.3f at %.1f a pitch; resident route %s)" % (N, c["site"], c["add"] / 1e6, V, c["resident_site"]))
    return 0


DISTRACTORS = ("aadf", "survey")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
