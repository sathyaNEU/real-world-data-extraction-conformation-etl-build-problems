"""task270 assertions on the built pack: the input gates, the call and its margins, every semantic fork row (SF1 to
SF17), the ladder, the three rules on the clean truth (R1, R2, R3), the separation of the asks from the call, the
asks' devices, the cells, the goldens against figures.json, and the realism sweep.

    python3 task270/generator/checks.py"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc        # noqa: E402
import common as K  # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    files = sorted(os.listdir(T))
    # ------------------------------------------------------------------ input gates
    ok("GATE files >= 10", len(files) >= 10, len(files))
    ok("GATE formats >= 3", len({f.rsplit(".", 1)[1] for f in files}) >= 3, {f.rsplit(".", 1)[1] for f in files})
    with open(os.path.join(T, K.F_DEATHS), encoding="utf-8") as fh:
        n_deaths = sum(1 for _ in fh) - 1
    ok("GATE a file of 25,000 rows", n_deaths >= 25000, n_deaths)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("GATE distractors >= 2, named in metadata, not in file names as such", len(meta["distractor_files"]) >= 2
       and all(d in files for d in meta["distractor_files"]), meta["distractor_files"])
    ok("GATE no file describes the data", not any(re.search(r"readme|dictionary|notes|manifest|schema", f, re.I)
                                                  for f in files), files)
    # ------------------------------------------------------------------ the call
    out, deaths, C, E = calc.rungs(T)
    areas = sorted(K.AREA_NAMES)
    gold = sorted(a for a in areas if out[a]["G"] < K.LINE)
    ok("CALL golden set", gold == sorted(["Coldwater Plains", "Dunesford", "Saltwick Shoals", "Windermoor"]), gold)
    ok("CALL figures.json carries the call", F["call"] == gold, F["call"])
    below = max(out[a]["G"] for a in gold)
    above = min(out[a]["G"] for a in areas if a not in gold)
    ok("CALL margin below the line >= 0.08", K.LINE - below >= 0.08, round(K.LINE - below, 3))
    ok("CALL margin above the line >= 0.08", above - K.LINE >= 0.08, round(above - K.LINE, 3))
    # ------------------------------------------------------------------ the semantic forks
    sf1 = sorted(a for a in areas if out[a]["C"] < K.LINE)
    ok("SF1 the crude closure names another set (ruled out by 3.2)", sf1 != gold and "Cobbleton" in sf1, sf1)
    by_code, by_name = calc.read_corr(T)
    sf2_deaths = _by_registration_year(by_code, deaths)
    sf2 = _call_with(sf2_deaths, deaths, C, E)
    ok("SF2 registration year gives the same call", sf2 == gold, sf2)
    sf3 = _call_with([d for d in deaths if d[5] == "NSW"], deaths, C, E)
    ok("SF3 the extract alone gives the same call", sf3 == gold, sf3)
    ages_ok = all(calc.age_on(d[2], d[3]) == d[4] for d in deaths if d[2] is not None)
    ok("SF4 age at death is completed years at the date of death on every record", ages_ok)
    sf5 = sorted(a for a in areas if out[a]["G_closed"] < K.LINE)
    ok("SF5 the unscaled rebuild gives the same call", sf5 == gold, sf5)
    for sf, key in (("SF6", "G_nosplit"), ("SF7", "G_bysex"), ("SF8", "G_dropdob"), ("SF9", "G_floor"),
                    ("SF10", "G_ax45")):
        same_set = sorted(a for a in areas if out[a][key] < K.LINE) == gold
        same_cells = all(round(out[a][key], 1) == round(out[a]["G"], 1) for a in areas)
        spread = max(abs(out[a][key] - out[a]["G"]) for a in areas)
        ok("%s %s gives the same call and every cell" % (sf, key), same_set and same_cells, round(spread, 4))
    exp_set = sorted(a for a in areas if calc.life_e85_reading(out[a]["D"] / out[a]["E"], "exp") < K.LINE)
    exp_cells = all(round(calc.life_e85_reading(out[a]["D"] / out[a]["E"], "exp"), 1) == round(out[a]["G"], 1)
                    for a in areas)
    ok("SF10 a constant rate through each year of age gives the same call and every cell", exp_set == gold and exp_cells)
    qm_set = sorted(a for a in areas if calc.life_e85_reading(out[a]["D"] / out[a]["E"], "qm") < K.LINE)
    ok("SF10 the rate read as the probability of dying names another set (ruled out by 3.2)", qm_set != gold, qm_set)
    hc_set = sorted(a for a in areas if calc.life_e85_reading(out[a]["D"] / out[a]["E"], "halfclose") < K.LINE)
    ok("SF18 95 and over closed with half a year names another set (ruled out by 3.2)", hc_set != gold, hc_set)
    n_nodob = sum(1 for d in deaths if d[2] is None and d[3].year in K.WINDOW and d[4] >= 85)
    ok("SF8 deaths at 85 and over in the window without a date of birth are few", 0 < n_nodob <= 30, n_nodob)
    ok("SF11 no area within 0.08 of the line", all(abs(out[a]["G"] - K.LINE) >= 0.08 for a in areas))
    sf12 = _call_with(_by_registry_field(deaths), deaths, C, E)
    ok("SF12 the registry's LGA field gives the same call", sf12 == gold, sf12)
    sf13 = []
    for a in areas:
        D = out[a]["D"]
        Ex = calc.reconstruct(C, deaths, E, a)
        sf13.append(a) if calc.life_e85(D / Ex) < K.LINE else None
    ok("SF13 the three 30 Junes summed (the golden's base) reproduce the call", sorted(sf13) == gold)
    rows = calc.read_ah(T)
    v0, r30 = calc.ah_golden(rows, by_code)
    same = all(calc.ah_golden(rows, by_code, gap_min=g)[0] == v0 for g in (10, 30, 60, 90))
    ok("SF14 any gap from 0 to 90 minutes gives the same visits", same)
    by_case = {}
    for r in rows:
        by_case.setdefault(r["case_ref"], []).append(r)
    gaps = []
    for rs in by_case.values():
        rs = sorted(rs, key=lambda r: r["arrived_at"])
        end = None
        for r in rs:
            arr, dep = calc._ts(r["arrived_at"]), calc._ts(r["departed_at"])
            if end is not None:
                gaps.append((arr - end).total_seconds() / 60)
            end = dep if end is None or arr > end else max(end, dep)
    ok("SF14 every later arrival on a case comes while a clinician is there or 90 minutes or more after",
       all(g <= 0 or g >= 90 for g in gaps), (round(max([g for g in gaps if g <= 0], default=0), 1),
                                              round(min([g for g in gaps if g > 0], default=0), 1)))
    straddle = sum(1 for r in rows if len({r["requested_at"][:4], r["arrived_at"][:4], r["departed_at"][:4]}) > 1)
    ok("SF15 no attendance's request, arrival and departure straddle a year end", straddle == 0, straddle)
    ok("SF16 every resident attendance carries a residence SA2 and an age",
       all(r["residence_sa2_code"] and r["age_at_attendance"] for r in rows))
    paths = calc.ah_paths(rows, by_code)
    ok("SF17 counting client keys differs from residents in every area",
       all(paths["residents_keys"][a] != r30[a] for a in areas))
    # ------------------------------------------------------------------ the ladder
    ladder = {k: sorted(a for a in areas if out[a][k] < K.LINE) for k in ("C", "R1", "R2", "R2s")}
    ok("LADDER no cheap rung names the golden set", all(v != gold for v in ladder.values()), ladder)
    ok("LADDER the default path (R2) ends on Coldwater Plains, Spraymouth and Windermoor",
       ladder["R2"] == ["Coldwater Plains", "Spraymouth", "Windermoor"], ladder["R2"])
    ok("LADDER the default split misses Spraymouth by 0.3 or more", out["Spraymouth"]["G"] - out["Spraymouth"]["R2"]
       >= 0.3, round(out["Spraymouth"]["G"] - out["Spraymouth"]["R2"], 3))
    ok("LADDER the default split puts Saltwick Shoals above the line by 0.1 or more",
       out["Saltwick Shoals"]["R2"] - K.LINE >= 0.1, round(out["Saltwick Shoals"]["R2"], 3))
    # ------------------------------------------------------------------ cells and figures
    for a in areas:
        g = out[a]["G"]
        ok("CELL %s clears its one-decimal edge by 0.02" % a, 0.05 - abs(g - round(g, 1)) >= 0.02, round(g, 4))
        ok("FIG %s life expectancy" % a, F["e85"][a] == round(g, 1), (F["e85"][a], round(g, 3)))
    gv, gr = calc.ah_golden(rows, by_code)
    ok("FIG visits", F["visits"] == gv)
    ok("FIG residents", F["residents"] == gr)
    _check_goldens(F)
    # ------------------------------------------------------------------ the asks' devices and separation
    _devices(rows, by_code, areas)
    src = open(os.path.join(HERE, "calc.py")).read()
    rungs_src = src[src.index("def rungs("):src.index("# -----", src.index("def rungs("))]
    ok("SEPARATION the call's computation never reads the after-hours file", "F_AH" not in rungs_src
       and "read_ah" not in rungs_src)
    # ------------------------------------------------------------------ the three rules on the clean truth
    _three_rules(out)
    # ------------------------------------------------------------------ realism
    _realism(files, deaths)
    fails = [r for r in RESULTS if not r[1]]
    for label, good, detail in RESULTS:
        if not good:
            print("FAIL", label, detail)
    print("%d of %d checks pass" % (len(RESULTS) - len(fails), len(RESULTS)))
    return 1 if fails else 0


def _call_with(dsel, deaths, C, E):
    res = []
    for a in K.AREA_NAMES:
        D = calc.deaths_by_age(dsel, a)
        if calc.life_e85(D / calc.reconstruct(C, deaths, E, a)) < K.LINE:
            res.append(a)
    return sorted(res)


def _by_registration_year(by_code, deaths):
    out = []
    with open(os.path.join(T, K.F_DEATHS), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            area = by_code.get(r["usual_residence_sa2_code"])
            if area is None:
                continue
            out.append((area, r["sex"], None, dt.date(int(r["registration_date"][:4]), 7, 1), int(r["age_at_death"]),
                        "NSW"))
    wb = openpyxl.load_workbook(os.path.join(T, K.F_INTERSTATE), read_only=True)
    head = None
    for row in wb["Deaths"].iter_rows(values_only=True):
        if head is None:
            head = list(row) if row and row[0] == "State of registration" else None
            continue
        if row[0] is None:
            continue
        rec = dict(zip(head, row))
        area = by_code.get(str(rec["Usual residence SA2 code (ASGS 2021)"]))
        if area:
            reg = rec["Date of registration"]
            out.append((area, rec["Sex"], None, dt.date(reg.year, 7, 1), int(rec["Age at death"]), "X"))
    wb.close()
    return out


def _by_registry_field(deaths):
    out = []
    with open(os.path.join(T, K.F_DEATHS), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["usual_residence_lga_name"] not in K.AREA_NAMES:
                continue
            dob = dt.date.fromisoformat(r["date_of_birth"]) if r["date_of_birth"] else None
            out.append((r["usual_residence_lga_name"], r["sex"], dob, dt.date.fromisoformat(r["date_of_death"]),
                        int(r["age_at_death"]), "NSW"))
    return out + [d for d in deaths if d[5] != "NSW"]


def _devices(rows, by_code, areas):
    by_case = {}
    for r in rows:
        by_case.setdefault(r["case_ref"], []).append(r)
    co = {a: 0 for a in areas}
    ret = {a: 0 for a in areas}
    for case, rs in by_case.items():
        a = by_code.get(rs[0]["residence_sa2_code"])
        if a is None or int(rs[0]["age_at_attendance"]) < 85 or len(rs) < 2:
            continue
        rs = sorted(rs, key=lambda r: r["arrived_at"])
        t = [dt.datetime.fromisoformat(r["arrived_at"][:19]) for r in rs]
        if any((t[i + 1] - t[i]).total_seconds() <= 300 for i in range(len(t) - 1)):
            co[a] += 1
        if any((t[i + 1] - t[i]).total_seconds() >= 6000 for i in range(len(t) - 1)):
            ret[a] += 1
    ok("DEVICE A1 every area has clinicians arriving together and returns on a case",
       all(co[a] > 0 and ret[a] > 0 for a in areas), (co, ret))
    gaps = []
    for case, rs in by_case.items():
        rs = sorted(rs, key=lambda r: r["arrived_at"])
        for i in range(len(rs) - 1):
            g = (dt.datetime.fromisoformat(rs[i + 1]["arrived_at"][:19]) -
                 dt.datetime.fromisoformat(rs[i]["arrived_at"][:19])).total_seconds() / 60
            gaps.append(g)
    ok("DEVICE A1 arrivals together are under 5 minutes apart and returns over 100 minutes after",
       all(g < 5 or g >= 100 for g in gaps), (min(gaps), max(g for g in gaps if g < 100) if gaps else None))
    two = {a: set() for a in areas}
    for r in rows:
        a = by_code.get(r["residence_sa2_code"])
        if a and int(r["age_at_attendance"]) >= 85 and r["external_id"]:
            two[a].add(r["external_id"])
    h1 = {r["client_key"] for r in rows if r["arrived_at"] < "2026-07-01"}
    ok("DEVICE A2 every area has residents seen under both keys", all(len(two[a] & h1) > 0 for a in areas))
    paths = calc.ah_paths(rows, by_code)
    _, gr = calc.ah_golden(rows, by_code)
    ok("DEVICE A2 the over-clean (birth month, sex, SA2) misses every area",
       all(paths["residents_attrs"][a] != gr[a] for a in areas))
    gv, _ = calc.ah_golden(rows, by_code)
    ok("DEVICE A1 counting rows and counting cases both miss every area",
       all(paths["visits_rows"][a] != gv[a] and paths["visits_cases"][a] != gv[a] for a in areas))
    ok("DEVICE no external identifier on a January to June row",
       all(not r["external_id"] for r in rows if r["arrived_at"] < "2026-07-01"))


def _three_rules(out):
    import world as W
    import records as R
    import build as B
    A, P, Y = B.world()
    areas = sorted(K.AREA_NAMES)
    truth = {}
    for a in A:
        ia = P["area"] == a.i
        Et = np.zeros(calc.NA)
        for y in K.WINDOW:
            on = W.alive_on(P, dt.date(y, 6, 30)) & ia
            ag = np.minimum(W.ages_on_fast(P, dt.date(y, 6, 30)), K.TOP)
            Et += np.bincount(ag[on & (ag >= 85)] - 85, minlength=calc.NA)[:calc.NA]
        truth[a.name] = Et
    gold = sorted(a for a in areas if out[a]["G"] < K.LINE)
    clean = sorted(a for a in areas if calc.life_e85(out[a]["D"] / truth[a]) < K.LINE)
    ok("R1 the field's raw material ships: deaths with dates of birth, census single years, estimates to 85 and over",
       all(k in calc.read_erp(T)[(2026, "Windermoor", "P")] for k in ("85 and over",))
       and not any(k in calc.read_erp(T)[(2026, "Windermoor", "P")] for k in ("85-89", "90-94")))
    ok("R2 on the clean truth (the true population at each age) the golden set stands", clean == gold, clean)
    # the easy route on the clean truth: the census split with the true census-night population, no adjustment
    cen = {}
    on = W.alive_on(P, K.CENSUS)
    ag = np.minimum(W.ages_on_fast(P, K.CENSUS), K.TOP)
    for a in A:
        v = np.bincount(ag[on & (P["area"] == a.i) & (ag >= 85)] - 85, minlength=calc.NA)[:calc.NA].astype(float)
        cen[a.name] = v / v.sum()
    easy = sorted(a for a in areas if calc.life_e85(out[a]["D"] / (cen[a] * truth[a].sum())) < K.LINE)
    ok("R3 the easy route on the clean truth still files the wrong set", easy != gold, easy)
    ok("R3 the easy route on the clean truth names Spraymouth", "Spraymouth" in easy, easy)


def _check_goldens(F):
    wb = openpyxl.load_workbook(os.path.join(TASK, "golden", K.G_BOOK), read_only=True)
    ws = wb["Area list"]
    seen = 0
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[1] in K.AREA_NAMES:
            a = row[1]
            seen += 1
            ok("GOLDEN %s row agrees with figures.json" % a, row[2] == F["e85"][a] and row[3] == F["qualifies"][a]
               and row[4] == F["visits"][a] and row[5] == F["residents"][a], row)
    ok("GOLDEN workbook has all twelve areas", seen == 12, seen)
    wb.close()
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("WRITEUP no em or en dash", "—" not in sub and "–" not in sub)


def _realism(files, deaths):
    from pypdf import PdfReader
    text = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, K.F_GUIDE)).pages)
    flat = re.sub(r"\s+", " ", text)
    for s in ("95 and over as the last group", "wherever the death was registered", "estimated resident population of"
              " that age at 30 June 2024, 30 June 2025 and 30 June 2026", "fewer than seven more years",
              "a person who dies at an age has lived half of that year of age",
              "the survivors to 95 divided by that group's death rate"):
        ok("DOC guidelines carry: %s" % s, s in flat)
    for p in K.PEOPLE.values():
        ok("DOC persona %s in the guidelines" % p, p in flat)
    bad = []
    for f in files:
        if f.endswith(".csv"):
            t = open(os.path.join(T, f), encoding="utf-8").read()
            if "—" in t or "–" in t or re.search(r"fictional|constructed|this exercise", t, re.I):
                bad.append(f)
    if "—" in flat or "–" in flat or re.search(r"fictional|fictitious|this exercise", flat, re.I):
        bad.append(K.F_GUIDE)
    ok("REALISM no dash or out-of-fiction word under target", not bad, bad)
    tot = {}
    for d in deaths:
        tot[d[0]] = tot.get(d[0], 0) + 1
    ok("REALISM no two areas share a death total", len(set(tot.values())) == len(tot), tot)
    regs_ok = True
    with open(os.path.join(T, K.F_DEATHS), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["registration_date"] < r["date_of_death"] or r["registration_date"] > K.EXTRACT_TO.isoformat():
                regs_ok = False
                break
    ok("REALISM every registration on or after its death and by 30 June 2027", regs_ok)
    with open(os.path.join(T, K.F_DEATHS), encoding="utf-8") as fh:
        numbers = [r["registration_number"] for r in csv.DictReader(fh)]
    ok("REALISM every registration number is unique", len(set(numbers)) == len(numbers), len(numbers) - len(set(numbers)))
    with open(os.path.join(T, K.F_AH), encoding="utf-8") as fh:
        neg = sum(1 for r in csv.DictReader(fh) if int(r["age_at_attendance"]) < 0)
    ok("REALISM no attendance before the client's birth", neg == 0, neg)
    late = [d for d in deaths if d[3].year == 2026 and d[4] >= 85]
    ok("MATURITY every 2026 death at 85 and over is in the extract window", len(late) > 0)


if __name__ == "__main__":
    sys.exit(main())
