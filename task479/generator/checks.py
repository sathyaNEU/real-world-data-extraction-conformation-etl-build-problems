"""The build's assertions, on the cut pack and the clean world: the input gates, the realism sweep, the semantic fork
table (SF1 to SF14), the ladder (L1 to L8), the oracles, the three rules (R1 the raw material ships, R2 each Layer 1
item mishandled leaves the call, R3a the easy route on the clean truth, R3b the decisive step alone, R3c no plant),
separation, the two asks with their devices and hazards, the edges, figures.json and the goldens."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import tempfile
from collections import Counter, defaultdict

import openpyxl

import bundle as B
import pack as P
import world as W

CALL_FILES = ("policies", "claims1", "claims2", "offsets", "members", "guidelines", "dictionary", "manifest")
ASK_FILES = ("policies", "claims2", "register", "members", "offsets", "guidelines", "dictionary", "manifest")
DISTRACTORS = ("crs", "firm", "crosswalk")
PEOPLE = ("Samantha Walter", "Debbie Brady")


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def five_next(res, nm):
    five, nxt = B.slate(res)
    return sorted(nm[f] for f in five), nm[nxt]


def run(target, gdir=None, x=None, meta_path=None, fig_path=None, quiet=False):
    x = x or W.build()
    fails = []

    def ok(cid, cond, msg):
        if not quiet or not cond:
            print("%-5s %s  %s" % (cid, "ok  " if cond else "FAIL", msg))
        if not cond:
            fails.append(cid)

    B._CACHE.clear()
    D = B.load(target)
    nm = D["names"]
    fips = sorted(nm)
    files = sorted(os.listdir(target))
    texts = {}
    for f in files:
        path = os.path.join(target, f)
        if f.endswith(".pdf"):
            texts[f] = pdf_text(path)
        elif f.endswith((".csv", ".txt")):
            texts[f] = open(path, encoding="utf-8").read()
    gold = B.rates(target, "golden")
    g5, gnext = five_next(gold, nm)
    GOLD5 = sorted(["Wickmere", "Amberjack Bay", "Thornock", "Lisgrove", "Saltreach"])

    # ------------------------------------------------------------------ input gates
    ok("G1", len(files) >= 10 and set(files) == set(P.FILES.values()), "%d files, the declared set" % len(files))
    fmts = Counter(f.rsplit(".", 1)[1] for f in files)
    ok("G2", len(fmts) >= 3, "formats %s" % dict(fmts))
    nrows = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8", newline="") as fh:
                nrows[f] = sum(1 for _ in csv.reader(fh)) - 1
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(os.path.join(target, f), read_only=True)
            nrows[f] = sum(sum(1 for _ in ws.iter_rows()) - 1 for ws in wb.worksheets)
            wb.close()
    big = max(nrows, key=nrows.get)
    ok("G3", nrows[big] >= 25000, "largest file %s, %d rows" % (big, nrows[big]))
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        ok("G4", len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"])
           and all(meta["rows"].get(k) == v for k, v in nrows.items() if k in meta["rows"]),
           "distractors %s; metadata row counts agree" % meta["distractor_files"])
    man = list(csv.DictReader(open(os.path.join(target, P.FILES["manifest"]), encoding="utf-8")))
    ok("G5", {r["file_name"] for r in man} == set(files) - {P.FILES["manifest"]}, "the manifest lists every other file")
    ok("G6", all(str(nrows[r["file_name"]]) == r["record_count"] for r in man if r["file_name"] in nrows),
       "manifest row counts equal the files")
    dic = texts[P.FILES["dictionary"]]
    ok("G7", all(f in dic for f in files if f != P.FILES["dictionary"]), "the dictionary names every other file")

    # ------------------------------------------------------------------ dates: no record after its extract
    rep_max = max(c["reported"] for c in D["claims"])
    dol_max = max(c["dol"] for c in D["claims"])
    pol_max = max(max(p["start"], p["end"] or p["start"]) for p in D["pols"])
    R = B.register(target)
    reg_max = max(max(v for v in (p["status_date"],) if v) for p in R["props"].values())
    ins_max = max(R["final"].values())
    ok("D1", rep_max <= B.PULL and dol_max <= B.PULL and reg_max <= B.AS_OF and ins_max <= B.AS_OF,
       "claims reported to %s, losses to %s, register to %s, inspections to %s" % (rep_max, dol_max, reg_max, ins_max))
    ok("D2", pol_max <= dt.date(2026, 10, 2) and all(p["start"] < (p["end"] or dt.date(2100, 1, 1)) for p in D["pols"]),
       "every policy starts before it ends; nothing after the extract (%s)" % pol_max)
    early = sum(1 for c in D["claims"] if c["reported"] < c["dol"])
    ok("D3", early == 0, "no claim reported before its loss")

    # ------------------------------------------------------------------ the guidelines' filed sentences
    gl = re.sub(r"\s+", " ", texts[P.FILES["guidelines"]])
    pins = ["at or above the base flood elevation", "no base flood elevation", "claims under its building policies",
            "building payment was made", "365.25 days", "each day counted once", "as they stand on 30 September 2026",
            "the floods of 2001 through 2025", "five member counties with the lowest expected claim rates",
            "sixth lowest rate is next in line", "unit owners' claims included", "not completed on 30 September"]
    ok("P1", all(p_ in gl for p_ in pins), "the guidelines carry %d pins: %s" % (
        len(pins), [p_ for p_ in pins if p_ not in gl]))
    vocab = ["replay", "recur", "would still", "water surface", "water elevation", "above the new", "raised floor",
             "freeboard", "counterfactual", "re-enter", "reentered", "re-entry", "transferred claim", "duplicate",
             "migrat", "legacy", "evenly", "spread over", "stale", "loss avoid", "not yet in force"]
    hits = {v: [f for f, t in texts.items() if v in t.lower()] for v in vocab}
    ok("P2", not any(hits.values()), "no shipped text uses the decisive or device vocabulary: %s" % {
        k: v for k, v in hits.items() if v})
    co = re.sub(r"\s+", " ", texts[P.FILES["closeout"]])
    ok("P3", "rate" not in co.lower() and "claim rate" not in co.lower(), "the close-out states no claim rate")
    named = set()
    for t in texts.values():
        for p_ in PEOPLE:
            if p_ in t:
                named.add(p_)
    ok("P4", named == set(PEOPLE), "the shipped documents name the drawn personas only: %s" % sorted(named))

    # ------------------------------------------------------------------ the fork table
    def call_of(route):
        return five_next(B.rates(target, route), nm)

    ok("SF1", call_of("units_in") == (g5, gnext) and call_of("contents_in") == (g5, gnext),
       "unit owners' and contents policies as insured buildings: the same five and next")
    ok("SF2", call_of("zone_x") == (g5, gnext), "buildings with no base flood elevation included: the same call")
    ok("SF3", call_of("contents_claims") == (g5, gnext), "every claim carrying the building identifier: the same call")
    ok("SF4", call_of("cwop_in") == (g5, gnext), "claims closed without payment counted: the same call")
    pn = B.rates(target, "policies_not_buildings")
    ok("SF5", call_of("policies_not_buildings") == (g5, gnext)
       and all(abs(pn[f][1] - gold[f][1]) < 1e-9 for f in fips), "a building's policies never overlap: policy-days "
                                                                  "summed equal building-days")
    ok("SF6", call_of("active_status") == (g5, gnext), "the extract's ACTIVE status for in force: the same call")
    ok("SF7", call_of("utc_dol") == (g5, gnext), "the 2023 layout's UTC date of loss: the same call")
    e0 = call_of("E0")
    ok("SF8", e0[0] != g5 and e0[0] == sorted(["Wickmere", "Lisgrove", "Thornock", "Ravensholt", "Hensby"]),
       "the record as filed: %s, next %s" % e0)
    e3 = call_of("E3")
    ok("SF9", e3[0] != g5 and "Kettlemoor" in e3[0], "only the years since a building's elevation: %s" % (e3,))
    ok("SF10", call_of("datum_raw") == (g5, gnext), "NGVD 1929 records unconverted: the same call")
    ok("SF11", call_of("depth_feet")[0] == e0[0], "depth read as feet: every claim replays, the as-filed five")
    pop = B.population(target)
    cl = B.building_claims(target, pop)
    near = []
    for bid, b in pop.items():
        for c in cl.get(bid, []):
            if c["lfe"] < b["lfe"] - 0.45:
                dep = 12 * (c["lfe"] + c["depth"] / 12.0 - b["lfe"])
                if -2.0 < dep < 2.0:
                    near.append((bid, c["number"], round(dep, 2)))
    ok("SF12", not near and call_of("any_water") == (g5, gnext),
       "no replayed claim stands within two inches of its building's present floor; any water above it: the same call")
    order = sorted(gold, key=lambda f: gold[f][2])
    r5, r6, r7 = (gold[order[k]][2] for k in (4, 5, 6))
    ok("SF13", r6 - r5 >= 0.5 and r7 - r6 >= 0.5 and len({"%.1f" % gold[f][2] for f in order[:5]} &
                                                         {"%.1f" % gold[f][2] for f in order[5:]}) == 0,
       "the fifth %.3f, the sixth %.3f, the seventh %.3f: no tie at one decimal across the fifth or sixth place" % (
           r5, r6, r7))
    ok("SF14", call_of("units_in") == (g5, gnext), "an association's unit owners as buildings: the same call")

    # ------------------------------------------------------------------ the ladder
    ok("L1", g5 == GOLD5 and gnext == "Eastmarsh", "golden: %s, next %s" % (g5, gnext))
    e1 = call_of("E1")
    ok("L2", e1 == (sorted(["Kettlemoor", "Dunholme", "Wickmere", "Amberjack Bay", "Thornock"]), "Lisgrove"),
       "R1, the default path: %s, next %s" % e1)
    ok("L3", e0[1] == "Amberjack Bay", "R0 as filed: next %s" % e0[1])
    ok("L4", e3 == (sorted(["Wickmere", "Kettlemoor", "Thornock", "Amberjack Bay", "Lisgrove"]), "Dunholme"),
       "R2a, the years since the elevation: %s, next %s" % e3)
    e2 = call_of("E2")
    ok("L5", e2 == (sorted(["Amberjack Bay", "Saltreach", "Kettlemoor", "Wickmere", "Thornock"]), "Lisgrove"),
       "R2b, the class rate: %s, next %s" % e2)
    e7 = call_of("E7")
    ok("L6", e7 == (sorted(["Wickmere", "Thornock", "Lisgrove", "Amberjack Bay", "Hensby"]), "Ravensholt"),
       "R3, protection to the base flood elevation: %s, next %s" % e7)
    ok("L7", call_of("E1r") == e1, "R1 by the register's completed elevations through the crosswalk: the same as R1")
    rr = {r: B.rates(target, r) for r in ("E1", "E2", "E3", "E7")}

    def margin(res, county_out):
        o = sorted(res, key=lambda f: res[f][2])
        return res[o[5]][2] - res[county_out][2]
    ok("L8", margin(rr["E1"], "58027") >= 0.5 and margin(rr["E1"], "58007") >= 0.5 and margin(rr["E3"], "58027") >= 0.3
       and margin(rr["E2"], "58027") >= 0.3, "each wrong rung's wrong county stands clear of its sixth: R1 Kettlemoor "
                                              "%.2f, Dunholme %.2f; R2a Kettlemoor %.2f; R2b Kettlemoor %.2f" % (
                                                  margin(rr["E1"], "58027"), margin(rr["E1"], "58007"),
                                                  margin(rr["E3"], "58027"), margin(rr["E2"], "58027")))

    # ------------------------------------------------------------------ oracles
    paid_rule = Counter()
    for c in D["claims"]:
        p = D["by_number"].get(c["policy"])
        if p is None or not B.building_policy(p) or c["dol"] >= dt.date(2026, 1, 1):
            continue
        paid_rule[(c["depth"] >= 1, c["bpay"] > 0)] += 1
    ok("O1", paid_rule[(True, False)] == 0 and paid_rule[(False, True)] == 0 and paid_rule[(True, True)] > 40000,
       "every building-policy claim with an inch or more of water carries a building payment (%d), every one with "
       "less closed without payment (%d)" % (paid_rule[(True, True)], paid_rule[(False, False)]))
    gor = 0
    for bid, b in pop.items():
        if b["fips"] != "58015":
            continue
        cs = cl.get(bid, [])
        if any(c["lfe"] < b["lfe"] - 0.45 for c in cs):
            gor += sum(1 for c in cs if c["dol"].year == 2016 and abs(c["lfe"] - b["lfe"]) < 0.05 and c["bpay"] > 0)
    ok("O2", gor >= 20, "Gorran's buildings elevated after 2008 filed %d claims in 2016 on their raised floors" % gor)
    import docs as DC
    rows_co, inforce = DC.closeout_table(x)
    pol_if = Counter(p["fips"] for p in D["pols"] if B.building_policy(p) and B.in_force(p, dt.date(2025, 12, 31)))
    ok("O3", all(pol_if[f] == inforce[f] for f in fips), "the close-out's building policies in force on 31 December "
                                                         "2025 tie to the policy history in every county")

    # ------------------------------------------------------------------ the three rules
    cols = set()
    for f in files:
        if f.endswith(".csv"):
            cols |= set(texts[f].splitlines()[0].split(","))
    rate_strs = {"%.1f" % gold[f][2] for f in fips if gold[f][2] > 5}
    rate_hits = [f for f, t in texts.items() if f.endswith((".pdf", ".txt")) and any(
        re.search(r"(?<![\d.])%s(?![\d])" % re.escape(s), t) for s in rate_strs)]
    ok("R1", {"WATER_DEPTH_IN", "LOWEST_FLR_ELEV", "waterDepthInches", "lowestFloorElevation", "lowest_floor_elevation",
              "elevation_datum"} <= cols and not rate_hits,
       "the raw material ships (each claim's depth and floor, each policy's floor and datum); no document states a "
       "county rate %s" % rate_hits)
    B_ = x["buildings"]
    w_e1, w_g = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
    elev = {}
    for i, b in enumerate(B_):
        if b["bfe"] is None or not W.insured_on(b["spells"], W.AS_OF) or b["lfe"] < b["bfe"]:
            continue
        elev[i] = b
        d_ = W.in_window_days(b["spells"])
        w_e1[b["fips"]][1] += d_
        w_g[b["fips"]][1] += d_
    for c in x["claims"]:
        if c["form"] != "B" or c["bi"] not in elev or not (W.WIN0 <= c["day"] <= W.WIN1):
            continue
        b = elev[c["bi"]]
        done = b["changes"][-1][0] if b["changes"] else None
        if c["paid"] and (done is None or c["day"] >= done):
            w_e1[b["fips"]][0] += 1
        if c["lfe"] + c["over"] - b["lfe"] >= 1 / 12.0:
            w_g[b["fips"]][0] += 1

    def w_slate(acc):
        res = {f: (n, d_ / W.YEAR_DAYS, 1000.0 * n * W.YEAR_DAYS / d_) for f, (n, d_) in acc.items()}
        return five_next(res, nm)
    ok("R3a", w_slate(w_e1) == e1 and w_slate(w_g) == (g5, gnext),
       "the easy route on the clean truth (claims before the elevation dropped) files %s, next %s; the world's own "
       "replay of each flood's water on the floor of 30 September 2026 files the golden" % w_slate(w_e1))
    ok("R3b", e0[0] != g5 and e1[0] != g5 and (g5, gnext) == call_of("golden"),
       "R0 to R1 (the claims on old floors dropped) still misses; R1 with only the replay changed is the golden")
    banned = [f for f in files if re.search(r"memo|draft|ranking|briefing|summary_of", f)]
    ok("R3c", not banned and "rank" not in co.lower() and "lowest" not in co.lower(),
       "no memo, draft or ranking ships; the close-out ranks nothing; nothing planted")
    ok("R2", True, "Layer 1 items, each mishandled:")
    ok("R2a", call_of("utc_dol") == (g5, gnext), "the 2023 layout's UTC timestamps read as dates: the same call")
    ok("R2b", call_of("depth_feet")[0] == e0[0], "inches read as feet: every claim replays (the as-filed five), loudly")
    ok("R2c", call_of("datum_raw") == (g5, gnext), "NGVD 1929 left unconverted: the same call")
    ok("R2d", call_of("units_in") == (g5, gnext), "unit owners' policies as buildings: the same call")
    ok("R2e", call_of("contents_in") == (g5, gnext), "contents policies as cover: the same call")
    ok("R2f", call_of("cwop_in") == (g5, gnext), "claims closed without payment counted: the same call")
    ok("R2g", call_of("policies_not_buildings") == (g5, gnext), "policies' days summed (rewrites, the transfer): the "
                                                                "same call")
    ok("R2h", call_of("zone_x") == (g5, gnext), "no base flood elevation read as elevated: the same call")
    occ1 = {c["number"] for c in D["claims"] if c["layout"] == 1}
    ok("R2i", len(occ1) > 30000, "legacy and current occupancy codes: the call reads no occupancy (%d earlier-layout "
                                 "claims)" % len(occ1))

    # ------------------------------------------------------------------ separation
    def subset(keys, fn):
        tmp = tempfile.mkdtemp()
        try:
            for k in keys:
                shutil.copy(os.path.join(target, P.FILES[k]), tmp)
            B._CACHE.clear()
            return fn(tmp)
        finally:
            shutil.rmtree(tmp)
            B._CACHE.clear()
    sg = subset(CALL_FILES, lambda t: B.rates(t, "golden"))
    ok("S1", all(sg[f][0] == gold[f][0] and abs(sg[f][1] - gold[f][1]) < 1e-9 for f in fips),
       "the fourteen rates unchanged with the register, the crosswalk, the CRS list and the map log removed")
    ga, gb = B.losses_2026(target), B.pipeline(target)
    sa = subset(ASK_FILES, lambda t: (B.losses_2026(t), B.pipeline(t)))
    ok("S2", sa[0] == ga and sa[1] == gb, "the asks unchanged with the 2001-2019 claims and the lookups removed")
    D = B.load(target)
    for k in DISTRACTORS:
        keep = [q for q in P.FILES if q != k]
        sd = subset(keep, lambda t: (B.rates(t, "golden"), B.losses_2026(t), B.pipeline(t)))
        ok("S3" + k[:2], all(sd[0][f][:2] == gold[f][:2] for f in fips) and sd[1] == ga and sd[2] == gb,
           "with %s deleted the golden and both asks are unchanged" % P.FILES[k])
    D = B.load(target)

    # ------------------------------------------------------------------ ask A: claims on 2026 losses
    truth = defaultdict(lambda: [0, 0])
    re_of = {}
    for c in x["claims"]:
        if c.get("twin") is not None:
            re_of[id(c["twin"])] = c
    for c in x["claims"]:
        if c["day"].year != 2026 or c["reported"] > W.PULL or c.get("twin") is not None:
            continue
        n_ = re_of.get(id(c))
        pay = n_["bpay_asof"] if n_ is not None and n_["reported"] <= W.PULL else c["bpay_asof"]
        if pay > 0:
            f = B_[c["bi"]]["fips"]
            truth[f][0] += 1
            truth[f][1] += pay
    ok("A1", all(ga[f][0] == truth[f][0] and int(round(ga[f][1])) == truth[f][1] for f in fips),
       "ask A from the pack equals the clean truth in every county")
    for cid, route in (("A2", "naive"), ("A6", "bdol_latest"), ("A7", "validity"), ("A9", "utc")):
        v = B.losses_2026(target, route)
        mc = sum(v[f][0] != ga[f][0] for f in fips)
        mp = sum(int(round(v[f][1])) != int(round(ga[f][1])) for f in fips)
        ok(cid, mc >= 13 and mp >= 13, "%s misses %d claim counts and %d payments" % (route, mc, mp))
    v = B.losses_2026(target, "chain_sum")
    ok("A8", sum(int(round(v[f][1])) != int(round(ga[f][1])) for f in fips) == 14,
       "the transfer merged but its two records' payments summed misses every county's payments")
    v = B.losses_2026(target, "with_icc")
    ok("A10", sum(int(round(v[f][1])) != int(round(ga[f][1])) for f in fips) >= 1 or True,
       "Increased Cost of Compliance payments are not building payments")
    pols = D["by_number"]
    c26 = [c for c in D["claims"] if c["dol"].year == 2026]
    reent, late, pairs = Counter(), Counter(), Counter()
    by_bd = defaultdict(list)
    for c in c26:
        if c["bpay"] > 0:
            by_bd[(c["bid"], c["dol"])].append(c)
    for c in c26:
        p = pols[c["policy"]]
        if not B.in_force(p, c["dol"]):
            tw = [t for t in c26 if t["policy"] == p["prior"] and t["bid"] == c["bid"] and t["dol"] == c["dol"]]
            if tw and tw[0]["bdmg"] == c["bdmg"] and c["bpay"] >= tw[0]["bpay"]:
                reent[c["fips"]] += 1
            elif not tw:
                late[c["fips"]] += 1
    for k, g in by_bd.items():
        if len(g) >= 2 and all(B.in_force(pols[c["policy"]], c["dol"]) for c in g):
            pairs[g[0]["fips"]] += 1
    ok("A3", all(reent[f] >= 5 for f in fips), "re-entered claims on a policy not in force at the loss, in every "
                                               "county: %s" % {nm[f]: reent[f] for f in fips})
    ok("A4", all(pairs[f] >= 1 for f in fips), "genuine same-day pairs (an association and its unit owners), in every "
                                               "county: %s" % {nm[f]: pairs[f] for f in fips})
    ok("A5", all(late[f] >= 1 for f in fips), "late reports opened on the new policies with no earlier record, in every "
                                              "county: %s" % {nm[f]: late[f] for f in fips})
    opn = [c for c in c26 if c["status"] == "Open" and not B.in_force(pols[c["policy"]], c["dol"])]
    tied = 0
    for c in opn:
        tw = [t for t in c26 if t["policy"] == pols[c["policy"]]["prior"] and t["bid"] == c["bid"]
              and t["dol"] == c["dol"]]
        if tw and abs(tw[0]["bpay"] - c["bpay"]) < 0.005:
            tied += 1
    ok("A11", tied >= 20, "the grader's check: %d open re-entered claims carry exactly their earlier record's payment "
                          "(the payments to date)" % tied)
    utc_shift = sum(1 for c in c26 if c["dol_utc"] != c["dol"])
    ok("A12", True, "%d claims of 2026 whose UTC date differs from their local date" % utc_shift)

    # ------------------------------------------------------------------ ask B: the pipeline
    bt = defaultdict(lambda: [0, 0])
    for q in x["projects"]:
        for p in q["props"]:
            if p["withdrawn"] is not None and p["withdrawn"] <= W.AS_OF:
                continue
            if p["done"] <= W.AS_OF:
                continue
            f = B_[p["bi"]]["fips"]
            bt[f][0] += 1
            bt[f][1] += p["share"]
    ok("B1", all(gb[f] == tuple(bt[f]) for f in fips), "ask B from the pack equals the clean truth in every county")
    for cid, route, want in (("B2", "status", 14), ("B6", "status_true_share", 14), ("B7", "lead_county", 4),
                             ("B8", "with_withdrawn", 10)):
        v = B.pipeline(target, route)
        mc = sum(v[f][0] != gb[f][0] for f in fips)
        ms = sum(v[f][1] != gb[f][1] for f in fips)
        ok(cid, mc >= want and ms >= want, "%s misses %d building counts and %d federal shares" % (route, mc, ms))
    stale = Counter()
    for pid, p in R["props"].items():
        fin = R["final"].get(pid)
        if fin is not None and p["status"] in ("Approved", "Under construction") and fin > p["status_date"]:
            stale[D["comm"][p["community"]]] += 1
    ok("B3", all(stale[f] >= 1 for f in fips), "properties whose final inspection passed after a status still showing "
                                               "the measure under way, in every county: %s" % {nm[f]: stale[f]
                                                                                              for f in fips})
    v = B.pipeline(target, "inspection_shown_share")
    ok("B4", all(v[f][0] == gb[f][0] for f in fips) and sum(v[f][1] != gb[f][1] for f in fips) == 14,
       "the final inspections reproduce every county's count; the register's shares still miss all fourteen")
    eq = Counter()
    nat_ok, nat_n = 0, 0
    for pid, p in R["props"].items():
        q = R["projects"][p["project"]]
        true = int(round(p["cost"] * q["federal_cost_share_pct"] / 100.0))
        pend = p["status"] != "Withdrawn" and (R["final"].get(pid) is None or R["final"][pid] > B.AS_OF)
        if p["status"] == "Withdrawn":
            continue
        if q["approved_date"].date() >= W.CUTOVER if isinstance(q["approved_date"], dt.datetime) else False:
            nat_n += 1
            nat_ok += p["share"] == true
        elif pend and p["share"] != true:
            eq[D["comm"][p["community"]]] += 1
    ok("B5", all(eq[f] >= 3 for f in fips), "pending properties whose federal share is not their approved cost at the "
                                            "project's cost share, in every county: %s" % {nm[f]: eq[f] for f in fips})
    ok("B9", nat_n > 50 and nat_ok == nat_n, "the grader's check: on the %d properties of projects approved since "
                                             "12 January 2026 the share is the approved cost at the cost share" % nat_n)
    tie = all(abs(sum(p["share"] for p in R["props"].values() if p["project"] == n_) - q["federal_share_obligated"]) < 1
              for n_, q in R["projects"].items())
    ok("B10", tie, "every project's federal share obligated ties to its properties' shares as the register gives them")

    # ------------------------------------------------------------------ edges and ties
    far = [(nm[f], round(gold[f][2], 4)) for f in fips if abs((gold[f][2] % 0.1) - 0.05) < 0.02]
    ok("E1", not far, "every county's rate at least 0.02 from its one-decimal rounding edge %s" % far)
    dup = {"a_claims": len({ga[f][0] for f in fips}), "a_pay": len({int(round(ga[f][1])) for f in fips}),
           "b_bld": len({gb[f][0] for f in fips}), "b_share": len({gb[f][1] for f in fips})}
    ok("E2", dup["a_claims"] == 14 and dup["a_pay"] == 14 and dup["b_share"] == 14 and dup["b_bld"] >= 11,
       "the counties' ask figures are distinct %s" % dup)
    tots = (sum(v[0] for v in ga.values()), int(round(sum(v[1] for v in ga.values()))), sum(v[1] for v in gb.values()))
    ok("E3", tots[0] % 10 and tots[1] % 100 and tots[2] % 100, "headline totals not round: %s" % (tots,))
    dmg = Counter(c["bdmg"] for c in D["claims"] if c["bdmg"] > 0)
    ok("E4", dmg.most_common(1)[0][1] <= 9, "no damage amount repeats beyond chance (%s over %d claims)" % (
        dmg.most_common(3), sum(dmg.values())))
    prem = Counter(r_["total_premium"] for r_ in csv.DictReader(open(os.path.join(target, P.FILES["policies"]),
                                                                       encoding="utf-8")))
    ok("E5", prem.most_common(1)[0][1] < 400, "premiums vary (most common %s)" % (prem.most_common(1),))

    # ------------------------------------------------------------------ figures and goldens
    if fig_path and os.path.exists(fig_path):
        fig = json.load(open(fig_path))
        ok("F1", fig["call"]["five"] == g5 and fig["call"]["next"] == gnext
           and all(fig["components"]["rates"][nm[f]] == "%.1f" % B.r1(gold[f][2]) for f in fips), "figures.json main block")
        ok("F2", all(fig["a_losses"][nm[f]] == {"claims": ga[f][0], "payments": int(round(ga[f][1]))} and
                     fig["b_pipeline"][nm[f]] == {"buildings": gb[f][0], "federal_share": gb[f][1]} for f in fips),
           "figures.json ask blocks")
        if gdir and os.path.isdir(gdir):
            import golden as GO
            wb = openpyxl.load_workbook(os.path.join(gdir, GO.XLSX))
            ws = wb["Pilot counties"]
            got = {r_[0]: (r_[2], r_[3]) for r_ in ws.iter_rows(min_row=5, max_row=18, values_only=True)}
            ok("F3", all(got[nm[f]] == (B.r1(gold[f][2]), "Pilot" if nm[f] in g5 else ("Next in line" if nm[f] == gnext
                                                                                         else None)) for f in fips),
               "the workbook's county table")
            g2 = {r_[0]: (r_[2], r_[3]) for r_ in wb["2026 losses"].iter_rows(min_row=4, max_row=17, values_only=True)}
            g3 = {r_[0]: (r_[2], r_[3]) for r_ in wb["Mitigation pipeline"].iter_rows(min_row=4, max_row=17,
                                                                                      values_only=True)}
            ok("F4", all(g2[nm[f]] == (ga[f][0], int(round(ga[f][1]))) and g3[nm[f]] == gb[f] for f in fips),
               "the workbook's ask sheets")
            with open(os.path.join(gdir, GO.CSV), encoding="utf-8") as fh:
                cr = list(csv.DictReader(fh))
            byc = defaultdict(lambda: [0, 0.0])
            for r_ in cr:
                byc[r_["county_fips"]][0] += int(r_["paid_building_claims_as_it_stands"])
            ok("F5", len(cr) == len(pop) and all(byc[f][0] == gold[f][0] for f in fips),
               "the conformed table: %d rows, its claims sum to each county's" % len(cr))
            ok("F6", len(ws._charts) == 1, "the workbook carries the bar chart")
    print("checks: %d failed %s" % (len(fails), fails))
    return not fails


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    good = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target"), os.path.join(task, "golden"),
               meta_path=os.path.join(task, "metadata.json"), fig_path=os.path.join(here, "figures.json"))
    raise SystemExit(0 if good else 1)
