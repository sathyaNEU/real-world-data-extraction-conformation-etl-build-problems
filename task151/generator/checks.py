"""task151 checks, run on every build: the input gates; the three-rules block (R1 the field's raw material, R2 every
mess item neutral, R3a the analyst test on the clean truth and the pack, R3b the decisive step alone, R3c no plant,
R3s the strict rule 3 test on every shipped sentence that bears on how the figure is computed); the bins and the
one-sigma test; every construction of the golden; the out-of-sample back-test; every rival by name; every semantic
fork row (SF1 to SF19) and closure axis (C1 to C22); the ask with every stop, hazard and the cracker's path; the
separation line (the call's files byte-identical to the shipped commit) and the distractors; the realism sweep; the
goldens and the prompt. Any failure stops the build."""
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
              DOC.F_WP, DOC.F_NOTES]
ASK_FILES = [REC.F_PAY, REC.F_HRIS, REC.F_CODES, REC.F_REG]
DISTRACTORS = [REC.F_PROJ, REC.F_SCHED27, REC.F_TRANS, REC.F_ILREP, DOC.F_ILRULES]
# every file the call reads, as shipped at e93c6561 (target.zip 83bf068f): the rubric repair moves none of them
SHIPPED_CALL_FILES = {
    "lsf_batting_2021_2024.txt": "f5ae0bee4447473a827dcaa694a782ef44e5de0351f39efdf3094bb54ed83689",
    "lsf_batting_2025_2026.csv": "56f1b187c3f7a13cea32e2f11c9b98092be4ce100c5095ead5a78533783229ea",
    "lsf_player_id_crosswalk.csv": "ceca79b6f4cc3ea2246035e414e17860d0e2acb59d0f1ed6b2eb4afce3f85d0f",
    "league_club_directory.csv": "de5efc944a881b2ffb35bb1f6c31ad6dd6f952330d401cdad217cb6adfb84684",
    "hvbd_winter_depth_charts_2021_2026.xlsx": "e351a59f7c395394b5aecbb948f59ddcff2d9c97fd922210d9882b81afb17df3",
    "ral_depth_chart_2027.xlsx": "d053dbed8c291d3f17fe290aff577e4d4231102e6ef1e22c77f8828fd4d7abdf",
    "term_sheets_2027_free_agent_hitters.pdf": "524373318a4256e5f9a37dc5ccae2a6610a948c435bfbab70b656f1fd0875a65",
    "FIN-14_player_compensation_accounting_policy.pdf": "c6a49bc369f66930f0db84152b49ed01fdd527c923c437b4636ed6fbd785215c",
    "CF-14.4_look-back_working_paper.pdf": "c55637fcd94f20b704b9c780e554f2ecf6554503e9917fafc164699f67e0f3a3",
    "lsf_feed_notes.txt": "9c7c155442788ff4c81a19cc2d8b1cfe4fa25e6d142303da315d26f32ed9b746",
    "league_calendar_2021_2027.csv": "42e999b3c2e71e5518144cb335808dd1c60ce1385193941a11ec4ff2a5d648c2",
    "hvbd_hitter_projections_2022_2027.csv": "4ad50fe25fe383372b8c8a0c49aa5c044074af50b3476c5a7cf633662d965827",
}
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
    P, T, G, RV, B = R["P"], R["T"], R["G"], R["R"], R["B"]
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
    fin = texts[DOC.F_FIN14] + " " + texts[DOC.F_WP]          # FIN-14 and its working paper CF-14.4 (4.4)
    terms = texts[DOC.F_TERMS]
    how = fin + " " + terms + " " + texts[REC.F_DC27] + " " + texts[DOC.F_NOTES] + " " + texts[REC.F_DC]
    C("R3s no shipped sentence names a distribution, a comparison set, a rate per start or how starts are lost",
      not re.search(METHOD, how, re.I), re.findall(r".{40}(?:%s).{40}" % METHOD, how, re.I)[:3])
    C("R3s FIN-14 fixes the estimand (4.2, 4.3) and the selection criterion (4.4, its population, thresholds and score "
      "in working paper CF-14.4), and names no basis",
      "multiplied by the probability" in fin and "the contract stands as signed through the season" in fin and
      "set in close-file working paper CF-14.4" in texts[DOC.F_FIN14] and
      "The Club uses the basis with the lowest average" in texts[DOC.F_WP] and not re.search(
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
    thin = "the slot's plate appearances with its substitutes', per start"
    tv = RV[thin]
    readings = [("the seasons 2023 to 2026", {}), ("2024 to 2026", dict(seasons_=(2024, 2025, 2026))),
                ("2023 to 2025", dict(seasons_=(2023, 2024, 2025))), ("2022 to 2025", dict(seasons_=(2022, 2023, 2024, 2025))),
                ("the lineups without catchers", dict(tests_nc=True)), ("the planning club's 100", dict(est_club=True)),
                ("a threshold passed", dict(strict=True))]
    lost = []
    for what, kw in readings:
        LBt, _, pr = calc.lookback(P, T, names=list(calc.FAMILY) + [thin], **kw)
        best = min(calc.FAMILY, key=LBt.get)
        dd = pr[thin] - pr[best]
        lost.append((what, 100 * (LBt[thin] / LBt[best] - 1), dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd)))))
    C("LB9 the round 3 judge's near rival '%s' files %s (%+.2f bins, players %s) and loses the look-back on every "
      "reading, by %.2f to %.2f per cent (hitter-paired z %.2f to %.2f; %.2f per cent on the filed reading): it counts a "
      "substitute's plate appearances against the starter's start" % (
          thin, K.money(calc.r250(tv)), bins(tv, G["total"]), [calc.r100(v) // 1000 for v in acc[thin].values()],
          min(x[1] for x in lost), max(x[1] for x in lost), min(x[2] for x in lost), max(x[2] for x in lost),
          lost[0][1]), calc.r250(tv) != GOLD_TOTAL and all(x[1] > 0.1 for x in lost) and LB[thin] > gb * 1.001, lost)
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
                                "own record given a weight of 5 per cent", "regression on the projection, the slot and catching",
                                "the slot's plate appearances with its substitutes', per start"]
    for sid, what, kw in (("SF11", "the seasons read as 2024 to 2026 only", dict(seasons_=(2024, 2025, 2026))),
                          ("SF11", "the seasons read as 2023 to 2025 only", dict(seasons_=(2023, 2024, 2025))),
                          ("SF11", "the seasons read as 2022 to 2025 (no 2022 hitter has two earlier seasons)",
                           dict(seasons_=(2022, 2023, 2024, 2025))),
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

    # ---- the ask: playing-time bonuses other than plate-appearance bonuses paid, 2023 to 2025
    rep = list(csv.DictReader(open(os.path.join(target, REC.F_ILREP), encoding="utf-8")))
    BT = calc.ask_totals(B)
    GT_ASK = {2023: 525000, 2024: 1005000, 2025: 1085000}
    C("AK1 paid for 2023, 2024, 2025: %s (%d player rows)" % (", ".join(K.money(GT_ASK[y]) for y in sorted(GT_ASK)),
                                                              len(B)),
      {y: round(v) for y, v in BT.items()} == GT_ASK and len(B) == 18, ({y: round(v) for y, v in BT.items()}, len(B)))
    truth_ask = {(y, REC.hris_name(L.players[k].name)): v for (k, y), v in REC.pitcher_bonuses().items()
                 if y in calc.ASK_SEASONS}
    C("AK2 fair: the golden is the season as it happened, every row (the generator's lines reached, priced by the "
      "contract)", {k2: round(v) for k2, v in B.items()} == {k2: round(v) for k2, v in truth_ask.items()},
      sorted(set(B) ^ set(truth_ask)))
    pay = list(csv.DictReader(open(os.path.join(target, REC.F_PAY), encoding="utf-8")))
    codes = {r["earning_code"]: r for r in csv.DictReader(open(os.path.join(target, REC.F_CODES), encoding="utf-8"))}
    pnames = {REC.legacy_name(L.players[k].name) for k in REC.PITCHER_CONTRACTS}
    pre_oct = [r for r in pay if r["employee_name"] in pnames and r["pay_date"][5:] == "10-15" and
               r["pay_date"] < "2026-01-01" and r["status"] == "PAID"]
    pre_jan = [r for r in pay if r["employee_name"] in pnames and r["pay_date"][5:] == "01-15" and
               r["pay_date"] < "2026-01-01"]
    C("AK3 the primary: every pitcher's season-end payment before the HRIS cutover is a legacy E45 OTHER BONUS line (%d), "
      "the code the earning-code table migrates as other bonus, and every legacy January half is E40 PERF BONUS (%d), "
      "the code it migrates as the playing-time bonus" % (len(pre_oct), len(pre_jan)),
      pre_oct and all(r["earning_code"] == "E45" and r["earning_description"] == "OTHER BONUS" for r in pre_oct) and
      pre_jan and all(r["earning_code"] == "E40" for r in pre_jan) and codes["E45"]["migrated_as"] == "BOT" and
      codes["E40"]["migrated_as"] == "BPA" and codes["BPA"]["description"] == "Playing-time bonus" and
      codes["BOT"]["description"] == "Other bonus", (len(pre_oct), len(pre_jan)))
    twins = [r for r in pay if r["earning_code"] == "E45" and r["employee_name"] not in pnames]
    C("AK3b the catch-all code has benign twins: E45 also carries award bonuses and deferred salary to hitters (%d lines)"
      % len(twins),
      len(twins) >= 2 and all(r["pay_date"][5:] in ("10-15", "11-15") for r in twins), len(twins))
    pnames_all = pnames | {REC.hris_name(L.players[k].name) for k in REC.PITCHER_CONTRACTS}
    hitters_pt = [r for r in pay if r["earning_code"] in ("E40", "BPA") and r["employee_name"] not in pnames_all]
    C("AK3c the playing-time code carries the hitters' plate-appearance bonuses in the season-end run (%d lines), so "
      "the code reads as the playing-time code" % len(hitters_pt), len(hitters_pt) >= 5 and
      all(r["pay_date"][5:] == "10-15" for r in hitters_pt))
    terms_of = defaultdict(list)
    for r in calc.register(target):
        for m_, a_, l_ in calc.parse_terms(r[calc.OTHER_COL]):
            terms_of[(r["Player"], r["Seasons"])].append((a_, len(l_)))
    def valid_full(name, y, amount):
        for (nm, ss), tt in terms_of.items():
            if nm == name and y in calc.seasons_of(ss):
                sums = {0}
                for a_, n_ in tt:
                    sums = {s + a_ * j for s in sums for j in range(n_ + 1)}
                return round(amount) in sums
        return False
    cr = calc.ask(P, "cracker")
    last_rows = {(y, n) for (y, n) in B if any(r["Player"] == n and calc.parse_terms(r[calc.OTHER_COL]) and
                                               max(calc.seasons_of(r["Seasons"])) == y for r in calc.register(target))}
    cu_rows = set()
    cu_first = set()
    for k_, y_ in REC.CATCH_UP:
        nm_ = REC.hris_name(L.players[k_].name)
        cu_rows |= {(y_, nm_), (y_ + 1, nm_)}
        cu_first.add((y_, nm_))
    C("AK3d the wrong reading is complete: every amount the playing-time codes carry for a season is itself a full bonus "
      "the player's own terms allow, and the %d seasons they carry nothing for (%d a contract's last, %d whose January "
      "half the legacy run missed) read as seasons with no line reached, so no row fails a check against the register"
      % (len(last_rows) + len(cu_first), len(last_rows), len(cu_first)),
      all(valid_full(n, y, v) for (y, n), v in cr.items()) and set(B) - set(cr) == last_rows | cu_first
      and len(last_rows) == 7 and len(cu_first) == 2, sorted(set(B) - set(cr)))
    crt = calc.ask_totals(cr)
    hit_rows = [k2 for k2 in B if abs(cr.get(k2, 0) - B[k2]) < 0.5]
    hit_tot = [y for y in BT if abs(crt.get(y, 0) - BT[y]) < 0.5]
    C("AK4 the cracker (the earning-code table's playing-time codes, each legacy line by its name, voids netted, each "
      "half to its season) misses all %d figures: every row it carries at exactly half its golden, a contract's last "
      "season not at all" % (len(B) + len(BT)),
      not hit_rows and not hit_tot and all(abs(cr[k2] - B[k2] / 2) < 0.5 for k2 in cr), (hit_rows, hit_tot))
    designed = {"payyear": (18, 3), "e45_whole": (8, 3), "e45_all": (9, 3), "map": (1, 1), "register_id": (1, 1),
                "gross": (1, 1), "settle_whole": (5, 3), "double": (7, 3), "cap": (5, 3), "roundest": (5, 3)}
    for mode, (rows_min, tot_min) in designed.items():
        S2 = calc.ask(P, mode)
        T2 = calc.ask_totals(S2)
        miss_rows = [k2 for k2 in B if abs(S2.get(k2, 0) - B[k2]) >= 0.5]
        miss_tot = [y for y in BT if abs(T2.get(y, 0) - BT[y]) >= 0.5]
        C("AK5 stop '%s' misses %d rows and %d totals (designed at least %d and %d), each outside its bin" % (
            mode, len(miss_rows), len(miss_tot), rows_min, tot_min),
          len(miss_rows) >= rows_min and len(miss_tot) >= tot_min, (miss_rows, {y: round(v) for y, v in T2.items()}))
    mp = {r["legacy_employee_no"]: r for r in csv.DictReader(open(os.path.join(target, REC.F_HRIS), encoding="utf-8"))}
    reg_rows = calc.register(target)
    reg_ids = {str(r["Employee ID"]): r["Player"] for r in reg_rows}
    names_of = defaultdict(set)
    for r in pay:
        if r["employee_id"].isdigit():
            names_of[r["employee_id"]].add(r["employee_name"])
    multi = {e: n for e, n in names_of.items() if len(n) > 1}
    old_k, new_k = REC.REISSUED
    C("AK6 one legacy number carries two players (%s), the HRIS map gives it to the later one and the register to the "
      "earlier one" % sorted(multi), len(multi) == 1 and list(multi.values())[0] == {
          REC.legacy_name(L.players[old_k].name), REC.legacy_name(L.players[new_k].name)} and
      mp[list(multi)[0]]["employee_name"] == REC.hris_name(L.players[new_k].name) and
      reg_ids.get(list(multi)[0]) == REC.hris_name(L.players[old_k].name), multi)
    D_ = calc.ask(P, detail=True)
    carried = sorted((y, n, round(v["award"])) for (y, n), v in D_.items() if v["award"])
    C("AK7 three legacy season-end lines carry the player's All-Star bonus beside his playing-time half %s" % carried,
      len(carried) == 3 and {y for y, _, _ in carried} == {2023, 2024, 2025}, carried)
    void = [r for r in pay if r["status"] in ("VOIDED", "VOID REVERSAL")]
    C("AK8 one void and reissue nets to one payment", len(void) == 2 and sum(float(r["amount"]) for r in void) == 0)
    jan23 = [r for r in pay if r["pay_date"] == "2023-01-15" and r["earning_code"] == "E40"]
    C("AK9 the January 2023 line is the 2022 season's second half (the pay-year reading moves it into 2023)",
      len(jan23) == 1 and jan23[0]["employee_name"] in pnames, jan23)
    # ---- the second device: the season-end line after a contract's last season settles the deferred salary too
    reg_all = calc.register(target)
    sal_paid = defaultdict(float)
    by_ln = {calc.legacy_key(r["Player"]): r["Player"] for r in reg_all}
    by_eid = {str(r["Employee ID"]): r["Player"] for r in reg_all}
    for r in pay:
        if r["earning_code"] in calc.SALARY_CODES:
            nm = by_eid.get(r["employee_id"]) if not r["employee_id"].isdigit() else by_ln.get(r["employee_name"])
            sal_paid[(nm, int(r["pay_date"][:4]))] += float(r["amount"])
    short = {}
    for r in reg_all:
        ss = calc.seasons_of(r["Seasons"])
        sh = sum(r["Salary %d" % y] - sal_paid[(r["Player"], y)] for y in ss if 2023 <= y <= 2026 and r.get("Salary %d" % y))
        if abs(sh) > 0.5:
            short[(r["Player"], r["Seasons"])] = round(sh, 2)
    dfr_rows = {k2: v["deferral"] for k2, v in D_.items() if v["deferral"]}
    gen_dfr = {(y, REC.hris_name(L.players[k].name)): REC.deferral_due(k, y) for k in REC.PITCHER_CONTRACTS
               for y in calc.ASK_SEASONS if REC.last_season(k, y) and REC.deferral_due(k, y)}
    tmax = {k2: max(calc.combos([(a_, n_) for (nm, ss), tt in terms_of.items() if nm == k2[1] and
                                 k2[0] in calc.seasons_of(ss) for a_, n_ in tt])) for k2 in B}
    C("DF1 the second device: after a contract's last season the season-end line settles the season's whole bonus and, "
      "on %d pitchers' contracts, the salary the contract deferred to its end; each such line less any award is above "
      "the largest bonus his terms allow, and the excess is the register's salary less the salary lines paid over the "
      "contract, to the dollar %s" % (len(dfr_rows), sorted((y, n, round(v)) for (y, n), v in dfr_rows.items())),
      len(dfr_rows) == 5 and {k2: round(v) for k2, v in dfr_rows.items()} == {k2: round(v) for k2, v in gen_dfr.items()}
      and all(D_[k2]["oct"] - D_[k2]["award"] > tmax[k2] and D_[k2]["jan"] == 0 for k2 in dfr_rows) and
      {y for y, _ in dfr_rows} == set(calc.ASK_SEASONS), dfr_rows)
    full1 = calc.ask(P, "settle_whole")
    f1t = calc.ask_totals(full1)
    f1_miss = {k2 for k2 in B if abs(full1.get(k2, 0) - B[k2]) >= 0.5}
    C("DF2 the full handling of the catch-all (both payments whatever the code, every All-Star taken out, the reissued "
      "number by name, the void netted, each payment to its season) misses the %d deferral rows and all three totals, "
      "keeping %d of %d figures" % (len(f1_miss), len(B) - len(f1_miss), len(B) + len(BT)),
      f1_miss == set(dfr_rows) | cu_rows and all(abs(f1t[y] - BT[y]) >= 0.5 for y in BT), sorted(f1_miss))
    C("DF3 every deferral row's golden is below the largest bonus his terms allow, so cutting the line to his terms "
      "misses it too", all(B[k2] < tmax[k2] for k2 in dfr_rows) and
      {k2 for k2 in B if abs(calc.ask(P, "cap").get(k2, 0) - B[k2]) >= 0.5} == set(dfr_rows) | cu_rows)
    dbl = calc.ask(P, "double")
    C("DF4 twice the January half misses every contract's last season (no January payment follows it)",
      all(abs(dbl.get(k2, 0) - B[k2]) >= 0.5 for k2 in last_rows) and all(abs(dbl[k2] - B[k2]) < 0.5 for k2 in dbl
                                                                          if k2 not in last_rows))
    rnd = calc.ask(P, "roundest")
    C("DF8 aimed: splitting a line his terms cannot hold into a bonus they allow and the roundest remainder (a guess at a "
      "round non-bonus payment, no reconciliation) misses every deferral row and every total",
      {k2 for k2 in B if abs(rnd.get(k2, 0) - B[k2]) >= 0.5} == set(dfr_rows) | cu_rows and
      all(abs(calc.ask_totals(rnd)[y] - BT[y]) >= 0.5 for y in BT), sorted((k2, rnd.get(k2)) for k2 in dfr_rows))
    # the third device: a January run that missed a half, settled inside the next season-end line
    nc = calc.ask(P, "no_catchup")
    nct = calc.ask_totals(nc)
    nc_miss = {k2 for k2 in B if abs(nc.get(k2, 0) - B[k2]) >= 0.5}
    gold_detail = calc.ask(P, "golden", detail=True)
    exact = []
    for k_, y_ in REC.CATCH_UP:
        nm_ = REC.hris_name(L.players[k_].name)
        a_, b_ = gold_detail[(y_, nm_)], gold_detail[(y_ + 1, nm_)]
        exact.append(abs(a_["jan"] - (a_["oct"] - a_["award"])) < 0.5 and abs(b_["oct"] - b_["award"] - b_["jan"]) < 0.5)
    C("CU1 the third device: the January run after %s missed the half it owed, and the next season-end line exceeds the "
      "January half after it by exactly that season's October half (net of the All-Star bonus its line carries), to the "
      "dollar; the golden puts it back in its season" % ", ".join("%s %d" % (REC.hris_name(L.players[k_].name), y_)
                                                             for k_, y_ in REC.CATCH_UP),
      all(exact) and len(exact) == 2, exact)
    aw_of = defaultdict(set)
    for r in calc.register(target):
        for a_ in calc.parse_awards(r[calc.AWARD_COL]):
            aw_of[r["Player"]].add(a_)
    C("CU2 the full handling of every other device without it (each season-end line to its season, each January line to "
      "the one before) misses the %d catch-up rows and all three totals, every wrong row a full bonus the player's terms "
      "allow as read or once an award his register lists is taken out, so no check against the register fails"
      % len(cu_rows),
      nc_miss == cu_rows and all(abs(nct[y] - BT[y]) >= 0.5 for y in BT) and
      all(valid_full(n, y, nc[(y, n)]) or any(valid_full(n, y, nc[(y, n)] - w) for w in aw_of[n])
          for (y, n) in cu_rows if (y, n) in nc), sorted((k2, nc.get(k2)) for k2 in cu_rows))
    pay_rows = calc.read_csv(os.path.join(target, calc.F_PAY))
    oct_lines = [r for r in pay_rows if r["earning_code"] == "E45" and r["pay_date"].endswith("-10-15")]
    C("CU3 no marker: every season-end catch-all line carries the same code, description and status, the catch-up "
      "lines among them", len({(r["earning_code"], r["earning_description"], r["status"]) for r in oct_lines
                                if r["status"] == "PAID"}) == 1, len(oct_lines))
    reg_text = " ".join(str(c) for r in reg_all for c in r.values() if c is not None)
    wbh = openpyxl.load_workbook(os.path.join(target, REC.F_REG), read_only=True)
    head_text = " ".join(str(c) for row in wbh["Register"].iter_rows(max_row=4, values_only=True) for c in row if c)
    C("DF5 silent: no shipped file states a deferral of a club contract (the register carries no deferral column or "
      "note; FIN-14 3.2 states the policy, and the term sheets the 2027 signing's own deferral, 2033 to 2037)",
      not re.search(r"defer", reg_text + " " + head_text, re.I) and
      not re.search(r"defer", " ".join(t for f, t in texts.items() if f not in (DOC.F_FIN14, DOC.F_TERMS)), re.I) and
      re.search(r"deferred,\s+payable\s+in\s+equal\s+installments\s+2033\s+to\s+2037", texts[DOC.F_TERMS]))
    hit_def = {by_ln.get(r["employee_name"]): float(r["amount"]) for r in pay if r["earning_code"] == "E45" and
               r["pay_date"] == "2024-10-15" and r["employee_name"] not in pnames}
    vet_short = {k2: v for k2, v in short.items() if k2[1] == "2023-2024" and not any(
        calc.parse_terms(r[calc.OTHER_COL]) for r in reg_all if (r["Player"], r["Seasons"]) == k2)}
    star24 = {n: sum(calc.parse_awards(r[calc.AWARD_COL])) for r in reg_all for n in [r["Player"]]
              if r["Seasons"] == "2023-2024" and "All-Star" in (r[calc.AWARD_COL] or "")}
    C("DF6 benign twins: the catch-all carries the deferred salary of two hitters whose contracts ended in 2024, one "
      "line alone and one with an All-Star bonus in the same line; the ask counts neither (no hitter's contract carries "
      "other terms) %s" % sorted((n, round(v)) for (n, _), v in vet_short.items()),
      len(vet_short) == 2 and len(hit_def) == 2 and all(abs(hit_def.get(n, 0) - v - star24.get(n, 0)) < 0.5
                                                        for (n, _), v in vet_short.items()) and
      sum(1 for (n, _) in vet_short if n in star24) == 1, (hit_def, vet_short))
    pit_short = {k2: v for k2, v in short.items() if any(calc.parse_terms(r[calc.OTHER_COL]) for r in reg_all
                                                         if (r["Player"], r["Seasons"]) == k2)}
    C("DF7 the deferral is salary: the five pitchers' contracts are the only ones with other terms whose salary lines "
      "fall short of the register, and each by its deferral", sorted(round(v) for v in pit_short.values()) ==
      sorted(round(v) for v in dfr_rows.values()), pit_short)
    C("SF20 the deferred salary inside the season-end line is not a playing-time bonus: FIN-14 3.2 sets deferred "
      "salary apart from 4.1's class, and each line less the deferral is a bonus his terms allow",
      "3.2 Salary deferred under a contract" in texts[DOC.F_FIN14] and all(round(B[k2]) in calc.combos(
          [(a_, n_) for (nm, ss), tt in terms_of.items() if nm == k2[1] and k2[0] in calc.seasons_of(ss)
           for a_, n_ in tt]) for k2 in dfr_rows))
    C("SF21 the season-end line after a contract's last season is the whole season paid (a first half with the second "
      "unpaid reads the same figure: paid is paid), and no such line carries an award", all(
          D_[k2]["jan"] == 0 and D_[k2]["award"] == 0 for k2 in last_rows))
    assigned = [r["Player"] for r in reg_all if str(r["Status"]).startswith("Assigned to")]
    C("SF22 the register's salary is the contract's, gross of the deferral: every contract's salary lines add to it to "
      "the cent but the seven with a deferral (short by it) and the one assigned mid-season (short by the salary after "
      "its assignment)", set(short) == set(pit_short) | set(vet_short) | {k2 for k2 in short if k2[0] in assigned} and
      len(pit_short) == 5 and len(vet_short) == 2 and len(assigned) == 1, sorted(short))
    # the portal's determinism return of 10-29: the payment schedule the golden reads each season's payments by is
    # filed once, in the register's header, as the contract terms (never the late halves)
    nd = calc.ask(P, "no_catchup", detail=True)

    def on_schedule(d, k2):
        v = d.get(k2)
        if v is None:
            return False
        if k2 in last_rows:
            return v["jan"] == 0
        return v["jan"] > 0.5 and abs(v["oct"] - v["award"] - v["jan"]) < 0.5
    C("SF23 'paid for each season' with a half paid late: the register's note files the schedule (one half in the "
      "October 15 run after the season, one half in the January 15 run after that, in full in the October run after a "
      "contract's last season); the golden keeps it on all %d rows, the season-by-run reading breaks it on each of the "
      "%d catch-up rows (no January half on a contract running on, or unequal halves), so a quoted sentence rules it "
      "out; the note names no player and no missed payment (positive control: the header's maintainer line read)"
      % (len(B), len(cu_rows)),
      "Maintained by Baseball Operations and Finance" in head_text and REC.PAY_NOTE in head_text and
      all(on_schedule(D_, k2) for k2 in B) and not any(on_schedule(nd, k2) for k2 in cu_rows) and
      not re.search(r"miss|late|catch|carr|White|Livingston", REC.PAY_NOTE, re.I),
      ([k2 for k2 in B if not on_schedule(D_, k2)], [k2 for k2 in cu_rows if on_schedule(nd, k2)]))
    main_figs = {GOLD_TOTAL} | set(GOLD_PER.values())
    C("AK10 no ask figure equals a figure of the call", not ({round(v) for v in B.values()} | set(GT_ASK.values())) &
      main_figs)
    C("AK11 every ask figure is whole dollars", all(abs(v - round(v)) < 1e-6 for v in list(B.values()) + list(BT.values())))
    doc_text = " ".join(t for f, t in texts.items() if f.endswith((".pdf", ".txt")) and not f.startswith("lsf_batting"))
    shown = [K.money(v)[1:] for v in list(B.values()) + list(BT.values())
             if re.search(r"(?<![\d,])" + re.escape(K.money(v)[1:]) + r"(?![\d,])", doc_text)]
    C("AK12 no ask figure stands in a shipped document (the term sheets, FIN-14, CF-14.4, the rules, the feed notes; "
      "positive control: the term sheets' $320,000 line is found)", not shown and "320,000" in doc_text, shown)
    fin_txt = texts[DOC.F_FIN14]
    measures = {m for r in reg_rows for m, _, _ in calc.parse_terms(r[calc.OTHER_COL])}
    C("SF15 'playing-time bonuses other than plate-appearance bonuses' is FIN-14 4.1's class: every measure the register "
      "carries is one 4.1 names (%s), and no hitter's contract carries one" % sorted(measures),
      measures and all(m in fin_txt.lower() for m in measures) and not any(
          calc.parse_terms(r[calc.OTHER_COL]) for r in reg_rows if r["Pos"] != "P"), measures)
    ptxt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    py = calc.ask_totals(calc.ask(P, "payyear"))
    opening = {y: K.SEASON[y][0] for y in K.SEASON}
    C("SF16 'paid for each season' is the season earned: every January payment falls before that year's Opening Day, "
      "and the pay-year reading files %s" % {y: round(v) for y, v in sorted(py.items())},
      "that we paid for each of the 2023, 2024 and 2025 seasons" in ptxt and all(
          calc.ymd(r["pay_date"]) < opening[int(r["pay_date"][:4])] for r in pay if r["pay_date"][5:7] == "01") and
      all(abs(py.get(y, 0) - BT[y]) >= 0.5 for y in BT), py)
    C("SF17 'paid' is through the pull: every half of the 2023 to 2025 bonuses is paid by January 15, 2026, and nothing "
      "is dated after December 11, 2026", not any(r["pay_date"] > K.ASOF.isoformat() for r in pay) and
      all(r["pay_date"] <= "2026-01-15" for r in pay if r["employee_name"] in pnames_all and r["earning_code"] in (
          "E40", "E45", "BPA") and r["pay_date"][5:7] in ("10", "01")))
    C("SF18 award bonuses are not playing time: FIN-14 5 treats them apart from 4.1",
      "5. Award bonuses" in fin_txt and "relief appearances and days on the Active List" in fin_txt)
    C("SF19 the register is the only population: no 2026 season bonus is paid by the pull (due January 15, 2027)",
      not any(r["pay_date"] >= "2026-10-01" and r["earning_code"] in ("BPA", "BOT") for r in pay))

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
        C("SEP2 the ask unchanged with the distractors deleted", calc.ask(Pa) == B)
    finally:
        shutil.rmtree(tmp)
    main_docs = " ".join(texts[f] for f in (DOC.F_FIN14, DOC.F_WP, DOC.F_TERMS, REC.F_DC27, DOC.F_NOTES))
    C("SEP3 no main-call document carries an ask's organ (payroll codes, payment runs, employee numbers)",
      not re.search(r"January 15|October 15|earning code|E40|E45|BPA|OTHER BONUS|PERF BONUS|employee number|"
                    r"legacy payroll|HRIS|migrat", main_docs) and "plate appearances" in main_docs)
    import hashlib
    moved = [f for f, h in SHIPPED_CALL_FILES.items() if
             hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest() != h]
    C("SEP4 every file the call reads is byte-identical to the shipped commit e93c6561 (%d files)" %
      len(SHIPPED_CALL_FILES), not moved, moved)
    C("SEP5 the ask reads no file the call reads, and the call none of the ask's", not set(ASK_FILES) &
      set(SHIPPED_CALL_FILES))
    for f in DISTRACTORS:
        tmp = tempfile.mkdtemp(prefix="t151dis", dir=os.path.dirname(target))
        try:
            for g2 in files:
                if g2 != f:
                    shutil.copy(os.path.join(target, g2), tmp)
            Pd = calc.load(tmp)
            Gd = calc.golden(Pd)
            C("D1 deleting %s leaves the golden and the ask" % f, abs(Gd["total"] - G["total"]) < 0.01 and
              calc.ask(Pd) == B)
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
    bonus_pay = [r for r in pay if r["earning_code"] not in ("E01", "SAL", "E10", "SGN") and r["status"] == "PAID"
                 and float(r["amount"]) > 0]
    off_rule = [r for r in bonus_pay if r["pay_date"][5:] not in ("10-15", "01-15", "11-15", "07-31") and
                r["pay_date"] != (REC.VOID_REISSUE[1] + dt.timedelta(days=7)).isoformat()]
    C("H6 every bonus payment falls in a bonus run (October 15, January 15, November 15 for awards, July 31 for an "
      "All-Star from 2026), one reissue apart", not off_rule, off_rule[:3])
    wb_reg = openpyxl.load_workbook(os.path.join(target, REC.F_REG), read_only=True)
    C("H9b no notes, readme or dictionary sheet or file ships: the register is one sheet", wb_reg.sheetnames ==
      ["Register"] and not [f for f in files if re.search(r"readme|notes?\b|dictionary|manifest", f, re.I) and
                            f not in (DOC.F_NOTES,)], wb_reg.sheetnames)
    resolvable = all(r["employee_id"] in mp or r["employee_id"] in reg_ids for r in pay if r["employee_id"].isdigit())
    C("B8 every legacy employee number in the payroll is in the HRIS map or the register", resolvable)
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
    ws3 = wb["Other PT bonuses 2023-2025"]
    pb, ptot, yy = {}, {}, None
    for r in ws3.iter_rows(min_row=4, values_only=True):
        if isinstance(r[0], int) and r[1]:
            yy = r[0]
            pb[(r[0], r[1])] = r[7]
        elif r[1] and str(r[1]).startswith("Total"):
            ptot[int(str(r[1]).split()[-1])] = r[7]
    C("GD3 the workbook's payments equal the ask, row by row and in total", pb == {
        (y, DL.plain(n)): round(v) for (y, n), v in B.items() if v} and ptot == {y: round(v) for y, v in BT.items()},
      (pb, ptot))
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
