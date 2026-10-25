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
    for r in rows(P("census_enrolments_2019_2026.csv")):
        d = r["CENSUS_DATE"]
        y = int(d[-4:]) if "/" in d else int(d[:4])
        if r["STATUS"] in ("EN", "Enrolled"):
            enrolled[y].add(r["STUDENT_ID"])
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
    base, tie, yv, isf = [], [], [], []
    for (y, sid), e in sorted(ent.items()):
        ps = pr.get((y, sid))
        base.append([1.0, (e["asc"] - 186) / 34, e["fif"], e["pt"], e["mature"], e["hard"], np.mean(ps) if ps else 0.5,
                     e["lc"], e["hall"], e["acc"] / 100.0] + [float(e["fac"] == f) for f in ("BUS", "SCI", "ENG", "HLT")])
        tie.append(rep.get((y, sid), 0))
        isf.append(y == 2026)
        if y < 2026:
            nxt = enrolled[y + 1] if y < 2025 else enrolled[2026]
            key = sid if y < 2025 else xw.get(sid)
            yv.append(0.0 if key in nxt else 1.0)
    base, tie, isf = np.array(base, float), np.array(tie, float), np.array(isf)

    def feats(form):
        if form.startswith("ge"):
            return (tie >= int(form[2:]))[:, None].astype(float)
        if form == "log":
            return np.log1p(tie)[:, None]
        if form == "sqrt":
            return np.sqrt(tie)[:, None]
        e = {"bands": [0, 1, 2, 3, 4, 6, 9, 15, 22, 10 ** 9], "bands5": [0, 1, 3, 6, 10, 10 ** 9]}[form]
        return np.column_stack([((tie >= lo) & (tie < hi)).astype(float) for lo, hi in zip(e[:-1], e[1:])][1:])
    fits = {}
    for form in ("bands", "bands5", "ge5", "ge7", "ge10", "ge15", "ge22", "log", "sqrt"):
        Xa = np.column_stack([base, feats(form)])
        m = sm.GLM(np.array(yv), Xa[~isf], family=sm.families.Binomial()).fit()
        fits[form] = (float(m.predict(Xa[isf]).sum()), float(m.aic))
    form = min(fits, key=lambda k: fits[k][1])
    call = fits[form][0]
    # SF12: the count-free model loses by far on the filed criterion, and the cutover notes carry no section 6;
    # SF13: the forms here printing outside the bin (the log, the 22-classmate indicator) lose to every form inside it
    m0 = sm.GLM(np.array(yv), base[~isf], family=sm.families.Binomial()).fit()
    if not float(m0.aic) - fits[form][1] > 800:
        bad.append("SF12 count-free model only %.1f AIC worse" % (float(m0.aic) - fits[form][1]))
    inside = [k for k in fits if int(250 * round(fits[k][0] / 250.0)) == figs["call_not_enrolled_2027"]]
    outside = [k for k in fits if k not in inside]
    if any(fits[k][1] <= max(fits[j][1] for j in inside) for k in outside):
        bad.append("SF13 a form outside the bin beats one inside: %s" % ", ".join(outside))
    from pypdf import PdfReader
    cut = " ".join(" ".join(p.extract_text().split()) for p in PdfReader(P("arc_cutover_notes_registry.pdf")).pages)
    if "6. Class enrolments" in cut or "choose their classes" in cut or "who chooses" in cut:
        bad.append("SF12 the cutover notes carry a class-enrolment section")
    # SF14: the count-free model misses the record's own entrants who meet fewer than 10 others twice
    yh = np.array(yv)
    th = tie[~isf]
    lowm = th < 10
    p_all = m0.predict(base[~isf][lowm]).sum()
    seg = figs["check_fewer_than_10_twice_2019_2025"]
    if (int(lowm.sum()) != seg["entrants"] or int(yh[lowm].sum()) != seg["not_enrolled"]
            or abs(p_all - seg["count_free_predicted"]) > 0.15):
        bad.append("SF14 segment check %d %d %.2f" % (lowm.sum(), yh[lowm].sum(), p_all))
    Xf = base[isf]
    printed = int(250 * round(call / 250.0))
    if printed != figs["call_not_enrolled_2027"]:
        bad.append("call %.1f (%s)" % (call, form))
    if len(Xf) != figs["cc1_intake_2026_at_census"]:
        bad.append("intake %d" % len(Xf))
    none2026 = sum(1 for (y, sid) in ent if y == 2026 and rep.get((y, sid), 0) == 0)
    if none2026 != figs["cc2_intake_2026_no_repeat_classmate"]:
        bad.append("no repeat %d" % none2026)
    # teaching groups, 200 level and above: each distinct set of active classes meeting together in one room at one
    # time (day, start, teaching weeks) is one group; its size is the students its classes list who hold an enrolled
    # programme attempt at the 2026 census
    ws = openpyxl.load_workbook(P("s1_2026_class_timetable.xlsx"), read_only=True).worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = list(next(it))
    slot_classes = defaultdict(set)
    info = {}
    for v in it:
        rec = dict(zip(head, v))
        if rec["Class Status"] != "Active" or int(rec["Level"]) < 200:
            continue
        info[rec["Class Code"]] = (rec["Owning Faculty"], int(rec["Level"]))
        slot_classes[(rec["Room"], rec["Day"], rec["Start"], rec["Teaching Weeks"])].add(rec["Class Code"])
    enrolled26 = {r["STUDENT_ID"] for r in rows(P("census_enrolments_2019_2026.csv"))
                  if r["CENSUS_DATE"] == "2026-10-01" and r["STATUS"] == "Enrolled"}
    members = defaultdict(set)
    for r in rows(P("arc_s1_2026_class_enrolments.csv")):
        members[r["class_code"]].add(r["arc_student_id"])
    cnt = defaultdict(int)
    for gset in {frozenset(s) for s in slot_classes.values()}:
        cs = sorted(gset)
        lv = min(info[c][1] for c in cs)
        size = len(set().union(*(members[c] for c in cs)) & enrolled26)
        tag = "200" if lv == 200 else "300up"
        cnt[(FAC[info[cs[0]][0]], tag, "over30" if size > 30 else "30orfewer")] += 1
    for f in ("ass", "bus", "sci", "eng", "hlt"):
        for tag in ("200", "300up"):
            for band in ("30orfewer", "over30"):
                k = "ask_groups_s1_2026_%s_%s_%s" % (f, tag, band)
                if cnt[(f, tag, band)] != figs[k]:
                    bad.append("%s %d" % (k, cnt[(f, tag, band)]))
    print("verify: call %.1f (%s) -> %d, intake %d, %d graded figures checked, %d failed%s"
          % (call, form, printed, len(Xf), 3 + 20, len(bad), (": " + "; ".join(bad)) if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
