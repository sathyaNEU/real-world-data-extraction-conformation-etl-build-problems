"""The generator's assertions on every build: the three rules (R1 raw material, R2 each mess item neutral, R3a the
analyst test, R3b the decisive step alone, R3c no plant), the ladder and the shortcuts beside it, every row of the
semantic fork table (SF1 to SF17), the estimators' convergence and the margins, the ask's golden against the
generator's truth, its stops, its forcing and its silence, the separation line (the call's files byte-identical to the
shipped cut), the distractors, the screen that no shipped file or sheet
describes the data (by name and by content, each positive-controlled), the provenance in metadata.json, the input
gates, the realism sweep and the invented names (H21)."""
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
import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader

import analysis as A
import common as K
import verify as V
import world as W

PASSED = []
TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the files the call reads, as the shipped cut carried them (target.zip c38b70927ef7065db923fe1d22411dca, 2026-11-01)
SHIPPED_CALL_MD5 = {"results": "73a1363a5c217432f122ed7bc065d8a4", "records": "bae22579527947c549c5277fbd1a6c7c",
                    "inventory": "380c66ed79239b82d168718baac2bb14", "iup": "ed262b26a9e54e712c23ee322d7e08c9",
                    "guide": "e173cef2301a76d7866ab0df42bbbdb1"}


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
    r0o = A.presence(D)
    epo = A.ep_route(D)
    check("survivor anatomy, back-test: every well R0 puts over the line stands at an entry point with a result over 4.0",
          all(set(v) <= set(epo.get(k, set())) for k, v in r0o.items()))
    sst = collections.defaultdict(list)
    for x in A.window(D):
        for n in x["on"]:
            sst[(x["pws"], x["ep"], n)].append(max(A.value(x, "PFOA"), A.value(x, "PFOS")))
    gw = {(p, e, n) for p, s in G["over"].items() for e, n in s}
    aw = [(p, e, n) for (p, e), w in D["wells"].items() if p in D["listed"] for n in w]
    tops = [set(sorted(aw, key=lambda k, f=f: -f(sst[k]))[:len(gw)]) for f in (np.mean, np.median, np.max, np.min)]
    tops.append(set(sorted(aw, key=lambda k: -D["wells"][(k[0], k[1])][k[2]])[:len(gw)]))
    check("survivor anatomy, shock: no sort of the active wells by the mean, median, highest or lowest of the samples "
          "each ran in, or by rated capacity, puts the golden's 23 on top", all(t != gw for t in tops))
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
    inv = V.inventory(target)                       # the verifier's own xlsx reader
    wells = inv[inv.facility_type == "Well"]
    cols = list(inv.columns)
    check("SF16 control: the verifier's xlsx reader finds the inventory's pump column beside rated capacity, %d well "
          "rows, both pump types" % len(wells),
          cols.index("pump") == cols.index("rated_capacity_gpm") + 1 and len(wells) >= 200 and
          set(wells.pump.str.rsplit(", ", n=1).str[0]) == {"Vertical turbine", "Submersible"})
    check("SF16 the pump fact is filed once, in the inventory's own pump column: every well's pump on a constant-speed "
          "drive, the plants and the interconnection blank, and no other shipped file says it",
          bool(wells.pump.str.endswith(", constant speed").all()) and
          bool(inv[inv.facility_type != "Well"].pump.isna().all()) and
          [f for f, t in texts.items() if re.search(r"constant[ -]speed", t, re.I)] == [K.FILES["inventory"]])
    check("SF16 the plan does not carry the pump fact (read by the checks' extractor and by the verifier's), and its "
          "own-water sentence is read by both",
          not any(re.search(r"constant[ -]speed|whenever it runs|rated discharge", t, re.I)
                  for t in (texts[K.FILES["iup"]], pypdf_text(target, K.FILES["iup"]))) and
          all("A well's own water is the water the well itself pumps." in t
              for t in (texts[K.FILES["iup"]], pypdf_text(target, K.FILES["iup"]))))
    gap, mid, nrec = flow_gap(target)
    check("SF16 the entry-point flow on every listed record with its wells recorded matches the running wells' rated "
          "capacities to within 7 per cent (the verifier's readers, %d records, median gap %.1f per cent, largest %.1f)"
          % (nrec, 100 * mid, 100 * gap), gap <= 0.07 and mid <= 0.02 and nrec >= 300)
    check("SF16 the 2025 monthly volumes as mixing proportions file %d systems, ruled out by the pump column and the "
          "entry-point flow (a constant-speed well pumps at its rated capacity whenever it runs)" % len(mv["funded"]),
          walk_key(mv)[:2] != base[:2])
    nblank = sum(1 for x in D["samples"] if x["listed"] and x["on"] is None and x["date"].year in K.WINDOW)
    check("SF17 sources not recorded (%d samples): left out or inferred from the entry-point flow, same call" % nblank,
          nblank > 0 and walk_key(A.route(D, A.over_from_levels(A.own_levels(D, missing="infer")))) == base)

    # ------------------------------------------------------------------------------------------ the ask
    # the water the listed systems' wells pumped in 2025, by Table 6-1's county and calendar quarter (16 figures)
    aa = A.ask_a(D, target)
    tq = W.pumped_by_county_quarter(S, T["ops"])
    check("Ask: the golden equals the generator's truth (each well's own water once, by county and quarter)",
          aa == {c: {q: round(v / 1e6, 1) for q, v in d.items()} for c, d in tq.items()}, str(aa))
    check("Ask: figures.json carries it, 16 figures", F["ask_a"] == aa and sum(len(v) for v in aa.values()) == 16)
    edge = min(abs(((v / 1e5) % 1) - 0.5) for d in tq.values() for v in d.values())
    check("Ask: every county-quarter figure sits at least a tenth of a rounding step from an edge (%.3f)" % edge,
          edge >= 0.10)
    for mode, lab, cells in (("careful", "the careful solver's route (wells only, each register meter once)", 16),
                             ("every_row", "every line as written", 16),
                             ("every_row_all", "every line, the interconnection's purchase in", 16),
                             ("over", "only the overloaded well's line at its entry point", 16),
                             ("readings", "the golden from the meter readings (the June meter change)", 1),
                             ("active_only", "the golden with active wells only (the emergency well out)", 1)):
        v = A.ask_a(D, target, mode)
        miss = [(c, q) for c in aa for q in aa[c] if abs(v.get(c, {}).get(q, 0) - aa[c][q]) > 0.05]
        check("Ask stop: %s misses %d of 16" % (lab, cells), len(miss) == cells, str(v))
    cv = A.ask_a(D, target, "careful")
    gap = min(abs(cv[c][q] - aa[c][q]) for c in aa for q in aa[c])
    check("Ask stop: the careful route misses every county-quarter by %.1f million gallons or more (ten or more "
          "rounding steps)" % gap, gap >= 1.0)
    check("Ask rival link: leaving the second well's own line out gives the golden in every county-quarter",
          A.ask_a(D, target, "drop_child") == aa)
    check("Ask rival link: the other well taken off only in the months its host's line is beyond the host's pump gives "
          "the golden in every county-quarter (the second well runs only in the months it leads, and in every one of "
          "them the line is beyond the pump)", A.ask_a(D, target, "half") == aa, str(A.ask_a(D, target, "half")))
    lines = A.mor_lines(D, target)
    wl = [l for l in lines if l["type"] == "Well"]
    sh = A.shared_meters(target)
    once = A.each_meter_once(wl, sh)
    pairs, fits = A.nested(once, sh)
    fac = {f["facility_id"]: f for f in D["inv"]}
    truth_nest = {(s["full"], p, c) for s in S for (n, p, c) in W.NESTED if s["name"] == n}
    found = {(next(x["system_name"] for x in D["inv"] if x["facility_id"] == p), int(fac[p]["facility_name"].split()[-1]),
              int(fac[c]["facility_name"].split()[-1])) for p, c in pairs.items()}
    check("Ask device: the pump physics, read from the rows, finds exactly the generator's four wellhouse meters and "
          "the one second well each carries (one listed system in each county)", found == truth_nest and
          all(len(v) == 1 for v in fits.values()) and len(fits) == 4 and
          sorted(D["listed"][fac[p]["pws_id"]]["county"] for p in pairs) == sorted(("Engvall", "Granlund", "Hedstrom",
                                                                                    "Sandholm")), str((found, fits)))
    by = collections.defaultdict(dict)
    for l in once:
        by[l["fid"]][l["month"]] = l
    worst = {p: max(by[p][m]["gal"] / A.most(by[p][m]) if A.most(by[p][m]) else 99 for m in by[p]) for p in pairs}
    perq = all(any(by[p][m]["gal"] > 1.4 * A.most(by[p][m]) for m in by[p] if W.quarter(m) == q)
               for p in pairs for q in A.QUARTERS)
    twice = min(sum(1 for m in by[p] if by[p][m]["gal"] > 2.0 * A.most(by[p][m])) for p in pairs)
    check("Ask forcing: each wellhouse line goes beyond 1.4 times what its own pump can deliver in its days in service in "
          "at least one month of every quarter, beyond twice it in %d months or more, up to %.1f times"
          % (twice, max(worst.values())), perq and twice >= 2)
    net = max((by[p][m]["gal"] - by[c][m]["gal"]) / A.most(by[p][m]) for p, c in pairs.items() for m in by[p]
              if A.most(by[p][m]))
    check("Ask forcing: net of its second well, each wellhouse line is within its pump in every month (at most %.2f "
          "of rated capacity for 24 hours of each day in service)" % net, net <= 0.95)
    rest = max(l["gal"] / A.most(l) for l in once if l["fid"] not in pairs and l["fid"] not in sh and A.most(l))
    check("Ask forcing: every other listed well line is within its pump (at most %.2f), so nothing else in the reports "
          "goes beyond a pump" % rest, rest <= 0.95)
    third = []
    for p, c in pairs.items():
        for o, om in by.items():
            if o in (p, c) or (fac[o]["pws_id"], fac[o]["entry_point"]) != (fac[p]["pws_id"], fac[p]["entry_point"]):
                continue
            third.append(max((by[p][m]["gal"] - om[m]["gal"]) / A.most(by[p][m]) for m in by[p] if A.most(by[p][m])))
    check("Ask over-cleaning half: each wellhouse entry point has another, separately metered well, and taking it off "
          "leaves the wellhouse line beyond its pump (at least %.1f times)" % min(third), len(third) >= 4 and
          min(third) > 1.5)
    met = A.rd(target, K.FILES["meters"])
    nm = [m for m in met if m["facility_ids"] in pairs or m["facility_ids"] in pairs.values()]
    check("Ask silence: the register lists each wellhouse meter and each second well's meter on its one facility at "
          "the wellhouse discharge, as every single-facility well meter", len(nm) == 8 and
          all(m["location"] == "wellhouse discharge" and ";" not in m["facility_ids"] for m in nm) and
          {m["location"] for m in met if ";" not in m["facility_ids"] and m["location"] != "interconnect vault"} ==
          {"wellhouse discharge"})
    rows_mor = A.rd(target, K.FILES["mor"])
    amt = collections.Counter((r["pws_id"], r["report_month"], r["volume_gal"]) for r in rows_mor
                              if r["facility_id"] not in sh)
    seqs = collections.defaultdict(list)
    for r in rows_mor:
        seqs[r["facility_id"]].append(r)
    cont = all(a["meter_end"] == b["meter_start"] for f in list(pairs) + list(pairs.values())
               for a, b in zip(sorted(seqs[f], key=lambda r: r["report_month"]),
                               sorted(seqs[f], key=lambda r: r["report_month"])[1:]))
    check("Ask silence: off the register's shared meters no two lines of one system and month carry the same gallons, "
          "and the wellhouse and second-well meters read on without a restart", max(amt.values()) == 1 and cont)
    shared_listed = sorted({m["pws_id"] for m in met if ";" in m["facility_ids"] and m["pws_id"] in D["listed"]})
    check("Ask hazard: one listed system's two wells share a header meter the register lists on both, its readings on "
          "both lines, and three systems off the list do the same", len(shared_listed) == 1 and
          sum(1 for m in met if ";" in m["facility_ids"] and m["pws_id"] not in D["listed"]) == 3)
    check("Ask hazards: the interconnection's September purchase, the June meter change and the emergency well's three "
          "July days are on the listed systems' lines", any(fac[r["facility_id"]]["facility_type"] == "Interconnection"
                                                             and int(r["volume_gal"]) > 0 for r in rows_mor
                                                             if r["facility_id"] in fac and r["pws_id"] in D["listed"])
          and any(m["removed"] for m in met if m["pws_id"] in D["listed"]) and
          any(fac[r["facility_id"]]["status"] == "Emergency" and int(r["volume_gal"]) > 0 for r in rows_mor
              if r["facility_id"] in fac))

    import ceiling as CL
    kc, km, n, pair, ctrl = CL.score(target)
    check("ceiling.py on the cut pack: the careful-solver cracker keeps %d of %d ask figures, the mirror %d, pair "
          "ceiling %.1f, the full includer reproduces figures.json" % (kc, n, km, pair),
          kc == 0 and km == 0 and pair <= 40 and ctrl)

    # ------------------------------------------------------------------------------------------ separation, distractors
    check("separation: the call computed from the call's files alone (results, records, inventory, plan) equals the "
          "golden", call_alone(target, G))
    import hashlib
    check("separation: every file the call reads is byte-identical to the shipped cut (target.zip c38b7092)",
          {k: hashlib.md5(open(os.path.join(target, K.FILES[k]), "rb").read()).hexdigest() for k in K.CALL_FILES}
          == SHIPPED_CALL_MD5)
    for k in K.DISTRACTORS:
        check("distractor: %s deleted leaves the call and the ask unchanged" % K.FILES[k], without(target, K.FILES[k], G,
                                                                                                     aa))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("distractors named in metadata.json by bundle path", sorted(meta["distractor_files"]) ==
          sorted("target/" + K.FILES[k] for k in K.DISTRACTORS))
    check("no shipped file name says distractor, decoy or answer", not any(re.search(r"distract|decoy|answer|truth", f, re.I)
                                                                         for f in os.listdir(target)))

    # ------------------------------------------------------------------------------------------ nothing describes the data
    # dataset-generation section 3: no file or sheet whose job is to say what the data is, what a column means or how
    # the files fit together. By name, with the leak sweep's own patterns and a notes or request token, positive-
    # controlled on the names this build used to ship (the department's notes file, the inventory's Notes sheet).
    check("describing-file control: the name patterns refuse the names this build used to ship",
          bool(DESCRIBE.search("data_request_notes_2026-09-02") and DESCRIBE.search("data_dictionary") and
               DESCRIBE_SHEET.match("Notes") and not DESCRIBE.search("pfas_initial_monitoring_sampling_guide_rev2")))
    shipped = sorted(os.listdir(target))
    check("no shipped file describes the data, by name (no notes, readme, dictionary, manifest or definitions file, and "
          "no text file at all)", not [f for f in shipped if DESCRIBE.search(f.rsplit(".", 1)[0])] and
          not [f for f in shipped if f.rsplit(".", 1)[1] in ("txt", "md", "rtf", "html")], str(shipped))
    sheets = {f: load_workbook(os.path.join(target, f), read_only=True).sheetnames for f in shipped if f.endswith(".xlsx")}
    check("no shipped sheet describes the data, by name (the inventory is its Facilities sheet alone)",
          sheets == {K.FILES["inventory"]: ["Facilities"]} and
          not [s for v in sheets.values() for s in v if DESCRIBE_SHEET.match(s.strip())], str(sheets))
    idents = data_identifiers(target)
    control = " ".join(next(csv.reader(open(os.path.join(target, K.FILES["records"]), encoding="utf-8"))))
    check("describing-content control: the column finder names the records' own header (%d identifiers)" %
          len(named_identifiers(control, idents)), len(named_identifiers(control, idents)) >= 8)
    docs = [f for f in shipped if f.endswith(".pdf")]
    known = {K.FILES["iup"]: "A well's own water is the water the well itself pumps.",
             K.FILES["guide"]: "Blanks and duplicates check the sampling and the laboratory"}
    check("describing-content control: every shipped document is read (text extracted, a known sentence found)",
          sorted(docs) == sorted(known) and all(len(texts[f]) > 1000 and known[f] in texts[f] for f in docs))
    check("no shipped document describes the data, by content (each names fewer than 4 of the data files' column "
          "identifiers and fewer than 8 of their columns)",
          all(len(named_identifiers(texts[f], idents)) < 4 and len(named_columns(texts[f], target)) < 8 for f in docs),
          str({f: sorted(named_columns(texts[f], target)) for f in docs}))

    # ------------------------------------------------------------------------------------------ provenance
    meta_files = {m["path"][len("target/"):]: m for m in meta["files"]}
    check("provenance: metadata.json records every shipped file and nothing else", sorted(meta_files) == shipped and
          set(K.PROVENANCE) == set(K.FILES), str(sorted(set(meta_files) ^ set(shipped))))
    check("provenance: metadata.json's row counts are the shipped files' own",
          all(meta_files[f]["rows"] == rows_of(target, f) for f in shipped))
    late = {f: d for f, d in ((f, latest_date(target, f)) for f in shipped)
            if d and d > dt.date.fromisoformat(meta_files[f]["extracted_or_issued"])}
    check("provenance: no file carries a date after the date it was extracted or issued", not late, str(late))
    check("provenance: the pack's as-of date is its latest document's (the draft plan, 30 September 2026)",
          meta["as_of"] == K.AS_OF.isoformat() == max(m["extracted_or_issued"] for m in meta["files"]))
    sv = A.rd(target, K.FILES["survey"])
    check("units (closure 18): the state's export reports ng/L on its own units column, the federal survey micrograms "
          "per litre on its own",
          {r["units"] for r in A.rd(target, K.FILES["results"])} == {"ng/L"} and {r["Units"] for r in sv} == {"µg/L"})

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


# the leak sweep's own describing-name patterns (leak-check/leak.py DESCRIBE_NAME, DESCRIBE_SHEET), with a notes and a
# data-request token added for the names this build used to ship
DESCRIBE = re.compile(r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|"
                      r"fields?_(guide|notes|list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|"
                      r"file_layout|glossary|column_(notes|descriptions?)|data_?notes|how_to_read|about_this|export_notes|"
                      r"extract_notes|feed_notes|desk_notes|data_team_notes|definitions|schema|layouts?_notes|"
                      r"handling_notes|release_notes|notes|data_request\w*)(?![a-z])", re.I)
DESCRIBE_SHEET = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|field notes|"
                            r"about|about this (file|workbook)|how to (read|use)( this)?|columns?)$", re.I)
COLUMN = re.compile(r"^[A-Za-z][A-Za-z0-9_ ]*$")


def pypdf_text(target, name):
    """A PDF's text the way verify.py reads it (pypdf, page by page), whitespace closed up."""
    return re.sub(r"\s+", " ", "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, name)).pages))


def flow_gap(target):
    """The largest and the median gap, as a share, between a listed record's entry-point flow and the rated capacities
    of the wells its sampler recorded, read the way verify.py reads them (its plan, its inventory, its parse of the
    sources in service, the records through pandas); and how many records they cover."""
    ids = {p["pws"] for p in V.plan(target)}
    inv = V.inventory(target)
    act = inv[(inv.status == "Active") & (inv.facility_type == "Well") & inv.pws_id.isin(ids)]
    cap = {}
    for _, f in act.iterrows():
        cap.setdefault((f.pws_id, f.entry_point), {})[int(f.facility_name.split()[-1])] = int(f.rated_capacity_gpm)
    rec = pd.read_csv(os.path.join(target, K.FILES["records"]), dtype={"pws_id": str})
    gaps = []
    for _, r in rec[rec.pws_id.isin(ids)].iterrows():
        w = cap[(r.pws_id, r.sample_point)]
        on = V.wells_in(r.sources_in_service, sorted(w))
        if on is None:
            continue
        tot = sum(w[k] for k in on)
        gaps.append(abs(float(r.ep_flow_gpm) - tot) / tot)
    return max(gaps), float(np.median(gaps)), len(gaps)


def data_columns(target):
    """Every data file's column names: each CSV's header and the workbook's first row."""
    cols = set()
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            cols |= set(next(csv.reader(open(p, encoding="utf-8"))))
        elif f.endswith(".xlsx"):
            cols |= {str(c) for c in next(load_workbook(p, read_only=True).worksheets[0].iter_rows(values_only=True))}
    return {c.strip() for c in cols if len(c.strip()) >= 4 and COLUMN.match(c.strip())}


def data_identifiers(target):
    """The column names written as identifiers (snake_case, a digit, interior capitals): what a dictionary lists."""
    return {c for c in data_columns(target) if "_" in c or re.search(r"\d", c) or re.search(r"[a-z][A-Z]", c)}


def named(text, cols):
    return {c for c in cols if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), text)}


def named_identifiers(text, idents):
    return named(text, idents)


def named_columns(text, target):
    return named(text, data_columns(target))


def rows_of(target, f):
    p = os.path.join(target, f)
    if f.endswith(".csv"):
        return len(list(csv.DictReader(open(p, newline="", encoding="utf-8"))))
    if f.endswith(".xlsx"):
        return sum(1 for _ in load_workbook(p, read_only=True).worksheets[0].iter_rows()) - 1
    return None


def latest_date(target, f):
    """The latest calendar date a data file carries: ISO dates, month-first dates and report months (a month counts
    at its last day). Documents state dates in words and are not read here."""
    p = os.path.join(target, f)
    if f.endswith(".csv"):
        text = open(p, encoding="utf-8").read()
    elif f.endswith(".xlsx"):
        text = " ".join(str(v) for r in load_workbook(p, read_only=True).worksheets[0].iter_rows(values_only=True)
                        for v in r if v is not None)
    else:
        return None
    out = []
    for y, m, d in re.findall(r"\b(20\d\d|19\d\d)-(\d\d)-(\d\d)\b", text):
        out.append(dt.date(int(y), int(m), int(d)))
    for m, d, y in re.findall(r"\b(\d\d)/(\d\d)/(20\d\d|19\d\d)\b", text):
        out.append(dt.date(int(y), int(m), int(d)))
    if f == K.FILES["mor"]:
        for y, m in re.findall(r",(20\d\d)-(\d\d),", text):
            out.append(dt.date(int(y) + int(m) // 12, int(m) % 12 + 1, 1) - dt.timedelta(days=1))
    return max(out) if out else None


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


def without(target, name, G, aa):
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f != name:
                shutil.copy(os.path.join(target, f), tmp)
        D2 = A.load(tmp)
        G2 = A.golden(D2)
        return walk_key(G2) == walk_key(G) and A.ask_a(D2, tmp) == aa
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
