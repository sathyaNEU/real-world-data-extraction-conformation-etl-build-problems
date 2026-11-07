"""task445 architecture 3: the golden, computed from target/ alone, and the three deliverables.

Every route the checks price is a parameter: how an optional question's demand is read (the candidates who answered
all three essays; question means; a Section A adjustment; the pairs each two-essay candidate answered), which marking
event stands, and how the asks read the files."""
import csv
import datetime as dt
import io
import json
import os
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
QS = ["4", "5", "6"]
BOUNDS = [("A", 66), ("B", 57), ("C", 48), ("D", 39), ("E", 30)]
LINE = 1.5
OFFSETS = {"Australia/Darwin": 9.5, "Australia/Brisbane": 10.0, "Australia/Perth": 8.0, "Pacific/Fiji": 12.0,
           "Pacific/Port_Moresby": 10.0, "Pacific/Efate": 11.0, "Pacific/Guadalcanal": 11.0, "Asia/Jakarta": 7.0,
           "Asia/Dili": 9.0, "Asia/Kuala_Lumpur": 8.0, "Asia/Singapore": 8.0}
REGIONS = ["NT", "QT", "WA", "PC", "ID", "MS"]
MONTHS = [(2025, 12), (2026, 1), (2026, 2)]


def rd(x):
    return int(np.floor(x + 0.5))


def _read(target, name):
    return list(csv.DictReader(open(os.path.join(target, name), encoding="utf-8")))


def load(target=TARGET):
    marks = _read(target, "p2_essay_marks_2026.csv")
    seca = {r["candidate_no"]: int(r["section_a_total"]) for r in _read(target, "p2_section_a_scan_2026.csv")}
    cen = _read(target, "aeb_centres_register.csv")
    region = {}
    tz = {}
    for r in cen:
        region[r["centre_code"]] = r["region_code"]
        tz[r["centre_code"]] = r["time_zone"]
        if r["merged_from"]:
            region[r["merged_from"]] = r["region_code"]
            tz[r["merged_from"]] = r["time_zone"]
            region.setdefault("_cur_" + r["merged_from"], r["centre_code"])
    cur = {r["merged_from"]: r["centre_code"] for r in cen if r["merged_from"]}
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, "asc_history_entries_2026.xlsx"), read_only=True)["Entries"]
    later, entered = {}, {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        no, prev, centre, status = row[0], row[1], row[2], row[3]
        if status == "ENTERED":
            entered[no] = centre
            if prev:
                later[prev] = no
    return dict(marks=marks, seca=seca, region=region, tz=tz, cur=cur, target=target, later=later, entered=entered)


def essays(D, stand="senior", join=True):
    """Final mark per candidate and question: the senior examiner's re-mark stands (stand='senior'), or the first
    mark (stand='first'); absent candidates carry no essay."""
    out = defaultdict(dict)
    centre = {}
    absent = set()
    rank = {"FIRST": 0, "SENIOR": 1}
    seen = {}
    for r in D["marks"]:
        c = D["later"].get(r["candidate_no"], r["candidate_no"]) if join else r["candidate_no"]
        centre[c] = D["entered"].get(c, r["centre_code"]) if join else r["centre_code"]
        if r["script_status"] == "ABSENT":
            absent.add(c)
            continue
        q = r["question"][1:]
        k = (c, q)
        e = rank[r["marking_event"]]
        if stand == "first" and e == 1:
            continue
        if k not in seen or e >= seen[k]:
            seen[k] = e
            out[c][q] = int(r["mark"])
    return out, centre, absent


def demand(E, seca, how="all_three"):
    """Each optional question's demand against the others taken together (marks), by the route named."""
    if how == "all_three":
        rows = [m for m in E.values() if len(m) == 3]
        return {q: float(np.mean([(sum(m[o] for o in QS if o != q) / 2.0) - m[q] for m in rows])) for q in QS}, len(rows)
    if how == "means":
        mu = {q: np.mean([m[q] for m in E.values() if q in m]) for q in QS}
        return {q: float(np.mean([mu[o] for o in QS if o != q]) - mu[q]) for q in QS}, None
    if how == "section_a":
        y, X = [], []
        for c, m in E.items():
            for q, v in m.items():
                y.append(v)
                X.append([1.0, seca.get(c, 0), q == "5", q == "6"])
        b = np.linalg.lstsq(np.array(X, float), np.array(y, float), rcond=None)[0]
        eff = {"4": 0.0, "5": b[2], "6": b[3]}
        return {q: float(np.mean([eff[o] for o in QS if o != q]) - eff[q]) for q in QS}, None
    if how == "pairs":
        diff = defaultdict(list)
        for m in E.values():
            if len(m) == 2:
                a, b = sorted(m)
                diff[(a, b)].append(m[a] - m[b])
        d = {k: float(np.mean(v)) for k, v in diff.items()}
        eff = {"4": 0.0, "5": -d[("4", "5")], "6": -d[("4", "6")]}
        return {q: float(np.mean([eff[o] for o in QS if o != q]) - eff[q]) for q in QS}, None
    raise ValueError(how)


def scaling(dem):
    return {q: (rd(v) if v >= LINE else 0) for q, v in dem.items()}


def grade(total):
    for g, b in BOUNDS:
        if total >= b:
            return g
    return "U"


def sat_set(D, E, absent):
    """Every candidate present for the paper: an essay marked, or Section A scanned (code 2.3)."""
    return sorted((set(E) | set(D["seca"])) - absent)


def results(E, seca, centre, D, raise_by, absent=frozenset()):
    out = []
    for c in sat_set(D, E, set(absent)):
        if c not in centre:
            centre[c] = D["entered"][c]
        m = {q: min(25, v + raise_by.get(q, 0)) for q, v in E.get(c, {}).items()}
        best = sorted(m, key=lambda q: (-m[q], q))[:2]
        secb = sum(m[q] for q in best)
        sa = seca.get(c, 0)
        cc = D["cur"].get(centre[c], centre[c])
        out.append(dict(cand=c, centre=cc, region=D["region"][centre[c]], section_a=sa, marks=m, credited=best,
                        section_b=secb, total=sa + secb, grade=grade(sa + secb)))
    return out


def ask_entries(D, E, centre, absent):
    sat = Counter()
    ans = {q: Counter() for q in QS}
    for c in sat_set(D, E, set(absent)):
        r = D["region"][centre.get(c) or D["entered"][c]]
        sat[r] += 1
        for q in E.get(c, {}):
            ans[q][r] += 1
    return {r: dict(sat=sat[r], **{"q" + q: ans[q][r] for q in QS}) for r in REGIONS}


def ask_reviews(D, month_by="local"):
    rows = _read(D["target"], "post_results_reviews_2025.csv")
    req = Counter()
    gc = Counter()
    for r in rows:
        if r["component"] != "P2" or r["outcome"] == "WD":
            continue
        utc = dt.datetime.strptime(r["requested_utc"], "%Y-%m-%dT%H:%M:%SZ")
        t = utc + dt.timedelta(hours=OFFSETS[D["tz"][r["centre_code"]]]) if month_by == "local" else utc
        key = ((t.year, t.month), D["region"][r["centre_code"]])
        req[key] += 1
        if r["outcome"] == "GC":
            gc[key] += 1
    return {"%d-%02d" % m: {r: dict(requests=req[(m, r)], grade_changes=gc[(m, r)]) for r in REGIONS} for m in MONTHS}


def solve(target=TARGET):
    D = load(target)
    E, centre, absent = essays(D)
    dem, n3 = demand(E, D["seca"])
    raise_by = scaling(dem)
    res = results(E, D["seca"], centre, D, raise_by, absent)
    base = results(E, D["seca"], centre, D, {}, absent)
    gcount = Counter(r["grade"] for r in res)
    changed = sum(1 for a, b in zip(res, base) if a["grade"] != b["grade"])
    return dict(D=D, E=E, centre=centre, absent=absent, demand=dem, n_all_three=n3, raise_by=raise_by, results=res,
                grades={g: gcount.get(g, 0) for g in [g for g, _ in BOUNDS] + ["U"]}, changed=changed,
                entries=ask_entries(D, E, centre, absent),
                rungs={h: demand(E, D["seca"], h)[0] for h in ("means", "section_a", "pairs")})


def figures(S):
    return {"call": {"question_scaled": "6" if S["raise_by"]["6"] else "none", "raise_marks": S["raise_by"]["6"]},
            "demand_1dp": {q: "%.1f" % v for q, v in S["demand"].items()},
            "all_three_candidates": S["n_all_three"],
            "grades": S["grades"], "grade_changed": S["changed"],
            "candidates_graded": len(S["results"]),
            "stated": {"line": "1.5", "question_max": 25},
            "ask_a": S["entries"]}
