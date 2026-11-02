"""Generator assertions on the clean truth and on the cut pack.  run(W, target, E) returns a list of
(label, ok, detail); build.py fails on any False."""
import os, re, json, shutil, tempfile, zipfile, csv
from datetime import datetime
import numpy as np
import analysis as A
import routes as R
import pack as P
import world as Wd

ASK_UNITS = {"july_mwh": 0.01, "requests": 1.0, "voltage_pct": 0.01}


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def bin_of(v, u):
    return round(round(v / u) * u, 6)


def run(W, target, E):
    out = []

    def ok(label, cond, detail=""):
        out.append((label, bool(cond), detail))

    D, U, C = E["D"], E["units"], E["call"]
    apts = W["apts"]
    unit_of = {a["apt"].replace("-", ""): a for a in apts}
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------------------------- three rules
    # R1: the field's raw material ships, the deciding quantity in no column
    pq_rows = sum(len(v) for v in D["pq"].values())
    ok("R1a raw material: hourly voltage per meter and half-hourly interval data ship",
       pq_rows >= 25000 and len(D["nem12"]) == len(apts), "%d PQ rows, %d NMIs" % (pq_rows, len(D["nem12"])))
    heads = []
    for n, sh_, first in [(P.REG_NAME, "Child meters", "Child NMI"), (P.LOTS_NAME, "Lots", "Lot"),
                          (P.WORKS_NAME, "Chargers", "Unit"), (P.WORKS_NAME, "Cooktop conversions", "Unit"),
                          (P.APPS_NAME, "Applications", "Application")]:
        hdr, _ = A.table_after(A.xlsx_rows(os.path.join(target, n), sh_), first)
        heads += [str(h).lower() for h in hdr]
    for n in files:
        if n.endswith(".csv") and not n.startswith("nem12"):
            with open(os.path.join(target, n)) as f:
                heads += [h.lower() for h in f.readline().strip().split(",")]
    heads += [k.lower() for k in D["events"][0].keys()]
    ok("R1b no shipped column holds an apartment's phase", not any(re.search(r"\bphase\b", h) for h in heads),
       "headers checked: %d" % len(heads))
    truth_groups_ok = 0
    for r in D["risers"]:
        g = E["groups"][r["riser"]]
        lab = {}
        good = True
        for u, k in g.items():
            p = unit_of[u]["phase"]
            if lab.setdefault(k, p) != p:
                good = False
        if len(set(lab.values())) != len(lab):
            good = False
        truth_groups_ok += good
    ok("R1c the voltage grouping recovers every riser's true phases from the pack", truth_groups_ok == len(D["risers"]),
       "%d of %d risers" % (truth_groups_ok, len(D["risers"])))

    # R3a: the analyst test on the clean truth: balanced phasing with every filed rule applied
    bal_set = E["rung_sets"]["balanced"]
    ok("R3a the balanced default files a wrong set", set(bal_set) != set(C["designated"]),
       "balanced %s against %s" % (bal_set, C["designated"]))
    truth_assign = {r["riser"]: {u: unit_of[u]["phase"] for u in E["groups"][r["riser"]]} for r in D["risers"]}
    C_truth = A.call(D, U, E["M"], truth_assign)
    ok("R3b the default with only the phase step changed (true phases) files the golden",
       C_truth["designated"] == C["designated"], str(C_truth["designated"]))
    ok("R3b each lower rung's single correction stays wrong",
       set(E["rung_sets"]["rotation"]) != set(C["designated"]) and set(E["rung_sets"]["simulated"]) != set(C["designated"]),
       "rotation %s, simulated %s" % (E["rung_sets"]["rotation"], E["rung_sets"]["simulated"]))
    # R3c: no plant: no repeated day vector within or across meters, no copied block
    vecs = set()
    dup = 0
    for nmi, days in D["nem12"].items():
        for d, recs in days.items():
            for rr in recs:
                if rr["vals"].sum() < 0.05 or rr["q"] == "V":
                    continue
                key = (rr["sfx"], tuple(np.round(rr["vals"], 3)))
                if key in vecs:
                    dup += 1
                vecs.add(key)
    ok("R3c no copied or repeated block of interval data", dup == 0, "%d repeats" % dup)
    keys = [(k, tuple(v for _, v in s[:48])) for k, s in D["pq"].items()]
    ok("R3c no two meters share a voltage series", len({k[1] for k in keys}) == len(keys), "%d series" % len(keys))
    ok("R3c no memo, draft or stakeholder figure ships", not any(re.search(r"memo|draft|note|readme|dictionary|manifest", n, re.I) for n in files),
       ", ".join(files))

    # ------------------------------------------------------------------------------------------ the ladder
    sh = {k: v["share"] for k, v in C["risers"].items()}
    lim = D["K"]["limit"] * 100
    ok("ladder: the golden designates between four and seven rising mains", 4 <= len(C["designated"]) <= 7, str(C["designated"]))
    margin = min(abs(v - lim) for v in sh.values())
    ok("ladder: every rising main clears the 80 per cent line by 4.5 points or more", margin >= 4.5, "%.2f" % margin)
    ok("ladder: rung 0 (balanced) designates at most one main", len(bal_set) <= 1, str(bal_set))
    rot, sim = set(E["rung_sets"]["rotation"]), set(E["rung_sets"]["simulated"])
    G = set(C["designated"])
    ok("ladder: rung 1 (rotation) differs from the golden by two mains or more", len(rot ^ G) >= 2, str(sorted(rot ^ G)))
    ok("ladder: rung 2 (expected busiest phase under random phasing) files a wrong set", len(sim ^ G) >= 1, str(sorted(sim ^ G)))
    ok("ladder: rungs 1 and 2 name different sets", rot != sim, "")
    # shock: the golden set is no interval of any shipped statistic
    stats = {"balanced": {k: v["balanced"] for k, v in E["rungs"].items()},
             "rating": {r["riser"]: -r["rating_a"] for r in D["risers"]},
             "july use": E["july_mwh"], "requests": E["requests"], "voltage": E["voltage_pct"],
             "added": {r["riser"]: sum(U[u]["added"] for u in U if U[u]["riser"] == r["riser"]) for r in D["risers"]},
             "three-phase count": {r["riser"]: sum(U[u]["three"] for u in U if U[u]["riser"] == r["riser"]) for r in D["risers"]}}
    intervals = []
    for name, st in stats.items():
        order = sorted(st, key=lambda k: -st[k])
        for i in range(len(order)):
            for j in range(i + 1, len(order) + 1):
                if set(order[i:j]) == G:
                    intervals.append(name)
    ok("ladder: the golden set is no interval of any shipped statistic", not intervals, ", ".join(intervals))

    # ------------------------------------------------------------------------------------ method family
    for m in ("raw_hier", "diff_complete", "det_ward"):
        g2 = A.phase_groups(D, U, m)
        C2 = A.call(D, U, E["M"], g2)
        same = all(abs(C2["risers"][k]["share"] - sh[k]) < 1e-9 for k in sh)
        ok("method: grouping by %s gives the same groups, call and figures" % m, same and C2["designated"] == C["designated"], "")
    # the reflex sweep: mean-voltage terciles (the lowest-voltage third read as the busiest phase)
    terc = {}
    for r in D["risers"]:
        us = [u for u in U if U[u]["riser"] == r["riser"] and not U[u]["three"]]
        mv = {u: np.mean([v for _, v in D["pq"][(U[u]["serial"], "1")]]) for u in us}
        order = sorted(us, key=lambda u: mv[u])
        terc[r["riser"]] = {u: (k * 3) // len(order) for k, u in enumerate(order)}
    Ct = A.call(D, U, E["M"], terc)
    ok("method: mean-voltage terciles (a reflex reading of the voltages) file a wrong set", set(Ct["designated"]) != G,
       str(Ct["designated"]))
    # separation of the voltage groups
    seps = []
    for r in D["risers"]:
        us = sorted(E["groups"][r["riser"]])
        allus = sorted(u for u in U if U[u]["riser"] == r["riser"])
        ser = {}
        for u in allus:
            x = U[u]
            if x["three"]:
                ser[u] = np.mean([[v for _, v in D["pq"][(x["serial"], e)]] for e in "123"], axis=0)
            else:
                ser[u] = np.array([v for _, v in D["pq"][(x["serial"], "1")]])
        mean = np.mean([ser[u] for u in allus], axis=0)
        X = np.array([ser[u] - mean for u in us])
        Cm = np.corrcoef(X)
        g = [E["groups"][r["riser"]][u] for u in us]
        within = min(Cm[a, b] for a in range(len(us)) for b in range(a + 1, len(us)) if g[a] == g[b])
        across = max(Cm[a, b] for a in range(len(us)) for b in range(a + 1, len(us)) if g[a] != g[b])
        seps.append(within - across)
    ok("method: every riser's phase groups separate (least within-group correlation above the most across)", min(seps) > 0.05,
       "least gap %.3f" % min(seps))

    # ------------------------------------------------------------------------------------- semantic forks
    std_flat = " ".join(D["std_text"].split())
    ok("SF1 every apartment sits on exactly one of the schedule's rising mains",
       len(D["risers"]) == 18 and all(sum(1 for r in D["risers"] if r["riser"][0] == x["tower"] and r["lo"] <= x["floor"] <= r["hi"]) == 1 for x in U.values()), "")
    ok("SF2 demand is twice the half-hour kWh (the standard's own sentence ships)",
       "half-hourly demand being twice its metered kWh in the half-hour" in std_flat, "")
    ok("SF4 market time and Melbourne local time coincide in July (daylight saving runs October to April)",
       datetime(2026, 7, 13) > datetime(2026, 4, 5) and datetime(2026, 7, 17) < datetime(2026, 10, 4), "")
    # SF3 window shifted a half-hour either way
    for s_ in (-1, 1):
        Ms = A.evening_matrix(D, U, shift=s_)
        Cs = A.call(D, U, Ms, E["groups"])
        ok("SF3 the window read a half-hour %s gives the same designated set" % ("early" if s_ < 0 else "late"),
           Cs["designated"] == C["designated"], str(Cs["designated"]))
    # SF5 most heavily loaded phase before the additions
    alt = []
    for r in D["risers"]:
        _, _, per = A.busiest(U, E["M"], r["riser"], E["groups"][r["riser"]], r["rating_a"], D["K"]["volt"])
        us = [u for u in U if U[u]["riser"] == r["riser"]]
        S = np.zeros((3, len(next(iter(E["M"].values())))))
        Ad = np.zeros(3)
        for u in us:
            if U[u]["three"]:
                S += E["M"][u] / 3
                Ad += U[u]["added"] / 3
            else:
                S[E["groups"][r["riser"]][u]] += E["M"][u]
                Ad[E["groups"][r["riser"]][u]] += U[u]["added"]
        k = int(np.argmax(S.max(1)))
        v = (S.max(1)[k] + Ad[k]) / (r["rating_a"] * D["K"]["volt"] / 1000) * 100
        if v > lim:
            alt.append(r["riser"])
    ok("SF5 'any phase' against 'the phase busiest before the additions': same set", sorted(alt) == sorted(C["designated"]), str(alt))
    # SF6 coincident against non-coincident peaks
    nonco = []
    for r in D["risers"]:
        us = [u for u in U if U[u]["riser"] == r["riser"]]
        tot = sum(E["M"][u].max() for u in us)
        nonco.append(tot)
    ok("SF6 the standard's summed (coincident) demand differs from summed individual peaks", min(n - C["risers"][r["riser"]]["kw"] for n, r in zip(nonco, D["risers"])) > 0, "")
    # SF7 additions placed on the unit's phase; SF8 three-phase split; SF9 230 V; SF10 strictly above
    ok("SF7 every charger and conversion unit in the works schedule is an apartment on a riser",
       all(c["Unit"].replace("-", "") in U for c in D["chargers"] + D["cooktops"]), "")
    three_alt = {}
    for r in D["risers"]:
        rid = r["riser"]
        g = dict(E["groups"][rid])
        for u in U:
            if U[u]["riser"] == rid and U[u]["three"]:
                g[u] = 0
        Ux = {k: dict(v, three=False) if v["three"] else v for k, v in U.items()}
        three_alt[rid] = A.busiest(Ux, E["M"], rid, g, r["rating_a"], D["K"]["volt"])[1]
    ok("SF8 a three-phase supply is read as equal on its three phases (the standard's sentence ships)",
       "A three-phase apartment draws its demand equally on the three phases" in " ".join(D["std_text"].split()),
       "single-phase reading would file %s" % sorted(k for k, v in three_alt.items() if v > lim))
    ok("SF9 the standard's 230 V is the conversion used", D["K"]["volt"] == 230.0, "")
    ok("SF10 no rising main sits on the 80 per cent line", all(abs(v - lim) > 0.5 for v in sh.values()), "")
    ok("SF11 the standard's window is read from the filed sentence (half-hours 17:00 to 20:30, 13 to 17 July)",
       D["K"]["first"] == 34 and D["K"]["last"] == 41 and D["K"]["days"] == [13, 14, 15, 16, 17], str(D["K"]))
    ok("SF12 every apartment's NEM12 records in the window are single actual records (no exchange, gap or substitute)",
       all(len(D["nem12"][U[u]["nmi"]]["202607%02d" % d]) == (2 if any(r["sfx"] == "E2" for r in D["nem12"][U[u]["nmi"]]["202607%02d" % d]) else 1)
           and all(r["q"] == "A" for r in D["nem12"][U[u]["nmi"]]["202607%02d" % d]) for u in U for d in range(13, 18)), "")
    ok("SF13 the controlled-load register carries nothing in the window",
       all(sum(r["vals"][34:42].sum() for r in D["nem12"][U[u]["nmi"]]["202607%02d" % d] if r["sfx"] == "E2") == 0 for u in U for d in range(13, 18)), "")
    ok("SF14 'the undesignated riser nearest the line' is unique", sorted(sh[k] for k in sh if k not in G)[-1] - sorted(sh[k] for k in sh if k not in G)[-2] > 0.5, "")

    # ------------------------------------------------------------------------------------ bin distances
    graded = [(k, sh[k]) for k in C["designated"]] + ([(C["nearest"], sh[C["nearest"]])] if C["nearest"] else [])
    e_min = min(edge(v, 1.0) for _, v in graded)
    ok("bins: every graded share of rating sits 0.15 or more inside its whole-per-cent bin", e_min >= 0.15,
       "tightest %.3f" % e_min)
    em = min(edge(v, 0.01) for v in E["july_mwh"].values())
    ok("bins: every July use figure sits 0.0003 MWh or more inside its bin (above the register and interval rounding)", em >= 0.0003, "tightest %.5f" % em)
    em = min(edge(v, 0.01) for v in E["voltage_pct"].values())
    ok("bins: no time-outside figure sits on a rounding tie", em >= 1e-6, "tightest %.6f" % em)
    ivr = {}
    for u, x in U.items():
        ivr[u] = sum(r_["vals"].sum() for d in D["nem12"][x["nmi"]] for r_ in D["nem12"][x["nmi"]][d])
    diffs = [abs(ivr[u] - E["per_unit_use"][u]) for u in U if len(D["nem12"][U[u]["nmi"]]) == 31 and not any(
        r_["q"].startswith("E") for d in D["nem12"][U[u]["nmi"]] for r_ in D["nem12"][U[u]["nmi"]][d])]
    ok("bins: where both are actual, the interval sum and the register movement agree within 0.05 kWh", max(diffs) < 0.05, "max %.4f kWh" % max(diffs))

    # ------------------------------------------------------------------------------ asks: devices and truth
    truth_use = {a["apt"].replace("-", ""): a["july_kwh_true"] for a in apts}
    ok("ask A: the golden July use equals the truth for every apartment within 0.05 kWh",
       max(abs(E["per_unit_use"][u] - truth_use[u]) for u in truth_use) < 0.05, "")
    gold = {k: E[k] for k in ASK_UNITS}

    def kept(route_vals, key):
        u = ASK_UNITS[key]
        return sum(1 for k in gold[key] if bin_of(route_vals[k], u) == bin_of(gold[key][k], u))

    for name, fn, key, cap in [("natural interval sum", R.a_intervals_all, "july_mwh", 9), ("one record a day", R.a_dedup, "july_mwh", 2),
                               ("careful route (the later actual read for an estimate)", R.a_cracker, "july_mwh", 4),
                               ("estimated reads as given", R.a_estimates_as_given, "july_mwh", 1),
                               ("general supply alone", R.a_general_only, "july_mwh", 0),
                               ("rows by written unit", R.b_rows_by_unit, "requests", 9), ("careful route (the date rule)", R.b_cracker, "requests", 6),
                               ("UTC dates, summed", R.c_sum_utc, "voltage_pct", 3),
                               ("careful route without the hourly cross-check (every record joined into spans)", R.c_cracker, "voltage_pct", 0),
                               ("calendar UTC days", R.c_union_utc, "voltage_pct", 0),
                               ("elements summed", R.c_elements_summed, "voltage_pct", 3)]:
        k = kept(fn(D, U), key)
        ok("ask device: %s keeps at most %d of 18 %s figures" % (name, cap, key), k <= cap, "%d kept" % k)
    # F3 and F2: the export's own legend fixes the reading; every July figure lands in its bin only under it
    with open(os.path.join(target, P.READS_NAME)) as f:
        rrows = list(csv.DictReader(f))
    leg_r = {(r["register"], r["register_desc"]) for r in rrows}
    leg_t = {(r["read_type"], r["read_type_desc"]) for r in rrows}
    ok("F2: the reads export names its registers (E1 general supply, E2 controlled load) on every row",
       leg_r == {("E1", "General supply"), ("E2", "Controlled load")}, str(sorted(leg_r)))
    ok("F3: the reads export describes its read types (A actual, E estimated) on every row",
       leg_t == {("A", "Actual"), ("E", "Estimated")}, str(sorted(leg_t)))
    est_ser = {r["meter_serial"] for r in rrows if r["read_type"] == "E"}
    est_ris = {x["riser"] for x in U.values() if x["serial"] in est_ser}
    given = R.a_estimates_as_given(D, U)
    moved = [k for k in est_ris if bin_of(given[k], 0.01) != bin_of(E["july_mwh"][k], 0.01)]
    ok("F3: with the estimated midnight reads taken as given, every riser holding one leaves its bin",
       len(moved) == len(est_ris) and len(est_ris) >= 17, "%d of %d risers with an estimate" % (len(moved), len(est_ris)))
    later = {}
    for r in rrows:
        if r["read_local"].startswith("2026-08-01") and r["read_local"][11:] != "00:00":
            later.setdefault(r["meter_serial"], set()).add(r["read_type"])
    ok("F3: every estimated midnight read has an actual read later on 1 August beside it",
       all(sv in later for sv in est_ser), "%d estimated meters" % len(est_ser))
    twins = [sv for sv in later if sv not in est_ser]
    ok("ask A: some meters with an actual midnight read also carry a later special read (no marker)", len(twins) >= 5, "%d" % len(twins))
    gen = R.a_general_only(D, U)
    ok("F2: the general supply register alone moves every riser out of its bin",
       all(bin_of(gen[k], 0.01) != bin_of(E["july_mwh"][k], 0.01) for k in gen), "")
    ok("F2: the standard files use as both registers together",
       "general supply and controlled load together" in " ".join(D["std_text"].split()), "")
    # round 2 (Q5): section 6 files which record governs, the limits' inclusivity and the market-time days
    std6 = " ".join(D["std_text"].split())
    ok("Q5: section 6 files that a record counts only where the meter's own hourly maximum or minimum is outside the limits",
       "a record counts only where the meter's own hourly maximum or minimum, in an hour the record covers, is itself outside the limits" in std6, "")
    ok("Q5: section 6 files outside as above 253 V or below 216 V", "while its voltage is above 253 V or below 216 V" in std6, "")
    ok("Q5: section 6 sets the run of days from midnight to midnight in market time",
       "from the midnight in market time that begins the first day to the midnight that ends the last" in std6, "")
    lit = R.c_literal(D, U)
    ok("Q5: section 6 read word for word gives the golden on all 18 risers", all(abs(lit[k] - E["voltage_pct"][k]) < 1e-12 for k in lit), "")
    every = R.c_cracker(D, U)
    ok("Q5: ignoring the hourly cross-check moves every riser out of its bin (the 18 cells the ceiling counts)",
       all(bin_of(every[k], 0.01) != bin_of(E["voltage_pct"][k], 0.01) for k in every), "")
    exts = [float(e["v_extreme"]) for e in D["events"]]
    ok("Q5: no event record's extreme sits at a limit (253.0 V or 216.0 V)", not any(abs(x - 253.0) < 1e-9 or abs(x - 216.0) < 1e-9 for x in exts),
       "lowest extreme %.1f" % min(exts))
    conv = {"limits inclusive": R.c_literal(D, U, inclusive=True), "the record's own extreme also beyond the limit": R.c_literal(D, U, own_extreme=True)}
    for name, vals in conv.items():
        ok("Q5: %s gives the same figures on every riser" % name, all(abs(vals[k] - lit[k]) < 1e-12 for k in lit), "")
    endinc = R.c_literal(D, U, end_second=1)
    moves = {k: abs(endinc[k] - lit[k]) for k in lit}
    room = {k: edge(E["voltage_pct"][k], 0.01) for k in lit}
    margin = {k: room[k] - moves[k] for k in lit}
    kt = min(margin, key=margin.get)
    ok("Q5: every cell's distance to its rounding edge exceeds what any boundary convention moves (an end second counted inclusively the largest)",
       all(margin[k] > 0 for k in lit), "tightest %s: room %.5f against a move of %.5f" % (kt, room[kt], moves[kt]))
    # F1: the standard files the any-phase reading for three-phase supplies
    ok("F1: the standard files when a three-phase supply is outside the limits",
       "A three-phase supply is outside the limits while any one of its phases is outside them" in " ".join(D["std_text"].split()), "")
    # the asks' devices move no call figure: zero device rows in the call's population
    exch_days = [int(e["exchanged_local"][:2]) for e in D["exchanges"]]
    ok("separation: every meter exchange falls before 13 July", max(exch_days) < 13, str(sorted(set(exch_days))))
    gaps = [min(int(d[6:]) for d in range(1)) if False else None]
    short = [x["nmi"] for x in U.values() if len(D["nem12"][x["nmi"]]) < 31]
    first_missing = min(min(set(range(1, 32)) - {int(d[6:]) for d in D["nem12"][n]}) for n in short) if short else 99
    ok("separation: interval gaps start after 17 July", first_missing > 17, "first missing day %d" % first_missing)
    est_days = sorted({int(d[6:]) for n in D["nem12"] for d, recs in D["nem12"][n].items() if any(r["q"].startswith("E") for r in recs)})
    ok("separation: no substituted day falls in 13 to 17 July", not set(est_days) & set(range(13, 18)), str(est_days))
    late_old = 0
    for a in D["apps"]:
        sp = a["Car space"].strip()
        if sp[:3] in ("B2-", "B3-") and datetime.strptime(a["Lodged"], "%d/%m/%Y") >= datetime(2025, 3, 15):
            if A.true_space(a, D, U) != sp:
                late_old += 1
    ok("ask B: old car space numbers written after the re-marking are resolved by the applicant's own space", late_old >= 6, "%d" % late_old)
    # F4: every application maps to exactly one car space under the evidence (the re-marking date and the
    # applicant's own spaces, by the unit written or the lot an owner elsewhere gives)
    amb, offsite, no_lot = 0, 0, 0
    lots_known = {int(r["Lot"]) for r in D["lots"]}
    for a in D["apps"]:
        cands = A.candidate_spaces(a, D)
        own = A.applicant_spaces(a, D, U)
        w = a["Unit or owner address"]
        if A.parse_unit(w) is None and "(for the OC)" not in w:
            offsite += 1
            if A.parse_lot(w) not in lots_known:
                no_lot += 1
        if own is None:
            if len(cands) != 1 or cands[0] in {s_ for x in U.values() for s_ in x["spaces"]}:
                amb += 1
        elif sum(1 for c in cands if c in own) != 1:
            amb += 1
    ok("F4: every application maps to exactly one car space under the evidence", amb == 0, "%d ambiguous of %d" % (amb, len(D["apps"])))
    ok("F4: every owner writing from another address gives a lot the register holds", offsite >= 5 and no_lot == 0, "%d off-site, %d without a lot" % (offsite, no_lot))
    # ask C: the stored-log re-sends, refereed by the meters' own hourly maxima
    hv_ex, hv_in = [], []
    for e in D["events"]:
        st = datetime.strptime(e["start_utc"], "%Y-%m-%dT%H:%M:%SZ")
        en = datetime.strptime(e["end_utc"], "%Y-%m-%dT%H:%M:%SZ")
        h = st.replace(minute=0, second=0)
        vs = []
        while h < en:
            v = D["pq_max"].get((e["meter_serial"], e["element"], h.strftime("%Y-%m-%dT%H:%M:%SZ")))
            if v is not None:
                vs.append(v[1])
            h = h + (datetime(2026, 1, 1, 1) - datetime(2026, 1, 1, 0))
        if vs:
            (hv_ex if A.excursion_record(e, D) else hv_in).append(max(vs))
    ok("ask C: the hourly maxima separate the records cleanly (every excursion's hour 253.1 V or more, every other record's hours 252.9 V or less)",
       min(hv_ex) >= 253.1 and max(hv_in) <= 252.9, "excursions from %.1f, others to %.1f" % (min(hv_ex), max(hv_in)))
    rs_written = [e for e in W["events_written"] if e.get("resent")]
    rs_in = [e for e in rs_written if datetime(2026, 7, 12) <= e["start"] < datetime(2026, 7, 20)]
    ok("ask C: the records the hourly maxima refuse are exactly the re-sent ones", len(hv_in) == len(rs_in) >= 100, "%d refused, %d re-sent" % (len(hv_in), len(rs_in)))
    inside = 0
    orig = {}
    for e in W["events_written"]:
        if not e.get("resent"):
            orig.setdefault((e["serial"], e["element"]), []).append((e["start"], e["end"]))
    from datetime import timedelta as _td
    for c in rs_written:
        s0, t0 = c["start"] - _td(hours=10), c["end"] - _td(hours=10)
        if any(a0 <= s0 and t0 <= b0 for a0, b0 in orig.get((c["serial"], c["element"]), [])):
            inside += 1
    ok("ask C: each re-sent record, moved back ten hours, lies inside the excursion it repeats", inside == len(rs_written), "%d of %d" % (inside, len(rs_written)))
    short = min((c["end"] - c["start"]).total_seconds() for c in rs_written)
    ok("ask C: every re-sent record spans nine minutes or more (no five-minute average could hide it under 253 V)", short >= 540, "shortest %.0f s" % short)
    sb = R.c_shifted_back(D, U)
    ok("ask C: dropping the re-sent records and moving them back ten hours give the same figures", all(abs(sb[k] - E["voltage_pct"][k]) < 1e-12 for k in sb), "")
    truth_secs = {}
    for e in W["events_written"]:
        if e.get("resent"):
            continue
        s2, t2 = max(e["start"], A.WEEK_UTC[0]), min(e["end"], A.WEEK_UTC[1])
        if t2 > s2:
            truth_secs.setdefault(e["i"], []).append((s2, t2))
    tot = {}
    for i, lst in truth_secs.items():
        u = apts[i]["apt"].replace("-", "")
        tot[u] = R._union(lst)
    ok("ask C: the golden time outside equals each apartment's true excursions for every apartment",
       all(abs(E["secs"].get(u, 0.0) - tot.get(u, 0.0)) < 1e-6 for u in set(tot) | set(E["secs"])), "")

    # --------------------------------------------------------------------------------------- input gates
    exts = {n.rsplit(".", 1)[1] for n in files}
    ok("gate: ten or more files", len(files) >= 10, str(len(files)))
    ok("gate: three or more formats", len(exts) >= 3, str(sorted(exts)))
    big = max(sum(1 for _ in open(os.path.join(target, n))) for n in files if n.endswith(".csv"))
    ok("gate: a file of 25,000 rows or more", big >= 25000, str(big))
    ok("gate: two or more distractors exist in the pack", all(d in files for d in P.DISTRACTORS) and len(P.DISTRACTORS) >= 2, "")
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "t")
    shutil.copytree(target, t2)
    for d in P.DISTRACTORS:
        os.remove(os.path.join(t2, d))
    E2 = A.everything(t2)
    same = (E2["call"]["designated"] == C["designated"] and all(abs(E2["call"]["risers"][k]["share"] - sh[k]) < 1e-12 for k in sh)
            and E2["july_mwh"] == E["july_mwh"] and E2["requests"] == E["requests"] and E2["voltage_pct"] == E["voltage_pct"])
    shutil.rmtree(tmp)
    ok("gate: deleting every distractor leaves the call and every ask unchanged", same, "")
    ok("gate: no file or sheet describes the data", not any(re.search(r"readme|dictionary|field.?notes|manifest|schema", n, re.I) for n in files), "")

    # ----------------------------------------------------------------------------------------- realism
    std = " ".join(D["std_text"].split())
    ok("realism: the standard's text reads back (positive control)", "A charger request is an owner's application" in std and len(std) > 1500, "%d chars" % len(std))
    ok("realism: the rising main schedule reads back with every main", len(D["risers"]) == 18, str(len(D["risers"])))
    ok("realism: no forbidden decisive vocabulary in the standard", not re.search(r"voltage.{0,40}phase|correlat|identif|co-?move|cluster", std, re.I), "")
    nmis = sorted(int(x["nmi"][4:10]) for x in U.values())
    ok("realism: NMIs are no arithmetic sequence", len({b - a for a, b in zip(nmis, nmis[1:])}) > 5, "")
    sers = sorted(int(x["serial"][2:]) for x in U.values())
    ok("realism: meter serials are no arithmetic sequence", len({b - a for a, b in zip(sers, sers[1:])}) > 5, "")
    ok("realism: NMI checksums are valid", all(int(x["nmi"][-1]) == Wd.nmi_checksum(x["nmi"][:-1]) for x in U.values()), "")
    rs = [round(v, 2) for v in E["july_mwh"].values()]
    ok("realism: no two risers share a July use and none is round", len(set(rs)) == len(rs) and not any(abs(v - round(v)) < 0.005 for v in rs), "")
    people = set(re.findall(r"(Kayla Hunt|Alan Herrera)", std))
    ok("realism: the only personas are the card's", people <= {"Kayla Hunt", "Alan Herrera"}, str(people))
    ok("realism: the PQ hourly export covers exactly 12 to 20 July UTC",
       all(s[0][0] == "2026-07-12T00:00:00Z" and s[-1][0] == "2026-07-19T23:00:00Z" for s in D["pq"].values()), "")
    dates_apps = [datetime.strptime(a["Decision date"], "%d/%m/%Y") for a in D["apps"] if a["Decision date"]]
    ok("realism: no committee decision after the register's 31 October 2026 date", max(dates_apps) <= datetime(2026, 10, 31), str(max(dates_apps).date()))
    ok("realism: every lodged date precedes its decision", all(datetime.strptime(a["Lodged"], "%d/%m/%Y") <= datetime.strptime(a["Decision date"], "%d/%m/%Y")
                                                            for a in D["apps"] if a["Decision date"]), "")
    return out
