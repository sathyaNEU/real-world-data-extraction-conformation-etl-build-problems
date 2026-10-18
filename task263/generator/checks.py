"""The generator's assertions on every build: the three rules (R1 raw material, R2 each mess item neutral, R3a the
analyst test, R3b the decisive step alone, R3c no plant), the ladder and the shortcuts beside it, every row of the
semantic fork table (SF1 to SF17), the estimators' convergence and the margins, the asks' goldens against the
generator's truth and their stops, the separation line, the distractors, the input gates, the realism sweep and the
invented names (H21)."""
from __future__ import annotations

import collections
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

import numpy as np

import analysis as A
import common as K
import world as W

PASSED = []
TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(label, cond, detail=""):
    if not cond:
        raise AssertionError("%s %s" % (label, detail))
    PASSED.append(label)


def walk_key(r):
    return (len(r["funded"]), r["stop"], r["left"])


def same_over(a, b):
    return {k: set(v) for k, v in a.items() if v} == {k: set(v) for k, v in b.items() if v}


def clean_truth(D, T):
    """The listed systems' 2024 and 2025 routine and confirmation samples as the world made them: the true blends,
    no laboratory scatter, no reporting limit, the wells pumping and their actual flows."""
    out = []
    for x in T["X"]:
        if not x["listed"] or x["kind"] not in ("RT", "CO") or x["when"].year not in K.WINDOW:
            continue
        out.append(dict(no=x["no"], pws=x["pws"], ep=x["ep"], kind=x["kind"], date=x["when"].date(), on=list(x["on"]),
                        flow=sum(x["flows"].values()), res={a: (x["true"][a], 1e-9) for a in A.AN2}, listed=True,
                        flows=x["flows"]))
    return dict(D, samples=out)


def run(target, T):
    del PASSED[:]
    D = A.load(target)
    G = A.golden(D)
    name = {p["pws"]: p["name"] for p in D["plan"]}
    by_name = {v: k for k, v in name.items()}
    F = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    S = T["S"]
    listed = [s for s in S if s["listed"]]

    # ------------------------------------------------------------------------------------------ the golden
    check("golden: 16 systems reached", len(G["funded"]) == 16, str(len(G["funded"])))
    check("golden: the first system not reached is the Village of Nordvold", name[G["stop"]] == "Village of Nordvold")
    check("golden: $451,200 of the set-aside left", G["left"] == 451200, str(G["left"]))
    check("golden: the write-up's figures.json carries the same call",
          F["call"] == dict(systems_reached=16, first_not_reached="Village of Nordvold", left=451200, grants_made=35548800,
                            stop_grant=691200))
    truth = W.golden_grants(listed)
    check("golden: every system's grant equals the generator's truth (the wells' own water before any sampling)",
          all(G["grants"][s["pws"]] == truth[s["name"]] for s in listed))
    tw = {s["pws"]: {(w["ep"], w["no"]) for w in s["wells"] if w["status"] == "Active" and W.own_level(w) > K.LINE}
          for s in listed}
    check("golden: the wells over the line are exactly the wells whose own water is over 4.0 ng/L (23 wells)",
          same_over(G["over"], tw) and sum(len(v) for v in tw.values()) == 23)
    near = min(abs(max(v) - K.LINE) for lv in G["levels"].values() for v in lv.values())
    check("golden: no well's estimated own level within 1.0 ng/L of the line", near > 1.0, "%.3f" % near)
    check("golden: every listed entry point is identifiable from its 2024 and 2025 samples (full rank) and from its "
          "routine samples alone", all(v is not None for v in G["levels"].values()) and
          all(v is not None for v in A.own_levels(D, kinds=("RT",)).values()))
    nsamp = collections.Counter((x["pws"], x["ep"]) for x in A.window(D))
    check("golden: every listed entry point has 8 or more samples in the window", min(nsamp.values()) >= 8,
          str(min(nsamp.values())))

    # ------------------------------------------------------------------------------------------ R: the three rules
    heads = {}
    for k in ("results", "records", "mor", "meters", "register", "connections"):
        with open(os.path.join(target, K.FILES[k]), encoding="utf-8") as fh:
            heads[k] = next(csv.reader(fh))
    check("R1 the field's raw material ships: entry-point results by sample and analyte, and a collection record per "
          "sample naming the wells pumping and the entry-point flow",
          {"state_sample_no", "sample_point", "analyte", "result", "result_sign"} <= set(heads["results"]) and
          {"state_sample_no", "sources_in_service", "ep_flow_gpm"} <= set(heads["records"]))
    banned = re.compile(r"own|share|fraction|proportion|well_level|eligib|grant|over_line", re.I)
    check("R1 no shipped column holds the deciding quantity (no well's own level, mixing share, eligibility or grant)",
          not any(banned.search(c) for k in heads for c in heads[k]), str([c for k in heads for c in heads[k]
                                                                          if banned.search(c)]))
    check("R1 the golden's decisive computation reads the sample rows: %d samples across 24 entry points" %
          len(A.window(D)), len(A.window(D)) == sum(nsamp.values()) and len(nsamp) == 24)
    # R2: each Layer 1 item mishandled leaves the call where it was
    base = walk_key(G)
    for label, kw in (("non-detects at zero", dict(nd=0.0)), ("non-detects at the reporting limit", dict(nd=1.0)),
                      ("field duplicates kept as samples", dict(kinds=("RT", "CO", "FD"))),
                      ("2026 samples kept (past the plan's years)", dict(years=(2024, 2025, 2026))),
                      ("blank sources in service inferred from the entry-point flow", dict(missing="infer"))):
        o = A.over_from_levels(A.own_levels(D, **kw))
        check("R2 mess neutral: %s keeps the same 23 wells and the golden walk" % label,
              same_over(o, G["over"]) and walk_key(A.route(D, o)) == base)
    rows_frb = [dict(x, on=x["on"]) for x in D["samples"] if x["listed"] and x["kind"] in ("RT", "CO", "FRB") and
                x["date"].year in K.WINDOW and x["on"] is not None]
    o = A.over_from_levels(A.own_levels(D, rows=rows_frb))
    check("R2 mess neutral: field reagent blanks kept as samples (non-detects at half the limit) keep the golden",
          same_over(o, G["over"]))
    D_both = both_revisions(D, target)
    o = A.over_from_levels(A.own_levels(D_both))
    check("R2 mess neutral: both report revisions kept keeps the golden", same_over(o, G["over"]))
    check("R2 mess neutral: the statewide export filtered to Table 6-1's PWS ids gives the twenty listed systems",
          len({x["pws"] for x in D["samples"] if x["listed"]}) == 20)
    check("R2 mess neutral: the 537.1 laboratory's analyte list carries PFOA and PFOS for every sample it ran",
          all(set(A.AN2) <= set(x["res"]) for x in D["samples"]))
    check("R2 mess neutral: month-first collection dates read day-first move no 2024 or 2025 sample across the "
          "window's ends", day_first_safe(target))
    # R3: the analyst test on the clean truth
    C = clean_truth(D, T)
    r0 = A.route(C, A.presence(C))
    check("R3a the analyst test on the clean truth: each well given the average of the samples it ran in files 7 "
          "systems, stopping at the Village of Nesvold", len(r0["funded"]) == 7 and name[r0["stop"]] == "Village of Nesvold",
          str((len(r0["funded"]), name.get(r0["stop"]))))
    lv = {}
    for ep in {(x["pws"], x["ep"]) for x in C["samples"]}:
        rr = [x for x in C["samples"] if (x["pws"], x["ep"]) == ep]
        nos = sorted(D["wells"][ep])
        M = np.zeros((len(rr), len(nos)))
        for i, x in enumerate(rr):
            t = sum(x["flows"].values())
            for n in x["on"]:
                M[i, nos.index(n)] = x["flows"][n] / t
        ests = [np.linalg.lstsq(M, np.array([x["res"][a][0] for x in rr]), rcond=None)[0] for a in A.AN2]
        lv[ep] = {n: (float(ests[0][i]), float(ests[1][i])) for i, n in enumerate(nos)}
    r3 = A.route(C, A.over_from_levels(lv))
    check("R3b the decisive step alone on the clean truth (each entry point's samples solved as a mass balance) files "
          "the golden: 16 systems, stopping at Nordvold", walk_key(r3)[:2] == base[:2] and
          same_over(A.over_from_levels(lv), tw))
    for lab, o, n_exp in (("the flow-share weighted average", A.presence(C, weight=True), 8),
                          ("the samples a well ran alone", A.solo(C), 11)):
        r = A.route(C, o)
        check("R3b one correction alone stays wrong on the clean truth: %s files %d systems" % (lab, n_exp),
              len(r["funded"]) == n_exp and r["stop"] != G["stop"])
    check("R3c no plant: no sample's results (four or more detections) repeat another sample's except a reissued "
          "report of itself",
          no_repeated_samples(target))
    texts = all_text(target)
    check("R3c no plant: no shipped file names a well's own level, a mixing share, a mass balance or a grant amount",
          not any(re.search(r"mass balance|unmix|own level|mixing (share|proportion)|least squares|\$[0-9,]{7,} grant",
                            t, re.I) for f, t in texts.items()))
    check("R3c no plant: the plan names no system's grant, eligible well or reach",
          not re.search(r"Well \d|eligible capacity of|reaches \d", texts[K.FILES["iup"]]))

    # ------------------------------------------------------------------------------------------ the ladder
    rungs = [("R0 (default) the average of the samples a well ran in", A.presence(D), 7, "Village of Nesvold", 672000),
             ("R1 the same average weighted by flow share", A.presence(D, weight=True), 8, "Elvholm Falls Water Utility", 2400000),
             ("R2 the samples a well ran alone, its average where it never did", A.solo(D), 11, "Skogen Municipal Water", 1708800),
             ("R3 the mass balance (golden)", G["over"], 16, "Village of Nordvold", 451200)]
    seen = set()
    for lab, o, n, stop, left in rungs:
        r = A.route(D, o)
        check("ladder: %s files %d systems, stops at %s, leaves $%s" % (lab, n, stop, "{:,}".format(left)),
              (len(r["funded"]), name[r["stop"]], r["left"]) == (n, stop, left),
              str((len(r["funded"]), name.get(r["stop"]), r["left"])))
        seen.add((n, stop, left))
    check("ladder: every rung names a different count, stop and balance", len(seen) == 4)
    for lab, o, n, stop in (("every well at an entry point with a result over 4.0", A.ep_route(D), 6, "Kesselring Waterworks"),
                            ("the wells pumping at a result over 4.0", A.pumping_at_exceedance(D), 6, "Kesselring Waterworks"),
                            ("the median of a well's samples", A.presence(D, agg=np.median), 8, "Elvholm Falls Water Utility"),
                            ("the wells in each entry point's highest sample", A.top_sample(D), 13,
                             "Isaksen Ridge Sanitary District No. 1"),
                            ("the samples a well ran alone, nothing where it never did", A.solo(D, False), 19, None)):
        r = A.route(D, o)
        check("cells: %s files %d systems (%s)" % (lab, n, stop or "nobody left out"),
              len(r["funded"]) == n and (name.get(r["stop"]) if r["stop"] else None) == stop,
              str((len(r["funded"]), name.get(r["stop"]))))
    r0g = A.route(D, A.presence(D))
    hits = sum(1 for p in G["funded"] if p in r0g["funded"] and r0g["grants"][p] == G["grants"][p])
    check("ladder worth: R0 gets 1 of the golden's 16 grants", hits == 1, str(hits))
    for lab, o in (("R0", A.presence(D)), ("R1", A.presence(D, weight=True)), ("R2", A.solo(D))):
        for nd in (0.0, 1.0):
            pass
    # the rungs hold under each reading of the non-detects
    for nd in (0.0, 1.0):
        D2 = dict(D)
        old = A.value
        A.value = (lambda x, a, nd2=nd, f=old: f(x, a, nd2))
        try:
            ks = [walk_key(A.route(D2, f()))[:2] for f in (lambda: A.presence(D2), lambda: A.presence(D2, weight=True),
                                                            lambda: A.solo(D2))]
        finally:
            A.value = old
        check("ladder: the rungs file 7, 8 and 11 systems with non-detects at %.1f times the limit" % nd,
              [k[0] for k in ks] == [7, 8, 11])

    # ------------------------------------------------------------------------------------------ convergence
    for lab, kw in (("non-negative least squares", dict(solver="nnls")), ("chained subtraction", dict(method="chained")),
                    ("the entry-point flow shared by capacity", dict(weights="flow")),
                    ("equal shares", dict(weights="equal")), ("routine samples only", dict(kinds=("RT",)))):
        lvx = A.own_levels(D, **kw)
        o = A.over_from_levels(lvx)
        check("convergence: %s flags the same 23 wells and files the golden" % lab,
              all(v is not None for v in lvx.values()) and same_over(o, G["over"]) and walk_key(A.route(D, o)) == base)
    o = A.over_from_levels(G["levels"], rule="sum")
    check("convergence: the sum of PFOA and PFOS against 4.0 flags the same wells", same_over(o, G["over"]))

    # ------------------------------------------------------------------------------------------ the fork table
    check("SF1 the systems on the list: Table 6-1's twenty, in order", [p["rank"] for p in D["plan"]] == list(range(1, 21)))
    r = A.route(D, A.ep_route(D))
    check("SF2 the entry point's water read as each well's files 6 systems (ruled out by the plan's own-water sentence)",
          len(r["funded"]) == 6 and "the water the well itself pumps" in texts[K.FILES["iup"]])
    check("SF3 the years: 2026 samples added or routine samples alone keep the call",
          walk_key(A.route(D, A.over_from_levels(A.own_levels(D, years=(2024, 2025, 2026))))) == base and
          walk_key(A.route(D, A.over_from_levels(A.own_levels(D, kinds=("RT",))))) == base)
    check("SF4 either analyte over 4.0, not their sum: same call either way", walk_key(A.route(D, o)) == base)
    check("SF5 'more than' against '4.0 or more': no estimate within 1.0 ng/L of 4.0", near > 1.0)
    em = [f for f in D["inv"] if f["status"] == "Emergency" and f["pws_id"] in D["listed"]]
    check("SF6 active wells: the listed systems' one emergency well ran at no sample, so it has no own water to judge",
          len(em) == 2 and all(f["facility_id"] not in sampled_facilities(D) for f in em))
    check("SF7 rated capacity: the plan names the inventory's rated capacity",
          "Rated capacity is the capacity the department's source facility inventory records" in texts[K.FILES["iup"]])
    check("SF8 MGD: every rated capacity of a listed system's well is a whole number of gallons a minute, so each "
          "grant is exact to the dollar", all(isinstance(g, int) for g in G["grants"].values()))
    check("SF9 the cap: Halvorsen's two wells over the line (1,800 gpm, $6,220,800) are capped at $6,000,000",
          G["grants"][by_name["City of Halvorsen Water Department"]] == 6000000)
    rs = A.walk(D, G["grants"], skip=True)
    check("SF10 stops: skipping Nordvold and funding later grants that fit gives the same 16 (none fits $451,200)",
          (len(rs["funded"]), rs["left"]) == (16, 451200))
    check("SF11 the order: the plan funds in the order of Table 6-1", "in the order of Table 6-1" in texts[K.FILES["iup"]])
    check("SF12 reach: every listed system has a well over the line, so every system has a grant above zero",
          all(G["grants"][p["pws"]] > 0 for p in D["plan"]))
    check("SF13 left: $36,000,000 less the sixteen grants", K.FUND - sum(G["grants"][p] for p in G["funded"]) == G["left"])
    check("SF14 non-detects at zero, half or the limit flag the same wells",
          all(same_over(A.over_from_levels(A.own_levels(D, nd=nd)), G["over"]) for nd in (0.0, 0.5, 1.0)))
    check("SF15 quality-control samples and reissued reports: duplicates, blanks or both revisions kept, same wells",
          same_over(A.over_from_levels(A.own_levels(D, kinds=("RT", "CO", "FD"))), G["over"]) and
          same_over(A.over_from_levels(A.own_levels(D_both)), G["over"]))
    check("SF16 the mixing proportions: rated capacities, the entry-point flow or equal shares, same wells",
          all(same_over(A.over_from_levels(A.own_levels(D, weights=w)), G["over"]) for w in ("rated", "flow", "equal")))
    mv = monthly_volume_route(D, target)
    check("SF16 the 2025 monthly volumes as mixing proportions file %d systems, ruled out by the inventory's note that a "
          "well delivers its rated discharge whenever it runs" % len(mv["funded"]),
          walk_key(mv)[:2] != base[:2] and "delivers its rated discharge whenever it runs" in texts[K.FILES["inventory"]])
    nblank = sum(1 for x in D["samples"] if x["listed"] and x["on"] is None and x["date"].year in K.WINDOW)
    check("SF17 sources not recorded (%d samples): left out or inferred from the entry-point flow, same call" % nblank,
          nblank > 0 and walk_key(A.route(D, A.over_from_levels(A.own_levels(D, missing="infer")))) == base)

    # ------------------------------------------------------------------------------------------ the asks
    aa = A.ask_a(D, target)
    truth_a = {c: round(v / 1e6, 1) for c, v in W.pumped_by_county(S, T["ops"]).items()}
    check("Ask A: the golden equals the generator's truth (each well once)", aa == truth_a, str((aa, truth_a)))
    check("Ask A: figures.json carries it", F["ask_a"] == aa)
    edges = [abs((v * 10) % 1 - 0.5) for v in (x / 1e6 for x in W.pumped_by_county(S, T["ops"]).values())]
    check("Ask A: every county's figure sits at least 0.05 of a rounding step from an edge", min(
        abs(((v / 1e5) % 1) - 0.5) for v in W.pumped_by_county(S, T["ops"]).values()) > 0.05)
    for mode, lab, counties in (("every_row", "every row of the reports (shared meters on both wells)", None),
                                ("active_only", "active wells only", ["Hedstrom"]),
                                ("readings", "the meter readings in place of the gallons", ["Granlund"]),
                                ("every_row_all", "every row, purchased water included", None)):
        v = A.ask_a(D, target, mode)
        miss = [c for c in aa if abs(v[c] - aa[c]) > 0.05]
        check("Ask A stop: %s misses %s" % (lab, "every county" if counties is None else ", ".join(counties)),
              (len(miss) == 4) if counties is None else set(counties) <= set(miss), str(v))
    ab = A.ask_b(D, target)
    check("Ask B: the golden equals the generator's truth (chains of full purchases in service)",
          ab == W.people_reached(S, T["conns"]), str(ab))
    check("Ask B: figures.json carries it", F["ask_b"] == ab)
    for mode, lab, counties in (("listed", "the listed systems alone", None), ("one_step", "buyers one step out", None),
                                ("as_found", "the chains, each id's register row as found", None),
                                ("active_only", "the chains, inactive ids left out", None),
                                ("every_tie", "every tie followed", ["Granlund", "Sandholm"])):
        v = A.ask_b(D, target, mode)
        miss = [c for c in ab if v.get(c) != ab[c]]
        check("Ask B stop: %s misses %s" % (lab, "every county" if counties is None else ", ".join(counties)),
              (len(miss) == 4) if counties is None else set(counties) == set(miss), str(v))
    two = [m for m in A.rd(target, K.FILES["meters"]) if ";" in m["facility_ids"]]
    lst = {p["pws"] for p in D["plan"]}
    cty = {p["pws"]: p["county"] for p in D["plan"]}
    check("Ask A device: one shared header meter at a listed system in each county, and three off the list",
          sorted(cty[m["pws_id"]] for m in two if m["pws_id"] in lst) == sorted(("Granlund", "Engvall", "Hedstrom", "Sandholm"))
          and sum(1 for m in two if m["pws_id"] not in lst) == 3)
    check("Ask B device: a buyer of a buyer in each county", chains_by_county(target, D) == {"Granlund", "Engvall",
                                                                                             "Hedstrom", "Sandholm"})
    reg = {r["pws_id"]: r for r in A.rd(target, K.FILES["register"])}
    con = A.rd(target, K.FILES["connections"])
    ren = [s for s in S if s.get("old_pws")]
    check("Ask B device: a buyer in each county renumbered on a change of owner, the register holding the old id as an "
          "inactive system of the same name and county at an older population, every connection still on the old id",
          sorted(s["county"] for s in ren) == sorted(("Granlund", "Engvall", "Hedstrom", "Sandholm")) and
          all(reg[s["old_pws"]]["status"] == "Inactive" and reg[s["pws"]]["status"] == "Active" and
              reg[s["old_pws"]]["system_name"] == reg[s["pws"]]["system_name"] and
              reg[s["old_pws"]]["county"] == reg[s["pws"]]["county"] and
              reg[s["old_pws"]]["population_served"] != reg[s["pws"]]["population_served"] for s in ren) and
          not any(s["pws"] in (x["buyer_pws_id"], x["seller_pws_id"]) for s in ren for x in con) and
          all(any(s["old_pws"] in (x["buyer_pws_id"], x["seller_pws_id"]) for x in con) for s in ren))
    check("Ask B device: no other active system shares an inactive id's name and county (the closed systems the "
          "register keeps match none)", sum(1 for r in reg.values() if r["status"] == "Inactive" and any(
              q["status"] == "Active" and q["system_name"] == r["system_name"] and q["county"] == r["county"]
              for q in reg.values())) == len(ren))

    import cracker as CR
    rows_cr = CR.score(target)
    _, lc, ls, pair = CR.ceiling(rows_cr, rows_cr)
    check("cracker.py on the cut pack: the cracker keeps no ask figure (%s), pair ceiling %.1f" % (
        ", ".join("%s %d of %d" % (a, h, n) for a, n, h in rows_cr), pair), lc == 0 and pair <= 40)

    # ------------------------------------------------------------------------------------------ separation, distractors
    check("separation: the call computed from the call's files alone (results, records, inventory, plan) equals the "
          "golden", call_alone(target, G))
    for k in K.DISTRACTORS:
        check("distractor: %s deleted leaves the call and both asks unchanged" % K.FILES[k], without(target, K.FILES[k], G,
                                                                                                     aa, ab))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("distractors named in metadata.json by bundle path", sorted(meta["distractor_files"]) ==
          sorted("target/" + K.FILES[k] for k in K.DISTRACTORS))
    check("no shipped file name says distractor, decoy or answer", not any(re.search(r"distract|decoy|answer|truth", f, re.I)
                                                                         for f in os.listdir(target)))

    # ------------------------------------------------------------------------------------------ input gates
    files = os.listdir(target)
    check("input gate: 10 or more files (%d)" % len(files), len(files) >= 10)
    check("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    nres = sum(1 for _ in open(os.path.join(target, K.FILES["results"]), encoding="utf-8")) - 1
    check("input gate: a file of 25,000 or more rows (results, %d)" % nres, nres >= 25000)
    check("input gate: two or more distractors", len(meta["distractor_files"]) >= 2)

    # ------------------------------------------------------------------------------------------ realism
    check("realism: every 2025 sample's wells in service ran on at least one day of that month in the operating reports",
          mor_consistent(target, D))
    check("realism: every listed record's entry-point flow is within 7 per cent of its wells' rated capacities",
          all(abs(x["flow"] - sum(D["wells"][(x["pws"], x["ep"])][n] for n in x["on"])) <=
              0.07 * sum(D["wells"][(x["pws"], x["ep"])][n] for n in x["on"]) for x in D["samples"]
              if x["listed"] and x["on"]))
    check("realism: no em or en dash in any shipped text", not any("—" in t or "–" in t for t in texts.values()))
    people = set(re.findall(r"\b(Judy Carey|Lynn Whitaker)\b", " ".join(texts.values())))
    check("realism: the only people named are the two drawn personas", people <= {"Judy Carey", "Lynn Whitaker"} and
          not re.search(r"\b(John|Jane) (Doe|Smith)\b|Acme|Company [A-Z]\b", " ".join(texts.values())))
    check("realism: every shipped file carries the export's timestamp",
          len({int(os.path.getmtime(os.path.join(target, f))) for f in files}) == 1)
    check("realism: no monthly volume repeated across three facilities, or across two with the same days in service, "
          "beyond the shared meters' twin rows",
          mor_unique(target))
    pops = [int(r["population_served"]) for r in A.rd(target, K.FILES["register"])]
    check("realism: no round populations among the listed systems and their buyers (multiples of 100)",
          not any(p["pop"] % 100 == 0 for p in D["plan"]))
    check("H21 invented names clear of real places (no distinctive word within one edit of a real US place on the "
          "near-miss register, no retired name surviving)", h21(texts))
    print("checks: %d assertions passed" % len(PASSED))
    return PASSED


# ---------------------------------------------------------------------------------------------- helpers
def monthly_volume_route(D, target):
    """The mass balance with each 2025 sample's wells weighted by their month's pumped volume (2024 by capacity)."""
    fid = {(f["pws_id"], f["entry_point"], int(f["facility_name"].split()[-1])): f["facility_id"] for f in D["inv"]
           if f["facility_type"] == "Well" and f["entry_point"]}
    vol = {(r["facility_id"], int(r["report_month"][5:])): int(r["volume_gal"]) for r in A.rd(target, K.FILES["mor"])}
    by = collections.defaultdict(list)
    for x in A.window(D):
        by[(x["pws"], x["ep"])].append(x)
    levels = {}
    for ep, rr in by.items():
        w = D["wells"][ep]
        nos = sorted(w)
        M = np.zeros((len(rr), len(nos)))
        Y = np.zeros((len(rr), 2))
        for i, x in enumerate(rr):
            q = ({n: max(vol.get((fid[(ep[0], ep[1], n)], x["date"].month), 0), 1) for n in x["on"]}
                 if x["date"].year == 2025 else {n: w[n] for n in x["on"]})
            t = sum(q.values())
            for n in x["on"]:
                M[i, nos.index(n)] = q[n] / t
            Y[i] = [A.value(x, "PFOA"), A.value(x, "PFOS")]
        B = np.linalg.lstsq(M, Y, rcond=None)[0]
        levels[ep] = {n: (float(B[j, 0]), float(B[j, 1])) for j, n in enumerate(nos)}
    return A.route(D, A.over_from_levels(levels))


def both_revisions(D, target):
    """The samples with every report revision kept as a separate sample."""
    rec = {r["state_sample_no"]: r for r in A.rd(target, K.FILES["records"])}
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in A.rd(target, K.FILES["results"]):
        by[r["state_sample_no"]][int(r["report_revision"])][r["analyte"]] = (
            None if r["result_sign"] == "<" else float(r["result"]), float(r["reporting_limit"]))
    out = []
    for x in D["samples"]:
        for rev, res in by[x["no"]].items():
            out.append(dict(x, res=res))
    return dict(D, samples=out)


def day_first_safe(target):
    for r in A.rd(target, K.FILES["records"]):
        m, d, y = r["collected"][:10].split("/")
        if int(m) <= 12 and int(d) <= 12:
            if (int(y) in K.WINDOW) != (int(y) in K.WINDOW):
                return False
    return True


def no_repeated_samples(target):
    vec = collections.defaultdict(dict)
    for r in A.rd(target, K.FILES["results"]):
        vec[(r["state_sample_no"], r["report_revision"])][r["analyte"]] = r["result"]
    seen = {}
    for (no, rev), v in vec.items():
        key = tuple(sorted(v.items()))
        if sum(1 for _, x in key if x) < 4:          # a near-empty report (one or two traces) can coincide honestly
            continue
        if key in seen and seen[key] != no:
            return False
        seen[key] = no
    return True


def sampled_facilities(D):
    fid = {(f["pws_id"], f["entry_point"], int(f["facility_name"].split()[-1])): f["facility_id"] for f in D["inv"]
           if f["facility_type"] == "Well" and f["entry_point"]}
    return {fid.get((x["pws"], x["ep"], n)) for x in D["samples"] if x["on"] for n in x["on"]}


def chains_by_county(target, D):
    reg = {r["pws_id"]: r for r in A.rd(target, K.FILES["register"])}
    con = [c for c in A.rd(target, K.FILES["connections"]) if c["connection_type"] == "Full purchase" and not c["in_service_to"]]
    first = {c["buyer_pws_id"] for c in con if c["seller_pws_id"] in D["listed"]}
    second = {c["buyer_pws_id"] for c in con if c["seller_pws_id"] in first}
    return {reg[p]["county"] for p in second}


def mor_consistent(target, D):
    days = {}
    for r in A.rd(target, K.FILES["mor"]):
        days[(r["facility_id"], int(r["report_month"][5:]))] = int(r["days_in_service"])
    fid = {(f["pws_id"], f["entry_point"], int(f["facility_name"].split()[-1])): f["facility_id"] for f in D["inv"]
           if f["facility_type"] == "Well" and f["entry_point"]}
    for x in D["samples"]:
        if x["date"].year != 2025 or not x["on"] or (x["pws"], x["ep"], x["on"][0]) not in fid:
            continue
        for n in x["on"]:
            if days.get((fid[(x["pws"], x["ep"], n)], x["date"].month), 0) < 1:
                return False
    return True


def mor_unique(target):
    shared = set()
    for m in A.rd(target, K.FILES["meters"]):
        if ";" in m["facility_ids"]:
            shared |= set(m["facility_ids"].split(";"))
    seen = collections.defaultdict(list)
    for r in A.rd(target, K.FILES["mor"]):
        if int(r["volume_gal"]) > 0 and r["facility_id"] not in shared:
            seen[(r["report_month"], r["volume_gal"])].append(r["days_in_service"])
    # an exact coincidence between two unrelated wells that ran different days is honest; a value repeating across
    # three wells, or two wells sharing the volume and the days, is a capped or copied stream
    return all(len(v) == 1 or (len(v) == 2 and v[0] != v[1]) for v in seen.values())


def all_text(folder):
    out = {}
    for f in os.listdir(folder):
        p = os.path.join(folder, f)
        if f.endswith(".pdf"):
            out[f] = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True,
                                                         text=True).stdout)
        elif f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                xml = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
            out[f] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", xml))
        else:
            out[f] = open(p, encoding="utf-8").read()
    return out


def call_alone(target, G):
    tmp = tempfile.mkdtemp()
    try:
        for k in K.CALL_FILES:
            shutil.copy(os.path.join(target, K.FILES[k]), tmp)
        D2 = A.load(tmp)
        G2 = A.golden(D2)
        return walk_key(G2) == walk_key(G) and G2["grants"] == G["grants"]
    finally:
        shutil.rmtree(tmp)


def without(target, name, G, aa, ab):
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f != name:
                shutil.copy(os.path.join(target, f), tmp)
        D2 = A.load(tmp)
        G2 = A.golden(D2)
        return walk_key(G2) == walk_key(G) and A.ask_a(D2, tmp) == aa and A.ask_b(D2, tmp) == ab
    finally:
        shutil.rmtree(tmp)


# the US places nearest the invented names (zip-code places of every state, every county, cities over 15,000; each
# within two edits of an invented word) and the names this build retired after screening
REAL = ['almont', 'alstead', 'ardmore', 'aredale', 'ashland', 'bellwood', 'bergland', 'bergman', 'birnamwood',
        'blackford', 'boswell', 'bracken', 'braidwood', 'branford', 'brantwood', 'breeden', 'breese', 'breien',
        'bremen', 'brentford', 'briarwood', 'broken', 'bronwood', 'carland', 'causland', 'clarkfork', 'clelland',
        'coalwood', 'cogswell', 'colbert', 'cranford', 'deadwood', 'dellwood', 'doswell', 'eastland', 'echola',
        'echols', 'edgerton', 'ellwood', 'elwood', 'farland', 'fennimore', 'fossil', 'gapland', 'glendale',
        'glenford', 'glenhope', 'glenmont', 'grayland', 'greeley', 'greendale', 'greenford', 'halstad', 'harford',
        'hartford', 'henley', 'horsham', 'irondale', 'kaiser', 'keesler', 'keiser', 'kendale', 'kenmore', 'kesler',
        'kessler', 'kieler', 'kleberg', 'kneeland', 'landes', 'langford', 'lansford', 'larimore', 'lonsdale',
        'lowber', 'lundys', 'marlboro', 'marlton', 'marmora', 'melba', 'melmore', 'millmont', 'millstadt', 'milmont',
        'modale', 'morvin', 'mosheim', 'nenglewood', 'noorvik', 'oberlin', 'olcott', 'opal', 'opheim', 'orrum',
        'otter', 'ottine', 'overgaard', 'owendale', 'ragland', 'rayland', 'raywood', 'redford', 'rigby', 'roby',
        'rodney', 'romney', 'ronco', 'ronneby', 'rosedale', 'rossburg', 'roswell', 'roundo', 'royal', 'rugby',
        'rydal', 'sandhill', 'sedmeston', 'selby', 'shelby', 'solen', 'solvang', 'taberg', 'temvik', 'topsail',
        'topsham', 'udall', 'uleta', 'ulster', 'uriah', 'vesta', 'vestal', 'volborg', 'vossburg', 'wesley',
        'wickett', 'wolcott', 'wrigley']
RETIRED = ['tillerton', 'halloway', 'marsden', 'westmere', 'brennan', 'quenby', 'corrigan', 'lindell', 'ashgrove',
           'paxton', 'dalby', 'sedgwick', 'kettering', 'ivanhoe', 'fenwick', 'vantage', 'norrell', 'garvey', 'ellery',
           'orrin', 'harlow', 'corran', 'ostrem', 'danvers', 'kittredge', 'northgate', 'brookfield', 'ridgeway',
           'eastfork', 'kilby', 'allard', 'lakemont', 'ridgeline']
GENERIC = set("""lake lakes falls prairie ridge creek hollow heights grove valley bluff point springs crossing mills corners
city village town of water utility sanitary district no municipal mobile home park estates waterworks department
cooperative rural association junction east west north south court township regional and light the county state
environmental health laboratory analytical testing inc emergency interconnect treatment plant home""".split())


def h21(texts):
    def lev(a, b):
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            cur = [i]
            for j, cb in enumerate(b, 1):
                cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
            prev = cur
        return prev[-1]
    S, conns = W.statewide()
    import records as R
    names = {s["full"] for s in S} | set(K.COUNTIES) | {l[1] for l in R.LABS} | {l[2] for l in R.LABS} | \
        {t for v in R.TOWNS.values() for t in v}
    words = {w for n in names for w in re.sub(r"[^a-z ]", " ", n.lower()).split() if w not in GENERIC and len(w) >= 4}
    for w in words:
        for r in REAL:
            if (len(w) >= 5 and lev(w, r) <= 1) or w == r:
                return False
    blob = " ".join(texts.values()).lower()
    return not any(re.search(r"\b%s\b" % r, blob) for r in RETIRED)
