"""task179 independent verifier: its own readers (the csv module and openpyxl), its own repeat-classmate count (pair
counting per class), statsmodels' IRLS for the logistic model, its own teaching-group and continuing-student counts.
Recomputes every graded figure in figures.json from target/ alone. Exit 1 on a mismatch.

    python3 task179/generator/verify.py [target]"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict
from itertools import combinations

import numpy as np
import openpyxl
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
FAC = {"FASS": "ass", "FBUS": "bus", "FSCI": "sci", "FENG": "eng", "FHLT": "hlt",
       "ASS": "ass", "BUS": "bus", "SCI": "sci", "ENG": "eng", "HLT": "hlt"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    P = lambda f: os.path.join(target, f)
    bad = []
    # census: enrolled ids by year
    enrolled = defaultdict(set)
    c26 = []
    for r in rows(P("census_enrolments_2019_2026.csv")):
        d = r["CENSUS_DATE"]
        y = int(d[-4:]) if "/" in d else int(d[:4])
        if r["STATUS"] in ("EN", "Enrolled"):
            enrolled[y].add(r["STUDENT_ID"])
        if y == 2026 and r["STATUS"] == "Enrolled" and int(r["YEAR_OF_STUDY"]) >= 2:
            c26.append(r)
    xw = {r["SIRIUS_STUDENT_NO"]: r["ARC_ID"] for r in rows(P("sirius_arc_student_crosswalk.csv"))}
    # admissions
    wb = openpyxl.load_workbook(P("admissions_entrants_2019_2026.xlsx"), read_only=True)
    ent = {}
    for ws in wb.worksheets:
        y = int(ws.title[:4])
        it = ws.iter_rows(values_only=True)
        head = list(next(it))
        for v in it:
            rec = dict(zip(head, v))
            if rec["Entry Basis"] != "First-time":
                continue
            sid = str(rec.get("Student No") or rec.get("Student ID"))
            if sid not in enrolled[y]:
                continue
            asc = rec.get("ASC Points") or rec.get("ASC Score")
            dob = rec["Date of Birth"]
            acc = rec["Offer Accepted"]
            ent[(y, sid)] = dict(asc=float(asc), fif=rec["First in Family"] == "Y", pt=rec["Attendance"] == "PT",
                                 hard=rec["Hardship Grant"] == "Y", lc=rec["Living-Learning Community"] == "Y",
                                 hall=rec["Accommodation"] not in ("Family home", "Private"),
                                 mature=(y - dob.year) >= 21, acc=(acc - dt.datetime(y, 1, 1)).days, fac=rec["Faculty"])
    # classes and repeat classmates
    members = defaultdict(list)
    for r in rows(P("sirius_fy_cohort_classes_2019_2025.csv")):
        members[(int(r["COHORT_YR"]), r["TERM"] + "/" + r["CLASS_NBR"])].append(r["STUDENT_NO"])
    for r in rows(P("arc_s1_2026_first_year_classes.csv")):
        members[(2026, r["class_code"])].append(r["arc_student_id"])
    shared = defaultdict(int)
    for (y, _), ms in members.items():
        for a, b in combinations(sorted(ms), 2):
            shared[(y, a, b)] += 1
    rep = defaultdict(int)
    for (y, a, b), n in shared.items():
        if n >= 2:
            rep[(y, a)] += 1
            rep[(y, b)] += 1
    # progress ratings
    val = {"S": 0, "C": 1, "R": 2, "Satisfactory": 0, "Some concern": 1, "At risk": 2}
    pr = defaultdict(list)
    for r in rows(P("progress_check_wk6_2019_2026.csv")):
        if r["RATING"] in val:
            pr[(int(r["YEAR"]), r["STUDENT"])].append(val[r["RATING"]])
    edges = [0, 1, 2, 3, 4, 6, 9, 15, 22, 10 ** 9]
    X, yv, Xf = [], [], []
    for (y, sid), e in sorted(ent.items()):
        t = rep.get((y, sid), 0)
        band = [1.0 if lo <= t < hi else 0.0 for lo, hi in zip(edges[:-1], edges[1:])][1:]
        ps = pr.get((y, sid))
        row = [1.0, (e["asc"] - 186) / 34, e["fif"], e["pt"], e["mature"], e["hard"], np.mean(ps) if ps else 0.5,
               e["lc"], e["hall"], e["acc"] / 100.0] + [float(e["fac"] == f) for f in ("BUS", "SCI", "ENG", "HLT")] + band
        if y == 2026:
            Xf.append(row)
        else:
            X.append(row)
            nxt = enrolled[y + 1] if y < 2025 else enrolled[2026]
            key = sid if y < 2025 else xw.get(sid)
            yv.append(0.0 if key in nxt else 1.0)
    m = sm.GLM(np.array(yv), np.array(X, float), family=sm.families.Binomial()).fit()
    call = float(m.predict(np.array(Xf, float)).sum())
    printed = int(250 * round(call / 250.0))
    if printed != figs["call_not_enrolled_2027"]:
        bad.append("call %.1f" % call)
    if len(Xf) != figs["cc1_intake_2026_at_census"]:
        bad.append("intake %d" % len(Xf))
    none2026 = sum(1 for (y, sid) in ent if y == 2026 and rep.get((y, sid), 0) == 0)
    if none2026 != figs["cc2_intake_2026_no_repeat_classmate"]:
        bad.append("no repeat %d" % none2026)
    # teaching groups: classes meeting in one room, on one day, at one start and over the same weeks are one group
    ws = openpyxl.load_workbook(P("s1_2026_class_timetable.xlsx"), read_only=True).worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = list(next(it))
    slot_classes = defaultdict(set)
    info = {}
    for v in it:
        rec = dict(zip(head, v))
        if rec["Class Status"] != "Active":
            continue
        info[rec["Class Code"]] = (rec["Owning Faculty"], rec["Enrolled at Census"])
        slot_classes[(rec["Room"], rec["Day"], rec["Start"], rec["Teaching Weeks"])].add(rec["Class Code"])
    comp = {c: {c} for c in info}
    for cs in slot_classes.values():
        cs = list(cs)
        merged = set().union(*(comp[c] for c in cs))
        for c in merged:
            comp[c] = merged
    groups = {frozenset(s) for s in comp.values()}
    cnt = defaultdict(lambda: [0, 0])
    for gset in groups:
        fac = FAC[info[next(iter(gset))][0]]
        n = sum(info[c][1] for c in gset)
        cnt[fac][0] += 1
        cnt[fac][1] += n > 30
    for f in ("ass", "bus", "sci", "eng", "hlt"):
        if cnt[f][0] != figs["ask_groups_s1_2026_%s" % f]:
            bad.append("groups %s %d" % (f, cnt[f][0]))
        if cnt[f][1] != figs["ask_groups_over30_s1_2026_%s" % f]:
            bad.append("over30 %s %d" % (f, cnt[f][1]))
    # continuing students
    cat = rows(P("programme_catalogue_2026.csv"))
    pfac = {r["CODE"]: FAC[r["OWNING_FACULTY"]] for r in cat if r["TYPE"] == "Programme"}
    combo = {frozenset(r["COMPONENTS"].split(";")): r["COMPONENTS"].split(";")[0] for r in cat if r["TYPE"] == "Conjoint"}
    trf = defaultdict(list)
    for r in rows(P("programme_transfers_2025_2026.csv")):
        trf[r["STUDENT"]].append((r["FROM_PROGRAMME"], r["TO_PROGRAMME"]))
    by = defaultdict(list)
    for r in c26:
        by[r["STUDENT_ID"]].append(r)
    cont = defaultdict(int)
    for sid, rs in by.items():
        progs = {r["PROGRAMME"] for r in rs}
        yos = min(int(rs[0]["YEAR_OF_STUDY"]), 4)
        if len(progs) == 1:
            p = progs.pop()
        else:
            moves = [t for (f_, t) in trf.get(sid, []) if f_ in progs and t in progs]
            p = moves[-1] if moves else combo[frozenset(progs)]
        cont[(pfac[p], yos)] += 1
    for f in ("ass", "bus", "sci", "eng", "hlt"):
        for yy in (2, 3, 4):
            k = "ask_continuing_2026_%s_y%d" % (f, yy)
            if cont[(f, yy)] != figs[k]:
                bad.append("%s %d" % (k, cont[(f, yy)]))
    print("verify: call %.1f -> %d, intake %d, %d graded figures checked, %d failed%s"
          % (call, printed, len(Xf), 3 + 10 + 15, len(bad), (": " + "; ".join(bad)) if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
