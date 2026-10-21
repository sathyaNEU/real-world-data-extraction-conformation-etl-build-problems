"""Read the cut pack the way an analyst would, and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the conformed finance, enrollment, campus codes, credit hours and the fall census
    per_fte(b, route)       each campus's fiscal 2026 instruction expense per FTE under a route
    awarded(b, v)           the five lowest
    ask_a(b, dedup)         each branch campus's fall 2026 FTE
    ask_b(b, persons)       each branch campus's unduplicated fall 2026 headcount"""
import csv
import os

import numpy as np

FILES = {
    "f1a": "ipeds_f1a_fy2026_finance_lakemoor_public.csv",
    "e12": "ipeds_e12_2025-26_enrollment_lakemoor_public.csv",
    "codes": "lhecb_campus_codes_2026.csv",
    "ch": "lhecb_credit_hours_by_level_2025-26.csv",
    "census": "lhecb_fall2026_census_enrollment_branch_campuses.csv",
}
LEVELS = ("Lower division", "Upper division", "Graduate")
GOLDEN_FORMS = ("golden", "wls_fte", "with_intercept", "direct", "by_term")
ROUTES = GOLDEN_FORMS + ("fte_split", "credit_hour_split", "two_level", "exclude_children", "zero")


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load(target):
    f1a = {r["UNITID"]: r for r in _csv(os.path.join(target, FILES["f1a"]))}
    e12 = {r["UNITID"]: r for r in _csv(os.path.join(target, FILES["e12"]))}
    code = {r["campus_code"]: r["unitid"] for r in _csv(os.path.join(target, FILES["codes"]))}
    ch = {}
    chterm = {}
    for r in _csv(os.path.join(target, FILES["ch"])):
        u = code[r["campus_code"]]
        ch.setdefault(u, {lv: 0 for lv in LEVELS})[r["course_level"]] += int(r["student_credit_hours"])
        chterm.setdefault((u, r["term"]), {lv: 0 for lv in LEVELS})[r["course_level"]] += int(r["student_credit_hours"])
    ids = sorted(f1a)
    fte = {u: float(e12[u]["FTEUG"]) + float(e12[u]["FTEGD"]) for u in ids}
    inst = {u: float(f1a[u]["F1C011"]) for u in ids}
    kind = {u: ("P" if f1a[u]["PRCH_F"] == "1" else "C" if f1a[u]["PRCH_F"] == "2" else "S") for u in ids}
    parent = {u: f1a[u]["IDX_F"] for u in ids}
    census = _csv(os.path.join(target, FILES["census"]))
    return {"ids": ids, "fte": fte, "inst": inst, "kind": kind, "parent": parent, "ch": ch, "chterm": chterm,
            "code": code, "census": census, "e12": e12}


def systems(b):
    out = {}
    for u in b["ids"]:
        if b["kind"][u] == "P":
            out[u] = [u] + [c for c in b["ids"] if b["parent"][c] == u]
    return out


def fit(b, form="golden"):
    """Instruction expense per credit hour by level, fitted on the campuses that report alone."""
    S = [u for u in b["ids"] if b["kind"][u] == "S"]
    if form == "two_level":
        X = np.array([[b["ch"][u]["Lower division"] + b["ch"][u]["Upper division"], b["ch"][u]["Graduate"]]
                      for u in S], float)
    elif form == "by_term":
        rows, y = [], []
        for u in S:
            tot = sum(sum(b["chterm"][(u, t)].values()) for t in ("2025FA", "2026SP", "2026SU"))
            for t in ("2025FA", "2026SP", "2026SU"):
                c = b["chterm"][(u, t)]
                rows.append([c[lv] for lv in LEVELS])
                y.append(b["inst"][u] * sum(c.values()) / tot)
        coef, *_ = np.linalg.lstsq(np.array(rows, float), np.array(y), rcond=None)
        return coef
    else:
        X = np.array([[b["ch"][u][lv] for lv in LEVELS] for u in S], float)
    y = np.array([b["inst"][u] for u in S])
    if form == "with_intercept":
        X = np.column_stack([X, np.ones(len(S))])
    if form == "wls_fte":
        w = np.sqrt(1.0 / np.array([b["fte"][u] for u in S]))
        coef, *_ = np.linalg.lstsq(X * w[:, None], y * w, rcond=None)
    else:
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return coef


def predicted(b, u, coef, form="golden"):
    c = b["ch"][u]
    if form == "two_level":
        return coef[0] * (c["Lower division"] + c["Upper division"]) + coef[1] * c["Graduate"]
    v = sum(coef[i] * c[lv] for i, lv in enumerate(LEVELS))
    if form == "with_intercept":
        v += coef[3]
    return v


def per_fte(b, route="golden"):
    """Each campus's fiscal 2026 instruction expense per FTE. Standalone campuses report their own; a parent's return
    is split among the parent and its branches by the route."""
    out = {u: b["inst"][u] / b["fte"][u] for u in b["ids"] if b["kind"][u] == "S"}
    form = route if route in ("wls_fte", "with_intercept", "two_level", "by_term") else "golden"
    coef = fit(b, form) if route in GOLDEN_FORMS + ("two_level",) else None
    for p, mem in systems(b).items():
        tot = b["inst"][p]
        if route == "fte_split":
            w = {u: b["fte"][u] for u in mem}
        elif route == "credit_hour_split":
            w = {u: sum(b["ch"][u].values()) for u in mem}
        elif route == "exclude_children":
            out[p] = tot / sum(b["fte"][u] for u in mem)
            continue
        elif route == "zero":
            for u in mem:
                out[u] = (tot if u == p else 0.0) / b["fte"][u]
            continue
        else:
            w = {u: predicted(b, u, coef, form) for u in mem}
        if route == "direct":
            for u in mem:
                out[u] = w[u] / b["fte"][u]
            continue
        s = sum(w.values())
        for u in mem:
            out[u] = tot * w[u] / s / b["fte"][u]
    return out


def awarded(b, v):
    return sorted(sorted(v, key=lambda u: v[u])[:5])


# ------------------------------------------------------------------------------------------------ asks
def ask_a(b, dedup=True):
    """Each branch campus's fall 2026 FTE: undergraduate credit hours over 15 plus graduate over 12, a student's
    course counted once (a cross-listed course carries the student under both course numbers, at one meeting)."""
    seen = set()
    out = {}
    for r in b["census"]:
        u = b["code"][r["campus_code"]]
        key = (r["campus_code"], r["student_id"], r["meeting_days"], r["start_time"], r["instructor_id"]) if dedup \
            else (r["campus_code"], r["student_id"], r["subject"], r["course_number"], r["crn"])
        if key in seen:
            continue
        seen.add(key)
        out[u] = out.get(u, 0.0) + int(r["credit_hours"]) / (12.0 if r["course_level"] == "GR" else 15.0)
    return {u: round(v, 1) for u, v in out.items()}


def ask_b(b, persons=True):
    """Each branch campus's unduplicated fall 2026 headcount; persons links a student's rows under the old and the new
    id by birth date, sex, home ZIP code and first term within the campus ("partial" by the first three only, which
    merges different students who share them; "full" with the major too, which the new systems recoded)."""
    out = {}
    for r in b["census"]:
        u = b["code"][r["campus_code"]]
        if persons == "partial":
            key = (r["birth_date"], r["sex"], r["home_zip"])
        elif persons == "full":
            key = (r["birth_date"], r["sex"], r["home_zip"], r["first_term"], r["major_cip"])
        elif persons:
            key = (r["birth_date"], r["sex"], r["home_zip"], r["first_term"])
        else:
            key = r["student_id"]
        out.setdefault(u, set()).add(key)
    return {u: len(v) for u, v in out.items()}
