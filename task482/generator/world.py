"""The world of task482 (architecture 3): the Companies Registration Office of Ardmuir, fourteen regional offices
registering new companies, and the management board's third-quarter 2026 timeliness review.

An application's clock runs in working days from the day it is complete (its receipt, or the reply to a query) to its
registration. On the 9 October extract part of each office's July to September applications is still open, and the
open ones are the slow ones: the offices with a backlog hold their slow applications there.

    x = build()    the truth: offices, applications with their complete and registration days, fees"""
import datetime as dt

import numpy as np

SEED = 4823
EXTRACT = dt.date(2026, 10, 9)
LINE = 20
HOLIDAYS = [dt.date(2026, 8, 3), dt.date(2026, 10, 26), dt.date(2026, 6, 1), dt.date(2026, 12, 25),
            dt.date(2026, 12, 28), dt.date(2026, 5, 4)]

# office code, name, applications in the quarter, median working days of the quick, share in the backlog,
# backlog median working days, place ("b" over on the golden, under on the registered median; "o" over on the golden
# and on the registered median; "u" under on the golden; "y" under on the golden, over when every open application is
# counted as late), and the share of applications received in the second half of September (a filing rush)
OFFICES = [
    ("CRO-AD", "Ardmuir", 3900, 11.0, 0.55, 42, "b", 0.00),
    ("CRO-BN", "Bannock", 1700, 9.0, 0.10, 34, "u", 0.00),
    ("CRO-CV", "Carrick", 1300, 11.5, 0.56, 43, "b", 0.00),
    ("CRO-DL", "Dunlay", 2100, 15.0, 0.10, 32, "y", 0.50),
    ("CRO-ES", "Eskmoor", 900, 9.5, 0.08, 30, "u", 0.00),
    ("CRO-FM", "Fallowmere", 1600, 24.0, 0.20, 45, "o", 0.00),
    ("CRO-GQ", "Glenquhar", 1100, 10.5, 0.57, 41, "b", 0.00),
    ("CRO-HL", "Harlaw", 2600, 8.5, 0.07, 28, "u", 0.00),
    ("CRO-IB", "Inverbeck", 800, 15.0, 0.10, 32, "y", 0.50),
    ("CRO-KM", "Kelso Moss", 1900, 10.0, 0.11, 33, "u", 0.00),
    ("CRO-LW", "Lenwick", 1200, 11.0, 0.54, 44, "b", 0.00),
    ("CRO-MG", "Mossgiel", 1500, 24.5, 0.18, 46, "o", 0.00),
    ("CRO-NM", "Northmuir", 2300, 9.5, 0.09, 31, "u", 0.00),
    ("CRO-SL", "Strathlorn", 1000, 15.0, 0.10, 32, "y", 0.50),
]
IDS = [o[0] for o in OFFICES]


def working_days(a, b):
    """Working days from day a to day b (b after a): weekdays not on the holiday list, a not counted."""
    n = 0
    d = a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in HOLIDAYS:
            n += 1
    return n


def add_working(a, k):
    d = a
    while k > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in HOLIDAYS:
            k -= 1
    return d


def km_median(times, events):
    """The product-limit median: the smallest time at which the survival estimate falls to one half or below."""
    order = sorted(zip(times, events))
    n = len(order)
    s = 1.0
    i = 0
    while i < n:
        t = order[i][0]
        d = sum(1 for tt, e in order[i:] if tt == t and e)
        c = sum(1 for tt, e in order[i:] if tt == t)
        s *= 1 - d / (n - i)
        if s <= 0.5:
            return t
        i += c
    return None


def build():
    rng = np.random.default_rng(SEED)
    days = [dt.date(2026, 7, 1) + dt.timedelta(days=k) for k in range(92)]
    wdays = [d for d in days if d.weekday() < 5 and d not in HOLIDAYS]
    apps = []
    k = 0
    late = [d for d in wdays if d >= dt.date(2026, 9, 14)]
    for code, name, n, qm, share, bm, place, surge in OFFICES:
        for tries in range(80):
            sub = []
            for i in range(n):
                rec = late[int(rng.integers(0, len(late)))] if rng.random() < surge else \
                    wdays[int(rng.integers(0, len(wdays)))]
                query = rng.random() < 0.22
                comp = add_working(rec, int(rng.integers(2, 12))) if query else rec
                if comp >= EXTRACT:
                    comp, query = rec, False
                slow = rng.random() < share
                dur = max(1, int(round(float(rng.lognormal(np.log(bm if slow else qm), 0.35 if slow else 0.45)))))
                reg = add_working(comp, dur)
                sub.append({"office": code, "received": rec, "complete": comp, "dur": dur, "registered": reg,
                            "query": query})
            m = summary(sub)
            ok = {"b": m["km"] > LINE + 1.5 and m["closed"] < LINE - 1.5,
                  "o": m["km"] > LINE + 1.5 and m["closed"] > LINE + 1.5,
                  "u": m["km"] < LINE - 1.5,
                  "y": m["km"] < LINE - 1.5 and m["open_late"] > LINE + 1.5}[place]
            if ok and abs(m["km"] - LINE) >= 1.5 and abs(m["open_age"] - LINE) >= 0.5:
                break
        else:
            raise SystemExit("office %s not placed" % code)
        for a in sub:
            k += 1
            a["k"] = k
        apps += sub
    x = {"apps": apps}
    # receipts outside the quarter that the logs also carry: late June's registered in July, early October's
    extra = []
    for code, name, n, qm, *_ in OFFICES:
        for _ in range(int(n * 0.05)):
            rec = dt.date(2026, 6, 15) + dt.timedelta(days=int(rng.integers(0, 16)))
            if rec.weekday() >= 5 or rec in HOLIDAYS:
                continue
            dur = max(1, int(round(float(rng.lognormal(np.log(qm), 0.45)))))
            extra.append({"office": code, "received": rec, "complete": rec, "dur": dur,
                          "registered": add_working(rec, dur), "query": False})
        for _ in range(int(n * 0.02)):
            rec = dt.date(2026, 10, 1) + dt.timedelta(days=int(rng.integers(0, 6)))
            if rec.weekday() >= 5:
                continue
            dur = int(rng.integers(1, 4))
            extra.append({"office": code, "received": rec, "complete": rec, "dur": dur,
                          "registered": add_working(rec, dur), "query": False})
    x["extra"] = [a for a in extra if dt.date(2026, 7, 1) <= a["registered"] <= EXTRACT]
    _fees(x, rng)
    return x


def summary(sub):
    """An office's medians on the truth: the product-limit median with open applications censored at their age, the
    median of the registered alone, the median counting each open one at its age, and counting each open one as
    over the line."""
    t, e, closed, at_age, late = [], [], [], [], []
    for a in sub:
        age = working_days(a["complete"], EXTRACT)
        if a["registered"] <= EXTRACT:
            t.append(a["dur"])
            e.append(True)
            closed.append(a["dur"])
            at_age.append(a["dur"])
            late.append(a["dur"])
        else:
            t.append(age)
            e.append(False)
            at_age.append(age)
            late.append(10 ** 6)
    return {"km": km_median(t, e), "closed": float(np.median(closed)), "open_age": float(np.median(at_age)),
            "open_late": float(np.median(late)), "true": float(np.median([a["dur"] for a in sub]))}


def _fees(x, rng):
    """Every card payment an office took in the quarter: the registration fee with each application on its receipt
    day (EUR 50, or EUR 100 for the two-day service) and the office's other fees (name reservations, annual return
    filings, certified copies); truth by the day paid."""
    pays = []
    days = [dt.date(2026, 6, 24) + dt.timedelta(days=k) for k in range(110)]
    for a in x["apps"]:
        pays.append({"office": a["office"], "day": a["received"], "amount": 100 if rng.random() < 0.12 else 50})
    for code, name, n, *_ in OFFICES:
        for d in days:
            if d.weekday() >= 5 or d in HOLIDAYS:
                continue
            for _ in range(int(rng.poisson(n / 65.0 * 1.6))):
                pays.append({"office": code, "day": d, "amount": int(rng.choice([20, 20, 25, 40, 60]))})
    x["pays"] = pays
    q3 = [p for p in pays if dt.date(2026, 7, 1) <= p["day"] <= dt.date(2026, 9, 30)]
    x["fees"] = {code: (sum(1 for p in q3 if p["office"] == code), sum(p["amount"] for p in q3 if p["office"] == code))
                 for code in IDS}
