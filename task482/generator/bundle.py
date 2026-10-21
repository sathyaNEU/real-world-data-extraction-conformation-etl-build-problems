"""Read the cut pack the way an analyst would, and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the conformed registrations, the open caseload, the holiday calendar and the payments
    medians(b, route)       each office's median working days for its third-quarter applications under a route
    planned(b, m)           the offices over 20
    ask(b, by_terminal)     each office's card payments made in the quarter: number and amount"""
import csv
import datetime as dt
import os

import numpy as np

FILES = {
    "log_old": "cro_registrations_legacy_system_2026-07.csv",
    "log_new": "cro_registrations_case_system_2026-08_to_2026-10.csv",
    "open": "cro_open_caseload_snapshot_2026-10-09.csv",
    "holidays": "cro_public_holidays_2026.csv",
    "pays": "cro_card_payments_settled_2026-07_to_2026-10.csv",
    "batches": "cro_card_settlement_batches_2026q3.csv",
}
EXTRACT = dt.date(2026, 10, 9)
LINE = 20
Q3 = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
GOLDEN_FORMS = ("golden", "km_interpolated", "km_strict")
ROUTES = GOLDEN_FORMS + ("registered_only", "open_at_age", "open_as_late", "calendar_days")


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _d(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date() if "/" in s else dt.date.fromisoformat(s)


def load(target):
    hol = {dt.date.fromisoformat(r["date"]) for r in _csv(os.path.join(target, FILES["holidays"]))}
    reg = []
    for r in _csv(os.path.join(target, FILES["log_old"])):
        reg.append(("CRO-" + r["Office"], _d(r["Received"]), _d(r["Complete"]), _d(r["Registered"])))
    for r in _csv(os.path.join(target, FILES["log_new"])):
        reg.append((r["office_code"], _d(r["received_on"]), _d(r["clock_start"]), _d(r["registered_on"])))
    opn = [(r["office_code"], _d(r["received_on"]), _d(r["clock_start"]), int(r["open_applications"]))
           for r in _csv(os.path.join(target, FILES["open"]))]
    ids = sorted({r[0] for r in reg})
    return {"hol": hol, "reg": reg, "open": opn, "ids": ids, "target": target}


def wd(b, a, c):
    n = 0
    d = a
    while d < c:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in b["hol"]:
            n += 1
    return n


def km(times, events, form="golden"):
    order = sorted(zip(times, events))
    n = len(order)
    s, i, prev_t, prev_s = 1.0, 0, 0, 1.0
    while i < n:
        t = order[i][0]
        grp = [e for tt, e in order[i:] if tt == t]
        d = sum(grp)
        s_new = s * (1 - d / (n - i))
        if form == "km_strict" and s_new < 0.5:
            return t
        if form != "km_strict" and s_new <= 0.5:
            if form == "km_interpolated" and s > 0.5 and d:
                return prev_t + (t - prev_t) * (s - 0.5) / (s - s_new)
            return t
        if d:
            prev_t, prev_s = t, s_new
        s = s_new
        i += len(grp)
    return None


def medians(b, route="golden"):
    cal = route == "calendar_days"
    dist = (lambda a, c: (c - a).days) if cal else (lambda a, c: wd(b, a, c))
    out = {}
    for u in b["ids"]:
        t, e = [], []
        for o, rec, comp, regd in b["reg"]:
            if o == u and Q3[0] <= rec <= Q3[1]:
                t.append(dist(comp, regd))
                e.append(True)
        for o, rec, comp, k in b["open"]:
            if o == u and Q3[0] <= rec <= Q3[1]:
                age = dist(comp, EXTRACT)
                t += [age] * k
                e += [False] * k
        if route == "registered_only":
            out[u] = float(np.median([tt for tt, ee in zip(t, e) if ee]))
        elif route == "open_at_age":
            out[u] = float(np.median(t))
        elif route == "open_as_late":
            out[u] = float(np.median([tt if ee else 10 ** 6 for tt, ee in zip(t, e)]))
        else:
            out[u] = km(t, e, "golden" if route == "calendar_days" else route)
    return out


def planned(b, m):
    return sorted(u for u in m if m[u] > LINE)


def ask(b, by_terminal=True):
    """Card payments made in the quarter: by the batch's terminal day, or (the easy route) by the settlement day."""
    term = {r["batch_id"]: _d(r["terminal_date"]) for r in _csv(os.path.join(b["target"], FILES["batches"]))}
    out = {u: [0, 0.0] for u in b["ids"]}
    for r in _csv(os.path.join(b["target"], FILES["pays"])):
        d = term[r["batch_id"]] if by_terminal else _d(r["settled_on"])
        if Q3[0] <= d <= Q3[1]:
            out[r["office_code"]][0] += 1
            out[r["office_code"]][1] += float(r["amount_eur"])
    return {u: (v[0], round(v[1], 2)) for u, v in out.items()}
