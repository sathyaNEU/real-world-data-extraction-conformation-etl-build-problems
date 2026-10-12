"""Independent verifier for task501: reads only the shipped bundle (the target folder) with the csv module, openpyxl and
pdfplumber, shares no code with the generator, recomputes the call and every ask figure, and compares them with
generator/figures.json.

    python3 task501/generator/verify.py <target> <figures.json>"""
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np

GROUPS = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54),
          (55, 59), (60, 64), (65, 69), (70, 200)]
OPTS = {"A": (2013, 2017), "B": (2008, 2012), "C": (2003, 2007), "D": (1993, 1997), "E": (1993, 2002)}


def rows(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def find(target, prefix):
    return [f for f in os.listdir(target) if f.startswith(prefix)][0]


def group(a):
    return next(i for i, (lo, hi) in enumerate(GROUPS) if lo <= a <= hi)


def call(target):
    prof = {}
    for r in rows(target, find(target, "measles_immunity_profile")):
        y = 1927 if "earlier" in r["year_of_birth"] else int(r["year_of_birth"])
        prof[y] = float(r["per_cent_immune"]) / 100
    N = np.zeros(15)
    S = np.zeros(15)
    by_yob = {}
    for r in rows(target, find(target, "population_projection")):
        a = 100 if "over" in r["age_at_1_january_2028"] else int(r["age_at_1_january_2028"])
        y = 1927 if "earlier" in r["year_of_birth"] else int(r["year_of_birth"])
        n = int(r["persons"])
        g = group(a)
        N[g] += n
        S[g] += n * (1 - prof[y])
        by_yob[y] = by_yob.get(y, 0) + n
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(target, find(target, "nscs_2023")), read_only=True)["Table 2"]
    M = np.array([[float(x) for x in r[1:16]] for r in ws.iter_rows(min_row=3, max_row=17, values_only=True)])
    import pdfplumber
    with pdfplumber.open(os.path.join(target, find(target, "mmr_catch_up_options"))) as pdf:
        text = " ".join((p.extract_text() or "") for p in pdf.pages)
    text = re.sub(r"\s+", " ", text)
    made = {}
    for m in re.finditer(r"(\d{4}) to (\d{4}) \d{1,2} to \d{1,2} .*?(\d{1,3}(?:,\d{3})+) (\d{1,3}(?:,\d{3})*) (\d{2})% "
                         r"(\d{1,3}(?:,\d{3})*)", text):
        span = (int(m.group(1)), int(m.group(2)))
        made.setdefault(span, []).append(int(m.group(6).replace(",", "")))
    eff = {"A": [((2013, 2017), made[(2013, 2017)][0])], "B": [((2008, 2012), made[(2008, 2012)][0])],
           "C": [((2003, 2007), made[(2003, 2007)][0])], "D": [((1993, 1997), made[(1993, 1997)][0])],
           "E": [((1993, 1997), made[(1993, 1997)][1]), ((1998, 2002), made[(1998, 2002)][0])]}
    q = 15.0 / max(abs(np.linalg.eigvals(M)))

    def R(Sg):
        return float(max(abs(np.linalg.eigvals(q * (Sg / N)[:, None] * M.T))))
    out = {"No catch-up": R(S)}
    for k, parts in eff.items():
        S2 = S.copy()
        for (a, b), mi in parts:
            g = group(2027 - b)
            assert g == group(2027 - a)
            S2[g] -= mi
        out["Option %s" % k] = R(S2)
    return out


def residents(target):
    cut = dt.date(2024, 7, 1)
    region = {"LH20", "LH21", "LH22", "LH23", "LH24", "LH25", "LH26"}
    codes = {r["lho_code"]: r["health_region"] for r in rows(target, find(target, "lho_codes"))}
    assert {c for c, h in codes.items() if h == "Oriel Health Region"} == region
    people = {}
    for r in rows(target, find(target, "register_people")):
        code, rec = r["lho_code"], dt.date.fromisoformat(r["lho_recorded"])
        here = code in region or (code == "LH27" and rec < cut)
        people[r["person_number"]] = (dt.date.fromisoformat(r["date_of_birth"]), here)
    return people


def doses(target, people):
    surv = {r["retired_number"]: r["surviving_number"] for r in rows(target, find(target, "register_merges"))}
    drop = {r["line_ref"] for r in rows(target, find(target, "gp_return_queries"))
            if r["outcome"] in ("Replaced by corrected line", "Withdrawn by practice")}
    asat = dt.date(2027, 6, 30)
    per = {}
    for r in rows(target, find(target, "register_mmr_events")):
        if r["source_ref"] in drop:
            continue
        d = dt.date.fromisoformat(r["date_given"])
        if d > asat:
            continue
        p = r["person_number"]
        while p in surv:
            p = surv[p]
        if p in people and people[p][1]:
            per.setdefault(p, []).append(d)
    count = {}
    for p, ds in per.items():
        dob = people[p][0]
        first = dt.date(dob.year + 1, dob.month, dob.day)
        n, prev = 0, None
        for d in sorted(ds):
            if d < first or (prev is not None and (d - prev).days < 28):
                continue
            n, prev = n + 1, d
        count[p] = n
    return count


def cases(target):
    rs = rows(target, find(target, "nds_measles_cases"))
    legacy = {r["legacy_ref"] for r in rs if r["legacy_ref"]}
    out = []
    for r in rs:
        if r["classification"] != "Confirmed":
            continue
        onset = dt.datetime.strptime(r["onset_date"], "%d/%m/%Y").date()
        if not (dt.date(2019, 1, 1) <= onset <= dt.date(2027, 6, 30)):
            continue
        m = re.search(r"Legacy no\.\s*(MZ\d{2}/\d{4})", r["comments"])
        if m and m.group(1) in legacy:
            continue
        out.append((dt.datetime.strptime(r["date_of_birth"], "%d/%m/%Y").date().year, r["importation"] == "Imported"))
    return out


def main(argv):
    target, figs_path = argv[0], argv[1]
    figs = json.load(open(figs_path, encoding="utf-8"))
    bad = []
    r = call(target)
    for k, v in r.items():
        shown = "%.1f" % (np.floor(v * 10 + 0.5) / 10)
        if shown != figs["reproduction_number"][k]:
            bad.append(("R " + k, shown, figs["reproduction_number"][k]))
    below = [k for k, v in r.items() if v < 1]
    if below != ["Option B"] or r["No catch-up"] < 1:
        bad.append(("call", below, "Option B"))
    people = residents(target)
    cnt = doses(target, people)
    cs = cases(target)
    for k, (a, b) in OPTS.items():
        res = [p for p, (dob, here) in people.items() if here and a <= dob.year <= b]
        n0 = sum(1 for p in res if cnt.get(p, 0) == 0)
        n1 = sum(1 for p in res if cnt.get(p, 0) == 1)
        conf = sum(1 for y, imp in cs if a <= y <= b)
        imp = sum(1 for y, i in cs if a <= y <= b and i)
        for label, val, key in (("residents", len(res), "ask1_register_residents"), ("none", n0, "ask2_no_valid_dose"),
                                ("one", n1, "ask2_one_valid_dose"), ("confirmed", conf, "ask3_confirmed_cases"),
                                ("imported", imp, "ask3_imported")):
            if int(figs[key][k].replace(",", "")) != val:
                bad.append((label + " " + k, val, figs[key][k]))
    if bad:
        for b in bad:
            print("VERIFY MISMATCH", b)
        raise SystemExit(1)
    print("VERIFY   independent recomputation matches figures.json: 6 reproduction numbers, the call, 25 ask figures")


if __name__ == "__main__":
    main(sys.argv[1:])
