"""task139's assertions, run on every build: the three rules on the generator's clean truth (R1 to R3c), the ladder and
every rival, every semantic fork row (SF1 to SF27), each graded figure's distance from its rounding edge, the asks'
devices and stops, the separation of the call from the ask files and the distractors, the realism sweep, the input
gates, and the goldens against figures.json. Reads the pack through calc.py and the world for the clean truth."""
from __future__ import annotations

import copy
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np
import openpyxl
import pandas as pd

import calc as C
import common as K
import world as WD

N = {"ok": 0}


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N["ok"] += 1


def _truth(W):
    """Every pilot intake's course under both groups, from its own latent draws (the clean truth, no sample)."""
    claims = WD._arrivals()
    ids = WD._pilot(claims)
    v12 = {s: WD.intakes_window(claims, s, dt.date(2025, 10, 1), K.EXTRACT_END) for s in K.PROG}
    T = {}
    for seg in K.PROG:
        pcs = sorted([claims[i] for i in ids if claims[i].seg == seg], key=lambda c: c.cid)
        L = WD._lat(K.rng("pilot-course", seg, W.stream[seg]), len(pcs))
        A = [copy.copy(c) for c in pcs]
        B = [copy.copy(c) for c in pcs]
        fE = WD._course(seg, A, L, ["E"] * len(A))
        WD._course(seg, B, L, ["U"] * len(B))
        iu = np.array([c.indemnity for c in B])
        ie = np.array([c.indemnity for c in A])
        indu, inde = iu > 0.005, ie > 0.005
        T[seg] = dict(delta=float((iu - ie).mean()), d=float(iu[indu].mean() - ie[inde].mean()),
                      L_all=float(fE.mean()), L_cl=float(fE[inde].mean()))
    return T, v12


def run(target, golden, W=None, meta_path=None):
    N["ok"] = 0
    G = C.golden(target)
    D, M, g, v12 = G["D"], G["M"], G["g"], G["v12"]
    F = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    P = lambda f: os.path.join(target, f)

    # ---- input gates ------------------------------------------------------------------------------------------
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, ("files", len(files)))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, fmts)
    ok(len(D["extract"]) >= 25000, ("spine rows", len(D["extract"])))
    meta = json.load(open(meta_path)) if meta_path else None
    if meta:
        ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "distractors")
        ok(all(x["license"] and x["date"] and x["source"] for x in meta["files"]), "provenance")
    ok(not any(re.search(r"distractor|decoy|answer|trap|stump", f, re.I) for f in files), "no file names the device")
    import csv as _csv
    with open(os.path.join(target, K.MANIFEST), newline="", encoding="utf-8") as fh:
        listed = [r["file"] for r in _csv.DictReader(fh)]
    ok(sorted(listed) == sorted(f for f in files if f != K.MANIFEST), "H9: the manifest lists every shipped file once")
    dwb = openpyxl.load_workbook(os.path.join(target, K.DICTIONARY), read_only=True)
    in_dict = {r[0] for r in dwb.worksheets[0].iter_rows(min_row=5, values_only=True) if r and r[0]}
    ok(in_dict == {K.EXTRACT, K.MERGES, K.REGISTER, K.NURSE_LOG, K.PAYMENTS, K.ACH_RETURNS, K.CROSSWALK},
       ("H9: the dictionary names the files its scope line names", sorted(in_dict)))

    # ---- the pack reads back to the world (R2: every mess item resolves, nothing lost) -------------------------
    if W is not None:
        for seg in K.PROG:
            for k in ("nU", "nE", "indU", "indE"):
                ok(M[seg][k] == W.realised[seg][k], ("R2 counts", seg, k, M[seg][k], W.realised[seg][k]))
            for k in ("sevU", "sevE", "L_all", "L_cl", "delta", "V"):
                ok(abs(M[seg][k] - W.realised[seg][k]) < 1e-6 * max(1, abs(W.realised[seg][k])),
                   ("R2 measure", seg, k, M[seg][k], W.realised[seg][k]))
    reg, rv, log, ex = D["register"], D["review"], D["log"], D["extract"]
    ok(reg["legacy"].is_unique and len(reg) == 5227, "R2: register claims unique")
    ok(rv["legacy"].isin(set(reg["legacy"])).all() and rv["legacy"].is_unique, "R2: every review row is one pilot intake")
    rtxt = _doc_text(target, only=K.REVIEW_PDF)
    n_open = int((rv["status"] == "Open").sum())
    tot = round(float((rv["ttd"] + rv["tpd"] + rv["ppd"]).sum()), 2)
    ok(len(rv) == 1600 and "(%d of the sampled claims)" % n_open in rtxt and "$%s." % format(tot, ",.2f") in rtxt
       and "4,339 claims" in rtxt, ("the review report's counts and total tie to its workbook", n_open, tot))
    ok(int((reg["arm"] == "E").sum()) == 2613 and int((log["reopen"] == "Y").sum()) == len(log) - 2613,
       "the note's 2,613 ERN files, every further log row a reopening")
    ok(log["legacy"].isin(set(reg[reg["arm"] == "E"]["legacy"])).all(), "R2: every log row is an ERN intake")
    raw_refs = set(log["claim_ref"])
    ok(any(r != C.norm_legacy(r) for r in raw_refs), "R2: the nurses' typed variants are present")
    ok(len(set(C.norm_legacy(r) for r in raw_refs)) == (log["reopen"] != "Y").sum(), "R2: one file a typed number")
    dd = log["opened"].str[3:5].astype(int)
    ok((dd > 12).any(), "R2: the log's US dates are identifiable (a day above 12)")
    cross = dict(zip(D["cross"]["legacy_code"], D["cross"]["new_code"]))
    exseg = dict(zip(ex["legacy_claim_no"], ex["segment"]))
    ok(all(exseg[l] == cross[s] for l, s in zip(reg["legacy"], reg["Segment"])), "SF16: crosswalk and extract agree")
    wb = openpyxl.load_workbook(P(K.REVIEW_BOOK), read_only=True, data_only=True)
    for seg in K.PROG:
        rows = [r for r in wb[seg].iter_rows(values_only=True) if r and r[0]]
        tot = [r for r in rows if str(r[0]).startswith("Sheet total")][0]
        s = rv[rv["seg"] == seg]
        ok(abs(tot[3] - s["ttd"].sum()) < 0.01 and abs(tot[5] - s["ppd"].sum()) < 0.01, ("R2: sheet total", seg))
        ok(len(s) == 200 and (s.merge(reg[["legacy", "arm"]], on="legacy")["arm"].value_counts() == 100).all(),
           ("100 a group", seg))

    # ---- R1: the field's raw material ships, no column holds the deciding quantity ------------------------------
    ok(set(["Group"]).issubset(reg.columns) and "claim_type" in ex.columns and {"ttd", "tpd", "ppd"} <= set(rv.columns),
       "R1: assignments, claim types and verified amounts at claim grain")
    cols = " ".join(list(ex.columns) + list(reg.columns) + list(log.columns) + list(D["pay"].columns)).lower()
    ok(not re.search(r"saving|per_intake|rate|frequency|kept|saw\b|pure_premium", cols), "R1: no deciding column")

    # ---- R3: the analyst test on the clean truth ----------------------------------------------------------------
    if W is not None:
        T, v12w = _truth(W)
        easy = C.rung(T, saving="d", L="L_cl", cap_L="L_cl", vol=v12w)
        gold = C.rung(T, vol=v12w)
        ok(easy["teams"]["HC-SS"] == 0 and easy["teams"]["RW-SS"] == 0 and easy["teams"]["RW-OT"] == 3,
           ("R3a: the easy route on the clean truth leaves the strain units empty", easy["teams"]))
        ok(gold["teams"] == g["teams"], ("R3b: the decisive step alone files the golden allocation", gold["teams"]))
        for name, kw in (("R1", dict(saving="d", L="L_all", cap_L="L_all")),
                         ("R2b", dict(saving="delta", L="L_cl", cap_L="L_cl")),
                         ("R3", dict(saving="delta", L="L_all", cap_L=None))):
            r = C.rung(T, vol=v12w, **kw)
            ok(r["teams"] != g["teams"], ("R3b: a lower correction alone stays wrong on the truth", name, r["teams"]))
        ok(abs(gold["credit"] - easy["credit"]) > 1500000, "R3: the two estimators of the truth stand apart")
    docs_txt = _doc_text(target)
    for w in ("per intake", "per assigned", "frequency", "kept at work", "conversion rate", "indemnity rate",
              "intention to treat", "selection", "costlier", "remainder", "randomised pilot"):
        ok(w not in docs_txt.lower(), ("R3c: a document names the decisive step", w))
    for fig in ("4,100,000", "4.1 million", "2,000,000", "2.0 million"):
        ok(fig not in docs_txt, ("R3c: a document states a credit", fig))
    ok("placement" not in docs_txt.lower() or "placement goes to the Committee" in docs_txt, "R3c: no placement stated")

    # ---- the ladder --------------------------------------------------------------------------------------------
    gold_teams = {"HC-SS": 3, "HC-OT": 3, "RW-SS": 2, "RW-OT": 0, "MF-SS": 3, "MF-OT": 3, "CN-SS": 0, "CN-OT": 3}
    ok(g["teams"] == gold_teams and sum(g["teams"].values()) == 17, ("golden allocation", g["teams"]))
    ok(K.round_to(g["credit"], 100000) == 4100000, ("golden credit", g["credit"]))
    lad = {"R0": C.rung(M, saving="d", L="L_cl", cap_L="L_cl", vol=v12),
           "R0s": C.rung(M, saving="d", L="L_sam", cap_L="L_sam", vol=v12),
           "R1b": C.rung(M, saving="d", L="L_all", cap_L="L_all", vol=v12),
           "R2": C.rung(M, vol=v12, rank="saving"),
           "R2b": C.rung(M, saving="delta", L="L_cl", cap_L="L_cl", vol=v12),
           "R3": C.rung(M, vol=v12, cap_L=None)}
    Mx = {s: dict(M[s], pd=M[s]["pE"] * M[s]["d"], pud=M[s]["pU"] * M[s]["d"]) for s in K.PROG}
    lad["R1"] = C.rung(Mx, saving="pd", vol=v12)
    lad["R1u"] = C.rung(Mx, saving="pud", vol=v12)
    ok(lad["R0"]["teams"] == {"HC-SS": 0, "HC-OT": 3, "RW-SS": 0, "RW-OT": 3, "MF-SS": 2, "MF-OT": 3, "CN-SS": 3,
                              "CN-OT": 3}, ("default path", lad["R0"]["teams"]))
    ok(K.round_to(lad["R0"]["credit"], 100000) == 2000000, ("default credit", lad["R0"]["credit"]))
    for k, r in lad.items():
        miss = sum(abs(r["teams"][s] - g["teams"][s]) for s in K.PROG)
        ok(miss >= 2, ("a rival lands the allocation", k, r["teams"]))
        ok(K.round_to(r["credit"], 100000) != 4100000, ("a rival lands the credit bin", k, r["credit"]))
    ok(all(lad["R0"]["value"][s] < 0.25 * g["value"][s] for s in ("HC-SS", "RW-SS", "MF-SS")),
       "the decisive move multiplies the strain units' value")
    order = ["HC-SS", "HC-OT", "RW-SS", "RW-OT", "MF-SS", "MF-OT", "CN-SS", "CN-OT"]
    note = {"R0": ("03032333", 2048524), "R0s": ("03032333", 2048360), "R1": ("03032333", 1985501),
            "R1u": ("03033323", 2081829), "R1b": ("03033323", 2248360), "R2b": ("32303303", 3398667),
            "R2": ("33023303", 3793208), "R3": ("32303303", 4200799)}
    for k, (teams, credit) in note.items():
        ok("".join(str(lad[k]["teams"][s]) for s in order) == teams and round(lad[k]["credit"]) == credit,
           ("the note's ladder row", k, lad[k]["teams"], lad[k]["credit"]))
    ok(round(g["credit"]) == 4105562 and round(4150000 - g["credit"]) == 44438, "the note's golden position")
    ok([round(lad["R0"]["value"][s]) for s in ("HC-SS", "RW-SS", "MF-SS")] == [34106, 28214, 56016] and
       [round(g["value"][s]) for s in ("HC-SS", "RW-SS", "MF-SS", "HC-OT", "RW-OT")] == [292364, 286892, 281996, 191656,
                                                                                          130715], "the note's move")
    ok(round(g["value"]["HC-OT"] / g["value"]["RW-OT"], 2) == 1.47, "the note's cut ratio")
    ok([s for s in order if lad["R0"]["teams"][s] == g["teams"][s]] == ["HC-OT", "MF-OT", "CN-OT"] and
       sum(lad["R3"]["teams"][s] == g["teams"][s] for s in order) == 6 and
       all(K.round_to(lad["R3"]["value"][s], 10000) == K.round_to(g["value"][s], 10000) for s in order),
       "the note's worth on the graded figures")
    ok(min((round(K.edge_distance(g["value"][s], 10000)), s) for s in order) == (1892, "RW-SS"), "the note's nearest edge")
    # the cut and dominance
    funded = [s for s in K.PROG if g["teams"][s] > 0]
    left = [s for s in K.PROG if g["teams"][s] == 0]
    ok(min(g["value"][s] for s in funded) >= 1.3 * max(g["value"][s] for s in left), "SF19: the cut stands apart")
    ok(g["cap"]["RW-SS"] == 2 and all(g["cap"][s] == 3 for s in K.PROG if s != "RW-SS"), ("the fill caps", g["cap"]))
    # every rival's per-team saving set differs from the golden on graded values
    ok(all(K.round_to(lad["R0"]["value"][s], 10000) != K.round_to(g["value"][s], 10000) for s in K.PROG),
       "the default path misses every team saving")

    # ---- semantic forks -----------------------------------------------------------------------------------------
    ok(all(g["value"][s] > 0 for s in K.PROG), "SF2: every segment's saving is positive")
    ok(sum(min(3, g["cap"][s]) for s in K.PROG) >= 17, "SF3: three a unit leaves room for seventeen")
    # SF4: the fill limit on a monthly basis
    months = pd.date_range("2025-10-01", "2026-09-01", freq="MS")
    monthly = {}
    for s in K.PROG:
        rs = []
        for m in months:
            a, b = m.date(), (m + pd.offsets.MonthEnd(0)).date()
            n = C.intakes(D, a, b)[s]
            rs.append(n * 365 / ((b - a).days + 1) * M[s]["L_all"] / K.TEAM_PLACE_DAYS)
        monthly[s] = (round(min(rs), 2), round(max(rs), 2))
    ok(2.0 <= monthly["RW-SS"][0] and monthly["RW-SS"][1] < 3.0, ("SF4: RW-SS keeps two on every month", monthly["RW-SS"]))
    ok(monthly["RW-SS"] == (2.04, 2.76) and monthly["MF-OT"][0] == 2.80 and
       all(monthly[s][0] >= 3.0 for s in K.PROG if s not in ("RW-SS", "MF-OT")), ("SF4: the note's monthly range", monthly))
    # SF5: the cap on every forecast basis
    bases = {"latest": v12,
             "2025": C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31)),
             "2025 as filed": C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), fix_vintage=False, dedup=False),
             "2024": C.intakes(D, dt.date(2024, 1, 1), dt.date(2024, 12, 31)),
             "2024 as filed": C.intakes(D, dt.date(2024, 1, 1), dt.date(2024, 12, 31), fix_vintage=False, dedup=False),
             "2026 annualised": {s: v * 365 / 273 for s, v in C.intakes(D, dt.date(2026, 1, 1), K.EXTRACT_END).items()},
             "latest x1.03": {s: v * 1.03 for s, v in v12.items()}}
    ann = {y: C.intakes(D, dt.date(y, 1, 1), dt.date(y, 12, 31)) for y in range(2021, 2026)}
    trend = {}
    for s in K.PROG:
        b_, a_ = np.polyfit(np.arange(2021, 2026), [ann[y][s] for y in range(2021, 2026)], 1)
        trend[s] = a_ + b_ * 2027
    bases["trend"] = trend
    for name, vol in bases.items():
        r = C.rung(M, vol=vol)
        ok(r["teams"] == g["teams"], ("SF5: the cap on another forecast basis", name, r["teams"]))
    fills = {name: {s: vol[s] * M[s]["L_all"] / K.TEAM_PLACE_DAYS for s in K.PROG} for name, vol in bases.items()}
    rw = [f["RW-SS"] for f in fills.values()]
    ok(len(bases) == 8 and (round(min(rw), 2), round(max(rw), 2)) == (2.33, 2.65) and
       round(min(f[s] for f in fills.values() for s in K.PROG if s != "RW-SS"), 2) == 3.97, "SF5: the note's range")
    # SF6, SF9, SF15: amounts
    rvj = rv.merge(reg[["legacy", "arm"]], on="legacy")

    def with_sev(fn):
        Mz = {s: dict(M[s]) for s in K.PROG}
        for s in K.PROG:
            for arm, key in (("U", "sevU"), ("E", "sevE")):
                Mz[s][key] = fn(rvj[(rvj["seg"] == s) & (rvj["arm"] == arm)])
            Mz[s]["delta"] = Mz[s]["pU"] * Mz[s]["sevU"] - Mz[s]["pE"] * Mz[s]["sevE"]
        return C.rung(Mz, vol=v12)
    r = with_sev(lambda x: float(x["ttd"].mean()))
    ok(K.round_to(r["credit"], 100000) == 2900000 and r["teams"] != g["teams"], ("SF6: TTD alone moves the call", r["credit"]))
    r = with_sev(lambda x: float((x[x["status"] == "Closed"][["ttd", "tpd", "ppd"]].sum(axis=1)).mean()))
    ok(K.round_to(r["credit"], 100000) == 4200000, ("SF15: closed claims alone move the credit", r["credit"]))
    Mt = {s: dict(M[s], delta=M[s]["delta"] * 1.04 ** 2) for s in K.PROG}
    ok(K.round_to(C.rung(Mt, vol=v12)["credit"], 100000) == 4400000, "SF9: a trend moves the credit")
    # SF11, SF12: place-days
    r = C.rung(C.pilot_metrics(D, inclusive=False), vol=v12)
    ok(K.round_to(r["credit"], 100000) == 4300000 and
       sum(K.round_to(r["value"][s], 10000) > K.round_to(g["value"][s], 10000) for s in K.PROG) == 5,
       ("SF11: the day difference moves the credit and five team savings", r["credit"]))
    r = C.rung(C.pilot_metrics(D, reopen=False), vol=v12)
    ok(r["teams"] == g["teams"] and K.round_to(r["credit"], 100000) == 4100000 and
       all(K.round_to(r["value"][s], 10000) == K.round_to(g["value"][s], 10000) for s in K.PROG),
       "SF12: dropping the reopenings converges on every graded figure")
    ok(round(r["credit"]) == 4121010, ("SF12: the note's figure", r["credit"]))
    # SF13: groups as assigned are groups as treated
    e_ids = set(reg[reg["arm"] == "E"]["legacy"])
    ok(set(log["legacy"]) == e_ids, "SF13: every ERN intake has a file and no usual-handling intake has one")
    # SF14: three readings of an indemnity claim
    conv = ex[ex["legacy_claim_no"] != ""]
    t1 = set(conv[conv["claim_type"] == "IND"]["legacy_claim_no"]) & set(reg["legacy"])
    t2 = set(conv[conv["first_indemnity_date"] != ""]["legacy_claim_no"]) & set(reg["legacy"])
    ok(t1 == t2 and len(t1) == 4339, ("SF14", len(t1), len(t2)))
    if W is not None:
        frame = {W.claims[i].legacy_no for i in W.pilot_ids if W.claims[i].ind and W.claims[i].first_ind <= K.VALUATION}
        ok(frame == t1, "SF14: the review's frame at 30 June 2026 is the same set")
    # SF17: office-stratified
    Mo = {o: C.pilot_metrics(D, office=o) for o in ("STL", "KC")}
    Mp = {}
    for s in K.PROG:
        w = {o: int(((reg["seg"] == s) & (reg["Office"] == o)).sum()) for o in ("STL", "KC")}
        Mp[s] = dict(delta=sum(w[o] * Mo[o][s]["delta"] for o in w) / sum(w.values()),
                     L_all=sum(w[o] * Mo[o][s]["L_all"] for o in w) / sum(w.values()))
    r = C.rung(Mp, vol=v12)
    ok(r["teams"] == g["teams"] and K.round_to(r["credit"], 100000) == 4100000 and round(r["credit"]) == 4123300,
       ("SF17: office-stratified converges", r["credit"]))
    # SF18: the rounding path
    ok(sum(g["teams"][s] * K.round_to(g["value"][s], 10000) for s in K.PROG) == 4090000, "SF18")
    # SF20 is R3a/R3b above; SF1, SF7, SF8, SF10: the filed sentences are present where the table says
    for frag in ("Each segment's claims are worked in one unit", "A claim unit houses at most three teams",
                 "over the year must fill every place", "The day a file opens and the day it closes both count",
                 "A file reopened after it closed holds a place again", "An intake is a claim whose first report"):
        ok(frag in docs_txt, ("SF1 SF3 SF4 SF11 SF12 SF21: the charter's sentence", frag))
    for frag in ("will not pay because the teams took", "twenty places for 365", "open and closed claims alike",
                 "with no trend", "what the pilot measured in that segment", "this credit is indemnity only"):
        ok(frag in docs_txt, ("SF6 SF7 SF8 SF9 SF10 SF15: the memo's sentence", frag))
    # SF7: the memo states the credit once, as what it is, and restates no comparison of what the intakes pay
    memo_txt = _doc_text(target, only=K.PICK_MEMO)
    ok("will not pay because the teams took them." in memo_txt and "adjusters alone" not in memo_txt and
       "would pay" not in memo_txt, "SF7: memo paragraph 2 files the credit once, with no restated comparison")
    ok("PR-2026-041" in memo_txt and "pick memo 4" not in memo_txt, "the memo carries its Pricing reference")
    # row order: reversed register and log give the same figures
    D2 = dict(D)
    D2["register"] = D["register"].iloc[::-1].reset_index(drop=True)
    D2["log"] = D["log"].iloc[::-1].reset_index(drop=True)
    M2 = C.pilot_metrics(D2)
    ok(all(abs(M2[s]["delta"] - M[s]["delta"]) < 1e-9 for s in K.PROG), "axis 14: row order")

    # ---- the asks ------------------------------------------------------------------------------------------------
    a1 = G["ask1"]
    s1 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), fix_vintage=False, dedup=False)
    s2 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), fix_vintage=True, dedup=False)
    s3 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), fix_vintage=False, dedup=True)
    for name, st in (("S1", s1), ("S2", s2), ("S3", s3)):
        ok(all(st[s] != a1[s] for s in K.PROG), ("SF21 SF22: Ask 1 stop lands", name))
    ok(min(s2[s] - a1[s] for s in K.PROG) == 2 and max(s2[s] - a1[s] for s in K.PROG) == 9,
       "SF22: the parallel-run copies on every segment, 2 to 9")
    ok(min(s3[s] - a1[s] for s in K.PROG) == 24 and max(s3[s] - a1[s] for s in K.PROG) == 80,
       "SF21: the flag as filed, 24 to 80 high")
    ok([s1[s] for s in K.PROG] == [1621, 856, 991, 734, 1442, 812, 1178, 700] and
       [s2[s] for s in K.PROG] == [1546, 827, 947, 710, 1362, 773, 1118, 669] and
       [s3[s] for s in K.PROG] == [1612, 851, 983, 732, 1436, 809, 1169, 697], "Ask 1: the note's stops")
    x25 = ex[(ex["report_date"] >= "2025-01-01") & (ex["report_date"] <= "2025-12-31")]
    bad = x25[(x25["legacy_claim_no"] != "") & (x25["time_off_at_report"] == "Y") & (x25["disability_began"] > x25["report_date"])]
    newrows = ex[ex["legacy_claim_no"] == ""]
    incons = newrows[(newrows["time_off_at_report"] == "Y") != ((newrows["disability_began"] != "") &
                                                              (newrows["disability_began"] <= newrows["report_date"]))]
    ok(len(bad) > 100 and len(incons) == 0, ("SF21: the converted flag's tell, and new rows consistent", len(bad), len(incons)))
    inj = {}
    for s in K.PROG:
        y = ex[(ex["segment"] == s) & (ex["injury_date"] >= "2025-01-01") & (ex["injury_date"] <= "2025-12-31")]
        inj[s] = len(y)
    ok(any(inj[s] != a1[s] for s in K.PROG), "SF23: injury year would read otherwise")
    i1 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), by="injury_date")
    moved = [abs(i1[s] - a1[s]) for s in K.PROG if i1[s] != a1[s]]
    ok(len(moved) == 5 and min(moved) == 2 and max(moved) == 9, ("SF23: the injury year moves five segments", i1))
    # Ask 1 as filed: the dictionary's definitions executed word for word are the golden, on their own code path
    DD = _dictionary(target)
    tor_def, file_def = DD[(K.EXTRACT, "time_off_at_report")], DD[(K.EXTRACT, "(file)")]
    ok("(disability_began on or before report_date)" in tor_def and "the legacy LOST_TIME indicator" in tor_def and
       "for any claim with time lost on record" in tor_def, ("SF21: the dictionary files the flag on converted claims", tor_def))
    ok("parallel run of 29 May to 1 June 2025 and keyed in both systems is listed twice" in file_def and
       "the same office, segment, class_code, injury_date, report_date and disability_began" in file_def,
       ("SF22: the dictionary files the parallel run's double listing", file_def))
    pkey = ["office", "segment", "class_code", "injury_date", "report_date", "disability_began"]
    natives = ex[ex["legacy_claim_no"] == ""]
    nat_at = {}
    for k_, cno in zip(map(tuple, natives[pkey].values.tolist()), natives["claim_no"]):
        nat_at.setdefault(k_, []).append(cno)
    win = ex[(ex["legacy_claim_no"] != "") & (ex["report_date"] >= "2025-05-29") & (ex["report_date"] <= "2025-06-01")]
    twin = {cno: nat_at[k_] for k_, cno in zip(map(tuple, win[pkey].values.tolist()), win["claim_no"]) if k_ in nat_at}
    ok(len(twin) == 62 and all(len(v) == 1 for v in twin.values()) and len({v[0] for v in twin.values()}) == 62 and
       len(win) - len(twin) == 4 and natives["report_date"].min() == "2025-05-29",
       ("SF22: 62 converted claims each pair one new-number claim, four converted claims are listed once", len(twin)))
    k5 = pkey[:-1]
    nat5 = set(map(tuple, natives[k5].values.tolist()))
    hit5 = [cno for k_, cno in zip(map(tuple, win[k5].values.tolist()), win["claim_no"]) if k_ in nat5]
    ok(len(hit5) == 63 and len(set(hit5) - set(twin)) == 1,
       ("SF22: without disability_began one converted claim listed once pairs a new-number claim", len(hit5)))
    x25p = ex[(ex["report_date"] >= "2025-01-01") & (ex["report_date"] <= "2025-12-31") & ex["segment"].isin(K.PROG)]
    merged = set(D["merges"]["claim_no"])
    lit, lit_dates = {s: 0 for s in K.PROG}, {s: 0 for s in K.PROG}
    for r in x25p.itertuples(index=False):
        if r.claim_no in twin:                       # listed twice: counted once, on its new-number row
            continue
        if r.claim_no in merged:                     # merged into another claim: counted with that claim
            continue
        by_dates = r.disability_began != "" and r.disability_began <= r.report_date
        lit[r.segment] += by_dates if r.legacy_claim_no else (r.time_off_at_report == "Y")
        lit_dates[r.segment] += by_dates
    ok(lit == a1 and lit_dates == a1, ("SF21 SF22 SF28: the dictionary and the merges executed literally are the golden",
                                       lit, a1))
    ok([a1[s] for s in K.PROG] == [1537, 822, 939, 708, 1356, 770, 1109, 666], ("Ask 1 golden", a1))
    # the same intake definition on the main call's window: every row there is a new-system row and the flag is it
    xm = ex[(ex["report_date"] >= "2025-10-01") & (ex["report_date"] <= "2026-09-30") & ex["segment"].isin(K.PROG)]
    vdates = {s: int(((xm["segment"] == s) & (xm["disability_began"] != "") &
                      (xm["disability_began"] <= xm["report_date"])).sum()) for s in K.PROG}
    vflag = {s: int(((xm["segment"] == s) & (xm["time_off_at_report"] == "Y")).sum()) for s in K.PROG}
    ok((xm["legacy_claim_no"] == "").all() and vdates == vflag == v12, ("one intake definition on the call's window", vflag))
    # the rival readings of Ask 1 each miss, each ruled out by a filed sentence
    s4 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), strict=True)
    ok(all(s4[s] != a1[s] for s in K.PROG) and (min(a1[s] - s4[s] for s in K.PROG), max(a1[s] - s4[s] for s in K.PROG))
       == (37, 124),
       ("SF21: time lost beginning before the report date only (strict) misses every segment", s4))
    s5 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), dedup="window")
    off5 = sorted(s for s in K.PROG if s5[s] != a1[s])
    once = win[~win["claim_no"].isin(twin)]
    ok(off5 == ["CN-SS", "HC-SS", "MF-SS"] and sorted(set(once["segment"])) == off5 and
       all(a1[s] - s5[s] == int((once["segment"] == s).sum()) for s in K.PROG) and
       {s: a1[s] - s5[s] for s in off5} == {"CN-SS": 1, "HC-SS": 2, "MF-SS": 1},
       ("SF22: dropping every converted claim of the parallel run drops the four listed once", s5))
    s6 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), dedup="global")
    took25 = x25p[np.where(x25p["legacy_claim_no"] != "", (x25p["disability_began"] != "") &
                           (x25p["disability_began"] <= x25p["report_date"]), x25p["time_off_at_report"] == "Y")]
    took25 = took25[~took25["claim_no"].isin(merged)]
    ok(all(s6[s] < a1[s] for s in K.PROG) and int((took25.groupby(pkey).size() > 1).sum()) == 148 and
       (min(a1[s] - s6[s] for s in K.PROG), max(a1[s] - s6[s] for s in K.PROG)) == (3, 34),
       ("SF22: a dedup on those fields across the year deletes genuine same-day claims in every segment", s6))
    # SF28, Ask 1's silent device: from the upgrade to 15 September 2025 a resent first report set up a second claim,
    # merged into the first when found; the merge sits only in the claims system's merge file
    mg = D["merges"]
    on_ex = set(ex["claim_no"])
    exi = ex.set_index("claim_no")
    ok(mg["claim_no"].is_unique and mg["merged_into"].isin(on_ex).all() and not mg["merged_into"].isin(merged).any(),
       "SF28: one row a merged claim, each merged into a claim on the extract that was never merged itself")
    mx = mg[mg["claim_no"].isin(on_ex)]
    rm, sv = exi.loc[mx["claim_no"]], exi.loc[mx["merged_into"]]
    ok(len(mx) >= 40 and (rm["time_off_at_report"] == "Y").all() and (rm["legacy_claim_no"] == "").all() and
       (rm["claim_type"] == "MO").all() and (rm["status"] == "CLOSED").all() and
       list(rm["closed_date"]) == list(mx["merge_date"]),
       ("SF28: each merged claim on the extract is a new-system claim flagged Y, medical only, closed on its merge date",
        len(mx)))
    lag = (pd.to_datetime(rm["report_date"]).values - pd.to_datetime(sv["report_date"]).values) / np.timedelta64(1, "D")
    ok(all(list(rm[c]) == list(sv[c]) for c in ("office", "segment", "class_code", "injury_date", "disability_began",
                                                 "time_off_at_report")) and lag.min() >= 2 and lag.max() <= 12,
       "SF28: a merged claim repeats its claim's first report, received 2 to 12 days later")
    ok(rm["report_date"].min() >= "2025-06-04" and rm["report_date"].max() < "2025-09-15" and
       sv["report_date"].min() >= "2025-06-02" and mg["merge_date"].str[:4].eq("2025").all() and
       mg["merge_date"].max() <= "2025-12-31",
       "SF28: every merged claim reported after the upgrade and before 15 September 2025, every merge in 2025")
    ok(all(K.is_working(dt.date.fromisoformat(x)) for x in mg["merge_date"]), "SF28: every merge on a working day")
    ok(not ((rm["report_date"] >= "2025-10-01") & (rm["report_date"] <= "2026-09-30")).any() and
       not mx["merged_into"].map(exi["legacy_claim_no"]).ne("").any(),
       "SF28: zero merged claims in the call's window and none among converted claims (the pilot's)")
    nx = mg[~mg["claim_no"].isin(on_ex)]
    ok(len(nx) >= 5 and (exi.loc[nx["merged_into"], "time_off_at_report"] == "N").all(),
       "SF28: the merged claims off the extract repeat first reports that recorded no time lost")
    kseg = {s: int(((rm["segment"] == s) & (rm["report_date"] <= "2025-12-31")).sum()) for s in K.PROG}
    ok(min(kseg.values()) >= 3 and len(set(kseg.values())) >= 4 and
       kseg == {"HC-SS": 17, "HC-OT": 8, "RW-SS": 11, "RW-OT": 4, "MF-SS": 11, "MF-OT": 7, "CN-SS": 9, "CN-OT": 6} and
       (len(mg), len(mx), len(nx)) == (92, 86, 6), ("SF28: merged claims in every segment, the note's counts", kseg))
    g5 = int((took25.groupby([k for k in pkey if k != "report_date"]).size() > 1).sum())
    ok(g5 > 148, ("SF28: more genuine groups on the five first-report fields than on the six", g5))
    s7 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), merges=False)
    s8 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), merges="both")
    s9 = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), dedup="global5", merges=False)
    s1n = C.intakes(D, dt.date(2025, 1, 1), dt.date(2025, 12, 31), fix_vintage=False, dedup=False, merges=False)
    ok(all(s7[s] - a1[s] == kseg[s] for s in K.PROG),
       ("SF28: the dictionary executed with the merges unread, every segment high by its merged claims", s7))
    ok(all(a1[s] - s8[s] == kseg[s] for s in K.PROG), ("SF28: both claims of each merge dropped, every segment low", s8))
    ok(all(s9[s] < a1[s] for s in K.PROG), ("SF28: a dedup on the five first-report fields across the year, every "
                                            "segment low (genuine same-day claims deleted)", s9))
    ok(all(s1n[s] != a1[s] for s in K.PROG), ("Ask 1: the natural read misses every segment", s1n))
    ok([s1n[s] for s in K.PROG] == [1638, 864, 1002, 738, 1453, 819, 1187, 706] and
       [s7[s] for s in K.PROG] == [1554, 830, 950, 712, 1367, 777, 1118, 672] and
       (min(a1[s] - s9[s] for s in K.PROG), max(a1[s] - s9[s] for s in K.PROG)) == (23, 186),
       ("Ask 1: the note's stops S1 to S4", s1n, s7, s9))
    a2 = G["ask2"]
    t1_ = C.paid_2026(D, dedup_lines=False, drop_returns=False)
    t2_ = C.paid_2026(D, dedup_lines=True, drop_returns=False)
    t3_ = C.paid_2026(D, dedup_lines=False, drop_returns=True)
    t4_ = C.paid_2026(D, drop_void=False)
    pay = D["pay"]
    for name, st in (("S1", t1_), ("S2", t2_), ("S3", t3_), ("voids", t4_)):
        ok(all(K.round_to(st[s], 1000) != K.round_to(a2[s], 1000) for s in K.PROG), ("SF24 SF25 SF26: Ask 2 stop lands", name))
    voids = pay[(pay["line"] == "1") & (pay["status"] == "VOID")]
    ok(len(voids) == 85 and (voids["void_date"] != "").all(), "SF26: voided checks carry their status and date")
    ok(len(D["ach"]) == 275, "SF25: the bank's 275 returns")
    r1 = [t1_[s] / a2[s] for s in K.PROG]
    r3 = [t3_[s] / a2[s] for s in K.PROG]
    hi2 = [t2_[s] - a2[s] for s in K.PROG]
    hi4 = [t4_[s] - a2[s] for s in K.PROG]
    ok((round(min(r1), 2), round(max(r1), 2)) == (1.66, 1.86) and (round(min(r3), 2), round(max(r3), 2)) == (1.65, 1.84)
       and (round(min(hi2)), round(max(hi2))) == (10300, 50186) and (round(min(hi4)), round(max(hi4))) == (3814, 15519),
       ("Ask 2: the note's stops", r1, r3, hi2, hi4))
    pay = D["pay"]
    amt_per = pay.groupby("payment_no")["amount"].nunique()
    ok((amt_per == 1).all(), "SF24: a payment's lines all carry the same amount")
    ok(pay["claim_no"].isin(set(ex["claim_no"])).all(), "SF27: every payment's claim is on the extract")
    ok(D["ach"]["trace_number"].isin(set(pay["check_or_trace"])).all(), "SF25: every return matches an EFT")
    # SF24 to SF26 as filed: the amount repeats on a payment's lines; a voided check and a returned EFT did not pay,
    # and each was paid again by a check for the same claim, benefit, payee, period and amount
    ok(DD[(K.PAYMENTS, "amount")] == "Amount of the payment, US dollars, repeated on each line of the payment." and
       "one line for each week of benefits the payment covers" in DD[(K.PAYMENTS, "line")],
       "SF24: the dictionary files the amount as the payment's, repeated on each line")
    ok("VOID when the check was voided before it was cashed" in DD[(K.PAYMENTS, "status")], "SF26: a voided check")
    ok("ACH return items" in DD[(K.ACH_RETURNS, "(file)")], "SF25: the bank's file is described as its return items")
    hdr = pay[pay["line"] == "1"].drop(columns=["period_from", "period_to"]).merge(
        pay.groupby("payment_no").agg(pf=("period_from", "min"), pt=("period_to", "max")).reset_index(), on="payment_no")
    rk = ["claim_no", "benefit", "payee", "pf", "pt", "amount"]
    chk = hdr[(hdr["method"] == "CHK") & (hdr["status"] == "ISSUED")]
    ok(not chk.duplicated(rk).any(), "SF25 SF26: no two issued checks share claim, benefit, payee, period and amount")
    ret = hdr[hdr["check_or_trace"].isin(set(D["ach"]["trace_number"]))]
    rm = ret.merge(chk, on=rk, how="left", suffixes=("", "_r"))
    reiss = rm[rm["payment_no_r"].notna()]
    late = set(D["ach"][D["ach"]["trace_number"].isin(ret[~ret["payment_no"].isin(reiss["payment_no"])]["check_or_trace"])]
               ["return_date"])
    ok(len(ret) == 275 and (ret["method"] == "EFT").all() and len(reiss) == 271 and (reiss["issue_date_r"] > reiss["issue_date"]).all()
       and late == {"20260929"}, ("SF25: 271 returned EFTs paid again by check, the four returned 29 September not yet", late))
    vm = hdr[hdr["status"] == "VOID"].merge(chk, on=rk, how="left", suffixes=("", "_r"))
    ok(len(vm) == 85 and vm["payment_no_r"].notna().all() and (vm["issue_date_r"] > vm["issue_date"]).all(),
       "SF26: every voided check replaced by a new check")
    for s in K.PROG:
        ok(K.edge_distance(a2[s], 1000) >= 150, ("Ask 2 bin", s, a2[s]))
    frozen2 = {"HC-SS": 3724902.87, "HC-OT": 4652050.38, "RW-SS": 1805107.0, "RW-OT": 3992889.77, "MF-SS": 4276854.09,
               "MF-OT": 5232875.49, "CN-SS": 4999081.47, "CN-OT": 7281912.56}
    ok(all(abs(a2[s] - frozen2[s]) < 0.005 for s in K.PROG), ("Ask 2 unchanged to the cent by the merged claims", a2))
    ok(len(set(a1.values())) == 8, "Ask 1 counts distinct")

    # ---- separation: the call never reads the ask files or the distractors -------------------------------------
    D3 = dict(D)
    D3["pay"] = D["pay"].iloc[0:0]
    D3["ach"] = D["ach"].iloc[0:0]
    M3 = C.pilot_metrics(D3)
    ok(C.rung(M3, vol=v12)["teams"] == g["teams"], "the call unchanged with the payment files removed")
    D4 = dict(D)
    D4["merges"] = D["merges"].iloc[0:0]
    ok(C.intakes(D4, dt.date(2025, 10, 1), K.EXTRACT_END) == v12 and
       C.intakes(D, dt.date(2025, 10, 1), K.EXTRACT_END, merges=False) == v12,
       "the call's fill check unchanged with the merge file removed or unread")
    for f in K.DISTRACTORS:
        ok(f in files, f)
    # the call reads none of: the draft, the survey, the staffing plan (calc.load opens none of them)
    import inspect
    src = inspect.getsource(C)
    ok(not re.search(r"K\.(CHARTER_DRAFT_DOC|SURVEY|STAFFING)", src), "the solution reads no distractor")

    # ---- bins ----------------------------------------------------------------------------------------------------
    for s in K.PROG:
        ok(K.edge_distance(g["value"][s], 10000) >= 1500, ("team saving bin", s, g["value"][s]))
    ok(K.edge_distance(g["credit"], 100000) >= 20000, ("credit bin", g["credit"]))
    ok(abs(g["credit"] - round(g["credit"], -5)) > 1000, "no round headline")

    # ---- realism sweep -------------------------------------------------------------------------------------------
    notes = [r for r in _review_notes(target) if r]
    from collections import Counter
    cn = Counter(notes)
    ok(max(cn.values()) <= 6, ("a verifier's note recurs", cn.most_common(3)))
    shapes = Counter(re.sub(r"[\d$,./]+", "#", n) for n in notes)
    ok(len(shapes) >= 20 and max(shapes.values()) <= 0.15 * len(notes), ("the verifiers' notes vary in form", shapes.most_common(3)))
    rrows = _review_rows(target)
    arm_of = dict(zip(reg["legacy"], reg["arm"]))
    rates = []
    for seg in K.PROG:
        rs = [r for r in rrows if r[0] == seg]
        items = [int(r[1].split(".")[1]) for r in rs]
        ok(all(r[1].startswith("B%d." % (K.PROG.index(seg) + 1)) for r in rs) and sorted(items) == list(range(1, 201)),
           ("the review's references: one workpaper section a sheet, items 1 to 200", seg))
        ok(sum(1 for a_, b_ in zip(items, items[1:]) if b_ == a_ + 1) <= 5, ("references in claim-number sequence", seg))
        arms = [arm_of[C.norm_legacy(C.strip_check(r[2]))] for r in rs]
        mE = np.mean([i for i, a_ in zip(items, arms) if a_ == "E"])
        mU = np.mean([i for i, a_ in zip(items, arms) if a_ == "U"])
        ok(abs(mE - mU) < 30, ("the review's item numbers carry no group", seg, mE, mU))
        rates.append(sum(1 for r in rs if r[3]) / len(rs))
    ok(max(rates) - min(rates) >= 0.05, ("each sheet's reviewer remarks at their own rate", rates))
    ok(len(set(M[s]["nU"] for s in K.PROG)) == 8, "pilot sizes vary by segment")
    for f in files:
        b = open(P(f), "rb").read()
        ok(not re.search(rb"openpyxl|python-docx|ReportLab|reportlab|matplotlib", b), ("toolchain signature", f))
    people = set(json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                             ".claude", "skills", "fingerprint", "cards", "task139.json")))["world"]["people"])
    named = set(re.findall(r"\b(?:Julie Winters|Joanna Sullivan|Kathleen Reilly|Joel Kelly|Kristen Hansen|Juan Castillo|"
                           r"Gregory Friedman|Margaret York)\b", docs_txt))
    ok(named <= people, ("a persona off the card", named - people))
    dates = re.findall(r"\b(20\d\d)-(\d\d)-(\d\d)\b", open(P(K.EXTRACT)).read()[-4000000:])
    ok(max("%s-%s-%s" % d for d in dates) <= "2026-09-30", "no date after the pull in the extract")
    ok(pay["issue_date"].max() <= "2026-09-30" and pay["issue_date"].min() >= "2026-01-01", "payments inside the window")
    ok(pd.to_datetime(log["closed"], format="%m/%d/%Y").max() <= pd.Timestamp("2025-08-04"), "every pilot file closed by the log's export")
    exd = pd.read_csv(os.path.join(target, K.EXTRACT), dtype=str)
    ok(all(exd[c].dropna().max() <= "2026-09-30" for c in ("injury_date", "report_date", "disability_began",
       "first_indemnity_date", "closed_date", "reopened_date")), "H16: no extract date past the pull")
    ok(pay["void_date"].dropna().max() <= "2026-09-30", "H16: no void past the pull")
    achd = pd.read_csv(os.path.join(target, K.ACH_RETURNS), dtype=str)
    ok(achd["return_date"].max() <= "20260930", "H16: no bank return past the window")
    svd = pd.read_csv(os.path.join(target, K.SURVEY), dtype=str)
    ok(pd.to_datetime(svd["returned"].dropna(), format="%m/%d/%Y").max() <= pd.Timestamp("2025-08-04"),
       "H16: no survey return past the export")

    # ---- goldens against figures ---------------------------------------------------------------------------------
    ok(F["teams"] == g["teams"] and F["credit"] == 4100000, "figures.json carries the call")
    import openpyxl as ox
    wb = ox.load_workbook(os.path.join(golden, K.GOLD_BOOK), data_only=True)
    ws = wb["Placement"]
    vals = {r[0]: (r[3], r[4]) for r in ws.iter_rows(values_only=True) if r and r[0] in K.PROG}
    ok(all(vals[s] == (F["teams"][s], F["team_saving"][s]) for s in K.PROG), "the workbook's placement")
    a1w = {r[0]: r[1] for r in wb["2025 intakes"].iter_rows(values_only=True) if r and r[0] in K.PROG}
    a2w = {r[0]: r[1] for r in wb["Indemnity paid 2026"].iter_rows(values_only=True) if r and r[0] in K.PROG}
    ok(a1w == F["ask1_intakes_2025"] and a2w == F["ask2_paid_2026"], "the workbook's asks")
    print("checks.py: %d assertions passed" % N["ok"])
    return N["ok"]


def _doc_text(target, only=None):
    """The text of every document and workbook in the pack (PDF via pdftotext, DOCX and XLSX via their XML), or of the
    one file named."""
    import subprocess
    out = []
    for f in sorted(os.listdir(target)):
        if only and f != only:
            continue
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out.append(subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout)
        elif f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.endswith(".xml") and ("sharedStrings" in n or "document" in n):
                        out.append(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "ignore")))
    txt = "\n".join(out)
    txt = re.sub(r"-\n\s*", "-", txt)
    return re.sub(r"\s+", " ", txt)


def _dictionary(target):
    """The data dictionary's definitions, keyed by (file, field); a file's own row is keyed (file, "(file)")."""
    wb = openpyxl.load_workbook(os.path.join(target, K.DICTIONARY), read_only=True, data_only=True)
    out = {}
    for r in wb["Fields"].iter_rows(values_only=True):
        if r and len(r) >= 3 and r[0] and r[1] and r[2] and r[0] != "File":
            out[(str(r[0]), str(r[1]))] = str(r[2])
    return out


def _review_rows(target):
    """Every verified row of the review workbook, sheet by sheet: (segment, KPA ref, claim number, note)."""
    wb = openpyxl.load_workbook(os.path.join(target, K.REVIEW_BOOK), read_only=True, data_only=True)
    out = []
    for seg in K.PROG:
        on = False
        for r in wb[seg].iter_rows(values_only=True):
            if r and r[0] == "KPA ref":
                on = True
                continue
            if not on or not r or not r[0]:
                continue
            if str(r[0]).startswith("Sheet total"):
                break
            out.append((seg, str(r[0]), str(r[1]), r[6]))
    return out


def _review_notes(target):
    return [r[3] for r in _review_rows(target)]
