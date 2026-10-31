"""The golden, computed from target/ alone: the 2027 forecast the plan's staffing rule compares, and the three asks.
Also every rival route the checks and the ceiling script price, each on the same loaded bundle.

    python3 task130/generator/analysis.py
"""
import csv
import datetime as dt
import json
import os
import re
import statistics
import sys
from collections import defaultdict

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
THRESHOLD = 540
FEE = (dt.date(2026, 7, 1), 152, 168)
UNSAT = {"UNSAT", "IHH CLOSURE", "Unsatisfactory", "Closed - imminent health hazard"}
NOACC = {"NO ACCESS", "No access"}


def _csv(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _nth(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def utc_to_local(s):
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    y = t.year
    a = dt.datetime.combine(_nth(y, 3, 6, 2), dt.time(10))      # 02:00 PST = 10:00 UTC
    b = dt.datetime.combine(_nth(y, 11, 6, 1), dt.time(9))      # 02:00 PDT = 09:00 UTC
    return t - dt.timedelta(hours=7 if a <= t < b else 8)


def load(target=TARGET):
    D = {}
    perm = _csv(target, "food_establishment_permits.csv")
    D["permits"] = {r["permit_id"]: r for r in perm}
    wb = openpyxl.load_workbook(os.path.join(target, "food_program_staff_roster.xlsx"), read_only=True)
    staff = {}
    for sh in wb.sheetnames:
        for i, row in enumerate(wb[sh].iter_rows(values_only=True)):
            if i == 0 or not row[0]:
                continue
            last, rest = row[1].split(", ")
            first, mid = rest.rsplit(" ", 1)
            staff[row[0]] = dict(emp=row[0], name="%s %s" % (first, last), initials=first[0] + mid[0] + last[0],
                                 role=row[2], assignment=row[3])
    D["staff"] = staff
    by_init = {s["initials"]: e for e, s in staff.items()}
    D["by_name"] = {s["name"]: e for e, s in staff.items()}
    visits = []
    for r in _csv(target, "inspections_2019-01_2024-03.csv"):
        t = dt.datetime.strptime(r["insp_date"] + " " + r["time_in"], "%m/%d/%Y %I:%M %p")
        visits.append(dict(src="legacy", id=r["inspection_no"], permit=r["permit_no"], t=t,
                           who=by_init[r["inspector"]], type=r["insp_type"].lower().replace("pre-opening", "preopen"),
                           result=r["result"], red=r["red_pts"], cref=""))
    for r in _csv(target, "inspections_2024-03_2026-12.csv"):
        visits.append(dict(src="current", id=r["inspection_id"], permit=r["permit_id"],
                           t=utc_to_local(r["inspected_at_utc"]), t_utc=r["inspected_at_utc"],
                           who=r["inspector_employee_no"], type=r["inspection_type"].lower().replace("pre-opening", "preopen"),
                           result=r["result"], red=r["red_points"], cref=r["complaint_id"]))
    visits.sort(key=lambda v: (v["t"], v["id"]))
    D["visits"] = visits
    wb = openpyxl.load_workbook(os.path.join(target, "routine_inspection_schedule_2027.xlsx"), read_only=True)
    sched = [dict(permit=r[0], risk=int(r[4]), d27=r[5], n=int(r[6]))
             for i, r in enumerate(wb["Schedule 2027"].iter_rows(values_only=True)) if i and r[0]]
    d27 = {r[0]: r[3] for i, r in enumerate(wb["Districts 2027"].iter_rows(values_only=True)) if i and r[0]}
    D["schedule"], D["d27"] = sched, d27
    return D


# ------------------------------------------------------------------ the call
def visit_counts(D, start=dt.date(2019, 1, 1), types=("routine", "complaint", "return", "preopen"), window=None,
                 count_noaccess=False):
    """For each routine inspection made (not a closed-premises call), the inspector's earlier inspected visits to the
    permit on the record from `start`; and the totals at the end of the record. `window` (months) counts only
    visits that recent; `count_noaccess` counts closed-premises calls as visits too."""
    seen = defaultdict(list)
    rows = []
    for v in D["visits"]:
        if v["t"].date() < start:
            continue
        key = (v["who"], v["permit"])
        if v["type"] == "routine" and v["result"] not in NOACC:
            h = seen[key]
            k = len(h) if window is None else sum(1 for s in h if (v["t"] - s).days <= window * 30.44)
            rows.append(dict(t=v["t"], permit=v["permit"], who=v["who"], k=k, unsat=v["result"] in UNSAT))
        if (count_noaccess or v["result"] not in NOACC) and v["type"] in types:
            seen[key].append(v["t"])
    return rows, seen


def cell_rates(D, rows, years=(2022, 2026), classes=(0, 1, 2)):
    top = classes[-1]
    c = defaultdict(lambda: [0, 0])
    for r in rows:
        if years[0] <= r["t"].year <= years[1]:
            risk = int(D["permits"][r["permit"]]["risk_category"])
            cell = c[(risk, min(r["k"], top))]
            cell[0] += r["unsat"]
            cell[1] += 1
    return {k: v[0] / v[1] for k, v in c.items()}, dict(c)


def forecast(D, rates, seen, classes=(0, 1, 2), window=None, end=dt.datetime(2026, 12, 31, 23, 59), detail=None,
             advance=True):
    top = classes[-1]
    tot = 0.0
    by = defaultdict(float)
    nk = defaultdict(int)
    for s in D["schedule"]:
        who = D["d27"][s["d27"]]
        h = seen.get((who, s["permit"]), [])
        k0 = len(h) if window is None else sum(1 for x in h if (end - x).days <= window * 30.44)
        for j in range(s["n"]):
            k = min(k0 + (j if advance else 0), top)
            p = rates[(s["risk"], k)]
            tot += p
            by[s["d27"]] += p
            nk[k] += 1
            if detail is not None:
                detail["sched"][s["d27"]] += 1
                detail["k%d" % k][s["d27"]] += 1
                if k == 0:
                    detail["first_part"][s["d27"]] += p
    return tot, dict(by), dict(nk)


def golden_call(D):
    rows, seen = visit_counts(D)
    rates, cells = cell_rates(D, rows)
    det = {k: defaultdict(float) for k in ("sched", "k0", "k1", "k2", "first_part")}
    tot, by, nk = forecast(D, rates, seen, detail=det)
    return dict(total=tot, by=by, nk=nk, rates=rates, cells=cells, add=tot > THRESHOLD,
                detail={k: dict(v) for k, v in det.items()})


# rival routes on the same bundle -----------------------------------
def route_category(D, years=(2022, 2026)):
    rows, seen = visit_counts(D)
    c = defaultdict(lambda: [0, 0])
    for r in rows:
        if years[0] <= r["t"].year <= years[1]:
            cc = c[int(D["permits"][r["permit"]]["risk_category"])]
            cc[0] += r["unsat"]
            cc[1] += 1
    return sum(c[s["risk"]][0] / c[s["risk"]][1] * s["n"] for s in D["schedule"])


def route_own_history(D, years=(2022, 2026), prior=4.0):
    rows, seen = visit_counts(D)
    c = defaultdict(lambda: [0, 0])
    own = defaultdict(lambda: [0, 0])
    for r in rows:
        if years[0] <= r["t"].year <= years[1]:
            risk = int(D["permits"][r["permit"]]["risk_category"])
            c[risk][0] += r["unsat"]
            c[risk][1] += 1
            own[r["permit"]][0] += r["unsat"]
            own[r["permit"]][1] += 1
    tot = 0.0
    for s in D["schedule"]:
        base = c[s["risk"]][0] / c[s["risk"]][1]
        a = own.get(s["permit"], [0, 0])
        tot += s["n"] * (a[0] + prior * base) / (a[1] + prior)
    return tot


def route_inspector(D, years=(2022, 2026)):
    """One criterion per inspector: each inspector's observed over expected unsatisfactory share, carried to the
    inspector named for each 2027 district."""
    rows, seen = visit_counts(D)
    c = defaultdict(lambda: [0, 0])
    for r in rows:
        if years[0] <= r["t"].year <= years[1]:
            cc = c[int(D["permits"][r["permit"]]["risk_category"])]
            cc[0] += r["unsat"]
            cc[1] += 1
    base = {k: v[0] / v[1] for k, v in c.items()}
    oe = defaultdict(lambda: [0.0, 0.0])
    for r in rows:
        if years[0] <= r["t"].year <= years[1]:
            x = oe[r["who"]]
            x[0] += r["unsat"]
            x[1] += base[int(D["permits"][r["permit"]]["risk_category"])]
    ratio = {w: v[0] / v[1] for w, v in oe.items()}
    return sum(base[s["risk"]] * ratio.get(D["d27"][s["d27"]], 1.0) * s["n"] for s in D["schedule"])


def route_tenure(D, years=(2022, 2026)):
    """A first-year criterion for newly appointed inspectors, read from the record's appointees: 2027 has none, so
    the category rates stand."""
    return route_category(D, years)


def route_trend(D):
    rows, seen = visit_counts(D)
    by = defaultdict(int)
    for r in rows:
        by[r["t"].year] += r["unsat"]
    ys = [2022, 2023, 2024, 2025, 2026]
    xs = [by[y] for y in ys]
    mx, my = sum(ys) / 5, sum(xs) / 5
    b = sum((y - mx) * (x - my) for y, x in zip(ys, xs)) / sum((y - mx) ** 2 for y in ys)
    return my + b * (2027 - mx)


def main_effects(cells, classes):
    """The cell rates from a logistic fit with risk category and visit class as main effects (no interaction),
    fitted to the grouped cells by iteratively reweighted least squares."""
    keys = sorted(cells)

    def row(rk, k):
        return [1.0, float(rk == 2), float(rk == 3)] + [float(k == c) for c in classes[1:]]
    X = np.array([row(*key) for key in keys])
    y = np.array([float(cells[key][0]) for key in keys])
    n = np.array([float(cells[key][1]) for key in keys])
    b = np.zeros(X.shape[1])
    for _ in range(60):
        eta = X @ b
        p = 1.0 / (1.0 + np.exp(-eta))
        w = n * p * (1.0 - p)
        b = np.linalg.solve(X.T @ (w[:, None] * X), X.T @ (w * (eta + (y - n * p) / w)))
    return {key: float(1.0 / (1.0 + np.exp(-(np.array(row(*key)) @ b)))) for key in keys}


def golden_variant(D, start=dt.date(2019, 1, 1), years=(2022, 2026), classes=(0, 1, 2), types=None, window=None,
                   model="cells", count_noaccess=False, advance=True):
    kw = {} if types is None else dict(types=types)
    rows, seen = visit_counts(D, start=start, window=window, count_noaccess=count_noaccess, **kw)
    rates, cells = cell_rates(D, rows, years=years, classes=classes)
    if model == "main":
        rates = main_effects(cells, classes)
    return forecast(D, rates, seen, classes=classes, window=window, advance=advance)[0]


def pair_with_terms(D, inspector=True, prior=None, years=(2022, 2026)):
    """The visit classes with each named inspector's own criterion (observed over expected under the cell rates)
    and, when `prior` is set, each establishment's own record shrunk by `prior` expected unsatisfactory inspections."""
    rows, seen = visit_counts(D)
    rates, cells = cell_rates(D, rows, years=years)
    oi, op = defaultdict(lambda: [0.0, 0.0]), defaultdict(lambda: [0.0, 0.0])
    for r in rows:
        if years[0] <= r["t"].year <= years[1]:
            p = rates[(int(D["permits"][r["permit"]]["risk_category"]), min(r["k"], 2))]
            oi[r["who"]][0] += r["unsat"]
            oi[r["who"]][1] += p
            op[r["permit"]][0] += r["unsat"]
            op[r["permit"]][1] += p
    tot = 0.0
    for s in D["schedule"]:
        who = D["d27"][s["d27"]]
        f = oi[who][0] / oi[who][1] if inspector and oi[who][1] else 1.0
        if prior is not None:
            a, e = op.get(s["permit"], [0.0, 0.0])
            f *= (a + prior) / (e + prior)
        k0 = len(seen.get((who, s["permit"]), []))
        for j in range(s["n"]):
            tot += min(1.0, rates[(s["risk"], min(k0 + j, 2))] * f)
    return tot


# ------------------------------------------------------------------ the asks
def norm_addr(a):
    a = a.upper().replace(".", "")
    for full, short in (("STREET", "ST"), ("AVENUE", "AVE"), ("ROAD", "RD"), ("DRIVE", "DR"), ("HIGHWAY", "HWY"),
                        ("LANE", "LN"), ("BOULEVARD", "BLVD")):
        a = re.sub(r"\b%s\b" % full, short, a)
    parts = a.split()
    if parts and parts[-1] in ("ST", "AVE", "RD", "DR", "HWY", "LN", "BLVD", "WAY", "LOOP", "GRADE"):
        parts = parts[:-1]
    return " ".join(parts)


def daysheet(target, D):
    wb = openpyxl.load_workbook(os.path.join(target, "return_team_capacity_report_2026.xlsx"), read_only=True)
    out = []
    for i, r in enumerate(wb["Day sheet log"].iter_rows(values_only=True)):
        if i == 0 or not r[0]:
            continue
        day = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
        out.append(dict(day=day, who=D["by_name"][r[1]], name=r[2], addr=norm_addr(r[3]), result=r[4]))
    return out


def return_dates(target, D, use_daysheet=True):
    """Each completed return inspection's date: the new system's stamp, except return-team records saved from day
    sheets, whose date is the day sheet's (the sheet's entry for the same officer and address in the week up to the
    stamp)."""
    sheet = daysheet(target, D) if use_daysheet else []
    by = defaultdict(list)
    for x in sheet:
        by[(x["who"], x["addr"])].append(x)
    team = {e for e, s in D["staff"].items() if s["role"] == "Return Inspection Officer"}
    out = {}
    used = set()
    for v in D["visits"]:
        if v["type"] != "return" or v["result"] in NOACC:
            continue
        d = v["t"].date()
        if use_daysheet and v["src"] == "current" and v["who"] in team and d <= dt.date(2026, 9, 15):
            key = (v["who"], norm_addr(D["permits"][v["permit"]]["street_address"]))
            cands = [x for x in by.get(key, []) if 1 <= (d - x["day"]).days <= 20 and id(x) not in used]
            if cands:
                x = min(cands, key=lambda x: x["day"])
                used.add(id(x))
                d = x["day"]
        out[v["id"]] = d
    return out


def _working(d, hol):
    return d.weekday() < 5 and d not in hol


def working_between(a, b, hol):
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if _working(d, hol):
            n += 1
    return n


def holidays(target):
    h = json.load(open(os.path.join(target, "county_holidays_2025-2027.json"), encoding="utf-8"))
    return {dt.date.fromisoformat(x["date"]) for y in h["years"].values() for x in y}


def episodes(D):
    """Each unsatisfactory routine inspection and the return visits that follow it at the permit, up to the next
    routine inspection there."""
    by = defaultdict(list)
    for v in D["visits"]:
        by[v["permit"]].append(v)
    eps = []
    for pid, vs in by.items():
        cur = None
        for v in vs:
            if v["type"] == "routine" and v["result"] not in NOACC:
                cur = dict(routine=v, returns=[]) if v["result"] in UNSAT else None
                if cur:
                    eps.append(cur)
            elif v["type"] == "return" and cur is not None:
                cur["returns"].append(v)
    return eps


def ask_a(target, D, use_daysheet=True):
    hol = holidays(target)
    rd = return_dates(target, D, use_daysheet)
    out = defaultdict(list)
    for ep in episodes(D):
        done = [r for r in ep["returns"] if r["result"] not in NOACC]
        if not done:
            continue
        first = min(done, key=lambda r: (rd[r["id"]], r["id"]))
        d = rd[first["id"]]
        if ep["routine"]["t"].year != 2026 or d.year != 2026:
            continue
        dist = int(D["permits"][ep["routine"]["permit"]]["district_2026"])
        out[dist].append(working_between(ep["routine"]["t"].date(), d, hol))
    return {k: statistics.median(v) for k, v in sorted(out.items())}, {k: len(v) for k, v in out.items()}


def complaints(target):
    return _csv(target, "complaints_2024-03_2026-12.csv")


def ask_b(target, D, first_notice=True):
    comp = complaints(target)
    by_id = {c["complaint_id"]: c for c in comp}
    by_perm = defaultdict(list)
    for c in comp:
        by_perm[c["permit_id"]].append(c)
    invs = [v for v in D["visits"] if v["type"] == "complaint" and v["src"] == "current"]
    prev = {}
    out = defaultdict(list)
    for v in sorted(invs, key=lambda v: v["t_utc"]):
        start = dt.datetime.strptime(v["t_utc"], "%Y-%m-%dT%H:%M:%SZ")
        if first_notice:
            lo = prev.get(v["permit"])
            cand = [dt.datetime.strptime(c["received_at_utc"], "%Y-%m-%dT%H:%M:%SZ") for c in by_perm[v["permit"]]]
            cand = [t for t in cand if t < start and (lo is None or t > lo)]
            first = min(cand)
        else:
            first = dt.datetime.strptime(by_id[v["cref"]]["received_at_utc"], "%Y-%m-%dT%H:%M:%SZ")
        prev[v["permit"]] = start
        if utc_to_local(v["t_utc"]).year != 2026:
            continue
        dist = int(D["permits"][v["permit"]]["district_2026"])
        out[dist].append((start - first).total_seconds() / 3600.0)
    return {k: statistics.median(v) for k, v in sorted(out.items())}, {k: len(v) for k, v in out.items()}


def letters(target):
    return _csv(target, "correspondence_log_2026.csv")


def ask_c(target, D, use_letters=True, use_daysheet=True):
    rd = return_dates(target, D, use_daysheet)
    na = defaultdict(set)          # permit -> dates of closed-premises return calls
    for v in D["visits"]:
        if v["type"] == "return" and v["result"] in NOACC:
            na[v["permit"]].add(v["t"].date())
    if use_letters:
        for x in letters(target):
            if x["template"].startswith("RV-NA"):
                na[x["permit_id"]].add(dt.date.fromisoformat(x["visit_date"]))
    eps = episodes(D)
    by_perm = defaultdict(list)
    for ep in eps:
        by_perm[ep["routine"]["permit"]].append(ep)
    fees = defaultdict(int)
    for pid, lst in by_perm.items():
        lst.sort(key=lambda e: e["routine"]["t"])
        for j, ep in enumerate(lst):
            if ep["routine"]["t"].year != 2026:
                continue
            t0 = ep["routine"]["t"].date()
            t1 = lst[j + 1]["routine"]["t"].date() if j + 1 < len(lst) else dt.date(2099, 1, 1)
            vis = [rd[r["id"]] for r in ep["returns"] if r["result"] not in NOACC]
            vis += [d for d in na.get(pid, ()) if t0 < d < t1]
            vis = sorted(set(vis)) if use_letters else sorted(vis)
            for d in vis[1:]:
                if d.year == 2026:
                    dist = int(D["permits"][pid]["district_2026"])
                    fees[dist] += FEE[1] if d < FEE[0] else FEE[2]
    return dict(sorted(fees.items()))


def main(target=TARGET):
    D = load(target)
    G = golden_call(D)
    a, an = ask_a(target, D)
    b, bn = ask_b(target, D)
    c = ask_c(target, D)
    det = G["detail"]
    F = dict(D=D, G=G, A=a, A_n=an, B=b, B_n=bn, C=c,
             sched_by={d: int(det["sched"].get(d, 0)) for d in G["by"]},
             first_by={d: int(det["k0"].get(d, 0)) for d in G["by"]},
             second_by={d: int(det["k1"].get(d, 0)) for d in G["by"]},
             first_part=det["first_part"],
             routes=dict(category=route_category(D), own=route_own_history(D), inspector=route_inspector(D),
                         trend=route_trend(D)))
    return F


if __name__ == "__main__":
    F = main()
    G = F["G"]
    print("2027 forecast %.1f, add a third officer: %s; visit classes %s" % (G["total"], G["add"], G["nk"]))
    print("rates", {k: round(v, 4) for k, v in sorted(G["rates"].items())})
    D = F["D"]
    print("routes: category %.1f own %.1f inspector %.1f trend %.1f" % (route_category(D), route_own_history(D),
                                                                       route_inspector(D), route_trend(D)))
    print("A", F["A"], F["A_n"])
    print("B", {k: round(v, 2) for k, v in F["B"].items()}, F["B_n"])
    print("C", F["C"])
