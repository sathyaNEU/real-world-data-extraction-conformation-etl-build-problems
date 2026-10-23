"""The build's assertions: the analyst test on the generator's clean truth, the golden and its family on the cut pack,
the rungs, the semantic forks (SFn), the asks' fairness and devices, the separation line, Layer 1 never carrying the
call, and the house checks. checks.run returns the number of failures."""
import datetime as dt
import os

import analysis as AN
import common as K
import pack as P

FAILS = []


def check(name, ok, detail=""):
    print("%s  %s%s" % ("ok  " if ok else "FAIL", name, ("  [%s]" % (detail,)) if detail != "" else ""))
    if not ok:
        FAILS.append(name)


def edit(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


# ------------------------------------------------------------------------------------------------ the clean truth
def recorded_faults(cr):
    v1 = cr["date"] < K.FORM_V2
    return [u for u in cr["units"] if u["fault"] or (v1 and u.get("fault2"))]


def recorded_use(cr, u):
    """The use the report lets a reader know: none for a driver who fled, none for a 2016 report's vehicle for hire or
    delivery whose operator the officer left blank."""
    if u["fled"]:
        return None
    if cr["date"] < K.FORM_V2 and u["use"] in K.CODES and not u.get("name"):
        return None
    return u["use"]


def truth_ratios(w, key, priv=("PV",)):
    """The rule's rate per mile, estimated the way `key` cuts the struck vehicles, on the generator's clean truth (no
    layout change, no clock or code to read, every location known)."""
    E = {}
    for c, v in w["E"].items():
        y, fc, ur, d, h = c
        k = key(y, fc, ur, K.GROUP_OF[(fc, ur)], d, h)
        E[k] = E.get(k, 0.0) + v
    af, n, tot = {}, {}, {}
    for cr in w["crashes"]:
        if cr["kind"] != "MV" or cr["undetermined"]:
            continue
        faults = recorded_faults(cr)
        for use in {"UNK" if u["fled"] else ("PV" if u["use"] in priv else u["use"]) for u in faults}:
            af[use] = af.get(use, 0) + 1
        if len(faults) != 1 or not cr["located"]:
            continue
        k = key(cr["year"], cr["fc"], cr["ur"], cr["group"], cr["dtype"], cr["hour"])
        for u in cr["units"]:
            if u is faults[0]:
                continue
            use = "PV" if u["use"] in priv else u["use"]
            n[(use, k)] = n.get((use, k), 0) + 1
            tot[k] = tot.get(k, 0) + 1
    mi = {}
    for (use, k), x in n.items():
        mi[use] = mi.get(use, 0.0) + E[k] * x / tot[k]
    rate = {u: af.get(u, 0) / mi[u] for u in mi}
    return {u: rate[u] / rate["PV"] for u in K.CODES}


def true_miles_ratios(w):
    """Each use's recorded crashes caused over the miles it truly drove (the generator's miles), against private."""
    mi = {}
    for (u, c), v in w["m"].items():
        mi[u] = mi.get(u, 0.0) + v
    af = {}
    for cr in w["crashes"]:
        if cr["kind"] != "MV" or cr["undetermined"]:
            continue
        for use in {u["use"] for u in recorded_faults(cr) if not u["fled"]}:
            af[use] = af.get(use, 0) + 1
    rate = {u: af.get(u, 0) / mi[u] for u in mi}
    return {u: rate[u] / rate["PV"] for u in K.CODES}


def truth_asks(w):
    """The asks on the truth: each person once at their final severity (K for a death within 30 days); each crash once
    at its most severe final injury."""
    import docs as DC
    ksi = {u: 0 for u in K.CODES}
    cost = {u: 0 for u in K.CODES}
    for cr in w["crashes"]:
        if cr["undetermined"]:
            continue
        uses = {recorded_use(cr, u) for u in recorded_faults(cr) if u["type"] in ("MV", "PK")} & set(K.CODES)
        if not uses:
            continue
        n = sum(1 for p in cr["persons"] if p["final"] in ("K", "A"))
        sev = min((p["final"] for p in cr["persons"]), key="KABCO".index, default="O")
        for u in uses:
            ksi[u] += n
            cost[u] += DC.COSTS[sev]
    return ksi, {u: AN.half_up(v / 1e6, 1) for u, v in cost.items()}


# ------------------------------------------------------------------------------------------------ Layer 1 mishandled
def mess_variant(D, how):
    """The call with one piece of the records' own mess mishandled, the method otherwise right."""
    import copy
    D2 = copy.copy(D)
    cr = {cid: dict(c) for cid, c in D.cr.items()}
    if how in ("utc_as_local", "fixed_offset"):
        for r in P.rows(D.target, "crashes"):
            if r["TIME_ZONE"] == "UTC" and r["CRASH_TIME"]:
                c = cr[r["CRASH_ID"]]
                h, m = (int(x) for x in r["CRASH_TIME"].split(":"))
                x = dt.datetime.fromisoformat(r["CRASH_DATE"]) + dt.timedelta(hours=h, minutes=m)
                if how == "fixed_offset":
                    x -= dt.timedelta(hours=8)
                c["hour"], c["date"] = x.hour, x.date()
                c["dtype"] = "we" if x.weekday() >= 5 else "wd"
    elif how == "form_v2_only":
        cr = {k: v for k, v in cr.items() if v["v2"]}
    elif how == "v1_unresolved_dropped":
        for c in cr.values():
            if not c["v2"]:
                c["units"] = [dict(u, use=("UNRES" if u["use"] in K.CODES else u["use"])) for u in c["units"]]
    D2.cr = cr
    return D2.ratios()[0]


def run(task, b, fig, res):
    del FAILS[:]
    target = os.path.join(task, "target")
    golden = os.path.join(task, "golden")
    D, g = res["D"], res["g"]
    w = b["w"]

    # 1. the analyst test on the clean truth: the easy route files the named wrong answer; the decisive step alone files
    # the golden
    easy = truth_ratios(w, lambda y, fc, ur, gr, d, h: "all")
    full = truth_ratios(w, lambda y, fc, ur, gr, d, h: (gr, d, h))
    check("ANALYST the easy route (the pooled struck-vehicle share as the miles share) files airport shuttles and "
          "paratransit", AN.covered(easy) == ["AS", "PT"], AN.covered(easy))
    check("ANALYST the decisive step alone (struck vehicles within road class, day type and hour, scaled by the "
          "stratum's miles) files the golden", AN.covered(full) == g["covered"], AN.covered(full))
    tm = true_miles_ratios(w)
    check("TRUTH the golden set is the set on the miles each use truly drove", AN.covered(tm) == g["covered"],
          {u: round(tm[u], 3) for u in K.CODES})
    check("TRUTH every use's estimate within 10 per cent of its true-miles ratio",
          all(abs(g["ratio"][u] / tm[u] - 1) < 0.10 for u in K.CODES),
          {u: round(g["ratio"][u] / tm[u] - 1, 3) for u in K.CODES})

    # 2. the golden on the cut pack
    check("GOLDEN four uses covered: taxicabs, ride-hail, parcel delivery, app-based delivery",
          g["covered"] == ["TX", "RH", "PD", "AD"], g["covered"])
    margin = min(abs(g["ratio"][u] / K.THRESHOLD - 1) for u in K.CODES)
    check("GOLDEN every use 10 per cent or more from the line", margin >= 0.10, round(margin, 3))
    check("GOLDEN figures.json carries the call", fig["call"]["count"] == 4 and fig["call"]["covered"] ==
          [K.LABEL[u] for u in g["covered"]])

    # 3. the family: every competent way of cutting the strata files the same call
    fam = AN.family(D)
    for k, v in sorted(fam.items()):
        check("FAMILY %s files the golden set" % k, AN.covered(v) == g["covered"], AN.covered(v))
    lab = {v: k for k, v in K.LABEL.items()}
    tenth = {u: {AN.half_up(v[u], 1) for k, v in fam.items() if k not in ("hr_private", "periods")} |
             {AN.half_up(g["ratio"][u], 1)} for u in K.CODES}
    na, nb = fig["nearest"]["above"], fig["nearest"]["under"]
    check("FAMILY the nearest use above the line rounds to the same tenth in every member",
          tenth[lab[na[0]]] == {na[1]}, tenth[lab[na[0]]])
    check("FAMILY every covered use rounds to the same tenth in every member",
          all(len(tenth[u]) == 1 for u in g["covered"]), {u: tenth[u] for u in g["covered"]})
    check("FAMILY the uses under the line stay under the stated tenth in every member, the two discounted included",
          all(v[lab[x]] < nb[1] for v in list(fam.values()) + [g["ratio"]] for x in nb[0])
          and sorted(lab[x] for x in nb[0]) == sorted(u for u in K.CODES if u not in g["covered"]),
          {x: round(max(v[lab[x]] for v in fam.values()), 3) for x in nb[0]})

    # 4. the rungs: each lands off the golden, for the reason the ladder gives
    rg = AN.rungs(D)
    for k, v in rg.items():
        check("RUNG %s lands off the golden set" % k, AN.covered(v) != g["covered"], AN.covered(v))
    check("RUNG the pooled share leaves ride-hail and taxicabs out", rg["pooled"]["RH"] < 1.3 and rg["pooled"]["TX"] < 1.3,
          (round(rg["pooled"]["RH"], 3), round(rg["pooled"]["TX"], 3)))
    check("RUNG the pooled share takes airport shuttles and paratransit in", AN.covered(rg["pooled"]) == ["AS", "PT"])
    check("RUNG the adjusted propensity files the pooled share's set", AN.covered(rg["adjusted"]) == ["AS", "PT"])
    check("RUNG road class alone leaves ride-hail out", rg["road"]["RH"] < 1.45, round(rg["road"]["RH"], 3))
    check("RUNG hour alone leaves parcel and app delivery out", rg["hour"]["PD"] < 1.45 and rg["hour"]["AD"] < 1.45,
          (round(rg["hour"]["PD"], 3), round(rg["hour"]["AD"], 3)))
    check("RUNG urban or rural with hour takes airport shuttles in", rg["urban_rural"]["AS"] > 1.6,
          round(rg["urban_rural"]["AS"], 3))
    check("RUNG the culpability share covers no use", AN.covered(rg["culpability"]) == [])
    check("RUNG per vehicle covers six uses", len(AN.covered(rg["per_vehicle"])) == 6, AN.covered(rg["per_vehicle"]))
    counts = {k: len(AN.covered(v)) for k, v in rg.items()}
    check("RUNG no rung files four uses", all(n != 4 for n in counts.values()), counts)

    # 5. the semantic forks: each reading closed by a sentence or filing the same call
    sf = {
        "SF1": ("private drivers with motorcycles", fam["mc_private"]),
        "SF2": ("a crash with two drivers at fault counted for neither", fam["one_at_fault"]),
        "SF3": ("drivers who fled counted as private", fam["hr_private"]),
        "SF4": ("day of week for day type", fam["dow"]),
        "SF5": ("functional system and area for road class", fam["fcl"]),
        "SF6": ("each year cut on its own", fam["yr"]),
        "SF7": ("two-vehicle crashes only as the struck vehicles", fam["two"]),
        "SF8": ("average-day expansion of the count stations", fam["avgday"]),
        "SF9": ("hit-and-run crashes out of the struck vehicles", fam["nohr"]),
        "SF10": ("crashes with no driver at fault in the struck vehicles", fam["undet"]),
        "SF11": ("State Patrol times read as local", mess_variant(D, "utc_as_local")),
        "SF12": ("State Patrol times at a fixed eight-hour offset", mess_variant(D, "fixed_offset")),
        "SF13": ("three periods of the day for the hour", fam["periods"]),
    }
    for k, (what, v) in sf.items():
        check("%s %s files the same call" % (k, what), AN.covered(v) == g["covered"], AN.covered(v))
    for how in ("form_v2_only", "v1_unresolved_dropped"):
        v = mess_variant(D, how)
        check("LAYER1 %s files the same call" % how, AN.covered(v) == g["covered"], AN.covered(v))

    # 6. the asks: the pack's golden reproduces the truth exactly, and each easy path misses
    tk, tc = truth_asks(w)
    ak, ac = fig["asks"]["ksi"], fig["asks"]["cost_millions"]
    check("ASK A the golden equals the truth's people killed or seriously injured, every use",
          all(ak[K.LABEL[u]] == tk[u] for u in K.CODES), (ak, tk))
    check("ASK B the golden equals the truth's crash cost, every use",
          all(ac[K.LABEL[u]] == tc[u] for u in K.CODES), (ac, tc))
    import cracker as CR
    cs = CR.score(target)
    for k, v in cs["paths"].items():
        if not k.endswith("golden"):
            check("ASK path %s misses at least 4 of 7" % k, v <= 3, v)
    check("ASK the cracker keeps no ask figure", cs["cracker_hits"] == 0, cs["cracker_hits"])

    # 7. fairness and the separation line
    ps = P.persons(target)
    dup_ok, relisted = True, 0
    for cid, lst in ps.items():
        seen = {}
        for p in sorted(lst, key=lambda x: x["pno"]):
            k = (p["unit"], p["seat"]) if p["seat"] else (p["unit"], p["ptype"])
            if k in seen:
                q = seen[k]
                relisted += 1
                if (q["age"], q["sex"], q["ptype"]) != (p["age"], p["sex"], p["ptype"]):
                    dup_ok = False
            seen[k] = p
    check("FAIR every person listed again shares seat, age, sex and type with the earlier row", dup_ok and relisted > 0,
          relisted)
    fp, dead = AN.final_persons(D)
    reg_rows = P.fatalities(target)
    found = sum(1 for (cid, unit, pt, age, sex) in dead
                if any((p["unit"], p["ptype"], p["age"], p["sex"]) == (unit, pt, age, sex) for p in fp.get(cid, ())))
    check("FAIR every register death matches one person in the persons file",
          len(dead) == len(reg_rows) == found, (len(dead), len(reg_rows), found))
    stale = sum(1 for cid, lst in fp.items()
                if min((p["final"] for p in lst), key="KABCO".index, default="O") != D.cr[cid]["sev"])
    check("DEVICE the crash table's severity is the first report's on crashes a later record or death changed",
          stale > 0, stale)
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis.py")).read()
    call_src = src.split("# the asks")[0]
    check("SEPARATION the call reads no persons, register or cost file",
          all(x not in call_src for x in ("P.persons(", "P.fatalities(", "P.costs(")))

    # 8. the design note's figures, recomputed (H2)
    mi, E, n, tot = D.miles()
    crs = {}
    for c in D.mv_crashes():
        if c["group"] is not None and c["hour"] is not None:
            k = (c["group"], c["dtype"], c["hour"])
            crs[k] = crs.get(k, 0) + 1

    def per100(keys):
        keys = list(keys)
        return round(sum(crs.get(k, 0) for k in keys) / sum(E[k] for k in keys) * 100, 1)
    ua = per100(k for k in E if k[0] == "UA")
    rf = per100(k for k in E if k[0] == "RF")
    night = per100(k for k in E if k[2] < 5)
    day = per100(k for k in E if k[1] == "wd" and 9 <= k[2] < 16)
    check("EVIDENCE crashes per 100 million miles: urban arterials 347.0, rural freeways 56.3, midnight to five 445.3, "
          "weekday working hours 161.2", (ua, rf, night, day) == (347.0, 56.3, 445.3, 161.2), (ua, rf, night, day))
    T, M = sum(tot.values()), sum(E.values())
    rh_s = round(100 * sum(x for (u, k), x in n.items() if u == "RH") / T, 2)
    rh_m = round(100 * mi["RH"] / M, 2)
    check("EVIDENCE ride-hail 5.79 per cent of the vehicles struck, 2.96 per cent of the miles", (rh_s, rh_m) == (5.79, 2.96),
          (rh_s, rh_m))
    deaths_never_k = sum(1 for (cid, unit, pt, age, sex) in dead if not any(
        p["sev"] == "K" and (p["unit"], p["ptype"], p["age"], p["sex"]) == (unit, pt, age, sex) for p in ps.get(cid, ())))
    rel_crashes = len({cid for cid, lst in ps.items() if len({((p["unit"], p["seat"]) if p["seat"] else
                                                               (p["unit"], p["ptype"])) for p in lst}) < len(lst)})
    check("EVIDENCE 4,545 later person records in 4,505 crashes; 2,038 register deaths, 283 never recorded K; 4,093 "
          "crashes whose final worst injury differs from CRASH_SEVERITY",
          (relisted, rel_crashes, len(dead), deaths_never_k, stale) == (4545, 4505, 2038, 283, 4093),
          (relisted, rel_crashes, len(dead), deaths_never_k, stale))

    # 9. house checks
    files = sorted(os.listdir(target))
    check("H4 the pack holds exactly the declared files", files == sorted(K.FILES.values()), files)
    contents = open(os.path.join(target, K.FILES["contents"]), encoding="utf-8").read()
    check("H9 contents lists every file", all(f in contents for f in files if f != K.FILES["contents"]))
    check("H4 the goldens are the two deliverables", sorted(os.listdir(golden)) == sorted(K.DELIVERABLES))
    places = [x.strip().lower() for x in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                           "h21_reference_places.txt")) if x.strip()]
    for nm in ["Stonereach", "Kelderwick", "Fairhollow"]:
        n = nm.lower()
        near = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        check("H21 %s is three or more edits from every reference place" % nm, not near, near[:3])
    for f in files:
        bb = open(os.path.join(target, f), "rb").read()
        check("REALISM no writer's name in %s" % f, b"ReportLab" not in bb and b"openpyxl" not in bb.lower()
              and b"matplotlib" not in bb.lower())
        if f.endswith((".csv", ".txt")):
            check("REALISM no em dash in %s" % f, "—".encode() not in bb)
    for f in os.listdir(golden):
        bb = open(os.path.join(golden, f), "rb").read()
        check("REALISM no writer's name in the golden %s" % f, b"openpyxl" not in bb.lower()
              and b"python-pptx" not in bb.lower())
    last = max(dt.date.fromisoformat(r["CRASH_DATE"]) for r in P.rows(target, "crashes"))
    check("H16 no crash after 2025 (UTC dates up to 1 January 2026)", last <= dt.date(2026, 1, 1), last)
    dd = max(dt.date.fromisoformat(r["DATE_OF_DEATH"]) for r in reg_rows)
    check("H16 no death after 30 January 2026", dd <= dt.date(2026, 1, 30), dd)
    leak = ["induced exposure", "not at fault", "not-at-fault", "struck vehicle", "exposure", "stratif", "quasi",
            "propensity", "share of the miles", "supplement", "listed again", "re-list"]
    for k in ("rule", "dictionary", "tmr", "costs"):
        txt = P.pdf_text(os.path.join(target, K.FILES[k])).lower()
        hit = [x for x in leak if x in txt]
        check("LEAK %s names no method or device word" % K.FILES[k], not hit, hit)
    hit = [x for x in leak if x in contents.lower()]
    check("LEAK contents names no method or device word", not hit, hit)
    head = open(os.path.join(target, K.FILES["platforms"]), encoding="utf-8").readline().lower()
    check("GATE G the platforms' reports carry no miles", "mile" not in head, head.strip())
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, K.FILES["operators"]), read_only=True)
    hdrs = " ".join(str(c) for sh in wb.worksheets for c in next(sh.iter_rows(values_only=True))).lower()
    check("GATE G the operator register carries no miles", "mile" not in hdrs, hdrs)
    print("checks: %d failed" % len(FAILS))
    return len(FAILS)
