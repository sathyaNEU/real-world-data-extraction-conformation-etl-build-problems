"""Independent verifier: reads only target.zip, on its own code path (csv module, openpyxl, its own IRLS Poisson fit), and
recomputes the call and every ask figure against figures.json. Returns the number of failures."""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BAD = []


def ok(name, cond, info=""):
    print(("ok   " if cond else "FAIL ") + name + ((" :: " + str(info)) if info != "" else ""))
    if not cond:
        BAD.append(name)


def rows(z, name):
    with z.open(name) as fh:
        return list(csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8")))


def irls_poisson(X, y, iters=60):
    b = np.zeros(X.shape[1])
    b[0] = np.log(y.mean())
    for _ in range(iters):
        eta = X @ b
        mu = np.exp(eta)
        z = eta + (y - mu) / mu
        WX = X * mu[:, None]
        b_new = np.linalg.solve(X.T @ WX, WX.T @ z)
        if np.max(np.abs(b_new - b)) < 1e-10:
            b = b_new
            break
        b = b_new
    return b


def main(zp):
    del BAD[:]
    F = json.load(open(os.path.join(HERE, "figures.json")))
    z = zipfile.ZipFile(zp)
    names = z.namelist()
    LON = ZoneInfo("Europe/London")
    leg = [r for r in rows(z, "walkin_tickets_legacy_2023-04_to_2024-11.csv") if r["Outcome"] == "Seen"]
    ev = rows(z, "phlebotomy_queue_events_2024-11-18_to_2026-09-30.csv")
    cut = dt.date(2024, 11, 18)
    seen = {}
    for r in leg:
        d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        if d < cut:
            k = (d, "GP" if r["Request"] == "GP form" else "HOSP")
            seen[k] = seen.get(k, 0) + 1
    hosp = []
    for r in ev:
        if r["event_type"] != "CHECKED_IN":
            continue
        d = dt.datetime.strptime(r["event_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC")).astimezone(LON).date()
        seen[(d, r["request_type"])] = seen.get((d, r["request_type"]), 0) + 1
        if r["request_type"] == "HOSP":
            hosp.append((d, r["request_org"], dt.date.fromisoformat(r["request_date"])))
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(z.read("reception_turned_away_log.xlsx")), data_only=True)
    away = {}
    for ws in wb.worksheets:
        layout = None
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Date":
                layout = "A" if row[3] == "GP form AM" else "B"
                continue
            if layout is None or not row:
                continue
            d = row[0]
            if isinstance(d, str) and re.fullmatch(r"\d{2}/\d{2}/\d{4}", d.strip()):
                d = dt.datetime.strptime(d.strip(), "%d/%m/%Y")
            if not isinstance(d, (dt.date, dt.datetime)):
                continue
            d = d.date() if isinstance(d, dt.datetime) else d
            if layout == "A":
                gp, h = (row[3] or 0) + (row[4] or 0), (row[5] or 0) + (row[6] or 0)
                if gp + h:
                    away[d] = (gp, h)
            else:
                away[d] = (row[2] or 0, row[3] or 0)
    days = sorted({d for d, _ in seen})
    gp = np.array([seen.get((d, "GP"), 0) for d in days], float)
    agp = np.array([away.get(d, (0, 0))[0] for d in days], float)
    ro = np.array([1.0 if d in away else 0.0 for d in days])
    arr = gp + agp
    wkday = {}
    for d, r in zip(days, ro):
        w = d - dt.timedelta(d.weekday())
        a, b = wkday.get(w, (0, 0))
        wkday[w] = (a + r, b + 1)
    wsh = {w: a / b for w, (a, b) in wkday.items()}

    def window_share(L):
        return np.array([sum(wsh.get(d - dt.timedelta(d.weekday() + 7 * j), 0.0) for j in range(1, L + 1)) / L for d in days])
    cols = [np.ones(len(days))]
    for k in range(1, 5):
        cols.append(np.array([1.0 if d.weekday() == k else 0.0 for d in days]))
    for m in range(2, 13):
        cols.append(np.array([1.0 if d.month == m else 0.0 for d in days]))
    cols.append(np.array([(d - dt.date(2023, 4, 3)).days / 365.25 for d in days]))
    cols.append(np.array([1.0] + [1.0 if (days[i] - days[i - 1]).days not in (1, 3) else 0.0 for i in range(1, len(days))]) * 0 +
                np.array([0.0] + [1.0 if (days[i] - days[i - 1]).days not in (1, 3) else 0.0 for i in range(1, len(days))]))
    # the run-out window: the mean share of the previous L weeks, L from one to twelve, the lowest AIC
    from math import lgamma
    lgy = sum(lgamma(y + 1) for y in arr)
    fits = {}
    for L in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12):
        sh = window_share(L)
        X = np.column_stack(cols + [sh])
        bb = irls_poisson(X, arr)
        mu = np.exp(X @ bb)
        fits[L] = (2 * X.shape[1] - 2 * (float((arr * np.log(mu) - mu).sum()) - lgy), bb, sh)
    L = min(fits, key=lambda k: fits[k][0])
    b, share = fits[L][1], fits[L][2]
    ok("call: the fit picks the %d-week window" % F["window_weeks"], L == F["window_weeks"], {k: round(v[0] - fits[L][0], 1) for k, v in fits.items()})
    fy = np.array([dt.date(2025, 4, 1) <= d <= dt.date(2026, 3, 31) for d in days])
    base = float((arr[fy] * np.exp(-b[-1] * share[fy])).sum())
    plan = base * 1.035 ** 2
    ok("call: the plan rounds to %s" % F["plan_visits_2027_28"], int(round(plan / 2500.0) * 2500) == F["plan_visits_2027_28"], round(plan))
    ok("call: unrounded plan within one visit", abs(plan - F["plan_unrounded"]) <= 1.0, round(plan, 2))
    ok("call: base within one visit", abs(base - F["base_2025_26"]) <= 1.0, round(base, 2))
    ok("component: GP-referred seen", int(gp[fy].sum()) == F["gp_seen_2025_26"], int(gp[fy].sum()))
    ok("component: GP-referred turned away", int(agp[fy].sum()) == F["gp_turned_away_2025_26"], int(agp[fy].sum()))
    ok("component: run-out days", int(ro[fy].sum()) == F["run_out_days_2025_26"], int(ro[fy].sum()))
    ok("coefficient", abs(b[-1] - F["coef_window_share"]) < 0.0006, round(b[-1], 4))
    ok("default path", int(round(arr[fy].sum() * 1.035 ** 2 / 2500.0) * 2500) == F["default_path_plan"])
    # ask A, own route: each new code's issue weekdays before the April templates link it to the old code with the
    # same weekdays; every 2025-26 visit then takes its specialty from the register
    reg = rows(z, "outpatient_clinic_codes.csv")
    newmap = {r["clinic_code"]: r["specialty"] for r in reg}
    early = {}
    oldw = {}
    for d, code, rd in hosp:
        if code in newmap and rd < dt.date(2026, 4, 1):
            early.setdefault(code, set()).add(rd.weekday())
        elif code not in newmap:
            oldw.setdefault(code, set()).add(rd.weekday())
    oldmap = {}
    for c, w in oldw.items():
        hit = [n for n, e in early.items() if e == w]
        ok("ask A: old code %s links to one new code" % c, len(hit) == 1, hit)
        oldmap[c] = newmap[hit[0]] if len(hit) == 1 else None
    tab = {}
    for d, code, rd in hosp:
        if dt.date(2025, 4, 1) <= d <= dt.date(2026, 3, 31):
            sp = newmap.get(code) or oldmap.get(code)
            q = "Q%d" % (((d.month - 4) % 12) // 3 + 1)
            tab[(sp, q)] = tab.get((sp, q), 0) + 1
    miss = [(sp, q) for sp, qq in F["hospital_visits_2025_26"].items() for q, v in qq.items() if tab.get((sp, q), 0) != v]
    ok("ask A: all 28 cells", not miss, miss[:3])
    # ask B, own route by identity: an unassigned line belongs to a holder who has no line that day, whose last line
    # before was sickness and who comes back; any other unassigned line is the vacant post
    ro_rows = [r for r in rows(z, "eroster_phlebotomy_2023-04_to_2026-09.csv") if r["Assignment"] != "Bank Phlebotomist"]
    by_day = {}
    for r in ro_rows:
        by_day.setdefault(r["Roster date"], []).append(r)
    span = {}
    for r in ro_rows:
        if r["Employee no"]:
            a0, a1 = span.get(r["Employee no"], (r["Roster date"], r["Roster date"]))
            span[r["Employee no"]] = (min(a0, r["Roster date"]), max(a1, r["Roster date"]))
    last = {}
    sick, rost = {}, {}
    for day in sorted(by_day):
        rs = by_day[day]
        present = {r["Employee no"] for r in rs if r["Employee no"]}
        absent_sick = [e for e, (a0, a1) in span.items() if a0 < day < a1 and e not in present and last.get(e) == "Sickness"]
        unassigned = sum(1 for r in rs if r["Vacant line"] == "Y")
        d = dt.date.fromisoformat(day)
        if dt.date(2025, 4, 1) <= d <= dt.date(2026, 3, 31):
            q = "Q%d" % (((d.month - 4) % 12) // 3 + 1)
            k = min(len(absent_sick), unassigned)
            sick[q] = sick.get(q, 0) + sum(1 for r in rs if r["Absence"] == "Sickness") + k
            rost[q] = rost.get(q, 0) + sum(1 for r in rs if r["Vacant line"] == "N") + k
        for r in rs:
            if r["Employee no"]:
                last[r["Employee no"]] = r["Absence"]
    for q, v in F["sickness_by_quarter"].items():
        ok("ask B %s days lost" % q, sick.get(q, 0) == v["days_lost"], sick.get(q, 0))
        ok("ask B %s rate" % q, round(100.0 * sick.get(q, 0) / rost[q], 1) == v["rate_pct"], round(100.0 * sick.get(q, 0) / rost[q], 3))
    # every format read back
    from pypdf import PdfReader
    rep = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(io.BytesIO(z.read("phlebotomy_annual_report_2025-26.pdf"))).pages))
    icb = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(io.BytesIO(z.read("icb_pathology_planning_assumptions_2026-27.pdf"))).pages))
    ok("pdf: the report's sickness definition reads back", "hours rostered to the substantive team" in rep)
    ok("pdf: the ICB's 3.5% reads back", "GP direct access phlebotomy 3.5%" in icb)
    bh = json.loads(z.read("bank_holidays_england.json"))
    ok("json: bank holidays read back", len(bh["england-and-wales"]["events"]) > 30)
    wbh = load_workbook(io.BytesIO(z.read("community_hub_session_plan_2027.xlsx")))
    ok("xlsx: the hub plan reads back", wbh.active.max_row > 5)
    ok("zip: thirteen files", len(names) == 13, len(names))
    print("verify: %d failed" % len(BAD))
    return len(BAD)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
