"""Generator checks for task268, run on the built pack and the world's clean truth. Every assertion is counted; any
failure stops the build. Labels: the ladder (rungs, the estimator family, bins), SF1 to SF11 (the semantic fork
table), R1 to R3c (the three rules, dataset-generation 7.1), the asks' devices, separation and the cracker, the input
gates and the realism sweep."""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

import analysis as A
import common as K
import deliver as DL
import records as R
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
N = [0]
GUL, FEN, WRE, LIN = "GUL", "FEN", "WRE", "LIN"


def ok(cond, label):
    N[0] += 1
    if not cond:
        raise AssertionError(label)


def edge(v, u=1.0):
    """Distance from v to the nearest edge of the cell it prints in at unit u."""
    return u / 2 - abs(v - round(v / u) * u)


def printed(S):
    return {h: DL.whole(100 * S[h]) for h in K.CODES}


def same_print(S1, S2, hosp=None):
    """The same hospital picked, the same runner-up, the same printed gap and the same printed survival for every
    hospital named."""
    p1, p2 = printed(S1), printed(S2)
    a1, b1, g1 = A.pick(S1)
    a2, b2, g2 = A.pick(S2)
    return a1 == a2 and b1 == b2 and DL.whole(100 * g1) == DL.whole(100 * g2) and \
        all(p1[h] == p2[h] for h in (hosp or K.CODES))


def world_cohort(w, view):
    """The 2022 and 2023 cohort straight from the generator's world, before any file is written: 'registry' as the
    registry sees it (the deaths the two sources report, follow-up ending at a move beyond the linkage or at the
    re-consent, the class the clinic records at each visit), 'truth' every patient's death or survival known."""
    out = []
    for p in w["patients"]:
        if p["year"] not in (2022, 2023) or p["reenrol"] is not None:
            continue
        two = R.two_year(p["dx"])
        hor = two - p["dx"]
        if view == "truth":
            dead = 0 <= p["death"] <= two
            out.append(dict(h=p["hosp"], T=(p["death"] - p["dx"]) if dead else hor, E=int(dead), lost=None, hor=hor,
                            visits=[], c0=p["c0"]))
            continue
        ends = sorted((x, why) for x, why in ((p["north_rec"], "north"), (p["wd"], "consent")) if x >= 0)
        end = ends[0] if ends else None
        seen = R.death_source(p) is not None and p["death"] <= two
        if seen and (end is None or p["death"] <= end[0]):
            T, E, lost = p["death"] - p["dx"], 1, None
        elif end is not None and end[0] < two:
            T, E, lost = end[0] - p["dx"], 0, end[1]
        else:
            T, E, lost = hor, 0, None
        vis = []
        for k in range(1, len(p["cls"])):
            v = int(p["vday"][k])
            if p["vatt"][k] and 0 < v - p["dx"] <= T and v <= R.end_day(p) and not (p["wd"] >= 0 and v >= p["wd"]):
                vis.append((v - p["dx"], int(p["cls"][k])))
        out.append(dict(h=p["hosp"], T=T, E=E, lost=lost, hor=hor, visits=vis, c0=p["c0"]))
    return out


def run(target, w):
    D = A.load(target)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    L = A.ladder(D)
    C = L["_cohort"]
    G = A.by_h(C)
    S = L["golden"]
    pick, runner, gap = A.pick(S)

    # ---------------------------------------------------------------- the ladder
    want = [("crude", FEN, 2.0), ("complete_case", WRE, 1.0), ("worst_case", WRE, 1.0), ("km", FEN, 1.0),
            ("km_exchange_censored", FEN, 0.8), ("ipcw_diagnosis_class", FEN, 0.6), ("ipcw_pooled", FEN, 1.5)]
    for r, h, m in want:
        a, b, g = A.pick(L[r])
        ok(a == h and 100 * g >= m, "ladder %s closes %s with margin %.1f (%s %.2f)" % (r, h, m, a, 100 * g))
        ok(sorted(K.CODES, key=lambda x: L[r][x]).index(GUL) >= 1, "ladder %s: Gullhaven not lowest below the decisive "
                                                                      "rung" % r)
    for r in A.FAMILY:
        a, b, g = A.pick(L[r])
        ok(a == GUL and b == FEN and 100 * g >= 2.5,
           "family %s closes Gullhaven, Fennick next, margin %.2f" % (r, 100 * g))
    ok(pick == GUL and runner == FEN, "the golden picks Gullhaven, Fennick the next lowest")
    for h in K.CODES:
        vals = [100 * L[r][h] for r in A.FAMILY]
        lo, hi = min(vals), max(vals)
        ok(DL.whole(lo) == DL.whole(hi) and min(lo - (DL.whole(lo) - 0.5), DL.whole(hi) + 0.5 - hi) >= (
           0.2 if h in (GUL, WRE) else 0.05), "%s: every form of the decisive estimator prints the same whole percent, "
                                               "the whole family clear of the edges (%.2f to %.2f)" % (h, lo, hi))
    gaps = [100 * A.pick(L[r])[2] for r in A.FAMILY]
    ok(DL.whole(min(gaps)) == DL.whole(max(gaps)) and min(min(gaps) - (DL.whole(min(gaps)) - 0.5),
                                                          DL.whole(max(gaps)) + 0.5 - max(gaps)) >= 0.3,
       "the gap prints the same whole point under every form, the family 0.3 or more from the edges (%.2f to %.2f)"
       % (min(gaps), max(gaps)))
    ok(DL.whole(100 * gap) == DL.whole(100 * S[runner]) - DL.whole(100 * S[pick]),
       "SF7 the gap from unrounded and from rounded survival agree")
    pos = [sorted(K.CODES, key=lambda x: L[r][x]).index(GUL) + 1 for r in ("crude", "km", "ipcw_diagnosis_class",
                                                                           "ipcw_pooled", "golden")]
    ok(pos == [4, 2, 2, 2, 1], "position: Gullhaven 4th crude, 2nd by Kaplan-Meier, weighted by the class at diagnosis "
                               "and weighted pooled, 1st at the decisive step (%s)" % pos)
    km_gap = 100 * A.pick(L["km"])[2]
    ok(A.pick(L["km"])[1] == GUL and DL.whole(km_gap) != DL.whole(100 * gap) and edge(km_gap) >= 0.15,
       "the default path's gap (Fennick to Gullhaven, %.2f) prints a different whole point from the golden's" % km_gap)
    ok(100 * (L["km"][GUL] - S[GUL]) >= 4.0 and abs(100 * (L["km"][FEN] - S[FEN])) < 0.5,
       "dominance: the decisive step moves Gullhaven by 4 points or more and Fennick by under half a point")
    ok(100 * (L["ipcw_diagnosis_class"][GUL] - S[GUL]) >= 3.0,
       "dominance: the class at diagnosis leaves Gullhaven 3 points or more above the golden")
    ok(A.pick(L["km"])[0] != A.pick(S)[0], "disagreement: the default path and the golden pick different hospitals")
    ok(fig["call"]["hospital"] == K.NAME[pick] and fig["call"]["gap"] == DL.whole(100 * gap)
       and fig["call"]["survival"] == DL.whole(100 * S[pick]), "figures.json carries the call, its survival and the gap")
    ok(all(fig["survival"][K.NAME[h]] == DL.whole(100 * S[h]) for h in K.CODES), "figures.json carries every survival")

    # ---------------------------------------------------------------- the semantic fork table
    ok(same_print(S, A.golden(D, basis="enrolment"), [GUL, FEN]),
       "SF1 the cohort chosen by enrolment date: the call, both hospitals' figures and the gap the same")
    fv = A.golden(D, basis="first_visit")
    ok(same_print(S, fv, [GUL]) and printed(fv)[FEN] != printed(S)[FEN],
       "SF1 the cohort chosen by first clinic visit: the call, Gullhaven's figure and the gap the same, Fennick at %d per "
       "cent, ruled out by the manual's 2.1 (the diagnosis date is the date of the diagnosing encounter)" % printed(fv)[FEN])
    hosp_of = {r["registry_id"]: A.HOSP[r["hospital"]] for r in D["patients"]}
    ok(all(A.HOSP[r["clinic"]] == hosp_of[r["registry_id"]] for r in D["visits"]),
       "SF2 every clinic visit is at the hospital of diagnosis")
    ok(same_print(S, A.golden(D, horizon=730)), "SF3 two years as 730 days: every printed figure and the gap the same")
    nx = A.golden(D, exchange_deaths=False)
    ok(A.pick(nx)[0] == GUL and printed(nx)[GUL] != printed(S)[GUL],
       "SF4 the exchange's deaths unread: Gullhaven at %d per cent, ruled out by the manual's 4.2" % printed(nx)[GUL])
    ok(A.pick(L["complete_case"])[0] == WRE, "SF5 the patients no longer followed left out: Wrenhaven")
    ok(min(K.CODES, key=lambda h: printed(S)[h]) == GUL and sum(printed(S)[h] == printed(S)[GUL] for h in K.CODES) == 1,
       "SF6 lowest after rounding: the same hospital, no hospital tying it")
    cnr = {r["registry_id"] for r in D["events"] if r["event"] == "CNR"}
    ok(A.pick(A.golden(D, drop=cnr))[0] == WRE, "SF8 the re-consent's withdrawals left out of Wrenhaven's cohort: "
                                                "Wrenhaven, ruled out by the charter's 3.2")
    ok(all(hosp_of[r] == WRE for r in cnr) and len(cnr) > 300, "SF8 every withdrawal is Wrenhaven's")
    last_visit = {}
    for r in D["visits"]:
        last_visit[r["registry_id"]] = max(last_visit.get(r["registry_id"], ""), r["visit_date"])
    rel = [r for r in D["events"] if r["event"] == "REL"]
    ok(all(r["registry_id"] in last_visit and last_visit[r["registry_id"]] < r["event_date"] for r in rel),
       "SF12 every relocation is recorded after the visit where the patient reported it, the last visit on record, so the "
       "class at the loss is the same whether the loss date's own visits are counted or not")
    movers = [p for p in C if p["lost"] == "north"]
    ok(all(p["visits"] and p["visits"][-1][0] < p["T"] for p in movers), "SF12 every mover's last visit precedes the loss")
    fl_new = {r["mrn"] for r in D["fl"]}
    ex_ids = {r["PARTNER_ID"] for r in D["exchange"]}
    leg2new = {r["legacy_mrn"]: r["new_mrn"] for r in D["crosswalk"]}
    rid2new = {r["registry_id"]: leg2new.get(r["mrn"], r["mrn"]) for r in D["patients"]}
    ok(not any(rid2new[x] in fl_new for x in ex_ids), "SF9 no death in both the Florida linkage and the exchange")
    spell = Counter(r["nyha_class"] for r in D["visits"])
    ok(len(spell) == 16 and all(s in A.CLASS for s in spell), "SF10 sixteen spellings of the four classes, every one read")
    ok(not any(p["h"] == "BRN" for p in C) and not any(r["hospital"] == "BRN" for r in D["patients"]
                                                       if r["diagnosis_date"] < "2024-01-01"),
       "SF11 no 2022 or 2023 enrolment carries the North Campus code")

    # ---------------------------------------------------------------- the three rules (dataset-generation 7.1)
    ok(len(D["visits"]) > 25000 and all(r["nyha_class"] for r in D["visits"]),
       "R1 the visit-level classes ship, the raw material of the weighting")
    ok(L["ipcw_diagnosis_class"][GUL] != S[GUL], "R1 the golden reads the class at each visit, not only at diagnosis")
    bad = re.compile(r"surviv|mortal|ipcw|censor|probab|hazard|risk|weight(?!_kg)", re.I)
    for f in sorted(os.listdir(target)):
        if f.endswith(".csv") or f.endswith(".txt"):
            head = open(os.path.join(target, f), encoding="utf-8").readline()
            ok(not bad.search(head), "R1 no shipped column holds a survival, weight or chance of loss: %s" % f)
    import openpyxl
    for f in sorted(os.listdir(target)):
        if f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(os.path.join(target, f), read_only=True)
            for ws in wb.worksheets:
                first = next(ws.iter_rows(max_row=1, values_only=True))
                ok(not bad.search(" ".join(str(x) for x in first if x)), "R1 no survival column in %s/%s" % (f, ws.title))
    ok(same_print(S, A.golden(D, raw_class=True)), "R2 the class spellings left unharmonised (each spelling its own "
                                                    "class): every printed figure and the gap the same")
    xc = A.golden(D, exchange_censors=True)
    ok(same_print(S, xc, [GUL, FEN]), "R2 the moves to Georgia, Alabama and South Carolina read as losses too: the call, "
                                      "Gullhaven's and Fennick's figures and the gap the same (Linmoor at %d per cent, "
                                      "ruled out by the manual's 4.2)" % printed(xc)[LIN])
    legacy_enrolled = [r for r in D["patients"] if r["mrn"].startswith("H") and r["diagnosis_date"] < "2024-01-01"]
    ok(len(legacy_enrolled) > 8000 and not any(r["mrn"] in fl_new for r in legacy_enrolled),
       "R2 the crosswalk unread: no 2022 or 2023 patient finds a Florida death (loud)")
    ok(all(re.fullmatch(r"20(22|23|24|25)(0[1-9]|1[0-2])\d\d", r["DOD"]) for r in D["exchange"]),
       "R2 the exchange's dates are YYYYMMDD throughout")
    ok(all(hasattr(r["dod"], "year") for r in D["fl"]), "R2 the Florida linkage's dates are date cells")
    ok(sum(1 for r in D["patients"] if r["hospital"] == "BRN") > 100, "R2 the North Campus code is in use from 2024")
    reg, tru = world_cohort(w, "registry"), world_cohort(w, "truth")
    rg, tg = A.by_h(reg), A.by_h(tru)
    km_w = {h: A.wkm(rg[h]) for h in K.CODES}
    ok(A.pick(km_w)[0] == FEN, "R3a the analyst test on the clean truth: Kaplan-Meier on the registry's view, every "
                               "filed rule applied, names Fennick")
    gw = {h: A.ipcw(rg[h]) for h in K.CODES}
    ok(all(abs(gw[h] - S[h]) < 1e-9 for h in K.CODES) and all(abs(km_w[h] - L["km"][h]) < 1e-9 for h in K.CODES),
       "R3b the registry's view built from the world and read from the files give the same estimates")
    ok(A.pick(gw)[0] == GUL and A.pick(gw)[2] >= 0.015, "R3b the decisive step alone on the clean truth names Gullhaven")
    tr = {h: 1 - sum(p["E"] for p in tg[h]) / len(tg[h]) for h in K.CODES}
    ok(A.pick(tr)[0] == GUL and A.pick(tr)[2] >= 0.015, "R3b every patient's true two-year status names Gullhaven "
                                                       "(%.2f points)" % (100 * A.pick(tr)[2]))
    ok(A.pick({h: A.ipcw(rg[h], key="diagnosis") for h in K.CODES})[0] == FEN and
       A.pick({h: A.ipcw(rg[h], pool=reg) for h in K.CODES})[0] == FEN,
       "R3b each lower rung's single correction on the clean truth (the class at diagnosis; a chance pooled over the "
       "hospitals) stays on Fennick")
    ok(all(abs(tr[h] - S[h]) < 0.02 for h in K.CODES), "R3b the golden within 2 points of every hospital's truth")
    blocks = Counter(tuple(r["weight_kg"] for r in D["visits"][i:i + 8]) for i in range(0, len(D["visits"]) - 8, 8))
    ok(max(blocks.values()) == 1, "R3c no repeated block of visit readings")
    sizes = [len(G[h]) for h in K.CODES]
    ok(len(set(sizes)) == 5 and all(s % 100 for s in sizes), "R3c cohort sizes differ and none is round")
    ok(not any(re.search(r"memo|draft|estimate|survival|analysis", f, re.I) for f in os.listdir(target)),
       "R3c no memo, draft or estimate file")

    # ---------------------------------------------------------------- the asks: devices, separation, the cracker
    aa, ab = A.ask_a(D), A.ask_b(D)
    rows25 = [r for r in D["lab"] if r["released"][:4] == "2025"]
    key = Counter((r["performing_lab"], r["mrn"], r["collected"]) for r in rows25)
    ok(max(key.values()) == 2, "Ask A: a specimen is reported at most twice")
    pairs = Counter(k[0] for k, v in key.items() if v == 2)
    for h in K.CODES:
        ok(20 <= pairs[h] <= 60, "Ask A %s: %d corrections re-accessioned and released again" % (h, pairs[h]))
    by = {}
    for r in rows25:
        by.setdefault((r["performing_lab"], r["mrn"], r["collected"]), []).append(r)
    for k, rs in by.items():
        if len(rs) == 2:
            a, b = sorted(rs, key=lambda r: r["released"])
            ok(int(b["accession"][1:]) > int(a["accession"][1:]) and a["result_status"] == b["result_status"] == "F"
               and a["result"] != b["result"], "Ask A: a correction carries a later accession, both final, a new value")
    ok(len({r["accession"] for r in D["lab"]}) == len(D["lab"]), "Ask A: accessions unique")
    for k, rs in by.items():
        if len(rs) == 2:
            a, b = rs
            ok(a["received"] == b["received"], "Ask A: a correction keeps its specimen's collection and receipt times")
            ok((A._num(a["result"]) >= K.REFERRAL) == (A._num(b["result"]) >= K.REFERRAL),
               "Ask A C1: no correction moves a specimen across the referral level, so either result counts it the same")
    ok(len({tuple(r.values()) for r in D["lab"]}) == len(D["lab"]), "Ask A: no exact duplicate row")
    times = {}
    for r in rows25:
        times.setdefault((r["performing_lab"], r["mrn"], r["collected"][:10]), set()).add(r["collected"])
    for h in K.CODES:
        n2 = sum(1 for k, v in times.items() if k[0] == h and len(v) >= 2)
        ok(n2 > pairs[h], "Ask A %s: genuine second specimens the same day (%d) outnumber the corrections" % (h, n2))
    ok(any(r["result"] == ">35000" for r in rows25) and any(r["result"] == "<35" for r in rows25),
       "Ask A hazard: results out of range written as text")
    ok(any(r["collected"][:10] == "2024-12-31" for r in rows25), "Ask A hazard: 31 December 2024 specimens reported in "
                                                                 "2025")
    ok(any(r["collected"][:4] == "2025" and r["released"][:4] == "2026" for r in D["lab"]),
       "Ask A hazard: 2025 specimens reported in January 2026")
    ok(any(r["ordering_location"].startswith("BRN-") and r["performing_lab"] == "BRE" for r in D["lab"]),
       "Ask A hazard: the North Campus orders through Brenmoor's laboratory")
    reen = {}
    pat = {r["registry_id"]: r for r in D["patients"]}
    new2rows = {}
    for r in D["patients"]:
        new2rows.setdefault(leg2new.get(r["mrn"], r["mrn"]), []).append(r)
    ev_rids = {r["registry_id"] for r in D["events"]}
    for r in D["patients"]:
        if A.diagnosed(r)[:4] != "2025":
            continue
        earlier = [q for q in new2rows[r["mrn"]] if q["registry_id"] != r["registry_id"]
                   and A.diagnosed(q) < A.diagnosed(r)]
        if earlier:
            h = A.HOSP[r["hospital"]]
            reen[h] = reen.get(h, 0) + 1
            ok(all(q["mrn"].startswith("H") and q["diagnosis_date"] < "2024-01-01" and q["registry_id"] not in ev_rids
                   for q in earlier), "Ask B: a re-enrolment's earlier enrolment is a 2022 or 2023 patient under a "
                                      "legacy number who never moved or withdrew")
    for h in K.CODES:
        ok(15 <= reen.get(h, 0) <= 40, "Ask B %s: %d re-enrolments under the new number" % (h, reen.get(h, 0)))
    ok(len({r["mrn"] for r in D["patients"]}) == len(D["patients"]) and len(pat) == len(D["patients"]),
       "Ask B: registry identifiers and record numbers unique in the registry")
    ok(any(r["diagnosis_date"][:4] == "2024" and r["enrolment_date"][:4] == "2025" for r in D["patients"]),
       "Ask B hazard: December 2024 diagnoses enrolled in 2025")
    late = [r for r in D["patients"] if r["diagnosis_date"] > r["enrolment_date"]]
    ok(all(K.MODULE_UPDATE.isoformat() <= r["enrolment_date"] < K.MODULE_FIX.isoformat() for r in late),
       "Ask B: a diagnosis date after the enrolment date only on enrolments between the November 2024 module update and "
       "the February 2025 fix (none in the cohort)")
    for h in K.CODES:
        x = [r for r in late if A.HOSP[r["hospital"]] == h and r["enrolment_date"][:4] == "2024"
             and r["diagnosis_date"][:4] == "2025"]
        ok(len(x) >= 5 and sum(r["diagnosis_setting"] in A.INPATIENT for r in x) >= 2,
           "Ask B %s: %d 2024 diagnoses whose record shows a 2025 date after the enrolment" % (h, len(x)))
    import datetime as _dt
    over = [p for p in w["patients"] if "dx_shown" in p]
    ok(all((W.DAY0 + _dt.timedelta(p["dx"])).year == (W.DAY0 + _dt.timedelta(p["enrol"])).year
           and p["enrol"] < p["dx_shown"] < (K.MODULE_FIX - W.DAY0).days and (W.DAY0 + _dt.timedelta(p["enrol"])).month != 1
           for p in over), "Ask B: every overwritten date sits after its enrolment and before the fix, the diagnosis in the "
                           "enrolment's year, no January enrolment overwritten")
    truth = {h: [0, 0] for h in K.CODES}
    for p in w["patients"]:
        if p["reenrol"] is None and p["enrol"] <= W.EXTRACT_DAY and (W.DAY0 + _dt.timedelta(p["dx"])).year == 2025:
            truth[p["hosp"]][0] += 1
            truth[p["hosp"]][1] += p["setting"] == "Inpatient"
    ok(all(tuple(truth[h]) == ab[h] for h in K.CODES), "Ask B: the golden reproduces every hospital's true 2025 new "
                                                       "diagnoses and inpatient diagnoses exactly")
    sett = Counter(r["diagnosis_setting"] for r in D["patients"] if r["diagnosis_date"][:4] == "2025")
    ok(sett["Inpatient"] > 0 and sett["INPT"] > 0 and sett["ED visit"] > 0, "Ask B hazard: Inpatient and INPT spellings, "
                                                                           "emergency visits not admitted")
    for h, what in (("plain", "the export as it stands (the cracker)"), ("day", "one result a patient a day")):
        x = A.ask_a(D, h)
        for c in K.CODES:
            ok(x[c][0] != aa[c][0] and x[c][1] != aa[c][1], "Ask A %s: %s misses both figures" % (c, what))
    x = A.ask_a(D, "first")
    for c in K.CODES:
        ok(x[c] == aa[c], "Ask A %s C1: the first release kept gives the same specimens and referral count" % c)
    for h, what in (("plain", "the registry as it stands (the cracker)"), ("drop_crosswalked", "every crosswalked number "
                                                                                              "dropped"),
                    ("reader", "the re-enrolments left out by the date shown (stage 4 round 1's reader)"),
                    ("dated", "the dates supported, the re-enrolments kept")):
        x = A.ask_b(D, h)
        for c in K.CODES:
            ok(x[c][0] != ab[c][0] and x[c][1] != ab[c][1], "Ask B %s: %s misses both figures" % (c, what))
    for c in K.CODES:
        ok(fig["ask_a"][K.NAME[c]] == {"tests": aa[c][0], "referral": aa[c][1]}, "figures.json Ask A %s" % c)
        ok(fig["ask_b"][K.NAME[c]] == {"new": ab[c][0], "inpatient": ab[c][1]}, "figures.json Ask B %s" % c)
        ok(all(v % 100 for v in aa[c] + ab[c]), "Ask figures for %s are not round" % c)
    ok(not any(r["registry_id"] in {p["rid"] for p in C} for r in D["patients"] if r["diagnosis_date"][:4] == "2025"),
       "separation: no re-enrolment in the 2022 and 2023 cohort")
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        with open(os.path.join(tmp, K.FILES["lab"]), "w", encoding="utf-8") as fo:
            fo.write(open(os.path.join(target, K.FILES["lab"]), encoding="utf-8").readline())
        keep = [r for r in D["patients"] if r["diagnosis_date"] < "2024-01-01"]
        with open(os.path.join(tmp, K.FILES["patients"]), "w", newline="", encoding="utf-8") as fo:
            wr = csv.DictWriter(fo, fieldnames=list(D["patients"][0].keys()), lineterminator="\r\n")
            wr.writeheader()
            wr.writerows(keep)
        D3 = A.load(tmp)
        ok(A.ladder(D3)["golden"] == S, "separation: the call computes identically with the laboratory file emptied and "
                                        "every enrolment from 2024 on removed")
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        for k in ("visits", "events", "exchange"):
            with open(os.path.join(tmp, K.FILES[k]), "w", encoding="utf-8") as fo:
                fo.write(open(os.path.join(target, K.FILES[k]), encoding="utf-8").readline())
        D4 = A.load(tmp)
        ok(A.ask_a(D4) == aa and A.ask_b(D4) == ab, "separation: the asks compute identically with the visits, the "
                                                   "follow-up events and the exchange's deaths emptied")
    finally:
        shutil.rmtree(tmp)
    for k in K.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in os.listdir(target):
                if f != K.FILES[k]:
                    shutil.copy(os.path.join(target, f), tmp)
            D5 = A.load(tmp)
            ok(A.ladder(D5)["golden"] == S and A.ask_a(D5) == aa and A.ask_b(D5) == ab,
               "distractor %s deleted: the call and every ask unchanged" % K.FILES[k])
        finally:
            shutil.rmtree(tmp)
    cr = subprocess.run([sys.executable, os.path.join(HERE, "cracker.py"), target], capture_output=True, text=True)
    ok(cr.returncode == 0, "the cracker's path misses every ask figure: " + cr.stdout[-600:] + cr.stderr[-600:])

    # ---------------------------------------------------------------- input gates and realism
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({os.path.splitext(f)[1] for f in files}) >= 3, "three or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "a 25,000-row file")
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(sorted(meta["distractor_files"]) == sorted("target/" + K.FILES[k] for k in K.DISTRACTORS),
       "metadata names the distractors")
    ok(not any("distractor" in f.lower() for f in files), "no file name says distractor")
    listed = {l.split()[0] for l in open(os.path.join(target, K.FILES["contents"]), encoding="utf-8").read().splitlines()
              if l.split() and "." in l.split()[0] and l.split()[0] in files}
    ok(listed == set(files) - {K.FILES["contents"]}, "H9 the contents list names every shipped file but itself")
    ext = K.EXTRACT.isoformat()
    ok(max(r["visit_date"] for r in D["visits"]) <= ext and max(r["enrolment_date"] for r in D["patients"]) <= ext
       and max(r["event_date"] for r in D["events"]) <= ext, "H16 no registry date after the extract")
    ok(max(r["dod"] for r in D["fl"]) <= K.DEATHS_TO and max(r["DOD"] for r in D["exchange"]) <= "20251231",
       "H16 no death after the sources' completeness date")
    ok(max(r["released"] for r in D["lab"]) < "2026-01-07", "H16 no laboratory release after the export window")
    ok(all(r["from"] >= "2026-01-05" for r in csv.DictReader(open(os.path.join(target, K.FILES["clinics"]),
                                                                   encoding="utf-8"))),
       "H16 the 2026 clinic timetable is the one forward-dated file (allowed)")
    cnr_day = {r["registry_id"]: r["event_date"] for r in D["events"] if r["event"] == "CNR"}
    ok(not any(r["event"] == "REL" and r["registry_id"] in cnr_day and r["event_date"] > cnr_day[r["registry_id"]]
               for r in D["events"]), "realism: no relocation recorded after a consent withdrawal")
    dx_of = {r["registry_id"]: r["diagnosis_date"] for r in D["patients"]}
    new_of = {r["registry_id"]: leg2new.get(r["mrn"], r["mrn"]) for r in D["patients"]}
    fl_day = {}
    for r in D["fl"]:
        fl_day[r["mrn"]] = min(fl_day.get(r["mrn"], r["dod"]), r["dod"])
    ok(not any(new_of[k] in fl_day and str(fl_day[new_of[k]]) < v for k, v in dx_of.items())
       and not any(r["DOD"] < dx_of[r["PARTNER_ID"]].replace("-", "") for r in D["exchange"]),
       "realism: no death dated before the diagnosis the record shows")
    gone_by = {}
    for r in D["patients"]:
        m = new_of[r["registry_id"]]
        if m in fl_day:
            gone_by[m] = str(fl_day[m])
    rid_new = {r["registry_id"]: new_of[r["registry_id"]] for r in D["patients"]}
    for r in D["exchange"]:
        m = rid_new[r["PARTNER_ID"]]
        d = "%s-%s-%s" % (r["DOD"][:4], r["DOD"][4:6], r["DOD"][6:])
        gone_by[m] = min(gone_by.get(m, d), d)
    for r in D["events"]:
        if r["event"] == "REL":
            m = rid_new[r["registry_id"]]
            gone_by[m] = min(gone_by.get(m, r["event_date"]), r["event_date"])
    ok(not any(r["mrn"] in gone_by and r["collected"][:10] >= gone_by[r["mrn"]] for r in D["lab"]),
       "realism: no laboratory specimen from a registry patient after their death or relocation")
    ok(all(r["destination_state"] in K.STATES_NORTH + list(K.EXCHANGE_STATES) for r in D["events"] if r["event"] == "REL")
       and all(r["destination_state"] == "" for r in D["events"] if r["event"] == "CNR"), "events carry their states")
    yrs = Counter(r["diagnosis_date"][:4] for r in D["patients"])
    ok(len({yrs[y] for y in ("2022", "2023", "2024", "2025")}) == 4, "the yearly enrolments vary")
    from pypdf import PdfReader
    must = {"charter": ["had the lowest two-year survival from diagnosis",
                        "including patients the registry no longer follows", "at or above 400 pg/mL"],
            "manual": ["The diagnosis date is the date of that encounter", "is recorded as a relocation (event REL), with the "
                       "state they are moving to", "The registry has no source for deaths in any other state",
                       "returned each quarter by the", "leaves follow-up that day (event CNR)"]}
    for k, sentences in must.items():
        path = os.path.join(target, K.FILES[k])
        strict = " ".join(" ".join((pg.extract_text() or "").split()) for pg in PdfReader(path, strict=True).pages)
        other = " ".join(subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.split())
        for t in sentences:
            ok(t in strict and t in other, "H25 %s reads the same under a strict parser and pdftotext: %r"
               % (K.FILES[k], t[:40]))
    names = [K.ORG.split()[0]] + [K.SHORT[h] for h in K.CODES]
    ok(len(set(names)) == 6, "every invented name distinct")
    print("checks: %d assertions passed" % N[0])
    measure(L, G, w)
    return N[0]


def measure(L, G, w):
    """The figures the design note quotes, printed from the build."""
    for r in A.WRONG + A.FAMILY:
        a, b, g = A.pick(L[r])
        print("  %-22s %s | %s by %.2f" % (r, " ".join("%s %.2f" % (h, 100 * L[r][h]) for h in K.CODES), a, 100 * g))
    for h in K.CODES:
        g = G[h]
        north = [p for p in g if p["lost"] == "north"]
        hi = sum(1 for p in north if p["visits"] and p["visits"][-1][1] >= 2)
        ex = [p for p in g if p["exch_full"] is not None and p["exch_full"] < p["hor"]]
        st = [p for p in g if p["lost"] is None and p not in ex]
        print("  %s n %d, deaths %d, moved north %d (%.1f%%, %d in class III or IV at the move), withdrawn %d, moved "
              "within the exchange %d (alive at two years %.1f%%, stayers %.1f%%), class at diagnosis movers %.2f "
              "others %.2f" % (h, len(g), sum(p["E"] for p in g), len(north), 100 * len(north) / len(g), hi,
                               sum(p["lost"] == "consent" for p in g), len(ex),
                               100 - 100 * sum(p["E"] for p in ex) / max(1, len(ex)),
                               100 - 100 * sum(p["E"] for p in st) / max(1, len(st)),
                               sum(p["c0"] for p in north) / max(1, len(north)),
                               sum(p["c0"] for p in g if p["lost"] != "north") / len(g)))
