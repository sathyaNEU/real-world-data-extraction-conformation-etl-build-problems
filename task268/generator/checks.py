"""Generator checks for task268, run on the built pack and the world's clean truth. Every assertion is counted; any
failure stops the build. Labels: the ladder, SF1 to SF12 (the semantic fork table), R1 to R3c (the three rules,
dataset-generation 7.1), the asks' devices and the cracker, the input gates and the realism sweep."""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

import numpy as np

import analysis as A
import common as K
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
N = [0]
HMD, BRB = "Halmorie Deep", "Brettach Bank"


def ok(cond, label):
    N[0] += 1
    if not cond:
        raise AssertionError(label)


def edge(v, u=1.0):
    """Distance from v to the nearest edge of the cell it rounds into at unit u."""
    return u / 2 - abs(v - round(v / u) * u)


def printed(f):
    return {g: round(100 * f[g]) for g in f}


def same_print(f1, f2, grounds=None):
    c1, c2 = A.call(f1), A.call(f2)
    p1, p2 = printed(f1), printed(f2)
    return all(p1[g] == p2[g] for g in (grounds or K.GROUND_NAMES)) and round(100 * c1["gap"]) == round(100 * c2["gap"]) \
        and c1["pick"] == c2["pick"] and c1["runner"] == c2["runner"]


def truth_falls(T, how):
    """The clean truth: 'stock' the ground's true weight of haddock, 'cpue' the fleet's expected catch per hour (the
    density of the cells it tows, weighted by its effort), 'plain' the survey's stations' expected catches averaged."""
    out = {}
    for g in K.GROUND_NAMES:
        idx = [i for i, c in enumerate(T["cells"]) if c["ground"] == g]
        ix = {}
        for y in K.YEARS:
            d = np.array([T["dens"][(i, y)] for i in idx])
            if how == "stock":
                ix[y] = float(np.sum(d * np.array([T["cells"][i]["area"] for i in idx])))
            elif how == "cpue":
                att = d ** W.BETA
                att[d < W.FLOOR * d.max()] = 0.0
                ix[y] = float(np.sum(att * d) / np.sum(att))
            elif how == "plain":
                st = [s for s in T["stations"] if s["ground"] == g and s["from"] <= y <= s["to"]]
                ix[y] = float(np.mean([T["dens"][(s["cell"], y)] * s["eff"] for s in st]))
        b = np.mean([ix[y] for y in K.BASE])
        out[g] = 1 - ix[K.LATEST] / b
    return out


def run(target, T):
    D = A.load(target)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    L = A.ladder(D)

    # ---------------------------------------------------------------- the ladder
    for r in ("R0", "R1", "R1v", "R2"):
        c = A.call(L[r])
        ok(c["pick"] == BRB and c["margin"] >= 1.15, "ladder %s closes Brettach Bank with margin 1.15 (%s %.2f)"
           % (r, c["pick"], c["margin"]))
        ok(c["order"].index(HMD) >= 1, "ladder %s: Halmorie Deep not first before the decisive rung" % r)
    G = L["R3"]
    c3 = A.call(G)
    ok(c3["pick"] == HMD and c3["margin"] >= 1.15, "R3 closes Halmorie Deep with margin 1.15 (%.2f)" % c3["margin"])
    ok(c3["runner"] == BRB, "SF6 the runner-up is Brettach Bank")
    ok(L["R3"][HMD] - L["R2"][HMD] > 0.15 and abs(L["R3"][BRB] - L["R2"][BRB]) < 0.05,
       "dominance: the stratified survey lifts Halmorie Deep's fall by more than 15 points, Brettach Bank's under 5")
    for g in K.GROUND_NAMES:
        ok(edge(100 * G[g]) >= 0.12, "%s's fall away from its whole percent's edge" % g)
    gap = 100 * c3["gap"]
    ok(edge(gap) >= 0.12, "the gap away from its whole point's edge")
    ok(round(gap) == round(100 * G[HMD]) - round(100 * G[BRB]), "SF7 the gap from unrounded and from rounded falls agree")
    ok(fig["call"]["ground"] == HMD and fig["call"]["gap"] == round(gap), "figures.json carries the call and the gap")
    ok(all(fig["falls"][g] == round(100 * G[g]) for g in K.GROUND_NAMES), "figures.json carries every fall")

    # ---------------------------------------------------------------- the semantic fork table
    tw = A.tows(D)
    ok(all(K.GROUND_CODE[t["ground"]] == t["code"] for t in tw), "SF1 every survey tow lies in a cell of its own ground")
    ok(A.call(A.falls(A.survey_index(D, measure="n")))["pick"] == HMD, "SF2 numbers for weight: the same call")
    ok(A.call(A.falls(A.survey_index(D), latest=2025))["pick"] == HMD, "SF3 2025 as the latest year: the same call")
    ok(same_print(G, A.falls(A.survey_index(D), base="pooled", pooled=A.pooled_base(D))),
       "SF4 the base as the three years' tows pooled: every printed fall and the gap the same")
    ix = A.survey_index(D)
    ratio = {g: np.mean([ix[g][y] for y in K.BASE]) / ix[g][2026] - 1 for g in K.GROUND_NAMES}
    ok(max(ratio, key=ratio.get) == HMD, "SF5 the base over 2026 less one: the same call")
    drop = {g: np.mean([ix[g][y] for y in K.BASE]) - ix[g][2026] for g in K.GROUND_NAMES}
    ok(max(drop, key=drop.get) == BRB and round(drop[BRB], 1) == 25.7 and round(drop[HMD], 1) == 24.2,
       "SF5 the drop in kg a tow puts Brettach Bank first (25.7 against 24.2), the reading plan 4.1 rules out")
    ok([A.call(L[r])["order"].index(HMD) + 1 for r in ("R0", "R1", "R1v", "R2", "R3")] == [6, 5, 6, 2, 1],
       "the ladder: Halmorie Deep 6th, 5th, 6th, 2nd, then 1st")
    ok(all(t["survey_year"] == t["date"][:4] and t["date"][5:7] == "10" for t in D["survey"]),
       "SF8 every tow in its survey year's October")
    ok(same_print(G, A.falls(A.survey_index(D, missed="impute")), [HMD, BRB]),
       "SF9 the station missed in 2020 (Cullardy Patch) carried from its other years: the call, both falls and the gap "
       "the same")
    ok(same_print(G, A.falls(A.survey_index(D, moved="drop")), [HMD, BRB]),
       "SF10 the replaced stations (Vallaskie Hole) dropped: the call, both falls and the gap the same")
    ok(same_print(G, A.falls(A.survey_index(D, weights="cells"))),
       "SF11 bands weighted by their count of cells: every printed fall and the gap the same")
    ok(same_print(G, A.falls(A.survey_index(D, band_by="depth"))),
       "SF11 bands from the sounder depth at the shot: every printed fall and the gap the same")
    ok(A.call(A.falls(A.survey_index(D, stat="geo")))["pick"] == HMD, "SF12 a geometric mean of the tows: the same call")

    # ---------------------------------------------------------------- the three rules (dataset-generation 7.1)
    ok(len(D["survey"]) > 1500 and all(r["haddock_kg"] != "" for r in D["survey"]),
       "R1 the survey's tow-level catches ship, the raw material of a design-based estimate")
    for f in os.listdir(target):
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").readline().lower()
            ok(not any(w in head for w in ("fall", "index", "stock", "biomass", "stratum", "weight_share")),
               "R1 no shipped column holds a ground's stock, index or fall: %s" % f)
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        for k in ("paper", "elog"):
            open(os.path.join(tmp, K.FILES[k]), "w").write(open(os.path.join(target, K.FILES[k])).readline())
        D2 = A.load(tmp)
        ok(A.falls(A.survey_index(D2)) == G, "R2 the logbooks' mess (paper round weight, e-logbook gutted weight, cells "
           "as rectangle and sub-square or as one code, the re-registered vessels, UTC haul times) moves nothing on the "
           "decisive path: the golden computes identically with both logbook files emptied")
    finally:
        shutil.rmtree(tmp)
    ok(True, "R2 the survey's replaced stations and the station missed in 2020: SF10 and SF9 above")
    tc = truth_falls(T, "cpue")
    ok(A.call(tc)["pick"] == BRB, "R3a the analyst test on the clean truth: the fleet's expected catch per hour, every "
       "filed rule applied, closes Brettach Bank")
    ts = truth_falls(T, "stock")
    ok(A.call(ts)["pick"] == HMD and A.call(ts)["margin"] >= 1.15, "R3b the decisive step alone on the clean truth (the "
       "true weight on each stock area) closes Halmorie Deep")
    tp = truth_falls(T, "plain")
    ok(A.call(tp)["pick"] == BRB, "R3b the lower rung on the clean truth (the stations' expected catches averaged "
       "plainly) leaves the call on Brettach Bank")
    for g in K.GROUND_NAMES:
        ys = [tuple(round(t["kg"], 1) for t in sorted(tw, key=lambda t: t["station"]) if t["ground"] == g and t["year"] == y)
              for y in K.YEARS]
        ok(len(set(ys)) == len(ys), "R3c no year's survey block copies another's: %s" % g)
    ok(len({round(T["dens"][(0, y)], 6) for y in K.YEARS}) == len(K.YEARS), "R3c no constant stream in the truth")

    # ---------------------------------------------------------------- the asks: devices, separation, the cracker
    aa, ab = A.ask_a(D), A.ask_b(D)
    notes = defaultdict(list)
    for r in D["notes"]:
        notes[r["note_no"]].append(r)
    valid = A.member_plns(D)
    member = lambda pln, day: any(a <= day and (b is None or day <= b) for a, b in valid.get(pln, []))
    import datetime as dt
    grp = defaultdict(list)
    for no, ls in notes.items():
        h = ls[0]
        grp[(h["buyer_reg"], h["vessel_pln"], h["landing_date"], h["port"])].append(no)
    sig = lambda n: tuple(sorted((l["species"], l["presentation"], l["grade"], l["boxes"], l["weight_kg"]) for l in notes[n]))
    reissued, sessions, lots = defaultdict(int), defaultdict(int), defaultdict(int)
    for (b, pln, day, port), nos in grp.items():
        if not ("2026-01-01" <= day <= "2026-09-30") or not member(pln, dt.date.fromisoformat(day)):
            continue
        sigs = [sig(n) for n in nos]
        if len(set(sigs)) < len(sigs):
            reissued[port] += 1
        if len(set(sigs)) > 1:
            sessions[port] += 1
    for no, ls in notes.items():
        h = ls[0]
        if "2026-01-01" <= h["landing_date"] <= "2026-09-30" and member(h["vessel_pln"], dt.date.fromisoformat(h["landing_date"])):
            ks = [(l["species"], l["presentation"], l["grade"], l["boxes"], l["weight_kg"]) for l in ls if l["species"] == "HAD"]
            if len(set(ks)) < len(ks):
                lots[h["port"]] += 1
    for p in K.PORT_NAMES:
        ok(2 <= reissued[p] <= 3, "Ask A %s: two or three corrected notes beside the notes they correct" % p)
        ok(sessions[p] >= 1, "Ask A %s: a member landing sold over two sessions to one buyer" % p)
        ok(lots[p] >= 1, "Ask A %s: identical haddock lots on one note" % p)
    for (b, pln, day, port), nos in grp.items():
        if len(nos) > 1:
            pairs = defaultdict(list)
            for n in nos:
                pairs[sig(n)].append(n)
            for s, ns in pairs.items():
                if len(ns) > 1:
                    pr = {tuple(l["price_per_kg"] for l in notes[n]) for n in ns}
                    ok(len(pr) == len(ns), "Ask A: a corrected note differs from the note it corrects in a price")
    hist = [h for h in D["history"] if h["Registered to"] is not None]
    ok(any(A._as_date(h["Registered to"]) == dt.date(2026, 5, 31) for h in hist), "Ask A: a member re-registered on 1 June 2026")
    for code in K.POOL_CODES:
        rows = [r for r in D["ledger"] if r["pool"] == code and r["type"] == "allocation"]
        lic = sum(float(r["tonnes"]) for r in rows if r["licence"])
        blank = [float(r["tonnes"]) for r in rows if not r["licence"]]
        ok(len(blank) == 1 and abs(blank[0] - lic) < 0.01, "Ask B %s: the pool's allocation posted beside its licences'" % code)
        ok(any(r["type"] == "carry_in" and not r["licence"] for r in D["ledger"] if r["pool"] == code),
           "Ask B %s: the carry-in booked to the pool" % code)
    ok(sum(1 for r in D["ledger"] if r["type"] == "swap") == 3, "Ask B: three pools' swaps booked at pool level")
    checks_a = {"plain": "the export as it stands (the cracker)", "session": "one note a buyer a landing",
                "lots": "identical lots collapsed"}
    for h, what in checks_a.items():
        a = A.ask_a(D, h)
        for p in K.PORT_NAMES:
            ok(round(a[p][0]) != round(aa[p][0]) and round(a[p][1]) != round(aa[p][1]),
               "Ask A %s: %s misses both figures" % (p, what))
    cur = A.ask_a(D, "current")
    ok(sum(round(cur[p][0]) != round(aa[p][0]) for p in K.PORT_NAMES) == 1, "Ask A: current letters only miss one port")
    for h, what in {"plain": "the ledger summed as it stands (the cracker)", "blank": "every blank-licence entry dropped",
                    "posted": "by posting date"}.items():
        b = A.ask_b(D, h)
        for p in K.POOL_CODES:
            ok(round(b[p]) != round(ab[p]), "Ask B %s: %s misses" % (p, what))
    bc = A.ask_b(D, "cancel")
    ok(sum(round(bc[p]) != round(ab[p]) for p in K.POOL_CODES) == 2, "Ask B: the cancelled lease read back moves two pools")
    for p in K.PORT_NAMES:
        ok(edge(aa[p][0]) >= 0.02 and edge(aa[p][1]) >= 0.02, "Ask A %s: tonnes and value away from their edges" % p)
        ok(fig["ask_a"][p] == {"tonnes": round(aa[p][0]), "value": round(aa[p][1])}, "figures.json Ask A %s" % p)
    for p in K.POOL_CODES:
        ok(edge(ab[p]) >= 0.02, "Ask B %s: quota left away from its tonne's edge" % p)
        ok(fig["ask_b"][p] == round(ab[p]), "figures.json Ask B %s" % p)
    # separation: the call never reads an ask file, and the asks never read the survey
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        for k in ("notes", "ledger", "factors"):
            open(os.path.join(tmp, K.FILES[k]), "w").write(open(os.path.join(target, K.FILES[k])).readline())
        D3 = A.load(tmp)
        ok(A.falls(A.survey_index(D3)) == G, "separation: the call computes identically with the ask files emptied")
        shutil.copy(os.path.join(target, K.FILES["notes"]), tmp)
        shutil.copy(os.path.join(target, K.FILES["ledger"]), tmp)
        shutil.copy(os.path.join(target, K.FILES["factors"]), tmp)
        open(os.path.join(tmp, K.FILES["survey"]), "w").write(open(os.path.join(target, K.FILES["survey"])).readline())
        D4 = A.load(tmp)
        ok(A.ask_a(D4) == aa and A.ask_b(D4) == ab, "separation: the asks compute identically with the survey emptied")
    finally:
        shutil.rmtree(tmp)
    for k in K.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in os.listdir(target):
                if f != K.FILES[k]:
                    shutil.copy(os.path.join(target, f), tmp)
            D5 = A.load(tmp)
            ok(A.falls(A.survey_index(D5)) == G and A.ask_a(D5) == aa and A.ask_b(D5) == ab,
               "distractor %s deleted: the call and every ask unchanged" % k)
        finally:
            shutil.rmtree(tmp)
    cr = subprocess.run([sys.executable, os.path.join(HERE, "cracker.py"), target], capture_output=True, text=True)
    ok(cr.returncode == 0, "the cracker's path misses every ask figure: " + cr.stdout[-400:])

    # ---------------------------------------------------------------- input gates and realism
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({os.path.splitext(f)[1] for f in files}) >= 3, "three or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "a 25,000-row file")
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(sorted(meta["distractor_files"]) == sorted("target/" + K.FILES[k] for k in K.DISTRACTORS), "metadata names the distractors")
    ok(not any("distractor" in f.lower() for f in files), "no file name says distractor")
    yrs = [sum(1 for r in D["elog"] if r["haul_start_utc"][:4] == str(y)) for y in K.ELOG_YEARS]
    ok(len(set(yrs)) == len(yrs), "the e-logbook's yearly counts vary")
    ok(len({round(aa[p][0]) for p in K.PORT_NAMES}) == 4 and all(round(aa[p][0]) % 100 for p in K.PORT_NAMES)
       and all(round(aa[p][1]) % 1000 for p in K.PORT_NAMES), "no round or repeated port totals")
    ok(all(round(ab[p]) % 100 for p in K.POOL_CODES), "no round pool totals")
    ok(all(abs(float(r["weight_kg"]) * float(r["price_per_kg"]) - float(r["value_gbp"])) < 0.006 for r in D["notes"]),
       "every note line's value is its weight times its price")
    listed = {l.split()[0] for l in open(os.path.join(target, K.FILES["contents"]), encoding="utf-8").read().splitlines()
              if l.split() and "." in l.split()[0] and l.split()[0] in files}
    ok(listed == set(files) - {K.FILES["contents"]}, "H9 the contents list names every shipped file but itself")
    from pypdf import PdfReader
    must = {"plan": ["the ground whose haddock stock in the year before that year has fallen furthest below its",
                     "the weight of haddock on its stock area", "the set of cells Annex A assigns to it"],
            "manual": ["twelve stations were placed in each depth band", "A station's depth band is the band the grid gives",
                       "A species not caught in a tow is recorded as zero"],
            "rules": ["with effect on or before that date"]}
    for k, sentences in must.items():
        path = os.path.join(target, K.FILES[k])
        strict = " ".join(" ".join((pg.extract_text() or "").split()) for pg in PdfReader(path, strict=True).pages)
        other = " ".join(subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.split())
        for t in sentences:
            ok(t in strict and t in other, "H25 %s reads the same under a strict parser and pdftotext: %r" % (K.FILES[k], t[:40]))
    names = set(K.GROUND_NAMES) | set(K.PORT_NAMES) | {"Dunvarra"}
    ok(len(names) == 11, "every invented place name distinct")
    print("checks: %d assertions passed" % N[0])
    return N[0]
