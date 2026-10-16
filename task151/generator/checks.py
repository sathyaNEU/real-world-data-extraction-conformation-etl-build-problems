"""task151 checks, run on every build: the input gates; the three-rules block (R1 the field's raw material, R2 every
mess item neutral, R3a the analyst test on the clean truth and the pack, R3b the decisive step alone, R3c no plant,
R3s the strict rule 3 test on every shipped sentence that bears on how the figure is computed); the bins and the
one-sigma test; every construction of the golden; the out-of-sample back-test; every rival by name; every semantic
fork row (SF1 to SF10) and closure axis (C1 to C22); both asks with every stop, hazard and the cracker's path; the
separation line and the distractors; the realism sweep; the goldens and the prompt. Any failure stops the build."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import defaultdict
from statistics import NormalDist

import numpy as np
import openpyxl

import calc
import common as K
import deliver as DL
import docs as DOC
import records as REC
import world as WD

NORM = NormalDist()
DASH = re.compile("[%s%s]" % (chr(0x2013), chr(0x2014)))
TASK = K.TASK
MAIN_FILES = [REC.F_LEGACY, REC.F_BAT, REC.F_XWALK, REC.F_CLUBS, REC.F_DC, REC.F_DC27, DOC.F_TERMS, DOC.F_FIN14,
              DOC.F_NOTES]
ASK_FILES = [REC.F_TRANS, REC.F_ILREP, DOC.F_ILRULES, REC.F_CAL, REC.F_PAY, REC.F_HRIS, REC.F_CODES, REC.F_REG]
DISTRACTORS = [REC.F_PROJ, REC.F_SCHED27]
METHOD = (r"per start|comparab|distribution|percentile|share of|simulat|resampl|bootstrap|regulars' seasons|"
          r"winter-planned|planned regulars")
SOFT = ("hitters with 81 or more starts", "hitters with 300 or more plate appearances")
GOLD_TOTAL = 4_250_000
GOLD_PER = {"P4": 500_000, "P1": 1_000_000, "P2": 600_000, "P3": 1_200_000, "P5": 900_000}
BIN = 250_000


class Checks:
    def __init__(self):
        self.res = []

    def __call__(self, label, ok, detail=""):
        self.res.append((label, bool(ok), detail))
        return ok

    def report(self):
        if os.environ.get("CHECKS_LABELS"):
            with open(os.environ["CHECKS_LABELS"], "w", encoding="utf-8") as fh:
                fh.writelines(("ok   " if ok else "FAIL ") + lab + "\n" for lab, ok, _ in self.res)
        bad = [r for r in self.res if not r[1]]
        for lab, ok, det in self.res:
            if not ok:
                print("FAIL %s %s" % (lab, str(det)[:900]))
        print("checks.py: %d assertions, %d failed" % (len(self.res), len(bad)))
        if bad:
            raise SystemExit(1)


# ---------------------------------------------------------------------------------------------------- readers
def pdf_text(path):
    out = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"], capture_output=True, check=True).stdout
    return re.sub(r"\s+", " ", out.decode("utf-8"))


def xlsx_strings(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    bits = []
    for ws in wb.worksheets:
        bits.append(ws.title)
        for row in ws.iter_rows(values_only=True):
            bits.extend(str(v) for v in row if isinstance(v, str))
    return " ".join(bits)


def docx_text(path):
    import docx
    d = docx.Document(path)
    bits = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            bits.extend(c.text for c in row.cells)
    return "\n".join(bits)


def shipped_text(target):
    """Every sentence and header the pack ships (the big record files by their header line)."""
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = pdf_text(p)
        elif f.endswith(".xlsx"):
            out[f] = xlsx_strings(p)
        elif f == DOC.F_NOTES or f == DOC.F_MANIFEST:
            out[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".json"):
            d = json.load(open(p, encoding="utf-8"))
            out[f] = " ".join("%s %s" % (k, v) for k, v in d.items() if k != "transactions") + " " + " ".join(
                sorted({t["type"] for t in d["transactions"]}))
        else:
            with open(p, encoding="utf-8", newline="") as fh:
                out[f] = fh.readline()
    return out


# ------------------------------------------------------------------------------------------------- the clean truth
def truth(L):
    """The world before any record is written: every planned regular's season of starts by the player's own key, the
    slot rates from every starter's line, the five's terms and slots as filed, and the vendor's projections."""
    starts = defaultdict(int)
    pa = defaultdict(int)
    sp, sn = defaultdict(int), defaultdict(int)
    for y in K.HIST:
        for ln in L.lines[y]:
            pa[(y, ln["key"])] += ln["pa"]
            if ln["seq"] == 0:
                starts[(y, ln["key"])] += 1
                sp[ln["slot"]] += ln["pa"]
                sn[ln["slot"]] += 1
    rate = {s: sp[s] / sn[s] for s in range(1, 10)}
    planned = [(y, k, pos, L.rosters[(y, c)]["slots"][pos]) for y in K.HIST for c in WD.CODES
               for pos, k in L.rosters[(y, c)]["starters"].items()]
    nc = [x for x in planned if x[2] != "C"]
    st = np.array([starts[(y, k)] for y, k, _, _ in nc], float)
    hv = REC.vendor_ids(L)
    proj = {(d["season"], d["k"]): d["pa"] for d in REC.projections(L, hv)}
    errs = np.array([pa[(y, k)] - proj[(y, k)] for y, k, _, _ in nc if (y, k) in proj and y <= 2026], float)
    return dict(starts=starts, pa=pa, rate=rate, st=st, nc=nc, proj=proj, errs=errs)


def truth_golden(Tr):
    per = {k: calc.ev(K.SIGNINGS[k]["bonus"], Tr["st"] * Tr["rate"][K.SIGNINGS[k]["slot"]]) for k in K.SIGN_ORDER}
    return per, sum(per.values())


def truth_default(Tr):
    sd = Tr["errs"].std()
    return sum(calc.ev_normal(K.SIGNINGS[k]["bonus"], Tr["proj"][(2027, k)], sd) for k in K.SIGN_ORDER)


def bins(a, b):
    return (a - b) / BIN


# ------------------------------------------------------------------------------------------------------ the checks
def run(target, golden, W, R, meta_path):
    C = Checks()
    L = W
    P, T, G, RV, A, B = R["P"], R["T"], R["G"], R["R"], R["A"], R["B"]
    F = G["five"]
    key_of = {L.players[k].name: k for k in K.SIGN_ORDER}
    files = sorted(os.listdir(target))
    texts = shipped_text(target)
    meta = json.load(open(meta_path, encoding="utf-8"))

    # ---- input gates
    rows = {f: (sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1)
            for f in files if f.endswith((".csv", ".txt")) and f != DOC.F_NOTES}
    C("G1 ten or more files", len(files) >= 10, len(files))
    C("G2 three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, sorted({f.rsplit(".", 1)[1] for f in files}))
    C("G3 a file of 25,000 rows or more", max(rows.values()) >= 25000, max(rows.values()))
    C("G4 two or more distractors, named only in metadata.json", sorted(meta["distractor_files"]) == sorted(DISTRACTORS)
      and not any("distract" in f for f in files))
    C("G5 every file has a source, date and licence", all(x.get("source") and x.get("date") and x.get("license")
                                                          for x in meta["files"]) and len(meta["files"]) == len(files))
    C("G6 no file is named after the stump", not any(re.search(r"issue|probab|regular|comparab|bonus_paid|stint", f)
                                                     for f in files), files)

    # ---- R1: the field's raw material
    heads = " ".join(texts[f] for f in files if f.endswith((".csv", ".txt")) and f != DOC.F_NOTES)
    C("R1a no shipped column holds a season's starts, a probability or plate appearances per start",
      not re.search(r"starts|games_started|\bGS\b|probab|per_start|pa_per", heads, re.I), heads[:300])
    C("R1b the golden reads every batting line and the vendor's winter lineups: %d lines, %d planned seasons"
      % (len(P.lines), G["n"]), len(P.lines) == sum(rows[f] for f in (REC.F_LEGACY, REC.F_BAT)) and G["n"] == 6 * 30 * 8)

    # ---- the golden itself
    C("M1 the accrual is $4,250,000 and each player's figure as filed", G["total_r"] == GOLD_TOTAL and
      {key_of[n]: v for n, v in G["per_r"].items()} == GOLD_PER, (G["total"], G["per"]))
    Tr = truth(L)
    tper, ttot = truth_golden(Tr)
    C("M2 the clean truth gives the same golden to the dollar", abs(ttot - G["total"]) < 0.5 and
      all(abs(tper[key_of[n]] - v) < 0.5 for n, v in G["per"].items()), (ttot, G["total"]))

    # ---- R2: every mess item neutral on the call
    for opt, what in (("no_ci", "legacy plate appearances without catcher's interference"),
                      ("dh_once", "doubleheaders merged into one start a date")):
        P2 = calc.load(target, mishandle=(opt,))
        G2 = calc.golden(P2)
        C("R2 %s leaves the call and every player figure" % what, G2["total_r"] == GOLD_TOTAL and
          G2["per_r"] == G["per_r"], (G2["total"], G2["per_r"]))
    st_ascii = np.array([T.starts[(r["season"], r["lg"])] for r in T.planned if r["pos"] != "C" and
                         calc.fold(r["name"]) == r["name"]], float)
    Ga = sum(calc.ev(f["lines"], st_ascii * G["rate"][f["slot"]]) for f in F)
    Gpa = {f["name"]: calc.r100(calc.ev(f["lines"], st_ascii * G["rate"][f["slot"]])) for f in F}
    C("R2 the vendor's accented names dropped (joined by name to the crosswalk) leaves the call",
      calc.r250(Ga) == GOLD_TOTAL and Gpa == G["per_r"], (Ga, Gpa))
    inv = {v: k for k, v in REC.VENDOR_CLUB.items()}
    club_st = defaultdict(int)
    for (y, g, d, club, pid, slot, stt, pa, pos) in P.lines:
        if stt:
            club_st[(y, pid, club)] += 1
    st_club = np.array([club_st[(r["season"], r["lg"], inv.get(r["team"], r["team"]))] for r in T.planned
                        if r["pos"] != "C"], float)
    Gc = sum(calc.ev(f["lines"], st_club * G["rate"][f["slot"]]) for f in F)
    C("R2 traded regulars' seasons cut to the planning club leaves the call", calc.r250(Gc) == GOLD_TOTAL, Gc)
    d_legacy = sum(1 for r in csv.DictReader(open(os.path.join(target, REC.F_LEGACY), encoding="utf-8"), delimiter="|")
                   if r["COMPL_DT"])
    C("R2 suspended games are one game each, under the date they began (%d legacy lines)" % d_legacy, d_legacy > 0)

    # ---- R3a: the analyst test
    tdef = truth_default(Tr)
    pdef = RV["default: vendor projection with a normal band"]
    C("R3a the easy route on the clean truth (the vendor's projection with a normal band from its past misses) files "
      "%s, %.1f bins from the golden" % (K.money(calc.r250(tdef)), bins(tdef, ttot)), calc.r250(tdef) != GOLD_TOTAL
      and abs(tdef - ttot) >= BIN, tdef)
    C("R3a the same route on the pack files the same rounded figure", calc.r250(pdef) == calc.r250(tdef), (pdef, tdef))
    at_hand = ("default: vendor projection with a normal band", "own three seasons as the draws",
               "the full nine's own plate appearances")
    pick = min(at_hand, key=lambda n: R["LB"][n])
    C("R3a the default path: FIN-14 4.4 run on the bases at hand (the vendor's projection with its band, the players' "
      "own seasons, the starting nines' seasons taken whole) keeps '%s' and files %s, %.2f bins from the golden" % (
          pick, K.money(calc.r250(RV[pick])), bins(RV[pick], G["total"])),
      pick == "the full nine's own plate appearances" and abs(RV[pick] - G["total"]) >= BIN and
      calc.r250(RV[pick]) != GOLD_TOTAL, (pick, RV[pick]))
    # ---- R3b: the decisive step alone; each lower correction stays wrong
    st = G["starts"]
    rt = G["rate"]
    alone = sum(calc.ev(f["lines"], st * rt[f["slot"]]) for f in F)
    C("R3b the easy route with only the decisive step changed files the golden", calc.r250(alone) == GOLD_TOTAL)
    for nm in ("new slot, normal band", "regulars at the old slot's rate",
               "vendor projection rescaled to the new slot, normal band", "opening-day lineups", "catchers kept in",
               "planned regulars who opened the season"):
        C("R3b one correction short (%s) misses by %.2f bins" % (nm, bins(RV[nm], G["total"])),
          abs(RV[nm] - G["total"]) >= BIN and calc.r250(RV[nm]) != GOLD_TOTAL, RV[nm])
    # ---- R3c: no plant
    lineups = defaultdict(list)
    for (y, g, d, club, pid, slot, stt, pa, pos) in P.lines:
        if stt:
            lineups[(y, club)].append((slot, pid))
    sigs = [tuple(sorted(v)) for v in lineups.values()]
    C("R3c no copied or repeated block: no two club-seasons share a lineup history", len(set(sigs)) == len(sigs))
    lines_per = [sum(1 for x in P.lines if x[0] == y) for y in K.HIST]
    C("R3c no season's line count repeats", len(set(lines_per)) == len(lines_per), lines_per)
    memo_like = [f for f in files if re.search(r"memo|email|draft|estimate|note_to", f)]
    C("R3c no memo, draft, estimate or stakeholder figure ships", not memo_like and not re.search(
        r"accru\w* (of|at) \$|\$[\d,]+ (accrual|accrued)", " ".join(texts.values()), re.I), memo_like)
    # ---- R3s: every shipped sentence that bears on how the figure is computed, executed literally
    fin = texts[DOC.F_FIN14]
    terms = texts[DOC.F_TERMS]
    how = fin + " " + terms + " " + texts[REC.F_DC27] + " " + texts[DOC.F_NOTES] + " " + texts[REC.F_DC]
    C("R3s no shipped sentence names a distribution, a comparison set, a rate per start or how starts are lost",
      not re.search(METHOD, how, re.I), re.findall(r".{40}(?:%s).{40}" % METHOD, how, re.I)[:3])
    C("R3s FIN-14 fixes the estimand (4.2, 4.3) and the selection criterion (4.4), and names no basis",
      "multiplied by the probability" in fin and "the contract stands as signed through the season" in fin and
      "The Club uses the basis with the lowest average" in fin and not re.search(
          r"projection|past seasons|player's record|regress|comparab|lineup slot|batting order|per start|catch|"
          r"\bstarts\b|\bslot", fin, re.I), re.findall(r".{30}(?:projection|regress|comparab|slot|catch).{30}", fin, re.I))
    vp = RV["vendor point"]
    C("R3s the literal combination with the field's ready projection (each bonus counted if the vendor's projection "
      "reaches it) files %s, not the golden" % K.money(calc.r250(vp)), abs(vp - G["total"]) >= BIN, vp)

    # ---- bins, one sigma, constructions
    off = G["total"] - G["total_r"]
    C("L1 the accrual sits mid-bin: %s from the centre of its $250,000 bin" % K.money(off), abs(off) <= 40000, off)
    offs = {n: v - G["per_r"][n] for n, v in G["per"].items()}
    C("L2 each player's accrual sits within $35,000 of its $100,000 centre", all(abs(v) <= 35000 for v in offs.values()),
      offs)
    sd, sdp = calc.bootstrap(P, T, n=300)
    C("L3 one bootstrap sigma (%s) keeps the rounded accrual" % K.money(sd), calc.r250(G["total"] - sd) == GOLD_TOTAL and
      calc.r250(G["total"] + sd) == GOLD_TOTAL, sd)
    C("L3 one sigma keeps every player's rounded figure", all(calc.r100(G["per"][n] - sdp[n]) == G["per_r"][n] and
                                                             calc.r100(G["per"][n] + sdp[n]) == G["per_r"][n] for n in sdp), sdp)
    CN, _ = calc.constructions(P, T)
    for nm, d in CN.items():
        tot = sum(d.values())
        if nm in SOFT:
            C("L4s loose regular set '%s' rounds alike (%s)" % (nm, K.money(round(tot))), calc.r250(tot) == GOLD_TOTAL
              and {n: calc.r100(v) for n, v in d.items()} == G["per_r"], tot)
            continue
        C("L4 construction '%s' rounds alike (%s, players %s)" % (nm, K.money(calc.r250(tot)), "same" if
          {n: calc.r100(v) for n, v in d.items()} == G["per_r"] else "differ"),
          calc.r250(tot) == GOLD_TOTAL and {n: calc.r100(v) for n, v in d.items()} == G["per_r"] and
          abs(tot - G["total_r"]) <= BIN / 2 - 10000, (tot, {n: round(v) for n, v in d.items()}))
    gt = sum(1 for (a, t, p) in [x for f in F for x in G["lines"][f["name"]]])
    strict = sum(calc.ev([(a, t + 1e-9) for a, t in f["lines"]], st * rt[f["slot"]]) for f in F)
    C("C9 a line reached at exactly its threshold: strict and inclusive readings round alike",
      calc.r250(strict) == GOLD_TOTAL and gt == 15)
    for nm, v in sorted(RV.items()):
        C("L5 rival '%s' misses by %.2f bins (%s)" % (nm, bins(v, G["total"]), K.money(calc.r250(v))),
          abs(v - G["total"]) >= BIN, v)
    C("L6 rivals on both sides of the golden", any(v < G["total"] - BIN for v in RV.values()) and
      any(v > G["total"] + BIN for v in RV.values()))
    # ---- the filed look-back (FIN-14 4.4) executed: the selection criterion ranks the bases
    LB, n_lb = R["LB"], R["n_lb"]
    gb = LB["golden"]
    acc = R["ACC"]
    win = min(LB, key=LB.get)
    proj_all = calc.projections(P)
    missing = [(y, r["lg"]) for y in calc.LB_SEASONS for r in T.planned if r["season"] == y and all(
        T.pa[(y - j, r["lg"])] >= calc.LB_MIN_PA for j in (1, 2)) and (y, r["lg"]) not in proj_all]
    C("LB0 FIN-14 4.4's hitters: %d hitter-seasons 2023 to 2026, every one with the vendor's projection" % n_lb,
      n_lb > 600 and not missing, missing[:3])
    C("LB1 the look-back's lowest score is a construction of the golden ('%s', %.5f; the golden basis %.5f)" % (
        win, LB[win], gb), win in calc.FAMILY, (win, LB[win]))
    for nm in calc.FAMILY + calc.LANDS:
        tot = sum(acc[nm].values())
        C("LB2 '%s' files the golden at the signings (%s, players %s)" % (nm, K.money(round(tot)), "same" if {
            n: calc.r100(v) for n, v in acc[nm].items()} == G["per_r"] else "differ"), calc.r250(tot) == GOLD_TOTAL
          and {n: calc.r100(v) for n, v in acc[nm].items()} == G["per_r"], (tot, acc[nm]))
    for nm in calc.FAMILY:
        C("LB2b '%s' ties the golden basis in the look-back (%+.2f per cent)" % (nm, 100 * (LB[nm] - gb) / gb),
          abs(LB[nm] - gb) / gb < 0.0025)
    for nm, sc in sorted(LB.items()):
        if nm not in calc.FAMILY:
            C("LB3 '%s' loses the look-back by %.2f per cent" % (nm, 100 * (sc - gb) / gb), sc > gb * 1.001, sc)
    floors = {"default: vendor projection with a normal band": 0.10, "vendor projection with its past misses": 0.10,
              "own three seasons as the draws": 0.10, "own seasons since 2021": 0.10, "opening-day lineups": 0.01,
              "planned regulars who opened the season": 0.01, "the full nine's own plate appearances": 0.10,
              "catchers kept in": 0.05, "planned regulars' own plate appearances": 0.03}
    for nm, m in floors.items():
        C("LB4 a visible margin: '%s' scores %.1f per cent above the golden basis (floor %d)" % (
            nm, 100 * (LB[nm] - gb) / gb, round(100 * m)), LB[nm] >= gb * (1 + m), LB[nm])
    C("LB5 weight on the player's record or the vendor's projection only worsens the score, more weight more so",
      gb < LB["own record given a weight of 2 per cent"] < LB["own record given a weight of 5 per cent"] <
      LB["own record given a weight of 10 per cent"] and gb < LB["vendor projection given a weight of 2 per cent"] <
      LB["vendor projection given a weight of 5 per cent"] < LB["vendor projection given a weight of 10 per cent"] and
      gb < LB["own seasons blended in at 5 per cent"] < LB["own seasons blended in at 10 per cent"])
    for nm, v in sorted(R["NEAR"].items()):
        C("LB6 near route '%s' (%+.2f bins, %s) loses the look-back by %.2f per cent" % (
            nm, bins(v, G["total"]), K.money(calc.r250(v)), 100 * (LB[nm] - gb) / gb), LB[nm] > gb * 1.001, (v, LB[nm]))
    lit = RV["the look-back's own hitters' seasons"]
    C("LB7 FIN-14 4.4 executed word for word as a basis (its own hitters' seasons) files %s, %.2f bins away: the "
      "criterion ranks bases, it is not one" % (K.money(calc.r250(lit)), bins(lit, G["total"])),
      abs(lit - G["total"]) >= BIN and calc.r250(lit) != GOLD_TOTAL, lit)
    for nm in ("the full nine's own plate appearances", "the full nine's own plate appearances, 2022-2026",
               "the full nine's own plate appearances, 2024-2026"):
        C("LB8 the audit's route '%s' misses by %.2f bins (one-bin rule)" % (nm, bins(RV[nm], G["total"])),
          abs(RV[nm] - G["total"]) >= BIN and calc.r250(RV[nm]) != GOLD_TOTAL, RV[nm])

    # ---- the out-of-sample back-test (fitted on 2021-2023, scored on the 2024-2026 planned regulars)
    train = [r for r in T.planned if r["pos"] != "C" and r["season"] <= 2023]
    test = [r for r in T.planned if r["pos"] != "C" and r["season"] >= 2024]
    rt3 = calc.rate(T, [2021, 2022, 2023])
    st_tr = np.array([T.starts[(r["season"], r["lg"])] for r in train], float)
    m3, s3 = st_tr.mean(), st_tr.std()
    pa_te = np.array([T.pa[(r["season"], r["lg"])] for r in test], float)
    proj = {(int(r["season"]), int(r["lg_id"])): int(r["pa"]) for r in P.proj}
    e_tr = np.array([T.pa[(r["season"], r["lg"])] - proj[(r["season"], r["lg"])] for r in train
                     if (r["season"], r["lg"]) in proj], float)
    sdv = e_tr.std()
    zs = {"season distribution at the slot": [], "normal band at the slot": [], "vendor projection with a band": []}
    for Tt in (500, 550, 600):
        act = float(np.mean(pa_te >= Tt))
        se = np.sqrt(act * (1 - act) / len(test))
        zs["season distribution at the slot"].append(
            (np.mean([np.mean(st_tr * rt3[r["ord"]] >= Tt) for r in test]) - act) / se)
        zs["normal band at the slot"].append(
            (np.mean([1 - NORM.cdf((Tt - rt3[r["ord"]] * m3) / (rt3[r["ord"]] * s3)) for r in test]) - act) / se)
        ok = [i for i, r in enumerate(test) if (r["season"], r["lg"]) in proj]
        act_v = float(np.mean(pa_te[ok] >= Tt))
        zs["vendor projection with a band"].append(
            (np.mean([1 - NORM.cdf((Tt - proj[(test[i]["season"], test[i]["lg"])]) / sdv) for i in ok]) - act_v) / se)
    C("BT1 back-tested on 2024-2026 from 2021-2023, the season distribution at the slot predicts the share reaching "
      "500, 550 and 600 within 2 standard errors", all(abs(z) < 2 for z in zs["season distribution at the slot"]),
      zs["season distribution at the slot"])
    C("BT2 the normal band at the slot misses by more than 3 standard errors at 550 and 600",
      all(abs(z) > 3 for z in zs["normal band at the slot"][1:]), zs["normal band at the slot"])
    C("BT3 the vendor's projection with its error band misses by more than 5 standard errors at every line",
      all(abs(z) > 5 for z in zs["vendor projection with a band"]), zs["vendor projection with a band"])
    by_slot = {}
    for s in (1, 2, 3, 7, 8, 9):
        by_slot[s] = rt[s]
    yr = {y: calc.rate(T, [y]) for y in K.HIST}
    C("BT4 plate appearances per start fall down the order in every season (first above fourth above seventh above "
      "ninth by at least 0.25 each)", all(yr[y][1] - yr[y][4] > 0.25 and yr[y][4] - yr[y][7] > 0.25 and
                                          yr[y][7] - yr[y][9] > 0.15 for y in K.HIST), {y: (round(yr[y][1], 2), round(yr[y][9], 2)) for y in K.HIST})
    corr = []
    plan_keys = {(r["season"], r["lg"]) for r in T.planned if r["pos"] != "C"}
    for (y, lg) in plan_keys:
        if (y - 1, lg) in plan_keys:
            corr.append((T.starts[(y - 1, lg)], T.starts[(y, lg)]))
    rho = float(np.corrcoef(np.array(corr).T)[0, 1])
    C("BT5 a planned regular's starts in one season say nothing about the next (correlation %.3f over %d pairs)"
      % (rho, len(corr)), abs(rho) < 0.08 and len(corr) > 500, rho)
    od_share = 1 - np.mean([(r["season"], r["lg"]) in T.opening for r in T.planned if r["pos"] != "C"])
    C("BT7 about one in six winter-planned regulars missed his club's first game (%.3f)" % od_share,
      0.14 < od_share < 0.21, od_share)

    # ---- the semantic fork rows
    tx = json.load(open(os.path.join(target, REC.F_TRANS), encoding="utf-8"))["transactions"]
    last_line = max(x[2] for x in P.lines)
    C("SF1 nothing after the signings bears on the five: no batting line after the 2026 season, no move for them after "
      "the November reinstatement, depth chart dated December 10", last_line <= K.SEASON[2026][1] and not any(
          t["date"] > "2026-11-23" for t in tx if t["player_id"] in {f["lg"] for f in F}) and
      "December 10, 2026" in texts[REC.F_DC27])
    C("SF2 the term sheets carry fifteen plate-appearance bonus lines and no other bonus for the five",
      sum(len(f["lines"]) for f in F) == 15 and not re.search(r"innings|games started|award|All-Star", terms))
    C("SF3 the batting lines are championship-season games only", all(
        K.SEASON[x[0]][0] <= x[2] <= K.SEASON[x[0]][1] for x in P.lines))
    C("SF4 the multi-year term sheets state no plate-appearance bonus in later seasons",
      terms.count("No plate-appearance bonuses in later seasons") == 4)
    C("SF5 the expected amount and the amount at the expected season differ by more than a bin",
      abs(RV["new slot at the mean starts"] - G["total"]) >= BIN and abs(RV["new slot at the median starts"] -
                                                                         G["total"]) >= BIN)
    C("SF6 FIN-14 4.3 takes the contract as standing all season and leaves the player's health in the probability",
      "the player is not traded or released and the contract is not renegotiated" in fin and
      "is part of the probability" in fin)
    for nm in ("every game started", "seasons with no injured-list stint, 2024-2026"):
        C("SF6b the reading of 4.3 with the player kept healthy ('%s') files %s, %.1f bins from the golden" % (
            nm, K.money(calc.r250(RV[nm])), bins(RV[nm], G["total"])), abs(RV[nm] - G["total"]) >= BIN and
          calc.r250(RV[nm]) != GOLD_TOTAL, RV[nm])
    C("SF7 the role is the depth chart's: the five bat fifth to ninth", [f["slot"] for f in F] == [5, 6, 7, 8, 9] and
      "the role the Club plans for him at the date of signing" in fin)
    alt = sum(G["per_r"].values())
    C("SF8 one rounding path: FIN-14 6 rounds the total from the unrounded amounts (%s); the rounded player figures "
      "add to %s, which is not the total" % (K.money(GOLD_TOTAL), K.money(alt)), "a total is the sum of the unrounded "
      "amounts, rounded only where it is reported" in fin and calc.r250(G["total"]) == GOLD_TOTAL and alt != GOLD_TOTAL,
      alt)
    memo = docx_text(os.path.join(golden, DL.F_MEMO))
    C("SF9 the memo carries the workbook's figures", K.money(GOLD_TOTAL) in memo and all(
        K.money(v) in memo for v in G["per_r"].values()))
    stamps = {os.path.getmtime(os.path.join(target, f)) for f in files}
    C("SF10 every file is stamped with the pull of December 11, 2026", stamps == {K.PULL_STAMP.timestamp()})

    # ---- the look-back's own terms (FIN-14 4.4): every reading ranks a construction of the golden first
    pool = list(calc.FAMILY) + ["default: vendor projection with a normal band", "own three seasons as the draws",
                                "the full nine's own plate appearances", "catchers kept in",
                                "planned regulars' own plate appearances", "opening-day lineups",
                                "own record given a weight of 5 per cent", "regression on the projection, the slot and catching"]
    for sid, what, kw in (("SF11", "the seasons read as 2024 to 2026 only", dict(seasons_=(2024, 2025, 2026))),
                          ("SF11", "the seasons read as 2023 to 2025 only", dict(seasons_=(2023, 2024, 2025))),
                          ("SF12", "the starting lineups without their catchers", dict(tests_nc=True)),
                          ("SF13", "the 100 plate appearances counted with the planning club only", dict(est_club=True)),
                          ("SF14", "a threshold reached only when passed", dict(strict=True))):
        LBx, nx, _ = calc.lookback(P, T, names=pool, **kw)
        wx = min(LBx, key=LBx.get)
        C("%s same call: the look-back with %s (%d hitter-seasons) still ranks a construction of the golden first ('%s')"
          % (sid, what, nx, wx), wx in calc.FAMILY, (wx, LBx))

    # ---- the closure axes
    C("C1 population: five term sheets, fifteen lines", len(F) == 5 and sum(len(f["lines"]) for f in F) == 15)
    C("C2 unit: whole US dollars on every line", all(a % 1000 == 0 for f in F for a, _ in f["lines"]))
    C("C3 window: the 2027 championship season on every term sheet", terms.count("2027 season:") == 5)
    C("C4 as-of: assessed at signing (FIN-14 4.2) and pulled December 11, 2026",
      "assessed at the date the contract is signed" in fin and "2026-12-11" in texts[DOC.F_MANIFEST])
    C("C5 version basis: one term sheet a player and one 2027 depth chart",
      len(P.terms) == 5 and sum(1 for f in files if "depth_chart_2027" in f) == 1)
    C("C6 denominator: every construction rounds alike (L4)", all(r[1] for r in C.res if r[0].startswith("L4")))
    C("C7 weighting: the age-matched sets round alike (L4)", any(r[0].startswith("L4 construction 'ages") for r in C.res))
    C("C8 window length: every history window rounds alike (L4)", any(r[0].startswith("L4 construction 'seasons from")
                                                                      for r in C.res))
    C("C10 rounding path: the total from the unrounded amounts (SF8)", G["total_r"] == calc.r250(sum(G["per"].values())))
    C("C11 tie-break: no two of the five share a slot", len({f["slot"] for f in F}) == 5)
    games = defaultdict(set)
    for (y, g, d, club, pid, slot, stt, pa, pos) in P.lines:
        games[(y, club)].add(g)
    C("C12 maturity: every club played 162 games in every season", all(len(v) == 162 for v in games.values()) and
      len(games) == 180)
    rl = sum(round(a * p, 2) for f in F for a, t, p in G["lines"][f["name"]])
    C("C13 order of operations: line amounts rounded to cents first give the same total", calc.r250(rl) == GOLD_TOTAL)
    P.lines.reverse()
    Grev = calc.golden(P)
    P.lines.reverse()
    C("C14 row order: the lines read in reverse give the same golden", abs(Grev["total"] - G["total"]) < 0.01)
    keyset = [(x[1], x[4]) for x in P.lines]
    C("C15 duplicates: one line per player per game in both layouts", len(set(keyset)) == len(keyset))
    leg = {r["PLAYER_CD"] for r in csv.DictReader(open(os.path.join(target, REC.F_LEGACY), encoding="utf-8"),
                                                  delimiter="|")}
    C("C16 identity: every legacy code is in the crosswalk and every planned regular is a League ID",
      leg <= set(P.legacy_to_id) and all(r["lg"] >= 600000 for r in T.planned))
    C("C17 netting: no negative count in either layout", all(x[7] >= 0 for x in P.lines))
    bad_pa = 0
    for r in csv.DictReader(open(os.path.join(target, REC.F_BAT), encoding="utf-8")):
        if int(r["pa"]) != sum(int(r[c]) for c in ("ab", "bb", "hbp", "sac_bunts", "sac_flies", "catchers_interference")):
            bad_pa += 1
    C("C18 units: platform plate appearances equal their components", bad_pa == 0, bad_pa)
    nst = defaultdict(int)
    for (y, g, d, club, pid, slot, stt, pa, pos) in P.lines:
        if stt:
            nst[(g, club)] += 1
    C("C19 codes: nine starters per club per game in both layouts", set(nst.values()) == {9})
    C("C20 integerisation: the prompt's rounding (L1, L2)", G["total_r"] % BIN == 0)
    C("C21 clause scope: FIN-14 4.1 lists plate appearances", "plate appearances, games played" in fin)
    sched = list(csv.DictReader(open(os.path.join(target, REC.F_SCHED27), encoding="utf-8")))
    cnt = defaultdict(int)
    for r in sched:
        cnt[r["home"]] += 1
        cnt[r["away"]] += 1
    C("C22 forward window: 162 games a club in 2027 and nine in the club's lineup", set(cnt.values()) == {162} and
      len(P.lineup27) == 9)

    # ---- Ask A: injured-list stints
    rep = list(csv.DictReader(open(os.path.join(target, REC.F_ILREP), encoding="utf-8")))
    C("A1 nine stints since Opening Day 2024, each with its date and days", len(A) == 9 and all(a["days"] > 0 for a in A),
      [(a["player"], str(a["eff"]), a["days"]) for a in A])
    true_eff = sorted((s["eff"], L.players[s["key"]].name) for s in L.stints if s["key"] in K.SIGN_ORDER and
                      s["season"] >= 2024)
    C("A2 the golden dates are the dates the stints took effect", [(a["eff"], a["player"]) for a in A] == true_eff)
    for mode, what in (("move", "the move's date as the date it took effect"), ("split", "every placement a stint"),
                       ("merge", "stints a week apart merged"), ("by_name", "the moves found by name")):
        S2 = calc.ask_a(P, mode)
        hit = sum(1 for a in A for s in S2 if s["player"] == a["player"] and s["eff"] == a["eff"]) + sum(
            1 for a in A for s in S2 if s["player"] == a["player"] and s["eff"] == a["eff"] and s["days"] == a["days"])
        C("A3 stop '%s' (%d rows) misses the golden's rows" % (what, len(S2)), len(S2) != 9 or hit == 0,
          [(s["player"], str(s["eff"]), s["days"]) for s in S2])
    mv = calc.ask_a(P, "move")
    C("A3b the move-date path misses all 18 figures", sum(1 for a, s in zip(A, mv) if a["eff"] == s["eff"]) == 0 and
      sum(1 for a, s in zip(A, mv) if a["days"] == s["days"]) == 0)
    hp = [a for a in A if a["player"] == L.players["P5"].name and a["eff"].year == 2025][0]
    sp = [s_ for s_ in L.stints if s_["key"] == "P5" and s_["season"] == 2025][0]
    C("HA1 the spring placement took effect before Opening Day; its days run from Opening Day",
      hp["eff"] < K.SEASON[2025][0] and hp["days"] == (sp["reinst"] - K.SEASON[2025][0]).days, (hp, sp["reinst"]))
    rules = texts[DOC.F_ILRULES]
    C("HA7 the rules date a placement from the day it takes effect, up to three days before its transaction",
      "may be up to three days before the date of the transaction" in rules and "after his placement takes effect" in
      rules and "the date of the transaction that placed him on it" in rules)
    op = [a for a in A if a["player"] == L.players["P4"].name and a["eff"].year == 2026][0]
    C("HA2 the stint open at the 2026 season's end runs through the last scheduled day",
      op["days"] == (K.SEASON[2026][1] - op["eff"]).days + 1 and any(
          t["type"] == "IL_REINSTATEMENT" and t["player_id"] == key_lg(F, op["player"]) for t in tx))
    rehab = [t for t in tx if t["type"] == "REHAB_ASSIGNMENT" and t["player_id"] in {f["lg"] for f in F}]
    C("HA3 two of the stints carry a rehabilitation assignment inside them", len(rehab) == 2)
    pat = [t for t in tx if t["type"] == "LIST_PLACEMENT" and t["player_id"] in {f["lg"] for f in F}]
    C("HA4 the paternity list is not a stint", len(pat) == 1 and "paternity" in pat[0]["description"])
    C("HA5 the 7-day concussion list is a stint", any(a["player"] == L.players["P5"].name and a["eff"].year == 2024
                                                      for a in A))
    trade = [t for t in tx if t["type"] == "TRADE" and t["player_id"] == key_lg(F, L.players["P2"].name)]
    C("HA6 a trade while on the list continues the stint", len(trade) == 1 and sum(
        1 for a in A if a["player"] == L.players["P2"].name and a["eff"].year == 2026) == 1)
    true_by = {(REC.report_name(L.players[s["key"]].name), s["eff"]) for s in L.stints}
    derived = {(r["player"], calc.mdy(r["eligible"]) - dt.timedelta(days=calc.MIN_DAYS[r["injured_list"]])) for r in rep}
    C("A4 fair: every report row's first date of reinstatement less the list's minimum is the true date the stint took "
      "effect (%d rows, %d stints)" % (len(rep), len(derived)), derived <= true_by, sorted(derived - true_by)[:5])
    rows5 = [r for r in rep if r["player"] in {calc.report_name(f["name"]) for f in F} and not r["pos"].endswith("HP")]
    placed5 = {(r["player"], calc.mdy(r["placed"])) for r in rows5}
    feed5 = {(calc.report_name(t["player"]), calc.ymd(t["date"])) for t in tx if t["type"] == "IL_PLACEMENT" and
             t["player_id"] in {f["lg"] for f in F}}
    C("A5 the report's placement dates are the feed's transaction dates (both sources agree on the move)",
      placed5 <= feed5 and len(feed5) == 11)
    early = [r for r in rep if calc.mdy(r["placed"]) > calc.ymd(r["report_date"])]
    C("A6 no report lists a placement before its transaction", not early, early[:3])
    twin = [t for t in tx if t["player"] == L.players["P1"].name and t["player_id"] != key_lg(F, L.players["P1"].name)]
    C("A7 a pitcher shares one signing's name; the feed tells them apart only by ID and position", len(twin) >= 4)

    # ---- Ask B: plate-appearance bonuses paid
    BT = calc.ask_b_totals(B)
    C("B1 paid for 2024, 2025, 2026: $325,000, $900,000, $412,500", {y: round(v) for y, v in BT.items()} ==
      {2024: 325000, 2025: 900000, 2026: 412500}, BT)
    notes = texts[REC.F_REG]
    C("B1b the register's notes file the population, the season, the reissue and the legacy code",
      "was paid to a player under a contract in this register that carries plate-appearance terms" in notes and
      "Both halves are the bonus of the season in which it was earned" in notes and
      "is one payment" in notes and "one E40 line can carry more than one bonus" in notes)
    for mode in ("face", "code_payyear", "code_season", "register", "gross", "payyear", "five"):
        B2 = calc.ask_b(P, mode)
        T2 = calc.ask_b_totals(B2)
        same = sum(1 for k2, v in B.items() if abs(B2.get(k2, 0) - v) < 0.5) + sum(
            1 for y in BT if abs(T2.get(y, 0) - BT[y]) < 0.5)
        C("B2 stop '%s' misses (totals %s)" % (mode, {y: round(v) for y, v in sorted(T2.items())}),
          any(abs(T2.get(y, 0) - BT[y]) >= 0.5 for y in BT), (same, T2))
    pay = list(csv.DictReader(open(os.path.join(target, REC.F_PAY), encoding="utf-8")))
    e40 = [r for r in pay if r["earning_code"] == "E40" and r["pay_date"] == "2024-10-15"]
    expect = {}
    for b in REC.vet_bonuses(L):
        if b["club"] == K.CLUB:
            expect[(b["k"], b["season"])] = expect.get((b["k"], b["season"]), 0) + b["amount"]
    star = {(k, y): dict(REC.VET_CONTRACTS[k]["awards"])[a] for (k, y), a in REC.AWARDS_WON.items()
            if "All-Star" in a and y == 2024 and (k, y) in expect}
    want_e40 = sorted(expect[(k, y)] / 2 + star.get((k, y), 0) for (k, y) in expect if y == 2024)
    C("B3 the legacy season-end lines hold each 2024 first half (%d of them carrying the season's All-Star bonus)" %
      len(star), sorted(float(r["amount"]) for r in e40) == want_e40 and len(star) == 1, (sorted(
          float(r["amount"]) for r in e40), want_e40))
    pt_lines = [r for r in pay if r["earning_code"] in ("BPA", "E40") and r["status"] == "PAID" and
                float(r["amount"]) > 0 and r["pay_date"][5:7] in ("10", "01") and r["pay_date"] >= "2024-10-01"]
    def legacy_or_hris(k):
        return {REC.hris_name(L.players[k].name), REC.legacy_name(L.players[k].name)}
    ok_lines = 0
    for (k, y), amt in expect.items():
        for r in pt_lines:
            if r["employee_name"] in legacy_or_hris(k):
                d = calc.ymd(r["pay_date"])
                season = d.year if d.month >= 7 else d.year - 1
                extra = star.get((k, y), 0) if d.month == 10 else 0
                if season == y and abs(float(r["amount"]) - amt / 2 - extra) < 0.5:
                    ok_lines += 1
    n_halves = sum(1 + (y <= 2025) for (k, y) in expect if 2024 <= y <= 2026)
    C("B3c every 2024-2026 playing-time line is half the season's plate-appearance and games-started lines reached for "
      "the club (the legacy October 2024 line to one player also carries his All-Star bonus): %d lines" % ok_lines,
      ok_lines == len([r for r in pt_lines if any(r["employee_name"] in legacy_or_hris(k) for k in REC.VET_CONTRACTS)])
      and ok_lines == n_halves, (ok_lines, n_halves))
    codes = list(csv.DictReader(open(os.path.join(target, REC.F_CODES), encoding="utf-8")))
    C("B3b the legacy performance-bonus code migrated as other bonus", any(r["earning_code"] == "E40" and
                                                                           r["migrated_as"] == "BOT" for r in codes))
    pt = [r for r in pay if r["earning_code"] == "BPA" and r["employee_name"] in
          {REC.hris_name(L.players[k].name) for k in REC.pitcher_bonus_rows(L)}]
    C("B4 the playing-time code also carries two pitchers' bonuses", len(pt) == 2)
    reg = calc.ask_b(P, "register")
    v4 = REC.hris_name(L.players["V4"].name)
    a4, l4 = REC.VET_CONTRACTS["V4"]["pa"]
    with_club = sum(a4 for b in REC.vet_bonuses(L) if b["k"] == "V4" and b["kind"] == "PA" and b["club"] == K.CLUB)
    C("B5 the assigned contract's later lines were not the club's to pay (register reading %s, paid %s)" % (
        K.money(reg[(2025, v4)]), K.money(B.get((2025, v4), 0))), reg[(2025, v4)] > B.get((2025, v4), 0) and
      abs(B.get((2025, v4), 0) - with_club) < 0.5 and with_club > 0, (reg[(2025, v4)], B.get((2025, v4)), with_club))
    C("B6 the 2026 second halves are not paid by December 11, 2026", not any(r["pay_date"] > "2026-12-11" for r in pay)
      and not any(r["pay_date"].startswith("2027") for r in pay))
    void = [r for r in pay if r["status"] in ("VOIDED", "VOID REVERSAL")]
    C("B7 one void and reissue nets to one payment", len(void) == 2 and sum(float(r["amount"]) for r in void) == 0)
    hm = {r["legacy_employee_no"] for r in csv.DictReader(open(os.path.join(target, REC.F_HRIS), encoding="utf-8"))}
    C("B8 every legacy employee number in the payroll is in the HRIS map", {
        r["employee_id"] for r in pay if r["pay_date"] < "2025-01-01"} <= hm)

    # ---- the cracker sheet
    cr_a = sum(1 for a, s in zip(A, calc.ask_a(P, "move")) if a["eff"] == s["eff"]) + sum(
        1 for a, s in zip(A, calc.ask_a(P, "move")) if a["days"] == s["days"])
    C("CR1 the cracker's Ask A path (the filed definition run on the feed and the report's placement dates) misses all "
      "18 figures", cr_a == 0, cr_a)
    crb = calc.ask_b(P, "face")
    crt = calc.ask_b_totals(crb)
    hit_b = [k2 for k2 in B if abs(crb.get(k2, 0) - B[k2]) < 0.5] + [y for y in BT if abs(crt.get(y, 0) - BT[y]) < 0.5]
    C("CR2 the cracker's Ask B path (the payroll's playing-time and legacy season-end lines at face value, each half to "
      "its season, voids netted, pitchers dropped) misses all %d figures" % (len(B) + len(BT)), not hit_b, hit_b)

    # ---- the separation line and the distractors
    tmp = tempfile.mkdtemp(prefix="t151sep", dir=os.path.dirname(target))
    try:
        for f in MAIN_FILES:
            shutil.copy(os.path.join(target, f), tmp)
        Pm = calc.load(tmp)
        Gm = calc.golden(Pm)
        C("SEP1 the call from the main-call files alone is the golden (no ask file or distractor read)",
          abs(Gm["total"] - G["total"]) < 0.01 and Gm["per_r"] == G["per_r"])
        for f in ASK_FILES:
            shutil.copy(os.path.join(target, f), tmp)
        Pa = calc.load(tmp)
        C("SEP2 both asks unchanged with the distractors deleted", calc.ask_a(Pa) == A and calc.ask_b(Pa) == B)
    finally:
        shutil.rmtree(tmp)
    main_docs = " ".join(texts[f] for f in (DOC.F_FIN14, DOC.F_TERMS, REC.F_DC27, DOC.F_NOTES))
    C("SEP3 no main-call document carries an ask's organ (payroll timing, earning codes, injured-list dates)",
      not re.search(r"January 15|earning code|E40|BPA|eligible|retroactive|half in the first payroll", main_docs))
    for f in DISTRACTORS:
        tmp = tempfile.mkdtemp(prefix="t151dis", dir=os.path.dirname(target))
        try:
            for g2 in files:
                if g2 != f:
                    shutil.copy(os.path.join(target, g2), tmp)
            Pd = calc.load(tmp)
            Gd = calc.golden(Pd)
            C("D1 deleting %s leaves the golden and both asks" % f, abs(Gd["total"] - G["total"]) < 0.01 and
              calc.ask_a(Pd) == A and calc.ask_b(Pd) == B)
        finally:
            shutil.rmtree(tmp)

    # ---- the realism sweep
    C("RS1 the unrounded accrual is not a round figure", round(G["total"]) % 1000 != 0, G["total"])
    allt = " ".join(texts.values()) + " " + memo
    C("RS2 the staff named are the drawn personas; no placeholder names", K.PEOPLE["agm"] in allt and
      K.PEOPLE["payroll"] in allt and K.PEOPLE["controller"] in memo and
      not re.search(r"John Doe|Jane Doe|Acme|Company [A-Z]\b|Player [A-Z]\b", allt))
    bad_meta = []
    for f in files + ["golden/" + x for x in os.listdir(golden)]:
        p = os.path.join(target, f) if not f.startswith("golden/") else os.path.join(golden, f[7:])
        raw = open(p, "rb").read()
        if f.endswith((".xlsx", ".docx")):
            z = zipfile.ZipFile(p)
            core = z.read("docProps/core.xml").decode()
            app = z.read("docProps/app.xml").decode() if "docProps/app.xml" in z.namelist() else ""
            if "openpyxl" in core + app or "python" in (core + app).lower():
                bad_meta.append(f)
            m = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core)
            when = dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%SZ").date()
            if when > K.ASOF:
                bad_meta.append((f, when))
        if f.endswith(".pdf") and (b"ReportLab" in raw or b"reportlab" in raw or b"D:2000" in raw):
            bad_meta.append(f)
    C("RS3 containers scrubbed: no writer's name, no stamp after the pull", not bad_meta, bad_meta)
    dash = [f for f, t in texts.items() if DASH.search(t)]
    for p in [os.path.join(TASK, "submission.md"), os.path.join(TASK, "prompt.txt"),
              os.path.join(TASK, "DESIGN_NOTE.md")]:
        if os.path.exists(p) and DASH.search(open(p, encoding="utf-8").read()):
            dash.append(p)
    if DASH.search(memo):
        dash.append(DL.F_MEMO)
    C("RS4 no en or em dash anywhere shipped or written", not dash, dash)
    team_pa = defaultdict(int)
    for (y, g, d, club, pid, slot, stt, pa, pos) in P.lines:
        team_pa[(y, club)] += pa
    sdt = float(np.std(list(team_pa.values())))
    C("RS5 club-season plate-appearance totals vary as a league's do (sd %.0f)" % sdt, 40 < sdt < 250, sdt)
    sub_rows = list(csv.DictReader(open(os.path.join(target, REC.F_BAT), encoding="utf-8")))
    C("RS5b the platform's substitute flag agrees with its batting-order code on every line", all(
        (r["is_substitute"] == "true") == (int(r["batting_order"]) % 100 != 0) for r in sub_rows))
    hitters = defaultdict(set)
    for r in P.plan:
        hitters[r["name"]].add(r["lg"])
    C("RS6 among hitters the five's names are unique", all(len(hitters[f["name"]]) == 1 for f in F))
    reasons = len({t["description"].split(". ", 1)[-1] for t in tx if t["type"] == "IL_PLACEMENT"})
    C("RS7 injuries vary on the feed (%d distinct)" % reasons, reasons >= 15)
    C("RS8 the term sheets' figures differ by contract", len({f["lines"][0][0] for f in F}) == 5 and
      len({tuple(t for _, t in f["lines"]) for f in F}) == 5)

    # ---- house fixes: payment dates the stated rule predicts (H6), citations (H8), the manifest (H9), dates (H16)
    pa_pay = [r for r in pay if r["earning_code"] in ("BPA", "E40") and r["employee_name"] in
              {REC.hris_name(L.players[k].name) for k in REC.VET_CONTRACTS} | {REC.legacy_name(L.players[k].name)
                                                                              for k in REC.VET_CONTRACTS}
              and r["status"] == "PAID" and float(r["amount"]) > 0]
    off_rule = [r for r in pa_pay if r["pay_date"][5:] not in ("10-15", "01-15", "11-15") and
                not (r["pay_date"] == "2026-10-22")]
    C("H6 every veteran's bonus payment falls on a date the register's notes give (one reissue apart)", not off_rule,
      off_rule[:3])
    gold_txt = xlsx_strings(os.path.join(golden, DL.F_BOOK)) + " " + memo + " " + sub_text()
    cited = set(re.findall(r"[\w.-]+\.(?:csv|txt|xlsx|pdf|json)", gold_txt)) - {DL.F_BOOK}
    C("H8 every file the goldens and the write-up cite ships", cited <= set(files), cited - set(files))
    man = [r["file"] for r in csv.DictReader(open(os.path.join(target, DOC.F_MANIFEST), encoding="utf-8"))]
    C("H9 the manifest lists exactly the shipped files", sorted(man) == files, set(files) ^ set(man))
    late = [t["date"] for t in tx if t["date"] > K.ASOF.isoformat()] + [r["pay_date"] for r in pay if
                                                                         r["pay_date"] > K.ASOF.isoformat()]
    late += [r["report_date"] for r in rep if r["report_date"] > K.ASOF.isoformat()]
    C("H16 no record dated after the pull (forward dates only in the 2027 schedule, calendar, terms and depth chart)",
      not late and max(x[2] for x in P.lines) < K.ASOF, late[:3])

    # ---- goldens and the write-up
    figs = json.load(open(os.path.join(K.HERE, "figures.json"), encoding="utf-8"))
    wb = openpyxl.load_workbook(os.path.join(golden, DL.F_BOOK), data_only=True)
    ws = wb["Accrual"]
    acc = {}
    tot_cell = None
    for row in ws.iter_rows(min_row=6, values_only=True):
        if isinstance(row[0], str) and row[0].endswith(", accrual"):
            acc[row[0][:-9]] = row[7]
        if row[0] == "Total":
            tot_cell = row[7]
    C("GD1 the workbook's accruals equal the golden", acc == G["per_r"] and tot_cell == GOLD_TOTAL, (acc, tot_cell))
    ws2 = wb["IL stints since 2024"]
    st_rows = [(r[0], r[4].date() if hasattr(r[4], "date") else r[4], r[7]) for r in ws2.iter_rows(min_row=4, values_only=True)
               if r[0] and r[7] is not None]
    C("GD2 the workbook's stints equal Ask A", st_rows == [(a["player"], a["eff"], a["days"]) for a in A], st_rows)
    ws3 = wb["PA bonuses paid 2024-2026"]
    pb = {}
    for r in ws3.iter_rows(min_row=4, values_only=True):
        if isinstance(r[0], int) and r[1] and not str(r[1]).startswith("Total"):
            pb[(r[0], r[1])] = r[2]
    C("GD3 the workbook's payments equal Ask B", pb == {(y, DL.plain(n)): round(v) for (y, n), v in B.items() if v}, pb)
    C("GD4 figures.json carries the call", figs["call"]["total"] == K.money(GOLD_TOTAL))
    C("GD5 two goldens, both named in the prompt", sorted(os.listdir(golden)) == sorted([DL.F_BOOK, DL.F_MEMO]))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    blocks = re.findall(r"^## (.+)$", sub, re.M)
    C("GD6 the write-up carries exactly the five blocks", blocks == ["Tags", "1. Final Recommendation",
                                                                     "2. Critical Components",
                                                                     "3. Step-by-Step Solution",
                                                                     "4. Deliverable Answers"], blocks)
    steps = re.findall(r"^\d+\. ", sub.split("## 3.")[1].split("## 4.")[0], re.M)
    C("GD7 at most eight steps", len(steps) <= 8, len(steps))
    named = set(re.findall(r"[\w.-]+\.(?:csv|txt|xlsx|pdf|json)", sub.split("## 4.")[0]))
    C("GD8 every file the steps name ships", named <= set(files), named - set(files))
    C("GD9 the memo states the accrual and each player's amount on about one page",
      len(memo.split()) < 480 and all(f["name"] in memo for f in F), len(memo.split()))
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read().strip()
    C("P1 the prompt is one paragraph under 1,000 characters naming both deliverables",
      len(prompt) < 1000 and "\n" not in prompt and DL.F_BOOK in prompt and DL.F_MEMO in prompt, len(prompt))
    C("P2 the prompt names no method, projection, depth chart or lineup slot",
      not re.search(r"project|depth|slot|lineup|batting order|distribution|regulars?\b(?!-season)|probab|band",
                    prompt, re.I))
    C.report()
    return C


def sub_text():
    p = os.path.join(TASK, "submission.md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def key_lg(F, name):
    return [f["lg"] for f in F if f["name"] == name][0]
