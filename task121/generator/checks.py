"""Generator checks for task121, run on every build: the linkage against the world, the call and its family, the
ladder, the three rules (R1 to R3), each Layer 1 item mishandled, the semantic fork rows, the separation of the asks'
devices from the call, the asks' devices against their stops, the input gates and the realism sweep."""
from __future__ import annotations

import datetime as dt
import os
import re

import numpy as np

import analysis as A
import common as K
import routes as RT

FAILS = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        FAILS.append(label)
    print("%s %s %s" % ("PASS" if cond else "FAIL", label, detail))


def pdf_text(path):
    import subprocess
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return ""


def whole(x):
    return int(np.floor(x + 0.5))


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w, sv = b["w"], b["sv"]
    D, J, c = res["D"], res["J"], res["call"]
    top, pts = c["top"], c["points"]
    gold = (top, c["top_points"])

    # ------------------------------------------------------------------ the linkage against the world
    truth = {x["serial"]: x for x in sv.resp}
    miss = 0
    for r in J.itertuples():
        x = truth[r.serial]
        miss += (r.crowded != int(x["crowded"])) + (r.late != int(x["late"])) + (r.unstaffed != int(x["unstaffed"])) \
            + (abs(r.fare - x["fare"]) > 1e-9)
    ok("LINK every questionnaire's four conditions recovered from the shipped records", miss == 0,
       "%d mismatches over %d" % (miss, len(J)))
    for col in ("crowded", "late", "unstaffed"):
        n = sum(getattr(r, col) != int(truth[r.serial][col]) for r in J.itertuples())
        ok("LINK %s recovered for every questionnaire" % col, n == 0, str(n))
    tw = {}
    for wave in (2025, 2026):
        xs = [x for x in sv.resp if x["wave"] == wave]
        ww = np.array([x["weight"] for x in xs])
        tw[wave] = {k: float(np.average([float(x[k]) for x in xs], weights=ww)) for k in ("crowded", "late", "unstaffed", "fare")}
    true_pts = {nm: -K.EFFECT[col if col != "fare" else "fare"] * (tw[2026][col] - tw[2025][col]) *
                (100 if col != "fare" else 100) for nm, col in
                [("crowding", "crowded"), ("punctuality", "late"), ("on-board staffing", "unstaffed"), ("fares", "fare")]}
    true_top = max(true_pts, key=true_pts.get)
    ok("CALL the world's own effects name the golden driver", true_top == top, "%s %s" % (true_top, true_pts))
    ok("CALL the world's own effects give the golden's whole points", whole(true_pts[top]) == c["top_points"],
       "%.2f" % true_pts[top])
    ok("CALL crowding, 3 points", gold == ("crowding", 3), str(gold))
    second = sorted(pts.values())[-2]
    ok("CALL the second driver sits 1.5 points or more below", pts[top] - second >= 1.5,
       "%.2f against %.2f" % (pts[top], second))

    # ------------------------------------------------------------------ the golden family
    fam = RT.golden_family(J)
    fam["logit"] = RT.logit_family(J)
    fam["stratified"] = dict(RT.stratified(J), fares=pts["fares"])
    for k, p in fam.items():
        t = max(p, key=p.get)
        ok("FAMILY %s files %s, %d points" % (k, t, whole(p[t])), (t, whole(p[t])) == gold,
           str({d: round(v, 2) for d, v in p.items()}))
        bridge = {d: whole(v) for d, v in p.items()}
        ok("FAMILY %s gives the golden bridge's whole points" % k,
           all(bridge[d] == fig["bridge_points"][d] for d in bridge), str(bridge))
    lo = min(p["crowding"] for p in fam.values())
    hi = max(p["crowding"] for p in fam.values())
    ok("MARGIN the family's crowding points sit 0.25 or more inside 2.5 and 3.5", lo >= 2.75 and hi <= 3.25,
       "%.2f to %.2f" % (lo, hi))
    edges = [abs(v - np.floor(v) - 0.5) for p in fam.values() for v in p.values()]
    ok("MARGIN every family member's bridge entry sits 0.03 or more from a half point", min(edges) >= 0.03,
       "%.3f" % min(edges))
    fall = c["shares"]["fall"]
    ok("MARGIN the shares sit off a rounding edge (no exclusion applies to Q1, so every route reads the same rows)",
       min(abs(v * 10 - np.floor(v * 10) - 0.5) for v in c["shares"]["overall"].values()) >= 0.01 and
       int(J["q1"].isna().sum()) == 0 and len(J) == len(D["resp"]), str(c["shares"]["overall"]))

    # ------------------------------------------------------------------ the ladder
    for mp in RT.MAPS:
        for outcome in ("q1", "sat"):
            for imp in ("regression", "correlation"):
                p = RT.kda(D, J, mapping=mp, outcome=outcome, importance=imp)
                ok("LADDER R0 derived importance (%s items, %s, %s) files on-board staffing" % (mp, outcome, imp),
                   RT.top(p) == "on-board staffing", str({k: round(v, 2) for k, v in p.items()}))
    r0 = RT.kda(D, J)
    ok("LADDER the default path (R0 as worded) ends on on-board staffing, 2 points",
       (RT.top(r0), whole(r0[RT.top(r0)])) == ("on-board staffing", 2), str(r0))
    r1 = RT.kitchen_sink(D, J)
    ok("LADDER R1 the conditions with the ratings as controls credit crowding with 1 point",
       (RT.top(r1), whole(r1[RT.top(r1)])) == ("crowding", 1), str({k: round(v, 2) for k, v in r1.items()}))
    ok("LADDER R1 books on-board staffing below nothing (the ratings absorb it)", r1["on-board staffing"] < 0)
    for mp in RT.MAPS:
        p = RT.kitchen_sink(D, J, mapping=mp)
        ok("LADDER R1 with the ratings booked to drivers (%s) stays off the golden" % mp,
           (RT.top(p), whole(p[RT.top(p)])) != gold, str({k: round(v, 2) for k, v in p.items()}))
    r2 = RT.cascade_did(J)
    ok("LADDER R2 the cascade groups against the rest credit crowding with no whole point",
       whole(r2["credited_to_crowding"]) == 0, str(r2))
    largest = min(RT.ITEMS, key=lambda q: fig_rating_fall(D, J, q))
    ok("LADDER the topline's largest fall is on-board staff availability (Q5F)", largest == "q5f", largest)

    # ------------------------------------------------------------------ the three rules
    head = open(os.path.join(target, K.FILES["responses"]), encoding="utf-8").readline().strip().split(",")
    ok("R1 the responses ship the verdict, the ten ratings and the written-in journey, no condition",
       "q1_overall" in head and all(q in head for q in RT.ITEMS) and
       not [h for h in head if re.search(r"crowd|late|staff|seat|load|delay", h)], str(head))
    heads = []
    for f in os.listdir(target):
        if f.endswith(".csv"):
            heads += open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
    ok("R1 no shipped column holds a driver's points, an effect or a respondent's condition",
       not [h for h in heads if re.search(r"crowded|importance|effect|driver|points|standing", h)], "")
    for lbl, kw in (("lateness at the train's destination", dict(late_at="destination")),
                    ("the whole run's busiest leg", dict(legs="run")),
                    ("coded stations only (written-in names dropped)", dict(codes_only=True))):
        cc = A.call(A.journeys(D, **kw))
        ok("R2 Layer 1: %s leaves the call" % lbl, (cc["top"], cc["top_points"]) == gold,
           "%s %d" % (cc["top"], cc["top_points"]))
    for lbl, kw in (("the leading unit's seats only", dict(seats_by="lead")),
                    ("one vehicle per class 166", dict(vehicles="first"))):
        cc = A.call(A.journeys(D, **kw))
        ok("R2 Layer 1: %s keeps crowding on top, the points move" % lbl,
           cc["top"] == top and cc["top_points"] != c["top_points"], "%s %d" % (cc["top"], cc["top_points"]))
    ok("R3a analyst test: every rule read, the tracker's driver analysis files on-board staffing",
       RT.top(r0) == "on-board staffing" and top != "on-board staffing")
    ok("R3b the decisive step alone (the conditions, no ratings) files the golden by every family member",
       all(max(p, key=p.get) == top for p in fam.values()))
    ok("R3b the conditions beside the ratings (R1) and the cascade comparison (R2) stay off the golden",
       whole(r1[RT.top(r1)]) != c["top_points"] and whole(r2["credited_to_crowding"]) != c["top_points"])
    docs = "".join(pdf_text(os.path.join(target, K.FILES[k])) for k in ("technote", "topline", "requirement", "standards"))
    ok("R3c no document names an importance, a halo, a driver analysis or a driver's share of the fall",
       not re.search(r"importance|halo|key driver|driver analysis|derived|share of the fall", docs, re.I))
    ok("R3c the requirement files the counterfactual, never a method",
       "would have fallen less had passengers' journeys met that driver as they did in spring 2025" in
       re.sub(r"\s+", " ", docs) and not re.search(r"regress|model|weighted least", docs, re.I))
    ok("R3c the topline reports the ratings without ranking the drivers",
       "accounts for" not in pdf_text(os.path.join(target, K.FILES["topline"])))

    # ------------------------------------------------------------------ semantic fork rows
    flat = re.sub(r"\s+", " ", docs)
    ok("SF1 satisfied is codes 4 and 5 (technical note 6)", "codes 4 and 5" in flat)
    ok("SF2 the share is weighted, of those who answered (technical note 5 and 6; letter)",
       "All results the agency reports are weighted" in flat and "of those who answered the question" in flat
       and "as the tracker reports it" in flat)
    cc = A.call(A.journeys(D, late_at="destination"))
    ok("SF3 lateness at the passenger's station (3.1(b)) or the destination, same call",
       "at the passenger's station five minutes or more" in flat and (cc["top"], cc["top_points"]) == gold)
    cc = A.call(A.journeys(D, legs="run"))
    ok("SF4 crowding on any leg of the journey (3.1(a)) or the run's busiest leg, same call",
       "between any two consecutive stations of the passenger's journey" in flat and
       (cc["top"], cc["top_points"]) == gold)
    ok("SF5 seats are the standard seats of the units formed (3.1(a), 2.3); the units carry no first class",
       "standard-class seats" in flat and set(D["units"]["Standard seats"]) <= {116, 138, 232})
    ok("SF6 no as-worked row is a train without on-board staff (field notes)",
       "One row per train worked by a member of on-board staff" in open(os.path.join(target, K.FILES["dictionary"])).read())
    ok("SF7 fares: the ticket type's change on the flow, nothing in spring 2025 (3.1(d))",
       "the change, in per cent, in the price of the passenger's ticket" in flat)
    ok("SF8 pooled, per-wave or logit effects, same call and bridge",
       all(max(p, key=p.get) == top for k, p in fam.items()))
    ok("SF9 service group and time band held or not, same call", max(fam["pooled+controls"], key=fam["pooled+controls"].get) == top)
    ok("SF10 the other three as they were: additive effects, the order of the drivers moves nothing",
       abs(sum(pts.values()) + c["unexplained"] - fall) < 1e-9)
    ok("SF11 a blank Q1 leaves the base (technical note 6); none blank", int(J["q1"].isna().sum()) == 0)
    gf = [d for d in K.BANK_HOLIDAYS if d in K.WINDOWS["w2026"]]
    nb = int(D["field"]["fieldwork_date"].isin([d.isoformat() for d in gf]).sum())
    ok("SF12 Good Friday and Easter Monday 2026 run the Sunday schedules (field notes); their batches link",
       nb > 0 and "Bank holidays run the SUN schedules" in open(os.path.join(target, K.FILES["dictionary"])).read(),
       str(nb))
    ok("SF13 every respondent's stations lie on their train's calling pattern, the boarding one first",
       bool((J["board"] != J["alight"]).all()) and len(J) == len(D["resp"]))
    ok("SF14 points to the nearest whole point, shares to one decimal (prompt); the bridge rows rounded alone",
       fig["call"]["points"] == whole(pts[top]))
    st_bh, n_bh = A.ask_standing(D, bank_holiday=True)
    st, n_st = A.ask_standing(D)
    ok("SF15 Bank Holiday Monday's Sunday trains read as a weekday's or not, the same standing",
       st_bh == st and n_bh != n_st, "%s / %s" % (n_bh, n_st))
    ok("SF16 the day's trains on the bank holiday are the Sunday schedules (field notes)",
       A.ask_ontime(D, days_of=A.calendar_days)[0] != res["ontime"])
    am = D["amend"]
    ro = {(r.roster_date, r.diagram): r for r in D["roster"].itertuples()}
    good = 0
    for r in am.itertuples():
        day = dt.date.fromisoformat(r.amend_date)
        if A.mins(r.logged) >= 12 * 60:
            day += dt.timedelta(days=1)
        t = ro.get((day.isoformat(), r.diagram))
        same = ro.get((r.amend_date, r.diagram))
        orig = "" if not isinstance(r.original_staff_ref, str) else r.original_staff_ref
        fits = t is not None and t.status in ("Sick", "Vacant") and (orig == (t.staff_ref if isinstance(t.staff_ref, str) else ""))
        if A.mins(r.logged) >= 12 * 60:
            fits = fits and (same is None or same.status == "Rostered" or
                             (isinstance(same.staff_ref, str) and same.staff_ref != orig))
        good += fits
    ok("SF17 every amendment fits exactly one turn: the morning's that day, the evening's the next day",
       good == len(am), "%d of %d" % (good, len(am)))
    ok("SF18 an arrival after midnight is the train's run date (field notes: a train is its headcode on its run date)",
       "train is its train identity (headcode) on its run date" in open(os.path.join(target, K.FILES["dictionary"])).read())

    # ------------------------------------------------------------------ separation of the asks from the call
    mv = D["mv"]
    arrj = {(r.run_date, r.train_uid, r.station): (r.wtt_time, r.recorded_time) for r in mv[mv["event_type"] == "ARRIVAL"].itertuples()}
    fw = D["field"].set_index("batch_id")
    cross = 0
    tr = A.train_index(D)
    for r in J.itertuples():
        b_ = fw.loc[D["resp"].set_index("serial").loc[r.serial, "batch_id"]]
        d = b_["fieldwork_date"]
        t = tr[(A.which_tt(d), b_["train_headcode"], A.days_label(d), b_["origin_station"], b_["origin_dep"])]
        pl, ac = arrj[(d, t["uid"], r.alight)]
        cross += abs(A.mins(ac) - A.mins(pl)) > 600
    ok("SEP no surveyed journey's arrival crosses midnight", cross == 0, str(cross))
    late_uids = {t["uid"] for t in w.tt["Dec24"].trains + w.tt["Dec25"].trains if t["calls"][-1][1] > 23 * 60 + 45}
    sampled = {bb["uid"] for bb in sv.batches}
    ok("SEP no fieldwork batch rode a train due after 23:45", not (late_uids & sampled), str(len(late_uids)))
    ok("SEP the amendments and the roster cover the baseline weeks only",
       D["amend"]["amend_date"].min() >= "2026-08-22" and D["roster"]["roster_date"].min() >= "2026-08-23")
    refurb_first = min(dt.date.fromisoformat(str(x)) for x in D["mods"]["Out of service"])
    ok("SEP the interior refresh began after the spring 2026 wave", refurb_first > K.WAVES[2026][1], str(refurb_first))
    J2 = A.journeys(D)
    ok("SEP the call reads no roster, amendment or modification (rebuilt without them, the same)",
       A.call(J2)["points"] == pts)

    # ------------------------------------------------------------------ the asks' devices
    gon = res["ontime"]
    for lbl, kw, need in (("clock times subtracted across midnight", dict(midnight=False), 5),
                          ("the trains with movement rows as the base", dict(base="ran"), 5),
                          ("the calendar's weekday on the bank holiday", dict(days_of=A.calendar_days), 5)):
        v = A.ask_ontime(D, **kw)[0]
        n = sum(round(v[g], 1) != round(gon[g], 1) for g in K.GROUP_ORDER)
        ok("DEVICE on time: %s moves %d of 5 groups" % (lbl, n), n >= need, str({g: round(x, 1) for g, x in v.items()}))
    gst = res["staffed"]
    for lbl, kw, need in (("amendments read on their log date", dict(cover_by="date"), 4),
                          ("amendments ignored", dict(cover_by=None), 5),
                          ("only trains that reached their destination", dict(ran_by="arrived"), 3)):
        v = A.ask_staffed(D, **kw)[0]
        n = sum(round(v[g], 1) != round(gst[g], 1) for g in K.GROUP_ORDER)
        ok("DEVICE staffed: %s moves %d of 5 groups" % (lbl, n), n >= need, str({g: round(x, 1) for g, x in v.items()}))
    for lbl, kw, need in (("the rows under the train's headcode summed", dict(key="headcode"), 4),
                          ("every class 166 vehicle row summed after the system move", dict(vehicles="sum"), 1),
                          ("the register's seats without the modifications", dict(mods=False), 2),
                          ("the leading unit's seats only", dict(seats_by="lead"), 3)):
        v = A.ask_standing(D, **kw)[0]
        n = sum(v[g] != st[g] for g in K.INTO_MVC)
        ok("DEVICE standing: %s moves %d of 4 groups" % (lbl, n), n >= need, str(v))
    crossing = sum(1 for d, uid, t in A.timetabled(D, A.latest_days())
                   if (d, uid, t["calls"][-1]) in arrj and A.mins(arrj[(d, uid, t["calls"][-1])][1]) -
                   A.mins(t["arr"][-1]) < -600)
    ok("FAIR every late-evening arrival after midnight is a train due before it (no early arrival across)",
       crossing > 0 and all(A.mins(t["arr"][-1]) >= 23 * 60 for d, uid, t in A.timetabled(D, A.latest_days())
                            if (d, uid, t["calls"][-1]) in arrj and
                            abs(A.mins(arrj[(d, uid, t["calls"][-1])][1]) - A.mins(t["arr"][-1])) > 600), str(crossing))
    ok("SILENT the cover entries logged in the evening sit among the morning ones (no flag column)",
       0 < int((am["logged"].map(A.mins) >= 720).sum()) < len(am) and list(am.columns) ==
       ["amend_date", "diagram", "original_staff_ref", "cover_staff_ref", "reason", "logged"])

    # ------------------------------------------------------------------ input gates
    files = os.listdir(target)
    ok("GATE ten or more files", len(files) >= 10, str(len(files)))
    ok("GATE three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3,
       str(sorted({f.rsplit(".", 1)[1] for f in files})))
    ok("GATE a file of 25,000 rows or more", b["counts"]["movements"] >= 25000, str(b["counts"]["movements"]))
    ok("GATE two or more distractors", len(K.DISTRACTORS) >= 2)
    ok("GATE no file name names the stump", not [f for f in files if re.search(r"halo|driver|importance|link", f, re.I)])

    # ------------------------------------------------------------------ realism sweep
    text = ""
    for f in files:
        if f.endswith((".csv", ".txt")):
            text += open(os.path.join(target, f), encoding="utf-8").read()
        elif f.endswith(".pdf"):
            text += pdf_text(os.path.join(target, f))
    ok("REAL no em dash in the pack", "—" not in text)
    ok("REAL every persona named in the pack is drawn", all(p in text for p in
                                                            (K.PEOPLE["contract"], K.PEOPLE["agency"],
                                                             K.PEOPLE["authority"])))
    ok("REAL the topline's overall shares are the golden's at whole per cents",
       "%.0f%%" % c["shares"]["overall"][2025] in text and "%.0f%%" % c["shares"]["overall"][2026] in text)
    ok("REAL no standing figure is a round hundred", all(v % 100 for v in st.values()), str(st))
    lwr = D["lw"]
    uid_of = {(r.run_date, r.headcode): r.train_uid for r in D["form"].itertuples()}
    depm = {(r.run_date, r.train_uid, r.station): r.recorded_time for r in D["mv"][D["mv"]["event_type"] == "DEPARTURE"].itertuples()}
    stale = [r for r in lwr.itertuples()
             if depm.get((r.run_date, uid_of.get((r.run_date, r.headcode)), r.station)) != r.departed]
    early = [r for r in stale if r.run_date < K.CREW_SYSTEM_MOVE.isoformat()]
    trip = lwr[lwr["vehicle"].notna()].groupby(["run_date", "unit_no", "station", "departed"])["passengers_est"].agg(
        ["nunique", "count", "max"]).reset_index()
    move = K.CREW_SYSTEM_MOVE.isoformat()
    before = trip[trip["run_date"] < move]
    after = trip[trip["run_date"] >= move]
    chance = int(((before["nunique"] == 1) & (before["max"] > 0)).sum())
    ok("SEP the class 166 rows written three times sit after the May 2026 move; the waves' 166 rows split the unit",
       len(after) > 0 and bool((after["nunique"] == 1).all()) and chance < 0.01 * len(before),
       "%d departures after, all agreeing; %d of %d before agree by chance" % (len(after), chance, len(before)))
    st_sum = A.ask_standing(D, vehicles="sum")[0]
    ok("FAIR the class 166 units' figure read once reproduces the world's loads (the golden), summed it triples them",
       st_sum["COAST"] > 3 * st["COAST"], "%d against %d" % (st_sum["COAST"], st["COAST"]))
    ok("SEP load-weigh rows under another train's headcode sit after the May 2026 system move only",
       len(stale) > 0 and not early, "%d rows, %d before" % (len(stale), len(early)))
    ukey = {}
    for r in lwr.itertuples():
        ukey.setdefault((r.run_date, r.unit_no, r.station, r.departed), set()).add(r.headcode)
    units_of = {}
    for r in D["form"].itertuples():
        units_of.setdefault((r.run_date, r.headcode), []).append(r.unit_no)
    found = total = 0
    for d, uid, t in A.timetabled(D, A.latest_days()):
        day = dt.date.fromisoformat(d)
        if t["calls"][-1] != "MVC" or (d, uid, t["calls"][-2]) not in depm or day.weekday() >= 5 or \
                day in K.BANK_HOLIDAYS or not (7 * 60 <= A.mins(t["arr"][-1]) <= 9 * 60 + 59):
            continue
        for u in units_of.get((d, t["headcode"]), []):
            total += 1
            found += len(ukey.get((d, u, t["calls"][-2], depm[(d, uid, t["calls"][-2])]), ())) == 1
    ok("FAIR every unit of every train into Marlvale Central has one load row at the station before it, by unit, "
       "station and the minute the train left", found == total and total > 300, "%d of %d" % (found, total))
    ok("REAL every sampled train ran (no batch on a cancelled train)",
       all(r["cancel"] is None for r in w.runs if (r["date"], r["uid"]) in {(bb["date"], bb["uid"]) for bb in sv.batches}))
    print("checks: %d run, %d failed%s" % (N[0], len(FAILS), (": " + "; ".join(FAILS)) if FAILS else ""))
    return 1 if FAILS else 0


def fig_rating_fall(D, J, q):
    M = RT.ratings(D, J)
    j = RT.ITEMS.index(q)
    x = M[:, j]
    a = ~np.isnan(x)
    w = J["weight"].values
    wave = J["wave"].values
    return np.average(x[a & (wave == 2026)], weights=w[a & (wave == 2026)]) - \
        np.average(x[a & (wave == 2025)], weights=w[a & (wave == 2025)])
